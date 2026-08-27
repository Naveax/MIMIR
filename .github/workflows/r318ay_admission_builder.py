from __future__ import annotations

import json
import os
from pathlib import Path

MAIN_SHA = os.environ["MAIN_SHA"]
MAIN_TREE = os.environ["MAIN_TREE"]
PROD_SHA = os.environ["PROD_SHA"]
PROD_TREE = os.environ["PROD_TREE"]
PARENT_SHA = os.environ["PARENT_SHA"]
PARENT_TREE = os.environ["PARENT_TREE"]
BUILDER_RUN = os.environ["BUILDER_RUN"]
BUILDER_JOB = os.environ["BUILDER_JOB"]
BUILDER_CI_RUN = os.environ["BUILDER_CI_RUN"]
BUILDER_CI_JOB = os.environ["BUILDER_CI_JOB"]
CANDIDATE_CI_RUN = os.environ["CANDIDATE_CI_RUN"]
CANDIDATE_CI_JOB = os.environ["CANDIDATE_CI_JOB"]
PUBLISHED_CI_RUN = os.environ["PUBLISHED_CI_RUN"]
PUBLISHED_CI_JOB = os.environ["PUBLISHED_CI_JOB"]

LIB_BLOB = "3742a0e856f51e50fd56ea963bb0bd6bac2d4b50"
TEST_BLOB = "f78956a22d0b2bb83e621cce24d88bce9484788b"
SPEC_BLOB = "d636344a63854b25f2be89540cf3dbf672a28b5c"
AT_CONTRACT = "3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5"
AW_HEAD = "5f1d983a7b67f84293f337f23b7e7c25fee48795"
AW_ARTIFACT = "9643254651"
AW_DIGEST = "9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc"
AX_HEAD = "465a3f2fc71e5eed6f00c16a04738031bef8d82c"
AX_ARTIFACT = "9644869549"
AX_DIGEST = "32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9"
BOXCARS = "c70e77df7af81b436cb545d070bb90c82f562d0b"

def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8", newline="\n")

def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)

p = "MIMIR_CONTINUE_HERE.md"
s = read(p)
s = replace_once(s, "LAST_PRODUCTION_CODE_SHA:\n  6a9f456c78ffccab177823234a8d9fe4ba59a850\n\nLAST_PRODUCTION_MILESTONE:\n  R3.18AU — bounded post-AQ mixed-continuation following-header production", f"LAST_PRODUCTION_CODE_SHA:\n  {PROD_SHA}\n\nLAST_PRODUCTION_MILESTONE:\n  R3.18AY — bounded post-AU one-following-payload production", "continue production header")
s = replace_once(s, "CURRENT_PASS:\n  R3.18AY — bounded post-AU one-following-payload production\n\nCURRENT_PASS_TYPE:\n  bounded production implementation / from one exact R3.18AU true following-header result under R3.18AT membership, validate/recompute the header authority, decode exactly one R3.18AW-admitted Int/32 payload with existing primitive scalar machinery, and stop exactly at payload end; the R3.18AX-observed following control remains evidence-only and must not be consumed", "CURRENT_PASS:\n  R3.18AZ — published-R3.18AY one-following-payload differential\n\nCURRENT_PASS_TYPE:\n  read-only published-production differential / compare published R3.18AY against exactly the immutable 40-row R3.18AW payload authority, require exact Int/32 boundary and value identity with mismatch 0 and deterministic repeatability, and stop at payload end with zero R3.18AX following-control consumption; production mutation forbidden", "continue current pass")
s = replace_once(s, "  R3.18AY ACTIVE bounded production: after one exact R3.18AU true following-header result, validate/recompute AU/AT authority, decode exactly one AW-admitted Int/32 payload, and stop at payload end with following-control consumption 0\n  NO production consumption of the AX-observed control bit, payload/control access on AV-false rows, next stream/header/payload, second later property-control bit, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted", f"  R3.18AY PRODUCTION at {PROD_SHA}: validates/recomputes exact R3.18AU true-header authority, decodes exactly one R3.18AW-admitted Int/32 payload, stops exactly at payload end, rejects all seven AU false terminators before payload decode, and consumes zero R3.18AX control bits\n  R3.18AZ ACTIVE read-only differential: compare published R3.18AY against exactly the 40 immutable AW payload witnesses; require exact Int/32 boundary/value identity, mismatch/reselection 0/0, repeatability PASS, and AX control consumption 0\n  NO production consumption of the AX-observed control bit, payload/control access on AV-false rows, next stream/header/payload, second later property-control bit, generalized/repeated property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted", "continue hard stop")
closure = f"""
R3_18AY_PRODUCTION_CLOSURE:
Outcome A / production {PROD_SHA} / tree {PROD_TREE}
parent: {PARENT_SHA} / parent tree {PARENT_TREE}
lib/test blobs: {LIB_BLOB} / {TEST_BLOB}
execution spec blob: {SPEC_BLOB}
builder: {BUILDER_RUN}/{BUILDER_JOB} SUCCESS / builder-head CI {BUILDER_CI_RUN}/{BUILDER_CI_JOB} SUCCESS
validation-only PR #206 CLOSED UNMERGED / exact clean-candidate CI {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS / exact pre-publish candidate CI count 1 / rerun 0
published-main CI: {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
R3.18AT contract: sha256:{AT_CONTRACT} / exact_tuple_only / 16 eight-field contexts / multiplicity 40 / 7 false terminators outside membership
R3.18AW authority: {AW_HEAD} / artifact {AW_ARTIFACT} / sha256:{AW_DIGEST} / exact payload rows 40 / Int=40 / width32=40 / semantic range 5..300
R3.18AX evidence: {AX_HEAD} / artifact {AX_ARTIFACT} / sha256:{AX_DIGEST} / false=37 true=3 / evidence-only / AY control consumption 0
clean production scope: crates/mimir-replay/src/lib.rs + crates/mimir-replay/tests/r3_18ay_post_au_payload.rs only / Cargo-doc-workflow-fixture-corpus-support mutation 0/0/0/0/0/0
focused target 15/15 PASS / exact AW true rows 40/40 / AU false terminators rejected 7/7 / deterministic repeatability PASS / post-payload poison including AX control isolated
fresh-main ancestry + force=false publication + exact SHA/tree readback PASS / source-only production publish Knowledge Archive count 0 by path filter
next exact pass: R3.18AZ published-R3.18AY one-following-payload differential; production mutation forbidden; AX control remains unread
""".strip()
if "R3_18AY_PRODUCTION_CLOSURE:" in s:
    raise SystemExit("continue AY closure already present")
s = s.rstrip() + "\n\n" + closure + "\n"
write(p, s)

p = "MIMIR_KNOWLEDGE_GRAPH.md"
s = read(p)
s = replace_once(s, "R3.18AY bounded post-AU one-following-payload production / ACTIVE                                              |", "R3.18AY bounded post-AU one-following-payload production / PRODUCTION CLOSED                                  |\nR3.18AZ published-R3.18AY one-following-payload differential / ACTIVE                                            |", "knowledge graph current lane")
s = replace_once(s, """137. `docs/continuity/MIMIR_R3_18AX_EXECUTION_SPEC.md`
138. `docs/continuity/MIMIR_R3_18AX_DECISION.md`
139. `docs/continuity/MIMIR_R3_18AY_EXECUTION_SPEC.md`
140. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
141. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
142. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
143. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
144. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
145. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
146. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`""", """137. `docs/continuity/MIMIR_R3_18AX_EXECUTION_SPEC.md`
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
148. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`""", "knowledge graph mandatory order")
kg_append = f"""
### R3.18AY bounded post-AU one-following-payload production: PRODUCTION / CLOSED
- production `{PROD_SHA}` / tree `{PROD_TREE}` / parent `{PARENT_SHA}`
- lib/test blobs `{LIB_BLOB}` / `{TEST_BLOB}`; execution spec blob `{SPEC_BLOB}`
- builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; builder-head CI `{BUILDER_CI_RUN}/{BUILDER_CI_JOB}` SUCCESS
- validation-only PR #206 closed unmerged; exact clean-candidate CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS; published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS
- exact clean scope only `crates/mimir-replay/src/lib.rs` + `crates/mimir-replay/tests/r3_18ay_post_au_payload.rs`; 293 additions; Cargo/docs/workflow/fixture/corpus/support mutation 0
- exact AW true payload lane 40/40; Int=40; width32=40; semantic range 5..300; all seven AU false terminators rejected before payload decode
- stop exactly at payload end; post-stop poison including AX control leaves result unchanged; AX following-control consumption 0; generalized/repeated cursor 0

### R3.18AZ published-R3.18AY one-following-payload differential: ACTIVE
- read-only on exactly the immutable 40-row R3.18AW payload authority; production remains `{PROD_SHA}`
- require published AY / AW / direct-native-oracle exact payload boundary and value identity 40/40, Int=40, width32=40, mismatch 0, witness reselection 0 and deterministic repeatability
- all seven AU false terminators remain outside the payload differential except fail-closed rejection checks; do not reinterpret them as payload rows
- R3.18AX false=37/true=3 remains evidence-only; consume zero following-control bits; production/Cargo/fixture/corpus/support mutation forbidden
""".strip()
if "### R3.18AY bounded post-AU one-following-payload production: PRODUCTION / CLOSED" in s:
    raise SystemExit("knowledge AY closure already present")
s = s.rstrip() + "\n\n" + kg_append + "\n"
write(p, s)

p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
s = read(p)
start = s.index("# 0. Current override")
end = s.index("\n---\n\n# 1. Status vocabulary", start)
new_override = f"""# 0. Current override — R3.18AY production / R3.18AZ active differential

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AY
- `{PROD_SHA}` / `{PROD_TREE}` is canonical production; parent `{PARENT_SHA}`;
- validates/recomputes exact R3.18AU true-header authority and rejects all seven AU false terminators before payload decode;
- decodes exactly one R3.18AW-admitted Int/32 payload and stops exactly at payload end;
- exact clean-candidate CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` and published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` are SUCCESS;
- production consumption of the R3.18AX-observed next control bit remains zero.

## CLOSED EVIDENCE — R3.18AW Outcome A
- exact 40 AV-true rows yielded one Int/32 payload with semantic range 5..300 and native/Boxcars mismatch 0; seven AV-false terminators were excluded;
- artifact `{AW_ARTIFACT}` / `sha256:{AW_DIGEST}`; production mutation 0.

## CLOSED EVIDENCE — R3.18AX Outcome A
- evidence `{AX_HEAD}` / artifact `{AX_ARTIFACT}` / `sha256:{AX_DIGEST}`;
- exact AW payload reconstruction 40/40; next one-bit distribution false=37 / true=3; oracle/native mismatch 0;
- the observed bit remains evidence-only and is not an R3.18AY production capability.

## CLOSED CONTRACT — R3.18AT Outcome A
- contract `sha256:{AT_CONTRACT}`; exact_tuple_only / 16 complete eight-field tuples / multiplicity 40;
- all seven false rows remain outside header membership; AJ/Z/P inheritance and RL223 widening remain rejected.

## ACTIVE READ-ONLY GATE — R3.18AZ
- compare published R3.18AY against exactly the immutable 40-row R3.18AW payload authority;
- require exact Int/32 tag/start/end/width/value identity, deterministic repeatability and mismatch/reselection 0/0;
- verify post-payload poison isolation and zero R3.18AX following-control reads;
- production mutation is forbidden.

## CLOSED
- production consumption of the AX-observed following control bit;
- payload/control success on the seven AV-false terminator rows;
- next stream/header/payload after the AX control boundary;
- second later property-control bit;
- context/value/boundary inheritance from historical R3.18AM/R3.18AN;
- repeated/generalized property loop or generic cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
"""
s = s[:start] + new_override.rstrip() + s[end:]
write(p, s)

current_state = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18AY — bounded post-AU one-following-payload production`
**Last read-only evidence:** `R3.18AX — Outcome A / AW payload exact 40/40 / false=37 true=3 / oracle-native exact 40/40 / mismatch 0 / artifact {AX_ARTIFACT}`
**Last completed contract:** `R3.18AT — exact_tuple_only / 16 eight-field contexts / multiplicity 40 / 7 false terminators outside membership / sha256:{AT_CONTRACT}`
**Current exact pass:** `R3.18AZ — published-R3.18AY one-following-payload differential`

## Truthful boundary

R3.18AY is canonical production. On the exact forty R3.18AU true-continuation rows it validates/recomputes the AU authority, decodes exactly one R3.18AW-admitted Int/32 payload and stops at payload end. The exact seven AU false terminators are rejected before payload decode. R3.18AX proved the next one-bit distribution false=37 / true=3, but that bit is still evidence-only and is not consumed by production.

```text
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
parent SHA/tree                        {PARENT_SHA} / {PARENT_TREE}
lib / focused-test blobs               {LIB_BLOB} / {TEST_BLOB}
builder                                {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
builder-head CI                        {BUILDER_CI_RUN}/{BUILDER_CI_JOB} SUCCESS
clean-candidate CI                     {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS / PR #206 closed unmerged
published-main CI                      {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
AW payload exact                       40/40
AU false terminators rejected          7/7
payload tag / width                    Int=40 / width32=40
semantic range                         5..300
AX control distribution                false=37 / true=3 evidence-only
following-control consumption          0
production clean scope                 2 files
```

## Current gate

R3.18AZ is a read-only published-production differential over exactly the immutable forty-row R3.18AW payload lane. It must prove published R3.18AY exact against AW/direct-native-oracle payload identity and boundaries, deterministic repeatability, mismatch/reselection zero, and zero R3.18AX following-control consumption. Production mutation is forbidden.

## Hard stop

No AX control-bit production, no payload/control success on the seven false terminators, no next stream/header/payload, no second later control, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
"""
write("docs/continuity/MIMIR_CURRENT_STATE.md", current_state)

handoff = f"""# MIMIR — Next Chat Handoff

Canonical production is **R3.18AY** at `{PROD_SHA}` / `{PROD_TREE}`, parent `{PARENT_SHA}`. The production commit is exact two-file scope: `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18ay_post_au_payload.rs`.

R3.18AY closure receipts: builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; builder-head CI `{BUILDER_CI_RUN}/{BUILDER_CI_JOB}` SUCCESS; validation-only PR #206 closed unmerged after exact candidate CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS; published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS. Fresh-main ancestry, force=false publication and exact SHA/tree readback passed.

The admitted behavior is deliberately narrow: exactly the 40 AW true payload rows decode one Int/32 payload and stop at payload end; all seven AU false terminators are rejected before payload decoding. R3.18AX's later one-bit distribution false=37 / true=3 remains evidence-only and production consumes zero of those control bits.

The active pass is **R3.18AZ published-R3.18AY one-following-payload differential**. Reuse exactly the immutable forty-row R3.18AW authority, compare published AY against AW plus direct-native/oracle identity, require exact tag/start/end/width/value and deterministic repeatability, and stop at payload end. Production mutation and AX control consumption are forbidden.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
"""
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)

p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(read(p))
if state.get("last_production_code_sha") != "6a9f456c78ffccab177823234a8d9fe4ba59a850":
    raise SystemExit("continuity json production authority drift")
if state.get("current_pass") != "R3.18AY":
    raise SystemExit("continuity json current pass drift")
state["last_production_code_sha"] = PROD_SHA
state["last_production_milestone"] = "R3.18AY"
state["last_production_milestone_name"] = "bounded post-AU one-following-payload production"
state["current_pass"] = "R3.18AZ"
state["current_pass_kind"] = "read-only published-production differential / exact immutable 40-row R3.18AW payload authority against published R3.18AY"
state["current_pass_goal"] = "Compare published R3.18AY against exactly the immutable 40-row R3.18AW payload authority and direct-native/oracle identity; require exact Int/32 tag/start/end/width/value, deterministic repeatability, mismatch and witness reselection zero, and stop at payload end."
state["current_pass_stop_boundary"] = "Read-only differential. Production mutation forbidden. Consume zero R3.18AX following-control bits. No payload/control success on the seven AU false terminators, no next stream/header/payload, no second later control, no generalized cursor, and no actor/frame/lifecycle/raw-state/event/skill/runtime widening."
files = state.get("next_files_to_read")
if not isinstance(files, list):
    raise SystemExit("continuity json next_files_to_read missing")
ay_spec = "docs/continuity/MIMIR_R3_18AY_EXECUTION_SPEC.md"
if ay_spec not in files:
    raise SystemExit("continuity json AY spec missing")
for name in ["docs/continuity/MIMIR_R3_18AY_DECISION.md", "docs/continuity/MIMIR_R3_18AZ_EXECUTION_SPEC.md"]:
    if name in files:
        raise SystemExit(f"continuity json unexpected preexisting {name}")
idx = files.index(ay_spec) + 1
files[idx:idx] = ["docs/continuity/MIMIR_R3_18AY_DECISION.md", "docs/continuity/MIMIR_R3_18AZ_EXECUTION_SPEC.md"]
write(p, json.dumps(state, indent=2, ensure_ascii=False) + "\n")

p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
s = read(p)
if "## 2026-08-27 — R3.18AY — Bounded post-AU one-following-payload production" in s:
    raise SystemExit("progress ledger AY entry already exists")
ledger = f"""
## 2026-08-27 — R3.18AY — Bounded post-AU one-following-payload production
Production base SHA: `{PARENT_SHA}`
Production commit SHA: `{PROD_SHA}`
Pass type: bounded production implementation
Outcome: A — ADMITTED / PUBLISHED

What changed:
- Added one boundary-specific production composition after an exact R3.18AU true following header.
- Recomputes and validates AU authority, decodes exactly one R3.18AW-admitted Int/32 payload, and stops at payload end.
- Rejects all seven AU false terminators before payload decode and consumes zero R3.18AX following-control bits.

Evidence:
- R3.18AW head `{AW_HEAD}` / artifact `{AW_ARTIFACT}` / `sha256:{AW_DIGEST}`.
- Exact payload lane 40/40, Int=40, width32=40, semantic range 5..300.
- R3.18AX control evidence remains false=37 / true=3 and evidence-only.

Validation:
- Builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; builder-head CI `{BUILDER_CI_RUN}/{BUILDER_CI_JOB}` SUCCESS.
- Validation-only PR #206 closed unmerged; exact candidate CI `{CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB}` SUCCESS.
- Published-main CI `{PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB}` SUCCESS.
- Fresh-main ancestry, force=false publication and exact SHA/tree readback PASS.

Boundaries opened:
- Exactly one published Int/32 payload composition after valid AU/AT true-header authority.

Boundaries still closed:
- R3.18AX following-control production.
- Payload/control success on seven AU false terminators.
- Next stream/header/payload, second later control, generalized cursor and wider semantic/runtime layers.

Important negative facts / anti-regressions:
- Production commit scope is exactly two files; Cargo/docs/workflow/fixture/corpus/support mutation 0.
- Post-payload poison including the AX control bit does not alter the AY result.

Next exact pass:
- R3.18AZ read-only published-production payload differential on exactly the forty immutable AW payload witnesses.
""".strip()
s = s.rstrip() + "\n\n" + ledger + "\n"
write(p, s)

decision = f"""# MIMIR R3.18AY — Bounded Post-AU One-Following-Payload Production Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `{PROD_SHA}` / `{PROD_TREE}`
**Parent:** `{PARENT_SHA}`

## Decision

R3.18AY closes Outcome A. On exactly the immutable forty-row R3.18AW payload authority, published production validates/recomputes the supplied R3.18AU true-header composition, begins exactly at the validated payload start, decodes exactly one signed Int/32 payload using the existing primitive scalar machinery, preserves exact payload boundary/value identity, and stops exactly at payload end. All seven R3.18AU false terminators are rejected before payload decoding.

This admission does not consume or authorize the R3.18AX-observed next `property_present` bit. The AX distribution false=37 / true=3 remains evidence-only. No next stream/header/payload, second later control, generalized/repeated property cursor or wider actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior is admitted.

## Exact authority

```text
canonical main before production       {PARENT_SHA} / {PARENT_TREE}
production SHA/tree                    {PROD_SHA} / {PROD_TREE}
lib / focused-test blobs               {LIB_BLOB} / {TEST_BLOB}
AY execution spec blob                 {SPEC_BLOB}
builder                                {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
builder-head natural CI                {BUILDER_CI_RUN}/{BUILDER_CI_JOB} SUCCESS
validation-only PR                     #206 CLOSED UNMERGED
clean-candidate CI                     {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS
published-main CI                      {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
R3.18AT contract                       sha256:{AT_CONTRACT}
R3.18AW evidence head                  {AW_HEAD}
R3.18AW artifact                       {AW_ARTIFACT} / sha256:{AW_DIGEST}
R3.18AX evidence head                  {AX_HEAD}
R3.18AX artifact                       {AX_ARTIFACT} / sha256:{AX_DIGEST}
pinned Boxcars                         {BOXCARS}
```

## Admitted production behavior

```text
AW true payload rows                    40/40
AU false terminators rejected           7/7
payload tag                             Int=40
payload width                           32 bits on 40/40
semantic range                          5..300
exact low-value witness                 1 row = 5
remaining observed values               39 rows = 300
header/payload authority recomputation  exact
deterministic repeatability             PASS
post-payload poison isolation           PASS
R3.18AX control bits consumed           0
generalized/repeated cursor             0
```

The focused `r3_18ay_post_au_payload` target passed 15/15 on the exact builder validation. Workspace check and Clippy with warnings denied passed there; the repository's full Windows verifier then passed on the exact clean candidate and again on published `main`.

## Clean publication

The production commit contains only:
- `crates/mimir-replay/src/lib.rs`;
- `crates/mimir-replay/tests/r3_18ay_post_au_payload.rs`.

The compare from parent is one commit ahead, two changed files and 293 additions. No Cargo/dependency, documentation, workflow, fixture, corpus, support, raw-state, event, skill, runtime or export mutation entered the production commit. The candidate was validated through PR #206 and that PR was closed unmerged. Fresh-main ancestry was rechecked immediately before publication; `main` advanced with `force=false`; exact SHA/tree readback matched; published-main CI succeeded. The source-only publish correctly produced no Knowledge Archive run because its path filter excludes production source.

## Hard stop

No R3.18AX following-control production, no payload/control success on the seven false terminators, no next stream/header/payload, no second later property-control bit, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18AZ is a separate read-only published-production differential. It must reuse exactly the immutable forty-row R3.18AW payload authority, compare published R3.18AY against AW plus independent direct-native/oracle identity, require exact Int/32 tag/start/end/width/value equality and deterministic repeatability, keep mismatch and witness reselection at zero, and consume no R3.18AX following-control bit. Only a separate later pass may consider control production.
"""
write("docs/continuity/MIMIR_R3_18AY_DECISION.md", decision)

az = f"""# MIMIR R3.18AZ — Published R3.18AY One-Following-Payload Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18AY `{PROD_SHA}` / `{PROD_TREE}`
**Payload evidence authority:** R3.18AW `{AW_HEAD}` / artifact `{AW_ARTIFACT}` / `sha256:{AW_DIGEST}`
**Header contract:** R3.18AT `sha256:{AT_CONTRACT}` / 16 exact eight-field tuples / multiplicity 40
**Later-control evidence:** R3.18AX false=37 / true=3 / artifact `{AX_ARTIFACT}` (evidence only; consumption forbidden)
**Production mutation:** forbidden
**Following control:** forbidden

## 1. Goal

Differentially validate the published R3.18AY bounded post-AU payload API against exactly the immutable forty-row R3.18AW payload authority. Prove the published composition itself reproduces the exact admitted Int/32 tag, start, end, width and lossless signed value and stops exactly at payload end.

The seven R3.18AU false terminators are not payload witnesses and must not be widened into the differential lane. They may be exercised only as fail-closed negative controls. The R3.18AX next `property_present` bit must remain unread.

## 2. Frozen authority

```text
R3.18AY production SHA/tree            {PROD_SHA} / {PROD_TREE}
parent                                  {PARENT_SHA} / {PARENT_TREE}
lib / focused-test blobs                {LIB_BLOB} / {TEST_BLOB}
AY execution spec blob                  {SPEC_BLOB}
AY clean-candidate CI                   {CANDIDATE_CI_RUN}/{CANDIDATE_CI_JOB} SUCCESS
AY published-main CI                    {PUBLISHED_CI_RUN}/{PUBLISHED_CI_JOB} SUCCESS
R3.18AT contract                        sha256:{AT_CONTRACT}
R3.18AW evidence head                   {AW_HEAD}
R3.18AW artifact                        {AW_ARTIFACT} / sha256:{AW_DIGEST}
R3.18AW payload identity                Int=40 / width32=40 / semantic range 5..300
R3.18AX evidence head                   {AX_HEAD}
R3.18AX artifact                        {AX_ARTIFACT} / sha256:{AX_DIGEST}
R3.18AX control distribution            false=37 / true=3
pinned Boxcars                          {BOXCARS}
witness reselection                     0
```

R3.18AW is the immutable payload authority. Historical R3.18AM/R3.18AN payload ordinal/value/boundary facts are not membership and may not be inherited.

## 3. Exact differential lane

For each of the exact forty AW payload witnesses:

1. reconstruct the exact valid published prerequisites through R3.18AU from the same witness;
2. invoke published R3.18AY exactly once;
3. require its retained/recomputed AU header authority to equal the frozen current authority;
4. require payload tag `Int`;
5. require payload start/end/width and final `stop_bit` to equal the R3.18AW row exactly;
6. require the privacy-safe lossless signed value to equal R3.18AW plus independent direct-native/oracle observation;
7. repeat and require bit-exact deterministic equality;
8. poison beginning exactly at AY `stop_bit`, including the AX control bit, and require the AY result to remain unchanged;
9. prove zero following-control and adjacent stream/header/payload consumption.

Expected totals:

```text
payload rows                    40/40
Int                             40
width32                         40
semantic range                  5..300
mismatch                        0
witness reselection             0
following-control consumption   0 bits
production mutation             0
```

## 4. Required negative controls

At minimum:
- all seven AU false terminators reject before payload decode;
- truncate any true row inside its 32-bit payload -> reject atomically;
- wrong actor -> reject;
- unresolved lookup -> reject;
- wrong exact version/context -> reject;
- corrupt/mismatched AU prior -> reject;
- wrong resolved tag -> reject;
- payload-start/header-stop mismatch -> reject;
- fabricated or historical-only header context -> reject;
- poison at exact payload end, including the AX bit, must not alter the valid result;
- source-scope guard proves one scalar payload primitive, zero control reads and no generalized/repeated cursor.

## 5. Evidence artifact

Produce one privacy-safe immutable R3.18AZ artifact containing exact AY SHA/tree/blob/CI receipts, exact AW/AT/AX authorities, forty frozen witness identities, per-row published-AY/AW/direct-native/oracle comparison, exact payload boundaries/widths/privacy-safe signed values, repeatability and negative-control results, following-control/adjacent-consumption counters, production/Cargo/fixture/corpus/support mutation counters, and a SHA-256 manifest/privacy result.

## 6. Validation

Require frozen witness identity 40/40, published AY exact 40/40, AW/direct-native/oracle exact 40/40, Int=40/width32=40, mismatch 0/witness reselection 0, all negatives and repeatability PASS, following-control consumption 0, focused AY/prerequisite regressions PASS, workspace fmt/check/test/clippy and repository verifier PASS, same exact evidence-head normal CI SUCCESS, production/Cargo/fixture/corpus/support mutation 0/0/0/0/0, and privacy scan PASS.

Before any dispatch or rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling. Use at most one validation-only PR for the exact evidence head if a natural CI cannot otherwise be obtained, and close it unmerged after SUCCESS.

## 7. Hard stop

No R3.18AX control consumption, no payload success on false terminators, no next stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Published R3.18AY matches all forty immutable AW payload witnesses exactly through payload end; mismatch 0; witness reselection 0; all negative/full validations PASS; following-control consumption 0; production mutation 0. Only then may a separate later pass consider production composition of exactly one AX-admitted next control bit.

### Outcome B
A reproducible bounded published-AY versus AW/direct-native/oracle mismatch or narrower safe subset exists. Record only the exact supported subset and keep control production closed.

### Outcome C
Authority drift, witness reselection, false-terminator widening, payload/context widening, R3.18AX control access, production mutation, generic chaining, privacy failure or validation contradiction. Stop without admission.
"""
write("docs/continuity/MIMIR_R3_18AZ_EXECUTION_SPEC.md", az)

expected = {"MIMIR_CONTINUE_HERE.md", "MIMIR_KNOWLEDGE_GRAPH.md", "docs/continuity/MIMIR_BOUNDARY_LOCKS.md", "docs/continuity/MIMIR_CONTINUITY_STATE.json", "docs/continuity/MIMIR_CURRENT_STATE.md", "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", "docs/continuity/MIMIR_PROGRESS_LEDGER.md", "docs/continuity/MIMIR_R3_18AY_DECISION.md", "docs/continuity/MIMIR_R3_18AZ_EXECUTION_SPEC.md"}
for f in expected:
    if not Path(f).exists():
        raise SystemExit(f"expected output missing: {f}")
print("R3.18AY->AZ continuity materialization complete")
