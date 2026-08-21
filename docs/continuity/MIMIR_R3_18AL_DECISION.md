# MIMIR R3.18AL — Published R3.18AK Following-Header Differential Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL**
**Production mutation:** none
**Canonical production:** `f20f529e3ada6e9a671ea91e5676a17a00770145` / `98c675811cca4e4d7f0122c762f371548c9266c2`

## Decision

R3.18AL closes Outcome A. The published R3.18AK post-AG following-header composition was validated on exactly the immutable R3.18AI 47-row lane with witness reselection 0. Published R3.18AK matched the frozen R3.18AI header on 47/47 rows and matched the direct stateless native header on 47/47 rows through exactly `payload_start`. The complete R3.18AJ exact-context family reconstructed as 17/17 contexts with multiplicity 47/47, all `Int`, and mismatch zero.

R3.18AL consumed zero following-payload bits and zero second-later-control bits. It changes no production source and admits no payload production, later control, generalized property loop/cursor, actor/frame/lifecycle/raw-state/event/slice/skill/counterfactual/runtime/export widening.

## Exact authority

```text
canonical base main/tree             02233c8125e658513dcb068370c48b1e8f15a01c / fc9293d821dd3e6e269763c3c0ab091428c29490
production SHA/tree                  f20f529e3ada6e9a671ea91e5676a17a00770145 / 98c675811cca4e4d7f0122c762f371548c9266c2
R3.18AJ contract SHA256              cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AI artifact                     9424764320 / sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5
evidence head/tree                   06b8570a25a989651fc800a4ded900ce5e2f3dbe / 2753baa23be49a819cfceb333977473864a1b02b
authority run/job                    32469442033 / 96732952709 SUCCESS
same-head normal CI                  32470066272 / 96734795022 SUCCESS
validation PR                        #130 closed unmerged
artifact                             9442034802 / 14650 bytes
artifact digest / ZIP SHA256         sha256:5fcb8f796ba365193698d5d27e2e7dc0e8c221dd42d7a901e956522b7ca1f639
continuity builder                   32472027614 / 96740627165
```

The downloaded artifact ZIP SHA-256 equals the GitHub artifact digest exactly. Its internal SHA-256 manifest verifies every payload file.

## Frozen result

```text
frozen rows                          47/47
published R3.18AK exact              47/47
direct stateless-header exact        47/47
R3.18AJ exact contexts               17/17
R3.18AJ exact multiplicity           47/47
observed tags                        Int=47
published/native/oracle mismatch     0
witness reselection                  0
following payload bits consumed      0
second later control bits consumed   0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Negative controls

Repeatability, bit-exact header truncation, corrupt AG control, corrupt prior/wrong actor, unresolved lookup, wrong exact version/context and post-payload-start poison invariance pass on 47/47 rows. Permanent R3.18AK focused regressions retain Cartesian `(60,5,68,Int,868,32,10)`, fabricated `(60,5,39,Int,868,32,10)`, and old-R3.18Z-only `(60,5,34,ActiveActor,868,32,10)` rejection. R3.18Z/R3.18P cross-boundary inheritance remains rejected.

## Superseded attempts

A duplicate evidence lane at `760705d1cdaef8cc752672008573b32df00adb29` failed only in temporary probe compilation because its expected `prop_id_bits` value was typed as `u32` instead of the production header's `u8`. It is not authority and was not rerun. The admitted authority is the independent successful head `06b8570a25a989651fc800a4ded900ce5e2f3dbe` above. A later helper-only mutation of that evidence branch is also not evidence authority; the admitted head remains immutable by exact SHA.

## Hard stop

Production remains R3.18AK. Post-AK following-payload **production**, another property-control bit, repeated/generalized property loops/cursors, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior remain closed.

## Next gate

R3.18AM is a separate read-only post-AK following-payload evidence pass on exactly the same 47 rows. It begins exactly at each validated R3.18AK `payload_start`, independently determines the observed payload width/value semantics for the R3.18AJ-admitted `Int` headers against pinned Boxcars and existing narrow native payload machinery, stops at exactly one payload end, and consumes zero bits of another property-control boundary. The 32-bit Int layout may be tested as a hypothesis from prior evidence but is not inherited by assumption at this boundary.
