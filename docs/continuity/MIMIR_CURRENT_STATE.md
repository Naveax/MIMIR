# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `9bfa837c69c4751f70ca63a17c65f0f89877ff32`
**Production milestone:** `R3.17G — direct native evidence-admitted K2 decoder implementation`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Completed K3 evidence:** `R3.17I — Outcome A / 47 of 47 / 1699169 occurrences / 1950 exact groups`
**Current exact pass:** `R3.17J — K3 contract admission for evidence-supported shapes only`

## 1. Truthful production boundary

Production remains exactly R3.17G. R3.17I is evidence-only and did not add a K3 decoder. MIMIR may still decode only one already-resolved K1 scalar or one R3.17F-admitted K2 payload and stop at the exact end bit.

```text
production SHA               9bfa837c69c4751f70ca63a17c65f0f89877ff32
production source blob       7288238cfb5338653552435be6af41f0dd7a4e85
R3.17I authority head        8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
R3.17I run/job               31812804986 / 94807233173 SUCCESS
R3.17I exact-head CI         31812804992 / 94807233091 SUCCESS
R3.17I artifact              9223916983
R3.17I artifact digest       sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
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
