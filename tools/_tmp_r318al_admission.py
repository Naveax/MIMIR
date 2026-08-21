from pathlib import Path
import json, re

BASE='02233c8125e658513dcb068370c48b1e8f15a01c'
BASE_TREE='fc9293d821dd3e6e269763c3c0ab091428c29490'
PROD='f20f529e3ada6e9a671ea91e5676a17a00770145'
PROD_TREE='98c675811cca4e4d7f0122c762f371548c9266c2'
AL_HEAD='06b8570a25a989651fc800a4ded900ce5e2f3dbe'
AL_TREE='2753baa23be49a819cfceb333977473864a1b02b'
AL_RUN='32469442033'
AL_JOB='96732952709'
AL_PUSH_CI='32469442060'
AL_PUSH_JOB='96732952869'
AL_PR_CI='32470066272'
AL_PR_JOB='96734795022'
AL_ART='9442034802'
AL_ART_SIZE='14650'
AL_DIGEST='sha256:5fcb8f796ba365193698d5d27e2e7dc0e8c221dd42d7a901e956522b7ca1f639'
AI_HEAD='9d424dae2ed8cc7a0a6868111805a48763131196'
AI_RUN='32418184036'
AI_JOB='96584056481'
AI_ART='9424764320'
AI_DIGEST='sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5'
AJ='cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c'
BOXCARS='c70e77df7af81b436cb545d070bb90c82f562d0b'

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,s):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(s,encoding='utf-8',newline='\n')
def rep(s,old,new,label):
    if old not in s: raise SystemExit(f'missing replacement {label}')
    return s.replace(old,new,1)

# New canonical decision.
write('docs/continuity/MIMIR_R3_18AL_DECISION.md', f'''# MIMIR R3.18AL — Published R3.18AK Following-Header Differential Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / CLOSED**
**Pass type:** read-only published-production differential
**Production mutation:** none
**Canonical production:** R3.18AK `{PROD}` / `{PROD_TREE}`

## Decision

R3.18AL closes Outcome A. On exactly the immutable 47-row R3.18AI authority, published R3.18AK matched the frozen AI header result and the direct stateless native header primitive on all 47 rows through `payload_start`. Exact R3.18AJ membership reconstructed 17/17 contexts with multiplicity 47/47, every row remained `Int`, native/oracle mismatch was zero, witness reselection was zero, and following-payload / second-later-control consumption remained `0/0`.

R3.18AL is evidence only. It changes no production Rust and does not admit the following payload, another property-control bit, a generic/repeated property cursor, next actor/frame behavior or semantic/runtime/export widening.

## Exact authority

```text
canonical parent/main               {BASE}
canonical parent tree               {BASE_TREE}
production SHA/tree                 {PROD} / {PROD_TREE}
R3.18AI evidence                    {AI_HEAD} / {AI_RUN}/{AI_JOB} SUCCESS
R3.18AI artifact                    {AI_ART} / {AI_DIGEST}
R3.18AJ contract                    sha256:{AJ}
R3.18AL evidence head/tree          {AL_HEAD} / {AL_TREE}
R3.18AL evidence run/job            {AL_RUN} / {AL_JOB} SUCCESS
R3.18AL natural push CI             {AL_PUSH_CI} / {AL_PUSH_JOB} SUCCESS
R3.18AL validation PR CI            {AL_PR_CI} / {AL_PR_JOB} SUCCESS
R3.18AL validation PR               #130 closed unmerged
R3.18AL artifact                    {AL_ART} / {AL_ART_SIZE} bytes
R3.18AL artifact digest             {AL_DIGEST}
artifact inner manifest             10/10 PASS
```

## Admitted evidence

```text
frozen rows                         47/47
published R3.18AK exact             47/47
direct stateless header exact       47/47
R3.18AJ exact contexts              17/17
R3.18AJ multiplicity                47/47
observed tags                       Int=47
native/oracle mismatch              0
witness reselection                 0
repeatability                       PASS
header truncation                   PASS
corrupt AG/prior/control            PASS
wrong actor                         PASS
unresolved lookup                   PASS
wrong version/context               PASS
Cartesian/fabricated/old-Z-only     PASS
post-payload-start poison           PASS
following payload bits consumed     0
second later control bits consumed  0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                             PASS
```

## Next gate

R3.18AM is a separate read-only evidence pass. It may characterize **exactly one** payload beginning at the published R3.18AK `payload_start` on exactly these same 47 frozen rows. The exact Boxcars target coordinate/ordinal must be reconstructed and verified from the immutable authority rather than assumed. The observed header tag `Int=47` is a header fact only: payload width/value/end must be independently proven against pinned Boxcars and the narrow existing native primitive. R3.18AM must stop at that one payload end and consume zero bits from another property-control boundary.
''')

# Next pass spec.
write('docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md', f'''# MIMIR R3.18AM — Post-AK Following-Property Payload Real-Replay Evidence

**Status:** ACTIVE
**Pass type:** read-only evidence / payload boundary discovery
**Production authority:** R3.18AK `{PROD}` / `{PROD_TREE}`
**Frozen parent differential:** R3.18AL `{AL_HEAD}` / `{AL_RUN}/{AL_JOB}`
**Contract authority:** R3.18AJ `sha256:{AJ}`
**Production mutation:** forbidden
**Another property control / repeated loop:** forbidden

## 1. Goal

Characterize exactly one payload beginning at published R3.18AK `stop_bit == following_header.payload_start_bit` on exactly the immutable 47-row R3.18AL/R3.18AI lane. Compare pinned Boxcars `{BOXCARS}` against the narrowest already-admitted native payload primitive for the observed header tag, prove exact payload start/end/width/value, and stop at that one payload end. Consume no later `property_present` bit.

R3.18AM is evidence only. It does not create a production payload-composition API.

## 2. Frozen authority

```text
production SHA/tree                 {PROD} / {PROD_TREE}
R3.18AJ contract                    sha256:{AJ}
R3.18AI immutable evidence          {AI_HEAD} / {AI_RUN}/{AI_JOB} / artifact {AI_ART}
R3.18AL evidence head/tree          {AL_HEAD} / {AL_TREE}
R3.18AL authority run/job           {AL_RUN} / {AL_JOB} SUCCESS
R3.18AL natural push CI             {AL_PUSH_CI} / {AL_PUSH_JOB} SUCCESS
R3.18AL validation PR CI            {AL_PR_CI} / {AL_PR_JOB} SUCCESS
R3.18AL artifact                    {AL_ART} / {AL_ART_SIZE} / {AL_DIGEST}
frozen rows                         47
header contexts                     17
header tags                         Int=47
witness reselection                 0
pinned Boxcars                      {BOXCARS}
```

Before evidence, fetch fresh `main`, require the exact production/AL/AJ authorities above, verify the immutable AL artifact and its 10/10 inner manifest, and prove witness reselection remains zero.

## 3. Exact source lane

Reuse exactly the 47 frozen R3.18AL rows. Do not select new replays, actors, properties or easier payloads. Reconstruct the exact valid R3.18AG prior/control and published R3.18AK header on every row and require the published AK stop to equal the frozen payload start.

The Boxcars target property coordinate, including its zero-based ordinal if instrumentation needs one, must be derived from and checked against the frozen witness identity. Do **not** hard-code a guessed ordinal merely by extrapolating from R3.18AC.

`Int=47` is a header fact only. R3.18AM must independently prove payload width, end and semantic value from the real lane.

## 4. Oracle/native rules

Instrument only pinned Boxcars `{BOXCARS}` at the exact frozen target coordinate and emit privacy-safe payload facts after the target attribute decoder consumes that one payload. Record exact payload start/end/width and semantic value sufficient for equality without emitting private raw windows.

For the native candidate, reuse the narrow existing admitted primitive for `Int`; do not invent a second parser and do not generalize to other tags. Known lower-level decoder capability is not evidence of this boundary: native/oracle start, end, width and semantic value must match on every row.

## 5. Differential checks

For every frozen row require:

- published R3.18AK reconstructs exactly and stops at frozen `payload_start`;
- pinned Boxcars target identity matches replay/frame/actor/property coordinates exactly;
- native candidate tag remains the frozen `Int` header tag;
- native/oracle payload start exact;
- native/oracle payload end exact;
- native/oracle payload width exact;
- native/oracle semantic value exact;
- deterministic repeated invocation;
- zero bits from the next property-control boundary consumed.

Report the exact observed width/value-shape distribution. Do not infer or inherit payload layout from R3.18AC or any older boundary.

## 6. Negative controls

At minimum require payload-prefix truncation rejection, wrong-tag decoder rejection, wrong replay/context rejection, malformed start/end rejection, repeated-invocation equality, post-payload poison invariance and proof that another `property_present` control is never inspected. Permanent AK/AJ widening negatives remain PASS.

## 7. Evidence artifact

Produce one privacy-safe immutable artifact containing exact production/AL/AJ/Boxcars receipts, frozen witness/replay identities, per-row AK/header identity and oracle/native payload comparison, exact width/value distribution, negative-control results, another-control consumption count, mutation counters and a SHA-256 manifest covering every artifact payload file.

## 8. Validation

Require deterministic double-run equality, permanent AK tests PASS, relevant primitive tests PASS, full `mimir-replay`, workspace fmt/check/test/clippy and repository verifier PASS, exact evidence-head normal CI SUCCESS, privacy PASS, witness reselection zero and production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`. Before any workflow dispatch or PR, reuse an equivalent queued/in-progress run for the same SHA/workflow/input.

## 9. Hard stop

R3.18AM may not mutate production Rust, Cargo, fixtures, corpus, dependencies or support lanes. It may not consume another property-control bit, create a generic/repeated property cursor, iterate another actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 10. Outcome gate

### Outcome A
All 47 frozen rows match pinned Boxcars exactly through one payload end, exact observed payload facts are complete, mismatch/reselection/another-control consumption are zero, privacy passes and production mutation is zero. Admit R3.18AM evidence. A later separate production pass may implement only the exact payload form justified by these facts.

### Outcome B
A reproducible native/oracle mismatch appears inside the bounded payload. Preserve the exact privacy-safe coordinate and keep production widening closed.

### Outcome C
Authority drift, witness reselection, privacy failure, another-control access, unproven payload shape, source mutation or validation contradiction. Stop without admission.
''')

# Small canonical state files.
write('docs/continuity/MIMIR_CURRENT_STATE.md', f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-21
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18AK — bounded post-AG following-header production composition`
**Last read-only evidence:** `R3.18AL — Outcome A / published-AK 47/47 / direct-header 47/47 / 17 exact AJ contexts / Int=47 / mismatch 0 / artifact {AL_ART}`
**Last contract:** `R3.18AJ — Outcome A / exact_tuple_only / 17 contexts / multiplicity 47 / sha256:{AJ}`
**Current exact pass:** `R3.18AM — read-only post-AK following-property payload evidence`

## Truthful boundary

Production remains R3.18AK. It validates one published R3.18AG true-control result, decodes exactly one following existing-actor header with the existing stateless primitive, requires complete R3.18AJ seven-field membership and stops exactly at `payload_start`.

R3.18AL closed Outcome A on the exact immutable 47-row AI lane: published AK and the direct stateless native header matched 47/47, all 17 AJ contexts reconstructed with multiplicity 47/47, every header tag was Int, mismatch/reselection were zero and payload/second-control consumption stayed 0/0.

```text
production SHA/tree                 {PROD} / {PROD_TREE}
AJ contract                         sha256:{AJ}
AL evidence head/tree               {AL_HEAD} / {AL_TREE}
AL authority run/job                {AL_RUN}/{AL_JOB} SUCCESS
AL natural push CI                  {AL_PUSH_CI}/{AL_PUSH_JOB} SUCCESS
AL validation PR CI                 {AL_PR_CI}/{AL_PR_JOB} SUCCESS
AL artifact                         {AL_ART} / {AL_ART_SIZE} bytes / {AL_DIGEST}
```

R3.18AM is read-only and may characterize exactly one payload beginning at the published AK `payload_start` on those same 47 rows. Payload facts must be independently proven against pinned Boxcars; production payload composition and another control remain closed.
''')

p='docs/continuity/MIMIR_BOUNDARY_LOCKS.md'; s=read(p)
start=s.index('# 0. Current override')
end=s.index('# 1. Status vocabulary')
new=f'''# 0. Current override — R3.18AL closed / R3.18AM active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AK
- `{PROD}` / `{PROD_TREE}`;
- one valid published R3.18AG true-control prerequisite;
- exact R3.18AJ seven-field membership;
- exactly one following existing-actor header; stop exactly at `payload_start`.

## CLOSED EVIDENCE — R3.18AL Outcome A
- exact immutable R3.18AI 47-row lane; witness reselection 0;
- published AK 47/47 and direct stateless header 47/47;
- exact AJ contexts 17/17, multiplicity 47/47, Int=47, mismatch 0;
- following-payload/second-control consumption 0/0;
- authority `{AL_RUN}/{AL_JOB}`, natural push CI `{AL_PUSH_CI}/{AL_PUSH_JOB}`, validation PR CI `{AL_PR_CI}/{AL_PR_JOB}` SUCCESS;
- artifact `{AL_ART}` / `{AL_DIGEST}` / inner manifest 10/10 PASS.

## CLOSED CONTRACT — R3.18AJ Outcome A
- `exact_tuple_only` 17 complete seven-field tuples; multiplicity 47; contract `sha256:{AJ}`;
- R3.18Z/R3.18P inheritance false.

## ACTIVE READ-ONLY GATE — R3.18AM
- exactly the same frozen 47 AL/AI rows; witness reselection forbidden;
- start at published AK `payload_start`, compare pinned Boxcars against the narrow native Int primitive;
- prove exact payload start/end/width/value rather than inheriting an older payload layout;
- stop at exactly one payload end; another control remains unopened; production mutation forbidden.

## CLOSED
- post-AK payload production composition; another property control; generic/repeated property cursor/loop;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

---

'''
write(p,s[:start]+new+s[end:])

write('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md', f'''# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AK** at `{PROD}` / `{PROD_TREE}`. It composes exactly one post-AG following header after a valid R3.18AG true control, requires full R3.18AJ exact-tuple membership, and stops at `payload_start`; no post-AK payload composition is production.

R3.18AL is **CLOSED Outcome A**. Authority `{AL_HEAD}` / tree `{AL_TREE}` / run-job `{AL_RUN}/{AL_JOB}` is SUCCESS. Natural same-head push CI `{AL_PUSH_CI}/{AL_PUSH_JOB}` and validation PR CI `{AL_PR_CI}/{AL_PR_JOB}` are SUCCESS. Artifact `{AL_ART}` is `{AL_ART_SIZE}` bytes with digest `{AL_DIGEST}` and internal manifest 10/10 PASS. Published-AK/direct-header equality is 47/47, AJ contexts 17/17, multiplicity 47/47, Int=47, mismatch 0, witness reselection 0 and payload/second-control consumption 0/0.

The active pass is **R3.18AM**, read-only following-payload evidence on exactly those same 47 rows. It must reconstruct the frozen Boxcars target coordinate, prove exact one-payload start/end/width/value independently, use the narrow existing Int primitive, and stop before another property-control bit. Do not infer a payload ordinal or layout merely from older AC evidence.

Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18AL_DECISION.md`, and `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md` first.
''')

# Structured state.
p='docs/continuity/MIMIR_CONTINUITY_STATE.json'; d=json.loads(read(p))
d['last_completed_read_only_audit']='R3.18AL'
d['current_pass']='R3.18AM'
d['current_pass_kind']='read-only evidence / post-AK following-property payload discovery'
d['current_pass_goal']='Characterize exactly one payload beginning at published R3.18AK payload_start on the exact immutable 47-row R3.18AL/R3.18AI lane against pinned Boxcars and the narrow native primitive.'
d['current_pass_stop_boundary']='Stop exactly at the one post-AK payload end. No another control, generic/repeated property cursor, next actor/frame or semantic/runtime/export widening.'
d['last_completed_evidence_pass']='R3.18AL'
if 'last_completed_evidence_outcome' in d:
    d['last_completed_evidence_outcome']='A — published R3.18AK/direct-header exact 47/47; 17/17 AJ contexts; multiplicity 47/47; Int=47; mismatch 0; payload/second-control 0/0.'
files=d.get('next_files_to_read',[])
for newf in ['docs/continuity/MIMIR_R3_18AL_DECISION.md','docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md']:
    if newf not in files:
        try: idx=files.index('docs/continuity/MIMIR_PASS_PROTOCOL.md')
        except ValueError: idx=len(files)
        files.insert(idx,newf)
d['next_files_to_read']=files
write(p,json.dumps(d,indent=2,ensure_ascii=False)+'\n')

# Progress ledger.
p='docs/continuity/MIMIR_PROGRESS_LEDGER.md'; s=read(p)
if '## 2026-08-21 — R3.18AL — Published R3.18AK following-header differential' in s:
    raise SystemExit('ledger AL entry already exists')
entry=f'''\n\n---\n\n## 2026-08-21 — R3.18AL — Published R3.18AK following-header differential\n\nProduction SHA: `{PROD}` / tree `{PROD_TREE}`\nPass type: read-only published-production differential\nOutcome: **A — ADMITTED / CLOSED**\n\nEvidence:\n- exact frozen R3.18AI lane 47/47, witness reselection 0;\n- evidence head/tree `{AL_HEAD}` / `{AL_TREE}`;\n- authority run/job `{AL_RUN}/{AL_JOB}` SUCCESS; natural push CI `{AL_PUSH_CI}/{AL_PUSH_JOB}` SUCCESS; validation PR CI `{AL_PR_CI}/{AL_PR_JOB}` SUCCESS;\n- artifact `{AL_ART}` / `{AL_ART_SIZE}` bytes / `{AL_DIGEST}` / inner manifest 10/10 PASS;\n- published AK 47/47, direct stateless header 47/47, AJ contexts 17/17, multiplicity 47/47, Int=47, mismatch 0;\n- required negative controls PASS; payload/second-control consumption 0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.\n\nBoundary opened:\n- R3.18AM read-only exactly-one following-payload evidence only.\n\nBoundaries still closed:\n- post-AK payload production composition; another property control; generic/repeated property loop/cursor; next actor/frame and semantic/runtime/export widening.\n'''
write(p,s.rstrip()+entry+'\n')

# Knowledge graph current line + reading-order tail + override.
p='MIMIR_KNOWLEDGE_GRAPH.md'; s=read(p)
s=rep(s,'R3.18AL active published-AK following-header differential                                              |','R3.18AL published-AK following-header differential / Outcome A CLOSED                        |\nR3.18AM active post-AK following-property payload evidence                                    |','graph current line')
old='''112. `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`\n113. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n114. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n115. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n116. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n117. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n118. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n119. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
new='''112. `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`\n113. `docs/continuity/MIMIR_R3_18AL_DECISION.md`\n114. `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md`\n115. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n116. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n117. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n118. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n119. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n120. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n121. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
s=rep(s,old,new,'graph reading order')
s += f'''\n\n## CURRENT OVERRIDE — R3.18AL CLOSED / R3.18AM ACTIVE\n\n- Production remains R3.18AK `{PROD}` / `{PROD_TREE}`.\n- R3.18AL Outcome A authority `{AL_HEAD}` / `{AL_TREE}` / `{AL_RUN}/{AL_JOB}` SUCCESS; natural push CI `{AL_PUSH_CI}/{AL_PUSH_JOB}` and validation PR CI `{AL_PR_CI}/{AL_PR_JOB}` SUCCESS.\n- Artifact `{AL_ART}` / `{AL_ART_SIZE}` bytes / `{AL_DIGEST}`; internal manifest 10/10 PASS.\n- Published AK/direct-header exact 47/47; AJ contexts 17/17; multiplicity 47/47; Int=47; mismatch 0; witness reselection 0; payload/second-control 0/0; privacy PASS.\n- R3.18AM is active read-only exactly-one following-payload evidence on the same frozen 47 rows. No payload production composition, another control, generic/repeated property cursor or semantic/runtime widening is admitted.\n'''
write(p,s)

# Master continuity targeted update.
p='MIMIR_CONTINUE_HERE.md'; s=read(p)
s=rep(s,'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AI — one following property-header evidence after published R3.18AG / Outcome A / 47/47 / 17 exact contexts / Int=47 / mismatch 0 / artifact 9424764320',f'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AL — published R3.18AK following-header differential / Outcome A / 47/47 / 17 exact AJ contexts / Int=47 / mismatch 0 / artifact {AL_ART}','continue audit')
s=rep(s,'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AI — one post-AG following header exact / 47 rows / 17 exact contexts / Int=47 / native-oracle mismatch 0 / following-payload-second-control 0/0 / artifact 9424764320',f'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AL — published AK/direct-header differential exact / 47 rows / 17 AJ contexts / Int=47 / mismatch 0 / payload-second-control 0/0 / artifact {AL_ART}','continue evidence')
s=rep(s,'CURRENT_PASS:\n  R3.18AL — published R3.18AK post-AG following-header differential audit','CURRENT_PASS:\n  R3.18AM — post-AK following-property payload real-replay evidence','continue pass')
s=rep(s,'CURRENT_PASS_TYPE:\n  read-only differential audit / validate published R3.18AK on the immutable R3.18AI 47-row lane through payload_start with zero production mutation','CURRENT_PASS_TYPE:\n  read-only evidence / characterize exactly one payload beginning at published R3.18AK payload_start on the immutable 47-row AL/AI lane','continue type')
s=rep(s,'  R3.18AL ACTIVE read-only differential: validate published AK on the exact immutable R3.18AI 47-row lane; production remains frozen at R3.18AK',f'  R3.18AL CLOSED Outcome A: published AK/direct-header exact 47/47; AJ contexts 17/17; multiplicity 47/47; Int=47; mismatch 0; payload/second-control 0/0; artifact {AL_ART}\n  R3.18AM ACTIVE read-only following-payload evidence on the same 47 rows; independently prove exact payload start/end/width/value and stop before another control','continue hard stop')
s=rep(s,'[>] R3.18 complete property loop — active R3.18AL published-AK following-header differential','[>] R3.18 complete property loop — active R3.18AM post-AK following-payload evidence','continue legend')
old_truth=f'> **MIMIR production is R3.18AK `{PROD}` / tree `{PROD_TREE}`. R3.18AK is CLOSED Outcome A: one post-AG following header, exact R3.18AJ 17-tuple membership, stop exactly at `payload_start`, published-main CI `32459617440/96703744791` SUCCESS. R3.18AL is active read-only published-AK differential on the immutable R3.18AI 47-row lane; payload, another control, loops/cursors and actor/frame/semantic/runtime widening remain closed.**'
new_truth=f'> **MIMIR production remains R3.18AK `{PROD}` / tree `{PROD_TREE}`. R3.18AL is CLOSED Outcome A on the immutable 47-row AI lane: published AK/direct-header exact 47/47, AJ contexts 17/17, Int=47, mismatch 0, payload/second-control 0/0, artifact `{AL_ART}`. R3.18AM is active read-only exactly-one following-payload evidence; production payload composition, another control, generic/repeated property cursors and actor/frame/semantic/runtime widening remain closed.**'
s=rep(s,old_truth,new_truth,'continue one-line truth')
closure=f'''R3_18AL_EVIDENCE_CLOSURE:\n  Outcome A / read-only / production unchanged at {PROD}\n  authority head/tree: {AL_HEAD} / {AL_TREE}\n  authority run/job: {AL_RUN} / {AL_JOB} SUCCESS\n  natural same-head push CI: {AL_PUSH_CI} / {AL_PUSH_JOB} SUCCESS\n  validation PR #130 CI: {AL_PR_CI} / {AL_PR_JOB} SUCCESS / closed unmerged\n  artifact: {AL_ART} / {AL_ART_SIZE} bytes / {AL_DIGEST}; downloaded ZIP digest exact / inner manifest 10/10 PASS\n  frozen rows 47/47 / published AK 47/47 / direct header 47/47 / AJ contexts 17/17 / multiplicity 47/47 / Int=47\n  mismatch 0 / witness reselection 0 / following payload + second later control bits 0/0 / privacy PASS\n  production-Cargo-fixture-corpus-support mutation 0/0/0/0/0\n\n'''
if 'R3_18AL_EVIDENCE_CLOSURE:' not in s:
    marker='R3_18AK_PRODUCTION_CLOSURE:'
    if marker not in s: raise SystemExit('missing AK closure marker')
    s=s.replace(marker,closure+marker,1)
marker='# CURRENT PASS CHECKLIST — R3.18AL'
pos=s.find(marker)
if pos<0: raise SystemExit('missing AL checklist marker')
check=f'''# HISTORICAL PASS CHECKLIST — R3.18AL (ADMITTED OUTCOME A)\n\n**Goal:** differentially validate published R3.18AK on exactly the immutable R3.18AI 47-row lane through `payload_start`, with zero production mutation.\n\n```text\n[x] Freeze production/tree, AI authority/artifact and exact AJ contract.\n[x] Reuse exactly the 47 frozen AI rows with witness reselection 0.\n[x] Compare published AK to frozen AI and direct stateless header on 47/47.\n[x] Reconstruct exact AJ membership 17/17 and multiplicity 47/47; Int=47.\n[x] Require stop_bit == payload_start exactly on 47/47.\n[x] Run truncation, corrupt-prior/control, wrong actor/lookup/version, Cartesian/fabricated/old-Z-only, repeatability and post-payload poison negatives.\n[x] Require following-payload / second-control consumption 0/0 and production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.\n[x] Produce privacy-safe artifact {AL_ART} / {AL_DIGEST}; inner manifest 10/10 PASS.\n[x] Authority {AL_RUN}/{AL_JOB}, natural push CI {AL_PUSH_CI}/{AL_PUSH_JOB}, validation PR CI {AL_PR_CI}/{AL_PR_JOB} SUCCESS.\n[x] Outcome A opens only separate R3.18AM read-only following-payload evidence.\n```\n\n---\n\n# CURRENT PASS CHECKLIST — R3.18AM\n\n**Goal:** characterize exactly one payload beginning at published R3.18AK `payload_start` on the exact immutable 47-row AL/AI lane, prove exact payload facts against pinned Boxcars, and stop before another control.\n\n```text\n[ ] Fetch fresh main and require R3.18AK production {PROD} / {PROD_TREE}.\n[ ] Freeze AL authority {AL_HEAD} / {AL_RUN}/{AL_JOB}, artifact {AL_ART}/{AL_DIGEST}, natural push CI {AL_PUSH_CI}/{AL_PUSH_JOB} and validation CI {AL_PR_CI}/{AL_PR_JOB}.\n[ ] Verify AL ZIP digest + inner manifest, frozen 47-row identity, witness reselection 0 and AJ contract sha256:{AJ}.\n[ ] Derive and verify the exact pinned-Boxcars target coordinate/ordinal from the frozen witness; do not assume it from older AC.\n[ ] Reconstruct published AK exactly on every row and require start == frozen payload_start.\n[ ] Compare native/oracle payload start/end/width/value on all 47 observed Int rows.\n[ ] Report exact observed width/value-shape distribution; do not inherit AC payload layout by assumption.\n[ ] Run truncation, wrong-tag/context, malformed-boundary, repeatability and post-payload-poison controls.\n[ ] Require another-property-control bits consumed 0 and production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.\n[ ] Produce privacy-safe immutable artifact with deterministic double-run equality and internal hashes.\n[ ] Require permanent AK/AJ focused tests and exact evidence-head normal CI/full repository verifier PASS.\n[ ] Outcome A may open only a later separate bounded production pass justified by observed AM facts; AM itself is evidence only.\n```\n'''
s=s[:pos]+check
write(p,s)

# Sanity assertions.
required={
'MIMIR_CONTINUE_HERE.md':['R3.18AM — post-AK','R3_18AL_EVIDENCE_CLOSURE:'],
'MIMIR_KNOWLEDGE_GRAPH.md':['R3.18AM active','MIMIR_R3_18AL_DECISION.md','MIMIR_R3_18AM_EXECUTION_SPEC.md'],
'docs/continuity/MIMIR_CONTINUITY_STATE.json':['"current_pass": "R3.18AM"','MIMIR_R3_18AL_DECISION.md','MIMIR_R3_18AM_EXECUTION_SPEC.md'],
'docs/continuity/MIMIR_CURRENT_STATE.md':['R3.18AL — Outcome A','R3.18AM'],
'docs/continuity/MIMIR_BOUNDARY_LOCKS.md':['R3.18AL closed / R3.18AM active'],
'docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md':['R3.18AL is **CLOSED Outcome A**','R3.18AM'],
'docs/continuity/MIMIR_PROGRESS_LEDGER.md':['## 2026-08-21 — R3.18AL —'],
'docs/continuity/MIMIR_R3_18AL_DECISION.md':[AL_HEAD,AL_DIGEST],
'docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md':[AL_HEAD,BOXCARS],
}
for p,marks in required.items():
    t=read(p)
    for m in marks:
        if m not in t: raise SystemExit(f'{p} missing {m}')
print('R3_18AL_ADMISSION_GENERATOR=PASS files=9 current=R3.18AM')
