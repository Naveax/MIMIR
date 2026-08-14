#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path

BASE_MAIN = "77028734ba33818c6ee7cac65f5f9e75aebca0e0"
PRODUCTION_SHA = "9bfa837c69c4751f70ca63a17c65f0f89877ff32"
PRODUCTION_BLOB = "7288238cfb5338653552435be6af41f0dd7a4e85"
EVIDENCE_HEAD = "8962ddc6bd77b5469fa7ebc93c95334e5725a8ab"
EVIDENCE_RUN = 31812804986
EVIDENCE_JOB = 94807233173
EVIDENCE_EXACT_CI = 31812804992
EVIDENCE_EXACT_CI_JOB = 94807233091
ARTIFACT_ID = 9223916983
ARTIFACT_DIGEST = "sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b"
GROUPS_SHA256 = "04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b"
PINNED_BOXCARS = "c70e77df7af81b436cb545d070bb90c82f562d0b"
ALLOWLIST_SHA256 = "9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911"

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def write(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8", newline="\n")

def parse_groups(path: Path):
    raw = path.read_bytes()
    if sha256_bytes(raw) != GROUPS_SHA256:
        raise SystemExit(f"groups SHA mismatch: {sha256_bytes(raw)}")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    if len(rows) != 1950:
        raise SystemExit(f"expected 1950 groups, got {len(rows)}")
    tags = {"Location", "RigidBody", "ReplicatedBoost", "PickupNew"}
    for row in rows:
        if row["attribute_tag"] not in tags:
            raise SystemExit(f"unexpected tag: {row['attribute_tag']}")
        if (row["version_major"], row["version_minor"], row["net_version"]) != (868, 32, 10):
            raise SystemExit(f"unexpected version context: {row}")
    return rows

AWAKE = re.compile(r"RigidBody:awake:location:sb(\d+):h\d+:cw\d+:quat56:linear:sb(\d+):h\d+:cw\d+:angular:sb(\d+):h\d+:cw\d+")
SLEEPING = re.compile(r"RigidBody:sleeping:location:sb(\d+):h\d+:cw\d+:quat56")

def derive_allowlist(rows):
    loc, rigid, pickup, boost = [], [], [], []
    occurrence = {}
    for row in rows:
        tag = row["attribute_tag"]
        ctx = 1 if row["is_rl_223"] else 0
        occurrence[tag] = occurrence.get(tag, 0) + int(row["occurrences"])
        shape = row["shape"]
        if tag == "Location":
            m = re.search(r":sb(\d+):", shape)
            if not m:
                raise SystemExit(f"bad Location shape: {shape}")
            loc.append((ctx << 5) | int(m.group(1)))
        elif tag == "RigidBody":
            if ":awake:" in shape:
                m = AWAKE.fullmatch(shape)
                if not m:
                    raise SystemExit(f"bad awake RigidBody shape: {shape}")
                location, linear, angular = map(int, m.groups())
                code = (ctx << 16) | (location << 10) | (linear << 5) | angular
            else:
                m = SLEEPING.fullmatch(shape)
                if not m:
                    raise SystemExit(f"bad sleeping RigidBody shape: {shape}")
                location = int(m.group(1))
                code = (ctx << 16) | (1 << 15) | (location << 10) | (31 << 5) | 31
            rigid.append(code)
        elif tag == "PickupNew":
            some = 1 if shape.endswith("SomeI32") else 0
            if not (shape.endswith("SomeI32") or shape.endswith("None")):
                raise SystemExit(f"bad PickupNew shape: {shape}")
            pickup.append((ctx << 1) | some)
        elif tag == "ReplicatedBoost":
            if shape != "ReplicatedBoost:u8x4":
                raise SystemExit(f"bad ReplicatedBoost shape: {shape}")
            boost.append(ctx)

    expected_occ = {"Location": 26734, "RigidBody": 1550254, "ReplicatedBoost": 11058, "PickupNew": 111123}
    if occurrence != expected_occ:
        raise SystemExit(f"occurrence mismatch: {occurrence}")
    checks = [("Location", loc, 11), ("RigidBody", rigid, 1934), ("PickupNew", pickup, 4), ("ReplicatedBoost", boost, 1)]
    for name, values, count in checks:
        if len(values) != count or len(set(values)) != count:
            raise SystemExit(f"{name} packed-code mismatch: {len(values)} / {len(set(values))}")

    allow = {
        "schema_version": 1,
        "source_evidence": {"pass": "R3.17I", "groups_jsonl_sha256": GROUPS_SHA256, "artifact_digest": ARTIFACT_DIGEST},
        "context": {"version_major": 868, "version_minor": 32, "net_version": 10},
        "packing": {
            "location": "(rl223_bit << 5) | selected_size_bits",
            "rigid_body": "(rl223_bit << 16) | (sleeping_bit << 15) | (location_size_bits << 10) | (linear_size_or_31 << 5) | angular_size_or_31; sleeping uses 31 sentinels for both velocities",
            "pickup_new": "(rl223_bit << 1) | some_i32_bit",
            "replicated_boost": "rl223_bit",
        },
        "allowed": {"location_codes": sorted(loc), "rigid_body_codes": sorted(rigid), "pickup_new_codes": sorted(pickup), "replicated_boost_codes": sorted(boost)},
    }
    rendered = json.dumps(allow, indent=2, sort_keys=True) + "\n"
    digest = sha256_bytes(rendered.encode("utf-8"))
    if digest != ALLOWLIST_SHA256:
        raise SystemExit(f"allowlist SHA mismatch: {digest}")
    return rendered

def decision_text():
    return f'''# MIMIR — R3.17J K3 Evidence-Supported Contract Admission Decision

**Date:** 2026-08-14
**Pass:** `R3.17J — K3 evidence-supported contract admission`
**Outcome:** **A — ADMITTED / COMPLETE**
**Production Rust changed:** **NO**

## Frozen authority

```text
continuity base               {BASE_MAIN}
native production SHA         {PRODUCTION_SHA}
native source blob            {PRODUCTION_BLOB}
R3.17I evidence head          {EVIDENCE_HEAD}
R3.17I authority run/job      {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.17I exact-head CI          {EVIDENCE_EXACT_CI} / {EVIDENCE_EXACT_CI_JOB} SUCCESS
R3.17I artifact               {ARTIFACT_ID}
R3.17I artifact digest        {ARTIFACT_DIGEST}
R3.17I groups SHA256          {GROUPS_SHA256}
pinned Boxcars SHA            {PINNED_BOXCARS}
supported replay lane         47
```

R3.17J is contract-only. The pinned oracle remains evidence, not a production dependency.

## Exact admitted context

A future K3 entry point must use an explicit caller-resolved context containing:

```text
version_major = 868
version_minor = 32
net_version   = 10
is_rl_223     = caller-resolved bool
```

Any other major, minor or net version is `unadmitted-context`. `is_rl_223` acceptance remains tag/shape-specific through the exact structural allowlist. The K3 contract is intentionally separate from the existing K2 context/API so admitting K3 cannot silently widen K2.

## Common one-value semantics

```text
bit order                 LSB-first
alignment                 unaligned payload start allowed
input                     network bytes + payload_start_bit + resolved tag + K3 context
success                   exactly one K3 value
payload_end_bit           first bit after that value
payload_width             payload_end_bit - payload_start_bit
trailing bits             left untouched; never interpreted as another property
failure                    no partial value escapes
cursor semantics          rollback to payload_start_bit on every failure
arithmetic                checked offsets/widths only
```

Minimum error classes:

```text
invalid-start
insufficient-bits
unadmitted-context
unadmitted-k3-shape
invalid-k3-value
unsupported-k3-tag
```

## Shared net10 vector wire primitive

For the current net10 lane:

```text
low = read 4 LSB-first bits
candidate = low + 16
if candidate < 22:
    discriminator = read 1 bit
    selected_size_bits = candidate if discriminator else low
else:
    selected_size_bits = low
component_width = selected_size_bits + 2
bias = 1 << (selected_size_bits + 1)
raw_x = read component_width bits
raw_y = read component_width bits
raw_z = read component_width bits
signed_component = raw_component - bias
semantic_component = f32(signed_component) / 100.0
```

`selected_size_bits` 20 and 21 remain unadmitted. More importantly, the union `0..19` is **not** a global acceptance range. A decoded vector shape is admitted only when the enclosing tag/context structural key is present in `MIMIR_R3_17J_K3_ADMITTED_GROUPS.json`.

This prevents cross-product widening. R3.17I observed 1,169 unique RigidBody structural shapes but only 1,934 exact RL223-context groups; a field-wise union would admit combinations never seen in evidence.

## Durable exact structural allowlist

Canonical file: `docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json`

```text
source R3.17I groups rows      1,950
Location exact groups            11
RigidBody exact groups         1,934
PickupNew exact groups             4
ReplicatedBoost exact groups       1
allowlist SHA256               {ALLOWLIST_SHA256}
```

Packing is collision-free over the admitted domains:

```text
Location:
  (rl223_bit << 5) | selected_size_bits
RigidBody:
  (rl223_bit << 16) | (sleeping_bit << 15) | (location_size_bits << 10)
  | (linear_size_or_31 << 5) | angular_size_or_31
  sleeping uses 31 sentinels for linear/angular
PickupNew:
  (rl223_bit << 1) | some_i32_bit
ReplicatedBoost:
  rl223_bit
```

The exact packed-code arrays are contract authority. Implementation may use a source-local sorted constant representation, but it must be regenerated from this canonical JSON and must not broaden it.

## Location contract

Wire: one admitted net10 vector. Success ends exactly after `z`. The exact RL223/shape pairs are the 11 Location codes in the allowlist. Evidence did **not** observe every one of the seven size shapes in both RL223 contexts, so `RL223 false or true` is not by itself sufficient to admit a Location shape.

## RigidBody contract

Wire order:

```text
sleeping:1 bit
location: admitted vector
rotation: exact quat56
if sleeping == false:
    linear_velocity: admitted vector
    angular_velocity: admitted vector
```

Sleeping payloads contain no velocity vectors. Awake payloads require both.

### Quaternion56

Exactly 56 bits:

```text
largest = 2 bits
a_raw   = 18 bits
b_raw   = 18 bits
c_raw   = 18 bits
```

For each 18-bit value `v`:

```text
max_value = 262143
pos_range = f32(v) / f32(max_value)
range = (pos_range - 0.5) * 2.0
unpacked = range * FRAC_1_SQRT_2
```

Let unpacked values be `a,b,c`; `radicand = 1.0 - a*a - b*b - c*c`; `extra = sqrt(radicand)`. `radicand < 0`, non-finite intermediates or a non-finite reconstructed quaternion are `invalid-k3-value`.

Placement by `largest`:

```text
0 => x=extra, y=a,     z=b,     w=c
1 => x=a,     y=extra, z=b,     w=c
2 => x=a,     y=b,     z=extra, w=c
3 => x=a,     y=b,     z=c,     w=extra
```

The legacy 48-bit compressed quaternion is explicitly unadmitted for this lane. After reading an otherwise field-valid RigidBody, construct its exact packed structural key and require membership in the 1,934-code RigidBody allowlist. Missing membership is `unadmitted-k3-shape` and rolls back atomically.

## ReplicatedBoost contract

Only exact context `(868,32,net10,RL223=true)` is admitted.

```text
grant_count:u8
boost_amount:u8
unused1:u8
unused2:u8
```

Exact width: 32 bits. RL223=false is unadmitted.

## PickupNew contract

Both RL223 contexts are evidenced, but only these branches:

```text
presence=false: presence:1 + picked_up:u8 = 9 bits
presence=true:  presence:1 + actor_ref:i32 + picked_up:u8 = 41 bits
```

The exact four context/branch combinations are all present in the allowlist.

## Planned public production surface for R3.17K

R3.17K may add a **separate** K3 one-value API, reusing `ReplayNetworkAttributeTagV1`:

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

The structural codec metadata is retained deliberately so the later differential audit can compare shape as well as semantic values.

## Positive and negative test contract

R3.17K focused tests must synthesize at least one valid payload for **every one of the 1,950 exact structural/context allowlist entries**.

They must also verify fail-closed behavior for wrong major/minor/net version; absent Location context/size pairs; vector size 20/21; vector truncation; every RigidBody candidate structural tuple absent from the allowlist; illicit sleeping velocity continuation; awake missing velocity; quat48; quat56 truncation and invalid reconstruction; ReplicatedBoost RL223=false/truncation; PickupNew truncation; unsupported non-K3 tag; invalid payload start; and trailing-bit non-consumption.

For structural exhaustiveness, tests may enumerate the finite current-lane candidate domain and assert acceptance iff the packed structural key is in the canonical allowlist.

Actual replay payload bytes are not persisted in contract files. R3.17L must regenerate real witness payloads ephemerally from the frozen 47-replay lane and pinned Boxcars, as R3.17H did for K2.

## Required gates

```text
R3.17I identities frozen                   PASS
1950/1950 groups represented               PASS
packed-code uniqueness                     PASS
cross-product widening                     0
unobserved shapes explicit rejects         PASS
atomic failure semantics                   PASS
exact one-value end semantics              PASS
privacy-safe synthetic positive plan       PASS
synthetic negative plan                    PASS
production Rust mutation                   0
Cargo / fixture / corpus mutation          0
```

## Capability consequence

No native K3 capability is created by R3.17J. Production remains R3.17G and may still decode only one admitted K1 scalar or one admitted K2 value.

## Next exact pass

Open `R3.17K — direct native K3 decoder implementation for contract-admitted variants only`.
'''

def k_spec_text():
    return f'''# MIMIR R3.17K — Direct Native K3 Decoder Implementation Execution Spec

**Pass type:** production implementation
**Contract authority:** R3.17J Outcome A
**Evidence authority:** R3.17I Outcome A
**Current production authority:** R3.17G

## Goal

Implement a direct, dependency-free, one-value native K3 decoder for exactly the R3.17J-admitted `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` structural/context groups. No property-loop continuation or actor/frame lifecycle work is part of this pass.

## Frozen identities

```text
continuity base before J     {BASE_MAIN}
native production SHA        {PRODUCTION_SHA}
native source blob           {PRODUCTION_BLOB}
R3.17I evidence head         {EVIDENCE_HEAD}
R3.17I run/job               {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.17I artifact              {ARTIFACT_ID}
R3.17I artifact digest       {ARTIFACT_DIGEST}
R3.17I groups SHA256         {GROUPS_SHA256}
R3.17J allowlist SHA256      {ALLOWLIST_SHA256}
pinned Boxcars SHA           {PINNED_BOXCARS}
```

Before implementation, fetch fresh `main`, read the admitted R3.17J decision and allowlist, and record the exact J continuity SHA. If fresh source changed after `{PRODUCTION_SHA}`, stop and reconstruct production truth before widening.

## Exact production scope

Preferred clean production scope:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/src/k3_admitted_groups.rs
crates/mimir-replay/tests/r3_17k_k3_attribute_decoder.rs
```

`k3_admitted_groups.rs` may contain only deterministic constants/generated lookup helpers corresponding exactly to the canonical R3.17J packed-code arrays. No Cargo dependency is expected or admitted.

## Required API

Add the separate one-value K3 surface frozen by R3.17J: `ReplayNetworkK3DecodeContextV1`, `ReplayNetworkVector3V1`, `ReplayNetworkQuaternion56V1`, `ReplayNetworkRigidBodyV1`, `ReplayNetworkReplicatedBoostV1`, `ReplayNetworkPickupNewV1`, `ReplayNetworkK3ValueV1`, `ReplayNetworkK3DecodeV1`, and `decode_replay_network_k3_v1`. Reuse `ReplayNetworkAttributeTagV1`; do not widen `decode_replay_network_k2_v1`.

## Context gate

Only version `868.32 / net10`. `Location`, `RigidBody`, and `PickupNew` use the exact RL223-context structural allowlist. `ReplicatedBoost` accepts RL223=true only. Every other major/minor/net context fails with `unadmitted-context` before semantic success.

## Vector primitive

Implement the exact R3.17J net10 prefix, discriminator, component-width, bias, signed conversion and `/100.0` semantic mapping. Parsing a vector size supported elsewhere does not admit it for the current tag/field/context.

At minimum: selected size 20/21 rejects; field-level impossible size rejects; full structural key absent from the canonical allowlist rejects. Every rejection rolls the internal cursor back to payload start.

## RigidBody

Implement only sleeping bit + admitted location + quat56 + awake-only admitted linear/angular velocities. No quat48 path. The final structural tuple must be present in the exact 1,934-code allowlist. Do not replace that check with independent field-range membership. Quaternion semantics must follow R3.17J and reject invalid/non-finite reconstruction.

## ReplicatedBoost

Decode four consecutive u8 values in the frozen field order. Exact width 32. RL223=false fails closed.

## PickupNew

Decode presence bit + optional signed i32 actor reference + picked_up u8. Exact widths 9 / 41. Both RL223 contexts are admitted because all four context/branch codes exist in the contract allowlist.

## Error/atomicity requirements

Minimum externally stable categories: `invalid-start`, `insufficient-bits`, `unadmitted-context`, `unadmitted-k3-shape`, `invalid-k3-value`, `unsupported-k3-tag`. Any error returns no K3 value and leaves the conceptual cursor at `payload_start_bit`. Checked arithmetic is mandatory.

## Focused test requirements

Generate at least one privacy-safe synthetic payload for every contract entry: Location 11 + RigidBody 1,934 + PickupNew 4 + ReplicatedBoost 1 = **1,950 exact positives**. Assert variant, width/end, structural codec metadata and semantic values.

Enumerate the finite current-lane structural domain and assert `accepted <=> packed key exists in R3.17J allowlist`. This must reject absent cross-product tuples, not only out-of-range fields.

Cover all R3.17J negative families: context, vector 20/21, truncation boundaries, quat48, invalid quat56, ReplicatedBoost RL223=false, unsupported tag, invalid start and trailing-bit non-consumption.

## Validation gates

```text
cargo fmt --check
cargo test -p mimir-replay --test r3_17k_k3_attribute_decoder
cargo test -p mimir-replay
cargo clippy --workspace --all-targets --all-features -- -D warnings
pwsh -NoProfile -File scripts/verify_repo.ps1
git diff --check
```

Also verify production constants reproduce the R3.17J allowlist counts/hash, Cargo manifests/lock unchanged, fixtures/corpus/support lane unchanged, and only admitted source/test scope changed.

## Clean publication protocol

Implement on a disposable branch rooted in fresh canonical main; validate; reconstruct a clean candidate directly from verified fresh main with only admitted production files; run normal CI on exact candidate SHA; re-read fresh main and require ancestry; publish with `force=false`; require exact published-main CI; only then sync continuity. Temporary workflows/generators never enter the clean production commit.

## Outcome rules

- **Outcome A:** all focused/exhaustive tests and repository gates pass; publish direct K3 decoder.
- **Outcome B:** contract representation/tooling ambiguity only; do not publish until resolved.
- **Outcome C:** contract contradiction, real witness mismatch discovered during implementation, or decoder defect; stop and return to corrective evidence/contract work.

## Hard stop

Even after K3 one-value decode succeeds: no second property, property loop, next actor/frame, actor state mutation, K4, raw-state/event/replay-slice/skill/runtime/export widening.

## Next pass after Outcome A publication

Open `R3.17L — native K3 differential audit against regenerated immutable R3.17I witness identities`.
'''

def current_state_text():
    return f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PRODUCTION_SHA}`
**Production milestone:** `R3.17G — direct native evidence-admitted K2 decoder implementation`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Completed K3 evidence:** `R3.17I — Outcome A / 47 of 47 / 1699169 occurrences / 1950 exact groups`
**Completed K3 contract:** `R3.17J — Outcome A / 1950 exact groups / zero cross-product widening`
**Current exact pass:** `R3.17K — direct native K3 decoder implementation`

## 1. Truthful production boundary

Production remains exactly R3.17G. R3.17J froze the K3 contract but did not implement it. MIMIR may still decode only one already-resolved K1 scalar or one R3.17F-admitted K2 payload and stop at the exact end bit.

```text
production SHA               {PRODUCTION_SHA}
production source blob       {PRODUCTION_BLOB}
R3.17I authority head        {EVIDENCE_HEAD}
R3.17I run/job               {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.17I artifact              {ARTIFACT_ID}
R3.17I artifact digest       {ARTIFACT_DIGEST}
R3.17J groups SHA256         {GROUPS_SHA256}
R3.17J allowlist SHA256      {ALLOWLIST_SHA256}
```

## 2. R3.17J contract closure

```text
contract outcome             A
version context              868.32 / net10 only
durable exact groups         1950 / 1950
Location groups              11
RigidBody groups             1934
PickupNew groups             4
ReplicatedBoost groups       1
cross-product widening       0
vector size 20/21            rejected
RigidBody quat48             rejected
ReplicatedBoost RL223=false  rejected
atomic failure               required
exact one-value end          required
production/Cargo/corpus      0 / 0 / 0 mutations
```

The exact structural/context allowlist is stored in `docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json`. RigidBody acceptance is based on exact context + sleeping + location/linear/angular tuples, not independent field ranges.

## 3. R3.17K exact next pass

Implement a separate direct K3 one-value API for exactly `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`. Preserve the 1,950-entry contract exactly, keep quat56-only RigidBody, fail closed on absent structural tuples, and stop at the first bit after one K3 value.

Focused tests must synthesize all 1,950 admitted groups and exhaustively reject absent current-lane structural combinations. Full `mimir-replay`, workspace clippy, repository verification, exact-candidate CI and published-main CI are mandatory before capability admission.

## 4. Still closed

```text
native K3 until R3.17K is published
K4 payload decode
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
'''

def patch_continue_here():
    p = Path("MIMIR_CONTINUE_HERE.md")
    text = p.read_text(encoding="utf-8")
    text = text.replace("LAST_COMPLETED_CONTRACT_PASS:\n  R3.17F — evidence-supported K2 object/reference/text contract / Outcome A", "LAST_COMPLETED_CONTRACT_PASS:\n  R3.17J — evidence-supported K3 spatial/physics contract / Outcome A / 1950 exact groups", 1)
    text = text.replace("CURRENT_PASS:\n  R3.17J — K3 contract admission for evidence-supported shapes only\n\nCURRENT_PASS_TYPE:\n  contract-only / docs + test-vector planning / NO production Rust change", "CURRENT_PASS:\n  R3.17K — direct native K3 decoder implementation for contract-admitted variants only\n\nCURRENT_PASS_TYPE:\n  production implementation / direct one-value K3 decoder + exhaustive focused tests", 1)
    old = """R3_17J_OPEN_BOUNDARY:
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
  R3.17K — direct native K3 decoder implementation for contract-admitted variants only"""
    new = f"""R3_17J_CONTRACT_CLOSURE:
  Outcome A / docs-only / production Rust unchanged
  exact context: version 868.32 / net10; RL223 acceptance remains tag/shape-specific
  common rule: LSB-first, unaligned allowed, checked arithmetic, atomic failure, exact one-value end
  shared vector codec: net10 4-bit low + conditional discriminator; selected size 20/21 rejected
  exact durable groups: 1950 = Location 11 + RigidBody 1934 + PickupNew 4 + ReplicatedBoost 1
  RigidBody: sleeping bit + location + quat56 + awake-only linear/angular; quat48 rejected
  exact structural allowlist SHA256: {ALLOWLIST_SHA256}
  cross-product widening: 0
  production/Cargo/corpus mutation: 0/0/0

R3_17K_OPEN_BOUNDARY:
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
  R3.17L — native K3 differential audit against regenerated immutable R3.17I witness identities"""
    if old not in text:
        raise SystemExit("MIMIR_CONTINUE_HERE current-pass block not found")
    write(str(p), text.replace(old, new, 1))

def patch_graph():
    p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
    text = p.read_text(encoding="utf-8")
    text = text.replace("R3.17I K3 evidence decision               |\nR3.17J active K3 contract spec            |", "R3.17I K3 evidence decision               |\nR3.17J K3 contract decision               |\nR3.17K active K3 implementation spec      |", 1)
    start = text.index("## Mandatory reading order")
    end = text.index("## Current replay-decoder chain")
    reading = """## Mandatory reading order

1. `MIMIR_CONTINUE_HERE.md`
2. `docs/continuity/MIMIR_CONTINUITY_STATE.json`
3. `docs/continuity/MIMIR_CURRENT_STATE.md`
4. `docs/continuity/MIMIR_R3_17C_DECISION.md`
5. `docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md`
6. `docs/continuity/MIMIR_R3_17D_DECISION.md`
7. `docs/continuity/MIMIR_R3_17E_EXECUTION_SPEC.md`
8. `docs/continuity/MIMIR_R3_17E_DECISION.md`
9. `docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md`
10. `docs/continuity/MIMIR_R3_17F_DECISION.md`
11. `docs/continuity/MIMIR_R3_17G_EXECUTION_SPEC.md`
12. `docs/continuity/MIMIR_R3_17G_DECISION.md`
13. `docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md`
14. `docs/continuity/MIMIR_R3_17H_DECISION.md`
15. `docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md`
16. `docs/continuity/MIMIR_R3_17I_DECISION.md`
17. `docs/continuity/MIMIR_R3_17J_EXECUTION_SPEC.md`
18. `docs/continuity/MIMIR_R3_17J_DECISION.md`
19. `docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json`
20. `docs/continuity/MIMIR_R3_17K_EXECUTION_SPEC.md`
21. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
22. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
23. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
24. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
25. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
26. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
27. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

"""
    text = text[:start] + reading + text[end:]
    text = text.replace(" -> R3.17J K3 evidence-supported contract admission: ACTIVE / CONTRACT-ONLY", f""" -> R3.17J K3 evidence-supported contract admission: OUTCOME A / CLOSED
      exact groups 1950 / cross-product widening 0
      allowlist sha256:{ALLOWLIST_SHA256}
      quat48 + vector20/21 + Boost RL223=false remain rejected
 -> R3.17K direct native K3 decoder implementation: ACTIVE""", 1)
    text = text.replace("R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` without widening production. R3.17J is contract-only and may admit only the observed R3.17I wire/context shapes; native K3 decode remains closed. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.", "R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` without widening production. R3.17J then froze exactly 1,950 structural/context groups with zero cross-product widening. R3.17K is the active production implementation pass; native K3 decode remains closed until that clean implementation is published and validated. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.", 1)
    insertion = f'''\n## R3.17J K3 contract closure\n\n```text\noutcome                     A / contract-only\nversion context             868.32 / net10 only\nexact groups                1950\nLocation                    11\nRigidBody                   1934\nPickupNew                   4\nReplicatedBoost             1\nallowlist SHA256            {ALLOWLIST_SHA256}\nvector size 20/21           rejected\nRigidBody quat48            rejected\nBoost RL223=false           rejected\ncross-product widening      0\nproduction/Cargo/corpus     0/0/0 mutations\nnext                        R3.17K direct native K3 implementation\n```\n\n'''
    marker = "## Authority rule"
    if marker not in text:
        raise SystemExit("graph authority marker not found")
    write(str(p), text.replace(marker, insertion + marker, 1))

def patch_state_json():
    p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    data["current_pass"] = "R3.17K"
    data["current_pass_kind"] = "production implementation for direct one-value K3 decoder over exact R3.17J-admitted groups"
    data["current_pass_goal"] = "Implement Location, RigidBody, ReplicatedBoost and PickupNew direct native K3 decoding for exactly the 1950 R3.17J structural/context groups with exhaustive focused tests."
    data["current_pass_stop_boundary"] = "One K3 value only; no second property, property-loop continuation, next actor/frame, lifecycle, K4, raw-state/event/skill/runtime/export widening; no Cargo/corpus/support-lane change."
    data["last_completed_contract_pass"] = "R3.17J"
    data["r3_17j"] = {"outcome":"A — admitted / complete","production_source_changed":False,"continuity_base_sha":BASE_MAIN,"production_sha":PRODUCTION_SHA,"production_source_blob":PRODUCTION_BLOB,"evidence_pass":"R3.17I","evidence_head":EVIDENCE_HEAD,"evidence_run":EVIDENCE_RUN,"evidence_job":EVIDENCE_JOB,"evidence_artifact_id":ARTIFACT_ID,"evidence_artifact_digest":ARTIFACT_DIGEST,"evidence_groups_sha256":GROUPS_SHA256,"admitted_groups_total":1950,"location_groups":11,"rigid_body_groups":1934,"pickup_new_groups":4,"replicated_boost_groups":1,"allowlist_sha256":ALLOWLIST_SHA256,"version_major":868,"version_minor":32,"net_version":10,"vector_size_20_21_admitted":False,"rigid_body_quat48_admitted":False,"replicated_boost_rl223_false_admitted":False,"cross_product_widening":0,"next_pass":"R3.17K"}
    data["next_files_to_read"] = ["MIMIR_CONTINUE_HERE.md","MIMIR_KNOWLEDGE_GRAPH.md","docs/continuity/MIMIR_CONTINUITY_STATE.json","docs/continuity/MIMIR_CURRENT_STATE.md","docs/continuity/MIMIR_R3_17C_DECISION.md","docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md","docs/continuity/MIMIR_R3_17D_DECISION.md","docs/continuity/MIMIR_R3_17E_EXECUTION_SPEC.md","docs/continuity/MIMIR_R3_17E_DECISION.md","docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md","docs/continuity/MIMIR_R3_17F_DECISION.md","docs/continuity/MIMIR_R3_17G_EXECUTION_SPEC.md","docs/continuity/MIMIR_R3_17G_DECISION.md","docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md","docs/continuity/MIMIR_R3_17H_DECISION.md","docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md","docs/continuity/MIMIR_R3_17I_DECISION.md","docs/continuity/MIMIR_R3_17J_EXECUTION_SPEC.md","docs/continuity/MIMIR_R3_17J_DECISION.md","docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json","docs/continuity/MIMIR_R3_17K_EXECUTION_SPEC.md","docs/continuity/MIMIR_PASS_PROTOCOL.md","docs/continuity/MIMIR_BOUNDARY_LOCKS.md","docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md","MIMIR_ALL_SOURCES_SUPERBOOK.md","docs/chatgpt-archive/SOURCE_REGISTRY.md","docs/chatgpt-archive/VALIDATION_MATRIX.md","docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md"]
    write(str(p), json.dumps(data, indent=2, ensure_ascii=False) + "\n")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--groups", required=True); args = ap.parse_args()
    rows = parse_groups(Path(args.groups)); allow = derive_allowlist(rows)
    write("docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json", allow)
    write("docs/continuity/MIMIR_R3_17J_DECISION.md", decision_text())
    write("docs/continuity/MIMIR_R3_17K_EXECUTION_SPEC.md", k_spec_text())
    write("docs/continuity/MIMIR_CURRENT_STATE.md", current_state_text())
    patch_continue_here(); patch_graph(); patch_state_json()
    exact = ["MIMIR_CONTINUE_HERE.md","MIMIR_KNOWLEDGE_GRAPH.md","docs/continuity/MIMIR_CONTINUITY_STATE.json","docs/continuity/MIMIR_CURRENT_STATE.md","docs/continuity/MIMIR_R3_17J_DECISION.md","docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json","docs/continuity/MIMIR_R3_17K_EXECUTION_SPEC.md"]
    for path in exact:
        if not Path(path).exists(): raise SystemExit(f"missing expected output: {path}")
    print("R3.17J contract patch generated")
    print("allowlist_sha256", sha256_bytes(Path("docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json").read_bytes()))

if __name__ == "__main__":
    main()
