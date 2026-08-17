# MIMIR R3.18V — Next Property-Control Bit Evidence Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / EXACT ONE-BIT BOUNDARY CHARACTERIZED**
**Production mutation:** none
**Canonical production:** `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b`

## Decision

R3.18V closes Outcome A. On exactly the immutable 47 R3.18U witnesses, the published R3.18T result reproduced exactly through its payload-end `stop_bit`, then pinned Boxcars and an independent evidence-only LSB-first read observed exactly one next `property_present` bit at that same offset. Start/value/end matched on 47/47 rows. The observed distribution is **false=0 / true=47**.

This decision admits only the evidence that one true control bit exists at this boundary on all frozen witnesses. It does not admit the following stream/header/payload, a second later control bit, a loop/cursor, false success semantics, or any wider actor/frame/runtime behavior.

## Exact authority

```text
canonical main before admission      06c7b0524692fc371e21526c17d5ecfe3a69e10e
canonical main tree                  5e253e5c42fa4b0e6fcc9c7c983cdb5ffc164862
production SHA/tree                  c2765ab9f04f9c981a6868cb6503bdf0e339ce1b / a6f27fe606cd3446da02ef1cb8cf53fff071e383
production lib / T test blobs        cf992670b461e9d923e773ed375bef2b42aea20d / 430676ec118fa0755a9c64abc0067bf5c5c88d05
evidence head/tree                   2b0c9f01559e77a6fdf21a097b8ab4d1a27b6ff5 / 229b3d68a82f6dadc19518614e27ff09e8006ad2
authority run/job                    32057732310 / 95471639989 SUCCESS
same-head normal CI                  32057732335 / 95471640230 SUCCESS
artifact                             9297068554 / 20484 bytes
artifact digest / ZIP SHA-256        sha256:e17426aad6d476eba17bb471dc92cd24b4b4d8727ad427ad15fa6e9c1dda9eb2
Boxcars instrumentation SHA-256      198096b6693c91cc146aae10fb0a5d3729dd778b7038e3915ede59fd246032b3
R3.18U artifact                      9296199852 / sha256:13262328812bc56c9ea58bbc42364308fb6c65487c51f062296b14993f3a626e
admission authority                  32058481331 / 95474000477
```

The downloaded artifact contained 12 files total: eleven evidence payload files plus their SHA-256 manifest. All eleven manifest entries verified and the ZIP SHA-256 matched the GitHub artifact digest exactly.

## Admitted evidence

```text
frozen rows                          47/47
published R3.18T reconstruction      47/47
next property_present false          0
next property_present true           47
native/oracle mismatch               0
witness reselection                  0
control truncation                   PASS 47/47
repeatability                        PASS 47/47
prior T stop mismatch negative       PASS 47/47
post-control poison                  PASS 47/47
next stream bits consumed            0
next header bits consumed            0
next payload bits consumed           0
second later control bits consumed   0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Hard stop

R3.18V does not authorize resolving or decoding the next stream ID, property object, attribute tag or payload. It does not authorize a second later control bit, false success/terminator semantics at this boundary, repeated/generalized property iteration, a public cursor, next actor/frame/lifecycle mutation, raw-state/event extraction, replay slicing, skills, counterfactual execution or runtime/export widening.

## Next gate

R3.18W is a separate bounded production implementation. Starting only from an already-valid published R3.18T result, it may validate the exact payload-end stop, read exactly one following `property_present` bit, admit **true only** because R3.18V observed true=47/false=0, and stop one bit later. False must fail closed. It may not resolve/decode any following stream/header/payload or read another control bit.
