# MIMIR R3.18AJ — Post-AG Following-Header Exact-Context Contract Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / BOUNDARY-SPECIFIC EXACT-TUPLE CONTRACT**
**Production mutation:** none
**Canonical production:** `2d351e8ceb601e2fbe515d2977b2103a4b2c7976` / `4123820ce6537f2d4942cd0b5f72b52e43b96c1d`
**Contract:** `docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c`

## Decision

R3.18AJ closes Outcome A. The immutable R3.18AI one-following-header observation has been crystallized into a boundary-specific contract containing exactly **17 complete seven-field tuples** with exact observed multiplicities summing to **47**. Membership is `exact_tuple_only`; all 47 observed rows are `Int` at this boundary.

Earlier R3.18Z and R3.18P contracts are not inherited, unioned or substituted at the post-AG boundary. Tag-only, component-only, Cartesian-product, versionless, fabricated and outside-tuple membership are rejected. Multiplicity is evidence provenance only, never a runtime-frequency promise.

## Exact authority

```text
canonical main before admission     a048ba25f2ef023d07bab17716838f1c4777fe27 / cd00dd18da0a177415ce569b7909ec6390cbb252
production SHA/tree                 2d351e8ceb601e2fbe515d2977b2103a4b2c7976 / 4123820ce6537f2d4942cd0b5f72b52e43b96c1d
production lib / AG test blobs      db923ebcb419d278f4ab0144fe7ed15b298b60fa / 3f3e1c8f3f6deb7f2558862a1032f8a102131443
AI evidence head/tree               9d424dae2ed8cc7a0a6868111805a48763131196 / b2fa45cff46c81e0458423d6aa3d9f630e2182a3
AI authority                        32418184036 / 96584056481 SUCCESS
AI validation PR / CI               #59 closed unmerged / 32420217393/96590396395 SUCCESS
AI artifact                         9424764320 / 12054 / sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5
AI header summary SHA-256           70ffb419d294d4e02bdd2ef843c84bcda466022d627d7dec0b736e8d19228dd1
AI header rows SHA-256              5dc8550d63688b263d87532f8330b3791736f04af98b0962cd91bd378fc4b8da
AI aggregate SHA-256                be2593e55bce17b03bd994b98dff5e9e25a4fcb9ee40c685947bc05181925135
AI published-main CI                32424170707/96602481420 SUCCESS
AI published-main Knowledge Archive 32424170684/96602481274 SUCCESS
AI published-run discovery          32424285013/96602844100 SUCCESS / artifact 9426876000
R3.18Z historical contract SHA-256  81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18P historical contract SHA-256  0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
AJ admission builder                32452755935/96684134535
```

## Admitted contract

```text
membership policy                   exact_tuple_only
tuple fields                        stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version
exact contexts                      17/17
observed multiplicity sum           47
observed tags                       Int=47
witness reselection                 0
R3.18Z inheritance                  false
R3.18P inheritance                  false
```

The exact tuple identities and multiplicities are authoritative only through the JSON contract named above.

## Anti-widening validation

```text
exact tuple equality                PASS 17/17
exact multiplicity equality         PASS 17/17 / sum 47
tag-only membership                 REJECT
component-only membership           REJECT
Cartesian candidate                 REJECT: (60,5,68,Int,868,32,10)
versionless candidate               REJECT
fabricated eighteenth tuple         REJECT: (60,5,39,Int,868,32,10)
R3.18Z-valid AJ-absent tuple         REJECT: (60,5,34,ActiveActor,868,32,10)
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

## Hard stop

R3.18AJ admits a contract only. It does not publish a post-AG header composition, decode the following payload, read another property-control bit, or authorize repeated/generalized property loops/cursors, next actor/frame/lifecycle work, raw-state/event materialization, replay slicing, skills, counterfactual execution or runtime/export widening.

## Next gate

R3.18AK is a separate bounded production pass. Starting only after a valid published R3.18AG true-control result, it may decode exactly one following existing-actor property header with the existing stateless header primitive, require exact R3.18AJ tuple membership, and stop exactly at `payload_start`. It may not decode payload or another control.
