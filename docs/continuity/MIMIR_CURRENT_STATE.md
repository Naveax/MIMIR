# MIMIR — Current Canonical State

**Continuity date:** 2026-08-15
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `7390e3b145372252caaa8fa1fe3e0cd13b83336c`
**Production milestone:** `R3.17K — direct native exact-contract K3 decoder implementation`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Completed K3 evidence:** `R3.17I — Outcome A / 47 of 47 / 1699169 occurrences / 1950 exact groups`
**Completed K3 contract:** `R3.17J — Outcome A / 1950 exact groups / zero cross-product widening`
**Completed K3 production:** `R3.17K — Outcome A / 1950 of 1950 exact groups + exhaustive structural acceptance`
**Completed K3 differential:** `R3.17L — Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch`
**Current exact pass:** `R3.17M — K4 gameplay-structured wire-format evidence`

## 1. Truthful production boundary

Production is now R3.17K. MIMIR may decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, or one R3.17J-admitted K3 payload and stop at the exact one-value end bit. K3 is limited to `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` with exact structural/context allowlist membership.

```text
production SHA               7390e3b145372252caaa8fa1fe3e0cd13b83336c
production tree              eebe4e21de77a43b5d9d43a34a0bfb08e06bab02
production parent            b0c0a4665e72da012d6447ca647db526a3da0020
lib.rs blob                  28d213f831c8968e6756a6ccea2cd7aa6cdbdfba
k3 groups blob               da545a7144fefabab7f5be4f07fde71311065293
focused K3 test blob         4d1434cc0e59a6e5c72a8404c102a87d71b8b223
R3.17J allowlist SHA256      9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
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

## 3. R3.17L differential closure

```text
authority head                0febcde7b312b6724e86ba156c700b41cf0562b7
authority run/job             31871353806 / 94980384463 SUCCESS
exact-head normal CI          31871353749 / 94980384205 SUCCESS
artifact                      9243555556
artifact digest               sha256:514580727df642ebde04d69824402db46ed48ff66755d4b17c0db6e69ac5eb3d
replay identity               47/47
Boxcars oracle decode         47/47
regenerated K3 occurrences    1699169
real group coverage           1950/1950
native decode                 1950/1950
variant/context/range/code    1950/1950 exact
semantic value                1950/1950 exact
mismatch                      0
max quaternion abs diff       5.960464477539063e-08
negative controls             PASS / 7 tests
privacy                       PASS
production/Cargo/fixture/
corpus/support mutation       0/0/0/0/0
outcome                       A
```

The frozen quaternion tolerance was `1e-5` only for the reconstructed largest component; the observed maximum was far below it. All vector components and non-largest quaternion components were compared by exact f32 bit identity.

## 4. R3.17M exact next pass

R3.17M is read-only K4 evidence over the same frozen 47-replay lane. Instrument pinned Boxcars for `CamSettings`, `TeamPaint`, `TeamLoadout`, `ClubColors`, `Reservation`, `StatEvent`, `PlayerHistoryKey`, `DemolishFx`, `DemolishExtended`, `ExtendedExplosion`, and `LoadoutsOnline`; classify every observed wire shape/context and persist deterministic privacy-safe witnesses. A zero-occurrence tag remains unadmitted.

Production K4 decoding remains closed. If R3.17M closes Outcome A, K4 contract admission is a separate pass before any native implementation. R3.18 property-loop work remains closed until the R3.17 attribute-family dependency is explicitly satisfied.

## 5. Still closed

```text
K4 contract / native payload decode
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
