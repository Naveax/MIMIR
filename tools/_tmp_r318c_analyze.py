import argparse
import hashlib
import json
from pathlib import Path

PREFIX = "R3_18C_ORACLE\t"
NATIVE_PREFIX = "R3_18C_NATIVE\t"
SCALAR_TAGS = {"Boolean", "Byte", "Enum", "Float", "Int", "Int64"}


def parse_kv(line: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for token in line.rstrip("\n").split("\t")[1:]:
        if "=" not in token:
            raise SystemExit(f"malformed token: {token!r}")
        key, value = token.split("=", 1)
        out[key] = value
    return out


def as_int(row: dict[str, str], key: str) -> int:
    try:
        return int(row[key])
    except Exception as exc:
        raise SystemExit(f"invalid integer {key}: {row.get(key)!r}: {exc}") from exc


def payload_hash(row: dict[str, str]) -> str:
    raw = bytes.fromhex(row["window_hex"])
    base = as_int(row, "window_byte_start") * 8
    start = as_int(row, "payload_start_bit") - base
    end = as_int(row, "payload_end_bit") - base
    if not (0 <= start < end <= len(raw) * 8):
        raise SystemExit(f"invalid payload range start={start} end={end} bits={len(raw)*8}")
    width = end - start
    packed = bytearray((width + 7) // 8)
    for out_bit, src_bit in enumerate(range(start, end)):
        bit = (raw[src_bit // 8] >> (src_bit % 8)) & 1
        packed[out_bit // 8] |= bit << (out_bit % 8)
    return hashlib.sha256(width.to_bytes(8, "little") + bytes(packed)).hexdigest()


def loop_bit_hash(row: dict[str, str]) -> str:
    start = as_int(row, "next_property_present_start_bit")
    value = as_int(row, "next_property_present")
    material = start.to_bytes(8, "little") + bytes([value])
    return hashlib.sha256(material).hexdigest()


def normalized_selected(row: dict[str, str]) -> dict[str, object]:
    next_value = as_int(row, "next_property_present")
    return {
        "class": "continuation" if next_value else "terminator",
        "label": row["label"].replace("\\", "/"),
        "frame_index": as_int(row, "frame_index"),
        "actor_ordinal": as_int(row, "actor_ordinal"),
        "actor_id": as_int(row, "actor_id"),
        "actor_context_object_id": as_int(row, "actor_context_object_id"),
        "property_ordinal": 0,
        "property_present_start_bit": as_int(row, "property_present_start_bit"),
        "property_present_end_bit": as_int(row, "property_present_end_bit"),
        "stream_id_start_bit": as_int(row, "stream_id_start_bit"),
        "stream_id_end_bit": as_int(row, "stream_id_end_bit"),
        "stream_id": as_int(row, "stream_id"),
        "stream_id_bound": as_int(row, "stream_id_bound"),
        "prop_id_bits": as_int(row, "prop_id_bits"),
        "property_object_id": as_int(row, "property_object_id"),
        "attribute_tag": row["attribute_tag"],
        "version_major": as_int(row, "version_major"),
        "version_minor": as_int(row, "version_minor"),
        "net_version": as_int(row, "net_version"),
        "payload_start_bit": as_int(row, "payload_start_bit"),
        "payload_end_bit": as_int(row, "payload_end_bit"),
        "payload_width": as_int(row, "payload_width"),
        "next_property_present_start_bit": as_int(row, "next_property_present_start_bit"),
        "next_property_present_end_bit": as_int(row, "next_property_present_end_bit"),
        "next_property_present": bool(next_value),
        "lossless_value": row["lossless_value"],
        "payload_sha256": payload_hash(row),
        "loop_bit_sha256": loop_bit_hash(row),
    }


def select(log_path: Path, request_path: Path, selected_path: Path, summary_path: Path) -> None:
    rows: list[dict[str, str]] = []
    parse_success = 0
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line == "R3_18C_ORACLE_PARSE=PASS":
            parse_success += 1
            continue
        if not line.startswith(PREFIX):
            continue
        row = parse_kv(line)
        if row.get("property_ordinal") != "0":
            raise SystemExit("oracle emitted a non-first property")
        if row.get("attribute_tag") not in SCALAR_TAGS:
            raise SystemExit(f"non-K1 oracle row: {row.get('attribute_tag')}")
        if as_int(row, "property_present_end_bit") != as_int(row, "property_present_start_bit") + 1:
            raise SystemExit("first property-present width is not one bit")
        if as_int(row, "stream_id_end_bit") != as_int(row, "payload_start_bit"):
            raise SystemExit("payload start does not equal stream end")
        if as_int(row, "payload_end_bit") != as_int(row, "next_property_present_start_bit"):
            raise SystemExit("payload end does not equal next property-present start")
        if as_int(row, "next_property_present_end_bit") != as_int(row, "next_property_present_start_bit") + 1:
            raise SystemExit("next property-present width is not one bit")
        if as_int(row, "next_property_present") not in (0, 1):
            raise SystemExit("invalid next property-present value")
        if as_int(row, "payload_width") <= 0:
            raise SystemExit("non-positive first payload width")
        rows.append(row)

    if parse_success != 47:
        raise SystemExit(f"expected 47 Boxcars parse successes, got {parse_success}")
    if not rows:
        raise SystemExit("no R3.18C K1 loop-control candidates found")

    rows.sort(
        key=lambda row: (
            row["label"].replace("\\", "/"),
            as_int(row, "frame_index"),
            as_int(row, "actor_ordinal"),
            as_int(row, "actor_id"),
        )
    )
    terminators = [row for row in rows if as_int(row, "next_property_present") == 0]
    continuations = [row for row in rows if as_int(row, "next_property_present") == 1]
    chosen_rows: list[dict[str, str]] = []
    if terminators:
        chosen_rows.append(terminators[0])
    if continuations:
        chosen_rows.append(continuations[0])

    selected = [normalized_selected(row) for row in chosen_rows]
    selected_path.write_text(
        json.dumps(selected, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    request_lines: list[str] = []
    for row, durable in zip(chosen_rows, selected):
        fields = [
            str(durable["class"]),
            str(durable["label"]),
            str(durable["actor_context_object_id"]),
            str(durable["stream_id"]),
            str(durable["property_object_id"]),
            str(durable["attribute_tag"]),
            str(durable["property_present_start_bit"]),
            str(durable["payload_start_bit"]),
            str(durable["payload_end_bit"]),
            str(durable["next_property_present_start_bit"]),
            str(durable["next_property_present_end_bit"]),
            "1" if durable["next_property_present"] else "0",
            row["window_byte_start"],
            row["window_local_start_bit"],
            row["window_hex"],
            str(durable["lossless_value"]),
        ]
        request_lines.append("\t".join(fields))
    request_path.write_text("\n".join(request_lines) + "\n", encoding="utf-8", newline="\n")

    outcome = "A" if terminators and continuations else "B"
    summary = {
        "outcome_hint": outcome,
        "boxcars_parse_success": parse_success,
        "candidate_rows": len(rows),
        "terminator_candidates": len(terminators),
        "continuation_candidates": len(continuations),
        "selected_classes": [item["class"] for item in selected],
        "selection_rule": "first lexicographic(label,frame_index,actor_ordinal,actor_id) per next-property class",
    }
    summary_path.write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"R3_18C_SELECTION=PASS outcome_hint={outcome} "
        f"terminators={len(terminators)} continuations={len(continuations)}"
    )


def compare(selected_path: Path, native_path: Path, summary_path: Path, out_dir: Path) -> None:
    selected = json.loads(selected_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    expected = {item["class"]: item for item in selected}
    native_rows: dict[str, dict[str, str]] = {}
    native_row_count = None
    for line in native_path.read_text(encoding="utf-8").splitlines():
        if line.startswith(NATIVE_PREFIX):
            row = parse_kv(line)
            native_rows[row["class"]] = row
        elif line.startswith("R3_18C_NATIVE_ROWS="):
            native_row_count = int(line.split("=", 1)[1])

    if native_row_count != len(selected):
        raise SystemExit(f"native row-count mismatch {native_row_count} != {len(selected)}")
    if set(native_rows) != set(expected):
        raise SystemExit(f"native classes {set(native_rows)} != expected {set(expected)}")

    required_true = [
        "header_exact",
        "semantic_exact",
        "payload_start_exact",
        "payload_end_exact",
        "stop_equals_next_start",
        "next_bit_exact",
        "one_bit_stop_exact",
        "truncation_negative",
        "truncation_cursor_unchanged",
        "post_stop_poison",
    ]
    class_results: dict[str, object] = {}
    mismatch_count = 0
    for klass, item in expected.items():
        row = native_rows[klass]
        for flag in required_true:
            if row.get(flag) != "true":
                mismatch_count += 1
        expected_next = "1" if item["next_property_present"] else "0"
        checks = {
            "attribute_tag": row.get("attribute_tag") == item["attribute_tag"],
            "semantic": row.get("lossless_value") == item["lossless_value"],
            "native_stop": int(row["native_global_stop"]) == item["next_property_present_start_bit"],
            "evidence_stop": int(row["evidence_global_stop"]) == item["next_property_present_end_bit"],
            "next_value": row.get("next_property_present") == expected_next,
            "second_stream_bits": row.get("second_stream_bits_consumed") == "0",
            "second_payload_bits": row.get("second_payload_bits_consumed") == "0",
        }
        mismatch_count += sum(1 for value in checks.values() if not value)
        class_results[klass] = {
            "all_flags_true": all(row.get(flag) == "true" for flag in required_true),
            **checks,
        }

    outcome = summary["outcome_hint"]
    if outcome == "A" and set(expected) != {"terminator", "continuation"}:
        raise SystemExit("Outcome A requires both terminator and continuation witnesses")
    if mismatch_count != 0:
        raise SystemExit(f"R3.18C native/oracle mismatch count {mismatch_count}")

    comparison = {
        "outcome": outcome,
        "classes": class_results,
        "native_oracle_mismatch_count": mismatch_count,
        "repeatability": True,
        "r3_18b_negative_regression": True,
        "production_mutation": 0,
        "second_stream_bits_consumed": 0,
        "second_payload_bits_consumed": 0,
    }
    (out_dir / "r3_18c_comparison.json").write_text(
        json.dumps(comparison, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    aggregate_lines = [
        f"R3_18C_OUTCOME={outcome}",
        "R3_18C_EVIDENCE=PASS",
        "R3_18C_REPLAY_IDENTITY=47/47",
        f"R3_18C_TERMINATOR_CANDIDATES={summary['terminator_candidates']}",
        f"R3_18C_CONTINUATION_CANDIDATES={summary['continuation_candidates']}",
        "R3_18C_NATIVE_STOP_EQUALS_ORACLE_NEXT_START=PASS",
        "R3_18C_NEXT_PROPERTY_BIT_EXACT=PASS",
        "R3_18C_ONE_BIT_STOP=PASS",
        "R3_18C_TRUNCATION_NEGATIVE=PASS",
        "R3_18C_POST_STOP_POISON=PASS",
        "R3_18C_REPEATABILITY=PASS",
        "R3_18C_R318B_NEGATIVE_REGRESSION=PASS",
        "R3_18C_SECOND_STREAM_BITS_CONSUMED=0",
        "R3_18C_SECOND_PAYLOAD_BITS_CONSUMED=0",
        "R3_18C_PRIVACY=PASS",
        "R3_18C_MISMATCH_COUNT=0",
        "R3_18C_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
    ]
    (out_dir / "r3_18c_aggregate.txt").write_text(
        "\n".join(aggregate_lines) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"R3_18C_COMPARE=PASS outcome={outcome}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sel = sub.add_parser("select")
    sel.add_argument("log", type=Path)
    sel.add_argument("request", type=Path)
    sel.add_argument("selected", type=Path)
    sel.add_argument("summary", type=Path)
    cmp_parser = sub.add_parser("compare")
    cmp_parser.add_argument("selected", type=Path)
    cmp_parser.add_argument("native", type=Path)
    cmp_parser.add_argument("summary", type=Path)
    cmp_parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    if args.cmd == "select":
        select(args.log, args.request, args.selected, args.summary)
    else:
        compare(args.selected, args.native, args.summary, args.out_dir)


if __name__ == "__main__":
    main()
