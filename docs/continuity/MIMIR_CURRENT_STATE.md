# MIMIR — Current Canonical State

**Continuity date:** 2026-09-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `3b07e223fdf326e8100412fad9410bb1b66d2cb9`
**Production tree:** `68b32f61d61c863b25e393cfa77575bac55217d7`
**Production milestone:** `R3.18BY — bounded post-BU mixed-continuation following-header production`
**Last read-only evidence/audit:** `R3.18CA — Outcome A / exact LoadoutsOnline [3245,4227) / width 982 / existing K4 accepted / artifact 10405136702`
**Last contract pass:** `R3.18BX — Outcome A / one exact eight-field tuple / contract 37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576`
**Current exact pass:** `R3.18CB — exact post-BU one-payload bounded production`

## Truthful boundary

R3.18BY remains canonical production at `3b07e223fdf326e8100412fad9410bb1b66d2cb9` / `68b32f61d61c863b25e393cfa77575bac55217d7` until CB is independently validated and published.

R3.18CA closed Outcome A at `01ebdf5a8c7b192ef19a280711b3b0947f373647` / `116d2ef967bdbcd04d2af855be16fb865500854b` with evidence `34989130467/104448878632` SUCCESS, same-head CI `34989130481` SUCCESS, and artifact `10405136702` / `sha256:7e5e94df57fe51513ead7b7ed973bcce81c983f51603892fa9022227c8a05876` / manifest `a4670cdd141a2c12242542cf3788c01af331267c526b6d612c633ded01708341`. The exact true `LoadoutsOnline` payload is `[3245,4227)`, width 982, semantic SHA-256 `7641391ebd59828550db4ee24036b07a47a0bf40057c9c34024e5461787eb142`; existing K4 membership accepts it and native/oracle structure+semantics match exactly. Repeatability 2/2, truncation rejection 3/3, post-end poison PASS, false-row payload access 0, next-control bits 0, second payloads 0, reselection 0, mutations 0/0/0/0/0.

R3.18CB may compose only that exact payload through the existing K4 decoder. The BU=false row remains a terminator at 11240.

## Hard stop

No K4 decoder/allowlist widening, no other payload context/tag/shape, no false-row payload, no next control after 4227, no second payload/header, no generalized property cursor/loop, and no wider semantic/runtime capability.
