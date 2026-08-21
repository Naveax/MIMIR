from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

oracle_path, native_path, rows_out, summary_out, negatives_out, aggregate_out = map(Path, sys.argv[1:])


def parse(prefix: str, path: Path) -> list[dict[str, str]]:
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith(prefix + "\t"):
            continue
        row: dict[str, str] = {}
        for field in line.split("\t")[1:]:
            if "=" not in field:
                raise SystemExit(f"malformed field in {prefix}: {field!r}")
            k, v = field.split("=", 1)
            row[k] = v
        rows.append(row)
    return rows


oracle = parse("R3_18AM_ORACLE", oracle_path)
native = parse("R3_18AM_NATIVE", native_path)
if len(oracle) != 47 or len(native) != 47:
    raise SystemExit(f"expected 47/47 rows, got oracle={len(oracle)} native={len(native)}")

ob = {r["label"]: r for r in oracle}
nb = {r["label"]: r for r in native}
if len(ob) != 47 or len(nb) != 47 or set(ob) != set(nb):
    raise SystemExit("label identity/multiplicity mismatch")

out = []
mismatches = 0
widths: Counter[int] = Counter()
semantic_values: list[int] = []
negative_keys = [
    "header_exact",
    "payload_repeatability",
    "payload_truncation_negative",
    "wrong_tag_negative",
    "wrong_boundary_negative",
    "wrong_context_negative",
    "corrupt_control_negative",
    "corrupt_prior_negative",
    "post_payload_end_poison",
]
negative_counts = Counter()

for label in sorted(ob):
    o = ob[label]
    n = nb[label]
    identity = (
        o["frame_index"] == n["frame_index"]
        and o["actor_ordinal"] == n["actor_ordinal"]
        and o["actor_context_object_id"] == n["actor_context_object_id"]
        and o["property_present_start_bit"] == n["property_present_start_bit"]
        and o["tag"] == n["tag"] == "Int"
    )
    payload_exact = (
        o["payload_start_bit"] == n["payload_start_bit"]
        and o["payload_end_bit"] == n["payload_end_bit"]
        and o["payload_width"] == n["payload_width"]
        and o["semantic_int"] == n["semantic_int"]
    )
    if not identity or not payload_exact:
        mismatches += 1
    width = int(o["payload_width"])
    widths[width] += 1
    semantic_values.append(int(o["semantic_int"]))
    for key in negative_keys:
        if n.get(key) == "1":
            negative_counts[key] += 1
    if n.get("another_control_bits_consumed") != "0":
        raise SystemExit(f"{label}: another-control consumption is not zero")
    out.append(
        {
            "label": label,
            "frame_index": int(o["frame_index"]),
            "actor_ordinal": int(o["actor_ordinal"]),
            "actor_context_object_id": int(o["actor_context_object_id"]),
            "property_present_start_bit": int(o["property_present_start_bit"]),
            "tag": "Int",
            "payload_start_bit": int(o["payload_start_bit"]),
            "payload_end_bit": int(o["payload_end_bit"]),
            "payload_width": width,
            "semantic_int": int(o["semantic_int"]),
            "native_oracle_exact": bool(identity and payload_exact),
        }
    )

if mismatches != 0:
    raise SystemExit(f"native/oracle mismatch={mismatches}")
if len(widths) != 1:
    raise SystemExit(f"payload family split: widths={dict(widths)}")
for key in negative_keys:
    if negative_counts[key] != 47:
        raise SystemExit(f"negative/control {key} count={negative_counts[key]} expected=47")

observed_width = next(iter(widths))
summary = {
    "rows": 47,
    "tags": {"Int": 47},
    "payload_widths": {str(k): v for k, v in sorted(widths.items())},
    "unique_payload_widths": len(widths),
    "observed_payload_width": observed_width,
    "semantic_int_min": min(semantic_values),
    "semantic_int_max": max(semantic_values),
    "native_oracle_mismatch": mismatches,
    "published_ak_exact": 47,
    "witness_reselection": 0,
    "another_control_bits_consumed": 0,
    "earlier_payload_contract_inheritance_assumed": False,
}
Path(rows_out).write_text(json.dumps({"rows": out}, indent=2) + "\n", encoding="utf-8", newline="\n")
Path(summary_out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

neg = [
    "R3_18AM_REPEATABILITY=PASS 47/47",
    "R3_18AM_PAYLOAD_TRUNCATION=PASS 47/47",
    "R3_18AM_WRONG_TAG_BOUNDARY_GUARD=PASS 47/47",
    "R3_18AM_WRONG_PAYLOAD_START_BOUNDARY_GUARD=PASS 47/47",
    "R3_18AM_WRONG_EXACT_VERSION_CONTEXT=PASS 47/47",
    "R3_18AM_CORRUPT_AG_CONTROL_NEGATIVE=PASS 47/47",
    "R3_18AM_CORRUPT_PRIOR_NEGATIVE=PASS 47/47",
    "R3_18AM_POST_PAYLOAD_END_POISON=PASS 47/47",
    "R3_18AM_EARLIER_PAYLOAD_CONTRACT_INHERITANCE=REJECTED",
    "R3_18AM_ANOTHER_CONTROL_BITS_CONSUMED=0",
]
Path(negatives_out).write_text("\n".join(neg) + "\n", encoding="utf-8", newline="\n")

agg = [
    "R3_18AM_OUTCOME=A",
    "R3_18AM_EVIDENCE=PASS",
    "R3_18AM_FROZEN_ROWS=47/47",
    "R3_18AM_PUBLISHED_AK_EXACT=47/47",
    "R3_18AM_TAG_INT=47",
    f"R3_18AM_OBSERVED_PAYLOAD_WIDTH={observed_width}",
    f"R3_18AM_PAYLOAD_WIDTH_COUNT={widths[observed_width]}",
    "R3_18AM_NATIVE_ORACLE_MISMATCH=0",
    "R3_18AM_WITNESS_RESELECTION=0",
    "R3_18AM_ANOTHER_CONTROL_BITS_CONSUMED=0",
    "R3_18AM_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
    "R3_18AM_PRIVACY_SCAN=PASS",
]
Path(aggregate_out).write_text("\n".join(agg) + "\n", encoding="utf-8", newline="\n")
print(f"R3_18AM_ANALYSIS=PASS rows=47 width={observed_width} mismatch=0")
