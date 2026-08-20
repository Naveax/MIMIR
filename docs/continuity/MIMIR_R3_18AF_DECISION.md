# MIMIR R3.18AF — Next Property-Control Bit Evidence Decision

**Date:** 2026-08-20
**Outcome:** **A — ADMITTED / EXACT ONE-BIT BOUNDARY CHARACTERIZED**
**Production mutation:** none
**Canonical production:** `ccadbf148381c007890d13d5fe8120866a0f40f9`

## Decision

R3.18AF closes Outcome A. On exactly the immutable 47 R3.18AE witnesses, the published R3.18AD result reproduced exactly through its ordinal-3 payload-end `stop_bit`, then pinned Boxcars and an independent evidence-only LSB-first read observed exactly one next `property_present` bit at the same offset. Start/value/end matched 47/47. The discovered distribution is **false=0 / true=47**.

This decision admits only that one true control bit on the frozen lane. It does not admit false success semantics, the following stream/header/payload, a second later control, a loop/cursor, alternate UniqueId layouts, next actor/frame iteration or wider semantic/runtime behavior.

## Exact authority

```text
canonical main before admission      9c3b92829ddbc80cc855f5bd76ae489eb156b81a
canonical main tree                  044865771f72d57045f12d927a9c0e8c58004326
production SHA/tree                  ccadbf148381c007890d13d5fe8120866a0f40f9 / 0882601060d0bb6d37fcc03ae7273dcf50dd0be3
production lib / AD test blobs       1254d5a3d16e7b97b1dee87a8b459514d25749ef / 013ad6da94b866ecaca94cd6420e7568d9b4b5ee
AF execution spec blob               fd3e4debac1c40756c37f106fc68440576678d6c
evidence head/tree                   30286c07727539d68f551140838fb2ef6802a26e / be808ad1ea757a095e37ccfe8f25b03e074dd732
authority run/job                    32344981062 / 96351720877 SUCCESS
same-head normal CI                  32345376481 / 96352906609 SUCCESS
validation PR                        #53 closed unmerged
artifact                             9397743505 / 12204 bytes
artifact digest / ZIP SHA-256        sha256:d7edeab657928c94c35c852ae302fd614cab92a52b7e44f671310200af4b268f
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
Boxcars instrumentation SHA-256      de5fecb234e4a53798ce8e59b728078c7719ae04ef5fa2966b2c3b67072e7adf
```

The downloaded artifact contains 11 files total: ten evidence payload files plus their SHA-256 manifest. All ten manifest entries verified and the ZIP SHA-256 equals the GitHub artifact digest exactly.

## Admitted evidence

```text
frozen rows                          47/47
published R3.18AD reconstruction      47/47
next property_present false           0
next property_present true            47
native/oracle mismatch                0
witness reselection                   0
control truncation                    PASS 47/47
repeatability                         PASS 47/47
prior AD stop mismatch negative       PASS 47/47
post-control poison                   PASS 47/47
next stream bits consumed             0
next header bits consumed             0
next payload bits consumed            0
second later control bits consumed    0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                          PASS
```

## Superseded attempt

`b821eb048f038758206144373713a9754bc1561a` / `32344721157/96350927162` is not scientific authority. It had already verified upstream artifacts and the ordinal-4 Boxcars observation 47/47, then failed because the temporary `crates/mimir-replay/examples` directory did not exist. The corrected authority changed only that harness materialization issue.

## Next gate

R3.18AG is a separate bounded production implementation. Starting only from an already-valid published R3.18AD result, it may validate the exact payload-end stop, read exactly one following `property_present` bit, admit **true only** because R3.18AF observed true=47/false=0, and stop one bit later. False must fail closed. It may not resolve/decode any following stream/header/payload or read another control bit.
