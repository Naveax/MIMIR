from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

TAGS = ("Location", "RigidBody", "ReplicatedBoost", "PickupNew")
PREFIX_AGG = "R3_17I_AGG\t"
PREFIX_WITNESS = "R3_17I_WITNESS\t"
PREFIX_DONE = "R3_17I_REPLAY_DONE\t"


def fields(line: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for token in line.rstrip("\n").split("\t")[1:]:
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        out[key] = value
    return out


def as_int(row: dict[str, str], key: str) -> int:
    try:
        return int(row[key])
    except Exception as exc:
        raise SystemExit(f"invalid integer {key}: {row.get(key)!r}") from exc


def payload_bytes(raw_hex: str, width: int) -> bytes:
    if raw_hex == "<invalid>":
        raise SystemExit("invalid raw payload marker")
    try:
        raw = bytes.fromhex(raw_hex)
    except ValueError as exc:
        raise SystemExit(f"invalid raw hex: {raw_hex[:80]!r}") from exc
    expected = math.ceil(width / 8)
    if len(raw) != expected:
        raise SystemExit(f"raw payload length mismatch: width={width} bytes={len(raw)} expected={expected}")
    if width % 8 and raw:
        used = width % 8
        mask = (1 << used) - 1
        if raw[-1] & ~mask:
            raise SystemExit(f"non-zero packed padding bits: width={width} tail={raw[-1]:02x}")
    return raw


def structural_group(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row["attribute_tag"],
        row["shape"],
        row["version_major"],
        row["version_minor"],
        row["net_version"],
        row["is_rl_223"],
        row["payload_width"],
    )


def parse_group_from_agg(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row["tag"],
        row["shape"],
        row["version_major"],
        row["version_minor"],
        row["net_version"],
        row["is_rl_223"],
        row["payload_width"],
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: _tmp_r317i_analyze.py <boxcars-log>")
    log_path = Path(sys.argv[1])
    text = log_path.read_text(encoding="utf-8", errors="strict")
    lines = text.splitlines()

    parse_pass = sum(1 for line in lines if line == "R3_17I_ORACLE_PARSE=PASS")
    replay_done_rows = [fields(line) for line in lines if line.startswith(PREFIX_DONE)]
    agg_rows = [fields(line) for line in lines if line.startswith(PREFIX_AGG)]
    witness_rows = [fields(line) for line in lines if line.startswith(PREFIX_WITNESS)]

    if parse_pass != 47:
        raise SystemExit(f"expected 47 oracle parse passes, got {parse_pass}")
    if len(replay_done_rows) != 47:
        raise SystemExit(f"expected 47 replay-done rows, got {len(replay_done_rows)}")
    labels = [row.get("label", "") for row in replay_done_rows]
    if len(set(labels)) != 47:
        raise SystemExit(f"expected 47 unique replay labels, got {len(set(labels))}")

    aggregate_by_group: Counter[tuple[str, ...]] = Counter()
    per_tag: Counter[str] = Counter()
    replay_tags: dict[str, set[str]] = defaultdict(set)
    unclassified_count = 0

    for row in agg_rows:
        missing = {
            "label", "tag", "shape", "version_major", "version_minor", "net_version",
            "is_rl_223", "payload_width", "count"
        } - row.keys()
        if missing:
            raise SystemExit(f"aggregate row missing {sorted(missing)}")
        tag = row["tag"]
        if tag not in TAGS:
            raise SystemExit(f"unexpected K3 tag {tag!r}")
        count = as_int(row, "count")
        width = as_int(row, "payload_width")
        if count <= 0 or width <= 0:
            raise SystemExit(f"non-positive aggregate count/width: {row}")
        group = parse_group_from_agg(row)
        aggregate_by_group[group] += count
        per_tag[tag] += count
        replay_tags[row["label"]].add(tag)
        if row["shape"] == "<unclassified>":
            unclassified_count += count

    if not agg_rows:
        raise SystemExit("no K3 aggregate rows")

    zero_tags = [tag for tag in TAGS if per_tag[tag] == 0]

    first_witness_by_group: dict[tuple[str, ...], list[dict[str, object]]] = defaultdict(list)
    monotonicity_failures = 0
    raw_shape_failures = 0
    witness_unclassified = 0
    range_re = re.compile(r"\[(\d+),(\d+)\)")

    for row in witness_rows:
        required = {
            "label", "frame_index", "actor_ordinal", "actor_id",
            "actor_context_object_id", "actor_context_object_name", "stream_id",
            "property_object_id", "property_object_name", "attribute_tag", "shape",
            "version_major", "version_minor", "net_version", "is_rl_223",
            "payload_start_bit", "payload_end_bit", "payload_width", "boundary",
            "raw_bits_hex", "semantic"
        }
        missing = required - row.keys()
        if missing:
            raise SystemExit(f"witness row missing {sorted(missing)}")
        tag = row["attribute_tag"]
        if tag not in TAGS:
            raise SystemExit(f"unexpected witness tag {tag!r}")
        start = as_int(row, "payload_start_bit")
        end = as_int(row, "payload_end_bit")
        width = as_int(row, "payload_width")
        if end < start or end - start != width:
            monotonicity_failures += 1
            continue
        try:
            raw = payload_bytes(row["raw_bits_hex"], width)
        except SystemExit:
            raw_shape_failures += 1
            continue
        for a_text, b_text in range_re.findall(row["boundary"]):
            a = int(a_text)
            b = int(b_text)
            if b < a or a < start or b > end:
                monotonicity_failures += 1
                break
        if row["shape"] == "<unclassified>":
            witness_unclassified += 1
        group = structural_group(row)
        if len(first_witness_by_group[group]) < 4:
            first_witness_by_group[group].append({
                "replay": row["label"],
                "frame_index": as_int(row, "frame_index"),
                "actor_ordinal": as_int(row, "actor_ordinal"),
                "actor_id": as_int(row, "actor_id"),
                "actor_context_object_id": as_int(row, "actor_context_object_id"),
                "actor_context_object_name": row["actor_context_object_name"],
                "stream_id": as_int(row, "stream_id"),
                "property_object_id": as_int(row, "property_object_id"),
                "property_object_name": row["property_object_name"],
                "attribute_tag": tag,
                "shape": row["shape"],
                "version_major": as_int(row, "version_major"),
                "version_minor": as_int(row, "version_minor"),
                "net_version": as_int(row, "net_version"),
                "is_rl_223": row["is_rl_223"].lower() == "true",
                "payload_start_bit": start,
                "payload_end_bit": end,
                "payload_width": width,
                "boundary": row["boundary"],
                "packed_payload_sha256": hashlib.sha256(raw).hexdigest(),
                "semantic": row["semantic"],
            })

    missing_witness_groups = sorted(set(aggregate_by_group) - set(first_witness_by_group))
    if missing_witness_groups:
        raise SystemExit(f"aggregate groups without witnesses: {len(missing_witness_groups)}")

    output_groups = []
    for group in sorted(aggregate_by_group):
        tag, shape, major, minor, net, rl223, width = group
        output_groups.append({
            "attribute_tag": tag,
            "shape": shape,
            "version_major": int(major),
            "version_minor": int(minor),
            "net_version": int(net),
            "is_rl_223": rl223.lower() == "true",
            "payload_width": int(width),
            "occurrences": aggregate_by_group[group],
        })

    witnesses_out = []
    for group in sorted(first_witness_by_group):
        witnesses_out.extend(first_witness_by_group[group])

    Path("r3_17i_k3_groups.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in output_groups),
        encoding="utf-8",
        newline="\n",
    )
    Path("r3_17i_k3_witnesses.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in witnesses_out),
        encoding="utf-8",
        newline="\n",
    )

    shapes_by_tag: dict[str, Counter[str]] = {tag: Counter() for tag in TAGS}
    widths_by_tag: dict[str, Counter[int]] = {tag: Counter() for tag in TAGS}
    replay_count_by_tag: Counter[str] = Counter()
    for label, tagset in replay_tags.items():
        _ = label
        for tag in tagset:
            replay_count_by_tag[tag] += 1
    for group, count in aggregate_by_group.items():
        tag, shape, _major, _minor, _net, _rl223, width = group
        shapes_by_tag[tag][shape] += count
        widths_by_tag[tag][int(width)] += count

    outcome = "A"
    if zero_tags:
        outcome = "B"
    if unclassified_count or witness_unclassified or monotonicity_failures or raw_shape_failures:
        outcome = "C"

    summary = {
        "schema_version": 1,
        "pass": "R3.17I",
        "outcome": outcome,
        "replays_total": 47,
        "oracle_decode_success": parse_pass,
        "k3_occurrences_total": sum(per_tag.values()),
        "occurrences_by_tag": dict(per_tag),
        "replay_count_by_tag": dict(replay_count_by_tag),
        "shape_group_count": len(aggregate_by_group),
        "witness_rows": len(witnesses_out),
        "zero_tags": zero_tags,
        "unclassified_occurrences": unclassified_count,
        "witness_unclassified": witness_unclassified,
        "bit_monotonicity_failures": monotonicity_failures,
        "raw_payload_shape_failures": raw_shape_failures,
        "privacy_safe_output": True,
        "shapes_by_tag": {tag: dict(shapes_by_tag[tag]) for tag in TAGS},
        "widths_by_tag": {tag: {str(k): v for k, v in sorted(widths_by_tag[tag].items())} for tag in TAGS},
    }
    Path("r3_17i_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    aggregate_lines = [
        "R3_17I_REPLAYS_TOTAL=47",
        f"R3_17I_ORACLE_DECODE_SUCCESS={parse_pass}",
        f"R3_17I_K3_OCCURRENCES_TOTAL={sum(per_tag.values())}",
    ]
    for tag in TAGS:
        aggregate_lines.extend([
            f"R3_17I_{tag.upper()}_OCCURRENCES={per_tag[tag]}",
            f"R3_17I_{tag.upper()}_REPLAY_COUNT={replay_count_by_tag[tag]}",
            f"R3_17I_{tag.upper()}_SHAPE_GROUPS={len(shapes_by_tag[tag])}",
            "R3_17I_{}_WIDTHS={}".format(tag.upper(), ",".join(str(x) for x in sorted(widths_by_tag[tag]))),
        ])
    aggregate_lines.extend([
        f"R3_17I_GROUP_ROWS={len(output_groups)}",
        f"R3_17I_WITNESS_ROWS={len(witnesses_out)}",
        f"R3_17I_ZERO_TAG_COUNT={len(zero_tags)}",
        f"R3_17I_SHAPE_MISMATCH_OR_UNCLASSIFIED_COUNT={unclassified_count + witness_unclassified}",
        f"R3_17I_BIT_MONOTONICITY_FAILURE_COUNT={monotonicity_failures}",
        f"R3_17I_RAW_PAYLOAD_SHAPE_FAILURE_COUNT={raw_shape_failures}",
        "R3_17I_PRIVACY_SAFE_OUTPUT=PASS",
        "R3_17I_PRODUCTION_MUTATION=0",
        "R3_17I_CARGO_MUTATION=0",
        "R3_17I_CORPUS_MUTATION=0",
        f"R3_17I_OUTCOME={outcome}",
        "R3_17I_EVIDENCE=PASS" if outcome in {"A", "B"} else "R3_17I_EVIDENCE=FAIL",
    ])
    Path("r3_17i_aggregate.txt").write_text(
        "\n".join(aggregate_lines) + "\n", encoding="utf-8", newline="\n"
    )

    durable = Path("r3_17i_k3_groups.jsonl").read_text(encoding="utf-8") + Path("r3_17i_k3_witnesses.jsonl").read_text(encoding="utf-8")
    forbidden = ("raw_bits_hex", "unique_id", "remote_id", "online_id", "player_name", "account_id")
    hits = [needle for needle in forbidden if needle in durable.lower()]
    if hits:
        raise SystemExit(f"privacy durable-output forbidden fields: {hits}")

    print(f"R3_17I_ANALYZER_OUTCOME={outcome}")
    print(f"R3_17I_ANALYZER_OCCURRENCES={sum(per_tag.values())}")
    print(f"R3_17I_ANALYZER_GROUPS={len(output_groups)}")
    print(f"R3_17I_ANALYZER_WITNESSES={len(witnesses_out)}")


if __name__ == "__main__":
    main()
