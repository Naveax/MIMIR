# MIMIR R3.18Y — One Following Property Header Evidence Decision

**Date:** 2026-08-18
**Outcome:** **A — ADMITTED / READ-ONLY HEADER DOMAIN CHARACTERIZED**
**Production mutation:** none
**Canonical production:** `58872e94f00ef094807f21ab2ff984ac66b97d91` / `d6965d77903ea99dad0465bb350b6a673ee7dd00`

## Decision

R3.18Y closes Outcome A. On exactly the immutable 47 R3.18X/R3.18V witnesses, starting at the published R3.18W stop, pinned Boxcars and an independent native observer agreed on exactly one following existing-actor property header through `payload_start`. Native/oracle mismatch is 0, witness reselection is 0, following-payload consumption is 0 and another-control consumption is 0.

The later boundary is structurally different from R3.18P. R3.18P inheritance was not assumed. R3.18Y observed exactly 18 full seven-field tuples with multiplicities summing to 47 and tag counts `ActiveActor=39`, `Int=7`, `UniqueId=1`.

## Exact authority

```text
base main/tree                      d0f2678271984acf5dc69f6456ccaaf443bb3113 / 0c2694f49427d34c5219eb921ed1c8c66cae30d5
production SHA/tree                 58872e94f00ef094807f21ab2ff984ac66b97d91 / d6965d77903ea99dad0465bb350b6a673ee7dd00
evidence head/tree                  413d6c24f8f390a57c21ed345f3f868c263f413c / c48630bf89c23a8348936f2adbb8f0c9ad0c977b
authority run/job                   32076198677 / 95529856476 SUCCESS
same-head normal CI                 32076881407 / 95531867271 SUCCESS
CI-only PR                          #30 CLOSED / NOT MERGED
artifact                            9303584468 / 19642 bytes
artifact digest / ZIP SHA-256       sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29
header summary SHA-256              035e56fcdfb643aec00e7474fddfc378afb8f8e4e9ad531c532159f0111a591f
header rows SHA-256                 0bfb38ca10d329d7c8cb66cee57449c17108213c9588a64d0ed4b511afbe9d47
aggregate SHA-256                   618ac3901b46c04732d57469b583ba2187bfe1007c3ff210094039cfc2e63082
manifest-file SHA-256               0de7e6cc92a748577f141108043a6db959ac281846de89a884b27619631bbbd2
Boxcars instrumentation SHA-256     2f219d67eaa49c3365386265784a7991534cb1ffc8e1ac69d9444cfdda73273a
admission authority                 32077577039 / 95533900890
```

The artifact manifest verified 9/9 evidence payload files. The ZIP SHA-256 equals the GitHub artifact digest.

## Exact observed tuples

Tuple order is `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)`.

```text
(60,5,34,ActiveActor,868,32,10) x1
(60,5,43,ActiveActor,868,32,10) x2
(60,5,80,ActiveActor,868,32,10) x4
(60,5,81,ActiveActor,868,32,10) x19
(60,5,84,Int,868,32,10) x6
(60,5,87,ActiveActor,868,32,10) x1
(60,5,87,Int,868,32,10) x1
(60,5,89,ActiveActor,868,32,10) x2
(60,5,91,ActiveActor,868,32,10) x1
(60,5,96,ActiveActor,868,32,10) x1
(60,5,104,ActiveActor,868,32,10) x2
(60,5,105,ActiveActor,868,32,10) x1
(60,5,108,ActiveActor,868,32,10) x1
(60,5,118,ActiveActor,868,32,10) x1
(67,6,63,ActiveActor,868,32,10) x1
(72,6,65,ActiveActor,868,32,10) x1
(72,6,68,ActiveActor,868,32,10) x1
(110,6,25,UniqueId,868,32,10) x1
```

## Admitted evidence

```text
frozen rows                         47/47
unique exact contexts               18
multiplicity sum                    47
ActiveActor / Int / UniqueId        39 / 7 / 1
native/oracle mismatch              0
witness reselection                 0
repeatability                       PASS 47/47
property truncation                 PASS 47/47
stream truncation                   PASS 47/47
prior W stop negative               PASS 47/47
wrong actor                         PASS 47/47
unresolved lookup                   PASS 47/47
wrong context                       PASS 47/47
post-payload_start poison           PASS 47/47
following payload bits consumed     0
another control bits consumed       0
R3.18P inheritance assumed          0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                             PASS
```

## Hard stop

R3.18Y admits evidence only. It does not admit any tuple as a production allowlist yet, does not inherit R3.18P, does not decode the following payload, does not read another property control, and does not create a repeated/generalized property cursor or widen actor/frame/lifecycle/raw-state/event/slice/skill/counterfactual/runtime/export behavior.

## Next gate

R3.18Z is a separate contract-only pass. It may crystallize only the exact 18 seven-field tuples and their 47 observed multiplicities into a boundary-specific exact-tuple contract. Tag-only, component-only, Cartesian-product, versionless, R3.18P cross-boundary inheritance and any nineteenth tuple must remain rejected. Production remains R3.18W.
