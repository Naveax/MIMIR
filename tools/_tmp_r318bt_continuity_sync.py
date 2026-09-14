from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path('.')
DATE = '2026-09-14'
MAIN_BASE = 'b0e306cb79fa2bd2fb0a2d5e961f5f0adf00f2d0'
PROD_SHA = '5ab14575d0a698d752db35db76f3dbb300cdec8d'
PROD_TREE = '1c0b4c0a50385a34ba730a52a98a89423ff56869'
PROD_PARENT = '2f4f536d52a10a28a66bcc7b9b9dc84f7e29b2a6'
LIB_BLOB = '3428608283d6d0022d466671f90afc9304726dd0'
BS_TEST_BLOB = '706bbdee62a09f04af7bcf70e22567793084d0d6'
BN_CONTRACT = '904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c'
BQ_HEAD = '16c43f38e740c57ae9cb90c92084002ec83815e7'
BQ_RUN = 34457725716
BQ_JOB = 102807933610
BQ_ARTIFACT = 10144392560
BQ_DIGEST = '52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c'
BR_HEAD = 'ff1daab35e2e75bf7446a98a07a1db67e5196dbd'
BR_ARTIFACT = 10267123608
BR_DIGEST = 'bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1'
BT_HEAD = 'b687f700a7bf00f28671ca3adbb6613b582e7848'
BT_TREE = 'f573860e733689fa03767702f6f1750e222664c3'
BT_RUN = 34816904695
BT_JOB = 103889382147
BT_CI_RUN = 34816904663
BT_CI_JOB = 103889381782
BT_ARTIFACT = 10336951993
BT_ARTIFACT_SIZE = 5213
BT_DIGEST = 'fef0df77821475ac3ee5acb417b500aa40708a573d286d30c5c42bcf23ef473d'
BT_WORKFLOW_BLOB = '69ecc8d1bbf3096be459582203350f541e558561'


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


# MIMIR_CONTINUE_HERE.md
p = read('MIMIR_CONTINUE_HERE.md')
p = replace_once(p,
    'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18BR — next property-control bit Outcome A / exact=2/2 / false=1 true=1 / mismatch 0 / artifact 10267123608',
    f'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18BT — published-R3.18BS one-following-payload differential Outcome A / exact=2/2 / BQ identity=2/2 / mismatch 0 / BR control consumed 0 / artifact {BT_ARTIFACT}',
    'continue audit')
p = replace_once(p,
    'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18BR — exact two next-control observations / Boolean-row=false / ActiveActor-row=true / mismatch=0 / adjacent reads=0 / artifact 10267123608',
    f'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18BT — exact published-BS differential / two payload rows / false terminator excluded / repeatability 2/2 / post-stop poison 2/2 / artifact {BT_ARTIFACT}',
    'continue evidence')
p = replace_once(p,
    'CURRENT_PASS:\n  R3.18BT — published-R3.18BS one-following-payload differential',
    'CURRENT_PASS:\n  R3.18BU — bounded post-BS next property-control production',
    'continue current pass')
p = replace_once(p,
    'CURRENT_PASS_TYPE:\n  read-only published-production differential / exact BS payload rows=2 / BQ identity comparison / BR control consumption forbidden',
    'CURRENT_PASS_TYPE:\n  bounded production implementation / exact BT-admitted rows=2 / consume exactly one BR-observed control bit / stop immediately after that bit',
    'continue current pass type')
marker = '# CURRENT OVERRIDE — 2026-09-14 — R3.18BT CLOSED / R3.18BU ACTIVE'
if marker in p:
    raise SystemExit('continue BT/BU override already exists')
p = p.rstrip() + f'''\n\n\n{marker}\n\n- canonical production remains R3.18BS `{PROD_SHA}` / tree `{PROD_TREE}`; R3.18BT was read-only and changed no production Rust.\n- R3.18BT exact evidence head `{BT_HEAD}` / tree `{BT_TREE}`; runner `{BT_RUN}/{BT_JOB}` SUCCESS; same-head natural CI `{BT_CI_RUN}/{BT_CI_JOB}` SUCCESS.\n- immutable R3.18BT artifact `{BT_ARTIFACT}` / size `{BT_ARTIFACT_SIZE}` / `sha256:{BT_DIGEST}`; workflow blob `{BT_WORKFLOW_BLOB}`.\n- Outcome A: published BS matches immutable BQ authority exactly 2/2; Boolean `[11238,11239)` value=true and ActiveActor `[3205,3238)` active=true/actor=1; BP false terminator excluded 1/1; mismatch=0; witness reselection=0; repeatability=2/2; post-payload poison=2/2; following BR control consumed=0.\n- active R3.18BU may compose exactly one R3.18BR-observed property-control bit after a valid exact R3.18BS result on only those two admitted rows: Boolean row=false, ActiveActor row=true.\n- R3.18BU must recompute BS, require exact supplied equality, require `control_start_bit == bs.stop_bit`, read exactly one checked LSB-first bit, return `stop_bit = control_start_bit + 1`, and read nothing after it.\n- BP false terminator, next stream/header/payload, second later control, generic/repeated cursor and all wider semantics remain closed.\n'''
write('MIMIR_CONTINUE_HERE.md', p)

# MIMIR_KNOWLEDGE_GRAPH.md
kg = read('MIMIR_KNOWLEDGE_GRAPH.md')
kg = replace_once(kg,
    'R3.18BT published-R3.18BS one-following-payload differential / ACTIVE\n',
    'R3.18BT published-R3.18BS one-following-payload differential / Outcome A CLOSED\nR3.18BU bounded post-BS next property-control production / ACTIVE\n',
    'kg chain')
kg = replace_once(kg,
    '189. `docs/continuity/MIMIR_R3_18BT_EXECUTION_SPEC.md`\n',
    '189. `docs/continuity/MIMIR_R3_18BT_EXECUTION_SPEC.md`\n190. `docs/continuity/MIMIR_R3_18BT_DECISION.md`\n191. `docs/continuity/MIMIR_R3_18BU_EXECUTION_SPEC.md`\n',
    'kg reading order')
kg_marker = '### R3.18BT published-R3.18BS one-following-payload differential: OUTCOME A / CLOSED'
if kg_marker in kg:
    raise SystemExit('kg BT closure already exists')
kg = kg.rstrip() + f'''\n\n\n{kg_marker}\n- evidence `{BT_HEAD}` / `{BT_TREE}`, runner `{BT_RUN}/{BT_JOB}` SUCCESS, same-head CI `{BT_CI_RUN}/{BT_CI_JOB}` SUCCESS.\n- immutable artifact `{BT_ARTIFACT}` / `sha256:{BT_DIGEST}`; BQ payload identity 2/2, mismatch 0, reselection 0, false terminator excluded 1/1.\n- repeatability 2/2 and post-payload poison 2/2; following BR control consumed 0; production mutation 0.\n\n### R3.18BU bounded post-BS next property-control production: ACTIVE\n- exact two-row lane only, gated by BT Outcome A and immutable BR control authority.\n- Boolean row consumes exactly one false control bit; ActiveActor row consumes exactly one true control bit.\n- recompute and exactly match BS, read one checked LSB-first bit at `bs.stop_bit`, stop at +1, and read nothing later.\n- BP false terminator, next stream/header/payload, second later control and generic/repeated cursor remain closed.\n'''
write('MIMIR_KNOWLEDGE_GRAPH.md', kg)

# Boundary locks current override.
locks = read('docs/continuity/MIMIR_BOUNDARY_LOCKS.md')
new_lock = f'''# 0. Current override — R3.18BT published differential closed / R3.18BU one-control production active\n\nThis current override supersedes older status wording later in this historical lock file.\n\n## PRODUCTION — R3.18BS\n- `{PROD_SHA}` / `{PROD_TREE}` remains canonical production while BU is active.\n- BS composes exactly one BQ-admitted payload and stops at payload end.\n\n## CLOSED READ-ONLY DIFFERENTIAL — R3.18BT\n- `{BT_HEAD}` / runner `{BT_RUN}/{BT_JOB}` / same-head CI `{BT_CI_RUN}/{BT_CI_JOB}` all SUCCESS.\n- artifact `{BT_ARTIFACT}` / `sha256:{BT_DIGEST}`.\n- exact 2/2 BQ identity; false terminator excluded; mismatch/reselection 0; BR control consumed 0; production mutation 0.\n\n## ACTIVE BOUNDED PRODUCTION — R3.18BU\n- only the exact two BT-admitted payload rows may continue.\n- use immutable BR authority: Boolean row=false, ActiveActor row=true.\n- recompute BS and require exact supplied equality; consume exactly one checked LSB-first control bit at BS stop; stop immediately after that bit.\n\n## CLOSED\n- control access on the BP false terminator;\n- success outside the two exact BT/BQ/BR rows;\n- next stream/header/payload after the one BU control bit;\n- second later property-control bit;\n- generalized/repeated cursor and wider semantics/runtime.\n\n# 1. Status vocabulary'''
locks, n = re.subn(r'(?s)# 0\. Current override — .*?\n# 1\. Status vocabulary', new_lock, locks, count=1)
if n != 1:
    raise SystemExit(f'boundary override replacement count={n}')
write('docs/continuity/MIMIR_BOUNDARY_LOCKS.md', locks)

# Current state concise canonical truth.
write('docs/continuity/MIMIR_CURRENT_STATE.md', f'''# MIMIR — Current Canonical State\n\n**Continuity date:** {DATE}\n**Repository:** `Naveax/MIMIR`\n**Canonical production SHA:** `{PROD_SHA}`\n**Production tree:** `{PROD_TREE}`\n**Production milestone:** `R3.18BS — bounded post-BO one-following-payload production`\n**Last read-only evidence/audit:** `R3.18BT — Outcome A / exact BQ identity 2/2 / mismatch 0 / BR control consumed 0 / artifact {BT_ARTIFACT}`\n**Last completed contract:** `R3.18BN — exact_tuple_only / 2 contexts / multiplicity 2 / contract {BN_CONTRACT}`\n**Current exact pass:** `R3.18BU — bounded post-BS next property-control production`\n\n## Truthful boundary\n\nR3.18BS remains canonical production. R3.18BT closed read-only with exact published-BS/BQ identity on both payload rows, BP-false exclusion, repeatability and post-stop poison stability. Runner `{BT_RUN}/{BT_JOB}` and same-head CI `{BT_CI_RUN}/{BT_CI_JOB}` are SUCCESS; immutable artifact `{BT_ARTIFACT}` / `sha256:{BT_DIGEST}`.\n\nR3.18BU may now consume exactly one R3.18BR-observed control bit after valid exact BS on only the two admitted rows: Boolean=false and ActiveActor=true. It must recompute BS, require exact supplied equality and exact boundary equality, consume one checked LSB-first bit, then stop immediately.\n\n## Hard stop\n\nNo BP-false access, no success outside the exact two rows, no next stream/header/payload, no second later control, no generalized/repeated cursor and no wider semantic/runtime behavior.\n''')

write('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md', f'''# MIMIR — Next Chat Handoff\n\nCanonical production remains **R3.18BS** at `{PROD_SHA}` / `{PROD_TREE}`.\n\nR3.18BT is **Outcome A / CLOSED READ-ONLY** at `{BT_HEAD}` / `{BT_TREE}`. Runner `{BT_RUN}/{BT_JOB}` SUCCESS and same-head CI `{BT_CI_RUN}/{BT_CI_JOB}` SUCCESS. Immutable artifact `{BT_ARTIFACT}` / size `{BT_ARTIFACT_SIZE}` / `sha256:{BT_DIGEST}`. Published BS matches frozen BQ authority 2/2; false terminator excluded 1/1; mismatch/reselection 0; repeatability 2/2; post-stop poison 2/2; BR control consumed 0; production mutation 0.\n\nActive pass: **R3.18BU — bounded post-BS next property-control production**. Use exactly the two admitted rows and immutable BR values: Boolean=false, ActiveActor=true. Recompute exact BS, require supplied equality and `control_start_bit == bs.stop_bit`, read exactly one checked LSB-first bit, stop at +1. Nothing after that bit is in scope.\n''')

# Progress ledger append.
ledger = read('docs/continuity/MIMIR_PROGRESS_LEDGER.md')
ledger_marker = '## 2026-09-14 — R3.18BT — Published R3.18BS One-Following-Payload Differential'
if ledger_marker in ledger:
    raise SystemExit('ledger BT entry already exists')
ledger = ledger.rstrip() + f'''\n\n---\n\n{ledger_marker}\nOutcome: **A — ADMITTED / READ-ONLY EVIDENCE**\n\nEvidence head/tree: `{BT_HEAD}` / `{BT_TREE}`\nRunner: `{BT_RUN}/{BT_JOB}` SUCCESS\nSame-head natural CI: `{BT_CI_RUN}/{BT_CI_JOB}` SUCCESS\nArtifact: `{BT_ARTIFACT}` / `{BT_ARTIFACT_SIZE}` bytes / `sha256:{BT_DIGEST}`\nProduction authority: unchanged R3.18BS `{PROD_SHA}` / `{PROD_TREE}`\n\nResults:\n- exact immutable BQ payload identity: 2/2; Boolean `[11238,11239)` true and ActiveActor `[3205,3238)` active=true actor=1;\n- BP false terminator excluded 1/1; mismatch=0; witness reselection=0;\n- repeatability=2/2; post-payload poison including BR control=2/2; following BR control consumed=0;\n- next stream/header/payload=0/0/0; second later control=0;\n- production/Cargo/fixture/corpus/support mutation=0/0/0/0/0; full validation PASS.\n\nAdmission consequence:\n- R3.18BT closes Outcome A without changing production;\n- R3.18BU may consume exactly one immutable BR-observed control bit on only the two admitted rows.\n'''
write('docs/continuity/MIMIR_PROGRESS_LEDGER.md', ledger)

# Continuity JSON: preserve history, update only canonical moving frontier + explicit BT/BU receipts.
state_path = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(state_path.read_text(encoding='utf-8'))
state['updated_date'] = DATE
state['last_completed_read_only_audit'] = 'R3.18BT'
state['current_pass'] = 'R3.18BU'
state['current_pass_kind'] = 'bounded post-BS next property-control production on exactly the two BT-admitted payload rows'
state['current_pass_goal'] = 'Recompute exact R3.18BS, consume exactly one immutable R3.18BR-observed control bit (Boolean=false, ActiveActor=true), and stop immediately after it.'
state['current_pass_stop_boundary'] = 'Stop exactly one bit after published BS payload_end_bit. Do not consume any next stream/header/payload or second later control.'
state['r3_18bt_admission'] = {
    'outcome': 'A', 'head_sha': BT_HEAD, 'tree_sha': BT_TREE,
    'run_id': BT_RUN, 'job_id': BT_JOB, 'same_head_ci_run_id': BT_CI_RUN,
    'same_head_ci_job_id': BT_CI_JOB, 'artifact_id': BT_ARTIFACT,
    'artifact_size': BT_ARTIFACT_SIZE, 'artifact_sha256': BT_DIGEST,
    'bq_identity_exact': '2/2', 'false_terminator_excluded': '1/1',
    'mismatch': 0, 'witness_reselection': 0, 'repeatability': '2/2',
    'post_payload_poison': '2/2', 'following_br_control_consumed': 0,
    'production_mutation': 0,
}
state['current_pass_contract'] = {
    'pass': 'R3.18BU', 'authority_rows': 2,
    'boolean_row_control': False, 'active_actor_row_control': True,
    'must_recompute_bs': True, 'supplied_bs_must_match_exactly': True,
    'control_start_equals_bs_stop': True, 'bits_consumed': 1,
    'false_terminator_allowed': False, 'next_stream_header_payload_allowed': False,
    'second_later_control_allowed': False, 'generic_repeated_cursor_allowed': False,
}
for f in ['docs/continuity/MIMIR_R3_18BT_DECISION.md', 'docs/continuity/MIMIR_R3_18BU_EXECUTION_SPEC.md']:
    if f not in state.get('next_files_to_read', []):
        state.setdefault('next_files_to_read', []).append(f)
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# Decision and next execution spec.
write('docs/continuity/MIMIR_R3_18BT_DECISION.md', f'''# MIMIR R3.18BT Decision — Published R3.18BS One-Following-Payload Differential\n\n**Date:** {DATE}\n**Status:** Outcome A — CLOSED / ADMITTED READ-ONLY EVIDENCE\n**Production authority after decision:** unchanged R3.18BS `{PROD_SHA}` / `{PROD_TREE}`\n\n## Immutable receipts\n\n- Evidence head/tree: `{BT_HEAD}` / `{BT_TREE}`\n- Workflow blob: `{BT_WORKFLOW_BLOB}`\n- Runner: `{BT_RUN}/{BT_JOB}` — SUCCESS\n- Same-head natural CI: `{BT_CI_RUN}/{BT_CI_JOB}` — SUCCESS\n- Artifact: `{BT_ARTIFACT}` / `{BT_ARTIFACT_SIZE}` bytes / `sha256:{BT_DIGEST}`\n- R3.18BQ: `{BQ_HEAD}` / `{BQ_RUN}/{BQ_JOB}` / artifact `{BQ_ARTIFACT}` / `sha256:{BQ_DIGEST}`\n- R3.18BR: `{BR_HEAD}` / artifact `{BR_ARTIFACT}` / `sha256:{BR_DIGEST}`\n- R3.18BN contract: `sha256:{BN_CONTRACT}`\n\n## Admitted result\n\nPublished R3.18BS exactly reproduces both immutable BQ payload witnesses: Boolean `[11238,11239)` value=true and ActiveActor `[3205,3238)` active=true actor=1. Exact identity is 2/2; BP false terminator exclusion is 1/1; mismatch=0; witness reselection=0. Repeatability and post-payload poison checks are 2/2. The following R3.18BR control bit is consumed zero times. No next stream/header/payload or second later control is read. Production/Cargo/fixture/corpus/support mutation is zero.\n\n## Decision\n\nOutcome A is admitted. R3.18BT is closed read-only. Production remains R3.18BS. The next pass may open exactly one R3.18BR-observed control bit after a valid exact BS result on the two admitted rows and nothing beyond that one bit.\n''')

write('docs/continuity/MIMIR_R3_18BU_EXECUTION_SPEC.md', f'''# MIMIR R3.18BU Execution Spec — Bounded Post-BS Next Property-Control Production\n\n**Date:** {DATE}\n**Status:** ACTIVE\n**Pass type:** bounded production composition\n**Production base:** R3.18BS `{PROD_SHA}` / `{PROD_TREE}`\n**Gate:** R3.18BT Outcome A\n\n## Exact authority\n\nR3.18BU is restricted to the two exact BT/BQ/BR rows:\n\n1. `external_fixtures/sample_002.replay` — BS Boolean payload `[11238,11239)` value=true; one following control bit is **false**.\n2. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay` — BS ActiveActor payload `[3205,3238)` active=true actor=1; one following control bit is **true**.\n\nThe R3.18BP false terminator remains outside membership. No witness reselection is allowed.\n\n## Required production behavior\n\n- Recompute R3.18BS exactly once and require exact equality with the supplied BS result.\n- Require the admitted row/context/tag and exact payload boundary/value identity.\n- Require `control_start_bit == bs.stop_bit == payload_end_bit`.\n- Read exactly one checked LSB-first property-control bit.\n- Require the read bit to equal immutable R3.18BR authority for that row.\n- Return `control_end_bit = control_start_bit + 1` and `stop_bit = control_end_bit`.\n- Read nothing after that bit.\n\n## Exact clean source scope\n\nOnly these production-candidate files may change:\n\n- `crates/mimir-replay/src/lib.rs`\n- `crates/mimir-replay/tests/r3_18bu_post_bs_following_control.rs`\n\nTemporary builder/evidence files must not enter the clean production commit.\n\n## Required negatives\n\nReject or remain invariant under: corrupt/mismatched BS prerequisite, wrong actor/context/tag, fabricated authority row, BP false terminator, truncation at control start, altered payload bounds/semantic/stop, wrong expected control value, and poison after returned stop. The two valid rows must be repeatable.\n\n## Validation gate\n\nRun focused BU tests, `cargo fmt --all -- --check`, workspace check, workspace Clippy with `-D warnings`, full workspace tests, repository verification and `git diff --check`. Reconstruct a clean two-file candidate on fresh main, require exact-head natural CI SUCCESS, publish by non-force fast-forward only, then require published-main exact-SHA CI SUCCESS before continuity admission.\n\n## Hard stop\n\nNo BP-false control access, no success outside exact two-row authority, no next stream/header/payload, no second later control, no generic/repeated cursor, no actor-state/runtime widening.\n''')

print('R3_18BT_CONTINUITY_SYNC=PASS')
