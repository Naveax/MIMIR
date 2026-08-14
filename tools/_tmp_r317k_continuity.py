import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTINUE = ROOT / "MIMIR_CONTINUE_HERE.md"
GRAPH = ROOT / "MIMIR_KNOWLEDGE_GRAPH.md"
STATE_JSON = ROOT / "docs/continuity/MIMIR_CONTINUITY_STATE.json"
CURRENT = ROOT / "docs/continuity/MIMIR_CURRENT_STATE.md"
DECISION = ROOT / "docs/continuity/MIMIR_R3_17K_DECISION.md"
NEXT_SPEC = ROOT / "docs/continuity/MIMIR_R3_17L_EXECUTION_SPEC.md"

PROD = "7390e3b145372252caaa8fa1fe3e0cd13b83336c"
PROD_TREE = "eebe4e21de77a43b5d9d43a34a0bfb08e06bab02"
PARENT = "b0c0a4665e72da012d6447ca647db526a3da0020"
LIB_BLOB = "d811879bb647de5e5bb56930244b9fddaa4ec583"
GROUP_BLOB = "2e7cc89699c2754a4ac66eb091d6422700715a23"
TEST_BLOB = "bbad0b405f4f27af309c3b71f2f3ba0a4da60c7b"
ALLOW_SHA = "9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911"


def require_replace(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one exact replacement target, found {count}")
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# MIMIR_CONTINUE_HERE.md
# ---------------------------------------------------------------------------
text = CONTINUE.read_text(encoding="utf-8")
text = require_replace(
    text,
    "LAST_PRODUCTION_CODE_SHA:\n  9bfa837c69c4751f70ca63a17c65f0f89877ff32",
    f"LAST_PRODUCTION_CODE_SHA:\n  {PROD}",
    "continue production sha",
)
text = require_replace(
    text,
    "LAST_PRODUCTION_MILESTONE:\n  R3.17G — direct native evidence-admitted K2 decoder implementation",
    "LAST_PRODUCTION_MILESTONE:\n  R3.17K — direct native exact-contract K3 decoder implementation",
    "continue production milestone",
)
text = require_replace(
    text,
    "CURRENT_PASS:\n  R3.17K — direct native K3 decoder implementation for contract-admitted variants only",
    "CURRENT_PASS:\n  R3.17L — native K3 differential audit against regenerated real-replay witnesses",
    "continue current pass",
)
text = require_replace(
    text,
    "CURRENT_PASS_TYPE:\n  production implementation / direct one-value K3 decoder + exhaustive focused tests",
    "CURRENT_PASS_TYPE:\n  read-only differential audit / real-replay native-vs-pinned-oracle verification; production Rust forbidden",
    "continue current pass type",
)
text = require_replace(
    text,
    "CURRENT_PRODUCTION_HARD_STOP:\n  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload may be decoded natively\n  stop exactly at payload_end_bit / stop_bit after that one value\n  NO second property, next actor, next frame, unobserved K2, K3 or K4 family is admitted",
    "CURRENT_PRODUCTION_HARD_STOP:\n  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload OR one R3.17J-admitted K3 payload may be decoded natively\n  K3 is limited to exact Location / RigidBody / ReplicatedBoost / PickupNew structural-context allowlist membership\n  stop exactly at payload_end_bit / stop_bit after that one value\n  NO second property, next actor, next frame, lifecycle mutation, unobserved K2/K3 shape or K4 family is admitted",
    "continue production hard stop",
)
old_tail = """R3_17K_OPEN_BOUNDARY:
  implement separate direct one-value K3 API for Location / RigidBody / ReplicatedBoost / PickupNew
  preserve exact 1950-entry structural/context allowlist; do not replace it with field-range unions
  focused tests synthesize every admitted group and exhaustively reject absent current-lane tuples
  exact end-bit + rollback semantics remain mandatory
  preferred production scope: lib.rs + k3_admitted_groups.rs + r3_17k focused integration test

R3_17K_HARD_STOP:
  no second property / property-loop continuation
  no next actor / next frame / lifecycle mutation
  no K4, raw-state, event, replay-slice, skill, runtime or export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17K OUTCOME A IS PUBLISHED:
  R3.17L — native K3 differential audit against regenerated immutable R3.17I witness identities
"""
new_tail = f"""R3_17K_PRODUCTION_CLOSURE:
  Outcome A / production / exact R3.17J contract only
  production SHA: {PROD}
  production tree: {PROD_TREE}
  parent: {PARENT}
  authority run/job: 31836699291 / 94884467585 SUCCESS
  first lint-only run: 31836440825 / 94883657836 NOT AUTHORITY
  exact-candidate CI: 31837081536 / 94885655480 SUCCESS
  published-main CI: 31837383875 / 94886588065 SUCCESS
  lib.rs blob: {LIB_BLOB}
  k3 allowlist module blob: {GROUP_BLOB}
  focused test blob: {TEST_BLOB}
  production allowlist equality: 1950/1950 exact / SHA256 {ALLOW_SHA}
  focused positives: all 1950 exact groups PASS; exhaustive current-lane structural acceptance PASS
  full mimir-replay suite: PASS; workspace clippy: PASS; full repository verifier: PASS
  exact production scope: lib.rs + k3_admitted_groups.rs + r3_17k focused integration test
  Cargo/fixture/corpus/support-lane changes: none
  property-loop / actor / frame / lifecycle widening: none

R3_17L_OPEN_BOUNDARY:
  read-only differential audit; production Rust changes are forbidden
  freeze R3.17K production SHA/tree/blobs, R3.17J allowlist, R3.17I artifact/groups and pinned Boxcars SHA
  regenerate real witness payloads ephemerally from the frozen 47-replay lane
  deterministically cover at least one real occurrence for every one of the 1950 admitted exact groups
  compare tag/value variant, exact start/end/width, structural codec metadata, context and semantic value against the pinned oracle
  retain only privacy-safe structural identities/hashes in durable evidence; raw witness payload bytes remain ephemeral
  any mismatch or contract contradiction stops the pass; do not repair production inside the audit

R3_17L_HARD_STOP:
  no production Rust, Cargo, fixture, corpus or support-lane mutation
  no second property / property-loop continuation
  no next actor / next frame / lifecycle mutation
  no K4, raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.17L:
  choose only from the execution roadmap after R3.17L Outcome A; do not assume R3.18 before the audit is closed
"""
text = require_replace(text, old_tail, new_tail, "continue K to L boundary")
CONTINUE.write_text(text, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# MIMIR_KNOWLEDGE_GRAPH.md
# ---------------------------------------------------------------------------
graph = GRAPH.read_text(encoding="utf-8")
graph = require_replace(
    graph,
    "R3.17J K3 contract decision               |\nR3.17K active K3 implementation spec      |",
    "R3.17J K3 contract decision               |\nR3.17K K3 production decision             |\nR3.17L active K3 differential audit spec  |",
    "graph canonical nodes",
)
graph = require_replace(
    graph,
    "19. `docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json`\n20. `docs/continuity/MIMIR_R3_17K_EXECUTION_SPEC.md`\n21. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n22. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n23. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n24. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n25. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n26. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n27. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "19. `docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json`\n20. `docs/continuity/MIMIR_R3_17K_EXECUTION_SPEC.md`\n21. `docs/continuity/MIMIR_R3_17K_DECISION.md`\n22. `docs/continuity/MIMIR_R3_17L_EXECUTION_SPEC.md`\n23. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n24. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n25. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n26. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n27. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n28. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n29. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "graph reading order",
)
graph = require_replace(
    graph,
    " -> R3.17K direct native K3 decoder implementation: ACTIVE",
    f" -> R3.17K direct native K3 decoder implementation: PRODUCTION / CLOSED\n      production {PROD}\n      authority 31836699291 / 94884467585 SUCCESS\n      candidate CI 31837081536 / 94885655480 SUCCESS\n      published CI 31837383875 / 94886588065 SUCCESS\n      1950/1950 exact allowlist groups + exhaustive structural acceptance PASS\n -> R3.17L native K3 real-replay differential audit: ACTIVE / READ-ONLY",
    "graph chain K/L",
)
old_lock = """Production can natively decode exactly one already-resolved K1 scalar or one R3.17F-admitted K2 payload. K2 success stops exactly at its payload end bit and does not authorize another property, actor, frame or lifecycle mutation.

R3.17H closed Outcome A without widening production: all 469 immutable K2 witnesses matched exactly and all seven negative controls failed closed. PartyLeader `None`, non-Epic PartyLeader and every other unseen K2 variant remain closed.

R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` without widening production. R3.17J then froze exactly 1,950 structural/context groups with zero cross-product widening. R3.17K is the active production implementation pass; native K3 decode remains closed until that clean implementation is published and validated. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.
"""
new_lock = f"""Production at `{PROD}` can natively decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, or one R3.17J-admitted K3 payload. Every success stops exactly at its one-value end bit and does not authorize another property, actor, frame or lifecycle mutation.

R3.17H closed Outcome A without widening K2: all 469 immutable K2 witnesses matched exactly and all seven negative controls failed closed. PartyLeader `None`, non-Epic PartyLeader and every other unseen K2 variant remain closed.

R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups with zero cross-product widening; R3.17K implemented exactly that contract and passed the 1,950-positive plus exhaustive structural acceptance gate. R3.17L is now the mandatory read-only real-replay differential audit. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.
"""
graph = require_replace(graph, old_lock, new_lock, "graph capability lock")
insert_before = "\n## Authority rule\n"
if graph.count(insert_before) != 1:
    raise RuntimeError("graph authority insertion target mismatch")
k_section = f"""
## R3.17K K3 production closure

```text
production SHA              {PROD}
production tree             {PROD_TREE}
parent                      {PARENT}
authority run/job           31836699291 / 94884467585 SUCCESS
first lint-only run         31836440825 / 94883657836 NOT AUTHORITY
exact-candidate CI          31837081536 / 94885655480 SUCCESS
published-main CI           31837383875 / 94886588065 SUCCESS
lib.rs blob                 {LIB_BLOB}
k3 groups blob              {GROUP_BLOB}
focused test blob           {TEST_BLOB}
canonical allowlist         1950/1950 exact
allowlist SHA256            {ALLOW_SHA}
focused/exhaustive tests    PASS
full mimir-replay           PASS
workspace clippy            PASS
full repository verifier    PASS
scope                       lib.rs + k3_admitted_groups.rs + r3_17k test only
Cargo/fixture/corpus        unchanged
outcome                     A / production
next                        R3.17L read-only K3 differential audit
```
"""
graph = graph.replace(insert_before, "\n" + k_section + insert_before, 1)
GRAPH.write_text(graph, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# MIMIR_CURRENT_STATE.md — deliberately rewritten as a compact current receipt.
# ---------------------------------------------------------------------------
current = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.17K — direct native exact-contract K3 decoder implementation`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Completed K3 evidence:** `R3.17I — Outcome A / 47 of 47 / 1699169 occurrences / 1950 exact groups`
**Completed K3 contract:** `R3.17J — Outcome A / 1950 exact groups / zero cross-product widening`
**Completed K3 production:** `R3.17K — Outcome A / 1950 of 1950 exact groups + exhaustive structural acceptance`
**Current exact pass:** `R3.17L — native K3 real-replay differential audit`

## 1. Truthful production boundary

Production is now R3.17K. MIMIR may decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, or one R3.17J-admitted K3 payload and stop at the exact one-value end bit. K3 is limited to `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` with exact structural/context allowlist membership.

```text
production SHA               {PROD}
production tree              {PROD_TREE}
production parent            {PARENT}
lib.rs blob                  {LIB_BLOB}
k3 groups blob               {GROUP_BLOB}
focused K3 test blob         {TEST_BLOB}
R3.17J allowlist SHA256      {ALLOW_SHA}
R3.17K authority run/job     31836699291 / 94884467585 SUCCESS
R3.17K exact-candidate CI    31837081536 / 94885655480 SUCCESS
R3.17K published-main CI     31837383875 / 94886588065 SUCCESS
```

The first K implementation run `31836440825 / 94883657836` is not authority; it failed only a Clippy `manual_div_ceil` lint in the synthetic test writer. The corrected authority run repeated every substantive gate from scratch.

## 2. R3.17K production closure

```text
contract groups               1950 / 1950 exact
Location                      11
RigidBody                     1934
PickupNew                     4
ReplicatedBoost               1
independent allowlist equality PASS
all 1950 synthetic positives  PASS
exhaustive structural gate    PASS
vector size 20/21             rejected
RigidBody quat48              rejected
ReplicatedBoost RL223=false   rejected
exact one-value end           PASS
full mimir-replay suite       PASS
workspace clippy              PASS
full repository verifier      PASS
production scope              exactly 3 files
Cargo/fixture/corpus/support  unchanged
```

The production API is separate from K2 and exposes `ReplayNetworkK3DecodeContextV1`, vector/quaternion/value structures, `ReplayNetworkK3DecodeV1`, and `decode_replay_network_k3_v1`. Exact RigidBody tuple membership remains mandatory; independent field-range unions do not admit a value.

## 3. R3.17L exact next pass

R3.17L is read-only. Regenerate real K3 witnesses ephemerally from the frozen 47-replay R3.17I lane using pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`, cover at least one real occurrence for every one of the 1,950 admitted exact groups, then compare native tag/variant, context, exact bit start/end/width, structural codec metadata and semantic values against the oracle.

A mismatch is not fixed inside R3.17L. It produces Outcome C and sends the project back to corrective evidence/contract/implementation work. Durable audit output remains privacy-safe; raw real payload bytes stay ephemeral.

## 4. Still closed

```text
K4 payload decode
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
"""
CURRENT.write_text(current, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# MIMIR_CONTINUITY_STATE.json — preserve historical objects, update only current truth.
# ---------------------------------------------------------------------------
state = json.loads(STATE_JSON.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-14"
state["last_production_code_sha"] = PROD
state["last_production_milestone"] = "R3.17K"
state["last_production_milestone_name"] = "direct native exact-contract K3 decoder implementation"
state["current_pass"] = "R3.17L"
state["current_pass_kind"] = "read-only native K3 differential audit against regenerated R3.17I real-replay witnesses"
state["current_pass_goal"] = "Regenerate privacy-safe real K3 witnesses across all 1950 admitted exact groups and compare R3.17K native decode against pinned Boxcars on variant, context, structural metadata, exact bit range and semantic value."
state["current_pass_stop_boundary"] = "Read-only audit only; no production Rust/Cargo/fixture/corpus/support-lane mutation and no second property, actor/frame, lifecycle, K4, raw-state/event/skill/runtime/export widening."
state["last_completed_production_pass"] = "R3.17K"
state["last_completed_production_outcome"] = "A — exact R3.17J K3 contract implemented; 1950/1950 synthetic positives and exhaustive structural acceptance PASS; candidate and published-main CI SUCCESS"
closed = list(state.get("closed_now", []))
closed = ["native K4 attribute payload decode" if item == "native K3/K4 attribute payload decode" else item for item in closed]
if "native K4 attribute payload decode" not in closed:
    closed.insert(0, "native K4 attribute payload decode")
state["closed_now"] = closed
next_files = list(state.get("next_files_to_read", []))
for item in [
    "docs/continuity/MIMIR_R3_17K_DECISION.md",
    "docs/continuity/MIMIR_R3_17L_EXECUTION_SPEC.md",
]:
    if item not in next_files:
        try:
            idx = next_files.index("docs/continuity/MIMIR_R3_17K_EXECUTION_SPEC.md") + 1
        except ValueError:
            idx = len(next_files)
        next_files.insert(idx, item)
state["next_files_to_read"] = next_files
state["r3_17k"] = {
    "outcome": "A — admitted / production",
    "pre_pass_main_sha": PARENT,
    "production_sha": PROD,
    "production_tree": PROD_TREE,
    "source_lib_blob": LIB_BLOB,
    "source_k3_groups_blob": GROUP_BLOB,
    "focused_test_blob": TEST_BLOB,
    "canonical_allowlist_sha256": ALLOW_SHA,
    "canonical_groups_total": 1950,
    "location_groups": 11,
    "rigid_body_groups": 1934,
    "pickup_new_groups": 4,
    "replicated_boost_groups": 1,
    "first_non_authority_run": 31836440825,
    "first_non_authority_job": 94883657836,
    "first_non_authority_reason": "Clippy manual_div_ceil lint in synthetic test writer only",
    "authority_run": 31836699291,
    "authority_job": 94884467585,
    "exact_candidate_ci_run": 31837081536,
    "published_main_ci_run": 31837383875,
    "independent_allowlist_equality": "1950/1950 PASS",
    "synthetic_positive_groups": "1950/1950 PASS",
    "exhaustive_structural_acceptance": "PASS",
    "full_mimir_replay": "PASS",
    "workspace_clippy": "PASS",
    "full_repository_verifier": "PASS",
    "production_files": [
        "crates/mimir-replay/src/lib.rs",
        "crates/mimir-replay/src/k3_admitted_groups.rs",
        "crates/mimir-replay/tests/r3_17k_k3_attribute_decoder.rs",
    ],
    "cargo_fixture_corpus_support_mutation": "0/0/0/0",
    "next_pass": "R3.17L",
}
STATE_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# New canonical decision and next-pass spec.
# ---------------------------------------------------------------------------
decision = f"""# MIMIR — R3.17K Direct Native K3 Decoder Implementation Decision

**Date:** 2026-08-14
**Pass:** `R3.17K — direct native K3 decoder implementation for contract-admitted variants only`
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production Rust changed:** **YES, exact three-file admitted scope**

## Frozen authority

```text
pre-K canonical main         {PARENT}
R3.17J allowlist SHA256      {ALLOW_SHA}
production SHA               {PROD}
production tree              {PROD_TREE}
production parent            {PARENT}
lib.rs blob                  {LIB_BLOB}
k3 groups module blob        {GROUP_BLOB}
focused test blob            {TEST_BLOB}
authority run/job            31836699291 / 94884467585 SUCCESS
exact-candidate CI           31837081536 / 94885655480 SUCCESS
published-main CI            31837383875 / 94886588065 SUCCESS
```

The earlier run `31836440825 / 94883657836` is **not authority**. All substantive decode and test gates passed there, but workspace Clippy rejected the synthetic test writer's manual `(len + 7) / 8` ceiling division. The only correction was `.div_ceil(8)` in disposable test-generation tooling; the authoritative run repeated every gate from scratch.

## Exact admitted production scope

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/src/k3_admitted_groups.rs
crates/mimir-replay/tests/r3_17k_k3_attribute_decoder.rs
```

No Cargo manifest/lock, fixture, replay corpus, support lane, workflow or temporary generator entered the clean production commit.

## Implemented surface

R3.17K adds a K3-specific one-value API without widening the existing K2 API:

```text
ReplayNetworkK3DecodeContextV1
ReplayNetworkVector3V1
ReplayNetworkQuaternion56V1
ReplayNetworkRigidBodyV1
ReplayNetworkReplicatedBoostV1
ReplayNetworkPickupNewV1
ReplayNetworkK3ValueV1
ReplayNetworkK3DecodeV1
decode_replay_network_k3_v1(...)
```

The decoder implements only `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` under replay context `868.32 / net10`, with RL223 and structural acceptance constrained by the exact R3.17J allowlist.

## Contract preservation

Production constants were regenerated from the canonical R3.17J JSON and independently read back against that JSON before tests:

```text
Location                    11
RigidBody                 1934
PickupNew                    4
ReplicatedBoost              1
total                      1950
independent equality       1950/1950 PASS
cross-product widening        0
```

RigidBody acceptance remains final-tuple membership, not a union of independently observed field ranges. Vector size 20/21, quat48, absent structural tuples and ReplicatedBoost RL223=false remain fail-closed.

## Validation result

The focused integration suite synthesized at least one valid payload for every one of the 1,950 admitted exact groups and then exhaustively enumerated the finite current-lane structural domain to assert `accepted <=> canonical allowlist membership`.

Additional negatives cover wrong replay context, invalid start, unsupported tag, vector truncation, invalid quat56 reconstruction, quat48/truncation, sleeping RigidBody trailing velocity-shaped bits, ReplicatedBoost RL223=false, PickupNew truncation and one-value trailing-bit non-consumption.

```text
1950 synthetic positives           PASS
exhaustive structural acceptance   PASS
full mimir-replay suite            PASS
workspace Clippy -D warnings       PASS
full repository verifier           PASS
exact candidate CI                 PASS
published-main CI                  PASS
```

## Capability consequence

Production may now decode **one** already-resolved R3.17J-admitted K3 value in addition to the previously admitted one-value K1/K2 surfaces. This does not admit a second property, property loop, next actor/frame, actor lifecycle mutation, K4, raw-state extraction, event extraction, replay slicing, skill synthesis, runtime integration or export widening.

Synthetic success is not the final K3 oracle check. R3.17L must perform a separate real-replay differential audit before any later parser widening is considered.

## Next exact pass

Open `R3.17L — native K3 differential audit against regenerated real-replay witnesses`.
"""
DECISION.write_text(decision, encoding="utf-8", newline="\n")

spec = f"""# MIMIR R3.17L — Native K3 Real-Replay Differential Audit Execution Spec

**Pass type:** read-only differential audit
**Production mutation:** forbidden
**Production authority:** R3.17K Outcome A
**Contract authority:** R3.17J Outcome A
**Evidence authority:** R3.17I Outcome A

## Goal

Regenerate real K3 witness payloads ephemerally from the frozen 47-replay R3.17I lane and compare the published R3.17K native decoder against pinned Boxcars for every admitted exact structural/context group. This pass certifies the native implementation; it does not widen it.

## Frozen identities

```text
R3.17K production SHA       {PROD}
R3.17K production tree      {PROD_TREE}
lib.rs blob                 {LIB_BLOB}
k3 groups module blob       {GROUP_BLOB}
focused test blob           {TEST_BLOB}
R3.17K authority run/job    31836699291 / 94884467585 SUCCESS
R3.17K candidate CI         31837081536 / 94885655480 SUCCESS
R3.17K published-main CI    31837383875 / 94886588065 SUCCESS
R3.17J allowlist SHA256     {ALLOW_SHA}
R3.17I evidence head        8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
R3.17I authority run/job    31812804986 / 94807233173 SUCCESS
R3.17I artifact             9223916983
R3.17I artifact digest      sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
R3.17I groups SHA256        04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b
pinned Boxcars SHA          c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane       47
exact admitted groups       1950
```

Before audit work, fetch fresh `main`, verify that the three production blobs above are unchanged, and verify the canonical J allowlist and R3.17I artifact identities. If production moved, reconstruct current truth before continuing.

## Real-witness reconstruction

Use the exact frozen 47 replay identities from R3.17I; do not widen the corpus. Instrument the pinned Boxcars oracle only at already-resolved K3 payload boundaries. Regenerate real payload observations ephemerally and deterministically select at least one real witness for **every one of the 1,950 R3.17J exact groups**.

The R3.17I group set is evidence-derived, so zero coverage for any admitted group is a contradiction or reconstruction failure, not permission to silently skip it.

Durable evidence may contain replay identity hashes/labels, frame/actor/property structural coordinates, context, exact bit ranges, packed structural codes, safe numeric/spatial values when required for comparison, and payload hashes. Do not persist unrelated player/account text or raw real payload bytes.

## Required native-vs-oracle comparisons

For every selected real witness, compare:

```text
resolved K3 tag / semantic variant
version 868.32 / net10 / RL223 context
payload_start_bit
payload_end_bit
payload_width
exact structural packed code
native success vs oracle success
```

Tag-specific comparisons:

### Location

Compare selected vector size, component width, raw x/y/z integer components, and semantic x/y/z.

### RigidBody

Compare sleeping branch, location vector structure/value, quaternion representation (`largest`, raw a/b/c, reconstructed x/y/z/w), and awake-only linear/angular vector structure/value. Sleeping witnesses must end immediately after quat56 and must not consume velocity-shaped trailing bits.

### ReplicatedBoost

Compare `grant_count`, `boost_amount`, `unused1`, `unused2`, exact 32-bit width and RL223=true gate.

### PickupNew

Compare presence branch, optional signed i32 instigator/reference, `picked_up`, and exact 9/41-bit width.

## Floating-point comparison rule

Before declaring equality, inspect the exact pinned Boxcars arithmetic for vector and quaternion reconstruction. If native and oracle perform the same operations in the same precision/order, require exact f32 bit equality. If the pinned source uses a materially different but mathematically equivalent operation order, define and persist a deterministic comparison rule before evaluating witnesses; do not improvise tolerances after observing mismatches.

## Negative controls

Regenerate or synthesize bounded controls that verify fail-closed behavior for at least:

```text
wrong major / minor / net_version
Location context/size pair absent from allowlist
vector selected size 20 / 21
vector truncation
RigidBody structural tuple absent from allowlist
RigidBody quat48 / quat56 truncation / invalid reconstruction
ReplicatedBoost RL223=false / truncation
PickupNew truncation
unsupported non-K3 tag
invalid payload start
trailing-bit non-consumption
atomic failure / no partial value escape
```

Negative controls do not authorize new shapes.

## Required gates

```text
fresh production identity                         PASS
47/47 replay identity verification                PASS
pinned Boxcars oracle decode                       47/47
R3.17I group reconstruction                        1950/1950
real witness group coverage                        1950/1950 minimum
native decode success on admitted witnesses        100%
tag / semantic variant match                       100%
context match                                      100%
payload start / end / width match                  100%
structural metadata / packed-code match            100%
semantic value match under predeclared rule        100%
negative controls                                  100%
bit monotonicity / packed-payload failures         0 / 0
privacy scan                                       PASS
production/Cargo/fixture/corpus/support mutation   0/0/0/0/0
normal CI on exact audit head                      PASS
```

## Outcome rules

- **Outcome A:** all 1,950 exact groups receive real witness coverage, every native/oracle comparison is exact under the predeclared numeric rule, negatives fail closed, privacy passes and mutation counts remain zero.
- **Outcome B:** reproducible evidence is insufficient to reconstruct one or more previously admitted groups; stop with targeted evidence work only. Do not widen or repair production.
- **Outcome C:** native/oracle mismatch, structural contradiction, source-identity contradiction or decoder defect. Stop. Repair evidence/contract/implementation in a separately admitted pass.

## Hard stop

R3.17L must not modify production Rust, Cargo files, fixtures, replay corpus or support lane. It must not consume a second property or advance actor/frame/lifecycle state. K4, raw-state, event, replay-slice, skill, runtime and export work remain closed.

## After Outcome A

Re-read `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md` and select the first dependency-valid unfinished pass. Do not pre-admit R3.18 merely because K3 differential closure succeeded.
"""
NEXT_SPEC.write_text(spec, encoding="utf-8", newline="\n")

print("R3.17K continuity closure generated")
print(f"production={PROD}")
print("next=R3.17L read-only differential audit")
