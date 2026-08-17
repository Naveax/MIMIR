# MIMIR — Next Chat Handoff

Canonical production is now **R3.18W** at `58872e94f00ef094807f21ab2ff984ac66b97d91` / `d6965d77903ea99dad0465bb350b6a673ee7dd00`. It validates one exact R3.18T following-payload result, reads exactly one control bit, succeeds only on true, rejects false, and stops one bit later. Authority `32060501395/95480474127`, clean-candidate CI `32062120856/95485540552`, PR CI `32062533181/95486877308`, and published-main CI `32062965119/95488256583` are SUCCESS.

The active pass is **R3.18X**, a read-only published-W differential on exactly the immutable 47 R3.18V witnesses. Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18W_DECISION.md`, and `docs/continuity/MIMIR_R3_18X_EXECUTION_SPEC.md` before work.

Frozen V authority: `2b0c9f01559e77a6fdf21a097b8ab4d1a27b6ff5` / `32057732310/95471639989`; same-head CI `32057732335/95471640230`; artifact `9297068554` / `20484` / `sha256:e17426aad6d476eba17bb471dc92cd24b4b4d8727ad427ad15fa6e9c1dda9eb2`; control false=0 true=47; adjacent stream/header/payload/second-control consumption 0/0/0/0. R3.18X must reproduce that exact one-bit boundary with the published W API and mutate nothing.
