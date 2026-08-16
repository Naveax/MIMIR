from __future__ import annotations

import json
from pathlib import Path

BASE_MAIN = "19e3f558bd343372c7fe863822ab961fb10976ad"
PROD = "492cc8218be7abc6db8f75acaea33d009ab2f175"
AUDIT_HEAD = "f2d87b732ad3103d50e2c047351f1017d4f3613f"
AUDIT_RUN = 31937527114
AUDIT_JOB = 95141677175
CI_RUN = 31937527123
CI_JOB = 95141677140
ARTIFACT = 9261118033
ARTIFACT_DIGEST = "sha256:bc366b75e003531ba17351e880f259457ceba7cda702d912580c686990ba1beb"


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one replacement, found {count}")
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# MIMIR_CONTINUE_HERE.md
# ---------------------------------------------------------------------------
main = read("MIMIR_CONTINUE_HERE.md")
main = once(
    main,
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.17L — native K3 differential audit / Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch",
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.17P — native K4 differential audit / Outcome A / 161 of 161 real-replay exact groups / 0 mismatch",
    "continue last audit",
)
main = once(
    main,
    "CURRENT_PASS:\n  R3.17P — native K4 real-replay differential audit\n\nCURRENT_PASS_TYPE:\n  read-only real-replay differential audit / exact 161-group certification",
    "CURRENT_PASS:\n  R3.18A — existing-actor single-property boundary evidence\n\nCURRENT_PASS_TYPE:\n  read-only real-replay evidence / one complete existing-actor property payload + exact end cursor",
    "continue current pass",
)
main = once(
    main,
    "  R3.17O production is implemented and published; R3.17P must certify it against regenerated real-replay witnesses before any later parser widening",
    "  R3.17P certified the published R3.17O K4 decoder on all 161 exact real-replay groups; R3.18A may now prove exactly one complete existing-actor property boundary without looping",
    "continue production hard stop",
)
old_boundary = """R3_17P_OPEN_BOUNDARY:
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
  only after Outcome A, re-read the execution roadmap and select the first dependency-valid unfinished pass; R3.18 is not pre-admitted
"""
new_boundary = f"""R3_17P_AUDIT_CLOSURE:
  Outcome A / read-only / production Rust unchanged at {PROD}
  authority head: {AUDIT_HEAD}
  authority run/job: {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
  exact-head normal CI: {CI_RUN} / {CI_JOB} SUCCESS
  artifact: {ARTIFACT}
  artifact digest: {ARTIFACT_DIGEST}
  47/47 replay identity + pinned Boxcars decode
  exact R3.17N group reconstruction + real witness coverage: 161/161
  native decode/tag/context/range/shape/semantic equality: 161/161 each
  mismatch count: 0; exhaustive K4 negative controls: PASS; privacy: PASS
  frozen numeric rule: exact f32 bit equality for CamSettings; exact vector wire fields + f32 bits; exact integer/boolean/object/count/version fields; tolerance 0
  LoadoutsOnline caller object table: same replay footer materialization, not inferred
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_18A_OPEN_BOUNDARY:
  read-only existing-actor single-property boundary evidence; production mutation forbidden
  select a deterministic real existing-actor update with property_present=true from the supported replay lane
  prove the already-resolved stream/property/tag context at the exact payload start
  decode exactly one already-admitted K1/K2/K3/K4 payload and require native payload_end_bit == pinned Boxcars oracle end bit
  stop before consuming the next property_present bit; this pass does not admit a property loop

R3_18A_HARD_STOP:
  no production Rust, Cargo, fixture, corpus or support-lane mutation
  no second property and no consumption of the next property_present bit
  no next actor / next frame / actor-table lifecycle mutation
  no new attribute family/shape/context admission
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.18A:
  only after Outcome A, admit the minimal production one-property composition needed by roadmap R3.18; property-loop continuation remains a later separately evidenced step
"""
main = once(main, old_boundary, new_boundary, "continue P->18A boundary")
write("MIMIR_CONTINUE_HERE.md", main)


# ---------------------------------------------------------------------------
# MIMIR_KNOWLEDGE_GRAPH.md
# ---------------------------------------------------------------------------
graph = read("MIMIR_KNOWLEDGE_GRAPH.md")
graph = once(
    graph,
    "R3.17P active K4 differential spec                |",
    "R3.17P K4 differential decision                     |\nR3.18A active single-property evidence spec               |",
    "graph canonical node",
)
old_order = """32. `docs/continuity/MIMIR_R3_17P_EXECUTION_SPEC.md`
33. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
34. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
35. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
36. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
37. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
38. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
39. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`
"""
new_order = """32. `docs/continuity/MIMIR_R3_17P_EXECUTION_SPEC.md`
33. `docs/continuity/MIMIR_R3_17P_DECISION.md`
34. `docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md`
35. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
36. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
37. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
38. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
39. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
40. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
41. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`
"""
graph = once(graph, old_order, new_order, "graph mandatory order")
graph = once(
    graph,
    " -> R3.17P native K4 real-replay differential audit: ACTIVE / READ-ONLY\n",
    f""" -> R3.17P native K4 real-replay differential audit: OUTCOME A / CLOSED
      authority {AUDIT_HEAD} / {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
      exact-head CI {CI_RUN} / {CI_JOB} SUCCESS
      artifact {ARTIFACT} / {ARTIFACT_DIGEST}
      47/47 oracle + 161/161 real-group native decode/tag/context/range/shape/semantic exact / 0 mismatch
      negative controls + privacy PASS / production-Cargo-fixture-corpus-support mutation 0/0/0/0/0
 -> R3.18A existing-actor single-property boundary evidence: ACTIVE / READ-ONLY
      prove exactly one complete real property payload and exact end cursor; stop before next property_present bit
""",
    "graph replay chain",
)
graph = once(
    graph,
    "Production at `492cc8218be7abc6db8f75acaea33d009ab2f175` can natively decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload. Every success stops exactly at its one-value end bit and does not authorize another property, actor, frame or lifecycle mutation. R3.17P is the separate real-replay certification pass for the K4 implementation.",
    "Production at `492cc8218be7abc6db8f75acaea33d009ab2f175` can natively decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload. Every success stops exactly at its one-value end bit and does not authorize another property, actor, frame or lifecycle mutation. R3.17P has now certified all 161 exact K4 groups against regenerated real-replay witnesses with zero mismatch; R3.18A is evidence-only and does not widen production.",
    "graph capability intro",
)
graph = once(
    graph,
    "R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups; R3.17K implemented them; R3.17L matched all 1,950 against real replay witnesses. R3.17M then observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups; R3.17N admitted those 161 groups byte-for-byte; R3.17O implemented exactly that contract with zero cross-product widening. R3.17P is now the separate native K4 real-replay differential audit. Property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed.",
    "R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups; R3.17K implemented them; R3.17L matched all 1,950 against real replay witnesses. R3.17M then observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups; R3.17N admitted those 161 groups byte-for-byte; R3.17O implemented exactly that contract with zero cross-product widening; R3.17P then matched all 161 exact K4 groups against real replay witnesses with zero mismatch. R3.18A now proves one complete existing-actor property boundary only. Property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed.",
    "graph capability history",
)
graph = once(
    graph,
    "R3.17P must certify all 161 exact groups against regenerated real-replay witnesses before later parser widening is considered.",
    f"""## R3.17P K4 differential closure

```text
authority head              {AUDIT_HEAD}
authority run/job           {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
exact-head normal CI        {CI_RUN} / {CI_JOB} SUCCESS
artifact                    {ARTIFACT}
artifact digest             {ARTIFACT_DIGEST}
replay identity/oracle      47/47
real group coverage         161/161
native decode               161/161
variant/context/range       161/161 exact
shape/semantic              161/161 exact
mismatch count              0
negative controls           PASS
privacy                     PASS
prod/Cargo/fixture/corpus/
support mutations           0/0/0/0/0
outcome                     A
```

R3.18A is now the first dependency-valid unfinished roadmap step: read-only evidence for exactly one complete existing-actor property payload and exact end cursor. It must stop before the next `property_present` bit; the property loop is not admitted by this transition.""",
    "graph P closure section",
)
write("MIMIR_KNOWLEDGE_GRAPH.md", graph)


# ---------------------------------------------------------------------------
# Machine-readable continuity state
# ---------------------------------------------------------------------------
state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-16"
state["last_completed_read_only_audit"] = "R3.17P"
state["last_completed_native_differential_audit"] = "R3.17P"
state["current_pass"] = "R3.18A"
state["current_pass_kind"] = "read-only existing-actor single-property boundary evidence"
state["current_pass_goal"] = "Select one deterministic real existing-actor property update, preserve the already-resolved stream/property/tag context, decode exactly one already-admitted K1/K2/K3/K4 payload, and prove the native payload end bit equals the pinned Boxcars oracle end bit."
state["current_pass_stop_boundary"] = "Read-only evidence; stop before consuming the next property_present bit. No second property, property loop, next actor/frame, lifecycle mutation, new attribute admission, raw-state/event/skill/runtime/export widening, or production/Cargo/fixture/corpus/support mutation."
state["closed_now"] = [
    "native property loop iteration beyond one complete property boundary",
    "second property consumption or next property_present bit consumption in R3.18A",
    "full actor envelope iteration",
    "full frame iteration",
    "actor state table mutation",
    "raw-state extraction",
    "event extraction",
    "replay slicing",
    "skill mining",
    "counterfactual rollout execution from native replay state",
]
order = state["next_files_to_read"]
anchor = "docs/continuity/MIMIR_R3_17P_EXECUTION_SPEC.md"
pos = order.index(anchor) + 1
for item in ["docs/continuity/MIMIR_R3_17P_DECISION.md", "docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md"]:
    if item in order:
        order.remove(item)
order[pos:pos] = ["docs/continuity/MIMIR_R3_17P_DECISION.md", "docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md"]
state["r3_17p"] = {
    "outcome": "A — admitted / complete",
    "pass_type": "read-only native K4 real-replay differential audit",
    "production_source_changed": False,
    "continuity_base_sha": BASE_MAIN,
    "production_sha": PROD,
    "production_tree": "a66c47d7fb58da508188e64d42141987a0021a07",
    "authority_head": AUDIT_HEAD,
    "workflow_run": AUDIT_RUN,
    "workflow_job": AUDIT_JOB,
    "exact_head_ci_run": CI_RUN,
    "exact_head_ci_job": CI_JOB,
    "artifact_id": ARTIFACT,
    "artifact_digest": ARTIFACT_DIGEST,
    "supported_replays": 47,
    "replay_identity_success": "47/47",
    "boxcars_oracle_decode": "47/47",
    "admitted_groups": 161,
    "group_reconstruction": "161/161",
    "real_witness_group_coverage": "161/161",
    "native_decode_success": "161/161",
    "tag_variant_match": "161/161",
    "context_match": "161/161",
    "payload_range_match": "161/161",
    "structural_shape_match": "161/161",
    "semantic_value_match": "161/161",
    "mismatch_count": 0,
    "numeric_rule": "exact f32 bits for CamSettings; exact vector size/component-width/raw components and exact f32 bits for vector families; exact integer/boolean/object/count/version fields; tolerance 0",
    "loadouts_online_object_table": "same-replay caller-resolved footer object materialization",
    "negative_controls": "PASS",
    "bit_monotonicity_failures": 0,
    "packed_payload_failures": 0,
    "privacy": "PASS",
    "production_cargo_fixture_corpus_support_mutation": "0/0/0/0/0",
    "witness_manifest_sha256": "82e86cbbf03092f96484199d950587f52b061a2414eb9bc7cdf54abab57b083a",
    "match_rows_sha256": "b87bf50cf3db618bda35fb90bd26230cfcfa77803812c81701b925a1af1d8201",
    "summary_sha256": "45fbe1de3b8b2b4c317ccbd15260d03ea1ddfb37fe07e25c0d11627741b66251",
    "negative_controls_sha256": "b591f70c39092d179edcf60354c42b1808f0f4f8ac0e1ff8fb54ee84533f90d7",
    "next_pass": "R3.18A",
}
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# Human-readable current state
# ---------------------------------------------------------------------------
current = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.17O — direct native exact-contract K4 decoder implementation`
**Completed K3 differential:** `R3.17L — Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch`
**Completed K4 evidence:** `R3.17M — Outcome A / 39463 occurrences / 161 exact structural-context groups / all 11 tags observed`
**Completed K4 contract:** `R3.17N — Outcome A / 161/161 byte-identical groups / zero cross-product widening`
**Completed K4 production:** `R3.17O — Outcome A / 161/161 exact contract implementation / zero widening`
**Completed K4 differential:** `R3.17P — Outcome A / 161/161 real-replay exact groups / 0 mismatch`
**Current exact pass:** `R3.18A — existing-actor single-property boundary evidence`

## 1. Truthful production boundary

Production remains R3.17O. MIMIR may decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload and stop at the exact one-value end bit. R3.17P certified that K4 boundary against real replay witnesses but did not widen production into a property loop.

```text
production SHA               {PROD}
production tree              a66c47d7fb58da508188e64d42141987a0021a07
lib.rs blob                  0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8
k4 groups blob               103503e25bc5af48381df021ab58133694fcece6
k4 native blob               a9c41f3bb11343165183ac9c815ab8fdf085936c
focused K4 test blob         70437244bb49224281ee3a2e745e7b8a4b7a093a
R3.17N allowlist SHA256      80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
```

## 2. R3.17P real-replay differential closure

```text
authority head               {AUDIT_HEAD}
authority run/job            {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
exact-head normal CI         {CI_RUN} / {CI_JOB} SUCCESS
artifact                     {ARTIFACT}
artifact digest              {ARTIFACT_DIGEST}
replay identity              47/47
Boxcars oracle decode        47/47
exact group reconstruction   161/161
real witness group coverage  161/161
native decode                161/161
variant/context/range        161/161 exact
shape/semantic               161/161 exact
mismatch count               0
negative controls            PASS
privacy                      PASS
production/Cargo/fixture/
corpus/support mutation      0/0/0/0/0
```

The numeric rule was frozen before evaluation: CamSettings requires exact f32 bit identity; vector families require exact selected size, component width, raw components and f32 bits; integer/boolean/object/count/version fields require exact equality. Tolerance is zero. `LoadoutsOnline` used the exact caller-resolved object table materialized from the same witness replay.

## 3. Evidence and contract authority

R3.17M remains the K4 wire-format evidence authority, R3.17N remains the exact 161-group contract authority, R3.17O remains production, and R3.17P is the real-replay certification authority. The four layers are intentionally separate.

```text
R3.17M authority             a50f09857f36ac52cec30b4bf3efbde9e15bb564 / 31881779861
R3.17N group SHA256          80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
R3.17O production            {PROD}
R3.17P authority             {AUDIT_HEAD} / {AUDIT_RUN}
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
```

## 4. R3.18A exact next pass

Roadmap R3.18 first requires one complete existing-actor property update before a property loop. R3.18A is the read-only evidence decomposition of that first boundary: choose a deterministic real update with `new == false` and `property_present == true`, preserve the already-resolved stream/property/tag context, decode exactly one already-admitted K1/K2/K3/K4 payload, and prove the native `payload_end_bit` equals the pinned Boxcars oracle end bit.

The hard stop is before consuming the next `property_present` bit. R3.18A does not admit a second property, loop continuation, next actor/frame, actor-table mutation, new attribute family, or production code.

## 5. Still closed

```text
second property / next property_present-bit consumption
property_present loop for one actor update
next actor / next frame iteration
actor lifecycle mutation
new attribute family/shape/context admission
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
"""
write("docs/continuity/MIMIR_CURRENT_STATE.md", current)


# ---------------------------------------------------------------------------
# R3.17P decision
# ---------------------------------------------------------------------------
decision = f"""# MIMIR R3.17P — Native K4 Real-Replay Differential Audit Decision

**Date:** 2026-08-16  
**Pass:** R3.17P  
**Outcome:** **A — ADMITTED / COMPLETE**  
**Pass type:** read-only real-replay differential audit  
**Production mutation:** none

## Frozen authority

```text
pre-audit canonical main     {BASE_MAIN}
production SHA               {PROD}
production tree              a66c47d7fb58da508188e64d42141987a0021a07
authority audit head         {AUDIT_HEAD}
authority run/job            {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
exact-head normal CI         {CI_RUN} / {CI_JOB} SUCCESS
artifact                     {ARTIFACT}
artifact digest              {ARTIFACT_DIGEST}
pinned Boxcars               c70e77df7af81b436cb545d070bb90c82f562d0b
R3.17N group SHA256          80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
```

The fresh-main audit before execution proved that `{BASE_MAIN}` differed from production only by the R3.17O continuity publication. The production Rust blobs remained exactly frozen.

## Admitted result

```text
replay identity              47/47
Boxcars oracle decode        47/47
exact group reconstruction   161/161
real witness group coverage  161/161
native decode success        161/161
tag variant match            161/161
context match                161/161
payload range match          161/161
structural shape match       161/161
semantic value match         161/161
mismatch count               0
bit monotonicity failures    0
packed payload failures      0
negative controls            PASS
privacy                      PASS
production mutation          0
Cargo mutation               0
fixture mutation             0
corpus mutation              0
support-lane mutation        0
```

The durable witness manifest, match rows and summary are privacy-safe. Account/player/title clear text was permitted only ephemerally inside the runner for semantic comparison.

## Numeric equality rule

The comparison rule was frozen before witness evaluation:

- `CamSettings`: exact raw IEEE-754 f32 bit identity for all compared fields;
- `DemolishFx`, `DemolishExtended`, `ExtendedExplosion` vectors: exact selected vector size, component width, raw X/Y/Z values and reconstructed f32 bit identity;
- integers, booleans, actor/object IDs, counts and version gates: exact equality;
- tolerance: **0**.

`LoadoutsOnline` used the exact caller-resolved object table materialized from the same replay as each witness. Product meaning was not inferred from the production branch being tested.

## Durable receipt hashes

```text
witness manifest SHA256      82e86cbbf03092f96484199d950587f52b061a2414eb9bc7cdf54abab57b083a
match rows SHA256            b87bf50cf3db618bda35fb90bd26230cfcfa77803812c81701b925a1af1d8201
summary SHA256               45fbe1de3b8b2b4c317ccbd15260d03ea1ddfb37fe07e25c0d11627741b66251
negative controls SHA256     b591f70c39092d179edcf60354c42b1808f0f4f8ac0e1ff8fb54ee84533f90d7
```

## Non-authority harness incident

The first disposable run `31937199601 / 95140880625` reached authority freeze, exact group reconstruction, semantic oracle rescan and 161/161 witness selection, then failed while compiling the external comparison harness because of a `serde_json::json!` expression syntax error. No production mismatch was observed. The corrected exact-head authority run `{AUDIT_RUN}` repeated the substantive gates and is the only R3.17P authority.

## Boundary consequence

R3.17P certifies R3.17O's exact K4 one-value decoder against real replay evidence. It does **not** admit a second property or property loop.

The execution roadmap was re-read after Outcome A. The first dependency-valid unfinished step is R3.18: one complete existing-actor property update and exact end cursor before loop continuation. MIMIR therefore opens **R3.18A**, a read-only evidence pass for exactly one complete existing-actor single-property boundary.
"""
write("docs/continuity/MIMIR_R3_17P_DECISION.md", decision)


# ---------------------------------------------------------------------------
# R3.18A execution spec
# ---------------------------------------------------------------------------
spec = f"""# MIMIR R3.18A — Existing-Actor Single-Property Boundary Evidence

**Status:** ACTIVE  
**Pass type:** read-only real-replay evidence  
**Production mutation:** forbidden  
**Roadmap parent:** R3.18 — one complete existing-actor property update

## 1. Goal

Prove one complete real existing-actor property update boundary end-to-end before any property-loop implementation is attempted.

The selected witness must have:

```text
new == false
property_present == true
already-resolved actor/class/cache context
bounded stream_id
resolved property object ID + admitted tag
payload_start_bit
exactly one already-admitted K1/K2/K3/K4 payload
payload_end_bit
```

Native and pinned Boxcars must agree on the resolved property identity/tag, payload start, semantic value under the already-admitted decoder contract, and exact payload end cursor.

## 2. Frozen authority

```text
continuity base main         {BASE_MAIN}
production SHA               {PROD}
production tree              a66c47d7fb58da508188e64d42141987a0021a07
R3.17P authority head        {AUDIT_HEAD}
R3.17P run/job               {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
R3.17P artifact              {ARTIFACT}
R3.17P artifact digest       {ARTIFACT_DIGEST}
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47 exact replays
```

Before execution, fresh `main` must be re-read and the production source/test blobs must still match R3.17O. Any production drift requires re-audit before this spec may be executed.

## 3. Witness selection

Use the exact frozen supported replay lane and pinned Boxcars oracle. Scan read-only and deterministically choose a real existing-actor update whose first property tag is already admitted by current production.

Selection must be reproducible from privacy-safe coordinates such as replay identity hash/path, frame index, actor ordinal/ID, property ordinal, stream ID, resolved property object ID/tag and exact bit offsets. Do not persist sensitive account/player/title clear text.

One canonical witness is sufficient for R3.18A because this pass proves the **single-property composition boundary**, not property-loop corpus coverage. Broader encountered-tag/loop requirements remain for the later R3.18 loop step.

## 4. Exact comparison contract

For the selected witness require:

```text
existing-actor branch             exact
property_present                  true / exact
bounded stream_id                 exact
resolved property object ID       exact
resolved attribute tag            exact
payload_start_bit                 exact
native one-value decode success   true
semantic value                    exact under its already-admitted family rule
payload_end_bit                   exact
cursor monotonicity               PASS
```

If the selected payload is a floating/vector family, reuse the already-frozen equality rule of the family that admitted it; do not invent a looser tolerance in R3.18A.

## 5. Atomicity and hard stop

The R3.18A probe must stop at `payload_end_bit` **before reading the next `property_present` bit**.

Forbidden in this pass:

- second property consumption;
- `property_present` loop continuation;
- next actor or next frame;
- actor-table/lifecycle mutation;
- new attribute family/shape/context admission;
- production Rust changes;
- Cargo, fixture, corpus or support-lane changes;
- raw-state, event, replay-slice, skill, runtime or export widening.

Malformed/truncated selected-property probes must fail atomically without reporting a successful end cursor.

## 6. Durable evidence

Persist only privacy-safe evidence:

```text
frozen source/oracle identities
selected replay identity hash/path from the frozen lane
frame + actor/property coordinates
stream/property/tag identity
payload start/end/width
payload hash, not private clear text
native/oracle equality booleans
negative-control result
mutation counters
artifact digest / receipt hashes
```

## 7. Outcome gate

### Outcome A

All of the following are required:

```text
fresh production identity                 PASS
selected real existing-actor witness      reproducible
property header identity                  exact
payload start                             exact
native one-value decode                   PASS
semantic comparison                       exact
payload end cursor                        exact
next property_present consumed            0 bits
malformed/truncated atomic negative        PASS
privacy                                   PASS
production/Cargo/fixture/corpus/support   0/0/0/0/0 mutations
normal CI on exact evidence head          SUCCESS
```

Only Outcome A may close R3.18A. The next pass may then admit the minimal production composition for one property update. **Property-loop continuation remains separately gated.**

### Outcome B

Evidence is valid but the selected boundary exposes an unresolved contract detail. Record it and keep production closed.

### Outcome C

Native/oracle disagreement, non-reproducible evidence, privacy failure, mutation, or invalid source identity. Stop and do not widen.
"""
write("docs/continuity/MIMIR_R3_18A_EXECUTION_SPEC.md", spec)

print("R3_17P_CONTINUITY_GENERATION=PASS")
