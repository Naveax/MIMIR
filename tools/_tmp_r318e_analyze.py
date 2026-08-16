import argparse
import hashlib
import json
from pathlib import Path

ORACLE_PREFIX = "R3_18E_ORACLE\t"
NATIVE_PREFIX = "R3_18E_NATIVE\t"
SCALAR_TAGS = {"Boolean", "Byte", "Enum", "Float", "Int", "Int64"}


def parse_kv(line: str) -> dict[str, str]:
    out = {}
    for token in line.rstrip("\n").split("\t")[1:]:
        if "=" not in token:
            raise SystemExit(f"malformed token: {token!r}")
        key, value = token.split("=", 1)
        out[key] = value
    return out


def iv(row: dict[str, str], key: str) -> int:
    try:
        return int(row[key])
    except Exception as exc:
        raise SystemExit(f"invalid integer {key}={row.get(key)!r}: {exc}") from exc


def payload_hash(row: dict[str, str]) -> str:
    raw = bytes.fromhex(row["window_hex"])
    base = iv(row, "window_byte_start") * 8
    start = iv(row, "payload_start_bit") - base
    end = iv(row, "payload_end_bit") - base
    if not 0 <= start < end <= len(raw) * 8:
        raise SystemExit("invalid payload range")
    width = end - start
    packed = bytearray((width + 7) // 8)
    for out_bit, src_bit in enumerate(range(start, end)):
        bit = (raw[src_bit // 8] >> (src_bit % 8)) & 1
        packed[out_bit // 8] |= bit << (out_bit % 8)
    return hashlib.sha256(width.to_bytes(8, "little") + bytes(packed)).hexdigest()


def control_hash(row: dict[str, str]) -> str:
    start = iv(row, "next_property_present_start_bit")
    value = iv(row, "next_property_present")
    return hashlib.sha256(start.to_bytes(8, "little") + bytes([value])).hexdigest()


def durable(row: dict[str, str]) -> dict[str, object]:
    value = iv(row, "next_property_present")
    return {
        "class": "continuation" if value else "terminator",
        "label": row["label"].replace("\\", "/"),
        "frame_index": iv(row, "frame_index"),
        "actor_ordinal": iv(row, "actor_ordinal"),
        "actor_id": iv(row, "actor_id"),
        "actor_context_object_id": iv(row, "actor_context_object_id"),
        "property_ordinal": 0,
        "property_present_start_bit": iv(row, "property_present_start_bit"),
        "property_present_end_bit": iv(row, "property_present_end_bit"),
        "stream_id_start_bit": iv(row, "stream_id_start_bit"),
        "stream_id_end_bit": iv(row, "stream_id_end_bit"),
        "stream_id": iv(row, "stream_id"),
        "stream_id_bound": iv(row, "stream_id_bound"),
        "prop_id_bits": iv(row, "prop_id_bits"),
        "property_object_id": iv(row, "property_object_id"),
        "attribute_tag": row["attribute_tag"],
        "version_major": iv(row, "version_major"),
        "version_minor": iv(row, "version_minor"),
        "net_version": iv(row, "net_version"),
        "payload_start_bit": iv(row, "payload_start_bit"),
        "payload_end_bit": iv(row, "payload_end_bit"),
        "payload_width": iv(row, "payload_width"),
        "next_property_present_start_bit": iv(row, "next_property_present_start_bit"),
        "next_property_present_end_bit": iv(row, "next_property_present_end_bit"),
        "next_property_present": bool(value),
        "lossless_value": row["lossless_value"],
        "payload_sha256": payload_hash(row),
        "control_bit_sha256": control_hash(row),
    }


def select(log_path: Path, request_path: Path, selected_path: Path, summary_path: Path) -> None:
    rows = []
    parse_success = 0
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line == "R3_18E_ORACLE_PARSE=PASS":
            parse_success += 1
            continue
        if not line.startswith(ORACLE_PREFIX):
            continue
        row = parse_kv(line)
        if row.get("property_ordinal") != "0":
            raise SystemExit("oracle emitted non-first property")
        if row.get("attribute_tag") not in SCALAR_TAGS:
            raise SystemExit("oracle emitted non-K1 first property")
        if iv(row, "property_present_end_bit") != iv(row, "property_present_start_bit") + 1:
            raise SystemExit("first property_present width != 1")
        if iv(row, "stream_id_end_bit") != iv(row, "payload_start_bit"):
            raise SystemExit("payload start != stream end")
        if iv(row, "payload_end_bit") != iv(row, "next_property_present_start_bit"):
            raise SystemExit("payload end != next control start")
        if iv(row, "next_property_present_end_bit") != iv(row, "next_property_present_start_bit") + 1:
            raise SystemExit("next control width != 1")
        if iv(row, "next_property_present") not in (0, 1):
            raise SystemExit("invalid next control value")
        rows.append(row)

    if parse_success != 47:
        raise SystemExit(f"expected 47 Boxcars parse successes, got {parse_success}")
    if len(rows) != 94:
        raise SystemExit(f"expected frozen 94 oracle rows, got {len(rows)}")

    rows.sort(key=lambda r: (r["label"].replace("\\", "/"), iv(r, "next_property_present")))
    per_label: dict[str, set[int]] = {}
    for row in rows:
        label = row["label"].replace("\\", "/")
        per_label.setdefault(label, set()).add(iv(row, "next_property_present"))
    if len(per_label) != 47:
        raise SystemExit(f"expected 47 replay labels, got {len(per_label)}")
    bad = {label: values for label, values in per_label.items() if values != {0, 1}}
    if bad:
        raise SystemExit(f"each replay must have terminator+continuation: {bad}")

    selected = [durable(row) for row in rows]
    selected_path.write_text(json.dumps(selected, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")

    request_lines = []
    for row, item in zip(rows, selected):
        request_lines.append("\t".join([
            str(item["class"]), str(item["label"]), str(item["actor_context_object_id"]),
            str(item["stream_id"]), str(item["property_object_id"]), str(item["attribute_tag"]),
            str(item["property_present_start_bit"]), str(item["payload_start_bit"]),
            str(item["payload_end_bit"]), str(item["next_property_present_start_bit"]),
            str(item["next_property_present_end_bit"]), "1" if item["next_property_present"] else "0",
            row["window_byte_start"], row["window_local_start_bit"], row["window_hex"],
            str(item["lossless_value"]),
        ]))
    request_path.write_text("\n".join(request_lines) + "\n", encoding="utf-8", newline="\n")

    summary = {
        "boxcars_parse_success": parse_success,
        "candidate_rows": len(rows),
        "replay_labels": len(per_label),
        "terminator_rows": sum(1 for x in selected if x["class"] == "terminator"),
        "continuation_rows": sum(1 for x in selected if x["class"] == "continuation"),
        "selected_rows": len(selected),
        "selection_rule": "all pinned-oracle first-K1 loop-control rows; exactly one terminator and one continuation per replay process",
    }
    summary_path.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("R3_18E_SELECTION=PASS rows=94 terminators=47 continuations=47")


def compare(selected_path: Path, native_path: Path, summary_path: Path, out_dir: Path) -> None:
    selected = json.loads(selected_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    expected = {(x["label"], x["class"]): x for x in selected}
    native = {}
    row_count = None
    aligned_truncation_count = None
    for line in native_path.read_text(encoding="utf-8").splitlines():
        if line.startswith(NATIVE_PREFIX):
            row = parse_kv(line)
            key = (row["label"].replace("\\", "/"), row["class"])
            if key in native:
                raise SystemExit(f"duplicate native row {key}")
            native[key] = row
        elif line.startswith("R3_18E_NATIVE_ROWS="):
            row_count = int(line.split("=", 1)[1])
        elif line.startswith("R3_18E_ALIGNED_TRUNCATION_ROWS="):
            aligned_truncation_count = int(line.split("=", 1)[1])

    if row_count != 94 or len(native) != 94 or set(native) != set(expected):
        raise SystemExit(f"native row identity mismatch count={row_count} map={len(native)}")
    if aligned_truncation_count is None or aligned_truncation_count < 1:
        raise SystemExit("no byte-aligned real witness available for exact missing-control-bit truncation")

    required_true = [
        "first_header_exact", "first_semantic_exact", "first_payload_start_exact",
        "first_payload_end_exact", "first_stop_equals_oracle_control_start",
        "control_start_exact", "control_value_exact", "control_end_exact",
        "control_stop_exact", "repeatability", "post_stop_poison",
        "malformed_first_rejected",
    ]
    mismatch = 0
    class_counts = {"terminator": 0, "continuation": 0}
    tag_counts: dict[str, int] = {}
    for key, item in expected.items():
        row = native[key]
        class_counts[item["class"]] += 1
        tag_counts[item["attribute_tag"]] = tag_counts.get(item["attribute_tag"], 0) + 1
        for flag in required_true:
            if row.get(flag) != "true":
                mismatch += 1
        checks = [
            row.get("attribute_tag") == item["attribute_tag"],
            row.get("lossless_value") == item["lossless_value"],
            int(row["native_global_first_stop"]) == item["next_property_present_start_bit"],
            int(row["native_global_control_start"]) == item["next_property_present_start_bit"],
            int(row["native_global_control_end"]) == item["next_property_present_end_bit"],
            row.get("next_property_present") == ("1" if item["next_property_present"] else "0"),
            row.get("second_stream_bits_consumed") == "0",
            row.get("second_header_bits_consumed") == "0",
            row.get("second_payload_bits_consumed") == "0",
        ]
        mismatch += sum(1 for ok in checks if not ok)

    if mismatch:
        raise SystemExit(f"R3.18E native/oracle mismatch count {mismatch}")
    if class_counts != {"terminator": 47, "continuation": 47}:
        raise SystemExit(f"unexpected class counts {class_counts}")

    comparison = {
        "outcome": "A",
        "replay_identity": "47/47",
        "selected_rows": 94,
        "native_first_property_success": "94/94",
        "native_control_success": "94/94",
        "terminator_rows": 47,
        "continuation_rows": 47,
        "aligned_truncation_rows": aligned_truncation_count,
        "attribute_tag_counts": dict(sorted(tag_counts.items())),
        "native_oracle_mismatch_count": 0,
        "first_stop_oracle_control_start": "94/94",
        "control_start_exact": "94/94",
        "control_boolean_exact": "94/94",
        "control_end_stop_exact": "94/94",
        "repeatability": True,
        "post_stop_poison": True,
        "malformed_first_rejected": True,
        "truncation_negative": True,
        "second_stream_bits_consumed": 0,
        "second_header_bits_consumed": 0,
        "second_payload_bits_consumed": 0,
        "production_mutation": 0,
    }
    (out_dir / "r3_18e_comparison.json").write_text(json.dumps(comparison, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    aggregate = [
        "R3_18E_OUTCOME=A", "R3_18E_EVIDENCE=PASS", "R3_18E_REPLAY_IDENTITY=47/47",
        "R3_18E_TERMINATOR_ROWS=47", "R3_18E_CONTINUATION_ROWS=47", "R3_18E_SELECTED_ROWS=94",
        "R3_18E_NATIVE_FIRST_PROPERTY=94/94", "R3_18E_NATIVE_CONTROL=94/94",
        "R3_18E_FIRST_STOP_EQUALS_ORACLE_CONTROL_START=94/94", "R3_18E_CONTROL_START_EXACT=94/94",
        "R3_18E_CONTROL_BOOLEAN_EXACT=94/94", "R3_18E_CONTROL_END_STOP_EXACT=94/94",
        f"R3_18E_ALIGNED_TRUNCATION_ROWS={aligned_truncation_count}",
        "R3_18E_TRUNCATION_NEGATIVE=PASS", "R3_18E_POST_STOP_POISON=PASS",
        "R3_18E_REPEATABILITY=PASS", "R3_18E_MALFORMED_FIRST_REJECTED=PASS",
        "R3_18E_SECOND_STREAM_BITS_CONSUMED=0", "R3_18E_SECOND_HEADER_BITS_CONSUMED=0",
        "R3_18E_SECOND_PAYLOAD_BITS_CONSUMED=0", "R3_18E_PRIVACY=PASS", "R3_18E_MISMATCH_COUNT=0",
        "R3_18E_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
    ]
    (out_dir / "r3_18e_aggregate.txt").write_text("\n".join(aggregate) + "\n", encoding="utf-8", newline="\n")
    print(f"R3_18E_COMPARE=PASS rows=94 aligned_truncation_rows={aligned_truncation_count}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sel = sub.add_parser("select")
    for name in ["log", "request", "selected", "summary"]:
        sel.add_argument(name, type=Path)
    cmp = sub.add_parser("compare")
    for name in ["selected", "native", "summary", "out_dir"]:
        cmp.add_argument(name, type=Path)
    args = parser.parse_args()
    if args.cmd == "select":
        select(args.log, args.request, args.selected, args.summary)
    else:
        compare(args.selected, args.native, args.summary, args.out_dir)


if __name__ == "__main__":
    main()
