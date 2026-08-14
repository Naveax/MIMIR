# MIMIR — R3.17D Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17D — primitive scalar native differential`
**Kind:** evidence-only / exact native-vs-oracle differential
**Frozen production SHA:** `c3d4c73ca34febb9f0383c59132a8bc8a363b06b`
**Frozen source blob:** `54e1bfb918ec1bd42a61cfa0131ca27412082ac5`
**R3.17A authority:** `4cd21ea6db14c9becc11c17149af9201071859bc`, run `31792028292`, job `94740870175`

## 1. Goal

Prove that the published R3.17C native one-scalar decoder reproduces the immutable R3.17A primitive-scalar oracle witnesses exactly before any wider attribute family receives promotion credit.

## 2. Frozen input authority

Recover from exact R3.17A job `94740870175` receipt markers:

```text
r3_17a_replay_identity.tsv       47 rows
r3_17a_scalar_witnesses.jsonl    96 rows, 16 per admitted scalar tag
r3_17a_summary.json
r3_17a_aggregate.txt
r3_17a_receipt_sha256.txt
```

The witness file SHA-256 is `b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9`.

Do not regenerate or reselect witnesses. R3.17D compares against the already frozen rows.

## 3. Native comparison procedure

For each witness:

1. verify its replay path SHA against the frozen identity table;
2. read the replay through current MIMIR structural readers only far enough to locate the raw network byte slice;
3. map the recorded scalar tag to the same admitted `ReplayNetworkAttributeTagV1`;
4. call `decode_replay_network_primitive_scalar_v1(network_bytes, payload_start_bit, tag)`;
5. compare the native result against the witness.

Required exact fields:

```text
attribute_tag
payload_start_bit
payload_end_bit
payload_width
stop_bit == payload_end_bit
```

Value comparison:

```text
Boolean -> bool / 0|1 exact
Byte    -> u8 exact
Enum    -> u16 numeric exact
Int     -> i32 exact bit interpretation
Int64   -> i64 exact bit interpretation
Float   -> raw_bits exact AND value.to_bits() exact
```

## 4. Required aggregate

```text
witness_rows = 96
native_decode_success = 96
exact_match = 96/96
mismatch_count = 0
native_error_count = 0
identity_error_count = 0
unsupported_tag_count = 0
production_mutation_count = 0
Cargo_mutation_count = 0
corpus_mutation_count = 0
```

Emit a bounded immutable job-log receipt containing the 96 comparison rows or enough exact row identities/hashes to reconstruct every comparison after short-lived artifacts expire.

## 5. Failure rules

Any mismatch in bit span, width, signed interpretation, Float raw bits, tag identity or stop position is Outcome C until explained. Do not widen the native decoder or mutate witnesses to make the comparison pass.

A fixture identity mismatch or receipt extraction problem is an evidence-harness failure; fix the harness only and rerun on the same production SHA.

## 6. Hard stop

R3.17D must not change production Rust, Cargo manifests/lockfile, replay corpus or fixtures. It must not iterate a second property, actor or frame, mutate actor lifecycle state, decode compound/spatial attributes, or open raw-state/event/skill/runtime/export surfaces.

## 7. Outcome

### Outcome A
96/96 exact native equality, zero errors/mutations. Admit R3.17C differential closure and select the next bounded attribute-family pass from the roadmap.

### Outcome B
Evidence is valid but reveals a narrow unsupported scalar shape outside the frozen contract. Open the smallest evidence follow-up; do not generalize.

### Outcome C
Native implementation contradicts frozen R3.17A evidence. Reopen R3.17C implementation only at the smallest proven mismatch.
