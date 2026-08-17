#!/usr/bin/env python3
from pathlib import Path
import json
import re

PROD='f41c59d26ed6c810a640b4fa8cd76129decb32aa'
PROD_TREE='606db4b5778e5218f2bd0117cc5dd72d7f3e37a5'
PARENT='1a3f89e7256c7c7ff4bf6b747a434504f1f2e572'
LIB_BLOB='b01b1e8629a4f4bc2452e67024ffb0d064bf58fb'
TEST_BLOB='4bb65af1d533752edc062202192232d6f1d4239c'
AUTH_RUN=32026722346
AUTH_JOB=95377559363
AUTH_ART=9287413927
AUTH_ART_SIZE=2818
AUTH_ART_DIGEST='sha256:1d4ae41e506a69e49ff58372ac0774c6257cbace96a3219bf6ab3ba5f68bf9bb'
SAME_CI=32026722356
SAME_CI_JOB=95377559490
CANDIDATE_CI=32027055064
CANDIDATE_CI_JOB=95378560725
PUBLISHED_CI=32027421491
PUBLISHED_CI_JOB=95379649817
P_CONTRACT='0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b'
O_HEAD='5046e1594b87ce2828db5faa48aceba456c3166f'
O_TREE='74fb036dfde837e3ecb7e459da00df9ff6c22e28'
O_RUN=32017369100
O_JOB=95349613184
O_ART=9284144768
O_ART_SIZE=25129
O_DIGEST='sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d'
O_SUMMARY_SHA='f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc'
O_HEADER_SHA='599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4'
O_AGG_SHA='170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233'


def replace_once(s, old, new, label):
    n=s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return s.replace(old,new,1)

# Decision and next-pass spec first so all later references point at real files.
Path('docs/continuity/MIMIR_R3_18Q_DECISION.md').write_text(f'''# MIMIR R3.18Q — Bounded Following-Property Header Production Decision

**Date:** 2026-08-17  
**Outcome:** **A — ADMITTED / PRODUCTION**  
**Production SHA:** `{PROD}`  
**Production tree:** `{PROD_TREE}`

## Decision

R3.18Q is admitted. From one already-valid R3.18J second-property payload result, production reuses the published R3.18M true-only following-control decoder and the existing stateless property-header primitive, requires the resolved following header to match one of the exact 18 R3.18P seven-field structural/version tuples, and stops exactly at that following header's `payload_start`.

The pass does not decode the following payload, read another property-control bit, create a repeatable property cursor, or widen actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export behavior.

## Exact authority

```text
pre-pass main                       {PARENT}
production SHA/tree                 {PROD} / {PROD_TREE}
lib.rs blob                         {LIB_BLOB}
focused test blob                   {TEST_BLOB}
R3.18P contract SHA256              {P_CONTRACT}
implementation authority            {AUTH_RUN} / {AUTH_JOB} SUCCESS
authority artifact                  {AUTH_ART} / {AUTH_ART_SIZE} bytes / {AUTH_ART_DIGEST}
same-trigger temporary-ops CI       {SAME_CI} / {SAME_CI_JOB} SUCCESS
exact clean-candidate CI            {CANDIDATE_CI} / {CANDIDATE_CI_JOB} SUCCESS
published-main CI                   {PUBLISHED_CI} / {PUBLISHED_CI_JOB} SUCCESS
Knowledge Archive on production PR  N/A — path-filtered to continuity/archive files
```

## Clean scope

Exactly two production files changed from `{PARENT}`:

1. `crates/mimir-replay/src/lib.rs` — +358 / -0
2. `crates/mimir-replay/tests/r3_18q_following_header.rs` — +188 / -0

Cargo manifests/lockfile, fixtures, corpus, docs, workflows and support tooling are absent from the clean production commit.

## Admitted behavior

- reuse the exact R3.18M following `property_present=true` control boundary;
- decode exactly one following existing-actor property header with the already-published stateless header primitive;
- preserve exact control/header present-bit coordinate agreement and actor-object agreement;
- admit only the exact 18 R3.18P tuples across `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)`;
- reject tag-only, component-only, fabricated Cartesian, versionless and nineteenth-tuple widening;
- require `header.stop_bit == payload_start_bit` and return that exact stop;
- consume zero following-payload bits and zero another-control bits.

Authority reconstruction matched the immutable R3.18O lane on 47/47 rows. For all 47, Q's embedded control equaled the published R3.18M control and Q's returned following header equaled the direct stateless native header. Focused validation passed 2 contract unit tests plus 4 permanent integration tests; truncation, wrong actor, fabricated exact-context and wrong-version negatives passed; post-payload poison invariance passed. Full repository verification passed on the authority build, exact clean candidate and published `main`.

## Frozen real-replay result

```text
R3.18O frozen rows                  47/47
R3.18P exact contexts               18
Q native composition exact          47/47
Q / R3.18M control equality         47/47
Q / stateless header equality       47/47
following payload bits consumed     0
another control bits consumed       0
production/Cargo/fixture/corpus/support mutation outside clean scope  0/0/0/0/0
```

## Hard stop

R3.18Q admits no following-property payload bytes or semantic value, no later `property_present` bit, no third/fourth generalized property composition, no repeatable public property cursor/loop, no context outside the exact R3.18P contract, no next actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual rollout execution, runtime bridge or export widening.

## Next gate

R3.18R is a separate read-only real-replay differential audit of the **published R3.18Q production API** on the immutable R3.18O 47-row lane. Following-payload widening remains forbidden until that evidence closes and a later pass explicitly defines a payload contract/evidence boundary.
''',encoding='utf-8',newline='\n')

Path('docs/continuity/MIMIR_R3_18R_EXECUTION_SPEC.md').write_text(f'''# MIMIR R3.18R — Published Following-Property Header Real-Replay Differential Audit

**Status:** ACTIVE  
**Pass type:** read-only evidence / differential validation  
**Production authority:** R3.18Q `{PROD}`  
**Production mutation:** forbidden  
**Following-property payload decode:** forbidden  
**Another property control / repeated loop:** forbidden

## 1. Goal

Differentially validate the published R3.18Q bounded following-property-header composition over the exact immutable 47-row R3.18O lane. Prove the production API itself, not merely the lower-level header primitive, and preserve the R3.18P exact-tuple boundary.

## 2. Frozen authority

```text
production SHA/tree                 {PROD} / {PROD_TREE}
production parent                   {PARENT}
production lib.rs blob              {LIB_BLOB}
R3.18Q focused test blob            {TEST_BLOB}
R3.18Q implementation authority     {AUTH_RUN} / {AUTH_JOB} SUCCESS
R3.18Q same-trigger ops CI          {SAME_CI} / {SAME_CI_JOB} SUCCESS
R3.18Q exact candidate CI           {CANDIDATE_CI} / {CANDIDATE_CI_JOB} SUCCESS
R3.18Q published-main CI            {PUBLISHED_CI} / {PUBLISHED_CI_JOB} SUCCESS
R3.18P contract SHA256              {P_CONTRACT}
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
R3.18O evidence head/tree           {O_HEAD} / {O_TREE}
R3.18O authority run/job            {O_RUN} / {O_JOB} SUCCESS
R3.18O artifact                     {O_ART} / {O_ART_SIZE} bytes
R3.18O artifact digest              {O_DIGEST}
R3.18O source-summary SHA256        {O_SUMMARY_SHA}
R3.18O header-rows SHA256           {O_HEADER_SHA}
R3.18O aggregate SHA256             {O_AGG_SHA}
```

Before evidence, fetch fresh `main`, require exact production SHA/tree/blobs above, verify the immutable R3.18O artifact and 11/11 inner manifest, verify R3.18P contract SHA256, and prove witness reselection remains zero.

## 3. Required source lane

Reuse exactly the frozen R3.18O 47 rows. Do not reselect easier replays or coordinates.

Frozen aggregate identity:

```text
rows                                47
following control true              47
exact structural/version tuples     18
Boolean rows                        39
ActiveActor rows                    8
version                             868.32 / net10 on all 47
following payload bits consumed     0
another control bits consumed       0
```

All 47 witnesses must reconstruct the same valid R3.18J prior and R3.18M true control used by R3.18O.

## 4. Published-production differential checks

For every frozen row invoke the published `decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1` API and require:

- the R3.18J prior reconstructs exactly at the frozen second-payload end;
- embedded R3.18M control start/value/end/stop equals the frozen control exactly;
- `following_property_present == true`;
- following header `property_present` start/end exact;
- stream start/end/value exact;
- `stream_id_bound` and `prop_id_bits` exact;
- resolved property-object index exact;
- resolved attribute tag exact;
- replay `(version_major, version_minor, net_version)` exact;
- the full seven-field tuple is a member of the immutable R3.18P contract;
- returned `following_header` equals the direct stateless native header result;
- returned `stop_bit == following_header.payload_start_bit` exact;
- zero following-payload bits and zero another-control bits consumed.

Native/oracle mismatch count must be zero on 47/47.

## 5. Negative controls

At minimum:

- truncation before all required following-header bits -> reject atomically;
- prior actor-object mismatch -> reject;
- unresolved/invalid following stream or property lookup -> reject before payload;
- resolved tuple outside the exact R3.18P set -> reject before payload;
- fabricated Cartesian tuple from individually observed components -> reject;
- wrong replay version with otherwise matching components -> reject;
- bits at and after `payload_start` may be poisoned without changing the returned production header;
- repeated identical invocation -> exact identical result.

Real frozen rows should exercise truncation and production equality wherever possible. Synthetic negatives may supplement but may not replace the 47-row real-lane differential.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing at least:

- exact production SHA/tree/lib/test blobs and validation receipts;
- exact R3.18P contract hash and immutable R3.18O evidence receipts;
- frozen replay/witness identity without private raw payload windows;
- per-row oracle/published-Q comparison;
- exact tuple and multiplicity summary;
- negative-control results;
- following-payload / another-control consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- hashes for every evidence file in the artifact.

## 7. Required validation

- deterministic double-run equality of the frozen selection/comparison;
- permanent focused R3.18Q tests PASS on the evidence head;
- full `mimir-replay` PASS;
- workspace format/check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18R may not change production Rust, Cargo files, fixtures, corpus, dependencies or support lanes. It may not decode or semantically claim the following payload, inspect another `property_present` bit, create a repeatable/generalized property loop or public cursor, widen R3.18P membership, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactual rollouts or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen rows match the published R3.18Q production API exactly, all negatives pass, mismatch is zero, following-payload/another-control consumption remains `0/0`, witness reselection is zero, privacy passes and production mutation is zero. Admit R3.18R evidence. A later **separate** pass may then define a bounded following-payload evidence/contract boundary; R3.18R itself admits no payload.

### Outcome B

A reproducible published-Q/oracle mismatch appears inside the already-admitted R3.18Q boundary. Record exact privacy-safe coordinates and keep payload/loop widening closed.

### Outcome C

Authority drift, production/source mutation, witness reselection, privacy failure, payload/later-control access, exact-contract widening or validation contradiction. Stop without admission.
''',encoding='utf-8',newline='\n')

# Master handbook.
p=Path('MIMIR_CONTINUE_HERE.md')
s=p.read_text(encoding='utf-8')
s=replace_once(s,'LAST_PRODUCTION_CODE_SHA:\n  fd74ba8c520ab83b808730572c41e45d6dc616e6','LAST_PRODUCTION_CODE_SHA:\n  '+PROD,'handbook prod SHA')
s=replace_once(s,'LAST_PRODUCTION_MILESTONE:\n  R3.18M — bounded native after-second-payload true-only control composition','LAST_PRODUCTION_MILESTONE:\n  R3.18Q — bounded following-property header production composition','handbook prod milestone')
s=replace_once(s,'CURRENT_PASS:\n  R3.18Q — bounded following-property header production composition','CURRENT_PASS:\n  R3.18R — published following-property header real-replay differential audit','handbook current pass')
s=replace_once(s,'CURRENT_PASS_TYPE:\n  production / compose exactly one following header after a valid R3.18M true control; exact R3.18P tuple membership; stop at payload_start','CURRENT_PASS_TYPE:\n  read-only differential / validate the published R3.18Q production API on the immutable R3.18O 47-row lane; exact R3.18P membership; no payload or later control','handbook pass type')
s=replace_once(s,
'  R3.18Q ACTIVE production pass: one following header only after valid R3.18M true control; exact R3.18P membership; stop at payload_start\n  NO following payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted',
f'  R3.18Q PRODUCTION at {PROD}: one following header only after valid R3.18M true control; exact R3.18P seven-field membership; stop exactly at payload_start; 47/47 frozen authority rows exact\n  R3.18R ACTIVE read-only differential on the immutable R3.18O 47-row lane\n  NO following payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted',
'handbook hard stop')
closure=f'''R3_18Q_PRODUCTION_CLOSURE:\n  Outcome A / production {PROD} / tree {PROD_TREE}\n  parent: {PARENT}\n  lib/test blobs: {LIB_BLOB} / {TEST_BLOB}\n  R3.18P contract sha256: {P_CONTRACT}\n  implementation authority: {AUTH_RUN} / {AUTH_JOB} SUCCESS; artifact {AUTH_ART} / {AUTH_ART_SIZE} bytes / {AUTH_ART_DIGEST}\n  same-trigger temporary-ops CI: {SAME_CI} / {SAME_CI_JOB} SUCCESS\n  exact clean-candidate CI: {CANDIDATE_CI} / {CANDIDATE_CI_JOB} SUCCESS\n  published-main CI: {PUBLISHED_CI} / {PUBLISHED_CI_JOB} SUCCESS\n  focused R3.18Q tests: 6 PASS; 18 exact tuples admitted; 47/47 frozen Q composition exact\n  Q/R3.18M control equality: 47/47; Q/stateless-header equality: 47/47\n  following payload / another-control bits consumed: 0/0\n  clean scope: lib.rs + r3_18q_following_header.rs only; Cargo/fixture/corpus/docs/workflow/support mutation 0\n'''
s=replace_once(s,'R3_18P_CONTRACT_CLOSURE:\n',closure+'R3_18P_CONTRACT_CLOSURE:\n','handbook Q closure')
s=s.replace('# CURRENT PASS CHECKLIST — R3.18Q','# HISTORICAL PASS CHECKLIST — R3.18Q (SUPERSEDED)',1)
pat=r'(# 39\. CURRENT ONE-LINE TRUTH\n\n)> .*?\n\n---'
new_truth=(r'\1> **MIMIR production is now at R3.18Q `'+PROD+r'`: after a valid R3.18M true following control it decodes exactly one following property header, requires exact R3.18P seven-field tuple membership, and stops at that header\'s `payload_start`. R3.18R is the active read-only published-API differential on the immutable R3.18O 47-row lane. Following payload, another control bit, generalized loops/cursors, actor/frame iteration, raw state, events and skills remain closed.**\n\n---')
s,n=re.subn(pat,new_truth,s,count=1,flags=re.S)
if n != 1:
    raise SystemExit(f'handbook one-line truth replacement count={n}')
if '# CURRENT PASS CHECKLIST — R3.18R' not in s:
    s += f'''\n\n---\n\n# CURRENT PASS CHECKLIST — R3.18R\n\n**Goal:** differentially validate published R3.18Q on the exact immutable R3.18O 47-row lane. Production Rust is frozen.\n\n```text\n[ ] Fetch fresh main; require production {PROD} / tree {PROD_TREE} and exact lib/test blobs.\n[ ] Verify R3.18P contract SHA256 {P_CONTRACT}.\n[ ] Freeze R3.18O head/run/job/artifact/digest plus 11/11 inner manifest; witness reselection = 0.\n[ ] Reconstruct the exact 47 valid R3.18J priors and R3.18M true controls used by R3.18O.\n[ ] Invoke the published R3.18Q API on all 47 rows.\n[ ] Require control equality 47/47 and following-header equality through payload_start 47/47.\n[ ] Require exact seven-field R3.18P membership and multiplicity reconstruction.\n[ ] Require native/oracle mismatch = 0 and following payload / another-control consumption = 0/0.\n[ ] Run truncation, wrong-actor, unresolved lookup, outside-tuple, Cartesian, wrong-version, repeatability and post-payload poison controls.\n[ ] Produce privacy-safe immutable evidence with hashes for every evidence file.\n[ ] Run focused Q tests, full mimir-replay/workspace/clippy/repository verification and same-head normal CI.\n[ ] Require production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.\n[ ] Outcome A may open a later separate following-payload evidence/contract pass only; R3.18R itself admits no payload.\n```\n'''
p.write_text(s,encoding='utf-8',newline='\n')

# Knowledge graph.
p=Path('MIMIR_KNOWLEDGE_GRAPH.md')
s=p.read_text(encoding='utf-8')
s=replace_once(s,
'R3.18Q active bounded following-property header production spec                              |',
'R3.18Q bounded following-property header production decision / CLOSED                         |\nR3.18R active published following-property header differential spec                            |',
'KG Q/R graph')
start=s.index('## Mandatory reading order\n\n')+len('## Mandatory reading order\n\n')
end=s.index('### ',start)
block=s[start:end]
items=[]
for line in block.splitlines():
    m=re.match(r'^\d+\.\s+(.+)$',line)
    if m:
        items.append(m.group(1))
qdec='`docs/continuity/MIMIR_R3_18Q_DECISION.md`'
rspec='`docs/continuity/MIMIR_R3_18R_EXECUTION_SPEC.md`'
for x in (qdec,rspec):
    while x in items:
        items.remove(x)
pos=items.index('`docs/continuity/MIMIR_R3_18Q_EXECUTION_SPEC.md`')+1
items[pos:pos]=[qdec,rspec]
new_block=''.join(f'{i}. {item}\n' for i,item in enumerate(items,1))+'\n'
s=s[:start]+new_block+s[end:]
qblock=f'''### R3.18Q following-property header: PRODUCTION / CLOSED\n- production `{PROD}` / tree `{PROD_TREE}`; parent `{PARENT}`\n- lib/test blobs `{LIB_BLOB}` / `{TEST_BLOB}`\n- authority `{AUTH_RUN}/{AUTH_JOB}`, ops CI `{SAME_CI}/{SAME_CI_JOB}`, clean-candidate CI `{CANDIDATE_CI}/{CANDIDATE_CI_JOB}`, published CI `{PUBLISHED_CI}/{PUBLISHED_CI_JOB}` SUCCESS\n- immutable R3.18P contract `{P_CONTRACT}`; exact contexts 18; frozen Q reconstruction 47/47\n- Q/R3.18M control equality 47/47; Q/stateless-header equality 47/47; payload/another-control consumption 0/0\n- next exact pass: R3.18R published R3.18Q API differential on the immutable R3.18O 47-row lane\n\n### R3.18R published following header differential: ACTIVE\n- read-only only; production `{PROD}` frozen\n- source lane: immutable R3.18O artifact `{O_ART}` / `{O_DIGEST}` and exact R3.18P contract\n- require 47/47 published-Q/oracle equality, exact tuple membership, negative controls, privacy and zero mutation\n- following payload and another property control remain closed\n\n'''
if '### R3.18Q following-property header: PRODUCTION / CLOSED' not in s:
    marker='### R3.18O following-property header evidence: OUTCOME A / CLOSED'
    idx=s.find(marker)
    if idx == -1:
        s += '\n'+qblock
    else:
        s=s[:idx]+qblock+s[idx:]
p.write_text(s,encoding='utf-8',newline='\n')

# Machine state.
p=Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
d=json.loads(p.read_text(encoding='utf-8'))
d['updated_date']='2026-08-17'
d['last_production_code_sha']=PROD
d['last_production_milestone']='R3.18Q'
d['last_production_milestone_name']='bounded following-property header production composition'
d['current_pass']='R3.18R'
d['current_pass_kind']='read-only differential / published R3.18Q following-property header audit'
d['current_pass_goal']='Differentially validate the published R3.18Q API on the immutable R3.18O 47-row lane, preserving exact R3.18P seven-field membership and stopping at payload_start.'
d['current_pass_stop_boundary']='Stop exactly at the following header payload_start. No following payload, another control bit, generalized/repeatable property loop, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening.'
d['closed_now']=[
    'false following property control in after-second-payload production context (R3.18L observed false=0)',
    'following property payload after the R3.18Q payload_start stop',
    'another property control bit beyond the R3.18Q stop',
    'following-header contexts outside the exact R3.18P seven-field tuple set',
    'repeated/generalized production property_present loop',
    'generic repeatedly-chainable public property cursor',
    'second-payload contexts outside exact Int and net10/non-RL223 String',
    'next actor / next frame iteration','actor state table mutation','raw-state extraction','event extraction','replay slicing','skill mining','counterfactual rollout execution from native replay state'
]
d['r3_18q']={
    'outcome':'A — admitted / production',
    'pre_pass_main_sha':PARENT,
    'production_sha':PROD,'production_tree':PROD_TREE,
    'lib_blob':LIB_BLOB,'focused_test_blob':TEST_BLOB,
    'r3_18p_contract_sha256':P_CONTRACT,
    'implementation_authority_run':AUTH_RUN,'implementation_authority_job':AUTH_JOB,
    'authority_artifact_id':AUTH_ART,'authority_artifact_size':AUTH_ART_SIZE,'authority_artifact_digest':AUTH_ART_DIGEST,
    'same_trigger_ops_ci_run':SAME_CI,'same_trigger_ops_ci_job':SAME_CI_JOB,
    'clean_candidate_ci_run':CANDIDATE_CI,'clean_candidate_ci_job':CANDIDATE_CI_JOB,
    'published_main_ci_run':PUBLISHED_CI,'published_main_ci_job':PUBLISHED_CI_JOB,
    'focused_tests':6,'exact_contexts':18,'frozen_native_rows':'47/47',
    'r3_18m_control_equality':'47/47','stateless_header_equality':'47/47',
    'following_payload_bits_consumed':0,'another_control_bits_consumed':0,
    'production_files':['crates/mimir-replay/src/lib.rs','crates/mimir-replay/tests/r3_18q_following_header.rs']
}
nxt=d.get('next_files_to_read',[])
for x in ['docs/continuity/MIMIR_R3_18Q_DECISION.md','docs/continuity/MIMIR_R3_18R_EXECUTION_SPEC.md']:
    while x in nxt:
        nxt.remove(x)
anchor='docs/continuity/MIMIR_R3_18Q_EXECUTION_SPEC.md'
pos=nxt.index(anchor)+1
nxt[pos:pos]=['docs/continuity/MIMIR_R3_18Q_DECISION.md','docs/continuity/MIMIR_R3_18R_EXECUTION_SPEC.md']
d['next_files_to_read']=nxt
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

# Concise canonical current state.
Path('docs/continuity/MIMIR_CURRENT_STATE.md').write_text(f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-17  
**Repository:** `Naveax/MIMIR`  
**Canonical production SHA:** `{PROD}`  
**Production tree:** `{PROD_TREE}`  
**Production milestone:** `R3.18Q — bounded following-property header production composition`  
**Last read-only evidence:** `R3.18O — Outcome A / 47/47 / 18 exact contexts / mismatch 0`  
**Last contract:** `R3.18P — Outcome A / exact seven-field tuple membership / 18 contexts / 47 multiplicities`  
**Current exact pass:** `R3.18R — published R3.18Q following-property header real-replay differential audit`

## Truthful production boundary

Production accepts one already-valid R3.18J second-payload result, reuses the published R3.18M true-only following control, decodes exactly one following existing-actor property header through `payload_start`, and requires exact membership in the 18-tuple R3.18P contract including replay version. It reads no following payload and no later property-control bit.

```text
production SHA/tree                 {PROD} / {PROD_TREE}
lib/test blobs                      {LIB_BLOB} / {TEST_BLOB}
R3.18P contract SHA256              {P_CONTRACT}
implementation authority            {AUTH_RUN} / {AUTH_JOB} SUCCESS
same-trigger ops CI                 {SAME_CI} / {SAME_CI_JOB} SUCCESS
exact clean-candidate CI            {CANDIDATE_CI} / {CANDIDATE_CI_JOB} SUCCESS
published-main CI                   {PUBLISHED_CI} / {PUBLISHED_CI_JOB} SUCCESS
focused R3.18Q tests                6 PASS
frozen native Q rows                47/47
R3.18M control equality             47/47
stateless-header equality           47/47
following payload / later control   0 / 0
```

## Current gate

R3.18R is read-only. It must validate the **published** R3.18Q API on the immutable R3.18O 47-row lane, prove exact control/header/tuple/stop equality with zero mismatch and zero witness reselection, run boundary negatives, emit privacy-safe immutable evidence, and mutate no production/Cargo/fixture/corpus/support files.

## Hard stop

Following payload decoding, another `property_present` bit, repeatable/generalized property loops or public cursors, tuple widening, next actor/frame iteration, lifecycle/raw-state/event/slice/skill/counterfactual/runtime/export behavior remain closed.
''',encoding='utf-8',newline='\n')

Path('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md').write_text(f'''# MIMIR — Next Chat Handoff

Fresh canonical production is **R3.18Q** at `{PROD}` (`{PROD_TREE}`). R3.18Q is fully published and validated: authority `{AUTH_RUN}/{AUTH_JOB}`, exact candidate CI `{CANDIDATE_CI}/{CANDIDATE_CI_JOB}`, published-main CI `{PUBLISHED_CI}/{PUBLISHED_CI_JOB}` all SUCCESS.

The active pass is **R3.18R**, a read-only differential of the published R3.18Q following-header API on the immutable R3.18O 47-row lane. Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18Q_DECISION.md`, and `docs/continuity/MIMIR_R3_18R_EXECUTION_SPEC.md` before work.

Critical locks: exact R3.18P contract SHA256 `{P_CONTRACT}`; R3.18O artifact `{O_ART}` digest `{O_DIGEST}`; witness reselection must remain zero. R3.18R may not modify production and may not consume following-payload bits or another property-control bit.
''',encoding='utf-8',newline='\n')

# Boundary locks: append one immutable production lock and the active differential stop.
p=Path('docs/continuity/MIMIR_BOUNDARY_LOCKS.md')
s=p.read_text(encoding='utf-8').rstrip()+"\n\n"
if '## R3.18Q following-property header production lock' not in s:
    s += f'''## R3.18Q following-property header production lock

- Production SHA/tree: `{PROD}` / `{PROD_TREE}`.
- Exact R3.18P contract: `{P_CONTRACT}`; membership is the full seven-field tuple only.
- From one valid R3.18J second payload, R3.18Q reuses R3.18M true control and decodes exactly one stateless following header.
- Exact stop is the following header `payload_start`; following-payload bits consumed `0`; another-control bits consumed `0`.
- Frozen authority result: 47/47 Q rows exact, 47/47 R3.18M control equality, 47/47 stateless-header equality.
- No tag-only/component-only/Cartesian/versionless widening, no repeated/generalized property loop/cursor.

## R3.18R active differential hard stop

- Read-only audit of published R3.18Q on the immutable R3.18O 47-row lane.
- Production/Cargo/fixture/corpus/support mutation is forbidden.
- Following payload, another `property_present`, loop/cursor, actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export widening is forbidden.
- Outcome A may only open a later separate payload evidence/contract pass; it does not itself admit payload.
'''
p.write_text(s,encoding='utf-8',newline='\n')

# Progress ledger: append canonical milestone lines.
p=Path('docs/continuity/MIMIR_PROGRESS_LEDGER.md')
s=p.read_text(encoding='utf-8').rstrip()+"\n\n"
if 'R3.18Q — bounded following-property header production' not in s:
    s += f'''## 2026-08-17 — R3.18Q — bounded following-property header production — Outcome A

- Published production `{PROD}` / tree `{PROD_TREE}`; parent `{PARENT}`.
- Authority `{AUTH_RUN}/{AUTH_JOB}` SUCCESS; exact-candidate CI `{CANDIDATE_CI}/{CANDIDATE_CI_JOB}` SUCCESS; published-main CI `{PUBLISHED_CI}/{PUBLISHED_CI_JOB}` SUCCESS.
- Clean scope: `crates/mimir-replay/src/lib.rs` + `crates/mimir-replay/tests/r3_18q_following_header.rs` only.
- R3.18P exact contract `{P_CONTRACT}`; 18 exact contexts; 47/47 frozen production compositions exact.
- Q/R3.18M control equality 47/47; Q/stateless-header equality 47/47; following payload / another-control consumption 0/0.
- Opened R3.18R read-only published-API differential; production frozen.
'''
p.write_text(s,encoding='utf-8',newline='\n')

# Sanity assertions used before repository-level verification.
assert Path('docs/continuity/MIMIR_R3_18Q_DECISION.md').exists()
assert Path('docs/continuity/MIMIR_R3_18R_EXECUTION_SPEC.md').exists()
assert f'LAST_PRODUCTION_CODE_SHA:\n  {PROD}' in Path('MIMIR_CONTINUE_HERE.md').read_text(encoding='utf-8')
assert 'CURRENT_PASS:\n  R3.18R' in Path('MIMIR_CONTINUE_HERE.md').read_text(encoding='utf-8')
assert 'R3.18Q bounded following-property header production decision / CLOSED' in Path('MIMIR_KNOWLEDGE_GRAPH.md').read_text(encoding='utf-8')
assert 'R3.18R active published following-property header differential spec' in Path('MIMIR_KNOWLEDGE_GRAPH.md').read_text(encoding='utf-8')
st=json.loads(Path('docs/continuity/MIMIR_CONTINUITY_STATE.json').read_text(encoding='utf-8'))
assert st['last_production_code_sha']==PROD
assert st['last_production_milestone']=='R3.18Q'
assert st['current_pass']=='R3.18R'
print('R3_18Q_CONTINUITY_GENERATION=PASS')
