#!/usr/bin/env python3
import json
from pathlib import Path

MAIN = "63f5de4e49abaf76fe6441a255a1a6770388a63c"
PROD = "2b608aafae97b10ecbc884f99e4bd4a73abf7a5c"
PROD_TREE = "b130caf211ce72577870c70d6c0d87cd006e1b29"
EVIDENCE = "1db03fddabf84bfa189f983fa4a3b9110d105442"
EVIDENCE_TREE = "be84d7709d60477bcbb916a11b4496dbddac2ab2"
ARTIFACT_DIGEST = "sha256:340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected one occurrence, got {n}")
    return text.replace(old, new, 1)


# 1) Handbook
p = "MIMIR_CONTINUE_HERE.md"
t = read(p)
t = replace_once(t,
"LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18F — second-property-header real-replay evidence / Outcome A / 47 continuation headers exact + 47 terminator negatives / 0 mismatch",
"LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18H — published R3.18G second-header real-replay differential audit / Outcome A / 94/94 exact / 0 mismatch",
"handbook last audit")
t = replace_once(t,
"LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18F — second-property-header real-replay evidence / Outcome A / 47/47 continuation headers / 47/47 terminators / 0 mismatch / second payload + third property 0 + 0",
"LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18H — published R3.18G second-header differential / Outcome A / 47 terminators + 47 continuations / Int=46 String=1 / 0 mismatch / second payload + third property 0 + 0",
"handbook last evidence")
t = replace_once(t,
"CURRENT_PASS:\n  R3.18H — production second-property-header real-replay differential audit\n\nCURRENT_PASS_TYPE:\n  read-only evidence / differential validation of published R3.18G over the frozen R3.18F 47-replay terminator/continuation lane",
"CURRENT_PASS:\n  R3.18I — second-property payload contract/evidence audit\n\nCURRENT_PASS_TYPE:\n  read-only evidence / characterize exactly one second-property payload on the frozen R3.18F continuation lane; no production composition and no third-property access",
"handbook current pass")
t = replace_once(t,
"  R3.18H is read-only differential validation of that published production API over the frozen 47 terminator + 47 continuation lane; second payload and third-property consumption must remain 0/0\n  NO second-property payload decode, third property, repeated/generalized property loop, K2/K3/K4 wrapper composition, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
"  R3.18H closed Outcome A on the published R3.18G API: 94/94 frozen rows exact, 47 terminators + 47 continuations, Int=46/String=1, 32 real header truncation negatives, mismatch 0, second payload + third-property consumption 0/0\n  R3.18I is read-only evidence only: on the same frozen lane, characterize exactly one second payload after the admitted second header; 46 Int rows and 1 String row must be handled as separate observed tag classes, with 47 terminators remaining no-payload/no-lookup controls\n  NO production second-property payload composition, third property/control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
"handbook hard stop")
closure = '''R3_18H_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at 2b608aafae97b10ecbc884f99e4bd4a73abf7a5c
  authority head/tree: 1db03fddabf84bfa189f983fa4a3b9110d105442 / be84d7709d60477bcbb916a11b4496dbddac2ab2
  authority run/job: 31960174729 / 95196833572 SUCCESS
  exact-head normal CI: 31960174713 / 95196833409 SUCCESS
  artifact: 9267045757 / size 12070 bytes
  artifact digest: sha256:340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645
  frozen R3.18F replay identity SHA256: b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
  frozen R3.18F witness SHA256: 99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
  94/94 native rows exact / 47 terminator + 47 continuation
  continuation tags: Int=46 / String=1
  terminator None/no-lookup: 47/47; real header truncation rows: 32
  unresolved-stream negative: PASS; tag-outside-Int/String negative: PASS
  repeatability: PASS; post-stop poison: PASS
  second payload / third property bits consumed: 0 / 0
  mismatch count: 0
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0
  artifact file SHA256: source_scope=38ff92a2448883802b73ea4e2ee0a65f18b83beb782d8f8c87451e2295f37fb8; replay_identity=b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf; frozen_witnesses=99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7; oracle_regeneration=97767f90f5f9d46afcb68f568cf28d021f2081ddbf62bb5f2536d8d7d1bf569e; comparison=de4ca9d70fb7f56aec1c279473c3289b236cfa48e3a17f1faec8942ac3548d10; negatives=4d0273b85c5af2ae2e2b1fd7b88fd5d876c210d1a20f4cdd544601d649c053c9; aggregate=4357bc88426ac50da065875f56bc2f806158080767292c6210623091f6fdc31b

'''
t = replace_once(t, "R3_17E_EVIDENCE_CLOSURE:\n", closure + "R3_17E_EVIDENCE_CLOSURE:\n", "handbook closure insertion")
marker = "# CURRENT PASS CHECKLIST — R3.18H\n"
idx = t.rfind(marker)
if idx < 0:
    raise SystemExit("handbook current checklist marker missing")
t = t[:idx] + '''# R3.18H EVIDENCE CLOSURE — 2026-08-16

```text
Outcome: A — ADMITTED / READ-ONLY EVIDENCE
authority head/tree: 1db03fddabf84bfa189f983fa4a3b9110d105442 / be84d7709d60477bcbb916a11b4496dbddac2ab2
custom evidence run/job: 31960174729 / 95196833572 SUCCESS
same-head normal CI: 31960174713 / 95196833409 SUCCESS
artifact: 9267045757
artifact digest: sha256:340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645
rows: 94/94 exact = 47 terminator + 47 continuation
continuation tags: Int=46 / String=1
header truncation rows: 32
terminator no-lookup rows: 47
unresolved-stream / disallowed-tag / repeatability / poison: PASS
second payload / third property bits: 0 / 0
mismatch: 0
production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0
```

Production authority remains R3.18G `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`. R3.18H admitted evidence only.

# CURRENT PASS CHECKLIST — R3.18I

- [ ] Fresh-read `main`; require R3.18G production authority unchanged except continuity-only commits after it.
- [ ] Freeze R3.18H authority receipt and the exact R3.18F 94-row lane; no witness reselection.
- [ ] Keep all 47 terminators as no-second-payload/no-lookup negative controls.
- [ ] For exactly 47 continuations, start only at the already-proven second `payload_start_bit`.
- [ ] Characterize the 46 `Int` payloads separately from the single `String` payload; do not infer cross-tag equivalence.
- [ ] Compare pinned Boxcars payload end + semantic value against existing native lower-level decoders where their already-admitted contracts apply.
- [ ] Record exact payload start/end/width and semantic equality; no third `property_present` bit may be read.
- [ ] Require deterministic repeatability, truncation-at-payload boundaries, post-stop poison invariance and wrong-context/tag fail-closed controls.
- [ ] Produce privacy-safe immutable evidence with per-file SHA256 receipt.
- [ ] Run full regression/workspace/clippy/repository verification and same-head normal CI.
- [ ] Require production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.
- [ ] Outcome A may only open a separate bounded second-property payload production-composition pass; if String remains unresolved, open a narrower String payload evidence/contract pass instead. No third property or loop.
'''
write(p, t)

# 2) Knowledge graph
p = "MIMIR_KNOWLEDGE_GRAPH.md"
t = read(p)
t = replace_once(t,
"R3.18H active production second-header differential spec                      |",
"R3.18H production second-header differential decision                         |\nR3.18I active second-property payload evidence spec                              |",
"kg graph")
t = replace_once(t,
"48. `docs/continuity/MIMIR_R3_18H_EXECUTION_SPEC.md`\n49. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n50. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n51. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n52. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n53. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n54. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n55. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
"48. `docs/continuity/MIMIR_R3_18H_EXECUTION_SPEC.md`\n49. `docs/continuity/MIMIR_R3_18H_DECISION.md`\n50. `docs/continuity/MIMIR_R3_18I_EXECUTION_SPEC.md`\n51. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n52. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n53. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n54. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n55. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n56. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n57. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
"kg reading order")
t = replace_once(t,
" -> R3.18H production second-header real-replay differential audit: ACTIVE / READ-ONLY EVIDENCE\n      reuse frozen R3.18F 47 terminator + 47 continuation rows against published R3.18G; require 94/94 exact, Int=46/String=1, mismatch 0 and second-payload/third-property bits 0/0",
" -> R3.18H production second-header real-replay differential audit: OUTCOME A / CLOSED\n      authority 1db03fddabf84bfa189f983fa4a3b9110d105442 / 31960174729 / 95196833572 SUCCESS; exact-head CI 31960174713 / 95196833409 SUCCESS\n      artifact 9267045757 / sha256:340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645\n      94/94 exact = 47 terminator + 47 continuation / Int=46 String=1 / 32 truncation / 47 no-lookup / mismatch 0 / second payload + third property 0+0\n -> R3.18I second-property payload contract/evidence audit: ACTIVE / READ-ONLY EVIDENCE\n      frozen continuation lane only: characterize exactly 46 Int + 1 String second payload through payload end; 47 terminators remain no-payload controls; no third property/control bit and no loop",
"kg chain")
old_cap = "Production at `4adadd185783954c7fb6ad67db14b77b377cdde5` includes R3.18B's one-property K1 wrapper plus R3.18D's structurally tied after-first-property control reader. After one valid R3.18B first K1 property, production may read exactly one next `property_present` bit and stop one bit later. It still cannot decode the second stream ID, second property header/tag, or second payload, and it does not expose a generalized repeated property loop. R3.18E closed Outcome A with 94/94 exact real-replay control rows and zero second-property consumption. R3.18F is read-only evidence for only the second-property header boundary through payload_start; production second-property composition remains closed."
new_cap = "Production at `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c` includes R3.18B's one-property K1 wrapper, R3.18D's structurally tied next-property control, and R3.18G's bounded optional second-property header composition. After one valid first K1 property, production may return `None` for a false next-property bit or resolve exactly one second header in the observed `Int|String` contexts and stop at that header's `payload_start`. It still cannot decode the second payload, read a third property/control bit, or expose a generalized repeated property loop. R3.18H closed Outcome A with 94/94 exact published-production differential rows and zero second-payload/third-property consumption. R3.18I may inspect exactly one second payload read-only on the frozen continuation lane, but production composition remains closed."
t = replace_once(t, old_cap, new_cap, "kg capability lock")
t = replace_once(t,
"R3.18F may observe only a second-property header boundary read-only; production second-property composition/payload, repeated loops, K2/K3/K4 wrapper composition, next actor/frame iteration and lifecycle mutation remain closed.",
"R3.18F proved the second header boundary, R3.18G published that bounded header composition, and R3.18H differentially validated it with zero mismatch. R3.18I may characterize exactly one second payload read-only; production second-payload composition, any third property/repeated loop, next actor/frame iteration and lifecycle mutation remain closed.",
"kg narrative")
write(p, t)

# 3) JSON state
p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
d = json.loads(read(p))
d["updated_date"] = "2026-08-16"
d["last_production_code_sha"] = PROD
d["last_production_milestone"] = "R3.18G"
d["last_completed_read_only_audit"] = "R3.18H"
d["last_completed_evidence_pass"] = "R3.18H"
d["last_completed_evidence_outcome"] = "A — published R3.18G differential exact on 94/94 frozen rows; 47 terminator + 47 continuation; Int=46/String=1; 32 truncation; mismatch 0; second payload/third property 0/0"
d["current_pass"] = "R3.18I"
d["current_pass_kind"] = "read-only evidence / second-property payload contract and boundary characterization"
d["current_pass_goal"] = "On the frozen R3.18F/R3.18H lane, characterize exactly one second-property payload for all 47 continuation rows (Int=46, String=1) and compare oracle/native semantics and payload end without reading a third property."
d["current_pass_stop_boundary"] = "Terminators stop at R3.18G control end. Continuations may read exactly from proven second payload_start through that one payload end. Do not read the next property_present bit; no third property, loop, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening."
d["closed_now"] = [
    "production second-property payload composition or semantic value claim",
    "third property control/header/payload observation or generalized production property_present loop",
    "generic repeatedly-chainable public property cursor",
    "second-header tag context outside the exact R3.18F observed Int/String set in the R3.18G composition",
    "next actor / next frame iteration",
    "actor state table mutation",
    "raw-state extraction",
    "event extraction",
    "replay slicing",
    "skill mining",
    "counterfactual rollout execution from native replay state"
]
reads = d["next_files_to_read"]
for item in ["docs/continuity/MIMIR_R3_18H_DECISION.md", "docs/continuity/MIMIR_R3_18I_EXECUTION_SPEC.md"]:
    if item in reads:
        reads.remove(item)
anchor = reads.index("docs/continuity/MIMIR_R3_18H_EXECUTION_SPEC.md") + 1
reads[anchor:anchor] = ["docs/continuity/MIMIR_R3_18H_DECISION.md", "docs/continuity/MIMIR_R3_18I_EXECUTION_SPEC.md"]
d["r3_18h"] = {
    "outcome": "A — admitted / read-only evidence",
    "production_source_changed": False,
    "production_sha": PROD,
    "production_tree": PROD_TREE,
    "authority_head_sha": EVIDENCE,
    "authority_tree": EVIDENCE_TREE,
    "authority_run": 31960174729,
    "authority_job": 95196833572,
    "exact_head_normal_ci_run": 31960174713,
    "exact_head_normal_ci_job": 95196833409,
    "artifact_id": 9267045757,
    "artifact_digest": ARTIFACT_DIGEST,
    "artifact_size_bytes": 12070,
    "frozen_rows": 94,
    "terminator_rows": 47,
    "continuation_rows": 47,
    "continuation_int": 46,
    "continuation_string": 1,
    "header_truncation_rows": 32,
    "terminator_no_lookup_rows": 47,
    "native_oracle_mismatch": 0,
    "second_payload_bits_consumed": 0,
    "third_property_bits_consumed": 0,
    "production_cargo_fixture_corpus_support_mutation": "0/0/0/0/0"
}
d["r3_18i"] = {
    "status": "active",
    "pass_type": "read-only evidence / second-property payload characterization",
    "frozen_terminators": 47,
    "frozen_continuations": 47,
    "observed_second_tags": {"Int": 46, "String": 1},
    "third_property_access": False,
    "production_mutation_allowed": False
}
write(p, json.dumps(d, indent=2, ensure_ascii=False) + "\n")

# 4) Current state
write("docs/continuity/MIMIR_CURRENT_STATE.md", f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18G — minimal native existing-actor bounded second-property header composition`
**Completed production differential:** `R3.18H — Outcome A / 94/94 frozen rows exact / 47 terminators + 47 continuations / Int=46 String=1 / mismatch 0`
**Current exact pass:** `R3.18I — second-property payload contract/evidence audit`

## 1. Truthful production boundary

R3.18G remains the production authority. After one already-valid R3.18B first K1 property it reuses R3.18D control and resolves at most one second property header. A false control returns `None` without lookup; a true control admits only the observed `Int | String` header contexts and stops exactly at the second `payload_start`. Production still does not consume the second payload and does not read a third property/control bit.

```text
production SHA/tree                 {PROD} / {PROD_TREE}
lib.rs blob                         5e2b9e5be9c6692e499abc97a89655c603728cef
R3.18G focused test blob            d56bf97d250b426e23fec4610cbb9ead6ec8a142
exact live-candidate validator      31957646865 / 95190626723 SUCCESS
published-main validator            31957892048 / 95191254798 SUCCESS
payload decoder calls / loops       0 / 0
```

## 2. R3.18H closure

R3.18H Outcome A is admitted as read-only evidence. It differentially exercised the **published R3.18G production API** over the frozen R3.18F 94-row lane.

```text
authority head/tree                 {EVIDENCE} / {EVIDENCE_TREE}
custom evidence run/job             31960174729 / 95196833572 SUCCESS
same-head normal CI                 31960174713 / 95196833409 SUCCESS
artifact                            9267045757 / 12070 bytes
artifact digest                     {ARTIFACT_DIGEST}
rows                                94/94 exact
class split                         47 terminator / 47 continuation
continuation tags                   Int=46 / String=1
real header truncation rows         32
terminator no-lookup rows           47
mismatch                            0
second payload / third property     0 / 0 bits consumed
production/Cargo/fixture/corpus/support mutation  0/0/0/0/0
```

Unresolved-stream, tag-outside-`Int|String`, repeatability and post-stop poison controls all passed. R3.18H did not widen production.

## 3. R3.18I exact next pass

R3.18I is read-only payload evidence. It reuses the exact frozen lane rather than selecting friendlier witnesses, because humans have already invented enough ways for benchmarks to accidentally become bedtime stories.

- keep all 47 terminators as no-second-payload/no-lookup controls;
- for all 47 continuations, start exactly at the already-proven second `payload_start`;
- characterize the 46 `Int` rows and the single `String` row separately;
- compare pinned Boxcars payload end and semantic value with already-admitted native lower-level decoders only where their existing contracts apply;
- stop exactly at that one payload end;
- do **not** read the next `property_present` bit;
- no production Rust/Cargo/fixture/corpus/support mutation.

Outcome A may open only a separate bounded production composition for one second payload. If the single String row is not covered exactly by the admitted K2 String contract, it must split into a narrower evidence/contract pass rather than being hand-waved into support.

## 4. Still closed

```text
production second-property payload composition
third property / third control bit / repeated property loop
generic repeatedly-chainable property cursor
second-header contexts outside exact Int/String
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction / events / replay slicing
skill / teacher / runtime / export widening
dependency or corpus/support expansion
```
''')

# 5) H decision
write("docs/continuity/MIMIR_R3_18H_DECISION.md", f'''# MIMIR R3.18H — Production Second-Property Header Differential Decision

**Date:** 2026-08-16
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE**
**Production authority:** `{PROD}`
**Production mutation:** none

## Decision

R3.18H is admitted. The published R3.18G bounded optional second-property-header composition matches the frozen R3.18F real-replay oracle lane exactly on all 94 rows. The pass remains evidence-only and does not admit second-payload production decoding, a third property or a repeated property loop.

## Exact authority

```text
canonical main at evidence start    {MAIN}
production SHA/tree                 {PROD} / {PROD_TREE}
production lib.rs blob              5e2b9e5be9c6692e499abc97a89655c603728cef
R3.18G focused test blob            d56bf97d250b426e23fec4610cbb9ead6ec8a142
R3.18H spec blob                    4b3eacad1698b22c421adda6af4a5142ced291e6
evidence head/tree                  {EVIDENCE} / {EVIDENCE_TREE}
authority run/job                   31960174729 / 95196833572 SUCCESS
same-head normal CI                 31960174713 / 95196833409 SUCCESS
artifact                            9267045757
artifact size                       12070 bytes
artifact digest                     {ARTIFACT_DIGEST}
```

## Frozen evidence result

```text
frozen replay identity              47/47
frozen witness rows                 94/94
native rows                         94/94
terminator rows                     47
continuation rows                   47
continuation Int                    46
continuation String                 1
terminator second_header=None       47
real header truncation rows         32
terminator no-lookup rows           47
unresolved-stream negative          PASS
tag outside Int/String negative     PASS
repeatability                       PASS
post-stop poison                    PASS
second payload bits consumed        0
third property bits consumed        0
native/oracle mismatch              0
production/Cargo/fixture/corpus/support mutation  0/0/0/0/0
```

Frozen R3.18F replay-identity SHA256 remains `b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf`; frozen witness SHA256 remains `99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7`, proving the lane was not silently reselected.

Artifact file SHA256 receipt:

```text
r3_18h_source_scope.txt             38ff92a2448883802b73ea4e2ee0a65f18b83beb782d8f8c87451e2295f37fb8
r3_18h_replay_identity.tsv          b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
r3_18h_frozen_witnesses.json        99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
r3_18h_oracle_regeneration.txt      97767f90f5f9d46afcb68f568cf28d021f2081ddbf62bb5f2536d8d7d1bf569e
r3_18h_comparison.json              de4ca9d70fb7f56aec1c279473c3289b236cfa48e3a17f1faec8942ac3548d10
r3_18h_negative_controls.txt        4d0273b85c5af2ae2e2b1fd7b88fd5d876c210d1a20f4cdd544601d649c053c9
r3_18h_aggregate.txt                4357bc88426ac50da065875f56bc2f806158080767292c6210623091f6fdc31b
```

## Hard stop

R3.18H admits no second-property payload production composition or semantic API, no third property/control bit, no generalized loop/cursor, no new tag context, no actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior and no dependency/support-lane widening.

## Next gate

R3.18I is a separate read-only second-property payload contract/evidence audit. It may characterize exactly one second payload on each of the 47 frozen continuation rows and must keep the 47 terminators as no-payload controls. It stops at the payload end and may not read a third `property_present` bit.
''')

# 6) I spec
write("docs/continuity/MIMIR_R3_18I_EXECUTION_SPEC.md", f'''# MIMIR R3.18I — Second-Property Payload Contract / Evidence Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / payload boundary and semantic characterization
**Production authority:** R3.18G `{PROD}`
**Prior differential authority:** R3.18H `{EVIDENCE}`
**Production mutation:** forbidden
**Third property / repeated loop:** forbidden

## 1. Goal

Characterize exactly one second-property payload after the already-proven R3.18G second header on the frozen real-replay lane. Establish exact payload end and semantic agreement separately for the observed `Int=46` and `String=1` continuation classes. Do not compose that payload into production yet.

## 2. Frozen authority

```text
canonical continuity base           {MAIN}
production SHA/tree                 {PROD} / {PROD_TREE}
production lib.rs blob              5e2b9e5be9c6692e499abc97a89655c603728cef
R3.18G focused test blob            d56bf97d250b426e23fec4610cbb9ead6ec8a142
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
R3.18F evidence head                27a855a9cfb82a0294dd1601e4da01c9fdfad264
R3.18F artifact                     9264673141 / sha256:e31e09abf322b6458f9034b06efe5502bb3b7f1011dfb08c9ffd6d1b1cd1b361
R3.18F replay identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
R3.18F frozen witnesses SHA256      99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
R3.18H evidence head/tree           {EVIDENCE} / {EVIDENCE_TREE}
R3.18H run/job                      31960174729 / 95196833572 SUCCESS
R3.18H same-head CI                 31960174713 / 95196833409 SUCCESS
R3.18H artifact                     9267045757 / {ARTIFACT_DIGEST}
```

Fresh-read all authorities before running. Any drift or witness reselection stops the pass.

## 3. Exact source lane

Reuse exactly the frozen 94 rows:

```text
47 terminators
47 continuations
continuation tags: Int=46 / String=1
```

Terminators remain negative controls. They have no admitted second payload and must not cause a lookup or payload read after the false control bit.

## 4. Continuation payload evidence

For every continuation row:

1. reconstruct and verify the already-admitted first property + R3.18G second header exactly;
2. begin payload work only at that second header's proven `payload_start_bit`;
3. obtain pinned-oracle second payload start/end/semantic value without consuming the next property-control bit;
4. invoke an existing native lower-level decoder only if the exact already-admitted tag/context contract applies;
5. compare native/oracle payload width, end bit and semantic value exactly under that decoder's existing comparison rules;
6. stop at the second payload end and record zero third-property bits consumed.

`Int` and `String` are separate evidence classes. The single String row cannot be generalized from the 46 Int rows. If its exact context falls outside the already-admitted K2 String production contract, record that fact and split the next pass instead of widening by analogy.

## 5. Required negative controls

At minimum:

- all 47 terminators: no second payload access;
- truncation at each required payload boundary: atomic reject;
- wrong tag/native decoder pairing: reject;
- wrong/unadmitted context: reject;
- post-payload poison: returned one-payload result unchanged;
- repeated identical invocation: byte-for-byte/field-for-field identical summary;
- third `property_present` bit poison or removal must not matter because R3.18I may not read it.

Real frozen rows should exercise truncation wherever possible. Synthetic controls may supplement but not replace real-lane checks.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact with:

- exact authority SHAs/trees/blobs/runs/artifacts;
- frozen replay/witness hashes;
- per-row class, payload start/end/width and privacy-safe semantic comparison result;
- separate Int and String aggregates;
- negative controls;
- zero third-property consumption counter;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA256 for every artifact file.

Do not emit private raw payload windows or replay-identifying user data beyond the already-approved replay identity scheme.

## 7. Validation

Require:

- exact 94-row frozen identity set;
- deterministic double-run equality;
- all applicable native/oracle payload comparisons exact;
- focused existing decoder tests PASS;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18I may not change production Rust/Cargo/lockfile/fixtures/corpus/support lanes. It may not publish a second-payload composition, read a third `property_present` bit/header/payload, create a repeated/generalized property loop, widen second-header tag contexts, iterate next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 continuation payloads are exactly characterized through payload end, applicable existing native decoders match pinned oracle semantics/end bits, the 46 Int and 1 String classes are both resolved under already-admitted contracts, negatives pass, third-property consumption is zero and mutation counters are zero. Admit evidence and open only a **separate bounded production second-property payload composition** pass.

### Outcome B

The Int class is exact but the String row is unresolved, outside the admitted K2 String context, or needs additional wire evidence. Admit only the supported evidence facts and open a narrower String payload evidence/contract pass. Production second-payload composition remains closed unless a separately scoped subset is explicitly admitted.

### Outcome C

Authority drift, witness reselection, native/oracle mismatch inside an already-admitted decoder contract, privacy failure, production mutation, or any third-property access. Stop without widening.
''')

# Final semantic guards
for path in ["MIMIR_CONTINUE_HERE.md", "MIMIR_KNOWLEDGE_GRAPH.md", "docs/continuity/MIMIR_CURRENT_STATE.md", "docs/continuity/MIMIR_R3_18H_DECISION.md", "docs/continuity/MIMIR_R3_18I_EXECUTION_SPEC.md"]:
    s = read(path)
    if "R3.18I" not in s:
        raise SystemExit(f"missing R3.18I in {path}")
if json.loads(read("docs/continuity/MIMIR_CONTINUITY_STATE.json"))["current_pass"] != "R3.18I":
    raise SystemExit("state current_pass mismatch")
print("R3_18H_CONTINUITY_GENERATION=PASS")
