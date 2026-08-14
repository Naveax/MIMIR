from __future__ import annotations

import json
from pathlib import Path

PROD_BASE = "85430b9eedb3bf16d66abcd895d68fbc7217818e"
PROD_SHA = "c3d4c73ca34febb9f0383c59132a8bc8a363b06b"
SOURCE_BLOB = "54e1bfb918ec1bd42a61cfa0131ca27412082ac5"
TEST_BLOB = "0293831df88723d6cf1e7fd13870bec6108d383a"
EVIDENCE_HEAD = "4cd21ea6db14c9becc11c17149af9201071859bc"
EVIDENCE_RUN = 31792028292
EVIDENCE_JOB = 94740870175


def clean_write(path: Path, content: str) -> None:
    lines = [line.rstrip() for line in content.strip().splitlines()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


handbook = Path("MIMIR_CONTINUE_HERE.md")
text = handbook.read_text(encoding="utf-8")
section = text.index("# 1. CANONICAL CURRENT STATE BLOCK")
block_start = text.index("```text", section)
block_end = text.index("```", block_start + len("```text")) + 3
new_block = f'''```text
REPOSITORY: Naveax/MIMIR
DEFAULT_BRANCH: main
LANGUAGE: Rust 2024 workspace
RUST_VERSION_FLOOR: 1.85

LAST_PRODUCTION_CODE_SHA:
  {PROD_SHA}

LAST_PRODUCTION_MILESTONE:
  R3.17C — native primitive scalar attribute decoder implementation

LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.17A — primitive scalar attribute wire-format evidence / Outcome A

LAST_COMPLETED_CONTINUITY_CHECK:
  R3.16C — post-implementation continuity repair and capability-boundary check

LAST_COMPLETED_CONTRACT_PASS:
  R3.17B — primitive scalar attribute wire contract / Outcome A

CURRENT_PASS:
  R3.17D — primitive scalar native differential

CURRENT_PASS_TYPE:
  evidence-only / exact native-vs-oracle differential / NO production Rust change

CURRENT_SUPPORTED_REPLAY_LANE:
  47 replays

CHECKED_IN_REPLAY_SET:
  103 total = 3 historical fixtures + largest_100 stress corpus

PINNED_BOXCARS_ORACLE:
  repository: nickbabcock/boxcars
  exact SHA: c70e77df7af81b436cb545d070bb90c82f562d0b

CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved primitive scalar payload may be decoded natively
  stop exactly at payload_end_bit / stop_bit after that one scalar
  NO second property, next actor, next frame, compound or spatial attribute is admitted

R3_17A_AUTHORITY:
  evidence head: {EVIDENCE_HEAD}
  evidence run/job: {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
  replay identity rows: 47
  bounded scalar witness rows: 96
  scalar observations: 2,141,139
  receipt stream: PASS

R3_17B_ADMITTED_CONTRACT:
  Boolean=1 bit / Byte=8 / Enum=11 / Float=32 / Int=32 / Int64=64
  LSB-first, no byte-alignment assumption, fixed-width exact consumption
  Float identity includes raw u32 bits; signed integer semantics preserve bit patterns
  truncation and unsupported tags fail without widening the cursor boundary

R3_17C_PRODUCTION_CLOSURE:
  base: {PROD_BASE}
  production SHA: {PROD_SHA}
  source Git blob: {SOURCE_BLOB}
  focused test Git blob: {TEST_BLOB}
  clean diff: exactly 2 files, +465/-0
  focused tests: 11/11 PASS
  disposable implementation run/job: 31795745652 / 94752360261 SUCCESS
  candidate CI: 31796122522 / 94753517283 SUCCESS
  candidate Knowledge Archive: 31796266602 / 94753955749 SUCCESS
  published-main CI: 31796509896 / 94754670068 SUCCESS
  published-main Knowledge Archive: 31796560814 / 94754827522 SUCCESS

R3_17D_OPEN_BOUNDARY:
  recover the immutable R3.17A 96-witness receipt from exact job logs
  run the native R3.17C decoder on the same replay/network bit positions and admitted tags
  compare exact tag, start/end/width, scalar value, Float raw bits and stop_bit
  require 96/96 exact equality and zero production/Cargo/corpus mutation

R3_17D_HARD_STOP:
  no production Rust change
  no second property / property loop continuation
  no RigidBody / ActiveActor / spatial or compound decoder
  no actor/frame iteration or lifecycle mutation
  no raw-state/event/skill/runtime/export widening
  no support-lane, Cargo or corpus change

NEXT PASS IF R3.17D OUTCOME A:
  select the next bounded attribute-family pass from the execution roadmap; do not widen by analogy
```'''
clean_write(handbook, text[:block_start] + new_block + text[block_end:])

knowledge = f'''# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

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
R3.17A evidence/decision                |
R3.17B contract decision                |
R3.17C production decision              |
R3.17D execution spec                   |
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
4. `docs/continuity/MIMIR_R3_17A_DECISION.md`
5. `docs/continuity/MIMIR_R3_17B_DECISION.md`
6. `docs/continuity/MIMIR_R3_17C_EXECUTION_SPEC.md`
7. `docs/continuity/MIMIR_R3_17C_DECISION.md`
8. `docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md`
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
 -> R3.14 actor envelope primitives
 -> R3.15 NewActor branch
 -> R3.16 existing-actor first-property header, hard stop payload_start_bit
 -> R3.17A primitive scalar evidence: Outcome A / 2,141,139 observations
 -> R3.17B primitive scalar contract: Outcome A
 -> R3.17C native one-scalar decoder: PUBLISHED
      production SHA {PROD_SHA}
      source blob {SOURCE_BLOB}
      11/11 focused tests
      hard stop payload_end_bit after one scalar
 -> R3.17D exact 96-witness native differential: ACTIVE
```

## Current capability lock

MIMIR may natively decode exactly one already-resolved primitive scalar payload for Boolean, Byte, Enum, Float, Int or Int64. The decoder starts at caller-supplied `payload_start_bit`, returns exact start/end/width/value metadata, and stops at that scalar's `payload_end_bit`.

It still cannot iterate a second property, next actor or next frame, mutate lifecycle state, or decode `RigidBody`, `ActiveActor`, spatial or other compound attribute families.

## R3.17C publication identity

```text
base                       {PROD_BASE}
production SHA             {PROD_SHA}
source blob                {SOURCE_BLOB}
test blob                  {TEST_BLOB}
focused                    11/11 PASS
disposable implementation  31795745652 / 94752360261 SUCCESS
candidate CI               31796122522 / 94753517283 SUCCESS
candidate knowledge        31796266602 / 94753955749 SUCCESS
published-main CI          31796509896 / 94754670068 SUCCESS
published-main knowledge   31796560814 / 94754827522 SUCCESS
```

## Authority rule

```text
current code/tests
> exact-SHA CI/evidence + immutable receipt streams
> MIMIR_CONTINUE_HERE.md
> docs/continuity/MIMIR_CONTINUITY_STATE.json
> docs/continuity/MIMIR_CURRENT_STATE.md
> admitted decision / active pass specs
> boundary locks
> roadmap
> historical artifacts/chat memory
```

## Verification

Run `scripts/verify_mimir_knowledge_archive.ps1`.
'''
clean_write(Path("MIMIR_KNOWLEDGE_GRAPH.md"), knowledge)

current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production milestone:** `R3.17C — native primitive scalar attribute decoder implementation`
**Completed evidence authority:** `R3.17A — Outcome A`
**Completed contract pass:** `R3.17B — Outcome A`
**Current exact pass:** `R3.17D — primitive scalar native differential`

## 1. Truthful production boundary

MIMIR can now decode exactly one already-resolved primitive scalar payload for:

```text
Boolean  1 bit
Byte     8 bits
Enum     11 bits
Float    32 bits, raw u32 + f32 interpretation
Int      32 bits, signed two's-complement interpretation
Int64    64 bits, signed two's-complement interpretation
```

The caller supplies `payload_start_bit` and `ReplayNetworkAttributeTagV1`. The native decoder reuses the existing LSB-first `NetworkBitCursor`, requires no byte alignment, and returns exact `payload_start_bit`, `payload_end_bit`, `payload_width`, value and `stop_bit`.

Production stops exactly after that one scalar. It does not continue the property loop.

## 2. R3.17C production identity

```text
pre-pass main                {PROD_BASE}
clean production SHA         {PROD_SHA}
production source blob       {SOURCE_BLOB}
focused test blob            {TEST_BLOB}
clean diff                   2 files, +465/-0
focused tests                11/11 PASS
disposable run/job           31795745652 / 94752360261 SUCCESS
candidate CI                 31796122522 / 94753517283 SUCCESS
candidate Knowledge          31796266602 / 94753955749 SUCCESS
published-main CI            31796509896 / 94754670068 SUCCESS
published-main Knowledge     31796560814 / 94754827522 SUCCESS
```

## 3. R3.17D exact next pass

R3.17D is evidence-only. Recover the immutable R3.17A `r3_17a_scalar_witnesses.jsonl` receipt from job `94740870175` and compare all 96 rows against the native decoder at the same replay/network bit positions.

Required exact comparisons:

```text
attribute tag
payload_start_bit
payload_end_bit
payload_width
Boolean / Byte / Enum / Int / Int64 value
Float raw u32 bits and f32.to_bits()
stop_bit == payload_end_bit
```

Admission requires 96/96 exact equality, no missing replay identity, no native error, and zero production/Cargo/corpus mutation.

## 4. Still closed

```text
second property / property-loop continuation
next actor / next frame iteration
RigidBody / ActiveActor / Location / other spatial or compound attribute payloads
actor lifecycle mutation
raw-state materialization
semantic events
replay slicing
skill mining
counterfactual rollout execution
training/runtime/export widening
support-lane expansion
```
'''
clean_write(Path("docs/continuity/MIMIR_CURRENT_STATE.md"), current)

state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["last_production_code_sha"] = PROD_SHA
state["last_production_milestone"] = "R3.17C"
state["last_production_milestone_name"] = "native primitive scalar attribute decoder implementation"
state["current_pass"] = "R3.17D"
state["current_pass_kind"] = "evidence-only exact native primitive scalar differential"
state["current_pass_goal"] = "Compare the published native primitive scalar decoder against all 96 immutable R3.17A scalar witnesses at the exact replay/network bit positions."
state["current_pass_stop_boundary"] = "Evidence-only: 96/96 exact native comparison; no production/Cargo/corpus change and no second property, actor/frame iteration, lifecycle mutation or wider attribute family."
state["r3_17c"] = {
    "outcome": "published / production",
    "base_sha": PROD_BASE,
    "production_sha": PROD_SHA,
    "source_git_blob": SOURCE_BLOB,
    "test_git_blob": TEST_BLOB,
    "focused_tests": "11/11 PASS",
    "clean_files": 2,
    "implementation_run": 31795745652,
    "implementation_job": 94752360261,
    "candidate_ci_run": 31796122522,
    "candidate_ci_job": 94753517283,
    "candidate_knowledge_run": 31796266602,
    "candidate_knowledge_job": 94753955749,
    "published_main_ci_run": 31796509896,
    "published_main_ci_job": 94754670068,
    "published_main_knowledge_run": 31796560814,
    "published_main_knowledge_job": 94754827522,
    "primitive_tags": ["Boolean", "Byte", "Enum", "Float", "Int", "Int64"],
    "one_scalar_only": True,
    "next_pass": "R3.17D",
}
for item in [
    "docs/continuity/MIMIR_R3_17C_DECISION.md",
    "docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md",
]:
    if item not in state["next_files_to_read"]:
        state["next_files_to_read"].append(item)
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

r317c = f'''# MIMIR — R3.17C Production Decision

**Date:** 2026-08-14
**Pass:** `R3.17C — primitive scalar attribute decoder implementation`
**Outcome:** **PUBLISHED / PRODUCTION CLOSED**

## Production identity

```text
base SHA                    {PROD_BASE}
production SHA              {PROD_SHA}
source                       crates/mimir-replay/src/lib.rs
source Git blob             {SOURCE_BLOB}
focused test                 crates/mimir-replay/tests/r3_17c_scalar_attribute_decoder.rs
focused test Git blob       {TEST_BLOB}
clean diff                  exactly 2 files, +465/-0
```

## Admitted implementation

The native decoder accepts network bytes, a caller-supplied `payload_start_bit`, and an already resolved `ReplayNetworkAttributeTagV1`. It decodes exactly one R3.17B-admitted primitive scalar:

```text
Boolean / Byte / Enum / Float / Int / Int64
```

It reuses the existing LSB-first `NetworkBitCursor`, assumes no byte alignment, preserves Float raw `u32` bit identity alongside `f32`, interprets signed integer bit patterns natively, and returns exact payload start/end/width/value plus `stop_bit == payload_end_bit`.

Unsupported/compound tags are rejected before payload decoding. No second property, actor or frame is consumed.

## Validation

```text
focused tests                      11/11 PASS
disposable implementation run/job 31795745652 / 94752360261 SUCCESS
candidate CI                       31796122522 / 94753517283 SUCCESS
candidate Knowledge Archive        31796266602 / 94753955749 SUCCESS
publication                        force=false fast-forward
published-main CI                  31796509896 / 94754670068 SUCCESS
published-main Knowledge Archive   31796560814 / 94754827522 SUCCESS
```

## Scope audit

Permanent production commit changed only:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_17c_scalar_attribute_decoder.rs`

No Cargo dependency, lockfile, fixture, corpus, workflow, temporary tool or continuity file entered the production commit.

## Hard stop retained

R3.17C grants only a one-scalar primitive. Property-loop continuation, second property, actor/frame iteration, lifecycle mutation, `RigidBody`, `ActiveActor`, spatial/compound payloads, raw state, events, skills, runtime and export surfaces remain closed.

## Next pass

`R3.17D — primitive scalar native differential` against the immutable R3.17A 96-witness authority.
'''
clean_write(Path("docs/continuity/MIMIR_R3_17C_DECISION.md"), r317c)

r317d = f'''# MIMIR — R3.17D Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17D — primitive scalar native differential`
**Kind:** evidence-only / exact native-vs-oracle differential
**Frozen production SHA:** `{PROD_SHA}`
**Frozen source blob:** `{SOURCE_BLOB}`
**R3.17A authority:** `{EVIDENCE_HEAD}`, run `{EVIDENCE_RUN}`, job `{EVIDENCE_JOB}`

## 1. Goal

Prove that the published R3.17C native one-scalar decoder reproduces the immutable R3.17A primitive-scalar oracle witnesses exactly before any wider attribute family receives promotion credit.

## 2. Frozen input authority

Recover from exact R3.17A job `94740870175` receipt markers:

```text
r3_17a_replay_identity.tsv       47 rows
r3_17a_scalar_witnesses.jsonl    96 rows, 16 per admitted scalar tag
r3_17a_summary.json
r3_17a_aggregate.txt
r3_17a_receipt_sha256.txt
```

The witness file SHA-256 is `b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9`.

Do not regenerate or reselect witnesses. R3.17D compares against the already frozen rows.

## 3. Native comparison procedure

For each witness:

1. verify its replay path SHA against the frozen identity table;
2. read the replay through current MIMIR structural readers only far enough to locate the raw network byte slice;
3. map the recorded scalar tag to the same admitted `ReplayNetworkAttributeTagV1`;
4. call `decode_replay_network_primitive_scalar_v1(network_bytes, payload_start_bit, tag)`;
5. compare the native result against the witness.

Required exact fields:

```text
attribute_tag
payload_start_bit
payload_end_bit
payload_width
stop_bit == payload_end_bit
```

Value comparison:

```text
Boolean -> bool / 0|1 exact
Byte    -> u8 exact
Enum    -> u16 numeric exact
Int     -> i32 exact bit interpretation
Int64   -> i64 exact bit interpretation
Float   -> raw_bits exact AND value.to_bits() exact
```

## 4. Required aggregate

```text
witness_rows = 96
native_decode_success = 96
exact_match = 96/96
mismatch_count = 0
native_error_count = 0
identity_error_count = 0
unsupported_tag_count = 0
production_mutation_count = 0
Cargo_mutation_count = 0
corpus_mutation_count = 0
```

Emit a bounded immutable job-log receipt containing the 96 comparison rows or enough exact row identities/hashes to reconstruct every comparison after short-lived artifacts expire.

## 5. Failure rules

Any mismatch in bit span, width, signed interpretation, Float raw bits, tag identity or stop position is Outcome C until explained. Do not widen the native decoder or mutate witnesses to make the comparison pass.

A fixture identity mismatch or receipt extraction problem is an evidence-harness failure; fix the harness only and rerun on the same production SHA.

## 6. Hard stop

R3.17D must not change production Rust, Cargo manifests/lockfile, replay corpus or fixtures. It must not iterate a second property, actor or frame, mutate actor lifecycle state, decode compound/spatial attributes, or open raw-state/event/skill/runtime/export surfaces.

## 7. Outcome

### Outcome A
96/96 exact native equality, zero errors/mutations. Admit R3.17C differential closure and select the next bounded attribute-family pass from the roadmap.

### Outcome B
Evidence is valid but reveals a narrow unsupported scalar shape outside the frozen contract. Open the smallest evidence follow-up; do not generalize.

### Outcome C
Native implementation contradicts frozen R3.17A evidence. Reopen R3.17C implementation only at the smallest proven mismatch.
'''
clean_write(Path("docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md"), r317d)

print("R3_17C_CONTINUITY_SYNC=PASS")
