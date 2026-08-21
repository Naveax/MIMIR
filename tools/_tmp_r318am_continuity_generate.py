from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN = "fec9dca3cb8366108245788fc9a2b24a0c99fe94"
BASE_TREE = "3bf5f68ec7df5565f78f89fd4bc2254f2a64e010"
PROD_SHA = "f20f529e3ada6e9a671ea91e5676a17a00770145"
PROD_TREE = "98c675811cca4e4d7f0122c762f371548c9266c2"
LIB_BLOB = "a4001e631b306ba0297fb8a4abc97778f81659c2"
AK_TEST_BLOB = "9014505e1736498ee5e2ef7a1ce6118030580202"
AJ_CONTRACT = "cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c"
AM_HEAD = "842b94ed4c4e57323433585fea48116ecf18989b"
AM_TREE = "486d0a0f3833dcb8872f062ae1927c9aefde87ba"
AM_RUN = "32473716883"
AM_JOB = "96745647750"
AM_CI_RUN = "32474038136"
AM_CI_JOB = "96746590106"
AM_PR = "135"
AM_ARTIFACT = "9443581172"
AM_ARTIFACT_SIZE = "14827"
AM_DIGEST = "2f65de5207bd96787fd7d1527a55991f08d5da614a0ddfce22a7aa267968e3c8"
AM_ROWS_SHA = "4258d85092d9d7dbf003126938f7cf09d1fc10fa74d4c75f4a6e38e367f68576"
AM_SUMMARY_SHA = "0b56f8822655b88822fc5ff485d206fdf8e7b57d053983031b766e90f8628e04"
AM_NEG_SHA = "517979e9b2254d60d961b97170a2fe58372dfe42ec2703f1181087b51766db41"
AM_AGG_SHA = "629ac231df4df5dd7209d3449fda7e243facddf22a7fc80a230d128ffa4d8e9e"
AM_REPLAY_SHA = "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf"
BOXCARS = "c70e77df7af81b436cb545d070bb90c82f562d0b"
BUILDER_RUN = os.environ.get("R318AM_BUILDER_RUN", "UNSET")
BUILDER_JOB = os.environ.get("R318AM_BUILDER_JOB", "UNSET")
if "UNSET" in (BUILDER_RUN, BUILDER_JOB):
    raise SystemExit("missing builder receipt")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one marker, got {count}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    out, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one regex match, got {count}")
    return out


# Durable decision.
decision = f"""# MIMIR R3.18AM — Post-AK One Following-Payload Evidence Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / READ-ONLY PAYLOAD EVIDENCE**
**Production mutation:** none
**Canonical production:** `{PROD_SHA}` / `{PROD_TREE}`

## Decision

R3.18AM closes Outcome A. On exactly the immutable 47-row R3.18AI/R3.18AL lane, the published R3.18AK header boundary was reconstructed exactly and one following payload was decoded independently by the pinned Boxcars oracle and the existing narrow native primitive. Every observed payload is `Int`, every payload width is exactly 32 bits, native/oracle mismatch is zero, and witness reselection is zero.

R3.18AM stops exactly at one payload end and consumes zero bits of another property-control boundary. The 32-bit Int shape is admitted only for this post-AK boundary; it is not inherited from earlier payload passes by assumption.

## Exact authority

```text
canonical base main/tree             {BASE_MAIN} / {BASE_TREE}
production SHA/tree                  {PROD_SHA} / {PROD_TREE}
production lib / AK test blobs       {LIB_BLOB} / {AK_TEST_BLOB}
R3.18AJ contract                     sha256:{AJ_CONTRACT}
evidence head/tree                   {AM_HEAD} / {AM_TREE}
authority run/job                    {AM_RUN} / {AM_JOB} SUCCESS
same-head normal CI                  {AM_CI_RUN} / {AM_CI_JOB} SUCCESS
validation PR                        #{AM_PR} closed unmerged
artifact                             {AM_ARTIFACT} / {AM_ARTIFACT_SIZE} bytes
artifact digest / ZIP SHA-256        sha256:{AM_DIGEST}
payload rows SHA-256                 {AM_ROWS_SHA}
summary SHA-256                      {AM_SUMMARY_SHA}
negative controls SHA-256            {AM_NEG_SHA}
aggregate SHA-256                    {AM_AGG_SHA}
replay identity SHA-256              {AM_REPLAY_SHA}
pinned Boxcars                       {BOXCARS}
continuity builder                   {BUILDER_RUN} / {BUILDER_JOB}
```

The downloaded artifact ZIP SHA-256 equals the GitHub artifact digest exactly and its internal manifest verifies 11/11 payload entries.

## Frozen result

```text
frozen rows                          47/47
published R3.18AK exact              47/47
observed tags                        Int=47
observed payload width               32 bits on 47/47
semantic Int range                   1..415
native/oracle mismatch               0
witness reselection                  0
another control bits consumed        0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Negative controls

Repeatability, payload truncation, wrong-tag boundary guard, wrong payload-start boundary guard, wrong exact version/context, corrupt AG control, corrupt prior, and post-payload-end poison invariance pass on 47/47 rows. Earlier payload-contract inheritance is explicitly rejected.

## Superseded harness attempts

Earlier evidence heads failed only in temporary evidence tooling before payload admission: one Boxcars ordinal-4 insertion-marker defect and one missing Rust 1.85 `rustfmt` component. Neither is evidence authority and neither was rerun. The admitted authority is exact head `{AM_HEAD}` above.

## Hard stop

Production remains R3.18AK. No post-AK payload production exists until R3.18AN is separately implemented, validated and published. Another property-control bit, repeated/generalized property loops/cursors, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior remain closed.

## Next gate

R3.18AN is a separate bounded production implementation for exactly one post-AK `Int` payload of exactly 32 bits on the R3.18AM-admitted boundary. It must validate/recompute the supplied R3.18AK prior, require exact R3.18AJ membership, begin exactly at `payload_start`, reuse only the existing narrow primitive scalar decoder for `Int`, stop exactly at `payload_end`, and consume zero bits of the following property-control boundary.
"""

an_spec = f"""# MIMIR R3.18AN — Bounded Post-AK Following-Payload Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Evidence authority:** R3.18AM Outcome A
**Production parent:** R3.18AK `{PROD_SHA}` / `{PROD_TREE}`
**Admitted payload family:** `Int`, exactly 32 bits
**Another property-control bit:** forbidden

## 1. Goal

Publish exactly one boundary-specific post-AK payload composition. Starting only from a valid R3.18AK following-header result whose complete seven-field context remains admitted by R3.18AJ, decode exactly one 32-bit `Int` payload and stop exactly at its payload end.

## 2. Frozen authority

```text
canonical parent                     {BASE_MAIN} / {BASE_TREE}
production parent                    {PROD_SHA} / {PROD_TREE}
production lib / AK test blobs       {LIB_BLOB} / {AK_TEST_BLOB}
R3.18AJ exact-context contract       sha256:{AJ_CONTRACT}
R3.18AM evidence head/tree           {AM_HEAD} / {AM_TREE}
R3.18AM authority                    {AM_RUN} / {AM_JOB} SUCCESS
R3.18AM same-head CI                 {AM_CI_RUN} / {AM_CI_JOB} SUCCESS
R3.18AM artifact                     {AM_ARTIFACT} / {AM_ARTIFACT_SIZE} / sha256:{AM_DIGEST}
rows / observed tags                 47 / Int=47
payload width                        32 on 47/47
semantic Int range                   1..415
after-payload control consumption    0
witness reselection                  0
```

## 3. Production contract

The API must be explicitly tied to this post-AK boundary and must:

1. validate/recompute the supplied R3.18AK result rather than trust caller coordinates;
2. require exact R3.18AJ seven-field membership;
3. require the resolved tag to be exactly `Int`;
4. begin exactly at the validated R3.18AK `payload_start`;
5. decode exactly one payload with the existing narrow primitive scalar decoder;
6. require exact 32-bit width and preserve the typed Int value;
7. return exact payload start/end/width/value and stop exactly at payload end;
8. consume zero bits of the following `property_present` control.

No generic cursor or repeatedly-chainable loop surface is admitted.

## 4. Required focused tests

At minimum:

- representative frozen R3.18AM rows exact through payload end;
- direct lower-decoder equality for `Int`;
- deterministic repeatability;
- bit-exact payload truncation rejection;
- wrong actor / unresolved lookup rejection through prior recomputation;
- malformed or non-R3.18AJ header tuple rejection;
- wrong replay/version/context rejection;
- non-Int tag rejection even if a lower decoder can parse it;
- wrong payload-start / tampered prior rejection;
- post-stop poison invariance beginning at the following property-control bit;
- exact 32-bit width and exact stop equality;
- following-control consumption = 0;
- source-scope regression: one AK recomputation + one Int primitive payload decode, no control read, no loops.

Synthetic tests supplement, never replace, the frozen real-replay authority.

## 5. Clean candidate

Expected clean production scope is exactly the minimum `crates/mimir-replay/src/lib.rs` change plus one focused `crates/mimir-replay/tests/r3_18an_post_ak_payload.rs` test file. No workflow/helper, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup enters the production commit.

Validation requires Rust 1.85 format/check/test/clippy, focused and full `mimir-replay` tests, repository verification, exact clean-candidate CI, fresh-main ancestry verification, force-free fast-forward publication, and published-main exact-SHA validation. Equivalent active runs must be reused; rerun is not polling.

## 6. Hard stop

No next `property_present` bit, no second payload/header/control, no generalized property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/slice/skill/counterfactual/runtime/export widening.

## 7. Outcome gate

### Outcome A
Exactly one 32-bit Int payload is composed over the admitted boundary with all focused/negative/full validations PASS and following-control consumption 0. Publish only that bounded composition, then open R3.18AO as a separate published-production differential.

### Outcome B
Only a stricter subset can be implemented safely. Publish only that subset and rewrite AO around the actual production contract.

### Outcome C
Authority drift, context/tag widening, unexplained mismatch, later-control access, generic chaining or validation contradiction. Stop without publication.
"""

for path in ("docs/continuity/MIMIR_R3_18AM_DECISION.md", "docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md"):
    if (ROOT / path).exists():
        raise SystemExit(f"unexpected existing file: {path}")
write("docs/continuity/MIMIR_R3_18AM_DECISION.md", decision)
write("docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md", an_spec)

# Master continuation current-state block and hard-stop lines.
p = "MIMIR_CONTINUE_HERE.md"
t = read(p)
t = replace_once(t,
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AL — published R3.18AK following-header differential / Outcome A / 47/47 / 17 exact contexts / Int=47 / mismatch 0 / artifact 9442034802",
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AM — post-AK one following-payload evidence / Outcome A / 47/47 / Int=47 / width=32 / mismatch 0 / artifact 9443581172",
    "continue last audit")
t = replace_once(t,
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AL — published AK/frozen AI/direct header exact 47/47 / 17 contexts / Int=47 / mismatch 0 / payload-control 0/0 / artifact 9442034802",
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AM — one post-AK payload exact 47/47 / Int=47 / 32-bit=47 / mismatch 0 / another-control=0 / artifact 9443581172",
    "continue last evidence")
t = replace_once(t,
    "CURRENT_PASS:\n  R3.18AM — post-AK one following-payload evidence",
    "CURRENT_PASS:\n  R3.18AN — bounded post-AK following-payload production",
    "continue current pass")
t = replace_once(t,
    "CURRENT_PASS_TYPE:\n  read-only payload evidence / begin at validated R3.18AK payload_start, decode exactly one payload against pinned Boxcars/native evidence, stop at payload end, consume zero another-control bits",
    "CURRENT_PASS_TYPE:\n  bounded production implementation / validate exact R3.18AK prior + R3.18AJ membership, decode exactly one 32-bit Int payload, stop at payload_end, consume zero following-control bits",
    "continue pass type")
t = replace_once(t,
    "  R3.18AM ACTIVE read-only payload evidence: start exactly at R3.18AK payload_start on the same 47 rows; prove one payload independently; another-control consumption must remain 0",
    "  R3.18AM CLOSED Outcome A: one post-AK payload exact 47/47; Int=47; width 32 on 47/47; semantic range 1..415; native-oracle mismatch 0; witness reselection 0; another-control 0; artifact 9443581172\n  R3.18AN ACTIVE bounded production: from one valid R3.18AK header with exact R3.18AJ membership, decode exactly one 32-bit Int payload and stop at payload_end; following control remains closed",
    "continue active gate")
t = replace_once(t,
    "  NO post-AK payload production before R3.18AM evidence closure, another property control, alternate unadmitted payload layout, repeated/generalized property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "  NO following property control after R3.18AN payload, alternate/unadmitted payload layout, repeated/generalized property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "continue no widening")
closure = f"""R3_18AM_EVIDENCE_CLOSURE:
  Outcome A / read-only / production unchanged at {PROD_SHA}
  evidence head/tree: {AM_HEAD} / {AM_TREE}
  authority run/job: {AM_RUN}/{AM_JOB} SUCCESS
  same-head normal CI: {AM_CI_RUN}/{AM_CI_JOB} SUCCESS / PR #{AM_PR} closed unmerged
  artifact: {AM_ARTIFACT} / {AM_ARTIFACT_SIZE} bytes / sha256:{AM_DIGEST}; downloaded ZIP digest exact / inner manifest 11/11 PASS
  frozen rows 47/47 / published-AK exact 47/47 / Int=47 / payload width 32 on 47/47 / semantic Int range 1..415 / mismatch 0
  witness reselection 0 / another-control bits 0 / earlier payload-contract inheritance rejected
  repeatability/truncation/wrong-tag/wrong-start/wrong-context/corrupt-AG/corrupt-prior/post-payload poison 47/47 PASS
  production/Cargo/fixture/corpus/support mutation 0/0/0/0/0 / privacy PASS

"""
t = replace_once(t, "R3_18AL_EVIDENCE_CLOSURE:\n", closure + "R3_18AL_EVIDENCE_CLOSURE:\n", "continue AM closure")
write(p, t)

# Boundary locks: replace only newest override.
p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
t = read(p)
override = f"""# 0. Current override — R3.18AM closed / R3.18AN active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AK
- `{PROD_SHA}` / `{PROD_TREE}` remains canonical production;
- exact R3.18AJ membership; exactly one following header; stop at `payload_start`.

## CLOSED PAYLOAD EVIDENCE — R3.18AM Outcome A
- immutable 47-row lane; published-AK exact 47/47; `Int=47`; exactly 32 payload bits on 47/47;
- semantic Int range 1..415; mismatch 0; witness reselection 0; another-control consumption 0;
- artifact `{AM_ARTIFACT}` / `sha256:{AM_DIGEST}`; internal manifest 11/11 PASS.

## ACTIVE PRODUCTION GATE — R3.18AN
- validate/recompute the exact R3.18AK prior and exact R3.18AJ membership;
- decode exactly one 32-bit `Int` payload from `payload_start` and stop at `payload_end`;
- following property-control bit remains closed.

## CLOSED
- another property-control bit; payload tags/layouts outside exact R3.18AM evidence; repeated/generalized property loop or generic cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

---

# 1. Status vocabulary"""
t = regex_once(t, r"# 0\. Current override.*?# 1\. Status vocabulary", override, "boundary override", re.S)
write(p, t)

# Structured continuity state.
p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(read(p))
state["updated_date"] = "2026-08-21"
state["last_completed_read_only_audit"] = "R3.18AM"
state["current_pass"] = "R3.18AN"
state["current_pass_kind"] = "bounded production implementation / one post-AK 32-bit Int payload"
state["current_pass_goal"] = "Validate the exact R3.18AK/R3.18AJ prior, decode exactly one R3.18AM-admitted 32-bit Int payload, stop at payload_end, and consume zero following-control bits."
state["current_pass_stop_boundary"] = "Exactly one 32-bit Int payload after R3.18AK. No following property-control bit, repeated/generalized property loop/cursor, next actor/frame or semantic/runtime/export widening."
closed = state.setdefault("closed_now", [])
for item in [
    "post-R3.18AK payload tags or layouts outside the exact R3.18AM Int/32 evidence",
    "another property control after the R3.18AM payload end",
    "repeated/generalized property loop or generic cursor after R3.18AM",
]:
    if item not in closed:
        closed.append(item)
reads = state.setdefault("next_files_to_read", [])
for item in [
    "docs/continuity/MIMIR_R3_18AM_DECISION.md",
    "docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md",
]:
    if item not in reads:
        insert_at = reads.index("docs/continuity/MIMIR_PASS_PROTOCOL.md") if "docs/continuity/MIMIR_PASS_PROTOCOL.md" in reads else len(reads)
        reads.insert(insert_at, item)
write(p, json.dumps(state, indent=2, ensure_ascii=False) + "\n")

# Current-state summary.
current = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-21
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18AK — bounded post-AG following-header production composition`
**Last read-only evidence:** `R3.18AM — Outcome A / 47/47 / Int=47 / payload width 32 / mismatch 0 / artifact {AM_ARTIFACT}`
**Last contract:** `R3.18AJ — Outcome A / exact_tuple_only / 17 contexts / multiplicity 47 / sha256:{AJ_CONTRACT}`
**Current exact pass:** `R3.18AN — bounded post-AK following-payload production`

## Truthful boundary

R3.18AK remains published production and stops at one admitted following-header `payload_start`. R3.18AL proved that header composition. R3.18AM then independently proved exactly one following payload on all 47 frozen rows: `Int=47`, width 32 on 47/47, semantic range 1..415, native/oracle mismatch 0, witness reselection 0 and another-control consumption 0.

```text
R3.18AM evidence                    {AM_RUN}/{AM_JOB} SUCCESS
R3.18AM same-head CI                {AM_CI_RUN}/{AM_CI_JOB} SUCCESS
R3.18AM validation PR               #{AM_PR} closed unmerged
R3.18AM artifact                    {AM_ARTIFACT} / {AM_ARTIFACT_SIZE} / sha256:{AM_DIGEST}
production mutation                 0
another-control consumption         0
```

## Current gate

R3.18AN is bounded production. Validate/recompute exact R3.18AK authority and R3.18AJ tuple membership, decode exactly one 32-bit `Int` payload using the existing narrow primitive scalar machinery, and stop at payload end.

## Hard stop

The following property-control bit, any payload layout/tag outside exact R3.18AM evidence, generalized/repeated property iteration/cursor, next actor/frame/lifecycle and raw-state/event/slice/skill/counterfactual/runtime/export behavior remain closed.
"""
write("docs/continuity/MIMIR_CURRENT_STATE.md", current)

handoff = f"""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AK** at `{PROD_SHA}` / `{PROD_TREE}`. R3.18AM is now **Outcome A / CLOSED** read-only payload evidence: head `{AM_HEAD}`, run/job `{AM_RUN}/{AM_JOB}` SUCCESS, same-head CI `{AM_CI_RUN}/{AM_CI_JOB}` SUCCESS, PR #{AM_PR} closed unmerged, artifact `{AM_ARTIFACT}` / `sha256:{AM_DIGEST}` independently downloaded and internally verified 11/11.

Frozen AM result: 47/47 published-AK exact; `Int=47`; payload width 32 on 47/47; semantic Int range 1..415; native/oracle mismatch 0; witness reselection 0; another-control bits 0; all required negatives 47/47 PASS; earlier payload-contract inheritance rejected; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.

The active pass is **R3.18AN**, bounded production. Recompute/validate the supplied R3.18AK result, require exact R3.18AJ context membership, decode exactly one 32-bit Int payload from `payload_start`, stop exactly at payload end, and consume zero following-control bits. No generic cursor or repeated loop.

Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json`, `docs/continuity/MIMIR_R3_18AK_DECISION.md`, `docs/continuity/MIMIR_R3_18AL_DECISION.md`, `docs/continuity/MIMIR_R3_18AM_DECISION.md`, and `docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md` before widening.
"""
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)

# Progress ledger: append immutable closure only once.
p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
t = read(p).rstrip()
marker = "## R3.18AM — post-AK one following-payload evidence"
if marker in t:
    raise SystemExit("AM ledger entry already exists")
t += f"""\n\n{marker}\n\n- Status: **Outcome A / CLOSED / read-only**.\n- Production unchanged: `{PROD_SHA}` / `{PROD_TREE}`.\n- Evidence: `{AM_HEAD}` / `{AM_RUN}/{AM_JOB}` SUCCESS.\n- Same-head CI: `{AM_CI_RUN}/{AM_CI_JOB}` SUCCESS; PR #{AM_PR} closed unmerged.\n- Artifact: `{AM_ARTIFACT}` / {AM_ARTIFACT_SIZE} bytes / `sha256:{AM_DIGEST}`; downloaded ZIP exact; internal manifest 11/11 PASS.\n- Frozen 47/47 published-AK exact; `Int=47`; width 32 on 47/47; semantic range 1..415; mismatch 0; witness reselection 0; another-control consumption 0.\n- Required negatives 47/47 PASS; earlier payload-contract inheritance rejected.\n- Next exact pass: **R3.18AN**, bounded one-payload production only.\n"""
write(p, t + "\n")

# Knowledge graph: current graph edge, mandatory reading order, and durable status note.
p = "MIMIR_KNOWLEDGE_GRAPH.md"
t = read(p)
t = regex_once(
    t,
    r"(?m)^R3\.18AM active .*?$",
    "R3.18AM post-AK one-payload evidence / Outcome A CLOSED                                      |\nR3.18AN active bounded post-AK 32-bit Int payload production                                  |",
    "KG current graph",
)
lines = t.splitlines()
heading = lines.index("## Mandatory reading order")
next_heading = next(i for i in range(heading + 1, len(lines)) if lines[i].startswith("## "))
section = lines[heading + 1:next_heading]
entries = []
other = []
for line in section:
    m = re.match(r"^(\d+)\. (`.+`)$", line)
    if m:
        entries.append(m.group(2))
    else:
        other.append(line)
needle = "`docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md`"
if needle not in entries:
    raise SystemExit("KG AM execution spec missing from reading order")
for new_entry in [
    "`docs/continuity/MIMIR_R3_18AM_DECISION.md`",
    "`docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md`",
]:
    if new_entry in entries:
        raise SystemExit(f"KG unexpected existing entry: {new_entry}")
pos = entries.index(needle) + 1
entries[pos:pos] = [
    "`docs/continuity/MIMIR_R3_18AM_DECISION.md`",
    "`docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md`",
]
renumbered = [f"{i}. {entry}" for i, entry in enumerate(entries, 1)]
lines[heading + 1:next_heading] = [""] + renumbered + [""]
t = "\n".join(lines).rstrip() + "\n"
status = f"""\n### R3.18AM post-AK payload evidence: OUTCOME A / CLOSED\n- evidence `{AM_HEAD}` / tree `{AM_TREE}`; run/job `{AM_RUN}/{AM_JOB}` SUCCESS\n- same-head CI `{AM_CI_RUN}/{AM_CI_JOB}` SUCCESS; PR #{AM_PR} closed unmerged\n- artifact `{AM_ARTIFACT}` / `sha256:{AM_DIGEST}`; ZIP exact / inner manifest 11/11 PASS\n- 47/47 published-AK exact; Int=47; payload width 32/47; semantic range 1..415; mismatch 0; reselection 0; another-control 0\n- production unchanged at `{PROD_SHA}`\n\n### R3.18AN bounded post-AK payload production: ACTIVE\n- exact R3.18AM family only: Int / 32 bits\n- validate/recompute R3.18AK + exact R3.18AJ membership; one primitive payload decode; stop at payload_end\n- following control, loops/cursors and semantic/runtime widening remain closed\n"""
if "### R3.18AM post-AK payload evidence: OUTCOME A / CLOSED" in t:
    raise SystemExit("KG AM status already exists")
t += status
write(p, t)
