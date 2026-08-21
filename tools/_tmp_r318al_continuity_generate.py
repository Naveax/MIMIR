from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_MAIN = "02233c8125e658513dcb068370c48b1e8f15a01c"
BASE_TREE = "fc9293d821dd3e6e269763c3c0ab091428c29490"
PROD_SHA = "f20f529e3ada6e9a671ea91e5676a17a00770145"
PROD_TREE = "98c675811cca4e4d7f0122c762f371548c9266c2"
AL_HEAD = "06b8570a25a989651fc800a4ded900ce5e2f3dbe"
AL_TREE = "2753baa23be49a819cfceb333977473864a1b02b"
AL_RUN = "32469442033"
AL_JOB = "96732952709"
AL_CI_RUN = "32470066272"
AL_CI_JOB = "96734795022"
AL_ARTIFACT = "9442034802"
AL_ARTIFACT_SIZE = "14650"
AL_DIGEST = "5fcb8f796ba365193698d5d27e2e7dc0e8c221dd42d7a901e956522b7ca1f639"
AJ_CONTRACT = "cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c"
AI_ARTIFACT = "9424764320"
AI_DIGEST = "ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5"
BUILDER_RUN = os.environ.get("R318AL_BUILDER_RUN", "UNSET")
BUILDER_JOB = os.environ.get("R318AL_BUILDER_JOB", "UNSET")
if "UNSET" in (BUILDER_RUN, BUILDER_JOB):
    raise SystemExit("missing builder receipt")


def read(p: str) -> str:
    return (ROOT / p).read_text(encoding="utf-8")

def write(p: str, text: str) -> None:
    q = ROOT / p; q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(text, encoding="utf-8", newline="\n")

def sub1(text: str, pat: str, repl: str, label: str, flags=0) -> str:
    out, n = re.subn(pat, repl, text, count=1, flags=flags)
    if n != 1: raise SystemExit(f"{label}: expected 1 match, got {n}")
    return out

def replace1(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1: raise SystemExit(f"{label}: expected 1 literal, got {n}")
    return text.replace(old, new, 1)

# Durable AL decision.
decision = f"""# MIMIR R3.18AL — Published R3.18AK Following-Header Differential Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL**
**Production mutation:** none
**Canonical production:** `{PROD_SHA}` / `{PROD_TREE}`

## Decision

R3.18AL closes Outcome A. The published R3.18AK post-AG following-header composition was validated on exactly the immutable R3.18AI 47-row lane with witness reselection 0. Published R3.18AK matched the frozen R3.18AI header on 47/47 rows and matched the direct stateless native header on 47/47 rows through exactly `payload_start`. The complete R3.18AJ exact-context family reconstructed as 17/17 contexts with multiplicity 47/47, all `Int`, and mismatch zero.

R3.18AL consumed zero following-payload bits and zero second-later-control bits. It changes no production source and admits no payload production, later control, generalized property loop/cursor, actor/frame/lifecycle/raw-state/event/slice/skill/counterfactual/runtime/export widening.

## Exact authority

```text
canonical base main/tree             {BASE_MAIN} / {BASE_TREE}
production SHA/tree                  {PROD_SHA} / {PROD_TREE}
R3.18AJ contract SHA256              {AJ_CONTRACT}
R3.18AI artifact                     {AI_ARTIFACT} / sha256:{AI_DIGEST}
evidence head/tree                   {AL_HEAD} / {AL_TREE}
authority run/job                    {AL_RUN} / {AL_JOB} SUCCESS
same-head normal CI                  {AL_CI_RUN} / {AL_CI_JOB} SUCCESS
validation PR                        #130 closed unmerged
artifact                             {AL_ARTIFACT} / {AL_ARTIFACT_SIZE} bytes
artifact digest / ZIP SHA256         sha256:{AL_DIGEST}
continuity builder                   {BUILDER_RUN} / {BUILDER_JOB}
```

The downloaded artifact ZIP SHA-256 equals the GitHub artifact digest exactly. Its internal SHA-256 manifest verifies every payload file.

## Frozen result

```text
frozen rows                          47/47
published R3.18AK exact              47/47
direct stateless-header exact        47/47
R3.18AJ exact contexts               17/17
R3.18AJ exact multiplicity           47/47
observed tags                        Int=47
published/native/oracle mismatch     0
witness reselection                  0
following payload bits consumed      0
second later control bits consumed   0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Negative controls

Repeatability, bit-exact header truncation, corrupt AG control, corrupt prior/wrong actor, unresolved lookup, wrong exact version/context and post-payload-start poison invariance pass on 47/47 rows. Permanent R3.18AK focused regressions retain Cartesian `(60,5,68,Int,868,32,10)`, fabricated `(60,5,39,Int,868,32,10)`, and old-R3.18Z-only `(60,5,34,ActiveActor,868,32,10)` rejection. R3.18Z/R3.18P cross-boundary inheritance remains rejected.

## Superseded attempts

A duplicate evidence lane at `760705d1cdaef8cc752672008573b32df00adb29` failed only in temporary probe compilation because its expected `prop_id_bits` value was typed as `u32` instead of the production header's `u8`. It is not authority and was not rerun. The admitted authority is the independent successful head `{AL_HEAD}` above. A later helper-only mutation of that evidence branch is also not evidence authority; the admitted head remains immutable by exact SHA.

## Hard stop

Production remains R3.18AK. Post-AK following-payload **production**, another property-control bit, repeated/generalized property loops/cursors, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior remain closed.

## Next gate

R3.18AM is a separate read-only post-AK following-payload evidence pass on exactly the same 47 rows. It begins exactly at each validated R3.18AK `payload_start`, independently determines the observed payload width/value semantics for the R3.18AJ-admitted `Int` headers against pinned Boxcars and existing narrow native payload machinery, stops at exactly one payload end, and consumes zero bits of another property-control boundary. The 32-bit Int layout may be tested as a hypothesis from prior evidence but is not inherited by assumption at this boundary.
"""
write("docs/continuity/MIMIR_R3_18AL_DECISION.md", decision)

am_spec = f"""# MIMIR R3.18AM — Post-AK One Following-Payload Evidence

**Status:** ACTIVE
**Pass type:** read-only structural/value differential evidence
**Production authority:** R3.18AK `{PROD_SHA}` / `{PROD_TREE}`
**Published-header authority:** R3.18AL Outcome A / `{AL_HEAD}`
**Production mutation:** forbidden
**Another property-control bit:** forbidden

## 1. Goal

On exactly the immutable R3.18AI/R3.18AL 47-row lane, reconstruct each valid published R3.18AK result, begin exactly at its `payload_start`, decode exactly one following payload, compare the native result against an independently pinned Boxcars oracle, and stop exactly at that payload end. Discover this boundary's payload width/value identity independently rather than inheriting earlier payload contracts by resemblance.

## 2. Frozen authority

```text
canonical parent                     {BASE_MAIN} / {BASE_TREE}
production SHA/tree                  {PROD_SHA} / {PROD_TREE}
R3.18AJ contract                     sha256:{AJ_CONTRACT} / exact_tuple_only / 17 contexts / multiplicity 47 / Int=47
R3.18AL evidence head/tree           {AL_HEAD} / {AL_TREE}
R3.18AL authority                    {AL_RUN} / {AL_JOB} SUCCESS
R3.18AL same-head CI                 {AL_CI_RUN} / {AL_CI_JOB} SUCCESS
R3.18AL artifact                     {AL_ARTIFACT} / {AL_ARTIFACT_SIZE} / sha256:{AL_DIGEST}
rows / contexts / tags               47 / 17 / Int=47
witness reselection                  0
```

## 3. Required evidence

For all 47 frozen rows record at minimum:

- replay identity and frozen frame/actor/header coordinates;
- exact R3.18AK header identity and `payload_start`;
- independently observed oracle payload start/end/width/value;
- native payload start/end/width/value;
- exact native/oracle equality;
- exact stop at one payload end;
- exact R3.18AJ context identity and multiplicity provenance;
- following another-control bits consumed = 0.

All observed headers are currently `Int`, but R3.18AM must prove the payload layout at this boundary. Prior 32-bit Int evidence is a hypothesis, not an inherited contract.

## 4. Required negative controls

At minimum:

1. deterministic repeatability;
2. bit-exact payload truncation before the observed payload end;
3. wrong attribute tag;
4. wrong exact version/context where context applies;
5. corrupt/mismatched R3.18AK prior/header boundary;
6. post-payload-end poison invariance;
7. R3.18AC/R3.18S or any earlier payload contract is not treated as boundary authority;
8. another property-control bit consumed = 0;
9. witness reselection = 0;
10. production/Cargo/fixture/corpus/support mutation = 0/0/0/0/0.

## 5. Oracle

Use pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b` as evidence-only structural/value oracle. Boxcars must not become a production dependency.

## 6. Validation

- exact frozen artifact/replay identities;
- native probe deterministic repeatability;
- focused R3.18AK regression;
- full `mimir-replay` tests;
- workspace check/test/clippy under Rust 1.85;
- repository verifier;
- one ordinary same-head CI run;
- anti-duplicate inspection before any manual dispatch/rerun;
- immutable privacy-safe artifact with internal SHA-256 manifest.

## 7. Hard stop

R3.18AM is evidence only. It must not add a post-AK payload production API, consume another property control, create a generalized/repeated property loop or cursor, advance actor/frame/lifecycle state, or widen raw-state/event/slice/skill/counterfactual/runtime/export layers.

## 8. Outcome gate

### Outcome A
All 47 rows establish one exact boundary-specific payload family with native/oracle mismatch zero and another-control consumption zero. Close R3.18AM and open R3.18AN as a separate bounded production implementation for exactly the proven payload family.

### Outcome B
Only a strict subset or multiple separately identifiable shapes are proven. Admit only the exact supported subset/families and write R3.18AN accordingly.

### Outcome C
Authority drift, unexplained mismatch, witness reselection, unbounded layout, another-control consumption, or production mutation. Stop without widening.
"""
write("docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md", am_spec)

# Master continuation block.
p = "MIMIR_CONTINUE_HERE.md"; t = read(p)
t = sub1(t, r"(?m)^LAST_COMPLETED_READ_ONLY_AUDIT:\n  .*$", "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AL — published R3.18AK following-header differential / Outcome A / 47/47 / 17 exact contexts / Int=47 / mismatch 0 / artifact 9442034802", "continue audit")
t = sub1(t, r"(?m)^LAST_COMPLETED_EVIDENCE_PASS:\n  .*$", "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AL — published AK/frozen AI/direct header exact 47/47 / 17 contexts / Int=47 / mismatch 0 / payload-control 0/0 / artifact 9442034802", "continue evidence")
t = sub1(t, r"(?m)^CURRENT_PASS:\n  R3\.18AL.*$", "CURRENT_PASS:\n  R3.18AM — post-AK one following-payload evidence", "continue pass")
t = sub1(t, r"(?m)^CURRENT_PASS_TYPE:\n  .*$", "CURRENT_PASS_TYPE:\n  read-only payload evidence / begin at validated R3.18AK payload_start, decode exactly one payload against pinned Boxcars/native evidence, stop at payload end, consume zero another-control bits", "continue type")
t = sub1(t, r"(?m)^  R3\.18AL ACTIVE read-only differential:.*$", "  R3.18AL CLOSED Outcome A: published-AK/frozen-AI/direct-header exact 47/47; AJ contexts 17/17; multiplicity 47/47; Int=47; mismatch 0; witness reselection 0; payload/control 0/0; artifact 9442034802\n  R3.18AM ACTIVE read-only payload evidence: start exactly at R3.18AK payload_start on the same 47 rows; prove one payload independently; another-control consumption must remain 0", "continue hard stop")
t = sub1(t, r"(?m)^  NO following payload, second later control,.*$", "  NO post-AK payload production before R3.18AM evidence closure, another property control, alternate unadmitted payload layout, repeated/generalized property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted", "continue no widening")
closure = f"""R3_18AL_EVIDENCE_CLOSURE:
  Outcome A / read-only / production unchanged at {PROD_SHA}
  evidence head/tree: {AL_HEAD} / {AL_TREE}
  authority run/job: {AL_RUN}/{AL_JOB} SUCCESS
  same-head normal CI: {AL_CI_RUN}/{AL_CI_JOB} SUCCESS / PR #130 closed unmerged
  artifact: {AL_ARTIFACT} / {AL_ARTIFACT_SIZE} bytes / sha256:{AL_DIGEST}; downloaded ZIP digest exact / inner manifest PASS
  47/47 published-AK exact / 47/47 direct-header exact / AJ contexts 17/17 / multiplicity 47/47 / Int=47 / mismatch 0
  witness reselection 0 / following payload bits 0 / second later control bits 0
  repeatability/truncation/corrupt-control/wrong-actor/unresolved/wrong-version/post-payload poison PASS; Cartesian/fabricated/old-Z focused negatives PASS
  production/Cargo/fixture/corpus/support mutation 0/0/0/0/0

"""
t = replace1(t, "R3_18AK_PRODUCTION_CLOSURE:\n", closure + "R3_18AK_PRODUCTION_CLOSURE:\n", "continue closure")
write(p, t)

# Boundary locks: replace only current override.
p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"; t = read(p)
override = f"""# 0. Current override — R3.18AL closed / R3.18AM active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AK
- `{PROD_SHA}` / `{PROD_TREE}` remains canonical production;
- exact R3.18AJ membership; exactly one following header; stop at `payload_start`;
- following payload and another control are not production capabilities.

## CLOSED DIFFERENTIAL — R3.18AL Outcome A
- exact immutable 47-row lane; published-AK/frozen-AI/direct-header exact 47/47;
- 17 exact contexts; multiplicity 47; `Int=47`; mismatch 0; witness reselection 0;
- artifact `{AL_ARTIFACT}` / `sha256:{AL_DIGEST}`;
- following-payload / second-later-control consumption 0/0.

## ACTIVE EVIDENCE GATE — R3.18AM
- begin exactly at each validated R3.18AK `payload_start` on the same 47 rows;
- prove exactly one payload against pinned Boxcars and native evidence;
- stop at payload end; another-control consumption must remain 0;
- production Rust remains frozen.

## CLOSED
- post-AK payload production before R3.18AM closure; another property control; false/unproven success semantics; alternate unadmitted payload layouts; repeated/generalized property loop or cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

---"""
t = sub1(t, r"# 0\. Current override.*?\n---", override, "boundary override", flags=re.S)
write(p, t)

# Current state and handoff are intentionally concise authoritative snapshots.
write("docs/continuity/MIMIR_CURRENT_STATE.md", f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-21
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18AK — bounded post-AG following-header production composition`
**Last read-only evidence:** `R3.18AL — Outcome A / published-AK + frozen-AI + direct-header exact 47/47 / 17 contexts / Int=47 / mismatch 0 / artifact {AL_ARTIFACT}`
**Last contract:** `R3.18AJ — Outcome A / exact_tuple_only / 17 contexts / multiplicity 47 / sha256:{AJ_CONTRACT}`
**Current exact pass:** `R3.18AM — post-AK one following-payload evidence`

## Truthful boundary

R3.18AK remains published production at `{PROD_SHA}` / `{PROD_TREE}` and stops exactly at one admitted following header `payload_start`. R3.18AL independently proved that published composition on all 47 frozen rows: published/frozen/direct exact 47/47, 17/17 exact AJ contexts, multiplicity 47/47, `Int=47`, mismatch 0, witness reselection 0, and no following-payload or later-control consumption.

```text
R3.18AL evidence                    {AL_RUN}/{AL_JOB} SUCCESS
R3.18AL same-head CI                {AL_CI_RUN}/{AL_CI_JOB} SUCCESS
R3.18AL validation PR               #130 closed unmerged
R3.18AL artifact                    {AL_ARTIFACT} / {AL_ARTIFACT_SIZE} / sha256:{AL_DIGEST}
production mutation                 0
following payload / later control   0 / 0
```

## Current gate

R3.18AM is read-only. On exactly the same 47 rows, begin at each validated R3.18AK `payload_start`, independently prove one following payload against pinned Boxcars/native evidence, stop at payload end, and consume zero another-control bits.

## Hard stop

Post-AK payload production, another property control, generalized/repeated property iteration/cursor, alternate unadmitted payload layouts, next actor/frame/lifecycle and raw-state/event/slice/skill/counterfactual/runtime/export behavior remain closed.
""")
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", f"""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AK** at `{PROD_SHA}` / `{PROD_TREE}`. R3.18AL is now **Outcome A / CLOSED** as a read-only published-AK differential: evidence `{AL_HEAD}`, run/job `{AL_RUN}/{AL_JOB}` SUCCESS, same-head CI `{AL_CI_RUN}/{AL_CI_JOB}` SUCCESS, PR #130 closed unmerged, artifact `{AL_ARTIFACT}` / `sha256:{AL_DIGEST}` independently downloaded and internally verified.

Frozen AL result: published-AK exact 47/47; frozen-AI equality 47/47; direct-header equality 47/47; exact R3.18AJ contexts 17/17; multiplicity 47/47; `Int=47`; mismatch 0; witness reselection 0; following-payload/second-later-control bits 0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.

The active pass is **R3.18AM**, read-only one-following-payload evidence. Reuse exactly the 47 frozen rows, start exactly at each published-AK `payload_start`, independently compare one payload against pinned Boxcars/native evidence, stop at payload end, and consume zero bits of another property-control boundary. Do not assume the payload width solely because earlier boundaries used `Int`.

Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json`, `docs/continuity/MIMIR_R3_18AK_DECISION.md`, `docs/continuity/MIMIR_R3_18AL_DECISION.md`, and `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md` before widening.
""")

# Machine state.
p = ROOT / "docs/continuity/MIMIR_CONTINUITY_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_date"] = "2026-08-21"
d["last_completed_read_only_audit"] = "R3.18AL"
d["current_pass"] = "R3.18AM"
d["current_pass_kind"] = "read-only structural/value evidence / one post-AK following payload"
d["current_pass_goal"] = "On exactly the immutable 47-row R3.18AI/R3.18AL lane, begin at R3.18AK payload_start and prove exactly one following payload against pinned Boxcars/native evidence with zero another-control consumption."
d["current_pass_stop_boundary"] = "Exactly one payload end after R3.18AK. No payload production, another property control, generalized loop/cursor, next actor/frame or semantic/runtime/export widening."
for item in [
    "post-R3.18AK following-payload production before R3.18AM evidence closure",
    "another property control after the one R3.18AM payload evidence boundary",
    "earlier payload-contract inheritance at the R3.18AM boundary",
]:
    if item not in d.get("closed_now", []): d.setdefault("closed_now", []).append(item)
for item in ["docs/continuity/MIMIR_R3_18AL_DECISION.md", "docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md"]:
    if item not in d.get("next_files_to_read", []): d.setdefault("next_files_to_read", []).append(item)
d["r3_18al"] = {
    "outcome": "A", "closed": True, "pass_kind": "read-only published-AK differential",
    "production_sha": PROD_SHA, "evidence_head": AL_HEAD, "evidence_tree": AL_TREE,
    "authority_run": int(AL_RUN), "authority_job": int(AL_JOB), "same_head_ci_run": int(AL_CI_RUN), "same_head_ci_job": int(AL_CI_JOB),
    "artifact_id": int(AL_ARTIFACT), "artifact_size": int(AL_ARTIFACT_SIZE), "artifact_sha256": AL_DIGEST,
    "rows": 47, "published_ak_exact": 47, "direct_header_exact": 47, "exact_contexts": 17, "multiplicity_sum": 47,
    "tags": {"Int": 47}, "native_oracle_mismatch": 0, "witness_reselection": 0,
    "following_payload_bits_consumed": 0, "second_later_control_bits_consumed": 0,
    "production_cargo_fixture_corpus_support_mutation": "0/0/0/0/0",
}
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

# Knowledge graph node + mandatory order.
p = "MIMIR_KNOWLEDGE_GRAPH.md"; t = read(p)
t = replace1(t, "R3.18AL active published-AK following-header differential", "R3.18AL published-AK following-header differential / Outcome A CLOSED\nR3.18AM post-AK one-following-payload evidence / ACTIVE", "kg graph")
t = replace1(t, "112. `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`\n113. `docs/continuity/MIMIR_PASS_PROTOCOL.md`", "112. `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`\n113. `docs/continuity/MIMIR_R3_18AL_DECISION.md`\n114. `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md`\n115. `docs/continuity/MIMIR_PASS_PROTOCOL.md`", "kg reading")
# Renumber the known trailing fixed items after insertion.
t = t.replace("114. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n115. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n116. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n117. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n118. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n119. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`", "116. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n117. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n118. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n119. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n120. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n121. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`")
old = "### R3.18AL published-AK following-header differential: ACTIVE\n- read-only; production frozen at R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145`\n- reuse exactly the immutable R3.18AI 47 rows, witness reselection 0\n- stop at payload_start; payload/control/loop/cursor widening remains closed"
new = f"""### R3.18AL published-AK following-header differential: OUTCOME A / CLOSED
- evidence `{AL_HEAD}` / tree `{AL_TREE}`; run/job `{AL_RUN}/{AL_JOB}` SUCCESS
- same-head CI `{AL_CI_RUN}/{AL_CI_JOB}` SUCCESS; PR #130 closed unmerged
- artifact `{AL_ARTIFACT}` / `sha256:{AL_DIGEST}`; downloaded ZIP/internal manifest PASS
- published-AK/frozen-AI/direct-header exact 47/47; AJ contexts 17/17; multiplicity 47/47; Int=47; mismatch 0; payload/control 0/0

### R3.18AM post-AK one-following-payload evidence: ACTIVE
- read-only; production frozen at R3.18AK `{PROD_SHA}`
- reuse exactly the immutable 47-row R3.18AI/R3.18AL lane; witness reselection 0
- start at AK payload_start; prove exactly one payload independently; stop at payload end; another-control bits remain 0"""
t = replace1(t, old, new, "kg AL section")
write(p, t)

# Ledger append only; preserve historical entries exactly.
p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"; t = read(p).rstrip()
if "R3.18AL — Published R3.18AK Following-Header Differential" in t:
    raise SystemExit("ledger already contains AL closure")
t += f"""\n\n## 2026-08-21 — R3.18AL — Published R3.18AK Following-Header Differential — Outcome A / CLOSED

- Canonical production unchanged: `{PROD_SHA}` / `{PROD_TREE}`.
- Evidence authority: `{AL_HEAD}` / `{AL_TREE}`; run/job `{AL_RUN}/{AL_JOB}` SUCCESS.
- Same-head normal CI: `{AL_CI_RUN}/{AL_CI_JOB}` SUCCESS; validation PR #130 closed unmerged.
- Immutable artifact: `{AL_ARTIFACT}` / {AL_ARTIFACT_SIZE} bytes / `sha256:{AL_DIGEST}`; downloaded ZIP digest exact and internal manifest PASS.
- Result: published-AK/frozen-AI/direct-header exact 47/47; AJ contexts 17/17; multiplicity 47/47; `Int=47`; mismatch 0; witness reselection 0.
- Negative controls: repeatability, bit-exact truncation, corrupt AG, wrong actor, unresolved lookup, wrong exact context, post-payload poison 47/47; Cartesian/fabricated/old-Z focused negatives PASS.
- Following payload / second later control consumed: 0/0.
- Production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0.
- Next pass opened: R3.18AM read-only one-following-payload evidence.\n"""
write(p, t)

# Final invariants.
for f in ["MIMIR_CONTINUE_HERE.md","MIMIR_KNOWLEDGE_GRAPH.md","docs/continuity/MIMIR_BOUNDARY_LOCKS.md","docs/continuity/MIMIR_CURRENT_STATE.md","docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md","docs/continuity/MIMIR_PROGRESS_LEDGER.md"]:
    s=read(f)
    if "R3.18AM" not in s: raise SystemExit(f"{f}: missing AM marker")
json.loads(read("docs/continuity/MIMIR_CONTINUITY_STATE.json"))
print("R3_18AL_CONTINUITY_GENERATION=PASS")
