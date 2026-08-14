from __future__ import annotations

import json
from pathlib import Path

BASE = "4c307b5907a3e888b224ff925213109e0436841a"
PROD_SHA = "c3d4c73ca34febb9f0383c59132a8bc8a363b06b"
SOURCE_BLOB = "54e1bfb918ec1bd42a61cfa0131ca27412082ac5"
EVIDENCE_HEAD = "e8f1522fb6289368bbd254d2f839091452377e9e"
EVIDENCE_RUN = 31798478106
EVIDENCE_JOB = 94760722134
NORMAL_CI_RUN = 31798478071
NORMAL_CI_JOB = 94760722233
ARTIFACT_ID = 9218372907
ARTIFACT_SHA = "db049fbfd8514bb1cd661ab6b73ddf517d9786e961d764e62bc4e6137ce83e6f"
IDENTITY_SHA = "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf"
WITNESS_JSONL_SHA = "b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9"
WITNESS_TSV_SHA = "ee7f1baaa7696056172e28da2fed0848975ff1d2440113bb4d242f49d0b9da6e"
COMPARISON_SHA = "f10fa74e2975e1d13c8f23c5a570409667b0c4057428439a414b47f8aaa39f73"
AGGREGATE_SHA = "fcc1d93ff55f3cee89211fc77a2842adca33f32f94705390610edf749df1540d"
RECEIPT_FILE_SHA = "c86e904254c6ce5a1eeeff03df9f9961ffd9169fce391d34849b54ddfccbe268"


def clean_write(path: Path, content: str) -> None:
    lines = [line.rstrip() for line in content.strip().splitlines()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


handbook = Path("MIMIR_CONTINUE_HERE.md")
text = handbook.read_text(encoding="utf-8")
section = text.index("# 1. CANONICAL CURRENT STATE BLOCK")
start = text.index("```text", section)
end = text.index("```", start + len("```text")) + 3
block = f'''```text
REPOSITORY: Naveax/MIMIR
DEFAULT_BRANCH: main
LANGUAGE: Rust 2024 workspace
RUST_VERSION_FLOOR: 1.85

LAST_PRODUCTION_CODE_SHA:
  {PROD_SHA}

LAST_PRODUCTION_MILESTONE:
  R3.17C — native primitive scalar attribute decoder implementation

LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.17D — primitive scalar native differential / Outcome A / 96/96 exact

LAST_COMPLETED_CONTINUITY_CHECK:
  R3.16C — post-implementation continuity repair and capability-boundary check

LAST_COMPLETED_CONTRACT_PASS:
  R3.17B — primitive scalar attribute wire contract / Outcome A

CURRENT_PASS:
  R3.17E — object/reference/text attribute wire-format evidence

CURRENT_PASS_TYPE:
  evidence-only / pinned oracle instrumentation / NO production Rust change

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
  NO second property, next actor, next frame, K2 object/reference/text, compound or spatial family is admitted

R3_17C_PRODUCTION_CLOSURE:
  production SHA: {PROD_SHA}
  source Git blob: {SOURCE_BLOB}
  focused tests: 11/11 PASS
  published-main CI: 31796509896 / 94754670068 SUCCESS
  published-main Knowledge Archive: 31796560814 / 94754827522 SUCCESS

R3_17D_EVIDENCE_CLOSURE:
  exact evidence head: {EVIDENCE_HEAD}
  authority run/job: {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
  exact-head normal CI: {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
  frozen witness rows: 96
  native decode success: 96
  exact match: 96/96
  mismatch/native/identity/unsupported errors: 0
  production/Cargo/corpus mutation: 0
  comparison SHA256: {COMPARISON_SHA}
  artifact: {ARTIFACT_ID} / sha256:{ARTIFACT_SHA}
  immutable receipt stream: PASS

R3_17E_OPEN_BOUNDARY:
  roadmap wave K2 only: ActiveActor / String / QWordString / UniqueId / PartyLeader
  measure real supported-corpus occurrence counts before selecting witnesses
  record exact payload start/end bits, lossless values/bytes, object-reference behavior, text encoding/version gates and truncation structure
  zero-observation or ambiguous-shape tags remain unadmitted

R3_17E_HARD_STOP:
  production Rust unchanged
  no native K2 decoder
  no second property / property-loop continuation
  no spatial/physics K3 or gameplay-structured K4 family
  no actor/frame iteration or lifecycle mutation
  no raw-state/event/skill/runtime/export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17E OUTCOME A:
  R3.17F — object/reference/text attribute contract admission for evidence-supported K2 tags only
```'''
clean_write(handbook, text[:start] + block + text[end:])

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
R3.17C production decision              |
R3.17D differential decision            |
R3.17E K2 execution spec                |
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
4. `docs/continuity/MIMIR_R3_17C_DECISION.md`
5. `docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md`
6. `docs/continuity/MIMIR_R3_17D_DECISION.md`
7. `docs/continuity/MIMIR_R3_17E_EXECUTION_SPEC.md`
8. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
9. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
10. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
11. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
12. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
13. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
14. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
 -> R3.14 actor envelope primitives
 -> R3.15 NewActor branch
 -> R3.16 existing-actor first-property header
 -> R3.17A-D K1 primitive scalar wave: EVIDENCE + CONTRACT + PRODUCTION + 96/96 AUDIT CLOSED
      production SHA {PROD_SHA}
      source blob {SOURCE_BLOB}
      R3.17D authority {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
      exact comparison {COMPARISON_SHA}
 -> R3.17E K2 object/reference/text wire-format evidence: ACTIVE
```

## Current capability lock

MIMIR may natively decode exactly one already-resolved K1 primitive scalar payload for Boolean, Byte, Enum, Float, Int or Int64. K2 (`ActiveActor`, `String`, `QWordString`, `UniqueId`, `PartyLeader`) remains evidence-only and has no native payload permission.

Property-loop continuation, next actor/frame iteration, lifecycle mutation, K3 spatial/physics and K4 gameplay-structured families remain closed.

## R3.17D closure identity

```text
evidence head              {EVIDENCE_HEAD}
authority run/job          {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
normal CI                  {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
artifact                   {ARTIFACT_ID}
artifact SHA256            {ARTIFACT_SHA}
identity TSV SHA256        {IDENTITY_SHA}
witness JSONL SHA256       {WITNESS_JSONL_SHA}
witness TSV SHA256         {WITNESS_TSV_SHA}
comparison TSV SHA256      {COMPARISON_SHA}
aggregate SHA256           {AGGREGATE_SHA}
receipt file SHA256        {RECEIPT_FILE_SHA}
exact native match         96/96
receipt stream             PASS
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
**Completed native differential:** `R3.17D — Outcome A / 96 of 96 exact`
**Current exact pass:** `R3.17E — object/reference/text attribute wire-format evidence`

## 1. Truthful production boundary

MIMIR can natively decode exactly one already-resolved primitive scalar payload for Boolean, Byte, Enum, Float, Int or Int64 and stops exactly after that value. R3.17D independently reproduced the immutable R3.17A 96-witness set at 96/96 exact equality.

No K2 object/reference/text payload is native production capability yet.

## 2. R3.17D closure authority

```text
production SHA                 {PROD_SHA}
production source blob         {SOURCE_BLOB}
evidence head                  {EVIDENCE_HEAD}
authority run/job              {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
exact-head normal CI           {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
witness rows                   96
native decode success          96
exact match                    96/96
mismatch count                 0
native error count             0
identity error count           0
unsupported tag count          0
production/Cargo/corpus mut.   0 / 0 / 0
artifact id                    {ARTIFACT_ID}
artifact zip SHA-256           {ARTIFACT_SHA}
identity TSV SHA-256           {IDENTITY_SHA}
witness JSONL SHA-256          {WITNESS_JSONL_SHA}
witness TSV SHA-256            {WITNESS_TSV_SHA}
comparison TSV SHA-256         {COMPARISON_SHA}
immutable receipt stream       PASS
```

## 3. R3.17E exact next pass

Roadmap K2 is the next attribute decoder wave:

```text
ActiveActor
String
QWordString
UniqueId
PartyLeader
```

R3.17E is evidence-only. Scan the exact supported 47-replay lane with pinned Boxcars, measure full occurrence counts first, then freeze bounded reproducible witnesses only for actually observed shapes.

For each tag, evidence must determine exact bit span/value representation and any context/version gates. In particular, do not assume actor-reference structure, string encoding, fixed width, optionality or UniqueId/PartyLeader layouts from type names. Zero-observation tags remain closed.

## 4. Still closed

```text
native K2 object/reference/text decoder
second property / property-loop continuation
next actor / next frame iteration
K3 Location/RigidBody/ReplicatedBoost/PickupNew
K4 gameplay structured attribute family
actor lifecycle mutation
raw-state materialization and semantic events
replay slicing / skill mining / counterfactual rollout
training/runtime/export widening
support-lane expansion
```
'''
clean_write(Path("docs/continuity/MIMIR_CURRENT_STATE.md"), current)

state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
if state.get("current_pass") != "R3.17D":
    raise SystemExit(f"unexpected current_pass: {state.get('current_pass')!r}")
state["last_completed_read_only_audit"] = "R3.17D"
state["last_completed_evidence_pass"] = "R3.17D"
state["last_completed_evidence_outcome"] = "A — published primitive scalar decoder matched all 96 immutable R3.17A witnesses exactly; zero native/identity/mismatch/unsupported/mutation errors; immutable receipt stream PASS"
state["current_pass"] = "R3.17E"
state["current_pass_kind"] = "evidence-only K2 object/reference/text attribute wire-format audit"
state["current_pass_goal"] = "Measure exact supported-corpus wire behavior for ActiveActor/String/QWordString/UniqueId/PartyLeader using the pinned oracle, without changing production Rust."
state["current_pass_stop_boundary"] = "Evidence-only K2 observation; no native K2 decoder, second property, actor/frame iteration, lifecycle mutation, K3/K4 widening, Cargo/corpus/support-lane change."
state["closed_now"] = [
    "native K2/K3/K4 attribute payload decode",
    "native property loop iteration beyond one already-resolved scalar",
    "second property consumption",
    "full actor envelope iteration",
    "full frame iteration",
    "actor state table mutation",
    "raw-state extraction",
    "event extraction",
    "replay slicing",
    "skill mining",
    "counterfactual rollout execution from native replay state",
]
state["r3_17d"] = {
    "outcome": "A — admitted / exact differential complete",
    "production_source_changed": False,
    "production_sha": PROD_SHA,
    "source_git_blob": SOURCE_BLOB,
    "evidence_head_sha": EVIDENCE_HEAD,
    "workflow_run": EVIDENCE_RUN,
    "workflow_job": EVIDENCE_JOB,
    "exact_head_ci_run": NORMAL_CI_RUN,
    "exact_head_ci_job": NORMAL_CI_JOB,
    "artifact_id": ARTIFACT_ID,
    "artifact_sha256": ARTIFACT_SHA,
    "identity_sha256": IDENTITY_SHA,
    "witness_jsonl_sha256": WITNESS_JSONL_SHA,
    "witness_tsv_sha256": WITNESS_TSV_SHA,
    "comparison_sha256": COMPARISON_SHA,
    "aggregate_sha256": AGGREGATE_SHA,
    "receipt_file_sha256": RECEIPT_FILE_SHA,
    "witness_rows": 96,
    "native_decode_success": 96,
    "exact_match": "96/96",
    "mismatch_count": 0,
    "native_error_count": 0,
    "identity_error_count": 0,
    "unsupported_tag_count": 0,
    "production_mutation_count": 0,
    "cargo_mutation_count": 0,
    "corpus_mutation_count": 0,
    "receipt_stream": "PASS",
    "next_pass": "R3.17E",
}
for item in [
    "docs/continuity/MIMIR_R3_17D_DECISION.md",
    "docs/continuity/MIMIR_R3_17E_EXECUTION_SPEC.md",
]:
    if item not in state["next_files_to_read"]:
        state["next_files_to_read"].append(item)
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

r317d = f'''# MIMIR — R3.17D Differential Decision

**Date:** 2026-08-14
**Pass:** `R3.17D — primitive scalar native differential`
**Outcome:** **A — ADMITTED / 96 OF 96 EXACT**
**Pass kind:** evidence-only differential
**Production Rust changed:** **NO**

## Frozen authorities

```text
canonical production SHA     {PROD_SHA}
production source blob       {SOURCE_BLOB}
R3.17D evidence head         {EVIDENCE_HEAD}
R3.17D authority run/job     {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
exact-head normal CI         {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
artifact                     {ARTIFACT_ID}
artifact SHA-256             {ARTIFACT_SHA}
identity TSV SHA-256         {IDENTITY_SHA}
witness JSONL SHA-256        {WITNESS_JSONL_SHA}
witness TSV SHA-256          {WITNESS_TSV_SHA}
comparison TSV SHA-256       {COMPARISON_SHA}
aggregate SHA-256            {AGGREGATE_SHA}
receipt file SHA-256         {RECEIPT_FILE_SHA}
immutable receipt stream     PASS
```

## Result

The current native R3.17C one-scalar decoder was run at the exact replay/network bit positions of all 96 immutable R3.17A witnesses. Result:

```text
witness rows                 96
native decode success        96
exact match                  96/96
mismatch count               0
native error count           0
identity error count         0
unsupported tag count        0
production mutation count    0
Cargo mutation count         0
corpus mutation count        0
```

Exact equality covered tag, payload start/end, consumed width, stop bit and scalar value. Float rows additionally required raw `u32` equality and identical `f32::to_bits()` identity.

The first evidence attempt already achieved 96/96 but failed only repository `cargo fmt --check` on the temporary harness. The final authority head changed only evidence-harness formatting and then passed the full repository verifier plus normal CI. No witness or production semantics were changed.

## Decision

R3.17 K1 primitive scalar wave is closed: evidence, contract, production implementation and frozen native differential have all passed. This does **not** authorize property-loop continuation or another attribute family by analogy.

The execution roadmap orders the next wave as K2 object/reference/text. Therefore the next exact pass is evidence-only `R3.17E`.
'''
clean_write(Path("docs/continuity/MIMIR_R3_17D_DECISION.md"), r317d)

r317e = '''# MIMIR — R3.17E Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17E — object/reference/text attribute wire-format evidence`
**Kind:** evidence-only / pinned oracle instrumentation
**Production Rust change:** forbidden

## 1. Goal

Begin roadmap wave K2 only after K1 primitive scalar closure. Candidate tags:

```text
ActiveActor
String
QWordString
UniqueId
PartyLeader
```

Measure real supported-corpus behavior before admitting any native contract. A candidate tag with zero usable observations or unresolved multiple shapes remains unadmitted.

## 2. Frozen production and corpus

```text
production SHA             c3d4c73ca34febb9f0383c59132a8bc8a363b06b
source blob                54e1bfb918ec1bd42a61cfa0131ca27412082ac5
supported replay lane      exact existing 47 replays
oracle                     nickbabcock/boxcars
oracle SHA                 c70e77df7af81b436cb545d070bb90c82f562d0b
```

The oracle is observation-only and must not become a production dependency.

## 3. Evidence procedure

Scan the full exact 47-replay lane and record complete occurrence counts for all five candidate K2 tags before witness selection. Freeze bounded witnesses per actually observed shape, preserving replay identity and stable frame/actor/property context.

For each usable occurrence capture enough information to reproduce independently:

```text
replay identity
frame/actor/property stable context
actor context object ID/name
property object ID/name
attribute tag
payload start bit
payload end bit
exact consumed width
lossless raw bytes/bits or structural field values
oracle decoded value
version/build/net-version fields relevant to shape
next structural cursor bit
```

## 4. Questions that evidence must answer

Do not infer these from names:

- `ActiveActor`: exact flag/reference structure, actor-ID representation/bounds, null/absent forms and build gates;
- `String`: exact length/encoding/termination rules, narrow vs wide text branches, empty string behavior and malformed lengths;
- `QWordString`: whether the observed form is fixed-width, string-like, integer-backed or version/context dependent;
- `UniqueId`: exact platform/type discriminants, payload branches, optional fields, lengths and version gates;
- `PartyLeader`: exact optional/null behavior and whether it reuses `UniqueId` encoding identically in all observed contexts;
- exact truncation boundaries for every observed shape;
- whether any tag has more than one wire shape across the supported lane.

## 5. Required aggregate

At minimum:

```text
replays_total = 47
oracle_decode_success count
per-tag occurrence count
per-tag replay count
per-tag usable witness count
per-tag unique wire shapes / widths
identity_error_count
oracle_error_count
bit_monotonicity_failure_count
shape_mismatch_or_unclassified_count
production_mutation_count = 0
Cargo_mutation_count = 0
corpus_mutation_count = 0
```

## 6. Hard stop

R3.17E may observe K2 payloads through the pinned oracle but must not:

```text
change production Rust
implement any native K2 decoder
decode or implement K3 Location/RigidBody/ReplicatedBoost/PickupNew
decode or implement K4 gameplay structured family
consume a native second property
iterate native next actor/frame
mutate lifecycle state
materialize raw game state or semantic events
open replay slicing / skill / teacher / runtime / export surfaces
change Cargo dependencies
change replay fixtures/corpus/support lane
```

## 7. Outcome rules

### Outcome A
At least one K2 tag has reproducible exact wire evidence sufficient for a narrow contract, every observed candidate shape is classified, and mutation counts remain zero. Open `R3.17F — object/reference/text attribute contract admission` for evidence-supported tags only.

### Outcome B
Evidence is valid but one or more observed tags have ambiguous/multiple shapes or insufficient support. Split the smallest tag/shape-specific evidence follow-up. Do not generalize.

### Outcome C
Oracle identity, cursor accounting or prior property-header assumptions contradict the current native boundary. Stop and reopen the smallest earlier contract before implementation.

## 8. Publication policy

Evidence branch only. Temporary oracle instrumentation, workflows and analyzers do not enter canonical production history. After Outcome A/B/C, admit only bounded decision/spec/continuity artifacts; production source remains frozen.
'''
clean_write(Path("docs/continuity/MIMIR_R3_17E_EXECUTION_SPEC.md"), r317e)

print("R3_17D_CONTINUITY_SYNC=PASS")
