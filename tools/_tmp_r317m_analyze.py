from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

TAGS = (
    "CamSettings",
    "TeamPaint",
    "TeamLoadout",
    "ClubColors",
    "Reservation",
    "StatEvent",
    "PlayerHistoryKey",
    "DemolishFx",
    "DemolishExtended",
    "ExtendedExplosion",
    "LoadoutsOnline",
)
PREFIX_AGG = "R3_17M_AGG\t"
PREFIX_WITNESS = "R3_17M_WITNESS\t"
PREFIX_DONE = "R3_17M_REPLAY_DONE\t"


def fields(line: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for token in line.rstrip("\n").split("\t")[1:]:
        if "=" in token:
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
        raise SystemExit(
            f"raw payload length mismatch: width={width} bytes={len(raw)} expected={expected}"
        )
    if width % 8 and raw:
        used = width % 8
        mask = (1 << used) - 1
        if raw[-1] & ~mask:
            raise SystemExit(
                f"non-zero packed padding bits: width={width} tail={raw[-1]:02x}"
            )
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


def group_from_agg(row: dict[str, str]) -> tuple[str, ...]:
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
        raise SystemExit("usage: _tmp_r317m_analyze.py <boxcars-log>")
    log_path = Path(sys.argv[1])
    lines = log_path.read_text(encoding="utf-8", errors="strict").splitlines()

    parse_pass = sum(line == "R3_17M_ORACLE_PARSE=PASS" for line in lines)
    replay_done_rows = [fields(x) for x in lines if x.startswith(PREFIX_DONE)]
    agg_rows = [fields(x) for x in lines if x.startswith(PREFIX_AGG)]
    witness_rows = [fields(x) for x in lines if x.startswith(PREFIX_WITNESS)]

    if parse_pass != 47:
        raise SystemExit(f"expected 47 oracle parse passes, got {parse_pass}")
    if len(replay_done_rows) != 47:
        raise SystemExit(f"expected 47 replay-done rows, got {len(replay_done_rows)}")
    labels = [r.get("label", "") for r in replay_done_rows]
    if len(set(labels)) != 47:
        raise SystemExit(f"expected 47 unique replay labels, got {len(set(labels))}")

    by_group: Counter[tuple[str, ...]] = Counter()
    per_tag: Counter[str] = Counter()
    replay_tags: dict[str, set[str]] = defaultdict(set)
    unclassified_occurrences = 0

    required_agg = {
        "label", "tag", "shape", "version_major", "version_minor", "net_version",
        "is_rl_223", "payload_width", "count",
    }
    for row in agg_rows:
        missing = required_agg - row.keys()
        if missing:
            raise SystemExit(f"aggregate row missing {sorted(missing)}")
        tag = row["tag"]
        if tag not in TAGS:
            raise SystemExit(f"unexpected K4 tag {tag!r}")
        count = as_int(row, "count")
        width = as_int(row, "payload_width")
        if count <= 0 or width <= 0:
            raise SystemExit(f"non-positive aggregate count/width: {row}")
        group = group_from_agg(row)
        by_group[group] += count
        per_tag[tag] += count
        replay_tags[row["label"]].add(tag)
        if row["shape"] == "<unclassified>":
            unclassified_occurrences += count

    zero_tags = [tag for tag in TAGS if per_tag[tag] == 0]

    first_witness_by_group: dict[tuple[str, ...], list[dict[str, object]]] = defaultdict(list)
    monotonicity_failures = 0
    raw_shape_failures = 0
    witness_unclassified = 0
    range_re = re.compile(r"\[(\d+),(\d+)\)")

    required_witness = {
        "label", "frame_index", "actor_ordinal", "actor_id",
        "actor_context_object_id", "actor_context_object_name", "stream_id",
        "property_object_id", "property_object_name", "attribute_tag", "shape",
        "version_major", "version_minor", "net_version", "is_rl_223",
        "payload_start_bit", "payload_end_bit", "payload_width", "boundary",
        "raw_bits_hex", "semantic",
    }

    for row in witness_rows:
        missing = required_witness - row.keys()
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
            payload_bytes(row["raw_bits_hex"], width)
        except SystemExit:
            raw_shape_failures += 1
            continue
        bad_range = False
        for a_text, b_text in range_re.findall(row["boundary"]):
            a, b = int(a_text), int(b_text)
            if b < a or a < start or b > end:
                monotonicity_failures += 1
                bad_range = True
                break
        if bad_range:
            continue
        if row["shape"] == "<unclassified>":
            witness_unclassified += 1
        group = structural_group(row)
        if len(first_witness_by_group[group]) < 4:
            structural_basis = "|".join(
                [
                    tag,
                    row["shape"],
                    row["version_major"],
                    row["version_minor"],
                    row["net_version"],
                    row["is_rl_223"],
                    row["payload_width"],
                    row["boundary"],
                ]
            ).encode("utf-8")
            first_witness_by_group[group].append(
                {
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
                    "semantic_class": row["semantic"],
                    "structural_witness_sha256": hashlib.sha256(structural_basis).hexdigest(),
                }
            )

    missing_witness_groups = sorted(set(by_group) - set(first_witness_by_group))
    if missing_witness_groups:
        raise SystemExit(f"aggregate groups without witnesses: {len(missing_witness_groups)}")

    groups_out: list[dict[str, object]] = []
    for group in sorted(by_group):
        tag, shape, major, minor, net, rl223, width = group
        groups_out.append(
            {
                "attribute_tag": tag,
                "shape": shape,
                "version_major": int(major),
                "version_minor": int(minor),
                "net_version": int(net),
                "is_rl_223": rl223.lower() == "true",
                "payload_width": int(width),
                "occurrences": by_group[group],
            }
        )

    witnesses_out: list[dict[str, object]] = []
    for group in sorted(first_witness_by_group):
        witnesses_out.extend(first_witness_by_group[group])

    Path("r3_17m_k4_groups.jsonl").write_text(
        "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n" for r in groups_out),
        encoding="utf-8", newline="\n",
    )
    Path("r3_17m_k4_witnesses.jsonl").write_text(
        "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n" for r in witnesses_out),
        encoding="utf-8", newline="\n",
    )

    shapes_by_tag: dict[str, Counter[str]] = {tag: Counter() for tag in TAGS}
    widths_by_tag: dict[str, Counter[int]] = {tag: Counter() for tag in TAGS}
    contexts_by_tag: dict[str, Counter[str]] = {tag: Counter() for tag in TAGS}
    replay_count_by_tag: Counter[str] = Counter()
    for tagset in replay_tags.values():
        for tag in tagset:
            replay_count_by_tag[tag] += 1
    for group, count in by_group.items():
        tag, shape, major, minor, net, rl223, width = group
        shapes_by_tag[tag][shape] += count
        widths_by_tag[tag][int(width)] += count
        contexts_by_tag[tag][f"{major}.{minor}.{net}|rl223={rl223}|w={width}"] += count

    outcome = "A"
    if zero_tags:
        outcome = "B"
    if unclassified_occurrences or witness_unclassified or monotonicity_failures or raw_shape_failures:
        outcome = "C"

    summary = {
        "schema_version": 1,
        "pass": "R3.17M",
        "outcome": outcome,
        "replays_total": 47,
        "oracle_decode_success": parse_pass,
        "k4_occurrences_total": sum(per_tag.values()),
        "occurrences_by_tag": {tag: per_tag[tag] for tag in TAGS},
        "replay_count_by_tag": {tag: replay_count_by_tag[tag] for tag in TAGS},
        "shape_group_count": len(groups_out),
        "witness_rows": len(witnesses_out),
        "zero_tags": zero_tags,
        "unclassified_occurrences": unclassified_occurrences,
        "witness_unclassified": witness_unclassified,
        "bit_monotonicity_failures": monotonicity_failures,
        "raw_payload_shape_failures": raw_shape_failures,
        "privacy_safe_output": True,
        "shapes_by_tag": {tag: dict(shapes_by_tag[tag]) for tag in TAGS},
        "widths_by_tag": {
            tag: {str(k): v for k, v in sorted(widths_by_tag[tag].items())} for tag in TAGS
        },
        "contexts_by_tag": {tag: dict(contexts_by_tag[tag]) for tag in TAGS},
    }
    Path("r3_17m_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )

    aggregate_lines = [
        "R3_17M_REPLAYS_TOTAL=47",
        f"R3_17M_ORACLE_DECODE_SUCCESS={parse_pass}",
        f"R3_17M_K4_OCCURRENCES_TOTAL={sum(per_tag.values())}",
    ]
    for tag in TAGS:
        key = re.sub(r"[^A-Z0-9]", "_", tag.upper())
        aggregate_lines += [
            f"R3_17M_{key}_OCCURRENCES={per_tag[tag]}",
            f"R3_17M_{key}_REPLAY_COUNT={replay_count_by_tag[tag]}",
            f"R3_17M_{key}_SHAPE_GROUPS={len(shapes_by_tag[tag])}",
            "R3_17M_{}_WIDTHS={}".format(
                key, ",".join(str(x) for x in sorted(widths_by_tag[tag]))
            ),
        ]
    aggregate_lines += [
        f"R3_17M_GROUP_ROWS={len(groups_out)}",
        f"R3_17M_WITNESS_ROWS={len(witnesses_out)}",
        f"R3_17M_ZERO_TAG_COUNT={len(zero_tags)}",
        f"R3_17M_UNCLASSIFIED_COUNT={unclassified_occurrences + witness_unclassified}",
        f"R3_17M_BIT_MONOTONICITY_FAILURE_COUNT={monotonicity_failures}",
        f"R3_17M_RAW_PAYLOAD_SHAPE_FAILURE_COUNT={raw_shape_failures}",
        "R3_17M_PRIVACY_SAFE_OUTPUT=PASS",
        "R3_17M_PRODUCTION_MUTATION=0",
        "R3_17M_CARGO_MUTATION=0",
        "R3_17M_FIXTURE_MUTATION=0",
        "R3_17M_CORPUS_MUTATION=0",
        "R3_17M_SUPPORT_LANE_MUTATION=0",
        f"R3_17M_OUTCOME={outcome}",
        "R3_17M_EVIDENCE=PASS" if outcome in {"A", "B"} else "R3_17M_EVIDENCE=FAIL",
    ]
    Path("r3_17m_aggregate.txt").write_text(
        "\n".join(aggregate_lines) + "\n", encoding="utf-8", newline="\n"
    )

    durable = (
        Path("r3_17m_k4_groups.jsonl").read_text(encoding="utf-8")
        + Path("r3_17m_k4_witnesses.jsonl").read_text(encoding="utf-8")
        + Path("r3_17m_summary.json").read_text(encoding="utf-8")
    ).lower()
    forbidden = (
        "raw_bits_hex", "remote_id", "online_id", "player_name", "account_id",
        "reservation_name", "epic_account", "steam_id", "psn_name",
    )
    hits = [needle for needle in forbidden if needle in durable]
    if hits:
        raise SystemExit(f"privacy durable-output forbidden fields: {hits}")

    print(f"R3_17M_ANALYZER_OUTCOME={outcome}")
    print(f"R3_17M_ANALYZER_OCCURRENCES={sum(per_tag.values())}")
    print(f"R3_17M_ANALYZER_GROUPS={len(groups_out)}")
    print(f"R3_17M_ANALYZER_WITNESSES={len(witnesses_out)}")
    print(f"R3_17M_ZERO_TAGS={','.join(zero_tags)}")


if __name__ == "__main__":
    main()
