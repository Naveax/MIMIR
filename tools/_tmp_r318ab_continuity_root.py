from pathlib import Path
import json, re, sys

AB_HEAD='b2f4b73600165b2d83389b6ce43709b64beba52a'
AB_TREE='8d36c8c7118db8c6f0d28c4ae88e0400cf4a3cd1'
AB_RUN='32230919566'
AB_JOB='96000311036'
AB_CI_RUN='32230919652'
AB_CI_JOB='96000311479'
AB_ART='9357559410'
AB_SIZE='12607'
AB_DIGEST='sha256:4b6d72b154440ee2b819f5a5ecb6fa3768e086b7ec4ba0d0c53d0e8e3ad23d99'
AB_FAILED_HEAD='f2f79e47fefbe7ee95ea5df84c78a86868f57bb3'
AB_FAILED_RUN='32229955227'
AB_FAILED_JOB='95997443235'
BASE='713298a04bbb5491286e7f4ee5bf47a5d201b28c'
BASE_TREE='5cca2c6c15013895e01ab4acf083fed59f8023da'
PROD='9392240c49f95766c214afee9865fed4155a87a4'
PROD_TREE='968520d480f78c528086e4e31b2ce307f4f8d232'
Z='81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9'

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,s): Path(p).write_text(s,encoding='utf-8',newline='\n')
def rep(s, old, new, label):
    if old not in s:
        raise SystemExit(f'missing replacement {label}')
    return s.replace(old,new,1)

p='docs/continuity/MIMIR_PROGRESS_LEDGER.md'; s=read(p)
entry=f'''\n\n---\n\n## 2026-08-19 — R3.18AB — Published R3.18AA post-W following-header differential\n\nProduction SHA: `{PROD}` / tree `{PROD_TREE}`\nPass type: read-only published-production differential\nOutcome: **A — ADMITTED / CLOSED**\n\nEvidence:\n- exact frozen R3.18Y lane 47/47, witness reselection 0;\n- authority head/tree `{AB_HEAD}` / `{AB_TREE}`;\n- authority run/job `{AB_RUN}/{AB_JOB}` SUCCESS; same-head CI `{AB_CI_RUN}/{AB_CI_JOB}` SUCCESS;\n- artifact `{AB_ART}` / `{AB_SIZE}` bytes / `{AB_DIGEST}`; downloaded ZIP digest exact and inner manifest 9/9 PASS;\n- published-AA/frozen-Y/direct-native mismatch 0; Z contexts 18/18; multiplicities 47/47; ActiveActor=39 / Int=7 / UniqueId=1;\n- repeatability, truncation, wrong actor, unresolved lookup, wrong version and post-payload poison 47/47; Cartesian and R3.18P-valid/Z-absent negatives retained by focused suite;\n- following-payload/another-control bits 0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.\n\nSuperseded attempt:\n- `{AB_FAILED_HEAD}` / `{AB_FAILED_RUN}/{AB_FAILED_JOB}` failed only because a byte-prefix truncation harness cut at `payload_start / 8`, leaving complete header bytes on 8 unaligned rows; positive/equality checks were already 47/47. Corrected authority uses a prefix before the post-W control/header byte. Production was never changed.\n\nBoundaries opened:\n- R3.18AC read-only ordinal-3 following-property payload evidence only.\n\nBoundaries still closed:\n- post-AA payload production composition; another property control; loops/cursors; next actor/frame; semantic/runtime/export widening.\n\nNext exact pass:\n- `R3.18AC — post-AA following-property payload real-replay evidence`.\n'''
if '## 2026-08-19 — R3.18AB —' in s: raise SystemExit('ledger AB entry already exists')
write(p,s.rstrip()+entry)

p='MIMIR_KNOWLEDGE_GRAPH.md'; s=read(p)
s=rep(s,'R3.18AB active published-AA following-header differential spec                                  |','R3.18AB published-AA following-header differential / Outcome A CLOSED                        |\nR3.18AC active post-AA ordinal-3 following-payload evidence                                  |','graph current line')
old='''91. `docs/continuity/MIMIR_R3_18AB_EXECUTION_SPEC.md`\n92. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n93. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n94. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n95. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n96. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n97. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n98. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
new='''91. `docs/continuity/MIMIR_R3_18AB_EXECUTION_SPEC.md`\n92. `docs/continuity/MIMIR_R3_18AB_DECISION.md`\n93. `docs/continuity/MIMIR_R3_18AC_EXECUTION_SPEC.md`\n94. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n95. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n96. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n97. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n98. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n99. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n100. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
s=rep(s,old,new,'graph reading order')
s += f'''\n\n## CURRENT OVERRIDE — R3.18AB CLOSED / R3.18AC ACTIVE\n\n- Production remains R3.18AA `{PROD}` / `{PROD_TREE}`.\n- R3.18AB Outcome A authority `{AB_HEAD}` / tree `{AB_TREE}` / `{AB_RUN}/{AB_JOB}` SUCCESS; same-head CI `{AB_CI_RUN}/{AB_CI_JOB}` SUCCESS.\n- Artifact `{AB_ART}` / `{AB_SIZE}` bytes / `{AB_DIGEST}`; ZIP digest exact and internal 9-entry manifest PASS.\n- Published AA / frozen Y / direct stateless header exact 47/47; R3.18Z contexts 18/18, multiplicities 47/47; ActiveActor=39 / Int=7 / UniqueId=1; mismatch 0; witness reselection 0; payload/control 0/0; privacy PASS.\n- Superseded `{AB_FAILED_HEAD}` / `{AB_FAILED_RUN}/{AB_FAILED_JOB}` was harness-only truncation 39/47; positive/equality checks were already 47/47 and production was unchanged.\n- R3.18AC is active read-only payload evidence at Boxcars property ordinal 3 on the same 47 rows. No payload production composition, another control, loop/cursor or semantic/runtime widening is admitted.\n'''
write(p,s)

p='MIMIR_CONTINUE_HERE.md'; s=read(p)
for old,new,label in [
('''LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18Y — one post-W following header evidence / Outcome A / 47/47 / 18 exact contexts / mismatch 0 / payload-control 0/0''',f'''LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AB — published AA differential / Outcome A / 47/47 / 18 exact Z contexts / mismatch 0 / payload-control 0/0 / artifact {AB_ART}''','continue audit'),
('''LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18Y — post-W following header / Outcome A / 47 rows / 18 exact tuples / ActiveActor=39 Int=7 UniqueId=1 / R3.18P inheritance 0''','''LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AB — published AA/frozen-Y/direct-header differential / Outcome A / 47 rows / 18 exact Z tuples / ActiveActor=39 Int=7 UniqueId=1 / mismatch 0''','continue evidence'),
('''CURRENT_PASS:\n  R3.18AB — published R3.18AA post-W following-header differential''','''CURRENT_PASS:\n  R3.18AC — post-AA ordinal-3 following-property payload evidence''','continue pass'),
('''CURRENT_PASS_TYPE:\n  read-only evidence / differentially validate published R3.18AA on the exact immutable R3.18Y 47-row lane''','''CURRENT_PASS_TYPE:\n  read-only evidence / characterize exactly one ordinal-3 payload after published R3.18AA on the exact immutable 47-row AB/Y lane''','continue type'),
('  R3.18AB ACTIVE read-only published-AA differential on the exact immutable R3.18Y 47-row lane; witness reselection forbidden; payload/control consumption must remain 0/0','  R3.18AB CLOSED Outcome A: published-AA/frozen-Y/direct-header exact 47/47; Z contexts 18/18; multiplicities 47/47; ActiveActor=39 Int=7 UniqueId=1; mismatch 0; payload/control 0/0; artifact 9357559410\n  R3.18AC ACTIVE read-only ordinal-3 payload evidence on the same frozen 47 rows; prove exact payload end/value/layout against pinned Boxcars and stop before another control','continue hard stop'),
('  NO following payload, another control, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted','  NO post-AA payload production composition, another control, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted','continue no'),
]: s=rep(s,old,new,label)
closure=f'''R3_18AB_EVIDENCE_CLOSURE:\n  Outcome A / read-only / production unchanged at {PROD}\n  authority head/tree: {AB_HEAD} / {AB_TREE}\n  authority run/job: {AB_RUN} / {AB_JOB} SUCCESS\n  exact-head normal CI: {AB_CI_RUN} / {AB_CI_JOB} SUCCESS\n  artifact: {AB_ART} / {AB_SIZE} bytes / {AB_DIGEST}; downloaded ZIP digest exact / inner manifest 9/9 PASS\n  frozen rows 47/47 / published-AA-frozen-Y-direct mismatch 0 / Z contexts 18/18 / multiplicities 47/47 / tags 39/7/1\n  repeatability/truncation/wrong-actor/unresolved/wrong-version/post-payload-poison 47/47; Cartesian + P-only-Z-absent PASS\n  witness reselection 0 / following payload + another-control bits 0/0 / privacy PASS / production-Cargo-fixture-corpus-support mutation 0/0/0/0/0\n  superseded attempt {AB_FAILED_HEAD} / {AB_FAILED_RUN}/{AB_FAILED_JOB}: harness-only truncation 39/47; positive/equality checks 47/47; production unchanged\n'''
if 'R3_18AB_EVIDENCE_CLOSURE:' not in s:
    marker='R3_18M_PRODUCTION_CLOSURE:'
    if marker not in s: raise SystemExit('missing closure insertion marker')
    s=s.replace(marker,closure+marker,1)
marker='# CURRENT PASS CHECKLIST — R3.18AB'
pos=s.find(marker)
if pos<0: raise SystemExit('missing AB current checklist')
historical=f'''# HISTORICAL PASS CHECKLIST — R3.18AB (ADMITTED OUTCOME A)\n\n**Goal:** differentially validate published R3.18AA over the exact immutable R3.18Y 47-row lane through `payload_start`, with zero production mutation.\n\n```text\n[x] Freeze production/tree/lib/test, Y authority/artifact and exact Z contract.\n[x] Reuse exactly the 47 frozen Y rows with witness reselection 0.\n[x] Compare published AA to frozen Y and direct stateless native header on 47/47.\n[x] Reconstruct exact Z membership 18/18 and multiplicities 47/47; tags ActiveActor=39 Int=7 UniqueId=1.\n[x] Require returned stop_bit == payload_start exactly on 47/47.\n[x] Run truncation, wrong actor/lookup/version, Cartesian, P-only-Z-absent, repeatability and post-payload-poison negatives.\n[x] Require following-payload / another-control consumption 0/0 and production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.\n[x] Produce privacy-safe artifact {AB_ART} / {AB_DIGEST}; ZIP digest exact, inner manifest 9/9, privacy PASS.\n[x] Exact evidence-head normal CI {AB_CI_RUN}/{AB_CI_JOB} SUCCESS; authority {AB_RUN}/{AB_JOB} SUCCESS.\n[x] Outcome A opens only separate R3.18AC read-only following-payload evidence; AB admits no payload production.\n```\n\n---\n\n# CURRENT PASS CHECKLIST — R3.18AC\n\n**Goal:** characterize exactly one payload beginning at published R3.18AA `payload_start` on the exact immutable 47-row AB/Y lane, compare pinned Boxcars ordinal 3 to the narrow existing native primitive for ActiveActor/Int/UniqueId, and stop before another control.\n\n```text\n[ ] Fetch fresh main; require production {PROD} / {PROD_TREE}, AB authority {AB_HEAD} / {AB_RUN}/{AB_JOB}, same-head CI {AB_CI_RUN}/{AB_CI_JOB}, artifact {AB_ART}/{AB_DIGEST}.\n[ ] Verify AB ZIP digest + inner manifest, frozen 47-row identity, witness reselection 0 and Z contract {Z}.\n[ ] Instrument pinned Boxcars c70e77df7af81b436cb545d070bb90c82f562d0b only at exact zero-based property ordinal 3.\n[ ] Reconstruct published AA exactly on every row and require start == frozen payload_start.\n[ ] Compare native/oracle payload start/end/width/semantic value on ActiveActor=39, Int=7 and UniqueId=1.\n[ ] For UniqueId, independently prove actual system id/layout/width; do not inherit a generic UniqueId width.\n[ ] Report exact width/subshape distributions; do not normalize or fabricate cross-product contexts.\n[ ] Run truncation, wrong-tag/context, repeatability, post-payload-poison and unsupported-UniqueId-layout controls.\n[ ] Require another-property-control bits consumed 0 and production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.\n[ ] Produce privacy-safe immutable artifact with deterministic double-run equality and internal hashes.\n[ ] Require permanent AA + relevant K1/K2 focused tests and exact evidence-head normal CI/full repository verifier PASS.\n[ ] Outcome A may open only a later separate exact payload contract/production gate justified by observed facts; AC itself is evidence only.\n```\n'''
s=s[:pos]+historical
write(p,s)

required={
'MIMIR_CONTINUE_HERE.md':['R3.18AC — post-AA ordinal-3','R3_18AB_EVIDENCE_CLOSURE:'],
'MIMIR_KNOWLEDGE_GRAPH.md':['R3.18AC active','MIMIR_R3_18AB_DECISION.md','MIMIR_R3_18AC_EXECUTION_SPEC.md'],
'docs/continuity/MIMIR_CONTINUITY_STATE.json':['"current_pass": "R3.18AC"','MIMIR_R3_18AB_DECISION.md','MIMIR_R3_18AC_EXECUTION_SPEC.md'],
'docs/continuity/MIMIR_CURRENT_STATE.md':['R3.18AB — Outcome A','R3.18AC'],
'docs/continuity/MIMIR_BOUNDARY_LOCKS.md':['R3.18AB closed / R3.18AC active'],
'docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md':['R3.18AB is **CLOSED Outcome A**','R3.18AC'],
'docs/continuity/MIMIR_PROGRESS_LEDGER.md':['## 2026-08-19 — R3.18AB —'],
'docs/continuity/MIMIR_R3_18AB_DECISION.md':[AB_HEAD,AB_DIGEST],
'docs/continuity/MIMIR_R3_18AC_EXECUTION_SPEC.md':[AB_HEAD,'property ordinal            3'],
}
for p,marks in required.items():
    t=read(p)
    for m in marks:
        if m not in t: raise SystemExit(f'{p} missing {m}')
print('R3_18AB_CONTINUITY_GENERATOR=PASS files=9 current=R3.18AC')
