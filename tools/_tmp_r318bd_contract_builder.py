#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(".")

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def sub_once(text, pattern, repl, label, flags=0):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"{label}: expected 1 replacement, got {n}")
    return out

CONTRACT_SHA = "33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27"

CONTRACT = {'schema_version': 1, 'contract': 'MIMIR_R3_18BD_POST_BA_MIXED_CONTINUATION_FOLLOWING_HEADER_CONTEXTS', 'status': 'admitted', 'admission_date': '2026-08-28', 'boundary': 'exactly one existing-actor following property header after a valid published R3.18BA true mixed control on the immutable R3.18BC continuation sublane; false controls terminate before header membership', 'membership_policy': 'exact_tuple_only', 'tuple_fields': ['stream_id_bound', 'prop_id_bits', 'property_object_index', 'attribute_tag', 'version_major', 'version_minor', 'net_version', 'is_rl_223'], 'frozen_lane_row_count': 40, 'false_terminator_count': 37, 'observed_header_row_count': 3, 'unique_exact_context_count': 3, 'authority': {'canonical_main_sha': '387e1693279dec062d3ef565cc5bc597de3a5a13', 'canonical_main_tree': 'a0dedfb8de603cc4e000a1777ed074eaed1c3163', 'canonical_main_ci_run': 33124420075, 'canonical_main_knowledge_archive_run': 33124420084, 'production_sha': '5d2bca711f528ab1bb607104379af503ff175697', 'production_tree': '6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a', 'r3_18bc_decision_blob': '7e864047299c6aacdaa7c990dffd1a2064ec7ff4', 'r3_18bd_execution_spec_blob': 'b9065f3e7bfa9e3a7d68386c4b49ccb25d2c529f', 'r3_18bc_evidence_head': '0f4d07f5caf77ec53f5e8b512867ad17b5835ca1', 'r3_18bc_evidence_tree': 'a198866dc3f18ffbd5cb16e32d39dada5f4116fc', 'r3_18bc_workflow_blob': 'e2c926f05379ff164bb5d3bfdd6f48347817a5af', 'r3_18bc_runner_blob': '546f3fd6e08d73834c2d405b5d7ec7cae57aaa08', 'r3_18bc_analyzer_blob': 'e2ebd01039af0d14f420ed2048beb158801cf658', 'r3_18bc_extender_blob': '06c84b5bfc4c4170e1d4268f72a62b09b09ff875', 'r3_18bc_run': 33122152803, 'r3_18bc_job': 98691409657, 'r3_18bc_same_head_ci_run': 33122152793, 'r3_18bc_same_head_ci_job': 98691409674, 'r3_18bc_artifact_id': 9666964713, 'r3_18bc_artifact_size': 7795, 'r3_18bc_artifact_sha256': '88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e', 'r3_18bc_manifest_sha256': 'd9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf', 'r3_18bc_header_rows_sha256': '131e8b3c964bb425d470a7036dcc8767f34783c002324bd644fff5749b086189', 'r3_18bc_header_summary_sha256': 'fa0cd7467b48bc5a63e95b0245cf41d40cea26b028322d25f6074426c546ec46', 'r3_18bc_candidate_partition_sha256': '12a6de4ea98e2710ce01a02f19834e52433bd25e6e915aea6f871c3d06428300', 'r3_18bc_frozen_targets_sha256': '4f7ae0b8c2a898478ac2f50342129f308e9e2c273f9ceb7a0531fe6656e3148c', 'r3_18bc_negative_controls_sha256': '5714746e1bddbbdf67cd8cec322392644dc366ca05fee98ea87ba420989affee', 'r3_18bc_validation_sha256': 'f7e09e08036d771c36716f5334ea47ec2c8b2cc9f242f57f9ff28bd3055265cf', 'r3_18bc_aggregate_sha256': '1a304054aff05137e21d2981df44d301e5c474da0374506b82cbd98ed5f57a95', 'pinned_boxcars_sha': 'c70e77df7af81b436cb545d070bb90c82f562d0b', 'witness_reselection': 0, 'native_oracle_mismatch': 0, 'following_payload_bits_consumed': 0, 'second_later_control_bits_consumed': 0}, 'observed_tag_counts': {'Boolean': 2, 'Float': 1}, 'observed_property_ordinal_counts': {'6': 3}, 'admitted_contexts': [{'stream_id_bound': 72, 'prop_id_bits': 6, 'property_object_index': 92, 'attribute_tag': 'Boolean', 'version_major': 868, 'version_minor': 32, 'net_version': 10, 'is_rl_223': False, 'observed_count': 1}, {'stream_id_bound': 72, 'prop_id_bits': 6, 'property_object_index': 94, 'attribute_tag': 'Boolean', 'version_major': 868, 'version_minor': 32, 'net_version': 10, 'is_rl_223': False, 'observed_count': 1}, {'stream_id_bound': 110, 'prop_id_bits': 6, 'property_object_index': 58, 'attribute_tag': 'Float', 'version_major': 868, 'version_minor': 32, 'net_version': 10, 'is_rl_223': False, 'observed_count': 1}], 'terminator_policy': {'false_rows_are_terminators': True, 'false_terminator_count': 37, 'false_terminators_produce_header_membership': False}, 'anti_widening': {'tag_only_membership': False, 'component_only_membership': False, 'cartesian_product_membership': False, 'versionless_membership': False, 'rl223_field_dropped_membership': False, 'rl223_false_to_true_membership': False, 'r3_18at_cross_boundary_inheritance': False, 'r3_18aj_cross_boundary_inheritance': False, 'r3_18z_cross_boundary_inheritance': False, 'r3_18p_cross_boundary_inheritance': False, 'false_terminator_header_synthesis': False, 'fabricated_fourth_tuple_admitted': False, 'multiplicity_is_runtime_frequency_promise': False, 'contexts_outside_exact_set_admitted': False}}

BD_DECISION = """# MIMIR R3.18BD — Exact Following-Header Context Contract Decision

**Date:** 2026-08-28
**Outcome:** **A — ADMITTED / BOUNDARY-SPECIFIC EXACT-EIGHT-FIELD CONTRACT**
**Production mutation:** none
**Canonical production:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Canonical continuity base:** `387e1693279dec062d3ef565cc5bc597de3a5a13` / `a0dedfb8de603cc4e000a1777ed074eaed1c3163`
**Contract:** `docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`

## Decision

R3.18BD closes Outcome A. The immutable R3.18BC three-row true-sublane header observation is frozen as exactly **three complete eight-field tuples**, each with evidence multiplicity one. The full mixed lane remains forty rows: **37 false R3.18BA controls are terminators outside header membership**, while only the exact three BC true rows contribute header contexts.

Membership is `exact_tuple_only`. Boolean-only, Float-only, ordinal-6-only, component-only, Cartesian, versionless, RL223-field-dropped, earlier-contract-inherited, or fabricated fourth-tuple membership is rejected. Multiplicity is evidence provenance, not a runtime-frequency promise.

## Exact authority

```text
canonical main before admission       387e1693279dec062d3ef565cc5bc597de3a5a13 / a0dedfb8de603cc4e000a1777ed074eaed1c3163
published-main CI / archive           33124420075 SUCCESS / 33124420084 SUCCESS
production SHA/tree                   5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BC decision / BD spec blobs           7e864047299c6aacdaa7c990dffd1a2064ec7ff4 / b9065f3e7bfa9e3a7d68386c4b49ccb25d2c529f
BC evidence head/tree                 0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
BC authority run/job                  33122152803 / 98691409657 SUCCESS
BC same-head CI                       33122152793 / 98691409674 SUCCESS
BC artifact                           9666964713 / 7795 bytes / sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
BC manifest SHA-256                   d9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf
BC header rows / summary SHA-256      131e8b3c964bb425d470a7036dcc8767f34783c002324bd644fff5749b086189 / fa0cd7467b48bc5a63e95b0245cf41d40cea26b028322d25f6074426c546ec46
BC partition / targets SHA-256        12a6de4ea98e2710ce01a02f19834e52433bd25e6e915aea6f871c3d06428300 / 4f7ae0b8c2a898478ac2f50342129f308e9e2c273f9ceb7a0531fe6656e3148c
BC negatives / validation SHA-256     5714746e1bddbbdf67cd8cec322392644dc366ca05fee98ea87ba420989affee / f7e09e08036d771c36716f5334ea47ec2c8b2cc9f242f57f9ff28bd3055265cf
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted contract

```text
membership policy                    exact_tuple_only
tuple fields                         stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223
frozen lane rows                     40
false terminators                    37 / outside header membership
observed header rows                 3
exact contexts                       3/3
observed multiplicity sum            3
observed tags                        Boolean=2 / Float=1
observed property ordinal            6 on 3/3
witness reselection                  0
native/oracle mismatch               0
following payload / second control   0/0
AT/AJ/Z/P inheritance                false/false/false/false
```

Exact admitted tuples:

```text
(72,  6, 92, Boolean, 868, 32, 10, false) x1
(72,  6, 94, Boolean, 868, 32, 10, false) x1
(110, 6, 58, Float,   868, 32, 10, false) x1
```

## Anti-widening validation

```text
exact tuple equality                 PASS 3/3
exact multiplicity equality          PASS 1/1/1 / sum 3
false terminators outside membership PASS 37/37
tag-only membership                  REJECT
component-only membership            REJECT
Cartesian candidate                  REJECT: (110,6,92,Boolean,868,32,10,false)
version-drop / version mutation      REJECT
RL223 field drop                     REJECT
RL223 false->true candidate          REJECT
fabricated fourth tuple              REJECT: (72,6,999,Boolean,868,32,10,false)
AT-valid BD-absent tuple             REJECT: (60,5,107,Int,868,32,10,false)
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

## Hard stop

R3.18BD admits a contract only. It does not publish a following-header production composition, decode the following payload, read a second later property-control bit, synthesize a header on any of the 37 false terminators, authorize a generalized/repeated property cursor, or widen actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior.

## Next gate

R3.18BE is a separate bounded production pass. It may validate/recompute one exact published R3.18BA mixed-control result. A false BA result must remain a successful no-header terminator. A true BA result may compose exactly one following existing-actor property header with the existing stateless primitive, must require exact R3.18BD eight-field membership, and must stop exactly at `payload_start`. No following payload or second later control is admitted.
"""

BE_SPEC = """# MIMIR R3.18BE — Bounded Post-BA Mixed-Continuation Following-Header Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Contract authority:** R3.18BD Outcome A / `docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`
**Following payload decode:** forbidden
**Second later property-control bit:** forbidden
**Generalized/repeated property loop:** forbidden

## 1. Goal

Publish the minimum boundary-specific composition after one valid published R3.18BA mixed control result.

- If the validated BA result is `property_present == false`, preserve it as a successful terminator and perform **no following-header lookup or wire consumption**.
- If the validated BA result is `property_present == true`, decode exactly one following existing-actor property header with the existing stateless header primitive, require exact R3.18BD eight-field tuple membership, expose that header identity, and stop exactly at `payload_start`.

No following payload or later control may be consumed.

## 2. Frozen authority

```text
canonical continuity parent           387e1693279dec062d3ef565cc5bc597de3a5a13 / a0dedfb8de603cc4e000a1777ed074eaed1c3163
production SHA/tree                   5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BC evidence head/tree                 0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
BC authority run/job                  33122152803/98691409657 SUCCESS
BC artifact                           9666964713 / sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
BD exact contract                     sha256:33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27
BD membership                         exact_tuple_only / 3 eight-field tuples / multiplicity 3
frozen mixed lane                     40 rows / false=37 / true=3
observed true-header tags             Boolean=2 / Float=1
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

R3.18BD, not resemblance to R3.18AT/AJ/Z/P, is the sole following-header context authority at this boundary.

## 3. Production contract

The new boundary-specific API must:

1. validate/recompute the supplied published R3.18BA prior instead of trusting arbitrary caller coordinates;
2. require exact equality of BA control start/end/stop with the recomputed prior;
3. branch on the validated BA boolean without re-reading that control;
4. on `false`, return a terminator/no-header result and perform zero stream/header/payload/later-control reads;
5. on `true`, invoke the existing stateless existing-actor header primitive exactly once at the validated BA stop;
6. retain all eight R3.18BD context fields, including `is_rl_223`;
7. require exact membership in the R3.18BD contract, with no tag/component/Cartesian/versionless/RL223-dropped membership;
8. require returned header `property_present == true` and exact alignment to the BA control boundary;
9. expose exact stream/header/property/tag/context coordinates and set final stop exactly to `payload_start`;
10. consume zero following-payload bits and zero second-later-control bits.

The API must not expose a repeatedly-chainable cursor or generic property loop.

## 4. Required focused tests

At minimum:

- exact immutable 40-row mixed lane: 37 false terminators + 3 true headers;
- false path succeeds 37/37 without header lookup and without any post-BA bit consumption;
- true path succeeds 3/3 and exact BD membership is 3/3;
- all 3 exact contexts exercised with multiplicity one each;
- observed tags remain Boolean=2 / Float=1;
- deterministic repeatability;
- truncation inside a true-row following header rejects atomically;
- wrong actor object rejects;
- unresolved stream/property lookup rejects;
- wrong exact version/context rejects;
- `is_rl_223` false->true mutation rejects;
- tag-only/component-only/Cartesian/versionless candidate rejects;
- AT-valid but BD-absent `(60,5,107,Int,868,32,10,false)` rejects;
- fabricated fourth tuple rejects;
- post-`payload_start` poison leaves the true-path header result unchanged;
- following payload and second later control consumption remain `0/0`;
- source-scope guard proves at most one header primitive call, zero payload decoders and no generalized/repeated property loop.

Synthetic tests supplement but do not widen the immutable BC/BD authority.

## 5. Clean candidate

The clean production commit must contain only the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18BE integration test file. No workflow/helper, evidence artifact, Cargo/dependency, fixture/corpus, continuity, raw-state/event/skill/runtime/export or unrelated cleanup may enter the production commit.

## 6. Validation and publication

Require:

- Rust 1.85 formatting;
- focused BE tests;
- directly affected BA/AY/header prerequisite regressions;
- workspace check;
- workspace test;
- clippy with warnings denied;
- repository verifier;
- exact clean-candidate normal CI;
- fresh-main ancestry verification;
- force-free publication;
- exact published-main SHA/tree readback;
- published-main validation on the exact published SHA.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse the existing run ID when equivalent. Rerun is never polling.

## 7. Hard stop

No following payload after the one admitted header, no second later property-control bit, no context outside the exact R3.18BD contract, no following-header synthesis for a false terminator, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A

The exact 37 false terminators remain no-header successes; the exact 3 true rows compose one header matching the R3.18BD contract; all focused/negative/full validations pass; payload/second-control consumption stays `0/0`. Publish only this bounded mixed-continuation composition. Then open a separate R3.18BF published-production differential pass.

### Outcome B

Only a strict safe subset or narrower result representation can be implemented without violating R3.18BD. Publish only that exact subset/representation and rewrite the next differential accordingly.

### Outcome C

Authority drift, false-terminator header access, context/RL223 widening, payload/later-control access, generic chaining, production-scope drift or validation contradiction. Stop without publication.
"""

p="MIMIR_CONTINUE_HERE.md"
t=read(p)
t=sub_once(t, r"(LAST_COMPLETED_CONTRACT_PASS:\n)  [^\n]+\n", r"\1  R3.18BD — post-BA mixed-continuation following-header exact-context contract / Outcome A / 3 exact eight-field tuples / multiplicity 3 / 37 false terminators outside membership / contract 33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27 / AT-AJ-Z-P inheritance false / RL223 retained\n", "handbook contract")
t=sub_once(t, r"(CURRENT_PASS:\n)  [^\n]+\n", r"\1  R3.18BE — bounded post-BA mixed-continuation following-header production\n", "handbook current pass")
t=sub_once(t, r"(CURRENT_PASS_TYPE:\n)  [^\n]+\n", r"\1  bounded production implementation / validate one exact published BA mixed control; false terminates with no header, true composes exactly one BD-admitted header and stops at payload_start\n", "handbook current type")
write(p,t)

p="MIMIR_KNOWLEDGE_GRAPH.md"
t=read(p)
t=sub_once(t, r"R3\.18BD exact following-header context contract / ACTIVE\n", "R3.18BD exact following-header context contract / Outcome A CLOSED\nR3.18BE bounded post-BA mixed-continuation following-header production / ACTIVE\n", "KG BD/BE graph")
old_tail="""143. `docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md`
144. `docs/continuity/MIMIR_R3_18BA_DECISION.md`
145. `docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md`
146. `docs/continuity/MIMIR_R3_18BB_DECISION.md`
147. `docs/continuity/MIMIR_R3_18BC_EXECUTION_SPEC.md`
148. `docs/continuity/MIMIR_R3_18BC_DECISION.md`
149. `docs/continuity/MIMIR_R3_18BD_EXECUTION_SPEC.md`
150. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
151. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
152. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
153. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
154. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
155. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
156. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
new_tail="""143. `docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md`
144. `docs/continuity/MIMIR_R3_18BA_DECISION.md`
145. `docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md`
146. `docs/continuity/MIMIR_R3_18BB_DECISION.md`
147. `docs/continuity/MIMIR_R3_18BC_EXECUTION_SPEC.md`
148. `docs/continuity/MIMIR_R3_18BC_DECISION.md`
149. `docs/continuity/MIMIR_R3_18BD_EXECUTION_SPEC.md`
150. `docs/continuity/MIMIR_R3_18BD_DECISION.md`
151. `docs/continuity/MIMIR_R3_18BE_EXECUTION_SPEC.md`
152. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
153. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
154. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
155. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
156. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
157. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
158. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
if t.count(old_tail)!=1:
    raise SystemExit("KG mandatory tail mismatch")
t=t.replace(old_tail,new_tail)
if "### R3.18BD exact following-header context contract: OUTCOME A / CLOSED" not in t:
    t += f"""

### R3.18BD exact following-header context contract: OUTCOME A / CLOSED
- contract `docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json` / sha256 `33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`
- exact_tuple_only / 3 complete eight-field contexts / multiplicity 3 / Boolean=2 Float=1
- full lane 40 rows; 37 false terminators outside header membership; exact true headers 3
- BC authority `0f4d07f5caf77ec53f5e8b512867ad17b5835ca1` / `33122152803/98691409657` SUCCESS / artifact `9666964713`
- anti-widening: tag/component/Cartesian/versionless/RL223-drop/AT-AJ-Z-P inheritance/fabricated-fourth all rejected
- production unchanged at R3.18BA; payload/second-control remain 0/0

### R3.18BE bounded post-BA mixed-continuation following-header production: ACTIVE
- validate/recompute one exact published BA mixed control
- false path: successful terminator, zero following-header access
- true path: exactly one stateless header primitive call, exact R3.18BD membership, stop at `payload_start`
- no following payload, second later control, generalized property cursor, or semantic/runtime widening
"""
write(p,t)

p="docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
t=read(p)
override=f"""# 0. Current override — R3.18BD contract closed / R3.18BE bounded production active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BA
- `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a` remains canonical production.
- one exact R3.18AY payload authority is recomputed and validated;
- exactly one following LSB-first `property_present` bit is consumed at AY stop;
- frozen split false=37 / true=3 remains authoritative;
- the boundary stops exactly one bit later.

## CLOSED EVIDENCE — R3.18BC Outcome A
- evidence `0f4d07f5caf77ec53f5e8b512867ad17b5835ca1` / `33122152803/98691409657` SUCCESS;
- same-head CI `33122152793/98691409674` SUCCESS;
- artifact `9666964713` / `sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e`;
- 37 false terminators / 3 true one-header observations; native/oracle mismatch 0;
- exact contexts 3; Boolean=2 / Float=1; payload/second-control 0/0.

## CLOSED CONTRACT — R3.18BD Outcome A
- contract sha256 `33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`;
- membership policy `exact_tuple_only`;
- exactly 3 complete eight-field tuples, multiplicity 1 each / sum 3;
- all 37 false terminators remain outside header membership;
- no AT/AJ/Z/P inheritance, no component/Cartesian/versionless/RL223-dropped widening.

## ACTIVE BOUNDED PRODUCTION — R3.18BE
- validate/recompute one exact published BA mixed-control prior;
- false BA result is a successful no-header terminator with zero following-header access;
- true BA result may invoke exactly one existing stateless header primitive;
- true header must match exact R3.18BD membership;
- final stop is exactly `payload_start`.

## CLOSED
- any following-header synthesis on the 37 BA false terminators;
- any header context outside exact R3.18BD membership;
- following payload after the one R3.18BE header;
- second later property-control bit;
- repeated/generalized property loop or generic cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

"""
t=sub_once(t, r"# 0\. Current override.*?(?=# 1\. Status vocabulary)", override, "boundary override", flags=re.S)
write(p,t)

p="docs/continuity/MIMIR_CONTINUITY_STATE.json"
state=json.loads(read(p))
state["updated_date"]="2026-08-28"
state["last_completed_contract_pass"]="R3.18BD"
state["current_pass"]="R3.18BE"
state["current_pass_kind"]="bounded production composition of exactly one R3.18BD-admitted following header after a validated published R3.18BA mixed control"
state["current_pass_goal"]="Validate/recompute the exact published BA mixed control; preserve 37 false rows as no-header terminators and compose exactly one BD-admitted header on only the 3 true rows, stopping at payload_start."
state["current_pass_stop_boundary"]="No following payload, no second later control, no header on a false terminator, no context outside exact R3.18BD membership, and no generalized cursor."
state["r3_18bd"]={
    "outcome":"A",
    "canonical_base_sha":"387e1693279dec062d3ef565cc5bc597de3a5a13",
    "canonical_base_tree":"a0dedfb8de603cc4e000a1777ed074eaed1c3163",
    "production_sha_unchanged":"5d2bca711f528ab1bb607104379af503ff175697",
    "contract_path":"docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json",
    "contract_sha256":CONTRACT_SHA,
    "membership_policy":"exact_tuple_only",
    "frozen_rows":40,
    "false_terminators":37,
    "observed_header_rows":3,
    "exact_contexts":3,
    "observed_multiplicity_sum":3,
    "observed_tags":{"Boolean":2,"Float":1},
    "witness_reselection":0,
    "native_oracle_mismatch":0,
    "following_payload_bits_consumed":0,
    "second_later_control_bits_consumed":0,
    "earlier_contract_inheritance":False
}
arr=state.get("next_files_to_read",[])
bd_exec="docs/continuity/MIMIR_R3_18BD_EXECUTION_SPEC.md"
bd_dec="docs/continuity/MIMIR_R3_18BD_DECISION.md"
be_exec="docs/continuity/MIMIR_R3_18BE_EXECUTION_SPEC.md"
for x in (bd_dec,be_exec):
    while x in arr:
        arr.remove(x)
if bd_exec in arr:
    idx=arr.index(bd_exec)+1
    arr[idx:idx]=[bd_dec,be_exec]
else:
    arr.extend([bd_exec,bd_dec,be_exec])
state["next_files_to_read"]=arr
closed=state.get("closed_now",[])
for item in [
    "following-header contexts outside exact R3.18BD evidence-supported eight-field membership",
    "R3.18AT/R3.18AJ/R3.18Z/R3.18P cross-boundary header-context inheritance at R3.18BD",
    "dropping or flipping is_rl_223 in R3.18BD membership",
    "following-header success on any of the 37 R3.18BA false terminator rows",
    "following payload after the future R3.18BE one-header boundary",
    "second later property-control bit after R3.18BE",
    "generalized/repeated property loop or generic cursor after R3.18BE",
]:
    if item not in closed:
        closed.append(item)
state["closed_now"]=closed
write(p,json.dumps(state,indent=2,ensure_ascii=False)+"\n")

write("docs/continuity/MIMIR_CURRENT_STATE.md", f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-28
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `5d2bca711f528ab1bb607104379af503ff175697`
**Production tree:** `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last evidence:** `R3.18BC — Outcome A / 37 false terminators + 3 exact following headers / contexts=3 / artifact 9666964713`
**Last contract:** `R3.18BD — Outcome A / exact_tuple_only / 3 eight-field tuples / contract 33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`
**Current exact pass:** `R3.18BE — bounded post-BA mixed-continuation following-header production`

## Truthful boundary

R3.18BA remains production. R3.18BC proved the immutable forty-row split exactly: 37 false terminators and three true rows, each with one native header matching pinned Boxcars through `payload_start`. R3.18BD freezes only the three observed complete eight-field contexts:

```text
(72,  6, 92, Boolean, 868, 32, 10, false) x1
(72,  6, 94, Boolean, 868, 32, 10, false) x1
(110, 6, 58, Float,   868, 32, 10, false) x1
```

The contract is `exact_tuple_only`; the 37 false rows contribute no header membership. AT/AJ/Z/P contracts are history/methodology only and are not inherited.

## Current gate

R3.18BE may validate/recompute one published BA mixed control. False must return a successful no-header terminator with zero following-header reads. True may compose exactly one existing-actor header with the stateless primitive, require exact R3.18BD membership, and stop at `payload_start`.

## Hard stop

No following payload, second later control, false-row header synthesis, context outside exact BD membership, generalized cursor, or actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
""")

write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", f"""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BA** at `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`.

R3.18BC is **Outcome A / CLOSED**: evidence `0f4d07f5caf77ec53f5e8b512867ad17b5835ca1`, run/job `33122152803/98691409657` SUCCESS, same-head CI `33122152793/98691409674` SUCCESS, artifact `9666964713` / 7795 / `sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e`. The forty-row lane is false=37 / true=3; the three true rows each have one exact following header; unique contexts=3; payload/second-control 0/0.

R3.18BD is **Outcome A / CLOSED**. Contract `docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json` has SHA-256 `33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27` and admits exactly three complete eight-field tuples with multiplicity one each. All 37 false terminators remain outside header membership. Tag/component/Cartesian/versionless/RL223-dropped and AT/AJ/Z/P inherited membership are rejected.

The active pass is **R3.18BE — bounded post-BA mixed-continuation following-header production**. Validate/recompute published BA. False terminates with no header access. True may compose exactly one stateless header under exact BD membership and must stop at `payload_start`. No following payload or second control.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
""")

p="docs/continuity/MIMIR_PROGRESS_LEDGER.md"
t=read(p)
entry=f"""
## 2026-08-28 — R3.18BD — Exact following-header context contract after R3.18BC

Production base SHA: `5d2bca711f528ab1bb607104379af503ff175697`
Production commit SHA: unchanged / `5d2bca711f528ab1bb607104379af503ff175697`
Pass type: contract-only admission
Outcome: **A — CLOSED**

What changed:
- no production source changed;
- the exact three R3.18BC complete eight-field header contexts were frozen under `exact_tuple_only`;
- all 37 false R3.18BA terminators remain outside header membership;
- R3.18BE is opened as a separate bounded production pass.

Authority:
- canonical base `387e1693279dec062d3ef565cc5bc597de3a5a13` / `a0dedfb8de603cc4e000a1777ed074eaed1c3163`;
- published-base CI `33124420075` SUCCESS and Knowledge Archive `33124420084` SUCCESS;
- BC evidence `0f4d07f5caf77ec53f5e8b512867ad17b5835ca1` / `33122152803/98691409657` SUCCESS;
- BC same-head CI `33122152793/98691409674` SUCCESS;
- artifact `9666964713` / 7795 / `sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e`;
- contract sha256 `33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`.

Admitted membership:
- `(72,6,92,Boolean,868,32,10,false)` x1;
- `(72,6,94,Boolean,868,32,10,false)` x1;
- `(110,6,58,Float,868,32,10,false)` x1;
- multiplicity sum 3; false terminators 37 outside membership.

Anti-widening:
- tag-only REJECT;
- component-only REJECT;
- Cartesian REJECT;
- versionless/version-drop REJECT;
- RL223 drop/false->true REJECT;
- fabricated fourth tuple REJECT;
- AT/AJ/Z/P cross-boundary inheritance REJECT;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.

Boundaries still closed:
- following payload;
- second later property control;
- header synthesis on any false terminator;
- generalized/repeated property cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

Next exact pass:
- `R3.18BE — bounded post-BA mixed-continuation following-header production`.

---
"""
if "## 2026-08-28 — R3.18BD — Exact following-header context contract after R3.18BC" not in t:
    if not t.endswith("\n"):
        t+="\n"
    t+=entry
write(p,t)

write("docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json", json.dumps(CONTRACT,indent=2,ensure_ascii=False)+"\n")
write("docs/continuity/MIMIR_R3_18BD_DECISION.md", BD_DECISION)
write("docs/continuity/MIMIR_R3_18BE_EXECUTION_SPEC.md", BE_SPEC)
print("R3_18BD_CONTRACT_PATCH=PASS")
