# MIMIR R3.18Z — After-R3.18W Following-Header Exact-Context Contract Decision

**Date:** 2026-08-18
**Outcome:** **A — ADMITTED / BOUNDARY-SPECIFIC EXACT-TUPLE CONTRACT**
**Production mutation:** none
**Canonical production:** `58872e94f00ef094807f21ab2ff984ac66b97d91` / `d6965d77903ea99dad0465bb350b6a673ee7dd00`
**Contract:** `docs/continuity/MIMIR_R3_18Z_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9`

## Decision

R3.18Z closes Outcome A. The exact R3.18Y one-header observation has been crystallized into a boundary-specific contract containing exactly 18 complete seven-field tuples with observed multiplicities summing to 47. Membership is `exact_tuple_only`.

The earlier R3.18P contract is not inherited at this later boundary. Tag-only, component-only, Cartesian-product, versionless and any outside-tuple membership are rejected. Multiplicity remains provenance only and is not a runtime-frequency promise.

## Exact authority

```text
canonical main before admission     ff69da3ce17d3632cfa544190a515a227f6e65f2 / 140c6f8fa386f93eb60843321572b5cc7ae75de2
production SHA/tree                 58872e94f00ef094807f21ab2ff984ac66b97d91 / d6965d77903ea99dad0465bb350b6a673ee7dd00
R3.18Y evidence head/tree           413d6c24f8f390a57c21ed345f3f868c263f413c / c48630bf89c23a8348936f2adbb8f0c9ad0c977b
R3.18Y authority                    32076198677 / 95529856476 SUCCESS
R3.18Y same-head CI                 32076881407 / 95531867271 SUCCESS
R3.18Y artifact                     9303584468 / 19642 / sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29
Y header summary SHA-256            035e56fcdfb643aec00e7474fddfc378afb8f8e4e9ad531c532159f0111a591f
Y header rows SHA-256               0bfb38ca10d329d7c8cb66cee57449c17108213c9588a64d0ed4b511afbe9d47
Y aggregate SHA-256                 618ac3901b46c04732d57469b583ba2187bfe1007c3ff210094039cfc2e63082
Y manifest-file SHA-256             0de7e6cc92a748577f141108043a6db959ac281846de89a884b27619631bbbd2
Y Boxcars instrumentation SHA-256   2f219d67eaa49c3365386265784a7991534cb1ffc8e1ac69d9444cfdda73273a
R3.18P historical contract SHA-256  0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
R3.18P cross-boundary inheritance   false
admission authority                 32138284739 / 95714641485
```

## Admitted contract

```text
membership policy                   exact_tuple_only
tuple fields                        stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version
exact contexts                      18/18
observed multiplicity sum           47
ActiveActor / Int / UniqueId        39 / 7 / 1
witness reselection                 0
```

The exact tuple list and multiplicities are authoritative only through the JSON contract named above.

## Anti-widening validation

```text
exact tuple equality                PASS 18/18
exact multiplicity equality         PASS 18/18 / sum 47
tag-only membership                 REJECT
component-only membership           REJECT
Cartesian candidate                 REJECT
versionless candidate               REJECT
nineteenth tuple                    REJECT
R3.18P-valid Z-absent tuple         REJECT: (60,5,102,Boolean,868,32,10)
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

## Hard stop

R3.18Z admits a contract only. It does not publish a post-W header composition, does not decode the following payload, does not read another control bit, and does not authorize repeated/generalized property loops or cursors, next actor/frame/lifecycle work, raw-state/event materialization, replay slicing, skills, counterfactual execution or runtime/export widening.

## Next gate

R3.18AA is a separate bounded production pass. Starting only after a valid published R3.18W true control, it may decode exactly one following header with the existing stateless header primitive, require exact R3.18Z tuple membership, and stop exactly at `payload_start`. It may not decode payload or another control.
