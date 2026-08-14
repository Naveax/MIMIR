from __future__ import annotations

import json
from pathlib import Path

BASE = "2d338d4244ce07122bb97097c516193f68ff73b7"
PROD = "9bfa837c69c4751f70ca63a17c65f0f89877ff32"
SOURCE_BLOB = "7288238cfb5338653552435be6af41f0dd7a4e85"
AUDIT_HEAD = "9b8e8fe82ab5bdc663eecc3f5d3cd1e3b8ee38ac"
AUDIT_RUN = 31809282874
AUDIT_JOB = 94795704797
AUDIT_CI_RUN = 31809282903
AUDIT_CI_JOB = 94795705073
ARTIFACT_ID = 9222624242
ARTIFACT_DIGEST = "sha256:d6c773d593c3c50957507a19056e85aef8b769fdc03fd88c6d693b1258c0af28"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


# 1. Master continuity handbook.
p = Path("MIMIR_CONTINUE_HERE.md")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    """LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.17E — K2 object/reference/text wire evidence / Outcome A / 47/47 / 110539 occurrences\n\nLAST_COMPLETED_CONTRACT_PASS:\n  R3.17F — evidence-supported K2 object/reference/text contract / Outcome A\n\nCURRENT_PASS:\n  R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses\n\nCURRENT_PASS_TYPE:\n  read-only differential audit / NO production capability widening""",
    """LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.17H — native K2 differential audit / Outcome A / 469 of 469 exact / 7 of 7 negatives\n\nLAST_COMPLETED_CONTRACT_PASS:\n  R3.17F — evidence-supported K2 object/reference/text contract / Outcome A\n\nCURRENT_PASS:\n  R3.17I — K3 spatial/physics wire-format evidence\n\nCURRENT_PASS_TYPE:\n  read-only evidence / pinned-oracle instrumentation / NO production Rust change""",
    "continue current pass",
)
s = replace_once(
    s,
    """R3_17H_OPEN_BOUNDARY:\n  read-only differential audit only; production Rust mutation forbidden\n  anchor to immutable R3.17E evidence identities and pinned Boxcars SHA\n  select the exact 469 privacy-safe R3.17E witness occurrences\n  regenerate raw values only ephemerally; persist no clear player/account payloads\n  compare native vs pinned oracle shape, exact width/end, context gate and semantic equality in-memory\n\nR3_17H_HARD_STOP:\n  no production implementation changes in the audit pass\n  no second property / property-loop continuation\n  no unobserved K2 variants\n  no K3/K4, lifecycle, raw-state, event, skill, runtime or export widening\n  no Cargo, fixture, corpus or support-lane change\n\nNEXT PASS IF R3.17H OUTCOME A:\n  decide the next evidence family only after the differential closure is admitted""",
    f"""R3_17H_AUDIT_CLOSURE:\n  Outcome A / read-only / production Rust unchanged at {PROD}\n  authority head: {AUDIT_HEAD}\n  authority run/job: {AUDIT_RUN} / {AUDIT_JOB} SUCCESS\n  exact-head normal CI: {AUDIT_CI_RUN} / {AUDIT_CI_JOB} SUCCESS\n  artifact: {ARTIFACT_ID}\n  artifact digest: {ARTIFACT_DIGEST}\n  immutable witnesses selected: 469/469\n  native decode success: 469/469\n  tag/semantic variant exact: 469/469\n  payload width exact: 469/469\n  payload end exact: 469/469\n  context gate exact: 469/469\n  semantic value exact in-memory: 469/469\n  negative controls: 7/7 PASS; privacy scan: PASS\n  production/Cargo/corpus mutation: 0/0/0\n\nR3_17I_OPEN_BOUNDARY:\n  evidence-only K3 spatial/physics family: Location / RigidBody / ReplicatedBoost / PickupNew\n  use the same exact 47 supported replay identities and pinned Boxcars SHA\n  characterize exact payload start/end/width, version/context gates, field boundaries and observed shapes\n  select privacy-safe witnesses for every observed shape/context family\n  a missing/unobserved tag or ambiguous shape is Outcome B, not permission to infer a contract from oracle source\n\nR3_17I_HARD_STOP:\n  no production Rust implementation in the evidence pass\n  no K3 contract admission by analogy; only observed shapes may become future candidates\n  no second property / property-loop continuation\n  no K4, lifecycle, raw-state, event, skill, runtime or export widening\n  no Cargo, fixture, corpus or support-lane change\n\nNEXT PASS IF R3.17I OUTCOME A:\n  R3.17J — contract admission for evidence-supported K3 shapes only""",
    "continue H->I block",
)
p.write_text(s, encoding="utf-8", newline="\n")


# 2. Knowledge graph.
p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    """R3.17G K2 production decision           |\nR3.17H active differential spec         |""",
    """R3.17G K2 production decision           |\nR3.17H K2 differential decision         |\nR3.17I active K3 evidence spec           |""",
    "graph decision list",
)
s = replace_once(
    s,
    """13. `docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md`\n14. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n15. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n16. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n17. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n18. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n19. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n20. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`""",
    """13. `docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md`\n14. `docs/continuity/MIMIR_R3_17H_DECISION.md`\n15. `docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md`\n16. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n17. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n18. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n19. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n20. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n21. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n22. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`""",
    "graph reading order",
)
s = replace_once(
    s,
    """ -> R3.17H native K2 differential audit: ACTIVE""",
    f""" -> R3.17H native K2 differential audit: OUTCOME A / CLOSED\n      authority {AUDIT_HEAD}\n      run/job {AUDIT_RUN} / {AUDIT_JOB} SUCCESS\n      exact-head CI {AUDIT_CI_RUN} / {AUDIT_CI_JOB} SUCCESS\n      artifact {ARTIFACT_ID} / {ARTIFACT_DIGEST}\n      469/469 exact on decode/variant/width/end/context/semantic; 7/7 negatives PASS\n -> R3.17I K3 spatial/physics wire evidence: ACTIVE""",
    "graph replay chain",
)
s = replace_once(
    s,
    """R3.17H is read-only. It may regenerate raw witness values ephemerally for comparison, but no clear player/account payload may enter durable evidence. PartyLeader `None`, non-Epic PartyLeader and every other unseen K2 variant remain closed.\n\nProperty-loop continuation, next actor/frame iteration, lifecycle mutation, K3 spatial/physics and K4 gameplay-structured families remain closed.""",
    """R3.17H closed Outcome A without widening production: all 469 immutable K2 witnesses matched exactly and all seven negative controls failed closed. PartyLeader `None`, non-Epic PartyLeader and every other unseen K2 variant remain closed.\n\nR3.17I is evidence-only for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; native K3 decode remains closed. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.""",
    "graph capability lock",
)
insert = f"""
## R3.17H differential closure

```text
authority head              {AUDIT_HEAD}
authority run/job           {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
exact-head normal CI        {AUDIT_CI_RUN} / {AUDIT_CI_JOB} SUCCESS
artifact                    {ARTIFACT_ID}
artifact digest             {ARTIFACT_DIGEST}
witness selection           469/469
native decode               469/469
variant / width / end       469/469 exact
context / semantic          469/469 exact
negative controls           7/7 PASS
privacy scan                PASS
production/Cargo/corpus     0/0/0 mutations
outcome                     A
```

"""
s = replace_once(s, "## Authority rule\n", insert + "## Authority rule\n", "graph H closure insertion")
p.write_text(s, encoding="utf-8", newline="\n")


# 3. Machine-readable continuity state.
p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
data = json.loads(p.read_text(encoding="utf-8"))
data["last_completed_read_only_audit"] = "R3.17H"
data["current_pass"] = "R3.17I"
data["current_pass_kind"] = "read-only K3 spatial/physics wire-format evidence"
data["current_pass_goal"] = (
    "Characterize exact observed Location, RigidBody, ReplicatedBoost and PickupNew wire shapes, "
    "field boundaries, payload widths/end bits and version/context gates across the frozen 47-replay lane."
)
data["current_pass_stop_boundary"] = (
    "Evidence only; no production Rust, Cargo, corpus/support-lane, K3 contract/implementation, "
    "property-loop, lifecycle, K4 or downstream widening."
)
data["last_completed_native_differential_audit"] = "R3.17H"
data["r3_17h"] = {
    "outcome": "A — admitted / complete",
    "production_source_changed": False,
    "continuity_base_sha": BASE,
    "production_sha": PROD,
    "production_source_blob": SOURCE_BLOB,
    "evidence_head_sha": AUDIT_HEAD,
    "workflow_run": AUDIT_RUN,
    "workflow_job": AUDIT_JOB,
    "exact_head_ci_run": AUDIT_CI_RUN,
    "exact_head_ci_job": AUDIT_CI_JOB,
    "artifact_id": ARTIFACT_ID,
    "artifact_digest": ARTIFACT_DIGEST,
    "witness_rows_selected": 469,
    "native_decode_success": 469,
    "variant_exact": 469,
    "payload_width_exact": 469,
    "payload_end_exact": 469,
    "context_gate_exact": 469,
    "semantic_value_exact": 469,
    "negative_controls": "7/7 PASS",
    "privacy_scan": "PASS",
    "production_mutation": 0,
    "cargo_mutation": 0,
    "corpus_fixture_mutation": 0,
    "match_rows_sha256": "745d4db19c55f91a3f8b8b88d85db866aeb3c8d64f15570a0f9af52677e37375",
    "summary_sha256": "24f9233670e52c8cd384782d7e4449bce91e7c06b54310a82cad1c1860c118e2",
    "aggregate_sha256": "752dd675cf211ea47aa2daa928032a4e104c4e68d0224dc8b98d6079b09b7701",
    "next_pass": "R3.17I",
}
closed = data.get("closed_now", [])
closed = [
    "native K3/K4 attribute payload decode" if x == "native K2/K3/K4 attribute payload decode" else x
    for x in closed
]
data["closed_now"] = closed
files = data.get("next_files_to_read", [])
needle = "docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md"
if needle not in files:
    raise SystemExit("continuity state missing R3.17H spec in reading order")
new_files = []
for item in files:
    new_files.append(item)
    if item == needle:
        new_files.append("docs/continuity/MIMIR_R3_17H_DECISION.md")
        new_files.append("docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md")
data["next_files_to_read"] = new_files
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


# 4. Short current-state document.
Path("docs/continuity/MIMIR_CURRENT_STATE.md").write_text(
f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.17G — direct native evidence-admitted K2 decoder implementation`
**Completed K1 differential:** `R3.17D — Outcome A / 96 of 96 exact`
**Completed K2 evidence:** `R3.17E — Outcome A / 47 of 47 / 110539 occurrences`
**Completed K2 contract:** `R3.17F — Outcome A / atomic evidence-supported shapes`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Current exact pass:** `R3.17I — K3 spatial/physics wire-format evidence`

## 1. Truthful production boundary

Production remains exactly R3.17G. MIMIR can directly decode one already-resolved K1 scalar or one R3.17F-admitted K2 payload and then stops at the exact end bit. R3.17H audited that K2 surface; it did not add another property, actor, frame, lifecycle transition or K3 decoder.

```text
production SHA               {PROD}
production source blob       {SOURCE_BLOB}
R3.17H authority head        {AUDIT_HEAD}
R3.17H run/job               {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
R3.17H exact-head CI         {AUDIT_CI_RUN} / {AUDIT_CI_JOB} SUCCESS
R3.17H artifact              {ARTIFACT_ID}
R3.17H artifact digest       {ARTIFACT_DIGEST}
```

## 2. R3.17H closure

The immutable 469 R3.17E witness identities were regenerated from the same 47 replay lane with pinned Boxcars and compared against the native R3.17G decoder.

```text
witness selection            469 / 469
native decode                469 / 469
attribute variant            469 / 469 exact
payload width                469 / 469 exact
payload end                  469 / 469 exact
context gate                 469 / 469 exact
semantic value               469 / 469 exact in-memory
negative controls            7 / 7 PASS
privacy scan                 PASS
production/Cargo/corpus      0 / 0 / 0 mutations
outcome                      A
```

Two earlier disposable runs failed only in temporary audit plumbing before native/oracle comparison and are not authority: the first attempted an unnecessary raw-SHA fetch; the second used a line-ending-sensitive file SHA check. V3 replaced that check with the immutable Git blob identity and is the sole admitted audit authority.

## 3. R3.17I exact next pass

R3.17I is evidence-only for the roadmap K3 spatial/physics family:

```text
Location
RigidBody
ReplicatedBoost
PickupNew
```

On the exact same 47-replay lane, instrument pinned Boxcars to record exact payload start/end/width, version/context, field boundaries and every observed wire-shape family. Select privacy-safe witnesses per observed shape/context. If a tag is absent or a shape is ambiguous, request targeted evidence rather than inferring a production contract from Boxcars source.

No production Rust change is allowed in R3.17I. Outcome A may open `R3.17J — contract admission for evidence-supported K3 shapes only`.

## 4. Still closed

```text
native K3/K4 payload decode
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
""",
encoding="utf-8",
newline="\n",
)


# 5. R3.17H decision.
Path("docs/continuity/MIMIR_R3_17H_DECISION.md").write_text(
f"""# MIMIR — R3.17H Native K2 Differential Audit Decision

**Date:** 2026-08-14
**Pass:** `R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses`
**Outcome:** **A — ADMITTED / COMPLETE**
**Production Rust changed:** **NO**

## Frozen authority

```text
continuity base               {BASE}
native production SHA         {PROD}
native source blob            {SOURCE_BLOB}
R3.17E evidence head          19db534a3668f84f1c5ce36ef1252c52841d890f
R3.17E artifact               9219554878
R3.17E artifact digest        sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
R3.17E witnesses SHA256       7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
pinned Boxcars SHA            c70e77df7af81b436cb545d070bb90c82f562d0b
R3.17H authority head         {AUDIT_HEAD}
authority run/job             {AUDIT_RUN} / {AUDIT_JOB} SUCCESS
exact-head normal CI          {AUDIT_CI_RUN} / {AUDIT_CI_JOB} SUCCESS
artifact                      {ARTIFACT_ID}
artifact digest               {ARTIFACT_DIGEST}
```

## Differential result

The exact immutable 469 R3.17E witness occurrences were regenerated from all 47 supported replay identities. Raw/oracle semantic material existed only in ephemeral runner storage. The packed payload for each selected occurrence was normalized to bit zero without changing the packed bit sequence, then decoded by the frozen R3.17G native decoder.

```text
47 replay identities                     PASS
oracle regeneration                      47/47 / 110539 K2 occurrences
immutable witness selection              469/469
native decode success                    469/469
attribute tag / semantic variant         469/469 exact
payload width                            469/469 exact
payload end / consumed bits              469/469 exact
context gate                             469/469 exact
semantic value                           469/469 exact in-memory
negative controls                        7/7 PASS
privacy scan                             PASS
production mutation                      0
Cargo mutation                           0
corpus / fixture mutation                0
```

The seven fail-closed controls covered PartyLeader None, non-Epic PartyLeader, an unadmitted UniqueId system, wrong UniqueId net version, RL223 QWordString Empty, RL223 QWordString UTF16 and wrong Epic declared length.

## Durable receipt identities

```text
source scope SHA256          faff88fd850dfd9e6e8fd6b840a584f5890d27b394b938384d5944dddbf61c6c
replay identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
driver manifest SHA256       c27363f06a5eb408f5af925b3e86d4f5f7e0db687fddd337b9cf5e3c7cc3f573
match rows SHA256            745d4db19c55f91a3f8b8b88d85db866aeb3c8d64f15570a0f9af52677e37375
summary SHA256               24f9233670e52c8cd384782d7e4449bce91e7c06b54310a82cad1c1860c118e2
aggregate SHA256             752dd675cf211ea47aa2daa928032a4e104c4e68d0224dc8b98d6079b09b7701
```

Durable rows contain structural identities, cryptographic hashes and match flags only. Clear player names, account IDs, raw identity payloads and private text were not persisted.

## Rejected disposable attempts

Two earlier temporary runs are explicitly non-authoritative:

```text
31808925259 / 94794512217
  stopped before oracle build because the workflow attempted an unnecessary direct raw-SHA fetch

31809102097 / 94795103857
  stopped before oracle build because a canonical helper was checked with a line-ending-sensitive file SHA256
```

Neither reached native-vs-oracle semantic comparison. V3 froze the canonical helper by immutable Git blob identity `e6a551154a90ba7fa2cf5b887c9a8cfb9cfe933c` and is the sole audit authority.

## Capability consequence

R3.17H confirms the already-published R3.17G K2 surface. It does **not** widen production capability. One successful K2 value still stops at its exact payload end bit; no second property, actor/frame iteration or lifecycle mutation is admitted.

## Next exact pass

Roadmap order makes the first unfinished attribute wave `K3 spatial/physics`. Open:

`R3.17I — K3 spatial/physics wire-format evidence` for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` only.
""",
encoding="utf-8",
newline="\n",
)


# 6. R3.17I execution spec.
Path("docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md").write_text(
f"""# MIMIR R3.17I — K3 Spatial/Physics Wire-Format Evidence Execution Spec

**Pass type:** read-only evidence
**Production implementation:** forbidden
**Production authority:** R3.17G Outcome A, confirmed by R3.17H Outcome A
**Oracle:** pinned Boxcars only

## Goal

Characterize the exact observed wire shapes for the roadmap K3 spatial/physics attribute family across the frozen 47-replay supported lane, without admitting or implementing a native K3 decoder.

```text
Location
RigidBody
ReplicatedBoost
PickupNew
```

## Frozen identities

```text
continuity base              {BASE}
native production SHA        {PROD}
native source blob           {SOURCE_BLOB}
R3.17H authority head        {AUDIT_HEAD}
R3.17H artifact              {ARTIFACT_ID}
R3.17H artifact digest       {ARTIFACT_DIGEST}
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
```

## Evidence method

1. Verify fresh main and the exact frozen native source blob before instrumentation.
2. Reuse the exact 47 replay identities already admitted by R3.17E/R3.17H; do not widen the corpus in this pass.
3. Instrument pinned Boxcars at the already-resolved attribute payload boundary and decode all four K3 tags while recording exact payload start/end/width and version/context.
4. Record field-boundary evidence sufficient to distinguish observed wire shapes:
   - `Location`: vector codec/context and exact component/payload boundaries.
   - `RigidBody`: sleeping flag, location, rotation representation/context, velocity presence branches and exact subfield boundaries.
   - `ReplicatedBoost`: exact field order/width for grant count, boost amount and the two remaining bytes.
   - `PickupNew`: optional instigator/reference branch, picked-up byte and exact branch boundaries.
5. Classify every observed occurrence into a deterministic shape identifier derived from actual wire structure, not from debug formatting alone.
6. Produce frequency distributions by tag, shape, version/net-version/context and payload width.
7. Select deterministic privacy-safe witnesses covering every observed shape/context family. Persist structural identities, bounded numeric/spatial values where safe, packed-payload hashes and exact bit ranges; do not persist unrelated player/account identity material.
8. Cross-check cursor monotonicity, packed-bit shape and exact replay identity. Production Rust, manifests, fixtures and corpus stay unchanged.

## Required evidence gates

```text
replay identity verification             47 / 47
oracle replay decode                     47 / 47
K3 occurrence accounting                 exact / deterministic
Location occurrences                     > 0 or Outcome B targeted evidence
RigidBody occurrences                    > 0 or Outcome B targeted evidence
ReplicatedBoost occurrences              > 0 or Outcome B targeted evidence
PickupNew occurrences                    > 0 or Outcome B targeted evidence
observed shape classification            100%
shape mismatch / unclassified            0
bit monotonicity failures                0
raw packed-payload shape failures        0
privacy scan                             PASS
production mutation                      0
Cargo mutation                           0
corpus / fixture mutation                0
```

If any tag has zero supported-lane occurrences, or an observed branch cannot be classified without guessing, use Outcome B and request only the targeted missing evidence. Boxcars source code alone is not enough to admit an unobserved branch.

## Evidence fields

Every durable occurrence/witness identity should be reproducible from a structural key including at least:

```text
replay identity
frame / actor ordinal
actor context
stream/property identity
attribute tag
version + net_version + relevant context gates
payload start bit
payload end bit
payload width
shape id
packed payload SHA256
```

Field-specific structural summaries may be stored only when they are required to prove the wire shape and are privacy-safe.

## Outcome rules

- **Outcome A:** all four tags are observed, every K3 occurrence is deterministically classified, cursor/raw-payload checks are clean, privacy passes and production/Cargo/corpus mutation is zero.
- **Outcome B:** supported evidence is insufficient for one or more tags/branches; request targeted evidence without widening production.
- **Outcome C:** oracle instrumentation or existing structural assumptions contradict reproducible replay evidence; stop and repair the evidence model before any contract pass.

## Hard stop

R3.17I must not change production Rust, Cargo manifests/lockfiles, fixtures, supported replay policy or downstream capability. It does not admit K3 decoding, second-property continuation, actor/frame iteration, lifecycle mutation, K4, raw state, events, replay slicing, skills, runtime or export.

## Next pass

Only on Outcome A open `R3.17J — K3 contract admission for evidence-supported shapes only`. R3.17J is contract-only; native K3 implementation must remain a later separate pass.
""",
encoding="utf-8",
newline="\n",
)

print("R3_17H_CONTINUITY_SYNC=PASS")
