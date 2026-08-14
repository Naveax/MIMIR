# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `c3d4c73ca34febb9f0383c59132a8bc8a363b06b`
**Production milestone:** `R3.17C — native primitive scalar attribute decoder implementation`
**Completed evidence authority:** `R3.17A — Outcome A`
**Completed contract pass:** `R3.17B — Outcome A`
**Current exact pass:** `R3.17D — primitive scalar native differential`

## 1. Truthful production boundary

MIMIR can now decode exactly one already-resolved primitive scalar payload for:

```text
Boolean  1 bit
Byte     8 bits
Enum     11 bits
Float    32 bits, raw u32 + f32 interpretation
Int      32 bits, signed two's-complement interpretation
Int64    64 bits, signed two's-complement interpretation
```

The caller supplies `payload_start_bit` and `ReplayNetworkAttributeTagV1`. The native decoder reuses the existing LSB-first `NetworkBitCursor`, requires no byte alignment, and returns exact `payload_start_bit`, `payload_end_bit`, `payload_width`, value and `stop_bit`.

Production stops exactly after that one scalar. It does not continue the property loop.

## 2. R3.17C production identity

```text
pre-pass main                85430b9eedb3bf16d66abcd895d68fbc7217818e
clean production SHA         c3d4c73ca34febb9f0383c59132a8bc8a363b06b
production source blob       54e1bfb918ec1bd42a61cfa0131ca27412082ac5
focused test blob            0293831df88723d6cf1e7fd13870bec6108d383a
clean diff                   2 files, +465/-0
focused tests                11/11 PASS
disposable run/job           31795745652 / 94752360261 SUCCESS
candidate CI                 31796122522 / 94753517283 SUCCESS
candidate Knowledge          31796266602 / 94753955749 SUCCESS
published-main CI            31796509896 / 94754670068 SUCCESS
published-main Knowledge     31796560814 / 94754827522 SUCCESS
```

## 3. R3.17D exact next pass

R3.17D is evidence-only. Recover the immutable R3.17A `r3_17a_scalar_witnesses.jsonl` receipt from job `94740870175` and compare all 96 rows against the native decoder at the same replay/network bit positions.

Required exact comparisons:

```text
attribute tag
payload_start_bit
payload_end_bit
payload_width
Boolean / Byte / Enum / Int / Int64 value
Float raw u32 bits and f32.to_bits()
stop_bit == payload_end_bit
```

Admission requires 96/96 exact equality, no missing replay identity, no native error, and zero production/Cargo/corpus mutation.

## 4. Still closed

```text
second property / property-loop continuation
next actor / next frame iteration
RigidBody / ActiveActor / Location / other spatial or compound attribute payloads
actor lifecycle mutation
raw-state materialization
semantic events
replay slicing
skill mining
counterfactual rollout execution
training/runtime/export widening
support-lane expansion
```
