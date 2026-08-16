# MIMIR — R3.18B Decision

**Date:** 2026-08-16
**Pass:** `R3.18B — minimal native existing-actor single-property K1 composition`
**Outcome:** **A — ADMITTED / PUBLISHED PRODUCTION**
**Property loop:** not admitted

## Decision

R3.18B is now canonical production. MIMIR composes the existing R3.16B first-property header with the existing R3.17C primitive scalar decoder for exactly one existing-actor K1 property. The wrapper accepts only `Boolean`, `Byte`, `Enum`, `Float`, `Int`, and `Int64`, preserves the resolved header identity, and returns the scalar payload end as its exact stop bit.

This publication does not authorize a second property, a `property_present` loop, or K2/K3/K4 dispatch through the new wrapper.

## Frozen production authority

```text
parent main                  f12365b43029f19f3ab1dd889e651f9781b0655e
production SHA               de7a2ba40663bb619ca7bd8654846ce87670d023
production tree              d1889038ca2eaeb8bb0f05e44b811d906f84cf6e
lib.rs blob                  478ae5b70514fcff79117b834733849517c48500
focused test blob            927e9a2c834115d1c918fa96fb6d0690bd03965e
implementation run/job       31942254523 / 95153021330 SUCCESS
exact candidate validation   31942696817 / 95154052998 SUCCESS
published main CI            31942870294 / 95154460239 SUCCESS
published-main validator     31942896666 / 95154519828 SUCCESS
```

## Admitted behavior

```text
property_present=true        required
header authority             existing R3.16B decoder
payload authority            existing R3.17C primitive scalar decoder
admitted wrapper tags        Boolean / Byte / Enum / Float / Int / Int64
header stop                  exact payload_start_bit
wrapper stop                 exact scalar.payload_end_bit
next property_present        unread / 0 bits consumed
non-K1 resolved tag          fail closed before payload read
```

The focused suite is 8/8 PASS and includes aligned/unaligned starts for all six K1 tags, the R3.18A real-context `Int=62` regression, poison trailing bits, property-absent rejection, non-K1 rejection, header truncation, payload truncation, and repeatability.

## Clean scope

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_18b_single_k1_property.rs
```

No `Cargo.toml`, `Cargo.lock`, fixture, corpus, support script, workflow, or continuity file entered the clean production commit.

## Validation result

The exact clean candidate and the published `main` both passed the repository verifier. The published production SHA is therefore `de7a2ba40663bb619ca7bd8654846ce87670d023` rather than the older R3.17O authority.

## Next exact pass

`R3.18C — existing-actor property-loop terminator/continuation evidence`.

R3.18C is read-only. It may prove the exact next `property_present` position after one R3.18B K1 property and consume exactly that one bit for terminator/continuation evidence. It may not decode a second property stream/header/payload or mutate production.
