# MIMIR R3.18BH — Next Property-Control Bit Evidence Decision

**Date:** 2026-09-07
**Outcome:** **A — ADMITTED / READ-ONLY ONE-BIT EVIDENCE**
**Production mutation:** none
**Canonical production remains:** `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`

## Decision

R3.18BH closes Outcome A on exactly the three immutable R3.18BG payload rows. Each exact BG payload end was rematerialized without witness reselection, then pinned Boxcars and an independent native LSB-first observer read exactly one following `property_present` bit. Native/oracle bit and one-bit boundary matched on 3/3 rows.

The observed distribution is **false=1 / true=2** (mixed false+true observed). No expected polarity was inherited from an earlier ordinal. No following stream ID, property header, payload, second later control bit, actor/frame state or generalized cursor state was consumed.

## Exact authority

```text
continuity authority before BH        1fbfb8f05bc4c06c21f4cfe79697bd4097b26cc0
production SHA/tree                   1d717d3e82179edd85b197968f46b8f951a3e828 / 72cf2b907437a1ba62cc9deebd7608f7d0372f81
BH execution spec blob                252a86a85ad2d7aed75796be3cd70f47aff601a9
BG evidence head                      02e1799001b670db24f1e0076f2afd6c05f5afdf
BG evidence run/job                   34112731371/101715102551 SUCCESS
BG same-head CI                       34112731358/101712578621 SUCCESS
BG artifact                           10015405999 / sha256:a43a528a49fa6d07ef1c92266c6dc9ed4ef2a3e87e7f69f65f2f40d39f3fa15a
BG inner manifest                     sha256:b06097e08cc276e80e17543f36a3ab05ac184b335ec12ded0fd460e2129d5e46
BH evidence head/tree                 c728658ac237a45f34b3af002c27f704f5293fb5 / 9761d42cd55d3152fe19653ea5be67efd826f2fa
BH authority run/job                  34132181073/101774645567 SUCCESS
BH same-head CI                       34132181159/101775846915 SUCCESS
BH artifact                           10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH artifact name                      r318bh-next-property-control-bit-evidence-v3
BH inner manifest                     sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Frozen result

```text
BG payload rows exact                 3/3
next control false                    1
next control true                     2
native/oracle exact                   3/3
native/oracle mismatch                0
witness reselection                   0
following stream/header/payload       0/0/0 bits
second later control                  0 bits
production mutation                   0
privacy                               PASS
```

## Canonical sequencing consequence

R3.18BH does **not** make the control bit a production capability. Canonical production still stops at the R3.18BE following-header `payload_start`, because R3.18BG payload decoding is evidence-only. Consistent with the earlier R3.18AW → R3.18AX → R3.18AY sequencing rule, the next bounded production pass is **R3.18BI**: publish exactly one BG-admitted primitive payload after a valid BE/BD header and stop at payload end. Only after that payload production is independently differential-tested may the BH control semantics be considered for production in a later separate pass.

## Hard stop

No BH control-bit production consumption, no stream/header/payload after BH, no second later control, no payload/control access on the 37 BF-false rows or 7 upstream AU-false rows, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
