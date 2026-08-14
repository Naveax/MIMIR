# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Pre-contract canonical main:** `2e27638812111f73d06ef9e52955f10a26cfebd4`
**Production code checkpoint:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Production milestone:** `R3.16B — native existing-actor first-property envelope header implementation`
**Completed evidence pass:** `R3.17A — Outcome A`
**Completed contract pass:** `R3.17B — Outcome A`
**Current exact pass:** `R3.17C — primitive scalar attribute decoder implementation`

---

## 1. Truthful production boundary

Production behavior is still unchanged from R3.16B at this continuity checkpoint. MIMIR resolves one existing-actor property header through `stream_id`, inherited/static property lookup, object/tag identity and `payload_start_bit`, then stops before consuming the attribute payload.

R3.17A supplied evidence and R3.17B admitted the wire contract. Neither pass by itself grants runtime decode capability.

## 2. R3.17A immutable evidence authority

```text
canonical evidence base       ded95e8ae512876b46453585be05b8358025314a
evidence head                 4cd21ea6db14c9becc11c17149af9201071859bc
workflow run/job              31792028292 / 94740870175  SUCCESS
exact-head normal CI          31792028275 / 94740869974  SUCCESS
artifact id                   9216016802
artifact zip SHA-256          59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
replay identity rows          47
bounded witness rows          96
oracle parse success          47 / 47
scalar occurrences            2,141,139
shape mismatch                0
bit monotonicity failure      0
unexpected tag shape          0
production mutation           0
Cargo mutation                0
corpus mutation               0
receipt stream                PASS
```

## 3. R3.17B admitted primitive scalar contract

```text
Boolean   width 1    semantic bool
Byte      width 8    semantic u8
Enum      width 11   numeric u16, 0..=2047; no enum-name mapping
Float     width 32   exact raw u32 identity + f32::from_bits(raw)
Int       width 32   signed i32 using the identical two's-complement bit pattern
Int64     width 64   signed i64 using the identical two's-complement bit pattern
```

Common rule: start exactly at `payload_start_bit`, consume LSB-first with no byte-alignment requirement, and advance exactly the admitted fixed width on success. If fewer than the required bits remain, fail closed with zero cursor advance. A tag outside this six-tag family is unsupported and consumes zero payload bits.

Float raw bits are part of the result contract so NaN payloads and signed zero remain bit-exact. Enum remains a numeric wire value only.

## 4. R3.17C exact implementation boundary

R3.17C may add one narrow decoder that accepts network bytes, an admitted `payload_start_bit` and the already-resolved `ReplayNetworkAttributeTagV1`, and returns exactly one typed scalar plus start/end/width metadata.

The implementation must reuse the existing private LSB-first `NetworkBitCursor` / `read_bits_le` semantics. It must not infer a second property or depend on actor lifecycle state.

Expected value semantics:

```text
Boolean(bool)
Byte(u8)
Enum(u16)
Float { raw_bits: u32, value: f32 }
Int(i32)
Int64(i64)
```

A successful decoder stops exactly at `payload_end_bit = payload_start_bit + width`. Poison bits after that point remain unread.

## 5. Still closed

```text
RigidBody / ActiveActor / spatial payload families
property-loop continuation / second property
next actor iteration
next frame iteration
actor lifecycle mutation
raw-state materialization
semantic events
replay slicing
skill mining
counterfactual rollout execution
training/runtime/export widening
support-lane expansion
Cargo dependency changes
replay corpus changes
```

Outcome A for R3.17C opens `R3.17D — primitive scalar native differential` against the frozen R3.17A witness authority.
