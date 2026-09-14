# MIMIR R3.18BU Decision — Bounded Post-BS Next Property-Control Production

**Date:** 2026-09-14
**Status:** CLOSED / ADMITTED PUBLISHED PRODUCTION
**Canonical production:** `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4` / parent `9a86252e02d383ebc2ff9665e678f4c2319f47d9`

## Receipts
- lib/test/spec blobs: `1c4db09cff43e0ab56f5efb5e8078da3a1189937` / `e6170f90b47e3f04bd798edbc61f2fa59e5213dd` / `ac1ce2120320bd552e5be24e2309fea23d5a2a50`
- builder `34823631010/103910607381` SUCCESS
- validation PR #219 CLOSED UNMERGED
- exact-head CI `34826521464/103919838545` SUCCESS
- published-main CI `34827065398/103921549254` SUCCESS
- immutable BR `ff1daab35e2e75bf7446a98a07a1db67e5196dbd` / artifact `10267123608` / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1`
- BT artifact `10336951993` / `sha256:fef0df77821475ac3ee5acb417b500aa40708a573d286d30c5c42bcf23ef473d`

## Admitted result
1. `external_fixtures/sample_002.replay`: exact BS Boolean payload ends 11239; BU control `[11239,11240)` = false; stop 11240.
2. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: exact BS ActiveActor payload ends 3238; BU control `[3238,3239)` = true; stop 3239.

BU recomputes/matches exact BS, consumes exactly one checked LSB-first control bit, matches frozen BR and stops. BP false terminator and all adjacent/wider structure remain excluded.

## Decision
R3.18BU is canonical production. Open R3.18BV as read-only exact published-BU differential only.
