#!/usr/bin/env python3
from pathlib import Path
import json
import re

PROD='fd74ba8c520ab83b808730572c41e45d6dc616e6'
PROD_TREE='6285928b3ca724c77b761e70c54f7bd0763f11f0'
LIB_BLOB='029c48e38ea0257f8cdb3fa8715bde5a789213e7'
TEST_BLOB='a9bd2d0a8007c8cae76a0d14ad0c11ed387fe5a6'
IMPL_RUN='31999687944'
IMPL_JOB='95297550306'
SAME_HEAD_CI='31999687880'
SAME_HEAD_CI_JOB='95297550231'
CANDIDATE_CI='31999898754'
CANDIDATE_CI_JOB='95298116788'
PUBLISHED_CI='32000211020'
PUBLISHED_CI_JOB='95298954375'


def replace_once(s, old, new, label):
    n=s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return s.replace(old,new,1)

# Master continuity handbook.
p=Path('MIMIR_CONTINUE_HERE.md')
s=p.read_text(encoding='utf-8')
s=replace_once(s,'LAST_PRODUCTION_CODE_SHA:\n  330ab01890a7c09eff1805e437584fb3be0a1134','LAST_PRODUCTION_CODE_SHA:\n  '+PROD,'handbook prod sha')
s=replace_once(s,'LAST_PRODUCTION_MILESTONE:\n  R3.18J — bounded native second-property payload composition','LAST_PRODUCTION_MILESTONE:\n  R3.18M — bounded native after-second-payload true-only control composition','handbook prod milestone')
s=replace_once(s,'CURRENT_PASS:\n  R3.18M — bounded native after-second-payload control-bit composition','CURRENT_PASS:\n  R3.18N — published after-second-payload control real-replay differential audit','handbook current pass')
s=replace_once(s,'CURRENT_PASS_TYPE:\n  production implementation / from one already-valid R3.18J second-payload result, consume exactly one following property_present bit; admit only the R3.18L-observed true context and stop one bit later','CURRENT_PASS_TYPE:\n  read-only differential / validate the published R3.18M true-only following-control API on the exact frozen R3.18L 47-row lane; no following stream/header/payload access','handbook pass type')
s=replace_once(s,'  R3.18M ACTIVE production implementation may compose exactly this one after-second-payload control bit, true context only; false is evidence-unobserved and must fail closed\n  NO following stream/header/payload, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted','  R3.18M PRODUCTION at '+PROD+': from one valid R3.18J second-payload result it validates the prior payload boundary, consumes exactly one following property_present bit, admits only true, and stops one bit later; false remains fail-closed\n  R3.18N ACTIVE read-only differential on the exact frozen R3.18L 47-row true-only lane\n  NO following stream/header/payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted','handbook hard stop')
closure=f'''R3_18M_PRODUCTION_CLOSURE:\n  Outcome A / production {PROD} / tree {PROD_TREE}\n  lib/test blobs: {LIB_BLOB} / {TEST_BLOB}\n  implementation v3: {IMPL_RUN} / {IMPL_JOB} SUCCESS\n  same-head temp CI: {SAME_HEAD_CI} / {SAME_HEAD_CI_JOB} SUCCESS\n  exact clean-candidate CI: {CANDIDATE_CI} / {CANDIDATE_CI_JOB} SUCCESS\n  published-main CI: {PUBLISHED_CI} / {PUBLISHED_CI_JOB} SUCCESS\n  focused R3.18M tests: 6 PASS; full mimir-replay/workspace/clippy/repository verification: PASS\n  source boundary: exactly one read_bit / following stream-header-payload decoder calls 0 / property loops 0\n  admitted value: following property_present=true only; false fails closed\n  stop: exactly prior R3.18J payload end + 1 bit\n  Cargo/fixture/corpus/support/workflow mutation in clean production commit: 0/0/0/0/0\n'''
s=replace_once(s,'R3_18L_EVIDENCE_CLOSURE:\n',closure+'R3_18L_EVIDENCE_CLOSURE:\n','handbook M closure insert')
# Convert old embedded current labels to explicit history rather than deleting useful records.
s=s.replace('# 13. CURRENT PASS CHECKLIST — R3.14A','# 13. HISTORICAL PASS CHECKLIST — R3.14A (SUPERSEDED)',1)
s=s.replace('# CURRENT PASS CHECKLIST — R3.18I','# HISTORICAL PASS CHECKLIST — R3.18I (SUPERSEDED)',1)
# Repair quick dashboard drift if those historical rows are still present.
for old,new in [
('[>] R3.14A first frame + first actor oracle evidence','[x] R3.14A first frame + first actor oracle evidence'),
('[ ] R3.14B bit-cursor/bounded-int contract','[x] R3.14B bit-cursor/bounded-int contract'),
('[ ] R3.14C native bit primitive','[x] R3.14C native bit primitive'),
('[ ] R3.14D first actor envelope native reader','[x] R3.14D first actor envelope native reader'),
('[ ] R3.14E differential closure','[x] R3.14E differential closure'),
('[ ] R3.15 NewActor payload','[x] R3.15 NewActor payload'),
('[ ] R3.16 existing actor/property envelope','[x] R3.16 existing actor/property envelope'),
('[ ] R3.17 attribute decoder families','[x] R3.17 attribute decoder families'),
('[ ] R3.18 complete property loop','[>] R3.18 complete property loop'),
]:
    s=s.replace(old,new,1)
# Replace the stale one-line truth block deterministically.
pat=r'(# 39\. CURRENT ONE-LINE TRUTH\n\n)> .*?\n\n---'
new_truth=(r'\1> **MIMIR production is now at R3.18M `'+PROD+r'`: after one valid R3.18J second payload, exactly one following `property_present` bit is consumed; only the R3.18L-observed `true` context is admitted and the API stops one bit later. R3.18N is the active read-only published-API differential on the frozen 47-row lane. Following stream/header/payload, another control bit, a generalized property loop, actor/frame iteration, raw state, events and skills remain closed.**\n\n---')
s,n=re.subn(pat,new_truth,s,count=1,flags=re.S)
if n != 1:
    raise SystemExit(f'handbook one-line truth replacement count={n}')
if '# CURRENT PASS CHECKLIST — R3.18N' not in s:
    s += f'''\n\n---\n\n# CURRENT PASS CHECKLIST — R3.18N\n\n**Goal:** differentially validate the published R3.18M true-only following-control composition on the exact frozen R3.18L 47-row lane. Production Rust is frozen.\n\n```text\n[ ] Fresh-read main; require production SHA {PROD} and exact lib/test blobs.\n[ ] Freeze R3.18L authority head/run/job/artifact/digest; witness reselection = 0.\n[ ] Reconstruct the exact 47 valid R3.18J second-payload results used by R3.18L.\n[ ] Invoke the published R3.18M API, not a lower-level bit reader.\n[ ] Require following property_present start/value/end/stop exact on 47/47 rows.\n[ ] Require value distribution false=0 / true=47 and native/oracle mismatch=0.\n[ ] Require no following stream/header/payload or another control bit consumed.\n[ ] Run truncation, prior-boundary mismatch, repeatability and post-stop poison controls.\n[ ] Produce privacy-safe immutable evidence with per-file hashes and exact production receipts.\n[ ] Run same-head normal CI plus full repository verification.\n[ ] Require production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.\n[ ] Outcome A may open a separate following-property header evidence pass only; it does not itself admit that header.\n```\n'''
p.write_text(s,encoding='utf-8',newline='\n')

# Knowledge graph.
p=Path('MIMIR_KNOWLEDGE_GRAPH.md')
s=p.read_text(encoding='utf-8')
s=replace_once(s,'R3.18M active bounded after-second-payload control implementation spec       |','R3.18M bounded after-second-payload true-only control production decision / CLOSED\nR3.18N active published after-second-payload control differential spec       |','KG M/N graph')
start=s.index('## Mandatory reading order\n\n')+len('## Mandatory reading order\n\n')
end=s.index('### R3.18I payload evidence:',start)
block=s[start:end]
items=[]
for line in block.splitlines():
    m=re.match(r'^\d+\.\s+(.+)$',line)
    if m: items.append(m.group(1))
mdec='`docs/continuity/MIMIR_R3_18M_DECISION.md`'
nspec='`docs/continuity/MIMIR_R3_18N_EXECUTION_SPEC.md`'
for x in [mdec,nspec]:
    if x in items: items.remove(x)
pos=items.index('`docs/continuity/MIMIR_R3_18M_EXECUTION_SPEC.md`')+1
items[pos:pos]=[mdec,nspec]
new_block=''.join(f'{i}. {item}\n' for i,item in enumerate(items,1))+'\n'
s=s[:start]+new_block+s[end:]
kg_closure=f'''### R3.18M following control: PRODUCTION / CLOSED\n- production `{PROD}` / tree `{PROD_TREE}`\n- lib/test blobs `{LIB_BLOB}` / `{TEST_BLOB}`\n- implementation `{IMPL_RUN}/{IMPL_JOB}`, same-head CI `{SAME_HEAD_CI}/{SAME_HEAD_CI_JOB}`, clean-candidate CI `{CANDIDATE_CI}/{CANDIDATE_CI_JOB}`, published CI `{PUBLISHED_CI}/{PUBLISHED_CI_JOB}` SUCCESS\n- exactly one following control bit; admitted true only; false fails closed; following stream/header/payload and loops remain closed\n- next exact pass: R3.18N published R3.18M API differential on frozen 47-row lane\n\n'''
if '### R3.18M following control: PRODUCTION / CLOSED' not in s:
    s=s.replace('## Current replay-decoder chain\n',kg_closure+'## Current replay-decoder chain\n',1)
p.write_text(s,encoding='utf-8',newline='\n')

# Machine state.
p=Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
d=json.loads(p.read_text(encoding='utf-8'))
d['updated_date']='2026-08-17'
d['last_production_code_sha']=PROD
d['last_production_milestone']='R3.18M'
d['last_production_milestone_name']='bounded native after-second-payload true-only control composition'
d['last_completed_read_only_audit']='R3.18L'
d['current_pass']='R3.18N'
d['current_pass_kind']='read-only differential / published R3.18M after-second-payload true-only control audit'
d['current_pass_goal']='Differentially validate the published R3.18M API over the exact frozen R3.18L 47-row lane, requiring exact true control start/value/end/stop and zero following stream/header/payload access.'
d['current_pass_stop_boundary']='Stop exactly one bit after the R3.18J second payload end. No following stream/header/payload, another control bit, repeated/generalized loop, next actor/frame/lifecycle/raw-state/event/skill/runtime/export widening.'
d['closed_now']=[
    'false following property control in after-second-payload production context (R3.18L observed false=0)',
    'following property stream/header/payload after the R3.18M control bit',
    'another property control bit beyond the R3.18M stop',
    'repeated/generalized production property_present loop',
    'generic repeatedly-chainable public property cursor',
    'second-payload contexts outside exact Int and net10/non-RL223 String',
    'next actor / next frame iteration','actor state table mutation','raw-state extraction','event extraction','replay slicing','skill mining','counterfactual rollout execution from native replay state'
]
d['last_completed_evidence_pass']='R3.18L'
d['last_completed_evidence_outcome']='A — 47/47 frozen after-second-payload control rows exact; false=0 true=47; mismatch 0; following stream/header/payload 0/0/0; production unchanged before R3.18M.'
d['r3_18m']={
    'outcome':'A — admitted / production',
    'pre_pass_main_sha':'346f5596c1ad38dd944cc50404206aab508ba951',
    'production_sha':PROD,'production_tree':PROD_TREE,'lib_blob':LIB_BLOB,'focused_test_blob':TEST_BLOB,
    'implementation_run':int(IMPL_RUN),'implementation_job':int(IMPL_JOB),
    'same_head_ci_run':int(SAME_HEAD_CI),'same_head_ci_job':int(SAME_HEAD_CI_JOB),
    'clean_candidate_ci_run':int(CANDIDATE_CI),'clean_candidate_ci_job':int(CANDIDATE_CI_JOB),
    'published_main_ci_run':int(PUBLISHED_CI),'published_main_ci_job':int(PUBLISHED_CI_JOB),
    'focused_tests':6,'following_control_true_admitted':True,'following_control_false_admitted':False,
    'following_bits_consumed':1,'following_stream_bits_consumed':0,'following_header_bits_consumed':0,'following_payload_bits_consumed':0,
    'production_files':['crates/mimir-replay/src/lib.rs','crates/mimir-replay/tests/r3_18m_following_control.rs']
}
nxt=d.get('next_files_to_read',[])
for x in ['docs/continuity/MIMIR_R3_18M_DECISION.md','docs/continuity/MIMIR_R3_18N_EXECUTION_SPEC.md']:
    if x in nxt: nxt.remove(x)
pos=nxt.index('docs/continuity/MIMIR_R3_18M_EXECUTION_SPEC.md')+1
nxt[pos:pos]=['docs/continuity/MIMIR_R3_18M_DECISION.md','docs/continuity/MIMIR_R3_18N_EXECUTION_SPEC.md']
d['next_files_to_read']=nxt
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

# Concise current state.
Path('docs/continuity/MIMIR_CURRENT_STATE.md').write_text(f'''# MIMIR — Current Canonical State\n\n**Continuity date:** 2026-08-17\n**Repository:** `Naveax/MIMIR`\n**Canonical production SHA:** `{PROD}`\n**Production milestone:** `R3.18M — bounded native after-second-payload true-only control composition`\n**Completed read-only evidence:** `R3.18L — Outcome A / 47/47 / false=0 true=47 / mismatch 0`\n**Current exact pass:** `R3.18N — published R3.18M after-second-payload control real-replay differential audit`\n\n## Truthful production boundary\n\nProduction accepts one already-valid R3.18J second-payload result, proves its stop is exactly the second payload end, reads exactly one following `property_present` bit, accepts only the R3.18L-observed `true` context, and stops exactly one bit later. `false` remains fail-closed because R3.18L observed no false witness. No following stream/header/payload is read.\n\n```text\nproduction SHA/tree                 {PROD} / {PROD_TREE}\nlib/test blobs                      {LIB_BLOB} / {TEST_BLOB}\nimplementation v3                   {IMPL_RUN} / {IMPL_JOB} SUCCESS\nsame-head temp CI                   {SAME_HEAD_CI} / {SAME_HEAD_CI_JOB} SUCCESS\nexact clean-candidate CI            {CANDIDATE_CI} / {CANDIDATE_CI_JOB} SUCCESS\npublished-main CI                   {PUBLISHED_CI} / {PUBLISHED_CI_JOB} SUCCESS\nfocused R3.18M tests                6 PASS\nfollowing control admission         true only; false rejected\nfollowing stream/header/payload     0 / 0 / 0\n```\n\n## Current gate\n\nR3.18N must invoke the published R3.18M API on the immutable 47-row R3.18L lane and prove exact control start/value/end/stop with zero mismatch and zero following stream/header/payload access. Production source is frozen.\n\n## Still closed\n\n```text\nfalse after-second-payload control context\nfollowing property stream/header/payload\nanother property control bit\nrepeated/generalized property loop\ngeneric repeatedly-chainable property cursor\nnext actor / next frame iteration\nactor lifecycle mutation\nraw-state extraction / events / replay slicing\nskill / teacher / runtime / export widening\n```\n''',encoding='utf-8',newline='\n')

# Boundary override append.
p=Path('docs/continuity/MIMIR_BOUNDARY_LOCKS.md')
s=p.read_text(encoding='utf-8')
if '## CURRENT OVERRIDE — R3.18M PRODUCTION / R3.18N ACTIVE' not in s:
    s += f'''\n\n---\n\n## CURRENT OVERRIDE — R3.18M PRODUCTION / R3.18N ACTIVE\n\nFresh source/tests and exact-SHA evidence override older current-like sections above.\n\n```text\nOPEN / PRODUCTION:\n  R3.18M at {PROD}\n  from one valid R3.18J second-payload result, validate exact prior payload end\n  read exactly one following property_present bit\n  admit true only; false fails closed\n  stop exactly one bit later\n\nACTIVE EVIDENCE:\n  R3.18N published-R3.18M differential on exact frozen R3.18L 47-row lane\n\nCLOSED:\n  false following-control production context\n  following stream/header/payload\n  another control bit\n  repeated/generalized property loop\n  next actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export widening\n```\n'''
p.write_text(s,encoding='utf-8',newline='\n')

# Durable R3.18M decision.
Path('docs/continuity/MIMIR_R3_18M_DECISION.md').write_text(f'''# MIMIR R3.18M — Bounded After-Second-Payload Control Production Decision\n\n**Date:** 2026-08-17\n**Outcome:** **A — ADMITTED / PRODUCTION PUBLISHED**\n**Production SHA:** `{PROD}`\n**Production tree:** `{PROD_TREE}`\n\n## Decision\n\nR3.18M is admitted. Given one already-valid R3.18J second-property payload result, production validates the prior second-header/payload boundary, reads exactly one following `property_present` bit, and stops exactly one bit later. R3.18L observed `true` on all 47 frozen rows and no `false` witness, so production admits only `true`; `false` fails closed.\n\nThe new API does not decode a following stream ID, property header, payload, another control bit, or a generalized property loop.\n\n## Exact authority\n\n```text\npre-pass main                       346f5596c1ad38dd944cc50404206aab508ba951\nproduction SHA/tree                 {PROD} / {PROD_TREE}\nlib.rs blob                         {LIB_BLOB}\nfocused test blob                   {TEST_BLOB}\nimplementation v3                   {IMPL_RUN} / {IMPL_JOB} SUCCESS\nsame-head temp CI                   {SAME_HEAD_CI} / {SAME_HEAD_CI_JOB} SUCCESS\nclean-candidate CI                  {CANDIDATE_CI} / {CANDIDATE_CI_JOB} SUCCESS\npublished-main CI                   {PUBLISHED_CI} / {PUBLISHED_CI_JOB} SUCCESS\nR3.18L evidence head                9205ac1616e686589938f952782a32f03d0d1488\nR3.18L run/job                      31978791346 / 95242213413 SUCCESS\nR3.18L artifact                     9271817700\nR3.18L artifact digest              sha256:db5d2db96429a4f2b699dca5176fc4d218f9eb9e4faa8dee813b766896f70c1c\n```\n\n## Clean scope\n\nExactly two production files changed from the pre-pass main:\n\n1. `crates/mimir-replay/src/lib.rs`\n2. `crates/mimir-replay/tests/r3_18m_following_control.rs`\n\nNo Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file entered the clean production commit.\n\n## Validation\n\n- 6 focused R3.18M tests PASS;\n- full `mimir-replay` regression PASS;\n- workspace check/test PASS;\n- workspace clippy with warnings denied PASS;\n- repository verifier PASS;\n- exact clean-candidate Windows CI PASS;\n- exact published-main Windows CI PASS;\n- source audit: exactly one `read_bit`, zero following stream/header/payload decoder calls, zero property loops.\n\nThe v1 and v2 branches are non-authority orchestration attempts. v2 proved the production patch through repository verification; its final scope check failed only because `git diff --name-only` omits an untracked newly-created test file. v3 corrected the audit by combining tracked diff and untracked-file enumeration; the production patch itself was unchanged.\n\n## Hard stop\n\nR3.18M does not admit `false` in this context, a following stream ID/header/payload, another property-control bit, repeated/generalized property iteration, a chainable public cursor, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening, or support/dependency expansion.\n\n## Next exact pass\n\n`R3.18N — published R3.18M after-second-payload control real-replay differential audit` over the immutable 47-row R3.18L lane. Only a clean Outcome A may open a separate evidence pass for the following property header.\n''',encoding='utf-8',newline='\n')

# Next execution spec.
Path('docs/continuity/MIMIR_R3_18N_EXECUTION_SPEC.md').write_text(f'''# MIMIR R3.18N — Published After-Second-Payload Control Real-Replay Differential Audit\n\n**Status:** ACTIVE\n**Pass type:** read-only evidence / production differential\n**Production authority:** R3.18M `{PROD}`\n**Production mutation:** forbidden\n**Following stream/header/payload:** forbidden\n\n## 1. Goal\n\nDifferentially validate the published R3.18M true-only following-control composition over the exact frozen R3.18L 47-row lane. Invoke the production R3.18M API, not a lower-level bit reader, and prove exact start/value/end/stop behavior without consuming the following stream ID or any later property data.\n\n## 2. Frozen authority\n\n```text\nproduction SHA/tree                 {PROD} / {PROD_TREE}\nlib.rs blob                         {LIB_BLOB}\nR3.18M focused test blob            {TEST_BLOB}\nimplementation v3                   {IMPL_RUN} / {IMPL_JOB} SUCCESS\nclean-candidate CI                  {CANDIDATE_CI} / {CANDIDATE_CI_JOB} SUCCESS\npublished-main CI                   {PUBLISHED_CI} / {PUBLISHED_CI_JOB} SUCCESS\nR3.18L evidence head                9205ac1616e686589938f952782a32f03d0d1488\nR3.18L artifact                     9271817700\nR3.18L artifact digest              sha256:db5d2db96429a4f2b699dca5176fc4d218f9eb9e4faa8dee813b766896f70c1c\nfrozen rows                         47 continuation rows\ncontrol distribution                false=0 / true=47\nR3.18L native/oracle mismatch       0\nfollowing stream/header/payload     0 / 0 / 0\n```\n\nBefore evidence, fetch fresh main, verify production source/test blobs and every receipt above, then reuse the exact R3.18L witnesses without reselection.\n\n## 3. Required differential checks\n\nFor each of 47 rows:\n\n- reconstruct the exact valid R3.18J second-payload result used by R3.18L;\n- invoke `decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1`;\n- require `property_present_start_bit == R3.18J stop == oracle control start`;\n- require value `true`;\n- require exact control end and `stop_bit == start + 1`;\n- require oracle/native mismatch zero;\n- require zero following stream/header/payload bits consumed.\n\nNo false production success is expected or admitted.\n\n## 4. Negative controls\n\nAt minimum: missing/truncated following control bit; malformed prior R3.18J stop; missing/inconsistent prior second header/payload; synthetic false following-control rejection; repeated identical invocation; and poison beginning at returned stop. All must fail closed or remain invariant as appropriate.\n\n## 5. Evidence artifact\n\nEmit a privacy-safe immutable artifact containing exact production receipts, frozen replay/witness identities, per-row control comparison without raw private payload windows, aggregate counts, negative controls, following stream/header/payload consumption counters, mutation counters and hashes of every evidence file.\n\n## 6. Required validation\n\nFocused R3.18M regression, full `mimir-replay`, workspace check/test/clippy, repository verifier, deterministic repeatability, same-head normal CI, privacy scan and production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.\n\n## 7. Hard stop\n\nNo production Rust/Cargo/fixture/corpus/support mutation. Do not consume or semantically claim the following stream ID, header, payload or another control bit. No repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening.\n\n## 8. Outcome gate\n\n### Outcome A\nAll 47 frozen rows match the published R3.18M API exactly with value true, zero mismatch and zero following stream/header/payload bits consumed. Admit R3.18N evidence, then define a separate evidence pass for exactly the following property header through its payload start.\n\n### Outcome B\nA reproducible production/authority mismatch appears. Record it and keep the following-property header boundary closed.\n\n### Outcome C\nAuthority drift, witness reselection, source mutation, privacy failure, following-stream access or validation contradiction. Stop without admission.\n''',encoding='utf-8',newline='\n')

print('R3_18M_CONTINUITY_PATCH=PASS files=7 next=R3.18N')
