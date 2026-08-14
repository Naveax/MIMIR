from pathlib import Path
import json
import re

BASE = "4df00aa76a99b85a122210c4f929523f72fe9ef4"
PROD = "9bfa837c69c4751f70ca63a17c65f0f89877ff32"
PROD_BLOB = "7288238cfb5338653552435be6af41f0dd7a4e85"
EVIDENCE_HEAD = "8962ddc6bd77b5469fa7ebc93c95334e5725a8ab"
RUN = 31812804986
JOB = 94807233173
CI_RUN = 31812804992
CI_JOB = 94807233091
ARTIFACT = 9223916983
ARTIFACT_DIGEST = "sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


# MIMIR_CONTINUE_HERE.md
p = Path("MIMIR_CONTINUE_HERE.md")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    "CURRENT_PASS:\n  R3.17I — K3 spatial/physics wire-format evidence\n\nCURRENT_PASS_TYPE:\n  read-only evidence / pinned-oracle instrumentation / NO production Rust change",
    "CURRENT_PASS:\n  R3.17J — K3 contract admission for evidence-supported shapes only\n\nCURRENT_PASS_TYPE:\n  contract-only / docs + test-vector planning / NO production Rust change",
    "continue current pass",
)
old = '''R3_17I_OPEN_BOUNDARY:
  evidence-only K3 spatial/physics family: Location / RigidBody / ReplicatedBoost / PickupNew
  use the same exact 47 supported replay identities and pinned Boxcars SHA
  characterize exact payload start/end/width, version/context gates, field boundaries and observed shapes
  select privacy-safe witnesses for every observed shape/context family
  a missing/unobserved tag or ambiguous shape is Outcome B, not permission to infer a contract from oracle source

R3_17I_HARD_STOP:
  no production Rust implementation in the evidence pass
  no K3 contract admission by analogy; only observed shapes may become future candidates
  no second property / property-loop continuation
  no K4, lifecycle, raw-state, event, skill, runtime or export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17I OUTCOME A:
  R3.17J — contract admission for evidence-supported K3 shapes only
'''
new = f'''R3_17I_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at {PROD}
  authority head: {EVIDENCE_HEAD}
  authority run/job: {RUN} / {JOB} SUCCESS
  exact-head normal CI: {CI_RUN} / {CI_JOB} SUCCESS
  artifact: {ARTIFACT}
  artifact digest: {ARTIFACT_DIGEST}
  47/47 oracle decode; 1699169 K3 occurrences; exact groups 1950; privacy-safe witnesses 6276
  Location: 26734 / 47 replays / 7 observed vector shapes / exact context groups 11
  RigidBody: 1550254 / 47 replays / 1169 observed structural shapes / exact context groups 1934
  ReplicatedBoost: 11058 / 11 replays / exact u8x4 / RL223=true observed only
  PickupNew: 111123 / 47 replays / None=90312 / SomeI32=20811
  RigidBody awake=1548807 / sleeping=1447 / rotation=quat56 only
  version context: 868.32 / net10 only; Location/RigidBody/PickupNew observed in RL223 false+true
  zero-tag/unclassified/bit-monotonicity/raw-payload failures: 0/0/0/0
  privacy-safe output: PASS; production/Cargo/corpus mutation: 0/0/0

R3_17J_OPEN_BOUNDARY:
  contract-only for the R3.17I evidence-supported K3 shapes; production Rust mutation forbidden
  freeze shared net10 vector prefix/component semantics only for observed size/header outcomes
  freeze Location, RigidBody, ReplicatedBoost and PickupNew context gates and atomic failure behavior
  preserve exact one-value end-bit semantics and privacy-safe evidence-derived test-vector requirements
  unseen vector size/header outcomes, quat48, other net/version contexts and unsupported branch combinations stay closed

R3_17J_HARD_STOP:
  no native K3 implementation during contract admission
  no second property / property-loop continuation
  no K4, lifecycle, raw-state, event, skill, runtime or export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17J OUTCOME A:
  R3.17K — direct native K3 decoder implementation for contract-admitted variants only
'''
s = replace_once(s, old, new, "continue R3.17I block")
p.write_text(s, encoding="utf-8", newline="\n")

# MIMIR_KNOWLEDGE_GRAPH.md
p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    "R3.17H K2 differential decision         |\nR3.17I active K3 evidence spec           |",
    "R3.17H K2 differential decision         |\nR3.17I K3 evidence decision               |\nR3.17J active K3 contract spec            |",
    "graph continuity nodes",
)
s = replace_once(
    s,
    "15. `docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md`\n16. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n17. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n18. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n19. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n20. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n21. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n22. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "15. `docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md`\n16. `docs/continuity/MIMIR_R3_17I_DECISION.md`\n17. `docs/continuity/MIMIR_R3_17J_EXECUTION_SPEC.md`\n18. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n19. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n20. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n21. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n22. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n23. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n24. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "reading order",
)
s = replace_once(
    s,
    " -> R3.17I K3 spatial/physics wire evidence: ACTIVE",
    f" -> R3.17I K3 spatial/physics wire evidence: OUTCOME A / CLOSED\n      authority {EVIDENCE_HEAD}\n      run/job {RUN} / {JOB} SUCCESS\n      exact-head CI {CI_RUN} / {CI_JOB} SUCCESS\n      artifact {ARTIFACT} / {ARTIFACT_DIGEST}\n      47/47 / 1699169 occurrences / 1950 exact groups / 6276 witnesses / 0 structural failures\n -> R3.17J K3 evidence-supported contract admission: ACTIVE / CONTRACT-ONLY",
    "decoder chain",
)
s = replace_once(
    s,
    "R3.17I is evidence-only for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; native K3 decode remains closed. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.",
    "R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` without widening production. R3.17J is contract-only and may admit only the observed R3.17I wire/context shapes; native K3 decode remains closed. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.",
    "capability lock",
)
insert = f'''
## R3.17I K3 evidence closure

```text
authority head              {EVIDENCE_HEAD}
authority run/job           {RUN} / {JOB} SUCCESS
exact-head normal CI        {CI_RUN} / {CI_JOB} SUCCESS
artifact                    {ARTIFACT}
artifact digest             {ARTIFACT_DIGEST}
replays                     47/47
K3 occurrences              1699169
exact context groups        1950
privacy-safe witnesses      6276
Location                    26734 / 47 replays / 7 structural shapes
RigidBody                   1550254 / 47 replays / awake 1548807 / sleeping 1447 / quat56 only
ReplicatedBoost             11058 / 11 replays / u8x4 / RL223=true only observed
PickupNew                   111123 / 47 replays / None 90312 / SomeI32 20811
zero-tag/unclassified       0/0
bit/raw-payload failures    0/0
privacy                     PASS
production/Cargo/corpus     0/0/0 mutations
outcome                     A
```

'''
s = replace_once(s, "## Authority rule\n", insert + "## Authority rule\n", "K3 closure insertion")
p.write_text(s, encoding="utf-8", newline="\n")

# MIMIR_CONTINUITY_STATE.json
p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
data = json.loads(p.read_text(encoding="utf-8"))
data["updated_date"] = "2026-08-14"
data["current_pass"] = "R3.17J"
data["current_pass_kind"] = "contract-only K3 spatial/physics admission for evidence-supported shapes"
data["current_pass_goal"] = "Freeze exact net10 Location, RigidBody, ReplicatedBoost and PickupNew wire/context contracts from R3.17I Outcome A without implementing native K3 decoding."
data["current_pass_stop_boundary"] = "Contract only; no production Rust, Cargo, corpus/support-lane, K3 implementation, property-loop, lifecycle, K4 or downstream widening."
data["last_completed_evidence_pass"] = "R3.17I"
data["last_completed_evidence_outcome"] = "A — 47/47 oracle decode; 1699169 K3 occurrences; all four tags observed; 1950 exact groups; zero structural/mutation failures; privacy-safe output PASS"
files = data.get("next_files_to_read", [])
for name in ["docs/continuity/MIMIR_R3_17I_DECISION.md", "docs/continuity/MIMIR_R3_17J_EXECUTION_SPEC.md"]:
    if name not in files:
        anchor = "docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md"
        idx = files.index(anchor) + 1 if anchor in files else len(files)
        files.insert(idx, name)
data["next_files_to_read"] = files
data["r3_17i"] = {
    "outcome": "A — admitted / evidence complete",
    "production_source_changed": False,
    "continuity_base_sha": BASE,
    "production_sha": PROD,
    "production_source_blob": PROD_BLOB,
    "oracle_sha": "c70e77df7af81b436cb545d070bb90c82f562d0b",
    "evidence_head_sha": EVIDENCE_HEAD,
    "workflow_run": RUN,
    "workflow_job": JOB,
    "exact_head_ci_run": CI_RUN,
    "exact_head_ci_job": CI_JOB,
    "artifact_id": ARTIFACT,
    "artifact_digest": ARTIFACT_DIGEST,
    "artifact_size_bytes": 1411635,
    "replays_total": 47,
    "oracle_decode_success": 47,
    "k3_occurrences_total": 1699169,
    "location_occurrences": 26734,
    "rigid_body_occurrences": 1550254,
    "replicated_boost_occurrences": 11058,
    "pickup_new_occurrences": 111123,
    "rigid_body_awake": 1548807,
    "rigid_body_sleeping": 1447,
    "pickup_new_none": 90312,
    "pickup_new_some_i32": 20811,
    "exact_context_groups": 1950,
    "witness_rows": 6276,
    "unclassified": 0,
    "bit_monotonicity_failures": 0,
    "raw_payload_shape_failures": 0,
    "privacy_safe_output": True,
    "production_mutation": 0,
    "cargo_mutation": 0,
    "corpus_mutation": 0,
    "source_scope_sha256": "b47aacbcb2c1b6a245b0b8779b6e48369814934f045f2e73db1be98e485cd619",
    "replay_identity_sha256": "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf",
    "groups_sha256": "04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b",
    "witnesses_sha256": "4ceb2290f753c59e4c3880eb43817923fbf3d6a44232582ca834205719839fda",
    "summary_sha256": "258a81be5c81e660e4db31fcef99b6ee78822496243ebaad0495cc0cb1e44a1e",
    "aggregate_sha256": "884fee52b216fbb49ccd6e88be4a10cf66bc9e952ceb853d24923046b4d24e08",
    "receipt_manifest_sha256": "1d63c0c4be779b65f98c3082656a20b42901d524b6b2e3d6171bdfdae3394303",
    "next_pass": "R3.17J"
}
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

# Current canonical state: replace whole concise document.
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.17G — direct native evidence-admitted K2 decoder implementation`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Completed K3 evidence:** `R3.17I — Outcome A / 47 of 47 / 1699169 occurrences / 1950 exact groups`
**Current exact pass:** `R3.17J — K3 contract admission for evidence-supported shapes only`

## 1. Truthful production boundary

Production remains exactly R3.17G. R3.17I is evidence-only and did not add a K3 decoder. MIMIR may still decode only one already-resolved K1 scalar or one R3.17F-admitted K2 payload and stop at the exact end bit.

```text
production SHA               {PROD}
production source blob       {PROD_BLOB}
R3.17I authority head        {EVIDENCE_HEAD}
R3.17I run/job               {RUN} / {JOB} SUCCESS
R3.17I exact-head CI         {CI_RUN} / {CI_JOB} SUCCESS
R3.17I artifact              {ARTIFACT}
R3.17I artifact digest       {ARTIFACT_DIGEST}
```

## 2. R3.17I closure

```text
oracle decode                47 / 47
K3 occurrences               1,699,169
Location                     26,734 / 47 replays / 7 observed vector shapes
RigidBody                    1,550,254 / 47 replays
  awake                      1,548,807
  sleeping                   1,447
  rotation                   quat56 only observed
ReplicatedBoost              11,058 / 11 replays / u8x4 / RL223=true only observed
PickupNew                    111,123 / 47 replays
  None                       90,312
  SomeI32                    20,811
exact context groups         1,950
privacy-safe witnesses       6,276
zero tags                    0
unclassified                 0
bit monotonicity failures    0
raw payload shape failures   0
privacy                      PASS
production/Cargo/corpus      0 / 0 / 0 mutations
outcome                      A
```

All observed K3 entries are version 868.32 / net10. `Location`, `RigidBody`, and `PickupNew` occur under both RL223 false and true. `ReplicatedBoost` is observed only under RL223 true. RigidBody uses only the 56-bit quaternion representation in this evidence lane; the older 48-bit representation remains unadmitted.

## 3. R3.17J exact next pass

R3.17J is contract-only. Freeze the exact observed net10 vector prefix/component rule, field order, context gates, end-bit semantics, truncation/malformed behavior, and privacy-safe evidence-derived test-vector contract for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`.

The shared vector candidate may admit only evidence-supported size/header outcomes. RigidBody must preserve sleeping versus awake velocity presence and quat56-only evidence. `ReplicatedBoost` remains restricted to its observed RL223=true context unless separately evidenced. `PickupNew` may consider only the observed `None` and `SomeI32` branches.

No production Rust change is allowed in R3.17J. Outcome A may open `R3.17K — direct native K3 decoder implementation for contract-admitted variants only`.

## 4. Still closed

```text
native K3/K4 payload decode
unobserved vector size/header outcomes
RigidBody quat48 / other version contexts
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
'''
Path("docs/continuity/MIMIR_CURRENT_STATE.md").write_text(current, encoding="utf-8", newline="\n")

# R3.17I decision.
decision = f'''# MIMIR — R3.17I K3 Spatial/Physics Wire-Format Evidence Decision

**Date:** 2026-08-14
**Pass:** `R3.17I — K3 spatial/physics wire-format evidence`
**Outcome:** **A — ADMITTED / COMPLETE**
**Production Rust changed:** **NO**

## Frozen authority

```text
continuity base               {BASE}
native production SHA         {PROD}
native source blob            {PROD_BLOB}
pinned Boxcars SHA            c70e77df7af81b436cb545d070bb90c82f562d0b
R3.17I authority head         {EVIDENCE_HEAD}
authority run/job             {RUN} / {JOB} SUCCESS
exact-head normal CI          {CI_RUN} / {CI_JOB} SUCCESS
artifact                      {ARTIFACT}
artifact size                 1411635 bytes
artifact digest               {ARTIFACT_DIGEST}
```

The downloaded canonical artifact ZIP hashes to the same SHA-256 carried by the GitHub artifact digest.

## Evidence result

```text
replay identities                         47 / 47 PASS
oracle replay decode                      47 / 47
K3 occurrences                            1,699,169
exact version/context groups              1,950
privacy-safe witness rows                 6,276
zero required tags                        0
shape mismatch / unclassified             0
bit monotonicity failures                 0
raw packed-payload shape failures         0
privacy scan                              PASS
production mutation                       0
Cargo mutation                            0
corpus / fixture mutation                 0
```

### Location

```text
occurrences                  26,734
replays                      47
version                      868.32 / net10
RL223                        false + true observed
observed structural shapes  7
exact context groups         11
payload widths               11, 31, 34, 52, 55, 59, 62 bits
```

Observed standalone vector size/header outcomes:

```text
size_bits 0  -> header 5 / component width 2
size_bits 7  -> header 4 / component width 9
size_bits 8  -> header 4 / component width 10
size_bits 14 -> header 4 / component width 16
size_bits 15 -> header 4 / component width 17
size_bits 16 -> header 5 / component width 18
size_bits 17 -> header 5 / component width 19
```

### RigidBody

```text
occurrences                  1,550,254
replays                      47
version                      868.32 / net10
RL223                        false + true observed
awake                        1,548,807
sleeping                     1,447
observed structural shapes   1,169
exact context groups         1,934
rotation                     56-bit quaternion only observed
```

Wire order is evidence-consistent with:

```text
sleeping bit
location vector
56-bit quaternion
if awake:
  linear velocity vector
  angular velocity vector
```

Observed vector size/header sets are intentionally recorded per subfield rather than generalized beyond evidence:

```text
awake location:   size_bits 10..19
sleeping location:size_bits 13,16,17,18,19
linear velocity:  size_bits 0..18
angular velocity: size_bits 0..15
```

For net10, observed header length is 5 bits for size_bits 0..5 and 16..19, and 4 bits for size_bits 6..15. Size bits 20/21 and the older 48-bit rotation representation were not observed and are not admitted by this pass.

### ReplicatedBoost

```text
occurrences                  11,058
replays                      11
version                      868.32 / net10
RL223                        true only observed
shape                        u8 x 4
payload width                32 bits
field order                  grant_count / boost_amount / unused1 / unused2
```

### PickupNew

```text
occurrences                  111,123
replays                      47
version                      868.32 / net10
RL223                        false + true observed
None branch                  90,312 / 9 bits
SomeI32 branch               20,811 / 41 bits
wire order                   presence bit / optional signed i32 actor ref / picked_up u8
```

## Durable receipt identities

```text
source scope SHA256          b47aacbcb2c1b6a245b0b8779b6e48369814934f045f2e73db1be98e485cd619
replay identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
instrumentation patch        6acf108213e526e15c463eb7f059a239f6f78b3b20036500c1ed3879e7cca013
groups JSONL                 04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b
witnesses JSONL              4ceb2290f753c59e4c3880eb43817923fbf3d6a44232582ca834205719839fda
summary JSON                 258a81be5c81e660e4db31fcef99b6ee78822496243ebaad0495cc0cb1e44a1e
aggregate                    884fee52b216fbb49ccd6e88be4a10cf66bc9e952ceb853d24923046b4d24e08
receipt manifest             1d63c0c4be779b65f98c3082656a20b42901d524b6b2e3d6171bdfdae3394303
raw Boxcars log              5bc6d8508b2a4af98b405d083f16b425c7fa9d092fc633eff61ff693562e4c5e
```

Durable witness rows contain structural identities, bounded numeric/spatial evidence and packed-payload hashes; unrelated account/player identity material and raw packed payload bytes are not persisted.

## Rejected disposable attempt

`31812224854 / 94805348633` is explicitly non-authoritative. Its frozen gate, Boxcars build/tests, 47-replay scan and analyzer all reached the same Outcome A counts, but the workflow then rejected the valid 1,950 groups / 6,276 witnesses using an arbitrary receipt-size bound. The authority run replaced that bound with the actual invariant: at least one and at most four witnesses per exact group. No analyzer, instrumentation, production, Cargo or corpus semantics changed.

## Capability consequence

R3.17I supplies wire evidence only. It does not make any K3 tag a native MIMIR decoder capability. Production remains R3.17G and still stops after one admitted K1/K2 value.

## Next exact pass

Open `R3.17J — K3 contract admission for evidence-supported shapes only` as contract-only. Production implementation remains forbidden until a later separate pass.
'''
Path("docs/continuity/MIMIR_R3_17I_DECISION.md").write_text(decision, encoding="utf-8", newline="\n")

# R3.17J execution spec.
spec = f'''# MIMIR R3.17J — K3 Evidence-Supported Contract Admission Execution Spec

**Pass type:** contract-only
**Production implementation:** forbidden
**Evidence authority:** R3.17I Outcome A
**Production authority:** R3.17G, unchanged

## Goal

Convert the exact R3.17I observations for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` into a minimal fail-closed native-decoder contract without writing production K3 decoding code.

## Frozen identities

```text
continuity base              {BASE}
native production SHA        {PROD}
native source blob           {PROD_BLOB}
R3.17I evidence head         {EVIDENCE_HEAD}
R3.17I authority run/job     {RUN} / {JOB} SUCCESS
R3.17I artifact              {ARTIFACT}
R3.17I artifact digest       {ARTIFACT_DIGEST}
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
```

## Common contract questions to freeze

1. LSB-first unaligned one-value input and exact consumed/end-bit semantics.
2. Atomic failure: on unsupported, malformed or truncated input, no successful partial K3 value may escape.
3. Exact version/context gate. Current evidence is 868.32 / net10 only.
4. Checked arithmetic for bit width and component bounds.
5. No acceptance of an unobserved vector header/size merely because pinned Boxcars source supports it.
6. Evidence-derived privacy-safe positive vectors and synthetic negative vectors.
7. No hidden property-loop continuation: success returns exactly after one value.

## Shared net10 vector candidate

R3.17I proves the net10 prefix rule on observed outcomes:

```text
read low 4 bits
candidate = low + 16
if candidate < 22:
  consume one discriminator bit and select low or candidate
else:
  select low without discriminator
component_width = selected_size_bits + 2
read x/y/z with exactly component_width each
semantic float component = signed/decompressed integer / 100
```

Contract admission must explicitly bound accepted `selected_size_bits` to evidence-supported sets. Across K3 evidence the union is 0..19. `20` and `21` remain unobserved and must not silently become admitted.

Per-field evidence sets to preserve:

```text
standalone Location           0,7,8,14,15,16,17
RigidBody awake location      10..19
RigidBody sleeping location   13,16,17,18,19
RigidBody linear velocity     0..18
RigidBody angular velocity    0..15
```

The contract must decide whether to encode those per-field sets directly or prove that a narrower shared primitive plus field-level guards preserves the same admitted surface. It must not broaden to unobserved values by cross-product convenience.

## Location candidate

```text
context       version 868.32 / net10 / RL223 false or true
wire          one admitted net10 vector
end bit       exactly after z component
```

Only the seven R3.17I standalone vector structural shapes are candidates.

## RigidBody candidate

```text
context       version 868.32 / net10 / RL223 false or true
wire          sleeping bit
              admitted location vector
              56-bit quaternion
              if awake: admitted linear vector + admitted angular vector
sleeping      no velocity payload
awake         both velocity payloads required
end bit       exact after quaternion when sleeping; exact after angular vector when awake
```

The 48-bit legacy rotation path is unobserved and must remain rejected. Size/header outcomes outside the R3.17I per-subfield sets remain rejected.

## ReplicatedBoost candidate

```text
context       version 868.32 / net10 / RL223 true only
wire          grant_count:u8
              boost_amount:u8
              unused1:u8
              unused2:u8
width         exactly 32 bits
```

RL223=false is unobserved for this tag and remains closed unless separately evidenced.

## PickupNew candidate

```text
context       version 868.32 / net10 / RL223 false or true
None          presence=false + picked_up:u8 = 9 bits
SomeI32       presence=true + actor_ref:i32 + picked_up:u8 = 41 bits
```

No other branch shape is admitted.

## Negative/malformed contract requirements

The contract must specify fail-closed behavior for at least:

```text
wrong replay major/minor or net_version
unobserved vector selected_size_bits 20/21
truncated 4-bit vector prefix
truncated discriminator when required
truncated x/y/z component
RigidBody truncated sleeping/location/quaternion
RigidBody awake missing either velocity vector
RigidBody legacy quat48 attempt in current lane
ReplicatedBoost wrong RL223 context or truncation at each byte boundary
PickupNew truncation after presence, partial i32, or partial picked_up byte
extra bits are not consumed as a second property
```

## Required contract gates

```text
R3.17I authority identities frozen          PASS
all admitted forms trace to evidence        100%
unobserved forms remain explicit rejects    PASS
atomic failure semantics defined            PASS
exact end-bit semantics defined             PASS
privacy-safe positive vector plan           PASS
synthetic negative vector plan               PASS
production Rust mutation                     0
Cargo / fixture / corpus mutation            0
```

## Outcome rules

- **Outcome A:** exact evidence-supported K3 contract is frozen with no capability widening; open R3.17K implementation.
- **Outcome B:** evidence cannot support a required contract distinction; return to targeted evidence only.
- **Outcome C:** contract modeling contradicts R3.17I evidence or current production primitives; stop and repair before implementation.

## Hard stop

Do not implement a native K3 decoder in R3.17J. Do not continue to a second property, actor, frame or lifecycle state. K4, raw state, events, replay slicing, skills, runtime and export remain closed.

## Next pass

Only on Outcome A open `R3.17K — direct native K3 decoder implementation for contract-admitted variants only`.
'''
Path("docs/continuity/MIMIR_R3_17J_EXECUTION_SPEC.md").write_text(spec, encoding="utf-8", newline="\n")

print("R3_17I_CONTINUITY_SYNC=PASS")
