from pathlib import Path
import json
import re

ROOT = Path('.')
CANONICAL_BASE = 'dd7d9550910a0ad08cd5f1a171d782b5dd4e954a'
PROD = '4adadd185783954c7fb6ad67db14b77b377cdde5'
PROD_TREE = '67b1969eaff49d2913b88b3921f27b1bd7fe8193'
LIB_BLOB = '42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662'
R318D_TEST_BLOB = '2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b'
EVIDENCE_HEAD = 'aae03a7fdec85e30be3954d14ffdc8cd1d86121e'
EVIDENCE_RUN = 31949407736
EVIDENCE_JOB = 95170443262
NORMAL_CI_RUN = 31949407685
NORMAL_CI_JOB = 95170443059
ARTIFACT_ID = 9264243765
ARTIFACT_DIGEST = '005afc3c97bd6bdb9aef69be993538fd813e30481923c59beefcf37e71cdfc9b'
ORACLE = 'c70e77df7af81b436cb545d070bb90c82f562d0b'


def regex_one(text: str, pattern: str, replacement: str, label: str, flags=re.MULTILINE) -> str:
    out, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f'{label}: expected one match, got {count}')
    return out


def replace_one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one match, got {count}')
    return text.replace(old, new, 1)


# Master continuity handbook.
p = ROOT / 'MIMIR_CONTINUE_HERE.md'
s = p.read_text(encoding='utf-8')
s = regex_one(s, r'^LAST_COMPLETED_READ_ONLY_AUDIT:\n  .+$', 'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18E — production control-bit real-replay differential audit / Outcome A / 94/94 exact / 0 mismatch', 'last read-only audit')
s = regex_one(s, r'^LAST_COMPLETED_EVIDENCE_PASS:\n  .+$', 'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18E — production control-bit differential audit / Outcome A / 47 terminator + 47 continuation / 94/94 exact / 0 mismatch', 'last evidence pass')
s = regex_one(s, r'^CURRENT_PASS:\n  .+$', 'CURRENT_PASS:\n  R3.18F — second-property-header real-replay evidence', 'current pass')
s = regex_one(s, r'^CURRENT_PASS_TYPE:\n  .+$', 'CURRENT_PASS_TYPE:\n  read-only evidence / observe the second property header boundary on the frozen real-replay continuation lane and stop at payload start', 'current pass type')

hard_stop = f'''CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload OR one R3.17J-admitted K3 payload OR one R3.17N-admitted K4 payload may be decoded natively
  K3 remains limited to its exact R3.17J structural/context allowlist; K4 remains limited to the exact 161 R3.17N tuples
  R3.18B composes exactly one existing-actor K1 property through its payload end
  R3.18D is production at {PROD} and, only from an already-valid R3.18B first-property result, reads exactly the next property_present bit and stops one bit later
  R3.18E closed Outcome A: 94/94 real-replay terminator/continuation rows matched pinned Boxcars exactly with zero second stream/header/payload consumption
  R3.18F is read-only second-property-header evidence only: on continuation witnesses it may observe property_present + bounded stream/header resolution through payload_start, then MUST stop before payload
  NO production second-property composition, second payload, repeated/generalized property loop, K2/K3/K4 wrapper composition, next actor, next frame, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening is admitted'''
s = regex_one(s, r'(?ms)^CURRENT_PRODUCTION_HARD_STOP:\n.*?(?=\nR3_17E_EVIDENCE_CLOSURE:)', hard_stop, 'production hard stop', flags=re.MULTILINE | re.DOTALL)

closure = f'''R3_18E_AUDIT_CLOSURE:
  Outcome A / read-only differential audit / production Rust unchanged at {PROD}
  canonical continuity base: {CANONICAL_BASE}
  evidence authority head: {EVIDENCE_HEAD}
  authority run/job: {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
  exact-head normal CI: {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
  artifact: {ARTIFACT_ID}
  artifact digest: sha256:{ARTIFACT_DIGEST}
  pinned oracle: nickbabcock/boxcars@{ORACLE}
  replay identity/oracle parse: 47/47
  deterministic rows: 94 = 47 terminator + 47 continuation
  native first-property success: 94/94
  native control success: 94/94
  first stop == oracle control start: 94/94
  control start/value/end/stop exact: 94/94
  native/oracle mismatch: 0
  aligned exact truncation negatives: 6; truncation/post-stop-poison/repeatability/malformed-first controls: PASS
  observed K1 tag rows: Boolean=1 / Byte=6 / Float=41 / Int=46
  second stream/header/payload bits consumed: 0/0/0
  privacy: PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0
  source scope SHA256: 3af876d4fee21e6f769b8db908babb67ec061dcc9265ab266aa4a0ce89a6d42a
  replay identity SHA256: b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
  Boxcars instrumentation SHA256: cd52172333fd095377c15d263f1f178291eb3588a637cc34720a202bc1408667
  selected witnesses SHA256: 3fbbece797c146e71dd5b569cce6882d5719ea2d39ecdd5198da351dc028e4c8
  selection summary SHA256: 353d90d7385fcf34f4dca246d63949653f7124641cf7a81185e62b32e0bff1cf
  comparison SHA256: 9789a2fb6a5573a6bdacef2702c7cff169e764f244eb1736144b9b2c8258452d
  aggregate SHA256: 1b505299bc155aa32d9e48dd6d1d39327ac9025fa480472d2c67cc721270fabd

R3_18F_OPEN_BOUNDARY:
  read-only second-property-header evidence; production Rust mutation forbidden
  production authority remains {PROD}; canonical docs may be newer
  replay identity lane remains the exact 47 supported replays; pinned oracle remains nickbabcock/boxcars@{ORACLE}
  deterministically reproduce the R3.18E 47 continuation + 47 terminator witness classes before observing any second header
  continuation positive lane: after exact R3.18B first property + exact R3.18D control=true, independently invoke the existing admitted property-header primitive at that same property_present start
  compare property_present, stream-id bit start/end/value, resolved property object, resolved attribute tag, payload_start and stop exactly with pinned Boxcars
  stop at second-property payload_start; second payload bits consumed MUST remain zero
  terminator negative lane: the same header primitive at control=false must consume exactly one property_present bit, expose no stream/object/tag/payload fields, and stop at the control end
  require deterministic repeatability, privacy-safe evidence, zero native/oracle mismatch and zero production/Cargo/fixture/corpus/support mutation

R3_18F_HARD_STOP:
  no production source, Cargo, fixture, corpus or support-lane mutation
  no second-property payload decode or semantic value claim
  no third property control/header observation and no repeated property loop
  no K2/K3/K4 composition through the R3.18B wrapper
  no next actor, next frame, lifecycle mutation, raw state, event, replay slice, skill, runtime or export widening

NEXT PASS AFTER R3.18F:
  only after Outcome A may a separate contract/production admission pass for a bounded second-property-header composition be defined; R3.18F itself publishes no production decoder and admits no second payload
'''
s = regex_one(
    s,
    r'(?ms)^R3_18E_OPEN_BOUNDARY:\n.*?^NEXT PASS AFTER R3\.18E:\n  [^\n]+$',
    closure.rstrip(),
    'R3.18E closure block',
    flags=re.MULTILINE | re.DOTALL,
)
p.write_text(s, encoding='utf-8', newline='\n')

# Machine-readable continuity state.
p = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(p.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-16'
state['last_production_code_sha'] = PROD
state['last_production_milestone'] = 'R3.18D'
state['last_production_milestone_name'] = 'minimal native existing-actor next-property control bit'
state['last_completed_read_only_audit'] = 'R3.18E'
state['last_completed_evidence_pass'] = 'R3.18E'
state['last_completed_evidence_outcome'] = 'A — 47/47 replay identity/oracle parse; 47 terminator + 47 continuation rows; 94/94 native first-property/control exact; start/value/end/stop exact; mismatch 0; second stream/header/payload bits 0/0/0'
state['current_pass'] = 'R3.18F'
state['current_pass_kind'] = 'read-only second-property-header real-replay evidence / exact header boundary only, no payload'
state['current_pass_goal'] = 'On the frozen R3.18E continuation witnesses, validate the second property_present + stream/header resolution boundary through payload_start against pinned Boxcars, while terminators remain one-bit no-header negatives.'
state['current_pass_stop_boundary'] = 'Stop at second-property payload_start for continuation rows and at the one-bit property_present end for terminators. No second payload, third property, repeated loop, production mutation, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening.'
state['closed_now'] = [
    'production second-property header composition',
    'second-property payload consumption or semantic value claim',
    'third property control/header observation or generalized production property_present loop',
    'K2/K3/K4 composition through the R3.18B single-property wrapper',
    'full actor envelope iteration',
    'full frame iteration',
    'actor state table mutation',
    'raw-state extraction',
    'event extraction',
    'replay slicing',
    'skill mining',
    'counterfactual rollout execution from native replay state',
]
state['r3_18e'] = {
    'outcome': 'A — admitted / read-only differential complete',
    'pass_type': 'production control-bit real-replay differential audit',
    'production_sha': PROD,
    'production_tree': PROD_TREE,
    'canonical_continuity_base': CANONICAL_BASE,
    'evidence_head_sha': EVIDENCE_HEAD,
    'authority_run': EVIDENCE_RUN,
    'authority_job': EVIDENCE_JOB,
    'same_head_normal_ci_run': NORMAL_CI_RUN,
    'same_head_normal_ci_job': NORMAL_CI_JOB,
    'artifact_id': ARTIFACT_ID,
    'artifact_sha256': ARTIFACT_DIGEST,
    'oracle_sha': ORACLE,
    'replay_identity': '47/47',
    'terminator_rows': 47,
    'continuation_rows': 47,
    'selected_rows': 94,
    'native_first_property_success': '94/94',
    'native_control_success': '94/94',
    'first_stop_equals_oracle_control_start': '94/94',
    'control_start_exact': '94/94',
    'control_boolean_exact': '94/94',
    'control_end_stop_exact': '94/94',
    'native_oracle_mismatch_count': 0,
    'aligned_truncation_rows': 6,
    'truncation_negative': 'PASS',
    'post_stop_poison': 'PASS',
    'repeatability': 'PASS',
    'malformed_first_rejected': 'PASS',
    'second_stream_bits_consumed': 0,
    'second_header_bits_consumed': 0,
    'second_payload_bits_consumed': 0,
    'privacy': 'PASS',
    'production_cargo_fixture_corpus_support_mutation': '0/0/0/0/0',
    'source_scope_sha256': '3af876d4fee21e6f769b8db908babb67ec061dcc9265ab266aa4a0ce89a6d42a',
    'replay_identity_sha256': 'b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf',
    'boxcars_instrumentation_sha256': 'cd52172333fd095377c15d263f1f178291eb3588a637cc34720a202bc1408667',
    'selected_witnesses_sha256': '3fbbece797c146e71dd5b569cce6882d5719ea2d39ecdd5198da351dc028e4c8',
    'selection_summary_sha256': '353d90d7385fcf34f4dca246d63949653f7124641cf7a81185e62b32e0bff1cf',
    'comparison_sha256': '9789a2fb6a5573a6bdacef2702c7cff169e764f244eb1736144b9b2c8258452d',
    'aggregate_sha256': '1b505299bc155aa32d9e48dd6d1d39327ac9025fa480472d2c67cc721270fabd',
    'next_pass': 'R3.18F',
}
reads = state.get('next_files_to_read', [])
for item in ['docs/continuity/MIMIR_R3_18E_DECISION.md', 'docs/continuity/MIMIR_R3_18F_EXECUTION_SPEC.md']:
    while item in reads:
        reads.remove(item)
anchor = 'docs/continuity/MIMIR_R3_18E_EXECUTION_SPEC.md'
if anchor not in reads:
    raise SystemExit('missing R3.18E spec reading anchor')
idx = reads.index(anchor) + 1
reads[idx:idx] = ['docs/continuity/MIMIR_R3_18E_DECISION.md', 'docs/continuity/MIMIR_R3_18F_EXECUTION_SPEC.md']
state['next_files_to_read'] = reads
p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# Current-state summary.
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.18D — minimal native existing-actor next-property control bit`
**Completed production differential:** `R3.18E — Outcome A / 94 real-replay rows / 94/94 exact / 0 mismatch / second stream+header+payload 0+0+0`
**Current exact pass:** `R3.18F — second-property-header real-replay evidence`

## 1. Truthful production boundary

Production remains R3.18D at `{PROD}`. After one already-valid R3.18B first K1 property, production may read exactly one next `property_present` bit and stop one bit later. R3.18E validated that exact production boundary against pinned Boxcars on 94 deterministic real-replay rows with zero mismatch. No production source changed during R3.18E.

```text
production SHA                       {PROD}
production tree                      {PROD_TREE}
lib.rs blob                          {LIB_BLOB}
R3.18D focused test blob             {R318D_TEST_BLOB}
R3.18E evidence head                 {EVIDENCE_HEAD}
R3.18E authority run/job             {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.18E same-head normal CI           {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
R3.18E artifact                      {ARTIFACT_ID}
R3.18E artifact SHA256               {ARTIFACT_DIGEST}
```

## 2. R3.18E admitted evidence

The exact 47-replay identity/oracle lane reproduced 47 terminator and 47 continuation rows. Published R3.18B first-property decoding and published R3.18D control decoding succeeded on 94/94 rows. First-property stop equaled the oracle control start on 94/94; control start, boolean and end/stop were exact on 94/94; mismatch count was zero. Truncation, post-stop poison, repeatability and malformed-first negatives passed. Second stream/header/payload consumption remained 0/0/0, privacy passed, and production/Cargo/fixture/corpus/support mutation remained 0/0/0/0/0.

## 3. R3.18F exact next pass

R3.18F is read-only second-property-header evidence. Reproduce the R3.18E witness classes. On each continuation row, require the R3.18D control bit to be true, then independently run the existing property-header primitive at that same `property_present` start and compare the second stream-ID range/value, resolved property object/tag, payload-start and stop against pinned Boxcars. Stop exactly at second-property payload start. On terminator rows, the header primitive must consume only the false property-present bit and expose no header/payload fields.

## 4. Still closed

```text
production second-property header composition
second-property payload decode / semantic value claim
third property or repeated/generalized property loop
K2/K3/K4 dispatch through the R3.18B wrapper
next actor / next frame iteration
actor lifecycle mutation
new attribute family/shape/context admission
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/fixture/corpus/support production expansion
```
'''
(ROOT / 'docs/continuity/MIMIR_CURRENT_STATE.md').write_text(current, encoding='utf-8', newline='\n')

# R3.18E decision.
decision = f'''# MIMIR R3.18E — Production Control-Bit Differential Decision

**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL COMPLETE**
**Production SHA (unchanged):** `{PROD}`
**Evidence authority head:** `{EVIDENCE_HEAD}`

## 1. Decision

R3.18E validates the published R3.18D one-bit after-first-K1-property control API against pinned Boxcars on the exact supported real-replay lane. All required deterministic witnesses matched exactly. This admits the evidence result only; it does not widen production into a second-property decoder or repeated property loop.

## 2. Exact receipts

```text
canonical continuity base             {CANONICAL_BASE}
production SHA/tree                   {PROD} / {PROD_TREE}
evidence authority head               {EVIDENCE_HEAD}
authority run/job                     {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
same-head normal CI                   {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
artifact                              {ARTIFACT_ID}
artifact SHA256                       {ARTIFACT_DIGEST}
pinned Boxcars                        {ORACLE}
```

## 3. Differential result

```text
replay identity / oracle parse        47/47
terminator rows                       47
continuation rows                     47
total selected rows                   94
native first-property success         94/94
native control success                94/94
first stop == oracle control start    94/94
control start exact                   94/94
control boolean exact                 94/94
control end/stop exact                94/94
native/oracle mismatch                0
aligned truncation rows               6
second stream/header/payload bits     0/0/0
privacy                               PASS
production/Cargo/fixture/corpus/
support mutation                      0/0/0/0/0
```

Observed K1 tag distribution across the 94 rows was Boolean=1, Byte=6, Float=41 and Int=46. Negative controls for exact truncation, post-stop poison, repeatability and malformed-first-property rejection all passed.

## 4. Immutable artifact file hashes

```text
source scope                          3af876d4fee21e6f769b8db908babb67ec061dcc9265ab266aa4a0ce89a6d42a
replay identity                       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation               cd52172333fd095377c15d263f1f178291eb3588a637cc34720a202bc1408667
selected witnesses                    3fbbece797c146e71dd5b569cce6882d5719ea2d39ecdd5198da351dc028e4c8
selection summary                     353d90d7385fcf34f4dca246d63949653f7124641cf7a81185e62b32e0bff1cf
comparison                            9789a2fb6a5573a6bdacef2702c7cff169e764f244eb1736144b9b2c8258452d
aggregate                             1b505299bc155aa32d9e48dd6d1d39327ac9025fa480472d2c67cc721270fabd
```

## 5. Still closed

R3.18E does not admit production second-property header composition, any second-property payload, a third property, a repeated/generalized property loop, K2/K3/K4 wrapper widening, actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill/runtime/export behavior, or dependency expansion.

## 6. Next pass

`R3.18F` is a separate read-only second-property-header real-replay evidence pass. It may observe only the second property header boundary through `payload_start` on the continuation lane and must not decode the payload.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18E_DECISION.md').write_text(decision, encoding='utf-8', newline='\n')

# R3.18F execution spec.
spec = f'''# MIMIR R3.18F — Second-Property-Header Real-Replay Evidence

**Status:** ACTIVE
**Pass type:** read-only boundary evidence
**Production mutation:** forbidden
**Second-property payload decode:** forbidden
**Third property / repeated loop:** forbidden

## 1. Goal

Establish whether the already-admitted property-header primitive matches pinned Boxcars at the second-property boundary exposed by R3.18D, without publishing a new production composition and without consuming the second payload.

## 2. Frozen authority

```text
canonical continuity base            {CANONICAL_BASE}
production SHA/tree                  {PROD} / {PROD_TREE}
production lib blob                  {LIB_BLOB}
R3.18D focused test blob             {R318D_TEST_BLOB}
R3.18E evidence head                 {EVIDENCE_HEAD}
R3.18E authority run/job             {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.18E same-head normal CI           {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
R3.18E artifact                      {ARTIFACT_ID}
R3.18E artifact SHA256               {ARTIFACT_DIGEST}
pinned Boxcars                       {ORACLE}
supported replay lane                47
frozen source witness classes        47 terminator + 47 continuation
```

Before evidence work, fetch fresh `main`, prove every commit after `{PROD}` is continuity-only, verify source/test blobs and the R3.18E receipts, and reconstruct the exact replay identity lane.

## 3. Witness policy

Reproduce the deterministic R3.18E witness classes without changing their replay identity or first-property/control coordinates.

- Positive second-header lane: exactly one continuation witness per replay when the frozen lane reproduces, target 47.
- Terminator negative lane: exactly one terminator witness per replay, target 47.
- If either class count drifts, stop and classify the drift before changing any target.

Record only privacy-safe relative replay identity/hash and structural bit/object/tag facts.

## 4. Native evidence path — continuation rows

For every continuation witness:

1. build the existing production lookup plan;
2. run the published R3.18B single-K1-property decoder at the frozen first-property start;
3. run the published R3.18D control API and require `next_property_present == true`;
4. require the R3.18D control start equals the oracle second `property_present` start;
5. independently invoke `decode_replay_network_existing_actor_first_property_header_v1` at that same second `property_present` start using the same actor object and lookup plan;
6. require `property_present == true`;
7. compare stream-ID start/end/value, resolved property object, resolved attribute tag, payload-start and stop exactly with pinned Boxcars;
8. stop at `payload_start`. Do not decode or interpret any second-property payload bit.

The existing function name contains `first_property`; R3.18F uses it only as a stateless header primitive at an explicit bit start for evidence. This pass does not redefine its production role or publish a repeated loop.

## 5. Terminator negative lane

For every terminator witness, invoke the same header primitive at the false control-bit start and require:

```text
property_present == false
property_present_end == R3.18D control end
stop_bit == property_present_end
stream-id fields == None
resolved object/tag == None
payload_start == None
```

No lookup-derived or payload boundary may appear after a false terminator.

## 6. Required aggregate gates

```text
replay identity / oracle parse          47/47
R3.18E witness reconstruction           94/94
continuation rows                       47
terminator rows                         47
continuation header native success      47/47
second property_present exact           47/47
second stream start/end/value exact     47/47
resolved property object exact          47/47
resolved attribute tag exact            47/47
second payload_start/stop exact         47/47
terminator one-bit stop exact           47/47
terminator optional header fields None  47/47
native/oracle mismatch                  0
second payload bits consumed            0
third-property bits consumed            0
privacy                                 PASS
production/Cargo/fixture/corpus/
support mutation                        0/0/0/0/0
```

## 7. Negative controls

At minimum prove:

- truncate within the required second stream-ID/header bits for a deterministic continuation witness: fail closed;
- mutate bits strictly after the second-header stop/payload-start: header result unchanged;
- repeat the same continuation header observation: exact;
- mutate an otherwise-resolved second stream ID to an unresolved value in an isolated synthetic copy: fail closed;
- terminator rows never attempt stream/header resolution after the false bit.

No negative may decode the second payload.

## 8. Evidence artifact

Emit an immutable privacy-safe artifact containing source/production/R3.18E receipts, replay identity manifest, pinned Boxcars instrumentation receipt, reproduced source witnesses, continuation second-header rows, terminator negatives, aggregate summary, negative controls and file hashes. Record artifact ID and digest.

## 9. Outcome gate

### Outcome A

All frozen continuation second-header boundaries match exactly, all terminator negatives stop after one bit, mismatch is zero, and second-payload/third-property consumption remains zero. Close R3.18F. Only then may a separate contract/production admission pass be defined.

### Outcome B

A bounded native/oracle discrepancy exists. Record the exact stream/header class and keep production second-property admission closed.

### Outcome C

Authority drift, corpus drift, privacy failure, production mutation, scope widening, second-payload consumption, or any third-property/repeated-loop observation. Stop without admission.

## 10. Hard stop

R3.18F does not publish a second-property decoder, decode a second payload, observe a third property, generalize a property loop, widen K2/K3/K4 wrapper composition, iterate actors/frames, mutate lifecycle state, extract raw-state/events, slice replays, or widen skill/runtime/export/dependency behavior.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18F_EXECUTION_SPEC.md').write_text(spec, encoding='utf-8', newline='\n')

# Knowledge graph.
p = ROOT / 'MIMIR_KNOWLEDGE_GRAPH.md'
g = p.read_text(encoding='utf-8')
g = regex_one(
    g,
    r'^R3\.18E active control-bit differential audit spec\s+\|$',
    'R3.18E control-bit differential decision                              |\nR3.18F active second-property-header evidence spec                       |',
    'graph latest nodes',
)

# Rebuild mandatory reading order while preserving every existing entry.
section_start = g.index('## Mandatory reading order\n')
section_end = g.index('\n## Current replay-decoder chain', section_start)
section = g[section_start:section_end]
entries = []
for line in section.splitlines():
    m = re.match(r'^\d+\. `([^`]+)`$', line)
    if m:
        entries.append(m.group(1))
for item in ['docs/continuity/MIMIR_R3_18E_DECISION.md', 'docs/continuity/MIMIR_R3_18F_EXECUTION_SPEC.md']:
    while item in entries:
        entries.remove(item)
anchor = 'docs/continuity/MIMIR_R3_18E_EXECUTION_SPEC.md'
if anchor not in entries:
    raise SystemExit('knowledge graph missing R3.18E spec anchor')
idx = entries.index(anchor) + 1
entries[idx:idx] = ['docs/continuity/MIMIR_R3_18E_DECISION.md', 'docs/continuity/MIMIR_R3_18F_EXECUTION_SPEC.md']
new_section = '## Mandatory reading order\n\n' + '\n'.join(f'{i}. `{item}`' for i, item in enumerate(entries, 1)) + '\n'
g = g[:section_start] + new_section + g[section_end:]

old_chain = ''' -> R3.18E production control-bit real-replay differential audit: ACTIVE / READ-ONLY
      reproduce the frozen 94 R3.18C terminator+continuation rows and compare published R3.18D start/value/end exactly; production mutation and second property remain forbidden'''
new_chain = f''' -> R3.18E production control-bit real-replay differential audit: OUTCOME A / CLOSED
      authority {EVIDENCE_HEAD} / {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
      exact-head CI {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
      artifact {ARTIFACT_ID} / sha256:{ARTIFACT_DIGEST}
      47/47 replay identity + 47 terminator + 47 continuation / 94/94 first-property+control exact / mismatch 0 / second stream+header+payload 0+0+0
 -> R3.18F second-property-header real-replay evidence: ACTIVE / READ-ONLY
      reproduce the same 47 continuation + 47 terminator classes; compare second header through payload_start only; second payload and third property remain forbidden'''
g = replace_one(g, old_chain, new_chain, 'graph replay chain')
g = replace_one(
    g,
    'R3.18E is read-only differential validation of this exact production boundary against pinned Boxcars on the real-replay lane.',
    'R3.18E closed Outcome A with 94/94 exact real-replay control rows and zero second-property consumption. R3.18F is read-only evidence for only the second-property header boundary through payload_start; production second-property composition remains closed.',
    'graph capability lock current audit',
)
g = replace_one(
    g,
    'R3.18D may publish only that one control bit; second property decoding, repeated property loops, K2/K3/K4 wrapper composition, next actor/frame iteration and lifecycle mutation remain closed.',
    'R3.18D publishes only that one control bit; R3.18E validated it with zero mismatch. R3.18F may observe only a second-property header boundary read-only; production second-property composition/payload, repeated loops, K2/K3/K4 wrapper composition, next actor/frame iteration and lifecycle mutation remain closed.',
    'graph historical tail',
)
p.write_text(g, encoding='utf-8', newline='\n')

print('R3_18E_CONTINUITY_GENERATOR=PASS')
