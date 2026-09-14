# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BU** `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`.

R3.18BW is **Outcome A / CLOSED READ-ONLY** at `778b12988046da4d186248877bd577eb2a533a58` / `5a6e7bd95c95f3e38db34a543b396aec747db985`; runner `34843377101/103973337631` and same-head natural CI `34843377045/103976995152` SUCCESS; artifact `10346819501` / `sha256:ee8a1878241b45765a7fa57c64c179c40090836096055fc5626a58724b5796fd`. Exact BU rows=2/2, false/true=1/1, one header exact=1/1, mismatch/reselection/false-header=0/0/0, payload/second-control=0/0.

R3.18BX is **Outcome A / CLOSED CONTRACT**. Exact membership is only `(110,6,67,LoadoutsOnline,868,32,10,false)` x1; contract `sha256:37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576`; one false BU terminator remains outside membership.

Active pass: **R3.18BY — bounded post-BU mixed-continuation following-header production**. False validated BU must return no-header without post-BU reads. True validated BU may invoke one existing-actor header suffix, require exact BX membership and stop at payload_start 3245. No payload or later control is in scope.
