from __future__ import annotations

import json
from pathlib import Path

BASE_SHA = "2e27638812111f73d06ef9e52955f10a26cfebd4"
EVIDENCE_HEAD = "4cd21ea6db14c9becc11c17149af9201071859bc"
EVIDENCE_RUN = 31792028292
EVIDENCE_JOB = 94740870175
ARTIFACT_ID = 9216016802
ARTIFACT_SHA256 = "59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, found {count}: {old!r}")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")


def write_clean(path: Path, content: str) -> None:
    lines = [line.rstrip() for line in content.strip().splitlines()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


handbook = Path("MIMIR_CONTINUE_HERE.md")
replace_once(
    handbook,
    "LAST_COMPLETED_CONTINUITY_CHECK:\n  R3.16C — post-implementation continuity repair and capability-boundary check\n\nCURRENT_PASS:\n  R3.17B — primitive scalar attribute contract admission\n\nCURRENT_PASS_TYPE:\n  contract-only / docs-state / NO production Rust change",
    "LAST_COMPLETED_CONTINUITY_CHECK:\n  R3.16C — post-implementation continuity repair and capability-boundary check\n\nLAST_COMPLETED_CONTRACT_PASS:\n  R3.17B — primitive scalar attribute wire contract / Outcome A\n\nCURRENT_PASS:\n  R3.17C — primitive scalar attribute decoder implementation\n\nCURRENT_PASS_TYPE:\n  production implementation / one-scalar decoder / bounded additive change",
)
replace_once(
    handbook,
    "R3_17B_CONTRACT_SCOPE:\n  admit only Boolean / Byte / Enum / Float / Int / Int64 scalar wire contracts",
    "R3_17B_ADMITTED_CONTRACT:\n  Boolean / Byte / Enum / Float / Int / Int64 scalar wire contracts",
)
replace_once(
    handbook,
    "R3_17B_HARD_STOP:\n  production Rust unchanged\n  no native scalar payload implementation yet\n  no RigidBody / ActiveActor / spatial-family contract or implementation\n  no second property, actor, or frame iteration\n  no lifecycle mutation\n  no raw-state/event/skill/runtime/export widening\n  no Cargo or corpus change\n\nNEXT PASS IF R3.17B OUTCOME A:\n  R3.17C — primitive scalar attribute decoder implementation",
    "R3_17C_IMPLEMENTATION_SCOPE:\n  add one narrow native scalar decoder from payload_start_bit + admitted attribute tag\n  reuse the existing private LSB-first NetworkBitCursor and atomic read_bits_le rule\n  decode exactly one Boolean / Byte / Enum / Float / Int / Int64 payload\n  preserve Float raw u32 bits plus f32 interpretation\n  return exact payload start/end/width and stop exactly after that scalar\n\nR3_17C_HARD_STOP:\n  no RigidBody / ActiveActor / spatial-family decoder\n  no property-loop continuation or second property\n  no next actor or next frame iteration\n  no lifecycle mutation\n  no raw-state/event/skill/runtime/export widening\n  no Cargo dependency or replay corpus change\n\nNEXT PASS IF R3.17C OUTCOME A:\n  R3.17D — primitive scalar native differential",
)

knowledge_graph = r'''# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

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
R3.17B decision                         |
R3.17C execution spec                   |
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
7. `docs/continuity/MIMIR_R3_17B_DECISION.md`
8. `docs/continuity/MIMIR_R3_17C_EXECUTION_SPEC.md`
9. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
10. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
11. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
12. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
13. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
14. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
15. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

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
  -> R3.17B primitive scalar wire contract: CLOSED / Outcome A
       Boolean=1, Byte=8, Enum=11, Float=32, Int=32, Int64=64 bits
       LSB-first, unaligned starts allowed, atomic truncation failure
  -> R3.17C primitive scalar native decoder: ACTIVE
```

## R3.17B admitted scalar contract

```text
Boolean   1 bit   bool
Byte      8 bits  u8
Enum      11 bits u16 numeric 0..=2047
Float     32 bits raw u32 identity + f32::from_bits interpretation
Int       32 bits signed i32 from identical two's-complement bit pattern
Int64     64 bits signed i64 from identical two's-complement bit pattern
```

All values begin exactly at `payload_start_bit`, use the existing LSB-first network cursor, require no byte alignment, consume exactly the admitted width on success, and fail without cursor advance on truncation. Unsupported/compound tags are outside the contract and must not consume payload bits.

## Current capability lock

MIMIR production still stops at `payload_start_bit`. R3.17B admits a contract only; it does not itself decode payload bits.

R3.17C may add exactly one scalar decoder for the six admitted tags. It may not continue to a second property, actor or frame, and may not decode spatial or compound attribute families.

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
write_clean(Path("MIMIR_KNOWLEDGE_GRAPH.md"), knowledge_graph)

current_state = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Pre-contract canonical main:** `{BASE_SHA}`
**Production code checkpoint:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Production milestone:** `R3.16B — native existing-actor first-property envelope header implementation`
**Completed evidence pass:** `R3.17A — Outcome A`
**Completed contract pass:** `R3.17B — Outcome A`
**Current exact pass:** `R3.17C — primitive scalar attribute decoder implementation`

---

## 1. Truthful production boundary

Production behavior is still unchanged from R3.16B at this continuity checkpoint. MIMIR resolves one existing-actor property header through `stream_id`, inherited/static property lookup, object/tag identity and `payload_start_bit`, then stops before consuming the attribute payload.

R3.17A supplied evidence and R3.17B admitted the wire contract. Neither pass by itself grants runtime decode capability.

## 2. R3.17A immutable evidence authority

```text
canonical evidence base       ded95e8ae512876b46453585be05b8358025314a
evidence head                 {EVIDENCE_HEAD}
workflow run/job              {EVIDENCE_RUN} / {EVIDENCE_JOB}  SUCCESS
exact-head normal CI          31792028275 / 94740869974  SUCCESS
artifact id                   {ARTIFACT_ID}
artifact zip SHA-256          {ARTIFACT_SHA256}
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

## 3. R3.17B admitted primitive scalar contract

```text
Boolean   width 1    semantic bool
Byte      width 8    semantic u8
Enum      width 11   numeric u16, 0..=2047; no enum-name mapping
Float     width 32   exact raw u32 identity + f32::from_bits(raw)
Int       width 32   signed i32 using the identical two's-complement bit pattern
Int64     width 64   signed i64 using the identical two's-complement bit pattern
```

Common rule: start exactly at `payload_start_bit`, consume LSB-first with no byte-alignment requirement, and advance exactly the admitted fixed width on success. If fewer than the required bits remain, fail closed with zero cursor advance. A tag outside this six-tag family is unsupported and consumes zero payload bits.

Float raw bits are part of the result contract so NaN payloads and signed zero remain bit-exact. Enum remains a numeric wire value only.

## 4. R3.17C exact implementation boundary

R3.17C may add one narrow decoder that accepts network bytes, an admitted `payload_start_bit` and the already-resolved `ReplayNetworkAttributeTagV1`, and returns exactly one typed scalar plus start/end/width metadata.

The implementation must reuse the existing private LSB-first `NetworkBitCursor` / `read_bits_le` semantics. It must not infer a second property or depend on actor lifecycle state.

Expected value semantics:

```text
Boolean(bool)
Byte(u8)
Enum(u16)
Float {{ raw_bits: u32, value: f32 }}
Int(i32)
Int64(i64)
```

A successful decoder stops exactly at `payload_end_bit = payload_start_bit + width`. Poison bits after that point remain unread.

## 5. Still closed

```text
RigidBody / ActiveActor / spatial payload families
property-loop continuation / second property
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
Cargo dependency changes
replay corpus changes
```

Outcome A for R3.17C opens `R3.17D — primitive scalar native differential` against the frozen R3.17A witness authority.
'''
write_clean(Path("docs/continuity/MIMIR_CURRENT_STATE.md"), current_state)

state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
if state.get("current_pass") != "R3.17B":
    raise SystemExit(f"unexpected current_pass: {state.get('current_pass')!r}")
state["current_pass"] = "R3.17C"
state["current_pass_kind"] = "production implementation / primitive scalar one-value decoder"
state["current_pass_goal"] = "Implement the admitted Boolean/Byte/Enum/Float/Int/Int64 one-scalar decoder from payload_start_bit using the existing LSB-first cursor, with exact value representation and atomic truncation behavior."
state["current_pass_stop_boundary"] = "Decode at most one admitted primitive scalar and stop at its exact payload_end_bit; no second property, actor/frame iteration, lifecycle mutation, spatial/compound payloads, raw-state/event/skill/runtime/export widening, Cargo change or corpus change."
state["last_completed_contract_pass"] = "R3.17B"
state["r3_17b"] = {
    "outcome": "A — admitted / contract complete",
    "production_source_changed": False,
    "production_code_sha": "ebc0fa31ba90a8496c3d1719e436d2c17b605ff7",
    "continuity_base_sha": BASE_SHA,
    "evidence_head_sha": EVIDENCE_HEAD,
    "evidence_run": EVIDENCE_RUN,
    "evidence_job": EVIDENCE_JOB,
    "artifact_id": ARTIFACT_ID,
    "artifact_sha256": ARTIFACT_SHA256,
    "contracts": {
        "Boolean": {"width_bits": 1, "semantic": "bool"},
        "Byte": {"width_bits": 8, "semantic": "u8"},
        "Enum": {"width_bits": 11, "semantic": "u16 numeric 0..=2047"},
        "Float": {"width_bits": 32, "semantic": "raw u32 identity + f32::from_bits"},
        "Int": {"width_bits": 32, "semantic": "i32 two's-complement bit pattern"},
        "Int64": {"width_bits": 64, "semantic": "i64 two's-complement bit pattern"},
    },
    "lsb_first": True,
    "byte_alignment_required": False,
    "atomic_truncation_failure": True,
    "unsupported_tag_zero_consumption": True,
    "next_pass": "R3.17C",
}
for item in [
    "docs/continuity/MIMIR_R3_17B_DECISION.md",
    "docs/continuity/MIMIR_R3_17C_EXECUTION_SPEC.md",
]:
    if item not in state["next_files_to_read"]:
        state["next_files_to_read"].append(item)
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

r317b_decision = f'''# MIMIR — R3.17B Contract Admission Decision

**Date:** 2026-08-14
**Pass:** `R3.17B — primitive scalar attribute contract admission`
**Outcome:** **A — ADMITTED / CONTRACT COMPLETE**
**Pass kind:** docs-only contract admission
**Production Rust changed:** **NO**

## Frozen authorities

```text
canonical continuity base    {BASE_SHA}
production code checkpoint   ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
R3.17A evidence head         {EVIDENCE_HEAD}
R3.17A workflow run/job      {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.17A artifact              {ARTIFACT_ID}
R3.17A artifact SHA-256      {ARTIFACT_SHA256}
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
full scalar oracle SHA-256   af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1
96-witness SHA-256           b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
aggregate SHA-256            b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e
receipt stream               PASS
```

R3.17A observed 2,141,139 primitive scalar payloads over the exact 47-replay supported lane with zero shape mismatches, zero bit-monotonicity failures and zero unexpected tag shapes.

## Contract admitted

Exactly six primitive scalar tags are admitted:

```text
Boolean   width 1    wire 0/1                 semantic bool
Byte      width 8    unsigned                 semantic u8
Enum      width 11   unsigned numeric         storage u16, range 0..=2047
Float     width 32   exact raw u32 pattern    semantic f32::from_bits(raw)
Int       width 32   exact raw 32-bit pattern semantic i32 two's-complement
Int64     width 64   exact raw 64-bit pattern semantic i64 two's-complement
```

The common cursor contract is:

```text
start = payload_start_bit
byte alignment is NOT required
read exactly the admitted width in the existing LSB-first network order
if fewer than width bits remain: fail closed and consume 0 bits
on success: end = start + width
unsupported/non-admitted tag: fail without consuming payload bits
```

Float result identity includes the raw `u32` bit pattern. An `f32` value alone is not sufficient for exact equality because NaN payloads and signed zero are bit-sensitive.

Enum is a numeric 11-bit value only. R3.17B does not admit an engine enum-name registry.

## Integration policy for R3.17C

R3.17C must be additive and must reuse the existing private `NetworkBitCursor` semantics. The preferred seam is a one-scalar decoder receiving:

```text
network bytes
payload_start_bit
already-resolved ReplayNetworkAttributeTagV1
```

and returning exactly one typed scalar plus exact start/end/width metadata.

Unless fresh source truth proves otherwise, production change scope is limited to:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17c_scalar_attribute_decoder.rs
```

Forbidden in R3.17C:

```text
Cargo.toml / Cargo.lock changes
external parser dependency
support-lane widening
RigidBody / ActiveActor / Location / spatial-family decode
property-loop continuation or second property
next actor or next frame iteration
actor lifecycle mutation
raw state / events / skills / runtime / export widening
```

## Outcome

No contract ambiguity or contradiction was found between R3.17A authority and canonical production cursor behavior. Outcome A is admitted.

## Next exact pass

`R3.17C — primitive scalar attribute decoder implementation`.
'''
write_clean(Path("docs/continuity/MIMIR_R3_17B_DECISION.md"), r317b_decision)

r317c_spec = f'''# MIMIR — R3.17C Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17C — primitive scalar attribute decoder implementation`
**Kind:** production implementation / bounded additive decoder
**Canonical implementation base:** `{BASE_SHA}` plus admitted R3.17B docs-only continuity commit
**Production code checkpoint before pass:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Evidence authority:** `{EVIDENCE_HEAD}`, run `{EVIDENCE_RUN}`, job `{EVIDENCE_JOB}`

## 1. Goal

Implement exactly one native primitive-scalar payload decoder for the six R3.17B-admitted tags:

```text
Boolean
Byte
Enum
Float
Int
Int64
```

The decoder begins at an already-resolved `payload_start_bit` and stops exactly after that one scalar. It does not own property-loop, actor-loop or frame-loop control flow.

## 2. Production seam

The existing R3.16B header already returns:

```text
resolved_attribute_tag: Option<ReplayNetworkAttributeTagV1>
payload_start_bit: Option<u64>
```

R3.17C should add an independent narrow decoder equivalent in meaning to:

```text
decode_replay_network_primitive_scalar_v1(
    network_bytes,
    payload_start_bit,
    attribute_tag,
) -> Result<ReplayNetworkPrimitiveScalarDecodeV1>
```

Exact Rust names may vary if source layout requires it, but the API must remain one-scalar and context-injected. Do not make the decoder rediscover actor/property context.

## 3. Required result semantics

Add a typed scalar value equivalent in meaning to:

```text
Boolean(bool)
Byte(u8)
Enum(u16)
Float {{ raw_bits: u32, value: f32 }}
Int(i32)
Int64(i64)
```

and a result envelope containing at least:

```text
attribute_tag
payload_start_bit
payload_end_bit
payload_width
value
stop_bit == payload_end_bit
```

For Float, raw `u32` identity is mandatory in addition to `f32` interpretation.

## 4. Wire rules

```text
Boolean  width 1
Byte     width 8
Enum     width 11
Float    width 32
Int      width 32
Int64    width 64
```

All reads are LSB-first through the existing `NetworkBitCursor`. No byte alignment may be assumed.

Signed integers are obtained from the exact raw bit pattern using two's-complement reinterpretation. Float is obtained with `f32::from_bits(raw_u32)`.

## 5. Atomic failure contract

Before success the decoder must not partially advance observable state.

Required failures:

- `payload_start_bit` outside network length;
- insufficient bits for the selected admitted width;
- unsupported/compound attribute tag.

All failures consume zero payload bits. The implementation may use a private local cursor because the public API is start-offset based; nevertheless truncation must preserve the existing atomic `read_bits_le` semantics.

## 6. Required focused tests

At minimum:

- aligned and unaligned start offsets for all six tags;
- exact `payload_end_bit = payload_start_bit + width`;
- `stop_bit == payload_end_bit`;
- Boolean `0` and `1`;
- Byte `0` and `255`;
- Enum synthetic `0` and `2047`;
- Float `+0.0`, `-0.0`, positive/negative infinity and at least one NaN payload with exact raw-bit preservation;
- Int `i32::MIN`, `-1`, `0`, `i32::MAX`;
- Int64 `i64::MIN`, `-1`, `0`, `i64::MAX`;
- every tag truncated by one bit fails;
- start exactly at network end fails for every non-zero-width tag;
- unsupported `RigidBody` and `ActiveActor` fail without reading poison bits;
- poison bits immediately after a valid scalar do not affect the decoded value or stop position;
- repeatability is exact.

## 7. Clean change scope

Expected permanent files:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17c_scalar_attribute_decoder.rs
```

No Cargo dependency, fixture, corpus, workflow, temporary evidence or continuity file belongs in the clean production commit.

## 8. Hard stop

R3.17C must not:

```text
decode RigidBody / ActiveActor / Location / Rotation / spatial families
decode strings, unique IDs, reservations, loadouts or other compound attributes
consume property_present after the scalar
iterate a second property
iterate a next actor or frame
mutate actor lifecycle state
materialize raw game state or semantic events
open replay slicing / skill / teacher / runtime / export surfaces
change Cargo dependencies
change the replay support lane or corpus
```

## 9. Validation and next pass

The clean candidate must pass focused tests, full repository verification, exact diff-scope audit and hosted CI/Knowledge Archive gates before publication.

After production publication, `R3.17D — primitive scalar native differential` must compare the native decoder against the frozen R3.17A 96-witness authority before any wider attribute family receives credit.
'''
write_clean(Path("docs/continuity/MIMIR_R3_17C_EXECUTION_SPEC.md"), r317c_spec)

# Final markdown whitespace normalization for exactly the target markdown files.
for rel in [
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_R3_17B_DECISION.md",
    "docs/continuity/MIMIR_R3_17C_EXECUTION_SPEC.md",
]:
    p = Path(rel)
    lines = [line.rstrip() for line in p.read_text(encoding="utf-8").splitlines()]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

print("R3_17B_CONTRACT_SYNC=PASS")
