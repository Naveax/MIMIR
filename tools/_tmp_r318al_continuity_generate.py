from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path.cwd()
BASE_MAIN = "02233c8125e658513dcb068370c48b1e8f15a01c"
BASE_TREE = "fc9293d821dd3e6e269763c3c0ab091428c29490"
PRODUCTION_SHA = "f20f529e3ada6e9a671ea91e5676a17a00770145"
PRODUCTION_TREE = "98c675811cca4e4d7f0122c762f371548c9266c2"
AL_HEAD = "cf672f97a5e280dda6b3c917d57ea95e37b0ac12"
AL_TREE = "676aa9a9e3b30112dfab07893eb09d480761b41e"
AL_RUN = "32470391102"
AL_JOB = "96735754596"
AL_PUSH_CI = "32470391196"
AL_PUSH_CI_JOB = "96735754648"
AL_PR_CI = "32470393543"
AL_PR_CI_JOB = "96735761501"
AL_ARTIFACT = "9442394567"
AL_ARTIFACT_SIZE = "14921"
AL_ARTIFACT_DIGEST = "a13d9adbc4e4eda92b0114320b851add6e95a76a462e6e75d21264f9cdf9ee68"
AI_HEAD = "9d424dae2ed8cc7a0a6868111805a48763131196"
AI_ARTIFACT = "9424764320"
AI_DIGEST = "ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5"
AJ_CONTRACT = "cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c"
BUILDER_RUN = os.environ.get("R318AL_BUILDER_RUN", "UNSET")
BUILDER_JOB = os.environ.get("R318AL_BUILDER_JOB", "UNSET")
if BUILDER_RUN == "UNSET" or BUILDER_JOB == "UNSET":
    raise SystemExit("builder run/job receipt missing")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected one marker, found {n}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, repl: str, label: str) -> str:
    out, n = re.subn(pattern, repl, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"{label}: expected one regex match, found {n}")
    return out


# Durable decision and next execution spec.
decision = f"""# MIMIR R3.18AL — Published R3.18AK Following-Header Differential Decision

**Date:** 2026-08-21
**Pass type:** read-only published-production differential
**Outcome:** **A — ADMITTED / CLOSED**
**Production mutation:** none
**Canonical production:** `{PRODUCTION_SHA}` / `{PRODUCTION_TREE}`

## Decision

R3.18AL closes Outcome A. On exactly the immutable R3.18AI 47-row lane, published R3.18AK reconstructed the admitted post-AG following header exactly through `payload_start` on all 47 rows. The direct stateless native header result matched 47/47, the exact R3.18AJ seven-field contexts and observed multiplicities reconstructed 17/17 and 47/47, all observed tags remained `Int`, and native/oracle mismatch and witness reselection were both zero.

The pass consumed zero following-payload bits and zero second-later-control bits. It therefore validates published R3.18AK only; it does not itself admit a payload decoder, payload production composition, another control bit, a repeated/generalized property cursor, next actor/frame iteration, or semantic/runtime/export widening.

## Exact authority

```text
canonical parent                    {BASE_MAIN} / {BASE_TREE}
production SHA/tree                 {PRODUCTION_SHA} / {PRODUCTION_TREE}
R3.18AI head/artifact               {AI_HEAD} / {AI_ARTIFACT} / sha256:{AI_DIGEST}
R3.18AJ contract                    sha256:{AJ_CONTRACT}
AL receipt-bound head/tree          {AL_HEAD} / {AL_TREE}
authority run/job                   {AL_RUN} / {AL_JOB} SUCCESS
same-head natural push CI           {AL_PUSH_CI} / {AL_PUSH_CI_JOB} SUCCESS / count 1
exact-head PR CI                    {AL_PR_CI} / {AL_PR_CI_JOB} SUCCESS
validation PR                       #132 closed unmerged
artifact                            {AL_ARTIFACT} / {AL_ARTIFACT_SIZE} bytes
artifact digest / ZIP SHA-256       sha256:{AL_ARTIFACT_DIGEST}
internal SHA-256 manifest           11/11 PASS
continuity builder                  {BUILDER_RUN} / {BUILDER_JOB}
```

The artifact number above is taken from the exact run API and independently downloaded ZIP. An earlier PR-body artifact number was stale and is not authority.

## Frozen result

```text
frozen rows                         47/47
published R3.18AK exact             47/47
direct stateless header exact       47/47
R3.18AJ exact contexts              17/17
R3.18AJ multiplicity                47/47
observed tag                        Int=47
native/oracle mismatch              0
witness reselection                 0
repeatability                       47/47 PASS
header truncation                   47/47 PASS
corrupt AG control                  47/47 PASS
wrong actor/prior                   47/47 PASS
unresolved lookup                   47/47 PASS
wrong exact version context         47/47 PASS
post-payload-start poison           47/47 PASS
Cartesian/fabricated/old-Z          PASS
R3.18Z/R3.18P inheritance           rejected
following payload bits consumed     0
second later control bits consumed  0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                        PASS
```

## Hard stop

Production remains R3.18AK. R3.18AL does not admit post-AK payload production, another property-control bit, false-success semantics, alternate unadmitted layouts, repeated/generalized property iteration, next actor/frame/lifecycle, raw-state/event/slice/skill/counterfactual/runtime/export widening.

## Next exact pass

`R3.18AM` is a separate read-only evidence pass. It may investigate exactly one payload beginning at each already-proven R3.18AL/R3.18AK `payload_start` on the same immutable 47 rows. The observed header tag is `Int` on all 47 rows, but payload width/value semantics remain hypotheses until independently confirmed. R3.18AM must stop at the payload end and consume zero bits of another property control.
"""

am_spec = f"""# MIMIR R3.18AM — Post-R3.18AK One-Payload Evidence

**Status:** ACTIVE
**Pass type:** read-only payload evidence
**Production authority:** R3.18AK `{PRODUCTION_SHA}` / `{PRODUCTION_TREE}`
**Parent evidence:** R3.18AL Outcome A
**Production mutation:** forbidden
**Another property-control bit:** forbidden

## 1. Goal

On exactly the immutable R3.18AL 47-row lane, begin at the already-proven published-R3.18AK `payload_start`, decode exactly one payload using the existing lower-level payload machinery, compare payload width and semantic value to an independently pinned Boxcars oracle, and stop exactly at that payload end.

The 47 published headers all resolve to `Int`. This is an observed header fact, not by itself a payload-width admission. A 32-bit signed-integer payload is the candidate hypothesis to test, not a predeclared result.

## 2. Frozen authority

```text
canonical admission parent          {BASE_MAIN} / {BASE_TREE}
production SHA/tree                 {PRODUCTION_SHA} / {PRODUCTION_TREE}
R3.18AL head/tree                   {AL_HEAD} / {AL_TREE}
R3.18AL authority                   {AL_RUN} / {AL_JOB} SUCCESS
R3.18AL same-head push CI           {AL_PUSH_CI} / {AL_PUSH_CI_JOB} SUCCESS / count 1
R3.18AL PR CI                       {AL_PR_CI} / {AL_PR_CI_JOB} SUCCESS
R3.18AL artifact                    {AL_ARTIFACT} / {AL_ARTIFACT_SIZE} / sha256:{AL_ARTIFACT_DIGEST}
rows                                47
published AK exact                  47/47
header tags                         Int=47
AJ exact contexts / multiplicity    17 / 47
witness reselection                 0
```

## 3. Required evidence

- verify replay identity and frozen row coordinates before decoding;
- reconstruct valid published R3.18AG prior/control and published R3.18AK header exactly 47/47;
- begin payload decode exactly at the frozen `payload_start` for every row;
- instrument pinned Boxcars at the same property and capture exact payload start/end plus semantic integer value;
- use existing MIMIR lower-level primitive payload decode, not a second ad-hoc parser;
- compare native/oracle payload start, payload end, width and semantic value 47/47;
- measure the observed payload-width distribution rather than assuming it;
- prove deterministic repeatability;
- prove truncation fails closed;
- prove wrong decoder/tag and wrong exact context fail closed where structurally applicable;
- poison bits after the measured payload end and prove the payload result is invariant;
- consume zero bits of the following `property_present` control.

## 4. Negative controls

At minimum include truncation before payload end, wrong decoder/tag, wrong exact version/context, corrupted published-AK boundary, repeatability, and post-payload-end poison. Do not fabricate a full-width invalid integer bit pattern merely to manufacture a negative if the wire domain accepts the full width; record that negative fact explicitly instead.

## 5. Evidence artifact

Produce privacy-safe immutable evidence containing exact source/production/oracle/replay identities, frozen witness coordinates, per-row payload comparison, width/semantic summary, negative-control summary, mutation/consumption counters, internal SHA-256 manifest and receipts. Witness reselection must remain zero.

## 6. Validation

Use the exact existing R3.18AL lane and pinned Boxcars SHA. Run focused regressions, full `mimir-replay`, workspace fmt/check/test/clippy, repository verifier and same-head CI. Before any dispatch/rerun, reuse an equivalent queued/waiting/in-progress run for the same SHA/workflow/input. Production/Cargo/fixture/corpus/support mutation must remain `0/0/0/0/0`.

## 7. Hard stop

R3.18AM is evidence only. It may not publish payload composition, read another property-control bit, create a generic/repeated property cursor, iterate another actor/frame, mutate lifecycle state, or widen into raw state/events/slices/skills/counterfactual/runtime/export behavior.

## 8. Outcome gate

### Outcome A
One exact payload family is independently confirmed on all frozen rows with mismatch zero and zero following-control consumption. A later separate R3.18AN production pass may implement only that admitted payload family and exact boundary/context.

### Outcome B
A bounded payload family split or harness gap is isolated. Admit only the supported subset and keep production unchanged.

### Outcome C
Authority drift, witness reselection, unexplained native/oracle mismatch, boundary over-read, context widening or production mutation. Stop without widening.
"""

for path in ["docs/continuity/MIMIR_R3_18AL_DECISION.md", "docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md"]:
    if (ROOT / path).exists():
        raise SystemExit(f"unexpected existing file: {path}")
write("docs/continuity/MIMIR_R3_18AL_DECISION.md", decision)
write("docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md", am_spec)

# MIMIR_CONTINUE_HERE.md
p = "MIMIR_CONTINUE_HERE.md"
t = read(p)
t = replace_once(t,
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AI — one following property-header evidence after published R3.18AG / Outcome A / 47/47 / 17 exact contexts / Int=47 / mismatch 0 / artifact 9424764320",
    f"LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AL — published R3.18AK following-header differential / Outcome A / 47/47 / 17 exact contexts / Int=47 / mismatch 0 / artifact {AL_ARTIFACT}",
    "continue last audit")
t = replace_once(t,
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AI — one post-AG following header exact / 47 rows / 17 exact contexts / Int=47 / native-oracle mismatch 0 / following-payload-second-control 0/0 / artifact 9424764320",
    f"LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AL — published AK exact / 47 rows / 17 exact contexts / Int=47 / native-oracle mismatch 0 / following-payload-second-control 0/0 / artifact {AL_ARTIFACT}",
    "continue last evidence")
t = replace_once(t,
    "CURRENT_PASS:\n  R3.18AL — published R3.18AK post-AG following-header differential audit",
    "CURRENT_PASS:\n  R3.18AM — post-R3.18AK one-payload evidence",
    "continue current pass")
t = replace_once(t,
    "CURRENT_PASS_TYPE:\n  read-only differential audit / validate published R3.18AK on the immutable R3.18AI 47-row lane through payload_start with zero production mutation",
    "CURRENT_PASS_TYPE:\n  read-only payload evidence / from each exact published-R3.18AK payload_start investigate exactly one Int-tagged payload and stop at its measured payload end; no another-control bit",
    "continue pass type")
t = replace_once(t,
    "  R3.18AL ACTIVE read-only differential: validate published AK on the exact immutable R3.18AI 47-row lane; production remains frozen at R3.18AK\n  NO following payload, second later control, false success semantics, alternate unadmitted layout, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    f"  R3.18AL CLOSED Outcome A: published AK/direct-header exact 47/47; AJ contexts 17/17 and multiplicity 47/47; Int=47; mismatch 0; witness reselection 0; payload/control consumption 0/0; artifact {AL_ARTIFACT}\n  R3.18AM ACTIVE read-only payload evidence: begin exactly at the proven AK payload_start and investigate one Int-tagged payload only; production remains frozen at R3.18AK\n  NO post-AK payload production, another property control, false success semantics, alternate unadmitted layout, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "continue hard stop")
closure = f"""
R3_18AL_EVIDENCE_CLOSURE:
  Outcome A / read-only / production unchanged at {PRODUCTION_SHA} / tree {PRODUCTION_TREE}
  authority head/tree: {AL_HEAD} / {AL_TREE}
  authority run/job: {AL_RUN} / {AL_JOB} SUCCESS
  natural same-head push CI: {AL_PUSH_CI} / {AL_PUSH_CI_JOB} SUCCESS / count 1
  exact-head PR CI: {AL_PR_CI} / {AL_PR_CI_JOB} SUCCESS / PR #132 closed unmerged
  artifact: {AL_ARTIFACT} / {AL_ARTIFACT_SIZE} bytes / sha256:{AL_ARTIFACT_DIGEST}; downloaded ZIP digest exact / inner manifest 11/11 PASS
  frozen rows 47/47 / published AK 47/47 / direct header 47/47 / AJ contexts 17/17 / multiplicity 47/47 / Int=47 / mismatch 0
  repeatability/truncation/corrupt-AG/wrong-actor/unresolved/wrong-version/post-payload poison 47/47; Cartesian/fabricated/old-Z PASS
  witness reselection 0 / following payload + second-control consumption 0/0 / privacy PASS / production-Cargo-fixture-corpus-support mutation 0/0/0/0/0
  exact run API corrects stale earlier PR-body artifact numbering; receipt above is authoritative
"""
t = replace_once(t, "\nR3_18AB_EVIDENCE_CLOSURE:\n", "\n" + closure + "\nR3_18AB_EVIDENCE_CLOSURE:\n", "continue AL closure insertion")
t = replace_once(t,
    "[>] R3.18 complete property loop — active R3.18AL published-AK following-header differential",
    "[>] R3.18 complete property loop — active R3.18AM post-AK one-payload evidence",
    "continue legend")
t = replace_once(t,
    f"> **MIMIR production is R3.18AK `{PRODUCTION_SHA}` / tree `{PRODUCTION_TREE}`. R3.18AK is CLOSED Outcome A: one post-AG following header, exact R3.18AJ 17-tuple membership, stop exactly at `payload_start`, published-main CI `32459617440/96703744791` SUCCESS. R3.18AL is active read-only published-AK differential on the immutable R3.18AI 47-row lane; payload, another control, loops/cursors and actor/frame/semantic/runtime widening remain closed.**",
    f"> **MIMIR production remains R3.18AK `{PRODUCTION_SHA}` / tree `{PRODUCTION_TREE}`. R3.18AL is CLOSED Outcome A at exact evidence head `{AL_HEAD}`: published AK/direct header exact 47/47, AJ contexts 17/17, Int=47, mismatch 0, witness reselection 0 and payload/control consumption 0/0. R3.18AM is active read-only evidence for exactly one post-AK Int-tagged payload; payload production, another control, loops/cursors and actor/frame/semantic/runtime widening remain closed.**",
    "continue one-line truth")
am_checklist = f"""# CURRENT PASS CHECKLIST — R3.18AM

**Goal:** independently establish the exact one-payload wire/semantic contract beginning at each frozen published-R3.18AK `payload_start`, without production mutation or another-control consumption.

```text
[ ] Fetch fresh main and require the published R3.18AL admission parent; freeze production at {PRODUCTION_SHA} / {PRODUCTION_TREE}.
[ ] Freeze R3.18AL authority {AL_HEAD}, run/job {AL_RUN}/{AL_JOB}, same-head push CI {AL_PUSH_CI}/{AL_PUSH_CI_JOB}, PR CI {AL_PR_CI}/{AL_PR_CI_JOB}, artifact {AL_ARTIFACT}/sha256:{AL_ARTIFACT_DIGEST}.
[ ] Reuse exactly the immutable 47 rows; replay identity and witness coordinates must match; witness reselection = 0.
[ ] Reconstruct valid AG prior/control + published AK header 47/47 and begin exactly at the frozen payload_start.
[ ] Instrument pinned Boxcars c70e77df7af81b436cb545d070bb90c82f562d0b at the same property and record exact payload start/end plus semantic integer value.
[ ] Decode with existing MIMIR lower-level payload machinery; do not add a second parser.
[ ] Measure payload width rather than assuming 32 bits; compare native/oracle start/end/width/value 47/47 with mismatch 0 for Outcome A.
[ ] Run repeatability, truncation, wrong decoder/tag, wrong context, corrupt-AK-boundary and post-payload-end poison negatives.
[ ] Prove another property-control bits consumed = 0 and no generic/repeated property cursor/loop is introduced.
[ ] Produce privacy-safe immutable evidence with internal SHA-256 manifest and exact source/oracle/replay receipts.
[ ] Run focused/full mimir-replay, workspace fmt/check/test/clippy, repository verifier and same-head normal CI; never rerun merely to poll.
[ ] Require production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.
[ ] Outcome A may open only a separate R3.18AN bounded payload-production pass for the independently admitted payload contract.
```
"""
t = regex_once(t, r"# CURRENT PASS CHECKLIST — R3\.18AL\n.*\Z", am_checklist, "continue checklist")
write(p, t)

# Continuity JSON state.
p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(read(p))
state["last_completed_read_only_audit"] = "R3.18AL"
state["last_completed_evidence_pass"] = "R3.18AL"
state["last_completed_evidence_outcome"] = f"A — published AK/direct header exact 47/47; AJ contexts 17/17; Int=47; mismatch 0; witness reselection 0; payload/control 0/0; artifact {AL_ARTIFACT}."
state["current_pass"] = "R3.18AM"
state["current_pass_kind"] = "read-only payload evidence / exactly one post-R3.18AK payload from frozen payload_start; production frozen"
state["current_pass_goal"] = "Independently establish exact payload width and semantic value for the 47 Int-tagged post-AK payloads on the immutable AL lane."
state["current_pass_stop_boundary"] = "Exactly one measured payload end. No another property-control bit, production composition, loop/cursor, actor/frame or semantic/runtime/export widening."
state["r3_18al"] = {
    "outcome": "A",
    "production_source_changed": False,
    "production_sha": PRODUCTION_SHA,
    "evidence_head": AL_HEAD,
    "evidence_tree": AL_TREE,
    "authority_run": AL_RUN,
    "authority_job": AL_JOB,
    "same_head_push_ci": AL_PUSH_CI,
    "same_head_push_ci_job": AL_PUSH_CI_JOB,
    "same_head_push_ci_count": 1,
    "pr_ci": AL_PR_CI,
    "pr_ci_job": AL_PR_CI_JOB,
    "artifact": int(AL_ARTIFACT),
    "artifact_size": int(AL_ARTIFACT_SIZE),
    "artifact_sha256": AL_ARTIFACT_DIGEST,
    "rows": 47,
    "published_ak_exact": 47,
    "direct_header_exact": 47,
    "aj_exact_contexts": 17,
    "aj_multiplicity_sum": 47,
    "tag_int": 47,
    "native_oracle_mismatch": 0,
    "witness_reselection": 0,
    "following_payload_bits_consumed": 0,
    "second_later_control_bits_consumed": 0,
}
for old, new in [
    ("following payload after the R3.18AK one-header production boundary", "post-R3.18AK following payload production composition"),
    ("post-R3.18AK following payload", "post-R3.18AK following payload production composition"),
]:
    state["closed_now"] = [new if x == old else x for x in state.get("closed_now", [])]
next_files = state.get("next_files_to_read", [])
for f in ["docs/continuity/MIMIR_R3_18AL_DECISION.md", "docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md"]:
    if f not in next_files:
        insert_at = next_files.index("docs/continuity/MIMIR_PASS_PROTOCOL.md") if "docs/continuity/MIMIR_PASS_PROTOCOL.md" in next_files else len(next_files)
        next_files.insert(insert_at, f)
state["next_files_to_read"] = next_files
write(p, json.dumps(state, indent=2, ensure_ascii=False) + "\n")

# Small current-state docs are intentionally rewritten as current truth.
write("docs/continuity/MIMIR_CURRENT_STATE.md", f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-21
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PRODUCTION_SHA}`
**Production tree:** `{PRODUCTION_TREE}`
**Production milestone:** `R3.18AK — bounded post-AG following-header production composition`
**Last read-only evidence:** `R3.18AL — Outcome A / 47/47 published AK + direct header / 17 exact contexts / Int=47 / mismatch 0 / artifact {AL_ARTIFACT}`
**Last contract:** `R3.18AJ — Outcome A / exact_tuple_only / 17 contexts / multiplicity 47 / sha256:{AJ_CONTRACT}`
**Current exact pass:** `R3.18AM — post-R3.18AK one-payload evidence`

## Truthful boundary

R3.18AK remains published production at `{PRODUCTION_SHA}` / `{PRODUCTION_TREE}`. R3.18AL independently validated that published API on the immutable 47-row AI lane through `payload_start`: published AK exact 47/47, direct stateless header exact 47/47, AJ contexts 17/17, multiplicity 47/47, Int=47, mismatch 0, witness reselection 0, payload/control consumption 0/0.

```text
R3.18AL head/tree                    {AL_HEAD} / {AL_TREE}
authority run/job                    {AL_RUN} / {AL_JOB} SUCCESS
same-head natural push CI            {AL_PUSH_CI} / {AL_PUSH_CI_JOB} SUCCESS / count 1
exact-head PR CI                     {AL_PR_CI} / {AL_PR_CI_JOB} SUCCESS
artifact                             {AL_ARTIFACT} / {AL_ARTIFACT_SIZE} / sha256:{AL_ARTIFACT_DIGEST}
artifact internal manifest           11/11 PASS
production mutation                  none
```

## Current gate

R3.18AM is read-only evidence. Reuse exactly the immutable 47 rows and begin at each proven published-AK `payload_start`. The observed header tag is Int on all rows, but payload width/value semantics must be independently measured against pinned Boxcars. Stop exactly at one payload end and consume zero bits of another property control.

## Hard stop

Post-AK payload production composition, another property control, generalized/repeated property iteration or cursor, alternate unadmitted layouts, next actor/frame/lifecycle and raw-state/event/slice/skill/counterfactual/runtime/export behavior remain closed.
""")

write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", f"""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AK** at `{PRODUCTION_SHA}` / `{PRODUCTION_TREE}`. R3.18AL is now CLOSED Outcome A as a read-only published-production differential.

R3.18AL exact authority is `{AL_HEAD}` / `{AL_TREE}` with evidence `{AL_RUN}/{AL_JOB}` SUCCESS, natural same-head push CI `{AL_PUSH_CI}/{AL_PUSH_CI_JOB}` SUCCESS with count 1, exact-head PR CI `{AL_PR_CI}/{AL_PR_CI_JOB}` SUCCESS, and immutable artifact `{AL_ARTIFACT}` / `{AL_ARTIFACT_SIZE}` bytes / `sha256:{AL_ARTIFACT_DIGEST}`. Independent download verified the ZIP digest and internal manifest 11/11. Results: published AK 47/47, direct header 47/47, AJ contexts 17/17, multiplicity 47/47, Int=47, mismatch 0, witness reselection 0, payload/control consumption 0/0.

The active pass is **R3.18AM**, read-only one-payload evidence. Reuse exactly the frozen 47 rows, begin at each proven AK `payload_start`, independently measure the Int-tagged payload width and signed semantic value against pinned Boxcars, and stop at the one payload end. Do not assume 32 bits before the evidence. Consume zero bits of another property control and do not mutate production Rust.

Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json`, `docs/continuity/MIMIR_R3_18AK_DECISION.md`, `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`, `docs/continuity/MIMIR_R3_18AL_DECISION.md`, and `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md` before continuing.
""")

# Boundary locks current override only.
p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
t = read(p)
t = replace_once(t, "# 0. Current override — R3.18AK production closed / R3.18AL active", "# 0. Current override — R3.18AK production / R3.18AL closed / R3.18AM active", "locks heading")
t = replace_once(t,
    "## ACTIVE EVIDENCE GATE — R3.18AL\n- validate published R3.18AK on exactly the immutable R3.18AI 47-row lane;\n- production Rust frozen; no witness reselection;\n- compare through `payload_start` only and prove payload/control consumption 0/0.\n\n## CLOSED\n- post-AK following payload; another property control; false success semantics; alternate unadmitted layouts; repeated/generalized property loop or generic cursor;",
    f"## CLOSED EVIDENCE — R3.18AL Outcome A\n- exact receipt-bound head `{AL_HEAD}`; published AK/direct header exact 47/47; AJ contexts 17/17; Int=47; mismatch 0; witness reselection 0; payload/control consumption 0/0; artifact `{AL_ARTIFACT}`.\n\n## ACTIVE EVIDENCE GATE — R3.18AM\n- reuse exactly the immutable 47-row AL lane and begin at each proven AK `payload_start`;\n- independently measure exactly one Int-tagged payload against pinned Boxcars; production Rust frozen;\n- stop at the one measured payload end and consume zero bits of another property control.\n\n## CLOSED\n- post-AK payload production composition; another property control; false success semantics; alternate unadmitted layouts; repeated/generalized property loop or generic cursor;",
    "locks gate")
write(p, t)

# Progress ledger is append-only.
p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
t = read(p)
entry = f"""

---

## 2026-08-21 — R3.18AL — Published R3.18AK following-header differential

Production base SHA: `{PRODUCTION_SHA}`
Production commit SHA: unchanged; read-only evidence pass
Pass type: published-API differential
Outcome: **A — ADMITTED / CLOSED**

What changed:
- no production Rust/Cargo/fixture/corpus/support source changed;
- published R3.18AK was checked on exactly the immutable R3.18AI 47-row lane;
- R3.18AM is opened only as a separate one-payload evidence gate.

Evidence:
- receipt-bound evidence head/tree `{AL_HEAD}` / `{AL_TREE}`;
- authority `{AL_RUN}/{AL_JOB}` SUCCESS;
- natural same-head push CI `{AL_PUSH_CI}/{AL_PUSH_CI_JOB}` SUCCESS, count 1;
- exact-head PR CI `{AL_PR_CI}/{AL_PR_CI_JOB}` SUCCESS; PR #132 closed unmerged;
- artifact `{AL_ARTIFACT}` / `{AL_ARTIFACT_SIZE}` bytes / `sha256:{AL_ARTIFACT_DIGEST}`; independent ZIP digest exact and internal manifest 11/11 PASS;
- published AK exact 47/47; direct stateless header exact 47/47; AJ contexts 17/17; multiplicity 47/47; Int=47; mismatch 0; witness reselection 0;
- repeatability/truncation/corrupt-AG/wrong-actor/unresolved/wrong-version/post-payload poison 47/47; Cartesian/fabricated/old-Z and earlier-contract inheritance negatives PASS;
- following-payload/second-later-control consumption 0/0; privacy PASS.

Important receipt correction:
- an earlier PR-body artifact number was stale; the exact evidence-run API and independently downloaded ZIP establish artifact `{AL_ARTIFACT}` and digest `sha256:{AL_ARTIFACT_DIGEST}` as authority.

Boundaries opened:
- read-only R3.18AM investigation of exactly one payload beginning at the already-proven AK `payload_start`.

Boundaries still closed:
- payload production composition;
- another property-control bit;
- repeated/generalized property loop/cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

Next exact pass:
- `R3.18AM — post-R3.18AK one-payload evidence; measure rather than assume payload width and stop before another control.`
"""
if "## 2026-08-21 — R3.18AL — Published R3.18AK following-header differential" in t:
    raise SystemExit("ledger AL entry already exists")
write(p, t.rstrip() + entry + "\n")

# Knowledge graph: current graph, mandatory order, and current-status block only.
p = "MIMIR_KNOWLEDGE_GRAPH.md"
t = read(p)
t = replace_once(t,
    "R3.18AK bounded post-AG following-header production composition / CLOSED\nR3.18AL active published-AK following-header differential",
    "R3.18AK bounded post-AG following-header production composition / CLOSED\nR3.18AL published-AK following-header differential / Outcome A CLOSED\nR3.18AM active post-AK one-payload evidence",
    "kg graph")
t = replace_once(t,
    "112. `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`\n113. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n114. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n115. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n116. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n117. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n118. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n119. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "112. `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`\n113. `docs/continuity/MIMIR_R3_18AL_DECISION.md`\n114. `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md`\n115. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n116. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n117. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n118. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n119. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n120. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n121. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "kg mandatory order")
t = replace_once(t,
    "### R3.18AL published-AK following-header differential: ACTIVE\n- read-only; production frozen at R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145`\n- reuse exactly the immutable R3.18AI 47 rows, witness reselection 0\n- stop at payload_start; payload/control/loop/cursor widening remains closed",
    f"### R3.18AL published-AK following-header differential: OUTCOME A / CLOSED\n- evidence `{AL_HEAD}` / `{AL_TREE}`; run/job `{AL_RUN}/{AL_JOB}` SUCCESS; same-head push CI `{AL_PUSH_CI}/{AL_PUSH_CI_JOB}` SUCCESS count 1; PR CI `{AL_PR_CI}/{AL_PR_CI_JOB}` SUCCESS\n- artifact `{AL_ARTIFACT}` / `sha256:{AL_ARTIFACT_DIGEST}`; manifest 11/11; published AK/direct header 47/47; AJ contexts 17/17; Int=47; mismatch 0; witness reselection 0\n- payload/control consumption 0/0; production unchanged at R3.18AK `{PRODUCTION_SHA}`\n\n### R3.18AM post-AK one-payload evidence: ACTIVE\n- read-only; reuse exactly the immutable AL 47 rows and begin at proven AK payload_start\n- Int=47 is the header fact; payload width/value must be independently measured against pinned Boxcars\n- stop at one payload end; another-control/production/loop/cursor widening remains closed",
    "kg AL-AM status")
write(p, t)

print("R3_18AL_CONTINUITY_GENERATION=PASS")
