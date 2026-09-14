# MIMIR R3.18BX — Exact Following-Header Context Contract Decision

**Date:** 2026-09-14
**Outcome:** **A — ADMITTED / BOUNDARY-SPECIFIC EXACT-EIGHT-FIELD CONTRACT**
**Production changed:** **NO**
**Canonical production:** R3.18BU `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`
**Contract:** `docs/continuity/MIMIR_R3_18BX_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576`

## Decision

R3.18BX closes Outcome A. Exactly the one complete eight-field context proven by R3.18BW is admitted with exact tuple equality and observed multiplicity one. The sole BU=false row remains a terminator outside header membership.

No tag-only, component-only, property-ordinal-only, Cartesian, versionless, RL223-dropped/flipped, historical-contract-inherited or fabricated membership is admitted. Multiplicity is evidence provenance, not a runtime-frequency promise.

## Frozen contract

```text
membership policy                     exact_tuple_only
frozen control rows                   2
false terminators                     1
observed header rows                  1
unique exact contexts                 1
multiplicity                          1
property ordinal                      8 on 1/1
production/Cargo/fixture/corpus/support 0/0/0/0/0
```

Exact admitted context:

```text
(110, 6, 67, LoadoutsOnline, 868, 32, 10, false) x1
```

## Validation receipts

```text
candidate head/tree                   6520e8c8aa47d14f8c2b457b7552aa6fb763d5fd / 757fcf1824a9c0c82d92ef21c7b46498af15db3b
candidate contract sha256             18dad57f84f1bf6d43ec1270c800fb0158f494b4c10d1156e0de5f6c6adb5851
candidate CI                          34844530873/103977139973 SUCCESS
candidate knowledge archive           34844530915/103977139602 SUCCESS
validation-only PR                    #221
validation PR CI                      34844544326/103977183134 SUCCESS
validation PR knowledge               34844544534/103977183772 SUCCESS
exact prevalidation                   34844773598/103977940876 SUCCESS
BW evidence                           778b12988046da4d186248877bd577eb2a533a58 / 34843377101/103973337631 SUCCESS
BW same-head CI                       34843377045/103976995152 SUCCESS
BW artifact                           10346819501 / sha256:ee8a1878241b45765a7fa57c64c179c40090836096055fc5626a58724b5796fd
final admitted contract sha256        37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576
```

## Sequencing consequence

The next pass is **R3.18BY — Bounded Post-BU Mixed-Continuation Following-Header Production**.

R3.18BY may validate/recompute one exact published BU result. A false BU result must return a successful no-header terminator with zero post-BU reads. A true result may decode exactly one following existing-actor header suffix, require exact R3.18BX membership, and stop exactly at `payload_start`.

## Hard stop

No following payload, no second later property-control bit, no header synthesis on the false terminator, no context outside exact R3.18BX membership, no repeated/generalized property loop/cursor, and no wider semantic/runtime layer.
