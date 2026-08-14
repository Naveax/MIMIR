# MIMIR — R3.17C Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17C — primitive scalar attribute decoder implementation`
**Kind:** production implementation / bounded additive decoder
**Canonical implementation base:** `2e27638812111f73d06ef9e52955f10a26cfebd4` plus admitted R3.17B docs-only continuity commit
**Production code checkpoint before pass:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Evidence authority:** `4cd21ea6db14c9becc11c17149af9201071859bc`, run `31792028292`, job `94740870175`

## 1. Goal

Implement exactly one native primitive-scalar payload decoder for the six R3.17B-admitted tags:

```text
Boolean
Byte
Enum
Float
Int
Int64
```

The decoder begins at an already-resolved `payload_start_bit` and stops exactly after that one scalar. It does not own property-loop, actor-loop or frame-loop control flow.

## 2. Production seam

The existing R3.16B header already returns:

```text
resolved_attribute_tag: Option<ReplayNetworkAttributeTagV1>
payload_start_bit: Option<u64>
```

R3.17C should add an independent narrow decoder equivalent in meaning to:

```text
decode_replay_network_primitive_scalar_v1(
    network_bytes,
    payload_start_bit,
    attribute_tag,
) -> Result<ReplayNetworkPrimitiveScalarDecodeV1>
```

Exact Rust names may vary if source layout requires it, but the API must remain one-scalar and context-injected. Do not make the decoder rediscover actor/property context.

## 3. Required result semantics

Add a typed scalar value equivalent in meaning to:

```text
Boolean(bool)
Byte(u8)
Enum(u16)
Float { raw_bits: u32, value: f32 }
Int(i32)
Int64(i64)
```

and a result envelope containing at least:

```text
attribute_tag
payload_start_bit
payload_end_bit
payload_width
value
stop_bit == payload_end_bit
```

For Float, raw `u32` identity is mandatory in addition to `f32` interpretation.

## 4. Wire rules

```text
Boolean  width 1
Byte     width 8
Enum     width 11
Float    width 32
Int      width 32
Int64    width 64
```

All reads are LSB-first through the existing `NetworkBitCursor`. No byte alignment may be assumed.

Signed integers are obtained from the exact raw bit pattern using two's-complement reinterpretation. Float is obtained with `f32::from_bits(raw_u32)`.

## 5. Atomic failure contract

Before success the decoder must not partially advance observable state.

Required failures:

- `payload_start_bit` outside network length;
- insufficient bits for the selected admitted width;
- unsupported/compound attribute tag.

All failures consume zero payload bits. The implementation may use a private local cursor because the public API is start-offset based; nevertheless truncation must preserve the existing atomic `read_bits_le` semantics.

## 6. Required focused tests

At minimum:

- aligned and unaligned start offsets for all six tags;
- exact `payload_end_bit = payload_start_bit + width`;
- `stop_bit == payload_end_bit`;
- Boolean `0` and `1`;
- Byte `0` and `255`;
- Enum synthetic `0` and `2047`;
- Float `+0.0`, `-0.0`, positive/negative infinity and at least one NaN payload with exact raw-bit preservation;
- Int `i32::MIN`, `-1`, `0`, `i32::MAX`;
- Int64 `i64::MIN`, `-1`, `0`, `i64::MAX`;
- every tag truncated by one bit fails;
- start exactly at network end fails for every non-zero-width tag;
- unsupported `RigidBody` and `ActiveActor` fail without reading poison bits;
- poison bits immediately after a valid scalar do not affect the decoded value or stop position;
- repeatability is exact.

## 7. Clean change scope

Expected permanent files:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17c_scalar_attribute_decoder.rs
```

No Cargo dependency, fixture, corpus, workflow, temporary evidence or continuity file belongs in the clean production commit.

## 8. Hard stop

R3.17C must not:

```text
decode RigidBody / ActiveActor / Location / Rotation / spatial families
decode strings, unique IDs, reservations, loadouts or other compound attributes
consume property_present after the scalar
iterate a second property
iterate a next actor or frame
mutate actor lifecycle state
materialize raw game state or semantic events
open replay slicing / skill / teacher / runtime / export surfaces
change Cargo dependencies
change the replay support lane or corpus
```

## 9. Validation and next pass

The clean candidate must pass focused tests, full repository verification, exact diff-scope audit and hosted CI/Knowledge Archive gates before publication.

After production publication, `R3.17D — primitive scalar native differential` must compare the native decoder against the frozen R3.17A 96-witness authority before any wider attribute family receives credit.
