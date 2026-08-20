# MIMIR R3.18AJ — Post-AG Following-Header Exact-Context Contract

**Status:** ACTIVE
**Pass type:** contract-only admission
**Evidence authority:** R3.18AI Outcome A
**Production authority:** R3.18AG `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`
**Production mutation:** forbidden
**Payload decode:** forbidden
**Another control bit:** forbidden

## 1. Goal

Turn the R3.18AI one-following-header structural observation into the narrowest explicit boundary-specific contract. Preserve the complete seven-field identity and exact observed multiplicities. Do not import the earlier R3.18Z or R3.18P header contracts merely because some components may look familiar.

## 2. Frozen evidence authority

```text
canonical admission parent           b419503b5ceb8c44af207f645232570b1c9f2e6d / 8bcdedf47233b0e6db605c6c532677d0f8166801
production SHA/tree                  2d351e8ceb601e2fbe515d2977b2103a4b2c7976 / 4123820ce6537f2d4942cd0b5f72b52e43b96c1d
production lib/test blobs            db923ebcb419d278f4ab0144fe7ed15b298b60fa / 3f3e1c8f3f6deb7f2558862a1032f8a102131443
R3.18AI execution spec blob          dd064744b86ce4718d389c2bd4bf080b962b16d7
R3.18AI evidence head/tree           9d424dae2ed8cc7a0a6868111805a48763131196 / b2fa45cff46c81e0458423d6aa3d9f630e2182a3
R3.18AI authority                    32418184036 / 96584056481 SUCCESS
R3.18AI same-head CI                 32420217393 / 96590396395 SUCCESS
R3.18AI artifact                     9424764320 / 12054 / sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5
header summary / rows / aggregate    70ffb419d294d4e02bdd2ef843c84bcda466022d627d7dec0b736e8d19228dd1 / 5dc8550d63688b263d87532f8330b3791736f04af98b0962cd91bd378fc4b8da / be2593e55bce17b03bd994b98dff5e9e25a4fcb9ee40c685947bc05181925135
rows / exact contexts                47 / 17
observed tags                        Int=47
earlier-header inheritance assumed  0
```

Witness reselection, context synthesis from older boundaries, and production mutation are forbidden.

## 3. Required contract artifact

Create `docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json` with:

- schema version and a boundary-specific post-AG contract name;
- membership policy `exact_tuple_only`;
- tuple fields exactly `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)`;
- observed row count 47;
- unique exact context count 17;
- exact R3.18AI authority receipts and payload hashes;
- exactly the 17 observed tuples and their exact observed multiplicities;
- explicit anti-widening flags, including no R3.18Z/R3.18P inheritance.

## 4. Admission semantics

Membership is full seven-field tuple equality only. Multiplicity is evidence provenance, not a runtime frequency guarantee.

The following are not admitted:

- tag-only membership, even though all current rows are `Int`;
- object/bound/width component membership;
- Cartesian products of individually observed components;
- versionless membership;
- R3.18Z or R3.18P tuple inheritance, union, or substitution by assumption;
- any tuple outside the exact 17-entry R3.18AI set.

## 5. Required negatives

At minimum prove:

1. exact 17/17 tuple equality against the immutable R3.18AI header summary;
2. exact 17/17 multiplicities and total sum 47;
3. tag-only candidate rejection;
4. component-only candidate rejection;
5. fabricated Cartesian candidate rejection;
6. version-drop candidate rejection;
7. an eighteenth fabricated tuple is rejected;
8. at least one earlier R3.18Z/R3.18P-valid but R3.18AJ-absent tuple is rejected at this boundary;
9. production/Cargo/fixture/corpus/support mutation remains 0/0/0/0/0.

## 6. Clean scope

Contract/continuity docs only. No Rust production source, tests, dependency, fixture, corpus, workflow, support-lane or runtime/export expansion may enter the clean contract commit.

## 7. Hard stop

R3.18AJ does not publish a header decoder/composition. The following payload, another property control, repeated/generalized property loops/cursors, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual and runtime/export layers remain closed.

## 8. Outcome gate

### Outcome A
Admit the exact boundary-specific 17-tuple contract with all anti-widening negatives PASS. Production remains R3.18AG. Open R3.18AK as a separate bounded production composition for exactly one post-AG following header, requiring exact R3.18AJ membership and stopping at `payload_start`.

### Outcome B
A bounded discrepancy in tuple identity or multiplicity is isolated. Admit only the supported subset and keep production unchanged.

### Outcome C
Any authority drift, earlier-contract inheritance, tuple widening, payload/control access or production mutation. Stop without admission.
