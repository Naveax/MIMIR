from pathlib import Path
import json
import re

ROOT = Path('.')
BASE_MAIN = '4adadd185783954c7fb6ad67db14b77b377cdde5'
BASE_TREE = '67b1969eaff49d2913b88b3921f27b1bd7fe8193'
PREVIOUS_MAIN = 'e9f3c4d34ebd84fc9c51431ad4489c4d407b1535'
LIB_BLOB = '42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662'
TEST_BLOB = '2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b'
IMPLEMENTATION_RUN = 31945358707
IMPLEMENTATION_JOB = 95160386174
EXACT_RUN = 31947511554
EXACT_JOB = 95165765329
MAIN_CI_RUN = 31947695046
MAIN_CI_JOB = 95166220676
PUBLISHED_RUN = 31947722626
PUBLISHED_JOB = 95166287502


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


# Master handbook
p = ROOT / 'MIMIR_CONTINUE_HERE.md'
s = p.read_text(encoding='utf-8')
s = regex_one(s, r'^LAST_PRODUCTION_CODE_SHA:\n  .+$', f'LAST_PRODUCTION_CODE_SHA:\n  {BASE_MAIN}', 'last production sha')
s = regex_one(s, r'^LAST_PRODUCTION_MILESTONE:\n  .+$', 'LAST_PRODUCTION_MILESTONE:\n  R3.18D — minimal native existing-actor next-property control bit', 'last production milestone')
s = regex_one(s, r'^LAST_COMPLETED_READ_ONLY_AUDIT:\n  .+$', 'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18C — property-loop terminator/continuation evidence / Outcome A / exact one-bit boundary / 0 mismatch', 'last read only audit')
s = regex_one(s, r'^CURRENT_PASS:\n  .+$', 'CURRENT_PASS:\n  R3.18E — production control-bit real-replay differential audit', 'current pass')
s = regex_one(s, r'^CURRENT_PASS_TYPE:\n  .+$', 'CURRENT_PASS_TYPE:\n  read-only differential audit / compare the published R3.18D one-bit control result against pinned Boxcars on the exact real-replay witness lane', 'current pass type')

hard_stop = f'''CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload OR one R3.17J-admitted K3 payload OR one R3.17N-admitted K4 payload may be decoded natively
  K3 remains limited to its exact R3.17J structural/context allowlist; K4 remains limited to the exact 161 R3.17N tuples
  R3.18B composes exactly one existing-actor K1 property through its payload end
  R3.18D is published production at {BASE_MAIN} and, only from an already-valid R3.18B first-property result, reads exactly the next property_present bit and stops one bit later
  R3.18E is read-only differential evidence only: compare that published one-bit result with pinned Boxcars on real witnesses; production mutation remains forbidden
  NO second property stream/header/payload, repeated/generalized property loop, K2/K3/K4 wrapper composition, next actor, next frame, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening is admitted'''
s = regex_one(s, r'(?ms)^CURRENT_PRODUCTION_HARD_STOP:\n.*?(?=\nR3_17E_EVIDENCE_CLOSURE:)', hard_stop, 'production hard stop', flags=re.MULTILINE | re.DOTALL)

closure = f'''R3_18D_PRODUCTION_CLOSURE:
  Outcome A / production / exact one-bit after-first-K1-property control only
  previous canonical main: {PREVIOUS_MAIN}
  production SHA/tree: {BASE_MAIN} / {BASE_TREE}
  lib.rs blob: {LIB_BLOB}
  focused R3.18D test blob: {TEST_BLOB}
  implementation run/job: {IMPLEMENTATION_RUN} / {IMPLEMENTATION_JOB} SUCCESS
  exact clean-candidate validator: {EXACT_RUN} / {EXACT_JOB} SUCCESS
  published main normal CI: {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
  exact published-main validator: {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
  exact clean scope: crates/mimir-replay/src/lib.rs + crates/mimir-replay/tests/r3_18d_next_property_control.rs
  source audit: exactly one NetworkBitCursor::read_bit; no read_bits_le/bounded/property-header/scalar/K2/K3/K4 call and no production while/for loop in the new control function
  positive boundary: false terminator + true continuation; aligned + unaligned ends; R3.18C Float terminator + Int=62 continuation shapes
  negatives/invariants: missing next bit fail-closed; malformed first-property boundary rejected; post-control poison has no effect; repeatability exact
  full mimir-replay, workspace check/test/clippy and full repository verifier: PASS
  Cargo/fixture/corpus/support/workflow/continuity changes in clean production commit: 0/0/0/0/0/0
  second property stream/header/payload consumed by the new API: 0/0/0

R3_18E_OPEN_BOUNDARY:
  read-only production differential audit; production Rust mutation forbidden
  exact production under audit: {BASE_MAIN}
  replay lane: the exact 47 supported replays with the same identity policy used by R3.18C
  pinned oracle: nickbabcock/boxcars@c70e77df7af81b436cb545d070bb90c82f562d0b
  reconstruct the deterministic R3.18C loop-control witness policy: at most one terminator and one continuation witness per replay, yielding the frozen 94-row target when both classes remain present
  for every selected row, run the published R3.18B first-property production decoder and then the published R3.18D control-bit API
  compare first-property stop == oracle next property_present start, control start, boolean value, one-bit end/stop, replay identity and witness context
  require zero native/oracle mismatch and zero second-stream/header/payload bits consumed
  include fail-closed truncation and post-stop poison/repeatability negatives without decoding the second property

R3_18E_HARD_STOP:
  no production source, Cargo, fixture, corpus or support-lane mutation
  no second property stream id, header/tag resolution or payload decode
  no repeated property loop / control-bit chaining in production or audit semantics
  no new K2/K3/K4 composition through the R3.18B wrapper
  no next actor, next frame, lifecycle mutation, raw state, event, replay slice, skill, runtime or export widening

NEXT PASS AFTER R3.18E:
  only after Outcome A and exact production differential parity may a separately scoped read-only second-property-header evidence pass be considered; R3.18E itself does not admit that header or a repeated loop
'''
s = regex_one(
    s,
    r'(?ms)^R3_18D_OPEN_BOUNDARY:\n.*?^NEXT PASS AFTER R3\.18D:\n  .+$',
    closure.rstrip(),
    'R3.18D closure block',
    flags=re.MULTILINE | re.DOTALL,
)
p.write_text(s, encoding='utf-8', newline='\n')

# Machine-readable state
p = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(p.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-16'
state['last_production_code_sha'] = BASE_MAIN
state['last_production_milestone'] = 'R3.18D'
state['last_production_milestone_name'] = 'minimal native existing-actor next-property control bit'
state['last_completed_read_only_audit'] = 'R3.18C'
state['last_completed_evidence_pass'] = 'R3.18C'
state['current_pass'] = 'R3.18E'
state['current_pass_kind'] = 'read-only production differential audit / published R3.18D one-bit control result versus pinned Boxcars'
state['current_pass_goal'] = 'Differentially validate the published R3.18D after-first-K1-property one-bit control result on the deterministic real-replay terminator/continuation witness lane with exact start/value/end parity and zero second-property consumption.'
state['current_pass_stop_boundary'] = 'Read only the already-proven next property_present control bit through production R3.18D and compare it with the pinned oracle. No second stream/header/payload, repeated property loop, production mutation, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening.'
state['closed_now'] = [
    'second property stream/header/payload consumption',
    'repeated or generalized production property_present loop beyond the published single control bit',
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
state['r3_18d'] = {
    'outcome': 'A — admitted / production complete',
    'pass_type': 'minimal native existing-actor next-property control bit',
    'previous_main_sha': PREVIOUS_MAIN,
    'production_sha': BASE_MAIN,
    'production_tree': BASE_TREE,
    'lib_blob': LIB_BLOB,
    'focused_test_blob': TEST_BLOB,
    'implementation_run': IMPLEMENTATION_RUN,
    'implementation_job': IMPLEMENTATION_JOB,
    'exact_candidate_validation_run': EXACT_RUN,
    'exact_candidate_validation_job': EXACT_JOB,
    'published_main_ci_run': MAIN_CI_RUN,
    'published_main_ci_job': MAIN_CI_JOB,
    'published_main_validation_run': PUBLISHED_RUN,
    'published_main_validation_job': PUBLISHED_JOB,
    'clean_files': [
        'crates/mimir-replay/src/lib.rs',
        'crates/mimir-replay/tests/r3_18d_next_property_control.rs',
    ],
    'control_bits_read': 1,
    'second_stream_bits_consumed': 0,
    'second_header_bits_consumed': 0,
    'second_payload_bits_consumed': 0,
    'source_audit': 'PASS / one read_bit / zero generic loop or second-property decoder calls',
    'focused_tests': 'PASS',
    'full_mimir_replay': 'PASS',
    'workspace_check_test_clippy': 'PASS',
    'full_repository_verifier': 'PASS',
    'cargo_fixture_corpus_support_workflow_continuity_mutation': '0/0/0/0/0/0',
    'next_pass': 'R3.18E',
}
reads = state.get('next_files_to_read', [])
for item in [
    'docs/continuity/MIMIR_R3_18D_DECISION.md',
    'docs/continuity/MIMIR_R3_18E_EXECUTION_SPEC.md',
]:
    while item in reads:
        reads.remove(item)
anchor = 'docs/continuity/MIMIR_R3_18D_EXECUTION_SPEC.md'
if anchor not in reads:
    raise SystemExit('missing R3.18D spec reading anchor')
idx = reads.index(anchor) + 1
reads[idx:idx] = [
    'docs/continuity/MIMIR_R3_18D_DECISION.md',
    'docs/continuity/MIMIR_R3_18E_EXECUTION_SPEC.md',
]
state['next_files_to_read'] = reads
p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# Current state summary
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{BASE_MAIN}`
**Production milestone:** `R3.18D — minimal native existing-actor next-property control bit`
**Completed loop-control evidence:** `R3.18C — Outcome A / 47 terminator + 47 continuation candidates / exact next bit / 0 mismatch`
**Current exact pass:** `R3.18E — production control-bit real-replay differential audit`

## 1. Truthful production boundary

R3.18D is production. Given one already-valid R3.18B first K1 property result, production may validate that result's boundary invariants, read exactly the next `property_present` bit at `first_property.stop_bit`, and return the one-bit start/end/stop plus the boolean continuation value. The new API stops immediately after that bit. It does not decode a second stream ID, property header/tag, or payload, and it is not a generalized repeatable property-loop cursor.

```text
previous canonical main              {PREVIOUS_MAIN}
production SHA                       {BASE_MAIN}
production tree                      {BASE_TREE}
lib.rs blob                          {LIB_BLOB}
R3.18D focused test blob             {TEST_BLOB}
implementation run/job               {IMPLEMENTATION_RUN} / {IMPLEMENTATION_JOB} SUCCESS
exact candidate validator            {EXACT_RUN} / {EXACT_JOB} SUCCESS
published main CI                    {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
published-main validator             {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
```

## 2. R3.18D admitted behavior

The production control function is structurally tied to `ReplayNetworkExistingActorSinglePrimitivePropertyV1`. It requires the first property/header/scalar boundaries to agree, checks the one-bit end with checked arithmetic, uses the existing private LSB-first `NetworkBitCursor`, performs exactly one `read_bit()`, and returns `next_property_present`, `property_present_start_bit`, `property_present_end_bit`, and `stop_bit`.

Independent source audit proved zero `read_bits_le`, bounded stream, property-header, scalar, K2/K3/K4 decoder or production `while`/`for` calls inside the new control function. Focused tests cover false terminator, true continuation, aligned and unaligned ends, the R3.18C Float and Int=62 shapes, post-stop poison, missing-next-bit failure, malformed first-property rejection and repeatability.

## 3. R3.18E exact next pass

R3.18E is read-only. Reconstruct the deterministic R3.18C real-replay loop-control witness policy on the exact 47 supported replay lane, target the frozen 94 terminator/continuation rows when reproduced, and run the published R3.18B first-property decoder followed by the published R3.18D one-bit control API. Compare the native first-property stop, control start, boolean value and one-bit end/stop with pinned Boxcars. Require zero mismatch and zero second stream/header/payload bits consumed.

## 4. Still closed

```text
second property stream/header/payload
repeated/generalized property_present loop
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

# R3.18D decision
decision = f'''# MIMIR R3.18D — Production Decision

**Outcome:** **A — ADMITTED / PRODUCTION COMPLETE**
**Production SHA:** `{BASE_MAIN}`
**Production tree:** `{BASE_TREE}`
**Previous canonical main:** `{PREVIOUS_MAIN}`

## 1. Decision

R3.18D publishes the smallest production capability justified by R3.18C. After one already-valid R3.18B first K1 property result, MIMIR may read exactly the next `property_present` bit at the first property's stop bit and stop one bit later.

This is a control observation, not a second-property decoder and not a generalized property loop.

## 2. Published API boundary

Production now exposes an after-first-primitive-property control result containing:

```text
next_property_present
property_present_start_bit
property_present_end_bit
stop_bit
```

The implementation validates the R3.18B first-property boundary, requires header/scalar/end invariants to agree, reads exactly one bit with the existing private LSB-first cursor, and requires `stop_bit == property_present_end_bit == property_present_start_bit + 1`.

## 3. Exact production identity

```text
production SHA                     {BASE_MAIN}
production tree                    {BASE_TREE}
lib.rs blob                        {LIB_BLOB}
focused test blob                  {TEST_BLOB}
clean production files             2
Cargo/fixture/corpus/support/
workflow/continuity mutation       0/0/0/0/0/0
```

## 4. Validation receipts

```text
implementation                     {IMPLEMENTATION_RUN} / {IMPLEMENTATION_JOB} SUCCESS
exact clean-candidate validator    {EXACT_RUN} / {EXACT_JOB} SUCCESS
published main normal CI           {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
published-main validator           {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
```

All required focused R3.18D tests, full `mimir-replay`, workspace check/test/clippy and full repository verifier passed.

## 5. Source boundary audit

The new control function contains exactly one `NetworkBitCursor::read_bit()` and no `read_bits_le`, bounded stream decoder, first-property-header decoder, single-property decoder, primitive scalar decoder, K2/K3/K4 decoder, or production `while`/`for` loop call.

Therefore the admitted consumption is exactly one next control bit. Second stream/header/payload consumption is `0/0/0`.

## 6. Still closed

- second property stream ID;
- second property header/tag resolution;
- second property payload;
- repeated/generalized property loop;
- K2/K3/K4 composition through the R3.18B wrapper;
- next actor/frame iteration;
- lifecycle/raw-state/event/replay-slice/skill/runtime/export widening.

## 7. Next pass

`R3.18E` is a separate read-only real-replay differential audit of the published one-bit control result. It must prove exact native/oracle start/value/end parity before any second-property header evidence is considered.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18D_DECISION.md').write_text(decision, encoding='utf-8', newline='\n')

# R3.18E spec
spec = f'''# MIMIR R3.18E — Production Control-Bit Real-Replay Differential Audit

**Status:** ACTIVE
**Pass type:** read-only differential audit
**Production mutation:** forbidden
**Second property decode:** forbidden
**Repeated property loop:** forbidden

## 1. Goal

Differentially validate the published R3.18D after-first-K1-property one-bit control result against pinned Boxcars on real replay witnesses. The pass may observe only the next `property_present` bit after one production-decoded R3.18B first property and must stop at the one-bit end.

## 2. Frozen production authority

```text
production SHA/tree                 {BASE_MAIN} / {BASE_TREE}
production lib blob                 {LIB_BLOB}
R3.18D focused test blob            {TEST_BLOB}
implementation run/job              {IMPLEMENTATION_RUN} / {IMPLEMENTATION_JOB} SUCCESS
exact candidate validator           {EXACT_RUN} / {EXACT_JOB} SUCCESS
published main CI                   {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
published-main validator            {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane               47
R3.18C target classes               terminator + continuation
R3.18C frozen target rows           94 = 47 + 47
```

Before evidence work, fetch fresh `main`, verify the production SHA/tree/source/test blobs, and prove that any newer commits are continuity-only.

## 3. Oracle/witness policy

Use the same exact 47-replay identity lane and pinned Boxcars policy as R3.18C. Reconstruct deterministically, per replay, at most one eligible terminator witness and one eligible continuation witness after an R3.18B-compatible K1 first property. The expected reproduced target is 94 rows if the frozen corpus remains identical.

For every selected row record privacy-safe structural facts only: replay identity hash/path-relative identifier, frame/actor/property ordinals, actor context object, stream ID/bound, property object/tag, first-property payload start/end, oracle next-bit start/value/end, and the production result.

## 4. Native differential path

For each witness:

1. build the production lookup plan using existing admitted code;
2. run `decode_replay_network_existing_actor_single_primitive_property_v1` at the exact first-property start;
3. require its stop equals the oracle next `property_present` start;
4. run `decode_replay_network_existing_actor_after_first_primitive_property_control_v1`;
5. compare control start, boolean value, end and stop exactly;
6. stop. Do not read a second stream/header/payload bit.

## 5. Required aggregate gates

```text
replay identity / oracle parse      47/47
terminator target rows              47
continuation target rows            47
total selected rows                 94
native first-property success       94/94
native control success              94/94
first stop == oracle next start     94/94
control start exact                 94/94
control boolean exact               94/94
control end/stop exact              94/94
native/oracle mismatch              0
second stream/header/payload bits   0/0/0
privacy                             PASS
production/Cargo/fixture/corpus/
support mutation                    0/0/0/0/0
```

If deterministic reconstruction of the frozen 94 rows differs, stop and classify the drift before changing the target.

## 6. Negative controls

At minimum prove:

- truncate exactly before the next control bit: fail closed;
- mutate bits strictly after the one-bit stop: result unchanged;
- repeat the same selected witness: result exact;
- malformed first-property boundary: reject before the control read.

No negative may be used as a pretext to decode a second property.

## 7. Evidence artifact

Emit an immutable privacy-safe artifact containing source/production authority receipts, replay identity manifest, pinned Boxcars instrumentation receipt, selected witnesses, native/oracle comparison rows, aggregate summary, negatives and file hashes. Record the GitHub artifact ID and digest.

## 8. Validation

Required:

- exact authority-head workflow SUCCESS;
- same-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation zero;
- privacy scan PASS;
- exact 94-row aggregate gates above;
- full repository verifier PASS where the evidence workflow uses repository code.

## 9. Outcome gate

### Outcome A

All 94 reproduced real-replay rows match the published R3.18D result exactly with zero mismatch and zero second-property consumption. Close R3.18E and only then define a separate read-only second-property-header evidence pass.

### Outcome B

A bounded production/oracle discrepancy exists. Record the exact class and keep second-property admission closed.

### Outcome C

Authority drift, corpus drift, privacy failure, production mutation, scope widening, or any second-property consumption. Stop without admission.

## 10. Hard stop

R3.18E does not admit second-property stream/header/payload decoding, repeated property loops, K2/K3/K4 wrapper widening, actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill/runtime/export behavior, or production dependency changes.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18E_EXECUTION_SPEC.md').write_text(spec, encoding='utf-8', newline='\n')

# Knowledge graph
p = ROOT / 'MIMIR_KNOWLEDGE_GRAPH.md'
g = p.read_text(encoding='utf-8')
g = replace_one(
    g,
    'R3.18D active next-property control-bit production spec            |',
    'R3.18D next-property control-bit production decision               |\nR3.18E active control-bit differential audit spec                       |',
    'graph latest nodes',
)

section_start = g.index('## Mandatory reading order\n')
section_end = g.index('\n## Current replay-decoder chain', section_start)
prefix = g[:section_start]
section = g[section_start:section_end]
suffix = g[section_end:]
lines = section.splitlines()
entries = []
for line in lines:
    m = re.match(r'^\d+\. `([^`]+)`$', line)
    if m:
        entries.append(m.group(1))
for item in ['docs/continuity/MIMIR_R3_18D_DECISION.md', 'docs/continuity/MIMIR_R3_18E_EXECUTION_SPEC.md']:
    if item in entries:
        entries.remove(item)
anchor = 'docs/continuity/MIMIR_R3_18D_EXECUTION_SPEC.md'
if anchor not in entries:
    raise SystemExit('knowledge graph missing R3.18D spec anchor')
idx = entries.index(anchor) + 1
entries[idx:idx] = ['docs/continuity/MIMIR_R3_18D_DECISION.md', 'docs/continuity/MIMIR_R3_18E_EXECUTION_SPEC.md']
new_section = '## Mandatory reading order\n\n' + '\n'.join(f'{i}. `{item}`' for i, item in enumerate(entries, 1)) + '\n'
g = prefix + new_section + suffix

old_chain = ''' -> R3.18D minimal native existing-actor next-property control bit: ACTIVE / PRODUCTION
      read exactly one next property_present bit after a valid R3.18B first K1 property; stop immediately after it; no second stream/header/payload and no repeated loop
'''
new_chain = f''' -> R3.18D minimal native existing-actor next-property control bit: PRODUCTION / CLOSED
      production {BASE_MAIN} / tree {BASE_TREE}
      lib/test blobs {LIB_BLOB} / {TEST_BLOB}
      implementation {IMPLEMENTATION_RUN} / {IMPLEMENTATION_JOB} SUCCESS
      exact candidate {EXACT_RUN} / {EXACT_JOB} SUCCESS
      published main CI {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
      published validator {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
      exactly one next property_present bit / second stream+header+payload bits 0+0+0 / no repeated loop
 -> R3.18E production control-bit real-replay differential audit: ACTIVE / READ-ONLY
      reproduce the frozen 94 R3.18C terminator+continuation rows and compare published R3.18D start/value/end exactly; production mutation and second property remain forbidden
'''
g = replace_one(g, old_chain, new_chain, 'replay decoder latest chain')

cap_start = g.index('## Current capability lock\n')
cap_body = cap_start + len('## Current capability lock\n')
next_para = g.index('\nR3.17H closed Outcome A', cap_body)
cap = f'''\nProduction at `{BASE_MAIN}` includes R3.18B's one-property K1 wrapper plus R3.18D's structurally tied after-first-property control reader. After one valid R3.18B first K1 property, production may read exactly one next `property_present` bit and stop one bit later. It still cannot decode the second stream ID, second property header/tag, or second payload, and it does not expose a generalized repeated property loop. R3.18E is read-only differential validation of this exact production boundary against pinned Boxcars on the real-replay lane.\n'''
g = g[:cap_body] + cap + g[next_para:]
p.write_text(g, encoding='utf-8', newline='\n')

print('R3_18D_CONTINUITY_GENERATOR=PASS')
