from pathlib import Path
import json

PROD = "9bfa837c69c4751f70ca63a17c65f0f89877ff32"
PRE = "4638aeabca8e971805d2e294fea0f24543e9e5a8"
SOURCE_BLOB = "7288238cfb5338653552435be6af41f0dd7a4e85"
TEST_BLOB = "92033a72a8a737605ac3bf91e10d130082277e04"

continue_path = Path("MIMIR_CONTINUE_HERE.md")
text = continue_path.read_text(encoding="utf-8")
replacements = {
'''LAST_PRODUCTION_CODE_SHA:
  c3d4c73ca34febb9f0383c59132a8bc8a363b06b

LAST_PRODUCTION_MILESTONE:
  R3.17C — native primitive scalar attribute decoder implementation''': f'''LAST_PRODUCTION_CODE_SHA:
  {PROD}

LAST_PRODUCTION_MILESTONE:
  R3.17G — direct native evidence-admitted K2 decoder implementation''',
'''LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.17E — K2 object/reference/text wire evidence / Outcome A / 47/47 / 110539 occurrences''': '''LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.17E — K2 object/reference/text wire evidence / Outcome A / 47/47 / 110539 occurrences''',
'''CURRENT_PASS:
  R3.17G — direct native K2 decoder implementation for contract-admitted variants only

CURRENT_PASS_TYPE:
  production implementation / one already-resolved K2 payload only''': '''CURRENT_PASS:
  R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses

CURRENT_PASS_TYPE:
  read-only differential audit / NO production capability widening''',
'''CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar payload may be decoded natively
  stop exactly at payload_end_bit / stop_bit after that one scalar
  NO native K2 decoder, second property, next actor, next frame, K3 or K4 family is admitted''': '''CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload may be decoded natively
  stop exactly at payload_end_bit / stop_bit after that one value
  NO second property, next actor, next frame, unobserved K2, K3 or K4 family is admitted''',
'''R3_17G_OPEN_BOUNDARY:
  implement direct native one-value K2 decoder only for R3.17F-admitted shapes
  reuse NetworkBitCursor and atomic rollback semantics
  synthetic privacy-safe focused vectors only
  expected source scope: crates/mimir-replay/src/lib.rs + r3_17g focused test

R3_17G_HARD_STOP:
  no second property / property-loop continuation
  no unobserved K2 variants
  no K3/K4, lifecycle, raw-state, event, skill, runtime or export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17G PUBLISHES CLEANLY:
  R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses''': f'''R3_17G_PRODUCTION_CLOSURE:
  production SHA: {PROD}
  source blob: {SOURCE_BLOB}
  focused test blob: {TEST_BLOB}
  implementation validation: 31805820332 / 94784362093 SUCCESS
  clean-candidate CI: 31806206582 / 94785622371 SUCCESS
  published-main CI: 31806554445 / 94786777798 SUCCESS
  exact production scope: crates/mimir-replay/src/lib.rs + r3_17g focused test only
  focused tests: 8/8 PASS; mimir-replay total: 189 PASS; workspace clippy: PASS
  native one-value K2: ActiveActor / String / QWordString / admitted UniqueId / admitted PartyLeader
  Cargo/fixture/corpus/support-lane changes: none

R3_17H_OPEN_BOUNDARY:
  read-only differential audit only; production Rust mutation forbidden
  anchor to immutable R3.17E evidence identities and pinned Boxcars SHA
  select the exact 469 privacy-safe R3.17E witness occurrences
  regenerate raw values only ephemerally; persist no clear player/account payloads
  compare native vs pinned oracle shape, exact width/end, context gate and semantic equality in-memory

R3_17H_HARD_STOP:
  no production implementation changes in the audit pass
  no second property / property-loop continuation
  no unobserved K2 variants
  no K3/K4, lifecycle, raw-state, event, skill, runtime or export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17H OUTCOME A:
  decide the next evidence family only after the differential closure is admitted'''
}
for old, new in replacements.items():
    if old not in text:
        if old == new:
            continue
        raise SystemExit(f"missing CONTINUE_HERE replacement block: {old[:80]!r}")
    text = text.replace(old, new, 1)
continue_path.write_text(text, encoding="utf-8", newline="\n")

current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.17G — direct native evidence-admitted K2 decoder implementation`
**Completed K1 differential:** `R3.17D — Outcome A / 96 of 96 exact`
**Completed K2 evidence:** `R3.17E — Outcome A / 47 of 47 / 110539 occurrences`
**Completed K2 contract:** `R3.17F — Outcome A / atomic evidence-supported shapes`
**Current exact pass:** `R3.17H — native K2 differential audit against immutable R3.17E witnesses`

## 1. Truthful production boundary

Production now includes a direct native decoder for exactly one already-resolved R3.17F-admitted K2 payload. It reuses the LSB-first `NetworkBitCursor`, accepts unaligned payload starts, returns exact payload end/width, and fails closed for unsupported tags, malformed/truncated text, unadmitted contexts and unobserved K2 shapes. It does not continue the property loop or mutate actor/frame state.

R3.17G production identity:

```text
production SHA               {PROD}
production source blob       {SOURCE_BLOB}
focused test blob            {TEST_BLOB}
implementation run/job       31805820332 / 94784362093 SUCCESS
clean-candidate CI            31806206582 / 94785622371 SUCCESS
published-main CI             31806554445 / 94786777798 SUCCESS
focused R3.17G tests          8 / 8 PASS
mimir-replay tests            189 PASS
workspace clippy              PASS
production file scope         exactly 2 files
Cargo/corpus/support widening none
```

## 2. Native K2 surface now admitted

```text
ActiveActor     exact 33-bit active + signed actor reference
String          signed-i32 Empty / Windows1252 / UTF16 contract branches
QWordString     legacy QWord64 or RL223 positive Windows1252 only
UniqueId        net10 Steam / PlayStation / PsyNet / Epic(declared=33), observed contexts only
PartyLeader     only Some(Epic declared=33), net10 + RL223 true
```

Unobserved variants remain rejected. Native K2 success authorizes exactly one value and nothing after its `payload_end_bit`.

## 3. R3.17H exact next pass

R3.17H is audit-only. Use the immutable R3.17E evidence authority and the exact 469 privacy-safe witness identities. Regenerate the corresponding raw payload/decoded values ephemerally with pinned Boxcars, feed those exact payloads to the native R3.17G decoder, and compare tag/shape, context gate, exact width/end and decoded semantic value in memory. Persist only privacy-safe hashes/counts/match flags.

No production Rust change is allowed in R3.17H.

## 4. Still closed

```text
unobserved K2 variants
second property / property-loop continuation
next actor / next frame iteration
K3 / K4 families
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
'''
Path("docs/continuity/MIMIR_CURRENT_STATE.md").write_text(current, encoding="utf-8", newline="\n")

graph = f'''# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

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
R3.17E K2 evidence decision             |
R3.17F K2 contract decision             |
R3.17G K2 production decision           |
R3.17H active differential spec         |
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
10. `docs/continuity/MIMIR_R3_17F_DECISION.md`
11. `docs/continuity/MIMIR_R3_17G_EXECUTION_SPEC.md`
12. `docs/continuity/MIMIR_R3_17G_DECISION.md`
13. `docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md`
14. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
15. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
16. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
17. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
18. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
19. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
20. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
 -> R3.14 actor envelope primitives
 -> R3.15 NewActor branch
 -> R3.16 existing-actor first-property header
 -> R3.17A-D K1 primitive scalar wave: CLOSED
      production c3d4c73ca34febb9f0383c59132a8bc8a363b06b
      R3.17D 31798478106 / 94760722134 SUCCESS / 96/96 exact
 -> R3.17E K2 object/reference/text evidence: OUTCOME A / CLOSED
      evidence 19db534a3668f84f1c5ce36ef1252c52841d890f
      authority 31801482588 / 94770260529 SUCCESS
      artifact 9219554878 / sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
      47/47 / 110539 K2 occurrences / 0 structural failures
 -> R3.17F evidence-supported K2 contract admission: OUTCOME A / CLOSED
 -> R3.17G direct native K2 decoder implementation: PRODUCTION / CLOSED
      production {PROD}
      implementation 31805820332 / 94784362093 SUCCESS
      candidate CI 31806206582 / 94785622371 SUCCESS
      published CI 31806554445 / 94786777798 SUCCESS
 -> R3.17H native K2 differential audit: ACTIVE
```

## Current capability lock

Production can natively decode exactly one already-resolved K1 scalar or one R3.17F-admitted K2 payload. K2 success stops exactly at its payload end bit and does not authorize another property, actor, frame or lifecycle mutation.

R3.17H is read-only. It may regenerate raw witness values ephemerally for comparison, but no clear player/account payload may enter durable evidence. PartyLeader `None`, non-Epic PartyLeader and every other unseen K2 variant remain closed.

Property-loop continuation, next actor/frame iteration, lifecycle mutation, K3 spatial/physics and K4 gameplay-structured families remain closed.

## R3.17G production closure

```text
production SHA              {PROD}
source blob                 {SOURCE_BLOB}
focused test blob           {TEST_BLOB}
implementation run/job      31805820332 / 94784362093 SUCCESS
clean candidate CI          31806206582 / 94785622371 SUCCESS
published main CI           31806554445 / 94786777798 SUCCESS
focused tests               8/8 PASS
mimir-replay tests          189 PASS
workspace clippy            PASS
scope                       lib.rs + r3_17g test only
Cargo/corpus/support        unchanged
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
Path("MIMIR_KNOWLEDGE_GRAPH.md").write_text(graph, encoding="utf-8", newline="\n")

state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-14"
state["last_production_code_sha"] = PROD
state["last_production_milestone"] = "R3.17G"
state["last_production_milestone_name"] = "direct native evidence-admitted K2 decoder implementation"
state["last_completed_contract_pass"] = "R3.17F"
state["current_pass"] = "R3.17H"
state["current_pass_kind"] = "read-only native K2 differential audit against immutable R3.17E evidence-supported witnesses"
state["current_pass_goal"] = "Compare the native R3.17G K2 decoder against exact R3.17E witness occurrences using ephemeral pinned-oracle values and privacy-safe durable receipts."
state["current_pass_stop_boundary"] = "Audit only; no production Rust, Cargo, corpus/support-lane, property-loop, lifecycle, K3/K4 or downstream widening."
state["last_completed_production_pass"] = "R3.17G"
state["last_completed_production_outcome"] = "admitted / published; 8 focused tests, 189 mimir-replay tests, clippy and exact-SHA CI PASS"
state["r3_17g"] = {
    "outcome": "admitted / production",
    "pre_pass_main_sha": PRE,
    "production_sha": PROD,
    "production_tree": "86f4419e5cce7f6264119a7530b67177e5ecd08d",
    "source_file": "crates/mimir-replay/src/lib.rs",
    "source_git_blob": SOURCE_BLOB,
    "focused_test_file": "crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs",
    "focused_test_git_blob": TEST_BLOB,
    "focused_tests": 8,
    "mimir_replay_tests": 189,
    "implementation_validation_run": 31805820332,
    "implementation_validation_job": 94784362093,
    "candidate_ci_run": 31806206582,
    "candidate_ci_job": 94785622371,
    "published_main_ci_run": 31806554445,
    "published_main_ci_job": 94786777798,
    "workspace_clippy": "PASS",
    "production_scope_files": [
        "crates/mimir-replay/src/lib.rs",
        "crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs"
    ],
    "cargo_mutation": False,
    "corpus_mutation": False,
    "support_lane_widening": False,
    "native_k2_one_value_decoder": True
}
state["r3_17h"] = {
    "status": "active",
    "pass_kind": "read-only differential audit",
    "witness_identity_source_sha256": "7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b",
    "witness_rows": 469,
    "oracle_sha": "c70e77df7af81b436cb545d070bb90c82f562d0b",
    "production_mutation_allowed": False,
    "privacy_rule": "raw/decoded account values may exist only ephemerally; durable output is structural and hashed"
}
# Keep navigation canonical and place G/H immediately after G spec if possible.
reading = state.get("next_files_to_read", [])
for item in ["docs/continuity/MIMIR_R3_17G_DECISION.md", "docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md"]:
    if item in reading:
        reading.remove(item)
try:
    idx = reading.index("docs/continuity/MIMIR_R3_17G_EXECUTION_SPEC.md") + 1
except ValueError:
    idx = 0
reading[idx:idx] = ["docs/continuity/MIMIR_R3_17G_DECISION.md", "docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md"]
state["next_files_to_read"] = reading
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

decision = f'''# MIMIR — R3.17G Native K2 Decoder Production Decision

**Date:** 2026-08-14
**Pass:** `R3.17G — direct native K2 decoder implementation for contract-admitted variants only`
**Outcome:** **A — ADMITTED / PRODUCTION PUBLISHED**
**Production Rust changed:** **YES, exact two-file scope**

## Frozen authority

```text
pre-pass main                 {PRE}
production SHA                {PROD}
production tree               86f4419e5cce7f6264119a7530b67177e5ecd08d
production source blob        {SOURCE_BLOB}
focused test blob             {TEST_BLOB}
R3.17F contract               Outcome A
R3.17E evidence head          19db534a3668f84f1c5ce36ef1252c52841d890f
pinned Boxcars SHA            c70e77df7af81b436cb545d070bb90c82f562d0b
implementation run/job        31805820332 / 94784362093 SUCCESS
clean-candidate CI            31806206582 / 94785622371 SUCCESS
published-main CI             31806554445 / 94786777798 SUCCESS
```

## Exact production scope

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs
```

No Cargo manifest/lockfile, fixture, replay corpus, support-lane or unrelated crate change was admitted.

## Production capability admitted

`decode_replay_network_k2_v1` directly decodes exactly one already-resolved K2 payload using the existing LSB-first `NetworkBitCursor` semantics. The public result retains exact start/end/width identity and typed semantics. The caller supplies the already-resolved attribute tag plus `net_version` / `is_rl_223` context.

Admitted variants are exactly the R3.17F surface:

```text
ActiveActor
  active:1 + actor:i32 => 33 bits

String
  signed-i32 Empty / positive Windows1252 / negative UTF16LE

QWordString
  !RL223 => u64
  RL223  => positive Windows1252 only

UniqueId at net_version 10
  Steam
  PlayStation in observed RL223 context
  PsyNet in observed RL223 context
  Epic Windows1252 declared length 33

PartyLeader
  only net10 + RL223 + Some(Epic Windows1252 declared=33)
```

Unobserved systems, context combinations and text forms fail closed.

## Failure / stop semantics

Stable failure categories include `invalid-start`, `insufficient-bits`, `invalid-text-length`, `unadmitted-context`, `unadmitted-k2-shape`, and `unsupported-k2-tag`.

The implementation snapshots the payload start and restores the internal cursor on decode failure. Success returns the exact first bit after one K2 value. No success or failure grants permission to decode a second property.

## Text semantics

Windows-1252 decoding is implemented locally without adding a dependency. UTF-16LE uses deterministic lossy surrogate replacement. As frozen by R3.17F, the final declared terminator byte/code unit is omitted semantically but is not required to be numerically zero.

## Validation

The focused R3.17G integration suite contains 8 privacy-safe synthetic tests covering admitted shapes, unaligned starts, exact end bits, truncation, malformed lengths, wrong contexts, unadmitted systems/shapes, unsupported tag and invalid start behavior.

```text
focused tests                         8 / 8 PASS
cargo test -p mimir-replay            189 PASS
cargo clippy --workspace --all-targets -- -D warnings
                                      PASS
scripts/verify_repo.ps1               PASS
clean candidate exact-SHA CI          PASS
published main exact-SHA CI           PASS
```

An initial disposable validation attempt was not admitted because clippy found only two hygiene defects: an empty line after a doc comment and an unread rollback assignment. The corrected v2 retained the same passing behavior tests, removed those lint defects, and is the sole implementation authority listed above.

## Still closed

```text
unobserved K2 variants
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
K3 / K4
raw state / events / replay slices / skills
runtime / export widening
support-lane widening
```

## Next exact pass

`R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses`.
'''
Path("docs/continuity/MIMIR_R3_17G_DECISION.md").write_text(decision, encoding="utf-8", newline="\n")

spec = '''# MIMIR R3.17H — Native K2 Differential Audit Execution Spec

**Pass type:** read-only differential audit
**Production implementation:** forbidden
**Native authority:** R3.17G production Outcome A
**Evidence authority:** R3.17E Outcome A

## Goal

Prove that the direct native R3.17G K2 decoder agrees with the pinned Boxcars oracle on the exact privacy-safe witness occurrences selected by immutable R3.17E evidence, without widening production capability.

## Frozen identities

```text
native production SHA        9bfa837c69c4751f70ca63a17c65f0f89877ff32
native source blob           7288238cfb5338653552435be6af41f0dd7a4e85
R3.17E evidence head         19db534a3668f84f1c5ce36ef1252c52841d890f
R3.17E artifact              9219554878
R3.17E artifact digest       sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
R3.17E witnesses SHA256      7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
R3.17E witness rows          469
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
```

## Audit method

1. Verify fresh main and the exact native source blob before doing any evidence work.
2. Verify the 47 replay identities used by R3.17E.
3. Recreate the pinned Boxcars instrumentation from the canonical R3.17E evidence tooling or an exactly equivalent reviewed patch.
4. Decode the 47 replay lane and regenerate raw K2 payload bits plus oracle semantic values only in ephemeral runner storage.
5. Select exactly the 469 witness occurrence identities from immutable `r3_17e_k2_witnesses.jsonl` using structural keys such as replay path, frame, actor ordinal, stream/property identity, tag, context, start/end/width and packed-payload SHA256.
6. Feed each selected packed payload to `decode_replay_network_k2_v1` under the witness context. A temporary audit harness may normalize the witness payload start to bit zero only if it proves the packed bit sequence is identical.
7. Compare native vs oracle in memory for tag/variant, context acceptance, exact consumed width/end, text encoding/declared length, reference/system fields and decoded semantic value.
8. Persist only privacy-safe aggregate rows, structural identifiers, match flags and cryptographic hashes. Do not persist clear player names, account ids, remote ids or replay-private text.

## Required audit gates

```text
witness rows selected                 469 / 469
native decode success                 469 / 469
attribute tag / semantic variant      469 / 469 exact
payload width                         469 / 469 exact
payload end / consumed bits           469 / 469 exact
context gate                          469 / 469 exact
semantic value                        469 / 469 exact in-memory
privacy scan                          PASS
production mutation                   0
Cargo mutation                        0
corpus/fixture mutation               0
```

If a witness cannot be regenerated or matched unambiguously, do not silently replace it. Outcome B must request targeted evidence for the missing identity.

## Required negative controls

The audit harness must also prove that selected nearby unadmitted variants remain rejected, using synthetic privacy-safe payloads only. At minimum cover PartyLeader None, a non-Epic PartyLeader, an unadmitted UniqueId system, wrong net version, RL223 QWordString Empty/UTF16, and wrong Epic declared length.

These negative controls are audit-only and do not widen the production contract.

## Outcome rules

- **Outcome A:** all 469 immutable witnesses match exactly, all negative controls fail closed as contracted, privacy scan passes, and production/Cargo/corpus mutation is zero.
- **Outcome B:** a bounded witness/evidence ambiguity exists; request targeted evidence only.
- **Outcome C:** a native/oracle semantic contradiction or reproducible decoder defect exists; stop widening and open a corrective implementation pass.

## Hard stop

R3.17H must not change production Rust, manifests, fixtures, supported replay policy or downstream capability. It does not admit second-property continuation, actor/frame iteration, lifecycle mutation, K3/K4, raw state, events, replay slicing, skills, runtime or export.

## Next pass

Do not pre-commit the next attribute family. On Outcome A, inspect the remaining canonical roadmap and evidence gaps, then open the first still-unfinished evidence pass under the same evidence -> contract -> implementation -> audit discipline.
'''
Path("docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md").write_text(spec, encoding="utf-8", newline="\n")

print("R3.17G continuity + R3.17H spec applied")
