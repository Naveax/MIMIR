from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_BASE = "ded95e8ae512876b46453585be05b8358025314a"
PRODUCTION_SHA = "ebc0fa31ba90a8496c3d1719e436d2c17b605ff7"
EVIDENCE_HEAD = "4cd21ea6db14c9becc11c17149af9201071859bc"

# Master handbook: replace only the canonical current-state code block.
continue_path = ROOT / "MIMIR_CONTINUE_HERE.md"
text = continue_path.read_text(encoding="utf-8")
heading = "# 1. CANONICAL CURRENT STATE BLOCK"
start_heading = text.index(heading)
code_start = text.index("```text", start_heading)
code_end = text.index("```", code_start + len("```text"))
block = '''```text
REPOSITORY: Naveax/MIMIR
DEFAULT_BRANCH: main
LANGUAGE: Rust 2024 workspace
RUST_VERSION_FLOOR: 1.85

LAST_PRODUCTION_CODE_SHA:
  ebc0fa31ba90a8496c3d1719e436d2c17b605ff7

LAST_PRODUCTION_MILESTONE:
  R3.16B — native existing-actor first-property envelope header implementation

LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.17A — primitive scalar attribute wire-format evidence / Outcome A

LAST_COMPLETED_CONTINUITY_CHECK:
  R3.16C — post-implementation continuity repair and capability-boundary check

CURRENT_PASS:
  R3.17B — primitive scalar attribute contract admission

CURRENT_PASS_TYPE:
  contract-only / docs-state / NO production Rust change

CURRENT_SUPPORTED_REPLAY_LANE:
  47 replays

CHECKED_IN_REPLAY_SET:
  103 total = 3 historical fixtures + largest_100 stress corpus

PINNED_BOXCARS_ORACLE:
  repository: nickbabcock/boxcars
  exact SHA: c70e77df7af81b436cb545d070bb90c82f562d0b

CURRENT_PRODUCTION_HARD_STOP:
  existing-actor first-property header stops exactly at payload_start_bit
  NO native attribute payload bit is admitted yet

R3_17A_AUTHORITY:
  canonical evidence base: ded95e8ae512876b46453585be05b8358025314a
  evidence head: 4cd21ea6db14c9becc11c17149af9201071859bc
  evidence run/job: 31792028292 / 94740870175 SUCCESS
  exact-head normal CI: 31792028275 / 94740869974 SUCCESS
  artifact: 9216016802
  artifact SHA256: 59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
  replay identity rows: 47
  bounded witness rows: 96
  scalar occurrences: 2,141,139
  receipt stream: PASS
  production mutation: 0
  Cargo mutation: 0
  corpus mutation: 0

R3_17A_OBSERVED_FIXED_WIDTHS:
  Boolean: 84,545 occurrences / 47 replays / 1 bit
  Byte: 1,730,595 occurrences / 47 replays / 8 bits
  Enum: 180,624 occurrences / 47 replays / 11 bits
  Float: 33,857 occurrences / 47 replays / 32 bits
  Int: 109,920 occurrences / 47 replays / 32 bits
  Int64: 1,598 occurrences / 14 replays / 64 bits
  shape mismatch: 0
  bit monotonicity failure: 0
  unexpected tag shape: 0

R3_17B_CONTRACT_SCOPE:
  admit only Boolean / Byte / Enum / Float / Int / Int64 scalar wire contracts
  LSB-first from the current payload_start_bit; no byte-alignment assumption
  fixed-width exact cursor consumption
  Float preserves raw u32 bits alongside f32 interpretation
  signed integer interpretation follows the pinned oracle source contract
  truncation and unsupported-tag failure must be atomic / zero-consumption

R3_17B_HARD_STOP:
  production Rust unchanged
  no native scalar payload implementation yet
  no RigidBody / ActiveActor / spatial-family contract or implementation
  no second property, actor, or frame iteration
  no lifecycle mutation
  no raw-state/event/skill/runtime/export widening
  no Cargo or corpus change

NEXT PASS IF R3.17B OUTCOME A:
  R3.17C — primitive scalar attribute decoder implementation
```'''
text = text[:code_start] + block + text[code_end + 3:]
continue_path.write_text(text, encoding="utf-8", newline="\n")

current_state = '''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Pre-admission canonical main:** `ded95e8ae512876b46453585be05b8358025314a`
**Production code checkpoint:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Production milestone:** `R3.16B — native existing-actor first-property envelope header implementation`
**Completed evidence pass:** `R3.17A — Outcome A`
**Current exact pass:** `R3.17B — primitive scalar attribute contract admission`

---

## 1. Truthful production boundary

Production behavior is unchanged from R3.16B. MIMIR can resolve one existing-actor property header through `stream_id`, inherited/static property lookup, object/tag identity and `payload_start_bit`, then stops before consuming the attribute payload.

R3.17A did not widen production. It measured the next wire layer through a pinned external oracle only.

## 2. R3.17A immutable evidence authority

```text
canonical evidence base       ded95e8ae512876b46453585be05b8358025314a
evidence head                 4cd21ea6db14c9becc11c17149af9201071859bc
workflow run/job              31792028292 / 94740870175  SUCCESS
exact-head normal CI          31792028275 / 94740869974  SUCCESS
artifact id                   9216016802
artifact zip SHA-256          59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
artifact size                 51,639,177 bytes
replay identity rows          47
bounded witness rows          96
oracle parse success          47 / 47
scalar occurrences            2,141,139
shape mismatch                0
bit monotonicity failure      0
unexpected tag shape          0
production mutation           0
Cargo mutation                0
corpus mutation               0
receipt stream                PASS
```

The bounded job-log receipt includes all 47 replay identities, 96 witnesses, aggregate/summary content and content hashes. The expiring artifact is therefore not the sole audit authority.

## 3. Observed primitive scalar family

```text
Boolean   84,545 occurrences    47 replays   width 1
Byte   1,730,595 occurrences    47 replays   width 8
Enum     180,624 occurrences    47 replays   width 11
Float     33,857 occurrences    47 replays   width 32
Int      109,920 occurrences    47 replays   width 32
Int64      1,598 occurrences    14 replays   width 64
```

All six candidate tags were observed. No candidate remains a zero-observation placeholder.

Important receipt hashes:

```text
instrumentation patch  f10fc6206aaba14b8afd368c5ede8d8ce6bc1e4a7a56049be9d7012aa8b82877
full scalar oracle     af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1
96 witnesses           b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
summary                a2f8a7c8efb87083986bb635d9c2c81e992556bbe9a41263d7bfd453c404ce2c
aggregate              b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e
```

## 4. R3.17B current contract pass

R3.17B may admit only the six evidence-backed primitive scalar wire contracts. It is docs/state only; no Rust code is modified.

The common contract is LSB-first at the existing payload cursor with no byte-alignment assumption. Successful decode consumes exactly the tag's admitted fixed width. Insufficient input or a non-admitted tag must fail atomically without advancing the cursor.

Float identity is the raw 32-bit pattern first; `f32` is its interpretation. Signed integer semantics are pinned to the oracle source contract, while the replay corpus evidence establishes the exact consumed widths on the supported lane.

## 5. Still closed

```text
native scalar payload decoder
RigidBody / ActiveActor / spatial payload families
second property / property loop
next actor iteration
next frame iteration
actor lifecycle mutation
raw-state materialization
semantic events
replay slicing
skill mining
counterfactual rollout execution
training/runtime/export widening
support-lane expansion
```

Outcome A for R3.17B opens `R3.17C — primitive scalar attribute decoder implementation`.
'''
(ROOT / "docs/continuity/MIMIR_CURRENT_STATE.md").write_text(current_state, encoding="utf-8", newline="\n")

state_path = ROOT / "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state.update({
    "updated_date": "2026-08-14",
    "last_completed_read_only_audit": "R3.17A",
    "current_pass": "R3.17B",
    "current_pass_kind": "contract-only primitive scalar attribute wire contract admission",
    "current_pass_goal": "Admit only the evidence-backed Boolean/Byte/Enum/Float/Int/Int64 wire contracts, including exact widths, representations, cursor rules and atomic truncation semantics, without changing production Rust.",
    "current_pass_stop_boundary": "No production payload decoder yet; no spatial families, property loop, actor/frame iteration, lifecycle mutation, raw-state/event/skill/runtime/export widening, Cargo change or corpus change.",
    "last_completed_evidence_pass": "R3.17A",
    "last_completed_evidence_outcome": "A — all six primitive scalar candidate tags observed; 2,141,139 total occurrences; fixed widths exact; zero shape/monotonicity/unexpected-shape errors; immutable receipt stream PASS",
})
state["r3_17a"] = {
    "outcome": "A — admitted evidence / production unchanged",
    "canonical_evidence_base": CANONICAL_BASE,
    "production_code_sha": PRODUCTION_SHA,
    "production_source_blob": "625ab2322e35f5f835871d42b9efeb04f5c299ab",
    "evidence_head_sha": EVIDENCE_HEAD,
    "workflow_run": 31792028292,
    "workflow_job": 94740870175,
    "exact_head_ci_run": 31792028275,
    "exact_head_ci_job": 94740869974,
    "artifact_id": 9216016802,
    "artifact_size_bytes": 51639177,
    "artifact_sha256": "59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af",
    "oracle_repo": "nickbabcock/boxcars",
    "oracle_sha": "c70e77df7af81b436cb545d070bb90c82f562d0b",
    "oracle_frame_decoder_blob": "6f2ff153d3a27cdacccc65e3f23851489077a7d8",
    "oracle_attributes_blob": "5e2d5bc1cd8187af30c3ea95193ad987645cb76e",
    "selector_sha256": "2ecbeea804f193796a539baee1e968719f03c0cd706efff0c22a61e6ef943dae",
    "replay_identity_sha256": "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf",
    "instrumentation_patch_sha256": "f10fc6206aaba14b8afd368c5ede8d8ce6bc1e4a7a56049be9d7012aa8b82877",
    "full_oracle_sha256": "af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1",
    "witness_sha256": "b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9",
    "summary_sha256": "a2f8a7c8efb87083986bb635d9c2c81e992556bbe9a41263d7bfd453c404ce2c",
    "aggregate_sha256": "b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e",
    "replays_total": 47,
    "oracle_decode_success": 47,
    "scalar_occurrences_total": 2141139,
    "witness_rows": 96,
    "tags": {
        "Boolean": {"occurrences": 84545, "replays": 47, "width_bits": 1, "witnesses": 16},
        "Byte": {"occurrences": 1730595, "replays": 47, "width_bits": 8, "witnesses": 16},
        "Enum": {"occurrences": 180624, "replays": 47, "width_bits": 11, "witnesses": 16},
        "Float": {"occurrences": 33857, "replays": 47, "width_bits": 32, "witnesses": 16},
        "Int": {"occurrences": 109920, "replays": 47, "width_bits": 32, "witnesses": 16},
        "Int64": {"occurrences": 1598, "replays": 14, "width_bits": 64, "witnesses": 16},
    },
    "shape_mismatch_count": 0,
    "bit_monotonicity_failure_count": 0,
    "unexpected_tag_shape_count": 0,
    "production_mutation_count": 0,
    "cargo_mutation_count": 0,
    "corpus_mutation_count": 0,
    "receipt_stream": "PASS",
    "next_pass": "R3.17B",
}
reads = list(state.get("next_files_to_read", []))
for item in [
    "docs/continuity/MIMIR_R3_17A_DECISION.md",
    "docs/continuity/MIMIR_R3_17B_EXECUTION_SPEC.md",
]:
    if item not in reads:
        reads.append(item)
state["next_files_to_read"] = reads
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

graph = '''# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

> **Role:** Root cross-link and verification graph for all MIMIR knowledge sources.
>
> Current source/tests and exact-SHA evidence outrank prose. `MIMIR_CONTINUE_HERE.md` remains the execution handbook.

## Canonical graph

```text
fresh GitHub source/tests + exact-SHA evidence
        |
        v
MIMIR_CONTINUE_HERE.md
        |
        +-------------------------------+
        |                               |
        v                               v
docs/continuity/                MIMIR_ALL_SOURCES_SUPERBOOK.md
CURRENT_STATE + STATE.json              |
R3.17A decision                         |
R3.17B execution spec                   |
        |                               |
        +---------------+---------------+
                        |
                        v
docs/chatgpt-archive/SOURCE_REGISTRY.md
                        |
                        v
docs/chatgpt-archive/VALIDATION_MATRIX.md
                        |
                        v
docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md
                        |
                        v
scripts/verify_mimir_knowledge_archive.ps1
```

## Mandatory reading order

1. `MIMIR_CONTINUE_HERE.md`
2. `docs/continuity/MIMIR_CONTINUITY_STATE.json`
3. `docs/continuity/MIMIR_CURRENT_STATE.md`
4. `docs/continuity/MIMIR_R3_17A_EXECUTION_SPEC.md`
5. `docs/continuity/MIMIR_R3_17A_DECISION.md`
6. `docs/continuity/MIMIR_R3_17B_EXECUTION_SPEC.md`
7. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
8. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
9. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
10. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
11. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
12. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
13. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
  -> R3.14A-E bit cursor + first actor envelope evidence/production/audit
  -> R3.15A-D NewActor evidence/contract/implementation/differential
  -> R3.16A first existing-actor property-header evidence: 47/47
  -> R3.16B production property-header reader: ADMITTED
       production SHA ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
       exact hard stop payload_start_bit
  -> R3.16C continuity/check: CLOSED / Outcome A
  -> R3.17A primitive scalar wire-format evidence: CLOSED / Outcome A
       2,141,139 scalar observations
       47 replay identities + 96 bounded witnesses frozen in immutable job log
  -> R3.17B primitive scalar wire contract: ACTIVE
```

## R3.17A observed scalar shapes

```text
Boolean   1 bit    84,545 occurrences    47 replays
Byte      8 bits   1,730,595 occurrences 47 replays
Enum      11 bits  180,624 occurrences   47 replays
Float     32 bits  33,857 occurrences    47 replays
Int       32 bits  109,920 occurrences   47 replays
Int64     64 bits  1,598 occurrences     14 replays
```

There were zero scalar shape mismatches, zero bit-monotonicity failures and zero unexpected scalar widths on the exact supported lane.

## Current capability lock

MIMIR still stops at `payload_start_bit`. R3.17A proves wire evidence; it does not add a native payload decoder.

R3.17B is contract-only. It may admit the six observed scalar wire contracts, exact LSB-first widths, value representations and atomic truncation behavior. It cannot admit spatial/compound tags or production decoding.

## R3.17A evidence identity

```text
evidence head             4cd21ea6db14c9becc11c17149af9201071859bc
run/job                    31792028292 / 94740870175 SUCCESS
artifact                   9216016802
artifact SHA256            59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
full oracle SHA256         af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1
witness SHA256             b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
aggregate SHA256           b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e
receipt stream             PASS
```

## Authority rule

```text
current code/tests
> exact-SHA CI/evidence + immutable receipt stream
> MIMIR_CONTINUE_HERE.md
> docs/continuity/MIMIR_CONTINUITY_STATE.json
> docs/continuity/MIMIR_CURRENT_STATE.md
> admitted decision / active pass specs
> boundary locks
> roadmap
> historical artifacts/chat memory
```

## Verification

Run `scripts/verify_mimir_knowledge_archive.ps1`. The root graph intentionally preserves links to `MIMIR_ALL_SOURCES_SUPERBOOK.md`, `docs/chatgpt-archive/SOURCE_REGISTRY.md`, `docs/chatgpt-archive/VALIDATION_MATRIX.md`, `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`, and the verifier itself.
'''
(ROOT / "MIMIR_KNOWLEDGE_GRAPH.md").write_text(graph, encoding="utf-8", newline="\n")

r317a_decision = '''# MIMIR — R3.17A Decision

**Date:** 2026-08-14
**Outcome:** `A — primitive scalar wire evidence exact / admitted`
**Production source changed:** `NO`
**Production code checkpoint remains:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`

## Decision

The primitive scalar evidence pass is admitted. All six candidate scalar tags were observed in the exact supported 47-replay lane, and every observed payload consumed one fixed width matching the pinned Boxcars source behavior.

R3.17A is evidence only. It does not grant MIMIR a native scalar payload decoder.

## Frozen authority

```text
canonical evidence base    ded95e8ae512876b46453585be05b8358025314a
evidence head              4cd21ea6db14c9becc11c17149af9201071859bc
workflow run/job           31792028292 / 94740870175 SUCCESS
exact-head normal CI       31792028275 / 94740869974 SUCCESS
artifact id                9216016802
artifact size              51,639,177 bytes
artifact SHA-256           59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
oracle                     nickbabcock/boxcars @ c70e77df7af81b436cb545d070bb90c82f562d0b
frame_decoder.rs blob      6f2ff153d3a27cdacccc65e3f23851489077a7d8
attributes.rs blob         5e2d5bc1cd8187af30c3ea95193ad987645cb76e
selector SHA-256           2ecbeea804f193796a539baee1e968719f03c0cd706efff0c22a61e6ef943dae
replay identity SHA-256    b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
replay identity rows       47
bounded witness rows       96
receipt stream             PASS
```

## Aggregate result

```text
oracle decode success      47 / 47
scalar occurrences         2,141,139
Boolean                    84,545 / 47 replays / 1 bit
Byte                       1,730,595 / 47 replays / 8 bits
Enum                       180,624 / 47 replays / 11 bits
Float                      33,857 / 47 replays / 32 bits
Int                        109,920 / 47 replays / 32 bits
Int64                      1,598 / 14 replays / 64 bits
shape mismatches           0
bit monotonicity failures  0
unexpected tag shapes      0
production mutations       0
Cargo mutations            0
corpus mutations           0
```

## Durable content hashes

```text
instrumentation patch      f10fc6206aaba14b8afd368c5ede8d8ce6bc1e4a7a56049be9d7012aa8b82877
full scalar oracle         af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1
96 witnesses               b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
summary                    a2f8a7c8efb87083986bb635d9c2c81e992556bbe9a41263d7bfd453c404ce2c
aggregate                  b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e
```

The job log permanently contains the bounded receipt stream. The one-day artifact is supplemental, not the only evidence carrier.

## Interpretation limits

- Fixed widths are admitted only for the six scalar tags above.
- Float exact identity is the raw 32-bit pattern; decimal rendering is not an exact comparison authority.
- `Int` and `Int64` signed interpretation is supported by the pinned oracle source contract; the supported replay witnesses do not need to contain every signed-domain edge case.
- `Enum` is admitted as an 11-bit numeric wire value, not as a semantic enum-name registry.
- No claim is made that compound/spatial tag families share these layouts.

## Next exact pass

`R3.17B — primitive scalar attribute contract admission`.
'''
(ROOT / "docs/continuity/MIMIR_R3_17A_DECISION.md").write_text(r317a_decision, encoding="utf-8", newline="\n")

r317b_spec = '''# MIMIR — R3.17B Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17B — primitive scalar attribute contract admission`
**Kind:** contract-only / docs-state / no production Rust
**Production code checkpoint:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Evidence authority:** `4cd21ea6db14c9becc11c17149af9201071859bc`, run `31792028292`, job `94740870175`

## 1. Goal

Freeze the smallest implementation contract justified by R3.17A for exactly these six tags:

```text
Boolean
Byte
Enum
Float
Int
Int64
```

This pass admits a wire contract, not executable decoding capability.

## 2. Common cursor contract

All six scalar values begin at the already-admitted `payload_start_bit` and use the existing replay network LSB-first bit order.

There is **no byte-alignment precondition**. A scalar may begin at any valid bit offset.

For an admitted tag with required width `W`:

```text
start = payload_start_bit
if total_bits - start < W:
    fail closed
    consume 0 bits
    return no value
else:
    consume exactly W bits LSB-first
    end = start + W
    return typed value + exact start/end/width metadata
```

Failure must be atomic. This matches the existing private `NetworkBitCursor::read_bits_le` boundary rule, which checks the complete range before advancing the cursor.

A tag outside this six-tag contract fails without consuming payload bits.

## 3. Admitted scalar wire contracts

### Boolean

```text
width: 1 bit
wire value: 0 or 1
semantic value: bool
```

### Byte

```text
width: 8 bits
wire value: unsigned 8-bit
semantic value: u8
```

### Enum

```text
width: 11 bits
wire value: unsigned 11-bit numeric value
storage type: u16
range permitted by width: 0..=2047
```

R3.17B does not map the numeric value to an engine enum name.

### Float

```text
width: 32 bits
exact identity: raw u32 bit pattern
semantic interpretation: f32::from_bits(raw)
```

The raw `u32` is mandatory in the result contract. `f32` comparison alone is insufficient because NaN payloads and signed zero require bit-exact identity.

### Int

```text
width: 32 bits
exact wire pattern: 32 raw bits
semantic interpretation: signed i32 using the same two's-complement bit pattern
```

### Int64

```text
width: 64 bits
exact wire pattern: 64 raw bits
semantic interpretation: signed i64 using the same two's-complement bit pattern
```

## 4. Proposed implementation result shape for R3.17C

The later implementation should expose an additive narrow value type equivalent in meaning to:

```text
Boolean(bool)
Byte(u8)
Enum(u16)
Float { raw_bits: u32, value: f32 }
Int(i32)
Int64(i64)
```

and an envelope containing at least:

```text
attribute_tag
payload_start_bit
payload_end_bit
payload_width
value
explicit stop reason / one-scalar boundary
```

Exact Rust names remain an implementation choice, but semantics above are fixed by this contract.

## 5. Required R3.17C implementation tests

At minimum:

- aligned and unaligned start offsets for every admitted tag;
- exact end offset equals `start + width`;
- Boolean 0/1;
- Byte 0/255;
- Enum 0/2047 synthetic boundaries plus evidence witnesses;
- Float raw-bit preservation, including `+0.0`, `-0.0`, infinities and at least one NaN payload synthetically;
- Int `i32::MIN`, `-1`, `0`, `i32::MAX` synthetically;
- Int64 `i64::MIN`, `-1`, `0`, `i64::MAX` synthetically;
- truncation at every `width - 1` boundary fails with zero cursor advance;
- unsupported/compound tag fails with zero cursor advance;
- poison bits after the scalar remain unread;
- no second property/actor/frame consumption.

R3.17D must later perform native differential comparison against the frozen R3.17A witness set before wider attribute decoding is credited.

## 6. Explicitly not admitted

```text
RigidBody
ActiveActor
Location / rotation / spatial families
UniqueId / reservation / product structures
string-like or object-reference payloads
private/loadout/party/team paint compound payloads
property-loop continuation
second property
next actor
next frame
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
```

## 7. Outcome rules

### Outcome A

The six scalar contracts, common cursor rule, representations and fail-closed semantics are accepted without production mutation.

Open `R3.17C — primitive scalar attribute decoder implementation`.

### Outcome B

A contract ambiguity is found that cannot be resolved from the frozen evidence/source. Open the smallest tag-specific evidence follow-up; do not implement the ambiguous tag.

### Outcome C

The proposed contract contradicts canonical production cursor behavior or R3.17A authority. Stop and reopen the conflicting earlier pass.

## 8. Hard stop

R3.17B changes no production Rust, Cargo dependency, fixture or replay corpus. It grants no runtime decoding capability.
'''
(ROOT / "docs/continuity/MIMIR_R3_17B_EXECUTION_SPEC.md").write_text(r317b_spec, encoding="utf-8", newline="\n")

print("R3_17A_ADMISSION_SYNC=PASS")
