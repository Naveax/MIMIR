from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

TAGS = ("ActiveActor", "String", "QWordString", "UniqueId", "PartyLeader")
WITNESSES_PER_SHAPE = 12
SYSTEM_KIND = {
    0: "SplitScreen",
    1: "Steam",
    2: "PlayStation",
    4: "Xbox",
    5: "QQ",
    6: "Switch",
    7: "PsyNet",
    11: "Epic",
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


def expected_hex_chars(width: int) -> int:
    return ((width + 7) // 8) * 2


def payload_bytes(raw_hex: str, width: int) -> bytes:
    if raw_hex == "<invalid>" or len(raw_hex) != expected_hex_chars(width):
        raise ValueError("invalid packed raw payload length")
    data = bytes.fromhex(raw_hex)
    if width % 8 and data:
        used = width % 8
        if data[-1] >> used:
            raise ValueError("non-zero packed padding bits")
    return data


def text_wire_shape(data: bytes, offset: int = 0) -> tuple[str, int, int]:
    if len(data) < offset + 4:
        raise ValueError("text payload lacks i32 length")
    size = int.from_bytes(data[offset : offset + 4], "little", signed=True)
    if size == 0:
        content_bytes = 0
        encoding = "Empty"
    elif size > 0:
        content_bytes = size
        encoding = "Windows1252"
    else:
        if size == -(1 << 31):
            raise ValueError("text size cannot be negated")
        content_bytes = (-size) * 2
        encoding = "UTF16"
    total_bytes = 4 + content_bytes
    if len(data) < offset + total_bytes:
        raise ValueError("text payload shorter than declared length")
    return encoding, size, total_bytes


def unique_expected_width(system_id: int, net_version: int, data: bytes) -> tuple[str, int]:
    kind = SYSTEM_KIND.get(system_id)
    if kind is None:
        raise ValueError(f"unknown unique-id system id {system_id}")
    if system_id == 0:
        return kind, 40
    if system_id in (1, 4, 5):
        return kind, 80
    if system_id == 2:
        return kind, 336 if net_version >= 1 else 272
    if system_id == 6:
        return kind, 272
    if system_id == 7:
        return kind, 80 if net_version >= 10 else 272
    if system_id == 11:
        encoding, declared, text_bytes = text_wire_shape(data, 1)
        return f"{kind}:{encoding}:declared={declared}", 8 + text_bytes * 8 + 8
    raise AssertionError("unreachable")


def classify_and_sanitize(
    tag: str,
    row: dict[str, str],
    data: bytes,
    width: int,
) -> tuple[str, str]:
    oracle_shape = row.get("shape", "")
    net_version = as_int(row, "net_version")
    is_rl_223 = row["is_rl_223"].lower() == "true"
    decoded = row.get("decoded", "")

    if tag == "ActiveActor":
        if oracle_shape != "ActiveActor33" or width != 33:
            raise ValueError("ActiveActor shape/width mismatch")
        active = "unknown"
        if decoded.startswith("active:"):
            active = decoded.split(";", 1)[0].split(":", 1)[1]
        return "ActiveActor33", f"active={active};actor_ref=present"

    if tag == "String":
        encoding, declared, total_bytes = text_wire_shape(data)
        expected_width = total_bytes * 8
        if width != expected_width:
            raise ValueError(
                f"String width {width} != declared wire width {expected_width}"
            )
        decoded_fp = hashlib.sha256(decoded.encode("utf-8")).hexdigest()
        return (
            f"String:{encoding}:declared={declared}",
            f"oracle_decoded_summary_sha256={decoded_fp}",
        )

    if tag == "QWordString":
        if is_rl_223:
            encoding, declared, total_bytes = text_wire_shape(data)
            expected_width = total_bytes * 8
            if width != expected_width:
                raise ValueError(
                    f"QWordString text width {width} != declared wire width {expected_width}"
                )
            decoded_fp = hashlib.sha256(decoded.encode("utf-8")).hexdigest()
            return (
                f"QWordString:String:{encoding}:declared={declared}",
                f"oracle_decoded_summary_sha256={decoded_fp}",
            )
        if oracle_shape != "QWord64" or width != 64:
            raise ValueError("QWordString legacy QWord shape/width mismatch")
        return (
            "QWordString:QWord64",
            f"decoded_value_sha256={hashlib.sha256(decoded.encode('utf-8')).hexdigest()}",
        )

    if tag == "UniqueId":
        if len(data) < 1:
            raise ValueError("UniqueId lacks system id")
        system_id = data[0]
        kind_shape, expected_width = unique_expected_width(system_id, net_version, data)
        if width != expected_width:
            raise ValueError(
                f"UniqueId {kind_shape} width {width} != expected {expected_width}"
            )
        expected_prefix = f"UniqueId:{SYSTEM_KIND[system_id]}"
        if not oracle_shape.startswith(expected_prefix):
            raise ValueError(
                f"UniqueId oracle shape {oracle_shape!r} != {expected_prefix!r}"
            )
        return (
            f"UniqueId:{kind_shape}",
            f"system_id={system_id};remote_kind={SYSTEM_KIND[system_id]};identity=redacted",
        )

    if tag == "PartyLeader":
        if len(data) < 1:
            raise ValueError("PartyLeader lacks system id")
        system_id = data[0]
        if system_id == 0:
            if width != 8 or oracle_shape != "None":
                raise ValueError("PartyLeader null shape/width mismatch")
            return "PartyLeader:None", "system_id=0;identity=none"
        kind_shape, expected_width = unique_expected_width(system_id, net_version, data)
        if width != expected_width:
            raise ValueError(
                f"PartyLeader {kind_shape} width {width} != expected {expected_width}"
            )
        expected_prefix = f"Some:UniqueId:{SYSTEM_KIND[system_id]}"
        if not oracle_shape.startswith(expected_prefix):
            raise ValueError(
                f"PartyLeader oracle shape {oracle_shape!r} != {expected_prefix!r}"
            )
        return (
            f"PartyLeader:Some:{kind_shape}",
            f"system_id={system_id};remote_kind={SYSTEM_KIND[system_id]};identity=redacted",
        )

    raise ValueError(f"unsupported tag {tag}")


log_path = Path(sys.argv[1])
lines = log_path.read_text(encoding="utf-8", errors="strict").splitlines()
parse_passes = sum(line == "R3_17E_ORACLE_PARSE=PASS" for line in lines)
shape_mismatches = [
    line for line in lines if line.startswith("R3_17E_SHAPE_MISMATCH\t")
]
raw_rows = [parse_kv_line(line) for line in lines if line.startswith("R3_17E_K2\t")]

records: list[dict[str, object]] = []
monotonicity_failures = 0
raw_shape_failures = 0
unclassified = 0
for row in raw_rows:
    tag = row["attribute_tag"]
    if tag not in TAGS:
        raise SystemExit(f"unexpected K2 tag in receipt: {tag}")
    start = as_int(row, "payload_start_bit")
    end = as_int(row, "payload_end_bit")
    width = as_int(row, "payload_width")
    next_cursor = as_int(row, "next_cursor_bit")
    if start > end or end - start != width or next_cursor != end:
        monotonicity_failures += 1

    raw_hex = row.get("raw_bits_hex", "")
    data = b""
    try:
        data = payload_bytes(raw_hex, width)
        shape, safe_decoded = classify_and_sanitize(tag, row, data, width)
    except (ValueError, KeyError):
        raw_shape_failures += 1
        unclassified += 1
        shape = ""
        safe_decoded = ""

    raw_sha = hashlib.sha256(data).hexdigest() if shape else ""
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
            "packed_payload_sha256": raw_sha,
            "decoded_structure": safe_decoded,
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
    tag_shapes = [shape for shape in sorted(shapes_by_tag[tag]) if shape]
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
                str(rec["packed_payload_sha256"]),
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

with Path("r3_17e_k2_oracle.jsonl").open(
    "w", encoding="utf-8", newline="\n"
) as handle:
    for rec in records:
        handle.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

with Path("r3_17e_k2_witnesses.jsonl").open(
    "w", encoding="utf-8", newline="\n"
) as handle:
    for rec in witnesses:
        handle.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

summary: dict[str, object] = {
    "replays_total": 47,
    "oracle_decode_success": parse_passes,
    "k2_occurrences_total": len(records),
    "shape_mismatch_or_unclassified_count": len(shape_mismatches) + unclassified,
    "bit_monotonicity_failure_count": monotonicity_failures,
    "raw_payload_shape_failure_count": raw_shape_failures,
    "privacy": {
        "cleartext_payloads_in_oracle_jsonl": False,
        "cleartext_unique_ids_in_oracle_jsonl": False,
        "payload_identity": "packed-payload SHA-256 plus structural fields",
    },
    "witness_rows": len(witnesses),
    "tags": {},
}
for tag in TAGS:
    summary["tags"][tag] = {
        "occurrences": counts[tag],
        "replay_count": len(replays_by_tag[tag]),
        "unique_widths": sorted(widths_by_tag[tag]),
        "shapes": dict(
            sorted((shape, count) for shape, count in shapes_by_tag[tag].items() if shape)
        ),
        "rl223_modes": {
            str(key).lower(): value for key, value in sorted(rl223_by_tag[tag].items())
        },
        "witnesses": sum(1 for r in witnesses if r["attribute_tag"] == tag),
    }

Path("r3_17e_summary.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
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
        f"{shape}:{count}"
        for shape, count in sorted(shapes_by_tag[tag].items())
        if shape
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
        "R3_17E_PRIVACY_SAFE_OUTPUT=PASS",
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
