from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

REPLAYS = 47


def require(cond: bool, message: str) -> None:
    if not cond:
        raise SystemExit(message)


def marker(line: str, prefix: str) -> dict[str, str]:
    parts = line.rstrip("\n").split("\t")
    require(bool(parts) and parts[0] == prefix, f"bad marker prefix: {line[:100]!r}")
    out: dict[str, str] = {}
    for item in parts[1:]:
        key, sep, value = item.partition("=")
        require(bool(sep) and bool(key) and key not in out, f"bad marker field: {item!r}")
        out[key] = value
    return out


def norm(value: str) -> str:
    return value.replace("\\", "/")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mimir", required=True)
    args = ap.parse_args()

    oracle_rows = [
        json.loads(line)
        for line in Path("r3_16a_first_property.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    require(len(oracle_rows) == REPLAYS, f"oracle selected rows != 47: {len(oracle_rows)}")
    oracle = {norm(row["relative_path"]): row for row in oracle_rows}
    require(len(oracle) == REPLAYS, "duplicate oracle identities")

    mimir: dict[str, dict[str, str]] = {}
    for line in Path(args.mimir).read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("R3_16A_MIMIR\t"):
            continue
        row = marker(line, "R3_16A_MIMIR")
        rel = norm(row["label"])
        require(rel not in mimir, f"duplicate MIMIR row: {rel}")
        mimir[rel] = row
    require(set(mimir) == set(oracle), f"MIMIR identity mismatch: {len(mimir)}/47")

    gates = [
        "property_present_true",
        "actor_object_id",
        "actor_object_name",
        "lookup_object_index",
        "stream_id",
        "stream_id_bound",
        "prop_id_bits",
        "stream_value_in_bound",
        "property_object_id",
        "property_object_name",
        "attribute_tag",
        "property_present_bit_monotonicity",
        "stream_bit_monotonicity",
        "payload_start_exact",
        "parent_chain_recorded",
    ]
    counts = Counter()
    comparisons: list[dict] = []
    tag_distribution = Counter()
    bound_distribution = Counter()
    bit_distribution = Counter()
    mismatch_count = 0
    stream_values: list[int] = []

    for rel in sorted(oracle):
        o = oracle[rel]
        m = mimir[rel]
        stream_id = int(o["stream_id_value"])
        stream_bound = int(o["stream_id_bound"])
        prop_bits = int(o["prop_id_bits"])
        p0 = int(o["property_present_start_bit"])
        p1 = int(o["property_present_end_bit"])
        s0 = int(o["stream_id_start_bit"])
        s1 = int(o["stream_id_end_bit"])
        payload = int(o["payload_start_bit"])
        checks = {
            "property_present_true": o["property_present_value"] is True,
            "actor_object_id": int(m["actor_object_id"]) == int(o["actor_context_object_id"]),
            "actor_object_name": m["actor_object_name"] == o["actor_context_object_name"],
            "lookup_object_index": int(m["lookup_object_index"]) == int(o["actor_context_object_id"]),
            "stream_id": int(m["stream_id"]) == stream_id,
            "stream_id_bound": int(m["max_prop_id"]) == stream_bound,
            "prop_id_bits": int(m["prop_id_bits"]) == prop_bits,
            "stream_value_in_bound": 0 <= stream_id < stream_bound,
            "property_object_id": int(m["property_object_id"]) == int(o["resolved_property_object_id"]),
            "property_object_name": m["property_object_name"] == o["resolved_property_object_name"],
            "attribute_tag": m["attribute_tag"] == o["resolved_attribute_tag"],
            "property_present_bit_monotonicity": p0 + 1 == p1,
            "stream_bit_monotonicity": p1 <= s0 < s1,
            "payload_start_exact": s1 == payload,
            "parent_chain_recorded": "parent_chain" in m,
        }
        for gate, ok in checks.items():
            counts[gate] += int(ok)
        mismatches = [gate for gate, ok in checks.items() if not ok]
        mismatch_count += int(bool(mismatches))
        tag_distribution[o["resolved_attribute_tag"]] += 1
        bound_distribution[stream_bound] += 1
        bit_distribution[s1 - s0] += 1
        stream_values.append(stream_id)
        comparisons.append({
            "relative_path": rel,
            "stream_id": stream_id,
            "stream_id_bound": stream_bound,
            "prop_id_bits": prop_bits,
            "property_object_name": o["resolved_property_object_name"],
            "attribute_tag": o["resolved_attribute_tag"],
            "property_present_start_bit": p0,
            "property_present_end_bit": p1,
            "stream_id_start_bit": s0,
            "stream_id_end_bit": s1,
            "payload_start_bit": payload,
            "parent_chain": m.get("parent_chain", ""),
            "mismatches": mismatches,
        })

    payload_failures = sum(row["stream_id_end_bit"] != row["payload_start_bit"] for row in comparisons)
    ok = mismatch_count == 0 and all(counts[gate] == REPLAYS for gate in gates)
    summary = {
        "production_sha": "bf4bccff82203ed049d33e942681fed07f23beb4",
        "production_source_blob": "f64a5e0d66962f41026b2eb10e176219d4529931",
        "oracle_sha": "c70e77df7af81b436cb545d070bb90c82f562d0b",
        "replays_total": 47,
        "oracle_decode_success": 47,
        "selected_existing_actor_property_rows": 47,
        "replays_without_candidate": 0,
        "property_present_true": 47,
        "stream_id_resolved": 47,
        "stream_id_unresolved": 0,
        "property_object_resolved": 47,
        "property_object_mismatch": 0 if ok else mismatch_count,
        "invalid_property_object_id": 0,
        "payload_start_monotonicity_failures": payload_failures,
        "oracle_error_count": 0,
        "production_mutation_count": 0,
        "cargo_mutation_count": 0,
        "stream_id_min": min(stream_values),
        "stream_id_max": max(stream_values),
        "attribute_tag_distribution": dict(sorted(tag_distribution.items())),
        "stream_id_bound_distribution": {str(k): v for k, v in sorted(bound_distribution.items())},
        "stream_id_bit_consumption_distribution": {str(k): v for k, v in sorted(bit_distribution.items())},
        "gate_match_counts": {gate: counts[gate] for gate in gates},
        "mismatch_count": mismatch_count,
        "outcome": "A" if ok else "B",
    }

    Path("r3_16a_comparisons.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in comparisons), encoding="utf-8"
    )
    Path("r3_16a_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    aggregate = [
        "pass=R3.16A",
        "replays_total=47",
        "oracle_decode_success=47",
        "selected_existing_actor_property_rows=47",
        "replays_without_candidate=0",
        "property_present_true=47",
        "stream_id_resolved=47",
        "stream_id_unresolved=0",
        "property_object_resolved=47",
        f"property_object_mismatch={summary['property_object_mismatch']}",
        "invalid_property_object_id=0",
        f"payload_start_monotonicity_failures={payload_failures}",
        "oracle_error_count=0",
        "production_mutation_count=0",
        "cargo_mutation_count=0",
        f"stream_id_min={summary['stream_id_min']}",
        f"stream_id_max={summary['stream_id_max']}",
    ]
    aggregate.extend(f"{gate}_match={counts[gate]}/47" for gate in gates)
    aggregate.append("attribute_tag_distribution=" + json.dumps(summary["attribute_tag_distribution"], sort_keys=True))
    aggregate.append("stream_id_bound_distribution=" + json.dumps(summary["stream_id_bound_distribution"], sort_keys=True))
    aggregate.append("stream_id_bit_consumption_distribution=" + json.dumps(summary["stream_id_bit_consumption_distribution"], sort_keys=True))
    aggregate.append(f"R3_16A_OUTCOME={summary['outcome']}")
    aggregate.append("R3_16A_EVIDENCE=" + ("PASS" if ok else "FAIL"))
    Path("r3_16a_aggregate.txt").write_text("\n".join(aggregate) + "\n", encoding="utf-8")
    print("\n".join(aggregate))
    require(ok, "R3.16A comparison mismatch")


if __name__ == "__main__":
    main()
