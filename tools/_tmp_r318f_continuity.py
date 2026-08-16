from pathlib import Path
import json
import re

ROOT = Path('.')
CANONICAL_BASE = '3a10ee59ba42722b59ca6c5b816205f6e5d603ea'
CANONICAL_TREE = 'ff8049a18431977e054652a0836217fcc39d84a7'
PROD = '4adadd185783954c7fb6ad67db14b77b377cdde5'
PROD_TREE = '67b1969eaff49d2913b88b3921f27b1bd7fe8193'
LIB_BLOB = '42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662'
R318B_TEST_BLOB = '927e9a2c834115d1c918fa96fb6d0690bd03965e'
R318D_TEST_BLOB = '2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b'
R318F_SPEC_BLOB = 'e6b92ea5628f107112a088421f318cd45a384e87'
EVIDENCE_HEAD = '27a855a9cfb82a0294dd1601e4da01c9fdfad264'
EVIDENCE_TREE = '4058b67d72219cbbf0534c6002049202fab487f3'
EVIDENCE_RUN = 31951039411
EVIDENCE_JOB = 95174417526
NORMAL_CI_RUN = 31951039378
NORMAL_CI_JOB = 95174417478
ARTIFACT_ID = 9266197133
ARTIFACT_DIGEST = '641a62c1467d7bc56d6b3fd1c9377276a6eec0ab02666c062623afa3955114f3'
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
s = regex_one(s, r'^LAST_COMPLETED_READ_ONLY_AUDIT:\n  .+$', 'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18F — second-property-header real-replay evidence / Outcome A / 47 continuation headers exact + 47 terminator negatives / 0 mismatch', 'last read-only audit')
s = regex_one(s, r'^LAST_COMPLETED_EVIDENCE_PASS:\n  .+$', 'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18F — second-property-header real-replay evidence / Outcome A / 47/47 continuation headers / 47/47 terminators / 0 mismatch / second payload + third property 0 + 0', 'last evidence pass')
s = regex_one(s, r'^CURRENT_PASS:\n  .+$', 'CURRENT_PASS:\n  R3.18G — minimal native existing-actor second-property-header composition', 'current pass')
s = regex_one(s, r'^CURRENT_PASS_TYPE:\n  .+$', 'CURRENT_PASS_TYPE:\n  production implementation / bounded optional second-property header after one valid R3.18B first primitive property; stop at second payload_start', 'current pass type')

hard_stop = f'''CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload OR one R3.17J-admitted K3 payload OR one R3.17N-admitted K4 payload may be decoded natively
  K3 remains limited to its exact R3.17J structural/context allowlist; K4 remains limited to the exact 161 R3.17N tuples
  R3.18B composes exactly one existing-actor K1 property through its payload end
  R3.18D is production at {PROD} and, only from an already-valid R3.18B first-property result, reads exactly the next property_present bit and stops one bit later
  R3.18E closed Outcome A: 94/94 real-replay terminator/continuation control rows matched pinned Boxcars exactly
  R3.18F closed Outcome A: all 47 continuation second headers matched through payload_start, all 47 terminators stopped after one bit, mismatch 0, second payload and third-property consumption 0/0
  R3.18G may publish only one bounded optional second-property header after a valid first primitive property and R3.18D control; continuation tag admission is limited to Byte/Enum/Float/Int/Int64 as actually observed in R3.18F
  NO second-property payload decode, third property, repeated/generalized property loop, K2/K3/K4 wrapper composition, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted'''
s = regex_one(s, r'(?ms)^CURRENT_PRODUCTION_HARD_STOP:\n.*?(?=\nR3_17E_EVIDENCE_CLOSURE:)', hard_stop, 'production hard stop', flags=re.MULTILINE | re.DOTALL)

closure = f'''R3_18F_EVIDENCE_CLOSURE:
  Outcome A / read-only second-property-header evidence / production Rust unchanged at {PROD}
  canonical continuity base: {CANONICAL_BASE}
  evidence authority head/tree: {EVIDENCE_HEAD} / {EVIDENCE_TREE}
  authority run/job: {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
  exact-head normal CI: {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
  artifact: {ARTIFACT_ID}
  artifact digest: sha256:{ARTIFACT_DIGEST}
  pinned oracle: nickbabcock/boxcars@{ORACLE}
  replay identity/oracle parse: 47/47
  R3.18E witness reconstruction: 94/94 = 47 terminator + 47 continuation
  continuation second-header native success: 47/47
  second property_present exact: 47/47 continuation + 47/47 terminator false
  second stream start/end/value exact: 47/47
  second stream shape bound/prop-bits exact: 47/47
  resolved second property object exact: 47/47
  resolved second attribute tag exact: 47/47
  second payload_start/stop exact: 47/47
  terminator one-bit stop + optional header fields None: 47/47 + 47/47
  continuation tag rows: Byte=12 / Enum=1 / Float=4 / Int=28 / Int64=2
  real second-header truncation negatives: 26
  unresolved-stream synthetic / terminator-no-lookup synthetic / post-stop poison / repeatability: PASS
  native/oracle mismatch: 0
  second payload bits consumed: 0
  third-property bits consumed: 0
  privacy: PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0
  source scope SHA256: a6e14057249bccc3643f519774731cb5d03ed1aad6e7337009715601b95d3a7e
  replay identity SHA256: b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
  Boxcars instrumentation receipt SHA256: 79c80c104556e8338a7f3fb943194149743650996c988a2a9136ef5cfa7567b6
  selected witnesses SHA256: 92c83039872436f3165bcb32b8b6914f6aefdbd0aa03b030235a8c4979ee3301
  selection summary SHA256: e19384c00d4ec6650b8781319c3133709375715317406b5745222941423824d7
  comparison SHA256: f4b05f9fe6ca6e081fbffaba431efefc20e14a9e99b9dc5f654016842dec0de5
  aggregate SHA256: 9919aa8bfb5e70a48344442bb40c0de7c89ea41f92bc532afa5343b3c469a9b9

R3_18G_OPEN_BOUNDARY:
  production implementation pass justified only by R3.18F Outcome A
  production authority before pass remains {PROD}; canonical docs may be newer
  publish one explicitly named after-first-primitive / second-property-header composition only
  input should be network bytes + already-valid R3.18B first-property result + lookup plan; derive actor object from the first-property header rather than expose a generic chain cursor
  internally compose the existing R3.18D control result with the existing property-header primitive
  terminator path: control=false -> second_header=None and stop exactly at control end; no lookup/header/payload read beyond the false bit
  continuation path: control=true -> independently decode the second header at that exact property_present start, require the header-present coordinates to agree with the control result, resolve stream/object/tag, and stop exactly at second payload_start
  continuation tag admission is limited to the exact R3.18F observed set: Byte, Enum, Float, Int, Int64
  Boolean and all compound/non-observed second-header tags fail closed in this new composition even if some lower-level primitive can represent them
  second payload bytes/bits remain opaque and unconsumed

R3_18G_HARD_STOP:
  no second-property payload decode or semantic value claim
  no third property control/header observation and no repeated/generalized property loop
  no generic repeatedly-chainable public property cursor
  no K2/K3/K4 composition through the R3.18B wrapper
  no new tag/shape/context admission beyond Byte/Enum/Float/Int/Int64 for this second-header API
  no next actor, next frame, lifecycle mutation, raw state, event, replay slice, skill, runtime or export widening
  no Cargo/fixture/corpus/support/dependency widening

NEXT PASS AFTER R3.18G:
  only after a clean production publication + exact published-main validation may a separate real-replay differential audit validate the production second-header composition before any second-property payload admission
'''
s = regex_one(
    s,
    r'(?ms)^R3_18F_OPEN_BOUNDARY:\n.*?^NEXT PASS AFTER R3\.18F:\n  [^\n]+$',
    closure.rstrip(),
    'R3.18F closure block',
    flags=re.MULTILINE | re.DOTALL,
)
p.write_text(s, encoding='utf-8', newline='\n')

# Machine-readable state.
p = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(p.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-16'
state['last_production_code_sha'] = PROD
state['last_production_milestone'] = 'R3.18D'
state['last_production_milestone_name'] = 'minimal native existing-actor next-property control bit'
state['last_completed_read_only_audit'] = 'R3.18F'
state['last_completed_evidence_pass'] = 'R3.18F'
state['last_completed_evidence_outcome'] = 'A — 47/47 continuation second headers exact; 47/47 terminators one-bit/no-optionals; 26 real truncation negatives; mismatch 0; second payload/third-property bits 0/0'
state['current_pass'] = 'R3.18G'
state['current_pass_kind'] = 'production implementation / bounded optional second-property header after first primitive property'
state['current_pass_goal'] = 'Publish the smallest production composition justified by R3.18F: terminator None at the R3.18D control end or one continuation second header through payload_start, with second payload opaque.'
state['current_pass_stop_boundary'] = 'Stop at R3.18D control end for terminators or second-property payload_start for continuations. No second payload, third property, repeated loop, non-observed second tag, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening.'
state['closed_now'] = [
    'second-property payload consumption or semantic value claim',
    'third property control/header observation or generalized production property_present loop',
    'generic repeatedly-chainable public property cursor',
    'Boolean or compound/non-observed second-header tag admission in the R3.18G composition',
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
state['r3_18f'] = {
    'outcome': 'A — admitted / read-only evidence complete',
    'pass_type': 'second-property-header real-replay evidence',
    'production_sha': PROD,
    'production_tree': PROD_TREE,
    'canonical_continuity_base': CANONICAL_BASE,
    'evidence_head_sha': EVIDENCE_HEAD,
    'evidence_tree': EVIDENCE_TREE,
    'authority_run': EVIDENCE_RUN,
    'authority_job': EVIDENCE_JOB,
    'same_head_normal_ci_run': NORMAL_CI_RUN,
    'same_head_normal_ci_job': NORMAL_CI_JOB,
    'artifact_id': ARTIFACT_ID,
    'artifact_sha256': ARTIFACT_DIGEST,
    'oracle_sha': ORACLE,
    'replay_identity': '47/47',
    'r3_18e_witness_reconstruction': '94/94',
    'continuation_rows': 47,
    'terminator_rows': 47,
    'continuation_header_native_success': '47/47',
    'second_property_present_exact': '47/47 + 47/47 terminator false',
    'second_stream_start_end_value_exact': '47/47',
    'second_stream_shape_exact': '47/47',
    'resolved_property_object_exact': '47/47',
    'resolved_attribute_tag_exact': '47/47',
    'second_payload_start_stop_exact': '47/47',
    'terminator_one_bit_stop_exact': '47/47',
    'terminator_optional_header_fields_none': '47/47',
    'continuation_attribute_tag_counts': {'Byte': 12, 'Enum': 1, 'Float': 4, 'Int': 28, 'Int64': 2},
    'header_truncation_rows': 26,
    'unresolved_stream_synthetic': 'PASS',
    'terminator_no_lookup_synthetic': 'PASS',
    'post_stop_poison': 'PASS',
    'repeatability': 'PASS',
    'native_oracle_mismatch_count': 0,
    'second_payload_bits_consumed': 0,
    'third_property_bits_consumed': 0,
    'privacy': 'PASS',
    'production_cargo_fixture_corpus_support_mutation': '0/0/0/0/0',
    'source_scope_sha256': 'a6e14057249bccc3643f519774731cb5d03ed1aad6e7337009715601b95d3a7e',
    'replay_identity_sha256': 'b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf',
    'boxcars_instrumentation_receipt_sha256': '79c80c104556e8338a7f3fb943194149743650996c988a2a9136ef5cfa7567b6',
    'selected_witnesses_sha256': '92c83039872436f3165bcb32b8b6914f6aefdbd0aa03b030235a8c4979ee3301',
    'selection_summary_sha256': 'e19384c00d4ec6650b8781319c3133709375715317406b5745222941423824d7',
    'comparison_sha256': 'f4b05f9fe6ca6e081fbffaba431efefc20e14a9e99b9dc5f654016842dec0de5',
    'aggregate_sha256': '9919aa8bfb5e70a48344442bb40c0de7c89ea41f92bc532afa5343b3c469a9b9',
    'next_pass': 'R3.18G',
}
reads = state.get('next_files_to_read', [])
for item in ['docs/continuity/MIMIR_R3_18F_DECISION.md', 'docs/continuity/MIMIR_R3_18G_EXECUTION_SPEC.md']:
    while item in reads:
        reads.remove(item)
anchor = 'docs/continuity/MIMIR_R3_18F_EXECUTION_SPEC.md'
if anchor not in reads:
    raise SystemExit('missing R3.18F reading anchor')
idx = reads.index(anchor) + 1
reads[idx:idx] = ['docs/continuity/MIMIR_R3_18F_DECISION.md', 'docs/continuity/MIMIR_R3_18G_EXECUTION_SPEC.md']
state['next_files_to_read'] = reads
p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# Current state.
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.18D — minimal native existing-actor next-property control bit`
**Completed second-header evidence:** `R3.18F — Outcome A / 47/47 continuation headers exact / 47/47 terminators / 26 truncation negatives / mismatch 0 / second payload + third property 0 + 0`
**Current exact pass:** `R3.18G — minimal native existing-actor second-property-header composition`

## 1. Truthful production boundary

Production remains R3.18D at `{PROD}` until R3.18G is cleanly implemented, independently validated and force-free published. R3.18F did not mutate production. It proved that the existing property-header primitive matches pinned Boxcars at the second-property boundary on all 47 continuation witnesses and stops correctly on all 47 terminators.

```text
production SHA                       {PROD}
production tree                      {PROD_TREE}
lib.rs blob                          {LIB_BLOB}
R3.18B focused test blob             {R318B_TEST_BLOB}
R3.18D focused test blob             {R318D_TEST_BLOB}
R3.18F evidence head/tree            {EVIDENCE_HEAD} / {EVIDENCE_TREE}
R3.18F authority run/job             {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.18F same-head normal CI           {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
R3.18F artifact                      {ARTIFACT_ID}
R3.18F artifact SHA256               {ARTIFACT_DIGEST}
```

## 2. R3.18F admitted evidence

The exact 47-replay lane reconstructed all 94 R3.18E witness classes. Continuation second headers matched 47/47 for property-present coordinates, stream start/end/value/bound/prop-bits, resolved property object/tag and payload-start/stop. Terminators matched 47/47 for one-bit stop and no optional header fields. Twenty-six real continuation rows exercised exact truncation inside the required second stream/header bits. Unresolved-stream, terminator-no-lookup, post-stop-poison and repeatability controls passed. Mismatch was zero; second payload and third-property consumption remained zero.

Observed continuation second-header tags were Byte=12, Enum=1, Float=4, Int=28 and Int64=2.

## 3. R3.18G exact next pass

R3.18G is a production implementation pass, but only for one bounded optional second-property header after an already-valid R3.18B first primitive property. Compose R3.18D control with the existing header primitive. Terminators return no second header and stop at the control end. Continuations may return exactly one second header and stop at its payload start. The new composition admits only Byte, Enum, Float, Int and Int64 as second-header tags because those are the exact R3.18F observed set.

## 4. Still closed

```text
second-property payload decode / semantic value claim
third property or repeated/generalized property loop
generic repeatedly-chainable property cursor
Boolean or compound/non-observed second-header tags in R3.18G
K2/K3/K4 dispatch through the R3.18B wrapper
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/fixture/corpus/support/dependency expansion
```
'''
(ROOT / 'docs/continuity/MIMIR_CURRENT_STATE.md').write_text(current, encoding='utf-8', newline='\n')

# Decision.
decision = f'''# MIMIR R3.18F — Second-Property-Header Evidence Decision

**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE COMPLETE**
**Production SHA (unchanged):** `{PROD}`
**Evidence authority head:** `{EVIDENCE_HEAD}`

## 1. Decision

R3.18F proves the second-property header boundary on the exact supported real-replay lane without consuming the second payload. All continuation second headers matched pinned Boxcars exactly through `payload_start`; all terminators stopped after their false one-bit control and exposed no header fields. The result admits only this evidence boundary. Production remains R3.18D until a separate implementation pass succeeds.

## 2. Exact receipts

```text
canonical continuity base             {CANONICAL_BASE}
production SHA/tree                   {PROD} / {PROD_TREE}
evidence authority head/tree          {EVIDENCE_HEAD} / {EVIDENCE_TREE}
authority run/job                     {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
same-head normal CI                   {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
artifact                              {ARTIFACT_ID}
artifact SHA256                       {ARTIFACT_DIGEST}
pinned Boxcars                        {ORACLE}
```

## 3. Evidence result

```text
replay identity / oracle parse        47/47
R3.18E witness reconstruction         94/94
continuation rows                     47
terminator rows                       47
continuation header native success    47/47
second property_present exact         47/47 + 47/47 terminator false
second stream start/end/value exact   47/47
second stream bound/prop-bits exact   47/47
resolved property object exact        47/47
resolved attribute tag exact          47/47
second payload_start/stop exact       47/47
terminator one-bit stop exact         47/47
terminator optionals None             47/47
real header truncation negatives      26
native/oracle mismatch                0
second payload bits consumed          0
third-property bits consumed          0
privacy                               PASS
production/Cargo/fixture/corpus/
support mutation                      0/0/0/0/0
```

Continuation second-header tag distribution was Byte=12, Enum=1, Float=4, Int=28 and Int64=2. Unresolved-stream synthetic, false-terminator no-lookup synthetic, post-stop poison and repeatability controls all passed.

## 4. Immutable artifact file hashes

```text
source scope                          a6e14057249bccc3643f519774731cb5d03ed1aad6e7337009715601b95d3a7e
replay identity                       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation receipt       79c80c104556e8338a7f3fb943194149743650996c988a2a9136ef5cfa7567b6
selected witnesses                    92c83039872436f3165bcb32b8b6914f6aefdbd0aa03b030235a8c4979ee3301
selection summary                     e19384c00d4ec6650b8781319c3133709375715317406b5745222941423824d7
comparison                            f4b05f9fe6ca6e081fbffaba431efefc20e14a9e99b9dc5f654016842dec0de5
aggregate                             9919aa8bfb5e70a48344442bb40c0de7c89ea41f92bc532afa5343b3c469a9b9
```

## 5. Still closed

R3.18F does not admit production second-header composition by itself, any second payload, a third property, a repeated/generalized property loop, a generic chainable property cursor, K2/K3/K4 wrapper widening, actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill/runtime/export behavior or dependency expansion.

## 6. Next pass

`R3.18G` is the minimal production admission justified by this evidence: one optional second header after a valid first primitive property, terminating at the second payload start. Its continuation tag allowlist is exactly Byte, Enum, Float, Int and Int64. Second payload remains forbidden.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18F_DECISION.md').write_text(decision, encoding='utf-8', newline='\n')

# R3.18G production execution spec.
spec = f'''# MIMIR R3.18G — Minimal Native Existing-Actor Second-Property Header Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18F Outcome A
**Second-property payload decode:** forbidden
**Third property / repeated loop:** forbidden
**Generic chainable property cursor:** forbidden

## 1. Goal

Publish the smallest production composition justified by R3.18F: after one already-valid R3.18B K1 first property, compose the existing R3.18D next-property control with the existing property-header primitive and return either a terminator or exactly one second header through `payload_start`.

This pass does not decode the second payload and does not create a general property loop.

## 2. Frozen authority

```text
canonical main before pass           {CANONICAL_BASE}
canonical tree                       {CANONICAL_TREE}
production SHA/tree                  {PROD} / {PROD_TREE}
production lib blob                  {LIB_BLOB}
R3.18B focused test blob             {R318B_TEST_BLOB}
R3.18D focused test blob             {R318D_TEST_BLOB}
R3.18F spec blob                     {R318F_SPEC_BLOB}
R3.18F authority head/tree           {EVIDENCE_HEAD} / {EVIDENCE_TREE}
R3.18F run/job                       {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.18F same-head normal CI           {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS
R3.18F artifact                      {ARTIFACT_ID}
R3.18F artifact digest               sha256:{ARTIFACT_DIGEST}
continuation second headers          47/47 exact
terminator negatives                 47/47 exact
native/oracle mismatch               0
second payload / third property bits 0 / 0
```

Before mutation, fetch fresh `main`; prove every commit after `{PROD}` is continuity-only; verify source/test/spec blobs and both R3.18F SUCCESS receipts; verify the artifact ID/digest.

## 3. Admitted production API shape

Prefer a non-generic API explicitly tied to one first primitive property, conceptually:

```text
input:
  network bytes
  + &ReplayNetworkExistingActorSinglePrimitivePropertyV1
  + &ReplayNetworkLookupPlanV1

internally:
  validate the R3.18B first-property invariants
  control = existing R3.18D after-first-primitive control decoder

if control.next_property_present == false:
  return control
  second_header = None
  stop_bit = control.stop_bit
  perform no property lookup/header/payload read after the false bit

if control.next_property_present == true:
  header = existing property-header primitive at control.property_present_start_bit
  require header.property_present == true
  require header.property_present_start/end == control.property_present_start/end
  require header actor object == first_property.header.actor_object_index
  require resolved tag in {{Byte, Enum, Float, Int, Int64}}
  second_header = Some(header)
  stop_bit = header.payload_start_bit == header.stop_bit
```

A result type may contain the R3.18D control result, an optional second header and exact stop bit. Its name must encode **after first primitive** / **second property header** semantics. Do not expose a generic cursor intended for repeated chaining.

## 4. Exact second-header tag allowlist

R3.18F observed and validated exactly:

```text
Byte   12
Enum    1
Float   4
Int    28
Int64   2
```

Therefore this new composition admits only `Byte`, `Enum`, `Float`, `Int`, `Int64` for a present second header. `Boolean`, K2, K3, K4, unknown or otherwise non-observed second-header tags must fail closed before any second payload read. This does not change the lower-level header primitive's existing independent capabilities.

## 5. Fail-closed rules

Reject atomically on:

- malformed or internally inconsistent R3.18B first-property boundary;
- R3.18D control truncation or inconsistency;
- continuation header whose present-bit coordinates do not exactly agree with the R3.18D control;
- unresolved second stream ID/property mapping;
- arithmetic/bit-range failure inside the second header;
- present second header resolving to a tag outside Byte/Enum/Float/Int/Int64;
- any impossible stop/payload-start relationship.

Failure exposes no successful second-header composition and performs no second payload decode.

## 6. Required focused tests

At minimum:

```text
false terminator -> None / exact control stop                 positive
false terminator performs no lookup after control             positive
continuation Byte                                              positive
continuation Enum                                              positive
continuation Float                                             positive
continuation Int                                               positive
continuation Int64                                             positive
aligned and unaligned second-header starts                     positive
R3.18F-shaped real boundary witnesses                          positive
control/header present-coordinate agreement                    exact
header stop == second payload_start                            exact
second payload poison / absence after payload_start            no effect
post-header poison                                             no effect
missing control bit                                            reject atomically
truncation inside second stream/header                         reject atomically
unresolved second stream                                       reject
Boolean second header                                          reject before payload
compound/non-observed second header                            reject before payload
repeatability                                                  exact
```

Use synthetic/R3.18F-shaped byte windows in tests. Do not check raw oracle windows into the clean production commit.

## 7. Source reuse rule

Reuse the published R3.18D control decoder and existing property-header primitive. Do not duplicate bounded stream decoding, lookup resolution or bit-cursor rules. Do not call scalar/K2/K3/K4 payload decoders from the new composition.

## 8. Clean production scope

Preferred clean scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18g_*.rs`

A tiny isolated source module is allowed only if direct inspection materially improves boundary enforcement. No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file may enter the clean production commit.

## 9. Source-boundary audit

Before publication, independently prove in the new composition block:

- exactly one call to the R3.18D control decoder;
- at most one call to the existing property-header primitive;
- zero scalar/K2/K3/K4 payload decoder calls;
- no `while` or `for` property loop;
- explicit five-tag allowlist;
- terminator returns before any second-header lookup path;
- no third-property access.

## 10. Validation and publication

Required before publication:

- focused R3.18G tests;
- full `mimir-replay` suite;
- workspace check/test/clippy under the Rust 1.85 floor;
- full repository verifier;
- exact clean-candidate SHA validator;
- fresh-main ancestry audit;
- force-free fast-forward publication;
- fresh `main` readback;
- exact published-main validator.

## 11. Hard stop

R3.18G does not admit:

- any second-property payload bit or semantic value;
- a third property control/header;
- repeated/generalized property loops;
- a generic repeatedly-chainable public property cursor;
- Boolean or compound/non-observed second-header tag widening;
- K2/K3/K4 composition through R3.18B;
- next actor / next frame iteration;
- actor lifecycle mutation;
- raw-state/event/replay-slice/skill/runtime/export widening;
- Cargo/fixture/corpus/support/dependency expansion.

## 12. Outcome gate

### Outcome A

The bounded optional second-header composition is published with exactly the constraints above and every validation gate passes. Then run a separate real-replay differential audit of the production second-header composition before any second-property payload admission.

### Outcome B

Implementation reveals a bounded contract mismatch between first-property/control/header semantics. Record it and keep production at R3.18D.

### Outcome C

Any source drift, loop/generalization, non-observed tag admission, second-payload consumption, third-property access, scope widening, MSRV failure or validation contradiction. Stop without publication.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18G_EXECUTION_SPEC.md').write_text(spec, encoding='utf-8', newline='\n')

# Knowledge graph.
p = ROOT / 'MIMIR_KNOWLEDGE_GRAPH.md'
g = p.read_text(encoding='utf-8')
g = regex_one(
    g,
    r'^R3\.18F active second-property-header evidence spec\s+\|$',
    'R3.18F second-property-header evidence decision                        |\nR3.18G active bounded second-property-header production spec              |',
    'graph latest nodes',
)

section_start = g.index('## Mandatory reading order\n')
section_end = g.index('\n## Current replay-decoder chain', section_start)
section = g[section_start:section_end]
entries = []
for line in section.splitlines():
    m = re.match(r'^\d+\. `([^`]+)`$', line)
    if m:
        entries.append(m.group(1))
for item in ['docs/continuity/MIMIR_R3_18F_DECISION.md', 'docs/continuity/MIMIR_R3_18G_EXECUTION_SPEC.md']:
    while item in entries:
        entries.remove(item)
anchor = 'docs/continuity/MIMIR_R3_18F_EXECUTION_SPEC.md'
if anchor not in entries:
    raise SystemExit('knowledge graph missing R3.18F spec anchor')
idx = entries.index(anchor) + 1
entries[idx:idx] = ['docs/continuity/MIMIR_R3_18F_DECISION.md', 'docs/continuity/MIMIR_R3_18G_EXECUTION_SPEC.md']
new_section = '## Mandatory reading order\n\n' + '\n'.join(f'{i}. `{item}`' for i, item in enumerate(entries, 1)) + '\n'
g = g[:section_start] + new_section + g[section_end:]

g = regex_one(
    g,
    r'(?m)^ -> R3\.18F second-property-header real-replay evidence: ACTIVE / READ-ONLY\n      .*$',
    f''' -> R3.18F second-property-header real-replay evidence: OUTCOME A / CLOSED
      authority {EVIDENCE_HEAD} / {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS; exact-head CI {NORMAL_CI_RUN} / {NORMAL_CI_JOB} SUCCESS; artifact {ARTIFACT_ID} / sha256:{ARTIFACT_DIGEST}
      47/47 continuation headers exact + 47/47 terminators exact / 26 real truncation negatives / mismatch 0 / second payload + third property 0 + 0
 -> R3.18G bounded optional second-property-header composition: ACTIVE / PRODUCTION IMPLEMENTATION
      compose one R3.18D control + at most one existing header primitive; terminator None or continuation stop at payload_start; only Byte/Enum/Float/Int/Int64; second payload and third property forbidden''',
    'graph replay chain',
)
p.write_text(g, encoding='utf-8', newline='\n')

print('R3_18F_CONTINUITY_GENERATOR=PASS')
