from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path('.')
DATE = '2026-09-09'
PROD_SHA = 'cbb823ce7d3fc871c35a83afc5ee21ae71945821'
PROD_TREE = '146cb78edfb434fd43e532593efce8e35ee97111'
PROD_PARENT = 'a07b405ee5bb299b468d6bcfc8e66ba89a69e40d'
PARENT_TREE = '9548fcc5cf3d2f8d054b049aee5110edca5342a9'
LIB_BLOB = '89359ead38b18e4a71448217561caed97a41b915'
TEST_BLOB = '5bfd9a81e0de21e70f93e24d8b43a4b540724e9c'
BO_SPEC_BLOB = '3be058d574cf55f3dfaf9e369c37bf3fa42afaa4'
BUILDER_HEAD = '225880eb90f36b3c0f03d144726045d089528257'
BUILDER_RUN = 34346270277
BUILDER_JOB = 102448481752
CANDIDATE_CI_RUN = 34347518210
CANDIDATE_CI_JOB = 102452536398
PUBLISHED_CI_RUN = 34348026122
PUBLISHED_CI_JOB = 102454170761
BM_HEAD = '689b1a24b57a84c81dc19c9a308fb1423f191c4b'
BM_TREE = '1d4e95409e1125b01a78aae6a436190b3c1381f4'
BM_RUN = 34334615939
BM_JOB = 102410984005
BM_CI_RUN = 34334615886
BM_CI_JOB = 102411487443
BM_ARTIFACT = 10097405795
BM_ARTIFACT_SHA = 'bd51a612be2cdd87d9ce1eb141f3f77f47ae29d42aabc8fc16c260a175f27963'
BN_CONTRACT_SHA = '904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c'
BN_CONTRACT_BLOB = 'c5f5a0cd0df3969646fecd8e137a2770c2daae71'
BOXCARS = 'c70e77df7af81b436cb545d070bb90c82f562d0b'


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected one anchor, got {n}')
    return text.replace(old, new, 1)


def replace_field(text: str, key: str, value: str) -> str:
    pattern = rf'(?m)^({re.escape(key)}:\n)  .*?$'
    out, n = re.subn(pattern, rf'\g<1>  {value}', text, count=1)
    if n != 1:
        raise SystemExit(f'{key}: expected one field, got {n}')
    return out


decision = f'''# MIMIR R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production Decision

**Date:** {DATE}
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `{PROD_SHA}` / `{PROD_TREE}`
**Parent:** `{PROD_PARENT}`
**Contract authority:** R3.18BN `sha256:{BN_CONTRACT_SHA}`

## Decision

R3.18BO closes Outcome A on exactly the immutable three-row R3.18BM/R3.18BN/R3.18BK lane. The one published-BK false row remains a successful no-header terminator with zero post-BK reads. Exactly two published-BK true rows compose exactly one existing-actor following property header with the existing stateless suffix primitive, require exact R3.18BN eight-field tuple membership, and stop exactly at `payload_start`.

Exact admitted true contexts remain:

```text
(72,  6, 95, Boolean,     868, 32, 10, false) x1
(110, 6, 66, ActiveActor, 868, 32, 10, false) x1
```

No following payload or second later property-control bit is consumed. No generalized/repeated cursor is introduced.

## Exact authority

```text
canonical parent                      {PROD_PARENT} / {PARENT_TREE}
production SHA/tree                   {PROD_SHA} / {PROD_TREE}
lib/test blobs                        {LIB_BLOB} / {TEST_BLOB}
BO execution spec blob                {BO_SPEC_BLOB}
production builder head               {BUILDER_HEAD}
production builder                    {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
exact-candidate CI                    {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS
published-main CI                     {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
BM evidence head/tree                 {BM_HEAD} / {BM_TREE}
BM evidence run/job                   {BM_RUN}/{BM_JOB} SUCCESS
BM same-head CI                       {BM_CI_RUN}/{BM_CI_JOB} SUCCESS
BM artifact                           {BM_ARTIFACT} / sha256:{BM_ARTIFACT_SHA}
BN contract blob                      {BN_CONTRACT_BLOB}
BN contract                           sha256:{BN_CONTRACT_SHA}
BN membership                         exact_tuple_only / 2 eight-field tuples / multiplicity 2
pinned Boxcars                        {BOXCARS}
```

## Admitted production behavior

```text
frozen BK rows                        3/3
BK false terminators                  1/1
false following header                none 1/1
false post-BK reads                   0
BK true continuations                 2/2
true following headers                exact 2/2
exact BN contexts                     2/2
true tags                             Boolean=1 / ActiveActor=1
property ordinal                      7 on 2/2
upstream AU exclusions                7/7
intermediate BE exclusions            37/37
following payload bits consumed       0
second later control bits consumed    0
generalized/repeated cursor           0
```

The clean production commit contains only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18bo_post_bk_following_header.rs`. No Cargo/dependency, continuity, workflow, fixture, corpus, support, raw-state/event/skill/runtime/export or unrelated mutation entered production.

## Validation

The R3.18BO builder passed exact authority freeze, exact two-file scope, Rust 1.85 formatting, focused BO contract/integration tests, direct BK/BI/BE regressions, workspace/repository validation and clean-candidate reconstruction. The byte-identical candidate passed normal CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}`. Fresh `main` ancestry was rechecked, publication used `force=false`, exact SHA/tree readback matched, and published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` passed on the exact production SHA.

## Hard stop

No following payload, no second later property-control bit, no header on the false BK terminator, no context outside exact R3.18BN membership, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18BP is a separate read-only published-production differential. It must compare published R3.18BO against exactly the immutable three-row BM/BN/BK authority, preserve false=1 / true=2, require exact true-header identity/boundaries and BN membership, keep mismatch and witness reselection at zero, and consume no following payload or second later control.
'''
write('docs/continuity/MIMIR_R3_18BO_DECISION.md', decision)

bp = f'''# MIMIR R3.18BP — Published R3.18BO Mixed Following-Header Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BO `{PROD_SHA}` / `{PROD_TREE}`
**Contract authority:** R3.18BN `sha256:{BN_CONTRACT_SHA}`
**Production mutation:** forbidden
**Following payload:** forbidden
**Second later property-control bit:** forbidden
**Witness reselection:** forbidden

## 1. Goal

Validate published R3.18BO against exactly the immutable three-row R3.18BM/R3.18BN/R3.18BK authority.

- The exact BK-false row must remain a successful no-header terminator and stop at the validated BK boundary with zero post-BK reads.
- The exact two BK-true rows must return exactly one following header matching frozen R3.18BM identity/boundaries and exact R3.18BN eight-field membership, then stop exactly at `payload_start`.
- No following payload or second later control may be consumed.
- The 7 upstream AU exclusions and 37 intermediate BE exclusions remain outside the BO success lane.

## 2. Frozen authority

```text
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
parent                                 {PROD_PARENT}
lib/test blobs                         {LIB_BLOB} / {TEST_BLOB}
BO execution spec blob                 {BO_SPEC_BLOB}
BO production builder                  {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
BO exact-candidate CI                  {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS
BO published-main CI                   {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
BM evidence head/tree                  {BM_HEAD} / {BM_TREE}
BM evidence run/job                    {BM_RUN}/{BM_JOB} SUCCESS
BM artifact                            {BM_ARTIFACT} / sha256:{BM_ARTIFACT_SHA}
BN contract                            sha256:{BN_CONTRACT_SHA}
BN membership                          exact_tuple_only / 2 eight-field tuples / multiplicity 2
immutable mixed lane                   3 rows / false=1 / true=2
observed true-header tags              Boolean=1 / ActiveActor=1
property ordinal                       7 on 2/2
upstream exclusions                    AU=7 / BE=37
pinned Boxcars                         {BOXCARS}
```

## 3. Exact differential lane

For every exact frozen BK witness:
1. reconstruct the exact valid published prerequisites through R3.18BK;
2. call published R3.18BO once;
3. require embedded BK control equality with the recomputed published BK result;
4. on false, require `following_header == None` and BO stop equal BK stop;
5. on true, require exactly one header matching frozen BM identity/boundaries;
6. require exact R3.18BN membership, multiplicity sum 2 and Boolean=1 / ActiveActor=1;
7. require true BO stop equal frozen `payload_start`;
8. repeat and require bit-exact identical result;
9. poison bits beginning at returned stop and require BO unchanged;
10. stop without payload or later-control access.

Expected totals:

```text
rows                         3/3
false no-header              1
true exact header            2
exact BN contexts            2/2
BN multiplicity sum          2
tag distribution             Boolean=1 / ActiveActor=1
property ordinal             7 on 2/2
mismatch                     0
witness reselection          0
following payload            0 bits
second later control         0 bits
```

## 4. Required negative controls

At minimum: false-row post-stop poison; all 7 AU and 37 BE exclusions remain outside BO success; true-header truncation; true `payload_start` poison; wrong actor; unresolved lookup; wrong exact version/context; corrupt BK prerequisite; RL223 flip/drop; tag/component/Cartesian/versionless widening; older-contract BN-absent tuple; fabricated third tuple; source-scope guard with zero payload decoder and no repeated/generalized loop.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact BO SHA/tree/blob/CI receipts, BM/BN authority receipts, all three frozen witness identities, per-row BK/BO/BM/direct-header comparison, exact context/multiplicity and tag summaries, repeatability and negative controls, payload/later-control counters, production/Cargo/fixture/corpus/support mutation counters, same-head natural-CI receipt, privacy result and SHA-256 manifest.

## 6. Validation

Require frozen identity 3/3; published BO exact 3/3; false=1 / true=2; true frozen header identity/boundary exact 2/2; exact BN contexts 2/2 and multiplicity 2; Boolean=1 / ActiveActor=1; mismatch/reselection 0/0; repeatability and all negatives PASS; following payload/second control 0/0; focused BO regressions; full fmt/check/test/clippy/repository verifier; same-head CI SUCCESS; mutation 0/0/0/0/0; privacy PASS.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs. Reuse an existing exact run if present. Rerun is never polling.

## 7. Hard stop

No following payload, no second later control, no context outside exact R3.18BN, no header on the false terminator, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Published R3.18BO matches all 3 immutable BM/BN/BK witnesses exactly: false=1 no-header, true=2 exact header, exact contexts/multiplicity and tag distribution preserved, mismatch 0, witness reselection 0, all negative/full validations PASS, and following-payload/second-control consumption 0/0. Only then may a separate later evidence pass inspect exactly one following payload on the exact two true rows.

### Outcome B
A bounded mismatch or narrower safe subset is isolated. Record only the exact supported subset and keep following-payload evidence closed.

### Outcome C
Authority/witness drift, false-terminator header access, true-header mismatch, BN widening, adjacent payload/later-control access, production mutation, generic chaining or privacy failure. Stop without widening.
'''
write('docs/continuity/MIMIR_R3_18BP_EXECUTION_SPEC.md', bp)

current = f'''# MIMIR — Current Canonical State

**Continuity date:** {DATE}
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18BO — bounded post-BK mixed-continuation following-header production`
**Last read-only evidence/audit:** `R3.18BM — Outcome A / false=1 true=2 / one-header exact 2/2 / contexts=2 / artifact {BM_ARTIFACT}`
**Last completed contract:** `R3.18BN — exact_tuple_only / 2 eight-field contexts / multiplicity 2 / contract {BN_CONTRACT_SHA}`
**Current exact pass:** `R3.18BP — published R3.18BO mixed following-header differential`

## Truthful boundary

R3.18BO is canonical production. Exactly three valid published R3.18BK rows enter BO. The one false BK row terminates successfully without post-BK header access. Exactly two true BK rows compose one R3.18BN-admitted existing-actor following header and stop at `payload_start`; tags are Boolean=1 / ActiveActor=1 and property ordinal is 7 on 2/2.

```text
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
parent                                 {PROD_PARENT}
lib/test blobs                         {LIB_BLOB} / {TEST_BLOB}
builder                                {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
exact-candidate CI                     {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS
published-main CI                      {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
valid BO rows                          3/3
false no-header                        1
true exact header                      2
exact BN contexts                      2/2
true tags                              Boolean=1 / ActiveActor=1
property ordinal                       7 on 2/2
upstream exclusions                    AU=7 / BE=37
following payload / second control     0 / 0
```

## Active differential gate

R3.18BP is read-only. It must compare published BO against exactly the immutable BM/BN/BK three-row authority, preserve false=1 / true=2, exact header identity and exact BN membership, keep mismatch/reselection at zero, and consume no payload or later-control bits.

## Hard stop

No following payload, second later control, header on the false terminator, context outside exact R3.18BN membership, generalized/repeated property cursor, or actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
'''
write('docs/continuity/MIMIR_CURRENT_STATE.md', current)

handoff = f'''# MIMIR — Next Chat Handoff

Canonical production is **R3.18BO** at `{PROD_SHA}` / `{PROD_TREE}`.

**R3.18BM is CLOSED / Outcome A evidence.** Exact three-row lane false=1 / true=2; two true headers are native/Boxcars exact 2/2 through `payload_start`; contexts=2; payload/second-control=0/0; artifact `{BM_ARTIFACT}`.

**R3.18BN is CLOSED / Outcome A contract.** Exact contract `sha256:{BN_CONTRACT_SHA}` admits only `(72,6,95,Boolean,868,32,10,false)` x1 and `(110,6,66,ActiveActor,868,32,10,false)` x1.

**R3.18BO is CLOSED / Outcome A production.** Exact BK lane false=1 successful no-header terminator; true=2 exact BN headers; stop=`payload_start`; payload/second-control=0/0. Builder `{BUILDER_RUN}/{BUILDER_JOB}`, candidate CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` and published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` are SUCCESS.

Active pass: **R3.18BP — Published R3.18BO Mixed Following-Header Differential**.

R3.18BP is read-only. Reuse exactly the immutable three BM/BN/BK witnesses, require exact BN membership and zero mismatch/reselection, and consume no following payload or second later control.

Read first: `MIMIR_CONTINUE_HERE.md`, BM decision, BN execution spec, BN contract, BN decision, BO execution spec, BO decision, BP execution spec, continuity state/current state/boundary locks, then the root knowledge graph chain.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run.
'''
write('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md', handoff)

state_path = 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(read(state_path))
state['updated_date'] = DATE
state['last_production_code_sha'] = PROD_SHA
state['last_production_milestone'] = 'R3.18BO'
state['last_production_milestone_name'] = 'bounded post-BK mixed-continuation following-header production'
state['current_pass'] = 'R3.18BP'
state['current_pass_kind'] = 'read-only published-production differential over the exact three-row BM/BN/BK mixed following-header authority'
state['current_pass_goal'] = 'Compare published R3.18BO against exactly the immutable three-row authority; preserve false=1 no-header and true=2 exact BN headers, mismatch/reselection 0/0, and stop without payload or later-control access.'
state['current_pass_stop_boundary'] = 'No following payload, no second later control, no header on the false terminator, no context outside exact R3.18BN membership, and no generalized cursor.'
for item in [
    'following payload after published R3.18BO',
    'second later property-control bit after published R3.18BO',
    'header synthesis on the R3.18BO false terminator',
    'following-header contexts outside exact R3.18BN membership after R3.18BO',
    'generalized/repeated property loop or generic cursor after R3.18BO',
    'production mutation during R3.18BP',
]:
    if item not in state['closed_now']:
        state['closed_now'].append(item)
read_order = state.get('next_files_to_read', [])
for item in ['docs/continuity/MIMIR_R3_18BO_DECISION.md', 'docs/continuity/MIMIR_R3_18BP_EXECUTION_SPEC.md']:
    if item not in read_order:
        try:
            idx = read_order.index('docs/continuity/MIMIR_PASS_PROTOCOL.md')
        except ValueError:
            idx = len(read_order)
        read_order.insert(idx, item)
state['next_files_to_read'] = read_order
write(state_path, json.dumps(state, indent=2, ensure_ascii=False) + '\n')

locks = read('docs/continuity/MIMIR_BOUNDARY_LOCKS.md')
start = locks.index('# 0. Current override')
end = locks.index('# 1. Status vocabulary')
override = f'''# 0. Current override — R3.18BO production closed / R3.18BP differential active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BO
- `{PROD_SHA}` / `{PROD_TREE}` is canonical production.
- exactly the three immutable BM/BN/BK authority rows are admitted at the BO following-header boundary.
- false=1 is a successful no-header terminator with zero post-BK reads.
- true=2 compose exactly one stateless following header under exact R3.18BN membership and stop at `payload_start`.
- following payload / second later control remains 0/0.

## CLOSED READ-ONLY EVIDENCE — R3.18BM Outcome A
- evidence `{BM_HEAD}` / `{BM_RUN}/{BM_JOB}` SUCCESS; same-head CI `{BM_CI_RUN}/{BM_CI_JOB}` SUCCESS.
- exact split: one false terminator / two true headers; native/Boxcars exact 2/2; unique contexts 2.

## CLOSED CONTRACT — R3.18BN Outcome A
- contract sha256 `{BN_CONTRACT_SHA}`; exact_tuple_only; 2 complete eight-field tuples; multiplicity sum 2.
- the one BK-false terminator remains outside header membership.

## ACTIVE READ-ONLY DIFFERENTIAL — R3.18BP
- compare published R3.18BO against exactly the immutable three-row authority;
- preserve false=1 no-header and true=2 exact BN headers;
- require mismatch/reselection 0/0 and repeatability;
- consume zero following-payload and zero second-later-control bits;
- production mutation is forbidden.

## CLOSED
- header on the false terminator;
- context outside exact R3.18BN membership;
- following payload after R3.18BO;
- second later property-control bit;
- repeated/generalized property loop or generic cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

'''
locks = locks[:start] + override + locks[end:]
write('docs/continuity/MIMIR_BOUNDARY_LOCKS.md', locks)

master = read('MIMIR_CONTINUE_HERE.md')
master = replace_field(master, 'LAST_PRODUCTION_CODE_SHA', PROD_SHA)
master = replace_field(master, 'LAST_PRODUCTION_MILESTONE', 'R3.18BO — bounded post-BK mixed-continuation following-header production')
master = replace_field(master, 'CURRENT_PASS', 'R3.18BP — published R3.18BO mixed following-header differential')
master = replace_field(master, 'CURRENT_PASS_TYPE', 'read-only published-production differential / exact three-row BM/BN/BK authority / false=1 no-header / true=2 exact BN headers / payload-second-control 0/0')
master += f'''\n\n# CURRENT OVERRIDE — {DATE} — R3.18BO CLOSED / R3.18BP ACTIVE\n\nThis newest current override supersedes stale R3.18BO ACTIVE wording in historical/checklist sections above.\n\n- canonical production: `{PROD_SHA}` / `{PROD_TREE}`;\n- BO exact lane: 3 rows / false=1 no-header / true=2 exact BN headers;\n- exact BN contract: `sha256:{BN_CONTRACT_SHA}`;\n- candidate CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` and published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS;\n- following payload / second later control: 0/0;\n- active pass: R3.18BP read-only published-production differential;\n- production mutation, payload access, later-control access and generalized cursor remain forbidden.\n'''
write('MIMIR_CONTINUE_HERE.md', master)

kg = read('MIMIR_KNOWLEDGE_GRAPH.md')
kg = replace_once(kg, 'R3.18BO bounded post-BK mixed-continuation following-header production / ACTIVE', 'R3.18BO bounded post-BK mixed-continuation following-header production / PRODUCTION CLOSED\nR3.18BP published-R3.18BO mixed following-header differential / ACTIVE', 'graph chain')
old = '''172. `docs/continuity/MIMIR_R3_18BO_EXECUTION_SPEC.md`
173. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
174. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
175. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
176. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
177. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
178. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
179. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
new = '''172. `docs/continuity/MIMIR_R3_18BO_EXECUTION_SPEC.md`
173. `docs/continuity/MIMIR_R3_18BO_DECISION.md`
174. `docs/continuity/MIMIR_R3_18BP_EXECUTION_SPEC.md`
175. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
176. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
177. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
178. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
179. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
180. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
181. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
kg = replace_once(kg, old, new, 'mandatory reading order')
kg += f'''\n\n## CURRENT OVERRIDE — {DATE} — R3.18BO CLOSED / R3.18BP ACTIVE\n\nThis newest override supersedes older historical `ACTIVE` wording above.\n\n- canonical production is R3.18BO `{PROD_SHA}` / `{PROD_TREE}`;\n- clean production scope is `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18bo_post_bk_following_header.rs`;\n- builder `{BUILDER_RUN}/{BUILDER_JOB}`, candidate CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` and published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` are SUCCESS;\n- BO lane is exactly 3 rows: false=1 no-header / true=2 exact BN headers;\n- BN membership remains `sha256:{BN_CONTRACT_SHA}` with Boolean=1 / ActiveActor=1 and ordinal 7 on 2/2;\n- payload / second later control consumption is 0/0;\n- R3.18BP is ACTIVE and read-only; no wider capability is admitted.\n'''
write('MIMIR_KNOWLEDGE_GRAPH.md', kg)

ledger = read('docs/continuity/MIMIR_PROGRESS_LEDGER.md')
if '## 2026-09-09 — R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production' in ledger:
    raise SystemExit('BO ledger entry already exists')
ledger += f'''\n\n---\n\n## 2026-09-09 — R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production\n\nProduction base SHA: `{PROD_PARENT}`\nProduction commit SHA: `{PROD_SHA}`\nPass type: bounded production implementation\nOutcome: **A — ADMITTED / PUBLISHED**\n\nWhat changed:\n- one boundary-specific BO composition plus one focused integration test;\n- exact BK prior is recomputed; false=1 terminates with no header; true=2 compose one exact BN header and stop at `payload_start`.\n\nAuthority / validation:\n- builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS at `{BUILDER_HEAD}`;\n- candidate `{PROD_SHA}` / `{PROD_TREE}`; lib/test `{LIB_BLOB}` / `{TEST_BLOB}`;\n- candidate CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS;\n- published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS;\n- BM artifact `{BM_ARTIFACT}` / `sha256:{BM_ARTIFACT_SHA}`;\n- BN contract `sha256:{BN_CONTRACT_SHA}` / exact_tuple_only / 2 tuples / multiplicity 2;\n- fresh ancestry / force=false / exact readback PASS.\n\nObserved behavior:\n- BK lane 3/3; false=1; true=2; Boolean=1 / ActiveActor=1; ordinal 7 on 2/2; AU exclusions 7 / BE exclusions 37; payload/second-control 0/0; generalized cursor 0.\n\nBoundaries still closed:\n- following payload; second later control; header on false; context outside exact BN; generalized cursor; wider semantic/runtime layers.\n\nNext exact pass:\n- `R3.18BP — published R3.18BO mixed following-header differential` on exactly the immutable three-row authority.\n'''
write('docs/continuity/MIMIR_PROGRESS_LEDGER.md', ledger)

for path in [
    'MIMIR_CONTINUE_HERE.md',
    'MIMIR_KNOWLEDGE_GRAPH.md',
    'docs/continuity/MIMIR_BOUNDARY_LOCKS.md',
    'docs/continuity/MIMIR_CONTINUITY_STATE.json',
    'docs/continuity/MIMIR_CURRENT_STATE.md',
    'docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md',
    'docs/continuity/MIMIR_PROGRESS_LEDGER.md',
    'docs/continuity/MIMIR_R3_18BO_DECISION.md',
    'docs/continuity/MIMIR_R3_18BP_EXECUTION_SPEC.md',
]:
    if not (ROOT / path).is_file():
        raise SystemExit(f'missing generated file: {path}')

print('R3_18BO_ADMISSION_GENERATOR=PASS')
print('R3_18BP_OPENED=PASS')
