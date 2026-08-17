# MIMIR R3.18Q — Bounded Following-Property Header Production Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production SHA:** `f41c59d26ed6c810a640b4fa8cd76129decb32aa`
**Production tree:** `606db4b5778e5218f2bd0117cc5dd72d7f3e37a5`

## Decision

R3.18Q is admitted. From one already-valid R3.18J second-property payload result, production reuses the published R3.18M true-only following-control decoder and the existing stateless property-header primitive, requires the resolved following header to match one of the exact 18 R3.18P seven-field structural/version tuples, and stops exactly at that following header's `payload_start`.

The pass does not decode the following payload, read another property-control bit, create a repeatable property cursor, or widen actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export behavior.

## Exact authority

```text
pre-pass main                       1a3f89e7256c7c7ff4bf6b747a434504f1f2e572
production SHA/tree                 f41c59d26ed6c810a640b4fa8cd76129decb32aa / 606db4b5778e5218f2bd0117cc5dd72d7f3e37a5
lib.rs blob                         b01b1e8629a4f4bc2452e67024ffb0d064bf58fb
focused test blob                   4bb65af1d533752edc062202192232d6f1d4239c
R3.18P contract SHA256              0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
implementation authority            32026722346 / 95377559363 SUCCESS
authority artifact                  9287413927 / 2818 bytes / sha256:1d4ae41e506a69e49ff58372ac0774c6257cbace96a3219bf6ab3ba5f68bf9bb
same-trigger temporary-ops CI       32026722356 / 95377559490 SUCCESS
exact clean-candidate CI            32027055064 / 95378560725 SUCCESS
published-main CI                   32027421491 / 95379649817 SUCCESS
Knowledge Archive on production PR  N/A — path-filtered to continuity/archive files
```

## Clean scope

Exactly two production files changed from `1a3f89e7256c7c7ff4bf6b747a434504f1f2e572`:

1. `crates/mimir-replay/src/lib.rs` — +358 / -0
2. `crates/mimir-replay/tests/r3_18q_following_header.rs` — +188 / -0

Cargo manifests/lockfile, fixtures, corpus, docs, workflows and support tooling are absent from the clean production commit.

## Admitted behavior

- reuse the exact R3.18M following `property_present=true` control boundary;
- decode exactly one following existing-actor property header with the already-published stateless header primitive;
- preserve exact control/header present-bit coordinate agreement and actor-object agreement;
- admit only the exact 18 R3.18P tuples across `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)`;
- reject tag-only, component-only, fabricated Cartesian, versionless and nineteenth-tuple widening;
- require `header.stop_bit == payload_start_bit` and return that exact stop;
- consume zero following-payload bits and zero another-control bits.

Authority reconstruction matched the immutable R3.18O lane on 47/47 rows. For all 47, Q's embedded control equaled the published R3.18M control and Q's returned following header equaled the direct stateless native header. Focused validation passed 2 contract unit tests plus 4 permanent integration tests; truncation, wrong actor, fabricated exact-context and wrong-version negatives passed; post-payload poison invariance passed. Full repository verification passed on the authority build, exact clean candidate and published `main`.

## Frozen real-replay result

```text
R3.18O frozen rows                  47/47
R3.18P exact contexts               18
Q native composition exact          47/47
Q / R3.18M control equality         47/47
Q / stateless header equality       47/47
following payload bits consumed     0
another control bits consumed       0
production/Cargo/fixture/corpus/support mutation outside clean scope  0/0/0/0/0
```

## Hard stop

R3.18Q admits no following-property payload bytes or semantic value, no later `property_present` bit, no third/fourth generalized property composition, no repeatable public property cursor/loop, no context outside the exact R3.18P contract, no next actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual rollout execution, runtime bridge or export widening.

## Next gate

R3.18R is a separate read-only real-replay differential audit of the **published R3.18Q production API** on the immutable R3.18O 47-row lane. Following-payload widening remains forbidden until that evidence closes and a later pass explicitly defines a payload contract/evidence boundary.
