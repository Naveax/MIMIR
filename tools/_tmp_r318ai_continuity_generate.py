from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE_MAIN = "b419503b5ceb8c44af207f645232570b1c9f2e6d"
BASE_TREE = "8bcdedf47233b0e6db605c6c532677d0f8166801"
PRODUCTION_SHA = "2d351e8ceb601e2fbe515d2977b2103a4b2c7976"
PRODUCTION_TREE = "4123820ce6537f2d4942cd0b5f72b52e43b96c1d"
LIB_BLOB = "db923ebcb419d278f4ab0144fe7ed15b298b60fa"
AG_TEST_BLOB = "3f3e1c8f3f6deb7f2558862a1032f8a102131443"
AI_SPEC_BLOB = "dd064744b86ce4718d389c2bd4bf080b962b16d7"
AI_HEAD = "9d424dae2ed8cc7a0a6868111805a48763131196"
AI_TREE = "b2fa45cff46c81e0458423d6aa3d9f630e2182a3"
AI_RUN = "32418184036"
AI_JOB = "96584056481"
AI_PR = "59"
AI_CI_RUN = "32420217393"
AI_CI_JOB = "96590396395"
AI_ARTIFACT = "9424764320"
AI_ARTIFACT_SIZE = "12054"
AI_ARTIFACT_DIGEST = "ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5"
AI_HEADER_ROWS_SHA256 = "5dc8550d63688b263d87532f8330b3791736f04af98b0962cd91bd378fc4b8da"
AI_HEADER_SUMMARY_SHA256 = "70ffb419d294d4e02bdd2ef843c84bcda466022d627d7dec0b736e8d19228dd1"
AI_NEGATIVES_SHA256 = "9cacb2a613958fe399114d3030f2fd1bba2c463c1efdb607498abf9af1ea843e"
AI_AGGREGATE_SHA256 = "be2593e55bce17b03bd994b98dff5e9e25a4fcb9ee40c685947bc05181925135"
AI_FROZEN_WITNESSES_SHA256 = "31b1b759a33a4831e0cfe0ca7028a85c2573149a0e7426bc7c9b4a59c2315019"
AI_REPLAY_IDENTITY_SHA256 = "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf"
BUILDER_RUN = os.environ.get("R318AI_BUILDER_RUN", "UNSET")
BUILDER_JOB = os.environ.get("R318AI_BUILDER_JOB", "UNSET")

if BUILDER_RUN == "UNSET" or BUILDER_JOB == "UNSET":
    raise SystemExit("builder run/job receipt was not supplied")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one marker, found {count}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, repl: str, label: str) -> str:
    out, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one regex match, found {count}")
    return out


# ---------------------------------------------------------------------------
# Durable decision and next exact execution spec.
# ---------------------------------------------------------------------------

decision = f"""# MIMIR R3.18AI — One Following Property-Header Evidence Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / ONE FOLLOWING HEADER EXACT**
**Production mutation:** none
**Canonical production:** `{PRODUCTION_SHA}`

## Decision

R3.18AI closes Outcome A. On exactly the immutable 47 R3.18AH/R3.18AF witnesses, MIMIR reconstructed the valid published R3.18AG true-control boundary, began exactly at that control's `stop_bit`, decoded exactly one following existing-actor property header with the existing stateless header machinery, and stopped exactly at the header `payload_start`. The independent pinned-Boxcars structural oracle matched the native result on all 47 rows with mismatch zero.

The observed later-boundary structural family contains **17 exact seven-field contexts**, all 47 rows resolving to the `Int` attribute tag. This is evidence only. It does not inherit R3.18Z or R3.18P context contracts and it does not admit a production header composition, the following payload, another control bit, a generalized property loop/cursor, next actor/frame iteration, or semantic/runtime widening.

## Exact authority

```text
canonical main before admission      {BASE_MAIN}
canonical main tree                  {BASE_TREE}
production SHA/tree                  {PRODUCTION_SHA} / {PRODUCTION_TREE}
production lib / AG test blobs       {LIB_BLOB} / {AG_TEST_BLOB}
AI execution spec blob               {AI_SPEC_BLOB}
evidence head/tree                   {AI_HEAD} / {AI_TREE}
authority run/job                    {AI_RUN} / {AI_JOB} SUCCESS
validation PR                        #{AI_PR} closed unmerged
same-head normal CI                  {AI_CI_RUN} / {AI_CI_JOB} SUCCESS
artifact                             {AI_ARTIFACT} / {AI_ARTIFACT_SIZE} bytes
artifact digest / ZIP SHA-256        sha256:{AI_ARTIFACT_DIGEST}
header rows SHA-256                  {AI_HEADER_ROWS_SHA256}
header summary SHA-256               {AI_HEADER_SUMMARY_SHA256}
negative controls SHA-256            {AI_NEGATIVES_SHA256}
aggregate SHA-256                    {AI_AGGREGATE_SHA256}
continuity builder                   {BUILDER_RUN} / {BUILDER_JOB}
```

The downloaded artifact ZIP SHA-256 equals the GitHub artifact digest exactly. Its nine payload entries all match `r3_18ai_artifact_sha256.txt` (9/9 PASS).

## Admitted evidence

```text
frozen rows                          47/47
published R3.18AG exact              47/47
one following header exact           47/47
native/oracle mismatch               0
unique exact contexts                17
observed tags                        Int=47
witness reselection                  0
repeatability                        PASS 47/47
header truncation                    PASS 47/47
corrupt AG negative                  PASS 47/47
wrong actor negative                 PASS 47/47
unresolved lookup negative           PASS 47/47
wrong context negative               PASS 47/47
post-payload-start poison            PASS 47/47
following payload bits consumed      0
second later control bits consumed   0
earlier-header contract inheritance  0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Artifact provenance

```text
frozen witnesses SHA-256             {AI_FROZEN_WITNESSES_SHA256}
replay identity SHA-256              {AI_REPLAY_IDENTITY_SHA256}
```

## Next gate

R3.18AJ is a separate **contract-only** admission pass. It may admit only the complete observed seven-field tuples `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)` and their exact evidence multiplicities from the immutable R3.18AI summary. Membership must be `exact_tuple_only`. R3.18Z/R3.18P contexts may not be inherited or unioned by assumption. Production remains frozen and no payload or later control bit may be consumed.
"""

aj_spec = f"""# MIMIR R3.18AJ — Post-AG Following-Header Exact-Context Contract

**Status:** ACTIVE
**Pass type:** contract-only admission
**Evidence authority:** R3.18AI Outcome A
**Production authority:** R3.18AG `{PRODUCTION_SHA}`
**Production mutation:** forbidden
**Payload decode:** forbidden
**Another control bit:** forbidden

## 1. Goal

Turn the R3.18AI one-following-header structural observation into the narrowest explicit boundary-specific contract. Preserve the complete seven-field identity and exact observed multiplicities. Do not import the earlier R3.18Z or R3.18P header contracts merely because some components may look familiar.

## 2. Frozen evidence authority

```text
canonical admission parent           {BASE_MAIN} / {BASE_TREE}
production SHA/tree                  {PRODUCTION_SHA} / {PRODUCTION_TREE}
production lib/test blobs            {LIB_BLOB} / {AG_TEST_BLOB}
R3.18AI execution spec blob          {AI_SPEC_BLOB}
R3.18AI evidence head/tree           {AI_HEAD} / {AI_TREE}
R3.18AI authority                    {AI_RUN} / {AI_JOB} SUCCESS
R3.18AI same-head CI                 {AI_CI_RUN} / {AI_CI_JOB} SUCCESS
R3.18AI artifact                     {AI_ARTIFACT} / {AI_ARTIFACT_SIZE} / sha256:{AI_ARTIFACT_DIGEST}
header summary / rows / aggregate    {AI_HEADER_SUMMARY_SHA256} / {AI_HEADER_ROWS_SHA256} / {AI_AGGREGATE_SHA256}
rows / exact contexts                47 / 17
observed tags                        Int=47
earlier-header inheritance assumed  0
```

Witness reselection, context synthesis from older boundaries, and production mutation are forbidden.

## 3. Required contract artifact

Create `docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json` with:

- schema version and a boundary-specific post-AG contract name;
- membership policy `exact_tuple_only`;
- tuple fields exactly `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)`;
- observed row count 47;
- unique exact context count 17;
- exact R3.18AI authority receipts and payload hashes;
- exactly the 17 observed tuples and their exact observed multiplicities;
- explicit anti-widening flags, including no R3.18Z/R3.18P inheritance.

## 4. Admission semantics

Membership is full seven-field tuple equality only. Multiplicity is evidence provenance, not a runtime frequency guarantee.

The following are not admitted:

- tag-only membership, even though all current rows are `Int`;
- object/bound/width component membership;
- Cartesian products of individually observed components;
- versionless membership;
- R3.18Z or R3.18P tuple inheritance, union, or substitution by assumption;
- any tuple outside the exact 17-entry R3.18AI set.

## 5. Required negatives

At minimum prove:

1. exact 17/17 tuple equality against the immutable R3.18AI header summary;
2. exact 17/17 multiplicities and total sum 47;
3. tag-only candidate rejection;
4. component-only candidate rejection;
5. fabricated Cartesian candidate rejection;
6. version-drop candidate rejection;
7. an eighteenth fabricated tuple is rejected;
8. at least one earlier R3.18Z/R3.18P-valid but R3.18AJ-absent tuple is rejected at this boundary;
9. production/Cargo/fixture/corpus/support mutation remains 0/0/0/0/0.

## 6. Clean scope

Contract/continuity docs only. No Rust production source, tests, dependency, fixture, corpus, workflow, support-lane or runtime/export expansion may enter the clean contract commit.

## 7. Hard stop

R3.18AJ does not publish a header decoder/composition. The following payload, another property control, repeated/generalized property loops/cursors, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual and runtime/export layers remain closed.

## 8. Outcome gate

### Outcome A
Admit the exact boundary-specific 17-tuple contract with all anti-widening negatives PASS. Production remains R3.18AG. Open R3.18AK as a separate bounded production composition for exactly one post-AG following header, requiring exact R3.18AJ membership and stopping at `payload_start`.

### Outcome B
A bounded discrepancy in tuple identity or multiplicity is isolated. Admit only the supported subset and keep production unchanged.

### Outcome C
Any authority drift, earlier-contract inheritance, tuple widening, payload/control access or production mutation. Stop without admission.
"""

if (ROOT / "docs/continuity/MIMIR_R3_18AI_DECISION.md").exists():
    raise SystemExit("R3.18AI decision unexpectedly already exists")
if (ROOT / "docs/continuity/MIMIR_R3_18AJ_EXECUTION_SPEC.md").exists():
    raise SystemExit("R3.18AJ execution spec unexpectedly already exists")
write("docs/continuity/MIMIR_R3_18AI_DECISION.md", decision)
write("docs/continuity/MIMIR_R3_18AJ_EXECUTION_SPEC.md", aj_spec)


# ---------------------------------------------------------------------------
# MIMIR_CONTINUE_HERE.md — current state, hard stop, closure and checklists.
# ---------------------------------------------------------------------------

p = "MIMIR_CONTINUE_HERE.md"
t = read(p)
t = replace_once(
    t,
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AH — published R3.18AG post-AD true-control differential / Outcome A / 47/47 / false=0 true=47 / mismatch 0 / artifact 9420166543",
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AI — one following property-header evidence after published R3.18AG / Outcome A / 47/47 / 17 exact contexts / Int=47 / mismatch 0 / artifact 9424764320",
    "continue last read-only audit",
)
t = replace_once(
    t,
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AH — published AG exact one-bit differential / 47 rows / false=0 true=47 / mismatch 0 / next stream-header-payload-second-control 0/0/0/0 / artifact 9420166543",
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AI — one post-AG following header exact / 47 rows / 17 exact contexts / Int=47 / native-oracle mismatch 0 / following-payload-second-control 0/0 / artifact 9424764320",
    "continue last evidence",
)
t = replace_once(
    t,
    "CURRENT_PASS:\n  R3.18AI — one following property-header evidence after published R3.18AG control",
    "CURRENT_PASS:\n  R3.18AJ — post-AG following-header exact-context contract",
    "continue current pass",
)
t = replace_once(
    t,
    "CURRENT_PASS_TYPE:\n  read-only structural evidence / from the exact published R3.18AG stop decode exactly one following property header and stop at that header payload_start; no payload or second later control",
    "CURRENT_PASS_TYPE:\n  contract-only admission / admit exactly the 17 complete seven-field contexts observed by R3.18AI with exact_tuple_only membership; no production, payload or later control",
    "continue current pass type",
)
t = replace_once(
    t,
    "  R3.18AI ACTIVE read-only: begin exactly at the published R3.18AG stop, decode one following property header only, and stop exactly at that header payload_start; following payload and another control remain closed\n  NO following payload after the R3.18AI header, second later control, false success semantics, alternate UniqueId layout, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "  R3.18AI CLOSED Outcome A: one post-AG following header exact 47/47; 17 exact seven-field contexts; Int=47; native-oracle mismatch 0; witness reselection 0; following payload/second-control 0/0; artifact 9424764320\n  R3.18AJ ACTIVE contract-only: admit only exact complete seven-field tuple equality and exact R3.18AI multiplicities; no earlier-header contract inheritance, production composition, payload or later control\n  NO following-header production before R3.18AJ admission, following payload, second later control, false success semantics, alternate UniqueId layout, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "continue current hard stop",
)

closure = f"""R3_18AI_EVIDENCE_CLOSURE:
  Outcome A / read-only / production unchanged at {PRODUCTION_SHA}
  canonical main before admission: {BASE_MAIN} / tree {BASE_TREE}
  authority head/tree: {AI_HEAD} / {AI_TREE}
  authority run/job: {AI_RUN} / {AI_JOB} SUCCESS
  validation PR: #{AI_PR} closed unmerged / exact-head normal CI {AI_CI_RUN} / {AI_CI_JOB} SUCCESS
  artifact: {AI_ARTIFACT} / {AI_ARTIFACT_SIZE} bytes / sha256:{AI_ARTIFACT_DIGEST}; downloaded ZIP digest exact / inner manifest 9/9 PASS
  frozen rows 47/47 / published AG exact 47/47 / one following header exact 47/47 / native-oracle mismatch 0 / witness reselection 0
  exact structural contexts 17 / observed tags Int=47 / earlier-header contract inheritance assumed 0
  repeatability/header-truncation/corrupt-AG/wrong-actor/unresolved-lookup/wrong-context/post-payload-start-poison 47/47
  following payload + second later control bits 0/0 / production-Cargo-fixture-corpus-support mutation 0/0/0/0/0 / privacy PASS
  continuity authority: {BUILDER_RUN}/{BUILDER_JOB}
"""
t = replace_once(t, "R3_18M_PRODUCTION_CLOSURE:\n", closure + "R3_18M_PRODUCTION_CLOSURE:\n", "continue AI closure insertion")

t = replace_once(
    t,
    "> **MIMIR production remains R3.18AG `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`. R3.18AH is now closed Outcome A: published AG matched the frozen 47-row one-bit lane exactly with true=47, false=0, mismatch 0 and no adjacent consumption. R3.18AI is the active read-only one-following-header evidence pass and must stop at that header's `payload_start`; following payload, another control, loops/cursors, actor/frame and semantic/runtime widening remain closed.**",
    "> **MIMIR production remains R3.18AG `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`. R3.18AI is closed Outcome A: the post-AG following header matched 47/47 with 17 exact contexts, Int=47, native-oracle mismatch 0 and zero payload/later-control consumption. R3.18AJ is the active contract-only exact-tuple admission; production header composition, following payload, another control, loops/cursors, actor/frame and semantic/runtime widening remain closed.**",
    "continue one-line truth",
)

checklist_marker = "# CURRENT PASS CHECKLIST — R3.18AI"
pos = t.find(checklist_marker)
if pos < 0:
    raise SystemExit("continue AI current checklist marker missing")
if t.find(checklist_marker, pos + 1) >= 0:
    raise SystemExit("continue AI current checklist marker duplicated")
new_tail = f"""# HISTORICAL PASS CHECKLIST — R3.18AI (OUTCOME A / CLOSED)

**Goal:** investigate exactly one following property header beginning at the published R3.18AG stop and stop at that header's `payload_start` without production mutation.

```text
[x] Canonical base main {BASE_MAIN} / {BASE_TREE}; production frozen at {PRODUCTION_SHA} / {PRODUCTION_TREE}.
[x] Reused exactly the 47 immutable AH/AF witnesses; witness reselection 0.
[x] Evidence head/tree {AI_HEAD} / {AI_TREE}; authority {AI_RUN}/{AI_JOB} SUCCESS.
[x] Immutable artifact {AI_ARTIFACT} / {AI_ARTIFACT_SIZE} bytes / sha256:{AI_ARTIFACT_DIGEST}; downloaded ZIP digest exact; inner manifest 9/9 PASS.
[x] Published AG reconstruction exact 47/47 and exactly one following header exact 47/47; native-oracle mismatch 0.
[x] Observed 17 exact complete seven-field contexts; tags Int=47; earlier-header contract inheritance assumed 0.
[x] Repeatability, header truncation, corrupt-AG, wrong-actor, unresolved-lookup, wrong-context and post-payload-start poison negatives PASS 47/47.
[x] Following payload/second later control consumption 0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.
[x] Validation PR #{AI_PR} exact-head CI {AI_CI_RUN}/{AI_CI_JOB} SUCCESS; PR closed unmerged.
[x] Outcome A admits only the observed one-header structural facts. Production composition, payload and another control remain closed.
```

---

# CURRENT PASS CHECKLIST — R3.18AJ

**Goal:** admit the narrowest exact-context contract for the 17 complete seven-field post-AG following-header contexts observed by R3.18AI. Production remains frozen.

```text
[ ] Fetch fresh main and require the R3.18AI admission parent exactly; production remains {PRODUCTION_SHA} / {PRODUCTION_TREE}.
[ ] Freeze R3.18AI evidence {AI_HEAD}/{AI_TREE}, authority {AI_RUN}/{AI_JOB}, same-head CI {AI_CI_RUN}/{AI_CI_JOB}, artifact {AI_ARTIFACT}/sha256:{AI_ARTIFACT_DIGEST}.
[ ] Read immutable R3.18AI header summary {AI_HEADER_SUMMARY_SHA256}; require rows=47, unique exact contexts=17, tags Int=47, witness reselection=0.
[ ] Create `docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json` with membership_policy=`exact_tuple_only` and the complete seven-field tuple schema.
[ ] Preserve all 17 tuple identities and exact multiplicities; require multiplicity sum 47.
[ ] Reject tag-only, component-only, Cartesian-product, version-drop and fabricated eighteenth-tuple candidates.
[ ] Prove at least one R3.18Z/R3.18P-valid but AJ-absent tuple is rejected; earlier-header inheritance must remain false.
[ ] Change continuity/contract docs only; production/Cargo/fixture/corpus/support mutation must remain 0/0/0/0/0.
[ ] Run JSON/contract self-checks, knowledge archive verifier and normal CI on the exact clean candidate.
[ ] Outcome A may open only a separate R3.18AK bounded one-header production composition requiring exact AJ membership and stopping at payload_start.
```
"""
t = t[:pos] + new_tail
write(p, t)


# ---------------------------------------------------------------------------
# Root knowledge graph: current node, reading order and immediate sections.
# ---------------------------------------------------------------------------

p = "MIMIR_KNOWLEDGE_GRAPH.md"
t = read(p)
t = replace_once(
    t,
    "R3.18AI active one-following-property-header evidence after published AG control                         |",
    "R3.18AI one-following-property-header evidence after published AG control / Outcome A CLOSED               |\nR3.18AJ active post-AG following-header exact-context contract                                                  |",
    "graph canonical AI/AJ",
)
old_order = """103. `docs/continuity/MIMIR_R3_18AH_EXECUTION_SPEC.md`
104. `docs/continuity/MIMIR_R3_18AH_DECISION.md`
105. `docs/continuity/MIMIR_R3_18AI_EXECUTION_SPEC.md`
106. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
107. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
108. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
109. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
110. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
111. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
112. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
new_order = """103. `docs/continuity/MIMIR_R3_18AH_EXECUTION_SPEC.md`
104. `docs/continuity/MIMIR_R3_18AH_DECISION.md`
105. `docs/continuity/MIMIR_R3_18AI_EXECUTION_SPEC.md`
106. `docs/continuity/MIMIR_R3_18AI_DECISION.md`
107. `docs/continuity/MIMIR_R3_18AJ_EXECUTION_SPEC.md`
108. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
109. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
110. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
111. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
112. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
113. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
114. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
t = replace_once(t, old_order, new_order, "graph mandatory order")
old_ai_section = """### R3.18AI one-following-property-header evidence: ACTIVE
- begin exactly at the published R3.18AG stop on the same frozen 47 witnesses
- decode one following property header only and stop exactly at that header payload_start
- following payload, another control, generalized property loop/cursor and semantic/runtime widening remain closed
"""
new_ai_section = f"""### R3.18AI one-following-property-header evidence: OUTCOME A / CLOSED
- evidence `{AI_HEAD}` / tree `{AI_TREE}`; run/job `{AI_RUN}/{AI_JOB}` SUCCESS
- artifact `{AI_ARTIFACT}` / `sha256:{AI_ARTIFACT_DIGEST}`; exact-head CI `{AI_CI_RUN}/{AI_CI_JOB}` SUCCESS; PR #{AI_PR} closed unmerged
- published AG exact 47/47; following header exact 47/47; 17 exact contexts; Int=47; native-oracle mismatch 0; witness reselection 0
- following payload/second later control 0/0; earlier-header contract inheritance 0; production unchanged at `{PRODUCTION_SHA}`

### R3.18AJ post-AG following-header exact-context contract: ACTIVE
- contract-only; membership must be complete seven-field `exact_tuple_only`
- preserve exactly 17 R3.18AI tuples and exact multiplicities summing to 47
- no R3.18Z/R3.18P inheritance, production composition, following payload or later control
"""
t = replace_once(t, old_ai_section, new_ai_section, "graph AI section")
write(p, t)


# ---------------------------------------------------------------------------
# Boundary locks: only the top current override is authoritative.
# ---------------------------------------------------------------------------

p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
t = read(p)
new_override = f"""# 0. Current override — R3.18AI closed / R3.18AJ active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AG
- `{PRODUCTION_SHA}` / `{PRODUCTION_TREE}`; production remains unchanged by R3.18AI;
- input must already be one valid published R3.18AD result under exact `868.32 / net10 / non-RL223` context;
- prior payload allowlist remains exactly ActiveActor/33, Int/32, UniqueId system1-Steam/80;
- read exactly one bit at prior `stop_bit`; admit **true only**; false fails closed; stop exactly one bit later.

## CLOSED EVIDENCE — R3.18AI Outcome A
- exact immutable 47-row lane; published AG exact 47/47; one following header exact 47/47; native-oracle mismatch 0; witness reselection 0;
- 17 complete observed seven-field contexts; all tags Int=47; earlier-header contract inheritance assumed 0;
- repeatability/header-truncation/corrupt-AG/wrong-actor/unresolved-lookup/wrong-context/post-payload-start-poison negatives 47/47;
- following payload/second later control consumption 0/0;
- artifact `{AI_ARTIFACT}` / `sha256:{AI_ARTIFACT_DIGEST}`; same-head CI `{AI_CI_RUN}/{AI_CI_JOB}` SUCCESS.

## ACTIVE CONTRACT-ONLY GATE — R3.18AJ
- admit only the exact 17 complete R3.18AI seven-field tuples and exact multiplicities;
- membership policy must be `exact_tuple_only`;
- R3.18Z/R3.18P inheritance, component unions, Cartesian products and versionless matching are forbidden;
- production mutation, payload decode and another control bit are forbidden.

## CLOSED
- post-AG following-header production composition until R3.18AJ is admitted;
- following payload after the R3.18AI header; second later control; false success semantics; alternate UniqueId systems/layouts; repeated/generalized property loop or generic cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

---

# 1. Status vocabulary"""
t = regex_once(
    t,
    r"# 0\. Current override — R3\.18AH closed / R3\.18AI active\n.*?\n---\n\n# 1\. Status vocabulary",
    new_override,
    "boundary current override",
)
write(p, t)


# ---------------------------------------------------------------------------
# Machine-readable continuity state.
# ---------------------------------------------------------------------------

p = ROOT / "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(p.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-21"
state["last_completed_read_only_audit"] = "R3.18AI"
state["current_pass"] = "R3.18AJ"
state["current_pass_kind"] = "contract-only exact-context admission / post-AG following-header boundary"
state["current_pass_goal"] = "Admit exactly the 17 complete seven-field header contexts and exact multiplicities observed by R3.18AI using exact_tuple_only membership, without inheriting earlier header contracts."
state["current_pass_stop_boundary"] = "Contract docs only. No production header composition, following payload, second later control, generalized property loop/cursor, next actor/frame or semantic/runtime/export widening."
state["last_completed_evidence_pass"] = "R3.18AI"
state["last_completed_evidence_outcome"] = "A — one post-AG following header exact 47/47; 17 exact complete contexts; Int=47; native-oracle mismatch 0; witness reselection 0; following payload/second-control 0/0; artifact 9424764320."
paths = state["next_files_to_read"]
ai_spec_path = "docs/continuity/MIMIR_R3_18AI_EXECUTION_SPEC.md"
ai_decision_path = "docs/continuity/MIMIR_R3_18AI_DECISION.md"
aj_spec_path = "docs/continuity/MIMIR_R3_18AJ_EXECUTION_SPEC.md"
for extra in (ai_decision_path, aj_spec_path):
    if extra in paths:
        raise SystemExit(f"continuity next_files_to_read unexpectedly already contains {extra}")
idx = paths.index(ai_spec_path) + 1
paths[idx:idx] = [ai_decision_path, aj_spec_path]
for closed in (
    "post-AG following-header production composition before R3.18AJ exact-context admission",
    "R3.18Z or R3.18P context inheritance at the R3.18AI/R3.18AJ boundary",
):
    if closed not in state["closed_now"]:
        state["closed_now"].append(closed)
state["r3_18ai"] = {
    "outcome": "A",
    "production_source_changed": False,
    "production_code_sha": PRODUCTION_SHA,
    "base_main_sha": BASE_MAIN,
    "base_tree_sha": BASE_TREE,
    "evidence_head_sha": AI_HEAD,
    "evidence_tree_sha": AI_TREE,
    "authority_run_id": int(AI_RUN),
    "authority_job_id": int(AI_JOB),
    "validation_pr": int(AI_PR),
    "validation_ci_run_id": int(AI_CI_RUN),
    "validation_ci_job_id": int(AI_CI_JOB),
    "artifact_id": int(AI_ARTIFACT),
    "artifact_size_bytes": int(AI_ARTIFACT_SIZE),
    "artifact_sha256": AI_ARTIFACT_DIGEST,
    "rows": 47,
    "published_ag_exact": 47,
    "following_header_exact": 47,
    "unique_exact_contexts": 17,
    "observed_tags": {"Int": 47},
    "native_oracle_mismatch": 0,
    "witness_reselection": 0,
    "following_payload_bits_consumed": 0,
    "second_later_control_bits_consumed": 0,
    "earlier_header_contract_inheritance_assumed": False,
    "production_cargo_fixture_corpus_support_mutation": [0, 0, 0, 0, 0],
    "privacy_scan": "PASS",
    "continuity_builder_run_id": int(BUILDER_RUN),
    "continuity_builder_job_id": int(BUILDER_JOB),
}
p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# Small canonical summary files are replaced completely.
# ---------------------------------------------------------------------------

current_state = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-21
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PRODUCTION_SHA}`
**Production tree:** `{PRODUCTION_TREE}`
**Production milestone:** `R3.18AG — bounded true-only property-control production after published R3.18AD payload`
**Last read-only evidence:** `R3.18AI — Outcome A / 47/47 following header / 17 exact contexts / Int=47 / native-oracle mismatch 0 / artifact {AI_ARTIFACT}`
**Current exact pass:** `R3.18AJ — post-AG following-header exact-context contract`

## Truthful boundary

Production remains R3.18AG `{PRODUCTION_SHA}` / `{PRODUCTION_TREE}`. R3.18AI changed no production source. On exactly the frozen 47-row lane, published R3.18AG reconstructed exactly 47/47 and the one following header matched the independent oracle 47/47 with 17 complete observed contexts, `Int=47`, mismatch 0, witness reselection 0 and following-payload/second-control consumption 0/0.

```text
canonical main before AI admission   {BASE_MAIN} / {BASE_TREE}
production SHA/tree                  {PRODUCTION_SHA} / {PRODUCTION_TREE}
production lib / focused test blobs  {LIB_BLOB} / {AG_TEST_BLOB}
R3.18AI execution spec               {AI_SPEC_BLOB}
evidence head/tree                   {AI_HEAD} / {AI_TREE}
authority run/job                    {AI_RUN} / {AI_JOB} SUCCESS
validation PR #{AI_PR}               closed unmerged
same-head normal CI                  {AI_CI_RUN} / {AI_CI_JOB} SUCCESS
artifact                             {AI_ARTIFACT} / {AI_ARTIFACT_SIZE} / sha256:{AI_ARTIFACT_DIGEST}
artifact integrity                   downloaded ZIP digest exact / inner manifest 9/9 PASS
continuity builder                   {BUILDER_RUN} / {BUILDER_JOB}
```

## Current gate

R3.18AJ is contract-only. Use the immutable R3.18AI header summary and admit exactly the 17 complete seven-field tuples with exact observed multiplicities and `exact_tuple_only` membership. Reject tag-only, component-only, Cartesian, versionless, fabricated and earlier-contract-inherited candidates. No Rust production source may change.

## Hard stop

Production remains frozen. Post-AG following-header production composition is not admitted until this contract closes. The following payload, another control, generalized/repeated property iteration or cursor, alternate unadmitted layouts, next actor/frame/lifecycle and raw-state/event/slice/skill/counterfactual/runtime/export behavior remain closed.
"""
write("docs/continuity/MIMIR_CURRENT_STATE.md", current_state)

handoff = f"""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AG** at `{PRODUCTION_SHA}` / `{PRODUCTION_TREE}`. R3.18AI is **Outcome A / CLOSED**: evidence `{AI_HEAD}` / tree `{AI_TREE}`, authority `{AI_RUN}/{AI_JOB}`, validation PR #{AI_PR} same-head CI `{AI_CI_RUN}/{AI_CI_JOB}`, artifact `{AI_ARTIFACT}` / `sha256:{AI_ARTIFACT_DIGEST}`. The downloaded ZIP digest matched GitHub metadata exactly and its inner manifest verified 9/9.

R3.18AI exact result: frozen rows 47/47, published AG exact 47/47, one following header exact 47/47, 17 exact complete seven-field contexts, Int=47, native-oracle mismatch 0, witness reselection 0; repeatability/header-truncation/corrupt-AG/wrong-actor/unresolved-lookup/wrong-context/post-payload-start-poison negatives 47/47; following-payload/second-control consumption 0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS; earlier-header contract inheritance assumed 0.

The active pass is **R3.18AJ**, contract-only. Create the exact boundary-specific context contract from the immutable R3.18AI summary: 17 complete tuples, exact multiplicities summing to 47, membership `exact_tuple_only`. Do not inherit R3.18Z/R3.18P contexts, publish production header composition, consume payload/control bits, or widen loop/actor/frame/semantic/runtime boundaries.

Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18AI_DECISION.md`, and `docs/continuity/MIMIR_R3_18AJ_EXECUTION_SPEC.md` before continuing.
"""
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)


# ---------------------------------------------------------------------------
# Progress ledger is append-only for the new admitted milestone.
# ---------------------------------------------------------------------------

p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
t = read(p)
ledger_marker = "## R3.18AI one-following-property-header evidence — Outcome A / CLOSED"
if ledger_marker in t:
    raise SystemExit("progress ledger already contains R3.18AI closure")
ledger = f"""

---

## R3.18AI one-following-property-header evidence — Outcome A / CLOSED

- Production unchanged: `{PRODUCTION_SHA}` / `{PRODUCTION_TREE}`.
- Canonical parent: `{BASE_MAIN}` / `{BASE_TREE}`.
- Evidence head/tree: `{AI_HEAD}` / `{AI_TREE}`.
- Authority run/job: `{AI_RUN}` / `{AI_JOB}` SUCCESS.
- Validation PR #{AI_PR}: closed unmerged; exact-head normal CI `{AI_CI_RUN}` / `{AI_CI_JOB}` SUCCESS.
- Immutable artifact: `{AI_ARTIFACT}` / {AI_ARTIFACT_SIZE} bytes / `sha256:{AI_ARTIFACT_DIGEST}`; downloaded ZIP exact; manifest 9/9 PASS.
- Frozen rows 47/47; published AG exact 47/47; following header exact 47/47; native-oracle mismatch 0; witness reselection 0.
- Exact contexts 17; tags Int=47; earlier-header contract inheritance assumed 0.
- Repeatability, truncation, corrupt-AG, wrong-actor, unresolved lookup, wrong-context and post-payload-start poison negatives PASS 47/47.
- Following payload/second later control bits 0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.
- Continuity builder: `{BUILDER_RUN}` / `{BUILDER_JOB}`.
- Admitted scope: structural evidence only. No production header composition, payload, later control, loop/cursor or semantic/runtime widening.

## NEXT — R3.18AJ exact-context contract

- Contract-only pass over the immutable R3.18AI header summary.
- Admit exactly 17 complete seven-field tuples and exact multiplicities summing to 47.
- Membership `exact_tuple_only`; no tag/component/Cartesian/versionless matching and no R3.18Z/R3.18P inheritance.
- Production remains R3.18AG. Following payload and later control remain closed.
"""
write(p, t.rstrip() + ledger + "\n")


# ---------------------------------------------------------------------------
# Final internal consistency checks before the workflow performs repo checks.
# ---------------------------------------------------------------------------

required = {
    "MIMIR_CONTINUE_HERE.md": ["CURRENT_PASS:\n  R3.18AJ", "R3_18AI_EVIDENCE_CLOSURE:", "CURRENT PASS CHECKLIST — R3.18AJ"],
    "MIMIR_KNOWLEDGE_GRAPH.md": ["R3.18AI one-following-property-header evidence after published AG control / Outcome A CLOSED", "R3.18AJ active post-AG", "106. `docs/continuity/MIMIR_R3_18AI_DECISION.md`", "107. `docs/continuity/MIMIR_R3_18AJ_EXECUTION_SPEC.md`"],
    "docs/continuity/MIMIR_BOUNDARY_LOCKS.md": ["R3.18AI closed / R3.18AJ active", "ACTIVE CONTRACT-ONLY GATE — R3.18AJ"],
    "docs/continuity/MIMIR_CURRENT_STATE.md": ["Current exact pass:** `R3.18AJ", "17 complete observed contexts"],
    "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md": ["active pass is **R3.18AJ**", "exact_tuple_only"],
    "docs/continuity/MIMIR_PROGRESS_LEDGER.md": [ledger_marker, "## NEXT — R3.18AJ exact-context contract"],
    "docs/continuity/MIMIR_R3_18AI_DECISION.md": ["Outcome:** **A", AI_ARTIFACT_DIGEST],
    "docs/continuity/MIMIR_R3_18AJ_EXECUTION_SPEC.md": ["**Status:** ACTIVE", "exact_tuple_only", "R3.18AK"],
}
for path, markers in required.items():
    text = read(path)
    for marker in markers:
        if marker not in text:
            raise SystemExit(f"{path}: required marker missing: {marker}")

state_check = json.loads(read("docs/continuity/MIMIR_CONTINUITY_STATE.json"))
if state_check["current_pass"] != "R3.18AJ" or state_check["last_completed_evidence_pass"] != "R3.18AI":
    raise SystemExit("continuity state current/evidence pass mismatch")
if state_check["r3_18ai"]["unique_exact_contexts"] != 17:
    raise SystemExit("continuity state R3.18AI context count mismatch")

print("PASS R3.18AI continuity generator")
print(f"builder={BUILDER_RUN}/{BUILDER_JOB}")
