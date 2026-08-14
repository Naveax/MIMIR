# MIMIR R3.17K — Direct Native K3 Decoder Implementation Execution Spec

**Pass type:** production implementation
**Contract authority:** R3.17J Outcome A
**Evidence authority:** R3.17I Outcome A
**Current production authority:** R3.17G

## Goal

Implement a direct, dependency-free, one-value native K3 decoder for exactly the R3.17J-admitted `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` structural/context groups. No property-loop continuation or actor/frame lifecycle work is part of this pass.

## Frozen identities

```text
continuity base before J     77028734ba33818c6ee7cac65f5f9e75aebca0e0
native production SHA        9bfa837c69c4751f70ca63a17c65f0f89877ff32
native source blob           7288238cfb5338653552435be6af41f0dd7a4e85
R3.17I evidence head         8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
R3.17I run/job               31812804986 / 94807233173 SUCCESS
R3.17I artifact              9223916983
R3.17I artifact digest       sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
R3.17I groups SHA256         04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b
R3.17J allowlist SHA256      9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before implementation, fetch fresh `main`, read the admitted R3.17J decision and allowlist, and record the exact J continuity SHA. If fresh source changed after `9bfa837c69c4751f70ca63a17c65f0f89877ff32`, stop and reconstruct production truth before widening.

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
