from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path('.')
DATE = '2026-09-14'
MAIN_BASE = '58d7e0ac79e4e098215c06e0bc1d365cd5720d61'
MAIN_TREE = '2c7768c9dcac5d96781e8c6d583d75b66bda66b1'
PROD_SHA = '43c5d6248e2ea606b2eb0fd95f5c50758c372356'
PROD_TREE = 'd1b7b40ed4e361d9c047e0494fb821688ef7d7b4'
PROD_PARENT = '9a86252e02d383ebc2ff9665e678f4c2319f47d9'
LIB_BLOB = '1c4db09cff43e0ab56f5efb5e8078da3a1189937'
BU_TEST_BLOB = 'e6170f90b47e3f04bd798edbc61f2fa59e5213dd'
BU_SPEC_BLOB = 'ac1ce2120320bd552e5be24e2309fea23d5a2a50'
BV_SPEC_BLOB = 'f6d37f928e7171ac1d100447d1f4775b948abb2a'
BV_HEAD = '45c6a5b57ee96c8e4b8b472e548c6b1f2d4c426c'
BV_TREE = '68da2ace745390781ea7e5ade25aaf2c051098d3'
BV_WORKFLOW_BLOB = '30d772fc07c7c290418cee5a0dc8160e2cf6b00f'
BV_RUN = 34830085977
BV_JOB = 103932439559
BV_CI_RUN = 34830086065
BV_CI_JOB = 103932439965
BV_ARTIFACT = 10340803017
BV_ARTIFACT_SIZE = 5957
BV_DIGEST = '5dee811012dda32203126105d6edc17a5067a0c9ec6299af32e12642515015f0'
BR_HEAD = 'ff1daab35e2e75bf7446a98a07a1db67e5196dbd'
BR_ARTIFACT = 10267123608
BR_DIGEST = 'bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1'
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


# Master continuity frontier.
p = read('MIMIR_CONTINUE_HERE.md')
p = replace_once(
    p,
    'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18BT — published-R3.18BS one-following-payload differential Outcome A / exact=2/2 / BQ identity=2/2 / mismatch 0 / BR control consumed 0 / artifact 10336951993',
    f'LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18BV — published-R3.18BU one-control differential Outcome A / exact=2/2 / BS prerequisite=2/2 / false=1 true=1 / mismatch 0 / adjacent consumption 0/0/0/0 / artifact {BV_ARTIFACT}',
    'continue audit',
)
p = replace_once(
    p,
    'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18BT — exact published-BS differential / two payload rows / false terminator excluded / repeatability 2/2 / post-stop poison 2/2 / artifact 10336951993',
    f'LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18BV — exact published-BU differential / two control rows / false terminator 1 / true continuation 1 / repeatability 2/2 / post-stop poison 2/2 / artifact {BV_ARTIFACT}',
    'continue evidence',
)
p = replace_once(
    p,
    'CURRENT_PASS:\n  R3.18BV — published-R3.18BU one-control differential',
    'CURRENT_PASS:\n  R3.18BW — one following-property-header evidence after published R3.18BU mixed control',
    'continue current',
)
p = replace_once(
    p,
    'CURRENT_PASS_TYPE:\n  read-only published-production differential / exact BU control rows=2 / BR identity comparison / adjacent consumption forbidden',
    'CURRENT_PASS_TYPE:\n  read-only boundary evidence / exact BV rows=2 / false terminator=1 / true continuation=1 / observe one following header through payload_start only',
    'continue current type',
)
marker = '# CURRENT OVERRIDE — 2026-09-14 — R3.18BV CLOSED / R3.18BW ACTIVE'
if marker in p:
    raise SystemExit('continue BV/BW override duplicate')
p = p.rstrip() + f'''\n\n\n{marker}\n\n- canonical production remains R3.18BU `{PROD_SHA}` / `{PROD_TREE}` / parent `{PROD_PARENT}`; BV was read-only and changed no production Rust.\n- R3.18BV evidence `{BV_HEAD}` / `{BV_TREE}`; runner `{BV_RUN}/{BV_JOB}` SUCCESS; same-head natural CI `{BV_CI_RUN}/{BV_CI_JOB}` SUCCESS.\n- immutable artifact `{BV_ARTIFACT}` / {BV_ARTIFACT_SIZE} bytes / `sha256:{BV_DIGEST}`; workflow blob `{BV_WORKFLOW_BLOB}`.\n- Outcome A: published BU exact 2/2 with independently reconstructed BS prerequisite 2/2; Boolean row false `[11239,11240)`, ActiveActor row true `[3238,3239)`; mismatch/reselection 0/0; repeatability and post-stop poison 2/2; following stream/header/payload/second-control consumption 0/0/0/0.\n- active R3.18BW preserves both BV identities: the false Boolean row terminates at BU stop with zero header access; only the true ActiveActor row may expose exactly one following property header through `payload_start`, compared with pinned Boxcars `{BOXCARS}`, then stop.\n- following payload, second later control, false-row header access, witness reselection, production mutation, generalized/repeated cursor and wider semantics remain closed.\n'''
write('MIMIR_CONTINUE_HERE.md', p)

# Knowledge graph.
kg = read('MIMIR_KNOWLEDGE_GRAPH.md')
kg = replace_once(
    kg,
    'R3.18BV published-R3.18BU one-control differential / ACTIVE\n',
    'R3.18BV published-R3.18BU one-control differential / Outcome A CLOSED\nR3.18BW one following-property-header evidence after published R3.18BU mixed control / ACTIVE\n',
    'kg chain',
)
kg = replace_once(
    kg,
    '193. `docs/continuity/MIMIR_R3_18BV_EXECUTION_SPEC.md`\n',
    '193. `docs/continuity/MIMIR_R3_18BV_EXECUTION_SPEC.md`\n194. `docs/continuity/MIMIR_R3_18BV_DECISION.md`\n195. `docs/continuity/MIMIR_R3_18BW_EXECUTION_SPEC.md`\n',
    'kg reading order',
)
kg_marker = '### R3.18BV published-R3.18BU one-control differential: OUTCOME A / CLOSED'
if kg_marker in kg:
    raise SystemExit('kg BV closure duplicate')
kg = kg.rstrip() + f'''\n\n\n{kg_marker}\n- evidence `{BV_HEAD}` / `{BV_TREE}`; runner `{BV_RUN}/{BV_JOB}` SUCCESS; same-head CI `{BV_CI_RUN}/{BV_CI_JOB}` SUCCESS.\n- artifact `{BV_ARTIFACT}` / `sha256:{BV_DIGEST}`; exact published-BU 2/2; BS prerequisite 2/2; false/true 1/1; mismatch/reselection 0/0.\n- repeatability 2/2; post-stop poison 2/2; following stream/header/payload/second-control 0/0/0/0; production mutation 0.\n\n### R3.18BW one following-property-header evidence after published R3.18BU mixed control: ACTIVE\n- preserve exact BV 2-row lane; Boolean=false row is a terminator at 11240.\n- only ActiveActor=true row may enter one following-header observation from BU stop 3239 through exact `payload_start`.\n- compare native structure to pinned Boxcars; classify the complete observed header/context tuple; stop at payload_start.\n- no payload decode, no second later control, no false-row header access, no reselection and no generalized cursor.\n'''
write('MIMIR_KNOWLEDGE_GRAPH.md', kg)

# Boundary locks.
locks = read('docs/continuity/MIMIR_BOUNDARY_LOCKS.md')
new_lock = f'''# 0. Current override — R3.18BV differential closed / R3.18BW one-header evidence active\n\n## PRODUCTION — R3.18BU\n- `{PROD_SHA}` / `{PROD_TREE}` remains canonical production.\n- exact controls: Boolean false `[11239,11240)` and ActiveActor true `[3238,3239)`.\n\n## CLOSED READ-ONLY DIFFERENTIAL — R3.18BV\n- `{BV_HEAD}` / runner `{BV_RUN}/{BV_JOB}` / same-head CI `{BV_CI_RUN}/{BV_CI_JOB}` SUCCESS.\n- artifact `{BV_ARTIFACT}` / `sha256:{BV_DIGEST}`; exact 2/2; BS prerequisite 2/2; false/true 1/1; mismatch/reselection 0/0; adjacent consumption 0/0/0/0.\n\n## ACTIVE READ-ONLY BOUNDARY EVIDENCE — R3.18BW\n- preserve both exact BV identities; false Boolean row terminates with no header access.\n- only the exact true ActiveActor row may observe one following property header through `payload_start`; compare native structure with pinned Boxcars and stop there.\n\n## CLOSED\n- following-header access on the false BU row;\n- witness substitution/reselection;\n- following payload decode or production header composition;\n- second later property-control bit;\n- generalized/repeated property loop/cursor and wider runtime semantics.\n\n# 1. Status vocabulary'''
locks, n = re.subn(r'(?s)# 0\. Current override — .*?\n# 1\. Status vocabulary', new_lock, locks, count=1)
if n != 1:
    raise SystemExit(f'boundary override replacement count={n}')
write('docs/continuity/MIMIR_BOUNDARY_LOCKS.md', locks)

# Concise current truth.
write('docs/continuity/MIMIR_CURRENT_STATE.md', f'''# MIMIR — Current Canonical State\n\n**Continuity date:** {DATE}\n**Repository:** `Naveax/MIMIR`\n**Canonical production SHA:** `{PROD_SHA}`\n**Production tree:** `{PROD_TREE}`\n**Production milestone:** `R3.18BU — bounded post-BS next property-control production`\n**Last read-only evidence/audit:** `R3.18BV — Outcome A / exact 2/2 / BS prerequisite 2/2 / false=1 true=1 / artifact {BV_ARTIFACT}`\n**Current exact pass:** `R3.18BW — one following-property-header evidence after published R3.18BU mixed control`\n\n## Truthful boundary\n\nR3.18BU remains canonical production. R3.18BV closed read-only at `{BV_HEAD}` / `{BV_TREE}` with runner `{BV_RUN}/{BV_JOB}` and natural same-head CI `{BV_CI_RUN}/{BV_CI_JOB}` SUCCESS. Immutable artifact `{BV_ARTIFACT}` / `sha256:{BV_DIGEST}` proves exact published-BU 2/2, BS prerequisite 2/2, one false terminator, one true continuation, repeatability/post-stop poison 2/2, and zero adjacent consumption.\n\nR3.18BW may inspect exactly one following property header only on the exact ActiveActor=true continuation row after BU stop 3239. The Boolean=false row must terminate at 11240 with zero following-header access. Native header structure must match pinned Boxcars and stop at `payload_start`.\n\n## Hard stop\n\nNo following payload, second later control, false-row header access, witness reselection, production mutation, generalized cursor or wider semantic/runtime behavior.\n''')

write('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md', f'''# MIMIR — Next Chat Handoff\n\nCanonical production remains **R3.18BU** `{PROD_SHA}` / `{PROD_TREE}`.\n\nR3.18BV is **Outcome A / CLOSED READ-ONLY** at `{BV_HEAD}` / `{BV_TREE}`. Runner `{BV_RUN}/{BV_JOB}` and same-head natural CI `{BV_CI_RUN}/{BV_CI_JOB}` are SUCCESS. Immutable artifact `{BV_ARTIFACT}` / {BV_ARTIFACT_SIZE} bytes / `sha256:{BV_DIGEST}`. Exact published BU=2/2, BS prerequisite=2/2, false/true=1/1, mismatch/reselection=0/0, repeatability/post-stop poison=2/2, adjacent stream/header/payload/second-control=0/0/0/0.\n\nActive pass: **R3.18BW — one following-property-header evidence after published R3.18BU mixed control**. Preserve exactly the two BV identities. `sample_002.replay` false control terminates at 11240 with no header access. Only `079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay` true control may observe one following property header beginning from BU stop 3239, compare through `payload_start` against pinned Boxcars, classify its complete structural/context tuple, and stop. No payload or later control is in scope.\n''')

# Ledger.
ledger = read('docs/continuity/MIMIR_PROGRESS_LEDGER.md')
ledger_marker = '## 2026-09-14 — R3.18BV — Published R3.18BU One-Control Differential'
if ledger_marker in ledger:
    raise SystemExit('ledger BV duplicate')
ledger = ledger.rstrip() + f'''\n\n---\n\n{ledger_marker}\nOutcome: **A — ADMITTED / READ-ONLY EVIDENCE**\n\nEvidence head/tree: `{BV_HEAD}` / `{BV_TREE}`\nRunner: `{BV_RUN}/{BV_JOB}` SUCCESS\nSame-head natural CI: `{BV_CI_RUN}/{BV_CI_JOB}` SUCCESS\nArtifact: `{BV_ARTIFACT}` / {BV_ARTIFACT_SIZE} bytes / `sha256:{BV_DIGEST}`\nProduction authority: unchanged R3.18BU `{PROD_SHA}` / `{PROD_TREE}`\n\nResults:\n- exact published-BU control rows: 2/2; independently reconstructed BS prerequisite: 2/2;\n- Boolean row false `[11239,11240)`; ActiveActor row true `[3238,3239)`; false/true=1/1;\n- mismatch=0; witness reselection=0; BP false terminator excluded=1/1;\n- repeatability=2/2; post-stop poison=2/2; following stream/header/payload/second-control=0/0/0/0;\n- production/Cargo/fixture/corpus/support mutation=0/0/0/0/0; validation/privacy PASS.\n\nAdmission consequence:\n- R3.18BV closes Outcome A without production mutation;\n- R3.18BW may inspect one following property header only on the exact true ActiveActor continuation row, while the false Boolean row remains a terminator.\n'''
write('docs/continuity/MIMIR_PROGRESS_LEDGER.md', ledger)

# Structured continuity state.
state_path = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(state_path.read_text(encoding='utf-8'))
state['updated_date'] = DATE
state['last_completed_read_only_audit'] = 'R3.18BV'
state['last_completed_evidence_pass'] = 'R3.18BV'
state['last_completed_evidence_outcome'] = f'A — published R3.18BU differential exact 2/2; BS prerequisite 2/2; false/true 1/1; mismatch/reselection 0/0; adjacent consumption 0/0/0/0; artifact {BV_ARTIFACT}.'
state['current_pass'] = 'R3.18BW'
state['current_pass_kind'] = 'read-only one-following-property-header evidence after published R3.18BU mixed control'
state['current_pass_goal'] = 'Preserve the exact BV two-row lane; keep the false Boolean row terminated and compare one following header through payload_start on only the exact true ActiveActor row against pinned Boxcars.'
state['current_pass_stop_boundary'] = 'False row stops at BU stop 11240. True row stops exactly at the observed following header payload_start; consume no payload or second later control.'
state['r3_18bv_admission'] = {
    'status': 'outcome_a_read_only',
    'head': BV_HEAD,
    'tree': BV_TREE,
    'run': BV_RUN,
    'job': BV_JOB,
    'same_head_ci_run': BV_CI_RUN,
    'same_head_ci_job': BV_CI_JOB,
    'artifact': BV_ARTIFACT,
    'artifact_size': BV_ARTIFACT_SIZE,
    'artifact_digest': BV_DIGEST,
    'workflow_blob': BV_WORKFLOW_BLOB,
    'rows': 2,
    'published_bu_exact': 2,
    'bs_prerequisite_exact': 2,
    'false': 1,
    'true': 1,
    'mismatch': 0,
    'witness_reselection': 0,
    'repeatability': 2,
    'post_stop_poison': 2,
    'following_stream_header_payload_second_control': [0, 0, 0, 0],
}
state['current_pass_contract'] = {
    'pass': 'R3.18BW',
    'rows': 2,
    'false_terminators': 1,
    'true_continuations': 1,
    'header_observations': 1,
    'pinned_boxcars': BOXCARS,
    'production_mutation': False,
    'witness_reselection': False,
    'following_payload': False,
    'second_control': False,
    'generic_cursor': False,
}
for f in ['docs/continuity/MIMIR_R3_18BV_DECISION.md', 'docs/continuity/MIMIR_R3_18BW_EXECUTION_SPEC.md']:
    if f not in state.get('next_files_to_read', []):
        state.setdefault('next_files_to_read', []).append(f)
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

# Decision.
write('docs/continuity/MIMIR_R3_18BV_DECISION.md', f'''# MIMIR R3.18BV Decision — Published R3.18BU One-Control Differential\n\n**Date:** {DATE}\n**Status:** OUTCOME A / CLOSED READ-ONLY\n**Production authority:** R3.18BU `{PROD_SHA}` / `{PROD_TREE}`\n**Evidence head/tree:** `{BV_HEAD}` / `{BV_TREE}`\n\n## Immutable receipts\n- evidence runner `{BV_RUN}/{BV_JOB}` SUCCESS\n- same-head natural CI `{BV_CI_RUN}/{BV_CI_JOB}` SUCCESS\n- artifact `{BV_ARTIFACT}` / {BV_ARTIFACT_SIZE} bytes / `sha256:{BV_DIGEST}`\n- workflow blob `{BV_WORKFLOW_BLOB}`\n- immutable BR `{BR_HEAD}` / artifact `{BR_ARTIFACT}` / `sha256:{BR_DIGEST}`\n- pinned Boxcars `{BOXCARS}`\n\n## Admitted result\n1. `external_fixtures/sample_002.replay`: published BU control false at `[11239,11240)`, stop 11240; exact BS prerequisite ends 11239.\n2. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: published BU control true at `[3238,3239)`, stop 3239; exact BS prerequisite ends 3238.\n\nAggregate: exact 2/2; BS prerequisite 2/2; false/true 1/1; mismatch 0; witness reselection 0; BP-false excluded 1/1; repeatability 2/2; post-stop poison 2/2; following stream/header/payload/second-control 0/0/0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; validation/privacy PASS.\n\n## Decision\nR3.18BV closes Outcome A without production mutation. The false Boolean row is a terminator. Open R3.18BW as a separate read-only one-following-header evidence pass on only the exact true ActiveActor continuation row. No payload or later control is admitted.\n''')

# Next exact execution spec, patterned after the analogous BM/AS one-header boundary passes.
write('docs/continuity/MIMIR_R3_18BW_EXECUTION_SPEC.md', f'''# MIMIR R3.18BW — One Following-Property-Header Evidence After Published R3.18BU Mixed Control\n\n**Status:** ACTIVE\n**Pass type:** read-only boundary evidence\n**Production authority:** R3.18BU `{PROD_SHA}` / `{PROD_TREE}`\n**Differential authority:** R3.18BV `{BV_HEAD}` / `{BV_RUN}/{BV_JOB}` / artifact `{BV_ARTIFACT}` / `sha256:{BV_DIGEST}`\n**Production mutation:** forbidden\n**Following payload decode:** forbidden\n**Second later control:** forbidden\n**Witness reselection:** forbidden\n\n## 1. Goal\nPreserve exactly the immutable R3.18BV two-row mixed-control lane. The exact false published-BU Boolean row is a terminator and must stop at BU. On only the exact **1 true** ActiveActor row, observe one following property header through `payload_start`, compare it exactly with native/pinned-Boxcars structural authority, classify the complete observed context, and stop.\n\nThis pass characterizes one header boundary only. It does not publish a following-header composition and does not decode the following payload.\n\n## 2. Frozen authority\n```text\ncanonical continuity base             {MAIN_BASE} / {MAIN_TREE}\nproduction SHA/tree                   {PROD_SHA} / {PROD_TREE}\nproduction parent                     {PROD_PARENT}\nlib / BU focused-test blobs           {LIB_BLOB} / {BU_TEST_BLOB}\nBU execution spec blob                {BU_SPEC_BLOB}\nBV execution spec blob                {BV_SPEC_BLOB}\nBV evidence head/tree                 {BV_HEAD} / {BV_TREE}\nBV authority run/job                  {BV_RUN}/{BV_JOB} SUCCESS\nBV same-head CI                       {BV_CI_RUN}/{BV_CI_JOB} SUCCESS\nBV artifact                           {BV_ARTIFACT} / {BV_ARTIFACT_SIZE} / sha256:{BV_DIGEST}\nBV frozen rows                        2\nBV false / true                       1 / 1\nBV mismatch / reselection             0 / 0\nBV adjacent consumption               0/0/0/0\nBR authority                          {BR_HEAD} / artifact {BR_ARTIFACT} / sha256:{BR_DIGEST}\npinned Boxcars                        {BOXCARS}\n```\n\nHeader tag/context distribution is **not frozen in advance** and must be discovered from the exact one true row. Do not infer a Cartesian allowlist or inherit an older header contract.\n\n## 3. Frozen identities\nExact true continuation:\n```text\ntest_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay BU stop 3239\n```\nExact false terminator:\n```text\nexternal_fixtures/sample_002.replay                                      BU stop 11240\n```\nNo other replay/witness may be selected or substituted.\n\n## 4. Witness classification\nFor both frozen BV rows:\n- reconstruct exact published R3.18BS and R3.18BU;\n- require BU control value/start/end/stop to equal BV/BR authority;\n- if false, classify as terminator and stop with zero following-header access;\n- if true, require identity equal to the exact one-row continuation set and allow exactly one header observation.\n\nRequired split: terminator 1; continuation 1; total 2. Any identity/count drift is Outcome B/C until explained.\n\n## 5. Positive header path — exact 1 true row\nFor the exact ActiveActor continuation:\n1. reconstruct the existing production lookup plan and exact prerequisite chain through published BU;\n2. invoke the existing stateless existing-actor property-header primitive at the exact BU control boundary required by that primitive;\n3. require property-present state true and equal BV/BU authority;\n4. compare stream start/end/value/bound and property-ID width exactly with pinned Boxcars/native structural authority;\n5. compare resolved property object and attribute tag exactly;\n6. retain complete structural/context identity, including replay/version/net-version/RL223 fields actually required by resolution;\n7. compare `payload_start_bit` and header stop exactly;\n8. repeat and require deterministic equality;\n9. poison beginning at `payload_start` and require the returned header unchanged;\n10. stop at `payload_start`.\n\nDo not invoke a payload decoder.\n\n## 6. Terminator path — exact 1 false row\nFor `external_fixtures/sample_002.replay`, published BU control must remain false and exact at `11239 -> 11240`. No following stream/property lookup, header success, payload boundary or later-control access may be claimed after BU stop.\n\n## 7. Evidence outputs\nProduce one privacy-safe immutable evidence artifact containing BV/BU/BR receipts, both control-row reconstructions, exact 1/1 terminator/continuation split, the true-row native and pinned-Boxcars header coordinates, stream bound/property-ID width, resolved property/tag, complete replay/version/net-version/RL223 context, complete tuple multiplicity, repeatability/negative controls, zero payload/later-control counters, zero mutation counters, same-head natural CI receipt, privacy result and SHA-256 inner manifest.\n\n## 8. Required negative controls\nAt minimum:\n- deterministic truncation inside the true-row following header -> fail closed;\n- unresolved stream/property lookup -> reject;\n- wrong actor object/context -> reject;\n- corrupt/mismatched BU prior -> reject;\n- repeatability -> exact equality;\n- poison beginning at `payload_start` -> header unchanged;\n- false Boolean terminator no-header path -> 1/1;\n- fabricated/substituted continuation identity -> reject;\n- source-scope guard -> zero following-payload decoder calls and no repeated/generalized property loop;\n- following payload / second later control consumption -> 0/0.\n\n## 9. Required gates\n```text\nBV witness identities                     2/2 exact\npublished BS/BU reconstruction            2/2 exact\nfalse terminator                          1/1 exact stop\ntrue continuation rows                    1/1\ntrue-row one-header native success        1/1\nnative/Boxcars header equality            1/1\nresolved property object/tag              1/1 exact\npayload_start / header stop               1/1 exact\nheader tuple classification               1/1\nunclassified / mismatch                   0 / 0\nwitness reselection                       0\nfollowing payload bits consumed           0\nsecond later control bits consumed        0\nnegative controls                         PASS\nrepeatability                             PASS\nprivacy                                   PASS\nproduction/Cargo/fixture/corpus/support   0/0/0/0/0\nsame exact evidence-head natural CI       SUCCESS\n```\n\nRun focused BU/BV boundary regressions plus Rust 1.85 fmt/check/test/clippy and the full repository verifier. Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs; reuse an equivalent exact run and never use rerun as polling.\n\n## 10. Hard stop\nNo following payload decode, no second later property control, no production header composition, no header access on the false row, no witness outside the exact one true row, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.\n\n## 11. Outcome gate\n### Outcome A\nThe exact true-row following header matches through `payload_start`; the exact false row remains a terminator; complete header/context classification is exact; mismatch/unclassified/reselection are zero; negatives/full validation/privacy pass; production mutation is zero; following payload/second-control consumption is 0/0. Then a separate smallest exact contract-only pass may freeze only the observed complete header context before any production composition.\n\n### Outcome B\nA bounded header/context distinction or evidence gap exists. Record it and keep production following-header composition closed.\n\n### Outcome C\nAuthority/witness drift, native/oracle mismatch, false-row header access, payload/second-control consumption, production mutation, privacy failure, fabricated continuation membership or generalized chaining. Stop without widening.\n''')

print('R3_18BV_CONTINUITY_SYNC=PASS')
