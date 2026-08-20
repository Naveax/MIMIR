# MIMIR R3.18AE — Published R3.18AD Ordinal-3 Payload Differential Decision

**Date:** 2026-08-20
**Outcome:** **A — ADMITTED / PUBLISHED API EXACT ON FROZEN LANE**
**Production mutation:** none
**Canonical production:** `ccadbf148381c007890d13d5fe8120866a0f40f9`

## Decision

R3.18AE closes Outcome A. The published R3.18AD API reproduces the immutable R3.18AC ordinal-3 payload authority exactly on all 47 frozen witnesses. The embedded/recomputed R3.18AA/R3.18Z following header matches the frozen AB authority through `payload_start`, and the published payload matches frozen AC plus the direct lower-level native decoder through exactly one payload end. The API stops at that payload end and consumes zero bits from a potential next `property_present` control.

This decision admits only the published differential. It does not admit another control bit, next stream/header/payload, alternate UniqueId layouts, a generalized property loop/cursor, next actor/frame iteration or downstream semantic/runtime behavior.

## Exact authority

```text
canonical main before admission      03c2e431d9e5a31ccfbb0f6bbda8d767be192df2
canonical main tree                  62efc09d2474b35feed5e5ed7f436914010b3f0e
production SHA/tree                  ccadbf148381c007890d13d5fe8120866a0f40f9 / 0882601060d0bb6d37fcc03ae7273dcf50dd0be3
production lib / AD test blobs       1254d5a3d16e7b97b1dee87a8b459514d25749ef / 013ad6da94b866ecaca94cd6420e7568d9b4b5ee
evidence head/tree                   d72b20275f55c44b97d9ec516f2dffbff84a2d6a / a24b6360bf8cace5dfc6fb0ecec4e31f12c986b8
authority run/job                    32282584789 / 96164550815 SUCCESS
same-head normal CI                  32342929705 / 96345500068 SUCCESS
validation PR                        #51 closed unmerged
artifact                             9376466530 / 11057 bytes
artifact digest / ZIP SHA-256        sha256:0eacd0b43929699145a961825de2dbeb6b31342d1cacfa1c68c71cbdd9fc43f4
R3.18AC artifact                     9359697636 / sha256:a6914044dfd8991d74b95caeb3507fb2469175c4458c5b50b55395b8ea67b9df
R3.18Z contract SHA-256              81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
```

The downloaded artifact contains 9 files total: eight evidence payload files plus their SHA-256 manifest. All eight manifest entries verified and the ZIP SHA-256 equals the GitHub artifact digest exactly.

## Admitted evidence

```text
frozen rows                          47/47
published / frozen AB header mismatch 0
published / frozen AC / direct mismatch 0
ActiveActor                          39 rows × 33 bits
Int                                   7 rows × 32 bits
UniqueId                              1 row × 80 bits
UniqueId layout                      system_id=1 / Steam
witness reselection                  0
repeatability                        PASS 47/47
truncation negative                  PASS 47/47
wrong-context negative               PASS 47/47
post-payload poison                  PASS 47/47
non-Z header negative                PASS
lower-level-valid Epic 312-bit UID   PASS / rejected at AD boundary
another-control bits consumed        0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Hard stop

R3.18AE does not authorize reading the bit after the published R3.18AD payload end. Following stream/header/payload decoding, a second later control bit, alternate UniqueId systems/layouts, repeated/generalized property iteration, next actor/frame/lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual execution and runtime/export widening remain closed.

## Next gate

R3.18AF is a separate read-only boundary characterization pass. It may start only at the exact published R3.18AD `stop_bit`, observe exactly one next `property_present` bit on the same immutable 47 witnesses, compare it with pinned Boxcars and an independent evidence-only one-bit read, and stop one bit later. Its false/true distribution must be discovered from evidence rather than assumed.
