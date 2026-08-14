from __future__ import annotations

import json
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path

TAGS = ("Boolean", "Byte", "Enum", "Float", "Int", "Int64")
EXPECTED_WIDTHS = {
    "Boolean": 1,
    "Byte": 8,
    "Enum": 11,
    "Float": 32,
    "Int": 32,
    "Int64": 64,
}


def parse_kv_line(line: str) -> dict[str, str]:
    fields = line.rstrip("\n").split("\t")
    out: dict[str, str] = {}
    for field in fields[1:]:
        if "=" not in field:
            raise ValueError(f"malformed field: {field!r}")
        key, value = field.split("=", 1)
        out[key] = value
    return out


def as_int(row: dict[str, str], key: str) -> int:
    return int(row[key])


log_path = Path(sys.argv[1])
lines = log_path.read_text(encoding="utf-8", errors="strict").splitlines()
parse_passes = sum(line == "R3_17A_ORACLE_PARSE=PASS" for line in lines)
shape_mismatches = [line for line in lines if line.startswith("R3_17A_SHAPE_MISMATCH\t")]
raw_rows = [parse_kv_line(line) for line in lines if line.startswith("R3_17A_SCALAR\t")]

records: list[dict[str, object]] = []
monotonicity_failures = 0
unexpected_widths = 0
for row in raw_rows:
    tag = row["attribute_tag"]
    if tag not in TAGS:
        raise SystemExit(f"unexpected scalar tag in receipt: {tag}")
    start = as_int(row, "payload_start_bit")
    end = as_int(row, "payload_end_bit")
    width = as_int(row, "payload_width")
    next_cursor = as_int(row, "next_cursor_bit")
    if start > end or end - start != width or next_cursor != end:
        monotonicity_failures += 1
    if width != EXPECTED_WIDTHS[tag]:
        unexpected_widths += 1

    lossless = row["lossless_value"]
    rec: dict[str, object] = {
        "relative_path": row["label"],
        "frame_index": as_int(row, "frame_index"),
        "actor_ordinal": as_int(row, "actor_ordinal"),
        "actor_id": as_int(row, "actor_id"),
        "actor_context_object_id": as_int(row, "actor_context_object_id"),
        "actor_context_object_name": row["actor_context_object_name"],
        "stream_id": as_int(row, "stream_id"),
        "property_object_id": as_int(row, "property_object_id"),
        "property_object_name": row["property_object_name"],
        "attribute_tag": tag,
        "version_major": as_int(row, "version_major"),
        "version_minor": as_int(row, "version_minor"),
        "net_version": as_int(row, "net_version"),
        "payload_start_bit": start,
        "payload_end_bit": end,
        "payload_width": width,
        "next_cursor_bit": next_cursor,
        "lossless_value": lossless,
    }
    if tag == "Float":
        raw_u32 = int(lossless)
        rec["float_raw_u32"] = raw_u32
        rec["float_decoded_f32"] = struct.unpack("<f", struct.pack("<I", raw_u32))[0]
    else:
        rec["numeric_value"] = int(lossless)
    records.append(rec)

records.sort(
    key=lambda r: (
        str(r["attribute_tag"]),
        str(r["relative_path"]),
        int(r["frame_index"]),
        int(r["actor_ordinal"]),
        int(r["stream_id"]),
        int(r["payload_start_bit"]),
    )
)

counts = Counter(str(r["attribute_tag"]) for r in records)
replays_by_tag: dict[str, set[str]] = defaultdict(set)
widths_by_tag: dict[str, set[int]] = defaultdict(set)
values_by_tag: dict[str, set[str]] = defaultdict(set)
for rec in records:
    tag = str(rec["attribute_tag"])
    replays_by_tag[tag].add(str(rec["relative_path"]))
    widths_by_tag[tag].add(int(rec["payload_width"]))
    values_by_tag[tag].add(str(rec["lossless_value"]))

# Bounded deterministic witness selection: prefer a new replay/property/value
# combination, then fill from the remaining sorted rows. The full row stream is
# retained separately, so witnesses are only a human-review convenience.
witnesses: list[dict[str, object]] = []
for tag in TAGS:
    tag_rows = [r for r in records if r["attribute_tag"] == tag]
    chosen: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()
    for rec in tag_rows:
        key = (
            str(rec["relative_path"]),
            str(rec["property_object_name"]),
            str(rec["lossless_value"]),
        )
        if key in seen:
            continue
        seen.add(key)
        chosen.append(rec)
        if len(chosen) == 16:
            break
    if len(chosen) < 16:
        selected_ids = {id(r) for r in chosen}
        for rec in tag_rows:
            if id(rec) in selected_ids:
                continue
            chosen.append(rec)
            if len(chosen) == 16:
                break
    witnesses.extend(chosen)

all_out = Path("r3_17a_scalar_oracle.jsonl")
with all_out.open("w", encoding="utf-8", newline="\n") as handle:
    for rec in records:
        handle.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

wit_out = Path("r3_17a_scalar_witnesses.jsonl")
with wit_out.open("w", encoding="utf-8", newline="\n") as handle:
    for rec in witnesses:
        handle.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

summary = {
    "replays_total": 47,
    "oracle_decode_success": parse_passes,
    "scalar_occurrences_total": len(records),
    "shape_mismatch_count": len(shape_mismatches),
    "bit_monotonicity_failure_count": monotonicity_failures,
    "unexpected_tag_shape_count": unexpected_widths + len(shape_mismatches),
    "tags": {},
}
for tag in TAGS:
    tag_rows = [r for r in records if r["attribute_tag"] == tag]
    numeric_values = [int(r["lossless_value"]) for r in tag_rows]
    tag_summary: dict[str, object] = {
        "occurrences": counts[tag],
        "replay_count": len(replays_by_tag[tag]),
        "unique_widths": sorted(widths_by_tag[tag]),
        "unique_lossless_values": len(values_by_tag[tag]),
        "witnesses": sum(1 for r in witnesses if r["attribute_tag"] == tag),
    }
    if numeric_values:
        tag_summary["lossless_min"] = min(numeric_values)
        tag_summary["lossless_max"] = max(numeric_values)
    summary["tags"][tag] = tag_summary

Path("r3_17a_summary.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
)

errors = 0
if parse_passes != 47:
    errors += 1
if shape_mismatches:
    errors += 1
if monotonicity_failures:
    errors += 1
if unexpected_widths:
    errors += 1

observed_tags = [tag for tag in TAGS if counts[tag] > 0]
outcome = "A" if errors == 0 and observed_tags else "C"
aggregate_lines = [
    "R3_17A_REPLAYS_TOTAL=47",
    f"R3_17A_ORACLE_DECODE_SUCCESS={parse_passes}",
    f"R3_17A_SCALAR_OCCURRENCES_TOTAL={len(records)}",
]
for tag in TAGS:
    widths = ",".join(str(x) for x in sorted(widths_by_tag[tag])) or "none"
    aggregate_lines.append(
        f"R3_17A_TAG={tag} occurrences={counts[tag]} replays={len(replays_by_tag[tag])} widths={widths} witnesses={sum(1 for r in witnesses if r['attribute_tag'] == tag)}"
    )
aggregate_lines.extend(
    [
        f"R3_17A_SHAPE_MISMATCH_COUNT={len(shape_mismatches)}",
        f"R3_17A_BIT_MONOTONICITY_FAILURE_COUNT={monotonicity_failures}",
        f"R3_17A_UNEXPECTED_TAG_SHAPE_COUNT={unexpected_widths + len(shape_mismatches)}",
        f"R3_17A_OUTCOME={outcome}",
        f"R3_17A_EVIDENCE={'PASS' if outcome == 'A' else 'FAIL'}",
    ]
)
Path("r3_17a_aggregate.txt").write_text(
    "\n".join(aggregate_lines) + "\n", encoding="utf-8", newline="\n"
)
print("\n".join(aggregate_lines))
if outcome != "A":
    raise SystemExit(1)
