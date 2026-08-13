from __future__ import annotations
import json
from pathlib import Path

PROD = '7b17cb9033b6c71d476e500380d78402cbb3c56d'
BASE = '9c0f81a084b2df0e64496af87c0edc50814bcbc6'

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,s): Path(p).write_text(s, encoding='utf-8', newline='\n')
def replace_once(s,a,b,label):
    n=s.count(a)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, found {n}')
    return s.replace(a,b,1)

# Continue handbook: newest override wins.
p='MIMIR_CONTINUE_HERE.md'; s=read(p)
marker='## R3.14D PRODUCTION ADMITTED / ACTIVE R3.14E'
if marker in s: raise SystemExit('continue marker exists')
s += f'''\n\n---\n\n## R3.14D PRODUCTION ADMITTED / ACTIVE R3.14E\n\n> **CURRENT OVERRIDE:** Fresh source/tests and exact-SHA evidence still outrank prose.\n\n```text\nlast production code SHA = {PROD}\nproduction milestone     = R3.14D — first actor envelope header native reader\nR3.14D                   = COMPLETE / PRODUCTION\nACTIVE NEXT PASS         = R3.14E — native first-envelope differential audit\n```\n\nR3.14D decision: `docs/continuity/MIMIR_R3_14D_DECISION.md`.\nR3.14E exact spec: `docs/continuity/MIMIR_R3_14E_EXECUTION_SPEC.md`.\n\nR3.14D production now natively consumes first-frame time/delta through the R3.14C cursor, verifies raw timing bits against the admitted timing preamble, then reads exactly one first actor envelope through `actor_present -> bounded actor_id -> alive -> new` according to branch conditions and stops.\n\nStill closed: `name_id`, object/spawn/property/stream/attribute payloads, second actor/frame, actor state, raw state, events, skills.\n\nR3.14E is evidence-only: compare the native reader against the exact 47-row R3.14A pinned-Boxcars evidence. Production Rust must not change.\n'''
write(p,s)

# Current state top pointer + latest section.
p='docs/continuity/MIMIR_CURRENT_STATE.md'; s=read(p)
s=replace_once(s,'**Production code checkpoint:** `bad2db9d5043a7a0087a4fab1d278df5f36c7717`',f'**Production code checkpoint:** `{PROD}`','current sha')
s=replace_once(s,'**Production milestone:** `R3.14C — private native network bit cursor + bounded-u32 primitive`','**Production milestone:** `R3.14D — first actor envelope header native reader`','current milestone')
s=replace_once(s,'**Next exact pass:** `R3.14D — first actor envelope header native reader`','**Next exact pass:** `R3.14E — native first-envelope differential audit`','current next')
s += f'''\n\n---\n\n# 19. R3.14D production admission / R3.14E active\n\nR3.14D is production at `{PROD}`. The first native reader now materializes one first-frame/first-actor envelope header through `new` only.\n\nValidation: 17 focused tests PASS; locked repository verifier PASS; clean CI `31702049792` SUCCESS; published-main CI `31702341993` SUCCESS; source blob `67752868807c0b7169e46f22762c7a0ea9efce40`; source SHA-256 `06b767622108ca1aea82ee5c0aad6cc503fbcfddaba05012cf022dd901a5a385`.\n\nActive pass: `R3.14E`, evidence-only 47-replay native-vs-pinned-Boxcars differential audit. No production Rust change is allowed.\n'''
write(p,s)

# Structured state.
p='docs/continuity/MIMIR_CONTINUITY_STATE.json'; st=json.loads(read(p))
st['last_production_code_sha']=PROD
st['last_production_milestone']='R3.14D'
st['last_production_milestone_name']='first actor envelope header native reader'
st['current_pass']='R3.14E'
st['current_pass_kind']='evidence-only differential audit: native first actor envelope vs pinned Boxcars over exact 47 replay lane'
st['current_pass_goal']='Compare R3.14D native first-envelope output to immutable R3.14A pinned-Boxcars oracle evidence for all 47 supported replay identities with exact raw timing, actor branch fields, stop bit, and structural context equality.'
st['current_pass_stop_boundary']='Evidence only. Do not change production Rust or consume name_id, object/spawn/property/stream/attribute payloads, second actor/frame, actor state, raw state, events, or skills.'
st['r3_14d']={
 'outcome':'admitted / production','pre_pass_main_sha':BASE,'production_sha':PROD,
 'production_tree':'9252b8f48fb89beda9f4ea63e1367365a1434a20','source_file':'crates/mimir-replay/src/lib.rs',
 'source_git_blob':'67752868807c0b7169e46f22762c7a0ea9efce40','source_sha256':'06b767622108ca1aea82ee5c0aad6cc503fbcfddaba05012cf022dd901a5a385',
 'focused_tests':17,'validation_run':31701754758,'validation_head_sha':'77a5f0f24ee309d6216f7f7bb4bbeb1bfbc6b4ca',
 'validated_bot_sha':'7555acf7f47cbda639a91c649c807797d0eaa57a','validation_artifact_id':9181561121,
 'validation_artifact_sha256':'dab3a48ef1b58cbbbd39c832009fc722d047c21f84c12cb4e8f7cc69313a935d',
 'clean_branch_ci_run':31702049792,'published_main_ci_run':31702341993,
 'first_actor_envelope_reader_in_production':True,'differential_47_replay_admitted':False}
st['next_files_to_read']=[
 'MIMIR_CONTINUE_HERE.md','MIMIR_KNOWLEDGE_GRAPH.md','docs/continuity/MIMIR_CONTINUITY_STATE.json','docs/continuity/MIMIR_CURRENT_STATE.md',
 'docs/continuity/MIMIR_R3_14A_DECISION.md','docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md','docs/continuity/MIMIR_R3_14C_DECISION.md','docs/continuity/MIMIR_R3_14D_DECISION.md','docs/continuity/MIMIR_R3_14E_EXECUTION_SPEC.md',
 'docs/continuity/MIMIR_PASS_PROTOCOL.md','docs/continuity/MIMIR_BOUNDARY_LOCKS.md','docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md','docs/continuity/MIMIR_PROGRESS_LEDGER.md']
write(p,json.dumps(st,ensure_ascii=False,indent=2)+'\n')

# Ledger append.
p='docs/continuity/MIMIR_PROGRESS_LEDGER.md'; s=read(p)
marker='## 2026-08-13 — R3.14D — First actor envelope header native reader'
if marker in s: raise SystemExit('ledger marker exists')
s += f'''\n\n---\n\n## 2026-08-13 — R3.14D — First actor envelope header native reader\n\nProduction base SHA: `{BASE}`\nProduction commit SHA: `{PROD}`\nPass type: narrow production implementation + clean reconstruction + publication\nOutcome: **ADMITTED / PRODUCTION**\n\nWhat changed:\n- added native first-frame/first-actor result/reader through `new`;\n- consumed timing raw bits through the native cursor and cross-checked timing preamble raw bits;\n- used canonical bounded-u32 for actor ID;\n- preserved branch-dependent `Option` state and stopped before `name_id`.\n\nValidation:\n- 17 focused tests PASS;\n- full locked repository verifier PASS;\n- source blob `67752868807c0b7169e46f22762c7a0ea9efce40`;\n- source SHA-256 `06b767622108ca1aea82ee5c0aad6cc503fbcfddaba05012cf022dd901a5a385`;\n- validation artifact SHA-256 `dab3a48ef1b58cbbbd39c832009fc722d047c21f84c12cb4e8f7cc69313a935d`;\n- clean CI `31702049792` SUCCESS;\n- published-main CI `31702341993` SUCCESS.\n\nNext exact pass: `R3.14E — native first-envelope differential audit`.\n'''
write(p,s)

# Boundary latest override.
p='docs/continuity/MIMIR_BOUNDARY_LOCKS.md'; s=read(p)
s += f'''\n\n---\n\n## CURRENT OVERRIDE — At R3.14E\n\nOPEN / PRODUCTION at `{PROD}`:\n```text\nprivate native bit primitives\nfirst frame timing raw/value native consumption\none first actor envelope: actor_present -> bounded actor_id -> alive -> new, branch-dependent\n```\n\nR3.14E is EVIDENCE-ONLY differential audit. Production source remains frozen.\n\nStill CLOSED: `name_id`, post-name bit, object/spawn/property/stream/attribute payloads, second actor/frame, actor state, raw state, events, skills.\n'''
write(p,s)

# Roadmap current pointer.
p='docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md'; s=read(p)
s=replace_once(s,'**Scope:** from current R3.14D checkpoint to the full MIMIR target architecture','**Scope:** from current R3.14E checkpoint to the full MIMIR target architecture','roadmap scope')
s=replace_once(s,'**Current production checkpoint:** R3.14C private native bit cursor + bounded-u32 primitive','**Current production checkpoint:** R3.14D first actor envelope header native reader','roadmap prod')
s=replace_once(s,'**Current next pass:** R3.14D first actor envelope header native reader','**Current next pass:** R3.14E native first-envelope differential audit','roadmap next')
s=replace_once(s,'# D. R3.14D — First actor envelope header native reader — ACTIVE','# D. R3.14D — First actor envelope header native reader — COMPLETE / PRODUCTION','roadmap D')
s=replace_once(s,'# E. R3.14E — Native first-envelope differential audit','# E. R3.14E — Native first-envelope differential audit — ACTIVE','roadmap E')
write(p,s)

# Continuity README.
p='docs/continuity/README.md'; s=read(p)
s=s.replace('### `MIMIR_R3_14D_EXECUTION_SPEC.md`\n**Şu anda yapılacak exact pass.** First frame + one first actor-envelope header through `new`, then hard stop before `name_id`.','### `MIMIR_R3_14D_DECISION.md`\nCompleted R3.14D production admission for one first actor-envelope header through `new`.\n\n### `MIMIR_R3_14E_EXECUTION_SPEC.md`\n**Şu anda yapılacak exact pass.** Evidence-only 47-replay native-vs-pinned-Boxcars differential audit.')
write(p,s)

# Superbook latest current truth.
p='MIMIR_ALL_SOURCES_SUPERBOOK.md'; s=read(p)
s += f'''\n\n---\n\n## CURRENT REPLAY DECODER ADMISSION UPDATE — R3.14D PRODUCTION / R3.14E ACTIVE\n\nCurrent production code SHA is `{PROD}`. MIMIR now has one native first actor-envelope reader through `new`, but fields after `new` remain closed. Active pass R3.14E is evidence-only and must compare all 47 current supported replay identities against the exact R3.14A pinned-Boxcars evidence before R3.15A can open. Historical parser sources remain evidence/migration material only.\n'''
write(p,s)

# Knowledge graph append newest mandatory reading and chain override.
p='MIMIR_KNOWLEDGE_GRAPH.md'; s=read(p)
s += f'''\n\n---\n\n## LATEST CANONICAL OVERRIDE — R3.14D PRODUCTION / R3.14E ACTIVE\n\n```text\nR3.14C primitives — production\n        |\n        v\nR3.14D first actor envelope reader — PRODUCTION {PROD}\n        |\n        v\nR3.14E 47-replay native-vs-Boxcars differential audit — ACTIVE / evidence-only\n        |\n        v\nR3.15A NewActor evidence — CLOSED until R3.14E Outcome A\n```\n\nLatest mandatory reading order:\n1. `MIMIR_CONTINUE_HERE.md`\n2. `docs/continuity/MIMIR_CONTINUITY_STATE.json`\n3. `docs/continuity/MIMIR_CURRENT_STATE.md`\n4. `docs/continuity/MIMIR_R3_14D_DECISION.md`\n5. `docs/continuity/MIMIR_R3_14E_EXECUTION_SPEC.md`\n6. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n7. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n8. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n9. `docs/continuity/MIMIR_PROGRESS_LEDGER.md`\n10. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n11. `docs/chatgpt-archive/README.md`\n12. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n13. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n14. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`\n\nCurrent code/tests and exact-SHA evidence still outrank every document.\n'''
write(p,s)

# Handoff concise current prompt.
p='docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md'
write(p,f'''# MIMIR — Next Chat Handoff\n\nRepository: `Naveax/MIMIR`\n\nFresh main must first be compared to `{PROD}`. Apply the latest mandatory reading order in `MIMIR_KNOWLEDGE_GRAPH.md`.\n\nCurrent production milestone: R3.14D first actor envelope header native reader.\nActive exact pass: R3.14E evidence-only native-vs-pinned-Boxcars differential audit.\n\nR3.14E must use the exact 47 replay identities and oracle rows from R3.14A, pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`, selector manifest SHA-256 `28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55`, and oracle artifact SHA-256 `d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b`.\n\nRequire 47/47 exact equality for time raw u32, delta raw u32, actor_present, actor_id, alive, new, stop_bit, plus structural context. No production Rust changes. Hard stop remains before name_id and every later network/semantic layer.\n\nIf Outcome A, next is R3.15A NewActor read-only differential evidence.\n''')

print('R3_14D_CONTINUITY_SYNC_PATCH=PASS')
