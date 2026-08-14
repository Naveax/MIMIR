from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "ebc0fa31ba90a8496c3d1719e436d2c17b605ff7"

# 1) Repair the canonical current-state block in the master handbook without
# rewriting the rest of the long-form execution manual.
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
  R3.16A — existing-actor first-property envelope evidence / Outcome A

LAST_COMPLETED_CONTINUITY_CHECK:
  R3.16C — post-implementation continuity repair and capability-boundary check

CURRENT_PASS:
  R3.17A — primitive scalar attribute wire-format evidence

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
  existing-actor first-property header stops exactly at payload_start_bit
  NO native attribute payload bit is admitted yet

R3_16B_CLOSURE:
  base main SHA: fc020729396ad9f62ee4b8fd8fe6808f5bdb5489
  production SHA: ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
  production source blob: 625ab2322e35f5f835871d42b9efeb04f5c299ab
  production source SHA256: 186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28
  focused tests: 8/8 PASS
  frozen differential: 47/47 PASS
  clean diff: exactly 2 files, +331/-0
  post-main CI: 31788526050 / 94729854512 SUCCESS
  post-main Knowledge Archive: 31788566184 / 94729983908 SUCCESS

R3_17A_OPEN_BOUNDARY:
  evidence may observe primitive scalar attribute payload wire formats through the pinned oracle
  candidate family: Boolean, Byte, Int, Int64, Float, Enum
  record corpus frequency, exact bit spans, values, truncation-relevant structure, and identity
  zero-observation tags remain unadmitted rather than guessed

R3_17A_HARD_STOP:
  production Rust unchanged
  no native payload decoder
  no RigidBody / ActiveActor / spatial-family implementation
  no property-loop iteration
  no second property, actor, or frame
  no actor lifecycle mutation
  no raw-state/event/skill/runtime/export widening

IN_FLIGHT_NON_PRODUCTION_BRANCH:
  none admitted at continuity sync time

NEXT PASS IF R3.17A OUTCOME A:
  R3.17B — primitive scalar attribute contract admission
```'''
text = text[:code_start] + block + text[code_end + 3:]
continue_path.write_text(text, encoding="utf-8", newline="\n")

# 2) Rewrite the deliberately-current state document. Historical detail remains
# in decisions/state JSON; this file should not lie about current production.
current_state = '''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14  
**Repository:** `Naveax/MIMIR`  
**Canonical main / production checkpoint:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`  
**Production milestone:** `R3.16B — native existing-actor first-property envelope header implementation`  
**Completed continuity check:** `R3.16C`  
**Next exact pass:** `R3.17A — primitive scalar attribute wire-format evidence`

---

## 1. Current truthful production boundary

MIMIR can natively advance through the admitted replay network prefix far enough to:

```text
frame time/delta
first actor present/id/alive/new envelope
NewActor name/object/spawn trajectory branch
existing-actor one-property-present decision
one canonical bounded stream_id
existing static/inherited property lookup resolution
resolved property object/tag metadata
payload_start_bit
```

Production then **stops before the first attribute payload bit**.

The R3.16B production result is intentionally a header/context primitive. It does not scan for later existing actors, iterate a property loop, mutate actor lifecycle state, or decode attribute values.

## 2. R3.16B admitted identity

```text
pre-pass canonical main       fc020729396ad9f62ee4b8fd8fe6808f5bdb5489
clean production SHA          ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
production source             crates/mimir-replay/src/lib.rs
source Git blob               625ab2322e35f5f835871d42b9efeb04f5c299ab
source SHA-256                186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28
permanent focused test        crates/mimir-replay/tests/r3_16b_property_header.rs
test Git blob                 0fea53e1758e7b0b5f8d2a14b98cbce5feb400c2
clean diff                    2 files, +331 / -0
focused tests                 8 / 8 PASS
frozen oracle rows            47
native differential           47 / 47 PASS
```

R3.16B reuses the canonical bounded-u32 primitive. `prop_id_bits` is not treated as a fixed-width permission; actual stream-ID consumption remains value/bound dependent.

## 3. R3.16B hosted validation and publication closure

```text
disposable full verifier + differential run/job  31787682424 / 94727174844  SUCCESS
candidate PR CI run/job                           31788230442 / 94728918384  SUCCESS
candidate Knowledge Archive run/job               31788291777 / 94729116078  SUCCESS
published-main CI run/job                         31788526050 / 94729854512  SUCCESS
published-main Knowledge Archive run/job           31788566184 / 94729983908  SUCCESS
publication                                        force=false fast-forward
```

The clean production commit contains only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_16b_property_header.rs` relative to its parent. Temporary evidence/publisher machinery did not enter canonical production history.

## 4. Current closed boundaries

Still closed:

```text
native attribute payload decoding of every tag
second property / property loop
complete existing-actor update parsing
next actor iteration
next frame iteration
actor lifecycle state-table mutation
raw-state materialization
semantic ball/car/player reconstruction
event extraction
replay slicing
skill mining
counterfactual rollout execution
training/runtime/export widening
support-lane expansion
```

Observed tag names are not payload contracts. In particular, seeing `RigidBody`, `ActiveActor`, `Byte`, `Float`, or `Int` in oracle evidence does not mean MIMIR can natively decode those payloads.

## 5. R3.17A exact next pass

R3.17A is evidence-only and begins the roadmap's attribute decoder family program with primitive scalar payloads:

```text
Boolean
Byte
Int
Int64
Float
Enum
```

The pass must use the pinned Boxcars revision and the exact supported 47-replay lane. It should measure actual occurrences first, then collect exact payload start/end bits, raw/decoded values, tag/object identity, and enough surrounding structure to define truncation/fail-closed rules later.

A tag with zero usable observations is **not admitted by analogy**. It remains closed or receives a targeted evidence follow-up.

R3.17A changes no production Rust. Outcome A may open `R3.17B — primitive scalar attribute contract admission`.
'''
(ROOT / "docs/continuity/MIMIR_CURRENT_STATE.md").write_text(current_state, encoding="utf-8", newline="\n")

# 3) Update machine-readable continuity while preserving all historical pass data.
state_path = ROOT / "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state.update({
    "updated_date": "2026-08-14",
    "last_production_code_sha": BASE,
    "last_production_milestone": "R3.16B",
    "last_production_milestone_name": "native existing-actor first-property envelope header implementation",
    "last_completed_read_only_audit": "R3.16A",
    "last_completed_continuity_check": "R3.16C",
    "current_pass": "R3.17A",
    "current_pass_kind": "evidence-only primitive scalar attribute wire-format audit",
    "current_pass_goal": "Measure and freeze exact oracle wire behavior for Boolean/Byte/Int/Int64/Float/Enum payloads on the exact supported 47-replay lane, without changing production Rust.",
    "current_pass_stop_boundary": "Production remains stopped at payload_start_bit; no native payload decoder, property loop, actor/frame iteration, lifecycle mutation, raw-state/event/skill/runtime/export widening, or guessed contract for zero-observation tags.",
    "last_completed_evidence_pass": "R3.16A",
    "last_completed_evidence_outcome": "A — 47/47 existing-actor first-property envelope rows resolved exactly; zero identity/oracle/lookup/mismatch/mutation errors; immutable job-log receipt PASS",
})
state["r3_16b"] = {
    "outcome": "A — admitted / production",
    "pre_pass_main_sha": "fc020729396ad9f62ee4b8fd8fe6808f5bdb5489",
    "production_sha": BASE,
    "source_file": "crates/mimir-replay/src/lib.rs",
    "source_git_blob": "625ab2322e35f5f835871d42b9efeb04f5c299ab",
    "source_sha256": "186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28",
    "test_file": "crates/mimir-replay/tests/r3_16b_property_header.rs",
    "test_git_blob": "0fea53e1758e7b0b5f8d2a14b98cbce5feb400c2",
    "focused_tests": 8,
    "oracle_rows": 47,
    "differential_match": "47/47",
    "disposable_validation_run": 31787682424,
    "disposable_validation_job": 94727174844,
    "candidate_ci_run": 31788230442,
    "candidate_ci_job": 94728918384,
    "candidate_knowledge_run": 31788291777,
    "candidate_knowledge_job": 94729116078,
    "published_main_ci_run": 31788526050,
    "published_main_ci_job": 94729854512,
    "published_main_knowledge_run": 31788566184,
    "published_main_knowledge_job": 94729983908,
    "changed_files": 2,
    "additions": 331,
    "deletions": 0,
    "publication_force": False,
    "payload_bits_consumed": False,
    "next_pass": "R3.16C",
}
state["r3_16c"] = {
    "outcome": "A — continuity repaired / capability boundary confirmed",
    "production_source_changed": False,
    "production_sha": BASE,
    "confirmed_hard_stop": "payload_start_bit before attribute payload",
    "next_pass": "R3.17A",
}
closed = list(state.get("closed_now", []))
for item in [
    "native attribute payload decode",
    "native property loop iteration beyond the first admitted header",
    "second property consumption",
    "full actor envelope iteration",
    "full frame iteration",
    "actor state table mutation",
    "raw-state extraction",
    "event extraction",
    "replay slicing",
    "skill mining",
    "counterfactual rollout execution from native replay state",
]:
    if item not in closed:
        closed.append(item)
state["closed_now"] = closed
reads = list(state.get("next_files_to_read", []))
for item in [
    "docs/continuity/MIMIR_R3_16B_DECISION.md",
    "docs/continuity/MIMIR_R3_16C_EXECUTION_SPEC.md",
    "docs/continuity/MIMIR_R3_16C_DECISION.md",
    "docs/continuity/MIMIR_R3_17A_EXECUTION_SPEC.md",
]:
    if item not in reads:
        reads.append(item)
state["next_files_to_read"] = reads
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

# 4) Keep the root graph short and current; historical details stay in decisions.
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
R3.16B decision                         |
R3.16C continuity decision              |
R3.17A execution spec                   |
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
4. `docs/continuity/MIMIR_R3_16B_DECISION.md`
5. `docs/continuity/MIMIR_R3_16C_EXECUTION_SPEC.md`
6. `docs/continuity/MIMIR_R3_16C_DECISION.md`
7. `docs/continuity/MIMIR_R3_17A_EXECUTION_SPEC.md`
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
  -> R3.14A-E bit cursor + first actor envelope evidence/production/audit
  -> R3.15A-D NewActor evidence/contract/implementation/differential
  -> R3.16A first existing-actor property-header evidence: 47/47
  -> R3.16B production property-header reader: ADMITTED
       production SHA ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
       exact hard stop payload_start_bit
  -> R3.16C continuity/check: CLOSED / Outcome A
  -> R3.17A primitive scalar attribute wire-format evidence: ACTIVE
```

## Current capability lock

MIMIR can resolve one existing-actor property header through `stream_id`, property lookup and tag identity, then stops at `payload_start_bit`.

It still **cannot natively decode any attribute payload**. Oracle visibility into `RigidBody`, `ActiveActor`, `Byte`, `Float`, `Int`, or any other tag is not production capability.

R3.17A is evidence-only for the primitive scalar family (`Boolean`, `Byte`, `Int`, `Int64`, `Float`, `Enum`). Zero-observation tags remain closed.

## R3.16B closure identity

```text
base main                 fc020729396ad9f62ee4b8fd8fe6808f5bdb5489
production SHA            ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
source blob               625ab2322e35f5f835871d42b9efeb04f5c299ab
source SHA256             186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28
focused tests             8/8 PASS
native differential       47/47 PASS
post-main CI              31788526050 / 94729854512 SUCCESS
post-main knowledge       31788566184 / 94729983908 SUCCESS
```

## Authority rule

```text
current code/tests
> exact-SHA CI/evidence
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

# 5) Immutable closure/next-pass docs.
r316b = '''# MIMIR — R3.16B Decision

**Date:** 2026-08-14  
**Outcome:** `A — implementation exact / admitted to production`  
**Production SHA:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`

## Decision

The narrow native existing-actor first-property header implementation is admitted. It consumes one `property_present` decision and, when present, one canonical bounded `stream_id`, resolves the existing static/inherited property context, records the exact payload boundary, and stops before consuming attribute payload bits.

## Frozen closure evidence

```text
base main                              fc020729396ad9f62ee4b8fd8fe6808f5bdb5489
disposable implementation authority    d843906a33321a3bde06a44e7187e92dd0c1d436
disposable verifier/differential       31787682424 / 94727174844 SUCCESS
clean production SHA                   ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
source Git blob                        625ab2322e35f5f835871d42b9efeb04f5c299ab
source SHA-256                         186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28
focused test Git blob                  0fea53e1758e7b0b5f8d2a14b98cbce5feb400c2
focused tests                          8/8 PASS
immutable R3.16A rows                  47
native differential                    47/47 PASS
clean diff                             exactly 2 files, +331/-0
candidate CI                           31788230442 / 94728918384 SUCCESS
candidate Knowledge Archive            31788291777 / 94729116078 SUCCESS
published-main CI                      31788526050 / 94729854512 SUCCESS
published-main Knowledge Archive       31788566184 / 94729983908 SUCCESS
publication                            force=false fast-forward
```

## Scope audit

Canonical production changed only:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_16b_property_header.rs`

No Cargo manifest/lockfile, replay fixture/corpus, workflow, evidence tool, export crate, runtime, teacher, skill, or training surface entered the production commit.

## Hard stop preserved

No attribute payload bit is consumed. No second property, property loop, next actor/frame, lifecycle mutation, raw-state/event/skill/runtime/export capability is admitted.

## Next exact pass

`R3.16C — implementation continuity/check`.
'''
(ROOT / "docs/continuity/MIMIR_R3_16B_DECISION.md").write_text(r316b, encoding="utf-8", newline="\n")

r316c_spec = '''# MIMIR — R3.16C Execution Spec

**Date:** 2026-08-14  
**Pass:** `R3.16C — implementation continuity/check`  
**Kind:** continuity sync / post-publication capability audit  
**Production base:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`

## Goal

Reconcile canonical continuity with already-published R3.16B repository truth and verify that publication opened no boundary beyond the admitted one-property header.

## Allowed surface

Continuity/docs state only. Production Rust, Cargo files, corpus/fixtures, workflows and tools are forbidden in the clean R3.16C commit.

## Required checks

- exact main is the admitted R3.16B production SHA;
- clean parent diff is exactly the two admitted R3.16B files;
- permanent focused tests exist and describe the payload hard stop;
- R3.16B hosted candidate and post-main gates are green;
- master handbook/current state/machine state/knowledge graph no longer claim an older active pass;
- no text claims native payload decoding;
- next work follows the roadmap's evidence-first attribute decoder family program.

## Outcome A

Continuity is repaired without production mutation. Open `R3.17A — primitive scalar attribute wire-format evidence`.

## Hard stop

R3.16C cannot modify or reinterpret replay parser behavior.
'''
(ROOT / "docs/continuity/MIMIR_R3_16C_EXECUTION_SPEC.md").write_text(r316c_spec, encoding="utf-8", newline="\n")

r316c_decision = '''# MIMIR — R3.16C Decision

**Date:** 2026-08-14  
**Outcome:** `A — continuity repaired / capability boundary confirmed`  
**Production SHA remains:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`

R3.16C confirms that R3.16B is production reality and that the native decoder still stops exactly at `payload_start_bit` before any attribute payload.

This pass changes continuity/docs only. It does not widen replay parsing, actor lifecycle, raw state, events, skills, training, runtime, export, dependencies, fixtures, or corpus coverage.

The stale R3.14-era master/current-state/knowledge-graph pointers are superseded by the synchronized R3.16B closure identity.

**Next exact pass:** `R3.17A — primitive scalar attribute wire-format evidence`.
'''
(ROOT / "docs/continuity/MIMIR_R3_16C_DECISION.md").write_text(r316c_decision, encoding="utf-8", newline="\n")

r317a = '''# MIMIR — R3.17A Execution Spec

**Date:** 2026-08-14  
**Pass:** `R3.17A — primitive scalar attribute wire-format evidence`  
**Kind:** evidence-only / pinned oracle instrumentation  
**Frozen production base:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`

## 1. Goal

Begin the roadmap's attribute-decoder family program with the smallest low-ambiguity scalar family. Measure real supported-corpus behavior before admitting a native payload contract.

Candidate tags:

```text
Boolean
Byte
Int
Int64
Float
Enum
```

A candidate tag with no usable observations remains unadmitted. Do not infer its wire format from naming similarity.

## 2. Corpus and oracle

```text
MIMIR production base: ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
supported replay lane: 47 exact replays
checked-in corpus identity rules: unchanged
oracle: nickbabcock/boxcars
oracle SHA: c70e77df7af81b436cb545d070bb90c82f562d0b
```

The oracle is observation-only and must not become a production dependency.

## 3. Evidence selection

Scan the exact supported lane for existing-actor property updates resolving to the candidate scalar tags. Record full occurrence counts before selecting bounded witness rows.

For each usable witness capture at least:

```text
replay identity
frame index / actor index or equivalent stable position
actor context object ID/name
property object ID/name
attribute tag
property payload start bit
property payload end bit
exact consumed width
raw bits or lossless raw value representation
decoded oracle value
any build/version gate relevant to wire shape
next structural cursor position needed to prove exact end
```

Preserve enough identity to reproduce each row independently.

## 4. Required questions

For every observed candidate tag determine, from evidence rather than assumption:

- exact bit width or value-dependent width;
- signedness / integer representation where relevant;
- endianness / bit order interaction;
- float representation and whether raw IEEE bits must be preserved for exact differential comparison;
- enum/object lookup dependence if `Enum` is not a simple scalar in all builds;
- truncation points that a future native decoder must fail closed on;
- whether the wire shape changes by build/version/object context.

## 5. Required aggregate report

At minimum:

```text
replays_total = 47
oracle_decode_success count
per-tag occurrence count
per-tag usable witness count
per-tag unique consumed widths
per-tag min/max or representative value distribution when meaningful
identity_error_count
oracle_error_count
bit_monotonicity_failure_count
unexpected_tag_shape_count
production_mutation_count = 0
Cargo_mutation_count = 0
corpus_mutation_count = 0
```

## 6. Hard stop

R3.17A may inspect payloads through the pinned oracle but must not:

```text
change production Rust
decode payloads natively in MIMIR
implement RigidBody / ActiveActor / Location / spatial families
iterate a native second property
advance native actor/frame loops
mutate lifecycle state
materialize raw game state or semantic events
open replay slicing / skill / teacher / runtime / export surfaces
change Cargo dependencies
change replay fixtures/corpus
```

## 7. Outcome rules

### Outcome A

At least one candidate scalar tag has reproducible, exact, non-contradictory wire evidence sufficient for a narrow contract; all observed candidate shapes are classified; production/Cargo/corpus mutation remains zero.

Proceed to `R3.17B — primitive scalar attribute contract admission`. The contract may admit only the tags actually supported by evidence.

### Outcome B

Evidence is real but one or more candidate tags have multiple/unclear shapes or insufficient observations. Split the smallest tag-specific evidence follow-up. Do not generalize.

### Outcome C

Oracle identity, cursor accounting, or prior property-header assumptions contradict current evidence. Stop and reopen the relevant earlier contract before any payload implementation.

## 8. Publication policy

Evidence branch only. Temporary instrumentation/scripts/workflows are not production. After Outcome A/B/C, admit only bounded decision/spec/continuity artifacts; production source remains exactly the frozen R3.16B SHA.
'''
(ROOT / "docs/continuity/MIMIR_R3_17A_EXECUTION_SPEC.md").write_text(r317a, encoding="utf-8", newline="\n")

print("R3_16C_CONTINUITY_PATCH=PASS")
