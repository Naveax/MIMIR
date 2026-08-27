# MIMIR — Current Canonical State

**Continuity date:** 2026-08-28
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `5d2bca711f528ab1bb607104379af503ff175697`
**Production tree:** `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last evidence:** `R3.18BC — Outcome A / 37 false terminators + 3 exact following headers / contexts=3 / artifact 9666964713`
**Last contract:** `R3.18BD — Outcome A / exact_tuple_only / 3 eight-field tuples / contract 33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`
**Current exact pass:** `R3.18BE — bounded post-BA mixed-continuation following-header production`

## Truthful boundary

R3.18BA remains production. R3.18BC proved the immutable forty-row split exactly: 37 false terminators and three true rows, each with one native header matching pinned Boxcars through `payload_start`. R3.18BD freezes only the three observed complete eight-field contexts:

```text
(72,  6, 92, Boolean, 868, 32, 10, false) x1
(72,  6, 94, Boolean, 868, 32, 10, false) x1
(110, 6, 58, Float,   868, 32, 10, false) x1
```

The contract is `exact_tuple_only`; the 37 false rows contribute no header membership. AT/AJ/Z/P contracts are history/methodology only and are not inherited.

## Current gate

R3.18BE may validate/recompute one published BA mixed control. False must return a successful no-header terminator with zero following-header reads. True may compose exactly one existing-actor header with the stateless primitive, require exact R3.18BD membership, and stop at `payload_start`.

## Hard stop

No following payload, second later control, false-row header synthesis, context outside exact BD membership, generalized cursor, or actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
