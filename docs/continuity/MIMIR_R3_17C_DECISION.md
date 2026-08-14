# MIMIR — R3.17C Production Decision

**Date:** 2026-08-14
**Pass:** `R3.17C — primitive scalar attribute decoder implementation`
**Outcome:** **PUBLISHED / PRODUCTION CLOSED**

## Production identity

```text
base SHA                    85430b9eedb3bf16d66abcd895d68fbc7217818e
production SHA              c3d4c73ca34febb9f0383c59132a8bc8a363b06b
source                       crates/mimir-replay/src/lib.rs
source Git blob             54e1bfb918ec1bd42a61cfa0131ca27412082ac5
focused test                 crates/mimir-replay/tests/r3_17c_scalar_attribute_decoder.rs
focused test Git blob       0293831df88723d6cf1e7fd13870bec6108d383a
clean diff                  exactly 2 files, +465/-0
```

## Admitted implementation

The native decoder accepts network bytes, a caller-supplied `payload_start_bit`, and an already resolved `ReplayNetworkAttributeTagV1`. It decodes exactly one R3.17B-admitted primitive scalar:

```text
Boolean / Byte / Enum / Float / Int / Int64
```

It reuses the existing LSB-first `NetworkBitCursor`, assumes no byte alignment, preserves Float raw `u32` bit identity alongside `f32`, interprets signed integer bit patterns natively, and returns exact payload start/end/width/value plus `stop_bit == payload_end_bit`.

Unsupported/compound tags are rejected before payload decoding. No second property, actor or frame is consumed.

## Validation

```text
focused tests                      11/11 PASS
disposable implementation run/job 31795745652 / 94752360261 SUCCESS
candidate CI                       31796122522 / 94753517283 SUCCESS
candidate Knowledge Archive        31796266602 / 94753955749 SUCCESS
publication                        force=false fast-forward
published-main CI                  31796509896 / 94754670068 SUCCESS
published-main Knowledge Archive   31796560814 / 94754827522 SUCCESS
```

## Scope audit

Permanent production commit changed only:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_17c_scalar_attribute_decoder.rs`

No Cargo dependency, lockfile, fixture, corpus, workflow, temporary tool or continuity file entered the production commit.

## Hard stop retained

R3.17C grants only a one-scalar primitive. Property-loop continuation, second property, actor/frame iteration, lifecycle mutation, `RigidBody`, `ActiveActor`, spatial/compound payloads, raw state, events, skills, runtime and export surfaces remain closed.

## Next pass

`R3.17D — primitive scalar native differential` against the immutable R3.17A 96-witness authority.
