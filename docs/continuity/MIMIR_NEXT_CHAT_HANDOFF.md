# MIMIR — Next Chat Handoff

Canonical production is **R3.18BY** `3b07e223fdf326e8100412fad9410bb1b66d2cb9` / `68b32f61d61c863b25e393cfa77575bac55217d7`. Final exact-head push CI `34856781439/104018278890`, validation PR #223 CI `34856787577/104018300863`, and published-main CI `34857720437/104021486939` are SUCCESS; PR #223 is closed unmerged.

R3.18BW is **Outcome A / CLOSED READ-ONLY** at `778b12988046da4d186248877bd577eb2a533a58`; artifact `10346819501` / `sha256:ee8a1878241b45765a7fa57c64c179c40090836096055fc5626a58724b5796fd`. R3.18BX is **Outcome A / CLOSED CONTRACT** with only `(110,6,67,LoadoutsOnline,868,32,10,false)` x1, contract `sha256:37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576`.

R3.18BY publishes the exact two-row mixed lane: sample_002 BU=false terminates without header at 11240; largest_100/079 BU=true exposes exactly one admitted LoadoutsOnline header and stops at payload_start 3245.

Active pass: **R3.18BZ — published-R3.18BY mixed following-header differential**. It is read-only: exact two rows only, false header access 0, true header exact 1/1, payload/second-control consumption 0/0, no witness reselection or production mutation.
