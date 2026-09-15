# MIMIR R3.18BZ Decision — Published-R3.18BY Mixed Following-Header Differential

**Date:** 2026-09-15
**Status:** CLOSED / OUTCOME A / READ-ONLY
**Canonical production authority:** R3.18BY `3b07e223fdf326e8100412fad9410bb1b66d2cb9` / `68b32f61d61c863b25e393cfa77575bac55217d7`
**Continuity base:** `3c90dd10fb775ca45c8bd23b8330290f6ebafbbc` / `d2ef61ef1c34630db6139dde28f6d952e0a67e4a`
**Evidence head:** `cfcfb671555827b8003007ff766798a1206aca15` / `46b91c8ab80db2c67e04f5386de5db4538cc2a7f`
**Runner:** `34950884111/104321306221` SUCCESS
**Artifact:** `10389058675` / 3111 bytes / `sha256:e11eceb83779b2fb52c658edf8ee932d4c24228d7b8046b44b235203d9f79d39`
**Artifact manifest SHA-256:** `f298edbe583571ac1a1b477d74fde61f76b92983b0e4016a01639fd2de8930af`
**Frozen contract authority:** R3.18BX `sha256:37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576`

## Admission evidence

- exact published rows: `2/2`
- false BU terminator: `1/1`, no following-header access, stop `11240`
- true BU continuation/header: `1/1`, stream `[3239,3245)`, id 61, bound 110, prop bits 6, object 67, `TAGame.PRI_TA:ClientLoadoutsOnline`, tag `LoadoutsOnline`, property ordinal 8, stop `payload_start=3245`
- exact R3.18BX context `(110,6,67,LoadoutsOnline,868,32,10,false)`: `1/1`
- direct shared stateless-header structural match: `1/1`
- immutable R3.18BW row reconciliation: `2/2`
- native/oracle mismatch: `0`
- witness reselection: `0`
- following payload bits consumed: `0`
- second later control bits consumed: `0`
- production/Cargo/fixture/corpus/support mutation: `0/0/0/0/0`
- privacy scan: `PASS`

## Negative and validation matrix

Repeatability `2/2`, corrupt-BU `2/2`, post-stop poison `2/2`, version-major/minor/net/RL223 mutations `8/8`, false-terminator no-header `1/1`, true-header truncation `1/1`, unresolved actor/property lookups `1/1` each, direct-header equality `1/1`, false-before-suffix, no following-payload decoder, no second-later-control read and no generic cursor/loop all PASS. Rust 1.85 fmt, R3.18BY regression, BZ negative matrix, source scope, workspace check/test/clippy, knowledge archive verifier and git-diff check all PASS.

## Decision

R3.18BZ satisfies the execution spec's Outcome A gate exactly and is admitted closed. No production capability is widened. Open R3.18CA only as read-only evidence for one following payload on the exact BY=true LoadoutsOnline row beginning at `payload_start=3245`. The BU=false row remains outside payload access.

## Hard stop

No K4 decoder or allowlist widening, no production source mutation, no false-row payload access, no next property-control bit, no second payload, no historical width/shape inheritance, no generic/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
