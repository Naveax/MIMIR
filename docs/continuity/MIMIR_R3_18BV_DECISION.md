# MIMIR R3.18BV Decision — Published R3.18BU One-Control Differential

**Date:** 2026-09-14
**Status:** OUTCOME A / CLOSED READ-ONLY
**Production authority:** R3.18BU `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`
**Evidence head/tree:** `45c6a5b57ee96c8e4b8b472e548c6b1f2d4c426c` / `68da2ace745390781ea7e5ade25aaf2c051098d3`

## Immutable receipts
- evidence runner `34830085977/103932439559` SUCCESS
- same-head natural CI `34830086065/103931122833` SUCCESS
- artifact `10341754652` / 2596 bytes / `sha256:d63f87d75c9c745cfab9b04116cbb3249bcdede7329a0ec8ea5371379548b982`
- workflow blob `30d772fc07c7c290418cee5a0dc8160e2cf6b00f`
- immutable BR `ff1daab35e2e75bf7446a98a07a1db67e5196dbd` / artifact `10267123608` / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1`
- pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`

## Admitted result
1. `external_fixtures/sample_002.replay`: published BU control false at `[11239,11240)`, stop 11240; exact BS prerequisite ends 11239.
2. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: published BU control true at `[3238,3239)`, stop 3239; exact BS prerequisite ends 3238.

Aggregate: exact 2/2; BS prerequisite 2/2; false/true 1/1; mismatch 0; witness reselection 0; BP-false excluded 1/1; repeatability 2/2; post-stop poison 2/2; following stream/header/payload/second-control 0/0/0/0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; validation/privacy PASS.

## Decision
R3.18BV closes Outcome A without production mutation. The false Boolean row is a terminator. Open R3.18BW as a separate read-only one-following-header evidence pass on only the exact true ActiveActor continuation row. No payload or later control is admitted.
