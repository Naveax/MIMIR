# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `5d2bca711f528ab1bb607104379af503ff175697`
**Production tree:** `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last read-only evidence/audit:** `R3.18BB — Outcome A / published BA exact 40/40 / false=37 true=3 / mismatch 0 / reselection 0 / artifact 9659874105`
**Current exact pass:** `R3.18BC — one following-property-header evidence after published BA mixed control`

## Truthful boundary

R3.18BA remains canonical production. It validates/recomputes one exact R3.18AY Int/32 payload composition, begins at the AY stop, consumes exactly one following LSB-first `property_present` bit, accepts both frozen R3.18AX classes, and stops exactly one bit later.

R3.18BB independently closed Outcome A against the immutable forty-row AX authority:

```text
evidence head/tree                     91595db2970ad395ec048ebd9326cfa97b01b38a / 40672cd1b546bca2b73ca252d727aa88ca9faec1
authority run/job                      33104207616 / 98629573433 SUCCESS
same-head natural CI                   33104207621 / 98629573926 SUCCESS
artifact                               9659874105 / 9295
artifact SHA-256                       0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e
internal manifest                      11/11 PASS
published BA exact                     40/40
AY prerequisite exact                  40/40
false / true                           37 / 3
mismatch / reselection                 0 / 0
adjacent stream/header/payload/second  0/0/0/0
mutation                               0/0/0/0/0
privacy                                PASS
```

The exact pre-control bit truncation claim remains inherited from R3.18AX 40/40 because all forty control starts are non-byte-aligned; BB separately proves byte-slice carrier truncation fails closed.

## Current gate

R3.18BC is evidence-only. Preserve all forty BB identities. The 37 false rows are strict terminators and perform zero following-header access. On only the exact three frozen true rows, observe one following property header through `payload_start`, compare native MIMIR structure with pinned Boxcars, classify complete contexts/tags without pre-assuming them, and stop.

Frozen true identities:

```text
external_fixtures/sample_002.replay                                      BA stop 11224
external_fixtures/sample_003.replay                                      BA stop 7808
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay BA stop 3160
```

## Hard stop

No following payload decode, no second later control, no production following-header composition, no generalized/repeated property cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
