from pathlib import Path
import json, os

PROD='ccadbf148381c007890d13d5fe8120866a0f40f9'
TREE='0882601060d0bb6d37fcc03ae7273dcf50dd0be3'
PARENT='671cd19a7d034b1377de5bed1dfd36600f45c8d7'
LIB='1254d5a3b0299677f6661712c371aacf27cdb45d'
TEST='013ad6da300cd88f7821b18634736e016af63276'
BUILDER='32241956973'
BUILDER_JOB='96034261394'
PR_CI='32242293315'
PR_JOB='96035296746'
Z='81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9'
AC_ART='9359697636'
AC_DIGEST='sha256:a6914044dfd8991d74b95caeb3507fb2469175c4458c5b50b55395b8ea67b9df'
CAND_CI=os.environ['AD_CANDIDATE_CI']
CAND_JOB=os.environ['AD_CANDIDATE_JOB']
MAIN_CI=os.environ['AD_MAIN_CI']
MAIN_JOB=os.environ['AD_MAIN_JOB']
RECEIPT_RUN=os.environ['AD_RECEIPT_RUN']
RECEIPT_JOB=os.environ['AD_RECEIPT_JOB']

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,s): Path(p).write_text(s,encoding='utf-8',newline='\n')
def rep(s,old,new,label):
    if s.count(old) != 1: raise SystemExit(f'{label}: expected one match, got {s.count(old)}')
    return s.replace(old,new,1)

def render_template(src,dst):
    s=read(src)
    replacements={
        '__AD_CANDIDATE_CI__':CAND_CI,
        '__AD_CANDIDATE_JOB__':CAND_JOB,
        '__AD_MAIN_CI__':MAIN_CI,
        '__AD_MAIN_JOB__':MAIN_JOB,
        '__AD_RECEIPT_RUN__':RECEIPT_RUN,
        '__AD_RECEIPT_JOB__':RECEIPT_JOB,
    }
    for old,new in replacements.items():
        if old not in s: raise SystemExit(f'{src}: missing {old}')
        s=s.replace(old,new)
    if '__AD_' in s: raise SystemExit(f'{src}: unresolved placeholder')
    write(dst,s)

render_template('/tmp/MIMIR_R3_18AD_DECISION.template.md','docs/continuity/MIMIR_R3_18AD_DECISION.md')
render_template('/tmp/MIMIR_R3_18AE_EXECUTION_SPEC.template.md','docs/continuity/MIMIR_R3_18AE_EXECUTION_SPEC.md')

# Machine-readable state.
p='docs/continuity/MIMIR_CONTINUITY_STATE.json'; d=json.loads(read(p))
d['updated_date']='2026-08-19'
d['last_production_code_sha']=PROD
d['last_production_milestone']='R3.18AD'
d['last_production_milestone_name']='bounded post-AA ordinal-3 payload composition'
d['current_pass']='R3.18AE'
d['current_pass_kind']='read-only evidence / published R3.18AD ordinal-3 payload differential'
d['current_pass_goal']='Differentially validate published R3.18AD on the exact immutable R3.18AC 47-row lane through one payload end.'
d['current_pass_stop_boundary']='Stop exactly at the published R3.18AD payload end. Do not inspect another property-control bit or widen UniqueId layouts/property iteration.'
for item in [
    'alternate UniqueId systems/layouts in R3.18AD production',
    'another property control after published R3.18AD payload end',
    'generic/repeated property cursor after R3.18AD',
]:
    if item not in d['closed_now']: d['closed_now'].append(item)
for path in ['docs/continuity/MIMIR_R3_18AD_DECISION.md','docs/continuity/MIMIR_R3_18AE_EXECUTION_SPEC.md']:
    if path not in d['next_files_to_read']:
        idx=d['next_files_to_read'].index('docs/continuity/MIMIR_PASS_PROTOCOL.md')
        d['next_files_to_read'].insert(idx,path)
write(p,json.dumps(d,indent=2,ensure_ascii=False)+'\n')

# Current state.
write('docs/continuity/MIMIR_CURRENT_STATE.md',f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-19
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production tree:** `{TREE}`
**Production milestone:** `R3.18AD — bounded post-AA ordinal-3 payload composition`
**Last read-only evidence:** `R3.18AC — Outcome A / 47/47 / ActiveActor 39×33 / Int 7×32 / UniqueId system1-Steam 1×80 / mismatch 0 / another-control 0`
**Last structural contract:** `R3.18Z — exact_tuple_only / 18 complete seven-field tuples / 47 multiplicities / R3.18P inheritance false`
**Current exact pass:** `R3.18AE — published R3.18AD ordinal-3 payload differential`

## Truthful boundary

Production R3.18AD is `{PROD}` / `{TREE}`. Starting only from a valid R3.18AA boundary, it preserves complete R3.18Z exact header membership and decodes exactly one R3.18AC-admitted ordinal-3 payload. ActiveActor is exactly 33 bits, Int exactly 32 bits, and UniqueId exactly system_id=1 / Steam / 80 bits. Production stops at payload end and reads no another property-control bit.

```text
production SHA/tree                 {PROD} / {TREE}
parent                              {PARENT}
lib / focused-test blobs            {LIB} / {TEST}
builder                             {BUILDER}/{BUILDER_JOB}
validation PR CI                    {PR_CI}/{PR_JOB}
exact clean push CI                 {CAND_CI}/{CAND_JOB}
published-main CI                   {MAIN_CI}/{MAIN_JOB}
published receipt helper            {RECEIPT_RUN}/{RECEIPT_JOB}
Z contract SHA256                   {Z}
AC artifact                         {AC_ART} / {AC_DIGEST}
```

R3.18AE is read-only. It must replay the exact AC 47-row lane through the published AD API and require published/frozen/oracle/direct-native equality through exactly one payload end. Production mutation, alternate UniqueId layouts, another control, generalized property iteration and all semantic/runtime widening remain closed.
''')

# Next handoff.
write('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md',f'''# MIMIR — Next Chat Handoff

Canonical production is **R3.18AD** at `{PROD}` / `{TREE}`. It composes exactly one AC-admitted ordinal-3 payload after a valid published R3.18AA boundary, preserves R3.18Z exact header membership, admits only ActiveActor/33, Int/32 and UniqueId system1-Steam/80, and stops exactly at payload end.

R3.18AD authority: builder `{BUILDER}/{BUILDER_JOB}` SUCCESS, validation PR CI `{PR_CI}/{PR_JOB}` SUCCESS, exact clean push CI `{CAND_CI}/{CAND_JOB}` SUCCESS, published-main CI `{MAIN_CI}/{MAIN_JOB}` SUCCESS, publication receipt `{RECEIPT_RUN}/{RECEIPT_JOB}` SUCCESS. Clean production scope is exactly `lib.rs` plus `r3_18ad_post_aa_payload.rs`.

The active pass is **R3.18AE**, read-only published-production differential on the exact immutable R3.18AC 47-row lane. Require 47/47 published/frozen/oracle/direct-native equality through payload end, ActiveActor=39×33, Int=7×32, UniqueId=1×80 system1-Steam, witness reselection 0 and another-control bits 0. No production mutation or later-control access is allowed.
''')

# Boundary lock current override.
p='docs/continuity/MIMIR_BOUNDARY_LOCKS.md'; s=read(p)
start=s.index('# 0. Current override')
end=s.index('# 1. Status vocabulary')
override=f'''# 0. Current override — R3.18AD production / R3.18AE active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AD
- `{PROD}` / `{TREE}`, parent `{PARENT}`;
- valid R3.18AA boundary and full R3.18Z exact header membership remain mandatory;
- exactly one ordinal-3 payload only: ActiveActor/33, Int/32, or UniqueId system1-Steam/80;
- stop exactly at payload end; another property-control bits consumed 0;
- clean scope exactly lib.rs + one focused AD test.

## VALIDATION
- builder `{BUILDER}/{BUILDER_JOB}` SUCCESS;
- validation PR CI `{PR_CI}/{PR_JOB}` SUCCESS;
- exact clean push CI `{CAND_CI}/{CAND_JOB}` SUCCESS;
- published-main CI `{MAIN_CI}/{MAIN_JOB}` SUCCESS;
- receipt helper `{RECEIPT_RUN}/{RECEIPT_JOB}` SUCCESS.

## ACTIVE READ-ONLY GATE — R3.18AE
- exact immutable AC 47-row lane only; witness reselection forbidden;
- published AD vs frozen AC / pinned oracle / direct native must match through payload end;
- no production mutation and no another-control inspection.

## CLOSED
- alternate UniqueId systems/layouts or widths;
- another property control after AD payload end;
- repeated/generalized property loop or generic cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

---

'''
write(p,s[:start]+override+s[end:])

# Progress ledger.
p='docs/continuity/MIMIR_PROGRESS_LEDGER.md'; s=read(p)
if '## 2026-08-19 — R3.18AD —' in s: raise SystemExit('AD ledger entry already exists')
entry=f'''\n\n---\n\n## 2026-08-19 — R3.18AD — Bounded post-AA ordinal-3 payload production\n\nProduction SHA/tree: `{PROD}` / `{TREE}`\nParent: `{PARENT}`\nOutcome: **A — ADMITTED / PRODUCTION**\n\n- exact clean scope: `crates/mimir-replay/src/lib.rs` + `crates/mimir-replay/tests/r3_18ad_post_aa_payload.rs`;\n- lib/test blobs `{LIB}` / `{TEST}`;\n- preserves R3.18AA + R3.18Z exact header authority;\n- admits ActiveActor/33, Int/32, UniqueId system1-Steam/80 only;\n- lower-level-valid Epic 312-bit UniqueId explicitly rejected;\n- focused AD tests 5/5 plus AA/K2/scalar focused suites PASS;\n- full mimir-replay/workspace/clippy/repository verification PASS;\n- builder `{BUILDER}/{BUILDER_JOB}`, PR CI `{PR_CI}/{PR_JOB}`, clean push CI `{CAND_CI}/{CAND_JOB}`, published-main CI `{MAIN_CI}/{MAIN_JOB}` SUCCESS;\n- publication fresh-main `force=false`; receipt `{RECEIPT_RUN}/{RECEIPT_JOB}` SUCCESS;\n- another-control bits consumed 0; no generic loop/cursor or capability widening.\n\nNext exact gate: R3.18AE read-only published-AD differential on the frozen AC 47-row lane.\n'''
write(p,s.rstrip()+entry)

# Knowledge graph.
p='MIMIR_KNOWLEDGE_GRAPH.md'; s=read(p)
s=rep(s,'R3.18AD active bounded post-AA ordinal-3 payload production                                  |','R3.18AD bounded post-AA ordinal-3 payload production / Outcome A CLOSED                  |\nR3.18AE active published R3.18AD ordinal-3 payload differential                              |','KG status')
old='''94. `docs/continuity/MIMIR_R3_18AC_DECISION.md`\n95. `docs/continuity/MIMIR_R3_18AD_EXECUTION_SPEC.md`\n96. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n97. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n98. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n99. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n100. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n101. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n102. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
new='''94. `docs/continuity/MIMIR_R3_18AC_DECISION.md`\n95. `docs/continuity/MIMIR_R3_18AD_EXECUTION_SPEC.md`\n96. `docs/continuity/MIMIR_R3_18AD_DECISION.md`\n97. `docs/continuity/MIMIR_R3_18AE_EXECUTION_SPEC.md`\n98. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n99. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n100. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n101. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n102. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n103. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n104. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
s=rep(s,old,new,'KG order')
s += f'''\n\n## CURRENT OVERRIDE — R3.18AD PRODUCTION / R3.18AE ACTIVE\n\n- Production `{PROD}` / `{TREE}`, parent `{PARENT}`.\n- R3.18AD admits exactly ActiveActor/33, Int/32, UniqueId system1-Steam/80 after valid AA/Z authority; stop at payload end; another-control 0.\n- Builder `{BUILDER}/{BUILDER_JOB}`, PR CI `{PR_CI}/{PR_JOB}`, clean push CI `{CAND_CI}/{CAND_JOB}`, main CI `{MAIN_CI}/{MAIN_JOB}`, receipt `{RECEIPT_RUN}/{RECEIPT_JOB}` all SUCCESS.\n- R3.18AE is active read-only published-AD differential on the exact immutable AC 47-row lane. Alternate layouts, another control, generic loops/cursors and semantic/runtime widening remain closed.\n'''
write(p,s)

# Root continuation state + checklist.
p='MIMIR_CONTINUE_HERE.md'; s=read(p)
for old,new,label in [
('''LAST_PRODUCTION_CODE_SHA:\n  9392240c49f95766c214afee9865fed4155a87a4''',f'''LAST_PRODUCTION_CODE_SHA:\n  {PROD}''','continue prod sha'),
('''LAST_PRODUCTION_MILESTONE:\n  R3.18AA — bounded post-W following-header composition''','''LAST_PRODUCTION_MILESTONE:\n  R3.18AD — bounded post-AA ordinal-3 payload composition''','continue prod milestone'),
('''CURRENT_PASS:\n  R3.18AD — bounded post-AA ordinal-3 following-property payload production''','''CURRENT_PASS:\n  R3.18AE — published R3.18AD ordinal-3 payload differential''','continue pass'),
('''CURRENT_PASS_TYPE:\n  production implementation / compose exactly one AC-admitted ordinal-3 payload after valid R3.18AA''','''CURRENT_PASS_TYPE:\n  read-only evidence / validate published R3.18AD on the exact immutable R3.18AC 47-row lane''','continue type'),
('  R3.18AD ACTIVE production: after valid AA, compose exactly one AC-admitted payload and stop at payload end','  R3.18AD PRODUCTION at ccadbf148381c007890d13d5fe8120866a0f40f9: after valid AA/Z authority, compose exactly one ActiveActor/33, Int/32 or UniqueId system1-Steam/80 payload and stop at payload end\n  R3.18AE ACTIVE read-only: published AD differential on exact AC 47-row lane; another-control consumption must remain 0'),
]: s=rep(s,old,new,label)
closure=f'''R3_18AD_PRODUCTION_CLOSURE:\n  Outcome A / production {PROD} / tree {TREE} / parent {PARENT}\n  lib/test blobs: {LIB} / {TEST}\n  builder: {BUILDER}/{BUILDER_JOB} SUCCESS\n  validation PR CI: {PR_CI}/{PR_JOB} SUCCESS\n  exact clean push CI: {CAND_CI}/{CAND_JOB} SUCCESS\n  published-main CI: {MAIN_CI}/{MAIN_JOB} SUCCESS\n  receipt helper: {RECEIPT_RUN}/{RECEIPT_JOB} SUCCESS\n  clean files: lib.rs + r3_18ad_post_aa_payload.rs only\n  admitted payloads: ActiveActor/33, Int/32, UniqueId system1-Steam/80 only\n  another-control bits 0 / alternate UniqueId layouts rejected / generic loop-cursor 0\n'''
if 'R3_18AD_PRODUCTION_CLOSURE:' not in s:
    marker='R3_18AC_EVIDENCE_CLOSURE:'
    idx=s.index(marker)
    s=s[:idx]+closure+s[idx:]
marker='# CURRENT PASS CHECKLIST — R3.18AD'
pos=s.find(marker)
if pos < 0: raise SystemExit('missing AD checklist')
tail=f'''# HISTORICAL PASS CHECKLIST — R3.18AD (ADMITTED OUTCOME A)\n\n```text\n[x] Freeze exact AC/Z/AA authority and fresh main.\n[x] Compose exactly one payload after valid AA using existing K2/scalar primitives.\n[x] Admit ActiveActor only at 33 bits; Int only at 32 bits; UniqueId only system1-Steam at 80 bits.\n[x] Reject lower-level-valid Epic 312-bit UniqueId at the AD boundary.\n[x] Stop exactly at payload end and consume no another property-control bit.\n[x] Focused AD tests 5/5 plus AA/K2/scalar suites PASS.\n[x] Full mimir-replay/workspace/clippy/repository verification PASS.\n[x] Clean production scope exactly two files.\n[x] Builder {BUILDER}/{BUILDER_JOB}, PR CI {PR_CI}/{PR_JOB}, clean push CI {CAND_CI}/{CAND_JOB}, main CI {MAIN_CI}/{MAIN_JOB} SUCCESS.\n[x] Published by fresh-main force=false fast-forward; receipt {RECEIPT_RUN}/{RECEIPT_JOB} SUCCESS.\n```\n\n---\n\n# CURRENT PASS CHECKLIST — R3.18AE\n\n**Goal:** differentially validate published R3.18AD over the exact immutable R3.18AC 47-row lane through one payload end, with zero production mutation and zero another-control access.\n\n```text\n[ ] Fetch fresh main and require published AD {PROD} / {TREE}, lib/test {LIB} / {TEST}.\n[ ] Verify builder/PR/clean-push/main CI receipts and immutable AC artifact {AC_ART}/{AC_DIGEST}.\n[ ] Reuse exactly the frozen AC 47 rows; witness reselection 0.\n[ ] Invoke published AD on every row and require embedded AA/header equality plus R3.18Z exact membership.\n[ ] Require published/frozen/oracle/direct-native payload start/end/width/value equality 47/47.\n[ ] Reconstruct ActiveActor 39×33, Int 7×32, UniqueId 1×80 system1-Steam exactly.\n[ ] Run truncation, wrong-context/tag, Epic-312 rejection, repeatability and post-payload-poison negatives.\n[ ] Require another-control bits consumed 0 and production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.\n[ ] Produce privacy-safe immutable evidence artifact with full internal hashes and deterministic double-run equality.\n[ ] Require exact evidence-head normal CI plus full focused/workspace/clippy/repository validation.\n[ ] Do not widen to another control, alternate UniqueId layout, generic loop/cursor, next actor/frame or semantic/runtime behavior.\n```\n'''
s=s[:pos]+tail
write(p,s)

required={
'MIMIR_CONTINUE_HERE.md':['R3_18AD_PRODUCTION_CLOSURE:','CURRENT_PASS:\n  R3.18AE'],
'MIMIR_KNOWLEDGE_GRAPH.md':['R3.18AE active published','MIMIR_R3_18AD_DECISION.md','MIMIR_R3_18AE_EXECUTION_SPEC.md'],
'docs/continuity/MIMIR_CONTINUITY_STATE.json':['"last_production_code_sha": "'+PROD+'"','"current_pass": "R3.18AE"'],
'docs/continuity/MIMIR_CURRENT_STATE.md':[PROD,'R3.18AE'],
'docs/continuity/MIMIR_BOUNDARY_LOCKS.md':['R3.18AD production / R3.18AE active'],
'docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md':[PROD,'R3.18AE'],
'docs/continuity/MIMIR_PROGRESS_LEDGER.md':['## 2026-08-19 — R3.18AD —'],
'docs/continuity/MIMIR_R3_18AD_DECISION.md':[PROD,CAND_CI,MAIN_CI],
'docs/continuity/MIMIR_R3_18AE_EXECUTION_SPEC.md':[PROD,CAND_CI,MAIN_CI],
}
for path,marks in required.items():
    t=read(path)
    for mark in marks:
        if mark not in t: raise SystemExit(f'{path}: missing {mark}')
json.loads(read('docs/continuity/MIMIR_CONTINUITY_STATE.json'))
print('R3_18AD_CONTINUITY_GENERATOR=PASS files=9 current=R3.18AE')
