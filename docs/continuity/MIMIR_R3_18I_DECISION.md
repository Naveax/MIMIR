# MIMIR R3.18I — Second-Property Payload Evidence Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**
**Production mutation:** **NONE**
**Production authority remains:** `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`

## Decision

R3.18I is admitted as read-only evidence. The frozen R3.18F/R3.18H lane was reused without witness reselection. All 94 rows reproduced: 47 terminators remained no-second-payload controls and all 47 continuations decoded exactly one second-property payload from the already-proven second `payload_start` through its exact payload end.

The continuation distribution is exactly `Int=46 / String=1`. Native/oracle mismatch is zero. No third-property/control bit was consumed. Wrong-tag, truncation, repeatability and post-payload poison/invariance controls passed. Production Rust, Cargo, fixtures, corpus and support lanes remained unchanged.

## Immutable authority

```text
pre-pass canonical main             3257d32fbc617b6dae7bb42d41629639acf6ce95
evidence head                       45090a2c18fb517088bb411782bbaed0d7d68199
evidence workflow run/job           31975063743 / 95233164711 SUCCESS
same-head normal CI run/job          31975063703 / 95233164610 SUCCESS
artifact                            9270842140 / 18741 bytes
artifact digest                     sha256:9890ed33780412a8900692a627b212d80428a08229f9f691d914c8def31e06e2
frozen rows                         94/94
terminator / continuation           47 / 47
continuation tags                   Int=46 / String=1
native/oracle mismatch              0
third-property bits consumed        0
witness reselection                 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

## Payload contract established by evidence

For the exact R3.18I lane only:

- `Int`: exactly 32 payload bits, native primitive-scalar semantics, exact end cursor;
- `String`: exactly the already-admitted K2 String wire contract for the observed row, declared length 7, Windows-1252, exact 88-bit payload width and exact end cursor;
- a terminator has no second payload and stops at the R3.18G control end;
- a continuation begins only at the R3.18G second header's exact `payload_start`;
- success stops immediately after exactly one second payload;
- the next `property_present` bit is outside this evidence pass.

This is evidence authority, not a production capability claim.

## Hard stop retained

Production still does not compose or expose a second-property payload, does not read the third `property_present` bit, and has no repeated/general property loop. Next actor/frame iteration, actor lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening remain closed.

## Next exact pass

`R3.18J — bounded native second-property payload composition` may implement only the exact `Int | String` second-payload surface established here, with one payload maximum and no third-control access.
