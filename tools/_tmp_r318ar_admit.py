from pathlib import Path
import json
import re

DATE = "2026-08-26"
BASE = "5bf20063a829526cc090ada8c4221d6b42ae5655"
BASE_TREE = "8fa16095e28b418d12c3050c69462ecae64ba880"
PROD = "e1ccbef95c8424b689dee7d77fd8fde2af3e0204"
PROD_TREE = "4e7100625096594bcc5c5b4c6a8054c283643b13"
PROD_PARENT = "ec2d6c29f90863d9e312856043d01fb98a0c2d2d"
LIB_BLOB = "b886c58400de0efe0a6a6113d79e6f78e751a213"
AQ_TEST_BLOB = "983cbda666f40cbc739b250eac87bc4ce0c9eb99"
AR_SPEC_BLOB = "01492ab1495dd93d5f066282773020d5b2890dc5"
AR_HEAD = "7dfe2a0fc451a40d4c750dd2e401a2f0aa36dd9d"
AR_TREE = "85a48eebc2d3292c524f482b5c131156fa8d7931"
AR_RUN = "32949846799/98118570100"
AR_CI = "32949846724/98118570114"
AR_ART = "9599823813"
AR_ART_SIZE = "9680"
AR_DIG = "20c7edce0ea6cc2d47168e9cb9bcc517cdad9b9bde78dcf7caa472403e525326"
AR_SUMMARY = "7b389bbb7f10945bea36d36dde6d47403922ae7774d59192c3865551b9c6aad5"
AR_COMPARISON = "8f4d9dd067a8493d9d7cd42f7580ee61612196a5a274ef2d067407308750356b"
AR_NEG = "c9ccb6c5d97c3184ee93223d0938b631e0ec246e2712a17cc4c1a02738904d86"
AR_VALIDATION = "ce3f97f4f2119052962204a4d90f52e22bb37245c44a3ebc27515f86e6b1c9f7"
AR_AGG = "90351a3d73d9de1b882b5dd1450d82764552c764865a18df80840fa7876795d9"
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

p = "MIMIR_CONTINUE_HERE.md"
rep1(p, """LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.18AP — next property-control bit evidence after published R3.18AN payload / Outcome A / 47/47 / false=7 / true=40 / mismatch 0 / artifact 9526988237""", f"""LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.18AR — published-R3.18AQ mixed following-control differential / Outcome A / 47/47 / false=7 / true=40 / mismatch 0 / artifact {AR_ART}""", "last audit")
rep1(p, """LAST_COMPLETED_EVIDENCE_PASS:
  R3.18AP — exact one-control observation 47/47 / false=7 / true=40 / oracle-native exact 47/47 / mismatch 0 / adjacent consumption 0/0/0/0 / artifact 9526988237""", f"""LAST_COMPLETED_EVIDENCE_PASS:
  R3.18AR — published AQ exact 47/47 / published AN prerequisite exact 47/47 / false=7 / true=40 / mismatch 0 / witness reselection 0 / adjacent consumption 0/0/0/0 / artifact {AR_ART}""", "last evidence")
rep1(p, """CURRENT_PASS:
  R3.18AR — published-R3.18AQ mixed following-control differential

CURRENT_PASS_TYPE:
  read-only published-production differential / reuse exactly the immutable R3.18AP 47-row lane, reconstruct the published R3.18AQ result, require exact false=7 true=40 start/value/end/stop equality, and consume zero following stream/header/payload/second-control bits""", """CURRENT_PASS:
  R3.18AS — one following-property-header evidence after published R3.18AQ mixed control

CURRENT_PASS_TYPE:
  read-only boundary evidence / preserve the exact R3.18AR split, observe one following property header only on the exact 40 true continuation rows, keep all 7 false rows terminated, and stop every positive row exactly at header payload_start with payload/second-control consumption zero""", "current pass")
rep1(p, """  R3.18AR ACTIVE read-only differential: prove published R3.18AQ exact on the immutable AP 47-row lane with false=7 / true=40 and adjacent consumption 0/0/0/0
  NO following stream/header/payload after the R3.18AQ/AR one-control boundary, second later property-control bit, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted""", """  R3.18AR CLOSED Outcome A: published R3.18AQ exact 47/47 on the immutable AP lane; published AN prerequisite exact 47/47; false=7 true=40; mismatch/reselection 0/0; adjacent consumption 0/0/0/0
  R3.18AS ACTIVE read-only header evidence: only the exact 40 true continuation rows may observe one following property header through payload_start; all 7 false rows terminate at AQ stop
  NO following payload or second later property-control bit after the R3.18AS header boundary, no header on false terminators, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted""", "frontier")
master = read(p)
marker = "R3_18AQ_PRODUCTION_CLOSURE:\n"
if master.count(marker) != 1:
    raise SystemExit("MIMIR_CONTINUE_HERE.md: AQ closure marker drift")
closure = f"""R3_18AR_EVIDENCE_CLOSURE:
Outcome A / read-only published-production differential / production unchanged at {PROD}
canonical continuity base: {BASE} / tree {BASE_TREE}
evidence head/tree: {AR_HEAD} / {AR_TREE}
authority run/job: {AR_RUN} SUCCESS
same-head natural CI: {AR_CI} SUCCESS / count=1 / rerun=0
artifact: {AR_ART} / {AR_ART_SIZE} bytes / sha256:{AR_DIG}; independently downloaded ZIP digest exact / inner manifest 10/10 PASS
frozen rows 47/47 / published R3.18AQ exact 47/47 / published R3.18AN prerequisite exact 47/47
control distribution: false=7 / true=40 / mismatch=0 / witness reselection=0
truncation / wrong actor / unresolved lookup / wrong exact context / corrupt AN prior / repeatability / post-stop poison / one-read-no-loop negatives PASS
focused AQ + fmt + workspace check/test/clippy -D warnings + repository verifier + diff-check + clean worktree PASS
next stream/header/payload/second-control consumption 0/0/0/0 / production-Cargo-fixture-corpus-support mutation 0/0/0/0/0 / privacy PASS
next exact pass: R3.18AS read-only one-following-header evidence on exactly the 40 true continuation rows; 7 false rows remain terminators; payload remains closed

"""
write(p, master.replace(marker, closure + marker, 1))

p = "MIMIR_KNOWLEDGE_GRAPH.md"
rep1(p, "R3.18AR published-R3.18AQ mixed following-control differential / ACTIVE                             |", """R3.18AR published-R3.18AQ mixed following-control differential / Outcome A CLOSED
R3.18AS one following-property-header evidence after published AQ mixed control / ACTIVE                |""", "graph frontier")
old_tail = """120. `docs/continuity/MIMIR_R3_18AP_EXECUTION_SPEC.md`
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
new_tail = """120. `docs/continuity/MIMIR_R3_18AP_EXECUTION_SPEC.md`
121. `docs/continuity/MIMIR_R3_18AP_DECISION.md`
122. `docs/continuity/MIMIR_R3_18AQ_EXECUTION_SPEC.md`
123. `docs/continuity/MIMIR_R3_18AQ_DECISION.md`
124. `docs/continuity/MIMIR_R3_18AR_EXECUTION_SPEC.md`
125. `docs/continuity/MIMIR_R3_18AR_DECISION.md`
126. `docs/continuity/MIMIR_R3_18AS_EXECUTION_SPEC.md`
127. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
128. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
129. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
130. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
131. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
132. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
133. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
rep1(p, old_tail, new_tail, "mandatory tail")
regex1(p, r"""### R3\.18AR published-R3\.18AQ mixed following-control differential: ACTIVE
.*?(?=
### R3\.18AG bounded post-AD true control:)""", f"""### R3.18AR published-R3.18AQ mixed following-control differential: OUTCOME A / CLOSED
- evidence `{AR_HEAD}` / tree `{AR_TREE}`; run/job `{AR_RUN}` SUCCESS
- same-head natural CI `{AR_CI}` SUCCESS / count=1 / rerun=0
- artifact `{AR_ART}` / `{AR_ART_SIZE}` bytes / `sha256:{AR_DIG}`; downloaded ZIP digest exact / inner manifest 10/10 PASS
- frozen AP identities 47/47; published AQ exact 47/47; published AN prerequisite exact 47/47
- false=7 / true=40; mismatch 0; witness reselection 0; repeatability 47/47
- truncation/wrong-actor/unresolved-lookup/wrong-context/corrupt-prior/post-stop-poison/source-scope negatives PASS
- adjacent stream/header/payload/second-control 0/0/0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS

### R3.18AS one following-property-header evidence after published AQ mixed control: ACTIVE
- reuse exactly the 47 AR/AP identities and their control split; witness reselection forbidden
- the exact 7 false rows are terminators and must expose no following-header fields
- only the exact 40 true rows may observe one following property header using the existing stateless header primitive
- compare property-present/header stream/object/tag/payload_start exactly with pinned Boxcars and stop at payload_start
- do not pre-assume header tag/context distribution; classify what the 40 frozen rows actually contain
- following payload and second later control consumption remain 0/0; production mutation forbidden
- a later contract/production step requires separate admission after AS Outcome A
""", "AR section")

p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
new_override = f"""# 0. Current override — R3.18AR closed / R3.18AS active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AQ
- `{PROD}` / `{PROD_TREE}` remains canonical production; parent `{PROD_PARENT}`;
- validates/recomputes one exact R3.18AN prior, consumes exactly one AP-admitted mixed `property_present` bit, accepts false and true, and stops one bit later;
- immutable published behavior remains false=7 / true=40.

## CLOSED DIFFERENTIAL — R3.18AR Outcome A
- evidence `{AR_HEAD}` / `{AR_TREE}`; run/job `{AR_RUN}` SUCCESS; same-head CI `{AR_CI}` SUCCESS;
- artifact `{AR_ART}` / `sha256:{AR_DIG}` / inner manifest 10/10 PASS;
- frozen rows 47/47; published AQ exact 47/47; published AN prerequisite exact 47/47;
- false=7 / true=40; mismatch 0; witness reselection 0; adjacent stream/header/payload/second-control 0/0/0/0.

## ACTIVE READ-ONLY GATE — R3.18AS
- preserve all 47 AR identities and the exact 7 false / 40 true split;
- false rows terminate at AQ stop and may not perform following-header lookup;
- only the exact 40 true rows may observe one following property header;
- stop every positive row exactly at that header's `payload_start`;
- classify actual header object/tag/context distribution without pre-admission;
- consume zero following-payload bits and zero second-later-control bits.

## CLOSED
- any following-header observation on the 7 false terminator rows;
- following payload after the R3.18AS header `payload_start`;
- second later property-control bit after the R3.18AS header;
- production following-header composition before separate evidence/contract admission;
- repeated/generalized property loop or generic cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

---
"""
regex1(p, r"""# 0\. Current override.*?
---
""", new_override, "current override")

p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
data = json.loads(read(p))
data["updated_date"] = DATE
data["last_completed_read_only_audit"] = "R3.18AR"
data["current_pass"] = "R3.18AS"
data["current_pass_kind"] = "read-only one-following-property-header evidence / exact 40 true rows after published R3.18AQ mixed control"
data["current_pass_goal"] = "Preserve the exact R3.18AR 7-false/40-true split; keep all false rows terminated and compare exactly one following property header through payload_start on only the exact 40 true continuation rows against pinned Boxcars, with no payload or second-control consumption."
data["current_pass_stop_boundary"] = "One following header through payload_start on the exact 40 true continuation rows only. The 7 false rows terminate at AQ stop. No following payload, second later control, production mutation, generalized loop/cursor or wider actor/frame/semantic/runtime/export behavior."
data["r3_18ar"] = {"outcome":"A","evidence_head":AR_HEAD,"evidence_tree":AR_TREE,"authority_run_job":AR_RUN,"same_head_natural_ci":AR_CI,"same_head_ci_count":1,"rerun_count":0,"artifact":int(AR_ART),"artifact_size":int(AR_ART_SIZE),"artifact_sha256":AR_DIG,"inner_manifest":"10/10 PASS","summary_sha256":AR_SUMMARY,"comparison_sha256":AR_COMPARISON,"negative_controls_sha256":AR_NEG,"validation_sha256":AR_VALIDATION,"aggregate_sha256":AR_AGG,"rows":47,"published_aq_exact":47,"published_an_prerequisite_exact":47,"false_count":7,"true_count":40,"mismatch":0,"witness_reselection":0,"repeatability":"47/47 PASS","next_stream_bits_consumed":0,"next_header_bits_consumed":0,"next_payload_bits_consumed":0,"second_later_control_bits_consumed":0,"production_cargo_fixture_corpus_support_mutation":"0/0/0/0/0","negative_controls":"PASS","privacy":"PASS"}
closed = data.setdefault("closed_now", [])
closed[:] = [x for x in closed if x != "following stream/header/payload after the published R3.18AQ one-control result during R3.18AR"]
for item in ["following-header evidence on any of the 7 R3.18AQ false terminator rows","following payload after the one R3.18AS header payload_start","second later property control bit after R3.18AS","production following-header composition before R3.18AS evidence/contract admission","generalized/repeated property loop or generic cursor after R3.18AS"]:
    if item not in closed: closed.append(item)
next_files = data.get("next_files_to_read", [])
ar_spec = "docs/continuity/MIMIR_R3_18AR_EXECUTION_SPEC.md"
ar_decision = "docs/continuity/MIMIR_R3_18AR_DECISION.md"
as_spec = "docs/continuity/MIMIR_R3_18AS_EXECUTION_SPEC.md"
if ar_spec not in next_files: raise SystemExit("continuity state: AR spec missing")
for path in [ar_decision, as_spec]:
    if path in next_files: next_files.remove(path)
idx = next_files.index(ar_spec) + 1
next_files[idx:idx] = [ar_decision, as_spec]
data["next_files_to_read"] = next_files
write(p, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

write("docs/continuity/MIMIR_CURRENT_STATE.md", f"""# MIMIR — Current Canonical State

**Continuity date:** {DATE}
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18AQ — bounded post-AN mixed following-control production`
**Last read-only evidence:** `R3.18AR — Outcome A / published AQ exact 47/47 / false=7 / true=40 / mismatch 0 / artifact {AR_ART}`
**Last contract:** `R3.18AJ — Outcome A / exact_tuple_only / 17 contexts / multiplicity 47 / sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c`
**Current exact pass:** `R3.18AS — one following-property-header evidence after published AQ mixed control`

## Truthful boundary

R3.18AQ remains canonical production. R3.18AR independently validated it on exactly the immutable AP 47-row lane. Published AQ and the published AN prerequisite were exact 47/47, with false=7 / true=40, mismatch 0 and witness reselection 0.

```text
AR evidence head/tree                 {AR_HEAD} / {AR_TREE}
AR authority run/job                  {AR_RUN} SUCCESS
AR same-head natural CI               {AR_CI} SUCCESS / count=1 / rerun=0
AR artifact                           {AR_ART} / {AR_ART_SIZE} bytes
AR artifact SHA-256                   {AR_DIG}
AR inner manifest                     10/10 PASS
published AQ exact                    47/47
published AN prerequisite exact       47/47
false / true                          7 / 40
mismatch / witness reselection        0 / 0
adjacent stream/header/payload/control 0/0/0/0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

## Current gate

R3.18AS is read-only. Preserve the exact 7 false / 40 true AR split. The false rows terminate at AQ stop. Only the exact 40 true rows may be passed to the existing stateless property-header primitive and compared with pinned Boxcars through `payload_start`.

## Hard stop

Do not pre-assume the 40-row header tag/context distribution. AS may not decode a following payload, read a second later control, publish a following-header production composition, create a generalized property loop/cursor, or widen actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior.
""")

write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", f"""# MIMIR — Next Chat Handoff

Canonical production is **R3.18AQ** at `{PROD}` / `{PROD_TREE}`. R3.18AR is closed Outcome A as a read-only published-production differential.

R3.18AR authority: evidence `{AR_HEAD}` / tree `{AR_TREE}`; run/job `{AR_RUN}` SUCCESS; same-head natural CI `{AR_CI}` SUCCESS with exact run count 1 and rerun 0; artifact `{AR_ART}` / `{AR_ART_SIZE}` bytes / `sha256:{AR_DIG}` with independently downloaded ZIP digest exact and inner manifest 10/10 PASS.

Scientific result: frozen rows 47/47; published AQ exact 47/47; published AN prerequisite exact 47/47; **false=7 / true=40**; mismatch 0; witness reselection 0; repeatability 47/47; adjacent stream/header/payload/second-control consumption 0/0/0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; negatives and privacy PASS.

The active pass is **R3.18AS**. Keep the exact 7 false rows terminated. On only the exact 40 true continuation rows, observe one following property header with the existing stateless header primitive, compare property-present/stream/object/tag/payload_start exactly with pinned Boxcars, and stop at payload_start. Do not pre-assume the tag/context distribution.

Do not decode the following payload, do not read a second later control, do not publish a production header composition, and do not create a generic/repeated property loop.

Before any workflow dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run if present. Rerun is never polling.
""")

p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
ledger = read(p).rstrip("\n")
entry = f"""

---

## {DATE} — R3.18AR — Published R3.18AQ Mixed Following-Control Differential

Production base SHA: `{PROD}`
Production commit SHA: unchanged
Pass type: read-only published-production differential
Outcome: **A — ADMITTED / COMPLETE**

What changed:
- no production Rust changed;
- reused exactly the immutable R3.18AP 47-row witness identities;
- reconstructed the published R3.18AQ result and compared value/start/end/stop against AP authority;
- preserved the exact terminator/continuation split.

Evidence:
- evidence head `{AR_HEAD}` / tree `{AR_TREE}`;
- authority `{AR_RUN}` SUCCESS;
- same-head natural CI `{AR_CI}` SUCCESS / count=1 / rerun=0;
- artifact `{AR_ART}` / `{AR_ART_SIZE}` bytes / `sha256:{AR_DIG}`;
- independently downloaded ZIP digest exact / inner manifest 10/10 PASS;
- published AQ exact 47/47; published AN prerequisite exact 47/47;
- false=7 / true=40; mismatch 0 / witness reselection 0 / repeatability 47/47;
- adjacent stream/header/payload/second-control consumption 0/0/0/0.

Validation:
- truncation, wrong actor, unresolved lookup, wrong exact context, corrupt AN prior, post-stop poison and one-read/no-loop source-scope negatives PASS;
- focused AQ suite, fmt, workspace check/test/clippy with warnings denied, repository verifier, diff-check and clean-worktree gates PASS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.

Boundaries opened:
- read-only investigation of exactly one following header on only the exact 40 true continuation rows.

Boundaries still closed:
- any following header on the 7 false terminator rows; following payload; second later property control; production following-header composition; generalized/repeated property loop/cursor; wider semantic/runtime layers.

Next exact pass:
- `R3.18AS — one following-property-header evidence after published R3.18AQ mixed control`.
"""
write(p, ledger + entry + "\n")

write("docs/continuity/MIMIR_R3_18AR_DECISION.md", f"""# MIMIR R3.18AR — Published R3.18AQ Mixed Following-Control Differential Decision

**Date:** {DATE}
**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL COMPLETE**
**Production SHA (unchanged):** `{PROD}`
**Evidence authority:** `{AR_HEAD}`

## Decision

R3.18AR validates the published R3.18AQ mixed following-control API against exactly the immutable R3.18AP 47-row authority lane. Published AQ reconstructs the valid AN prerequisite, starts at the frozen AP control boundary, returns the exact frozen boolean, ends/stops one bit later, and consumes nothing adjacent.

The exact distribution is **false=7 / true=40**. Both classes remain valid published AQ results. The seven false rows are terminators; the forty true rows are the only continuation candidates.

## Exact authority

```text
canonical continuity base             {BASE} / {BASE_TREE}
production SHA/tree                   {PROD} / {PROD_TREE}
production parent                     {PROD_PARENT}
lib / AQ focused-test blobs           {LIB_BLOB} / {AQ_TEST_BLOB}
AR execution spec blob                {AR_SPEC_BLOB}
evidence head/tree                    {AR_HEAD} / {AR_TREE}
authority run/job                     {AR_RUN} SUCCESS
same-head natural CI                  {AR_CI} SUCCESS / count=1 / rerun=0
artifact                              {AR_ART} / {AR_ART_SIZE} bytes
artifact SHA-256                      {AR_DIG}
pinned Boxcars                        {BOX}
AP artifact                           {AP_ART} / sha256:{AP_DIG}
```

The artifact ZIP was independently downloaded and its SHA-256 matched GitHub's digest exactly. Its internal manifest recomputed 10/10 files without mismatch.

## Differential result

```text
frozen witness identities             47/47
published AQ exact                    47/47
published AN prerequisite exact       47/47
false                                 7
true                                  40
mismatch                              0
witness reselection                   0
repeatability                         47/47 PASS
next stream bits consumed             0
next header bits consumed             0
next payload bits consumed            0
second later control bits consumed    0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                               PASS
```

## Negative and validation gates

Truncation before the control, wrong actor, unresolved lookup, wrong exact context, corrupt AN prior, post-stop poison and the source-scope one-read/no-loop guard all passed. Focused AQ tests, Rust 1.85 formatting, workspace check/test/clippy with warnings denied, full repository verifier, git diff check and clean-worktree verification passed.

## Durable artifact hashes

```text
summary                               {AR_SUMMARY}
comparison                            {AR_COMPARISON}
negative controls                     {AR_NEG}
validation                            {AR_VALIDATION}
aggregate                             {AR_AGG}
```

## Boundary consequence

R3.18AR certifies the published AQ boundary; it does not widen production. Exactly seven rows terminate after the AQ control. Exactly forty rows may be considered for a later following-header evidence pass.

## Next gate

R3.18AS is a separate read-only following-header evidence pass. It may inspect exactly one following property header only on the exact 40 true rows, using the existing stateless header primitive and pinned Boxcars, and must stop at `payload_start`. It may not decode the payload, read another control bit, or pre-admit a header tag/context distribution.
""")

write("docs/continuity/MIMIR_R3_18AS_EXECUTION_SPEC.md", f"""# MIMIR R3.18AS — One Following-Property-Header Evidence After Published R3.18AQ Mixed Control

**Status:** ACTIVE
**Pass type:** read-only boundary evidence
**Production authority:** R3.18AQ `{PROD}` / `{PROD_TREE}`
**Differential authority:** R3.18AR `{AR_HEAD}` / `{AR_RUN}` / artifact `{AR_ART}`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden

## Goal

Preserve exactly the immutable R3.18AR 47-row identity lane and its mixed control split. The seven false rows are terminators and must stop after the published AQ control. On only the exact forty true rows, observe one following property header through `payload_start`, compare it exactly with pinned Boxcars, and stop.

This pass characterizes the header boundary only. It does not publish a following-header composition and does not decode the following payload.

## Frozen authority

```text
canonical continuity base             {BASE} / {BASE_TREE}
production SHA/tree                   {PROD} / {PROD_TREE}
production parent                     {PROD_PARENT}
lib / AQ focused-test blobs           {LIB_BLOB} / {AQ_TEST_BLOB}
AR evidence head/tree                 {AR_HEAD} / {AR_TREE}
AR authority run/job                  {AR_RUN} SUCCESS
AR same-head CI                       {AR_CI} SUCCESS
AR artifact                           {AR_ART} / sha256:{AR_DIG}
AR frozen rows                        47
AR false / true                       7 / 40
AR mismatch / reselection             0 / 0
AR adjacent consumption               0/0/0/0
AP artifact                           {AP_ART} / sha256:{AP_DIG}
pinned Boxcars                        {BOX}
```

Witness reselection is forbidden. Header tag/context distribution is **not** frozen in advance and must be discovered from these exact forty true rows.

## Witness classification

For all 47 AR rows:
- reconstruct the exact published R3.18AQ result;
- require its control value/start/end/stop to equal AR;
- if false, classify as terminator and stop;
- if true, classify as a continuation row eligible for exactly one header observation.

Required split: terminator rows 7; continuation rows 40; total 47. A count or identity drift is Outcome B/C until explained; do not silently replace witnesses.

## Positive header path — exact 40 true rows

For each true row:
1. build the existing production lookup plan;
2. reconstruct the valid published AQ boundary;
3. invoke the existing stateless existing-actor property-header primitive at the exact AQ `property_present_start_bit`, using the same actor object and lookup plan;
4. require header `property_present == true`;
5. require header present-bit start/end to equal AQ start/end;
6. compare stream start/end/value/bound/prop-bit width exactly with pinned Boxcars;
7. compare resolved property object and resolved attribute tag exactly;
8. compare `payload_start_bit` and header stop exactly;
9. stop at `payload_start_bit`.

Do not invoke any K1/K2/K3/K4 payload decoder.

## Terminator path — exact 7 false rows

For every false row, AQ control must remain false and exact; no following-header lookup/success may be claimed; no stream/property lookup or payload boundary may appear after AQ stop; consumed header/payload/second-control bits remain zero.

## Evidence outputs

Report the actual forty-row distribution of resolved property objects, attribute tags, exact replay/version/net-version/RL223 context needed to explain header resolution, stream bounds/prop-id widths, exact header coordinates, and multiplicities of complete structural/context tuples. Do not infer a Cartesian allowlist. If multiple exact header contexts appear, a later contract pass must freeze exact evidence-supported tuples before production composition.

## Required negative controls

At minimum: truncation inside a deterministic true-row stream/header; unresolved stream/property lookup; wrong actor object; wrong exact context where required; true-row repeatability; poison beginning at payload_start; false terminator no-header path; and a source-scope guard proving zero payload decoder calls and no repeated/generalized property loop.

## Required gates

```text
AR witness identities                     47/47 exact
AR control reconstruction                 47/47 exact
false terminators                         7/7 exact stop
true continuation rows                    40/40
true-row header native success            40/40
property_present start/end                40/40 exact
stream start/end/value/bound              40/40 exact
resolved property object                  40/40 exact
resolved attribute tag                    40/40 exact
payload_start / header stop               40/40 exact
header tuple classification               40/40
unclassified/mismatch                     0
following payload bits consumed           0
second later control bits consumed        0
negative controls                         PASS
privacy                                   PASS
production/Cargo/fixture/corpus/support   0/0/0/0/0
same exact evidence-head normal CI        SUCCESS
```

Run focused boundary regressions plus Rust 1.85 fmt/check/test/clippy and the full repository verifier when repository code is used. Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs; reuse an equivalent exact run if present; rerun is never polling.

## Hard stop

No following-payload semantic decode, no second later property control, no production header composition, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
All 40 true-row following headers match exactly through `payload_start`; all 7 false rows remain terminators; header/context classification is complete; mismatch and unclassified counts are zero; negatives/full validation/privacy pass; production mutation is zero; payload/second-control consumption is 0/0. Then a separate contract/admission pass may be opened if exact header tuple membership must be frozen before production.

### Outcome B
A bounded header/context distinction or evidence gap exists. Record it and keep production following-header composition closed.

### Outcome C
Authority/witness drift, native/oracle header mismatch, false-row header access, payload/second-control consumption, production mutation, privacy failure or generalized chaining. Stop without widening.
""")

print("R3.18AR continuity generator complete")