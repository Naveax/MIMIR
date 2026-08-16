from pathlib import Path
import json

ROOT = Path('.')
BASE_MAIN = 'c5878cf755302fe52e9e67741486306cd30db059'
PROD = '492cc8218be7abc6db8f75acaea33d009ab2f175'
AUTH = '12ee215fd843260d5ece14f27aa1171cb862f49e'
RUN = 31941400273
JOB = 95151024131
CI_RUN = 31941400276
CI_JOB = 95151024211
ARTIFACT = 9262129856
DIGEST = 'sha256:295247a5f73159ac74539ffc5abf1eb2273fb6dc07a57f8b16976552a17b3ab8'


def replace_one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one match, got {count}')
    return text.replace(old, new, 1)


# Master continuity handbook.
p = ROOT / 'MIMIR_CONTINUE_HERE.md'
s = p.read_text(encoding='utf-8')
s = replace_one(
    s,
    'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.17M — K4 gameplay-structured wire-format evidence / Outcome A / 39463 occurrences / 161 exact groups',
    'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18A — existing-actor single-property boundary evidence / Outcome A / one real Int property / exact end cursor / 0 next-property bits',
    'last evidence pass',
)
s = replace_one(
    s,
    'CURRENT_PASS:\n  R3.18A — existing-actor single-property boundary evidence\n\nCURRENT_PASS_TYPE:\n  read-only real-replay evidence / one complete existing-actor property payload + exact end cursor',
    'CURRENT_PASS:\n  R3.18B — minimal native existing-actor single-property K1 composition\n\nCURRENT_PASS_TYPE:\n  production implementation / first property-present header + exactly one K1 primitive scalar payload',
    'current pass',
)
s = replace_one(
    s,
    '  R3.17P certified the published R3.17O K4 decoder on all 161 exact real-replay groups; R3.18A may now prove exactly one complete existing-actor property boundary without looping\n  NO second property, next actor, next frame, lifecycle mutation, unobserved K2/K3/K4 shape or family is admitted',
    '  R3.17P certified the published R3.17O K4 decoder on all 161 exact real-replay groups; R3.18A then proved one real existing-actor property header + Int payload through the exact end cursor with 0 next-property bits consumed\n  R3.18B may compose only the existing first-property header with the already-admitted K1 primitive scalar decoder; K2/K3/K4 composition and every property loop remain closed\n  NO second property, next actor, next frame, lifecycle mutation, unobserved shape/family, or extra context inference is admitted',
    'production hard stop',
)
old = '''R3_18A_OPEN_BOUNDARY:
  read-only existing-actor single-property boundary evidence; production mutation forbidden
  select a deterministic real existing-actor update with property_present=true from the supported replay lane
  prove the already-resolved stream/property/tag context at the exact payload start
  decode exactly one already-admitted K1/K2/K3/K4 payload and require native payload_end_bit == pinned Boxcars oracle end bit
  stop before consuming the next property_present bit; this pass does not admit a property loop

R3_18A_HARD_STOP:
  no production Rust, Cargo, fixture, corpus or support-lane mutation
  no second property and no consumption of the next property_present bit
  no next actor / next frame / actor-table lifecycle mutation
  no new attribute family/shape/context admission
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.18A:
  only after Outcome A, admit the minimal production one-property composition needed by roadmap R3.18; property-loop continuation remains a later separately evidenced step
'''
new = f'''R3_18A_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at {PROD}
  execution base main: {BASE_MAIN}
  authority head: {AUTH}
  authority run/job: {RUN} / {JOB} SUCCESS
  exact-head normal CI: {CI_RUN} / {CI_JOB} SUCCESS
  artifact: {ARTIFACT}
  artifact digest: {DIGEST}
  replay identity + pinned Boxcars parse: 47/47
  deterministic eligible first-property scalar candidates: 47
  selected witness: external_fixtures/sample_001.replay / frame 0 / actor ordinal 63 / actor id 2 / actor context object 98
  selected property: ordinal 0 / stream 27 of bound 67 / property object 55 / Int / value 62
  property_present bits: [10227,10228); stream bits: [10228,10234); payload bits: [10234,10266) / width 32
  payload SHA256: d2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f
  native header/payload-start/semantic/payload-end equality: PASS/PASS/PASS/PASS
  next property_present consumed bits: 0; truncation negative: PASS; mismatch count: 0; privacy: PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_18B_OPEN_BOUNDARY:
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
s = replace_one(s, old, new, 'R3.18A boundary block')
p.write_text(s, encoding='utf-8', newline='\n')

# Machine-readable state.
p = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(p.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-16'
state['last_completed_evidence_pass'] = 'R3.18A'
state['last_completed_evidence_outcome'] = 'A — one real existing-actor first property composed through exact payload end; 47/47 replay identity/oracle parse; header/start/semantic/end exact; 0 next-property bits; mismatch 0'
state['current_pass'] = 'R3.18B'
state['current_pass_kind'] = 'production implementation / minimal existing-actor single-property K1 composition'
state['current_pass_goal'] = 'Compose the existing R3.16B first-property header with the already-admitted R3.17C K1 primitive scalar decoder, return the exact one-property end cursor, and stop before the next property_present bit.'
state['current_pass_stop_boundary'] = 'Exactly one property_present=true header plus one K1 Boolean/Byte/Enum/Float/Int/Int64 payload. No second property/property loop, no K2/K3/K4 composition in the new API, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening, or Cargo/fixture/corpus/support changes.'
state['r3_18a'] = {
    'outcome': 'A — admitted / evidence complete',
    'pass_type': 'read-only real-replay existing-actor single-property boundary evidence',
    'production_source_changed': False,
    'continuity_base_sha': BASE_MAIN,
    'production_sha': PROD,
    'authority_head': AUTH,
    'workflow_run': RUN,
    'workflow_job': JOB,
    'exact_head_ci_run': CI_RUN,
    'exact_head_ci_job': CI_JOB,
    'artifact_id': ARTIFACT,
    'artifact_digest': DIGEST,
    'supported_replays': 47,
    'oracle_parse_success': 47,
    'eligible_first_property_scalar_candidates': 47,
    'selected_replay': 'external_fixtures/sample_001.replay',
    'frame_index': 0,
    'actor_ordinal': 63,
    'actor_id': 2,
    'actor_context_object_id': 98,
    'property_ordinal': 0,
    'stream_id': 27,
    'stream_id_bound': 67,
    'prop_id_bits': 6,
    'property_object_id': 55,
    'attribute_tag': 'Int',
    'lossless_value': '62',
    'property_present_start_bit': 10227,
    'property_present_end_bit': 10228,
    'stream_id_start_bit': 10228,
    'stream_id_end_bit': 10234,
    'payload_start_bit': 10234,
    'payload_end_bit': 10266,
    'payload_width': 32,
    'payload_sha256': 'd2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f',
    'property_header_identity_exact': True,
    'payload_start_exact': True,
    'semantic_value_exact': True,
    'payload_end_exact': True,
    'next_property_present_consumed_bits': 0,
    'truncation_negative': 'PASS',
    'mismatch_count': 0,
    'privacy': 'PASS',
    'production_cargo_fixture_corpus_support_mutation': '0/0/0/0/0',
    'source_scope_sha256': '1d8cce3aa2dd0d16f6ddd04a1b03f8e1fc3aa9ff231b2c224611b1cbda492ac9',
    'replay_identity_sha256': 'b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf',
    'boxcars_instrumentation_receipt_sha256': '97c2d07c16c7367e76e5f42a2383ee58e0aa970edcb04fa877ab6a24e49b5e44',
    'selected_witness_sha256': 'e67b93106d2c880db20ec6d80b788a78ca9753e271d64882128ff5a886386364',
    'selection_summary_sha256': '33b93011ffded48a1a2a25a477cf5b16f0886394ebb160cdb377f26fffcc783f',
    'comparison_sha256': 'ae6167b401e84fdd33383fb9fc3294dc472d2fafb0d58377cc021a7db4bd9194',
    'aggregate_sha256': 'f29bec6fc775b87f339bce94fde3a9ed9e10e46d78141e1299fcce1c4441e18b',
    'next_pass': 'R3.18B',
}
reads = state.get('next_files_to_read', [])
anchor = 'docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md'
for item in ['docs/continuity/MIMIR_R3_18A_DECISION.md', 'docs/continuity/MIMIR_R3_18B_EXECUTION_SPEC.md']:
    if item in reads:
        reads.remove(item)
idx = reads.index(anchor) + 1
reads[idx:idx] = ['docs/continuity/MIMIR_R3_18A_DECISION.md', 'docs/continuity/MIMIR_R3_18B_EXECUTION_SPEC.md']
state['next_files_to_read'] = reads
p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# Current-state summary: intentionally concise and current.
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.17O — direct native exact-contract K4 decoder implementation`
**Completed K4 differential:** `R3.17P — Outcome A / 161/161 real-replay exact groups / 0 mismatch`
**Completed single-property evidence:** `R3.18A — Outcome A / real existing-actor Int property / exact header + payload end / 0 next-property bits`
**Current exact pass:** `R3.18B — minimal native existing-actor single-property K1 composition`

## 1. Truthful production boundary

Production remains R3.17O. MIMIR can decode one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload. R3.17P certified K4 on all 161 exact real-replay groups. R3.18A proved that an existing-actor first-property header can be composed with an already-admitted payload decoder through the exact payload end without consuming the next property bit. **That evidence did not itself widen production.**

```text
production SHA               {PROD}
production tree              a66c47d7fb58da508188e64d42141987a0021a07
lib.rs blob                  0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8
k4 groups blob               103503e25bc5af48381df021ab58133694fcece6
k4 native blob               a9c41f3bb11343165183ac9c815ab8fdf085936c
focused K4 test blob         70437244bb49224281ee3a2e745e7b8a4b7a093a
```

## 2. R3.18A evidence closure

```text
execution base main          {BASE_MAIN}
authority head               {AUTH}
authority run/job            {RUN} / {JOB} SUCCESS
exact-head normal CI         {CI_RUN} / {CI_JOB} SUCCESS
artifact                     {ARTIFACT}
artifact digest              {DIGEST}
replay identity/oracle       47/47
eligible candidates          47 deterministic first-property scalars
selected replay              external_fixtures/sample_001.replay
frame / actor ordinal / id   0 / 63 / 2
actor context object         98
stream / bound / prop bits   27 / 67 / 6
property object / tag/value  55 / Int / 62
property_present             [10227,10228)
stream                       [10228,10234)
payload                      [10234,10266) / 32 bits
payload SHA256               d2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f
header/start/semantic/end    exact / exact / exact / exact
next property bits consumed  0
truncation negative          PASS
mismatch / privacy           0 / PASS
prod/Cargo/fixture/corpus/
support mutation             0/0/0/0/0
```

The first disposable R3.18A run was not authority because temporary probe formatting failed before native comparison. A later evidence run produced valid Outcome-A data but its same-head normal CI rejected a temporary example API newer than the Rust 1.85 MSRV. The final authority head reran every substantive gate after replacing that tooling-only API.

## 3. R3.18B exact next pass

R3.18B is a narrow production composition pass. Reuse the existing R3.16B first-property header reader, require `property_present == true`, resolve the existing stream/property/tag through the lookup plan, then dispatch **only** the six already-admitted K1 primitive scalar tags to the existing R3.17C decoder:

```text
Boolean
Byte
Enum
Float
Int
Int64
```

Return the exact one-property payload end and set the composition stop bit to that same end. Unsupported K2/K3/K4 tags must fail closed in this new API even though their separate one-value decoders already exist. The next `property_present` bit remains opaque and unread.

## 4. Still closed

```text
second property / property_present loop
K2/K3/K4 dispatch in the R3.18B composition API
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

# Decision and next execution spec.
decision = f'''# MIMIR — R3.18A Decision

**Date:** 2026-08-16
**Pass:** `R3.18A — existing-actor single-property boundary evidence`
**Outcome:** **A — ADMITTED / EVIDENCE COMPLETE**
**Production mutation:** none

## Decision

A real existing-actor update can be composed from the already-published R3.16B property header boundary through exactly one already-admitted primitive payload and stopped at the exact Boxcars payload end without reading the next `property_present` bit. This closes the evidence prerequisite for the first production one-property composition. It does **not** admit a property loop.

## Frozen authority

```text
execution base main          {BASE_MAIN}
production SHA               {PROD}
authority head               {AUTH}
authority run/job            {RUN} / {JOB} SUCCESS
exact-head normal CI         {CI_RUN} / {CI_JOB} SUCCESS
artifact                     {ARTIFACT}
artifact digest              {DIGEST}
pinned Boxcars               c70e77df7af81b436cb545d070bb90c82f562d0b
replay identity/oracle       47/47
eligible first properties    47 scalar candidates
```

## Selected real witness

```text
replay                       external_fixtures/sample_001.replay
frame                        0
actor ordinal / actor id     63 / 2
actor context object         98
property ordinal             0
stream id / bound            27 / 67
prop_id_bits                 6
property object              55
attribute tag                Int
semantic value               62
property_present bits        [10227,10228)
stream bits                  [10228,10234)
payload bits                 [10234,10266)
payload width                32
payload SHA256               d2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f
```

Native header identity, payload start, semantic value, and payload end all matched the pinned Boxcars oracle exactly. `next_property_present_consumed_bits = 0`, the truncated payload negative failed closed, mismatch count is 0, and the durable artifact passed the privacy gate.

## Scope and mutation audit

```text
production Rust              unchanged
Cargo manifest/lock          unchanged
fixtures                     unchanged
corpus                       unchanged
support lane                 unchanged
raw payload cleartext        not durable
production/Cargo/fixture/
corpus/support mutation      0/0/0/0/0
```

Receipt SHA-256 values:

```text
source scope                 1d8cce3aa2dd0d16f6ddd04a1b03f8e1fc3aa9ff231b2c224611b1cbda492ac9
replay identity              b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation      97c2d07c16c7367e76e5f42a2383ee58e0aa970edcb04fa877ab6a24e49b5e44
selected witness             e67b93106d2c880db20ec6d80b788a78ca9753e271d64882128ff5a886386364
selection summary            33b93011ffded48a1a2a25a477cf5b16f0886394ebb160cdb377f26fffcc783f
comparison                   ae6167b401e84fdd33383fb9fc3294dc472d2fafb0d58377cc021a7db4bd9194
aggregate                    f29bec6fc775b87f339bce94fde3a9ed9e10e46d78141e1299fcce1c4441e18b
```

## Non-authority attempts

The first disposable head stopped on rustfmt in the temporary native probe. The next head produced valid evidence but same-head normal CI rejected `usize::is_multiple_of` because it is newer than MIMIR's Rust 1.85 MSRV. Neither is authority. The final head `{AUTH}` reran the full oracle scan, native comparison, privacy/mutation gates and normal CI after the tooling-only correction.

## Next exact pass

`R3.18B — minimal native existing-actor single-property K1 composition`.

R3.18B may compose only the existing first-property header with the existing primitive K1 decoder. Property-loop continuation, K2/K3/K4 composition in this API, next actor/frame and lifecycle mutation remain closed.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18A_DECISION.md').write_text(decision, encoding='utf-8', newline='\n')

spec = f'''# MIMIR R3.18B — Minimal Native Existing-Actor Single-Property K1 Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18A Outcome A
**Property loop:** forbidden

## 1. Goal

Publish the smallest production composition that starts at an existing actor's first `property_present` bit, resolves one property with the already-published R3.16B header logic, decodes exactly one already-admitted K1 primitive scalar with the already-published R3.17C decoder, returns the exact payload end cursor, and stops.

This pass is glue between two already-authoritative native boundaries. It must not fork or reimplement either wire codec.

## 2. Frozen authority

```text
canonical main before pass   {BASE_MAIN}
production SHA               {PROD}
R3.18A authority head        {AUTH}
R3.18A run/job               {RUN} / {JOB} SUCCESS
R3.18A exact-head CI         {CI_RUN} / {CI_JOB} SUCCESS
R3.18A artifact              {ARTIFACT}
R3.18A artifact digest       {DIGEST}
selected real tag/value      Int / 62
selected payload bits        [10234,10266)
next property bits consumed  0
```

Before mutation, re-read fresh `main`. If production blobs differ from R3.17O or canonical main is no longer the R3.18A continuity parent, stop and re-audit ancestry.

## 3. Admitted production composition

The new narrow API may:

```text
input: network bytes + first-property start bit + existing actor object index + current lookup plan
→ call the existing R3.16B first-property header decoder
→ require property_present == true
→ require a resolved property object + resolved attribute tag + payload_start_bit
→ accept only Boolean / Byte / Enum / Float / Int / Int64
→ call the existing R3.17C primitive scalar decoder at that exact payload_start_bit
→ return header identity + scalar result + stop_bit
→ require stop_bit == scalar.payload_end_bit
```

It may not independently decode bounded stream IDs, reinterpret lookup inheritance, or copy the scalar wire implementation.

## 4. Fail-closed rules

Reject without successful composition on:

- `property_present == false`;
- unresolved/missing stream or property;
- resolved non-K1 tag, including every K2/K3/K4 tag;
- header truncation;
- payload truncation;
- start/range arithmetic failure.

The API must not read or inspect the bit at its returned `stop_bit`; poison bits after the payload must not affect the result.

## 5. Required tests

Focused tests must include:

```text
all six K1 tags                       positive
aligned + unaligned property start    positive
R3.18A-shaped Int=62 composition      positive
header fields preserved               exact
payload start/end/width/value         exact
stop_bit == payload_end_bit           exact
poison next-property/trailing bits     no effect
property absent                        reject
K2/K3/K4 resolved tag                  reject before payload dispatch
header truncation                      reject
payload truncation                     reject atomically
repeatability                          exact
```

Run the full `mimir-replay` suite, workspace check/test/clippy, and full repository verifier on the exact clean candidate SHA.

## 6. Production scope

Preferred clean production scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused R3.18B integration test under `crates/mimir-replay/tests/`

A separate source module is allowed only if direct source inspection shows it materially improves isolation without widening the API. No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane, runtime/export, or continuity file may enter the clean production commit.

## 7. Hard stop

R3.18B does **not** admit:

- a second property;
- reading the next `property_present` bit;
- a `property_present` loop;
- K2/K3/K4 dispatch through the new composition API;
- next actor or next frame;
- actor lifecycle table mutation;
- new attribute family/shape/context;
- raw-state/event/replay-slice/skill/runtime/export widening.

## 8. Outcome gate

### Outcome A

Clean production code implements only the boundary above, focused and full validation pass, exact production scope is audited, and publication is force-free. Then update continuity and open a separate **read-only property-loop evidence** pass.

### Outcome B

Implementation exposes a missing composition contract. Record it and keep production at R3.17O.

### Outcome C

Any native/oracle contradiction, source drift, unexpected mutation, or inability to preserve the hard stop. Stop without publication.
'''
(ROOT / 'docs/continuity/MIMIR_R3_18B_EXECUTION_SPEC.md').write_text(spec, encoding='utf-8', newline='\n')

# Knowledge graph.
p = ROOT / 'MIMIR_KNOWLEDGE_GRAPH.md'
g = p.read_text(encoding='utf-8')
g = replace_one(
    g,
    'R3.17P K4 differential decision                     |\nR3.18A active single-property evidence spec               |',
    'R3.17P K4 differential decision                     |\nR3.18A single-property evidence decision                    |\nR3.18B active single-property K1 composition spec             |',
    'graph chain head',
)
g = replace_one(
    g,
    '''33. `docs/continuity/MIMIR_R3_17P_DECISION.md`
34. `docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md`
35. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
36. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
37. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
38. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
39. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
40. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
41. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`''',
    '''33. `docs/continuity/MIMIR_R3_17P_DECISION.md`
34. `docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md`
35. `docs/continuity/MIMIR_R3_18A_DECISION.md`
36. `docs/continuity/MIMIR_R3_18B_EXECUTION_SPEC.md`
37. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
38. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
39. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
40. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
41. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
42. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
43. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`''',
    'reading order',
)
g = replace_one(
    g,
    ''' -> R3.18A existing-actor single-property boundary evidence: ACTIVE / READ-ONLY
      prove exactly one complete real property payload and exact end cursor; stop before next property_present bit''',
    f''' -> R3.18A existing-actor single-property boundary evidence: OUTCOME A / CLOSED
      authority {AUTH} / {RUN} / {JOB} SUCCESS
      exact-head CI {CI_RUN} / {CI_JOB} SUCCESS
      artifact {ARTIFACT} / {DIGEST}
      47/47 oracle parse / 47 deterministic candidates / selected sample_001 Int=62 / header+start+semantic+end exact / next-property bits 0 / mismatch 0
 -> R3.18B minimal native existing-actor single-property K1 composition: ACTIVE / PRODUCTION
      compose existing R3.16B header + existing R3.17C K1 decoder only; property loop remains closed''',
    'decoder chain R3.18A',
)
g = replace_one(
    g,
    'R3.18A now proves one complete existing-actor property boundary only. Property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed.',
    'R3.18A proved one complete real existing-actor property boundary with an Int payload, exact end cursor, and zero next-property bits consumed. R3.18B may now publish only the minimal K1 single-property composition. Property-loop continuation, K2/K3/K4 composition in that new API, next actor/frame iteration and lifecycle mutation remain closed.',
    'capability paragraph',
)
g = replace_one(
    g,
    'R3.18A is now the first dependency-valid unfinished roadmap step: read-only evidence for exactly one complete existing-actor property payload and exact end cursor. It must stop before the next `property_present` bit; the property loop is not admitted by this transition.',
    f'''## R3.18A single-property boundary evidence closure

```text
authority head              {AUTH}
authority run/job           {RUN} / {JOB} SUCCESS
exact-head normal CI        {CI_RUN} / {CI_JOB} SUCCESS
artifact                    {ARTIFACT}
artifact digest             {DIGEST}
replay identity/oracle      47/47
eligible scalar candidates  47
selected witness            sample_001 / frame0 / actor2 / object98 / stream27 / property55 / Int=62
property-present bits       [10227,10228)
stream bits                 [10228,10234)
payload bits                [10234,10266) / 32
header/start/semantic/end   exact / exact / exact / exact
next-property bits consumed 0
truncation negative         PASS
mismatch / privacy          0 / PASS
prod/Cargo/fixture/corpus/
support mutations           0/0/0/0/0
outcome                     A
```

R3.18B is now the first dependency-valid unfinished roadmap step: production composition of the existing first-property header with exactly one K1 primitive scalar payload. It must stop at the payload end; the property loop remains unadmitted.''',
    'graph tail',
)
p.write_text(g, encoding='utf-8', newline='\n')

print('R3_18A_CONTINUITY_GENERATION=PASS')
