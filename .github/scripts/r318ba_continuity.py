from pathlib import Path
import json

PROD_SHA = "5d2bca711f528ab1bb607104379af503ff175697"
PROD_TREE = "6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a"
PROD_PARENT = "109bad258d43963fd5432317503f99a7e1b8aa1b"
LIB_BLOB = "fe232760e63c3c1b46711084c70049f456ef345b"
TEST_BLOB = "41ef1c2c087cc52bf2bcf0fa65c911a31a6ffc13"
BA_SPEC_BLOB = "3db94f3d559de1a7152a55fa08f7cb4b50d50d74"
BUILDER_HEAD = "ce5e27641cb0240e7440b93092be69a8fc5b7a11"
BUILDER_RUN = 33091339939
BUILDER_JOB = 98584661482
PR = 208
PR_CI_RUN = 33091594385
PR_CI_JOB = 98585555551
CANDIDATE_CI_RUN = 33091611038
CANDIDATE_CI_JOB = 98585614713
PUBLISHED_CI_RUN = 33092084628
PUBLISHED_CI_JOB = 98587299347
AX_HEAD = "465a3f2fc71e5eed6f00c16a04738031bef8d82c"
AX_RUN = 33068572230
AX_JOB = 98504703417
AX_ARTIFACT = 9644869549
AX_SIZE = 18070
AX_DIGEST = "sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9"
AZ_ARTIFACT = 9652520412
AZ_DIGEST = "sha256:558c709e242d74150755565d07c7968853abad0a1de6c5f49cd8f5920e7f9fc4"


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)

# Decision.
decision = f'''# MIMIR R3.18BA — Bounded Post-AY Mixed Following-Control Production Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `{PROD_SHA}` / `{PROD_TREE}`
**Parent:** `{PROD_PARENT}`

## Decision

R3.18BA closes Outcome A. Published production validates/recomputes one exact R3.18AY Int/32 payload authority, begins exactly at the validated AY `stop_bit`, consumes exactly one LSB-first `property_present` bit, accepts both R3.18AX-observed boolean classes and stops exactly one bit later.

The immutable forty-row lane is preserved without witness reselection: **false=37 / true=3**. All seven upstream R3.18AU false terminators remain outside BA because they do not possess a valid AY payload. No following stream ID, following header, following payload, second later control bit, generalized/repeated property cursor, or wider actor/frame/semantic/runtime capability is admitted.

## Exact authority

```text
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
production parent                      {PROD_PARENT}
lib / focused-test blobs               {LIB_BLOB} / {TEST_BLOB}
BA execution spec blob                 {BA_SPEC_BLOB}
clean helper head                      {BUILDER_HEAD}
builder                                {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
validation-only PR                     #{PR} CLOSED UNMERGED
PR exact-head CI                       {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
candidate push CI                      {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS
published-main CI                      {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
R3.18AX evidence head                  {AX_HEAD}
R3.18AX authority                      {AX_RUN}/{AX_JOB} SUCCESS
R3.18AX artifact                       {AX_ARTIFACT} / {AX_SIZE} / {AX_DIGEST}
```

The clean production commit is exactly one commit ahead of the prior canonical main and contains only `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs` (129 + 167 additions, no deletions). Temporary builder workflow/script material did not enter production.

## Admitted production behavior

```text
valid AY/BA rows                       40/40
upstream AU false terminators excluded 7/7
control false                          37
control true                           3
AY authority recomputed                40/40
control start                          AY stop on 40/40
control end / BA stop                  start + 1 on 40/40
repeatability                          PASS
post-stop poison isolation             PASS
wrong actor / unresolved lookup        PASS
wrong exact context / corrupt AY       PASS
source scope                           one AY recompute + one read_bit
next stream/header/payload/second      0/0/0/0
```

The fixed builder passed the focused BA plus prerequisite regression target 18/18, `cargo check -p mimir-replay`, and Clippy with `-D warnings`. The exact clean SHA then passed both validation-only PR CI and candidate push CI, was published with `force=false`, and the exact published-main SHA passed repository CI again.

A superseded helper attempt failed only on the public API arity Clippy lint after the focused semantics had passed; it is not authority and was not rerun. The admitted API instead removes the redundant AU argument and recomputes through the AU authority embedded in the supplied AY composition.

## Hard stop

The 37 false BA rows terminate at BA stop. The 3 true rows are only continuation candidates; BA does not inspect what follows. The seven upstream AU false terminators remain outside the AY/BA lane entirely. Following stream/header/payload, another control, generalized cursor, next actor/frame/lifecycle, raw state, events, replay slices, skills, counterfactuals, runtime and export remain closed.

## Next gate

R3.18BB is a separate read-only published-production differential. It must compare published R3.18BA against exactly the immutable forty-row R3.18AX authority, preserve false=37 / true=3 with mismatch and witness reselection at zero, prove AY prerequisite plus control start/value/end/stop identity, and prove adjacent consumption remains 0/0/0/0. Only after BB Outcome A may a later separate pass inspect one following header on exactly the three frozen true continuation rows.
'''
write("docs/continuity/MIMIR_R3_18BA_DECISION.md", decision)

# Next execution spec.
bb = f'''# MIMIR R3.18BB — Published R3.18BA Mixed Following-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BA `{PROD_SHA}` / `{PROD_TREE}`
**Production mutation:** forbidden
**Frozen control authority:** R3.18AX `{AX_HEAD}` / run `{AX_RUN}/{AX_JOB}` / artifact `{AX_ARTIFACT}` / `{AX_DIGEST}`
**Following stream/header/payload:** forbidden
**Second later control:** forbidden

## 1. Goal

Differentially validate published R3.18BA against exactly the immutable forty-row R3.18AX one-bit authority. For each frozen witness, reconstruct the exact valid R3.18AY prerequisite, invoke published BA once, and require exact control start, boolean value, end and final stop equality with AX plus an independent native LSB-first observation.

The immutable distribution is **false=37 / true=3**. Both classes are valid BA results. The 37 false rows terminate after BA. The 3 true rows are continuation candidates only; BB itself does not decode a following header.

## 2. Frozen authority

```text
BA production SHA/tree                {PROD_SHA} / {PROD_TREE}
BA parent                              {PROD_PARENT}
BA lib/test blobs                      {LIB_BLOB} / {TEST_BLOB}
BA execution spec blob                 {BA_SPEC_BLOB}
BA builder                             {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
BA validation PR                      #{PR} closed unmerged
BA PR CI                              {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
BA candidate push CI                  {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS
BA published-main CI                  {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
AX evidence head                      {AX_HEAD}
AX authority run/job                  {AX_RUN}/{AX_JOB} SUCCESS
AX artifact                           {AX_ARTIFACT} / {AX_SIZE} bytes
AX artifact digest                    {AX_DIGEST}
AX inner manifest                     15/15 PASS
AX frozen rows                        40
AX distribution                       false=37 / true=3
AX mismatch/reselection               0 / 0
AX adjacent consumption               0/0/0/0
```

Witness reselection is forbidden. Historical AP/AQ or true-only M/W/AG ratios are not authority for this boundary.

## 3. Exact differential lane

For every exact R3.18AX witness:

1. reconstruct the same exact valid published R3.18AY prerequisite;
2. call published R3.18BA exactly once;
3. require BA retained payload composition == reconstructed AY authority;
4. require BA `property_present_start_bit == AY.stop_bit == AX control_start`;
5. require BA boolean == frozen AX boolean == independent native LSB-first observation;
6. require BA `property_present_end_bit == stop_bit == AX control_end == start + 1`;
7. repeat and require exact deterministic equality;
8. poison bits beginning at BA stop and require the BA result unchanged;
9. stop without following stream/header/payload or second-control access.

Expected totals:

```text
frozen rows             40/40
published BA exact      40/40
AY prerequisite exact   40/40
false                    37
true                      3
mismatch                  0
witness reselection       0
adjacent consumption      0/0/0/0
```

## 4. Required negative controls

At minimum:
- all seven upstream AU false terminators remain outside AY/BA and reject before BA control success;
- wrong actor authority -> reject before BA success;
- unresolved lookup -> reject before BA success;
- wrong exact context -> reject;
- corrupt/mismatched AY prior -> reject;
- truncated prerequisite/carrier -> fail closed;
- repeat identical invocation -> exact equality 40/40;
- poison at exact BA stop -> returned BA result unchanged 40/40;
- source-scope guard -> one AY recomputation, one `cursor.read_bit()`, no stream/header/payload decoder and no loop/cursor widening;
- next stream/header/payload/second-control consumption remains 0/0/0/0.

Because both booleans are admitted, flipping a frozen control bit is not an API-malformed negative. If used as a differential mutation it is a frozen-value mismatch, not an expected parser rejection.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact BA SHA/tree/blob/CI receipts, exact AX authority and manifest receipt, forty frozen witness identities, per-row AY/BA/AX/native comparison, repeatability and negative controls, adjacent-consumption counters, production/Cargo/fixture/corpus/support mutation counters, same-head natural-CI receipt, privacy result and SHA-256 manifest.

## 6. Validation

Require frozen identity 40/40, published BA exact 40/40, AY prerequisite exact 40/40, false=37 / true=3, mismatch/reselection 0/0, repeatability and all negatives PASS, adjacent 0/0/0/0, focused BA/prerequisite tests PASS, Rust 1.85 fmt/check/test/clippy with warnings denied, repository verifier PASS, same exact evidence-head natural CI SUCCESS, production/Cargo/fixture/corpus/support mutation 0/0/0/0/0 and privacy PASS.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling. At most one validation-only PR may be used if a natural same-head CI cannot otherwise be obtained.

## 7. Continuation classification

- exact 37 false rows: terminators at BA stop;
- exact 3 true rows: continuation candidates only.

The three AX-observed true witness identities are frozen by the AX artifact. BB does not reinterpret or reselect them.

## 8. Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 9. Outcome gate

### Outcome A
Published R3.18BA is exact on all forty immutable AX witnesses with false=37 / true=3, mismatch/reselection 0/0, all negative/full validations PASS and adjacent consumption 0/0/0/0. Only then may a separate later pass inspect exactly one following header on the exact three true rows.

### Outcome B
A reproducible bounded mismatch or narrower supported subset is isolated. Admit only that subset and keep following-header evidence closed.

### Outcome C
Authority drift, witness reselection, rejection of an AX-admitted boolean class, upstream false-terminator widening, adjacent access, production mutation, privacy failure or generic chaining. Stop without widening.
'''
write("docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md", bb)

# Current state and handoff are compact canonical summaries, so replace completely.
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last read-only evidence/audit:** `R3.18AZ — Outcome A / published AY exact 40/40 / mismatch 0 / reselection 0 / artifact {AZ_ARTIFACT}`
**Last completed contract:** `R3.18AT — exact_tuple_only / 16 eight-field contexts / multiplicity 40 / 7 false terminators outside membership`
**Current exact pass:** `R3.18BB — published R3.18BA mixed following-control differential`

## Truthful boundary

R3.18BA is canonical production. Exactly forty valid R3.18AY payload rows may enter BA; seven upstream R3.18AU false terminators remain outside the lane. BA recomputes AY, begins at AY payload end, consumes exactly one R3.18AX-admitted LSB-first `property_present` bit, accepts both false and true, and stops one bit later. The frozen distribution is false=37 / true=3. Production consumes no following stream/header/payload or second later control bit.

```text
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
parent                                 {PROD_PARENT}
lib/test blobs                         {LIB_BLOB} / {TEST_BLOB}
builder                                {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
validation PR                          #{PR} CLOSED UNMERGED
PR CI                                  {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
candidate push CI                      {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS
published-main CI                      {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
valid BA rows                          40/40
upstream false terminators excluded    7/7
control distribution                   false=37 / true=3
adjacent stream/header/payload/second  0/0/0/0
```

## Current gate

R3.18BB is read-only. It must validate published BA against exactly the immutable R3.18AX forty-row authority with mismatch/reselection zero and no adjacent consumption. It may not decode a following header, including on the three true rows.

## Hard stop

No following stream/header/payload, second later control, generalized property cursor, actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
'''
write("docs/continuity/MIMIR_CURRENT_STATE.md", current)

handoff = f'''# MIMIR — Next Chat Handoff

Canonical production is **R3.18BA** at `{PROD_SHA}` / `{PROD_TREE}`, parent `{PROD_PARENT}`. The clean production commit changes only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs`.

R3.18BA validates/recomputes one exact R3.18AY payload, begins at AY `stop_bit`, consumes exactly one R3.18AX-admitted LSB-first `property_present` bit, accepts both observed classes (**false=37 / true=3**), and stops exactly one bit later. All seven upstream AU false terminators remain outside BA. Adjacent stream/header/payload/second-control consumption is 0/0/0/0.

Validation: builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; PR #{PR} closed unmerged with CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS; exact candidate push CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS; published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS; publication force=false.

The active pass is **R3.18BB published R3.18BA mixed following-control differential**. Use exactly the immutable R3.18AX forty-row artifact `{AX_ARTIFACT}` / `{AX_DIGEST}`. Require published BA and AY prerequisite exact 40/40, false=37 / true=3, mismatch/reselection 0/0, repeatability/negatives PASS and adjacent consumption 0/0/0/0. BB is read-only and must not decode a following header.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
'''
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)

# Boundary locks: replace only the current override before the historical body.
locks_path = Path("docs/continuity/MIMIR_BOUNDARY_LOCKS.md")
locks = locks_path.read_text(encoding="utf-8")
start = locks.find("# 0. Current override —")
end = locks.find("# 1. Status vocabulary")
if start < 0 or end < 0 or end <= start:
    raise SystemExit("boundary lock anchors missing")
override = f'''# 0. Current override — R3.18BA production closed / R3.18BB active differential

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BA
- `{PROD_SHA}` / `{PROD_TREE}` is canonical production, parent `{PROD_PARENT}`.
- exactly 40 valid AY rows enter BA; seven upstream AU false terminators remain outside.
- BA recomputes AY, consumes exactly one mixed AX-admitted control bit, accepts false=37 / true=3, and stops one bit later.
- adjacent stream/header/payload/second-control consumption remains 0/0/0/0.

## ACTIVE READ-ONLY DIFFERENTIAL — R3.18BB
- immutable authority is the AX forty-row lane / artifact `{AX_ARTIFACT}` / `{AX_DIGEST}`.
- compare published BA start/value/end/stop plus AY prerequisite exactly; mismatch/reselection must remain 0/0.
- 37 false rows terminate; 3 true rows are continuation candidates only.

## CLOSED
- following stream/header/payload during BB, including on the three true rows;
- second later property-control bit;
- BA/BB access on seven upstream AU false terminators;
- repeated/generalized property loop or generic cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

'''
locks_path.write_text(locks[:start] + override + locks[end:], encoding="utf-8", newline="\n")

# Machine continuity state.
state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-27"
state["last_production_code_sha"] = PROD_SHA
state["last_production_milestone"] = "R3.18BA"
state["last_production_milestone_name"] = "bounded post-AY mixed following-control production"
state["current_pass"] = "R3.18BB"
state["current_pass_kind"] = "read-only published-production differential / exact R3.18BA versus immutable R3.18AX mixed-control authority"
state["current_pass_goal"] = "Validate published R3.18BA on exactly 40 frozen AX rows: AY prerequisite and control start/value/end/stop exact 40/40, false=37, true=3, mismatch/reselection 0/0."
state["current_pass_stop_boundary"] = "No following stream/header/payload or second later control; no generalized cursor; seven upstream AU false terminators remain outside; no actor/frame/lifecycle/raw-state/event/skill/runtime widening."
state["r3_18ba"] = {
    "status": "production_closed",
    "sha": PROD_SHA,
    "tree": PROD_TREE,
    "parent": PROD_PARENT,
    "lib_blob": LIB_BLOB,
    "test_blob": TEST_BLOB,
    "rows": 40,
    "upstream_false_terminators_excluded": 7,
    "false": 37,
    "true": 3,
    "adjacent_consumption": "0/0/0/0",
    "builder_run": BUILDER_RUN,
    "builder_job": BUILDER_JOB,
    "validation_pr": PR,
    "pr_ci_run": PR_CI_RUN,
    "candidate_ci_run": CANDIDATE_CI_RUN,
    "published_main_ci_run": PUBLISHED_CI_RUN
}
state["r3_18bb"] = {
    "status": "active_read_only_differential",
    "frozen_rows": 40,
    "authority": "R3.18AX",
    "artifact": AX_ARTIFACT,
    "artifact_digest": AX_DIGEST,
    "expected_false": 37,
    "expected_true": 3,
    "following_header_open": False
}
closed = state.setdefault("closed_now", [])
for item in [
    "following stream/header/payload during R3.18BB",
    "second later property-control bit after R3.18BA/R3.18BB",
    "following-header evidence before R3.18BB Outcome A"
]:
    if item not in closed:
        closed.append(item)
reads = state.setdefault("next_files_to_read", [])
ba_spec = "docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md"
ba_dec = "docs/continuity/MIMIR_R3_18BA_DECISION.md"
bb_spec = "docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md"
if ba_spec not in reads:
    raise SystemExit("BA spec missing from next_files_to_read")
for item in (ba_dec, bb_spec):
    while item in reads:
        reads.remove(item)
pos = reads.index(ba_spec) + 1
reads[pos:pos] = [ba_dec, bb_spec]
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

# Root handbook: update only the canonical state block and append one current override/closure.
handbook_path = Path("MIMIR_CONTINUE_HERE.md")
handbook = handbook_path.read_text(encoding="utf-8")
handbook = replace_once(
    handbook,
    "LAST_PRODUCTION_CODE_SHA:\n  2558cc0559422a3e6695e1501f20d96d83b23e6d\n\nLAST_PRODUCTION_MILESTONE:\n  R3.18AY — bounded post-AU one-following-payload production",
    f"LAST_PRODUCTION_CODE_SHA:\n  {PROD_SHA}\n\nLAST_PRODUCTION_MILESTONE:\n  R3.18BA — bounded post-AY mixed following-control production",
    "handbook production pointer"
)
handbook = replace_once(
    handbook,
    "CURRENT_PASS:\n  R3.18BA — bounded post-AY mixed following-control production\n\nCURRENT_PASS_TYPE:\n  bounded production implementation / validate-recompute one exact R3.18AY payload, consume exactly one AX-admitted mixed property_present bit (false=37 true=3), stop one bit later, and consume no following stream/header/payload/second-control bits",
    "CURRENT_PASS:\n  R3.18BB — published R3.18BA mixed following-control differential\n\nCURRENT_PASS_TYPE:\n  read-only published-production differential / exact BA-versus-AX control start-value-end-stop identity on the immutable 40-row lane; false=37 true=3; no following header",
    "handbook current pass"
)
marker = "# CURRENT OVERRIDE — R3.18BA PRODUCTION / R3.18BB ACTIVE"
if marker not in handbook:
    handbook += f'''\n\n---\n\n# CURRENT OVERRIDE — R3.18BA PRODUCTION / R3.18BB ACTIVE\n\nFresh source/tests and the receipts below override older current-like wording above.\n\n```text\nR3_18BA_PRODUCTION_CLOSURE:\nOutcome A / published production\nproduction SHA/tree: {PROD_SHA} / {PROD_TREE}\nparent: {PROD_PARENT}\nlib/test blobs: {LIB_BLOB} / {TEST_BLOB}\nbuilder: {BUILDER_RUN}/{BUILDER_JOB} SUCCESS\nvalidation-only PR #{PR}: CLOSED UNMERGED / CI {PR_CI_RUN}/{PR_CI_JOB} SUCCESS\ncandidate push CI: {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS\npublished-main CI: {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS\nclean scope: exactly lib.rs + r3_18ba_post_ay_payload_control.rs\nfrozen rows: 40 / upstream false terminators excluded 7\ncontrol distribution: false=37 / true=3\nadjacent stream/header/payload/second-control: 0/0/0/0\npublication: force=false\n\nCURRENT_PASS: R3.18BB\nTYPE: read-only published-production differential\nAUTHORITY: R3.18AX {AX_HEAD} / artifact {AX_ARTIFACT} / {AX_DIGEST}\nREQUIRE: BA exact 40/40 / AY prerequisite exact 40/40 / false=37 / true=3 / mismatch=0 / reselection=0 / adjacent=0/0/0/0\nHARD STOP: no following header/payload/stream/second-control; three true rows are continuation candidates only\n```\n'''
handbook_path.write_text(handbook, encoding="utf-8", newline="\n")

# Knowledge graph: current graph node and mandatory reading tail.
kg_path = Path("MIMIR_KNOWLEDGE_GRAPH.md")
kg = kg_path.read_text(encoding="utf-8")
kg = replace_once(
    kg,
    "R3.18BA bounded post-AY mixed following-control production / ACTIVE",
    "R3.18BA bounded post-AY mixed following-control production / PRODUCTION CLOSED\nR3.18BB published-R3.18BA mixed following-control differential / ACTIVE",
    "KG current graph"
)
old_tail = '''143. `docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md`\n144. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n145. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n146. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n147. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n148. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n149. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n150. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
new_tail = '''143. `docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md`\n144. `docs/continuity/MIMIR_R3_18BA_DECISION.md`\n145. `docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md`\n146. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n147. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n148. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n149. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n150. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n151. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n152. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
kg = replace_once(kg, old_tail, new_tail, "KG reading tail")
kg_marker = "### R3.18BA bounded post-AY mixed following-control production: PRODUCTION / CLOSED"
if kg_marker not in kg:
    kg += f'''\n\n{kg_marker}\n- production `{PROD_SHA}` / tree `{PROD_TREE}` / parent `{PROD_PARENT}`; exact clean scope two files.\n- builder `{BUILDER_RUN}/{BUILDER_JOB}`, PR CI `{PR_CI_RUN}/{PR_CI_JOB}`, candidate push CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}`, published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS; PR #{PR} closed unmerged; force=false publication.\n- exact 40-row AY/AX lane; false=37 / true=3; seven upstream false terminators excluded; adjacent consumption 0/0/0/0.\n- next exact pass: R3.18BB read-only published BA differential; no following header in BB.\n\n### R3.18BB published-R3.18BA mixed following-control differential: ACTIVE\n- immutable authority R3.18AX `{AX_HEAD}` / `{AX_RUN}/{AX_JOB}` / artifact `{AX_ARTIFACT}` / `{AX_DIGEST}`.\n- require published BA exact 40/40, AY prerequisite exact 40/40, false=37 / true=3, mismatch/reselection 0/0, adjacent 0/0/0/0.\n- production mutation and following stream/header/payload/second-control access are forbidden.\n'''
kg_path.write_text(kg, encoding="utf-8", newline="\n")

# Append-only progress ledger.
ledger_path = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
ledger = ledger_path.read_text(encoding="utf-8")
ledger_marker = "## 2026-08-27 — R3.18BA — Bounded post-AY mixed following-control production"
if ledger_marker in ledger:
    raise SystemExit("BA ledger entry already exists")
ledger += f'''\n\n---\n\n{ledger_marker}\nProduction base SHA: `{PROD_PARENT}`\nProduction commit SHA: `{PROD_SHA}` / tree `{PROD_TREE}`\nPass type: bounded production implementation\nOutcome: **A — ADMITTED / PUBLISHED**\n\nWhat changed:\n- Added one boundary-specific production composition after an exact valid R3.18AY payload.\n- Recomputes AY, consumes exactly one AX-admitted LSB-first `property_present` bit, accepts false and true, and stops one bit later.\n- Clean scope is exactly `lib.rs` + `r3_18ba_post_ay_payload_control.rs`; no Cargo/docs/workflow/fixture/corpus/support mutation entered production.\n\nEvidence and validation:\n- R3.18AX authority `{AX_HEAD}` / `{AX_RUN}/{AX_JOB}` / artifact `{AX_ARTIFACT}` / `{AX_DIGEST}`; 40 rows; false=37 / true=3; mismatch/reselection 0/0; adjacent 0/0/0/0.\n- Builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; focused BA/prerequisite target 18/18 PASS; check + Clippy `-D warnings` PASS.\n- Validation-only PR #{PR} closed unmerged; PR CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS.\n- Exact candidate push CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS.\n- Published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS.\n- Fresh-main ancestry and force=false publication PASS.\n\nBoundaries opened:\n- Exactly one mixed false/true control bit after validated AY payload.\n\nBoundaries still closed:\n- Following stream/header/payload, second later control, BA access on seven upstream false terminators, generalized cursor and all actor/frame/semantic/runtime widening.\n\nNext exact pass:\n- `R3.18BB — published R3.18BA mixed following-control differential` on exactly the immutable forty-row AX authority.\n'''
ledger_path.write_text(ledger, encoding="utf-8", newline="\n")

expected = {
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_BOUNDARY_LOCKS.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",
    "docs/continuity/MIMIR_PROGRESS_LEDGER.md",
    "docs/continuity/MIMIR_R3_18BA_DECISION.md",
    "docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md"
}
# This final scope check is intentionally performed by the workflow after the script runs.
print("R3_18BA_CONTINUITY_PATCH=PASS")
print("R3_18BB_OPENED=PASS")
