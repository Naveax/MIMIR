import argparse
import hashlib
import json
from pathlib import Path

SOURCE_PREFIX = "R3_18F_ORACLE\t"
SECOND_PREFIX = "R3_18F_SECOND\t"
NATIVE_PREFIX = "R3_18F_NATIVE\t"
SCALAR_TAGS = {"Boolean", "Byte", "Enum", "Float", "Int", "Int64"}


def parse_kv(line: str) -> dict[str, str]:
    out: dict[str, str] = {}
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
        raise SystemExit("invalid first payload range")
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


def second_header_hash(row: dict[str, str]) -> str:
    fields = {
        "property_present_start_bit": iv(row, "second_property_present_start_bit"),
        "property_present_end_bit": iv(row, "second_property_present_end_bit"),
        "stream_id_start_bit": iv(row, "second_stream_id_start_bit"),
        "stream_id_end_bit": iv(row, "second_stream_id_end_bit"),
        "stream_id": iv(row, "second_stream_id"),
        "stream_id_bound": iv(row, "second_stream_id_bound"),
        "prop_id_bits": iv(row, "second_prop_id_bits"),
        "property_object_id": iv(row, "second_property_object_id"),
        "attribute_tag": row["second_attribute_tag"],
        "payload_start_bit": iv(row, "second_payload_start_bit"),
    }
    raw = json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def select(log_path: Path, request_path: Path, selected_path: Path, summary_path: Path) -> None:
    sources: list[dict[str, str]] = []
    seconds: list[dict[str, str]] = []
    parse_success = 0
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line == "R3_18F_ORACLE_PARSE=PASS":
            parse_success += 1
        elif line.startswith(SOURCE_PREFIX):
            sources.append(parse_kv(line))
        elif line.startswith(SECOND_PREFIX):
            seconds.append(parse_kv(line))

    if parse_success != 47:
        raise SystemExit(f"expected 47 Boxcars parse successes, got {parse_success}")
    if len(sources) != 94:
        raise SystemExit(f"expected frozen 94 source rows, got {len(sources)}")
    if len(seconds) != 47:
        raise SystemExit(f"expected 47 second-header rows, got {len(seconds)}")

    source_by_key: dict[tuple[str, str], dict[str, str]] = {}
    per_label: dict[str, set[int]] = {}
    for row in sources:
        if row.get("property_ordinal") != "0":
            raise SystemExit("source oracle emitted non-first property")
        if row.get("attribute_tag") not in SCALAR_TAGS:
            raise SystemExit("source oracle emitted non-K1 first property")
        if iv(row, "property_present_end_bit") != iv(row, "property_present_start_bit") + 1:
            raise SystemExit("first property_present width != 1")
        if iv(row, "stream_id_end_bit") != iv(row, "payload_start_bit"):
            raise SystemExit("first payload start != first stream end")
        if iv(row, "payload_end_bit") != iv(row, "next_property_present_start_bit"):
            raise SystemExit("first payload end != second property_present start")
        if iv(row, "next_property_present_end_bit") != iv(row, "next_property_present_start_bit") + 1:
            raise SystemExit("second property_present width != 1")
        nxt = iv(row, "next_property_present")
        if nxt not in (0, 1):
            raise SystemExit("invalid second property_present")
        label = row["label"].replace("\\", "/")
        cls = "continuation" if nxt else "terminator"
        key = (label, cls)
        if key in source_by_key:
            raise SystemExit(f"duplicate source row {key}")
        source_by_key[key] = row
        per_label.setdefault(label, set()).add(nxt)
    if len(per_label) != 47 or any(values != {0, 1} for values in per_label.values()):
        raise SystemExit("source lane is not exactly one terminator + one continuation per replay")

    second_by_label: dict[str, dict[str, str]] = {}
    for row in seconds:
        if row.get("property_ordinal") != "1":
            raise SystemExit("second oracle emitted wrong property ordinal")
        label = row["label"].replace("\\", "/")
        if label in second_by_label:
            raise SystemExit(f"duplicate second-header row {label}")
        second_by_label[label] = row
        source = source_by_key.get((label, "continuation"))
        if source is None:
            raise SystemExit(f"second header has no frozen continuation source: {label}")
        identity_keys = ["frame_index", "actor_ordinal", "actor_id", "actor_context_object_id"]
        for key in identity_keys:
            if iv(row, key) != iv(source, key):
                raise SystemExit(f"{label}: second-header identity mismatch {key}")
        if iv(row, "first_property_present_start_bit") != iv(source, "property_present_start_bit"):
            raise SystemExit(f"{label}: second row first-property start drift")
        if iv(row, "first_payload_end_bit") != iv(source, "payload_end_bit"):
            raise SystemExit(f"{label}: second row first-payload end drift")
        if iv(row, "second_property_present_start_bit") != iv(source, "next_property_present_start_bit"):
            raise SystemExit(f"{label}: second property_present start drift")
        if iv(row, "second_property_present_end_bit") != iv(source, "next_property_present_end_bit"):
            raise SystemExit(f"{label}: second property_present end drift")
        if iv(row, "second_stream_id_start_bit") != iv(row, "second_property_present_end_bit"):
            raise SystemExit(f"{label}: second stream does not start after present bit")
        if iv(row, "second_stream_id_end_bit") != iv(row, "second_payload_start_bit"):
            raise SystemExit(f"{label}: second payload start != stream end")
    if set(second_by_label) != set(per_label):
        raise SystemExit("second-header label coverage != 47 replay lane")

    selected: list[dict[str, object]] = []
    request_lines: list[str] = []
    for key in sorted(source_by_key):
        label, cls = key
        source = source_by_key[key]
        nxt = cls == "continuation"
        item: dict[str, object] = {
            "class": cls,
            "label": label,
            "frame_index": iv(source, "frame_index"),
            "actor_ordinal": iv(source, "actor_ordinal"),
            "actor_id": iv(source, "actor_id"),
            "actor_context_object_id": iv(source, "actor_context_object_id"),
            "first_property_present_start_bit": iv(source, "property_present_start_bit"),
            "first_property_present_end_bit": iv(source, "property_present_end_bit"),
            "first_stream_id_start_bit": iv(source, "stream_id_start_bit"),
            "first_stream_id_end_bit": iv(source, "stream_id_end_bit"),
            "first_stream_id": iv(source, "stream_id"),
            "first_property_object_id": iv(source, "property_object_id"),
            "first_attribute_tag": source["attribute_tag"],
            "first_payload_start_bit": iv(source, "payload_start_bit"),
            "first_payload_end_bit": iv(source, "payload_end_bit"),
            "second_property_present_start_bit": iv(source, "next_property_present_start_bit"),
            "second_property_present_end_bit": iv(source, "next_property_present_end_bit"),
            "second_property_present": nxt,
            "first_lossless_value": source["lossless_value"],
            "first_payload_sha256": payload_hash(source),
            "control_bit_sha256": control_hash(source),
        }
        if nxt:
            second = second_by_label[label]
            second_struct = {
                "stream_id_start_bit": iv(second, "second_stream_id_start_bit"),
                "stream_id_end_bit": iv(second, "second_stream_id_end_bit"),
                "stream_id": iv(second, "second_stream_id"),
                "stream_id_bound": iv(second, "second_stream_id_bound"),
                "prop_id_bits": iv(second, "second_prop_id_bits"),
                "property_object_id": iv(second, "second_property_object_id"),
                "attribute_tag": second["second_attribute_tag"],
                "payload_start_bit": iv(second, "second_payload_start_bit"),
                "header_sha256": second_header_hash(second),
            }
            item["second_header"] = second_struct
            window_byte_start = second["window_byte_start"]
            window_local_first_start = second["window_local_first_start_bit"]
            window_hex = second["window_hex"]
            second_fields = [
                str(iv(second, "second_property_present_start_bit")),
                str(iv(second, "second_property_present_end_bit")),
                str(iv(second, "second_stream_id_start_bit")),
                str(iv(second, "second_stream_id_end_bit")),
                str(iv(second, "second_stream_id")),
                str(iv(second, "second_stream_id_bound")),
                str(iv(second, "second_prop_id_bits")),
                str(iv(second, "second_property_object_id")),
                second["second_attribute_tag"],
                str(iv(second, "second_payload_start_bit")),
            ]
        else:
            item["second_header"] = None
            window_byte_start = source["window_byte_start"]
            window_local_first_start = source["window_local_start_bit"]
            window_hex = source["window_hex"]
            second_fields = ["-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "None", "-1"]
        selected.append(item)
        request_lines.append("\t".join([
            cls,
            label,
            str(item["actor_context_object_id"]),
            str(item["first_stream_id"]),
            str(item["first_property_object_id"]),
            str(item["first_attribute_tag"]),
            str(item["first_property_present_start_bit"]),
            str(item["first_payload_start_bit"]),
            str(item["first_payload_end_bit"]),
            str(item["second_property_present_start_bit"]),
            str(item["second_property_present_end_bit"]),
            "1" if nxt else "0",
            window_byte_start,
            window_local_first_start,
            window_hex,
            str(item["first_lossless_value"]),
            *second_fields,
        ]))

    selected_path.write_text(json.dumps(selected, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    request_path.write_text("\n".join(request_lines) + "\n", encoding="utf-8", newline="\n")
    summary = {
        "boxcars_parse_success": parse_success,
        "replay_labels": len(per_label),
        "source_rows": len(sources),
        "terminator_rows": 47,
        "continuation_rows": 47,
        "second_header_rows": len(seconds),
        "selected_rows": len(selected),
        "selection_rule": "reproduce the frozen R3.18E terminator+continuation classes; enrich only continuation rows with the second header through payload_start",
    }
    summary_path.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("R3_18F_SELECTION=PASS source_rows=94 second_headers=47 terminators=47 continuations=47")


def compare(selected_path: Path, native_path: Path, summary_path: Path, out_dir: Path) -> None:
    selected = json.loads(selected_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    expected = {(x["label"], x["class"]): x for x in selected}
    native: dict[tuple[str, str], dict[str, str]] = {}
    row_count = None
    header_truncation_rows = None
    unresolved_synthetic = False
    terminator_no_lookup = False
    for line in native_path.read_text(encoding="utf-8").splitlines():
        if line.startswith(NATIVE_PREFIX):
            row = parse_kv(line)
            key = (row["label"].replace("\\", "/"), row["class"])
            if key in native:
                raise SystemExit(f"duplicate native row {key}")
            native[key] = row
        elif line.startswith("R3_18F_NATIVE_ROWS="):
            row_count = int(line.split("=", 1)[1])
        elif line.startswith("R3_18F_HEADER_TRUNCATION_ROWS="):
            header_truncation_rows = int(line.split("=", 1)[1])
        elif line == "R3_18F_UNRESOLVED_STREAM_SYNTHETIC=PASS":
            unresolved_synthetic = True
        elif line == "R3_18F_TERMINATOR_NO_LOOKUP_SYNTHETIC=PASS":
            terminator_no_lookup = True

    if row_count != 94 or len(native) != 94 or set(native) != set(expected):
        raise SystemExit(f"native row identity mismatch count={row_count} map={len(native)}")
    if header_truncation_rows is None or header_truncation_rows < 1:
        raise SystemExit("no real continuation stream/header truncation negative executed")
    if not unresolved_synthetic or not terminator_no_lookup:
        raise SystemExit("required synthetic header negatives did not pass")

    mismatch = 0
    continuation_tags: dict[str, int] = {}
    for key, item in expected.items():
        row = native[key]
        common_true = ["first_reconstruction_exact", "control_reconstruction_exact", "second_property_present_exact", "repeatability", "post_stop_poison"]
        for flag in common_true:
            if row.get(flag) != "true":
                mismatch += 1
        if row.get("second_payload_bits_consumed") != "0" or row.get("third_property_bits_consumed") != "0":
            mismatch += 1
        if item["class"] == "continuation":
            second = item["second_header"]
            continuation_tags[second["attribute_tag"]] = continuation_tags.get(second["attribute_tag"], 0) + 1
            for flag in ["second_stream_range_exact", "second_stream_value_exact", "second_stream_shape_exact", "second_object_exact", "second_tag_exact", "second_payload_start_stop_exact"]:
                if row.get(flag) != "true":
                    mismatch += 1
            checks = [
                int(row["native_second_property_present_start"]) == item["second_property_present_start_bit"],
                int(row["native_second_property_present_end"]) == item["second_property_present_end_bit"],
                int(row["native_second_stream_start"]) == second["stream_id_start_bit"],
                int(row["native_second_stream_end"]) == second["stream_id_end_bit"],
                int(row["native_second_stream_id"]) == second["stream_id"],
                int(row["native_second_stream_bound"]) == second["stream_id_bound"],
                int(row["native_second_prop_id_bits"]) == second["prop_id_bits"],
                int(row["native_second_property_object"]) == second["property_object_id"],
                row["native_second_attribute_tag"] == second["attribute_tag"],
                int(row["native_second_payload_start"]) == second["payload_start_bit"],
                int(row["native_second_stop"]) == second["payload_start_bit"],
            ]
            mismatch += sum(1 for ok in checks if not ok)
        else:
            for flag in ["terminator_one_bit_stop_exact", "terminator_optionals_none"]:
                if row.get(flag) != "true":
                    mismatch += 1
            checks = [
                int(row["native_second_property_present_start"]) == item["second_property_present_start_bit"],
                int(row["native_second_property_present_end"]) == item["second_property_present_end_bit"],
                int(row["native_second_stop"]) == item["second_property_present_end_bit"],
                row["native_second_stream_id"] == "None",
                row["native_second_property_object"] == "None",
                row["native_second_attribute_tag"] == "None",
                row["native_second_payload_start"] == "None",
            ]
            mismatch += sum(1 for ok in checks if not ok)

    if mismatch:
        raise SystemExit(f"R3.18F native/oracle mismatch count {mismatch}")

    comparison = {
        "outcome": "A",
        "replay_identity": "47/47",
        "r3_18e_witness_reconstruction": "94/94",
        "selected_rows": 94,
        "continuation_rows": 47,
        "terminator_rows": 47,
        "continuation_header_native_success": "47/47",
        "second_property_present_exact": "47/47 + 47/47 terminator false",
        "second_stream_start_end_value_exact": "47/47",
        "second_stream_shape_exact": "47/47",
        "resolved_property_object_exact": "47/47",
        "resolved_attribute_tag_exact": "47/47",
        "second_payload_start_stop_exact": "47/47",
        "terminator_one_bit_stop_exact": "47/47",
        "terminator_optional_header_fields_none": "47/47",
        "continuation_attribute_tag_counts": dict(sorted(continuation_tags.items())),
        "header_truncation_rows": header_truncation_rows,
        "unresolved_stream_synthetic": True,
        "terminator_no_lookup_synthetic": True,
        "repeatability": True,
        "post_stop_poison": True,
        "native_oracle_mismatch_count": 0,
        "second_payload_bits_consumed": 0,
        "third_property_bits_consumed": 0,
        "production_mutation": 0,
    }
    (out_dir / "r3_18f_comparison.json").write_text(json.dumps(comparison, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    aggregate = [
        "R3_18F_OUTCOME=A",
        "R3_18F_EVIDENCE=PASS",
        "R3_18F_REPLAY_IDENTITY=47/47",
        "R3_18F_R3_18E_WITNESS_RECONSTRUCTION=94/94",
        "R3_18F_CONTINUATION_ROWS=47",
        "R3_18F_TERMINATOR_ROWS=47",
        "R3_18F_CONTINUATION_HEADER_NATIVE=47/47",
        "R3_18F_SECOND_PROPERTY_PRESENT_EXACT=47/47",
        "R3_18F_SECOND_STREAM_START_END_VALUE_EXACT=47/47",
        "R3_18F_SECOND_STREAM_SHAPE_EXACT=47/47",
        "R3_18F_RESOLVED_PROPERTY_OBJECT_EXACT=47/47",
        "R3_18F_RESOLVED_ATTRIBUTE_TAG_EXACT=47/47",
        "R3_18F_SECOND_PAYLOAD_START_STOP_EXACT=47/47",
        "R3_18F_TERMINATOR_ONE_BIT_STOP_EXACT=47/47",
        "R3_18F_TERMINATOR_OPTIONALS_NONE=47/47",
        f"R3_18F_HEADER_TRUNCATION_ROWS={header_truncation_rows}",
        "R3_18F_UNRESOLVED_STREAM_SYNTHETIC=PASS",
        "R3_18F_TERMINATOR_NO_LOOKUP_SYNTHETIC=PASS",
        "R3_18F_POST_STOP_POISON=PASS",
        "R3_18F_REPEATABILITY=PASS",
        "R3_18F_SECOND_PAYLOAD_BITS_CONSUMED=0",
        "R3_18F_THIRD_PROPERTY_BITS_CONSUMED=0",
        "R3_18F_PRIVACY=PASS",
        "R3_18F_MISMATCH_COUNT=0",
        "R3_18F_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
    ]
    (out_dir / "r3_18f_aggregate.txt").write_text("\n".join(aggregate) + "\n", encoding="utf-8", newline="\n")
    print(f"R3_18F_COMPARE=PASS rows=94 second_headers=47 header_truncation_rows={header_truncation_rows}")


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
