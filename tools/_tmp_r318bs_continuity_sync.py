from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path('.')
DATE = '2026-09-11'
PROD_SHA = '5ab14575d0a698d752db35db76f3dbb300cdec8d'
PROD_TREE = '1c0b4c0a50385a34ba730a52a98a89423ff56869'
PROD_PARENT = '2f4f536d52a10a28a66bcc7b9b9dc84f7e29b2a6'
PARENT_TREE = '49df3c7cdb8dc36c0190cba51dc5a802f6fde3d2'
LIB_BLOB = '3428608283d6d0022d466671f90afc9304726dd0'
TEST_BLOB = '706bbdee62a09f04af7bcf70e22567793084d0d6'
BS_SPEC_BLOB = '77818f7113a357b2577948e6700bfaf63de27db9'
BUILDER_HEAD = '40009f866344778be8b5e5d4c4577cf292bb1189'
BUILDER_RUN = 34617577982
BUILDER_JOB = 103323236248
CANDIDATE_CI_RUN = 34617945689
CANDIDATE_CI_JOB = 103324450173
PUBLISHED_CI_RUN = 34618640843
PUBLISHED_CI_JOB = 103326748345
BQ_HEAD = '16c43f38e740c57ae9cb90c92084002ec83815e7'
BQ_ARTIFACT = 10144392560
BQ_DIGEST = '52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c'
BR_HEAD = 'ff1daab35e2e75bf7446a98a07a1db67e5196dbd'
BR_ARTIFACT = 10267123608
BR_DIGEST = 'bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1'
BN_CONTRACT = '904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c'
BOXCARS = 'c70e77df7af81b436cb545d070bb90c82f562d0b'


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one anchor, got {count}')
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# MIMIR_CONTINUE_HERE.md
# ---------------------------------------------------------------------------
continue_text = read('MIMIR_CONTINUE_HERE.md')
continue_text = replace_once(
    continue_text,
    'LAST_PRODUCTION_CODE_SHA:\n  cbb823ce7d3fc871c35a83afc5ee21ae71945821',
    f'LAST_PRODUCTION_CODE_SHA:\n  {PROD_SHA}',
    'continue production sha',
)
continue_text = replace_once(
    continue_text,
    'LAST_PRODUCTION_MILESTONE:\n  R3.18BO — bounded post-BK mixed-continuation following-header production',
    'LAST_PRODUCTION_MILESTONE:\n  R3.18BS — bounded post-BO one-following-payload production',
    'continue production milestone',
)
continue_text = replace_once(
    continue_text,
    'CURRENT_PASS:\n  R3.18BS — bounded post-BO one-following-payload production',
    'CURRENT_PASS:\n  R3.18BT — published-R3.18BS one-following-payload differential',
    'continue current pass',
)
continue_text = replace_once(
    continue_text,
    'CURRENT_PASS_TYPE:\n  bounded production implementation / exact BQ payload rows=2 / Boolean width1 + ActiveActor width33 / BR control consumption forbidden',
    'CURRENT_PASS_TYPE:\n  read-only published-production differential / exact BS payload rows=2 / BQ identity comparison / BR control consumption forbidden',
    'continue current pass type',
)
override_marker = '# CURRENT OVERRIDE — 2026-09-11 — R3.18BS CLOSED / R3.18BT ACTIVE'
if override_marker in continue_text:
    raise SystemExit('continue BS/BT override already exists')
continue_text = continue_text.rstrip() + f'''\n\n\n{override_marker}\n\n- canonical production is R3.18BS `{PROD_SHA}` / tree `{PROD_TREE}` / parent `{PROD_PARENT}`.\n- clean production scope is exactly `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18bs_post_bo_payload.rs`; lib/test blobs `{LIB_BLOB}` / `{TEST_BLOB}`.\n- builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; validation-only PR #218 closed unmerged; exact-head CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS; published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS.\n- exact production lane remains the two BQ payload witnesses only: Boolean `[11238,11239)` width1/value=true and ActiveActor `[3205,3238)` width33/active=true/actor=1; BP false terminator remains excluded.\n- R3.18BS stops exactly at payload end and consumes zero R3.18BR control bits; no next stream/header/payload, second later control or generalized/repeated cursor was admitted.\n- active R3.18BT is read-only: differentially validate published BS against the immutable two-row BQ authority, preserve BP-false exclusion and stop at published payload end. BR control remains evidence-only and closed to BT consumption.\n'''
write('MIMIR_CONTINUE_HERE.md', continue_text)

# ---------------------------------------------------------------------------
# MIMIR_KNOWLEDGE_GRAPH.md
# ---------------------------------------------------------------------------
kg = read('MIMIR_KNOWLEDGE_GRAPH.md')
kg = replace_once(
    kg,
    'R3.18BS bounded post-BO one-following-payload production / ACTIVE\n',
    'R3.18BS bounded post-BO one-following-payload production / PRODUCTION CLOSED\nR3.18BT published-R3.18BS one-following-payload differential / ACTIVE\n',
    'kg chain',
)
kg = replace_once(
    kg,
    '187. `docs/continuity/MIMIR_R3_18BS_EXECUTION_SPEC.md`\n',
    '187. `docs/continuity/MIMIR_R3_18BS_EXECUTION_SPEC.md`\n188. `docs/continuity/MIMIR_R3_18BS_DECISION.md`\n189. `docs/continuity/MIMIR_R3_18BT_EXECUTION_SPEC.md`\n',
    'kg reading order',
)
kg_marker = '### R3.18BS bounded post-BO one-following-payload production: PRODUCTION / CLOSED'
if kg_marker in kg:
    raise SystemExit('kg BS closure already exists')
kg = kg.rstrip() + f'''\n\n\n{kg_marker}\n- production `{PROD_SHA}` / tree `{PROD_TREE}` / parent `{PROD_PARENT}`; exact clean scope lib.rs + `r3_18bs_post_bo_payload.rs`.\n- builder `{BUILDER_RUN}/{BUILDER_JOB}`, exact-head CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` and published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS; validation PR #218 closed unmerged.\n- exact BQ payload lane published 2/2: Boolean width1 `[11238,11239)` / ActiveActor width33 `[3205,3238)`; BP false terminator excluded; following BR control consumption 0.\n- no next stream/header/payload, second later control, generalized/repeated property cursor or semantic/runtime widening admitted.\n\n### R3.18BT published-R3.18BS one-following-payload differential: ACTIVE\n- read-only differential on exactly the two immutable BQ payload rows under published BS.\n- require exact start/end/width/value identity, BP-false exclusion, repeatability and post-stop poison stability.\n- BR control remains evidence-only; BT consumes zero following-control bits and changes no production Rust.\n'''
write('MIMIR_KNOWLEDGE_GRAPH.md', kg)

# ---------------------------------------------------------------------------
# Boundary locks: replace the newest override atomically.
# ---------------------------------------------------------------------------
locks = read('docs/continuity/MIMIR_BOUNDARY_LOCKS.md')
new_lock = f'''# 0. Current override — R3.18BS payload production closed / R3.18BT published differential active\n\nThis current override supersedes older status wording later in this historical lock file.\n\n## PRODUCTION — R3.18BS\n- `{PROD_SHA}` / `{PROD_TREE}` is canonical production.\n- exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload is composed after valid BO/BN authority and production stops at payload end.\n- the BP false terminator remains outside the payload lane; R3.18BR following-control consumption is zero.\n\n## CLOSED READ-ONLY NEXT-CONTROL EVIDENCE — R3.18BR\n- evidence `{BR_HEAD}` / artifact `{BR_ARTIFACT}` / `sha256:{BR_DIGEST}` remains evidence-only.\n- exact=2/2; false=1 true=1; BP-false access=0; adjacent stream/header/payload/second-control=0/0/0/0.\n\n## ACTIVE READ-ONLY PUBLISHED-PAYLOAD DIFFERENTIAL — R3.18BT\n- validate published BS against exactly the two immutable BQ payload witnesses.\n- require exact payload identity/boundaries and BP-false exclusion; stop at published payload end.\n- consume zero BR control bits and mutate no production source.\n\n## CLOSED\n- payload access on the BP false terminator;\n- production consumption of the R3.18BR control bit;\n- next stream/header/payload after published BS/BT;\n- second later control;\n- generalized/repeated cursor and wider semantics/runtime.\n\n# 1. Status vocabulary'''
locks, n = re.subn(
    r'(?s)# 0\. Current override — R3\.18BR next-control evidence closed / R3\.18BS payload production active\n.*?\n# 1\. Status vocabulary',
    new_lock,
    locks,
    count=1,
)
if n != 1:
    raise SystemExit(f'boundary override: expected one replacement, got {n}')
write('docs/continuity/MIMIR_BOUNDARY_LOCKS.md', locks)

# ---------------------------------------------------------------------------
# Small canonical state docs are rewritten in full to avoid stale mixed status.
# ---------------------------------------------------------------------------
current_state = f'''# MIMIR — Current Canonical State\n\n**Continuity date:** {DATE}\n**Repository:** `Naveax/MIMIR`\n**Canonical production SHA:** `{PROD_SHA}`\n**Production tree:** `{PROD_TREE}`\n**Production milestone:** `R3.18BS — bounded post-BO one-following-payload production`\n**Last read-only evidence/audit:** `R3.18BR — Outcome A / exact rows 2/2 / false=1 true=1 / native-oracle mismatch=0 / artifact {BR_ARTIFACT}`\n**Last completed contract:** `R3.18BN — exact_tuple_only / 2 contexts / multiplicity 2 / contract {BN_CONTRACT}`\n**Current exact pass:** `R3.18BT — published-R3.18BS one-following-payload differential`\n\n## Truthful boundary\n\nR3.18BS is canonical production. After valid R3.18BO/R3.18BN authority it composes exactly one payload from the immutable R3.18BQ lane: Boolean `[11238,11239)` width1/value=true or ActiveActor `[3205,3238)` width33/active=true/actor=1. The BP false terminator remains excluded.\n\nThe production stop is exactly payload end. R3.18BR independently observed the next control bit on those two rows, but BS consumes zero such bits. Validation receipts are builder `{BUILDER_RUN}/{BUILDER_JOB}`, validation-only PR #218 exact-head CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}`, and published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}`, all SUCCESS.\n\nR3.18BT is active and read-only. It must differentially validate published BS against exactly the two immutable BQ payload witnesses, preserve BP-false exclusion, and stop at the published payload end without consuming the BR control bit.\n\n## Hard stop\n\nNo production consumption of the BR control bit, no payload access on the BP false terminator, no next stream/header/payload or second later control, no generalized/repeated cursor, and no wider semantic/runtime behavior.\n'''
write('docs/continuity/MIMIR_CURRENT_STATE.md', current_state)

handoff = f'''# MIMIR — Next Chat Handoff\n\nCanonical production is **R3.18BS** at `{PROD_SHA}` / `{PROD_TREE}` with parent `{PROD_PARENT}`.\n\nR3.18BQ remains **Outcome A / CLOSED** at `{BQ_HEAD}`; artifact `{BQ_ARTIFACT}` / `sha256:{BQ_DIGEST}`. Exact payload authority is two rows only: Boolean `[11238,11239)` width1/value=true and ActiveActor `[3205,3238)` width33/active=true/actor=1; the BP false terminator is excluded.\n\nR3.18BR remains **Outcome A / CLOSED READ-ONLY EVIDENCE** at `{BR_HEAD}`; artifact `{BR_ARTIFACT}` / `sha256:{BR_DIGEST}`. Its next-control split is false=1 / true=1 and is not production authority.\n\nR3.18BS is **Outcome A / PUBLISHED**. Builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; validation-only PR #218 closed unmerged with exact-head CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS; published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS. Clean production scope is exactly lib.rs plus `r3_18bs_post_bo_payload.rs`; production stops at payload end and consumes zero BR control bits.\n\nActive pass: **R3.18BT — published-R3.18BS one-following-payload differential**. Validate exactly the two immutable BQ payload rows against published BS, preserve BP-false exclusion and stop at payload end. Production mutation, BR control consumption, next stream/header/payload, second control and generalized cursor remain forbidden.\n'''
write('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md', handoff)

# ---------------------------------------------------------------------------
# Progress ledger append.
# ---------------------------------------------------------------------------
ledger = read('docs/continuity/MIMIR_PROGRESS_LEDGER.md')
ledger_marker = '## 2026-09-11 — R3.18BS — Bounded Post-BO One-Following-Payload Production'
if ledger_marker in ledger:
    raise SystemExit('ledger BS entry already exists')
ledger = ledger.rstrip() + f'''\n\n---\n\n{ledger_marker}\nOutcome: **A — ADMITTED / PRODUCTION**\n\nProduction base SHA: `{PROD_PARENT}`\nProduction commit SHA: `{PROD_SHA}`\nProduction tree: `{PROD_TREE}`\nPass type: bounded production implementation + clean reconstruction + validation-only PR + force-free publication\n\nWhat changed:\n- added one boundary-specific post-BO payload result/value/API using existing admitted Boolean scalar and ActiveActor K2 decoders;\n- recomputes exact BO authority, rejects the BP false terminator and stops exactly at payload end;\n- exact clean production scope is lib.rs plus `r3_18bs_post_bo_payload.rs`;\n- BR following-control consumption remains zero.\n\nValidation:\n- builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; focused BS integration suite 32/32 PASS; cargo check and Clippy `-D warnings` PASS;\n- validation-only PR #218 closed unmerged; exact-head CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS;\n- force=false publication and exact SHA/tree readback PASS; published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS.\n\nAuthority and exact lane:\n- BN contract `sha256:{BN_CONTRACT}` / exact two contexts / multiplicity 2;\n- BQ `{BQ_HEAD}` / artifact `{BQ_ARTIFACT}` / `sha256:{BQ_DIGEST}`;\n- Boolean `[11238,11239)` width1/value=true; ActiveActor `[3205,3238)` width33/active=true/actor=1; BP false terminator excluded;\n- post-stop poison including the BR control bit leaves BS result unchanged; following-control consumption 0.\n\nBoundaries opened:\n- R3.18BT may read-only differentially validate published BS on exactly the immutable two-row BQ lane.\n\nBoundaries still closed:\n- BR control production; next stream/header/payload; second later control; generalized/repeated property cursor; next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.\n\nNext exact pass:\n- `R3.18BT — published-R3.18BS one-following-payload differential`.\n'''
write('docs/continuity/MIMIR_PROGRESS_LEDGER.md', ledger)

# ---------------------------------------------------------------------------
# Decision + next execution spec.
# ---------------------------------------------------------------------------
decision = f'''# MIMIR R3.18BS — Bounded Post-BO One-Following-Payload Production Decision\n\n**Date:** {DATE}\n**Outcome:** **A — ADMITTED / PUBLISHED**\n**Canonical production:** `{PROD_SHA}` / `{PROD_TREE}`\n**Parent:** `{PROD_PARENT}` / `{PARENT_TREE}`\n**Header contract:** R3.18BN `sha256:{BN_CONTRACT}`\n**Payload evidence authority:** R3.18BQ `{BQ_HEAD}` / artifact `{BQ_ARTIFACT}` / `sha256:{BQ_DIGEST}`\n\n## Decision\n\nR3.18BS publishes exactly one boundary-specific payload after a valid R3.18BO true following-header composition. The admitted lane is exactly the two immutable R3.18BQ payload witnesses: Boolean `[11238,11239)` width1/value=true and ActiveActor `[3205,3238)` width33/active=true/actor=1. The R3.18BP false terminator remains outside the payload lane.\n\nThe implementation recomputes published BO authority, requires the validated payload-start boundary, uses the already-admitted Boolean scalar or ActiveActor K2 primitive, returns exact payload boundary/value information and stops exactly at payload end. The R3.18BR-observed next control bit is not consumed.\n\n## Exact authority and receipts\n\n```text\nproduction SHA/tree                  {PROD_SHA} / {PROD_TREE}\nparent SHA/tree                      {PROD_PARENT} / {PARENT_TREE}\nlib/test blobs                       {LIB_BLOB} / {TEST_BLOB}\nBS execution spec blob               {BS_SPEC_BLOB}\nproduction builder head              {BUILDER_HEAD}\nproduction builder run/job           {BUILDER_RUN}/{BUILDER_JOB} SUCCESS\nvalidation-only PR                   #218 CLOSED UNMERGED\nexact-head candidate CI              {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS\npublished-main CI                    {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS\nBN contract                          sha256:{BN_CONTRACT}\nBQ evidence head/artifact            {BQ_HEAD} / {BQ_ARTIFACT}\nBQ artifact digest                   sha256:{BQ_DIGEST}\nBR evidence head/artifact            {BR_HEAD} / {BR_ARTIFACT}\nBR artifact digest                   sha256:{BR_DIGEST}\npinned Boxcars                       {BOXCARS}\n```\n\n## Admitted production behavior\n\n```text\nBQ payload rows                      2/2\nBP false terminator                  excluded before payload decode\nBoolean                              [11238,11239) / width 1 / value true\nActiveActor                          [3205,3238) / width 33 / active true / actor 1\nproperty ordinal                     7 on 2/2\nfinal stop                           exact payload_end_bit\nfollowing BR control consumed        0\nnext stream/header/payload           0/0/0\nsecond later control                 0\ngeneralized/repeated cursor          0\n```\n\nThe clean production commit contains only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18bs_post_bo_payload.rs`. No temporary workflow/helper, Cargo/dependency, fixture/corpus, continuity, raw-state/event/skill/runtime/export or unrelated mutation entered production.\n\n## Validation\n\nThe final builder passed formatting, the focused BS integration suite 32/32, `cargo check -p mimir-replay --all-targets --all-features`, Clippy with warnings denied, exact two-file scope and clean reconstruction. Validation-only PR #218 supplied natural exact-head repository CI and was closed unmerged. Fresh-main ancestry was rechecked before publication; `main` was advanced with `force=false`; exact SHA/tree readback matched; published-main CI passed on the exact production SHA.\n\n## Hard stop\n\nNo R3.18BR control-bit production, no payload access on the BP false terminator, no next stream/header/payload, no second later control, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.\n\n## Next gate\n\nR3.18BT is a separate read-only published-production differential. It must validate published R3.18BS against exactly the immutable two-row BQ payload authority, preserve BP-false exclusion, require exact payload identity/boundaries and consume zero BR control bits.\n'''
write('docs/continuity/MIMIR_R3_18BS_DECISION.md', decision)

bt = f'''# MIMIR R3.18BT — Published R3.18BS One-Following-Payload Differential\n\n**Status:** ACTIVE\n**Pass type:** read-only published-production differential\n**Production authority:** R3.18BS `{PROD_SHA}` / `{PROD_TREE}`\n**Payload evidence authority:** R3.18BQ `{BQ_HEAD}` / artifact `{BQ_ARTIFACT}` / `sha256:{BQ_DIGEST}`\n**Header contract:** R3.18BN `sha256:{BN_CONTRACT}`\n**Later-control evidence:** R3.18BR false=1 / true=1; evidence only, consumption forbidden\n**Production mutation:** forbidden\n\n## 1. Goal\n\nDifferentially validate published R3.18BS against exactly the immutable two-row R3.18BQ payload authority. Reconstruct each exact valid prerequisite through R3.18BO, invoke published BS exactly once, require exact payload start/end/width/value identity, and stop at the published payload end.\n\nThe R3.18BP false terminator must remain excluded before payload decoding. R3.18BT must not consume the R3.18BR control bit or any next stream/header/payload/second-control data.\n\n## 2. Frozen authority\n\n```text\nproduction SHA/tree                  {PROD_SHA} / {PROD_TREE}\nproduction parent                    {PROD_PARENT}\nlib/test blobs                       {LIB_BLOB} / {TEST_BLOB}\nBS builder                           {BUILDER_RUN}/{BUILDER_JOB} SUCCESS\nBS exact-head CI                     {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS\nBS published-main CI                 {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS\nBN contract                          sha256:{BN_CONTRACT} / 2 contexts / multiplicity 2\nBQ authority                         {BQ_HEAD} / artifact {BQ_ARTIFACT}\nBQ payload rows                      2\nBoolean witness                      [11238,11239) / width1 / true\nActiveActor witness                  [3205,3238) / width33 / active=true actor=1\nBP false terminator                  1 / excluded\nBR next-control split                false=1 / true=1 / evidence only\n```\n\n## 3. Exact differential lane\n\nFor each immutable BQ payload witness:\n1. reconstruct the exact valid published prerequisites through R3.18BO;\n2. invoke published `decode_replay_network_post_bo_following_payload_v1` once;\n3. require exact retained BO header composition;\n4. require exact payload tag/start/end/width/value equality with the frozen BQ witness;\n5. require returned `stop_bit == payload_end_bit`;\n6. repeat and require bit-exact identical result;\n7. poison bits beginning at returned stop, including the BR control bit, and require BS output unchanged;\n8. stop without control/stream/header/payload access beyond BS.\n\nSeparately reconstruct the BP/BO false terminator and require BS rejection before payload decoding.\n\nExpected totals:\n\n```text\ntrue payload rows                    2/2\nBoolean                              1\nActiveActor                          1\nBP false terminator excluded         1/1\nBQ identity exact                    2/2\nmismatch                             0\nwitness reselection                  0\nfollowing BR control consumed        0\nnext stream/header/payload           0/0/0\nsecond later control                 0\n```\n\n## 4. Required negative controls\n\nAt minimum: BP false-terminator exclusion; corrupt BO prerequisite; wrong actor; unresolved lookup; wrong exact version/context; wrong/fabricated resolved tag; payload truncation; payload-start/header-stop mismatch; fabricated Cartesian BN context; historical BD/AT/AJ/Z/P-only context; repeatability; post-payload-end poison including the BR control bit; source-scope guard proving no generic/repeated cursor or later-control read.\n\n## 5. Validation\n\nRequire exact production SHA/tree/blobs, exact BQ authority identity, two successful published payload rows, one false terminator excluded, mismatch/reselection 0/0, all negative controls PASS, following-control consumption 0, production/Cargo/fixture/corpus/support mutation 0/0/0/0/0, focused BS regression, full repository verification and same-head natural CI. Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.\n\n## 6. Hard stop\n\nNo R3.18BR control production, no next stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.\n\n## 7. Outcome gate\n\n### Outcome A\nPublished R3.18BS matches both immutable BQ payload witnesses exactly, the BP false terminator remains excluded, mismatch/reselection are zero, all negative/full validations pass and following-control consumption is zero. Only then may a separate later pass consider whether the already-observed R3.18BR control bit should receive its own production gate.\n\n### Outcome B\nA bounded mismatch or narrower safe subset is isolated. Record only the exact supported subset and keep control-bit production closed.\n\n### Outcome C\nAuthority drift, payload identity mismatch, false-terminator payload access, BR control consumption, generic chaining, mutation leakage or validation contradiction. Stop without widening.\n'''
write('docs/continuity/MIMIR_R3_18BT_EXECUTION_SPEC.md', bt)

# ---------------------------------------------------------------------------
# Structured continuity state.
# ---------------------------------------------------------------------------
state_path = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(state_path.read_text(encoding='utf-8'))
state['updated_date'] = DATE
state['last_production_code_sha'] = PROD_SHA
state['last_production_milestone'] = 'R3.18BS'
state['last_production_milestone_name'] = 'bounded post-BO one-following-payload production'
state['last_completed_read_only_audit'] = 'R3.18BR'
state['current_pass'] = 'R3.18BT'
state['current_pass_kind'] = 'read-only published-R3.18BS one-following-payload differential on the two immutable R3.18BQ payload rows'
state['current_pass_goal'] = 'Validate published R3.18BS exactly against both BQ payload witnesses, preserve BP-false exclusion and stop at payload end without consuming the R3.18BR control bit.'
state['current_pass_stop_boundary'] = 'Stop exactly at published BS payload_end_bit. Do not consume the R3.18BR following control bit or any later stream/header/payload/control.'
# Repair an older continuity-only inconsistency: the master handbook already named BR as
# the latest evidence pass while this structured field still lagged at BM.
state['last_completed_evidence_pass'] = 'R3.18BR'
state['last_completed_evidence_outcome'] = 'A — exact two next-control observations after BQ payload end; false=1 true=1; mismatch/reselection 0/0; adjacent reads 0/0/0/0; artifact 10267123608.'
for item in [
    'docs/continuity/MIMIR_R3_18BS_DECISION.md',
    'docs/continuity/MIMIR_R3_18BT_EXECUTION_SPEC.md',
]:
    if item not in state['next_files_to_read']:
        state['next_files_to_read'].append(item)
for item in [
    'payload access on the R3.18BP false terminator after published R3.18BS',
    'production consumption of the R3.18BR-observed following control bit during R3.18BT',
    'next stream/header/payload after published R3.18BS payload_end_bit',
    'second later property-control bit after published R3.18BS',
    'generalized/repeated property loop or generic cursor after published R3.18BS',
]:
    if item not in state['closed_now']:
        state['closed_now'].append(item)
state['r3_18bs'] = {
    'status': 'published_outcome_a',
    'sha': PROD_SHA,
    'tree': PROD_TREE,
    'parent': PROD_PARENT,
    'lib_blob': LIB_BLOB,
    'test_blob': TEST_BLOB,
    'builder_head': BUILDER_HEAD,
    'builder_run': BUILDER_RUN,
    'builder_job': BUILDER_JOB,
    'validation_pr': 218,
    'validation_pr_merged': False,
    'candidate_ci_run': CANDIDATE_CI_RUN,
    'candidate_ci_job': CANDIDATE_CI_JOB,
    'published_ci_run': PUBLISHED_CI_RUN,
    'published_ci_job': PUBLISHED_CI_JOB,
    'target_rows': 2,
    'false_terminators_excluded': 1,
    'boolean_rows': 1,
    'boolean_width': 1,
    'active_actor_rows': 1,
    'active_actor_width': 33,
    'following_control_consumed': 0,
    'generalized_cursor': 0,
}
state['r3_18bt'] = {
    'status': 'active_read_only_published_payload_differential',
    'production_sha': PROD_SHA,
    'payload_authority_head': BQ_HEAD,
    'payload_authority_artifact': BQ_ARTIFACT,
    'target_rows': 2,
    'bp_false_terminators_excluded': 1,
    'following_control_consumption_allowed': False,
    'production_mutation_allowed': False,
}
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

print('R3.18BS continuity sync staged: 7 updated docs + BS decision + BT execution spec')
