# MIMIR — R3.17B Contract Admission Decision

**Date:** 2026-08-14
**Pass:** `R3.17B — primitive scalar attribute contract admission`
**Outcome:** **A — ADMITTED / CONTRACT COMPLETE**
**Pass kind:** docs-only contract admission
**Production Rust changed:** **NO**

## Frozen authorities

```text
canonical continuity base    2e27638812111f73d06ef9e52955f10a26cfebd4
production code checkpoint   ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
R3.17A evidence head         4cd21ea6db14c9becc11c17149af9201071859bc
R3.17A workflow run/job      31792028292 / 94740870175 SUCCESS
R3.17A artifact              9216016802
R3.17A artifact SHA-256      59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
full scalar oracle SHA-256   af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1
96-witness SHA-256           b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
aggregate SHA-256            b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e
receipt stream               PASS
```

R3.17A observed 2,141,139 primitive scalar payloads over the exact 47-replay supported lane with zero shape mismatches, zero bit-monotonicity failures and zero unexpected tag shapes.

## Contract admitted

Exactly six primitive scalar tags are admitted:

```text
Boolean   width 1    wire 0/1                 semantic bool
Byte      width 8    unsigned                 semantic u8
Enum      width 11   unsigned numeric         storage u16, range 0..=2047
Float     width 32   exact raw u32 pattern    semantic f32::from_bits(raw)
Int       width 32   exact raw 32-bit pattern semantic i32 two's-complement
Int64     width 64   exact raw 64-bit pattern semantic i64 two's-complement
```

The common cursor contract is:

```text
start = payload_start_bit
byte alignment is NOT required
read exactly the admitted width in the existing LSB-first network order
if fewer than width bits remain: fail closed and consume 0 bits
on success: end = start + width
unsupported/non-admitted tag: fail without consuming payload bits
```

Float result identity includes the raw `u32` bit pattern. An `f32` value alone is not sufficient for exact equality because NaN payloads and signed zero are bit-sensitive.

Enum is a numeric 11-bit value only. R3.17B does not admit an engine enum-name registry.

## Integration policy for R3.17C

R3.17C must be additive and must reuse the existing private `NetworkBitCursor` semantics. The preferred seam is a one-scalar decoder receiving:

```text
network bytes
payload_start_bit
already-resolved ReplayNetworkAttributeTagV1
```

and returning exactly one typed scalar plus exact start/end/width metadata.

Unless fresh source truth proves otherwise, production change scope is limited to:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17c_scalar_attribute_decoder.rs
```

Forbidden in R3.17C:

```text
Cargo.toml / Cargo.lock changes
external parser dependency
support-lane widening
RigidBody / ActiveActor / Location / spatial-family decode
property-loop continuation or second property
next actor or next frame iteration
actor lifecycle mutation
raw state / events / skills / runtime / export widening
```

## Outcome

No contract ambiguity or contradiction was found between R3.17A authority and canonical production cursor behavior. Outcome A is admitted.

## Next exact pass

`R3.17C — primitive scalar attribute decoder implementation`.
