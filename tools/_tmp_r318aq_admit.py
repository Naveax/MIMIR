from pathlib import Path
import json
import re

DATE = "2026-08-25"
BASE = "e1ccbef95c8424b689dee7d77fd8fde2af3e0204"
BASE_TREE = "4e7100625096594bcc5c5b4c6a8054c283643b13"
PARENT = "ec2d6c29f90863d9e312856043d01fb98a0c2d2d"
AQ_LIB_BLOB = "b886c58400de0efe0a6a6113d79e6f78e751a213"
AQ_TEST_BLOB = "983cbda666f40cbc739b250eac87bc4ce0c9eb99"
AQ_SPEC_BLOB = "fa8e5f6798a42fbeeed86b3b14ea7e4f39b35ebb"
AQ_BUILDER_HEAD = "4fee8974780fa2f8897bf0fea14ce13333a2dac4"
AQ_BUILDER_RUN = "32860339919/97842469079"
AQ_RECEIPT_ART = "9568109670"
AQ_RECEIPT_SIZE = "1183"
AQ_RECEIPT_DIG = "1d865740559cb0748f840b3cca3d4ab9c627ac251bc15f6f99dbabb20c2e3afe"
AQ_PR = "197"
AQ_PR_CI = "32861522922/97846413853"
AQ_PUBLISHED_CI = "32861924684/97847764026"
AP_HEAD = "736ac33c099a9183693bfcb2b5f5b74704a8808e"
AP_TREE = "840011b603b5bb330e018bd060650cfb3af29b73"
AP_RUN = "32745234196/97489066582"
AP_ART = "9526988237"
AP_DIG = "b50b01bd87c0b61ca2e407abe43ac5db9fb15290f7cd3e908332d2ac2a26c4cc"
BOX = "c70e77df7af81b436cb545d070bb90c82f562d0b"

def read(path):
    return Path(path).read_text(encoding="utf-8")

def write(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="\n")

def rep1(path, old, new, label):
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: {label}: expected 1 occurrence, got {count}")
    write(path, text.replace(old, new, 1))

def regex1(path, pattern, repl, label, flags=re.S):
    text = read(path)
    out, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"{path}: {label}: expected 1 regex match, got {count}")
    write(path, out)

# 1. Master continuity handbook.
p = "MIMIR_CONTINUE_HERE.md"
rep1(
    p,
    """LAST_PRODUCTION_CODE_SHA:
  3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38

LAST_PRODUCTION_MILESTONE:
  R3.18AN — bounded post-AK one-following-payload production""",
    f"""LAST_PRODUCTION_CODE_SHA:
  {BASE}

LAST_PRODUCTION_MILESTONE:
  R3.18AQ — bounded post-AN mixed following-control production""",
    "production block",
)
rep1(
    p,
    """CURRENT_PASS:
  R3.18AQ — bounded post-AN following-control production

CURRENT_PASS_TYPE:
  production implementation / validate one exact published R3.18AN prior, consume exactly one AP-admitted property_present bit, represent both false and true, stop one bit later, consume zero following stream/header/payload/second-control bits""",
    """CURRENT_PASS:
  R3.18AR — published-R3.18AQ mixed following-control differential

CURRENT_PASS_TYPE:
  read-only published-production differential / reuse exactly the immutable R3.18AP 47-row lane, reconstruct the published R3.18AQ result, require exact false=7 true=40 start/value/end/stop equality, and consume zero following stream/header/payload/second-control bits""",
    "current pass",
)
rep1(
    p,
    """  R3.18AQ ACTIVE bounded production: validate/recompute the exact R3.18AN prior, consume exactly one AP-admitted control bit, admit both false and true as data, and stop one bit later
  NO next stream/header/payload after the R3.18AQ control result, second later property-control bit, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted""",
    f"""  R3.18AQ PRODUCTION at {BASE}: validates/recomputes one exact R3.18AN prior, consumes exactly one AP-admitted property_present bit, accepts both false and true, and stops one bit later
  R3.18AR ACTIVE read-only differential: prove published R3.18AQ exact on the immutable AP 47-row lane with false=7 / true=40 and adjacent consumption 0/0/0/0
  NO following stream/header/payload after the R3.18AQ/AR one-control boundary, second later property-control bit, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted""",
    "frontier",
)
master = read(p)
marker = "R3_18AP_EVIDENCE_CLOSURE:\n"
if master.count(marker) != 1:
    raise SystemExit("MIMIR_CONTINUE_HERE.md: AP closure marker drift")
closure = f"""R3_18AQ_PRODUCTION_CLOSURE:
Outcome A / production / published exact mixed following-control boundary
production SHA/tree: {BASE} / {BASE_TREE}
parent: {PARENT}
lib/test blobs: {AQ_LIB_BLOB} / {AQ_TEST_BLOB}
AQ execution spec blob: {AQ_SPEC_BLOB}
builder: {AQ_BUILDER_HEAD} / {AQ_BUILDER_RUN} SUCCESS
builder receipt: artifact {AQ_RECEIPT_ART} / {AQ_RECEIPT_SIZE} bytes / sha256:{AQ_RECEIPT_DIG}
validation-only PR #{AQ_PR} closed unmerged / exact-head CI {AQ_PR_CI} SUCCESS
published-main CI: {AQ_PUBLISHED_CI} SUCCESS
clean scope: exactly lib.rs + r3_18aq_post_an_payload_control.rs / 657 insertions / no Cargo-doc-workflow-fixture-corpus mutation
frozen AP behavior: rows 47 / false=7 / true=40 / exactly one new control read / adjacent stream-header-payload-second-control 0/0/0/0
wrong-actor / unresolved-lookup / truncation / corrupt-AN-prior / wrong-context / repeatability / post-stop-poison / source-scope negatives PASS
fresh-main ancestry + force=false publication + exact-SHA readback PASS
next exact pass: R3.18AR published-R3.18AQ mixed following-control differential; no following header in AR

"""
write(p, master.replace(marker, closure + marker, 1))

# 2. Knowledge graph.
p = "MIMIR_KNOWLEDGE_GRAPH.md"
rep1(
    p,
    "R3.18AQ bounded post-AN following-control production / ACTIVE                                      |",
    """R3.18AQ bounded post-AN following-control production / PRODUCTION CLOSED
R3.18AR published-R3.18AQ mixed following-control differential / ACTIVE                             |""",
    "graph frontier",
)
old_tail = """120. `docs/continuity/MIMIR_R3_18AP_EXECUTION_SPEC.md`
121. `docs/continuity/MIMIR_R3_18AP_DECISION.md`
122. `docs/continuity/MIMIR_R3_18AQ_EXECUTION_SPEC.md`
123. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
124. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
125. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
126. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
127. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
128. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
129. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
new_tail = """120. `docs/continuity/MIMIR_R3_18AP_EXECUTION_SPEC.md`
121. `docs/continuity/MIMIR_R3_18AP_DECISION.md`
122. `docs/continuity/MIMIR_R3_18AQ_EXECUTION_SPEC.md`
123. `docs/continuity/MIMIR_R3_18AQ_DECISION.md`
124. `docs/continuity/MIMIR_R3_18AR_EXECUTION_SPEC.md`
125. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
126. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
127. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
128. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
129. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
130. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
131. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
rep1(p, old_tail, new_tail, "mandatory tail")
regex1(
    p,
    r"""### R3\.18AQ bounded post-AN following-control production: ACTIVE
.*?(?=
### R3\.18AG bounded post-AD true control:)""",
    f"""### R3.18AQ bounded post-AN following-control production: PRODUCTION / CLOSED
- production `{BASE}` / tree `{BASE_TREE}` / parent `{PARENT}`
- lib/test blobs `{AQ_LIB_BLOB}` / `{AQ_TEST_BLOB}`; exact clean scope two files / 657 insertions
- builder `{AQ_BUILDER_RUN}` SUCCESS / receipt artifact `{AQ_RECEIPT_ART}` / `sha256:{AQ_RECEIPT_DIG}`
- validation-only PR #{AQ_PR} closed unmerged; exact-head CI `{AQ_PR_CI}` SUCCESS; published-main CI `{AQ_PUBLISHED_CI}` SUCCESS
- immutable AP lane rows=47 / false=7 / true=40; both boolean classes succeed; exactly one new control read
- wrong actor / unresolved lookup / truncation / corrupt prior / wrong context / repeatability / post-stop poison negatives PASS
- next stream/header/payload/second-control consumption 0/0/0/0; force=false publication/readback PASS

### R3.18AR published-R3.18AQ mixed following-control differential: ACTIVE
- reuse exactly the immutable R3.18AP 47-row witnesses; witness reselection forbidden
- reconstruct published AQ and require exact start/value/end/stop equality with AP on all 47 rows
- expected immutable distribution false=7 / true=40; both are successful published AQ results
- false rows are terminators; no following-header claim is permitted from them
- AR consumes no following stream/header/payload/second-control and mutates no production
- only after AR Outcome A may a separate later pass investigate one following header on the exact 40 true continuation rows
""",
    "AQ section",
)

# 3. Boundary locks current override.
p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
new_override = f"""# 0. Current override — R3.18AQ closed / R3.18AR active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AQ
- `{BASE}` / `{BASE_TREE}` is canonical production; parent `{PARENT}`;
- validates/recomputes one exact published R3.18AN prior through its admitted Int/32 payload end;
- consumes exactly one following LSB-first `property_present` bit at the AN stop;
- accepts both AP-observed boolean values: false=7 / true=40 on the immutable lane;
- stops exactly one bit later and consumes no following stream/header/payload/second-control bits.

## CLOSED EVIDENCE — R3.18AP Outcome A
- immutable 47-row lane; published R3.18AN exact 47/47; oracle-native exact 47/47; mismatch 0; witness reselection 0;
- exact next `property_present` distribution false=7 / true=40;
- artifact `{AP_ART}` / `sha256:{AP_DIG}`; adjacent consumption 0/0/0/0.

## ACTIVE READ-ONLY GATE — R3.18AR
- differentially validate the published R3.18AQ API on exactly the same 47 AP witnesses;
- require published value/start/end/stop equality 47/47 and false=7 / true=40;
- both booleans remain valid data; no witness reselection or production mutation;
- stop at the AQ one-control boundary with adjacent stream/header/payload/second-control consumption 0/0/0/0.

## CLOSED
- following stream/header/payload after the R3.18AQ/AR one-control result;
- header evidence on any of the 7 false terminator rows;
- a second later property-control bit, alternate payload widening, repeated/generalized property loop or cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

---
"""
regex1(p, r"""# 0\. Current override.*?
---
""", new_override, "current override")

# 4. Continuity state.
p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
data = json.loads(read(p))
data["updated_date"] = DATE
data["last_production_code_sha"] = BASE
data["last_production_milestone"] = "R3.18AQ"
data["last_production_milestone_name"] = "bounded post-AN mixed following-control production"
data["current_pass"] = "R3.18AR"
data["current_pass_kind"] = "read-only published-production differential / exact R3.18AQ versus immutable R3.18AP one-control authority"
data["current_pass_goal"] = "Reuse exactly the immutable R3.18AP 47-row lane and prove published R3.18AQ returns the exact AP-admitted control start/value/end/stop with false=7 and true=40, mismatch zero, witness reselection zero and adjacent consumption zero."
data["current_pass_stop_boundary"] = "Published R3.18AQ one-control result only. No following stream/header/payload, second later control, generalized loop/cursor or wider actor/frame/semantic/runtime/export behavior."
data["r3_18aq"] = {
    "outcome": "A",
    "production_sha": BASE,
    "production_tree": BASE_TREE,
    "parent": PARENT,
    "lib_blob": AQ_LIB_BLOB,
    "focused_test_blob": AQ_TEST_BLOB,
    "execution_spec_blob": AQ_SPEC_BLOB,
    "builder_head": AQ_BUILDER_HEAD,
    "builder_run_job": AQ_BUILDER_RUN,
    "builder_receipt_artifact": int(AQ_RECEIPT_ART),
    "builder_receipt_size": int(AQ_RECEIPT_SIZE),
    "builder_receipt_sha256": AQ_RECEIPT_DIG,
    "validation_pr": AQ_PR,
    "validation_pr_closed_unmerged": True,
    "exact_head_ci": AQ_PR_CI,
    "published_main_ci": AQ_PUBLISHED_CI,
    "rows": 47,
    "false_count": 7,
    "true_count": 40,
    "new_control_reads": 1,
    "next_stream_bits_consumed": 0,
    "next_header_bits_consumed": 0,
    "next_payload_bits_consumed": 0,
    "second_later_control_bits_consumed": 0,
    "wrong_actor_negative": "PASS",
    "unresolved_lookup_negative": "PASS",
    "clean_scope_files": 2,
    "force_false_publication": "PASS",
    "published_readback": "PASS",
}
closed = data.setdefault("closed_now", [])
for item in [
    "following stream/header/payload after the published R3.18AQ one-control result during R3.18AR",
    "following-header evidence on any of the 7 R3.18AQ false terminator rows",
    "second later property control bit after R3.18AQ/R3.18AR",
    "generalized/repeated property loop or generic cursor after R3.18AQ/R3.18AR",
]:
    if item not in closed:
        closed.append(item)
next_files = data.get("next_files_to_read", [])
aq_spec = "docs/continuity/MIMIR_R3_18AQ_EXECUTION_SPEC.md"
aq_decision = "docs/continuity/MIMIR_R3_18AQ_DECISION.md"
ar_spec = "docs/continuity/MIMIR_R3_18AR_EXECUTION_SPEC.md"
if aq_decision not in next_files or ar_spec not in next_files:
    if aq_spec not in next_files:
        raise SystemExit("continuity state: AQ spec missing from next_files_to_read")
    idx = next_files.index(aq_spec) + 1
    for path in [ar_spec, aq_decision]:
        if path in next_files:
            next_files.remove(path)
    next_files[idx:idx] = [aq_decision, ar_spec]
data["next_files_to_read"] = next_files
write(p, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

# 5. Current state.
write(
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    f"""# MIMIR — Current Canonical State

**Continuity date:** {DATE}
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{BASE}`
**Production tree:** `{BASE_TREE}`
**Production milestone:** `R3.18AQ — bounded post-AN mixed following-control production`
**Last read-only evidence:** `R3.18AP — Outcome A / exact 47/47 / false=7 / true=40 / mismatch 0 / artifact {AP_ART}`
**Last contract:** `R3.18AJ — Outcome A / exact_tuple_only / 17 contexts / multiplicity 47 / sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c`
**Current exact pass:** `R3.18AR — published-R3.18AQ mixed following-control differential`

## Truthful boundary

R3.18AQ is now published production. It revalidates one exact R3.18AN Int/32 payload composition, reads exactly one following `property_present` bit, accepts both AP-observed values, and stops exactly one bit later. The immutable lane distribution remains **false=7 / true=40**.

```text
production SHA/tree                  {BASE} / {BASE_TREE}
parent                               {PARENT}
lib / focused-test blobs             {AQ_LIB_BLOB} / {AQ_TEST_BLOB}
builder run/job                      {AQ_BUILDER_RUN} SUCCESS
builder receipt                      {AQ_RECEIPT_ART} / sha256:{AQ_RECEIPT_DIG}
validation-only PR                   #{AQ_PR} closed unmerged
exact-head PR CI                     {AQ_PR_CI} SUCCESS
published-main CI                    {AQ_PUBLISHED_CI} SUCCESS
clean production scope               2 files / 657 insertions
frozen rows                          47
false / true                         7 / 40
new control reads                    1
adjacent stream/header/payload/control 0/0/0/0
force=false publication/readback     PASS
```

## Current gate

R3.18AR is read-only. It must reuse exactly the immutable R3.18AP 47-row witnesses and prove published R3.18AQ equals the AP control authority on value/start/end/stop for all rows. Both false and true remain valid published results.

## Continuation split

The seven false rows are terminators. A future following-header evidence pass may only be considered on the exact 40 true continuation rows, and only after R3.18AR closes Outcome A.

## Hard stop

AR may not read or resolve a following stream/header/payload, may not read a second later control bit, may not mutate production, and may not create a generalized property loop/cursor or widen actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior.
""",
)

# 6. Handoff.
write(
    "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",
    f"""# MIMIR — Next Chat Handoff

Canonical production is **R3.18AQ** at `{BASE}` / `{BASE_TREE}`, parent `{PARENT}`.

AQ authority: builder `{AQ_BUILDER_RUN}` SUCCESS on helper `{AQ_BUILDER_HEAD}`; receipt artifact `{AQ_RECEIPT_ART}` / `{AQ_RECEIPT_SIZE}` bytes / `sha256:{AQ_RECEIPT_DIG}`; validation-only PR #{AQ_PR} closed unmerged after exact-head CI `{AQ_PR_CI}` SUCCESS; published-main CI `{AQ_PUBLISHED_CI}` SUCCESS. Clean production scope is exactly `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18aq_post_an_payload_control.rs`.

Published behavior: immutable rows 47; false=7; true=40; both values succeed; exactly one new `property_present` bit is consumed; next stream/header/payload/second-control consumption 0/0/0/0. Wrong actor, unresolved lookup, truncation, corrupt AN prior, wrong context, repeatability and post-stop poison negatives PASS.

The active pass is **R3.18AR**, a read-only published-production differential. Reuse exactly the immutable R3.18AP 47 witnesses and require published AQ value/start/end/stop equality 47/47, false=7, true=40, mismatch 0, witness reselection 0, production mutation 0 and adjacent consumption 0/0/0/0.

Do not decode the following header in AR. The 7 false rows are terminators. Only after AR Outcome A may a separate later pass investigate one following header on the exact 40 true continuation rows.

Before any workflow dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run if present. Rerun is never polling.
""",
)

# 7. Progress ledger append-only entry.
p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
ledger = read(p).rstrip("\n")
entry = f"""

---

## {DATE} — R3.18AQ — Bounded Post-AN Mixed Following-Control Production

Production base SHA: `{PARENT}`
Production commit SHA: `{BASE}`
Pass type: bounded production implementation + clean reconstruction + publication
Outcome: **A — ADMITTED / PRODUCTION**

What changed:
- added one boundary-specific R3.18AQ result/API after exact R3.18AN;
- validates/recomputes the supplied AN authority and exact Int/32 payload end;
- consumes exactly one LSB-first following `property_present` bit;
- accepts both AP-admitted false and true outcomes;
- stops exactly one bit later;
- added one focused AQ integration test file with frozen-lane, negative and scope-lock coverage.

Evidence:
- immutable R3.18AP lane 47 rows;
- false=7 / true=40;
- exactly one new control read;
- following stream/header/payload/second-control consumption 0/0/0/0;
- wrong actor / unresolved lookup / truncation / corrupt prior / wrong context / repeatability / post-stop poison negatives PASS.

Validation:
- final builder `{AQ_BUILDER_RUN}` SUCCESS;
- builder receipt artifact `{AQ_RECEIPT_ART}` / `sha256:{AQ_RECEIPT_DIG}`;
- exact clean scope two files / 657 insertions;
- validation-only PR #{AQ_PR} closed unmerged;
- exact-head CI `{AQ_PR_CI}` SUCCESS;
- published-main CI `{AQ_PUBLISHED_CI}` SUCCESS;
- fresh-main ancestry, force=false fast-forward and exact-SHA readback PASS.

Boundaries opened:
- exactly one mixed false/true following control bit after one valid published R3.18AN payload.

Boundaries still closed:
- following stream/header/payload;
- second later control;
- generalized/repeated property loop/cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export layers.

Important negative facts / anti-regressions:
- false is valid at this exact AQ boundary; do not inherit true-only M/W/AG behavior;
- the 7 false rows are terminators and cannot be used for a following-header continuation claim.

Next exact pass:
- `R3.18AR — published-R3.18AQ mixed following-control differential` on exactly the immutable 47 AP witnesses.
"""
write(p, ledger + entry + "\n")

# 8. AQ production decision.
write(
    "docs/continuity/MIMIR_R3_18AQ_DECISION.md",
    f"""# MIMIR R3.18AQ — Bounded Post-AN Mixed Following-Control Production Decision

**Date:** {DATE}
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production:** `{BASE}` / `{BASE_TREE}`
**Parent:** `{PARENT}`

## Decision

R3.18AQ is admitted as the minimum production composition after R3.18AN. It revalidates/recomputes the exact supplied AN payload composition, requires the admitted Int/32 payload-end boundary, reads exactly one following LSB-first `property_present` bit, accepts both R3.18AP-observed boolean classes, and stops exactly one bit later.

Unlike R3.18M, R3.18W and R3.18AG, false is not an error here. The immutable evidence distribution is false=7 / true=40.

## Exact authority

```text
production SHA/tree                  {BASE} / {BASE_TREE}
parent                               {PARENT}
lib blob                             {AQ_LIB_BLOB}
focused test blob                    {AQ_TEST_BLOB}
AQ execution spec blob               {AQ_SPEC_BLOB}
final builder helper                 {AQ_BUILDER_HEAD}
final builder run/job                {AQ_BUILDER_RUN} SUCCESS
builder receipt artifact             {AQ_RECEIPT_ART} / {AQ_RECEIPT_SIZE} bytes
builder receipt SHA-256              {AQ_RECEIPT_DIG}
validation-only PR                   #{AQ_PR} closed unmerged
exact-head validation CI             {AQ_PR_CI} SUCCESS
published-main CI                    {AQ_PUBLISHED_CI} SUCCESS
AP evidence head/tree                {AP_HEAD} / {AP_TREE}
AP authority run/job                 {AP_RUN} SUCCESS
AP artifact                          {AP_ART} / sha256:{AP_DIG}
pinned Boxcars                       {BOX}
```

## Published behavior

```text
frozen rows                          47
false                                7
true                                 40
both boolean classes accepted        PASS
new control reads                    1
start/end/stop exact                 PASS
next stream bits consumed            0
next header bits consumed            0
next payload bits consumed           0
second later control bits consumed   0
wrong actor negative                 PASS
unresolved lookup negative           PASS
truncation negative                  PASS
corrupt AN prior negative            PASS
wrong exact context negative         PASS
repeatability                        PASS
post-stop poison invariance          PASS
source-scope one-read/no-loop guard  PASS
```

## Clean scope

Exactly two files changed from parent to production:
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/tests/r3_18aq_post_an_payload_control.rs`

The commit contains 657 insertions and no Cargo/dependency, continuity, workflow, fixture, corpus or unrelated production changes.

## Validation and publication

The final builder passed Rust 1.85 formatting, focused AQ tests, boundary regressions, workspace check/test/clippy with warnings denied, and repository verification. PR #{AQ_PR} provided exact-head normal CI and was closed unmerged. Fresh main still equaled the candidate parent, so `main` was fast-forwarded to the exact clean candidate with `force=false`. Exact published-main readback and natural CI then succeeded.

## Hard stop

No following stream/header/payload is admitted after the AQ one-control result. No second later control, repeated/generalized property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted.

The seven false rows are terminators; they do not authorize any following-header decode.

## Next gate

R3.18AR is a separate read-only published-production differential over exactly the immutable R3.18AP 47-row lane. It must prove published AQ value/start/end/stop equality with false=7 / true=40, mismatch zero, witness reselection zero, production mutation zero and adjacent consumption 0/0/0/0. It may not decode a following header.
""",
)

# 9. AR execution spec.
write(
    "docs/continuity/MIMIR_R3_18AR_EXECUTION_SPEC.md",
    f"""# MIMIR R3.18AR — Published R3.18AQ Mixed Following-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18AQ `{BASE}` / `{BASE_TREE}`
**Production mutation:** forbidden
**Following stream/header/payload:** forbidden
**Second later control:** forbidden

## Goal

Validate the published R3.18AQ one-control API against exactly the immutable R3.18AP 47-row authority lane. Prove that published AQ reconstructs the valid R3.18AN prerequisite, begins exactly at the frozen AP control start, returns the exact frozen boolean, ends/stops exactly one bit later, and consumes nothing adjacent.

The immutable distribution is **false=7 / true=40**. Both classes are successful published AQ results.

## Frozen authority

```text
production SHA/tree                  {BASE} / {BASE_TREE}
parent                               {PARENT}
lib/test blobs                       {AQ_LIB_BLOB} / {AQ_TEST_BLOB}
AQ execution spec blob               {AQ_SPEC_BLOB}
AQ builder                           {AQ_BUILDER_RUN} SUCCESS
AQ builder receipt                   {AQ_RECEIPT_ART} / sha256:{AQ_RECEIPT_DIG}
AQ validation PR                     #{AQ_PR} closed unmerged
AQ exact-head CI                     {AQ_PR_CI} SUCCESS
AQ published-main CI                 {AQ_PUBLISHED_CI} SUCCESS
AP evidence head/tree                {AP_HEAD} / {AP_TREE}
AP authority                         {AP_RUN} SUCCESS
AP artifact                          {AP_ART} / sha256:{AP_DIG}
AP frozen rows                       47
AP distribution                      false=7 / true=40
AP adjacent consumption              0/0/0/0
pinned Boxcars                       {BOX}
```

Witness reselection is forbidden.

## Exact differential lane

For every one of the exact 47 AP witnesses:

1. reconstruct the exact valid published R3.18AN prerequisite;
2. call the published R3.18AQ API once;
3. require AQ `property_present_start_bit` == frozen AP control start == AN stop;
4. require AQ boolean == frozen AP boolean;
5. require AQ end/stop == frozen AP control end == start + 1;
6. repeat and require exact identical result;
7. stop.

Expected totals:
```text
rows                 47/47
false                7
true                 40
mismatch             0
witness reselection  0
```

## Required negative controls

At minimum:
- truncate exactly before the AQ control bit -> reject atomically;
- wrong actor authority -> reject before AQ control success;
- unresolved lookup -> reject before AQ control success;
- wrong exact context -> reject;
- corrupt/mismatched AN prior -> reject;
- repeat identical invocation -> exact equality;
- poison bits beginning at AQ stop -> returned one-bit result unchanged;
- source-scope guard -> exactly one control read and no generic loop/header/payload decode;
- next stream/header/payload/second-control consumption remains 0/0/0/0.

Because both booleans are admitted, flipping a frozen bit is not an API-malformed negative. If used as a differential mutation, it must be reported as frozen-value mismatch rather than as expected API rejection.

## Validation

Require:
- exact 47/47 frozen witness identities;
- published AQ versus frozen AP value/start/end/stop exact 47/47;
- published AN prerequisite exact 47/47;
- false=7 / true=40;
- mismatch 0;
- witness reselection 0;
- repeatability PASS 47/47;
- all negative controls PASS;
- adjacent stream/header/payload/second-control consumption 0/0/0/0;
- focused R3.18AQ tests PASS;
- full mimir-replay/workspace fmt/check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy scan PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse an equivalent exact run if present. Rerun is never polling.

## Continuation classification

The frozen boolean controls continuation:
- the exact 7 false rows are terminators and must stop after the AQ control;
- the exact 40 true rows are continuation candidates.

AR itself does not decode any following header. Only if AR closes Outcome A may a separate later pass investigate exactly one following property header on the exact 40 true continuation rows, stopping at that header's payload start.

## Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
Published R3.18AQ is exact on all 47 immutable AP witnesses with false=7 / true=40, mismatch 0, witness reselection 0, all negative/full validations PASS and adjacent consumption 0/0/0/0. A later separate read-only pass may investigate one following header on exactly the 40 true continuation rows.

### Outcome B
A bounded mismatch or narrower supported subset is isolated. Admit only supported facts and keep following-header evidence closed.

### Outcome C
Authority/witness drift, published mismatch, rejection of an AP-admitted boolean class, adjacent access, production mutation, privacy failure or generic chaining. Stop without widening.
""",
)

print("R3.18AQ continuity generator complete")
