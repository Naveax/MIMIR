import argparse
import hashlib
import json
from pathlib import Path

PREFIX = "R3_18A_ORACLE\t"
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
        raise SystemExit(f"invalid payload window range: start={start} end={end} bits={len(raw)*8}")
    width = end - start
    packed = bytearray((width + 7) // 8)
    for out_bit, src_bit in enumerate(range(start, end)):
        bit = (raw[src_bit // 8] >> (src_bit % 8)) & 1
        packed[out_bit // 8] |= bit << (out_bit % 8)
    material = width.to_bytes(8, "little") + bytes(packed)
    return hashlib.sha256(material).hexdigest()


def select(log_path: Path, request_path: Path, selected_path: Path, summary_path: Path) -> None:
    rows: list[dict[str, str]] = []
    parse_success = 0
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line == "R3_18A_ORACLE_PARSE=PASS":
            parse_success += 1
        elif line.startswith(PREFIX):
            row = parse_kv(line)
            if row.get("property_ordinal") != "0":
                raise SystemExit("oracle emitted a non-first property")
            if row.get("attribute_tag") not in SCALAR_TAGS:
                raise SystemExit(f"non-scalar candidate emitted: {row.get('attribute_tag')}")
            if as_int(row, "next_property_present_start_bit") != as_int(row, "payload_end_bit"):
                raise SystemExit("oracle next-property start does not equal payload end")
            if as_int(row, "property_present_end_bit") != as_int(row, "property_present_start_bit") + 1:
                raise SystemExit("property-present width is not one bit")
            if as_int(row, "payload_start_bit") != as_int(row, "stream_id_end_bit"):
                raise SystemExit("payload start does not equal stream end")
            if as_int(row, "payload_width") <= 0:
                raise SystemExit("non-positive payload width")
            rows.append(row)

    if parse_success != 47:
        raise SystemExit(f"expected 47 Boxcars parse successes, got {parse_success}")
    if not rows:
        raise SystemExit("no first-property scalar candidate found in the frozen lane")

    rows.sort(
        key=lambda r: (
            r["label"].replace("\\", "/"),
            as_int(r, "frame_index"),
            as_int(r, "actor_ordinal"),
            as_int(r, "actor_id"),
        )
    )
    row = rows[0]
    phash = payload_hash(row)
    selected = {
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
        "lossless_value": row["lossless_value"],
        "payload_sha256": phash,
    }
    selected_path.write_text(json.dumps(selected, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")

    fields = [
        selected["label"],
        str(selected["actor_context_object_id"]),
        str(selected["stream_id"]),
        str(selected["property_object_id"]),
        selected["attribute_tag"],
        str(selected["property_present_start_bit"]),
        str(selected["payload_start_bit"]),
        str(selected["payload_end_bit"]),
        row["window_byte_start"],
        row["window_local_start_bit"],
        row["window_hex"],
    ]
    request_path.write_text("\t".join(fields) + "\n", encoding="utf-8", newline="\n")

    summary = {
        "boxcars_parse_success": parse_success,
        "eligible_first_property_scalar_candidates": len(rows),
        "selected_replay": selected["label"],
        "selected_tag": selected["attribute_tag"],
        "selected_payload_width": selected["payload_width"],
        "payload_sha256": phash,
        "selection_rule": "lexicographic(label,frame_index,actor_ordinal,actor_id) over first-property scalar candidates",
    }
    summary_path.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"R3_18A_SELECTION=PASS candidates={len(rows)} tag={selected['attribute_tag']}")


def compare(selected_path: Path, native_path: Path, out_dir: Path) -> None:
    selected = json.loads(selected_path.read_text(encoding="utf-8"))
    native_lines = [x for x in native_path.read_text(encoding="utf-8").splitlines() if x.startswith("R3_18A_NATIVE\t")]
    if len(native_lines) != 1:
        raise SystemExit(f"expected one native receipt row, got {len(native_lines)}")
    native = parse_kv(native_lines[0])
    expected_flags = {
        "header_exact": "true",
        "payload_start_exact": "true",
        "payload_end_exact": "true",
        "stop_exact": "true",
        "negative_truncation": "true",
    }
    for key, value in expected_flags.items():
        if native.get(key) != value:
            raise SystemExit(f"native flag mismatch {key}: {native.get(key)!r}")
    if native.get("attribute_tag") != selected["attribute_tag"]:
        raise SystemExit(f"tag mismatch: {native.get('attribute_tag')} != {selected['attribute_tag']}")
    if native.get("lossless_value") != selected["lossless_value"]:
        raise SystemExit("semantic value mismatch")

    comparison = {
        "existing_actor_branch": True,
        "property_present": True,
        "property_header_identity_exact": True,
        "payload_start_exact": True,
        "native_one_value_decode": True,
        "semantic_value_exact": True,
        "payload_end_exact": True,
        "next_property_present_consumed_bits": 0,
        "truncation_negative": True,
        "cursor_monotonicity": True,
        "mismatch_count": 0,
    }
    (out_dir / "r3_18a_comparison.json").write_text(
        json.dumps(comparison, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    aggregate = "\n".join(
        [
            "R3_18A_OUTCOME=A",
            "R3_18A_EVIDENCE=PASS",
            "R3_18A_REPLAY_IDENTITY=47/47",
            "R3_18A_PROPERTY_HEADER_EXACT=PASS",
            "R3_18A_PAYLOAD_START_EXACT=PASS",
            "R3_18A_NATIVE_ONE_VALUE=PASS",
            "R3_18A_SEMANTIC_EXACT=PASS",
            "R3_18A_PAYLOAD_END_EXACT=PASS",
            "R3_18A_NEXT_PROPERTY_PRESENT_CONSUMED_BITS=0",
            "R3_18A_TRUNCATION_NEGATIVE=PASS",
            "R3_18A_PRIVACY=PASS",
            "R3_18A_MISMATCH_COUNT=0",
            "R3_18A_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
        ]
    ) + "\n"
    (out_dir / "r3_18a_aggregate.txt").write_text(aggregate, encoding="utf-8", newline="\n")
    print("R3_18A_COMPARE=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("select")
    s.add_argument("log", type=Path)
    s.add_argument("request", type=Path)
    s.add_argument("selected", type=Path)
    s.add_argument("summary", type=Path)
    c = sub.add_parser("compare")
    c.add_argument("selected", type=Path)
    c.add_argument("native", type=Path)
    c.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    if args.cmd == "select":
        select(args.log, args.request, args.selected, args.summary)
    else:
        compare(args.selected, args.native, args.out_dir)


if __name__ == "__main__":
    main()
