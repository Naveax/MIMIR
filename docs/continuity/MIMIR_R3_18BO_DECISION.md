# MIMIR R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production Decision

**Date:** 2026-09-09
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`
**Parent:** `a07b405ee5bb299b468d6bcfc8e66ba89a69e40d`
**Contract authority:** R3.18BN `sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`

## Decision

R3.18BO closes Outcome A on exactly the immutable three-row R3.18BM/R3.18BN/R3.18BK lane. The one published-BK false row remains a successful no-header terminator with zero post-BK reads. Exactly two published-BK true rows compose exactly one existing-actor following property header with the existing stateless suffix primitive, require exact R3.18BN eight-field tuple membership, and stop exactly at `payload_start`.

Exact admitted true contexts remain:

```text
(72,  6, 95, Boolean,     868, 32, 10, false) x1
(110, 6, 66, ActiveActor, 868, 32, 10, false) x1
```

No following payload or second later property-control bit is consumed. No generalized/repeated cursor is introduced.

## Exact authority

```text
canonical parent                      a07b405ee5bb299b468d6bcfc8e66ba89a69e40d / 9548fcc5cf3d2f8d054b049aee5110edca5342a9
production SHA/tree                   cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
lib/test blobs                        89359ead38b18e4a71448217561caed97a41b915 / 5bfd9a81e0de21e70f93e24d8b43a4b540724e9c
BO execution spec blob                3be058d574cf55f3dfaf9e369c37bf3fa42afaa4
production builder head               225880eb90f36b3c0f03d144726045d089528257
production builder                    34346270277/102448481752 SUCCESS
exact-candidate CI                    34347518210/102452536398 SUCCESS
published-main CI                     34348026122/102454170761 SUCCESS
BM evidence head/tree                 689b1a24b57a84c81dc19c9a308fb1423f191c4b / 1d4e95409e1125b01a78aae6a436190b3c1381f4
BM evidence run/job                   34334615939/102410984005 SUCCESS
BM same-head CI                       34334615886/102411487443 SUCCESS
BM artifact                           10097405795 / sha256:bd51a612be2cdd87d9ce1eb141f3f77f47ae29d42aabc8fc16c260a175f27963
BN contract blob                      c5f5a0cd0df3969646fecd8e137a2770c2daae71
BN contract                           sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
BN membership                         exact_tuple_only / 2 eight-field tuples / multiplicity 2
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted production behavior

```text
frozen BK rows                        3/3
BK false terminators                  1/1
false following header                none 1/1
false post-BK reads                   0
BK true continuations                 2/2
true following headers                exact 2/2
exact BN contexts                     2/2
true tags                             Boolean=1 / ActiveActor=1
property ordinal                      7 on 2/2
upstream AU exclusions                7/7
intermediate BE exclusions            37/37
following payload bits consumed       0
second later control bits consumed    0
generalized/repeated cursor           0
```

The clean production commit contains only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18bo_post_bk_following_header.rs`. No Cargo/dependency, continuity, workflow, fixture, corpus, support, raw-state/event/skill/runtime/export or unrelated mutation entered production.

## Validation

The R3.18BO builder passed exact authority freeze, exact two-file scope, Rust 1.85 formatting, focused BO contract/integration tests, direct BK/BI/BE regressions, workspace/repository validation and clean-candidate reconstruction. The byte-identical candidate passed normal CI `34347518210/102452536398`. Fresh `main` ancestry was rechecked, publication used `force=false`, exact SHA/tree readback matched, and published-main CI `34348026122/102454170761` passed on the exact production SHA.

## Hard stop

No following payload, no second later property-control bit, no header on the false BK terminator, no context outside exact R3.18BN membership, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18BP is a separate read-only published-production differential. It must compare published R3.18BO against exactly the immutable three-row BM/BN/BK authority, preserve false=1 / true=2, require exact true-header identity/boundaries and BN membership, keep mismatch and witness reselection at zero, and consume no following payload or second later control.
