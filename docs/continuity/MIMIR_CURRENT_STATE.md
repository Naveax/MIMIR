# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `7390e3b145372252caaa8fa1fe3e0cd13b83336c`
**Production milestone:** `R3.17K — direct native exact-contract K3 decoder implementation`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Completed K3 evidence:** `R3.17I — Outcome A / 47 of 47 / 1699169 occurrences / 1950 exact groups`
**Completed K3 contract:** `R3.17J — Outcome A / 1950 exact groups / zero cross-product widening`
**Completed K3 production:** `R3.17K — Outcome A / 1950 of 1950 exact groups + exhaustive structural acceptance`
**Current exact pass:** `R3.17L — native K3 real-replay differential audit`

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

## 3. R3.17L exact next pass

R3.17L is read-only. Regenerate real K3 witnesses ephemerally from the frozen 47-replay R3.17I lane using pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`, cover at least one real occurrence for every one of the 1,950 admitted exact groups, then compare native tag/variant, context, exact bit start/end/width, structural codec metadata and semantic values against the oracle.

A mismatch is not fixed inside R3.17L. It produces Outcome C and sends the project back to corrective evidence/contract/implementation work. Durable audit output remains privacy-safe; raw real payload bytes stay ephemeral.

## 4. Still closed

```text
K4 payload decode
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
