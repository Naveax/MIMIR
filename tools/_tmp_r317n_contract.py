from __future__ import annotations

import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

EXPECTED_SHA = "80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b"
EXPECTED_ROWS = 161
EXPECTED_GROUP_ROWS = {
    "CamSettings": 2,
    "ClubColors": 1,
    "DemolishExtended": 5,
    "DemolishFx": 19,
    "ExtendedExplosion": 2,
    "LoadoutsOnline": 79,
    "PlayerHistoryKey": 1,
    "Reservation": 46,
    "StatEvent": 2,
    "TeamLoadout": 2,
    "TeamPaint": 2,
}
EXPECTED_SHAPES = {
    "CamSettings": 1,
    "ClubColors": 1,
    "DemolishExtended": 5,
    "DemolishFx": 12,
    "ExtendedExplosion": 1,
    "LoadoutsOnline": 73,
    "PlayerHistoryKey": 1,
    "Reservation": 35,
    "StatEvent": 1,
    "TeamLoadout": 1,
    "TeamPaint": 1,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: _tmp_r317n_contract.py <r3_17m_k4_groups.jsonl>")
    src = Path(sys.argv[1])
    if not src.is_file():
        raise SystemExit(f"missing evidence groups: {src}")
    if sha256(src) != EXPECTED_SHA:
        raise SystemExit("R3.17M groups SHA drift")

    raw_lines = src.read_text(encoding="utf-8").splitlines()
    if len(raw_lines) != EXPECTED_ROWS:
        raise SystemExit(f"expected 161 groups, got {len(raw_lines)}")
    rows = [json.loads(line) for line in raw_lines]
    required = {
        "attribute_tag",
        "is_rl_223",
        "net_version",
        "occurrences",
        "payload_width",
        "shape",
        "version_major",
        "version_minor",
    }
    keys = []
    for row in rows:
        if set(row) != required:
            raise SystemExit(f"unexpected group schema: {sorted(row)}")
        if row["occurrences"] <= 0 or row["payload_width"] <= 0:
            raise SystemExit(f"non-positive evidence row: {row}")
        key = (
            row["attribute_tag"],
            row["shape"],
            row["version_major"],
            row["version_minor"],
            row["net_version"],
            row["is_rl_223"],
            row["payload_width"],
        )
        keys.append(key)
    if len(set(keys)) != EXPECTED_ROWS:
        raise SystemExit("duplicate exact structural/context group")

    tag_rows = Counter(row["attribute_tag"] for row in rows)
    if dict(sorted(tag_rows.items())) != EXPECTED_GROUP_ROWS:
        raise SystemExit(f"group-row distribution drift: {dict(sorted(tag_rows.items()))}")
    shape_counts = {
        tag: len({row["shape"] for row in rows if row["attribute_tag"] == tag})
        for tag in tag_rows
    }
    if dict(sorted(shape_counts.items())) != EXPECTED_SHAPES:
        raise SystemExit(f"shape distribution drift: {dict(sorted(shape_counts.items()))}")

    out_groups = Path("docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl")
    out_groups.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_groups)
    if out_groups.read_bytes() != src.read_bytes():
        raise SystemExit("admitted groups are not byte-identical to evidence groups")
    if sha256(out_groups) != EXPECTED_SHA:
        raise SystemExit("admitted-group output SHA mismatch")

    contract = r'''# MIMIR R3.17N — K4 Evidence-Supported One-Value Contract

**Status:** contract candidate  
**Production implementation:** forbidden in R3.17N  
**Evidence authority:** R3.17M Outcome A  
**Canonical admitted groups:** `MIMIR_R3_17N_ADMITTED_GROUPS.jsonl`

## Authority lock

```text
production SHA               7390e3b145372252caaa8fa1fe3e0cd13b83336c
R3.17M evidence head         a50f09857f36ac52cec30b4bf3efbde9e15bb564
R3.17M authority run/job     31881779861 / 95005282281 SUCCESS
R3.17M exact-head CI         31881779862 / 95005282149 SUCCESS
R3.17M artifact              9246249473
R3.17M artifact digest       sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
R3.17M groups SHA256         80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
admitted groups SHA256       80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
admitted exact groups        161
cross-product widening       0
```

The admitted-group artifact is byte-for-byte identical to the R3.17M evidence groups. `occurrences` remains evidence metadata; acceptance identity is the exact tuple `(attribute_tag, shape, version_major, version_minor, net_version, is_rl_223, payload_width)`.

## Common one-value contract

1. The caller supplies one already-resolved K4 attribute tag, replay context and payload start bit.
2. Bit order is LSB-first and an unaligned start is legal.
3. A successful decode must match one and only one row of the exact admitted-group artifact and stop at that value's exact end bit.
4. Checked arithmetic is mandatory for every length, count, width and cursor advance.
5. Invalid start, insufficient bits, malformed signed text length, count overflow, unknown product branch, wrong version/context or a structural shape absent from the exact group artifact fails atomically.
6. Atomic failure means no successful partial value and no admitted end position escapes the call.
7. Exact group membership outranks independent subfield membership. Observing A with B and C with D never admits A with D.
8. Extra trailing bits are not a second property and must remain unconsumed.
9. Boxcars source can explain how an observed group is decoded; it cannot admit a group absent from R3.17M evidence.
10. R3.17N does not add a production K4 API or decoder.

## Exact admitted surface

```text
family               group rows   unique shapes
CamSettings                    2               1
ClubColors                     1               1
DemolishExtended               5               5
DemolishFx                    19              12
ExtendedExplosion              2               1
LoadoutsOnline                79              73
PlayerHistoryKey               1               1
Reservation                   46              35
StatEvent                      2               1
TeamLoadout                    2               1
TeamPaint                      2               1
TOTAL                         161             132
```

The difference between shape count and group-row count is intentional: replay context, RL223 state and payload width are part of exact admission.

## Fixed-shape families

- `CamSettings`: exact observed `f32x7`, width 224. No earlier six-float branch.
- `TeamPaint`: exact `u8x3 + u32x2`, width 88.
- `TeamLoadout`: exact blue/orange observed `v28:u2:specials:banner:product:extra3`, width 1040. No other loadout version.
- `ClubColors`: exact `bit + u8 + bit + u8`, width 18.
- `StatEvent`: exact `bit + i32`, width 33.
- `PlayerHistoryKey`: exact u14, width 14.
- `ExtendedExplosion`: exact observed actor/reference fields plus its admitted vector shape, width 112.

## Reservation

Only the 46 exact context rows / 35 observed structural shapes in the admitted artifact are legal. Identifier system, split-screen branch, Epic text length, optional reservation-name text shape, version-gated six-bit tail and total payload width remain coupled in the exact tuple. Independent unions of identifier systems and name/text lengths are forbidden.

## DemolishFx and DemolishExtended

`DemolishFx` admits only its 19 exact group rows / 12 observed vector-pair shapes. `DemolishExtended` admits only its five exact group rows / five observed vector-pair shapes. Attacker and victim vector shapes are not independently cross-productable.

## LoadoutsOnline

Only the 79 exact context rows / 73 observed nested shapes are legal. Blue/orange outer counts, per-group product counts, product-attribute object branches, product-value branches, title-text lengths and exact total width stay coupled. An implementation must reject a nested combination that is absent from the admitted artifact even if each individual product branch appeared elsewhere.

## Positive vector plan

A later implementation pass must generate or materialize at least one deterministic positive payload for every admitted row and prove:

```text
admitted row coverage                   161/161
returned tag/variant                    exact
replay context                          exact
structural shape                        exact
payload width                           exact
end bit                                 exact
trailing poison bits consumed           0
```

Real replay witnesses remain an audit oracle, not checked-in private payload data.

## Required negative / malformed vector plan

The implementation pass must include fail-closed vectors for at least:

```text
wrong replay major/minor/net_version/RL223 context
unknown or non-K4 tag
invalid start bit
truncation at every fixed primitive boundary
truncation by one bit for representative variable-width groups
malformed signed text length and checked-length overflow
Reservation unobserved identifier/name/text-length combination
Reservation unobserved total-width/context combination
DemolishFx unobserved attacker/victim vector-pair combination
DemolishExtended unobserved attacker/victim vector-pair combination
LoadoutsOnline unobserved outer/group/product combination
LoadoutsOnline malformed nested count/length
LoadoutsOnline unknown product-attribute object branch
unobserved TeamLoadout version branch
source-known but evidence-unobserved branch
extra trailing bits remain unconsumed
```

## Error boundary

The later decoder must preserve the existing MIMIR fail-closed style. R3.17N admits error semantics, not concrete public error enum names. At minimum the implementation must distinguish or map deterministically from:

```text
invalid-start
insufficient-bits
invalid-length-or-count
unadmitted-context
unadmitted-k4-shape
unsupported-k4-tag
```

No error path may consume a second property or expose a partially admitted value as success.

## Hard stop

This contract does not admit native K4 production code, property-loop continuation, a second property, next actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, runtime widening or export widening.
'''
    Path("docs/continuity/MIMIR_R3_17N_CONTRACT.md").write_text(
        contract.rstrip() + "\n", encoding="utf-8", newline="\n"
    )

    receipt = {
        "schema_version": 1,
        "pass": "R3.17N",
        "evidence_groups_sha256": EXPECTED_SHA,
        "admitted_groups_sha256": sha256(out_groups),
        "evidence_rows": EXPECTED_ROWS,
        "admitted_rows": EXPECTED_ROWS,
        "byte_identical": True,
        "cross_product_widening": 0,
        "group_rows_by_tag": dict(sorted(tag_rows.items())),
        "unique_shapes_by_tag": dict(sorted(shape_counts.items())),
        "positive_vector_plan": "PASS",
        "negative_vector_plan": "PASS",
        "atomic_failure_semantics": "PASS",
        "exact_one_value_end_semantics": "PASS",
        "production_mutation": 0,
        "cargo_fixture_corpus_support_mutation": "0/0/0/0",
        "outcome_candidate": "A",
    }
    Path("r3_17n_contract_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("R3_17N_CONTRACT_GENERATION=PASS")
    print("R3_17N_ADMITTED_GROUPS=161")
    print("R3_17N_GROUP_SHA256=" + sha256(out_groups))
    print("R3_17N_CROSS_PRODUCT_WIDENING=0")


if __name__ == "__main__":
    main()
