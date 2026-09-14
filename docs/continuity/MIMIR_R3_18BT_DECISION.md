# MIMIR R3.18BT Decision — Published R3.18BS One-Following-Payload Differential

**Date:** 2026-09-14
**Status:** Outcome A — CLOSED / ADMITTED READ-ONLY EVIDENCE
**Production authority after decision:** unchanged R3.18BS `5ab14575d0a698d752db35db76f3dbb300cdec8d` / `1c0b4c0a50385a34ba730a52a98a89423ff56869`

## Immutable receipts

- Evidence head/tree: `b687f700a7bf00f28671ca3adbb6613b582e7848` / `f573860e733689fa03767702f6f1750e222664c3`
- Workflow blob: `69ecc8d1bbf3096be459582203350f541e558561`
- Runner: `34816904695/103889382147` — SUCCESS
- Same-head natural CI: `34816904663/103889381782` — SUCCESS
- Artifact: `10336951993` / `5213` bytes / `sha256:fef0df77821475ac3ee5acb417b500aa40708a573d286d30c5c42bcf23ef473d`
- R3.18BQ: `16c43f38e740c57ae9cb90c92084002ec83815e7` / `34457725716/102807933610` / artifact `10144392560` / `sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c`
- R3.18BR: `ff1daab35e2e75bf7446a98a07a1db67e5196dbd` / artifact `10267123608` / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1`
- R3.18BN contract: `sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`

## Admitted result

Published R3.18BS exactly reproduces both immutable BQ payload witnesses: Boolean `[11238,11239)` value=true and ActiveActor `[3205,3238)` active=true actor=1. Exact identity is 2/2; BP false terminator exclusion is 1/1; mismatch=0; witness reselection=0. Repeatability and post-payload poison checks are 2/2. The following R3.18BR control bit is consumed zero times. No next stream/header/payload or second later control is read. Production/Cargo/fixture/corpus/support mutation is zero.

## Decision

Outcome A is admitted. R3.18BT is closed read-only. Production remains R3.18BS. The next pass may open exactly one R3.18BR-observed control bit after a valid exact BS result on the two admitted rows and nothing beyond that one bit.
