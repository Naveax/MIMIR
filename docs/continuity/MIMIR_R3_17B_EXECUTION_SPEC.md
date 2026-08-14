# MIMIR — R3.17B Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17B — primitive scalar attribute contract admission`
**Kind:** contract-only / docs-state / no production Rust
**Production code checkpoint:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Evidence authority:** `4cd21ea6db14c9becc11c17149af9201071859bc`, run `31792028292`, job `94740870175`

## 1. Goal

Freeze the smallest implementation contract justified by R3.17A for exactly these six tags:

```text
Boolean
Byte
Enum
Float
Int
Int64
```

This pass admits a wire contract, not executable decoding capability.

## 2. Common cursor contract

All six scalar values begin at the already-admitted `payload_start_bit` and use the existing replay network LSB-first bit order.

There is **no byte-alignment precondition**. A scalar may begin at any valid bit offset.

For an admitted tag with required width `W`:

```text
start = payload_start_bit
if total_bits - start < W:
    fail closed
    consume 0 bits
    return no value
else:
    consume exactly W bits LSB-first
    end = start + W
    return typed value + exact start/end/width metadata
```

Failure must be atomic. This matches the existing private `NetworkBitCursor::read_bits_le` boundary rule, which checks the complete range before advancing the cursor.

A tag outside this six-tag contract fails without consuming payload bits.

## 3. Admitted scalar wire contracts

### Boolean

```text
width: 1 bit
wire value: 0 or 1
semantic value: bool
```

### Byte

```text
width: 8 bits
wire value: unsigned 8-bit
semantic value: u8
```

### Enum

```text
width: 11 bits
wire value: unsigned 11-bit numeric value
storage type: u16
range permitted by width: 0..=2047
```

R3.17B does not map the numeric value to an engine enum name.

### Float

```text
width: 32 bits
exact identity: raw u32 bit pattern
semantic interpretation: f32::from_bits(raw)
```

The raw `u32` is mandatory in the result contract. `f32` comparison alone is insufficient because NaN payloads and signed zero require bit-exact identity.

### Int

```text
width: 32 bits
exact wire pattern: 32 raw bits
semantic interpretation: signed i32 using the same two's-complement bit pattern
```

### Int64

```text
width: 64 bits
exact wire pattern: 64 raw bits
semantic interpretation: signed i64 using the same two's-complement bit pattern
```

## 4. Proposed implementation result shape for R3.17C

The later implementation should expose an additive narrow value type equivalent in meaning to:

```text
Boolean(bool)
Byte(u8)
Enum(u16)
Float { raw_bits: u32, value: f32 }
Int(i32)
Int64(i64)
```

and an envelope containing at least:

```text
attribute_tag
payload_start_bit
payload_end_bit
payload_width
value
explicit stop reason / one-scalar boundary
```

Exact Rust names remain an implementation choice, but semantics above are fixed by this contract.

## 5. Required R3.17C implementation tests

At minimum:

- aligned and unaligned start offsets for every admitted tag;
- exact end offset equals `start + width`;
- Boolean 0/1;
- Byte 0/255;
- Enum 0/2047 synthetic boundaries plus evidence witnesses;
- Float raw-bit preservation, including `+0.0`, `-0.0`, infinities and at least one NaN payload synthetically;
- Int `i32::MIN`, `-1`, `0`, `i32::MAX` synthetically;
- Int64 `i64::MIN`, `-1`, `0`, `i64::MAX` synthetically;
- truncation at every `width - 1` boundary fails with zero cursor advance;
- unsupported/compound tag fails with zero cursor advance;
- poison bits after the scalar remain unread;
- no second property/actor/frame consumption.

R3.17D must later perform native differential comparison against the frozen R3.17A witness set before wider attribute decoding is credited.

## 6. Explicitly not admitted

```text
RigidBody
ActiveActor
Location / rotation / spatial families
UniqueId / reservation / product structures
string-like or object-reference payloads
private/loadout/party/team paint compound payloads
property-loop continuation
second property
next actor
next frame
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
```

## 7. Outcome rules

### Outcome A

The six scalar contracts, common cursor rule, representations and fail-closed semantics are accepted without production mutation.

Open `R3.17C — primitive scalar attribute decoder implementation`.

### Outcome B

A contract ambiguity is found that cannot be resolved from the frozen evidence/source. Open the smallest tag-specific evidence follow-up; do not implement the ambiguous tag.

### Outcome C

The proposed contract contradicts canonical production cursor behavior or R3.17A authority. Stop and reopen the conflicting earlier pass.

## 8. Hard stop

R3.17B changes no production Rust, Cargo dependency, fixture or replay corpus. It grants no runtime decoding capability.
