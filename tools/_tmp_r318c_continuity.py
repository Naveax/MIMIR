from pathlib import Path
import json
import re

ROOT = Path('.')
BASE_MAIN = 'f8f6467f2ee652892329f08a3e532b1e1f834fb3'
BASE_TREE = '9943ee5620091142379763422dc22178b2278fbc'
PROD = 'de7a2ba40663bb619ca7bd8654846ce87670d023'
PROD_TREE = 'd1889038ca2eaeb8bb0f05e44b811d906f84cf6e'
LIB_BLOB = '478ae5b70514fcff79117b834733849517c48500'
TEST_BLOB = '927e9a2c834115d1c918fa96fb6d0690bd03965e'
AUTH = 'a4b71ad43e5cf55c44c9518b24622ce29214acd2'
RUN = 31944102614
JOB = 95157425239
CI_RUN = 31944102575
CI_JOB = 95157425128
ARTIFACT = 9262820284
DIGEST = 'sha256:95e89cb350cc4c274d2b7a53198d78941bef54ff1b3f6a165b2ba9710659ec07'


def replace_one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


def regex_one(text: str, pattern: str, replacement: str, label: str) -> str:
    out, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f'{label}: expected one regex match, got {count}')
    return out


# ---------------------------------------------------------------------------
# Master execution handbook
# ---------------------------------------------------------------------------
p = ROOT / 'MIMIR_CONTINUE_HERE.md'
s = p.read_text(encoding='utf-8')
s = regex_one(
    s,
    r'^LAST_COMPLETED_EVIDENCE_PASS:\n  .+$',
    'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18C — property-loop terminator/continuation evidence / Outcome A / 47 terminator + 47 continuation candidates / exact one-bit control / 0 mismatch',
    'last completed evidence',
)
s = regex_one(
    s,
    r'^CURRENT_PASS:\n  .+$',
    'CURRENT_PASS:\n  R3.18D — minimal native existing-actor next-property control bit',
    'current pass',
)
s = regex_one(
    s,
    r'^CURRENT_PASS_TYPE:\n  .+$',
    'CURRENT_PASS_TYPE:\n  production implementation / read exactly one next property_present bit after one R3.18B K1 property',
    'current pass type',
)
old_stop = f'''  R3.18B is published production at {PROD} and composes exactly one existing-actor K1 property through its payload end without reading the next property_present bit
  R3.18C is read-only evidence only: it may prove the exact next property_present location and consume exactly that one continuation/terminator bit on selected real witnesses; production mutation remains forbidden
  NO second property stream/header/payload, production property loop, K2/K3/K4 wrapper composition, next actor, next frame, lifecycle mutation, unobserved shape/family, or extra context inference is admitted'''
new_stop = f'''  R3.18B is published production at {PROD} and composes exactly one existing-actor K1 property through its payload end without reading the next property_present bit
  R3.18C proved that this exact stop bit is the next property_present location on real terminator and continuation witnesses; the evidence probe consumed exactly one bit and zero second-stream/payload bits
  R3.18D may publish only an after-first-K1-property control-bit reader that consumes that single next property_present bit and stops immediately after it
  NO second property stream/header/payload, production property loop/repetition, K2/K3/K4 wrapper composition, next actor, next frame, lifecycle mutation, unobserved shape/family, or extra context inference is admitted'''
s = replace_one(s, old_stop, new_stop, 'production hard stop')

start = s.index('R3_18C_OPEN_BOUNDARY:')
end_marker = 'NEXT PASS AFTER R3.18C:\n  only after Outcome A, define the smallest separately validated production loop-control step; do not infer a generalized property loop or second-payload admission from one-bit continuation evidence\n'
end = s.index(end_marker, start) + len(end_marker)
new_boundary = f'''R3_18C_EVIDENCE_CLOSURE:
  Outcome A / read-only / production unchanged at {PROD}
  canonical evidence base main/tree: {BASE_MAIN} / {BASE_TREE}
  authority head: {AUTH}
  authority run/job: {RUN} / {JOB} SUCCESS
  exact-head normal CI: {CI_RUN} / {CI_JOB} SUCCESS
  artifact: {ARTIFACT}
  artifact digest: {DIGEST}
  replay identity + pinned Boxcars parse: 47/47
  loop-control candidate rows: 94 = 47 terminator + 47 continuation
  selected terminator: sample_001 / frame0 / actor60 / object344 / property18 / Float raw=1092616192 / payload [36593,36625) / next bit [36625,36626)=false
  selected continuation: sample_001 / frame0 / actor2 / object98 / property55 / Int=62 / payload [10234,10266) / next bit [10266,10267)=true
  native first-property stop == oracle next property_present start: PASS for both classes
  one-bit value/end exact: PASS for both classes; truncation cursor unchanged: PASS; post-stop poison: PASS; repeatability: PASS
  second stream bits consumed: 0; second payload bits consumed: 0; mismatch count: 0; privacy: PASS
  R3.18B focused regression: 8/8 PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_18D_OPEN_BOUNDARY:
  production implementation; one loop-control bit after one already-decoded R3.18B K1 property only
  accept network bytes plus an R3.18B single-property result (or an equivalently narrow first-property result reference) and require its boundary invariants before reading anything
  read exactly one bit at first_property.stop_bit; return next_property_present plus start/end/stop coordinates
  require control start == first_property.stop_bit and control stop == start+1
  false means exact terminator observation; true means continuation observed, but neither case authorizes second stream/header/payload decode in this pass
  implementation must not expose a reusable repeated-loop primitive that can be chained without the original first-property result
  focused tests must cover false/true, aligned/unaligned starts, both R3.18C witness shapes, truncation with no cursor advance, poison bits after the control stop, malformed first-property boundary rejection, and repeatability

R3_18D_HARD_STOP:
  no second property stream id, resolved property header, or payload decode
  no while/for property loop and no recursive/repeated control-bit consumption
  no K2/K3/K4 composition through the R3.18B wrapper
  no next actor / next frame / actor-table lifecycle mutation
  no Cargo, fixture, corpus, workflow, support-lane, raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.18D:
  only after clean production publication + exact validation, run a separate real-replay differential audit for the one-bit production control result before considering any second-property header or repeated loop admission
'''
s = s[:start] + new_boundary + s[end:]
p.write_text(s, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Machine-readable state
# ---------------------------------------------------------------------------
p = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(p.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-16'
state['last_completed_read_only_audit'] = 'R3.18C'
state['last_completed_evidence_pass'] = 'R3.18C'
state['last_completed_evidence_outcome'] = 'A — 47/47 replay identity/oracle parse; 47 terminator + 47 continuation candidates; selected real witnesses exact on first-property stop, next property_present value and one-bit end; second stream/payload bits 0/0; mismatch 0'
state['current_pass'] = 'R3.18D'
state['current_pass_kind'] = 'production implementation / after-first-K1-property next property_present control bit'
state['current_pass_goal'] = 'Publish the smallest production control-bit reader that, after one valid R3.18B K1 property result, reads exactly the next property_present bit at the proven stop boundary and returns its exact one-bit end without decoding a second property.'
state['current_pass_stop_boundary'] = 'Exactly one next property_present bit after one valid R3.18B first K1 property. No repeated loop/control-bit chaining, second stream/header/payload, K2/K3/K4 wrapper composition, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening, or Cargo/fixture/corpus/support/workflow change.'
state['closed_now'] = [
    'repeated production property_present loop beyond one next control bit',
    'second property stream/header/payload consumption',
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
state['r3_18c'] = {
    'outcome': 'A — admitted / evidence complete',
    'pass_type': 'read-only real-replay existing-actor next-property loop-control evidence',
    'production_source_changed': False,
    'continuity_base_sha': BASE_MAIN,
    'continuity_base_tree': BASE_TREE,
    'production_sha': PROD,
    'production_tree': PROD_TREE,
    'production_lib_blob': LIB_BLOB,
    'r3_18b_test_blob': TEST_BLOB,
    'authority_head': AUTH,
    'workflow_run': RUN,
    'workflow_job': JOB,
    'exact_head_ci_run': CI_RUN,
    'exact_head_ci_job': CI_JOB,
    'artifact_id': ARTIFACT,
    'artifact_digest': DIGEST,
    'supported_replays': 47,
    'oracle_parse_success': 47,
    'candidate_rows': 94,
    'terminator_candidates': 47,
    'continuation_candidates': 47,
    'terminator_witness': {
        'replay': 'external_fixtures/sample_001.replay',
        'frame_index': 0,
        'actor_ordinal': 115,
        'actor_id': 60,
        'actor_context_object_id': 344,
        'property_object_id': 18,
        'attribute_tag': 'Float',
        'lossless_raw_bits': '1092616192',
        'property_present_range': [36587, 36588],
        'stream_id': 17,
        'stream_id_bound': 25,
        'prop_id_bits': 4,
        'stream_range': [36588, 36593],
        'payload_range': [36593, 36625],
        'payload_width': 32,
        'payload_sha256': 'b4f510e22e0831cf02a9151cb6c11149fcb7d1c6570487ebcddc93970ac58583',
        'next_property_present_range': [36625, 36626],
        'next_property_present': False,
        'loop_bit_sha256': 'd189517f7ee56ad154263623d4ec3a8923a28692cd165600e93ee88672cd8145',
    },
    'continuation_witness': {
        'replay': 'external_fixtures/sample_001.replay',
        'frame_index': 0,
        'actor_ordinal': 63,
        'actor_id': 2,
        'actor_context_object_id': 98,
        'property_object_id': 55,
        'attribute_tag': 'Int',
        'lossless_value': '62',
        'property_present_range': [10227, 10228],
        'stream_id': 27,
        'stream_id_bound': 67,
        'prop_id_bits': 6,
        'stream_range': [10228, 10234],
        'payload_range': [10234, 10266],
        'payload_width': 32,
        'payload_sha256': 'd2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f',
        'next_property_present_range': [10266, 10267],
        'next_property_present': True,
        'loop_bit_sha256': 'e3d693ad5e420d2bd7828df2e5f18f38ec0a3f5660ac09414cea2fa06fd850c0',
    },
    'native_stop_equals_oracle_next_start': True,
    'next_property_bit_exact': True,
    'one_bit_stop_exact': True,
    'truncation_negative': 'PASS / cursor unchanged',
    'post_stop_poison': 'PASS',
    'repeatability': 'PASS',
    'r3_18b_negative_regression': '8/8 PASS',
    'second_stream_bits_consumed': 0,
    'second_payload_bits_consumed': 0,
    'mismatch_count': 0,
    'privacy': 'PASS',
    'production_cargo_fixture_corpus_support_mutation': '0/0/0/0/0',
    'source_scope_sha256': 'c4fdd423cbfd1672b96b748206440ddce7a47219fca3bb21fcb226fdfb9525e4',
    'replay_identity_sha256': 'b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf',
    'boxcars_instrumentation_receipt_sha256': '482ed1ddc230e0ae7b482e8e964663a831cce00a0a6480fc69a052ddd8cb5b7d',
    'selected_witnesses_sha256': '321c3ba2f7ded131ddafc2449f9aa784bd9c798294754bef4cbee2d3c6cedda5',
    'selection_summary_sha256': 'f4a9a12cfba9ba1850893d3421d141a25f462c53abbd36ae28ea152eafa86b3f',
    'comparison_sha256': 'b50ae6e09dd42450757c5a1e67646de638817007a67f8ef9a5c10dcb3129b2f0',
    'aggregate_sha256': 'a75bd832617fff9ed2bb450af78bec59efaee9e22f844534d514fee31b8e3d28',
    'next_pass': 'R3.18D',
}
reads = state.get('next_files_to_read', [])
anchor = 'docs/continuity/MIMIR_R3_18C_EXECUTION_SPEC.md'
for item in ['docs/continuity/MIMIR_R3_18C_DECISION.md', 'docs/continuity/MIMIR_R3_18D_EXECUTION_SPEC.md']:
    while item in reads:
        reads.remove(item)
if anchor not in reads:
    raise SystemExit('next_files_to_read missing R3.18C spec anchor')
idx = reads.index(anchor) + 1
reads[idx:idx] = ['docs/continuity/MIMIR_R3_18C_DECISION.md', 'docs/continuity/MIMIR_R3_18D_EXECUTION_SPEC.md']
state['next_files_to_read'] = reads
p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Current state summary
# ---------------------------------------------------------------------------
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.18B — minimal native existing-actor single-property K1 composition`
**Completed loop-control evidence:** `R3.18C — Outcome A / 47 terminator + 47 continuation candidates / exact next bit / 0 mismatch`
**Current exact pass:** `R3.18D — minimal native existing-actor next-property control bit`

## 1. Truthful production boundary

Production remains R3.18B. It composes exactly one existing-actor K1 property and stops at that scalar payload end. R3.18C now proves on real replay witnesses that this stop is exactly the next `property_present` location, for both a false terminator and true continuation. **R3.18C did not widen production.**

```text
canonical git main before closure  {BASE_MAIN}
production SHA                     {PROD}
production tree                    {PROD_TREE}
lib.rs blob                        {LIB_BLOB}
R3.18B focused test blob           {TEST_BLOB}
```

## 2. R3.18C evidence closure

```text
authority head                     {AUTH}
authority run/job                  {RUN} / {JOB} SUCCESS
same-head normal CI                {CI_RUN} / {CI_JOB} SUCCESS
artifact                           {ARTIFACT}
artifact digest                    {DIGEST}
replay identity / Boxcars parse    47/47
candidate rows                     94
terminator candidates              47
continuation candidates            47
native/oracle mismatch             0
second stream bits consumed        0
second payload bits consumed       0
privacy                            PASS
production/Cargo/fixture/corpus/
support mutation                   0/0/0/0/0
```

Selected terminator:

```text
replay                             external_fixtures/sample_001.replay
frame / actor ordinal / actor id   0 / 115 / 60
actor context / property object    344 / 18
first property                     Float / raw bits 1092616192
payload                            [36593,36625)
native stop / next-bit start       36625 / 36625
next property_present              false at [36625,36626)
one-bit evidence stop              36626
```

Selected continuation:

```text
replay                             external_fixtures/sample_001.replay
frame / actor ordinal / actor id   0 / 63 / 2
actor context / property object    98 / 55
first property                     Int / 62
payload                            [10234,10266)
native stop / next-bit start       10266 / 10266
next property_present              true at [10266,10267)
one-bit evidence stop              10267
```

Both witnesses passed exact header/semantic/payload boundaries, next-bit equality, one-bit stop, truncation-without-cursor-advance, post-stop poison, repeatability and R3.18B negative regression.

## 3. R3.18D exact next pass

Publish only the production equivalent of the one-bit evidence boundary. The new API should be structurally tied to an already-valid R3.18B first-property result, validate that result's end invariants, read the bit at `first_property.stop_bit`, and return:

```text
next_property_present
property_present_start_bit
property_present_end_bit
stop_bit
```

The stop must equal `start + 1`. `false` records an exact terminator; `true` records only that continuation exists. Neither result may decode the second stream ID, second property header, or second payload. The API must not be a chainable generalized loop primitive detached from the original first-property result.

## 4. Still closed

```text
repeated production property_present loop
second property stream/header/payload
K2/K3/K4 dispatch through the R3.18B wrapper
next actor / next frame iteration
actor lifecycle mutation
new attribute family/shape/context admission
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/fixture/corpus/support/workflow expansion
```
'''
(ROOT / 'docs/continuity/MIMIR_CURRENT_STATE.md').write_text(current, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# R3.18C decision
# ---------------------------------------------------------------------------
decision = f'''# MIMIR — R3.18C Decision

**Date:** 2026-08-16
**Pass:** `R3.18C — existing-actor property-loop terminator / continuation evidence`
**Outcome:** **A — ADMITTED / EVIDENCE COMPLETE**
**Production mutation:** none
**Second property decode:** none

## Decision

R3.18C proves the first loop-control edge after the published R3.18B one-property K1 composition. Across the frozen 47-replay lane, the pinned Boxcars oracle produced both required witness classes: 47 terminator candidates and 47 continuation candidates. For the selected real witnesses, the native R3.18B `stop_bit` is exactly the oracle's next `property_present` start, and an evidence-only native reader consumes exactly that one bit and stops immediately after it.

This evidence does not admit a production property loop or a second property stream/header/payload.

## Frozen authority

```text
canonical evidence base main/tree  {BASE_MAIN} / {BASE_TREE}
production SHA/tree                 {PROD} / {PROD_TREE}
authority head                      {AUTH}
authority run/job                   {RUN} / {JOB} SUCCESS
same-head normal CI                 {CI_RUN} / {CI_JOB} SUCCESS
artifact                            {ARTIFACT}
artifact digest                     {DIGEST}
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
replay identity/oracle              47/47
candidate rows                      94
terminator / continuation           47 / 47
```

## Selected terminator witness

```text
replay                              external_fixtures/sample_001.replay
frame / actor ordinal / actor id    0 / 115 / 60
actor context object                344
property object / tag               18 / Float
semantic raw bits                   1092616192
property_present                    [36587,36588)
stream id / bound / bits            17 / 25 / 4
stream range                        [36588,36593)
payload                             [36593,36625) / 32 bits
payload SHA256                      b4f510e22e0831cf02a9151cb6c11149fcb7d1c6570487ebcddc93970ac58583
next property_present               false / [36625,36626)
loop-bit SHA256                     d189517f7ee56ad154263623d4ec3a8923a28692cd165600e93ee88672cd8145
native stop                         36625
one-bit evidence stop               36626
```

## Selected continuation witness

```text
replay                              external_fixtures/sample_001.replay
frame / actor ordinal / actor id    0 / 63 / 2
actor context object                98
property object / tag / value       55 / Int / 62
property_present                    [10227,10228)
stream id / bound / bits            27 / 67 / 6
stream range                        [10228,10234)
payload                             [10234,10266) / 32 bits
payload SHA256                      d2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f
next property_present               true / [10266,10267)
loop-bit SHA256                     e3d693ad5e420d2bd7828df2e5f18f38ec0a3f5660ac09414cea2fa06fd850c0
native stop                         10266
one-bit evidence stop               10267
```

## Gate results

```text
native stop == oracle next start    PASS / both classes
next property bit exact             PASS / both classes
one-bit stop exact                  PASS / both classes
truncation negative                 PASS / cursor unchanged
post-stop poison                    PASS
native repeatability                PASS
R3.18B focused regression           8/8 PASS
second stream bits consumed         0
second payload bits consumed        0
native/oracle mismatch              0
privacy                             PASS
prod/Cargo/fixture/corpus/support   0/0/0/0/0 mutation
```

Receipt SHA-256 values:

```text
source scope                        c4fdd423cbfd1672b96b748206440ddce7a47219fca3bb21fcb226fdfb9525e4
replay identity                     b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation receipt     482ed1ddc230e0ae7b482e8e964663a831cce00a0a6480fc69a052ddd8cb5b7d
selected witnesses                  321c3ba2f7ded131ddafc2449f9aa784bd9c798294754bef4cbee2d3c6cedda5
selection summary                   f4a9a12cfba9ba1850893d3421d141a25f462c53abbd36ae28ea152eafa86b3f
comparison                          b50ae6e09dd42450757c5a1e67646de638817007a67f8ef9a5c10dcb3129b2f0
aggregate                           a75bd832617fff9ed2bb450af78bec59efaee9e22f844534d514fee31b8e3d28
```

## Next exact pass

`R3.18D — minimal native existing-actor next-property control bit`.

R3.18D may publish only the single proven bit after one valid R3.18B K1 property result. It may not decode a second stream/header/payload, repeat the control operation as a property loop, or widen K2/K3/K4 composition.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18C_DECISION.md').write_text(decision, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# R3.18D execution spec
# ---------------------------------------------------------------------------
spec = f'''# MIMIR R3.18D — Minimal Native Existing-Actor Next-Property Control Bit

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18C Outcome A
**Second property decode:** forbidden
**Repeated property loop:** forbidden

## 1. Goal

Publish the smallest production boundary justified by R3.18C: after one already-valid R3.18B K1 first-property result, read exactly the next `property_present` bit at the first property's stop bit, report terminator versus continuation, and stop one bit later.

This pass implements one loop-control observation. It does not implement the loop body for another property.

## 2. Frozen authority

```text
canonical main before pass          {BASE_MAIN}
production SHA/tree                 {PROD} / {PROD_TREE}
production lib blob                 {LIB_BLOB}
R3.18B focused test blob            {TEST_BLOB}
R3.18C authority head               {AUTH}
R3.18C run/job                      {RUN} / {JOB} SUCCESS
R3.18C same-head normal CI          {CI_RUN} / {CI_JOB} SUCCESS
R3.18C artifact                     {ARTIFACT}
R3.18C artifact digest              {DIGEST}
terminator candidates               47
continuation candidates             47
native/oracle mismatch              0
second stream/payload bits          0 / 0
```

Before mutation, fetch fresh `main` and verify that the production source/test blobs still match the R3.18B authority and that only continuity commits exist after `{PROD}`.

## 3. Admitted production API shape

Prefer an API structurally tied to the already-decoded first property, for example conceptually:

```text
input:
  network bytes
  + &ReplayNetworkExistingActorSinglePrimitivePropertyV1

validate:
  first_property.header.stop_bit == first_property.scalar.payload_start_bit
  first_property.stop_bit == first_property.scalar.payload_end_bit
  first_property.scalar.stop_bit == first_property.scalar.payload_end_bit

read:
  exactly one LSB-first bit at first_property.stop_bit

return:
  next_property_present: bool
  property_present_start_bit: u64
  property_present_end_bit: u64
  stop_bit: u64

require:
  property_present_start_bit == first_property.stop_bit
  property_present_end_bit == property_present_start_bit + 1
  stop_bit == property_present_end_bit
```

The function name/type should explicitly encode **after first primitive property** semantics rather than expose a generic repeatedly chainable property-loop cursor.

## 4. Fail-closed rules

Reject atomically on:

- malformed/internally inconsistent R3.18B first-property boundary;
- arithmetic overflow computing the one-bit end;
- missing next bit / truncated bytes;
- any start beyond the provided byte range.

On failure, expose no successful control result and consume no observable cursor state.

## 5. Required focused tests

At minimum:

```text
false terminator                         positive
true continuation                       positive
aligned first-property end               positive
unaligned first-property end             positive
R3.18C Float terminator shape            positive
R3.18C Int=62 continuation shape         positive
exact start/end/stop                     exact
post-control poison bits                 no effect
missing next bit                         reject atomically
malformed first-property boundary        reject
repeatability                            exact
```

Tests may construct R3.18C-shaped first-property results through the existing R3.18B production API; do not check in raw oracle payload windows merely to satisfy a regression.

## 6. Source reuse rule

Reuse existing private/native bit primitives where practical. Do not reimplement bounded stream decoding, property resolution, scalar payload decoding, or Boxcars behavior. This pass needs only one bit after an already-complete R3.18B result.

## 7. Clean production scope

Preferred clean scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18d_*.rs`

A separate tiny source module is allowed only if direct inspection shows it materially improves isolation. No `Cargo.toml`, `Cargo.lock`, fixture, corpus, workflow, temporary tool, support lane, or continuity file may enter the clean production commit.

## 8. Hard stop

R3.18D does **not** admit:

- decoding the second property stream ID;
- resolving the second property header/tag;
- decoding the second property payload;
- calling the control-bit reader repeatedly as a property loop;
- a `while` / `for` production property loop;
- K2/K3/K4 composition through the R3.18B wrapper;
- next actor / next frame iteration;
- actor lifecycle table mutation;
- raw-state/event/replay-slice/skill/runtime/export widening.

## 9. Validation and publication

Required before publication:

- exact source-boundary audit proving one-bit-only behavior;
- focused R3.18D tests;
- full `mimir-replay` suite;
- workspace check/test/clippy under the Rust 1.85 floor;
- full repository verifier;
- exact clean-candidate SHA validator;
- fresh-main ancestry audit;
- force-free fast-forward publication;
- exact published-main validator/readback.

## 10. Outcome gate

### Outcome A

The one-bit API is published with the exact boundary above and every validation gate passes. Then run a separate real-replay differential audit of the production control result before any second-property header/body admission.

### Outcome B

Implementation reveals an unresolved first-property/control-boundary contract. Record it and keep production at R3.18B.

### Outcome C

Any source drift, cursor ambiguity, scope widening, second-property consumption, MSRV failure, or validation contradiction. Stop without publication.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18D_EXECUTION_SPEC.md').write_text(spec, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Knowledge graph
# ---------------------------------------------------------------------------
p = ROOT / 'MIMIR_KNOWLEDGE_GRAPH.md'
g = p.read_text(encoding='utf-8')
g = replace_one(
    g,
    'R3.18B single-property K1 production decision                  |\nR3.18C active property-loop boundary evidence spec              |',
    'R3.18B single-property K1 production decision                  |\nR3.18C property-loop boundary evidence decision                   |\nR3.18D active next-property control-bit production spec            |',
    'graph chain head',
)
g = replace_one(
    g,
    '''37. `docs/continuity/MIMIR_R3_18B_DECISION.md`
38. `docs/continuity/MIMIR_R3_18C_EXECUTION_SPEC.md`
39. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
40. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
41. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
42. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
43. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
44. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
45. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`''',
    '''37. `docs/continuity/MIMIR_R3_18B_DECISION.md`
38. `docs/continuity/MIMIR_R3_18C_EXECUTION_SPEC.md`
39. `docs/continuity/MIMIR_R3_18C_DECISION.md`
40. `docs/continuity/MIMIR_R3_18D_EXECUTION_SPEC.md`
41. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
42. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
43. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
44. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
45. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
46. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
47. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`''',
    'mandatory reading order',
)
g = replace_one(
    g,
    ''' -> R3.18C existing-actor property-loop terminator/continuation evidence: ACTIVE / READ-ONLY
      prove native stop == next property_present start and consume exactly one terminator/continuation bit; second stream/header/payload remains closed''',
    f''' -> R3.18C existing-actor property-loop terminator/continuation evidence: OUTCOME A / CLOSED
      authority {AUTH} / {RUN} / {JOB} SUCCESS
      exact-head CI {CI_RUN} / {CI_JOB} SUCCESS
      artifact {ARTIFACT} / {DIGEST}
      47/47 oracle / 47 terminator + 47 continuation candidates / selected false+true exact / one-bit stop exact / second stream+payload bits 0+0 / mismatch 0
 -> R3.18D minimal native existing-actor next-property control bit: ACTIVE / PRODUCTION
      read exactly one next property_present bit after a valid R3.18B first K1 property; stop immediately after it; no second stream/header/payload and no repeated loop''',
    'decoder chain R3.18C',
)
g = replace_one(
    g,
    '''R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups; R3.17K implemented them; R3.17L matched all 1,950 against real replay witnesses. R3.17M then observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups; R3.17N admitted those 161 groups byte-for-byte; R3.17O implemented exactly that contract with zero cross-product widening; R3.17P then matched all 161 exact K4 groups against real replay witnesses with zero mismatch. R3.18A proved one complete real existing-actor property boundary with an Int payload and zero next-property bits consumed. R3.18B published the minimal K1 one-property composition. R3.18C is now read-only evidence for the next one-bit loop-control edge; production property-loop continuation, second property payloads, K2/K3/K4 wrapper composition, next actor/frame iteration and lifecycle mutation remain closed.''',
    '''R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups; R3.17K implemented them; R3.17L matched all 1,950 against real replay witnesses. R3.17M then observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups; R3.17N admitted those 161 groups byte-for-byte; R3.17O implemented exactly that contract with zero cross-product widening; R3.17P then matched all 161 exact K4 groups against real replay witnesses with zero mismatch. R3.18A proved one complete real existing-actor property boundary; R3.18B published the minimal K1 one-property composition. R3.18C then proved the exact next one-bit loop-control edge for both real terminator and continuation classes with zero second-property consumption. R3.18D may publish only that one control bit; second property decoding, repeated property loops, K2/K3/K4 wrapper composition, next actor/frame iteration and lifecycle mutation remain closed.''',
    'capability history paragraph',
)
old_tail = '''R3.18C is now the first dependency-valid unfinished roadmap step: read-only proof that the R3.18B stop bit is exactly the next `property_present` location, with one real terminator and one real continuation witness when available. The native evidence probe may consume only that one bit; a second stream/header/payload and production property loop remain unadmitted.'''
new_tail = f'''## R3.18C loop-control evidence closure

```text
authority head              {AUTH}
authority run/job           {RUN} / {JOB} SUCCESS
exact-head normal CI        {CI_RUN} / {CI_JOB} SUCCESS
artifact                    {ARTIFACT}
artifact digest             {DIGEST}
replay identity/oracle      47/47
candidate rows              94
terminator / continuation   47 / 47
selected terminator         sample_001 / Float raw1092616192 / native stop 36625 / next bit false / evidence stop 36626
selected continuation       sample_001 / Int=62 / native stop 10266 / next bit true / evidence stop 10267
one-bit boundary/value      exact / both classes
truncation + poison         PASS / PASS
second stream/payload bits  0 / 0
mismatch / privacy          0 / PASS
outcome                     A
```

R3.18D is now the first dependency-valid unfinished roadmap step: publish only the production one-bit control observation after one valid R3.18B first K1 property. It must stop after that bit. A second stream/header/payload and repeated property loop remain unadmitted.'''
g = replace_one(g, old_tail, new_tail, 'graph tail next pass')
p.write_text(g, encoding='utf-8', newline='\n')

print('R3_18C_CONTINUITY_GENERATION=PASS')
