from pathlib import Path
import json

MAIN = '6b73a7e8f8639f8078dff0e656fc0fb9ea0bbc18'
PROD = '7390e3b145372252caaa8fa1fe3e0cd13b83336c'
AUTH_HEAD = '0febcde7b312b6724e86ba156c700b41cf0562b7'
AUTH_RUN = 31871353806
AUTH_JOB = 94980384463
CI_RUN = 31871353749
CI_JOB = 94980384205
ARTIFACT = 9243555556
ARTIFACT_DIGEST = 'sha256:514580727df642ebde04d69824402db46ed48ff66755d4b17c0db6e69ac5eb3d'

HASHES = {
    'aggregate': '2d2f153f8f23f07efae3e90216acf9f7c2d4df83548825a622a5a1343e37f5f0',
    'source_scope': '05dad8c789c61ed0ad25654544625ae67f0a969e68067efaa18e1c7c8c36b4fc',
    'numeric_rule': '7bf0f71e178b9c3c132473d3c67ee194e3b7cea54fb6690fec69fcd39b6a1190',
    'replay_identity': 'b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf',
    'instrumentation_patch': '4c7f92eb0315b5f62fb0d7ed059c775ed1381c351033ccfbfa218d9e308e068f',
    'witness_manifest': 'e1b80971cc1787692d5355f14a6b18d49fdffd31baf7350b7783d6be6ae623ab',
    'match_rows': 'ff4c908872a6ff46a58cabaff0d13b12691360a3e82ca00f3c5b5caf2466a6b5',
    'summary': 'aade96f9a47d6ba4cf74ef2b27370e7f6758c8041e0a8951ce418b9965c92fe2',
    'negative_controls': 'a0a5dacc2c544d913f20bbbd68b2f736a33ca0974181fc62f4e1e410eeb66e7c',
    'receipt': 'ecdf56c674627de997e7de417a8f50335b03d170c494fe5b5207f1f581048677',
    'driver_receipt': 'bd2ac7c6fea99d140ba2f89240846d6e326b0badd69eda4b0c685a20e7a68365',
}

K4_TAGS = [
    'CamSettings', 'TeamPaint', 'TeamLoadout', 'ClubColors', 'Reservation',
    'StatEvent', 'PlayerHistoryKey', 'DemolishFx', 'DemolishExtended',
    'ExtendedExplosion', 'LoadoutsOnline',
]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one anchor, got {count}')
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# Decision and next-pass spec
# ---------------------------------------------------------------------------

decision = f'''# MIMIR R3.17L Decision — Native K3 Differential Audit

**Outcome:** A — ADMITTED / COMPLETE  
**Pass type:** read-only real-replay differential audit  
**Production Rust:** unchanged  
**Canonical production SHA:** `{PROD}`  
**Continuity base:** `{MAIN}`

## Authority

- evidence head: `{AUTH_HEAD}`
- authority workflow run/job: `{AUTH_RUN} / {AUTH_JOB}` — SUCCESS
- exact-head normal CI run/job: `{CI_RUN} / {CI_JOB}` — SUCCESS
- artifact: `{ARTIFACT}` (`r317l-native-k3-differential-v3`)
- artifact digest: `{ARTIFACT_DIGEST}`
- artifact ZIP size: 287,021 bytes
- pinned Boxcars: `c70e77df7af81b436cb545d070bb90c82f562d0b`
- R3.17J allowlist SHA256: `9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911`

The first two R3.17L runs are not authority. Attempt 1 stopped at external-probe Cargo workspace plumbing after already proving 47/47 replay regeneration and 1,950/1,950 real-witness group coverage. Attempt 2 stopped before audit work because Windows resolved `bash` to the WSL launcher. V3 froze the V1 workflow blob, used exact Git Bash, and made only the empty external-probe `[workspace]` repair. Semantic and tolerance rules were unchanged.

## Differential result

```text
replay identity                   47/47
Boxcars oracle decode             47/47
K3 occurrences regenerated        1,699,169
exact group reconstruction        1,950/1,950
real witness group coverage       1,950/1,950
native decode success             1,950/1,950
tag / value variant match         1,950/1,950
context match                     1,950/1,950
payload start/end/width match     1,950/1,950
packed-code match                 1,950/1,950
semantic-value match              1,950/1,950
mismatches                        0
negative controls                 PASS / 7 focused tests
bit monotonicity failures         0
packed-payload failures           0
privacy                           PASS
production mutation               0
Cargo mutation                    0
fixture mutation                  0
corpus mutation                   0
support-lane mutation             0
```

The frozen quaternion rule allowed at most `1e-5` absolute difference only for the reconstructed largest component because pinned Boxcars uses chained f32 `mul_add` while native production uses equivalent explicit f32 operations. The observed maximum was `5.960464477539063e-08`. Non-largest quaternion components and vector components were compared by exact f32 bit identity.

## Durable receipt hashes

```text
aggregate                         {HASHES['aggregate']}
source scope                      {HASHES['source_scope']}
numeric rule                      {HASHES['numeric_rule']}
replay identity                   {HASHES['replay_identity']}
Boxcars instrumentation patch     {HASHES['instrumentation_patch']}
witness manifest                  {HASHES['witness_manifest']}
match rows                        {HASHES['match_rows']}
summary                           {HASHES['summary']}
negative controls                 {HASHES['negative_controls']}
receipt manifest                  {HASHES['receipt']}
V3 driver receipt                 {HASHES['driver_receipt']}
```

The artifact was downloaded independently after the workflow. Its ZIP SHA256 matched the GitHub artifact digest exactly, all 14 expected files were present, and all 11 hashes listed by the internal receipt manifest recomputed without mismatch. The instrumentation patch contains field-name literals such as `raw_bits_hex`, but the durable witness/match/summary evidence contains no raw payload bytes or player/account identity.

## Admission

R3.17K is now differentially validated on the complete R3.17J exact K3 structural/context group surface represented by the frozen 47-replay lane. This closes the K3 spatial/physics wave without widening the production decoder.

R3.17L does **not** admit a second property, property-loop iteration, next actor/frame, lifecycle mutation, K4 payload decoding, raw state, events, replay slicing, skills, runtime or export widening.

## Next pass

The execution roadmap still places the K4 gameplay-structured attribute wave inside R3.17 before R3.18 property-loop work. Therefore the next pass is:

**R3.17M — K4 Gameplay Structured Wire-Format Evidence**

Production implementation remains forbidden in R3.17M.
'''
Path('docs/continuity/MIMIR_R3_17L_DECISION.md').write_text(decision, encoding='utf-8', newline='\n')

m_spec = f'''# MIMIR R3.17M Execution Spec — K4 Gameplay Structured Wire-Format Evidence

**Pass type:** read-only evidence  
**Production implementation:** forbidden  
**Production authority:** R3.17K, confirmed by R3.17L  
**Continuity base:** `{MAIN}`  
**Production SHA:** `{PROD}`  
**Pinned Boxcars:** `c70e77df7af81b436cb545d070bb90c82f562d0b`

## 1. Goal

Characterize the exact observed wire formats and context families for the R3.17 roadmap K4 gameplay-structured tags across the same frozen 47-replay supported lane:

```text
CamSettings
TeamPaint
TeamLoadout
ClubColors
Reservation
StatEvent
PlayerHistoryKey
DemolishFx
DemolishExtended
ExtendedExplosion
LoadoutsOnline
```

This pass gathers evidence only. It does not admit a K4 contract and does not add a native K4 decoder.

## 2. Frozen inputs

- supported replay lane: exact same 47 replay identities used by R3.17I/L
- replay identity SHA256: `{HASHES['replay_identity']}`
- R3.17L authority head: `{AUTH_HEAD}`
- R3.17L run/job: `{AUTH_RUN} / {AUTH_JOB}` SUCCESS
- R3.17L artifact: `{ARTIFACT}`
- R3.17L artifact digest: `{ARTIFACT_DIGEST}`
- native K3 production SHA: `{PROD}`
- no support-lane widening

## 3. Evidence method

1. Verify fresh `main`, production SHA/tree/blobs, exact 47 replay identities and pinned Boxcars SHA before instrumentation.
2. Instrument pinned Boxcars at the already-resolved attribute payload boundary. Production MIMIR code remains untouched.
3. For every K4 occurrence, record exact payload start/end/width, replay version/net-version/RL223 context, tag, structural branch choices and exact subfield boundaries.
4. Build deterministic shape IDs from wire structure and branch choices, never from debug-string formatting.
5. Record frequency distributions by tag, shape, version/context and payload width.
6. Persist privacy-safe deterministic witnesses covering every observed shape/context family. Raw payload bytes may be used ephemerally for validation but must not enter durable public evidence.
7. Validate cursor monotonicity, packed-bit shape, replay identity and deterministic rerun accounting.
8. Keep production/Cargo/fixture/corpus/support-lane mutation at zero.

## 4. Per-tag evidence requirements

The instrumentation must expose enough internal cursor markers to reconstruct the exact read order and branch shape for each observed tag. Source-code inspection may guide marker placement, but **source code alone is not admission evidence**. A tag or branch with zero supported-lane occurrences remains unadmitted.

At minimum, capture every version/context-gated optional branch, collection count/length, nested identifier/reference choice, primitive field width/order, and exact subfield bit range needed to make a later contract deterministic. Do not flatten structurally distinct branches into one shape merely because their decoded values happen to match.

## 5. Required gates

```text
replay identity                         47/47
Boxcars oracle decode                   47/47
K4 occurrence accounting               exact + deterministic
observed shape classification          100%
unclassified/mismatch                  0
bit monotonicity failures               0
raw packed-payload shape failures       0
privacy                                 PASS
production mutation                     0
Cargo mutation                          0
fixture/corpus/support-lane mutation    0/0/0
```

For each of the 11 target tags, occurrence count must be reported explicitly. Zero occurrence is valid evidence of insufficiency, not permission to infer a contract from Boxcars source.

## 6. Outcome rules

**Outcome A:** every K4 tag/branch intended for the next contract is observed sufficiently, all observed occurrences are deterministically classified, cursor/raw-payload gates are clean, privacy passes, and all mutation counters are zero. Only then may the next pass admit evidence-supported K4 shapes.

**Outcome B:** one or more tags or material branches lack supported-lane evidence. Keep production closed and perform only targeted evidence work or explicitly narrow the future K4 contract to evidence-supported tags.

**Outcome C:** instrumentation or structural assumptions are contradicted. Stop and repair the evidence model before any K4 contract pass.

## 7. Hard stop

No production Rust, Cargo, fixture, corpus or support-lane changes. No K4 contract or native K4 implementation. No second property/property loop, next actor/frame, lifecycle mutation, raw-state extraction, events, replay slicing, skill mining, runtime or export widening.

If R3.17M closes with Outcome A, the next pass is a **separate K4 contract admission pass**. R3.18 remains closed until the R3.17 attribute-family dependency is explicitly satisfied.
'''
Path('docs/continuity/MIMIR_R3_17M_EXECUTION_SPEC.md').write_text(m_spec, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# JSON state
# ---------------------------------------------------------------------------
state_path = Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-15'
state['last_completed_read_only_audit'] = 'R3.17L'
state['current_pass'] = 'R3.17M'
state['current_pass_kind'] = 'read-only K4 gameplay-structured wire-format evidence across the frozen 47-replay lane'
state['current_pass_goal'] = 'Characterize exact observed wire shapes, branches, contexts and subfield bit boundaries for the roadmap K4 gameplay-structured tags using pinned Boxcars, with deterministic privacy-safe evidence.'
state['current_pass_stop_boundary'] = 'Evidence only; no production Rust/Cargo/fixture/corpus/support-lane mutation, no K4 contract/implementation, and no second property, actor/frame, lifecycle, raw-state/event/skill/runtime/export widening.'
state['r3_17l'] = {
    'outcome': 'A — admitted / complete',
    'pass_type': 'read-only real-replay native K3 differential audit',
    'production_source_changed': False,
    'continuity_base_sha': MAIN,
    'production_sha': PROD,
    'authority_head': AUTH_HEAD,
    'workflow_run': AUTH_RUN,
    'workflow_job': AUTH_JOB,
    'exact_head_ci_run': CI_RUN,
    'exact_head_ci_job': CI_JOB,
    'artifact_id': ARTIFACT,
    'artifact_digest': ARTIFACT_DIGEST,
    'supported_replays': 47,
    'oracle_decode_success': 47,
    'regenerated_k3_occurrences': 1699169,
    'admitted_groups': 1950,
    'real_witness_group_coverage': '1950/1950',
    'native_decode_success': '1950/1950',
    'exact_semantic_match': '1950/1950',
    'mismatch_count': 0,
    'max_quaternion_reconstructed_component_abs_diff': 5.960464477539063e-08,
    'negative_controls': 'PASS / 7 focused tests',
    'privacy': 'PASS',
    'production_cargo_fixture_corpus_support_mutation': '0/0/0/0/0',
    'aggregate_sha256': HASHES['aggregate'],
    'witness_manifest_sha256': HASHES['witness_manifest'],
    'match_rows_sha256': HASHES['match_rows'],
    'summary_sha256': HASHES['summary'],
    'driver_receipt_sha256': HASHES['driver_receipt'],
    'next_pass': 'R3.17M',
}
# Keep evidence pass terminology honest: L is an audit, not the K4 evidence pass.
files = [x for x in state['next_files_to_read'] if x not in {
    'docs/continuity/MIMIR_R3_17L_DECISION.md',
    'docs/continuity/MIMIR_R3_17M_EXECUTION_SPEC.md',
}]
idx = files.index('docs/continuity/MIMIR_R3_17L_EXECUTION_SPEC.md') + 1
files[idx:idx] = ['docs/continuity/MIMIR_R3_17L_DECISION.md', 'docs/continuity/MIMIR_R3_17M_EXECUTION_SPEC.md']
state['next_files_to_read'] = files
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Current state
# ---------------------------------------------------------------------------
current_path = Path('docs/continuity/MIMIR_CURRENT_STATE.md')
current = current_path.read_text(encoding='utf-8')
current = replace_once(current, '**Continuity date:** 2026-08-14', '**Continuity date:** 2026-08-15', 'current date')
current = replace_once(current, '**Current exact pass:** `R3.17L — native K3 real-replay differential audit`', '**Completed K3 differential:** `R3.17L — Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch`\n**Current exact pass:** `R3.17M — K4 gameplay-structured wire-format evidence`', 'current pass header')
old = '''## 3. R3.17L exact next pass\n\nR3.17L is read-only. Regenerate real K3 witnesses ephemerally from the frozen 47-replay R3.17I lane using pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`, cover at least one real occurrence for every one of the 1,950 admitted exact groups, then compare native tag/variant, context, exact bit start/end/width, structural codec metadata and semantic values against the oracle.\n\nA mismatch is not fixed inside R3.17L. It produces Outcome C and sends the project back to corrective evidence/contract/implementation work. Durable audit output remains privacy-safe; raw real payload bytes stay ephemeral.\n\n## 4. Still closed\n'''
new = f'''## 3. R3.17L differential closure\n\n```text\nauthority head                {AUTH_HEAD}\nauthority run/job             {AUTH_RUN} / {AUTH_JOB} SUCCESS\nexact-head normal CI          {CI_RUN} / {CI_JOB} SUCCESS\nartifact                      {ARTIFACT}\nartifact digest               {ARTIFACT_DIGEST}\nreplay identity               47/47\nBoxcars oracle decode         47/47\nregenerated K3 occurrences    1699169\nreal group coverage           1950/1950\nnative decode                 1950/1950\nvariant/context/range/code    1950/1950 exact\nsemantic value                1950/1950 exact\nmismatch                      0\nmax quaternion abs diff       5.960464477539063e-08\nnegative controls             PASS / 7 tests\nprivacy                       PASS\nproduction/Cargo/fixture/\ncorpus/support mutation       0/0/0/0/0\noutcome                       A\n```\n\nThe frozen quaternion tolerance was `1e-5` only for the reconstructed largest component; the observed maximum was far below it. All vector components and non-largest quaternion components were compared by exact f32 bit identity.\n\n## 4. R3.17M exact next pass\n\nR3.17M is read-only K4 evidence over the same frozen 47-replay lane. Instrument pinned Boxcars for `CamSettings`, `TeamPaint`, `TeamLoadout`, `ClubColors`, `Reservation`, `StatEvent`, `PlayerHistoryKey`, `DemolishFx`, `DemolishExtended`, `ExtendedExplosion`, and `LoadoutsOnline`; classify every observed wire shape/context and persist deterministic privacy-safe witnesses. A zero-occurrence tag remains unadmitted.\n\nProduction K4 decoding remains closed. If R3.17M closes Outcome A, K4 contract admission is a separate pass before any native implementation. R3.18 property-loop work remains closed until the R3.17 attribute-family dependency is explicitly satisfied.\n\n## 5. Still closed\n'''
current = replace_once(current, old, new, 'current L section')
current = replace_once(current, 'K4 payload decode\nsecond property / property-loop continuation', 'K4 contract / native payload decode\nsecond property / property-loop continuation', 'current closed K4')
current_path.write_text(current, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Root handbook
# ---------------------------------------------------------------------------
hand_path = Path('MIMIR_CONTINUE_HERE.md')
hand = hand_path.read_text(encoding='utf-8')
hand = replace_once(hand, 'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.17H — native K2 differential audit / Outcome A / 469 of 469 exact / 7 of 7 negatives', 'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.17L — native K3 differential audit / Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch', 'handbook audit')
hand = replace_once(hand, 'CURRENT_PASS:\n  R3.17L — native K3 differential audit against regenerated real-replay witnesses\n\nCURRENT_PASS_TYPE:\n  read-only differential audit / real-replay native-vs-pinned-oracle verification; production Rust forbidden', 'CURRENT_PASS:\n  R3.17M — K4 gameplay-structured wire-format evidence\n\nCURRENT_PASS_TYPE:\n  read-only evidence / pinned-oracle wire-shape characterization; production Rust forbidden', 'handbook current pass')
old_open = '''R3_17L_OPEN_BOUNDARY:\n  read-only differential audit; production Rust changes are forbidden\n  freeze R3.17K production SHA/tree/blobs, R3.17J allowlist, R3.17I artifact/groups and pinned Boxcars SHA\n  regenerate real witness payloads ephemerally from the frozen 47-replay lane\n  deterministically cover at least one real occurrence for every one of the 1950 admitted exact groups\n  compare tag/value variant, exact start/end/width, structural codec metadata, context and semantic value against the pinned oracle\n  retain only privacy-safe structural identities/hashes in durable evidence; raw witness payload bytes remain ephemeral\n  any mismatch or contract contradiction stops the pass; do not repair production inside the audit\n\nR3_17L_HARD_STOP:\n  no production Rust, Cargo, fixture, corpus or support-lane mutation\n  no second property / property-loop continuation\n  no next actor / next frame / lifecycle mutation\n  no K4, raw-state, event, replay-slice, skill, runtime or export widening\n\nNEXT PASS AFTER R3.17L:\n  choose only from the execution roadmap after R3.17L Outcome A; do not assume R3.18 before the audit is closed\n'''
new_open = f'''R3_17L_AUDIT_CLOSURE:\n  Outcome A / read-only / production Rust unchanged at {PROD}\n  authority head: {AUTH_HEAD}\n  authority run/job: {AUTH_RUN} / {AUTH_JOB} SUCCESS\n  exact-head normal CI: {CI_RUN} / {CI_JOB} SUCCESS\n  artifact: {ARTIFACT}\n  artifact digest: {ARTIFACT_DIGEST}\n  47/47 replay identity + Boxcars oracle decode\n  1950/1950 exact group reconstruction + real witness coverage + native decode + semantic match\n  mismatch count: 0; negative controls: PASS; privacy: PASS\n  max quaternion reconstructed-largest abs diff: 5.960464477539063e-08 under frozen 1e-5 rule\n  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0\n\nR3_17M_OPEN_BOUNDARY:\n  read-only K4 gameplay-structured evidence; production Rust changes are forbidden\n  same frozen 47-replay lane and pinned Boxcars SHA only\n  target tags: CamSettings / TeamPaint / TeamLoadout / ClubColors / Reservation / StatEvent / PlayerHistoryKey / DemolishFx / DemolishExtended / ExtendedExplosion / LoadoutsOnline\n  characterize exact field order, optional/version branches, subfield bit boundaries, payload widths and context families\n  deterministic shape IDs and privacy-safe witnesses for every observed shape/context family\n  zero-occurrence tags/branches remain unadmitted; Boxcars source alone is not contract evidence\n\nR3_17M_HARD_STOP:\n  no production Rust, Cargo, fixture, corpus or support-lane mutation\n  no K4 contract or implementation\n  no second property / property-loop continuation\n  no next actor / next frame / lifecycle mutation\n  no raw-state, event, replay-slice, skill, runtime or export widening\n\nNEXT PASS AFTER R3.17M:\n  only if Outcome A, open a separate evidence-supported K4 contract admission pass; R3.18 remains closed\n'''
hand = replace_once(hand, old_open, new_open, 'handbook L/M boundary')
# Add L closure immediately after K production closure block if not present elsewhere.
needle = 'R3_17K_PRODUCTION_CLOSURE:\n'
if needle not in hand:
    raise SystemExit('handbook K closure missing')
hand_path.write_text(hand, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Knowledge graph
# ---------------------------------------------------------------------------
graph_path = Path('MIMIR_KNOWLEDGE_GRAPH.md')
graph = graph_path.read_text(encoding='utf-8')
graph = replace_once(graph, 'R3.17K K3 production decision             |\nR3.17L active K3 differential audit spec  |', 'R3.17K K3 production decision             |\nR3.17L K3 differential decision             |\nR3.17M active K4 evidence spec               |', 'graph top')
graph = replace_once(graph, '22. `docs/continuity/MIMIR_R3_17L_EXECUTION_SPEC.md`\n23. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n24. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n25. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n26. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n27. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n28. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n29. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`', '22. `docs/continuity/MIMIR_R3_17L_EXECUTION_SPEC.md`\n23. `docs/continuity/MIMIR_R3_17L_DECISION.md`\n24. `docs/continuity/MIMIR_R3_17M_EXECUTION_SPEC.md`\n25. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n26. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n27. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n28. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n29. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n30. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n31. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`', 'graph reading order')
graph = replace_once(graph, ' -> R3.17L native K3 real-replay differential audit: ACTIVE / READ-ONLY\n', f''' -> R3.17L native K3 real-replay differential audit: OUTCOME A / CLOSED\n      authority {AUTH_HEAD}\n      run/job {AUTH_RUN} / {AUTH_JOB} SUCCESS\n      exact-head CI {CI_RUN} / {CI_JOB} SUCCESS\n      artifact {ARTIFACT} / {ARTIFACT_DIGEST}\n      47/47 oracle + 1950/1950 real-group native semantic exact / 0 mismatch\n -> R3.17M K4 gameplay-structured wire-format evidence: ACTIVE / READ-ONLY\n''', 'graph chain')
graph = replace_once(graph, 'R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups with zero cross-product widening; R3.17K implemented exactly that contract and passed the 1,950-positive plus exhaustive structural acceptance gate. R3.17L is now the mandatory read-only real-replay differential audit. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.', 'R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups with zero cross-product widening; R3.17K implemented exactly that contract; R3.17L then matched all 1,950 exact groups against regenerated real-replay witnesses with zero mismatch. R3.17M is now the read-only K4 gameplay-structured wire-format evidence pass. K4 contract/implementation, property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed.', 'graph capability paragraph')
# Append L closure near end to preserve durable receipt in graph.
graph += f'''\n\n## R3.17L K3 differential closure\n\n```text\nauthority head              {AUTH_HEAD}\nauthority run/job           {AUTH_RUN} / {AUTH_JOB} SUCCESS\nexact-head normal CI        {CI_RUN} / {CI_JOB} SUCCESS\nartifact                    {ARTIFACT}\nartifact digest             {ARTIFACT_DIGEST}\nreplays                     47/47\nregenerated occurrences     1699169\nreal group coverage         1950/1950\nnative / semantic match     1950/1950 exact\nmismatch                    0\nmax quaternion abs diff     5.960464477539063e-08\nnegative controls           PASS\nprivacy                     PASS\nproduction/Cargo/fixture/\ncorpus/support mutations    0/0/0/0/0\noutcome                     A\nnext                        R3.17M K4 gameplay-structured wire evidence\n```\n'''
graph_path.write_text(graph, encoding='utf-8', newline='\n')

print('R3.17L continuity closure generated')
print('next=R3.17M K4 gameplay-structured wire-format evidence')
