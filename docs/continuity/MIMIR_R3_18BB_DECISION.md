# MIMIR R3.18BB — Published R3.18BA Mixed Following-Control Differential Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL CLOSED**
**Canonical production:** unchanged at R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Canonical continuity base:** `2bb5c48b3f627d6fe4f8ae6cb2eb2ea87408342e` / `7958e09ee5756d826307ac8b122fd748f43b8a23`

## Decision

R3.18BB closes Outcome A. Published R3.18BA matches exactly the immutable forty-row R3.18AX one-bit authority. The published BA result preserves the exact R3.18AY prerequisite and matches the frozen control start, boolean value, one-bit end, and final stop on all forty witnesses without reselection.

The frozen mixed distribution remains **false=37 / true=3**. The 37 false rows terminate at the BA stop. The exact three true rows are continuation candidates for a later separate header-evidence pass only. BB decodes no following stream ID, header, payload, or second later control.

## Exact authority

```text
production SHA/tree                    5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
continuity base/tree                   2bb5c48b3f627d6fe4f8ae6cb2eb2ea87408342e / 7958e09ee5756d826307ac8b122fd748f43b8a23
evidence head/tree                     91595db2970ad395ec048ebd9326cfa97b01b38a / 40672cd1b546bca2b73ca252d727aa88ca9faec1
workflow / runner blobs                8ae3f5418433a50ab8e0daf468c5e60015725a59 / 85f13b66d21809efc1e3f1cdd001bfdda6fc6fbe
authority run/job                      33104207616 / 98629573433 SUCCESS
same-head natural CI                   33104207621 / 98629573926 SUCCESS
artifact                               9659874105 / 9295 bytes
artifact SHA-256                       0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e
artifact manifest SHA-256              469e5e09e4299dad9d5c7990a8672b931530de68504b29a083d0dd50535d3894
AX source authority                    465a3f2fc71e5eed6f00c16a04738031bef8d82c / 33068572230/98504703417
AX artifact                            9644869549 / 18070 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
```

The downloaded authoritative ZIP matched GitHub artifact metadata byte-for-byte and its internal manifest recomputed **11/11** payload hashes successfully.

## Frozen result

```text
frozen witnesses                       40/40
published BA exact                     40/40
AY prerequisite exact                  40/40
control false                          37
control true                            3
mismatch                                0
witness reselection                     0
repeatability                          40/40 PASS
post-stop poison                       40/40 PASS
upstream AU false terminators          7/7 excluded
wrong actor                            PASS
unresolved lookup                      PASS
wrong exact context                    PASS
corrupt AY prior                       PASS
carrier truncation                     PASS / fail closed
exact pre-control truncation           inherited R3.18AX PASS 40/40
next stream/header/payload/second      0/0/0/0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                                PASS
```

All forty frozen control starts are non-byte-aligned. Therefore BB preserves R3.18AX as the exact bit-level truncation authority instead of fabricating a partial-byte EOF claim through the production `&[u8]` API.

## Superseded non-authority attempt

The first evidence head `a8ed349204d2a72f404ade717aba58fdbdfde815` / run `33103836525` is **not scientific authority**. Authority freeze and the forty-row differential/focused semantics passed, but the helper omitted the Rust 1.85 `rustfmt` component and failed before full validation. Its only artifact is the explicit non-authority failure receipt `9659612921` / 300 bytes / `sha256:987312289f9d8d73608247b37136ab488547e31ff2ba5e9d9ea866b898c061ab`. It was not rerun; v2 used a fresh sibling SHA with only the toolchain-component correction.

## Hard stop

R3.18BB admits no following header. The 37 false rows remain terminators. The exact three true rows authorize only a separate read-only evidence candidate. No following payload, second later control, generalized/repeated property cursor, next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted.

## Next gate

R3.18BC is read-only one-following-property-header evidence on exactly the three frozen BB/AX true witnesses. It must reconstruct published BA exactly, keep all 37 false rows as no-header terminators, observe exactly one following header on the three true rows through `payload_start`, compare native MIMIR structure with pinned Boxcars, discover rather than pre-assume exact header contexts/tags, and consume zero following-payload or second-control bits.
