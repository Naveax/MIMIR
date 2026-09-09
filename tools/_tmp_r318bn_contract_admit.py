from __future__ import annotations

from pathlib import Path
from collections import OrderedDict
import hashlib
import json
import re

ROOT = Path('.')
DATE = '2026-09-09'
BASE_SHA = '0e36965d2f469f8d2411535b359ac22f9e480fd6'
BASE_TREE = 'fc87430df448aff995a4a59c6c87b2cb196da52e'
PROD_SHA = 'f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf'
PROD_TREE = '07656c7a43c1afb97903ef33c1109b764fbf8b7d'
CONTRACT_SHA = '904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c'
CANDIDATE_SHA = 'c2c25c6b3e6a1c68636b60c444baa608238b2b95'
CANDIDATE_TREE = '50668fe5745bcc349a5e92bb9508992bd74f5f1a'
VALID_RUN = 34340205828
VALID_JOB = 102428959672
KA_RUN = 34340205835
KA_JOB = 102428960213
BASE_CI_RUN = 34339899692
BASE_CI_JOB = 102427972308
BM_HEAD = '689b1a24b57a84c81dc19c9a308fb1423f191c4b'
BM_TREE = '1d4e95409e1125b01a78aae6a436190b3c1381f4'
BM_RUN = 34334615939
BM_JOB = 102410984005
BM_CI_RUN = 34334615886
BM_CI_JOB = 102411487443
BM_ARTIFACT = 10097405795
BM_ARTIFACT_SIZE = 8340
BM_ARTIFACT_SHA = 'bd51a612be2cdd87d9ce1eb141f3f77f47ae29d42aabc8fc16c260a175f27963'
BM_MANIFEST_SHA = '167021cca2259c4d2ef16e9da50503007f381349219adb0f5684849f69f2cbd2'
BM_ROWS_SHA = '2210a7c5e5d74f7ab95e0ace692462979bc4ac5934073b886a29c56085524ae0'
BM_SUMMARY_SHA = '9b021ea415e76e06b8b38033c3d37a8ca11a8ca938ec5dfd4c9fd9096c690434'
BM_NEG_SHA = '0ebf4aa8ac72934f7c42af35560ce29db7f8fa32b772204f0a47a4e2526ee4d0'
BM_VALID_SHA = 'a21b33d5b5b0566b1f4f071178fcd40787ba6f8891b08627202f8ac556235bc9'
BM_CI_RECEIPT_SHA = '255a763ff6aa0ec566654c1f1fd9be95a1111669b1fbbebb53763771734a87ec'
BM_UPSTREAM_SHA = 'd98dc9d6002add804e6837ee9eeedc390682c665c531b52ca0a3f3bbcef43e1d'
BOXCARS = 'c70e77df7af81b436cb545d070bb90c82f562d0b'
BM_DECISION_BLOB = 'ff232e1ca0316bbae943ef1e3e40d2564d3226e0'
BN_SPEC_BLOB = '8afd2c1fe0a597767c58396449b24aa8c00beb5a'
CANDIDATE_CONTRACT_SHA = 'b60329891d7bddd34901bb8a9a423954a930173d597c0a9296d04d6b8a9b1e03'


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')


def replace_field(text: str, key: str, value: str) -> str:
    pattern = rf'(?m)^({re.escape(key)}:\n)  .*?$'
    out, n = re.subn(pattern, rf'\g<1>  {value}', text, count=1)
    if n != 1:
        raise SystemExit(f'expected one {key} field, got {n}')
    return out


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f'{label}: expected one anchor, got {text.count(old)}')
    return text.replace(old, new, 1)


fields = [
    'stream_id_bound', 'prop_id_bits', 'property_object_index', 'attribute_tag',
    'version_major', 'version_minor', 'net_version', 'is_rl_223'
]
contexts = [
    OrderedDict([
        ('stream_id_bound', 72), ('prop_id_bits', 6), ('property_object_index', 95),
        ('attribute_tag', 'Boolean'), ('version_major', 868), ('version_minor', 32),
        ('net_version', 10), ('is_rl_223', False), ('observed_count', 1),
    ]),
    OrderedDict([
        ('stream_id_bound', 110), ('prop_id_bits', 6), ('property_object_index', 66),
        ('attribute_tag', 'ActiveActor'), ('version_major', 868), ('version_minor', 32),
        ('net_version', 10), ('is_rl_223', False), ('observed_count', 1),
    ]),
]

authority = OrderedDict([
    ('canonical_main_sha', BASE_SHA),
    ('canonical_main_tree', BASE_TREE),
    ('canonical_main_ci_run', BASE_CI_RUN),
    ('canonical_main_ci_job', BASE_CI_JOB),
    ('r3_18bn_candidate_head', CANDIDATE_SHA),
    ('r3_18bn_candidate_tree', CANDIDATE_TREE),
    ('r3_18bn_candidate_contract_sha256', CANDIDATE_CONTRACT_SHA),
    ('r3_18bn_validation_run', VALID_RUN),
    ('r3_18bn_validation_job', VALID_JOB),
    ('r3_18bn_knowledge_archive_run', KA_RUN),
    ('r3_18bn_knowledge_archive_job', KA_JOB),
    ('production_sha', PROD_SHA),
    ('production_tree', PROD_TREE),
    ('r3_18bm_decision_blob', BM_DECISION_BLOB),
    ('r3_18bn_execution_spec_blob', BN_SPEC_BLOB),
    ('r3_18bm_evidence_head', BM_HEAD),
    ('r3_18bm_evidence_tree', BM_TREE),
    ('r3_18bm_run', BM_RUN),
    ('r3_18bm_job', BM_JOB),
    ('r3_18bm_same_head_ci_run', BM_CI_RUN),
    ('r3_18bm_same_head_ci_job', BM_CI_JOB),
    ('r3_18bm_artifact_id', BM_ARTIFACT),
    ('r3_18bm_artifact_size', BM_ARTIFACT_SIZE),
    ('r3_18bm_artifact_sha256', BM_ARTIFACT_SHA),
    ('r3_18bm_manifest_sha256', BM_MANIFEST_SHA),
    ('r3_18bm_header_rows_sha256', BM_ROWS_SHA),
    ('r3_18bm_header_summary_sha256', BM_SUMMARY_SHA),
    ('r3_18bm_negative_controls_sha256', BM_NEG_SHA),
    ('r3_18bm_validation_sha256', BM_VALID_SHA),
    ('r3_18bm_same_head_ci_receipt_sha256', BM_CI_RECEIPT_SHA),
    ('r3_18bm_upstream_receipts_sha256', BM_UPSTREAM_SHA),
    ('pinned_boxcars_sha', BOXCARS),
    ('witness_reselection', 0),
    ('native_oracle_mismatch', 0),
    ('unclassified_rows', 0),
    ('following_payload_bits_consumed', 0),
    ('second_later_control_bits_consumed', 0),
])

contract = OrderedDict([
    ('schema_version', 1),
    ('contract', 'MIMIR_R3_18BN_POST_BK_MIXED_CONTINUATION_FOLLOWING_HEADER_CONTEXTS'),
    ('status', 'admitted'),
    ('admission_date', DATE),
    ('boundary', 'exactly one existing-actor following property header after a valid published R3.18BK true mixed control on the immutable R3.18BM continuation sublane; the BK false control terminates before header membership'),
    ('membership_policy', 'exact_tuple_only'),
    ('tuple_fields', fields),
    ('frozen_lane_row_count', 3),
    ('false_terminator_count', 1),
    ('observed_header_row_count', 2),
    ('unique_exact_context_count', 2),
    ('authority', authority),
    ('observed_tag_counts', OrderedDict([('Boolean', 1), ('ActiveActor', 1)])),
    ('observed_property_ordinal_counts', OrderedDict([('7', 2)])),
    ('admitted_contexts', contexts),
    ('terminator_policy', OrderedDict([
        ('false_rows_are_terminators', True),
        ('false_terminator_count', 1),
        ('false_terminators_produce_header_membership', False),
    ])),
    ('anti_widening', OrderedDict([
        ('tag_only_membership', False),
        ('component_only_membership', False),
        ('property_ordinal_only_membership', False),
        ('cartesian_product_membership', False),
        ('versionless_membership', False),
        ('rl223_field_dropped_membership', False),
        ('rl223_false_to_true_membership', False),
        ('r3_18bd_cross_boundary_inheritance', False),
        ('r3_18at_cross_boundary_inheritance', False),
        ('r3_18aj_cross_boundary_inheritance', False),
        ('r3_18z_cross_boundary_inheritance', False),
        ('r3_18p_cross_boundary_inheritance', False),
        ('false_terminator_header_synthesis', False),
        ('fabricated_third_tuple_admitted', False),
        ('multiplicity_is_runtime_frequency_promise', False),
        ('contexts_outside_exact_set_admitted', False),
    ])),
])
contract_text = json.dumps(contract, indent=2, ensure_ascii=False) + '\n'
actual_contract_sha = hashlib.sha256(contract_text.encode()).hexdigest()
if actual_contract_sha != CONTRACT_SHA:
    raise SystemExit(f'contract hash mismatch {actual_contract_sha} != {CONTRACT_SHA}')
write('docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json', contract_text)


decision = f'''# MIMIR R3.18BN — Exact Following-Header Context Contract Decision

**Date:** {DATE}
**Outcome:** **A — ADMITTED / BOUNDARY-SPECIFIC EXACT-EIGHT-FIELD CONTRACT**
**Production changed:** **NO**
**Canonical production:** R3.18BK `{PROD_SHA}` / `{PROD_TREE}`
**Contract:** `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `{CONTRACT_SHA}`

## Decision

R3.18BN closes Outcome A. Exactly the two complete eight-field contexts proven by R3.18BM are admitted with exact tuple equality and multiplicity one each. The sole BK-false row remains a terminator outside header membership.

No tag-only, component-only, property-ordinal-only, Cartesian, versionless, RL223-dropped/flipped, R3.18BD/AT/AJ/Z/P inherited, or fabricated third-tuple membership is admitted. Multiplicity is evidence provenance, not a runtime-frequency promise.

## Frozen contract

```text
membership policy                     exact_tuple_only
frozen lane rows                      3
false terminators                     1
observed header rows                  2
unique exact contexts                 2
multiplicity                          1 + 1 = 2
property ordinal                      7 on 2/2
production/Cargo/fixture/corpus/support 0/0/0/0/0
```

Exact admitted contexts:

```text
(72,  6, 95, Boolean,     868, 32, 10, false) x1
(110, 6, 66, ActiveActor, 868, 32, 10, false) x1
```

## Validation receipts

```text
canonical contract base               {BASE_SHA} / {BASE_TREE}
base exact-SHA CI                     {BASE_CI_RUN}/{BASE_CI_JOB} SUCCESS
candidate head/tree                   {CANDIDATE_SHA} / {CANDIDATE_TREE}
candidate contract sha256             {CANDIDATE_CONTRACT_SHA}
exact contract validation             {VALID_RUN}/{VALID_JOB} SUCCESS
knowledge archive                     {KA_RUN}/{KA_JOB} SUCCESS
BM evidence                           {BM_HEAD} / {BM_RUN}/{BM_JOB} SUCCESS
BM same-head CI                       {BM_CI_RUN}/{BM_CI_JOB} SUCCESS
BM artifact                           {BM_ARTIFACT} / sha256:{BM_ARTIFACT_SHA}
final admitted contract sha256        {CONTRACT_SHA}
```

Required negatives passed for Cartesian recombination, version mutation/drop, RL223 false→true, fabricated third tuple, tag/component-only widening, and an R3.18BD-valid but BN-absent tuple `(72,6,92,Boolean,868,32,10,false)`.

## Sequencing consequence

The next pass is **R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production**.

R3.18BO may validate/recompute one exact published BK result. A false BK result must return a successful no-header terminator with zero post-BK reads. A true result may decode exactly one following existing-actor header using the stateless primitive, require exact R3.18BN membership, and stop exactly at `payload_start`.

## Hard stop

No following payload, no second later property-control bit, no header synthesis on the false terminator, no context outside exact R3.18BN membership, no repeated/generalized property loop/cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
'''
write('docs/continuity/MIMIR_R3_18BN_DECISION.md', decision)


bo_spec = f'''# MIMIR R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** R3.18BK `{PROD_SHA}` / `{PROD_TREE}`
**Contract authority:** R3.18BN Outcome A / `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `{CONTRACT_SHA}`
**Following payload decode:** forbidden
**Second later property-control bit:** forbidden
**Generalized/repeated property loop:** forbidden

## 1. Goal

Publish the minimum boundary-specific composition after one valid published R3.18BK mixed-control result.

- If the validated BK result is `property_present == false`, preserve it as a successful terminator and perform **no following-header lookup or wire consumption**.
- If the validated BK result is `property_present == true`, decode exactly one following existing-actor property header with the existing stateless header primitive, require exact R3.18BN eight-field tuple membership, expose that header identity, and stop exactly at `payload_start`.

No following payload or later control may be consumed.

## 2. Frozen authority

```text
canonical continuity parent           {BASE_SHA} / {BASE_TREE}
production SHA/tree                   {PROD_SHA} / {PROD_TREE}
BM evidence head/tree                 {BM_HEAD} / {BM_TREE}
BM evidence run/job                   {BM_RUN}/{BM_JOB} SUCCESS
BM artifact                           {BM_ARTIFACT} / sha256:{BM_ARTIFACT_SHA}
BN exact contract                     sha256:{CONTRACT_SHA}
BN membership                         exact_tuple_only / 2 eight-field tuples / multiplicity 2
frozen mixed lane                     3 rows / false=1 / true=2
observed true-header tags             Boolean=1 / ActiveActor=1
property ordinal                      7 on 2/2
pinned Boxcars                        {BOXCARS}
```

R3.18BN, not resemblance to older contracts, is the sole following-header context authority at this boundary.

## 3. Production contract

The new boundary-specific API must:

1. validate/recompute the supplied published R3.18BK prior instead of trusting arbitrary caller coordinates;
2. require exact equality of BK control start/end/stop with the recomputed prior;
3. branch on the validated BK boolean without re-reading that control;
4. on `false`, return a terminator/no-header result and perform zero stream/header/payload/later-control reads;
5. on `true`, invoke the existing stateless existing-actor header primitive exactly once at the validated BK stop;
6. retain all eight R3.18BN context fields, including `is_rl_223`;
7. require exact membership in the R3.18BN contract, with no tag/component/Cartesian/versionless/RL223-dropped membership;
8. require returned header `property_present == true` and exact alignment to the BK control boundary;
9. expose exact stream/header/property/tag/context coordinates and set final stop exactly to `payload_start`;
10. consume zero following-payload bits and zero second-later-control bits.

The API must not expose a repeatedly-chainable cursor or generic property loop.

## 4. Required focused tests

At minimum:

- exact immutable three-row mixed lane: 1 false terminator + 2 true headers;
- false path succeeds 1/1 without header lookup and without any post-BK bit consumption;
- true path succeeds 2/2 and exact BN membership is 2/2;
- both exact contexts exercised with multiplicity one each;
- observed tags remain Boolean=1 / ActiveActor=1; property ordinal remains 7 on 2/2;
- deterministic repeatability;
- truncation inside a true-row following header rejects atomically;
- wrong actor object rejects;
- unresolved stream/property lookup rejects;
- wrong exact version/context rejects;
- `is_rl_223` false→true mutation rejects;
- tag-only/component-only/Cartesian/versionless candidate rejects;
- BD-valid but BN-absent `(72,6,92,Boolean,868,32,10,false)` rejects;
- fabricated third tuple rejects;
- post-`payload_start` poison leaves the true-path header result unchanged;
- following payload and second later control consumption remain `0/0`;
- source-scope guard proves at most one header primitive call, zero payload decoders and no generalized/repeated property loop.

Synthetic tests supplement but do not widen immutable BM/BN authority.

## 5. Clean candidate

The clean production commit must contain only the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18BO integration test file. No workflow/helper, evidence artifact, Cargo/dependency, fixture/corpus, continuity, raw-state/event/skill/runtime/export or unrelated cleanup may enter the production commit.

## 6. Validation and publication

Require Rust 1.85 formatting, focused BO tests, directly affected BK/BI/header prerequisite regressions, workspace check/test, clippy with warnings denied, repository verifier, exact clean-candidate normal CI, fresh-main ancestry verification, force-free publication, exact published-main SHA/tree readback, and published-main validation on the exact published SHA.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs. Reuse the existing run ID when equivalent. Rerun is never polling.

## 7. Hard stop

No following payload after the one admitted header, no second later property-control bit, no context outside exact R3.18BN membership, no following-header synthesis for a false terminator, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A

The exact false terminator remains a no-header success; the two true rows compose one header matching R3.18BN; all focused/negative/full validations pass; payload/second-control consumption stays `0/0`. Publish only this bounded composition. Then open a separate **R3.18BP published-production differential** pass.

### Outcome B

Only a strict safe subset or narrower result representation can be implemented without violating R3.18BN. Publish only that exact subset/representation and rewrite the next differential accordingly.

### Outcome C

Authority drift, false-terminator header access, context/RL223 widening, payload/later-control access, generic chaining, production-scope drift or validation contradiction. Stop without publication.
'''
write('docs/continuity/MIMIR_R3_18BO_EXECUTION_SPEC.md', bo_spec)


# MIMIR_CONTINUE_HERE.md
p = 'MIMIR_CONTINUE_HERE.md'
text = read(p)
text = replace_field(text, 'LAST_COMPLETED_CONTRACT_PASS', f'R3.18BN — exact following-header context contract / Outcome A / 2 exact eight-field tuples / multiplicity 2 / 1 false terminator outside membership / contract {CONTRACT_SHA} / older-contract inheritance false / RL223 retained')
text = replace_field(text, 'CURRENT_PASS', 'R3.18BO — bounded post-BK mixed-continuation following-header production')
text = replace_field(text, 'CURRENT_PASS_TYPE', 'bounded production implementation / validate one exact published BK mixed control; false terminates with no header, true composes exactly one BN-admitted header and stops at payload_start')
append = f'''\n\n### R3.18BN exact following-header context contract: OUTCOME A / CLOSED
- contract `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json` / sha256 `{CONTRACT_SHA}`
- exact_tuple_only / 2 complete eight-field contexts / multiplicity 2 / Boolean=1 ActiveActor=1 / property ordinal 7 on 2/2
- full lane 3 rows; one BK-false terminator outside header membership; exact true headers 2
- validation `{VALID_RUN}/{VALID_JOB}` SUCCESS; Knowledge Archive `{KA_RUN}/{KA_JOB}` SUCCESS
- anti-widening: tag/component/ordinal/Cartesian/versionless/RL223-drop-or-flip/BD-AT-AJ-Z-P inheritance/fabricated-third all rejected
- production unchanged at R3.18BK; payload/second-control remain 0/0

### R3.18BO bounded post-BK mixed-continuation following-header production: ACTIVE
- validate/recompute one exact published BK mixed control
- false path: successful terminator, zero following-header access
- true path: exactly one stateless header primitive call, exact R3.18BN membership, stop at `payload_start`
- no following payload, second later control, generalized property cursor, or semantic/runtime widening
'''
if '### R3.18BN exact following-header context contract: OUTCOME A / CLOSED' in text:
    raise SystemExit('Continue already contains BN closed section')
text += append
write(p, text)


# Knowledge graph: chain + numbered mandatory order repair + newest override.
p = 'MIMIR_KNOWLEDGE_GRAPH.md'
text = read(p)
old_chain = 'R3.18BM one following-property-header evidence after published R3.18BK mixed control / Outcome A CLOSED\nR3.18BN exact following-header context contract after R3.18BM / ACTIVE'
new_chain = 'R3.18BM one following-property-header evidence after published R3.18BK mixed control / Outcome A CLOSED\nR3.18BN exact following-header context contract after R3.18BM / Outcome A CLOSED\nR3.18BO bounded post-BK mixed-continuation following-header production / ACTIVE'
text = replace_once(text, old_chain, new_chain, 'KG current chain')
old_reading = '''167. `docs/continuity/MIMIR_R3_18BM_EXECUTION_SPEC.md`
168. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
169. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
170. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
171. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
172. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
173. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
174. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
new_reading = '''167. `docs/continuity/MIMIR_R3_18BM_EXECUTION_SPEC.md`
168. `docs/continuity/MIMIR_R3_18BM_DECISION.md`
169. `docs/continuity/MIMIR_R3_18BN_EXECUTION_SPEC.md`
170. `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json`
171. `docs/continuity/MIMIR_R3_18BN_DECISION.md`
172. `docs/continuity/MIMIR_R3_18BO_EXECUTION_SPEC.md`
173. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
174. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
175. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
176. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
177. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
178. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
179. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
text = replace_once(text, old_reading, new_reading, 'KG mandatory reading repair')
kg_append = f'''\n\n## CURRENT OVERRIDE — 2026-09-09 — R3.18BN CLOSED / R3.18BO ACTIVE

This newest override supersedes older historical `ACTIVE` wording above.

- canonical production remains R3.18BK `{PROD_SHA}` / `{PROD_TREE}`;
- R3.18BN Outcome A is closed under contract `sha256:{CONTRACT_SHA}`;
- exact membership is two complete eight-field tuples, multiplicity 2, with the one BK-false row outside membership;
- exact tuples are `(72,6,95,Boolean,868,32,10,false)` x1 and `(110,6,66,ActiveActor,868,32,10,false)` x1;
- validation `{VALID_RUN}/{VALID_JOB}` and Knowledge Archive `{KA_RUN}/{KA_JOB}` are SUCCESS;
- no tag/component/ordinal/Cartesian/versionless/RL223-drop-or-flip/older-contract/fabricated membership is admitted;
- production/Cargo/fixture/corpus/support mutation remains `0/0/0/0/0`;
- R3.18BO is ACTIVE as the separate bounded production pass; false terminates without header, true may compose exactly one BN-member header and stop at `payload_start`.

Mandatory newest reading order:
1. `MIMIR_CONTINUE_HERE.md`
2. `docs/continuity/MIMIR_R3_18BM_DECISION.md`
3. `docs/continuity/MIMIR_R3_18BN_EXECUTION_SPEC.md`
4. `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json`
5. `docs/continuity/MIMIR_R3_18BN_DECISION.md`
6. `docs/continuity/MIMIR_R3_18BO_EXECUTION_SPEC.md`
7. `docs/continuity/MIMIR_CONTINUITY_STATE.json`
8. `docs/continuity/MIMIR_CURRENT_STATE.md`
9. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
10. `docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md`
11. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
12. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
13. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
14. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`
'''
if '## CURRENT OVERRIDE — 2026-09-09 — R3.18BN CLOSED / R3.18BO ACTIVE' in text:
    raise SystemExit('KG already contains BN/BO override')
text += kg_append
write(p, text)


# Boundary locks: replace only current override.
p = 'docs/continuity/MIMIR_BOUNDARY_LOCKS.md'
text = read(p)
start = text.index('# 0. Current override')
stop = text.index('# 1. Status vocabulary')
new_override = f'''# 0. Current override — R3.18BN exact-context contract closed / R3.18BO bounded production active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BK
- `{PROD_SHA}` / `{PROD_TREE}` remains canonical production.
- exactly the three immutable BI/BG/BH authority rows are admitted at the BK one-control boundary.
- false=1 / true=2 are both valid BK results; following stream/header/payload/second-control remain outside production.

## CLOSED READ-ONLY EVIDENCE — R3.18BM Outcome A
- evidence `{BM_HEAD}` / `{BM_RUN}/{BM_JOB}` SUCCESS; same-head CI `{BM_CI_RUN}/{BM_CI_JOB}` SUCCESS.
- exact three-row split: one false terminator / two true headers; native/Boxcars exact 2/2; unique contexts 2.
- exact contexts: `(72,6,95,Boolean,868,32,10,false)` and `(110,6,66,ActiveActor,868,32,10,false)`.
- mismatch/unclassified/reselection 0/0/0; following payload/second-control 0/0.

## CLOSED CONTRACT — R3.18BN Outcome A
- contract sha256 `{CONTRACT_SHA}`; membership policy `exact_tuple_only`.
- exactly 2 complete eight-field tuples, multiplicity 1 each / sum 2.
- the one BK-false terminator remains outside header membership.
- no tag/component/ordinal/Cartesian/versionless/RL223-drop-or-flip/BD-AT-AJ-Z-P inheritance/fabricated-third widening.

## ACTIVE BOUNDED PRODUCTION — R3.18BO
- validate/recompute one exact published BK mixed-control prior;
- false BK result is a successful no-header terminator with zero following-header access;
- true BK result may invoke exactly one existing stateless header primitive;
- true header must match exact R3.18BN membership;
- final stop is exactly `payload_start`.

## CLOSED
- any following-header synthesis on the BK-false terminator;
- any header context outside exact R3.18BN membership;
- following payload after the one R3.18BO header;
- second later property-control bit;
- repeated/generalized property loop or generic cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

'''
text = text[:start] + new_override + text[stop:]
write(p, text)


# Structured continuity JSON.
p = 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
data = json.loads(read(p))
data['updated_date'] = DATE
data['last_completed_contract_pass'] = 'R3.18BN'
data['current_pass'] = 'R3.18BO'
data['current_pass_kind'] = 'bounded production composition of exactly one R3.18BN-admitted following header after a validated published R3.18BK mixed control'
data['current_pass_goal'] = 'Validate/recompute the exact published BK mixed control; preserve the false row as a no-header terminator and compose exactly one BN-admitted header on only the two true rows, stopping at payload_start.'
data['current_pass_stop_boundary'] = 'No following payload, no second later control, no header on the false terminator, no context outside exact R3.18BN membership, and no generalized cursor.'
if 'last_completed_contract_outcome' in data:
    data['last_completed_contract_outcome'] = f'A — exact_tuple_only / 2 complete eight-field contexts / multiplicity 2 / one false terminator outside membership / contract {CONTRACT_SHA}.'
for key in ('mandatory_reading_order', 'mandatory_reading', 'current_reading_order'):
    if isinstance(data.get(key), list):
        for item in [
            'docs/continuity/MIMIR_R3_18BM_DECISION.md',
            'docs/continuity/MIMIR_R3_18BN_EXECUTION_SPEC.md',
            'docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json',
            'docs/continuity/MIMIR_R3_18BN_DECISION.md',
            'docs/continuity/MIMIR_R3_18BO_EXECUTION_SPEC.md',
        ]:
            if item not in data[key]:
                data[key].append(item)
blocked = data.get('blocked_frontiers')
if isinstance(blocked, list):
    for item in [
        'following-header success on the R3.18BK false terminator row',
        'following payload after the future R3.18BO one-header boundary',
        'second later property-control bit after R3.18BO',
        'generalized/repeated property loop or generic cursor after R3.18BO',
        'header context outside exact R3.18BN membership',
    ]:
        if item not in blocked:
            blocked.append(item)
data['r3_18bn'] = {
    'outcome': 'A',
    'canonical_base_sha': BASE_SHA,
    'canonical_base_tree': BASE_TREE,
    'production_sha_unchanged': PROD_SHA,
    'contract_path': 'docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json',
    'contract_sha256': CONTRACT_SHA,
    'membership_policy': 'exact_tuple_only',
    'frozen_lane_rows': 3,
    'false_terminators': 1,
    'observed_header_rows': 2,
    'unique_exact_contexts': 2,
    'multiplicity_sum': 2,
    'observed_tags': {'Boolean': 1, 'ActiveActor': 1},
    'observed_property_ordinal': 7,
    'validation_run_job': [VALID_RUN, VALID_JOB],
    'knowledge_archive_run_job': [KA_RUN, KA_JOB],
    'production_cargo_fixture_corpus_support_mutation': [0, 0, 0, 0, 0],
    'following_payload_second_control_bits': [0, 0],
}
write(p, json.dumps(data, indent=2, ensure_ascii=False) + '\n')


# Current state is deliberately concise and fully current.
current_state = f'''# MIMIR — Current Canonical State

**Continuity date:** {DATE}
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18BK — bounded post-BI next property-control production`
**Last read-only evidence/audit:** `R3.18BM — Outcome A / false=1 true=2 / one-header exact 2/2 / contexts=2 / artifact {BM_ARTIFACT}`
**Last completed contract:** `R3.18BN — exact_tuple_only / 2 eight-field contexts / multiplicity 2 / contract {CONTRACT_SHA}`
**Current exact pass:** `R3.18BO — bounded post-BK mixed-continuation following-header production`

## Truthful boundary

R3.18BK remains canonical production. R3.18BM closed evidence Outcome A on the exact immutable three-row lane. R3.18BN now closes contract Outcome A and freezes exactly these two complete contexts:

```text
(72,  6, 95, Boolean,     868, 32, 10, false) x1
(110, 6, 66, ActiveActor, 868, 32, 10, false) x1
```

The one BK-false row remains outside header membership. Exact contract SHA-256 is `{CONTRACT_SHA}`. Validation `{VALID_RUN}/{VALID_JOB}` and Knowledge Archive `{KA_RUN}/{KA_JOB}` are SUCCESS. Production/Cargo/fixture/corpus/support mutation is `0/0/0/0/0`.

## Active production gate

R3.18BO may validate/recompute one published BK mixed result. False must succeed as a no-header terminator with zero post-BK reads. True may invoke exactly one stateless existing-actor header primitive, require exact R3.18BN membership, and stop exactly at `payload_start`.

## Hard stop

No following payload, second later control, header on the false terminator, context outside exact R3.18BN membership, generalized/repeated property cursor, or actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
'''
write('docs/continuity/MIMIR_CURRENT_STATE.md', current_state)


handoff = f'''# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BK** at `{PROD_SHA}` / `{PROD_TREE}`.

**R3.18BM is CLOSED / Outcome A evidence.** Exact three-row lane false=1 / true=2; the false row has zero following-header access; the two true rows are native/Boxcars exact 2/2 through `payload_start`; contexts=2; payload/second-control=0/0.

**R3.18BN is CLOSED / Outcome A contract.** Exact contract `sha256:{CONTRACT_SHA}` admits only:
- `(72,6,95,Boolean,868,32,10,false)` x1
- `(110,6,66,ActiveActor,868,32,10,false)` x1

The one BK-false terminator remains outside membership. Contract validation `{VALID_RUN}/{VALID_JOB}` and Knowledge Archive `{KA_RUN}/{KA_JOB}` are SUCCESS. No production/Cargo/fixture/corpus/support mutation occurred.

Active pass: **R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production**.

R3.18BO must validate/recompute the exact BK prior; false returns a successful no-header terminator; true composes exactly one stateless header under exact BN membership and stops at `payload_start`. Following payload, second later control and generalized cursor remain forbidden.

Read first: `MIMIR_CONTINUE_HERE.md`, BM decision, BN execution spec, BN admitted contract, BN decision, BO execution spec, continuity state/current state/boundary locks, then the root knowledge graph authority chain.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. CI waiting is not a reason to duplicate the same SHA/workflow/input.
'''
write('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md', handoff)


p = 'docs/continuity/MIMIR_PROGRESS_LEDGER.md'
text = read(p)
entry = f'''\n\n## {DATE} — R3.18BN — Exact Following-Header Context Contract Outcome A

- canonical base `{BASE_SHA}` / `{BASE_TREE}`; production unchanged at R3.18BK `{PROD_SHA}` / `{PROD_TREE}`.
- candidate validation `{VALID_RUN}/{VALID_JOB}` SUCCESS; Knowledge Archive `{KA_RUN}/{KA_JOB}` SUCCESS.
- contract `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json` / sha256 `{CONTRACT_SHA}`.
- exact_tuple_only; 2 complete eight-field contexts; multiplicity 1+1=2; Boolean=1 / ActiveActor=1; property ordinal 7 on 2/2.
- one BK-false terminator remains outside membership.
- tag/component/ordinal/Cartesian/versionless/RL223-drop-or-flip/BD-AT-AJ-Z-P inheritance/fabricated-third negatives PASS.
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; following payload/second-control 0/0.

Next exact pass:
- `R3.18BO — bounded post-BK mixed-continuation following-header production`; false terminates without header, true composes exactly one BN-member header and stops at payload_start.
'''
if '## 2026-09-09 — R3.18BN — Exact Following-Header Context Contract Outcome A' in text:
    raise SystemExit('ledger already contains BN entry')
text += entry
write(p, text)


# Final local semantic guards.
contract_loaded = json.loads(read('docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json'))
tuples = {tuple(r[k] for k in fields) for r in contract_loaded['admitted_contexts']}
expected = {
    (72, 6, 95, 'Boolean', 868, 32, 10, False),
    (110, 6, 66, 'ActiveActor', 868, 32, 10, False),
}
assert tuples == expected
assert sum(r['observed_count'] for r in contract_loaded['admitted_contexts']) == 2
assert contract_loaded['terminator_policy']['false_terminators_produce_header_membership'] is False
assert all(v is False for v in contract_loaded['anti_widening'].values())
assert hashlib.sha256(read('docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json').encode()).hexdigest() == CONTRACT_SHA
print('R3_18BN_ADMISSION_GENERATOR=PASS')
