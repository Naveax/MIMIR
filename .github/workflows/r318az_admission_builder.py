from __future__ import annotations

import json
import re
from pathlib import Path

MAIN_SHA = "d12b7662a61571ecb43109ebbc753b790d37b6ad"
MAIN_TREE = "b90fb38e7e16bfd3948219856eef29f9ac1bb8f2"
PROD_SHA = "2558cc0559422a3e6695e1501f20d96d83b23e6d"
PROD_TREE = "93198ad2a4f929ac62b87beddbc9d5b5665f08d1"
EVIDENCE_HEAD = "f46479faa2b230f7fde474f7f7696a1024420879"
EVIDENCE_TREE = "0d022d27fda2275de9512d96231979e1d016491e"
EVIDENCE_RUN = "33086674062"
EVIDENCE_JOB = "98568084290"
EVIDENCE_CI_RUN = "33086674797"
EVIDENCE_CI_JOB = "98568087263"
ARTIFACT_ID = "9652520412"
ARTIFACT_SIZE = "18151"
ARTIFACT_DIGEST = "558c709e242d74150755565d07c7968853abad0a1de6c5f49cd8f5920e7f9fc4"

AW_HEAD = "5f1d983a7b67f84293f337f23b7e7c25fee48795"
AW_ARTIFACT = "9643254651"
AW_DIGEST = "9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc"
AX_HEAD = "465a3f2fc71e5eed6f00c16a04738031bef8d82c"
AX_ARTIFACT = "9644869549"
AX_DIGEST = "32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9"
AT_CONTRACT = "3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5"
BOXCARS = "c70e77df7af81b436cb545d070bb90c82f562d0b"

def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def write(path: str, text: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8", newline="\n")

def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)

def sub_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    out, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one regex match, found {count}")
    return out

def replace_section(text: str, start_marker: str, end_marker: str, replacement: str, label: str) -> str:
    start = text.find(start_marker)
    if start < 0:
        raise SystemExit(f"{label}: start marker missing")
    end = text.find(end_marker, start)
    if end < 0:
        raise SystemExit(f"{label}: end marker missing")
    return text[:start] + replacement.rstrip() + "\n" + text[end:]

# 1) MIMIR_CONTINUE_HERE.md
p = "MIMIR_CONTINUE_HERE.md"
s = read(p)
s = sub_once(
    s,
    r"LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3\.18AX — .*?\n\n",
    f"LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AZ — published-R3.18AY one-following-payload differential / Outcome A / published AY exact 40/40 against immutable AW/native oracle / Int=40 / width32=40 / semantic range 5..300 / false terminators rejected 7/7 / mismatch 0 / witness reselection 0 / AX control consumption 0 / evidence run {EVIDENCE_RUN} / artifact {ARTIFACT_ID}\n\n",
    "continue last audit",
)
s = sub_once(
    s,
    r"LAST_COMPLETED_EVIDENCE_PASS:\n  R3\.18AX — .*?\n\n",
    f"LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AZ — published AY/AW/native exact 40/40 / Int=40 / width32=40 / values 1x5 + 39x300 / false terminators rejected 7/7 / repeatability PASS / mismatch 0 / witness reselection 0 / post-stop poison PASS / AX control consumption 0 / same-head CI {EVIDENCE_CI_RUN} / artifact {ARTIFACT_ID}\n\n",
    "continue last evidence",
)
s = replace_once(
    s,
    "CURRENT_PASS:\n  R3.18AZ — published-R3.18AY one-following-payload differential\n\nCURRENT_PASS_TYPE:\n  read-only published-production differential / compare published R3.18AY against exactly the immutable 40-row R3.18AW payload authority, require exact Int/32 boundary and value identity with mismatch 0 and deterministic repeatability, and stop at payload end with zero R3.18AX following-control consumption; production mutation forbidden",
    "CURRENT_PASS:\n  R3.18BA — bounded post-R3.18AY mixed following-control production\n\nCURRENT_PASS_TYPE:\n  bounded production implementation / from one exact valid R3.18AY payload result, validate/recompute the AY/AW authority, begin exactly at payload end, consume exactly one R3.18AX-admitted property_present bit, preserve both false and true as valid mixed semantics, and stop one bit later; no following stream/header/payload/second-control access and no generalized cursor",
    "continue current pass",
)
s = replace_once(
    s,
    "  R3.18AZ ACTIVE read-only differential: compare published R3.18AY against exactly the 40 immutable AW payload witnesses; require exact Int/32 boundary/value identity, mismatch/reselection 0/0, repeatability PASS, and AX control consumption 0\n  NO production consumption of the AX-observed control bit, payload/control access on AV-false rows, next stream/header/payload, second later property-control bit, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    f"  R3.18AZ CLOSED Outcome A: published R3.18AY exact 40/40 on immutable AW/native authority; Int=40; width32=40; semantic range 5..300; false terminators rejected 7/7; mismatch/reselection 0/0; repeatability/post-stop poison PASS; AX control consumption 0; artifact {ARTIFACT_ID}\n  R3.18BA ACTIVE bounded production: after one exact valid R3.18AY payload result, validate/recompute AY/AW authority, consume exactly one AX-admitted property_present bit at payload end, accept both false and true, and stop one bit later\n  NO control access on the seven AV/AU false terminators, next stream/header/payload after the BA control, second later property-control bit, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted",
    "continue hard stop",
)
closure = f"""
R3_18AZ_DIFFERENTIAL_CLOSURE:
Outcome A / read-only differential complete / production unchanged {PROD_SHA} / tree {PROD_TREE}
continuity base: {MAIN_SHA} / tree {MAIN_TREE}
evidence head/tree: {EVIDENCE_HEAD} / {EVIDENCE_TREE}
authority run/job: {EVIDENCE_RUN}/{EVIDENCE_JOB} SUCCESS / same-head natural CI {EVIDENCE_CI_RUN}/{EVIDENCE_CI_JOB} SUCCESS / attempt 1 / rerun 0
artifact: {ARTIFACT_ID} / {ARTIFACT_SIZE} bytes / sha256:{ARTIFACT_DIGEST} / downloaded ZIP digest exact / inner manifest 13/13 PASS
R3.18AW authority: {AW_HEAD} / artifact {AW_ARTIFACT} / sha256:{AW_DIGEST}
R3.18AX evidence: {AX_HEAD} / artifact {AX_ARTIFACT} / sha256:{AX_DIGEST} / false=37 true=3 / evidence-only before BA
published AY/AW/native exact 40/40 / Int=40 / width32=40 / semantic 1x5 + 39x300 / mismatch 0 / witness reselection 0
false terminators rejected 7/7 / deterministic repeatability PASS / post-stop poison PASS / AX control bits consumed 0
production-Cargo-fixture-corpus-support mutation 0/0/0/0/0 / privacy PASS
next exact pass: R3.18BA bounded post-R3.18AY mixed following-control production; consume one AX-admitted bit only and stop one bit later
""".strip()
if "R3_18AZ_DIFFERENTIAL_CLOSURE:" in s:
    raise SystemExit("continue AZ closure already present")
s = s.rstrip() + "\n\n" + closure + "\n"
write(p, s)

# 2) MIMIR_KNOWLEDGE_GRAPH.md
p = "MIMIR_KNOWLEDGE_GRAPH.md"
s = read(p)
s = replace_once(
    s,
    "R3.18AZ published-R3.18AY one-following-payload differential / ACTIVE                                            |",
    "R3.18AZ published-R3.18AY one-following-payload differential / Outcome A CLOSED                                 |\nR3.18BA bounded post-R3.18AY mixed following-control production / ACTIVE                                             |",
    "knowledge active lane",
)
old_order = """137. `docs/continuity/MIMIR_R3_18AX_EXECUTION_SPEC.md`
138. `docs/continuity/MIMIR_R3_18AX_DECISION.md`
139. `docs/continuity/MIMIR_R3_18AY_EXECUTION_SPEC.md`
140. `docs/continuity/MIMIR_R3_18AY_DECISION.md`
141. `docs/continuity/MIMIR_R3_18AZ_EXECUTION_SPEC.md`
142. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
143. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
144. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
145. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
146. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
147. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
148. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
new_order = """137. `docs/continuity/MIMIR_R3_18AX_EXECUTION_SPEC.md`
138. `docs/continuity/MIMIR_R3_18AX_DECISION.md`
139. `docs/continuity/MIMIR_R3_18AY_EXECUTION_SPEC.md`
140. `docs/continuity/MIMIR_R3_18AY_DECISION.md`
141. `docs/continuity/MIMIR_R3_18AZ_EXECUTION_SPEC.md`
142. `docs/continuity/MIMIR_R3_18AZ_DECISION.md`
143. `docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md`
144. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
145. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
146. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
147. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
148. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
149. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
150. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
s = replace_once(s, old_order, new_order, "knowledge mandatory order")
kg_append = f"""
### R3.18AZ published-R3.18AY one-following-payload differential: OUTCOME A / CLOSED
- production unchanged `{PROD_SHA}` / tree `{PROD_TREE}`; continuity base `{MAIN_SHA}` / `{MAIN_TREE}`
- evidence `{EVIDENCE_HEAD}` / tree `{EVIDENCE_TREE}`; authority run/job `{EVIDENCE_RUN}/{EVIDENCE_JOB}` SUCCESS
- same-head natural CI `{EVIDENCE_CI_RUN}/{EVIDENCE_CI_JOB}` SUCCESS; attempt 1; rerun 0
- artifact `{ARTIFACT_ID}` / {ARTIFACT_SIZE} bytes / `sha256:{ARTIFACT_DIGEST}`; downloaded ZIP digest exact and inner manifest 13/13 PASS
- immutable AW / published AY / direct-native exact 40/40; Int=40; width32=40; semantic distribution 1x5 + 39x300; mismatch/reselection 0/0
- all seven AU false terminators reject; deterministic repeatability and post-stop poison PASS; R3.18AX following-control consumption 0
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS

### R3.18BA bounded post-R3.18AY mixed following-control production: ACTIVE
- exact authority is the immutable 40-row R3.18AX lane after an exact valid R3.18AY payload result
- validate/recompute the AY/AW prior, begin exactly at payload end, consume exactly one LSB-first `property_present` bit, and stop one bit later
- preserve AX mixed semantics exactly: false=37 and true=3 are both valid successful results; do not inherit true-only behavior from older boundaries
- consume no following stream/header/payload or second later control; no control success on the seven AU false terminators; no generalized/repeated cursor
""".strip()
if "### R3.18AZ published-R3.18AY one-following-payload differential: OUTCOME A / CLOSED" in s:
    raise SystemExit("knowledge AZ closure already present")
s = s.rstrip() + "\n\n" + kg_append + "\n"
write(p, s)

# 3) Boundary locks current override.
p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
s = read(p)
override = f"""# 0. Current override — R3.18AY production / R3.18AZ closed / R3.18BA active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AY
- `{PROD_SHA}` / `{PROD_TREE}` remains canonical production;
- validates/recomputes exact R3.18AU true-header authority, decodes exactly one R3.18AW-admitted Int/32 payload, and stops at payload end;
- all seven AU false terminators reject before payload decode;
- production consumption of the R3.18AX following-control bit remains zero until R3.18BA is separately admitted.

## CLOSED DIFFERENTIAL — R3.18AZ Outcome A
- evidence `{EVIDENCE_HEAD}` / `{EVIDENCE_TREE}`; run/job `{EVIDENCE_RUN}/{EVIDENCE_JOB}` SUCCESS;
- same-head CI `{EVIDENCE_CI_RUN}/{EVIDENCE_CI_JOB}` SUCCESS; artifact `{ARTIFACT_ID}` / `sha256:{ARTIFACT_DIGEST}`;
- published AY / immutable AW / direct-native exact 40/40; Int=40; width32=40; semantic range 5..300; mismatch/reselection 0/0;
- seven false terminators reject, repeatability and post-stop poison pass, AX control consumption 0.

## CLOSED EVIDENCE — R3.18AX Outcome A
- exact AW payload reconstruction 40/40; one next `property_present` bit false=37 / true=3;
- pinned Boxcars/native exact 40/40, mismatch 0 and adjacent consumption 0/0/0/0;
- this mixed bit distribution is the only following-control authority R3.18BA may use.

## ACTIVE PRODUCTION GATE — R3.18BA
- operate only after one exact valid R3.18AY payload result on the 40-row AX-supported lane;
- validate/recompute exact AY/AW authority and require exact payload stop;
- consume exactly one AX-admitted control bit; both false and true are successful results;
- stop one bit later with zero next stream/header/payload/second-control consumption.

## CLOSED
- control access on any of the seven AU/AV false terminators;
- next stream/header/payload after the R3.18BA control;
- second later property-control bit;
- historical AP or older boolean distributions as BA authority;
- generalized/repeated property loop or generic cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
"""
s = replace_section(s, "# 0. Current override", "\n---\n\n# 1. Status vocabulary", override, "boundary override")
write(p, s)

# 4) Machine-readable continuity state.
p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(read(p))
state["last_completed_read_only_audit"] = "R3.18AZ"
state["current_pass"] = "R3.18BA"
state["current_pass_kind"] = "bounded production implementation / exact one R3.18AX-admitted mixed property_present bit after a validated R3.18AY payload end"
state["current_pass_goal"] = "From an exact valid R3.18AY payload result, validate/recompute exact AY/AW authority, begin exactly at payload end, consume exactly one R3.18AX-admitted property_present bit, preserve false=37/true=3 semantics, and stop one bit later."
state["current_pass_stop_boundary"] = "Consume exactly one control bit only on the exact 40 AX-supported AY rows; accept both false and true; no control access on the seven AU false terminators, no next stream/header/payload, no second later control, no generalized cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening."
for item in [
    "next stream/header/payload after the R3.18BA one-bit production boundary",
    "second later property-control bit after R3.18BA",
    "generalized/repeated property loop or generic cursor after R3.18BA",
    "control success on the seven R3.18AU false terminators",
]:
    if item not in state["closed_now"]:
        state["closed_now"].append(item)
nfr = state.get("next_files_to_read", [])
needle = "docs/continuity/MIMIR_R3_18AZ_EXECUTION_SPEC.md"
if needle not in nfr:
    raise SystemExit("state mandatory AZ spec missing")
idx = nfr.index(needle) + 1
for item in ["docs/continuity/MIMIR_R3_18AZ_DECISION.md", "docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md"]:
    if item in nfr:
        raise SystemExit(f"state next_files already has {item}")
    nfr.insert(idx, item)
    idx += 1
state["next_files_to_read"] = nfr
write(p, json.dumps(state, indent=2, ensure_ascii=False) + "\n")

# 5) Current state.
current = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27  
**Repository:** `Naveax/MIMIR`  
**Canonical production SHA:** `{PROD_SHA}`  
**Production tree:** `{PROD_TREE}`  
**Production milestone:** `R3.18AY — bounded post-AU one-following-payload production`  
**Last completed read-only differential:** `R3.18AZ — Outcome A`  
**Current exact pass:** `R3.18BA — bounded post-R3.18AY mixed following-control production`

## R3.18AZ closure

R3.18AZ independently validated published R3.18AY against exactly the immutable 40-row R3.18AW payload authority and a direct-native oracle. Exact tag/start/end/width/value identity is 40/40 with `Int=40`, `width32=40`, semantic values `1x5 + 39x300`, mismatch 0 and witness reselection 0. All seven AU false terminators reject before payload use. Deterministic repeatability and post-stop poison isolation pass, and production consumed zero R3.18AX following-control bits.

```text
continuity base/tree       {MAIN_SHA} / {MAIN_TREE}
production SHA/tree        {PROD_SHA} / {PROD_TREE}
AZ evidence head/tree      {EVIDENCE_HEAD} / {EVIDENCE_TREE}
AZ evidence run/job        {EVIDENCE_RUN}/{EVIDENCE_JOB} SUCCESS
same-head natural CI       {EVIDENCE_CI_RUN}/{EVIDENCE_CI_JOB} SUCCESS
artifact                   {ARTIFACT_ID} / {ARTIFACT_SIZE} bytes
artifact SHA-256           {ARTIFACT_DIGEST}
AW authority/artifact      {AW_HEAD} / {AW_ARTIFACT}
AX authority/artifact      {AX_HEAD} / {AX_ARTIFACT}
AX mixed distribution      false=37 / true=3
```

The downloaded artifact ZIP matches GitHub's digest exactly and its inner manifest verifies all 13 payload files.

## Active R3.18BA boundary

R3.18BA may operate only after one exact valid R3.18AY payload result on the 40-row AX-supported lane. It must validate/recompute the AY/AW prior, begin exactly at payload end, read exactly one LSB-first `property_present` bit, preserve both AX-observed values as valid results, and stop one bit later.

False is admitted. True is admitted. Neither result authorizes a following stream ID or header in this pass.

## Hard stop

No control success on the seven AU false terminators, no next stream/header/payload after the BA control, no second later property-control bit, no historical AP distribution inheritance, no generalized/repeated property loop or generic cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

Before any dispatch or rerun, inspect queued/waiting/in-progress equivalent runs. Reuse an existing exact run ID. Rerun is never polling.
"""
write("docs/continuity/MIMIR_CURRENT_STATE.md", current)

# 6) Next-chat handoff.
handoff = f"""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AY** at `{PROD_SHA}` / `{PROD_TREE}`. R3.18AZ is **CLOSED Outcome A** as a read-only published-production differential; production code did not change.

R3.18AZ exact authority is `{EVIDENCE_HEAD}` / `{EVIDENCE_TREE}`, evidence run/job `{EVIDENCE_RUN}/{EVIDENCE_JOB}` SUCCESS, same-head natural CI `{EVIDENCE_CI_RUN}/{EVIDENCE_CI_JOB}` SUCCESS, artifact `{ARTIFACT_ID}` / `sha256:{ARTIFACT_DIGEST}`. Published AY matched the immutable AW/native payload authority 40/40 with Int=40, width32=40, values 1x5 + 39x300, mismatch/reselection 0/0, seven false terminators rejected, repeatability/post-stop poison PASS, and AX control consumption 0.

The active pass is **R3.18BA bounded post-R3.18AY mixed following-control production**. Reuse exactly the immutable R3.18AX 40-row authority. After validating/recomputing an exact R3.18AY payload prior, begin at payload end, consume exactly one `property_present` bit, accept both false=37 and true=3 as valid typed results, and stop one bit later.

Do not read a following stream/header/payload or second control bit. Do not touch the seven AU false terminators. Do not generalize into a repeated property cursor. Do not inherit the R3.18AP distribution.

Read `MIMIR_CONTINUE_HERE.md`, follow the mandatory order in `MIMIR_KNOWLEDGE_GRAPH.md`, then use `docs/continuity/MIMIR_R3_18AZ_DECISION.md` and `docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md` as the immediate gate.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
"""
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)

# 7) Progress ledger append.
p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
s = read(p)
ledger = f"""
## R3.18AZ — Published R3.18AY One-Following-Payload Differential — Outcome A / CLOSED

Date: 2026-08-27

Authority:
- canonical continuity base `{MAIN_SHA}` / tree `{MAIN_TREE}`;
- production unchanged `{PROD_SHA}` / tree `{PROD_TREE}`;
- evidence head `{EVIDENCE_HEAD}` / tree `{EVIDENCE_TREE}`;
- evidence run/job `{EVIDENCE_RUN}/{EVIDENCE_JOB}` SUCCESS;
- same-head natural CI `{EVIDENCE_CI_RUN}/{EVIDENCE_CI_JOB}` SUCCESS, attempt 1, rerun 0;
- artifact `{ARTIFACT_ID}` / {ARTIFACT_SIZE} bytes / `sha256:{ARTIFACT_DIGEST}`;
- downloaded ZIP digest exact; inner manifest 13/13 PASS.

Result:
- exact immutable AW rows 40/40;
- published AY / AW / direct-native exact 40/40;
- Int=40, width32=40, semantic distribution 1x5 + 39x300;
- all seven AU false terminators rejected;
- deterministic repeatability PASS;
- post-stop poison isolation PASS;
- mismatch 0, witness reselection 0;
- R3.18AX following-control consumption 0;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy PASS.

Next exact pass:
- `R3.18BA — bounded post-R3.18AY mixed following-control production`.
- Validate/recompute one exact R3.18AY payload prior, consume exactly one AX-admitted `property_present` bit at payload end, preserve both false=37 and true=3, and stop one bit later.
- No next stream/header/payload, second later control, false-terminator access or generalized cursor.
""".strip()
if "## R3.18AZ — Published R3.18AY One-Following-Payload Differential — Outcome A / CLOSED" in s:
    raise SystemExit("ledger AZ closure already present")
write(p, s.rstrip() + "\n\n" + ledger + "\n")

# 8) AZ decision.
decision = f"""# MIMIR R3.18AZ — Published R3.18AY One-Following-Payload Differential Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL COMPLETE**
**Production mutation:** none
**Canonical production remains:** `{PROD_SHA}` / `{PROD_TREE}`

## Decision

R3.18AZ closes Outcome A. Exactly the immutable forty R3.18AW payload witnesses were reused without reselection. Published R3.18AY, the frozen AW authority and an independent direct-native observer agree exactly on Int tag, payload start, payload end, 32-bit width and signed semantic value on 40/40 rows. The semantic distribution is one value `5` and thirty-nine values `300`.

All seven R3.18AU false terminators remain outside the payload lane and reject before payload use. Repeated evaluation is deterministic. Post-payload poison, including the R3.18AX following-control bit, leaves the published AY result unchanged. No R3.18AX control bit was consumed.

## Exact authority

```text
continuity base/tree                  {MAIN_SHA} / {MAIN_TREE}
canonical production SHA/tree        {PROD_SHA} / {PROD_TREE}
evidence head/tree                    {EVIDENCE_HEAD} / {EVIDENCE_TREE}
authority run/job                     {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
same-head natural CI                  {EVIDENCE_CI_RUN} / {EVIDENCE_CI_JOB} SUCCESS
run attempts / reruns                 1 / 0
artifact                              {ARTIFACT_ID} / {ARTIFACT_SIZE} bytes
artifact digest / downloaded ZIP      sha256:{ARTIFACT_DIGEST}
R3.18AW head/artifact                 {AW_HEAD} / {AW_ARTIFACT}
R3.18AW artifact digest               sha256:{AW_DIGEST}
R3.18AX head/artifact                 {AX_HEAD} / {AX_ARTIFACT}
R3.18AX artifact digest               sha256:{AX_DIGEST}
R3.18AT contract                      sha256:{AT_CONTRACT}
pinned Boxcars                        {BOXCARS}
```

The downloaded ZIP SHA-256 equals the GitHub artifact digest exactly. Its internal SHA-256 manifest covers and verifies all 13 evidence payload files.

## Differential result

```text
frozen AW payload rows                40/40
published R3.18AY exact               40/40
AW/direct-native exact                40/40
false terminators rejected            7/7
tag                                   Int=40
width                                 32 bits on 40/40
semantic distribution                 1x5 + 39x300
mismatch                              0
witness reselection                   0
deterministic repeatability           40/40 PASS
post-stop poison isolation            40/40 PASS
R3.18AX control bits consumed         0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                               PASS
```

## Boundary consequence

R3.18AZ validates the published R3.18AY payload boundary but does not widen production. The exact R3.18AX next-control evidence can now be considered by a separate bounded production pass. That authority is mixed: false=37 and true=3. Both classes are evidence-supported and neither may be discarded by copying a true-only rule from an older boundary.

## Hard stop

No control success on the seven AU false terminators, no next stream/header/payload after the one later control, no second later property-control bit, no historical R3.18AP boolean-distribution inheritance, no generalized/repeated property loop/cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18BA is a separate bounded production implementation. From one exact valid R3.18AY payload result it must validate/recompute the AY/AW prior, begin exactly at payload end, consume exactly one R3.18AX-admitted LSB-first `property_present` bit, return a boundary-specific typed result that accepts both false and true, and stop one bit later. It may not consume a following stream ID, header, payload or second control bit.
"""
write("docs/continuity/MIMIR_R3_18AZ_DECISION.md", decision)

# 9) BA execution spec.
spec = f"""# MIMIR R3.18BA — Bounded Post-R3.18AY Mixed Following-Control Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** `{PROD_SHA}` / `{PROD_TREE}`
**Evidence authority:** R3.18AX `{AX_HEAD}` / artifact `{AX_ARTIFACT}` / `sha256:{AX_DIGEST}`
**Published-prior validation:** R3.18AZ `{EVIDENCE_HEAD}` / `{EVIDENCE_RUN}/{EVIDENCE_JOB}` / artifact `{ARTIFACT_ID}`

## Goal

Publish exactly one boundary-specific composition after a valid R3.18AY payload. The API must validate/recompute the supplied AY prior, begin exactly at `prior.stop_bit`, consume exactly one `property_present` bit, represent both R3.18AX-observed values, and stop one bit later. It must read zero following stream/header/payload/second-control bits.

## Frozen evidence semantics

```text
AX-supported AY rows        40
false                       37
true                         3
published AY exact          40/40
oracle-native exact         40/40
mismatch                    0
witness reselection         0
adjacent consumption        0/0/0/0
AU false terminators         7 excluded
```

**Critical rule:** false is admitted. Do not copy true-only fail-closed behavior from R3.18M, R3.18W or R3.18AG, and do not inherit the R3.18AP false=7/true=40 distribution. The only BA boolean authority is the exact R3.18AX false=37/true=3 lane.

## Production contract

The new API must:
1. require enough prior authority to prevent arbitrary cursor advancement;
2. validate/recompute the supplied R3.18AY result against the exact AY/AW boundary;
3. require exact equality of the prior payload stop boundary;
4. reject every one of the seven AU false terminators before control access;
5. consume exactly one LSB-first control bit at the validated payload stop;
6. return a boundary-specific typed result containing the observed boolean and exact start/end/stop;
7. accept both false and true;
8. stop at `prior.stop_bit + 1`;
9. consume no next stream ID, header, payload or second later control;
10. fail atomically on malformed prior, out-of-range/truncated input, unresolved lookup or exact-context drift.

No generic chain cursor or repeated property loop is admitted.

## Required focused tests

At minimum:
- all 40 frozen R3.18AX rows exact, including exactly 37 false and 3 true witnesses;
- published R3.18AY prior recomputation exact on 40/40;
- all seven AU false terminators reject before control access;
- deterministic repeatability;
- truncation before the control bit rejects atomically;
- corrupt/mismatched AY prior rejects;
- wrong actor / unresolved lookup / wrong exact version-context rejects where prior reconstruction requires them;
- wrong payload tag/start/end authority rejects;
- exact control start/end/stop equality;
- post-stop poison invariance;
- false path succeeds and consumes no stream/header/payload;
- true path also stops before following stream/header;
- next stream/header/payload/second-control consumption 0/0/0/0;
- source-scope guard proving exactly one new control read and no generic loop.

## Clean candidate

Expected clean production scope is the minimum `crates/mimir-replay/src/lib.rs` change plus one focused `crates/mimir-replay/tests/r3_18ba_post_ay_following_control.rs` integration test. No workflow, temporary evidence helper, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup enters the clean production commit.

## Validation and publication

Require Rust 1.85 formatting, focused BA test, workspace check, clippy with warnings denied, workspace test, repository verifier, exact clean-candidate normal CI, fresh-main ancestry verification, force=false publication and published-main exact-SHA validation.

Before any dispatch or rerun, inspect queued/waiting/in-progress equivalent runs. If an equivalent run exists, reuse that run ID. Rerun is never polling. While CI runs, continue independent authority, scope and next-gate preparation.

## Hard stop

No control access on the seven AU false terminators, no following stream/header/payload after the one BA control bit, no second later control, no generalized/repeated property loop/cursor, no actor/frame/lifecycle advance, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
Publish the exact R3.18AX-admitted mixed false/true one-bit semantics with all focused/negative/full validations PASS and adjacent consumption 0/0/0/0. A later separate pass may differentially audit published BA before any following-header evidence.

### Outcome B
Only a narrower safe result representation can be implemented without violating the exact AX evidence. Publish only that narrower representation and keep every wider boundary closed.

### Outcome C
Authority drift, prior-boundary mismatch, rejection of an AX-admitted boolean class, false-terminator access, adjacent-bit access, generic chaining or validation contradiction. Stop without publication.
"""
write("docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md", spec)
