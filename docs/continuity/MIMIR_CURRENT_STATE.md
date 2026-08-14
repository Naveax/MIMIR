# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `9bfa837c69c4751f70ca63a17c65f0f89877ff32`
**Production milestone:** `R3.17G — direct native evidence-admitted K2 decoder implementation`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Completed K3 evidence:** `R3.17I — Outcome A / 47 of 47 / 1699169 occurrences / 1950 exact groups`
**Completed K3 contract:** `R3.17J — Outcome A / 1950 exact groups / zero cross-product widening`
**Current exact pass:** `R3.17K — direct native K3 decoder implementation`

## 1. Truthful production boundary

Production remains exactly R3.17G. R3.17J froze the K3 contract but did not implement it. MIMIR may still decode only one already-resolved K1 scalar or one R3.17F-admitted K2 payload and stop at the exact end bit.

```text
production SHA               9bfa837c69c4751f70ca63a17c65f0f89877ff32
production source blob       7288238cfb5338653552435be6af41f0dd7a4e85
R3.17I authority head        8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
R3.17I run/job               31812804986 / 94807233173 SUCCESS
R3.17I artifact              9223916983
R3.17I artifact digest       sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
R3.17J groups SHA256         04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b
R3.17J allowlist SHA256      9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
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
