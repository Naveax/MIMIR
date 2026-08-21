# MIMIR R3.18AK — Bounded Post-R3.18AG Following-Header Production Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Contract authority:** R3.18AJ Outcome A / `cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c`
**Production authority before pass:** R3.18AG `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`
**Following payload:** forbidden
**Another control bit:** forbidden
**Repeated/general property loop:** forbidden

## 1. Goal

Publish the smallest production composition justified by R3.18AJ. Starting only from an already-valid R3.18AG true-control result and the exact actor/lookup/version context required by the existing header primitive, decode exactly one following existing-actor property header, require full seven-field R3.18AJ membership, and stop exactly at that header's `payload_start`.

## 2. Frozen authority

```text
R3.18AJ admission base             a048ba25f2ef023d07bab17716838f1c4777fe27 / cd00dd18da0a177415ce569b7909ec6390cbb252
production SHA/tree                 2d351e8ceb601e2fbe515d2977b2103a4b2c7976 / 4123820ce6537f2d4942cd0b5f72b52e43b96c1d
production lib/test blobs           db923ebcb419d278f4ab0144fe7ed15b298b60fa / 3f3e1c8f3f6deb7f2558862a1032f8a102131443
R3.18AJ contract SHA-256            cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AJ exact contexts / rows       17 / 47
R3.18AJ tags                        Int=47
R3.18AI evidence                    9d424dae2ed8cc7a0a6868111805a48763131196 / 32418184036/96584056481
R3.18AI artifact                    9424764320 / sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5
R3.18AI published-main CI / KA      32424170707/96602481420 / 32424170684/96602481274
R3.18Z/R3.18P inheritance           forbidden
```

Before mutation, fetch fresh main, verify this contract byte-for-byte and verify production source/test identity remains exact.

## 3. Admitted composition

The implementation must be deliberately boundary-specific:

1. validate the supplied prior is a valid R3.18AG success result and starts/ends exactly at the already-admitted control boundary;
2. reuse the existing stateless existing-actor property-header primitive rather than introducing a new parser;
3. resolve one header only;
4. form the complete seven-field structural tuple;
5. require exact membership in `MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json`;
6. return the one typed header result and stop at `payload_start`;
7. consume zero following-payload bits and zero another-control bits.

Do not expose a generic repeatable cursor or property iterator.

## 4. Fail-closed rules

Reject atomically on prior-AG inconsistency, property/stream truncation, wrong actor, unresolved lookup, wrong replay version/context, any tuple outside the exact 17-entry AJ set, or arithmetic/position inconsistency. A tuple valid under R3.18Z/R3.18P but absent from R3.18AJ must fail at this boundary.

## 5. Required focused tests

At minimum:

- representative real R3.18AI-derived Int contexts across the observed bounds/widths;
- exact start/end/stream/header/payload-start boundary identity;
- repeatability;
- property and stream truncation;
- wrong actor / unresolved lookup / wrong exact version context;
- fabricated Cartesian `(60,5,68,Int,868,32,10)` rejection;
- fabricated eighteenth `(60,5,39,Int,868,32,10)` rejection;
- `(60,5,34,ActiveActor,868,32,10)` R3.18Z-valid/AJ-absent cross-boundary rejection;
- post-`payload_start` poison leaves the header result unchanged;
- following-payload bits consumed 0;
- another-control bits consumed 0;
- no property `while`/`for` loop and no generic public cursor.

## 6. Clean production scope

Preferred exact scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18ak_post_ag_following_header.rs`

No contract/doc/workflow/temp tool, Cargo manifest/lockfile, fixture, corpus or support expansion may enter the clean production commit.

## 7. Validation and publication

Require Rust 1.85 focused AK tests, full `mimir-replay`, workspace check/test/clippy, repository verifier, exact clean-candidate SHA CI, validation PR exact-head CI, fresh-main ancestry audit, force=false publication and published-main CI.

## 8. Hard stop

R3.18AK does not admit the post-AG following payload, another property-control bit, repeated/generalized property parsing, generic cursors, next actor/frame/lifecycle behavior, raw state/events, replay slicing, skills, counterfactual execution or runtime/export widening.

## 9. Outcome gate

### Outcome A
Publish exactly one AJ-admitted post-AG header through `payload_start`. Then open a separate read-only R3.18AL published-AK differential on the immutable 47-row AI lane.

### Outcome B
A bounded contract/composition mismatch is reproducible. Record it and keep production at R3.18AG.

### Outcome C
Authority drift, AJ-contract widening, R3.18Z/R3.18P inheritance, payload/control access, looping/generalization, production-scope drift or validation contradiction. Stop without publication.
