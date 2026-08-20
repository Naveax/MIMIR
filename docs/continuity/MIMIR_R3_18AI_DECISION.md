# MIMIR R3.18AI — One Following Property-Header Evidence Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / ONE FOLLOWING HEADER EXACT**
**Production mutation:** none
**Canonical production:** `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`

## Decision

R3.18AI closes Outcome A. On exactly the immutable 47 R3.18AH/R3.18AF witnesses, MIMIR reconstructed the valid published R3.18AG true-control boundary, began exactly at that control's `stop_bit`, decoded exactly one following existing-actor property header with the existing stateless header machinery, and stopped exactly at the header `payload_start`. The independent pinned-Boxcars structural oracle matched the native result on all 47 rows with mismatch zero.

The observed later-boundary structural family contains **17 exact seven-field contexts**, all 47 rows resolving to the `Int` attribute tag. This is evidence only. It does not inherit R3.18Z or R3.18P context contracts and it does not admit a production header composition, the following payload, another control bit, a generalized property loop/cursor, next actor/frame iteration, or semantic/runtime widening.

## Exact authority

```text
canonical main before admission      b419503b5ceb8c44af207f645232570b1c9f2e6d
canonical main tree                  8bcdedf47233b0e6db605c6c532677d0f8166801
production SHA/tree                  2d351e8ceb601e2fbe515d2977b2103a4b2c7976 / 4123820ce6537f2d4942cd0b5f72b52e43b96c1d
production lib / AG test blobs       db923ebcb419d278f4ab0144fe7ed15b298b60fa / 3f3e1c8f3f6deb7f2558862a1032f8a102131443
AI execution spec blob               dd064744b86ce4718d389c2bd4bf080b962b16d7
evidence head/tree                   9d424dae2ed8cc7a0a6868111805a48763131196 / b2fa45cff46c81e0458423d6aa3d9f630e2182a3
authority run/job                    32418184036 / 96584056481 SUCCESS
validation PR                        #59 closed unmerged
same-head normal CI                  32420217393 / 96590396395 SUCCESS
artifact                             9424764320 / 12054 bytes
artifact digest / ZIP SHA-256        sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5
header rows SHA-256                  5dc8550d63688b263d87532f8330b3791736f04af98b0962cd91bd378fc4b8da
header summary SHA-256               70ffb419d294d4e02bdd2ef843c84bcda466022d627d7dec0b736e8d19228dd1
negative controls SHA-256            9cacb2a613958fe399114d3030f2fd1bba2c463c1efdb607498abf9af1ea843e
aggregate SHA-256                    be2593e55bce17b03bd994b98dff5e9e25a4fcb9ee40c685947bc05181925135
continuity builder                   32423737353 / 96601143838
```

The downloaded artifact ZIP SHA-256 equals the GitHub artifact digest exactly. Its nine payload entries all match `r3_18ai_artifact_sha256.txt` (9/9 PASS).

## Admitted evidence

```text
frozen rows                          47/47
published R3.18AG exact              47/47
one following header exact           47/47
native/oracle mismatch               0
unique exact contexts                17
observed tags                        Int=47
witness reselection                  0
repeatability                        PASS 47/47
header truncation                    PASS 47/47
corrupt AG negative                  PASS 47/47
wrong actor negative                 PASS 47/47
unresolved lookup negative           PASS 47/47
wrong context negative               PASS 47/47
post-payload-start poison            PASS 47/47
following payload bits consumed      0
second later control bits consumed   0
earlier-header contract inheritance  0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Artifact provenance

```text
frozen witnesses SHA-256             31b1b759a33a4831e0cfe0ca7028a85c2573149a0e7426bc7c9b4a59c2315019
replay identity SHA-256              b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
```

## Next gate

R3.18AJ is a separate **contract-only** admission pass. It may admit only the complete observed seven-field tuples `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)` and their exact evidence multiplicities from the immutable R3.18AI summary. Membership must be `exact_tuple_only`. R3.18Z/R3.18P contexts may not be inherited or unioned by assumption. Production remains frozen and no payload or later control bit may be consumed.
