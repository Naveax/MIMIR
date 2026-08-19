# MIMIR R3.18AA — Bounded Post-W Following-Header Production Decision

**Date:** 2026-08-18
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production SHA:** `9392240c49f95766c214afee9865fed4155a87a4`
**Production tree:** `968520d480f78c528086e4e31b2ce307f4f8d232`
**Production parent:** `ac24d29edeacd04152afe318e25ae296385159c3`
**R3.18Z contract SHA-256:** `81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9`

## Decision

R3.18AA is admitted Outcome A. Production now composes exactly one existing-actor property header after a valid published R3.18W true control, reuses the existing stateless property-header primitive, requires complete seven-field membership in the boundary-specific R3.18Z contract, and stops exactly at that header's `payload_start`.

The production API does not decode the following payload, does not consume another property-control bit, and does not expose a repeatable/generalized property cursor or loop. The earlier R3.18P contract is not inherited at this boundary.

## Exact authority

```text
pre-pass canonical main             ac24d29edeacd04152afe318e25ae296385159c3
production SHA/tree                 9392240c49f95766c214afee9865fed4155a87a4 / 968520d480f78c528086e4e31b2ce307f4f8d232
production lib.rs blob              46523f47f94231362b60f8aee038e943e41c7972
R3.18AA focused test blob           7df8f84af37d771b12da1334bd195634e4cc6a54
R3.18Z contract SHA-256             81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18Y evidence head                413d6c24f8f390a57c21ed345f3f868c263f413c
R3.18Y authority                    32076198677/95529856476 SUCCESS
R3.18Y artifact                     9303584468 / sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29
clean builder authority             32142503228/95728286216 SUCCESS
exact clean-candidate CI            32143161309/95730448274 SUCCESS
published-main CI                   32143631391/95731995111 SUCCESS
published-run receipt helper        32143701901/95732221348 SUCCESS
published-run receipt artifact      9326934597 / sha256:4958371c58929cfd6a723787bedb4ef9d7f626f95e1533218e02208fdc6313eb
```

The production commit is the direct child of the pre-pass canonical main and was published by a fresh-main `force=false` fast-forward. Validation PR #38 and receipt PR #39 were closed without merge.

## Admitted production behavior

```text
input prior                         one valid R3.18T following-payload result
revalidated boundary                one published R3.18W true control
header decoder                      existing stateless existing-actor property-header primitive
membership                          exact full R3.18Z seven-field tuple only
admitted contexts                   18
frozen multiplicity authority       47
representative tags tested          ActiveActor / Int / UniqueId
stop                                exactly following_header.payload_start_bit
following payload bits consumed     0
another control bits consumed       0
property loop/cursor                none
```

## Validation

Focused R3.18AA tests passed 5/5. Real frozen R3.18Y-derived ActiveActor, Int and UniqueId representatives matched their exact W/header/payload-start coordinates. Repeatability and post-payload poison invariance passed. Truncation and wrong-actor cases fail closed. Wrong version, fabricated Cartesian membership, and the R3.18P-valid but R3.18Z-absent `(60,5,102,Boolean,868,32,10)` tuple are rejected.

The full repository verifier, workspace tests/checks and clippy passed both in the clean-builder authority and on the exact clean candidate. Published-main CI also passed on the exact production SHA.

## Clean scope

The clean production commit changes exactly:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_18aa_post_w_following_header.rs`

Cargo manifests/lockfile, docs, workflows, fixtures, corpus and support lanes are unchanged in the production commit.

## Hard stop

R3.18AA admits no post-W following payload, no later property-control bit, no repeated/generalized property loop or public cursor, no next actor/frame/lifecycle behavior, no raw-state or event materialization, no replay slicing, no skill mining, no counterfactual execution and no runtime/export widening.

## Next gate

R3.18AB is a separate read-only published-production differential. It must reuse the immutable R3.18Y 47-row witness lane with zero reselection, invoke the published R3.18AA API, require exact equality through `payload_start`, preserve R3.18Z exact membership and prove payload/another-control consumption remains `0/0`. R3.18AB may not change production.
