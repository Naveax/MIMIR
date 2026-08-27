from __future__ import annotations

import json
from pathlib import Path

DATE = "2026-08-27"
MAIN_SHA = "c49ce8f7b1e1145e5fb41a98dcaae9c5de61c37e"
PROD_SHA = "6a9f456c78ffccab177823234a8d9fe4ba59a850"
PROD_TREE = "cbda5db96e88cc208f872c2237cf4741b8fcfaef"
AV_HEAD = "fcbabd6953b4bade41f49b767f0dd73524e190d8"
AV_TREE = "922e7fb45de33b1803027e6cdcbbe55467a1bc2e"
AV_RUN = "33057596762"
AV_JOB = "98468171016"
AV_CI = "33057596712"
AV_CI_JOB = "98468756735"
AV_ARTIFACT = "9640472993"
AV_ARTIFACT_SIZE = "10256"
AV_DIGEST = "sha256:26082be08c8644a17076d9df2138128df110bbf39b4b3bceefdc823a9492d456"
AT_DIGEST = "3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5"
AS_HEAD = "475650fea59332f74b9f69da50e3e4471622ab7e"
AS_ARTIFACT = "9603335255"
AS_DIGEST = "sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45"
BOXCARS = "c70e77df7af81b436cb545d070bb90c82f562d0b"


def p(path: str) -> Path:
    return Path(path)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def write(path: str, text: str) -> None:
    p(path).write_text(text, encoding="utf-8", newline="\n")

# 1) Master continuity handbook: current state only + immutable closure receipt.
path = "MIMIR_CONTINUE_HERE.md"
text = p(path).read_text(encoding="utf-8")
text = replace_once(
    text,
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AS — one following-property-header evidence after published R3.18AQ mixed control / Outcome A / 47 frozen / false terminators 7 / true headers exact 40 / 16 exact contexts / Int=40 / mismatch 0 / artifact 9603335255",
    f"LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AV — published-R3.18AU mixed following-header differential / Outcome A / 47 frozen / false terminators 7 / true headers exact 40 / 16 exact contexts / multiplicity 40 / Int=40 / mismatch 0 / witness reselection 0 / payload-second-control 0/0 / artifact {AV_ARTIFACT}",
    "continue last read-only audit",
)
text = replace_once(
    text,
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AS — 47/47 frozen split preserved / false terminators 7/7 / true following headers exact 40/40 / 16 exact eight-field contexts / Int=40 / native-oracle mismatch 0 / witness reselection 0 / payload/second-control consumption 0/0 / artifact 9603335255",
    f"LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AV — published AU exact 47/47 / false terminators 7/7 / true following headers exact 40/40 / exact AT contexts 16/16 / multiplicity 40 / Int=40 / mismatch 0 / witness reselection 0 / payload/second-control consumption 0/0 / same-head CI {AV_CI} / artifact {AV_ARTIFACT}",
    "continue last evidence pass",
)
text = replace_once(
    text,
    "CURRENT_PASS:\n  R3.18AV — published-R3.18AU mixed following-header differential\n\nCURRENT_PASS_TYPE:\n  read-only published-production differential / replay the immutable 47-row AS/AT authority against published R3.18AU; preserve false=7 no-header terminators and true=40 exact one-header results; verify exact AT membership/boundaries and zero following-payload/second-control consumption; production mutation forbidden",
    "CURRENT_PASS:\n  R3.18AW — one following primitive payload evidence on exact AV-true rows\n\nCURRENT_PASS_TYPE:\n  read-only one-payload boundary evidence / rematerialize exactly the 40 R3.18AV true rows from the admitted AV artifact; exclude all 7 false terminators before payload decode; compare exactly one current primitive scalar against pinned Boxcars; stop at payload end with zero next-control consumption; production mutation forbidden",
    "continue current pass",
)
text = replace_once(
    text,
    "  R3.18AV ACTIVE read-only differential: compare published R3.18AU against the immutable 47-row AS/AT authority; require false=7, true=40, exact true headers 40/40, exact AT contexts/multiplicities, mismatch 0, and payload/second-control consumption 0/0\n  NO following payload or second later property-control bit after published R3.18AU, header on false terminators, contexts outside exact R3.18AT membership, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "  R3.18AV CLOSED Outcome A: published R3.18AU exact 47/47 on immutable AS/AT authority; false=7 no-header; true=40 exact headers; AT contexts 16/16; multiplicity 40; Int=40; mismatch/reselection 0/0; payload/second-control 0/0; artifact 9640472993\n  R3.18AW ACTIVE read-only evidence: inspect exactly one following primitive payload on only the 40 admitted AV-true rows; all 7 false terminators are excluded before payload decode; require native/Boxcars exact equality and stop at payload end\n  NO following-payload production composition, next property-control bit after the AW payload, payload access on AV-false rows, context outside exact AV/AT authority, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "continue frontier chain",
)
closure_marker = "\nR3_18AV_DIFFERENTIAL_CLOSURE:\n"
if closure_marker in text:
    raise SystemExit("continue AV closure already present")
text += f"""

R3_18AV_DIFFERENTIAL_CLOSURE:
Outcome A / read-only / production unchanged at {PROD_SHA} / tree {PROD_TREE}
evidence head/tree: {AV_HEAD} / {AV_TREE}
evidence run/job: {AV_RUN}/{AV_JOB} SUCCESS / same-head natural CI {AV_CI}/{AV_CI_JOB} SUCCESS / count=1 / rerun=0
artifact: {AV_ARTIFACT} / {AV_ARTIFACT_SIZE} bytes / {AV_DIGEST} / downloaded ZIP inner manifest PASS
published AU exact 47/47 / false=7 no-header / true=40 exact header / AT contexts 16/16 / multiplicity 40 / Int=40
mismatch 0 / witness reselection 0 / following payload bits 0 / second later control bits 0 / privacy PASS
negative controls PASS / production-Cargo-fixture-corpus-support mutation 0/0/0/0/0
next exact pass: R3.18AW one-following-primitive-payload evidence on exact forty AV-true rows only; all seven false rows excluded; next control remains closed
"""
write(path, text)

# 2) Knowledge graph: graph, mandatory reading order, current node.
path = "MIMIR_KNOWLEDGE_GRAPH.md"
text = p(path).read_text(encoding="utf-8")
text = replace_once(
    text,
    "R3.18AV published-R3.18AU mixed following-header differential / ACTIVE                                      |",
    "R3.18AV published-R3.18AU mixed following-header differential / Outcome A CLOSED                           |\nR3.18AW one following primitive payload evidence on exact AV-true rows / ACTIVE                                 |",
    "KG graph frontier",
)
text = replace_once(
    text,
    "133. `docs/continuity/MIMIR_R3_18AV_EXECUTION_SPEC.md`\n134. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n135. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n136. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n137. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n138. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n139. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n140. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "133. `docs/continuity/MIMIR_R3_18AV_EXECUTION_SPEC.md`\n134. `docs/continuity/MIMIR_R3_18AV_DECISION.md`\n135. `docs/continuity/MIMIR_R3_18AW_EXECUTION_SPEC.md`\n136. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n137. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n138. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n139. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n140. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n141. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n142. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "KG mandatory order tail",
)
text = replace_once(
    text,
    "### R3.18AV published-R3.18AU mixed following-header differential: ACTIVE\n- read-only on the immutable 47-row AS/AT authority; production remains `6a9f456c78ffccab177823234a8d9fe4ba59a850`\n- require published AU exact 47/47, false=7 no-header, true=40 exact headers, AT context/multiplicity equality, mismatch 0 and witness reselection 0\n- following payload and second later control remain unread; production/Cargo/fixture/corpus/support mutation forbidden\n- only Outcome A may open a separate R3.18AW one-following-payload evidence pass on the exact 40 true rows",
    f"### R3.18AV published-R3.18AU mixed following-header differential: OUTCOME A / CLOSED\n- evidence `{AV_HEAD}` / tree `{AV_TREE}`; run/job `{AV_RUN}/{AV_JOB}` SUCCESS\n- same-head natural CI `{AV_CI}/{AV_CI_JOB}` SUCCESS / count=1 / rerun=0\n- artifact `{AV_ARTIFACT}` / `{AV_ARTIFACT_SIZE}` bytes / `{AV_DIGEST}`; independently downloaded ZIP / inner manifest PASS\n- published AU exact 47/47; false=7 no-header; true=40 exact headers; exact AT contexts 16/16; multiplicity 40; Int=40\n- mismatch 0; witness reselection 0; following payload/second-control 0/0; negative/full validations PASS; privacy PASS\n- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; production remains `{PROD_SHA}`\n\n### R3.18AW one following primitive payload evidence: ACTIVE\n- read-only on exactly the 40 admitted AV-true rows; all 7 false terminators excluded before payload decoding\n- rematerialize current tag/boundary from the admitted AV artifact; historical AM/AN ordinal/value/boundary inheritance forbidden\n- compare one native primitive scalar against pinned Boxcars at current replay coordinates; require exact tag/start/end/width/lossless-value equality\n- stop at payload end; next property-control bit, production payload composition and generalized/repeated cursor remain closed",
    "KG AV/AW node",
)
write(path, text)

# 3) Boundary Locks: replace only current override block.
path = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
text = p(path).read_text(encoding="utf-8")
start_marker = "# 0. Current override — R3.18AU production / R3.18AV active"
end_marker = "\n---\n\n# 1. Status vocabulary"
start = text.find(start_marker)
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("boundary current override markers missing")
new_override = f"""# 0. Current override — R3.18AU production / R3.18AV closed / R3.18AW active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AU
- `{PROD_SHA}` / `{PROD_TREE}` remains canonical production;
- false stays a successful no-header terminator on the exact seven rows; true composes exactly one stateless following header under exact R3.18AT membership and stops at `payload_start`;
- no production mutation occurred in R3.18AV.

## CLOSED EVIDENCE — R3.18AV Outcome A
- evidence `{AV_HEAD}` / tree `{AV_TREE}` / run-job `{AV_RUN}/{AV_JOB}` SUCCESS;
- same-head natural CI `{AV_CI}/{AV_CI_JOB}` SUCCESS / count=1 / rerun=0;
- artifact `{AV_ARTIFACT}` / `{AV_ARTIFACT_SIZE}` bytes / `{AV_DIGEST}` / independently verified inner manifest;
- published AU exact 47/47; false=7 no-header; true=40 exact headers; exact AT contexts 16/16 / multiplicity 40 / Int=40;
- mismatch/reselection 0/0; following payload/second-control 0/0; negative controls and privacy PASS.

## CLOSED CONTRACT — R3.18AT Outcome A
- contract `sha256:{AT_DIGEST}`; exact_tuple_only / 16 complete eight-field tuples / multiplicity 40;
- all seven false rows remain outside header membership; AJ/Z/P inheritance and RL223 widening remain rejected.

## ACTIVE EVIDENCE GATE — R3.18AW
- exact input set is only the 40 AV-true rows rematerialized from the admitted AV artifact;
- all seven AV-false terminators are excluded before payload decoding;
- inspect exactly one current primitive scalar and compare native vs pinned Boxcars tag/start/end/width/lossless value;
- stop exactly at payload end with zero next-control access; production mutation forbidden.

## CLOSED
- following-payload production composition after R3.18AU;
- any payload access on the seven AV-false terminator rows;
- next property-control bit after the one R3.18AW payload evidence boundary;
- context/value/boundary inheritance from historical R3.18AM/R3.18AN;
- repeated/generalized property loop or generic cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
"""
text = text[:start] + new_override + text[end:]
write(path, text)

# 4) Machine continuity state.
path = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
data = json.loads(p(path).read_text(encoding="utf-8"))
if data.get("current_pass") != "R3.18AV":
    raise SystemExit(f"state expected AV current pass, got {data.get('current_pass')}")
data["updated_date"] = DATE
data["last_completed_read_only_audit"] = "R3.18AV"
data["current_pass"] = "R3.18AW"
data["current_pass_kind"] = "read-only one-following-primitive-payload evidence / exact R3.18AV true rows only"
data["current_pass_goal"] = "Rematerialize exactly the 40 R3.18AV true rows from the independently verified AV artifact, exclude all 7 false terminators before payload decoding, decode exactly one current primitive scalar at the proven AU header payload_start, require exact pinned-Boxcars equality, and stop at payload end with zero next-control consumption."
data["current_pass_stop_boundary"] = "Read-only. Stop exactly at the one decoded primitive payload end. No next property-control bit, no payload on AV-false rows, no following header after the payload, no generalized cursor, no production mutation, and no actor/frame/lifecycle/raw-state/event/skill/runtime widening."
closed = list(data.get("closed_now", []))
old_lock = "following payload after the one R3.18AU following header payload_start"
if closed.count(old_lock) != 1:
    raise SystemExit(f"state expected one AU payload lock, got {closed.count(old_lock)}")
closed[closed.index(old_lock)] = "production composition of the following payload after R3.18AU before a later production pass"
for item in [
    "payload evidence on any of the 7 R3.18AV false terminator rows",
    "next property-control bit after the one R3.18AW payload evidence boundary",
    "following header or another payload after the one R3.18AW payload evidence boundary",
    "historical R3.18AM/R3.18AN payload ordinal/value/boundary inheritance at R3.18AW",
]:
    if item not in closed:
        closed.append(item)
data["closed_now"] = closed
files = list(data.get("next_files_to_read", []))
anchor = "docs/continuity/MIMIR_R3_18AV_EXECUTION_SPEC.md"
if files.count(anchor) != 1:
    raise SystemExit("state AV spec anchor mismatch")
for new_file in ["docs/continuity/MIMIR_R3_18AV_DECISION.md", "docs/continuity/MIMIR_R3_18AW_EXECUTION_SPEC.md"]:
    if new_file in files:
        raise SystemExit(f"state file already present: {new_file}")
pos = files.index(anchor) + 1
files[pos:pos] = ["docs/continuity/MIMIR_R3_18AV_DECISION.md", "docs/continuity/MIMIR_R3_18AW_EXECUTION_SPEC.md"]
data["next_files_to_read"] = files
write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

# 5) Human current state, replaced deliberately because it is a short current-only document.
write("docs/continuity/MIMIR_CURRENT_STATE.md", f"""# MIMIR — Current Canonical State

**Continuity date:** {DATE}
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18AU — bounded post-AQ mixed-continuation following-header production`
**Last read-only evidence:** `R3.18AV — Outcome A / published AU exact 47/47 / false=7 / true=40 / AT contexts 16/16 / multiplicity 40 / Int=40 / artifact {AV_ARTIFACT}`
**Last completed contract:** `R3.18AT — exact_tuple_only / 16 eight-field contexts / multiplicity 40 / 7 false terminators outside membership / sha256:{AT_DIGEST}`
**Current exact pass:** `R3.18AW — one following primitive payload evidence on exact AV-true rows`

## Truthful boundary

R3.18AU remains canonical production. R3.18AV closed read-only Outcome A against the immutable AS/AT authority: all 47 published-AU results matched, including 7 successful no-header terminators and 40 exact one-header continuations. No payload or second later control was consumed and production remained unchanged.

```text
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
AV evidence head/tree                  {AV_HEAD} / {AV_TREE}
AV evidence run/job                    {AV_RUN} / {AV_JOB} SUCCESS
AV same-head CI                        {AV_CI} / {AV_CI_JOB} SUCCESS / count 1
AV artifact                            {AV_ARTIFACT} / {AV_ARTIFACT_SIZE} / {AV_DIGEST}
published AU exact                     47/47
false no-header terminators            7/7
true exact one-header rows             40/40
AT contexts / multiplicity             16/16 / 40
true tag distribution                  Int=40
mismatch / witness reselection         0 / 0
following payload / second control     0 / 0
production mutation                    0
```

## Current gate

R3.18AW is read-only. Rematerialize exactly the 40 AV-true rows from the admitted AV artifact, exclude all seven false rows before payload decoding, decode exactly one current primitive scalar at the proven payload boundary, independently compare it with pinned Boxcars, and stop exactly at payload end.

## Hard stop

No payload decoding on the seven false terminators, no next property-control bit after the AW payload, no following header/payload beyond that boundary, no historical AM/AN value or ordinal inheritance, no production mutation, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening.
""")

# 6) Next-chat handoff, current-only short document.
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", f"""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AU** at `{PROD_SHA}` / `{PROD_TREE}`. R3.18AV is now **CLOSED Outcome A** as a read-only differential; it did not mutate production.

R3.18AV authority: evidence `{AV_HEAD}` / tree `{AV_TREE}`; run/job `{AV_RUN}/{AV_JOB}` SUCCESS; same-head natural CI `{AV_CI}/{AV_CI_JOB}` SUCCESS with exact run count 1 and no rerun; artifact `{AV_ARTIFACT}` / `{AV_ARTIFACT_SIZE}` bytes / `{AV_DIGEST}`, independently downloaded with inner manifest PASS. Published AU matched 47/47: false=7 no-header, true=40 exact header, AT contexts 16/16, multiplicity 40, Int=40, mismatch/reselection 0/0, following-payload/second-control 0/0.

The active pass is **R3.18AW one-following-primitive-payload evidence**. Use only the exact 40 AV-true rows rematerialized from the admitted AV artifact. Exclude all 7 false rows before payload decoding. Use the current proven header tag/boundary, compare exactly one native scalar against pinned Boxcars at current replay coordinates, and stop at payload end with zero next-control access.

Do not inherit historical AM/AN property ordinal, payload boundaries or values; do not mutate production; do not read the next property-control bit; do not create a generic/repeated property loop. Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
""")

# 7) Append-only progress ledger.
path = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
text = p(path).read_text(encoding="utf-8")
heading = "## 2026-08-27 — R3.18AV — Published R3.18AU mixed following-header differential"
if heading in text:
    raise SystemExit("progress AV entry already exists")
text = text.rstrip() + f"""

---

{heading}
Production base SHA: `{PROD_SHA}`
Production commit SHA: unchanged (`{PROD_SHA}`)
Pass type: read-only published-production differential
Outcome: A / CLOSED

What changed:
- no production source changed;
- published R3.18AU was replayed against exactly the immutable R3.18AS/R3.18AT 47-row authority;
- false and true mixed-control branches were validated without witness reselection.

Evidence:
- evidence `{AV_HEAD}` / tree `{AV_TREE}`;
- run/job `{AV_RUN}/{AV_JOB}` SUCCESS;
- same-head natural CI `{AV_CI}/{AV_CI_JOB}` SUCCESS / count 1 / rerun 0;
- artifact `{AV_ARTIFACT}` / `{AV_ARTIFACT_SIZE}` bytes / `{AV_DIGEST}`; downloaded ZIP and inner manifest independently verified.

Validation:
- published AU exact 47/47;
- false=7 successful no-header terminators;
- true=40 exact one-header continuations;
- exact AT contexts 16/16 / multiplicity 40 / Int=40;
- mismatch 0 / witness reselection 0;
- following payload / second later control 0/0;
- negative controls, full library validation, same-head repository CI and privacy scan PASS.

Boundaries opened:
- read-only R3.18AW may inspect exactly one following primitive payload on only the 40 AV-true rows.

Boundaries still closed:
- payload access on the seven AV-false rows;
- following-payload production composition;
- next property-control bit after the AW payload;
- generic/repeated property cursor and all wider semantic/runtime layers.

Important negative facts / anti-regressions:
- historical R3.18AM/R3.18AN payload ordinal, positions and values are not current AW authority;
- R3.18AJ/Z/P context inheritance remains invalid at the AT/AV boundary;
- production/Cargo/fixture/corpus/support mutation was 0/0/0/0/0.

Next exact pass:
- R3.18AW — one following primitive payload evidence on exact forty AV-true rows only.
""" + "\n"
write(path, text)

# 8) AV decision.
decision_path = p("docs/continuity/MIMIR_R3_18AV_DECISION.md")
if decision_path.exists():
    raise SystemExit("AV decision already exists")
decision = f"""# MIMIR R3.18AV — Published R3.18AU Mixed Following-Header Differential Decision

**Date:** {DATE}
**Outcome:** **A — CLOSED / READ-ONLY ADMITTED**
**Canonical production remains:** `{PROD_SHA}` / `{PROD_TREE}`
**Production mutation:** none

## Decision

R3.18AV closes Outcome A. Published R3.18AU matches the immutable R3.18AS/R3.18AT 47-row authority exactly. All seven AQ-false rows remain successful no-header terminators. All forty AQ-true rows expose exactly the frozen following header under exact R3.18AT membership and stop at `payload_start`. No following payload or second later property-control bit is consumed.

This is a read-only differential admission, not a production payload admission. It opens only a separate R3.18AW evidence pass over exactly the forty true rows.

## Exact authority and receipts

```text
canonical main                         {MAIN_SHA}
canonical production SHA/tree          {PROD_SHA} / {PROD_TREE}
AV evidence head/tree                  {AV_HEAD} / {AV_TREE}
AV evidence run/job                    {AV_RUN} / {AV_JOB} SUCCESS
AV same-head natural CI                {AV_CI} / {AV_CI_JOB} SUCCESS
same-head CI count / rerun             1 / 0
AV artifact                            {AV_ARTIFACT} / {AV_ARTIFACT_SIZE} bytes
AV artifact digest                     {AV_DIGEST}
AS evidence head/artifact              {AS_HEAD} / {AS_ARTIFACT}
AS artifact digest                     {AS_DIGEST}
AT contract sha256                     {AT_DIGEST}
pinned Boxcars                         {BOXCARS}
```

The AV artifact was independently downloaded after workflow completion. Its internal `r3_18av_artifact_sha256.txt` verified every included file. The aggregate, authority receipt, negative-control receipt and same-head CI receipt all matched the values above.

## Admitted differential result

```text
frozen rows                            47/47
published R3.18AU exact                47/47
false no-header terminators            7/7
true exact following headers           40/40
exact AT contexts                      16/16
AT multiplicity                        40
observed tag                           Int=40
mismatch                               0
witness reselection                    0
following payload bits consumed        0
second later control bits consumed     0
production/Cargo/fixture/corpus/support 0/0/0/0/0
privacy                                PASS
```

## Negative controls

False-terminator post-stop poison, true-header truncation, post-`payload_start` poison isolation, wrong actor, unresolved lookup, wrong exact context, mismatched prerequisite, RL223 widening, component/Cartesian/versionless widening, AJ-valid-but-AT-absent membership, fabricated seventeenth tuple and source-scope zero-payload-decoder controls all passed.

## Hard stop

R3.18AV does not admit following-payload production, any payload on the seven false terminators, a next property-control bit, a following header/payload after that scalar, context widening, historical AM/AN payload inheritance, a generalized/repeated property cursor, or wider actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior.

## Next gate

R3.18AW is a separate read-only one-payload evidence pass. It must rematerialize exactly the forty AV-true rows from the admitted AV artifact, use each current proven header tag/boundary, independently compare one primitive scalar with pinned Boxcars, and stop at payload end with zero next-control consumption. All seven false rows remain outside the payload lane.
"""
write(str(decision_path), decision)

# 9) AW execution spec.
aw_path = p("docs/continuity/MIMIR_R3_18AW_EXECUTION_SPEC.md")
if aw_path.exists():
    raise SystemExit("AW spec already exists")
aw = f"""# MIMIR R3.18AW — One Following Primitive Payload Evidence

**Status:** ACTIVE
**Pass type:** read-only one-payload boundary evidence
**Production authority:** R3.18AU `{PROD_SHA}` / `{PROD_TREE}`
**Direct row authority:** admitted R3.18AV artifact `{AV_ARTIFACT}` / `{AV_DIGEST}`
**Production mutation:** forbidden
**Next property-control bit:** forbidden
**Witness reselection:** forbidden

## Goal

On exactly the forty R3.18AV true continuation rows, reconstruct the published prerequisites through R3.18AU, require exact equality with the admitted AV following-header row, decode exactly one current primitive scalar beginning at the proven `payload_start_bit`, independently measure the same scalar with pinned Boxcars at the same current replay coordinates, require exact native/oracle equality, and stop at payload end.

All seven AV-false terminators are excluded before payload decoding and remain no-header/no-payload terminators.

## Frozen authority

```text
AV evidence head/tree                  {AV_HEAD} / {AV_TREE}
AV run/job                             {AV_RUN} / {AV_JOB} SUCCESS
AV same-head CI                        {AV_CI} / {AV_CI_JOB} SUCCESS / count 1
AV artifact                            {AV_ARTIFACT} / {AV_ARTIFACT_SIZE} / {AV_DIGEST}
AV row split                           false=7 / true=40
AV exact AT contexts / multiplicity    16 / 40
AV observed header tags                Int=40
AT contract                            sha256:{AT_DIGEST}
AS source artifact                     {AS_ARTIFACT} / {AS_DIGEST}
pinned Boxcars                         {BOXCARS}
```

The admitted AV artifact, not historical R3.18AM/R3.18AN payload evidence, is the direct AW row authority.

## No historical value inheritance

R3.18AM/R3.18AN are methodology references only. AW must not inherit historical property ordinal `4`, historical payload start/end positions, historical semantic values, a fixed following-header width, or a historical tag merely because an earlier boundary was `Int`.

Current AV observes `Int=40`, but AW still rematerializes the tag and boundary from the admitted AV artifact. Expected `payload_start_bit` must not be used as an oracle selector input.

## Exact target materialization

- consume all 47 admitted AV rows in frozen order;
- require exactly 7 false rows with no following-header fields and exclude them before payload decode;
- require exactly 40 true rows with complete current header fields;
- require `control_end == stream_start` and `header_stop_bit == payload_start_bit`;
- require exact R3.18AT context multiset equality: 16 contexts / multiplicity 40;
- preserve replay identity, frame index, actor ordinal, actor object, control/header coordinates and version context;
- witness reselection = 0.

## Native one-scalar evidence

Use published `decode_replay_network_primitive_scalar_v1` only after published R3.18AU has been reconstructed and its following header has matched the admitted AV row.

Before payload read require requested payload start equal the proven AU header stop, requested tag equal the proven resolved header tag, and the tag belong to the production primitive scalar family. Production widths are Boolean=1, Byte=8, Enum=11, Float=32, Int=32 and Int64=64; unsupported/compound tags reject before payload read.

Require `payload_end_bit == payload_start_bit + payload_width` and stop there.

## Independent Boxcars oracle

Pin Boxcars exactly at `{BOXCARS}`. Target selection may use only current replay coordinates: frame index, actor ordinal, actor context object id, and current property-present start bit. Property ordinal is diagnostic only. Expected payload start is an oracle output, never selector input.

For exactly one matched property per target record property/header coordinates, observed tag, version context, payload start/end/width and a lossless primitive value.

## Native/oracle equality

Require exactly 40 native rows and exactly 40 oracle rows with identical frozen labels. For every row require exact equality of frame/actor identity, property-present boundary, stream identity/bounds, property object, tag, version context, payload start, payload end, payload width and lossless primitive value. Mismatch = 0.

## Required negative controls

- all 7 false rows absent from the payload target table and never invoke a payload decoder;
- repeat native scalar decode and require exact equality 40/40;
- truncate inside scalar payload -> atomic reject 40/40;
- request a tag different from the proven header tag -> reject before payload read 40/40;
- request `payload_start + 1` -> reject before payload read 40/40;
- mutate bits beginning at payload end -> decoded scalar unchanged 40/40;
- corrupt/mismatch published AU/header prerequisite -> reject;
- wrong actor, unresolved lookup, wrong exact context and RL223 widening remain rejected by the published prerequisite chain;
- AT component-only/Cartesian/versionless/AJ-only/fabricated-context widening remains rejected;
- source-scope guard proves one scalar decode only, no next-control decoder and no generalized/repeated property loop.

## Validation

Require independently verified AV artifact identity/digest/inner manifest; exact target materialization 40/40 with false excluded 7/7; replay identity 40/40; native payload rows 40/40; Boxcars rows 40/40; native/oracle mismatch 0; repeatability/truncation/wrong-tag/wrong-boundary/post-payload-poison 40/40 each; witness reselection 0; next-control consumption 0; focused regressions PASS; full fmt/check/test/clippy/repository verifier PASS; unique same-head normal CI SUCCESS; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## Hard stop

No next property-control bit, no following header after this payload, no second payload, no generalized property loop/cursor, no next actor/frame/lifecycle, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
All exact forty current AV-true rows produce one native primitive scalar exactly matching pinned independent Boxcars; all negatives/full validation pass; false terminators remain excluded; next-control consumption is zero. A separate later pass may then investigate exactly one next property-control bit.

### Outcome B
A narrower exact payload subset is isolated without witness reselection or context/value inheritance. Record only that exact subset and keep the next control closed.

### Outcome C
Authority drift, false-row payload access, current-header mismatch, native/oracle mismatch, unsupported current tag, payload over-read, next-control access, production mutation, generic chaining or privacy failure. Stop without widening.
"""
write(str(aw_path), aw)

print("R3_18AV_ADMISSION_GENERATOR=PASS")
