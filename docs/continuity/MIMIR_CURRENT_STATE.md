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
**Completed K4 evidence:** `R3.17M — Outcome A / 39463 occurrences / 161 exact structural-context groups / all 11 tags observed`
**Completed K4 contract:** `R3.17N — Outcome A / 161/161 byte-identical groups / zero cross-product widening`
**Current exact pass:** `R3.17O — direct native exact-contract K4 decoder implementation`

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

## 4. R3.17M K4 evidence closure

```text
authority head                a50f09857f36ac52cec30b4bf3efbde9e15bb564
authority run/job             31881779861 / 95005282281 SUCCESS
exact-head normal CI          31881779862 / 95005282149 SUCCESS
artifact                      9246249473
artifact digest               sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
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

## 5. R3.17N K4 contract closure

```text
contract authority head       086ec251aea4eea9881cfc224bfac2d09596269f
authority run/job             31883205829 / 95008550716 SUCCESS
clean contract main           c8ebb872e510574bb69ab28c719f415ece8b7665
clean contract tree           61e36d40e6af3853a887e840b22f759dda26ed75
exact candidate CI            31883438754 / 95009080782 SUCCESS
published Knowledge Archive   31883625387 / 95009532717 SUCCESS
published normal CI           31883625362 / 95009532734 SUCCESS
admitted groups               161/161 byte-identical
group SHA256                  80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
group blob                    b5fa6aaa729772ab3d113703952effe2346c9866
contract blob                 76deabf8241b419ca224645106d2a19b041e20f8
cross-product widening        0
atomic failure                PASS
exact one-value end           PASS
production/Cargo/fixture/
corpus/support mutation       0/0/0/0/0
outcome                       A
```

R3.17N admits the K4 contract only; production still cannot decode K4. Exact tuple membership remains mandatory, especially for Reservation and nested LoadoutsOnline shapes.

## 6. R3.17O exact next pass

Implement the direct native K4 one-value decoder for exactly the 161 R3.17N groups. Require 161/161 positive coverage, independent allowlist equality, zero cross-product widening, negative/malformed coverage, atomic failure, exact end-bit semantics, full repository validation and a clean `crates/mimir-replay`-only production diff. Cargo, fixtures, corpus and support lane remain unchanged.

R3.17O must not perform its own real-replay differential audit. That is a separate R3.17P pass after implementation Outcome A. R3.18 remains closed.

## 7. Still closed

```text
native K4 payload decode (until R3.17O closes)
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
