# MIMIR R3.18Z — After-R3.18W Following-Header Exact-Context Contract

**Status:** ACTIVE
**Pass type:** contract-only admission
**Evidence authority:** R3.18Y Outcome A
**Production authority:** R3.18W `58872e94f00ef094807f21ab2ff984ac66b97d91`
**Production mutation:** forbidden
**Payload decode:** forbidden
**Another control bit:** forbidden

## 1. Goal

Turn the R3.18Y structural observation into the narrowest explicit contract for exactly one following property header after the published R3.18W true control. The contract must preserve the complete seven-field identity and exact observed multiplicities without importing R3.18P semantics from the earlier boundary.

## 2. Frozen evidence authority

```text
R3.18Y evidence head/tree           413d6c24f8f390a57c21ed345f3f868c263f413c / c48630bf89c23a8348936f2adbb8f0c9ad0c977b
R3.18Y authority                    32076198677 / 95529856476 SUCCESS
R3.18Y same-head CI                 32076881407 / 95531867271 SUCCESS
R3.18Y artifact                     9303584468 / 19642 / sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29
header summary / rows / aggregate   035e56fcdfb643aec00e7474fddfc378afb8f8e4e9ad531c532159f0111a591f / 0bfb38ca10d329d7c8cb66cee57449c17108213c9588a64d0ed4b511afbe9d47 / 618ac3901b46c04732d57469b583ba2187bfe1007c3ff210094039cfc2e63082
rows / exact contexts               47 / 18
observed tags                       ActiveActor=39 / Int=7 / UniqueId=1
R3.18P inheritance assumed          0
```

## 3. Required contract artifact

Create `docs/continuity/MIMIR_R3_18Z_ADMITTED_HEADER_CONTEXTS.json` with:

- schema version and boundary-specific contract name;
- membership policy `exact_tuple_only`;
- tuple fields exactly `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)`;
- observed row count 47;
- unique exact context count 18;
- exact R3.18Y authority receipts and hashes;
- exactly the 18 observed tuples and exact observed multiplicities;
- explicit anti-widening flags.

## 4. Admission semantics

Membership is full tuple equality only. Multiplicity is evidence provenance, not a runtime frequency promise.

The following are not admitted:

- tag-only membership;
- object/bound/width component membership;
- Cartesian products of observed components;
- versionless membership;
- R3.18P tuple inheritance or union by assumption;
- any tuple outside the exact 18-entry set.

## 5. Required negatives

At minimum prove:

1. exact 18/18 tuple equality against R3.18Y summary;
2. exact 18/18 multiplicities and sum 47;
3. tag-only candidate rejection;
4. component-only candidate rejection;
5. fabricated Cartesian candidate rejection;
6. version-drop candidate rejection;
7. nineteenth-tuple candidate rejection;
8. an R3.18P-valid but R3.18Z-absent tuple is rejected at this later boundary;
9. production/Cargo/fixture/corpus/support mutation remains 0/0/0/0/0.

## 6. Clean scope

Contract/continuity docs only. No Rust production source, test semantics, dependency, fixture, corpus, workflow or support expansion may enter the clean contract commit.

## 7. Hard stop

R3.18Z does not publish a header decoder/composition at this boundary. Following payload, another property control, repeated/generalized property loops/cursors, next actor/frame/lifecycle and semantic/runtime/export layers remain closed.

## 8. Outcome gate

### Outcome A
Admit the exact boundary-specific 18-tuple contract with all anti-widening negatives PASS. Production remains R3.18W. Open R3.18AA as a separate bounded production composition for exactly one post-W following header, requiring exact R3.18Z membership and stopping at `payload_start`.

### Outcome B
A bounded discrepancy in tuple identity or multiplicity is isolated. Admit only the supported subset and keep production unchanged.

### Outcome C
Any authority drift, R3.18P inheritance, tuple widening, payload/control access or production mutation. Stop without admission.
