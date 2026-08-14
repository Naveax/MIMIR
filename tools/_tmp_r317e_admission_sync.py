from __future__ import annotations

import json
import re
from pathlib import Path

BASE = "cfe4882f99dbce5e8148e476c177a0586b1e7986"
PROD = "c3d4c73ca34febb9f0383c59132a8bc8a363b06b"
EVIDENCE = "f7c12025d433b76dd402d18172445f5ff595fb43"
RUN = 31801277266
JOB = 94769598916
ARTIFACT = 9219497766
ARTIFACT_SHA = "caf27991d7e5e39d3b6fb1101b89545525b485947501b0b28523298488bb5c86"

DECISION = f'''# MIMIR — R3.17E Decision

**Date:** 2026-08-14
**Pass:** `R3.17E — object/reference/text attribute wire-format evidence`
**Outcome:** **A — evidence exact / K2 observed-shape set admitted for contract work**
**Production Rust changed:** **NO**
**Production code checkpoint remains:** `{PROD}`

## Decision

The K2 evidence pass is admitted as read-only wire evidence. The exact supported 47-replay lane produced 110,539 K2 payload observations with zero shape mismatch/unclassified rows, zero bit-monotonicity failures, zero raw-payload shape failures, and zero production/Cargo/corpus mutation.

This decision does **not** grant a native K2 decoder. It opens contract admission only for shapes actually supported by the evidence below.

## Frozen authority

```text
canonical evidence base       {BASE}
evidence head                 {EVIDENCE}
workflow run/job              {RUN} / {JOB} SUCCESS
exact-head normal CI          31801277210 / 94769598732 SUCCESS
pinned Boxcars                c70e77df7af81b436cb545d070bb90c82f562d0b
frame_decoder.rs blob         6f2ff153d3a27cdacccc65e3f23851489077a7d8
attributes.rs blob            5e2d5bc1cd8187af30c3ea95193ad987645cb76e
artifact                      {ARTIFACT}
artifact SHA-256              {ARTIFACT_SHA}
replay identity rows          47
bounded witness rows          108
receipt stream                PASS
```

## Aggregate result

```text
oracle decode success         47 / 47
K2 occurrences                110,539
ActiveActor                   86,200 / 47 replays / exactly 33 bits
String                        14,670 / 47 replays / variable width
QWordString                   2,920 / 47 replays / QWord64 + StringText branches
UniqueId                      6,443 / 47 replays / 4 observed platform shapes
PartyLeader                   306 / 1 replay / Some(Epic) only
shape mismatch/unclassified   0
bit monotonicity failures     0
raw payload shape failures    0
production/Cargo/corpus mut.  0 / 0 / 0
```

## Evidence-supported shapes

### ActiveActor

All 86,200 observations consumed exactly 33 bits and matched the source shape:

```text
active: 1 bit
actor: signed i32 bit pattern / 32 bits
```

Both `is_rl_223=false` and `is_rl_223=true` replay families were observed.

### String

All 14,670 observations followed Boxcars `decode_text` and were variable-width. Evidence includes both positive and negative signed length prefixes.

The pinned source establishes:

```text
size: signed i32 / 32 bits
size == 0     -> empty string
size > 0      -> size bytes, Windows-1252, final 1-byte NUL omitted semantically
size < 0      -> (-size * 2) bytes, UTF-16LE, final 2-byte NUL omitted semantically
```

Observed total payload widths ranged over the evidence-recorded set from 32 through 312 bits; fixed-width String decoding is forbidden.

### QWordString

The build/context gate is material and was observed on both sides:

```text
is_rl_223 == false -> QWord64 / exactly 64 bits    (762 observations)
is_rl_223 == true  -> StringText / decode_text    (2,158 observations)
```

A single unconditional QWordString layout is forbidden.

### UniqueId

Only these platform shapes are evidence-supported on the current lane:

```text
Steam        5,087 observations
Epic         1,164 observations
PlayStation    128 observations
PsyNet          64 observations
```

Observed widths were 80, 312, and 336 bits depending on the branch/value. Platform dispatch is therefore part of the wire contract.

`Switch`, `Xbox`, `QQ`, and `SplitScreen` were **not observed** in this evidence lane and are not admitted by analogy.

### PartyLeader

Only one shape was observed:

```text
Some(UniqueId::Epic)   306 observations / 1 replay / 312 bits
```

`None` and every non-Epic PartyLeader branch remain unadmitted. Source visibility alone does not convert an unobserved branch into supported-lane evidence.

## Durable hashes

```text
instrumentation patch        e7b1244051c0e0f2a74f227bdd4029b9f54956d6486fcb619d550c27cfe4c660
full K2 oracle               02214804715ab75397a4492377326852fae2bea1071c0befec06802f60b2da39
108 witnesses                b315bb43fd33e13dfb485d7cde5189ea0961112b30906d2da8927c54e1597dd0
summary                      646312e1dd750cb81a339810741b46de98ed7b5bb257fcb2474c5f0586a2fd37
aggregate                    ec7a64a5a1618ed2e854a57b8835e2f45808eac7eaa54918fec6f6e9d291d92c
```

## Hard stop

R3.17E changes no production code and grants no K2 runtime capability. Property-loop continuation, next actor/frame iteration, lifecycle mutation, K3/K4 decoding, raw-state/event/skill/runtime/export widening, Cargo changes and support-lane expansion remain closed.

## Next exact pass

`R3.17F — object/reference/text attribute contract admission for evidence-supported K2 shapes only`.
'''

SPEC = f'''# MIMIR — R3.17F Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17F — object/reference/text attribute contract admission`
**Kind:** contract-only / docs-state / no production Rust
**Production checkpoint:** `{PROD}`
**Evidence authority:** `{EVIDENCE}`, run/job `{RUN} / {JOB}`

## 1. Goal

Freeze the smallest native implementation contract justified by R3.17E for K2. The pass may admit only evidence-supported branches. It does not implement them.

Candidate contract scope:

```text
ActiveActor
String
QWordString
UniqueId::Steam
UniqueId::Epic
UniqueId::PlayStation
UniqueId::PsyNet
PartyLeader::Some(UniqueId::Epic)
```

Unobserved branches remain closed.

## 2. Common cursor and failure contract

Every K2 decoder starts at the already-resolved `payload_start_bit`. No byte-alignment precondition may be invented.

The later implementation must be cursor-atomic:

```text
success -> return exact payload_start_bit / payload_end_bit / payload_width / typed value
failure -> return no value and consume 0 bits from the caller-visible cursor
```

Variable-width decoders must validate the complete declared branch before committing cursor advance. Invalid signed lengths, arithmetic overflow, impossible platform IDs, insufficient bytes/bits, encoding failure, or unadmitted branches fail closed.

Poison bits after the selected K2 payload remain unread. No property-loop continuation is admitted.

## 3. ActiveActor contract candidate

Evidence and pinned source agree on exactly 33 bits:

```text
active: bool from 1 bit
actor_id: signed i32 from the next 32 LSB-first bits
end = start + 33
```

The result should preserve the exact actor ID bit pattern/semantic signed value. This is an object reference value only; R3.17F does not resolve it through a lifecycle table.

## 4. String contract candidate

The text wire contract is signed-length-prefixed and variable-width:

```text
size: i32 / 32 bits
size == 0:
  value = ""
  width = 32
size > 0:
  byte_count = size
  read exactly byte_count bytes
  decode Windows-1252 after excluding the final 1-byte terminator
size < 0:
  byte_count = checked(-size * 2)
  read exactly byte_count bytes
  decode UTF-16LE after excluding the final 2-byte terminator
```

R3.17F must decide and document malformed terminator policy explicitly. It may not silently accept an absent declared byte range or integer overflow. The exact raw declared bytes should remain available for differential verification even when a semantic String is returned.

## 5. QWordString contract candidate

The replay/build context gate is part of the contract:

```text
is_rl_223 == false -> exactly 64 bits, unsigned u64/qword value
is_rl_223 == true  -> the full String contract from section 4
```

The later decoder therefore needs the already-admitted context flag as an explicit input; guessing the branch from remaining length or payload bytes is forbidden.

## 6. UniqueId contract candidate

The first byte is the platform/system discriminator. Only four observed branches may be admitted in R3.17F.

### Steam

Observed fixed width: 80 bits.

```text
system_id = 1 / u8
remote online_id = u64
local_id = u8
```

### Epic

Observed current-lane examples use the text branch and were 312 bits for the observed 32-character identifiers. The contract is variable in principle because the Epic remote ID uses the same signed-length text decoder.

```text
system_id = 11 / u8
remote Epic ID = String contract
after remote ID: local_id = u8
```

Do **not** freeze Epic to 312 bits merely because all current witnesses have that width.

### PlayStation

Observed width: 336 bits. R3.17F must freeze the exact pinned-source field ordering and fixed byte counts for the PlayStation branch before implementation. The native value should preserve opaque/unknown bytes rather than invent semantics.

### PsyNet

Observed width: 80 bits on the current admitted version/net-version lane. The pinned source contains version-dependent PsyNet structure. R3.17F may admit only the exact current-lane branch proven by the current version tuple; it must not generalize to unobserved version-gated extra bytes.

### Explicitly closed UniqueId platforms

```text
SplitScreen
Xbox
Switch
QQ
```

They were not observed in R3.17E and require targeted evidence before production support.

## 7. PartyLeader contract candidate

Only the observed branch is eligible:

```text
system/platform discriminator = Epic (11)
then the admitted UniqueId::Epic body
result = Some(Epic unique id)
```

`PartyLeader::None` and non-Epic branches remain unsupported. The implementation must fail without consuming bits when a PartyLeader payload selects an unadmitted branch.

## 8. Required R3.17G implementation tests if Outcome A

At minimum:

- ActiveActor active=false/true and signed actor-ID edge patterns;
- aligned and unaligned starts;
- exact 33-bit ActiveActor end cursor;
- String empty, positive Windows-1252, negative UTF-16LE;
- positive and negative String truncation at every structural boundary;
- signed-length overflow/malformed cases fail atomically;
- QWordString both `is_rl_223` branches and wrong-context non-equivalence;
- UniqueId Steam exact 80-bit tests;
- UniqueId Epic variable text length tests, not only 312-bit witnesses;
- PlayStation exact observed branch fixtures preserving opaque bytes;
- PsyNet exact current-version observed branch;
- unobserved UniqueId platform discriminators fail atomically;
- PartyLeader observed Some(Epic) success;
- PartyLeader None/non-Epic remains unsupported and atomic;
- poison bits after one payload remain unread;
- no second property, actor, or frame consumption.

A later differential pass must compare native K2 results and exact end bits against the frozen 108 R3.17E witnesses before K2 is considered closed.

## 9. Explicitly not admitted

```text
UniqueId SplitScreen/Xbox/Switch/QQ
PartyLeader None or non-Epic
K3 Location/RigidBody/ReplicatedBoost/PickupNew
K4 gameplay structured payloads
second property / property loop
next actor / next frame
actor lifecycle mutation
raw-state / event / skill / runtime / export widening
support-lane widening
Cargo dependency changes
```

## 10. Outcome rules

### Outcome A

The evidence-supported contracts above are precise enough for native implementation. Open:

`R3.17G — evidence-supported K2 native decoder implementation`.

### Outcome B

One or more candidate branches still have an unresolved wire ambiguity. Admit only the unambiguous subset and open the smallest targeted evidence follow-up before implementing the ambiguous branch.

### Outcome C

A proposed contract contradicts R3.17E evidence, pinned source, or current production cursor semantics. Stop and repair the conflicting assumption.

## 11. Hard stop

R3.17F is docs/state only. Production Rust, Cargo, fixtures and replay corpus remain byte-identical.
'''

CURRENT = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.17C — native primitive scalar attribute decoder implementation`
**Completed native differential:** `R3.17D — Outcome A / 96 of 96 exact`
**Completed K2 evidence:** `R3.17E — Outcome A / 110,539 observations`
**Current exact pass:** `R3.17F — object/reference/text attribute contract admission`

## 1. Truthful production boundary

MIMIR can natively decode exactly one already-resolved K1 primitive scalar payload for Boolean, Byte, Enum, Float, Int or Int64 and stops after that one value. No K2 payload is production capability yet.

## 2. R3.17E immutable evidence authority

```text
canonical evidence base       {BASE}
evidence head                 {EVIDENCE}
authority run/job             {RUN} / {JOB} SUCCESS
exact-head normal CI          31801277210 / 94769598732 SUCCESS
artifact                      {ARTIFACT}
artifact SHA-256              {ARTIFACT_SHA}
replay identity rows          47
bounded witness rows          108
K2 occurrences                110,539
shape mismatch/unclassified   0
bit monotonicity failures     0
raw payload shape failures    0
production/Cargo/corpus mut.  0 / 0 / 0
receipt stream                PASS
```

Durable hashes:

```text
instrumentation patch   e7b1244051c0e0f2a74f227bdd4029b9f54956d6486fcb619d550c27cfe4c660
full K2 oracle          02214804715ab75397a4492377326852fae2bea1071c0befec06802f60b2da39
108 witnesses           b315bb43fd33e13dfb485d7cde5189ea0961112b30906d2da8927c54e1597dd0
summary                 646312e1dd750cb81a339810741b46de98ed7b5bb257fcb2474c5f0586a2fd37
aggregate               ec7a64a5a1618ed2e854a57b8835e2f45808eac7eaa54918fec6f6e9d291d92c
```

## 3. Evidence-supported K2 shapes

```text
ActiveActor   86,200 / 47 replays / exactly 33 bits
String        14,670 / 47 / signed-length variable text
QWordString    2,920 / 47 / QWord64 762 + StringText 2,158
UniqueId       6,443 / 47 / Steam 5,087 + Epic 1,164 + PlayStation 128 + PsyNet 64
PartyLeader      306 / 1 / Some(Epic) only
```

Unobserved UniqueId SplitScreen/Xbox/Switch/QQ and PartyLeader None/non-Epic branches remain closed.

## 4. R3.17F exact pass

R3.17F is contract-only. It must freeze cursor-atomic native contracts for only the evidence-supported branches, including signed text length/encoding rules, QWordString's `is_rl_223` gate, observed UniqueId platform dispatch, and PartyLeader's observed Some(Epic) branch.

No production code changes in this pass.

## 5. Still closed

```text
native K2 decoder
unobserved K2 branches
second property / property-loop continuation
next actor / next frame iteration
K3 spatial/physics family
K4 gameplay structured family
actor lifecycle mutation
raw-state / event / replay slicing / skill mining
runtime/training/export widening
support-lane expansion
```

Outcome A opens `R3.17G — evidence-supported K2 native decoder implementation`.
'''

GRAPH = f'''# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

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
R3.17D K1 differential decision         |
R3.17E K2 evidence decision             |
R3.17F K2 contract spec                 |
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
8. `docs/continuity/MIMIR_R3_17E_DECISION.md`
9. `docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md`
10. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
11. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
12. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
13. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
14. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
15. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
16. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
 -> R3.14 actor envelope primitives
 -> R3.15 NewActor branch
 -> R3.16 existing-actor first-property header
 -> R3.17A-D K1 primitive scalar wave: CLOSED / PRODUCTION + 96/96 DIFFERENTIAL
      production SHA {PROD}
      source blob 54e1bfb918ec1bd42a61cfa0131ca27412082ac5
 -> R3.17E K2 object/reference/text evidence: CLOSED / Outcome A
      evidence head {EVIDENCE}
      110,539 observations / 47 replay lane / 108 witnesses
      receipt stream PASS
 -> R3.17F evidence-supported K2 wire contract: ACTIVE
```

## R3.17E K2 evidence shape summary

```text
ActiveActor  86,200  47 replays  33 bits exact
String       14,670  47 replays  variable signed-length text
QWordString   2,920  47 replays  QWord64 + StringText
UniqueId      6,443  47 replays  Steam/Epic/PlayStation/PsyNet only
PartyLeader     306   1 replay   Some(Epic) only
```

Zero shape mismatches, zero bit-monotonicity failures and zero raw payload-shape failures were observed. Unobserved branches remain closed.

## Current capability lock

MIMIR may natively decode exactly one already-resolved K1 primitive scalar payload. R3.17E is evidence only. R3.17F may admit wire contracts for evidence-supported K2 branches but grants no executable K2 decoder.

Property-loop continuation, next actor/frame iteration, actor lifecycle mutation, K3/K4 families and semantic/raw-state/skill/runtime widening remain closed.

## R3.17E evidence identity

```text
evidence head              {EVIDENCE}
authority run/job          {RUN} / {JOB} SUCCESS
normal CI                  31801277210 / 94769598732 SUCCESS
artifact                   {ARTIFACT}
artifact SHA256            {ARTIFACT_SHA}
full K2 oracle SHA256      02214804715ab75397a4492377326852fae2bea1071c0befec06802f60b2da39
witness SHA256             b315bb43fd33e13dfb485d7cde5189ea0961112b30906d2da8927c54e1597dd0
aggregate SHA256           ec7a64a5a1618ed2e854a57b8835e2f45808eac7eaa54918fec6f6e9d291d92c
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

HANDBOOK_BLOCK = f'''```text
REPOSITORY: Naveax/MIMIR
DEFAULT_BRANCH: main
LANGUAGE: Rust 2024 workspace
RUST_VERSION_FLOOR: 1.85

LAST_PRODUCTION_CODE_SHA:
  {PROD}

LAST_PRODUCTION_MILESTONE:
  R3.17C — native primitive scalar attribute decoder implementation

LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.17E — K2 object/reference/text wire evidence / Outcome A / 110,539 observations

LAST_COMPLETED_CONTINUITY_CHECK:
  R3.16C — post-implementation continuity repair and capability-boundary check

LAST_COMPLETED_CONTRACT_PASS:
  R3.17B — primitive scalar attribute wire contract / Outcome A

CURRENT_PASS:
  R3.17F — object/reference/text attribute contract admission

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
  one already-resolved K1 primitive scalar payload may be decoded natively
  stop exactly at payload_end_bit / stop_bit after that one scalar
  NO native K2 object/reference/text decoder is admitted yet

R3_17E_EVIDENCE_CLOSURE:
  exact evidence head: {EVIDENCE}
  authority run/job: {RUN} / {JOB} SUCCESS
  exact-head normal CI: 31801277210 / 94769598732 SUCCESS
  artifact: {ARTIFACT} / sha256:{ARTIFACT_SHA}
  replay identity rows: 47
  K2 occurrences: 110,539
  bounded witness rows: 108
  shape mismatch/unclassified: 0
  bit monotonicity failures: 0
  raw payload shape failures: 0
  production/Cargo/corpus mutation: 0 / 0 / 0
  immutable receipt stream: PASS

R3_17E_OBSERVED_SHAPES:
  ActiveActor: 86,200 / 47 replays / 33 bits exact
  String: 14,670 / 47 / variable signed-length text
  QWordString: 2,920 / 47 / QWord64 762 + StringText 2,158
  UniqueId: Steam 5,087 + Epic 1,164 + PlayStation 128 + PsyNet 64
  PartyLeader: Some(Epic) 306 / 1 replay only

R3_17F_CONTRACT_SCOPE:
  admit only evidence-supported K2 branches
  preserve signed String length and Windows-1252/UTF-16LE branch semantics
  preserve QWordString is_rl_223 context gate
  UniqueId support limited to Steam/Epic/PlayStation/PsyNet observed branches
  PartyLeader support limited to observed Some(Epic) branch
  all failures cursor-atomic / zero-consumption

R3_17F_HARD_STOP:
  production Rust unchanged
  no native K2 decoder yet
  no unobserved UniqueId/PartyLeader branches
  no second property / property-loop continuation
  no K3/K4 attribute family
  no next actor/frame or lifecycle mutation
  no raw-state/event/skill/runtime/export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17F OUTCOME A:
  R3.17G — evidence-supported K2 native decoder implementation
```'''

# New docs
Path("docs/continuity/MIMIR_R3_17E_DECISION.md").write_text(DECISION, encoding="utf-8", newline="\n")
Path("docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md").write_text(SPEC, encoding="utf-8", newline="\n")
Path("docs/continuity/MIMIR_CURRENT_STATE.md").write_text(CURRENT, encoding="utf-8", newline="\n")
Path("MIMIR_KNOWLEDGE_GRAPH.md").write_text(GRAPH, encoding="utf-8", newline="\n")

# JSON state
state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-14"
state["last_completed_read_only_audit"] = "R3.17E"
state["last_completed_evidence_pass"] = "R3.17E"
state["last_completed_evidence_outcome"] = "A — K2 evidence exact: 110,539 observations across ActiveActor/String/QWordString/UniqueId/PartyLeader; 108 bounded witnesses; zero shape/bit/raw-payload failures; immutable receipt stream PASS"
state["current_pass"] = "R3.17F"
state["current_pass_kind"] = "contract-only evidence-supported K2 object/reference/text wire contract admission"
state["current_pass_goal"] = "Admit only R3.17E-supported ActiveActor/String/QWordString/UniqueId Steam/Epic/PlayStation/PsyNet and PartyLeader Some(Epic) wire contracts without changing production Rust."
state["current_pass_stop_boundary"] = "No native K2 decoder yet; unobserved K2 branches, K3/K4, second property, actor/frame iteration, lifecycle mutation, raw-state/event/skill/runtime/export widening, Cargo/corpus/support-lane changes remain closed."
state["r3_17e"] = {
    "outcome": "A",
    "production_source_changed": False,
    "canonical_evidence_base": BASE,
    "production_sha": PROD,
    "production_source_blob": "54e1bfb918ec1bd42a61cfa0131ca27412082ac5",
    "evidence_head_sha": EVIDENCE,
    "authority_run": RUN,
    "authority_job": JOB,
    "normal_ci_run": 31801277210,
    "normal_ci_job": 94769598732,
    "artifact_id": ARTIFACT,
    "artifact_sha256": ARTIFACT_SHA,
    "replay_identity_rows": 47,
    "witness_rows": 108,
    "k2_occurrences_total": 110539,
    "active_actor": {"occurrences": 86200, "replays": 47, "widths": [33], "shapes": {"ActiveActor33": 86200}},
    "string": {"occurrences": 14670, "replays": 47, "variable_width": True, "shapes": {"StringText": 14670}},
    "qword_string": {"occurrences": 2920, "replays": 47, "widths": [64, 88, 96, 104], "shapes": {"QWord64": 762, "StringText": 2158}},
    "unique_id": {"occurrences": 6443, "replays": 47, "widths": [80, 312, 336], "shapes": {"Epic": 1164, "PlayStation": 128, "PsyNet": 64, "Steam": 5087}, "unobserved_closed": ["SplitScreen", "Xbox", "Switch", "QQ"]},
    "party_leader": {"occurrences": 306, "replays": 1, "widths": [312], "shapes": {"Some:UniqueId:Epic": 306}, "unobserved_closed": ["None", "non-Epic"]},
    "shape_mismatch_or_unclassified_count": 0,
    "bit_monotonicity_failure_count": 0,
    "raw_payload_shape_failure_count": 0,
    "production_mutation_count": 0,
    "cargo_mutation_count": 0,
    "corpus_mutation_count": 0,
    "full_oracle_sha256": "02214804715ab75397a4492377326852fae2bea1071c0befec06802f60b2da39",
    "witness_sha256": "b315bb43fd33e13dfb485d7cde5189ea0961112b30906d2da8927c54e1597dd0",
    "summary_sha256": "646312e1dd750cb81a339810741b46de98ed7b5bb257fcb2474c5f0586a2fd37",
    "aggregate_sha256": "ec7a64a5a1618ed2e854a57b8835e2f45808eac7eaa54918fec6f6e9d291d92c",
    "receipt_stream": "PASS",
    "next_pass": "R3.17F",
}
for entry in [
    "docs/continuity/MIMIR_R3_17E_DECISION.md",
    "docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md",
]:
    if entry not in state["next_files_to_read"]:
        state["next_files_to_read"].append(entry)
state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

# Replace only the canonical state text block in the handbook.
handbook_path = Path("MIMIR_CONTINUE_HERE.md")
handbook = handbook_path.read_text(encoding="utf-8")
section = "# 1. CANONICAL CURRENT STATE BLOCK"
section_pos = handbook.find(section)
if section_pos < 0:
    raise SystemExit("handbook canonical-state section not found")
block_start = handbook.find("```text", section_pos)
block_end = handbook.find("```", block_start + len("```text"))
if block_start < 0 or block_end < 0:
    raise SystemExit("handbook canonical-state fenced block not found")
handbook = handbook[:block_start] + HANDBOOK_BLOCK + handbook[block_end + 3:]
handbook_path.write_text(handbook, encoding="utf-8", newline="\n")

# Normalize trailing whitespace without weakening diff checks.
for rel in [
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_R3_17E_DECISION.md",
    "docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md",
]:
    path = Path(rel)
    text = path.read_text(encoding="utf-8")
    path.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8", newline="\n")

print("R3_17E_ADMISSION_SYNC=PASS")
