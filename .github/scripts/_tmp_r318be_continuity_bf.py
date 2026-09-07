from pathlib import Path
import json

PROD_SHA = "1d717d3e82179edd85b197968f46b8f951a3e828"
PROD_TREE = "72cf2b907437a1ba62cc9deebd7608f7d0372f81"
PROD_PARENT = "3fa88f27201ee91c51a3bb7a623c00b46204c1e0"
PARENT_TREE = "f193ee65fcc677178891fe5cb006f2fb2903cae9"
LIB_BLOB = "92d9d1893d75f9f0bd5ca921d8cf80455b88f0c3"
TEST_BLOB = "78f32c79a3526cbfeac4e32ccc06e5965cd3e97b"
BE_SPEC_BLOB = "c5f708fbc88732402bf057bd1274dc11f90669a2"
BUILDER_HEAD = "5ae76da91fb21ec9b62201673f6434fa2203cf6d"
BUILDER_RUN = 33129018318
BUILDER_JOB = 98713908063
PR = 209
PR_CI_RUN = 34094630343
PR_CI_JOB = 101655343287
PUBLISHED_CI_RUN = 34095061141
PUBLISHED_CI_JOB = 101656732728
BC_HEAD = "0f4d07f5caf77ec53f5e8b512867ad17b5835ca1"
BC_TREE = "a198866dc3f18ffbd5cb16e32d39dada5f4116fc"
BC_RUN = 33122152803
BC_JOB = 98691409657
BC_ARTIFACT = 9666964713
BC_DIGEST = "sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e"
BD_CONTRACT_BLOB = "b0c2610b3d36e25302f35037518990fa3bc9fe69"
BD_CONTRACT_SHA256 = "33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27"
PINNED_BOXCARS = "c70e77df7af81b436cb545d070bb90c82f562d0b"
DATE = "2026-09-07"


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


# Decision receipt.
decision = f'''# MIMIR R3.18BE — Bounded Post-BA Mixed-Continuation Following-Header Production Decision

**Date:** {DATE}
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `{PROD_SHA}` / `{PROD_TREE}`
**Parent:** `{PROD_PARENT}`

## Decision

R3.18BE closes Outcome A. On the exact immutable forty-row R3.18BA/R3.18BC/R3.18BD authority lane, all thirty-seven BA-false rows remain successful no-header terminators with zero post-BA reads. On the exact three BA-true rows, production composes exactly one existing-actor following header with the existing stateless primitive, requires exact R3.18BD eight-field membership, and stops exactly at `payload_start`.

The exact true-header contexts remain the three R3.18BD tuples with observed tags **Boolean=2 / Float=1**. No following payload or second later property-control bit is consumed. The seven upstream R3.18AU false terminators remain outside the BA/BE lane because they do not possess a valid BA prior.

This admission is boundary-specific. It does not admit header synthesis on false BA terminators, any context outside R3.18BD, following payload, later control, a generalized/repeated property cursor, or wider actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior.

## Exact authority

```text
canonical main before production       {PROD_PARENT} / {PARENT_TREE}
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
lib / focused-test blobs               {LIB_BLOB} / {TEST_BLOB}
BE execution spec blob                 {BE_SPEC_BLOB}
production builder head                {BUILDER_HEAD}
production builder                     {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
validation-only PR                     #{PR} CLOSED / UNMERGED
exact-candidate PR CI                  {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
published-main CI                      {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
BC evidence head/tree                  {BC_HEAD} / {BC_TREE}
BC evidence run/job                    {BC_RUN}/{BC_JOB} SUCCESS
BC artifact                            {BC_ARTIFACT} / {BC_DIGEST}
BD contract blob                       {BD_CONTRACT_BLOB}
BD contract                            sha256:{BD_CONTRACT_SHA256}
BD membership                          exact_tuple_only / 3 eight-field tuples / multiplicity 3
pinned Boxcars                         {PINNED_BOXCARS}
```

## Admitted production behavior

```text
frozen BA/BE rows                      40/40
BA false terminators                   37/37
false-path following header            none 37/37
false post-BA reads                    0
BA true continuations                  3/3
true following headers                 exact 3/3
exact R3.18BD contexts                 3/3
observed true-header tags              Boolean=2 / Float=1
upstream AU false terminators          7/7 excluded
following payload bits consumed        0
second later control bits consumed     0
generalized/repeated cursor            0
```

The builder passed the focused R3.18BE target plus BA/AY/header prerequisite regressions, workspace check/test, Clippy with warnings denied, and the repository verifier under Rust 1.85. The exact clean candidate then passed validation-only PR CI. PR #{PR} was closed unmerged, fresh `main` ancestry was rechecked, publication used `force=false`, exact SHA/tree readback matched, and the published-main SHA passed repository CI again.

## Clean publication

The production commit contains only:
- `crates/mimir-replay/src/lib.rs`;
- `crates/mimir-replay/tests/r3_18be_post_ba_following_header.rs`.

The exact diff is 775 additions / 2 deletions across those two files. No Cargo/dependency, continuity, workflow, fixture, corpus, support, raw-state/event/skill/runtime/export or unrelated mutation entered production.

## Hard stop

No following payload after the one admitted true-path header, no second later property-control bit, no header on any of the thirty-seven BA-false terminators, no context outside exact R3.18BD membership, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18BF is a separate read-only published-production differential. It must compare published R3.18BE against exactly the immutable forty-row BA/BC/BD authority, preserve false=37 and true=3, require exact true-header identity/boundaries and BD context equality, keep mismatch and witness reselection at zero, and consume no following payload or second later control. Only BF Outcome A may open a separate R3.18BG one-following-payload evidence pass on the exact three true rows.
'''
write("docs/continuity/MIMIR_R3_18BE_DECISION.md", decision)


# Next exact pass.
bf = f'''# MIMIR R3.18BF — Published R3.18BE Mixed Following-Header Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BE `{PROD_SHA}` / `{PROD_TREE}`
**Production mutation:** forbidden
**Following payload:** forbidden
**Second later property-control bit:** forbidden
**Witness reselection:** forbidden

## 1. Goal

Validate published R3.18BE against exactly the immutable forty-row R3.18BA/R3.18BC/R3.18BD authority lane.

- The exact 37 BA-false rows must remain successful no-header terminators and stop at the validated BA/BE terminator boundary with zero post-BA reads.
- The exact 3 BA-true rows must return exactly one following header matching the frozen R3.18BC identity/boundaries and exact R3.18BD eight-field membership, then stop exactly at `payload_start`.
- No following payload or second later control may be consumed.
- The seven upstream R3.18AU false terminators remain outside the BA/BE/BF lane and may not be promoted into a successful BE result.

## 2. Frozen authority

```text
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
parent                                 {PROD_PARENT}
lib / focused-test blobs               {LIB_BLOB} / {TEST_BLOB}
BE execution spec blob                 {BE_SPEC_BLOB}
BE production builder                  {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
BE validation PR                       #{PR} closed unmerged
BE exact-head PR CI                    {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
BE published-main CI                   {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
BC evidence head/tree                  {BC_HEAD} / {BC_TREE}
BC evidence run/job                    {BC_RUN}/{BC_JOB} SUCCESS
BC artifact                            {BC_ARTIFACT} / {BC_DIGEST}
BD contract                            sha256:{BD_CONTRACT_SHA256}
BD membership                          exact_tuple_only / 3 eight-field tuples / multiplicity 3
immutable mixed lane                   40 rows / false=37 / true=3
observed true-header tags              Boolean=2 / Float=1
upstream AU false terminators          7 rows excluded
pinned Boxcars                         {PINNED_BOXCARS}
```

R3.18BC and R3.18BD are immutable authorities. R3.18BF may not reselect witnesses, infer a larger tuple set, or inherit R3.18AT/AJ/Z/P membership.

## 3. Exact differential lane

For every exact frozen BA/BC/BD witness:

1. reconstruct the exact valid published prerequisites through R3.18BA;
2. call published R3.18BE once;
3. require the returned embedded BA control to equal the exact recomputed published BA result;
4. on false, require `following_header == None` and BE stop equal BA stop;
5. on true, require exactly one header whose stream/property/tag/context coordinates and boundary equal frozen R3.18BC authority;
6. require every true header to be an exact R3.18BD member, with exact context multiplicity sum 3 and tag distribution Boolean=2 / Float=1;
7. require true BE stop equal frozen header `payload_start`;
8. repeat and require bit-exact identical result;
9. poison bits beginning at the returned stop and require the returned BE result unchanged;
10. stop without payload or later-control access.

Expected totals:

```text
rows                         40/40
false no-header              37
true exact header            3
exact BD contexts            3/3
BD multiplicity sum          3
tag distribution             Boolean=2 / Float=1
mismatch                     0
witness reselection          0
following payload            0 bits
second later control         0 bits
```

## 4. Required negative controls

At minimum:
- all seven upstream AU false terminators remain outside BA/BE success;
- false-row poison beginning at BA/BE stop leaves the false terminator result unchanged;
- truncate a true row after BA but inside its following header -> reject atomically;
- poison at true-row `payload_start` -> published BE header result unchanged;
- wrong actor object -> reject;
- unresolved lookup -> reject;
- wrong exact version/context -> reject;
- corrupt or mismatched published BA prerequisite -> reject;
- flip/drop `is_rl_223` -> reject unless the complete resulting tuple is independently an exact BD member;
- tag-only/component-only/Cartesian/versionless membership -> reject;
- AT-valid but BD-absent `(60,5,107,Int,868,32,10,false)` -> reject;
- fabricated fourth tuple -> reject;
- source-scope guard -> at most one following-header primitive, zero payload decoders, no generalized/repeated loop.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact BE SHA/tree/blob/CI receipts, exact BC/BD authority receipts, all forty frozen witness identities, per-row BA/BE/BC/direct-header comparison, exact context/multiplicity and tag summaries, repeatability and negative controls, payload/later-control consumption counters, production/Cargo/fixture/corpus/support mutation counters, same-head natural-CI receipt, privacy result and SHA-256 manifest.

## 6. Validation

Require:
- frozen witness identity 40/40;
- published BE exact 40/40;
- false=37 / true=3;
- true frozen header identity/boundary exact 3/3;
- exact BD context identity 3/3 and multiplicity sum 3;
- Boolean=2 / Float=1;
- mismatch 0 and witness reselection 0;
- repeatability PASS;
- all negative controls PASS;
- following payload / second later control 0/0;
- focused BE regressions PASS;
- full mimir-replay/workspace fmt/check/test/clippy and repository verifier PASS;
- same-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy scan PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse an existing exact run if present. Rerun is never polling.

## 7. Hard stop

No following payload, no second later control, no context outside exact R3.18BD, no header on false terminators, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Published R3.18BE matches all 40 immutable BA/BC/BD witnesses exactly: false=37 no-header, true=3 exact header, exact contexts/multiplicity and tag distribution preserved, mismatch 0, witness reselection 0, all negative/full validations PASS, and following-payload/second-control consumption 0/0. A separate R3.18BG evidence pass may then inspect exactly one following payload on the exact three true rows only.

### Outcome B
A bounded differential mismatch or narrower safe subset is isolated. Record only the exact supported subset and keep following-payload evidence closed.

### Outcome C
Authority/witness drift, false-terminator header access, true-header mismatch, BD membership widening, adjacent payload/later-control access, production mutation, generic chaining or privacy failure. Stop without widening.
'''
write("docs/continuity/MIMIR_R3_18BF_EXECUTION_SPEC.md", bf)


# Compact canonical summaries are replaced completely.
current = f'''# MIMIR — Current Canonical State

**Continuity date:** {DATE}
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18BE — bounded post-BA mixed-continuation following-header production`
**Last read-only evidence/audit:** `R3.18BC — Outcome A / false=37 true=3 / true headers exact 3/3 / contexts=3 / artifact {BC_ARTIFACT}`
**Last completed contract:** `R3.18BD — exact_tuple_only / 3 eight-field contexts / multiplicity 3 / contract {BD_CONTRACT_SHA256}`
**Current exact pass:** `R3.18BF — published R3.18BE mixed following-header differential`

## Truthful boundary

R3.18BE is canonical production. Exactly forty valid R3.18BA rows may enter BE. Thirty-seven false BA controls terminate successfully without any post-BA header access. Exactly three true BA controls compose one R3.18BD-admitted existing-actor following header and stop at `payload_start`; observed tags are Boolean=2 / Float=1. Seven upstream AU false terminators remain outside the BA/BE lane. Production consumes no following payload or second later control.

```text
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
parent                                 {PROD_PARENT}
lib/test blobs                         {LIB_BLOB} / {TEST_BLOB}
builder                                {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
validation PR                          #{PR} CLOSED UNMERGED
PR CI                                  {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
published-main CI                      {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
valid BE rows                          40/40
false no-header                        37
true exact header                      3
exact BD contexts                     3/3
true tags                              Boolean=2 / Float=1
upstream AU false terminators excluded 7/7
following payload / second control     0/0
```

## Current gate

R3.18BF is read-only. It must validate published BE against exactly the immutable forty-row BA/BC/BD authority with mismatch/reselection zero, exact 37/3 branching, exact three BD contexts and no adjacent payload/later-control consumption. It may not decode a following payload.

## Hard stop

No following payload, second later control, generalized property cursor, actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
'''
write("docs/continuity/MIMIR_CURRENT_STATE.md", current)

handoff = f'''# MIMIR — Next Chat Handoff

Canonical production is **R3.18BE** at `{PROD_SHA}` / `{PROD_TREE}`, parent `{PROD_PARENT}`. The clean production commit changes only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18be_post_ba_following_header.rs`.

R3.18BE validates/recomputes one exact published R3.18BA mixed control. False rows (**37**) terminate successfully with no following-header access. True rows (**3**) compose exactly one stateless existing-actor header under exact R3.18BD membership and stop at `payload_start`; observed true tags are Boolean=2 / Float=1. Seven upstream AU false terminators remain outside the BA/BE lane. Following payload / second later control consumption is 0/0.

Validation: builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; PR #{PR} closed unmerged with exact-head CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS; published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS; publication force=false.

The active pass is **R3.18BF published R3.18BE mixed following-header differential**. Use exactly the immutable forty-row BC/BD-backed lane. Require published BE exact 40/40, false=37 / true=3, true headers exact 3/3, exact BD contexts 3/3, Boolean=2 / Float=1, mismatch/reselection 0/0, repeatability/negatives PASS and payload/second-control 0/0. BF is read-only and must not decode a following payload.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
'''
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)


# Boundary locks: replace current override only.
locks_path = Path("docs/continuity/MIMIR_BOUNDARY_LOCKS.md")
locks = locks_path.read_text(encoding="utf-8")
start = locks.find("# 0. Current override —")
end = locks.find("# 1. Status vocabulary")
if start < 0 or end < 0 or end <= start:
    raise SystemExit("boundary lock anchors missing")
override = f'''# 0. Current override — R3.18BE production closed / R3.18BF active differential

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BE
- `{PROD_SHA}` / `{PROD_TREE}` is canonical production, parent `{PROD_PARENT}`.
- exactly 40 valid BA rows enter BE; 37 false rows terminate with no header and 3 true rows compose one exact R3.18BD-admitted header.
- true headers stop at `payload_start`; exact tags Boolean=2 / Float=1.
- seven upstream AU false terminators remain outside BA/BE.
- following payload / second later control consumption remains 0/0.

## ACTIVE READ-ONLY DIFFERENTIAL — R3.18BF
- immutable authority is the forty-row BA/BC/BD-backed lane.
- compare published BE branching, header identity/boundary and exact BD membership with mismatch/reselection 0/0.
- 37 false rows terminate; 3 true rows expose exactly one header only.

## CLOSED
- following payload during BF, including on the three true rows;
- second later property-control bit;
- header synthesis on any of the 37 false BA rows;
- BA/BE/BF success on seven upstream AU false terminators;
- contexts outside exact R3.18BD membership;
- repeated/generalized property loop or generic cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

'''
locks_path.write_text(locks[:start] + override + locks[end:], encoding="utf-8", newline="\n")


# Machine continuity state.
state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"] = DATE
state["last_production_code_sha"] = PROD_SHA
state["last_production_milestone"] = "R3.18BE"
state["last_production_milestone_name"] = "bounded post-BA mixed-continuation following-header production"
state["current_pass"] = "R3.18BF"
state["current_pass_kind"] = "read-only published-production differential / exact published R3.18BE versus immutable BA/BC/BD mixed following-header authority"
state["current_pass_goal"] = "Validate published R3.18BE on exactly 40 frozen rows: false=37 no-header, true=3 exact BD headers, exact contexts 3/3, Boolean=2 / Float=1, mismatch/reselection 0/0."
state["current_pass_stop_boundary"] = "No following payload, no second later control, no header on false terminators, no context outside exact R3.18BD, no generalized cursor, and seven upstream AU false terminators remain outside."
state["r3_18be"] = {
    "status": "production_closed",
    "sha": PROD_SHA,
    "tree": PROD_TREE,
    "parent": PROD_PARENT,
    "lib_blob": LIB_BLOB,
    "test_blob": TEST_BLOB,
    "rows": 40,
    "false_no_header": 37,
    "true_exact_header": 3,
    "exact_bd_contexts": 3,
    "true_tag_distribution": {"Boolean": 2, "Float": 1},
    "upstream_au_false_terminators_excluded": 7,
    "adjacent_consumption": "payload=0/second_control=0",
    "builder_head": BUILDER_HEAD,
    "builder_run": BUILDER_RUN,
    "builder_job": BUILDER_JOB,
    "validation_pr": PR,
    "pr_ci_run": PR_CI_RUN,
    "published_main_ci_run": PUBLISHED_CI_RUN
}
state["r3_18bf"] = {
    "status": "active_read_only_differential",
    "frozen_rows": 40,
    "expected_false_no_header": 37,
    "expected_true_exact_header": 3,
    "contract": "R3.18BD exact_tuple_only",
    "contract_sha256": BD_CONTRACT_SHA256,
    "following_payload_open": False,
    "second_later_control_open": False
}
closed = state.setdefault("closed_now", [])
for item in [
    "following payload during R3.18BF",
    "second later property-control bit after R3.18BE/R3.18BF",
    "header synthesis on R3.18BE false terminators",
    "following-payload evidence before R3.18BF Outcome A"
]:
    if item not in closed:
        closed.append(item)
reads = state.setdefault("next_files_to_read", [])
be_spec = "docs/continuity/MIMIR_R3_18BE_EXECUTION_SPEC.md"
be_dec = "docs/continuity/MIMIR_R3_18BE_DECISION.md"
bf_spec = "docs/continuity/MIMIR_R3_18BF_EXECUTION_SPEC.md"
if be_spec not in reads:
    raise SystemExit("BE spec missing from next_files_to_read")
for item in (be_dec, bf_spec):
    while item in reads:
        reads.remove(item)
pos = reads.index(be_spec) + 1
reads[pos:pos] = [be_dec, bf_spec]
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


# Root handbook: update canonical pointers and append the newest override.
handbook_path = Path("MIMIR_CONTINUE_HERE.md")
handbook = handbook_path.read_text(encoding="utf-8")
handbook = replace_once(
    handbook,
    "LAST_PRODUCTION_CODE_SHA:\n  5d2bca711f528ab1bb607104379af503ff175697\n\nLAST_PRODUCTION_MILESTONE:\n  R3.18BA — bounded post-AY mixed following-control production",
    f"LAST_PRODUCTION_CODE_SHA:\n  {PROD_SHA}\n\nLAST_PRODUCTION_MILESTONE:\n  R3.18BE — bounded post-BA mixed-continuation following-header production",
    "handbook production pointer"
)
handbook = replace_once(
    handbook,
    "CURRENT_PASS:\n  R3.18BE — bounded post-BA mixed-continuation following-header production\n\nCURRENT_PASS_TYPE:\n  bounded production implementation / validate one exact published BA mixed control; false terminates with no header, true composes exactly one BD-admitted header and stops at payload_start",
    "CURRENT_PASS:\n  R3.18BF — published R3.18BE mixed following-header differential\n\nCURRENT_PASS_TYPE:\n  read-only published-production differential / exact BE-versus-BC/BD branch, header identity, boundary and membership on the immutable 40-row lane; no following payload",
    "handbook current pass"
)
marker = "# CURRENT OVERRIDE — R3.18BE PRODUCTION / R3.18BF ACTIVE"
if marker in handbook:
    raise SystemExit("BE handbook override already exists")
handbook += f'''\n\n---\n\n{marker}\n\nFresh source/tests and the receipts below override older current-like wording above.\n\n```text\nR3_18BE_PRODUCTION_CLOSURE:\nOutcome A / published production\nproduction SHA/tree: {PROD_SHA} / {PROD_TREE}\nparent: {PROD_PARENT}\nlib/test blobs: {LIB_BLOB} / {TEST_BLOB}\nbuilder: {BUILDER_RUN}/{BUILDER_JOB} SUCCESS / head {BUILDER_HEAD}\nvalidation-only PR #{PR}: CLOSED UNMERGED / CI {PR_CI_RUN}/{PR_CI_JOB} SUCCESS\npublished-main CI: {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS\nclean scope: exactly lib.rs + r3_18be_post_ba_following_header.rs\nfrozen rows: 40 / false no-header=37 / true exact-header=3\nBD contexts: 3/3 / Boolean=2 / Float=1\nupstream AU false terminators excluded: 7\nfollowing payload / second-control: 0/0\npublication: force=false\n\nCURRENT_PASS: R3.18BF\nTYPE: read-only published-production differential\nAUTHORITY: BC {BC_HEAD} / artifact {BC_ARTIFACT}; BD contract sha256:{BD_CONTRACT_SHA256}\nREQUIRE: BE exact 40/40 / false=37 / true=3 / true headers=3/3 / BD contexts=3/3 / mismatch=0 / reselection=0 / payload-control=0/0\nHARD STOP: no following payload/second-control; no false-row header; no generalized cursor\n```\n'''
handbook_path.write_text(handbook, encoding="utf-8", newline="\n")


# Knowledge graph: current graph node, reading tail, and append-only closure/opening.
kg_path = Path("MIMIR_KNOWLEDGE_GRAPH.md")
kg = kg_path.read_text(encoding="utf-8")
kg = replace_once(
    kg,
    "R3.18BE bounded post-BA mixed-continuation following-header production / ACTIVE",
    "R3.18BE bounded post-BA mixed-continuation following-header production / PRODUCTION CLOSED\nR3.18BF published-R3.18BE mixed following-header differential / ACTIVE",
    "KG current graph"
)
old_tail = '''149. `docs/continuity/MIMIR_R3_18BD_EXECUTION_SPEC.md`\n150. `docs/continuity/MIMIR_R3_18BD_DECISION.md`\n151. `docs/continuity/MIMIR_R3_18BE_EXECUTION_SPEC.md`\n152. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n153. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n154. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n155. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n156. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n157. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n158. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
new_tail = '''149. `docs/continuity/MIMIR_R3_18BD_EXECUTION_SPEC.md`\n150. `docs/continuity/MIMIR_R3_18BD_DECISION.md`\n151. `docs/continuity/MIMIR_R3_18BE_EXECUTION_SPEC.md`\n152. `docs/continuity/MIMIR_R3_18BE_DECISION.md`\n153. `docs/continuity/MIMIR_R3_18BF_EXECUTION_SPEC.md`\n154. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n155. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n156. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n157. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n158. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n159. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n160. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
kg = replace_once(kg, old_tail, new_tail, "KG reading tail")
kg_marker = "### R3.18BE bounded post-BA mixed-continuation following-header production: PRODUCTION / CLOSED"
if kg_marker in kg:
    raise SystemExit("BE KG closure already exists")
kg += f'''\n\n{kg_marker}\n- production `{PROD_SHA}` / tree `{PROD_TREE}` / parent `{PROD_PARENT}`; exact clean scope two files.\n- builder `{BUILDER_RUN}/{BUILDER_JOB}`, exact-head PR CI `{PR_CI_RUN}/{PR_CI_JOB}`, published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS; PR #{PR} closed unmerged; force=false publication.\n- exact 40-row lane; false=37 no-header / true=3 exact header; BD contexts 3/3; Boolean=2 / Float=1; seven upstream AU false terminators excluded; payload/control 0/0.\n- next exact pass: R3.18BF read-only published BE differential; no following payload in BF.\n\n### R3.18BF published-R3.18BE mixed following-header differential: ACTIVE\n- immutable authority BC `{BC_HEAD}` / `{BC_RUN}/{BC_JOB}` / artifact `{BC_ARTIFACT}` / `{BC_DIGEST}` plus BD contract `sha256:{BD_CONTRACT_SHA256}`.\n- require published BE exact 40/40, false=37, true=3 exact headers, BD contexts 3/3, Boolean=2 / Float=1, mismatch/reselection 0/0, payload/control 0/0.\n- production mutation and following payload/second-control access are forbidden.\n'''
kg_path.write_text(kg, encoding="utf-8", newline="\n")


# Append-only progress ledger.
ledger_path = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
ledger = ledger_path.read_text(encoding="utf-8")
ledger_marker = f"## {DATE} — R3.18BE — Bounded post-BA mixed-continuation following-header production"
if ledger_marker in ledger:
    raise SystemExit("BE ledger entry already exists")
ledger += f'''\n\n---\n\n{ledger_marker}\nProduction base SHA: `{PROD_PARENT}`\nProduction commit SHA: `{PROD_SHA}` / tree `{PROD_TREE}`\nPass type: bounded production implementation\nOutcome: **A — ADMITTED / PUBLISHED**\n\nWhat changed:\n- Added one boundary-specific following-header composition after an exact valid published R3.18BA mixed control.\n- Preserves 37 false rows as successful no-header terminators with zero post-BA reads.\n- Composes exactly one R3.18BD-admitted header on only 3 true rows, stopping at `payload_start`; Boolean=2 / Float=1.\n- Clean scope is exactly `lib.rs` + `r3_18be_post_ba_following_header.rs`; no Cargo/docs/workflow/fixture/corpus/support mutation entered production.\n\nEvidence and validation:\n- BC authority `{BC_HEAD}` / `{BC_RUN}/{BC_JOB}` / artifact `{BC_ARTIFACT}` / `{BC_DIGEST}`.\n- BD contract `sha256:{BD_CONTRACT_SHA256}` / exact_tuple_only / 3 contexts / multiplicity 3.\n- Builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS.\n- Validation-only PR #{PR} closed unmerged; PR CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS.\n- Published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS.\n- Fresh-main ancestry, exact SHA/tree readback and force=false publication PASS.\n\nBoundaries opened:\n- Exactly one following header after a validated BA true control, under exact R3.18BD membership.\n\nBoundaries still closed:\n- Header on BA false rows, following payload, second later control, context outside BD, BA/BE access on seven upstream AU false terminators, generalized cursor and all actor/frame/semantic/runtime widening.\n\nNext exact pass:\n- `R3.18BF — published R3.18BE mixed following-header differential` on exactly the immutable forty-row BC/BD-backed authority lane.\n'''
ledger_path.write_text(ledger, encoding="utf-8", newline="\n")

print("R3_18BE_CONTINUITY_PATCH=PASS")
print("R3_18BF_OPENED=PASS")
