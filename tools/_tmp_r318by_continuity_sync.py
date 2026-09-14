from __future__ import annotations

import json
import os
import re
from pathlib import Path

PROD_SHA = "3b07e223fdf326e8100412fad9410bb1b66d2cb9"
PROD_TREE = "68b32f61d61c863b25e393cfa77575bac55217d7"
PROD_PARENT = "16e21d91f8e60db7b7e7b76d66494327de6936cc"
PROD_BASE = "d4b0e84adf5603a6c2fe106a7f466cd497efdd43"
LIB_BLOB = "beadbb35ec5bcda427260f6f6c5afeb7780cdbc5"
TEST_BLOB = "07e0e4bdb346833d550248609b96af8e255d4c11"
SPEC_BLOB = "727c971cc1ac6d59d59bcbc3677d71e7a4f3267b"
BUILDER_RUN = "34849180581"
BUILDER_JOB = "103992470153"
PUSH_CI_RUN = "34856781439"
PUSH_CI_JOB = "104018278890"
PR_CI_RUN = "34856787577"
PR_CI_JOB = "104018300863"
MAIN_CI_RUN = os.environ["R318BY_MAIN_CI_RUN"]
MAIN_CI_JOB = os.environ["R318BY_MAIN_CI_JOB"]
BX_CONTRACT = "37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576"
BW_ARTIFACT = "10346819501"
BW_DIGEST = "ee8a1878241b45765a7fa57c64c179c40090836096055fc5626a58724b5796fd"


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


# MIMIR_CONTINUE_HERE.md
p = "MIMIR_CONTINUE_HERE.md"
s = read(p)
s = replace_once(
    s,
    "LAST_PRODUCTION_CODE_SHA:\n  43c5d6248e2ea606b2eb0fd95f5c50758c372356",
    f"LAST_PRODUCTION_CODE_SHA:\n  {PROD_SHA}",
    "continue production sha",
)
s = replace_once(
    s,
    "LAST_PRODUCTION_MILESTONE:\n  R3.18BU — bounded post-BS next property-control production",
    "LAST_PRODUCTION_MILESTONE:\n  R3.18BY — bounded post-BU mixed-continuation following-header production",
    "continue production milestone",
)
s = replace_once(
    s,
    "CURRENT_PASS:\n  R3.18BY — bounded post-BU mixed-continuation following-header production",
    "CURRENT_PASS:\n  R3.18BZ — published-R3.18BY mixed following-header differential",
    "continue current pass",
)
s = replace_once(
    s,
    "CURRENT_PASS_TYPE:\n  bounded production implementation / validate exact BU result / false=no-header terminator / true=one exact R3.18BX header / stop at payload_start",
    "CURRENT_PASS_TYPE:\n  read-only published-production differential / exact BY two-row lane / false=no-header terminator / true=one exact R3.18BX header / payload and later-control consumption 0/0",
    "continue pass type",
)
override = f"""

# CURRENT OVERRIDE — 2026-09-14 — R3.18BY CLOSED / R3.18BZ ACTIVE

- canonical production is R3.18BY `{PROD_SHA}` / `{PROD_TREE}`; exact base `{PROD_BASE}`, final parent `{PROD_PARENT}`.
- final production scope from the canonical base is exactly `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs`; lib/test/spec blobs `{LIB_BLOB}` / `{TEST_BLOB}` / `{SPEC_BLOB}`.
- production builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; final exact-head push CI `{PUSH_CI_RUN}/{PUSH_CI_JOB}` SUCCESS; validation PR #223 CLOSED UNMERGED with final PR CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS; published-main CI `{MAIN_CI_RUN}/{MAIN_CI_JOB}` SUCCESS.
- exact BY lane remains two rows: `sample_002` BU=false terminates at 11240 with no header; `largest_100/079...` BU=true exposes exactly one R3.18BX member header `(110,6,67,LoadoutsOnline,868,32,10,false)` and stops at payload_start 3245.
- R3.18BZ is ACTIVE as a read-only published-BY differential on only those two immutable rows. Following payload, second later control, false-row header access, witness reselection, production mutation and generalized/repeated property cursors remain closed.
"""
if "# CURRENT OVERRIDE — 2026-09-14 — R3.18BY CLOSED / R3.18BZ ACTIVE" not in s:
    s = s.rstrip() + override
write(p, s)

# MIMIR_KNOWLEDGE_GRAPH.md
p = "MIMIR_KNOWLEDGE_GRAPH.md"
s = read(p)
s = replace_once(
    s,
    "R3.18BY bounded post-BU mixed-continuation following-header production / ACTIVE",
    "R3.18BY bounded post-BU mixed-continuation following-header production / PRODUCTION CLOSED\nR3.18BZ published-R3.18BY mixed following-header differential / ACTIVE",
    "kg chain",
)
s = replace_once(
    s,
    "200. `docs/continuity/MIMIR_R3_18BY_EXECUTION_SPEC.md`",
    "200. `docs/continuity/MIMIR_R3_18BY_EXECUTION_SPEC.md`\n201. `docs/continuity/MIMIR_R3_18BY_DECISION.md`\n202. `docs/continuity/MIMIR_R3_18BZ_EXECUTION_SPEC.md`",
    "kg reading order",
)
kg_append = f"""

### R3.18BY bounded post-BU mixed-continuation following-header production: CLOSED / PUBLISHED
- canonical production `{PROD_SHA}` / `{PROD_TREE}`; base `{PROD_BASE}`; final parent `{PROD_PARENT}`; exact blobs lib/test/spec `{LIB_BLOB}` / `{TEST_BLOB}` / `{SPEC_BLOB}`.
- builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; exact-head push CI `{PUSH_CI_RUN}/{PUSH_CI_JOB}` SUCCESS; PR #223 CLOSED UNMERGED; final PR CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS; published-main CI `{MAIN_CI_RUN}/{MAIN_CI_JOB}` SUCCESS.
- false BU row terminates with no header at 11240; true BU row composes exactly one R3.18BX-admitted LoadoutsOnline header and stops at payload_start 3245.
- following payload/second later control remain 0/0; no generalized cursor or context widening admitted.

### R3.18BZ published-R3.18BY mixed following-header differential: ACTIVE
- audit exactly the immutable two-row BY lane against R3.18BW/BX authority and the shared stateless header primitive.
- expected false/true=1/1, exact true header=1/1, mismatch/reselection=0/0, following payload/second-control=0/0.
- production mutation, false-row header access and any wider semantic/runtime behavior remain forbidden.
"""
if "### R3.18BY bounded post-BU mixed-continuation following-header production: CLOSED / PUBLISHED" not in s:
    s = s.rstrip() + kg_append
write(p, s)

# Boundary locks: replace only the current override block.
p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
s = read(p)
new_block = f"""# 0. Current override — R3.18BY closed / R3.18BZ read-only differential active

## PRODUCTION AUTHORITY — R3.18BY
- `{PROD_SHA}` / `{PROD_TREE}` is canonical production; exact base `{PROD_BASE}`, final parent `{PROD_PARENT}`.
- exact production scope is `crates/mimir-replay/src/lib.rs` + `crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs`.
- false BU control `[11239,11240)` terminates without header; true BU control `[3238,3239)` composes exactly one R3.18BX member header and stops at 3245.

## CLOSED READ-ONLY EVIDENCE — R3.18BW
- `778b12988046da4d186248877bd577eb2a533a58`; runner `34843377101/103973337631`; artifact `{BW_ARTIFACT}` / `sha256:{BW_DIGEST}`.
- false/true=1/1; one header exact=1/1; false-row header access=0; payload/control=0/0.

## CLOSED EXACT CONTRACT — R3.18BX
- `exact_tuple_only`: `(110,6,67,LoadoutsOnline,868,32,10,false)` x1; contract `sha256:{BX_CONTRACT}`.
- one BU=false terminator remains outside membership.

## ACTIVE READ-ONLY DIFFERENTIAL — R3.18BZ
- exact published BY rows only: false terminator 1/1, true exact header 1/1.
- compare published BY against frozen BW/BX and the shared stateless header primitive; witness reselection 0.
- consume no following payload and no second later property-control bit.

## CLOSED
- following payload after BY header;
- second later property-control bit;
- header synthesis on the BU=false terminator;
- context outside exact R3.18BX membership;
- production mutation during R3.18BZ;
- historical-contract inheritance;
- generalized/repeated property loop/cursor and wider runtime semantics.

"""
pattern = r"# 0\. Current override.*?(?=# 1\. Status vocabulary)"
s2, count = re.subn(pattern, new_block, s, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f"boundary override: expected one block, got {count}")
write(p, s2)

# Current canonical state.
write(
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-09-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD_SHA}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18BY — bounded post-BU mixed-continuation following-header production`
**Last read-only evidence/audit:** `R3.18BW — Outcome A / BU 2/2 / false=1 true=1 / one header exact=1/1 / artifact {BW_ARTIFACT}`
**Last contract pass:** `R3.18BX — Outcome A / one exact eight-field tuple / contract {BX_CONTRACT}`
**Current exact pass:** `R3.18BZ — published-R3.18BY mixed following-header differential`

## Truthful boundary

R3.18BY is canonical production at `{PROD_SHA}` / `{PROD_TREE}`. Final exact-head push CI `{PUSH_CI_RUN}/{PUSH_CI_JOB}`, validation PR #223 CI `{PR_CI_RUN}/{PR_CI_JOB}`, and published-main CI `{MAIN_CI_RUN}/{MAIN_CI_JOB}` are SUCCESS.

The exact lane has two rows. `external_fixtures/sample_002.replay` keeps BU=false `[11239,11240)` as a no-header terminator at 11240. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay` keeps BU=true `[3238,3239)` and composes exactly one R3.18BX member header `(110,6,67,LoadoutsOnline,868,32,10,false)`, stopping at payload_start 3245.

R3.18BZ may only audit those exact published results against immutable R3.18BW/R3.18BX authority and the shared stateless header primitive.

## Hard stop

No following payload, second later control, false-row header synthesis, context widening, witness reselection, production mutation, historical-contract inheritance, generalized cursor or wider semantic/runtime behavior.
""",
)

# Handoff.
write(
    "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",
    f"""# MIMIR — Next Chat Handoff

Canonical production is **R3.18BY** `{PROD_SHA}` / `{PROD_TREE}`. Final exact-head push CI `{PUSH_CI_RUN}/{PUSH_CI_JOB}`, validation PR #223 CI `{PR_CI_RUN}/{PR_CI_JOB}`, and published-main CI `{MAIN_CI_RUN}/{MAIN_CI_JOB}` are SUCCESS; PR #223 is closed unmerged.

R3.18BW is **Outcome A / CLOSED READ-ONLY** at `778b12988046da4d186248877bd577eb2a533a58`; artifact `{BW_ARTIFACT}` / `sha256:{BW_DIGEST}`. R3.18BX is **Outcome A / CLOSED CONTRACT** with only `(110,6,67,LoadoutsOnline,868,32,10,false)` x1, contract `sha256:{BX_CONTRACT}`.

R3.18BY publishes the exact two-row mixed lane: sample_002 BU=false terminates without header at 11240; largest_100/079 BU=true exposes exactly one admitted LoadoutsOnline header and stops at payload_start 3245.

Active pass: **R3.18BZ — published-R3.18BY mixed following-header differential**. It is read-only: exact two rows only, false header access 0, true header exact 1/1, payload/second-control consumption 0/0, no witness reselection or production mutation.
""",
)

# Progress ledger append.
p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
s = read(p)
ledger = f"""

---

## 2026-09-14 — R3.18BY — Bounded Post-BU Mixed-Continuation Following-Header Production
Outcome: **A — ADMITTED / PUBLISHED PRODUCTION**

Canonical production: `{PROD_SHA}` / `{PROD_TREE}`. Canonical base: `{PROD_BASE}`. Final parent: `{PROD_PARENT}`. Blobs: lib `{LIB_BLOB}`, test `{TEST_BLOB}`, spec `{SPEC_BLOB}`.

Validation:
- builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS;
- final exact-head push CI `{PUSH_CI_RUN}/{PUSH_CI_JOB}` SUCCESS;
- validation PR #223 CLOSED UNMERGED; final PR CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS;
- published-main CI `{MAIN_CI_RUN}/{MAIN_CI_JOB}` SUCCESS;
- publication force=false; exact main readback PASS.

Admitted exact lane:
- `external_fixtures/sample_002.replay`: BU false `[11239,11240)`, no following header, stop 11240;
- `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: BU true `[3238,3239)`, one header stream `[3239,3245)`, stream 61/bound 110/prop bits 6/object 67/LoadoutsOnline/context 868.32/net10/non-RL223, stop payload_start 3245;
- exact R3.18BX membership only; following payload and second later control consumption 0/0; no generalized/repeated cursor.

Admission consequence:
- R3.18BY is canonical production;
- R3.18BZ opens read-only on exactly these two published rows; production mutation and payload/later-control access remain forbidden.
"""
if "## 2026-09-14 — R3.18BY — Bounded Post-BU Mixed-Continuation Following-Header Production" not in s:
    s = s.rstrip() + ledger
write(p, s)

# Machine state JSON.
p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(read(p))
state["updated_date"] = "2026-09-14"
state["last_production_code_sha"] = PROD_SHA
state["last_production_milestone"] = "R3.18BY"
state["last_production_milestone_name"] = "bounded post-BU mixed-continuation following-header production"
state["last_completed_production_pass"] = "R3.18BY"
state["last_completed_production_outcome"] = (
    f"A — bounded post-BU mixed-continuation following-header production published at {PROD_SHA}; "
    "exact two-row lane, false no-header terminator 1/1, true exact R3.18BX header 1/1, stop at payload_start 3245; exact-head and published-main CI SUCCESS."
)
state["current_pass"] = "R3.18BZ"
state["current_pass_kind"] = "read-only published-R3.18BY mixed following-header differential"
state["current_pass_goal"] = (
    "Audit exactly the two published R3.18BY rows against immutable R3.18BW/R3.18BX authority and the shared stateless header primitive; preserve false no-header 1/1 and true exact header 1/1."
)
state["current_pass_stop_boundary"] = (
    "False remains stopped at 11240. True remains stopped at following-header payload_start 3245. Consume no following payload or second later control."
)
for item in [
    "production mutation during R3.18BZ",
    "following payload consumption during R3.18BZ",
    "second later property-control consumption during R3.18BZ",
    "false-row following-header access during R3.18BZ",
    "witness reselection during R3.18BZ",
]:
    if item not in state.get("closed_now", []):
        state.setdefault("closed_now", []).append(item)
for item in [
    "docs/continuity/MIMIR_R3_18BY_DECISION.md",
    "docs/continuity/MIMIR_R3_18BZ_EXECUTION_SPEC.md",
]:
    if item not in state.get("next_files_to_read", []):
        state.setdefault("next_files_to_read", []).append(item)
state["r3_18by_production"] = {
    "outcome": "A — admitted / published production",
    "production_sha": PROD_SHA,
    "production_tree": PROD_TREE,
    "canonical_base_sha": PROD_BASE,
    "final_parent_sha": PROD_PARENT,
    "lib_blob": LIB_BLOB,
    "focused_test_blob": TEST_BLOB,
    "execution_spec_blob": SPEC_BLOB,
    "builder_run": int(BUILDER_RUN),
    "builder_job": int(BUILDER_JOB),
    "exact_head_push_ci_run": int(PUSH_CI_RUN),
    "exact_head_push_ci_job": int(PUSH_CI_JOB),
    "validation_pr": 223,
    "validation_pr_merged": False,
    "validation_pr_ci_run": int(PR_CI_RUN),
    "validation_pr_ci_job": int(PR_CI_JOB),
    "published_main_ci_run": int(MAIN_CI_RUN),
    "published_main_ci_job": int(MAIN_CI_JOB),
    "false_rows": 1,
    "true_rows": 1,
    "true_exact_header_rows": 1,
    "following_payload_bits_consumed": 0,
    "second_later_control_bits_consumed": 0,
    "contract_sha256": BX_CONTRACT,
}
write(p, json.dumps(state, indent=2, ensure_ascii=False) + "\n")

# Decision file.
decision = f"""# MIMIR R3.18BY Decision — Bounded Post-BU Mixed-Continuation Following-Header Production

**Date:** 2026-09-14
**Status:** CLOSED / ADMITTED PUBLISHED PRODUCTION
**Canonical production:** `{PROD_SHA}` / `{PROD_TREE}`
**Canonical base:** `{PROD_BASE}`
**Final parent:** `{PROD_PARENT}`
**Contract authority:** R3.18BX `sha256:{BX_CONTRACT}`

## Receipts
- lib/test/spec blobs: `{LIB_BLOB}` / `{TEST_BLOB}` / `{SPEC_BLOB}`
- production builder: `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS
- final exact-head push CI: `{PUSH_CI_RUN}/{PUSH_CI_JOB}` SUCCESS
- validation PR #223: CLOSED UNMERGED
- final validation PR CI: `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS
- published-main CI: `{MAIN_CI_RUN}/{MAIN_CI_JOB}` SUCCESS
- publication: force=false; exact main readback PASS

The initial builder candidate `16e21d91f8e60db7b7e7b76d66494327de6936cc` was followed only by the stable-Clippy `div_ceil` correction in the focused test. Final production diff from `{PROD_BASE}` remains exactly two files: `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs`.

## Admitted result
1. `external_fixtures/sample_002.replay`: validated BU false `[11239,11240)`; BY returns `following_header=None` and stops at 11240 with zero post-BU header access.
2. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: validated BU true `[3238,3239)`; BY decodes exactly one existing-actor header with stream `[3239,3245)`, id 61, bound 110, prop bits 6, object 67 `TAGame.PRI_TA:ClientLoadoutsOnline`, tag LoadoutsOnline, context 868.32/net10/non-RL223, and stops exactly at payload_start 3245.

Exact R3.18BX tuple membership is mandatory. Wrong actor/lookup/context, header truncation and corrupt BU prerequisite fail closed. Repeatability and post-stop poison checks pass. Following payload and second later property-control consumption remain 0/0.

## Decision
R3.18BY is canonical production. Open R3.18BZ as a read-only published-production differential on exactly the immutable two-row lane. No following payload, second later control, false-row header synthesis, context widening, witness reselection, production mutation or generalized/repeated property cursor is admitted.
"""
write("docs/continuity/MIMIR_R3_18BY_DECISION.md", decision)

# BZ spec must already have been copied into the candidate by the builder.
if not Path("docs/continuity/MIMIR_R3_18BZ_EXECUTION_SPEC.md").is_file():
    raise SystemExit("missing copied R3.18BZ execution spec")

print("R3_18BY_CONTINUITY_SYNC=PASS")
