#!/usr/bin/env python3
import json
import re
from pathlib import Path

MAIN = "1992ec94ab6a368e4143aad403ad6a223e3d3e5a"
PROD = "fd74ba8c520ab83b808730572c41e45d6dc616e6"
EHEAD = "9bbf59745c950b7be5a5a592724f41db80874973"
ERUN = "32007040663"
EJOB = "95318554719"
CIRUN = "32007040500"
CIJOB = "95318554225"
AID = "9280430420"
ADIG = "77245223aa0513b9ffaf65ed1cf404b70bb31908e81dc643800d0fd676d49021"
ASIZE = 21060


def write(path, text):
    Path(path).write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one occurrence, got {count}")
    return text.replace(old, new, 1)


decision = f"""# MIMIR R3.18N Decision — Published Following-Control Differential

## Status

**Outcome A — ADMITTED / COMPLETE / READ-ONLY.**

R3.18N differentially validated the published R3.18M after-second-payload following-`property_present` API on the exact immutable R3.18L 47-row continuation lane. Production Rust remains frozen at `{PROD}`.

## Authority

- pre-pass `main`: `{MAIN}`
- production SHA: `{PROD}`
- evidence head: `{EHEAD}`
- evidence run/job: `{ERUN}` / `{EJOB}` — SUCCESS
- exact-head normal CI run/job: `{CIRUN}` / `{CIJOB}` — SUCCESS
- artifact: `{AID}` / `{ASIZE}` bytes
- artifact digest: `sha256:{ADIG}`
- artifact name: `r318n-published-following-control-evidence`
- frozen witness reselection: `0`

## Admitted evidence

- frozen rows: `47/47`
- R3.18J reconstruction exact: `47/47`
- following control distribution: `false=0`, `true=47`
- published R3.18M / oracle mismatch: `0`
- exact following control start/value/end/stop: `47/47`
- truncated/missing following control negative: `47/47 PASS`
- prior R3.18J stop mismatch negative: `47/47 PASS`
- missing second header negative: `47/47 PASS`
- missing second payload negative: `47/47 PASS`
- synthetic false following control rejection: `47/47 PASS`
- repeatability: `47/47 PASS`
- post-stop poison/invariance: `47/47 PASS`
- following stream bits consumed: `0`
- following header bits consumed: `0`
- following payload bits consumed: `0`
- another control bit consumed: `0`
- privacy gate: `PASS`
- production/Cargo/fixture/corpus/support mutation: `0/0/0/0/0`

## Decision

The published R3.18M true-only one-bit composition is admitted on the exact frozen 47-row lane. This does **not** admit a following stream ID, following property header, following payload, another control bit, generalized property loop, next actor/frame, lifecycle state, raw state, events, replay slicing, skills, runtime, or export widening.

Outcome A opens only a separate **R3.18O following-property header evidence** pass. R3.18O is evidence-only and must stop at the following property's `payload_start` boundary without consuming payload bits or another property-control bit.
"""
write("docs/continuity/MIMIR_R3_18N_DECISION.md", decision)

ospec = f"""# MIMIR R3.18O Execution Spec — Following-Property Header Evidence

## Status

**ACTIVE after R3.18N Outcome A admission. Evidence-only. Production frozen.**

## Purpose

Characterize exactly one following existing-actor property header after the published R3.18M true-only control on the exact immutable R3.18N/R3.18L 47-row lane. Stop at that following property's `payload_start` boundary.

This pass may establish a narrow evidence-supported header boundary. It may not modify production Rust or admit any following payload or repeated property loop.

## Frozen authority

- R3.18N admission base: `{MAIN}`
- last production code SHA: `{PROD}`
- R3.18N evidence head: `{EHEAD}`
- R3.18N evidence run/job: `{ERUN}` / `{EJOB}` — SUCCESS
- R3.18N exact-head CI: `{CIRUN}` / `{CIJOB}` — SUCCESS
- R3.18N artifact: `{AID}`
- R3.18N artifact digest: `sha256:{ADIG}`
- exact witness lane: `47` rows, reselection forbidden
- inherited following-control distribution: `false=0`, `true=47`

Before any evidence run, fresh-read `main` and fail closed if production source, R3.18M API identity, N receipt, or frozen witness identity has drifted.

## Required evidence

For every one of the 47 frozen rows:

1. Reconstruct the exact admitted R3.18J second-payload boundary.
2. Invoke/validate the published R3.18M following-control composition and require `true` at the exact one-bit boundary.
3. Independently establish the following header oracle from the pinned evidence lane.
4. Decode/measure exactly the following header fields required to reach `payload_start`:
   - stream-id start/end/value,
   - stream-id bound,
   - prop-id bit width/context,
   - resolved property object/index,
   - resolved attribute tag,
   - payload-start bit.
5. Require exact native/evidence-oracle equality for all admitted header fields and cursor boundaries.
6. Stop at `payload_start`.

## Hard stop / forbidden widening

R3.18O must consume:

- following payload bits: `0`
- another property-control bit: `0`
- next actor/frame bits: `0`

It must not add a production decoder, generalized cursor/loop API, new dependency, support-lane expansion, fixture/corpus mutation, raw-state/event/skill/runtime/export behavior, or infer acceptance outside exact observed structural contexts.

## Required negative controls

- truncation at each observed following-header field boundary,
- prior R3.18M stop mismatch,
- unresolved/wrong stream context,
- property/tag/context outside the exact observed lane,
- repeatability,
- poison/invariance immediately after `payload_start`, proving no payload or later-control consumption.

## Validation

- frozen replay identity: `47/47`
- witness reselection: `0`
- independent oracle/native mismatch: `0` for Outcome A
- privacy-safe artifact only
- same-head normal CI: SUCCESS
- full `mimir-replay` regression: PASS
- workspace check/test/clippy: PASS
- repository verifier: PASS
- production/Cargo/fixture/corpus/support mutation: `0/0/0/0/0`

## Outcomes

### Outcome A

All 47 frozen rows are exact, observed header domains are bounded/contractable, all negatives pass, and the decoder stops at `payload_start`. Admit R3.18O as read-only evidence and open only the next narrowly justified canonical pass. Production remains unchanged until a separately specified production candidate is validated and published.

### Outcome B

Any mismatch, unbounded/heterogeneous structural context, negative-control failure, identity drift, or post-`payload_start` consumption keeps production frozen. Record the narrowed boundary and investigate before opening another pass.
"""
write("docs/continuity/MIMIR_R3_18O_EXECUTION_SPEC.md", ospec)

spath = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(spath.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-17"
state["last_completed_read_only_audit"] = "R3.18N"
state["last_completed_evidence_pass"] = "R3.18N"
state["last_completed_evidence_outcome"] = "A — published R3.18M API exact on frozen 47-row lane; false=0 true=47; mismatch 0; following stream/header/payload/another-control consumption 0/0/0/0."
state["current_pass"] = "R3.18O"
state["current_pass_kind"] = "read-only following-property header evidence"
state["current_pass_goal"] = "Characterize exactly one following property header after the published R3.18M true-only control on the same frozen 47-row lane and stop at payload_start."
state["current_pass_stop_boundary"] = "Stop exactly at following-property payload_start. Consume zero following payload bits and zero another-control bits; no generalized loop or later runtime widening."
state["r3_18n"] = {
    "outcome": "A — admitted / complete / read-only",
    "production_source_changed": False,
    "production_sha": PROD,
    "evidence_head": EHEAD,
    "evidence_run": int(ERUN),
    "evidence_job": int(EJOB),
    "same_head_ci_run": int(CIRUN),
    "same_head_ci_job": int(CIJOB),
    "artifact_id": int(AID),
    "artifact_size_bytes": ASIZE,
    "artifact_sha256": ADIG,
    "frozen_rows": 47,
    "control_false": 0,
    "control_true": 47,
    "r3_18j_reconstruction_exact": 47,
    "published_r3_18m_oracle_mismatch": 0,
    "following_stream_bits_consumed": 0,
    "following_header_bits_consumed": 0,
    "following_payload_bits_consumed": 0,
    "another_control_bits_consumed": 0,
    "witness_reselection": 0,
    "next_pass": "R3.18O"
}
order = state.get("next_files_to_read", [])
for p in ["docs/continuity/MIMIR_R3_18N_DECISION.md", "docs/continuity/MIMIR_R3_18O_EXECUTION_SPEC.md"]:
    if p not in order:
        anchor = "docs/continuity/MIMIR_PASS_PROTOCOL.md"
        idx = order.index(anchor) if anchor in order else len(order)
        order.insert(idx, p)
state["next_files_to_read"] = order
spath.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

current = f"""# MIMIR Current State

Updated: 2026-08-17

## Canonical truth

- repository: `Naveax/MIMIR`
- production code SHA: `{PROD}`
- last production milestone: **R3.18M**
- last completed read-only evidence pass: **R3.18N / Outcome A**
- active canonical pass: **R3.18O — following-property header evidence**
- supported/frozen evidence lane: **47 replays / 47 rows**

## R3.18N admitted receipt

- evidence head: `{EHEAD}`
- evidence run/job: `{ERUN}` / `{EJOB}` — SUCCESS
- same-head normal CI: `{CIRUN}` / `{CIJOB}` — SUCCESS
- artifact: `{AID}` / `{ASIZE}` bytes
- artifact digest: `sha256:{ADIG}`
- R3.18J reconstruction: `47/47` exact
- published R3.18M following control: `47/47` exact, `false=0`, `true=47`, mismatch `0`
- following stream/header/payload/another-control bits consumed: `0/0/0/0`
- witness reselection: `0`
- production/Cargo/fixture/corpus/support mutation: `0/0/0/0/0`

## Active boundary

R3.18O may only characterize one following property header after the admitted R3.18M control and stop at that property's `payload_start`. Following payload, another control bit, generalized/repeated property loop, next actor/frame, lifecycle state, raw state, events, replay slicing, skills, runtime and exports remain closed.

Read `docs/continuity/MIMIR_R3_18N_DECISION.md` and `docs/continuity/MIMIR_R3_18O_EXECUTION_SPEC.md` before widening anything.
"""
write("docs/continuity/MIMIR_CURRENT_STATE.md", current)

handoff = f"""# MIMIR Next Chat Handoff — R3.18O

Fresh-read `main` before work. Production remains `{PROD}` at R3.18M. R3.18N is admitted Outcome A and production source did not change.

Canonical R3.18N authority:
- evidence head `{EHEAD}`
- run/job `{ERUN}` / `{EJOB}` SUCCESS
- same-head CI `{CIRUN}` / `{CIJOB}` SUCCESS
- artifact `{AID}`
- digest `sha256:{ADIG}`
- exact frozen rows `47/47`, false=0 true=47, published API/oracle mismatch=0
- following stream/header/payload/another-control consumption `0/0/0/0`

First unfinished canonical pass: **R3.18O following-property header evidence**.

Read `MIMIR_CONTINUE_HERE.md`, apply the `MIMIR_KNOWLEDGE_GRAPH.md` mandatory order, then execute `docs/continuity/MIMIR_R3_18O_EXECUTION_SPEC.md`. Reuse the exact frozen N/L witness lane; witness reselection is forbidden. Stop at following `payload_start`; do not consume payload or another control bit and do not modify production Rust during evidence.
"""
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)

ledger_path = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
ledger = ledger_path.read_text(encoding="utf-8").rstrip()
if "## R3.18N — Published Following-Control Differential" not in ledger:
    ledger += f"""\n\n## R3.18N — Published Following-Control Differential

- status: **Outcome A / ADMITTED / READ-ONLY**
- production remains `{PROD}`
- evidence `{EHEAD}` / `{ERUN}` / `{EJOB}` SUCCESS
- same-head CI `{CIRUN}` / `{CIJOB}` SUCCESS
- artifact `{AID}` / `sha256:{ADIG}` / {ASIZE} bytes
- frozen 47/47; false=0 true=47; published R3.18M/oracle mismatch=0
- following stream/header/payload/another-control bits consumed 0/0/0/0; reselection=0
- next canonical pass: **R3.18O following-property header evidence**
"""
write(ledger_path, ledger)

hpath = Path("MIMIR_CONTINUE_HERE.md")
h = hpath.read_text(encoding="utf-8")
h = replace_once(h,
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18L — following-property control-bit evidence / Outcome A / 47/47 exact / false=0 true=47 / 0 mismatch / following stream+header+payload bits 0",
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18N — published R3.18M following-control differential / Outcome A / 47/47 exact / false=0 true=47 / 0 mismatch / following stream+header+payload+another-control bits 0",
    "handbook audit")
h = replace_once(h,
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18L — after-second-payload property_present evidence / Outcome A / 47 continuation rows / false=0 true=47 / 0 mismatch / no following stream/header/payload",
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18N — published after-second-payload control differential / Outcome A / 47 continuation rows / false=0 true=47 / 0 mismatch / no following stream/header/payload/another-control",
    "handbook evidence")
h = replace_once(h,
    "CURRENT_PASS:\n  R3.18N — published after-second-payload control real-replay differential audit",
    "CURRENT_PASS:\n  R3.18O — following-property header evidence",
    "handbook current pass")
h = replace_once(h,
    "CURRENT_PASS_TYPE:\n  read-only differential / validate the published R3.18M true-only following-control API on the exact frozen R3.18L 47-row lane; no following stream/header/payload access",
    "CURRENT_PASS_TYPE:\n  read-only differential / characterize exactly one following property header on the frozen 47-row lane and stop at payload_start; no following payload or another-control access",
    "handbook pass type")
h = replace_once(h,
    "  R3.18N ACTIVE read-only differential on the exact frozen R3.18L 47-row true-only lane\n  NO following stream/header/payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "  R3.18N CLOSED Outcome A: published R3.18M API matched the exact frozen 47-row lane; false=0 true=47; mismatch 0; following stream/header/payload/another-control consumption 0/0/0/0\n  R3.18O ACTIVE read-only following-property header evidence; stop at following payload_start\n  NO following payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "handbook hard stop")
marker = "R3_18L_EVIDENCE_CLOSURE:\n"
if "R3_18N_EVIDENCE_CLOSURE:" not in h:
    closure = f"""R3_18N_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at {PROD}
  authority head: {EHEAD}
  authority run/job: {ERUN} / {EJOB} SUCCESS
  exact-head normal CI: {CIRUN} / {CIJOB} SUCCESS
  artifact: {AID} / {ASIZE} bytes
  artifact digest: sha256:{ADIG}
  frozen rows: 47/47 exact / R3.18J reconstruction 47/47 / published R3.18M-oracle mismatch 0
  following control distribution: false=0 / true=47
  truncation / prior-stop / missing-header / missing-payload / false-control negatives: PASS 47/47
  repeatability / post-stop poison: PASS 47/47
  following stream/header/payload/another-control bits consumed: 0/0/0/0; witness reselection: 0; privacy: PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0
"""
    h = replace_once(h, marker, closure + marker, "handbook N closure")
truth_re = re.compile(r"# 39\. CURRENT ONE-LINE TRUTH\n\n> \*\*.*?\*\*\n", re.S)
truth = f"""# 39. CURRENT ONE-LINE TRUTH

> **MIMIR production remains R3.18M `{PROD}`. R3.18N is admitted Outcome A: the published true-only following-control API is exact on the frozen 47-row lane with false=0, true=47, mismatch 0 and zero following stream/header/payload/another-control consumption. R3.18O is the active read-only following-property header evidence pass and must stop at `payload_start`; payload, another control, generalized loops and later runtime layers remain closed.**
"""
h, n = truth_re.subn(truth, h, count=1)
if n != 1:
    raise SystemExit(f"handbook one-line truth replacement count {n}")
write(hpath, h)

kpath = Path("MIMIR_KNOWLEDGE_GRAPH.md")
k = kpath.read_text(encoding="utf-8")
k = replace_once(k,
    "R3.18N active published after-second-payload control differential spec       |",
    "R3.18N published after-second-payload control differential decision / Outcome A CLOSED\nR3.18O active following-property header evidence spec                             |",
    "KG graph node")
old_order = """60. `docs/continuity/MIMIR_R3_18N_EXECUTION_SPEC.md`
61. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
62. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
63. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
64. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
65. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
66. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
67. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
new_order = """60. `docs/continuity/MIMIR_R3_18N_EXECUTION_SPEC.md`
61. `docs/continuity/MIMIR_R3_18N_DECISION.md`
62. `docs/continuity/MIMIR_R3_18O_EXECUTION_SPEC.md`
63. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
64. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
65. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
66. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
67. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
68. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
69. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
k = replace_once(k, old_order, new_order, "KG mandatory order")
if "### R3.18N published following control: OUTCOME A / CLOSED" not in k:
    anchor = "## Current replay-decoder chain"
    summary = f"""### R3.18N published following control: OUTCOME A / CLOSED
- production unchanged at `{PROD}`
- evidence `{EHEAD}` / `{ERUN}/{EJOB}` SUCCESS; same-head CI `{CIRUN}/{CIJOB}` SUCCESS
- artifact `{AID}` / `sha256:{ADIG}` / {ASIZE} bytes
- 47/47 exact; false=0 true=47; published R3.18M/oracle mismatch=0; witness reselection=0
- following stream/header/payload/another-control bits consumed 0/0/0/0
- next exact pass: R3.18O following-property header evidence, hard stop at payload_start

### R3.18O following-property header evidence: ACTIVE
- exact frozen 47-row N/L lane only; no witness reselection
- evidence-only; production remains `{PROD}`
- stop at following payload_start; payload and another control remain closed

"""
    k = replace_once(k, anchor, summary + anchor, "KG N/O summary")
write(kpath, k)

print("R3_18N_CONTINUITY_PATCH=PASS files=8 next=R3.18O")
