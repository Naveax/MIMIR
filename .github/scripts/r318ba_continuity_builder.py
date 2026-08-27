from pathlib import Path
import json
import re
import shutil
import subprocess
import tempfile

MAIN_SHA = "5d2bca711f528ab1bb607104379af503ff175697"
MAIN_TREE = "6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a"
PARENT_SHA = "109bad258d43963fd5432317503f99a7e1b8aa1b"
CANDIDATE_BRANCH = "candidate/r318ba-admit-open-r318bb"

BUILDER_FIXED_SHA = "ce5e27641cb0240e7440b93092be69a8fc5b7a11"
BUILDER_RUN = "33091339939"
BUILDER_JOB = "98584661482"
BUILDER_CI = "33091339935"
FIRST_FAILED_RUN = "33090827273"
VALIDATION_PR = "208"
VALIDATION_PR_RUN = "33091594385"
VALIDATION_PR_JOB = "98585555551"
VALIDATION_BRANCH_RUN = "33091611038"
PUBLISHED_MAIN_RUN = "33092084628"
PUBLISHED_MAIN_JOB = "98587299347"

AX_HEAD = "465a3f2fc71e5eed6f00c16a04738031bef8d82c"
AX_TREE = "b164a8566c6ac57ddee1aed0a7edbf9f44250488"
AX_RUN = "33068572230"
AX_JOB = "98504703417"
AX_CI = "33068572200"
AX_CI_JOB = "98504703614"
AX_ARTIFACT = "9644869549"
AX_DIGEST = "32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9"

AZ_ARTIFACT = "9652520412"

EXPECTED = sorted([
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "docs/continuity/MIMIR_BOUNDARY_LOCKS.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",
    "docs/continuity/MIMIR_PROGRESS_LEDGER.md",
    "docs/continuity/MIMIR_R3_18BA_DECISION.md",
    "docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md",
])


def run(*args: str, capture: bool = False) -> str:
    p = subprocess.run(args, check=True, text=True, capture_output=capture)
    return p.stdout.strip() if capture else ""


run("git", "fetch", "origin", "main")
assert run("git", "rev-parse", "origin/main", capture=True) == MAIN_SHA
assert run("git", "rev-parse", f"{MAIN_SHA}^", capture=True) == PARENT_SHA
assert run("git", "show", "-s", "--format=%T", MAIN_SHA, capture=True) == MAIN_TREE

p = Path("MIMIR_CONTINUE_HERE.md")
text = p.read_text(encoding="utf-8")
text, n = re.subn(r"LAST_PRODUCTION_CODE_SHA:\n  [0-9a-f]{40}", f"LAST_PRODUCTION_CODE_SHA:\n  {MAIN_SHA}", text, count=1)
assert n == 1
text, n = re.subn(r"LAST_PRODUCTION_MILESTONE:\n  R3\.18AY — bounded post-AU one-following-payload production", "LAST_PRODUCTION_MILESTONE:\n  R3.18BA — bounded post-AY mixed following-control production", text, count=1)
assert n == 1
text, n = re.subn(r"CURRENT_PASS:\n  R3\.18BA — bounded post-AY mixed following-control production", "CURRENT_PASS:\n  R3.18BB — published-R3.18BA mixed following-control differential", text, count=1)
assert n == 1
text, n = re.subn(r"CURRENT_PASS_TYPE:\n  bounded production implementation / validate-recompute one exact R3\.18AY payload, consume exactly one AX-admitted mixed property_present bit \(false=37 true=3\), stop one bit later, and consume no following stream/header/payload/second-control bits", "CURRENT_PASS_TYPE:\n  read-only published-production differential / replay exact immutable AX forty-row authority against published R3.18BA, require false=37 true=3 and exact start/value/end/stop with mismatch/reselection 0/0, and consume no following stream/header/payload/second-control bits", text, count=1)
assert n == 1
p.write_text(text, encoding="utf-8", newline="\n")

p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
text = p.read_text(encoding="utf-8")
old = "R3.18BA bounded post-AY mixed following-control production / ACTIVE"
assert text.count(old) == 1
text = text.replace(old, "R3.18BA bounded post-AY mixed following-control production / PRODUCTION CLOSED\nR3.18BB published-R3.18BA mixed following-control differential / ACTIVE", 1)
p.write_text(text, encoding="utf-8", newline="\n")

p = Path("docs/continuity/MIMIR_BOUNDARY_LOCKS.md")
text = p.read_text(encoding="utf-8")
begin = text.index("# 0. Current override")
end = text.index("# 1. Status vocabulary", begin)
override = f'''# 0. Current override — R3.18BA production closed / R3.18BB active differential

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BA
- `{MAIN_SHA}` / `{MAIN_TREE}` is canonical production.
- one exact R3.18AY payload authority is recomputed and validated;
- exactly one following LSB-first `property_present` bit is consumed at AY stop;
- both frozen R3.18AX classes are admitted: false=37 / true=3;
- the boundary stops exactly one bit later;
- all seven upstream AU false terminators remain outside BA.

## CLOSED PRODUCTION VALIDATION — R3.18BA Outcome A
- fixed builder `{BUILDER_FIXED_SHA}` / `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS;
- clean candidate `{MAIN_SHA}` / `{MAIN_TREE}`;
- validation-only PR #{VALIDATION_PR} exact-head CI `{VALIDATION_PR_RUN}/{VALIDATION_PR_JOB}` SUCCESS and closed unmerged;
- published-main CI `{PUBLISHED_MAIN_RUN}/{PUBLISHED_MAIN_JOB}` SUCCESS;
- production scope exactly `lib.rs` plus `r3_18ba_post_ay_payload_control.rs`.

## ACTIVE READ-ONLY DIFFERENTIAL — R3.18BB
- replay exactly the immutable forty R3.18AX control witnesses against published BA;
- require published BA start/value/end/stop exact 40/40;
- require false=37 / true=3, mismatch=0 and witness reselection=0;
- false rows are terminators; only the exact three true rows may become candidates for a later separate header-evidence pass;
- BB itself decodes no following stream/header/payload and no second later control.

## CLOSED
- following stream/header/payload consumption during R3.18BB;
- header production/evidence before R3.18BB closes;
- second later property-control bit;
- BA/BB access on the seven upstream AU false terminators;
- repeated/generalized property loop or generic cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

'''
text = text[:begin] + override + text[end:]
p.write_text(text, encoding="utf-8", newline="\n")

p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(p.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-27"
state["last_production_code_sha"] = MAIN_SHA
state["last_production_milestone"] = "R3.18BA"
state["last_production_milestone_name"] = "bounded post-AY mixed following-control production"
state["last_completed_read_only_audit"] = "R3.18AZ"
state["current_pass"] = "R3.18BB"
state["current_pass_kind"] = "read-only published-production differential / exact R3.18BA mixed following-control validation"
state["current_pass_goal"] = "Replay exactly the immutable R3.18AX forty-row control authority against published R3.18BA; require exact start/value/end/stop 40/40, false=37 true=3, mismatch 0, witness reselection 0."
state["current_pass_stop_boundary"] = "No following stream/header/payload or second later control; no generalized cursor; no access on seven upstream AU false terminators; no actor/frame/lifecycle/raw-state/event/skill/runtime widening."
state["r3_18ba"] = {
    "outcome": "A",
    "status": "production_closed",
    "production_sha": MAIN_SHA,
    "production_tree": MAIN_TREE,
    "parent_sha": PARENT_SHA,
    "builder_fixed_sha": BUILDER_FIXED_SHA,
    "builder_run": int(BUILDER_RUN),
    "builder_job": int(BUILDER_JOB),
    "builder_helper_ci": int(BUILDER_CI),
    "validation_pr": int(VALIDATION_PR),
    "validation_pr_run": int(VALIDATION_PR_RUN),
    "validation_pr_job": int(VALIDATION_PR_JOB),
    "validation_branch_run": int(VALIDATION_BRANCH_RUN),
    "published_main_run": int(PUBLISHED_MAIN_RUN),
    "published_main_job": int(PUBLISHED_MAIN_JOB),
    "frozen_rows": 40,
    "upstream_false_terminators": 7,
    "false": 37,
    "true": 3,
    "next_stream_header_payload_second_control_consumption": [0, 0, 0, 0],
    "clean_production_files": ["crates/mimir-replay/src/lib.rs", "crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs"],
}
closed = state.setdefault("closed_now", [])
for item in [
    "following stream/header/payload during R3.18BB published-production differential",
    "second later property-control bit after published R3.18BA",
    "following-header evidence/production before R3.18BB differential closure",
]:
    if item not in closed:
        closed.append(item)
p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{MAIN_SHA}`
**Production tree:** `{MAIN_TREE}`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last read-only evidence/audit:** `R3.18AZ — Outcome A / published AY exact 40/40 / mismatch 0 / reselection 0 / artifact {AZ_ARTIFACT}`
**Current exact pass:** `R3.18BB — published-R3.18BA mixed following-control differential`

## Truthful boundary

R3.18BA is now canonical production. It validates/recomputes one exact R3.18AY Int/32 payload composition, starts exactly at the validated AY stop, consumes exactly one LSB-first following `property_present` bit, accepts both immutable R3.18AX-observed classes, and stops one bit later. The exact frozen distribution is false=37 / true=3 on forty valid payload rows; all seven upstream AU false terminators remain outside the BA lane.

```text
production SHA/tree                    {MAIN_SHA} / {MAIN_TREE}
production parent                      {PARENT_SHA}
fixed builder                          {BUILDER_FIXED_SHA}
builder run/job                        {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
builder helper-head CI                 {BUILDER_CI} SUCCESS
validation-only PR                     #{VALIDATION_PR} closed unmerged
exact-candidate PR CI                  {VALIDATION_PR_RUN}/{VALIDATION_PR_JOB} SUCCESS
validation-branch CI                   {VALIDATION_BRANCH_RUN} SUCCESS
published-main CI                      {PUBLISHED_MAIN_RUN}/{PUBLISHED_MAIN_JOB} SUCCESS
frozen BA rows                         40/40
upstream AU false terminators          7/7 excluded
BA false / true                        37 / 3
AY recomputation per BA call           exactly 1
new control reads per BA call          exactly 1
next stream/header/payload/second      0/0/0/0
production files                       exactly 2
```

The superseded first builder run `{FIRST_FAILED_RUN}` is not authority: focused behavior passed, but Clippy rejected the redundant eight-argument API (`too_many_arguments 8/7`). It was not rerun. The corrected API removes the redundant AU authority parameter and derives that authority through `ay_prior.header_composition`.

## Current gate

R3.18BB is read-only. It must replay exactly the immutable forty R3.18AX control witnesses against published R3.18BA and require exact start/value/end/stop equality, false=37 / true=3, mismatch 0 and witness reselection 0. The 37 false rows are terminators. Only the exact three true rows may be candidates for a later, separate following-header evidence pass.

R3.18AX already carries the exact bit-level `TRUNCATION_BEFORE_CONTROL=PASS 40/40` authority. All forty control starts are non-byte-aligned, so the production `&[u8]` API must not pretend it can represent a partial-byte EOF that preserves AY while deleting only the following bit. BA's carrier truncation negative remains fail-closed; the exact-before-bit claim remains AX evidence authority.

## Hard stop

R3.18BB decodes no following stream ID, header or payload and no second later control. No generic/repeated property cursor, next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is open.
'''
Path("docs/continuity/MIMIR_CURRENT_STATE.md").write_text(current, encoding="utf-8", newline="\n")

handoff = f'''# MIMIR — Next Chat Handoff

Canonical production is now **R3.18BA** at `{MAIN_SHA}` / `{MAIN_TREE}`. R3.18BA closed **Outcome A / PRODUCTION**: fixed builder `{BUILDER_FIXED_SHA}`, builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS, validation-only PR #{VALIDATION_PR} exact-head CI `{VALIDATION_PR_RUN}/{VALIDATION_PR_JOB}` SUCCESS and closed unmerged, and published-main CI `{PUBLISHED_MAIN_RUN}/{PUBLISHED_MAIN_JOB}` SUCCESS.

The production boundary recomputes one exact R3.18AY payload, consumes exactly one following `property_present` bit and stops one bit later. Frozen immutable R3.18AX semantics are false=37 / true=3 across forty valid rows; seven upstream AU false terminators remain outside. Adjacent stream/header/payload/second-control consumption remains 0/0/0/0.

The active pass is **R3.18BB — published-R3.18BA mixed following-control differential**. It is read-only: replay exactly the immutable forty AX witnesses, require published BA exact 40/40 for start/value/end/stop, false=37 / true=3, mismatch 0, witness reselection 0, deterministic repeatability and all bounded negatives. The 37 false rows terminate. Only the exact three true rows may become candidates for a later separate header-evidence pass; BB itself consumes no header or payload.

R3.18AX is the exact bit-level truncation authority (`TRUNCATION_BEFORE_CONTROL=PASS 40/40`). The BA carrier API is byte-slice based and all forty frozen control starts are non-byte-aligned, so do not widen BA with a bit-length transport parameter merely to simulate a partial-byte EOF.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
'''
Path("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md").write_text(handoff, encoding="utf-8", newline="\n")

decision = f'''# MIMIR R3.18BA — Bounded Post-AY Mixed Following-Control Production Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / PRODUCTION**
**Canonical production:** `{MAIN_SHA}` / `{MAIN_TREE}`
**Parent:** `{PARENT_SHA}`

## Decision

R3.18BA publishes exactly one boundary-specific mixed following-control result after one validated R3.18AY payload. The implementation recomputes and requires exact equality of the supplied AY authority, initializes the private LSB-first cursor at the validated AY stop, consumes exactly one `property_present` bit, accepts both immutable R3.18AX-observed boolean classes, and stops exactly one bit later.

On the exact frozen forty-row lane the distribution is false=37 / true=3. All seven upstream AU false terminators remain outside BA because no valid AY payload exists for them. No following stream ID, header, payload or second later control is consumed.

## Exact authority

```text
canonical parent                       {PARENT_SHA}
production SHA/tree                    {MAIN_SHA} / {MAIN_TREE}
fixed helper                           {BUILDER_FIXED_SHA}
builder run/job                        {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
builder helper-head CI                 {BUILDER_CI} SUCCESS
validation-only PR                     #{VALIDATION_PR} CLOSED / UNMERGED
exact-candidate PR CI                  {VALIDATION_PR_RUN}/{VALIDATION_PR_JOB} SUCCESS
validation-branch CI                   {VALIDATION_BRANCH_RUN} SUCCESS
published-main CI                      {PUBLISHED_MAIN_RUN}/{PUBLISHED_MAIN_JOB} SUCCESS
R3.18AX evidence head/tree             {AX_HEAD} / {AX_TREE}
R3.18AX run/job                        {AX_RUN}/{AX_JOB} SUCCESS
R3.18AX same-head CI                   {AX_CI}/{AX_CI_JOB} SUCCESS
R3.18AX artifact                       {AX_ARTIFACT} / sha256:{AX_DIGEST}
```

## Frozen result

```text
valid AY/BA rows                       40/40
upstream AU false terminators          7/7 excluded
BA false                               37
BA true                                3
AY recomputation                       exactly 1 per BA call
new LSB-first control read             exactly 1 per BA call
repeatability                          PASS
post-stop poison isolation             PASS
wrong actor / lookup / context         PASS
corrupt AY authority                   PASS
next stream/header/payload/second      0/0/0/0
production source scope                exactly 2 files
```

The focused BA plus directly affected prerequisite regression target passed 18/18 under Rust 1.85. `cargo check -p mimir-replay` and `cargo clippy -p mimir-replay --all-targets -- -D warnings` passed on the fixed builder. The repository's normal exact-candidate and published-main verifiers also passed.

## Superseded scaffolding

The first builder run `{FIRST_FAILED_RUN}` is historical non-authority. Its focused behavior tests passed, but Clippy rejected the original eight-argument BA API as `too_many_arguments (8/7)`. That run was not rerun. The correction removed redundant `au_prior` authority from the public boundary-specific API and recomputes AU through `ay_prior.header_composition`; the fixed helper and all later validation receipts above are authoritative.

A separate `builder/r318ba-production-v2` branch carried temporary helper files and is not clean production authority. The admitted production commit is the exact two-file clean candidate `{MAIN_SHA}`.

## Truncation precision

R3.18AX's immutable evidence receipt already proves exact bit-level `TRUNCATION_BEFORE_CONTROL=PASS 40/40`. All forty frozen BA control starts are non-byte-aligned. Therefore the production `&[u8]` carrier cannot express an EOF that preserves every AY payload bit while removing only the immediately following control bit. BA correctly remains a byte-slice API rather than widening with a new bit-length transport parameter solely for a test fixture. Carrier truncation remains fail-closed; exact-before-bit truncation remains AX evidence authority.

## Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no BA access on seven upstream false terminators, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18BB is a separate read-only published-production differential. It must replay exactly the immutable forty R3.18AX witnesses against published R3.18BA, require exact start/value/end/stop 40/40, preserve false=37 / true=3 with mismatch/reselection 0/0, and consume nothing adjacent. The 37 false rows are terminators. Only the exact three true rows may be considered by a later separate following-header evidence pass.
'''
Path("docs/continuity/MIMIR_R3_18BA_DECISION.md").write_text(decision, encoding="utf-8", newline="\n")

bb = f'''# MIMIR R3.18BB — Published R3.18BA Mixed Following-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BA `{MAIN_SHA}` / `{MAIN_TREE}`
**Frozen control authority:** R3.18AX `{AX_HEAD}` / artifact `{AX_ARTIFACT}` / `sha256:{AX_DIGEST}`
**Production mutation:** forbidden
**Following stream/header/payload:** forbidden
**Second later control:** forbidden

## 1. Goal

Validate published R3.18BA against exactly the immutable forty R3.18AX witnesses without reselection. Reconstruct the published prerequisites, call published BA once per frozen row, and require exact equality with the frozen AX control start, boolean value and one-bit end boundary.

The immutable distribution is **false=37 / true=3**. Both classes must be successful BA results. False rows terminate at BA stop. True rows are only continuation candidates for a later separate pass; BB itself does not decode their following header.

## 2. Exact lane

For every one of the exact forty AX witnesses:

1. reconstruct the exact valid published R3.18AY prerequisite;
2. call published R3.18BA;
3. require BA control start == AX frozen control start == AY stop;
4. require BA boolean == AX frozen boolean;
5. require BA end/stop == AX frozen end == start + 1;
6. repeat and require exact identical result;
7. poison bits beginning at BA stop and require the returned BA result unchanged;
8. stop.

Expected totals:

```text
rows                 40/40
false                37
true                 3
mismatch             0
witness reselection  0
```

The seven upstream AU false terminators remain outside the BB lane and must never reach a BA control success.

## 3. Required negatives

At minimum:
- corrupt/mismatched AY prior -> reject before BA success;
- wrong actor authority -> reject;
- unresolved lookup -> reject;
- wrong exact version context -> reject;
- upstream AU false terminator -> no AY/BA success;
- repeat identical invocation -> exact equality;
- poison bits beginning at BA stop -> result unchanged;
- source-scope guard -> exactly one AY recomputation and one control read, with no generic loop/header/payload decode;
- next stream/header/payload/second-control consumption remains 0/0/0/0.

Exact bit-level truncation immediately before the control is inherited from immutable R3.18AX evidence (`TRUNCATION_BEFORE_CONTROL=PASS 40/40`). All forty frozen control starts are non-byte-aligned, so BB must not fabricate a partial-byte EOF claim through the byte-slice production API. Carrier truncation may be tested only for fail-closed behavior actually representable by `&[u8]`.

## 4. Validation

Require:
- exact forty frozen witness identities;
- published BA versus frozen AX start/value/end/stop exact 40/40;
- false=37 / true=3;
- mismatch 0;
- witness reselection 0;
- repeatability PASS 40/40;
- post-stop poison isolation PASS 40/40;
- all authority/context/lookup negatives PASS;
- adjacent stream/header/payload/second-control consumption 0/0/0/0;
- focused BA tests PASS;
- full mimir-replay/workspace fmt/check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy scan PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse an equivalent exact run if present. Rerun is never polling.

## 5. Continuation classification

The frozen BA boolean controls only the next evidence candidate set:
- exact 37 false rows are terminators and must stop at BA;
- exact 3 true rows are candidates for a later separate one-header evidence pass.

R3.18BB itself authorizes no following header, payload or second control.

## 6. Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 7. Outcome gate

### Outcome A

Published R3.18BA is exact on all forty immutable AX witnesses with false=37 / true=3, mismatch 0, witness reselection 0, all negatives/full validation PASS and adjacent consumption 0/0/0/0. A later separate read-only pass may investigate exactly one following header on only the three true rows.

### Outcome B

A bounded mismatch or narrower supported subset is isolated. Admit only supported facts and keep following-header evidence closed.

### Outcome C

Authority/witness drift, published mismatch, rejection of an AX-admitted boolean class, adjacent access, production mutation, privacy failure or generic chaining. Stop without widening.
'''
Path("docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md").write_text(bb, encoding="utf-8", newline="\n")

p = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
text = p.read_text(encoding="utf-8").rstrip() + "\n"
assert "## 2026-08-27 — R3.18BA — Bounded post-AY mixed following-control production" not in text
ledger = f'''\n---\n\n## 2026-08-27 — R3.18BA — Bounded post-AY mixed following-control production\n\nProduction base SHA: `{PARENT_SHA}`\nProduction commit SHA: `{MAIN_SHA}`\nProduction tree: `{MAIN_TREE}`\nPass type: bounded production implementation + clean reconstruction + validation-only PR + force-free publication\nOutcome: **A — ADMITTED / PRODUCTION**\n\nWhat changed:\n- added one boundary-specific post-AY mixed following-control result/API;\n- recomputes exact R3.18AY authority, consumes exactly one LSB-first `property_present` bit and stops one bit later;\n- accepts both immutable AX classes false=37 / true=3;\n- keeps all seven upstream AU false terminators outside BA;\n- production scope is exactly two files.\n\nValidation:\n- fixed helper `{BUILDER_FIXED_SHA}` / builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS;\n- helper-head CI `{BUILDER_CI}` SUCCESS;\n- focused BA + affected prerequisite regressions 18/18 PASS;\n- cargo check and Clippy `-D warnings` PASS;\n- validation-only PR #{VALIDATION_PR} closed unmerged; exact-head CI `{VALIDATION_PR_RUN}/{VALIDATION_PR_JOB}` SUCCESS;\n- validation branch CI `{VALIDATION_BRANCH_RUN}` SUCCESS;\n- published-main CI `{PUBLISHED_MAIN_RUN}/{PUBLISHED_MAIN_JOB}` SUCCESS;\n- force=false publication and exact SHA/tree readback PASS.\n\nEvidence:\n- immutable AX authority `{AX_HEAD}` / `{AX_RUN}/{AX_JOB}` SUCCESS / artifact `{AX_ARTIFACT}` / `sha256:{AX_DIGEST}`;\n- frozen rows 40/40; false=37 / true=3; upstream false terminators 7/7 excluded;\n- one AY recomputation and one new control read per successful BA call;\n- adjacent stream/header/payload/second-control consumption 0/0/0/0.\n\nSuperseded scaffolding:\n- first builder run `{FIRST_FAILED_RUN}` was not rerun; behavior tests passed but Clippy rejected an 8-argument API;\n- corrected API removed redundant AU authority and all admitted receipts are on the fixed helper/candidate above.\n\nBoundaries opened:\n- published production now includes exactly one mixed following property-control bit after valid AY payload.\n\nBoundaries still closed:\n- following stream/header/payload, second later control, generalized cursor/loop, upstream false-terminator BA access and all wider semantic/runtime layers.\n\nNext exact pass:\n- `R3.18BB — published-R3.18BA mixed following-control differential` on exactly the immutable forty AX witnesses.\n'''
p.write_text(text + ledger, encoding="utf-8", newline="\n")

json.loads(Path("docs/continuity/MIMIR_CONTINUITY_STATE.json").read_text(encoding="utf-8"))
assert "R3.18BB published-R3.18BA mixed following-control differential / ACTIVE" in Path("MIMIR_KNOWLEDGE_GRAPH.md").read_text(encoding="utf-8")
assert f"**Canonical production SHA:** `{MAIN_SHA}`" in Path("docs/continuity/MIMIR_CURRENT_STATE.md").read_text(encoding="utf-8")
assert "R3.18BB" in Path("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md").read_text(encoding="utf-8")
run("git", "diff", "--check")

tmp = Path(tempfile.mkdtemp(prefix="r318ba-continuity-"))
for rel in EXPECTED:
    src = Path(rel)
    assert src.exists(), rel
    dst = tmp / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

run("git", "reset", "--hard", MAIN_SHA)
for rel in EXPECTED:
    src = tmp / rel
    dst = Path(rel)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

run("git", "add", *EXPECTED)
changed = sorted(run("git", "diff", "--cached", "--name-only", capture=True).splitlines())
assert changed == EXPECTED, (changed, EXPECTED)
run("git", "diff", "--cached", "--check")
run("pwsh", "-NoProfile", "-File", "scripts/verify_mimir_knowledge_archive.ps1")

run("git", "config", "user.name", "Naveax")
run("git", "config", "user.email", "79841922+Naveax@users.noreply.github.com")
run("git", "commit", "-m", "Admit R3.18BA and open R3.18BB")
assert run("git", "rev-parse", "HEAD^", capture=True) == MAIN_SHA
changed = sorted(run("git", "diff", "--name-only", MAIN_SHA, "HEAD", capture=True).splitlines())
assert changed == EXPECTED, (changed, EXPECTED)
assert run("git", "status", "--porcelain", capture=True) == ""
probe = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", CANDIDATE_BRANCH], text=True, capture_output=True)
assert probe.returncode == 2, probe.stdout
run("git", "push", "origin", f"HEAD:refs/heads/{CANDIDATE_BRANCH}")
print("CONTINUITY_COMMIT=" + run("git", "rev-parse", "HEAD", capture=True))
print("CONTINUITY_TREE=" + run("git", "show", "-s", "--format=%T", "HEAD", capture=True))
