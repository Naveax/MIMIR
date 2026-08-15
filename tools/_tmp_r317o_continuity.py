from __future__ import annotations

import json
import re
from pathlib import Path

BASE_MAIN = "492cc8218be7abc6db8f75acaea33d009ab2f175"
PRE_O_MAIN = "3392c28ba8ec7d72766303646c0ceb57ed1e5a19"
PROD_TREE = "a66c47d7fb58da508188e64d42141987a0021a07"
LIB_BLOB = "0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8"
K4_GROUP_BLOB = "103503e25bc5af48381df021ab58133694fcece6"
K4_NATIVE_BLOB = "a9c41f3bb11343165183ac9c815ab8fdf085936c"
TEST_BLOB = "70437244bb49224281ee3a2e745e7b8a4b7a093a"
AUTH_HEAD = "900d7eb122f10126558f13ea2c185cdb8c69fe1b"
AUTH_RUN = 31885987240
AUTH_JOB = 95015252318
CANDIDATE_CI_RUN = 31886194387
CANDIDATE_CI_JOB = 95015736899
PUBLISHED_CI_RUN = 31886353485
PUBLISHED_CI_JOB = 95016105618
GROUP_SHA = "80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b"
GROUP_BLOB = "b5fa6aaa729772ab3d113703952effe2346c9866"
CONTRACT_BLOB = "76deabf8241b419ca224645106d2a19b041e20f8"
M_EVIDENCE_HEAD = "a50f09857f36ac52cec30b4bf3efbde9e15bb564"
M_RUN = 31881779861
M_JOB = 95005282281
M_ARTIFACT = 9246249473
M_ARTIFACT_DIGEST = "sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987"
BOXCARS = "c70e77df7af81b436cb545d070bb90c82f562d0b"

ROOT = Path.cwd()
CONTINUE = ROOT / "MIMIR_CONTINUE_HERE.md"
GRAPH = ROOT / "MIMIR_KNOWLEDGE_GRAPH.md"
STATE = ROOT / "docs/continuity/MIMIR_CONTINUITY_STATE.json"
CURRENT = ROOT / "docs/continuity/MIMIR_CURRENT_STATE.md"
DECISION = ROOT / "docs/continuity/MIMIR_R3_17O_DECISION.md"
P_SPEC = ROOT / "docs/continuity/MIMIR_R3_17P_EXECUTION_SPEC.md"


def exact(text: str, old: str, new: str, label: str, count: int = 1) -> str:
    actual = text.count(old)
    if actual != count:
        raise RuntimeError(f"{label}: expected {count} occurrence(s), found {actual}")
    return text.replace(old, new, count)


def regex_once(text: str, pattern: str, repl: str, label: str) -> str:
    out, n = re.subn(pattern, repl, text, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f"{label}: expected one regex match, found {n}")
    return out


def normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n")).rstrip() + "\n"


def update_continue() -> None:
    text = CONTINUE.read_text(encoding="utf-8")
    text = exact(text, "LAST_PRODUCTION_CODE_SHA:\n  7390e3b145372252caaa8fa1fe3e0cd13b83336c", f"LAST_PRODUCTION_CODE_SHA:\n  {BASE_MAIN}", "continue production sha")
    text = exact(text, "LAST_PRODUCTION_MILESTONE:\n  R3.17K — direct native exact-contract K3 decoder implementation", "LAST_PRODUCTION_MILESTONE:\n  R3.17O — direct native exact-contract K4 decoder implementation", "continue production milestone")
    text = exact(text, "CURRENT_PASS:\n  R3.17O — direct native exact-contract K4 decoder implementation", "CURRENT_PASS:\n  R3.17P — native K4 real-replay differential audit", "continue current pass")
    text = exact(text, "CURRENT_PASS_TYPE:\n  production implementation / exact 161-group contract only", "CURRENT_PASS_TYPE:\n  read-only real-replay differential audit / exact 161-group certification", "continue pass type")
    old_lock = """CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload OR one R3.17J-admitted K3 payload may be decoded natively
  K3 is limited to exact Location / RigidBody / ReplicatedBoost / PickupNew structural-context allowlist membership
  stop exactly at payload_end_bit / stop_bit after that one value
  R3.17N admits the exact K4 contract but production K4 decode is not yet implemented
  NO second property, next actor, next frame, lifecycle mutation, unobserved K2/K3/K4 shape or family is admitted"""
    new_lock = """CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload OR one R3.17J-admitted K3 payload OR one R3.17N-admitted K4 payload may be decoded natively
  K3 remains limited to its exact R3.17J structural/context allowlist; K4 remains limited to the exact 161 R3.17N tuples
  stop exactly at payload_end_bit / stop_bit after that one value
  R3.17O production is implemented and published; R3.17P must certify it against regenerated real-replay witnesses before any later parser widening
  NO second property, next actor, next frame, lifecycle mutation, unobserved K2/K3/K4 shape or family is admitted"""
    text = exact(text, old_lock, new_lock, "continue hard stop")
    old_open = """R3_17O_OPEN_BOUNDARY:
  production implementation; exact R3.17N 161-group K4 contract only
  direct native one-value K4 decoder; arbitrary unaligned start; checked arithmetic; atomic failure
  all 161 admitted rows require positive coverage and independent allowlist equality
  Reservation / DemolishFx / DemolishExtended / LoadoutsOnline combinations remain exact-group coupled
  Cargo/fixture/corpus/support lane stay unchanged

R3_17O_HARD_STOP:
  no second property / property-loop continuation
  no next actor / next frame / lifecycle mutation
  no raw-state, event, replay-slice, skill, runtime or export widening
  no real-replay differential audit inside implementation pass

NEXT PASS AFTER R3.17O:
  only if Outcome A, open separate R3.17P native K4 real-replay differential audit; R3.18 remains closed"""
    new_open = f"""R3_17O_PRODUCTION_CLOSURE:
  Outcome A / production / exact R3.17N 161-group contract only
  pre-O canonical main: {PRE_O_MAIN}
  production SHA: {BASE_MAIN}
  production tree: {PROD_TREE}
  parent: {PRE_O_MAIN}
  authority head: {AUTH_HEAD}
  authority run/job: {AUTH_RUN} / {AUTH_JOB} SUCCESS
  exact-candidate CI: {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
  published-main CI: {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
  lib.rs blob: {LIB_BLOB}
  k4 allowlist module blob: {K4_GROUP_BLOB}
  k4 native module blob: {K4_NATIVE_BLOB}
  focused test blob: {TEST_BLOB}
  production allowlist equality: 161/161 exact / SHA256 {GROUP_SHA} / cross-product widening 0
  focused positives: all 161 exact groups PASS; focused malformed/context/cross-product negatives PASS
  full mimir-replay suite: PASS; workspace check/test/clippy: PASS; full repository verifier: PASS
  exact production scope: lib.rs + k4_admitted_groups.rs + k4_native.rs + r3_17o focused integration test
  Cargo/fixture/corpus/support-lane changes: none
  property-loop / actor / frame / lifecycle widening: none

R3_17P_OPEN_BOUNDARY:
  read-only native K4 real-replay differential audit; production mutation forbidden
  reuse the exact frozen 47-replay R3.17M lane and pinned Boxcars oracle
  regenerate at least one real witness for every one of the 161 R3.17N exact groups
  compare native/oracle tag, context, start/end/width, exact shape and semantic value
  private account/player/title text may be compared in memory only; durable evidence must remain privacy-safe

R3_17P_HARD_STOP:
  no production Rust, Cargo, fixture, corpus or support-lane mutation
  no second property / property-loop continuation
  no next actor / next frame / lifecycle mutation
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.17P:
  only after Outcome A, re-read the execution roadmap and select the first dependency-valid unfinished pass; R3.18 is not pre-admitted"""
    text = exact(text, old_open, new_open, "continue O->P boundary")
    CONTINUE.write_text(normalize(text), encoding="utf-8", newline="\n")


def update_graph() -> None:
    text = GRAPH.read_text(encoding="utf-8")
    text = exact(text, "R3.17O active K4 production spec              |", "R3.17O K4 production decision                   |\nR3.17P active K4 differential spec                |", "graph root")
    text = exact(text, "30. `docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md`\n31. `docs/continuity/MIMIR_PASS_PROTOCOL.md`", "30. `docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md`\n31. `docs/continuity/MIMIR_R3_17O_DECISION.md`\n32. `docs/continuity/MIMIR_R3_17P_EXECUTION_SPEC.md`\n33. `docs/continuity/MIMIR_PASS_PROTOCOL.md`", "graph reading order head")
    text = text.replace("32. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n33. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n34. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n35. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n36. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n37. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`", "34. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n35. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n36. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n37. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n38. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n39. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`", 1)
    text = exact(text, " -> R3.17O direct native exact-contract K4 decoder implementation: ACTIVE / PRODUCTION", f""" -> R3.17O direct native exact-contract K4 decoder implementation: PRODUCTION / CLOSED
      production {BASE_MAIN}
      authority {AUTH_HEAD} / {AUTH_RUN} / {AUTH_JOB} SUCCESS
      candidate CI {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
      published CI {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
      161/161 exact allowlist equality / cross-product widening 0 / focused+workspace+full verifier PASS
 -> R3.17P native K4 real-replay differential audit: ACTIVE / READ-ONLY""", "graph replay chain")
    old_cap = "Production at `7390e3b145372252caaa8fa1fe3e0cd13b83336c` can natively decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, or one R3.17J-admitted K3 payload. Every success stops exactly at its one-value end bit and does not authorize another property, actor, frame or lifecycle mutation."
    new_cap = f"Production at `{BASE_MAIN}` can natively decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload. Every success stops exactly at its one-value end bit and does not authorize another property, actor, frame or lifecycle mutation. R3.17P is the separate real-replay certification pass for the K4 implementation."
    text = exact(text, old_cap, new_cap, "graph capability")
    old_tail = "R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups with zero cross-product widening; R3.17K implemented exactly that contract; R3.17L matched all 1,950 exact groups against regenerated real-replay witnesses with zero mismatch. R3.17M observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups. R3.17N then admitted exactly those 161 groups byte-for-byte with zero cross-product widening. R3.17O is now the separate native K4 implementation pass; property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed."
    new_tail = "R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups; R3.17K implemented them; R3.17L matched all 1,950 against real replay witnesses. R3.17M then observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups; R3.17N admitted those 161 groups byte-for-byte; R3.17O implemented exactly that contract with zero cross-product widening. R3.17P is now the separate native K4 real-replay differential audit. Property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed."
    text = exact(text, old_tail, new_tail, "graph narrative")
    closure = f"""

## R3.17O K4 production closure

```text
production SHA              {BASE_MAIN}
production tree             {PROD_TREE}
production parent           {PRE_O_MAIN}
authority head              {AUTH_HEAD}
authority run/job           {AUTH_RUN} / {AUTH_JOB} SUCCESS
exact candidate CI          {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
published main CI           {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
lib.rs blob                 {LIB_BLOB}
k4 groups blob              {K4_GROUP_BLOB}
k4 native blob              {K4_NATIVE_BLOB}
focused test blob           {TEST_BLOB}
contract equality           161/161 exact
cross-product widening      0
Cargo/fixture/corpus/support unchanged
outcome                     A / PRODUCTION
```

R3.17P must certify all 161 exact groups against regenerated real-replay witnesses before later parser widening is considered.
"""
    if "## R3.17O K4 production closure" in text:
        raise RuntimeError("graph already contains O closure")
    text = normalize(text) + closure.lstrip("\n")
    GRAPH.write_text(normalize(text), encoding="utf-8", newline="\n")


def write_current() -> None:
    text = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-15
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{BASE_MAIN}`
**Production milestone:** `R3.17O — direct native exact-contract K4 decoder implementation`
**Completed K3 differential:** `R3.17L — Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch`
**Completed K4 evidence:** `R3.17M — Outcome A / 39463 occurrences / 161 exact structural-context groups / all 11 tags observed`
**Completed K4 contract:** `R3.17N — Outcome A / 161/161 byte-identical groups / zero cross-product widening`
**Completed K4 production:** `R3.17O — Outcome A / 161/161 exact contract implementation / zero widening`
**Current exact pass:** `R3.17P — native K4 real-replay differential audit`

## 1. Truthful production boundary

Production is now R3.17O. MIMIR may decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload and stop at the exact one-value end bit. K4 success requires exact membership in the canonical 161-row structural/context allowlist; independent field unions do not admit a value.

```text
production SHA               {BASE_MAIN}
production tree              {PROD_TREE}
production parent            {PRE_O_MAIN}
lib.rs blob                  {LIB_BLOB}
k4 groups blob               {K4_GROUP_BLOB}
k4 native blob               {K4_NATIVE_BLOB}
focused K4 test blob         {TEST_BLOB}
R3.17N allowlist SHA256      {GROUP_SHA}
R3.17O authority run/job     {AUTH_RUN} / {AUTH_JOB} SUCCESS
R3.17O exact-candidate CI    {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
R3.17O published-main CI     {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
```

The first two disposable implementation runs are not authority. `31885789107 / 95014781583` stopped before Rust because temporary tooling incorrectly assumed the canonical JSONL was tuple-sorted. `31885905139 / 95015053496` stopped before Rust because the independent equality checker compared non-admission evidence fields. The authoritative third run repeated every substantive gate after those plumbing-only corrections.

## 2. R3.17O production closure

```text
contract groups               161 / 161 exact
independent allowlist equality PASS
cross-product widening        0
all 161 synthetic positives   PASS
wrong context/tag/start        rejected
truncation                     rejected
Reservation malformed/text    rejected
Demolish cross-products        rejected
LoadoutsOnline unknown/cross   rejected
unobserved TeamLoadout version rejected
RL223 tuple mismatch           rejected
exact one-value end            PASS
full mimir-replay suite        PASS
workspace check/test/clippy    PASS
full repository verifier       PASS
production scope               exactly 4 files
Cargo/fixture/corpus/support   unchanged
```

The K4 API is separate and exposes `ReplayNetworkK4DecodeContextV1`, K4 semantic structures, `ReplayNetworkK4DecodeV1`, `R3_17N_K4_ADMITTED_GROUPS_V1`, and `decode_replay_network_k4_v1`. `LoadoutsOnline` receives the caller-resolved object table so product-attribute object IDs can be resolved without inventing a new lookup authority.

## 3. Evidence and contract authority

R3.17M remains the real-replay wire-format evidence authority: 47/47 pinned Boxcars decode, 39,463 K4 occurrences, all 11 target tags, 161 exact groups, 617 privacy-safe witnesses, zero structural failures. R3.17N remains the exact contract authority: the 161 admitted groups are byte-identical to the R3.17M group artifact and cross-product widening is zero.

```text
R3.17M authority head         {M_EVIDENCE_HEAD}
R3.17M run/job                {M_RUN} / {M_JOB} SUCCESS
R3.17M artifact               {M_ARTIFACT}
R3.17M artifact digest        {M_ARTIFACT_DIGEST}
R3.17N group SHA256           {GROUP_SHA}
R3.17N group blob             {GROUP_BLOB}
R3.17N contract blob          {CONTRACT_BLOB}
pinned Boxcars SHA            {BOXCARS}
supported replay lane         47
```

## 4. R3.17P exact next pass

R3.17P is read-only. Regenerate real K4 payload witnesses from the exact frozen 47-replay R3.17M lane and certify the published R3.17O native decoder against pinned Boxcars for **all 161 exact groups**. Compare tag, version/context, payload start/end/width, exact structural shape and semantic value. Sensitive account/player/title text may be compared in memory but must not be written in clear text to durable evidence.

Outcome A requires 161/161 real group coverage and 100% native/oracle equality, negative controls, privacy PASS, zero production/Cargo/fixture/corpus/support mutation, and normal CI on the exact audit head.

## 5. Still closed

```text
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/corpus/support-lane expansion
R3.18 reopening before R3.17P Outcome A + roadmap dependency check
```
"""
    CURRENT.write_text(normalize(text), encoding="utf-8", newline="\n")


def update_state() -> None:
    data = json.loads(STATE.read_text(encoding="utf-8"))
    data["updated_date"] = "2026-08-15"
    data["last_production_code_sha"] = BASE_MAIN
    data["last_production_milestone"] = "R3.17O"
    data["last_production_milestone_name"] = "direct native exact-contract K4 decoder implementation"
    data["current_pass"] = "R3.17P"
    data["current_pass_kind"] = "read-only native K4 real-replay differential audit"
    data["current_pass_goal"] = "Regenerate real witnesses for all 161 R3.17N exact K4 groups from the frozen 47-replay R3.17M lane and require 100% native-vs-Boxcars equality for tag/context/start/end/width/shape/semantic value with privacy-safe durable evidence."
    data["current_pass_stop_boundary"] = "Read-only audit; no production Rust/Cargo/fixture/corpus/support mutation, no second property/property loop, actor/frame/lifecycle, raw-state/event/skill/runtime/export widening, and no R3.18 reopening inside the audit."
    data["last_completed_production_pass"] = "R3.17O"
    data["last_completed_production_outcome"] = "A — exact R3.17N K4 contract implemented; 161/161 synthetic positives, exact allowlist equality, zero cross-product widening, focused negatives, workspace and published-main CI SUCCESS"
    closed = [x for x in data.get("closed_now", []) if not x.startswith("native K4 attribute payload decode")]
    certification = "K4 real-replay certification beyond synthetic contract tests until R3.17P Outcome A"
    if certification not in closed:
        closed.insert(0, certification)
    data["closed_now"] = closed
    reads = data.get("next_files_to_read", [])
    for path in ["docs/continuity/MIMIR_R3_17O_DECISION.md", "docs/continuity/MIMIR_R3_17P_EXECUTION_SPEC.md"]:
        if path not in reads:
            insert_at = reads.index("docs/continuity/MIMIR_PASS_PROTOCOL.md") if "docs/continuity/MIMIR_PASS_PROTOCOL.md" in reads else len(reads)
            reads.insert(insert_at, path)
    data["next_files_to_read"] = reads
    data["r3_17o"] = {
        "outcome": "A — admitted / production",
        "pass_type": "direct native exact-contract K4 one-value decoder implementation",
        "pre_pass_main_sha": PRE_O_MAIN,
        "production_sha": BASE_MAIN,
        "production_tree": PROD_TREE,
        "production_parent": PRE_O_MAIN,
        "authority_head": AUTH_HEAD,
        "workflow_run": AUTH_RUN,
        "workflow_job": AUTH_JOB,
        "exact_candidate_ci_run": CANDIDATE_CI_RUN,
        "exact_candidate_ci_job": CANDIDATE_CI_JOB,
        "published_main_ci_run": PUBLISHED_CI_RUN,
        "published_main_ci_job": PUBLISHED_CI_JOB,
        "lib_blob": LIB_BLOB,
        "k4_admitted_groups_blob": K4_GROUP_BLOB,
        "k4_native_blob": K4_NATIVE_BLOB,
        "focused_test_blob": TEST_BLOB,
        "contract_groups": 161,
        "allowlist_equality": "161/161 exact",
        "admitted_groups_sha256": GROUP_SHA,
        "cross_product_widening": 0,
        "focused_positive_coverage": "161/161 PASS",
        "focused_negative_controls": "PASS",
        "mimir_replay_suite": "PASS",
        "workspace_check_test_clippy": "PASS",
        "full_repository_verifier": "PASS",
        "production_scope_files": [
            "crates/mimir-replay/src/lib.rs",
            "crates/mimir-replay/src/k4_admitted_groups.rs",
            "crates/mimir-replay/src/k4_native.rs",
            "crates/mimir-replay/tests/r3_17o_k4_attribute_decoder.rs",
        ],
        "production_cargo_fixture_corpus_support_mutation": "4 files / 0/0/0/0 non-source lane mutations",
        "next_pass": "R3.17P",
    }
    STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_decision() -> None:
    text = f"""# MIMIR — R3.17O Direct Native K4 Decoder Implementation Decision

**Date:** 2026-08-15
**Pass:** `R3.17O — direct native exact-contract K4 decoder implementation`
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production Rust changed:** **YES, exact four-file admitted scope**

## Frozen authority

```text
pre-O canonical main         {PRE_O_MAIN}
R3.17N allowlist SHA256      {GROUP_SHA}
production SHA               {BASE_MAIN}
production tree              {PROD_TREE}
production parent            {PRE_O_MAIN}
lib.rs blob                  {LIB_BLOB}
k4 groups module blob        {K4_GROUP_BLOB}
k4 native module blob        {K4_NATIVE_BLOB}
focused test blob            {TEST_BLOB}
authority head               {AUTH_HEAD}
authority run/job            {AUTH_RUN} / {AUTH_JOB} SUCCESS
exact-candidate CI           {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
published-main CI            {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
```

The earlier disposable runs `31885789107 / 95014781583` and `31885905139 / 95015053496` are **not authority**. The first stopped before Rust because temporary generation tooling incorrectly assumed tuple-sorted contract rows. The second stopped before Rust because the independent equality checker compared the evidence-only `occurrences` field. Neither changed the K4 contract. The authoritative third run repeated every substantive gate from scratch.

## Exact admitted production scope

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/src/k4_admitted_groups.rs
crates/mimir-replay/src/k4_native.rs
crates/mimir-replay/tests/r3_17o_k4_attribute_decoder.rs
```

No Cargo manifest/lockfile, fixture, replay corpus, support lane, workflow or temporary generator entered the clean production commit.

## Implemented surface

R3.17O adds a K4-specific one-value API while preserving the earlier K1/K2/K3 APIs. The public surface includes `ReplayNetworkK4DecodeContextV1`, K4 loadout/reservation/actor/product semantic structures, `ReplayNetworkK4ValueV1`, `ReplayNetworkK4DecodeV1`, `R3_17N_K4_ADMITTED_GROUPS_V1`, and `decode_replay_network_k4_v1`.

The decoder covers exactly these 11 contract families: `CamSettings`, `TeamPaint`, `TeamLoadout`, `ClubColors`, `Reservation`, `StatEvent`, `PlayerHistoryKey`, `DemolishFx`, `DemolishExtended`, `ExtendedExplosion`, and `LoadoutsOnline`. `LoadoutsOnline` accepts the caller-resolved replay object table to resolve product-attribute object IDs; it does not create a second lookup authority.

## Contract preservation

The production allowlist was generated from the canonical R3.17N JSONL and independently read back before tests:

```text
canonical contract rows      161
production allowlist rows    161
missing                       0
extra                         0
cross-product widening        0
allowlist equality            161/161 PASS
allowlist SHA256              {GROUP_SHA}
```

Acceptance is exact tuple membership over tag, replay version 868.32, net10, RL223 context, payload width and structural shape. Reservation, demolition-vector and nested online-loadout branches are not widened by taking independent field unions.

## Validation result

The focused integration suite materialized a valid synthetic payload for every admitted row and checked exact tag, shape, width, end bit and repeatability. Negatives cover wrong context/tag/start, truncation, malformed reservation text, unobserved TeamLoadout version, demolition cross-products, LoadoutsOnline unknown/cross-product branches, and RL223 tuple mismatch.

```text
161 synthetic positives            PASS
independent allowlist equality      PASS
cross-product widening              0
focused negative controls           PASS
full mimir-replay suite             PASS
workspace check/test/clippy         PASS
full repository verifier            PASS
exact candidate CI                  PASS
published-main CI                   PASS
```

## Capability consequence

Production may now decode **one** already-resolved R3.17N-admitted K4 value in addition to previously admitted K1/K2/K3 one-value surfaces. Success stops exactly at that payload end. This does not admit a second property, property-loop continuation, next actor/frame, actor lifecycle mutation, raw-state extraction, event extraction, replay slicing, skill synthesis, runtime integration or export widening.

Synthetic contract success is not the final K4 oracle certification. R3.17P must compare the published native decoder against regenerated real-replay witnesses for all 161 exact groups before later parser widening is considered.

## Next exact pass

Open `R3.17P — native K4 real-replay differential audit against regenerated R3.17M witnesses`.
"""
    DECISION.write_text(normalize(text), encoding="utf-8", newline="\n")


def write_p_spec() -> None:
    text = f"""# MIMIR R3.17P — Native K4 Real-Replay Differential Audit Execution Spec

**Pass type:** read-only differential audit
**Production mutation:** forbidden
**Production authority:** R3.17O Outcome A
**Contract authority:** R3.17N Outcome A
**Evidence authority:** R3.17M Outcome A

## Goal

Regenerate real K4 witnesses ephemerally from the frozen 47-replay R3.17M lane and compare the published R3.17O native decoder against pinned Boxcars for every one of the 161 admitted exact structural/context groups. This pass certifies production; it does not widen it.

## Frozen identities

```text
R3.17O production SHA       {BASE_MAIN}
R3.17O production tree      {PROD_TREE}
lib.rs blob                 {LIB_BLOB}
k4 groups module blob       {K4_GROUP_BLOB}
k4 native module blob       {K4_NATIVE_BLOB}
focused test blob           {TEST_BLOB}
R3.17O authority head       {AUTH_HEAD}
R3.17O authority run/job    {AUTH_RUN} / {AUTH_JOB} SUCCESS
R3.17O candidate CI         {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
R3.17O published-main CI    {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
R3.17N allowlist SHA256     {GROUP_SHA}
R3.17M evidence head        {M_EVIDENCE_HEAD}
R3.17M authority run/job    {M_RUN} / {M_JOB} SUCCESS
R3.17M artifact             {M_ARTIFACT}
R3.17M artifact digest      {M_ARTIFACT_DIGEST}
pinned Boxcars SHA          {BOXCARS}
supported replay lane       47
exact admitted groups       161
```

Before audit work, fetch fresh `main`, verify all R3.17O production blobs and the canonical R3.17N allowlist, then verify the R3.17M artifact and exact 47 replay identities. If production moved, reconstruct current truth before continuing.

## Real-witness reconstruction

Use exactly the frozen 47 replay identities from R3.17M; do not widen the corpus. Instrument the pinned Boxcars oracle at the already-resolved K4 payload boundary, or reuse the previously verified R3.17M instrumentation only after exact source/patch identity checks. Regenerate deterministic structural observations and select at least one real witness for **every one of the 161 R3.17N groups**.

For `LoadoutsOnline`, supply the native decoder with the exact caller-resolved replay object table corresponding to that replay. Do not synthesize object names from the product branch being tested.

Durable evidence may include replay identity hashes/labels, frame/actor/property structural coordinates, version/context, bit ranges, structural shape, payload hashes, safe numeric fields and boolean/integer match flags. Never persist unrelated account/player names, Epic IDs, titles or other private text in clear form.

## Required native-vs-oracle comparisons

For every selected real witness compare:

```text
resolved K4 tag / semantic variant
version 868.32 / net10 / RL223 context
payload_start_bit
payload_end_bit
payload_width
exact structural shape
native success vs oracle success
semantic value
```

Tag-specific semantic requirements:

- `CamSettings`: compare all seven f32 fields by exact f32 bit identity when oracle operation order is identical.
- `TeamPaint`: compare all three u8 and two u32 fields exactly.
- `TeamLoadout`: compare version and every version-gated base/unknown/special/banner/product/extra field exactly.
- `ClubColors`: compare both flags and color bytes exactly.
- `Reservation`: compare system/ID branch, local ID, name encoding/length and unknown fields. Sensitive account/name text is compared only in memory; durable evidence stores hashes/length/encoding/match flags.
- `StatEvent` and `PlayerHistoryKey`: compare exact primitive fields.
- `DemolishFx` and `DemolishExtended`: compare actor flags/IDs and both vector structures/raw components/semantic components.
- `ExtendedExplosion`: compare actor/flag fields plus vector structure/raw/semantic values.
- `LoadoutsOnline`: compare nested group counts, each product object branch and numeric/text value. Sensitive title text is compared in memory and persisted only as hash/length/encoding/match flags.

## Floating-point comparison rule

Inspect the pinned Boxcars arithmetic before evaluating witnesses. If native and oracle use the same f32 operations in the same order, require exact f32 bit equality. If operation order differs materially while remaining mathematically equivalent, define and persist a deterministic comparison rule **before** evaluating the witness set. Never invent a tolerance after observing mismatches.

## Negative controls

Regenerate or synthesize bounded controls for at least:

```text
wrong major / minor / net_version
wrong RL223 tuple for a single-context group
unsupported non-K4 tag
invalid payload start
fixed and variable payload truncation
malformed signed text lengths including i32::MIN
unsupported Reservation system / unadmitted Reservation name-length combination
DemolishFx cross-product tuple absent from allowlist
DemolishExtended cross-product tuple absent from allowlist
LoadoutsOnline unknown product object / absent nested cross-product
unobserved TeamLoadout version/branch combination
trailing-bit non-consumption
atomic failure / no partial semantic value escape
```

Negative controls do not authorize new shapes.

## Required gates

```text
fresh production identity                         PASS
47/47 replay identity verification                PASS
pinned Boxcars oracle decode                       47/47
R3.17M group reconstruction                        161/161
real witness group coverage                        161/161 minimum
native decode success on admitted witnesses        100%
tag / semantic variant match                       100%
context match                                      100%
payload start / end / width match                  100%
exact structural shape match                       100%
semantic value match under predeclared rule        100%
negative controls                                  100%
bit monotonicity / packed-payload failures         0 / 0
privacy scan                                       PASS
production/Cargo/fixture/corpus/support mutation   0/0/0/0/0
normal CI on exact audit head                      PASS
```

## Outcome rules

- **Outcome A:** all 161 exact groups receive real witness coverage, every native/oracle comparison is exact under the predeclared numeric rule, negatives fail closed, privacy passes and mutations remain zero.
- **Outcome B:** reproducible evidence is insufficient to reconstruct one or more admitted groups; stop with targeted evidence work only. Do not widen or silently skip.
- **Outcome C:** any native/oracle mismatch, structural contradiction, source-identity contradiction or decoder defect. Stop and repair evidence/contract/implementation in a separately admitted pass.

## Hard stop

R3.17P must not modify production Rust, Cargo files, fixtures, replay corpus or support lane. It must not consume a second property or advance actor/frame/lifecycle state. Raw-state, events, replay slicing, skills, runtime and export work remain closed.

## After Outcome A

Re-read `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md` and select the first dependency-valid unfinished pass. R3.18 is not automatically admitted merely because K4 differential closure succeeded.
"""
    P_SPEC.write_text(normalize(text), encoding="utf-8", newline="\n")


def main() -> None:
    update_continue()
    update_graph()
    write_current()
    update_state()
    write_decision()
    write_p_spec()
    print("R3.17O continuity closure generated")
    print("next=R3.17P native K4 real-replay differential audit")


if __name__ == "__main__":
    main()
