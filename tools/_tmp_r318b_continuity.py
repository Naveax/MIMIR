from pathlib import Path
import json
import re

ROOT = Path('.')
BASE_MAIN = 'de7a2ba40663bb619ca7bd8654846ce87670d023'
BASE_TREE = 'd1889038ca2eaeb8bb0f05e44b811d906f84cf6e'
PARENT = 'f12365b43029f19f3ab1dd889e651f9781b0655e'
LIB_BLOB = '478ae5b70514fcff79117b834733849517c48500'
TEST_BLOB = '927e9a2c834115d1c918fa96fb6d0690bd03965e'
IMPL_RUN = 31942254523
IMPL_JOB = 95153021330
EXACT_RUN = 31942696817
EXACT_JOB = 95154052998
MAIN_CI_RUN = 31942870294
MAIN_CI_JOB = 95154460239
PUBLISHED_RUN = 31942896666
PUBLISHED_JOB = 95154519828


def replace_one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one match, got {count}')
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
s = regex_one(s, r'^LAST_PRODUCTION_CODE_SHA:\n  [0-9a-f]{40}$', f'LAST_PRODUCTION_CODE_SHA:\n  {BASE_MAIN}', 'last production sha')
s = regex_one(
    s,
    r'^LAST_PRODUCTION_MILESTONE:\n  .+$',
    'LAST_PRODUCTION_MILESTONE:\n  R3.18B — minimal native existing-actor single-property K1 composition',
    'last production milestone',
)
s = regex_one(
    s,
    r'^CURRENT_PASS:\n  .+$',
    'CURRENT_PASS:\n  R3.18C — existing-actor property-loop terminator/continuation evidence',
    'current pass',
)
s = regex_one(
    s,
    r'^CURRENT_PASS_TYPE:\n  .+$',
    'CURRENT_PASS_TYPE:\n  read-only real-replay evidence / exact next property_present bit after one native K1 property',
    'current pass type',
)
old_stop = '''  R3.17P certified the published R3.17O K4 decoder on all 161 exact real-replay groups; R3.18A then proved one real existing-actor property header + Int payload through the exact end cursor with 0 next-property bits consumed
  R3.18B may compose only the existing first-property header with the already-admitted K1 primitive scalar decoder; K2/K3/K4 composition and every property loop remain closed
  NO second property, next actor, next frame, lifecycle mutation, unobserved shape/family, or extra context inference is admitted'''
new_stop = f'''  R3.18B is published production at {BASE_MAIN} and composes exactly one existing-actor K1 property through its payload end without reading the next property_present bit
  R3.18C is read-only evidence only: it may prove the exact next property_present location and consume exactly that one continuation/terminator bit on selected real witnesses; production mutation remains forbidden
  NO second property stream/header/payload, production property loop, K2/K3/K4 wrapper composition, next actor, next frame, lifecycle mutation, unobserved shape/family, or extra context inference is admitted'''
s = replace_one(s, old_stop, new_stop, 'production hard stop body')
old_boundary = '''R3_18B_OPEN_BOUNDARY:
  production implementation; minimal existing-actor single-property composition only
  reuse the existing R3.16B first-property header reader and existing R3.17C primitive scalar decoder; do not duplicate either wire codec
  require property_present=true, resolve the exact stream/property/tag through the existing lookup plan, and admit only K1 Boolean/Byte/Enum/Float/Int/Int64 payload dispatch
  return the exact one-property end cursor with stop_bit == payload_end_bit; do not read the next property_present bit
  K2/K3/K4 composition is outside this pass despite those one-value decoders existing separately
  focused tests must cover all six K1 tags, truncation/unsupported/absent cases, poison bits after payload, and an R3.18A-shaped Int=62 regression

R3_18B_HARD_STOP:
  no second property and no property_present loop
  no K2/K3/K4 composition inside the new one-property API
  no next actor / next frame / actor-table lifecycle mutation
  no Cargo, fixture, corpus or support-lane change
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.18B:
  only after clean production publication + exact validation, select a separate evidence pass for property-loop terminator/continuation; do not infer loop admission from one-property success
'''
new_boundary = f'''R3_18B_PRODUCTION_CLOSURE:
  Outcome A / published production / minimal existing-actor one-property K1 composition
  production SHA/tree: {BASE_MAIN} / {BASE_TREE}
  parent main: {PARENT}
  lib.rs blob: {LIB_BLOB}
  focused test blob: {TEST_BLOB}
  implementation run/job: {IMPL_RUN} / {IMPL_JOB} SUCCESS
  exact clean-candidate validation: {EXACT_RUN} / {EXACT_JOB} SUCCESS
  published main CI: {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
  published-main validator: {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
  clean scope: crates/mimir-replay/src/lib.rs + crates/mimir-replay/tests/r3_18b_single_k1_property.rs only
  K1 dispatch: Boolean/Byte/Enum/Float/Int/Int64 only; non-K1 rejects before payload read
  exact one-property stop: header.stop_bit == payload_start_bit and composition.stop_bit == scalar.payload_end_bit
  focused tests: 8/8 PASS including R3.18A-shaped Int=62, poison trailing bits, absent/non-K1/truncation/repeatability
  production/Cargo/fixture/corpus/support/workflow/continuity mutation outside clean scope: 0/0/0/0/0/0/0

R3_18C_OPEN_BOUNDARY:
  read-only real-replay evidence; production Rust/Cargo/fixture/corpus/support mutation forbidden
  reuse the exact supported 47-replay lane and pinned Boxcars oracle; deterministically find real existing-actor updates whose first property is R3.18B-admitted K1
  require native R3.18B stop_bit == oracle next property_present start bit
  prove at least one terminator witness (next property_present=false) and at least one continuation witness (next property_present=true), if both exist in the frozen lane
  the native evidence probe may consume exactly one bit at that stop position and must stop immediately after it
  for false, prove exact loop terminator end = start+1 and zero stream/payload bits consumed; for true, prove continuation=true but do not decode the second stream/header/payload natively
  durable artifacts must remain privacy-safe and omit raw replay payload bytes

R3_18C_HARD_STOP:
  no production mutation
  no second property stream id, resolved header, or payload decode in the native evidence probe
  no production property_present loop
  no K2/K3/K4 widening through the R3.18B composition API
  no next actor / next frame / actor-table lifecycle mutation
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.18C:
  only after Outcome A, define the smallest separately validated production loop-control step; do not infer a generalized property loop or second-payload admission from one-bit continuation evidence
'''
s = replace_one(s, old_boundary, new_boundary, 'R3.18B boundary block')
p.write_text(s, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Machine-readable state
# ---------------------------------------------------------------------------
p = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(p.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-16'
state['last_production_code_sha'] = BASE_MAIN
state['last_production_milestone'] = 'R3.18B'
state['last_production_milestone_name'] = 'minimal native existing-actor single-property K1 composition'
state['last_completed_read_only_audit'] = 'R3.18A'
state['current_pass'] = 'R3.18C'
state['current_pass_kind'] = 'read-only real-replay evidence / property-loop terminator and continuation bit'
state['current_pass_goal'] = 'Prove that the R3.18B one-property stop bit is exactly the next property_present location on real existing-actor updates, and characterize both false terminator and true continuation cases without decoding a second property payload.'
state['current_pass_stop_boundary'] = 'Evidence-only: after one R3.18B-admitted K1 property, consume exactly one next property_present bit and stop. No second stream/header/payload native decode, production property loop, K2/K3/K4 wrapper widening, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening, or Cargo/fixture/corpus/support mutation.'
state['closed_now'] = [
    'production property_present loop beyond one complete K1 property',
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
state['r3_18b'] = {
    'outcome': 'A — admitted / published production',
    'pass_type': 'production implementation / minimal existing-actor single-property K1 composition',
    'production_sha': BASE_MAIN,
    'production_tree': BASE_TREE,
    'parent_main_sha': PARENT,
    'source_file': 'crates/mimir-replay/src/lib.rs',
    'source_git_blob': LIB_BLOB,
    'focused_test_file': 'crates/mimir-replay/tests/r3_18b_single_k1_property.rs',
    'focused_test_git_blob': TEST_BLOB,
    'implementation_run': IMPL_RUN,
    'implementation_job': IMPL_JOB,
    'exact_candidate_validation_run': EXACT_RUN,
    'exact_candidate_validation_job': EXACT_JOB,
    'published_main_ci_run': MAIN_CI_RUN,
    'published_main_ci_job': MAIN_CI_JOB,
    'published_main_validation_run': PUBLISHED_RUN,
    'published_main_validation_job': PUBLISHED_JOB,
    'focused_tests': '8/8 PASS',
    'admitted_tags': ['Boolean', 'Byte', 'Enum', 'Float', 'Int', 'Int64'],
    'r3_18a_int_62_regression': 'PASS',
    'trailing_next_property_poison_bits': 'PASS / no effect',
    'property_absent_negative': 'PASS',
    'non_k1_negative': 'PASS / rejected before payload read',
    'header_truncation_negative': 'PASS',
    'payload_truncation_negative': 'PASS',
    'repeatability': 'PASS',
    'header_stop_equals_payload_start': True,
    'composition_stop_equals_payload_end': True,
    'next_property_present_consumed_bits': 0,
    'clean_files': [
        'crates/mimir-replay/src/lib.rs',
        'crates/mimir-replay/tests/r3_18b_single_k1_property.rs',
    ],
    'cargo_fixture_corpus_support_workflow_continuity_mutation': '0/0/0/0/0/0/0',
    'next_pass': 'R3.18C',
}
reads = state.get('next_files_to_read', [])
anchor = 'docs/continuity/MIMIR_R3_18B_EXECUTION_SPEC.md'
for item in ['docs/continuity/MIMIR_R3_18B_DECISION.md', 'docs/continuity/MIMIR_R3_18C_EXECUTION_SPEC.md']:
    while item in reads:
        reads.remove(item)
if anchor not in reads:
    raise SystemExit('next_files_to_read missing R3.18B execution spec anchor')
idx = reads.index(anchor) + 1
reads[idx:idx] = [
    'docs/continuity/MIMIR_R3_18B_DECISION.md',
    'docs/continuity/MIMIR_R3_18C_EXECUTION_SPEC.md',
]
state['next_files_to_read'] = reads
p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Human-readable current state
# ---------------------------------------------------------------------------
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{BASE_MAIN}`
**Production milestone:** `R3.18B — minimal native existing-actor single-property K1 composition`
**Completed single-property evidence:** `R3.18A — Outcome A / exact one-property boundary / 0 next-property bits`
**Current exact pass:** `R3.18C — existing-actor property-loop terminator/continuation evidence`

## 1. Truthful production boundary

Production now includes R3.18B. MIMIR can start at an existing actor's first `property_present` bit, reuse the R3.16B header decoder, and compose exactly one property only when the resolved tag is one of the six already-admitted K1 primitive scalar tags. The composition stops exactly at that scalar payload end. It does not read the next `property_present` bit and it does not dispatch K2/K3/K4 through this wrapper.

Separate one-value K2/K3/K4 decoders remain production-authoritative at their previously admitted boundaries; R3.18B deliberately does not combine them into the property wrapper.

```text
production SHA               {BASE_MAIN}
production tree              {BASE_TREE}
parent                       {PARENT}
lib.rs blob                  {LIB_BLOB}
R3.18B focused test blob     {TEST_BLOB}
```

## 2. R3.18B production closure

```text
implementation run/job       {IMPL_RUN} / {IMPL_JOB} SUCCESS
exact candidate validation   {EXACT_RUN} / {EXACT_JOB} SUCCESS
published main CI            {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
published-main validator     {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
clean production files       2
focused R3.18B tests          8/8 PASS
K1 tags                       Boolean Byte Enum Float Int Int64
R3.18A-shaped Int=62          PASS
property absent               reject
non-K1 tag                    reject before payload read
header/payload truncation     reject
trailing poison bits          no effect
header stop == payload start  true
composition stop == end       true
next property bits consumed   0
Cargo/fixture/corpus/support/
workflow/continuity mutation  0/0/0/0/0/0/0
```

## 3. R3.18C exact next pass

R3.18C is evidence-only. On deterministic real existing-actor witnesses whose first property is R3.18B-admitted K1, compare the native one-property `stop_bit` to the pinned Boxcars oracle's next `property_present` start. Then consume **exactly one bit** at that location in the evidence probe.

Required witness classes, if both exist in the frozen supported lane:

```text
terminator     next property_present = false
continuation   next property_present = true
```

For the terminator case, prove the actor's property sequence ends exactly after that one bit and no stream/payload bits are consumed. For the continuation case, prove only that continuation is true and stop immediately after the bit. A second stream ID, property header, or payload remains outside the native evidence boundary.

## 4. Still closed

```text
production property_present loop
second property stream/header/payload
K2/K3/K4 dispatch through the R3.18B wrapper
next actor / next frame iteration
actor lifecycle mutation
new attribute family/shape/context admission
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/fixture/corpus/support-lane expansion
```
'''
(ROOT / 'docs/continuity/MIMIR_CURRENT_STATE.md').write_text(current, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# R3.18B decision
# ---------------------------------------------------------------------------
decision = f'''# MIMIR — R3.18B Decision

**Date:** 2026-08-16
**Pass:** `R3.18B — minimal native existing-actor single-property K1 composition`
**Outcome:** **A — ADMITTED / PUBLISHED PRODUCTION**
**Property loop:** not admitted

## Decision

R3.18B is now canonical production. MIMIR composes the existing R3.16B first-property header with the existing R3.17C primitive scalar decoder for exactly one existing-actor K1 property. The wrapper accepts only `Boolean`, `Byte`, `Enum`, `Float`, `Int`, and `Int64`, preserves the resolved header identity, and returns the scalar payload end as its exact stop bit.

This publication does not authorize a second property, a `property_present` loop, or K2/K3/K4 dispatch through the new wrapper.

## Frozen production authority

```text
parent main                  {PARENT}
production SHA               {BASE_MAIN}
production tree              {BASE_TREE}
lib.rs blob                  {LIB_BLOB}
focused test blob            {TEST_BLOB}
implementation run/job       {IMPL_RUN} / {IMPL_JOB} SUCCESS
exact candidate validation   {EXACT_RUN} / {EXACT_JOB} SUCCESS
published main CI            {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
published-main validator     {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
```

## Admitted behavior

```text
property_present=true        required
header authority             existing R3.16B decoder
payload authority            existing R3.17C primitive scalar decoder
admitted wrapper tags        Boolean / Byte / Enum / Float / Int / Int64
header stop                  exact payload_start_bit
wrapper stop                 exact scalar.payload_end_bit
next property_present        unread / 0 bits consumed
non-K1 resolved tag          fail closed before payload read
```

The focused suite is 8/8 PASS and includes aligned/unaligned starts for all six K1 tags, the R3.18A real-context `Int=62` regression, poison trailing bits, property-absent rejection, non-K1 rejection, header truncation, payload truncation, and repeatability.

## Clean scope

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_18b_single_k1_property.rs
```

No `Cargo.toml`, `Cargo.lock`, fixture, corpus, support script, workflow, or continuity file entered the clean production commit.

## Validation result

The exact clean candidate and the published `main` both passed the repository verifier. The published production SHA is therefore `{BASE_MAIN}` rather than the older R3.17O authority.

## Next exact pass

`R3.18C — existing-actor property-loop terminator/continuation evidence`.

R3.18C is read-only. It may prove the exact next `property_present` position after one R3.18B K1 property and consume exactly that one bit for terminator/continuation evidence. It may not decode a second property stream/header/payload or mutate production.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18B_DECISION.md').write_text(decision, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# R3.18C execution spec
# ---------------------------------------------------------------------------
spec = f'''# MIMIR R3.18C — Existing-Actor Property-Loop Terminator / Continuation Evidence

**Status:** ACTIVE
**Pass type:** read-only real-replay evidence
**Production mutation:** forbidden
**Second property payload:** forbidden

## 1. Goal

Prove the first loop-control edge immediately after the published R3.18B one-property composition.

For deterministic real existing-actor updates whose first property resolves to an R3.18B-admitted K1 scalar, prove that:

```text
native R3.18B stop_bit
== pinned Boxcars first-property payload end
== pinned Boxcars next property_present start bit
```

Then an evidence-only native probe may read exactly that one next `property_present` bit and must stop immediately afterward.

This is evidence for loop control, not implementation of a production property loop.

## 2. Frozen authority

```text
canonical main / production  {BASE_MAIN}
production tree              {BASE_TREE}
parent                       {PARENT}
lib.rs blob                  {LIB_BLOB}
R3.18B focused test blob     {TEST_BLOB}
R3.18B exact validation      {EXACT_RUN} / {EXACT_JOB} SUCCESS
R3.18B published main CI     {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
R3.18B published validator   {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
R3.18A oracle authority      12ee215fd843260d5ece14f27aa1171cb862f49e
R3.18A evidence run/job      31941400273 / 95151024131 SUCCESS
pinned Boxcars               c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        exact 47-replay identity lane
```

Before evidence work, re-read fresh `main` and verify the production SHA/tree/source blobs above. Any drift requires a new ancestry/source audit before continuing.

## 3. Witness selection

Regenerate or reuse the exact 47-replay identity lane under immutable SHA checks. With pinned Boxcars instrumentation, enumerate real existing-actor updates where:

1. the first property is present;
2. its resolved tag is one of `Boolean`, `Byte`, `Enum`, `Float`, `Int`, `Int64`;
3. Boxcars reaches the first payload end cleanly;
4. the following `property_present` bit exists.

Deterministically select:

- at least one **terminator** witness with next `property_present = false`;
- at least one **continuation** witness with next `property_present = true`;

if both classes exist in the frozen lane. If one class does not exist, do not manufacture a synthetic admission claim; record the evidence gap and choose Outcome B/C as appropriate.

Selection order must be deterministic, for example lexicographic replay label then frame index then actor ordinal/ID.

## 4. Required comparisons

For each selected witness, prove:

```text
replay identity                          exact
frame / actor identity                   exact
first property stream/property/tag       exact
first property semantic value            exact for the admitted K1 type
native first payload start               == oracle start
native first payload end / stop_bit      == oracle end
oracle next property_present start       == native stop_bit
native evidence bit value                == oracle next property_present value
native evidence stop                     == native stop_bit + 1
```

For a **terminator** witness additionally prove:

```text
next property_present = false
loop-control end = start + 1 bit
second stream bits consumed = 0
second payload bits consumed = 0
```

For a **continuation** witness prove only:

```text
next property_present = true
continuation exists
native probe stops immediately after that one bit
```

The native probe must not decode the second stream ID, resolve the second property header, or decode the second payload.

## 5. Negative and boundary controls

Required evidence controls:

- truncate exactly before the next `property_present` bit and require failure without cursor advance;
- mutate bits after the one-bit evidence stop and require identical result;
- invalid first-property/non-K1 inputs must remain rejected through the production R3.18B boundary;
- repeated runs over the same witness must be bit-exact and receipt-exact.

## 6. Privacy and artifact policy

Durable artifacts may contain replay identity hashes, frame/actor/property coordinates, bit ranges, decoded K1 semantic values where already non-sensitive, booleans, counts, mismatch summaries, and payload hashes.

Do not persist raw replay payload windows, player/account names, free-form title text, or other unnecessary cleartext replay content.

## 7. Mutation gate

This pass must leave unchanged:

```text
crates/mimir-replay/src/**
crates/mimir-replay/tests/**
Cargo.toml
Cargo.lock
external_fixtures/**
test_corpus/**
scripts/**
```

Disposable workflows/tools on an evidence branch are allowed but must never enter the clean production history.

## 8. Hard stop

R3.18C does **not** admit:

- any production Rust change;
- a production `property_present` loop;
- a second property stream/header/payload native decode;
- K2/K3/K4 composition through the R3.18B wrapper;
- next actor or next frame iteration;
- actor lifecycle table mutation;
- new attribute family/shape/context;
- raw-state/event/replay-slice/skill/runtime/export widening.

## 9. Outcome gate

### Outcome A

Both real terminator and continuation classes are proven when available, all native/oracle coordinates and one-bit values match exactly, negative controls pass, privacy/mutation gates pass, and same-head normal CI is green. Then continuity may open a separately specified minimal production loop-control pass. A generalized property loop is still not automatically admitted.

### Outcome B

The supported lane proves only part of the loop-control surface or lacks one required witness class. Record the bounded evidence and keep production at R3.18B.

### Outcome C

Any native/oracle coordinate mismatch, one-bit disagreement, source drift, privacy failure, unexpected mutation, or cursor ambiguity. Stop without production widening.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18C_EXECUTION_SPEC.md').write_text(spec, encoding='utf-8', newline='\n')

# ---------------------------------------------------------------------------
# Knowledge graph
# ---------------------------------------------------------------------------
p = ROOT / 'MIMIR_KNOWLEDGE_GRAPH.md'
g = p.read_text(encoding='utf-8')
g = replace_one(
    g,
    'R3.18A single-property evidence decision                    |\nR3.18B active single-property K1 composition spec             |',
    'R3.18A single-property evidence decision                    |\nR3.18B single-property K1 production decision                  |\nR3.18C active property-loop boundary evidence spec              |',
    'graph chain head',
)
g = replace_one(
    g,
    '''34. `docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md`
35. `docs/continuity/MIMIR_R3_18A_DECISION.md`
36. `docs/continuity/MIMIR_R3_18B_EXECUTION_SPEC.md`
37. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
38. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
39. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
40. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
41. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
42. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
43. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`''',
    '''34. `docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md`
35. `docs/continuity/MIMIR_R3_18A_DECISION.md`
36. `docs/continuity/MIMIR_R3_18B_EXECUTION_SPEC.md`
37. `docs/continuity/MIMIR_R3_18B_DECISION.md`
38. `docs/continuity/MIMIR_R3_18C_EXECUTION_SPEC.md`
39. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
40. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
41. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
42. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
43. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
44. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
45. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`''',
    'reading order',
)
g = replace_one(
    g,
    ''' -> R3.18B minimal native existing-actor single-property K1 composition: ACTIVE / PRODUCTION
      compose existing R3.16B header + existing R3.17C K1 decoder only; property loop remains closed''',
    f''' -> R3.18B minimal native existing-actor single-property K1 composition: PRODUCTION / CLOSED
      production {BASE_MAIN} / tree {BASE_TREE}
      lib/test blobs {LIB_BLOB} / {TEST_BLOB}
      exact candidate {EXACT_RUN} / {EXACT_JOB} SUCCESS
      published main CI {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
      published validator {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
      K1-only one-property composition / 8/8 focused PASS / next-property bits consumed 0
 -> R3.18C existing-actor property-loop terminator/continuation evidence: ACTIVE / READ-ONLY
      prove native stop == next property_present start and consume exactly one terminator/continuation bit; second stream/header/payload remains closed''',
    'decoder chain R3.18B',
)
g = replace_one(
    g,
    '''Production at `492cc8218be7abc6db8f75acaea33d009ab2f175` can natively decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload. Every success stops exactly at its one-value end bit and does not authorize another property, actor, frame or lifecycle mutation. R3.17P has now certified all 161 exact K4 groups against regenerated real-replay witnesses with zero mismatch; R3.18A is evidence-only and does not widen production.''',
    f'''Production at `{BASE_MAIN}` adds the R3.18B one-property K1 wrapper: an existing actor's first property header can now be composed with exactly one Boolean/Byte/Enum/Float/Int/Int64 scalar payload and returned at the exact payload end. Separate K2/K3/K4 one-value decoders remain authoritative at their existing boundaries, but the R3.18B wrapper deliberately rejects those tags before payload read. No next property bit, second property, actor, frame or lifecycle mutation is production-admitted.''',
    'capability lock production paragraph',
)
g = replace_one(
    g,
    '''R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups; R3.17K implemented them; R3.17L matched all 1,950 against real replay witnesses. R3.17M then observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups; R3.17N admitted those 161 groups byte-for-byte; R3.17O implemented exactly that contract with zero cross-product widening; R3.17P then matched all 161 exact K4 groups against real replay witnesses with zero mismatch. R3.18A proved one complete real existing-actor property boundary with an Int payload, exact end cursor, and zero next-property bits consumed. R3.18B may now publish only the minimal K1 single-property composition. Property-loop continuation, K2/K3/K4 composition in that new API, next actor/frame iteration and lifecycle mutation remain closed.''',
    '''R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups; R3.17K implemented them; R3.17L matched all 1,950 against real replay witnesses. R3.17M then observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups; R3.17N admitted those 161 groups byte-for-byte; R3.17O implemented exactly that contract with zero cross-product widening; R3.17P then matched all 161 exact K4 groups against real replay witnesses with zero mismatch. R3.18A proved one complete real existing-actor property boundary with an Int payload and zero next-property bits consumed. R3.18B published the minimal K1 one-property composition. R3.18C is now read-only evidence for the next one-bit loop-control edge; production property-loop continuation, second property payloads, K2/K3/K4 wrapper composition, next actor/frame iteration and lifecycle mutation remain closed.''',
    'capability history paragraph',
)
old_tail = '''R3.18B is now the first dependency-valid unfinished roadmap step: production composition of the existing first-property header with exactly one K1 primitive scalar payload. It must stop at the payload end; the property loop remains unadmitted.'''
new_tail = f'''## R3.18B single-property K1 production closure

```text
production SHA              {BASE_MAIN}
production tree             {BASE_TREE}
parent                      {PARENT}
lib.rs blob                 {LIB_BLOB}
focused test blob           {TEST_BLOB}
implementation run/job      {IMPL_RUN} / {IMPL_JOB} SUCCESS
exact candidate validation  {EXACT_RUN} / {EXACT_JOB} SUCCESS
published main CI           {MAIN_CI_RUN} / {MAIN_CI_JOB} SUCCESS
published validator         {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
focused tests               8/8 PASS
wrapper tags                Boolean/Byte/Enum/Float/Int/Int64
next-property bits          0
clean files                 2
Cargo/fixture/corpus/
support/workflow/docs       0/0/0/0/0/0 mutations
outcome                     A / production
```

R3.18C is now the first dependency-valid unfinished roadmap step: read-only proof that the R3.18B stop bit is exactly the next `property_present` location, with one real terminator and one real continuation witness when available. The native evidence probe may consume only that one bit; a second stream/header/payload and production property loop remain unadmitted.'''
g = replace_one(g, old_tail, new_tail, 'graph tail next pass')
p.write_text(g, encoding='utf-8', newline='\n')

print('R3_18B_CONTINUITY_GENERATION=PASS')
