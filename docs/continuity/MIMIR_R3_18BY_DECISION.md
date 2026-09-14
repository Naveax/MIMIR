# MIMIR R3.18BY Decision — Bounded Post-BU Mixed-Continuation Following-Header Production

**Date:** 2026-09-14
**Status:** CLOSED / ADMITTED PUBLISHED PRODUCTION
**Canonical production:** `3b07e223fdf326e8100412fad9410bb1b66d2cb9` / `68b32f61d61c863b25e393cfa77575bac55217d7`
**Canonical base:** `d4b0e84adf5603a6c2fe106a7f466cd497efdd43`
**Final parent:** `16e21d91f8e60db7b7e7b76d66494327de6936cc`
**Contract authority:** R3.18BX `sha256:37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576`

## Receipts
- lib/test/spec blobs: `beadbb35ec5bcda427260f6f6c5afeb7780cdbc5` / `07e0e4bdb346833d550248609b96af8e255d4c11` / `727c971cc1ac6d59d59bcbc3677d71e7a4f3267b`
- production builder: `34849180581/103992470153` SUCCESS
- final exact-head push CI: `34856781439/104018278890` SUCCESS
- validation PR #223: CLOSED UNMERGED
- final validation PR CI: `34856787577/104018300863` SUCCESS
- published-main CI: `34857720437/104021486939` SUCCESS
- publication: force=false; exact main readback PASS

The initial builder candidate `16e21d91f8e60db7b7e7b76d66494327de6936cc` was followed only by the stable-Clippy `div_ceil` correction in the focused test. Final production diff from `d4b0e84adf5603a6c2fe106a7f466cd497efdd43` remains exactly two files: `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs`.

## Admitted result
1. `external_fixtures/sample_002.replay`: validated BU false `[11239,11240)`; BY returns `following_header=None` and stops at 11240 with zero post-BU header access.
2. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: validated BU true `[3238,3239)`; BY decodes exactly one existing-actor header with stream `[3239,3245)`, id 61, bound 110, prop bits 6, object 67 `TAGame.PRI_TA:ClientLoadoutsOnline`, tag LoadoutsOnline, context 868.32/net10/non-RL223, and stops exactly at payload_start 3245.

Exact R3.18BX tuple membership is mandatory. Wrong actor/lookup/context, header truncation and corrupt BU prerequisite fail closed. Repeatability and post-stop poison checks pass. Following payload and second later property-control consumption remain 0/0.

## Decision
R3.18BY is canonical production. Open R3.18BZ as a read-only published-production differential on exactly the immutable two-row lane. No following payload, second later control, false-row header synthesis, context widening, witness reselection, production mutation or generalized/repeated property cursor is admitted.
