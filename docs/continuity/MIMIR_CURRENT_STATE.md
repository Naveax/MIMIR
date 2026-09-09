# MIMIR — Current Canonical State

**Continuity date:** 2026-09-09
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `cbb823ce7d3fc871c35a83afc5ee21ae71945821`
**Production tree:** `146cb78edfb434fd43e532593efce8e35ee97111`
**Production milestone:** `R3.18BO — bounded post-BK mixed-continuation following-header production`
**Last read-only evidence/audit:** `R3.18BM — Outcome A / false=1 true=2 / one-header exact 2/2 / contexts=2 / artifact 10097405795`
**Last completed contract:** `R3.18BN — exact_tuple_only / 2 eight-field contexts / multiplicity 2 / contract 904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`
**Current exact pass:** `R3.18BP — published R3.18BO mixed following-header differential`

## Truthful boundary

R3.18BO is canonical production. Exactly three valid published R3.18BK rows enter BO. The one false BK row terminates successfully without post-BK header access. Exactly two true BK rows compose one R3.18BN-admitted existing-actor following header and stop at `payload_start`; tags are Boolean=1 / ActiveActor=1 and property ordinal is 7 on 2/2.

```text
production SHA/tree                    cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
parent                                 a07b405ee5bb299b468d6bcfc8e66ba89a69e40d
lib/test blobs                         89359ead38b18e4a71448217561caed97a41b915 / 5bfd9a81e0de21e70f93e24d8b43a4b540724e9c
builder                                34346270277/102448481752 SUCCESS
exact-candidate CI                     34347518210/102452536398 SUCCESS
published-main CI                      34348026122/102454170761 SUCCESS
valid BO rows                          3/3
false no-header                        1
true exact header                      2
exact BN contexts                      2/2
true tags                              Boolean=1 / ActiveActor=1
property ordinal                       7 on 2/2
upstream exclusions                    AU=7 / BE=37
following payload / second control     0 / 0
```

## Active differential gate

R3.18BP is read-only. It must compare published BO against exactly the immutable BM/BN/BK three-row authority, preserve false=1 / true=2, exact header identity and exact BN membership, keep mismatch/reselection at zero, and consume no payload or later-control bits.

## Hard stop

No following payload, second later control, header on the false terminator, context outside exact R3.18BN membership, generalized/repeated property cursor, or actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
