# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Pre-admission canonical main:** `ded95e8ae512876b46453585be05b8358025314a`
**Production code checkpoint:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Production milestone:** `R3.16B — native existing-actor first-property envelope header implementation`
**Completed evidence pass:** `R3.17A — Outcome A`
**Current exact pass:** `R3.17B — primitive scalar attribute contract admission`

---

## 1. Truthful production boundary

Production behavior is unchanged from R3.16B. MIMIR can resolve one existing-actor property header through `stream_id`, inherited/static property lookup, object/tag identity and `payload_start_bit`, then stops before consuming the attribute payload.

R3.17A did not widen production. It measured the next wire layer through a pinned external oracle only.

## 2. R3.17A immutable evidence authority

```text
canonical evidence base       ded95e8ae512876b46453585be05b8358025314a
evidence head                 4cd21ea6db14c9becc11c17149af9201071859bc
workflow run/job              31792028292 / 94740870175  SUCCESS
exact-head normal CI          31792028275 / 94740869974  SUCCESS
artifact id                   9216016802
artifact zip SHA-256          59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
artifact size                 51,639,177 bytes
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

The bounded job-log receipt includes all 47 replay identities, 96 witnesses, aggregate/summary content and content hashes. The expiring artifact is therefore not the sole audit authority.

## 3. Observed primitive scalar family

```text
Boolean   84,545 occurrences    47 replays   width 1
Byte   1,730,595 occurrences    47 replays   width 8
Enum     180,624 occurrences    47 replays   width 11
Float     33,857 occurrences    47 replays   width 32
Int      109,920 occurrences    47 replays   width 32
Int64      1,598 occurrences    14 replays   width 64
```

All six candidate tags were observed. No candidate remains a zero-observation placeholder.

Important receipt hashes:

```text
instrumentation patch  f10fc6206aaba14b8afd368c5ede8d8ce6bc1e4a7a56049be9d7012aa8b82877
full scalar oracle     af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1
96 witnesses           b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
summary                a2f8a7c8efb87083986bb635d9c2c81e992556bbe9a41263d7bfd453c404ce2c
aggregate              b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e
```

## 4. R3.17B current contract pass

R3.17B may admit only the six evidence-backed primitive scalar wire contracts. It is docs/state only; no Rust code is modified.

The common contract is LSB-first at the existing payload cursor with no byte-alignment assumption. Successful decode consumes exactly the tag's admitted fixed width. Insufficient input or a non-admitted tag must fail atomically without advancing the cursor.

Float identity is the raw 32-bit pattern first; `f32` is its interpretation. Signed integer semantics are pinned to the oracle source contract, while the replay corpus evidence establishes the exact consumed widths on the supported lane.

## 5. Still closed

```text
native scalar payload decoder
RigidBody / ActiveActor / spatial payload families
second property / property loop
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
```

Outcome A for R3.17B opens `R3.17C — primitive scalar attribute decoder implementation`.
