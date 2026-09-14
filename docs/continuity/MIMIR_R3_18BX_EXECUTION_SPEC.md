# MIMIR R3.18BX — Exact Following-Header Context Contract After R3.18BW

**Status:** CLOSED / OUTCOME A
**Pass type:** contract-only admission
**Evidence authority:** R3.18BW Outcome A
**Production authority:** R3.18BU `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later property-control bit:** forbidden

## Goal

Freeze the narrowest exact-context contract supported by the immutable R3.18BW two-row lane. The BU=false row remains a terminator outside membership; the BU=true row contributes exactly one complete eight-field following-header context.

## Frozen authority

```text
canonical continuity base             64f81e106338493476954f207a997a2bc7c25c9a / 3f023aa0fb0f4d1c695b5d1e3eaab7b3321ff797
production SHA/tree                   43c5d6248e2ea606b2eb0fd95f5c50758c372356 / d1b7b40ed4e361d9c047e0494fb821688ef7d7b4
BW evidence head/tree                 778b12988046da4d186248877bd577eb2a533a58 / 5a6e7bd95c95f3e38db34a543b396aec747db985
BW evidence run/job                   34843377101/103973337631 SUCCESS
BW same-head natural CI               34843377045/103976995152 SUCCESS
BW artifact                           10346819501 / 3582 / sha256:ee8a1878241b45765a7fa57c64c179c40090836096055fc5626a58724b5796fd
BX candidate head/tree                6520e8c8aa47d14f8c2b457b7552aa6fb763d5fd / 757fcf1824a9c0c82d92ef21c7b46498af15db3b
BX candidate contract                 sha256:18dad57f84f1bf6d43ec1270c800fb0158f494b4c10d1156e0de5f6c6adb5851
BX candidate CI                       34844530873/103977139973 SUCCESS
BX candidate knowledge archive        34844530915/103977139602 SUCCESS
BX validation PR                      #221
BX validation PR CI                   34844544326/103977183134 SUCCESS
BX validation PR knowledge archive    34844544534/103977183772 SUCCESS
BX exact prevalidation                34844773598/103977940876 SUCCESS
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Exact admitted membership

```text
(110, 6, 67, LoadoutsOnline, 868, 32, 10, false) x1
```

Tuple field order:

```text
stream_id_bound, prop_id_bits, property_object_index, attribute_tag,
version_major, version_minor, net_version, is_rl_223
```

Membership is complete eight-field equality only. Tag-only, property-object-only, ordinal-only, versionless, Cartesian, RL223-dropped/flipped, R3.18BN/BD/AT inherited, or fabricated membership is forbidden.

## Required and satisfied gates

- immutable BW evidence exact and artifact reverified;
- same-head BW natural CI SUCCESS;
- source control partition 2 = one false terminator + one true header;
- exact context 1/1 and multiplicity one;
- false terminator outside membership;
- candidate repository CI and knowledge archive SUCCESS;
- validation-only PR CI and knowledge archive SUCCESS;
- dedicated exact prevalidation SUCCESS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## Outcome

Outcome A admits exactly one complete eight-field context with observed multiplicity one. Production remains R3.18BU. A separate R3.18BY pass may compose at most one following header after a validated BU result, returning the BU=false row as a no-header terminator and requiring exact R3.18BX membership on the BU=true row.

## Hard stop

No production mutation in R3.18BX, no following payload, no second later control, no false-terminator header synthesis, no context widening and no generalized/repeated property cursor.
