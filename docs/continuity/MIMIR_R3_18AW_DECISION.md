# MIMIR R3.18AW — One Following Primitive Payload Evidence Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / READ-ONLY PAYLOAD EVIDENCE**
**Production mutation:** none
**Canonical production remains:** `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef`

## Decision

R3.18AW closes Outcome A. Exactly the forty R3.18AV true continuation rows were rematerialized from the admitted AV artifact; all seven AV-false terminators were excluded before payload decoding. Each current following header was `Int`, and exactly one 32-bit scalar beginning at the proven payload boundary was decoded with the published native primitive scalar decoder and independently measured with pinned Boxcars. Native and oracle tag/start/end/width/value matched on 40/40 rows with mismatch zero. Privacy-safe semantic values ranged from 5 through 300.

No next property-control bit was consumed. R3.18AW is evidence only and does not publish a following-payload production composition.

## Exact authority

```text
canonical parent main/tree           b745b7eebdea325015d006ecf84efe1d14f4e827 / 46271056bc2563cf0cf66a0076bf3849816d2cec
production SHA/tree                  6a9f456c78ffccab177823234a8d9fe4ba59a850 / cbda5db96e88cc208f872c2237cf4741b8fcfaef
evidence head/tree                   5f1d983a7b67f84293f337f23b7e7c25fee48795 / 63cbbb752100ef6944b1ecf366e89854e0f2376a
authority run/job                    33064535889 / 98491267256 SUCCESS
same-head natural CI                 33064535850 / 98491266948 SUCCESS / count=1 / rerun=0
artifact                             9643254651 / 23599 bytes
artifact digest / ZIP SHA256         sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

The downloaded ZIP SHA-256 equals the GitHub artifact digest exactly. Its internal SHA-256 manifest verifies all 13 payload files.

## Frozen result

```text
AV true payload rows                 40/40
AV false rows excluded               7/7
observed tags                        Int=40
observed payload width               32 bits on 40/40
semantic Int range                   5..300
native/oracle mismatch               0
witness reselection                  0
next property-control bits read      0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## RL223 provenance correction

The temporary v1/v2 comparison initially treated MIMIR's `is_rl_223` contract field and Boxcars' same-named build-derived flag as if they were the same semantic quantity. They are not. MIMIR's R3.18AT/AV exact context remains `is_rl_223=false` on all forty rows. Pinned Boxcars derives its own flag from replay `BuildVersion`; the observed forty-row distribution is true=34 / false=6. Boxcars `decode_int` performs `read_i32()` and does not consume that build-derived flag.

The final admitted v3 evidence therefore preserves MIMIR's exact contract value, reports Boxcars' build-derived value separately, and compares only semantically equivalent payload/version fields. No context widening or false-to-true contract mutation was admitted.

## Superseded attempts

Earlier AW evidence attempts failed only in temporary evidence validation. The first attempt exposed rustfmt plus RL223-provenance conflation. The second reached native/Boxcars 40/40 but incorrectly asserted that Boxcars' build-derived flag must be true on all forty rows. Neither failed SHA was rerun. The immutable authority is the v3 head listed above.

## Hard stop

R3.18AW does not admit following-payload production composition, payload/control access on the seven AV-false terminators, a stream/header/payload after the payload, a second later property-control bit, a generalized/repeated property cursor, actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening, or historical AM/AN payload authority inheritance.

## Next gate

R3.18AX is a separate read-only boundary-evidence pass. It may rematerialize exactly the forty admitted AW payload ends and observe exactly one following `property_present` bit using pinned Boxcars plus an independent native one-bit observation. It must inherit no expected boolean distribution and must stop exactly one bit later without resolving a stream ID, header or payload.
