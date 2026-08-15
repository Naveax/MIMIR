# MIMIR — R3.17K Direct Native K3 Decoder Implementation Decision

**Date:** 2026-08-14
**Pass:** `R3.17K — direct native K3 decoder implementation for contract-admitted variants only`
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production Rust changed:** **YES, exact three-file admitted scope**

## Frozen authority

```text
pre-K canonical main         b0c0a4665e72da012d6447ca647db526a3da0020
R3.17J allowlist SHA256      9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
production SHA               7390e3b145372252caaa8fa1fe3e0cd13b83336c
production tree              eebe4e21de77a43b5d9d43a34a0bfb08e06bab02
production parent            b0c0a4665e72da012d6447ca647db526a3da0020
lib.rs blob                  28d213f831c8968e6756a6ccea2cd7aa6cdbdfba
k3 groups module blob        da545a7144fefabab7f5be4f07fde71311065293
focused test blob            4d1434cc0e59a6e5c72a8404c102a87d71b8b223
authority run/job            31836699291 / 94884467585 SUCCESS
exact-candidate CI           31837081536 / 94885655480 SUCCESS
published-main CI            31837383875 / 94886588065 SUCCESS
```

The earlier run `31836440825 / 94883657836` is **not authority**. All substantive decode and test gates passed there, but workspace Clippy rejected the synthetic test writer's manual `(len + 7) / 8` ceiling division. The only correction was `.div_ceil(8)` in disposable test-generation tooling; the authoritative run repeated every gate from scratch.

## Exact admitted production scope

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/src/k3_admitted_groups.rs
crates/mimir-replay/tests/r3_17k_k3_attribute_decoder.rs
```

No Cargo manifest/lock, fixture, replay corpus, support lane, workflow or temporary generator entered the clean production commit.

## Implemented surface

R3.17K adds a K3-specific one-value API without widening the existing K2 API:

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

The decoder implements only `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` under replay context `868.32 / net10`, with RL223 and structural acceptance constrained by the exact R3.17J allowlist.

## Contract preservation

Production constants were regenerated from the canonical R3.17J JSON and independently read back against that JSON before tests:

```text
Location                    11
RigidBody                 1934
PickupNew                    4
ReplicatedBoost              1
total                      1950
independent equality       1950/1950 PASS
cross-product widening        0
```

RigidBody acceptance remains final-tuple membership, not a union of independently observed field ranges. Vector size 20/21, quat48, absent structural tuples and ReplicatedBoost RL223=false remain fail-closed.

## Validation result

The focused integration suite synthesized at least one valid payload for every one of the 1,950 admitted exact groups and then exhaustively enumerated the finite current-lane structural domain to assert `accepted <=> canonical allowlist membership`.

Additional negatives cover wrong replay context, invalid start, unsupported tag, vector truncation, invalid quat56 reconstruction, quat48/truncation, sleeping RigidBody trailing velocity-shaped bits, ReplicatedBoost RL223=false, PickupNew truncation and one-value trailing-bit non-consumption.

```text
1950 synthetic positives           PASS
exhaustive structural acceptance   PASS
full mimir-replay suite            PASS
workspace Clippy -D warnings       PASS
full repository verifier           PASS
exact candidate CI                 PASS
published-main CI                  PASS
```

## Capability consequence

Production may now decode **one** already-resolved R3.17J-admitted K3 value in addition to the previously admitted one-value K1/K2 surfaces. This does not admit a second property, property loop, next actor/frame, actor lifecycle mutation, K4, raw-state extraction, event extraction, replay slicing, skill synthesis, runtime integration or export widening.

Synthetic success is not the final K3 oracle check. R3.17L must perform a separate real-replay differential audit before any later parser widening is considered.

## Next exact pass

Open `R3.17L — native K3 differential audit against regenerated real-replay witnesses`.
