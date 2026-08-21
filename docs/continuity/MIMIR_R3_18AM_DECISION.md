# MIMIR R3.18AM — Post-AK One Following-Payload Evidence Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / READ-ONLY PAYLOAD EVIDENCE**
**Production mutation:** none
**Canonical production:** `f20f529e3ada6e9a671ea91e5676a17a00770145` / `98c675811cca4e4d7f0122c762f371548c9266c2`

## Decision

R3.18AM closes Outcome A. On exactly the immutable 47-row R3.18AI/R3.18AL lane, the published R3.18AK boundary was reconstructed exactly and one following payload was observed independently with pinned Boxcars plus the existing native primitive scalar decoder. All 47 headers were `Int`; all 47 payloads were exactly 32 bits; privacy-safe semantic values ranged from 1 through 415. Native and oracle start/end/width/value matched on 47/47 rows with mismatch zero and witness reselection zero.

This pass consumes zero bits of the following property-control boundary. It is evidence only and does not itself publish a post-AK payload API.

## Exact authority

```text
canonical parent main/tree           fec9dca3cb8366108245788fc9a2b24a0c99fe94 / 3bf5f68ec7df5565f78f89fd4bc2254f2a64e010
production SHA/tree                  f20f529e3ada6e9a671ea91e5676a17a00770145 / 98c675811cca4e4d7f0122c762f371548c9266c2
R3.18AJ contract SHA256              cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AL authority head               06b8570a25a989651fc800a4ded900ce5e2f3dbe
evidence head/tree                   842b94ed4c4e57323433585fea48116ecf18989b / 486d0a0f3833dcb8872f062ae1927c9aefde87ba
authority run/job                    32473716883 / 96745647750 SUCCESS
same-head normal CI                  32474038136 / 96746590106 SUCCESS
validation PR                        #135 closed unmerged
artifact                             9443581172 / 14827 bytes
artifact digest / ZIP SHA256         sha256:2f65de5207bd96787fd7d1527a55991f08d5da614a0ddfce22a7aa267968e3c8
```

The downloaded artifact ZIP SHA-256 equals the GitHub artifact digest exactly. Its internal SHA-256 manifest verifies all 11 payload files.

## Frozen result

```text
frozen rows                          47/47
published R3.18AK exact              47/47
observed tags                        Int=47
observed payload width               32 bits on 47/47
semantic Int range                   1..415
native/oracle mismatch               0
witness reselection                  0
another property-control bits read   0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Negative controls

Repeatability, exact payload truncation, wrong-tag boundary guard, wrong-payload-start boundary guard, wrong exact version/context, corrupt AG control, corrupt prior, and post-payload-end poison invariance pass on 47/47 rows. Earlier R3.18AC/R3.18S payload contracts were explicitly not inherited as authority.

## Superseded attempts

Run `32473299304` on head `72184f77f3016ac38a41ca5bb11a9b44f2f1b16a` stopped before payload measurement because a temporary Boxcars instrumentation insertion marker did not match. Run `32473502712` on head `8917d4bfe69418f74f03b5611bf91670effad827` reached the independent 47/47 Boxcars payload oracle and then stopped because Rust 1.85 minimal lacked the rustfmt component required by the temporary native probe. Neither SHA was rerun. The immutable authority is `842b94ed4c4e57323433585fea48116ecf18989b`.

## Hard stop

Production remains R3.18AK until R3.18AN is separately implemented, validated and published. Another property-control bit, alternate payload tags/layouts, repeated/generalized property loops/cursors, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior remain closed.

## Next gate

R3.18AN is a bounded production pass. It may compose exactly one post-AK `Int/32` payload only after validating/recomputing the supplied R3.18AK/AJ header authority, must start exactly at `payload_start`, stop exactly at the 32-bit payload end, and consume zero bits of the following property-control boundary.
