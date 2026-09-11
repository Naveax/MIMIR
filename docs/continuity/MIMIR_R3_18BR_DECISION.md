# MIMIR R3.18BR — Next Property-Control Bit Evidence Decision

**Date:** 2026-09-11
**Outcome:** **A — CLOSED / ADMITTED READ-ONLY ONE-BIT EVIDENCE**
**Production mutation:** none
**Canonical production remains:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`

## Decision

R3.18BR closes Outcome A on exactly the two immutable R3.18BQ payload rows. Each BQ payload was byte-exactly rematerialized through its admitted `payload_end_bit`; the BP false terminator remained outside the BR lane. Exactly one following `property_present` bit was then observed with independent native evidence logic and pinned Boxcars, and native/oracle start/value/end matched 2/2 with zero reselection.

The observed distribution is **false=1 / true=1**. This distribution was not inherited from any historical boundary.

```text
BQ payload rows exact                    2/2
BQ rematerialization                     byte-exact 2/2
BP false terminator control access       0
next-control native/oracle exact          2/2
next-control false                        1
next-control true                         1
witness reselection                       0
following stream/header/payload           0/0/0
second later control                      0
production/Cargo/fixture/corpus/support   0/0/0/0/0
privacy + full validation                 PASS
```

Exact admitted observations:

- `external_fixtures/sample_002.replay`: admitted Boolean payload `[11238,11239)`; next control `[11239,11240)` = `false`.
- `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: admitted ActiveActor payload `[3205,3238)`; next control `[3238,3239)` = `true`.

## Exact authority

```text
canonical evidence parent/tree           265b780dc554715a7bc6bfb5c8e0fbe7ee279265 / d19218dea425819c8ec8eee8464ab5e198945bb6
production SHA/tree                      cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
BQ evidence head/tree                    16c43f38e740c57ae9cb90c92084002ec83815e7 / 58248877a59fb0ddad707e32f92b2cec91f6b434
BQ artifact                              10144392560 / sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c
BR evidence head/tree                    ff1daab35e2e75bf7446a98a07a1db67e5196dbd / 373d516dbab42b49216e50c09cbd6744863a88b1
BR run/job                               34606677020 / 103286690781 SUCCESS
BR same-head natural CI                  34606676915 / 103287920321 SUCCESS / count 1
BR artifact                              10267123608 / 8783 bytes / sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1
BR inner manifest SHA-256                f18ef70512227d5968a1fa0594bf522ae1924d9668a1bb353da8747618d3b7e1
pinned Boxcars                           c70e77df7af81b436cb545d070bb90c82f562d0b
```

The evidence candidate is exactly one commit ahead of the canonical parent and changes only `.github/workflows/_tmp_r318br_evidence.yml`. Its artifact manifest verifies every listed payload file. Workspace fmt/check/test/clippy, repository verifier, diff-check, privacy scan and unique same-head natural CI all passed.

## Canonical sequencing consequence

R3.18BR does **not** make the observed control bit the next production boundary. Canonical production R3.18BO still stops at following-header `payload_start`, because R3.18BQ payload decoding is evidence-only. Therefore the next bounded production pass is **R3.18BS**: publish exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload after a valid BO/BN header and stop at payload end. Only after that payload production is independently validated may the BR mixed control semantics be considered for production in a later pass.

## Hard stop

No production control-bit consumption is admitted by BR. No payload/control access on the BP false terminator, next stream/header/payload after the BR observation, second later control, generalized/repeated property cursor, actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening, or historical control-value inheritance is admitted.
