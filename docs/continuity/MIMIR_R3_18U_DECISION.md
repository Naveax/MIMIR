# MIMIR R3.18U — Published R3.18T Following-Payload Differential Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / PUBLISHED API EXACT ON FROZEN LANE**
**Production mutation:** none
**Canonical production:** `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b`

## Decision

R3.18U closes Outcome A. The published R3.18T API reproduces the immutable R3.18S one-following-payload authority exactly on all 47 frozen witnesses and all 18 exact R3.18P structural/version contexts. Header identity, payload boundary, payload width, typed semantic value and final stop all match. The published API stops at the one payload end and consumes zero bits from the potential next `property_present` control.

This decision admits only the published differential. It does not admit another control bit, another header/payload, a generalized property loop/cursor, context/tag widening, next actor/frame iteration or downstream semantic/runtime behavior.

## Exact authority

```text
canonical main before admission      7db2b554611ba27ddf0b98d64f562e9b07011a9f
canonical main tree                  8d52bfd710009b12812fd6dd2f38f2fe338c50c3
production SHA/tree                  c2765ab9f04f9c981a6868cb6503bdf0e339ce1b / a6f27fe606cd3446da02ef1cb8cf53fff071e383
production lib / T test blobs        cf992670b461e9d923e773ed375bef2b42aea20d / 430676ec118fa0755a9c64abc0067bf5c5c88d05
evidence head/tree                   a53d0c8b4c88bab229e5ac9ec2db7dda5f9400b4 / f0c716278ef47665e43572d0129c4e8acd9be182
authority run/job                    32055189778 / 95463604513 SUCCESS
same-head normal CI                  32055189737 / 95463604366 SUCCESS
artifact                             9296199852 / 20181 bytes
artifact digest / ZIP SHA-256        sha256:13262328812bc56c9ea58bbc42364308fb6c65487c51f062296b14993f3a626e
R3.18P contract SHA-256              0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
R3.18S artifact                      9293436309 / sha256:dac07647e288bfc3b177000e1bfa6b9cfd892b80fd77d46c2f4974a3832cf422
admission authority                  32056128408 / 95466589551
```

The superseded first R3.18U attempt failed before semantic evidence because GitHub returned HTTP 503 while serving the frozen R3.18S artifact ZIP. It is not an authority. The final authority above used the same evidence criteria with bounded retry for that transient transport failure.

## Admitted evidence

```text
frozen rows                          47/47
exact R3.18P contexts                18/18
Boolean                              39 rows × 1 bit
ActiveActor                          8 rows × 33 bits
published-T / frozen-S mismatch      0
embedded header identity             47/47
witness reselection                  0
repeatability                        47/47
truncation negative                  47/47
wrong actor negative                 47/47
unresolved lookup negative           47/47
wrong exact context negative         47/47
fabricated context negative          47/47
post-payload/next-control poison     47/47
another-control bits consumed        0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

The artifact contains 11 files total: ten evidence payload files plus their SHA-256 manifest. All ten manifest entries verified. The downloaded ZIP SHA-256 equals the GitHub artifact digest exactly.

## Hard stop

R3.18U does not authorize reading the bit after the published R3.18T payload end. Following stream/header/payload decoding, another control after that bit, repeated/generalized property iteration, next actor/frame/lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual execution and runtime/export widening remain closed.

## Next gate

R3.18V is a separate read-only boundary characterization pass. It may start only at the exact published R3.18T `stop_bit`, observe exactly one next `property_present` bit on the same immutable 47 witnesses, compare it with pinned Boxcars and an independent evidence-only one-bit read, and stop one bit later. Its false/true distribution must be discovered from evidence rather than assumed.
