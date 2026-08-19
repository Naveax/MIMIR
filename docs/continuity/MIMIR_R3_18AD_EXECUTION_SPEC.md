# MIMIR R3.18AD — Bounded Post-AA Ordinal-3 Payload Production

**Status:** ACTIVE
**Pass type:** production implementation
**Production authority before pass:** R3.18AA `9392240c49f95766c214afee9865fed4155a87a4`
**R3.18AC evidence authority:** `62bc43dd12dbde48fb503cccd4da46dfcf6ae252`
**R3.18Z header contract:** `81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9`
**Another property control / repeated loop:** forbidden

## 1. Goal

Publish the smallest production composition justified by R3.18AC: starting only from one already-valid published R3.18AA following-header result, decode exactly that ordinal-3 payload and stop exactly at its payload end.

R3.18AD may support only the three payload shapes observed and differentially proven by R3.18AC:

```text
ActiveActor   39 observed rows   exact payload width 33 bits
Int            7 observed rows   exact payload width 32 bits
UniqueId       1 observed row    system_id=1 / Steam / exact payload width 80 bits
```

This pass does not inspect another `property_present` bit and does not create a generalized/repeatable property iterator.

## 2. Frozen authority

```text
canonical pre-pass main/tree         f34413e00518b73cf3768cd1914eda8c728306df / cce54b2040c2a83ebbcce3b31250df5bc82102ca
production SHA/tree                  9392240c49f95766c214afee9865fed4155a87a4 / 968520d480f78c528086e4e31b2ce307f4f8d232
production lib/test blobs            46523f47f94231362b60f8aee038e943e41c7972 / 7df8f84af37d771b12da1334bd195634e4cc6a54
R3.18Z contract SHA256               81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18AC evidence head/tree           62bc43dd12dbde48fb503cccd4da46dfcf6ae252 / 9d5b550b4bb93688db9f3a67583067adb32425f6
R3.18AC authority run/job            32237834815 / 96021661994 SUCCESS
R3.18AC same-head CI                 32237834813 / 96021661894 SUCCESS
R3.18AC artifact                     9359697636 / 12010 bytes
R3.18AC artifact digest              sha256:a6914044dfd8991d74b95caeb3507fb2469175c4458c5b50b55395b8ea67b9df
R3.18AC receipt helper               32238679393 / 96024251802 SUCCESS
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before implementation, fetch fresh `main` and require the exact canonical continuity admission for R3.18AC, the unchanged R3.18AA production source/test identities, exact R3.18Z contract bytes, and immutable R3.18AC receipts/artifact.

## 3. Required production entry boundary

The new production function must accept an already-valid R3.18AA result, or otherwise compose through the exact published AA boundary without bypassing it. It must require:

- AA `stop_bit == following_header.payload_start_bit`;
- complete following-header structure remains valid;
- the complete seven-field header context remains admitted by R3.18Z exact-tuple membership;
- replay/K2 context remains the already-admitted `868.32 / net10 / non-RL223` boundary for the frozen lane;
- payload decoding begins exactly at the AA payload start.

It may not infer permission from tag alone, width alone, object id alone, or a Cartesian combination of observed components.

## 4. Allowed payload decoders

Reuse existing admitted primitives only.

### ActiveActor

- header tag must be `ActiveActor`;
- decode with `decode_replay_network_k2_v1` under the exact admitted K2 context;
- require `payload_width == 33`;
- return the typed active flag and actor id;
- stop exactly at decoder `payload_end_bit`.

### Int

- header tag must be `Int`;
- decode with `decode_replay_network_primitive_scalar_v1`;
- require `payload_width == 32`;
- return the typed signed 32-bit value;
- stop exactly at decoder `payload_end_bit`.

### UniqueId

- header tag must be `UniqueId`;
- decode with `decode_replay_network_k2_v1` under the exact admitted K2 context;
- require `payload_width == 80`;
- require `system_id == 1`;
- require remote kind `Steam`;
- return the exact typed system/remote/local identity supported by the existing lower-level value;
- reject PlayStation/PsyNet/Epic and every other system/layout at this boundary even if the lower-level K2 decoder supports them elsewhere.

No 336-bit or 312-bit UniqueId layout is admitted by R3.18AD.

## 5. Output and stop contract

The production result must carry enough typed structure to prove:

- the unchanged R3.18AA prior/header result;
- the decoded ordinal-3 payload variant;
- payload start;
- payload end / stop bit;
- exact payload width.

For every successful result:

```text
payload_start == prior.stop_bit == prior.following_header.payload_start_bit
stop_bit      == decoded payload_end_bit
another property-control bits consumed == 0
```

No next control value, bit position, or generalized continuation state may be exposed.

## 6. Fail-closed requirements

Reject atomically on at least:

- invalid or inconsistent R3.18AA prior;
- header context outside exact R3.18Z membership;
- unsupported header tag;
- truncation before complete payload;
- decoder start/end/width inconsistency;
- ActiveActor width other than 33;
- Int width other than 32;
- UniqueId width other than 80;
- UniqueId system other than 1;
- UniqueId remote kind other than Steam;
- wrong context where the selected lower-level decoder is context-sensitive;
- arithmetic/position inconsistency.

Lower-level support elsewhere must not silently widen this boundary.

## 7. Required tests

Use real R3.18AC frozen representatives for all three admitted classes:

- at least one ActiveActor row;
- at least one Int row;
- the exact single UniqueId system-1/Steam row.

Require:

- exact AA prior/header reconstruction;
- exact AC payload start/end/width/value equality;
- repeatability;
- prefix truncation rejection;
- post-payload poison invariance;
- rejection of unsupported tag/shape;
- synthetic rejection of a lower-level-valid but AC-unadmitted UniqueId layout/system;
- stop exactly at payload end with no another-control read.

The permanent focused test must not select new easier witnesses in place of the frozen AC representatives.

## 8. Clean production scope

Preferred clean production commit changes exactly:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18ad_*.rs`

No docs, workflow, temporary tools, Cargo manifest/lockfile, dependency, fixture, corpus or support-lane mutation belongs in the clean production commit.

## 9. Required validation

On Rust 1.85:

- `cargo fmt --all -- --check`;
- focused R3.18AD tests PASS;
- existing R3.18AA focused tests PASS;
- relevant K2 and primitive-scalar decoder tests PASS;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS;
- full repository verifier PASS;
- clean production scope verifier PASS;
- exact clean-candidate normal CI SUCCESS;
- exact-head validation PR CI SUCCESS;
- fresh-main `force=false` publication only;
- published-main CI SUCCESS.

Do not dispatch/rerun an equivalent workflow if the same SHA/workflow/input is already queued or running.

## 10. Hard stop

R3.18AD may not decode or inspect another property-control bit, expose a generic/repeatable property cursor or loop, admit alternate UniqueId systems/layouts, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactual rollouts, or widen runtime/export behavior.

## 11. Outcome gate

### Outcome A

The exact three AC-observed payload shapes compose correctly after valid AA, all focused/full validation passes, another-control consumption remains zero, and the clean production commit contains only the bounded implementation/test. Admit R3.18AD production.

### Outcome B

A reproducible mismatch appears inside an AC-observed shape or valid AA boundary. Record exact privacy-safe coordinates and keep production at R3.18AA.

### Outcome C

Authority drift, scope widening, unsupported layout admission, another-control access, source/fixture/corpus drift, or validation contradiction. Stop without publication.
