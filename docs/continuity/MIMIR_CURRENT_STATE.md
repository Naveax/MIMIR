# MIMIR — Current Canonical State

**Continuity date:** 2026-08-26
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `e1ccbef95c8424b689dee7d77fd8fde2af3e0204`
**Production tree:** `4e7100625096594bcc5c5b4c6a8054c283643b13`
**Production milestone:** `R3.18AQ — bounded post-AN mixed following-control production`
**Last read-only evidence:** `R3.18AS — Outcome A / false terminators 7/7 / true headers exact 40/40 / 16 exact eight-field contexts / Int=40 / artifact 9603335255`
**Last completed contract:** `R3.18AT — exact_tuple_only / 16 eight-field contexts / multiplicity 40 / 7 false terminators outside membership / sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5`
**Current exact pass:** `R3.18AU — bounded post-AQ mixed-continuation following-header production`

## Truthful boundary

R3.18AQ remains canonical production. R3.18AS proved exactly one following header on the immutable forty true continuation rows while preserving seven false terminators. R3.18AT freezes only the sixteen complete eight-field tuples observed there.

```text
AS evidence head/tree                 475650fea59332f74b9f69da50e3e4471622ab7e / 1303071ad3031f4095e29d775afd243286a67b64
AS artifact                           9603335255 / sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
AS false / true                       7 / 40
AS exact true headers                 40/40
AS native/oracle mismatch             0
AT contract                           sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
AT membership                         exact_tuple_only
AT exact contexts                     16/16
AT multiplicity sum                   40
AT tuple fields                       bound,width,object,tag,version major/minor,net version,is_rl_223
AT false terminators in membership    0 / 7 remain terminators
AT AJ/Z/P inheritance                 false/false/false
production mutation                   0
```

## Current gate

R3.18AU is a bounded production implementation. It must recompute/validate the supplied AQ prior. A false AQ result stays a successful terminator and must not perform header lookup. A true AQ result may compose exactly one following header using the existing stateless primitive only if the complete header context is an exact R3.18AT member, then must stop at `payload_start`.

## Hard stop

Do not decode the following payload, read a second later control, admit a context outside R3.18AT, synthesize a header for a false terminator, drop/flip the RL223 field, create a generalized/repeated property cursor, or widen actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior.
