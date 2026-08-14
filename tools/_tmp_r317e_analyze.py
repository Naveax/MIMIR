from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

TAGS = ("ActiveActor", "String", "QWordString", "UniqueId", "PartyLeader")
WITNESSES_PER_SHAPE = 12


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


def expected_hex_chars(width: int) -> int:
    return ((width + 7) // 8) * 2


log_path = Path(sys.argv[1])
lines = log_path.read_text(encoding="utf-8", errors="strict").splitlines()
parse_passes = sum(line == "R3_17E_ORACLE_PARSE=PASS" for line in lines)
shape_mismatches = [line for line in lines if line.startswith("R3_17E_SHAPE_MISMATCH\t")]
raw_rows = [parse_kv_line(line) for line in lines if line.startswith("R3_17E_K2\t")]

records: list[dict[str, object]] = []
monotonicity_failures = 0
raw_shape_failures = 0
unclassified = 0
for row in raw_rows:
    tag = row["attribute_tag"]
    if tag not in TAGS:
        raise SystemExit(f"unexpected K2 tag in receipt: {tag}")
    shape = row.get("shape", "")
    if not shape:
        unclassified += 1
    start = as_int(row, "payload_start_bit")
    end = as_int(row, "payload_end_bit")
    width = as_int(row, "payload_width")
    next_cursor = as_int(row, "next_cursor_bit")
    if start > end or end - start != width or next_cursor != end:
        monotonicity_failures += 1
    raw_hex = row.get("raw_bits_hex", "")
    if raw_hex == "<invalid>" or len(raw_hex) != expected_hex_chars(width):
        raw_shape_failures += 1
    else:
        try:
            bytes.fromhex(raw_hex)
        except ValueError:
            raw_shape_failures += 1

    records.append(
        {
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
            "shape": shape,
            "version_major": as_int(row, "version_major"),
            "version_minor": as_int(row, "version_minor"),
            "net_version": as_int(row, "net_version"),
            "is_rl_223": row["is_rl_223"].lower() == "true",
            "payload_start_bit": start,
            "payload_end_bit": end,
            "payload_width": width,
            "next_cursor_bit": next_cursor,
            "raw_bits_hex": raw_hex,
            "decoded": row.get("decoded", ""),
        }
    )

records.sort(
    key=lambda r: (
        str(r["attribute_tag"]),
        str(r["shape"]),
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
shapes_by_tag: dict[str, Counter[str]] = defaultdict(Counter)
rl223_by_tag: dict[str, Counter[bool]] = defaultdict(Counter)
for rec in records:
    tag = str(rec["attribute_tag"])
    replays_by_tag[tag].add(str(rec["relative_path"]))
    widths_by_tag[tag].add(int(rec["payload_width"]))
    shapes_by_tag[tag][str(rec["shape"])] += 1
    rl223_by_tag[tag][bool(rec["is_rl_223"])] += 1

witnesses: list[dict[str, object]] = []
for tag in TAGS:
    tag_shapes = sorted(shapes_by_tag[tag])
    for shape in tag_shapes:
        shape_rows = [
            r for r in records if r["attribute_tag"] == tag and r["shape"] == shape
        ]
        chosen: list[dict[str, object]] = []
        seen: set[tuple[str, str, int, str]] = set()
        for rec in shape_rows:
            key = (
                str(rec["relative_path"]),
                str(rec["property_object_name"]),
                int(rec["payload_width"]),
                str(rec["decoded"]),
            )
            if key in seen:
                continue
            seen.add(key)
            chosen.append(rec)
            if len(chosen) == WITNESSES_PER_SHAPE:
                break
        if len(chosen) < WITNESSES_PER_SHAPE:
            chosen_keys = {
                (
                    str(r["relative_path"]),
                    int(r["frame_index"]),
                    int(r["actor_ordinal"]),
                    int(r["payload_start_bit"]),
                )
                for r in chosen
            }
            for rec in shape_rows:
                row_key = (
                    str(rec["relative_path"]),
                    int(rec["frame_index"]),
                    int(rec["actor_ordinal"]),
                    int(rec["payload_start_bit"]),
                )
                if row_key in chosen_keys:
                    continue
                chosen.append(rec)
                chosen_keys.add(row_key)
                if len(chosen) == WITNESSES_PER_SHAPE:
                    break
        witnesses.extend(chosen)

with Path("r3_17e_k2_oracle.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
    for rec in records:
        handle.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

with Path("r3_17e_k2_witnesses.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
    for rec in witnesses:
        handle.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

summary: dict[str, object] = {
    "replays_total": 47,
    "oracle_decode_success": parse_passes,
    "k2_occurrences_total": len(records),
    "shape_mismatch_or_unclassified_count": len(shape_mismatches) + unclassified,
    "bit_monotonicity_failure_count": monotonicity_failures,
    "raw_payload_shape_failure_count": raw_shape_failures,
    "witness_rows": len(witnesses),
    "tags": {},
}
for tag in TAGS:
    summary["tags"][tag] = {
        "occurrences": counts[tag],
        "replay_count": len(replays_by_tag[tag]),
        "unique_widths": sorted(widths_by_tag[tag]),
        "shapes": dict(sorted(shapes_by_tag[tag].items())),
        "rl223_modes": {
            str(key).lower(): value for key, value in sorted(rl223_by_tag[tag].items())
        },
        "witnesses": sum(1 for r in witnesses if r["attribute_tag"] == tag),
    }

Path("r3_17e_summary.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
)

errors = 0
if parse_passes != 47:
    errors += 1
if shape_mismatches or unclassified:
    errors += 1
if monotonicity_failures:
    errors += 1
if raw_shape_failures:
    errors += 1
observed_tags = [tag for tag in TAGS if counts[tag] > 0]
outcome = "A" if errors == 0 and observed_tags else "C"

aggregate_lines = [
    "R3_17E_REPLAYS_TOTAL=47",
    f"R3_17E_ORACLE_DECODE_SUCCESS={parse_passes}",
    f"R3_17E_K2_OCCURRENCES_TOTAL={len(records)}",
]
for tag in TAGS:
    widths = ",".join(str(x) for x in sorted(widths_by_tag[tag])) or "none"
    shapes = ",".join(
        f"{shape}:{count}" for shape, count in sorted(shapes_by_tag[tag].items())
    ) or "none"
    aggregate_lines.append(
        f"R3_17E_TAG={tag} occurrences={counts[tag]} replays={len(replays_by_tag[tag])} widths={widths} shapes={shapes} witnesses={sum(1 for r in witnesses if r['attribute_tag'] == tag)}"
    )
aggregate_lines.extend(
    [
        f"R3_17E_WITNESS_ROWS={len(witnesses)}",
        f"R3_17E_SHAPE_MISMATCH_OR_UNCLASSIFIED_COUNT={len(shape_mismatches) + unclassified}",
        f"R3_17E_BIT_MONOTONICITY_FAILURE_COUNT={monotonicity_failures}",
        f"R3_17E_RAW_PAYLOAD_SHAPE_FAILURE_COUNT={raw_shape_failures}",
        f"R3_17E_OUTCOME={outcome}",
        f"R3_17E_EVIDENCE={'PASS' if outcome == 'A' else 'FAIL'}",
    ]
)
Path("r3_17e_aggregate.txt").write_text(
    "\n".join(aggregate_lines) + "\n", encoding="utf-8", newline="\n"
)
print("\n".join(aggregate_lines))
if outcome != "A":
    raise SystemExit(1)
