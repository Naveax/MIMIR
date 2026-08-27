# MIMIR R3.18AV — Published R3.18AU Mixed Following-Header Differential Decision

**Date:** 2026-08-27
**Outcome:** **A — CLOSED / READ-ONLY ADMITTED**
**Canonical production remains:** `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef`
**Production mutation:** none

## Decision

R3.18AV closes Outcome A. Published R3.18AU matches the immutable R3.18AS/R3.18AT 47-row authority exactly. All seven AQ-false rows remain successful no-header terminators. All forty AQ-true rows expose exactly the frozen following header under exact R3.18AT membership and stop at `payload_start`. No following payload or second later property-control bit is consumed.

This is a read-only differential admission, not a production payload admission. It opens only a separate R3.18AW evidence pass over exactly the forty true rows.

## Exact authority and receipts

```text
canonical main                         c49ce8f7b1e1145e5fb41a98dcaae9c5de61c37e
canonical production SHA/tree          6a9f456c78ffccab177823234a8d9fe4ba59a850 / cbda5db96e88cc208f872c2237cf4741b8fcfaef
AV evidence head/tree                  fcbabd6953b4bade41f49b767f0dd73524e190d8 / 922e7fb45de33b1803027e6cdcbbe55467a1bc2e
AV evidence run/job                    33057596762 / 98468171016 SUCCESS
AV same-head natural CI                33057596712 / 98468756735 SUCCESS
same-head CI count / rerun             1 / 0
AV artifact                            9640472993 / 10256 bytes
AV artifact digest                     sha256:26082be08c8644a17076d9df2138128df110bbf39b4b3bceefdc823a9492d456
AS evidence head/artifact              475650fea59332f74b9f69da50e3e4471622ab7e / 9603335255
AS artifact digest                     sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
AT contract sha256                     3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

The AV artifact was independently downloaded after workflow completion. Its internal `r3_18av_artifact_sha256.txt` verified every included file. The aggregate, authority receipt, negative-control receipt and same-head CI receipt all matched the values above.

## Admitted differential result

```text
frozen rows                            47/47
published R3.18AU exact                47/47
false no-header terminators            7/7
true exact following headers           40/40
exact AT contexts                      16/16
AT multiplicity                        40
observed tag                           Int=40
mismatch                               0
witness reselection                    0
following payload bits consumed        0
second later control bits consumed     0
production/Cargo/fixture/corpus/support 0/0/0/0/0
privacy                                PASS
```

## Negative controls

False-terminator post-stop poison, true-header truncation, post-`payload_start` poison isolation, wrong actor, unresolved lookup, wrong exact context, mismatched prerequisite, RL223 widening, component/Cartesian/versionless widening, AJ-valid-but-AT-absent membership, fabricated seventeenth tuple and source-scope zero-payload-decoder controls all passed.

## Hard stop

R3.18AV does not admit following-payload production, any payload on the seven false terminators, a next property-control bit, a following header/payload after that scalar, context widening, historical AM/AN payload inheritance, a generalized/repeated property cursor, or wider actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior.

## Next gate

R3.18AW is a separate read-only one-payload evidence pass. It must rematerialize exactly the forty AV-true rows from the admitted AV artifact, use each current proven header tag/boundary, independently compare one primitive scalar with pinned Boxcars, and stop at payload end with zero next-control consumption. All seven false rows remain outside the payload lane.
