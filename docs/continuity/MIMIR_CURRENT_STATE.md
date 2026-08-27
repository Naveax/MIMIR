# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `5d2bca711f528ab1bb607104379af503ff175697`
**Production tree:** `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last read-only evidence/audit:** `R3.18BC — Outcome A / one following header exact 3/3 / contexts=3 / artifact 9666964713`
**Current exact pass:** `R3.18BD — exact following-header context contract`

## Truthful boundary

R3.18BA remains canonical production. R3.18BC independently closed the next one-header evidence boundary without changing production.

```text
BC evidence head/tree                  0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
authority run/job                      33122152803 / 98691409657 SUCCESS
same-head natural CI                   33122152793 / 98691409674 SUCCESS
artifact                               9666964713 / 7795
artifact SHA-256                       88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
inner manifest                         14/14 PASS
source partition                       40/40
false terminators / true headers       37 / 3
native/Boxcars exact                   3/3
unique exact contexts                  3
mismatch / reselection                 0 / 0
payload / second-control bits          0 / 0
mutation                               0/0/0/0/0
privacy                                PASS
```

Exact observed complete contexts, each x1:

```text
(72,  6, 92, Boolean, 868, 32, 10, false)
(72,  6, 94, Boolean, 868, 32, 10, false)
(110, 6, 58, Float,   868, 32, 10, false)
```

Tuple fields are `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)`.

## Current gate

R3.18BD is contract-only. Freeze exact eight-field equality for only those three contexts and preserve all 37 false terminators outside membership. Reject component/tag/Cartesian/versionless/RL223/older-contract widening. Production remains R3.18BA.

## Hard stop

No production following-header composition, no following payload, no second later control, no generalized/repeated property cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
