from __future__ import annotations

import json
from pathlib import Path

BASE_MAIN = "b1a4ad1a04623e3c8b002a7ea60817120b5fb551"
PROD_SHA = "7390e3b145372252caaa8fa1fe3e0cd13b83336c"
M_HEAD = "a50f09857f36ac52cec30b4bf3efbde9e15bb564"
M_RUN = 31881779861
M_JOB = 95005282281
M_CI_RUN = 31881779862
M_CI_JOB = 95005282149
M_ARTIFACT = 9246249473
M_DIGEST = "sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987"
GROUP_SHA = "80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b"
WITNESS_SHA = "acd66e4b1fc6f8c13228c7c67c24855760d55569957177915521d685949f80c3"
SUMMARY_SHA = "0ae05ee497f27bf159ba3ca8b4d1ec59a8b3a131713883e72592024bf2ca59f8"
AGG_SHA = "f6ff0d70d81afbd1db4f84cb3eaf47c8a6325aeca5bb0294071b678da352f82a"
RECEIPT_SHA = "98bb8b03ad58c798dad16f41bf8ae90ad2823f3756790508dc47c2a6eeae65b8"
ORACLE_LOG_SHA = "ace53c1413c39da7afefa6ab73324e129bc8c1e660ceea2273e283ade0c73cb4"

TAG_COUNTS = {
    "CamSettings": (6314, 47, 1),
    "TeamPaint": (6498, 47, 1),
    "TeamLoadout": (6443, 47, 1),
    "ClubColors": (208, 1, 1),
    "Reservation": (6392, 47, 35),
    "StatEvent": (2279, 47, 1),
    "PlayerHistoryKey": (3840, 1, 1),
    "DemolishFx": (131, 36, 12),
    "DemolishExtended": (16, 2, 5),
    "ExtendedExplosion": (701, 47, 1),
    "LoadoutsOnline": (6641, 47, 73),
}


def exact_replace(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, got {count}")
    return text.replace(old, new, 1)


def write(path: str, text: str) -> None:
    Path(path).write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def decision_text() -> str:
    tag_lines = "\n".join(
        f"- `{tag}`: {occ} occurrences / {replays} replay(s) / {shapes} observed shape(s)"
        for tag, (occ, replays, shapes) in TAG_COUNTS.items()
    )
    return f"""# MIMIR R3.17M Decision — K4 Gameplay Structured Wire-Format Evidence

**Outcome:** A — ADMITTED / COMPLETE  
**Pass type:** read-only evidence  
**Production implementation:** unchanged / forbidden in this pass

## Frozen authority

```text
continuity base              {BASE_MAIN}
production SHA               {PROD_SHA}
evidence authority head      {M_HEAD}
authority run/job            {M_RUN} / {M_JOB} SUCCESS
exact-head normal CI         {M_CI_RUN} / {M_CI_JOB} SUCCESS
artifact                     {M_ARTIFACT}
artifact digest              {M_DIGEST}
pinned Boxcars               c70e77df7af81b436cb545d070bb90c82f562d0b
replay identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
```

## Result

The frozen 47-replay lane was scanned twice with the same pinned Boxcars instrumentation. Both raw oracle logs were byte-identical and every durable analysis output was hash-identical.

```text
replay identity                         47/47 PASS
Boxcars oracle decode                   47/47 PASS
K4 occurrences                          39463
exact structural/context groups         161
privacy-safe witness rows               617
zero-occurrence target tags             0
unclassified occurrences                0
bit monotonicity failures               0
raw packed-payload shape failures       0
privacy                                 PASS
production/Cargo/fixture/corpus/support 0/0/0/0/0
outcome                                 A
```

## Target-tag coverage

{tag_lines}

The sparse tags are still real supported-lane evidence: `ClubColors` and `PlayerHistoryKey` occur in one replay each, and `DemolishExtended` occurs in two. Their admission may therefore cover only the exact observed structural/context groups, never inferred neighboring branches.

## Determinism and durable receipt

```text
first raw oracle log SHA256     {ORACLE_LOG_SHA}
rerun raw oracle log SHA256     {ORACLE_LOG_SHA}
raw oracle logs identical       true
analysis outputs identical      true
K4 groups JSONL SHA256          {GROUP_SHA}
K4 witnesses JSONL SHA256       {WITNESS_SHA}
summary SHA256                  {SUMMARY_SHA}
aggregate SHA256                {AGG_SHA}
artifact ZIP SHA256             50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
```

The downloaded artifact ZIP was independently re-hashed against GitHub's digest and all 12 receipt-listed durable files matched their recorded SHA-256 values. The durable witness surface contains structural replay/property identities, exact bit ranges, context, shape and structural witness hashes; it contains no raw payload field and no player/account identifier field.

## Admission boundary

R3.17M proves only the 161 exact observed structural/context groups represented by `r3_17m_k4_groups.jsonl`. It does **not** admit:

- Cartesian products assembled from independently observed subfields,
- zero-occurrence branches or version contexts,
- source-code-only Boxcars branches,
- a native K4 decoder,
- a second property, actor, frame or lifecycle transition.

`Reservation` contributes 35 observed shapes and `LoadoutsOnline` 73; those families especially require exact tuple/group membership rather than convenient field-union widening.

## Next pass

Open `R3.17N — K4 Evidence-Supported Contract Admission`. R3.17N is contract-only. Production Rust remains frozen at `{PROD_SHA}` until a later implementation pass is separately admitted.
"""


def next_spec_text() -> str:
    return f"""# MIMIR R3.17N — K4 Evidence-Supported Contract Admission Execution Spec

**Pass type:** contract-only  
**Production implementation:** forbidden  
**Evidence authority:** R3.17M Outcome A  
**Production authority:** R3.17K, unchanged

## Goal

Convert the exact R3.17M observations for the 11 K4 gameplay-structured tags into a minimal fail-closed one-value decoder contract. Do not write production K4 decoding code in this pass.

## Frozen identities

```text
continuity base              {BASE_MAIN}
production SHA               {PROD_SHA}
R3.17M evidence head         {M_HEAD}
R3.17M authority run/job     {M_RUN} / {M_JOB} SUCCESS
R3.17M exact-head CI         {M_CI_RUN} / {M_CI_JOB} SUCCESS
R3.17M artifact              {M_ARTIFACT}
R3.17M artifact digest       {M_DIGEST}
R3.17M groups SHA256         {GROUP_SHA}
R3.17M witnesses SHA256      {WITNESS_SHA}
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
observed K4 groups           161
```

## Contract surface to freeze

The candidate K4 surface is exactly the 161 structural/context groups in the R3.17M groups JSONL:

```text
CamSettings        6314 occurrences / 1 shape
TeamPaint          6498 / 1
TeamLoadout        6443 / 1
ClubColors          208 / 1
Reservation        6392 / 35
StatEvent          2279 / 1
PlayerHistoryKey   3840 / 1
DemolishFx          131 / 12
DemolishExtended     16 / 5
ExtendedExplosion   701 / 1
LoadoutsOnline     6641 / 73
```

The contract must materialize a canonical, deterministic admitted-group artifact derived from the evidence artifact and prove byte-for-byte/equivalent tuple equality with the evidence groups. No group may be invented from prose or Boxcars source.

## Common contract rules

1. Input is one already-resolved attribute payload at an arbitrary unaligned bit start, LSB-first.
2. Success consumes exactly one contract-admitted K4 value and returns its exact end bit.
3. Wrong version/context, unsupported structural branch, malformed length/count, overflow or truncation fails atomically; no successful partial value escapes.
4. Exact replay version/net-version/RL223 context is part of admission where present in the evidence tuple.
5. Exact structural group membership outranks per-field union membership.
6. A branch seen only in one or two replays remains admissible only for its exact observed groups; rarity is not permission to generalize.
7. Boxcars source may explain a field ordering but may not admit an unobserved branch.
8. Extra trailing bits are not consumed as a second property.

## Family-specific minimums

### Fixed-shape families

Freeze exact observed field order/width for:

- `CamSettings`: observed `f32x7`, width 224.
- `TeamPaint`: `u8x3 + u32x2`, width 88.
- `TeamLoadout`: observed blue/orange `v28` loadout branch only, width 1040.
- `ClubColors`: `bit + u8 + bit + u8`, width 18.
- `StatEvent`: `bit + i32`, width 33.
- `PlayerHistoryKey`: exact u14, width 14.
- `ExtendedExplosion`: observed exact location-vector structural group plus actor/reference fields, width 112.

No earlier/later version branch is admitted merely because the oracle has code for it.

### Reservation

Freeze only the exact 35 observed structural/context groups. Identifier system, split-screen branch, Epic text-length shape, optional reservation-name text shape, six-bit version-gated tail and exact total width must remain group-coupled. Do not admit arbitrary identifier/name-length combinations.

### DemolishFx / DemolishExtended

Freeze exact actor/reference field order plus the exact observed vector-shape pairs. Do not admit the Cartesian product of independently observed attacker/victim vector shapes. `DemolishFx` has 12 observed shapes; `DemolishExtended` has 5.

### LoadoutsOnline

Freeze exactly the 73 observed nested shapes. Outer side counts, per-group product counts, product-attribute object branch, title-text lengths and product value branches remain coupled exactly as evidenced. Do not synthesize new online-loadout combinations from individually observed product branches.

## Required negative/malformed contract cases

At minimum define fail-closed tests for:

```text
wrong replay major/minor/net_version/RL223 context
unknown K4 tag
invalid start bit
truncation at every fixed primitive boundary
Reservation unobserved identifier/name/text-length combination
Reservation malformed signed text length / overflow
DemolishFx unobserved vector-pair combination
DemolishExtended unobserved vector-pair combination
LoadoutsOnline unobserved outer/group/product combination
LoadoutsOnline malformed count/length and unknown product object branch
unobserved TeamLoadout version branch
extra trailing bits not consumed as another property
```

## Required contract artifacts and gates

```text
R3.17M authority identities frozen            PASS
canonical admitted-group artifact             161 exact groups
admitted-group evidence equality              161/161
cross-product widening                        0
unobserved branches explicit rejects          PASS
atomic failure semantics                      PASS
exact one-value end semantics                 PASS
privacy-safe positive vector plan             PASS
synthetic negative vector plan                PASS
production Rust mutation                      0
Cargo / fixture / corpus / support mutation   0/0/0/0
```

The canonical admitted-group artifact should be checked in under `docs/continuity/` during R3.17N if Outcome A is selected, analogous to the R3.17J K3 group artifact. It is contract evidence, not production implementation.

## Outcome rules

- **Outcome A:** freeze exactly the evidence-supported K4 contract with 161/161 group equality and zero widening; only then open a separate native K4 implementation pass.
- **Outcome B:** a required contract distinction cannot be represented without ambiguity; return to targeted evidence.
- **Outcome C:** contract modeling contradicts R3.17M evidence or existing bit primitives; stop before implementation.

## Hard stop

Do not implement native K4 decoding in R3.17N. Do not consume a second property, actor or frame, mutate lifecycle state, extract raw state/events, slice replays, mine skills, or widen runtime/export.

## Next pass

Only on R3.17N Outcome A may a separate direct native K4 decoder implementation pass be opened. R3.18 remains closed until that implementation and its differential audit are separately completed or the roadmap is explicitly revised by evidence.
"""


def update_continue() -> None:
    p = Path("MIMIR_CONTINUE_HERE.md")
    s = p.read_text(encoding="utf-8")
    s = exact_replace(
        s,
        "LAST_COMPLETED_CONTRACT_PASS:\n  R3.17J — evidence-supported K3 spatial/physics contract / Outcome A / 1950 exact groups\n\nCURRENT_PASS:\n  R3.17M — K4 gameplay-structured wire-format evidence\n\nCURRENT_PASS_TYPE:\n  read-only evidence / pinned-oracle wire-shape characterization; production Rust forbidden",
        "LAST_COMPLETED_CONTRACT_PASS:\n  R3.17J — evidence-supported K3 spatial/physics contract / Outcome A / 1950 exact groups\n\nLAST_COMPLETED_EVIDENCE_PASS:\n  R3.17M — K4 gameplay-structured wire-format evidence / Outcome A / 39463 occurrences / 161 exact groups\n\nCURRENT_PASS:\n  R3.17N — K4 evidence-supported contract admission\n\nCURRENT_PASS_TYPE:\n  contract-only / exact evidence-group admission; production Rust forbidden",
        "continue current pass block",
    )
    old = """R3_17M_OPEN_BOUNDARY:
  read-only K4 gameplay-structured evidence; production Rust changes are forbidden
  same frozen 47-replay lane and pinned Boxcars SHA only
  target tags: CamSettings / TeamPaint / TeamLoadout / ClubColors / Reservation / StatEvent / PlayerHistoryKey / DemolishFx / DemolishExtended / ExtendedExplosion / LoadoutsOnline
  characterize exact field order, optional/version branches, subfield bit boundaries, payload widths and context families
  deterministic shape IDs and privacy-safe witnesses for every observed shape/context family
  zero-occurrence tags/branches remain unadmitted; Boxcars source alone is not contract evidence

R3_17M_HARD_STOP:
  no production Rust, Cargo, fixture, corpus or support-lane mutation
  no K4 contract or implementation
  no second property / property-loop continuation
  no next actor / next frame / lifecycle mutation
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.17M:
  only if Outcome A, open a separate evidence-supported K4 contract admission pass; R3.18 remains closed"""
    new = f"""R3_17M_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at {PROD_SHA}
  authority head: {M_HEAD}
  authority run/job: {M_RUN} / {M_JOB} SUCCESS
  exact-head normal CI: {M_CI_RUN} / {M_CI_JOB} SUCCESS
  artifact: {M_ARTIFACT}
  artifact digest: {M_DIGEST}
  47/47 replay identity + Boxcars oracle decode; deterministic double scan exact
  K4 occurrences: 39463; exact structural/context groups: 161; witnesses: 617
  all 11 target tags observed; zero/unclassified/bit/raw failures: 0/0/0/0
  groups SHA256: {GROUP_SHA}
  privacy: PASS; production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_17N_OPEN_BOUNDARY:
  contract-only; production Rust changes are forbidden
  freeze exactly the 161 R3.17M structural/context groups into a canonical admitted-group artifact
  prove 161/161 evidence equality and zero cross-product widening
  Reservation 35 shapes, DemolishFx 12, DemolishExtended 5 and LoadoutsOnline 73 remain exact-group coupled
  source-only or zero-occurrence branches remain rejected

R3_17N_HARD_STOP:
  no production Rust, Cargo, fixture, corpus or support-lane mutation
  no native K4 implementation
  no second property / property-loop continuation
  no next actor / next frame / lifecycle mutation
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.17N:
  only if Outcome A, open a separate direct native K4 decoder implementation pass; R3.18 remains closed"""
    s = exact_replace(s, old, new, "continue M boundary")
    write(str(p), s)


def update_graph() -> None:
    p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
    s = p.read_text(encoding="utf-8")
    s = exact_replace(
        s,
        "R3.17L K3 differential decision             |\nR3.17M active K4 evidence spec               |",
        "R3.17L K3 differential decision             |\nR3.17M K4 evidence decision                  |\nR3.17N active K4 contract spec                |",
        "graph nodes",
    )
    s = exact_replace(
        s,
        "23. `docs/continuity/MIMIR_R3_17L_DECISION.md`\n24. `docs/continuity/MIMIR_R3_17M_EXECUTION_SPEC.md`\n25. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n26. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n27. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n28. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n29. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n30. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n31. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
        "23. `docs/continuity/MIMIR_R3_17L_DECISION.md`\n24. `docs/continuity/MIMIR_R3_17M_EXECUTION_SPEC.md`\n25. `docs/continuity/MIMIR_R3_17M_DECISION.md`\n26. `docs/continuity/MIMIR_R3_17N_EXECUTION_SPEC.md`\n27. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n28. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n29. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n30. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n31. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n32. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n33. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
        "graph reading order",
    )
    s = exact_replace(
        s,
        " -> R3.17M K4 gameplay-structured wire-format evidence: ACTIVE / READ-ONLY",
        f" -> R3.17M K4 gameplay-structured wire-format evidence: OUTCOME A / CLOSED\n      authority {M_HEAD}\n      run/job {M_RUN} / {M_JOB} SUCCESS\n      exact-head CI {M_CI_RUN} / {M_CI_JOB} SUCCESS\n      artifact {M_ARTIFACT} / {M_DIGEST}\n      47/47 oracle / 39463 occurrences / 161 exact groups / 617 witnesses / 0 structural failures\n -> R3.17N K4 evidence-supported contract admission: ACTIVE / CONTRACT-ONLY",
        "graph decoder chain",
    )
    s = exact_replace(
        s,
        "R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups with zero cross-product widening; R3.17K implemented exactly that contract; R3.17L then matched all 1,950 exact groups against regenerated real-replay witnesses with zero mismatch. R3.17M is now the read-only K4 gameplay-structured wire-format evidence pass. K4 contract/implementation, property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed.",
        "R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups with zero cross-product widening; R3.17K implemented exactly that contract; R3.17L then matched all 1,950 exact groups against regenerated real-replay witnesses with zero mismatch. R3.17M subsequently observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups with zero structural failures. R3.17N is now contract-only and may admit only those exact groups; native K4 implementation, property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed.",
        "graph capability paragraph",
    )
    s += f"""

## R3.17M K4 evidence closure

```text
authority head              {M_HEAD}
authority run/job           {M_RUN} / {M_JOB} SUCCESS
exact-head normal CI        {M_CI_RUN} / {M_CI_JOB} SUCCESS
artifact                    {M_ARTIFACT}
artifact digest             {M_DIGEST}
replays / oracle            47/47
K4 occurrences              39463
exact groups                161
privacy-safe witnesses      617
all 11 target tags          observed
zero/unclassified/bit/raw   0/0/0/0
raw rerun determinism       exact / {ORACLE_LOG_SHA}
groups SHA256               {GROUP_SHA}
privacy                     PASS
prod/Cargo/fixture/corpus/
support mutations           0/0/0/0/0
outcome                     A
next                        R3.17N K4 contract admission
```
"""
    write(str(p), s)


def update_current_state() -> None:
    p = Path("docs/continuity/MIMIR_CURRENT_STATE.md")
    s = p.read_text(encoding="utf-8")
    s = exact_replace(
        s,
        "**Completed K3 differential:** `R3.17L — Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch`\n**Current exact pass:** `R3.17M — K4 gameplay-structured wire-format evidence`",
        "**Completed K3 differential:** `R3.17L — Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch`\n**Completed K4 evidence:** `R3.17M — Outcome A / 39463 occurrences / 161 exact structural-context groups / all 11 tags observed`\n**Current exact pass:** `R3.17N — K4 evidence-supported contract admission`",
        "current state header",
    )
    old = """## 4. R3.17M exact next pass

R3.17M is read-only K4 evidence over the same frozen 47-replay lane. Instrument pinned Boxcars for `CamSettings`, `TeamPaint`, `TeamLoadout`, `ClubColors`, `Reservation`, `StatEvent`, `PlayerHistoryKey`, `DemolishFx`, `DemolishExtended`, `ExtendedExplosion`, and `LoadoutsOnline`; classify every observed wire shape/context and persist deterministic privacy-safe witnesses. A zero-occurrence tag remains unadmitted.

Production K4 decoding remains closed. If R3.17M closes Outcome A, K4 contract admission is a separate pass before any native implementation. R3.18 property-loop work remains closed until the R3.17 attribute-family dependency is explicitly satisfied.

## 5. Still closed"""
    new = f"""## 4. R3.17M K4 evidence closure

```text
authority head                {M_HEAD}
authority run/job             {M_RUN} / {M_JOB} SUCCESS
exact-head normal CI          {M_CI_RUN} / {M_CI_JOB} SUCCESS
artifact                      {M_ARTIFACT}
artifact digest               {M_DIGEST}
replay identity               47/47
Boxcars oracle decode         47/47
K4 occurrences                39463
exact structural groups       161
privacy-safe witnesses        617
zero target tags              0
unclassified/bit/raw failures 0/0/0
deterministic rerun           exact
privacy                       PASS
production/Cargo/fixture/
corpus/support mutation       0/0/0/0/0
outcome                       A
```

All 11 target tags were observed. The largest structural families are `LoadoutsOnline` with 73 observed shapes and `Reservation` with 35; they remain exact-group evidence and must not be broadened through Cartesian products.

## 5. R3.17N exact next pass

R3.17N is contract-only. Freeze the exact 161 R3.17M structural/context groups into a canonical admitted-group artifact, prove 161/161 equality with the evidence artifact, define atomic failure and exact one-value end semantics, and keep all unobserved branches explicit rejects. Production Rust remains unchanged.

Only after R3.17N Outcome A may a separate native K4 implementation pass open. R3.18 property-loop work remains closed.

## 6. Still closed"""
    s = exact_replace(s, old, new, "current state M section")
    s = s.replace("K4 contract / native payload decode", "K4 contract not yet admitted / native payload decode", 1)
    write(str(p), s)


def update_state_json() -> None:
    p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
    state = json.loads(p.read_text(encoding="utf-8"))
    if state.get("current_pass") != "R3.17M":
        raise SystemExit(f"unexpected current_pass {state.get('current_pass')!r}")
    state["last_completed_evidence_pass"] = "R3.17M"
    state["last_completed_evidence_outcome"] = "A — 47/47 oracle decode; 39463 K4 occurrences; all 11 target tags observed; 161 exact structural/context groups; 617 privacy-safe witnesses; zero structural/mutation failures"
    state["current_pass"] = "R3.17N"
    state["current_pass_kind"] = "contract-only K4 evidence-supported exact-group admission"
    state["current_pass_goal"] = "Freeze exactly the 161 R3.17M structural/context groups into a canonical admitted-group contract with 161/161 evidence equality, atomic failure, exact one-value end semantics and zero cross-product widening."
    state["current_pass_stop_boundary"] = "Contract only; no production Rust/Cargo/fixture/corpus/support mutation, no native K4 implementation, and no second property, actor/frame, lifecycle, raw-state/event/skill/runtime/export widening."
    files = state["next_files_to_read"]
    anchor = "docs/continuity/MIMIR_R3_17M_EXECUTION_SPEC.md"
    idx = files.index(anchor) + 1
    for item in ["docs/continuity/MIMIR_R3_17M_DECISION.md", "docs/continuity/MIMIR_R3_17N_EXECUTION_SPEC.md"]:
        if item not in files:
            files.insert(idx, item)
            idx += 1
    state["r3_17m"] = {
        "outcome": "A — admitted / complete",
        "pass_type": "read-only K4 gameplay-structured wire-format evidence",
        "production_source_changed": False,
        "continuity_base_sha": BASE_MAIN,
        "production_sha": PROD_SHA,
        "authority_head": M_HEAD,
        "workflow_run": M_RUN,
        "workflow_job": M_JOB,
        "exact_head_ci_run": M_CI_RUN,
        "exact_head_ci_job": M_CI_JOB,
        "artifact_id": M_ARTIFACT,
        "artifact_digest": M_DIGEST,
        "supported_replays": 47,
        "oracle_decode_success": 47,
        "k4_occurrences": 39463,
        "exact_structural_context_groups": 161,
        "privacy_safe_witness_rows": 617,
        "zero_target_tags": 0,
        "unclassified_occurrences": 0,
        "bit_monotonicity_failures": 0,
        "raw_payload_shape_failures": 0,
        "deterministic_rerun": "PASS / raw logs and analysis outputs exact",
        "raw_oracle_log_sha256": ORACLE_LOG_SHA,
        "groups_sha256": GROUP_SHA,
        "witnesses_sha256": WITNESS_SHA,
        "summary_sha256": SUMMARY_SHA,
        "aggregate_sha256": AGG_SHA,
        "privacy": "PASS",
        "production_cargo_fixture_corpus_support_mutation": "0/0/0/0/0",
        "tag_occurrences": {tag: data[0] for tag, data in TAG_COUNTS.items()},
        "tag_replay_counts": {tag: data[1] for tag, data in TAG_COUNTS.items()},
        "tag_shape_counts": {tag: data[2] for tag, data in TAG_COUNTS.items()},
        "next_pass": "R3.17N",
    }
    write(str(p), json.dumps(state, indent=2, ensure_ascii=False))


def main() -> None:
    write("docs/continuity/MIMIR_R3_17M_DECISION.md", decision_text())
    write("docs/continuity/MIMIR_R3_17N_EXECUTION_SPEC.md", next_spec_text())
    update_continue()
    update_graph()
    update_current_state()
    update_state_json()
    print("R3.17M continuity closure generated")
    print("next=R3.17N K4 evidence-supported contract admission")


if __name__ == "__main__":
    main()
