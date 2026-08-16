from __future__ import annotations

import json
from pathlib import Path

PROD = '2b608aafae97b10ecbc884f99e4bd4a73abf7a5c'
TREE = 'b130caf211ce72577870c70d6c0d87cd006e1b29'
PARENT = '289c9cec0b709a27665370871dc7480b5df93270'
LIB = '5e2b9e5be9c6692e499abc97a89655c603728cef'
TEST = 'd56bf97d250b426e23fec4610cbb9ead6ec8a142'
IMPL_RUN = 31957142924
IMPL_JOB = 95189376563
NORMAL_RUN = 31957142895
NORMAL_JOB = 95189376551
EXACT_RUN = 31957646865
EXACT_JOB = 95190626723
PUBLISHED_RUN = 31957892048
PUBLISHED_JOB = 95191254798


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one anchor, found {count}: {old[:120]!r}')
    return text.replace(old, new, 1)

# 1) Machine-readable continuity state.
state_path = Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-16'
state['last_production_code_sha'] = PROD
state['last_production_milestone'] = 'R3.18G'
state['last_production_milestone_name'] = 'minimal native existing-actor bounded second-property header composition'
state['current_pass'] = 'R3.18H'
state['current_pass_kind'] = 'read-only evidence / production R3.18G second-property-header real-replay differential audit'
state['current_pass_goal'] = 'Differentially validate the published R3.18G optional second-header composition over the frozen 47-replay R3.18F terminator/continuation lane through second payload_start only.'
state['current_pass_stop_boundary'] = 'Stop at R3.18G terminator control end or continuation second-header payload_start. Second payload bits, third property, repeated loop, next actor/frame/lifecycle/raw-state/event/skill/runtime/export widening remain forbidden.'
state['r3_18g'] = {
    'outcome': 'A — admitted / production',
    'pre_pass_main_sha': PARENT,
    'production_sha': PROD,
    'production_tree': TREE,
    'lib_rs_blob': LIB,
    'focused_test_blob': TEST,
    'implementation_run': IMPL_RUN,
    'implementation_job': IMPL_JOB,
    'same_trigger_normal_ci_run': NORMAL_RUN,
    'same_trigger_normal_ci_job': NORMAL_JOB,
    'exact_live_candidate_validator_run': EXACT_RUN,
    'exact_live_candidate_validator_job': EXACT_JOB,
    'published_main_validator_run': PUBLISHED_RUN,
    'published_main_validator_job': PUBLISHED_JOB,
    'clean_scope': [
        'crates/mimir-replay/src/lib.rs',
        'crates/mimir-replay/tests/r3_18g_second_property_header.rs',
    ],
    'lib_additions': 157,
    'focused_test_additions': 363,
    'reused_decoder_calls': 2,
    'payload_decoder_calls': 0,
    'property_loops': 0,
    'second_header_tag_allowlist': ['Int', 'String'],
    'terminator_returns_none_before_header_lookup': True,
    'continuation_stops_at_payload_start': True,
    'second_payload_admitted': False,
    'third_property_admitted': False,
    'superseded_non_authority_candidate_receipt': 'fc59508291c43a6f08b3667f92cd1c7b665dc3d4',
}
read_order = state.get('next_files_to_read', [])
for entry in [
    'docs/continuity/MIMIR_R3_18G_DECISION.md',
    'docs/continuity/MIMIR_R3_18H_EXECUTION_SPEC.md',
]:
    if entry not in read_order:
        try:
            pos = read_order.index('docs/continuity/MIMIR_PASS_PROTOCOL.md')
        except ValueError:
            pos = len(read_order)
        read_order.insert(pos, entry)
state['next_files_to_read'] = read_order
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# 2) Current-state compact canonical summary.
Path('docs/continuity/MIMIR_CURRENT_STATE.md').write_text(f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production tree:** `{TREE}`
**Production milestone:** `R3.18G — minimal native existing-actor bounded second-property header composition`
**Completed second-header evidence:** `R3.18F — Outcome A / 47/47 continuation headers exact / 47/47 terminators / 32 truncation negatives / mismatch 0 / second payload + third property 0 + 0`
**Current exact pass:** `R3.18H — production second-header real-replay differential audit`

## 1. Truthful production boundary

R3.18G is published production at `{PROD}`. It composes an already-valid R3.18B first primitive property with the published R3.18D next-property control and, only when that control is true, one existing property-header primitive. Terminators return `None` at the control end without second-header lookup. Continuations admit only the exact R3.18F-observed `Int` / `String` header contexts and stop exactly at second `payload_start`. `String` is header resolution only; no String/K2 payload decoder is called.

```text
production SHA/tree                 {PROD} / {TREE}
parent                              {PARENT}
lib.rs blob                         {LIB}
R3.18G focused test blob            {TEST}
implementation run/job              {IMPL_RUN} / {IMPL_JOB} SUCCESS
same-trigger normal CI              {NORMAL_RUN} / {NORMAL_JOB} SUCCESS
exact live-candidate validator      {EXACT_RUN} / {EXACT_JOB} SUCCESS
published-main validator            {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
clean production scope              lib.rs + r3_18g focused test only
payload decoder calls / loops       0 / 0
```

The earlier `fc595082...` candidate receipt is not authority. Fresh branch truth was `{PROD}`, and the exact-live validator plus force-free publication were performed against that live SHA.

## 2. R3.18H exact next pass

R3.18H is read-only evidence. Reuse the frozen R3.18F 47-replay terminator/continuation lane and pinned Boxcars oracle. Differentially run the **published R3.18G production API**:

- 47 terminators must return `second_header=None`, stop exactly after the control bit and perform no second-header lookup;
- 47 continuations must exactly match control coordinates plus second-header stream/object/tag/payload-start coordinates;
- continuation tag distribution must remain exactly `Int=46`, `String=1` on the frozen lane;
- native/oracle mismatch must be zero;
- second payload and third-property consumption must remain `0 / 0`;
- truncation, unresolved-stream, disallowed-tag, post-stop poison and repeatability controls must fail closed or remain invariant as appropriate;
- production/Cargo/fixture/corpus/support files must remain unchanged.

## 3. Still closed

```text
second-property payload decode / semantic value claim
third property or repeated/generalized property loop
generic repeatedly-chainable property cursor
second-header tag contexts outside exact Int/String for the R3.18G composition
K2/K3/K4 dispatch through the R3.18B wrapper
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/fixture/corpus/support/dependency expansion
```
''', encoding='utf-8', newline='\n')

# 3) Production decision.
Path('docs/continuity/MIMIR_R3_18G_DECISION.md').write_text(f'''# MIMIR R3.18G — Bounded Second-Property Header Production Decision

**Date:** 2026-08-16  
**Outcome:** **A — ADMITTED / PRODUCTION**  
**Production SHA:** `{PROD}`  
**Production tree:** `{TREE}`

## Decision

R3.18G is admitted. The clean production commit adds one deliberately non-generic composition after an already-valid R3.18B first primitive property. It reuses the published R3.18D control decoder and existing property-header primitive, returns `None` immediately for a false next-property control, or returns exactly one second header for a true control and stops at that header's `payload_start`.

The composition admits only the exact R3.18F-observed second-header contexts `Int` and `String`. `String` is a resolved header tag only. No scalar/K2/K3/K4 payload decoder is invoked for the second property. No third-property access or property loop exists.

## Exact authority

```text
pre-pass main                       {PARENT}
production SHA/tree                 {PROD} / {TREE}
lib.rs blob                         {LIB}
focused test blob                   {TEST}
implementation run/job              {IMPL_RUN} / {IMPL_JOB} SUCCESS
same-trigger normal CI              {NORMAL_RUN} / {NORMAL_JOB} SUCCESS
exact live candidate validator      {EXACT_RUN} / {EXACT_JOB} SUCCESS
published-main validator            {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
```

The publication authority is the fresh live clean branch SHA `{PROD}`. An earlier log receipt named `fc59508291c43a6f08b3667f92cd1c7b665dc3d4`; it was superseded by live branch truth and was not used for publication.

## Clean scope

Exactly two production files changed from `{PARENT}`:

1. `crates/mimir-replay/src/lib.rs` — +157 / -0
2. `crates/mimir-replay/tests/r3_18g_second_property_header.rs` — +363 / -0

Cargo manifests/lockfile, fixtures, corpus, docs, workflows and support tooling were absent from the clean production commit.

## Admitted behavior

- false next-property control -> `second_header=None`, exact one-bit control stop, no second-header lookup;
- true next-property control -> exactly one property-header primitive at the same control bit;
- exact control/header present-coordinate agreement;
- same actor-object agreement with the first property;
- exact second-header tag allowlist `Int | String`;
- exact stop `header.stop_bit == payload_start_bit`;
- zero second-payload decoder calls;
- zero property loops / third-property access.

Focused R3.18G tests, full `mimir-replay`, workspace check/test/clippy and full repository verification passed on the exact live candidate and again on the exact published main.

## Hard stop

R3.18G does **not** admit second-property payload bits or semantic values, a third property, a repeated/generalized loop, generic cursor chaining, any second-header tag context outside `Int/String`, K2/K3/K4 wrapper composition, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening, or dependency/scope expansion.

## Next gate

R3.18H is a separate read-only real-replay differential audit of the **published R3.18G production API** on the frozen R3.18F terminator/continuation lane. No second-property payload admission may occur until that evidence closes and a later pass explicitly opens a new contract.
''', encoding='utf-8', newline='\n')

# 4) Next evidence-pass spec.
Path('docs/continuity/MIMIR_R3_18H_EXECUTION_SPEC.md').write_text(f'''# MIMIR R3.18H — Production Second-Property Header Real-Replay Differential Audit

**Status:** ACTIVE  
**Pass type:** read-only evidence / differential validation  
**Production authority:** R3.18G `{PROD}`  
**Production mutation:** forbidden  
**Second-property payload decode:** forbidden  
**Third property / repeated loop:** forbidden

## 1. Goal

Differentially validate the published R3.18G optional second-property-header composition over the frozen 47-replay R3.18F lane. Prove production behavior, not the lower-level header primitive in isolation.

## 2. Frozen authority

```text
production SHA/tree                 {PROD} / {TREE}
production parent                   {PARENT}
lib.rs blob                         {LIB}
R3.18G focused test blob            {TEST}
R3.18G implementation               {IMPL_RUN} / {IMPL_JOB} SUCCESS
R3.18G same-trigger normal CI       {NORMAL_RUN} / {NORMAL_JOB} SUCCESS
R3.18G exact candidate validator    {EXACT_RUN} / {EXACT_JOB} SUCCESS
R3.18G published-main validator     {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
R3.18F evidence head/tree           27a855a9cfb82a0294dd1601e4da01c9fdfad264 / 4058b67da82e9fbfcc078e975b26d186ec68e6f0
R3.18F artifact                     9264673141
R3.18F artifact digest              sha256:e31e09abf322b6458f9034b06efe5502bb3b7f1011dfb08c9ffd6d1b1cd1b361
R3.18F source-scope SHA256          492f63c3cfcb27967426816f97858c8f4ad1d9ebb6ce40719f6d829ff3f0ea55
R3.18F replay-identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
R3.18F witnesses SHA256             99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
R3.18F aggregate SHA256             57c90cb3617461aea1a078a7b0f72ae301fd35fc9d7c4f9fe56de6d7633a4a04
```

Before evidence, fetch fresh `main`, prove production source blobs unchanged from `{PROD}`, verify every receipt above, and verify the 47 replay identities against the frozen lane.

## 3. Required source lane

Reuse the frozen R3.18F 94-row boundary set:

```text
47 terminator rows
47 continuation rows
continuation second-header tags: Int=46 / String=1
```

Do not silently reselect easier witnesses. If any frozen replay or boundary no longer reproduces, that is evidence drift and must stop the pass.

## 4. Production differential checks

For every terminator row, invoke the published R3.18G composition and require:

- the first R3.18B property is exact;
- R3.18D control coordinates/value are exact;
- `next_property_present == false`;
- `second_header == None`;
- stop equals the one-bit control end;
- no second-header lookup or payload access occurs after the false bit.

For every continuation row, require:

- the first R3.18B property is exact;
- R3.18D control coordinates/value are exact and true;
- a second header is returned;
- second `property_present` start/end exact;
- stream start/end/value, stream bound and prop-id bits exact;
- resolved property object exact;
- resolved tag exact, with aggregate distribution exactly `Int=46 / String=1`;
- `payload_start_bit` exact;
- returned `stop_bit == payload_start_bit` exact;
- zero second-payload bits consumed;
- zero third-property bits consumed.

Native/oracle mismatch count must be zero.

## 5. Negative controls

At minimum:

- truncation before all required continuation header bits -> reject atomically;
- unresolved second stream -> reject before payload;
- second-header tag outside exact `Int/String` -> reject before payload;
- terminator with poisoned/missing lookup plan after first property -> still return `None` without lookup;
- bits at and after continuation `payload_start` may be poisoned without changing the returned header;
- repeated identical invocation -> exact identical result.

Where a real frozen row can exercise truncation, prefer it. Synthetic controls may supplement but may not replace real-lane differential checks.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing at least:

- exact production SHA/tree/blobs and validation receipts;
- pinned Boxcars SHA;
- frozen replay identity/source-scope hashes;
- per-row oracle/native comparison without raw private payload windows;
- aggregate terminator/continuation counts;
- exact tag counts;
- negative-control results;
- second-payload / third-property consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- hashes for every evidence file in the artifact.

## 7. Required validation

- deterministic double-run equality of the evidence selection/comparison;
- production focused R3.18G tests PASS on the evidence head;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18H may not change production Rust, Cargo files, fixtures, corpus, dependencies or support lanes. It may not decode or semantically claim the second payload, inspect a third property, create a property loop, widen second-header tags, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 94 frozen rows match the published R3.18G production composition exactly, negatives pass, mismatch is zero, second-payload/third-property consumption remains `0/0`, privacy passes and production mutation is zero. Admit R3.18H evidence and only then define the next separate bounded pass.

### Outcome B

A reproducible production/oracle mismatch appears within the already-admitted R3.18G boundary. Record exact privacy-safe coordinates and keep any further payload/loop widening closed.

### Outcome C

Authority drift, source mutation, witness reselection, privacy failure, second-payload access, third-property access, tag widening or validation contradiction. Stop without admission.
''', encoding='utf-8', newline='\n')

# 5) Knowledge graph: promote G, add H to graph/reading order/replay chain.
kg_path = Path('MIMIR_KNOWLEDGE_GRAPH.md')
kg = kg_path.read_text(encoding='utf-8')
kg = replace_once(
    kg,
    'R3.18F second-property-header evidence decision                        |\nR3.18G active bounded second-property-header production spec              |',
    'R3.18F second-property-header evidence decision                        |\nR3.18G bounded second-property-header production decision                    |\nR3.18H active production second-header differential spec                      |',
    'KG graph tail',
)
kg = replace_once(
    kg,
    '46. `docs/continuity/MIMIR_R3_18G_EXECUTION_SPEC.md`\n47. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n48. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n49. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n50. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n51. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n52. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n53. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`',
    '46. `docs/continuity/MIMIR_R3_18G_EXECUTION_SPEC.md`\n47. `docs/continuity/MIMIR_R3_18G_DECISION.md`\n48. `docs/continuity/MIMIR_R3_18H_EXECUTION_SPEC.md`\n49. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n50. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n51. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n52. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n53. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n54. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n55. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`',
    'KG reading order',
)
kg = replace_once(
    kg,
    ' -> R3.18G bounded optional second-property-header composition: ACTIVE / PRODUCTION IMPLEMENTATION\n      compose one R3.18D control + at most one existing header primitive; terminator None or continuation stop at payload_start; only exact observed Int/String headers; second payload and third property forbidden',
    f''' -> R3.18G bounded optional second-property-header composition: PRODUCTION / CLOSED
      production {PROD} / tree {TREE}
      lib/test blobs {LIB} / {TEST}
      implementation {IMPL_RUN} / {IMPL_JOB} SUCCESS; same-trigger CI {NORMAL_RUN} / {NORMAL_JOB} SUCCESS
      exact live candidate validator {EXACT_RUN} / {EXACT_JOB} SUCCESS; published validator {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
      exactly two reused decoder calls / zero payload decoder calls / zero property loops / Int+String header contexts only / second payload + third property still closed
 -> R3.18H production second-header real-replay differential audit: ACTIVE / READ-ONLY EVIDENCE
      reuse frozen R3.18F 47 terminator + 47 continuation rows against published R3.18G; require 94/94 exact, Int=46/String=1, mismatch 0 and second-payload/third-property bits 0/0''',
    'KG replay chain tail',
)
kg_path.write_text(kg, encoding='utf-8', newline='\n')

# 6) Master handbook: update current-state fields and hard-stop wording, then append a fresh active checklist.
book_path = Path('MIMIR_CONTINUE_HERE.md')
book = book_path.read_text(encoding='utf-8')
book = replace_once(book, 'LAST_PRODUCTION_CODE_SHA:\n  4adadd185783954c7fb6ad67db14b77b377cdde5', f'LAST_PRODUCTION_CODE_SHA:\n  {PROD}', 'book production sha')
book = replace_once(book, 'LAST_PRODUCTION_MILESTONE:\n  R3.18D — minimal native existing-actor next-property control bit', 'LAST_PRODUCTION_MILESTONE:\n  R3.18G — minimal native existing-actor bounded second-property header composition', 'book milestone')
book = replace_once(book, 'CURRENT_PASS:\n  R3.18G — minimal native existing-actor second-property-header composition', 'CURRENT_PASS:\n  R3.18H — production second-property-header real-replay differential audit', 'book current pass')
book = replace_once(book, 'CURRENT_PASS_TYPE:\n  production implementation / bounded optional second-property header after one valid R3.18B first primitive property; stop at second payload_start', 'CURRENT_PASS_TYPE:\n  read-only evidence / differential validation of published R3.18G over the frozen R3.18F 47-replay terminator/continuation lane', 'book pass type')
book = replace_once(
    book,
    '  R3.18G may publish only one bounded optional second-property header after a valid first primitive property and R3.18D control; continuation second-header tag admission is limited to the exact R3.18F observed set Int/String; this is header resolution only and does not admit either payload family\n  NO second-property payload decode, third property, repeated/generalized property loop, K2/K3/K4 wrapper composition, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted',
    f'''  R3.18G is production at {PROD}: after one valid R3.18B first primitive property it reuses R3.18D control plus at most one existing header primitive; terminator returns None before header lookup; continuation stops exactly at second payload_start; exact header contexts Int/String only
  R3.18G exact-live validator {EXACT_RUN}/{EXACT_JOB} and published validator {PUBLISHED_RUN}/{PUBLISHED_JOB} are SUCCESS; payload decoder calls 0; property loops 0
  R3.18H is read-only differential validation of that published production API over the frozen 47 terminator + 47 continuation lane; second payload and third-property consumption must remain 0/0
  NO second-property payload decode, third property, repeated/generalized property loop, K2/K3/K4 wrapper composition, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted''',
    'book hard stop',
)
append = f'''

---

# R3.18G PRODUCTION CLOSURE — 2026-08-16

```text
Outcome: A — ADMITTED / PRODUCTION
production SHA/tree: {PROD} / {TREE}
parent: {PARENT}
lib.rs blob: {LIB}
focused test blob: {TEST}
implementation run/job: {IMPL_RUN} / {IMPL_JOB} SUCCESS
same-trigger normal CI: {NORMAL_RUN} / {NORMAL_JOB} SUCCESS
exact live-candidate validator: {EXACT_RUN} / {EXACT_JOB} SUCCESS
published-main validator: {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
clean scope: lib.rs + r3_18g focused test only
source boundary: 2 reused decoder calls / 0 payload decoder calls / 0 loops
second-header contexts: Int / String only
second payload / third property: CLOSED / CLOSED
```

The live clean candidate `{PROD}` superseded an earlier non-authority log receipt `fc595082...`; publication and validation used fresh branch truth.

# CURRENT PASS CHECKLIST — R3.18H

- [ ] Fresh-read `main`; require `{PROD}` production source/tree/blobs or continuity-only commits after it.
- [ ] Freeze pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b` and all R3.18F artifact/source/replay/witness hashes.
- [ ] Reuse exactly 47 terminator + 47 continuation frozen rows; no silent witness reselection.
- [ ] Differentially invoke the **published R3.18G composition** on all 94 rows.
- [ ] Terminators: `None`, exact one-bit control stop, no second-header lookup.
- [ ] Continuations: exact control + stream/object/tag/payload_start; exact aggregate `Int=46 / String=1`.
- [ ] Require native/oracle mismatch `0`.
- [ ] Require second-payload / third-property bits consumed `0 / 0`.
- [ ] Run real truncation plus unresolved-stream, disallowed-tag, poison and repeatability negatives.
- [ ] Produce privacy-safe immutable evidence artifact and per-file SHA256 receipt.
- [ ] Run focused/full/workspace/clippy/full verifier on the exact evidence head.
- [ ] Require same exact evidence head normal CI SUCCESS.
- [ ] Require production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.
- [ ] Only after Outcome A update continuity/KG; do not open second payload inside R3.18H.
'''
if '# R3.18G PRODUCTION CLOSURE — 2026-08-16' in book:
    raise SystemExit('book already contains R3.18G closure')
book += append
book_path.write_text(book, encoding='utf-8', newline='\n')

print('R3_18G_CONTINUITY_GENERATION=PASS')
