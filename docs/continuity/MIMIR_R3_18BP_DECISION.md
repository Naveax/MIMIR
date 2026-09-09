# MIMIR R3.18BP — Published R3.18BO Mixed Following-Header Differential Decision

**Date:** 2026-09-09
**Outcome:** **A — CLOSED / ADMITTED READ-ONLY EVIDENCE**
**Canonical production:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`
**Evidence head/tree:** `319d2b910ac23008bcc5338f04a5f95a0ae5ac5b` / `1fc7223296b71256681a885de7e20161114532a9`
**Evidence run/job:** `34355148349` / `102477806191` SUCCESS
**Same-head CI:** `34355148286` / `102477834627` SUCCESS
**Artifact:** `10105612793` / `sha256:ffa6613fc7703f148d388650466f164068e5d454cfeb0a926c548caacda47240`

## Decision

R3.18BP closes Outcome A on exactly the immutable three-row BM/BN/BK authority. Published R3.18BO matched all three witnesses with no reselection and no adjacent consumption.

- false no-header terminator: 1/1;
- true exact following headers: 2/2;
- exact R3.18BN contexts: 2/2, multiplicity 2;
- tags: Boolean=1 / ActiveActor=1; property ordinal 7 on 2/2;
- published BO mismatch / witness reselection: 0/0;
- following payload / second later control consumption: 0/0;
- AU/BE exclusions: 7/7 and 37/37;
- production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0;
- privacy and full repository validation: PASS.

## Exact authority

```text
continuity base SHA/tree              bd7310eb8ba96f0bd8ebcd59ed3b1806e856ae52 / 17ad3834dc36c5e9e6ddd1f62d5147c16dd93946
canonical production SHA/tree         cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
BN contract                           sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
BP evidence head/tree                 319d2b910ac23008bcc5338f04a5f95a0ae5ac5b / 1fc7223296b71256681a885de7e20161114532a9
BP evidence run/job                   34355148349/102477806191 SUCCESS
BP same-head CI                        34355148286/102477834627 SUCCESS
BP artifact                           10105612793 / 7008 bytes / sha256:ffa6613fc7703f148d388650466f164068e5d454cfeb0a926c548caacda47240
BP inner manifest                     sha256:2e8fbf0b4a9c2d29d4fdb440dba54eabcd860c91bc25c49d486c969052bef174
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted read-only result

```text
rows                                      3/3
false no-header                       1/1
true exact header                     2/2
exact BN contexts                     2/2
BN multiplicity                          2
tags                                    Boolean=1 / ActiveActor=1
property ordinal 7                    2/2
mismatch / reselection                0 / 0
following payload / second control    0 / 0
mutation                               0/0/0/0/0
privacy                                PASS
```

## Hard stop

BP admits no payload production. No payload access on the false terminator, no next control, no generalized cursor and no wider actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior.

## Next gate

R3.18BQ may inspect exactly one following payload on the **two BP-true rows only**, using BP artifact `10105612793` as direct row authority. Boolean uses the exact one-bit primitive scalar layout. ActiveActor uses the exact K2 layout (`active: bool` plus signed 32-bit actor id, total 33 bits) under net10/non-RL223. BQ must independently compare current values and boundaries with pinned Boxcars; historical payload values or coordinates are not authority. Only BQ Outcome A may open a separate payload-end control-bit pass.
