# MIMIR R3.18AX — Next Property-Control Bit Evidence Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / READ-ONLY ONE-BIT EVIDENCE**
**Production mutation:** none
**Canonical production remains:** `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef`

## Decision

R3.18AX closes Outcome A. Exactly the forty R3.18AW payload rows were rematerialized without reselection and each exact AW Int/32 payload end was reconstructed before observation. All seven R3.18AV false terminators remained outside the target lane. Exactly one following `property_present` bit was then observed at the proven payload end with pinned Boxcars instrumentation and an independent native LSB-first observer. Start/value/end matched on 40/40 rows with mismatch zero.

The observed distribution is **false=37 / true=3**. No expected boolean ratio was inherited from R3.18AP or any earlier boundary. No following stream ID, header, payload or second later control bit was consumed.

## Exact authority

```text
canonical evidence base/tree          7741e132df86877cc26cf451f296fd7b7e9cdf30 / 38c66911494625a5ec02f4633424c5a8068a8182
production SHA/tree                   6a9f456c78ffccab177823234a8d9fe4ba59a850 / cbda5db96e88cc208f872c2237cf4741b8fcfaef
evidence head/tree                    465a3f2fc71e5eed6f00c16a04738031bef8d82c / b164a8566c6ac57ddee1aed0a7edbf9f44250488
authority run/job                     33068572230 / 98504703417 SUCCESS
same-head natural CI                  33068572200 / 98504703614 SUCCESS / count=1 / rerun=0
artifact                              9644869549 / 18070 bytes
artifact digest / ZIP SHA256          sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

The downloaded ZIP SHA-256 equals the GitHub artifact digest exactly. The ZIP contains 16 files; the SHA-256 inner manifest covers and verifies all 15 payload files.

## Frozen result

```text
AW payload rows exact                 40/40
AV false rows excluded                7/7
next control false                    37
next control true                     3
Boxcars/native exact                  40/40
mismatch                              0
expected distribution inherited       0
witness reselection                   0
next stream/header/payload/second     0/0/0/0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                               PASS
```

## Canonical sequencing consequence

R3.18AX does **not** make the control bit the next production boundary. Canonical production still stops at the R3.18AU following-header `payload_start`, because R3.18AW payload decoding is evidence-only. Therefore the next bounded production pass is R3.18AY: publish exactly one AW-admitted Int/32 payload after a valid AU/AT header and stop at payload end. Only after that payload production is independently validated may the AX mixed control semantics be considered for production in a later pass.

## Hard stop

No production control-bit consumption is admitted by AX. No payload/control access on the seven false terminators, next stream/header/payload after the AX observation, second later control, generalized property cursor, actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening, or historical AM/AN authority inheritance is admitted.
