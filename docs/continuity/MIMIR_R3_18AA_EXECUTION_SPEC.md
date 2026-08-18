# MIMIR R3.18AA — Bounded Post-R3.18W Following-Header Production Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Contract authority:** R3.18Z Outcome A / `81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9`
**Production authority before pass:** R3.18W `58872e94f00ef094807f21ab2ff984ac66b97d91`
**Following payload:** forbidden
**Another control bit:** forbidden
**Repeated/general property loop:** forbidden

## 1. Goal

Publish the smallest production composition justified by R3.18Z. Starting only from an already-valid R3.18W true-control result and the exact actor/lookup/version context required by the existing header primitive, decode exactly one following existing-actor property header, require full seven-field R3.18Z membership, and stop exactly at that header's `payload_start`.

## 2. Frozen authority

```text
production SHA/tree                 58872e94f00ef094807f21ab2ff984ac66b97d91 / d6965d77903ea99dad0465bb350b6a673ee7dd00
R3.18Z contract SHA-256             81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18Z exact contexts / rows        18 / 47
R3.18Z tags                         ActiveActor=39 / Int=7 / UniqueId=1
R3.18Y evidence                     413d6c24f8f390a57c21ed345f3f868c263f413c / 32076198677/95529856476
R3.18Y artifact                     9303584468 / sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29
R3.18P inheritance                  forbidden
```

Before mutation, fetch fresh main, verify this contract byte-for-byte and verify production source/test identity remains exact.

## 3. Admitted composition

The implementation must be deliberately boundary-specific:

1. validate the supplied prior is a valid R3.18W success result and starts/ends exactly at the already-admitted control boundary;
2. reuse the existing stateless existing-actor property-header primitive rather than introducing a new parser;
3. resolve one header only;
4. form the complete seven-field structural tuple;
5. require exact membership in `MIMIR_R3_18Z_ADMITTED_HEADER_CONTEXTS.json`;
6. return the one typed header result and stop at `payload_start`;
7. consume zero following-payload bits and zero another-control bits.

Do not expose a generic repeatable cursor or property iterator.

## 4. Fail-closed rules

Reject atomically on prior-W inconsistency, property/stream truncation, wrong actor, unresolved lookup, wrong replay version/context, any tuple outside the exact 18-entry Z set, or arithmetic/position inconsistency. A tuple valid under R3.18P but absent from R3.18Z must fail at this boundary.

## 5. Required focused tests

At minimum:

- real R3.18Y-derived ActiveActor, Int and UniqueId contexts;
- exact start/end/stream/header/payload-start boundary identity;
- repeatability;
- property and stream truncation;
- wrong actor / unresolved lookup / wrong exact version context;
- fabricated Cartesian tuple rejection;
- `(60,5,102,Boolean,868,32,10)` R3.18P-only cross-boundary rejection;
- post-`payload_start` poison leaves the header result unchanged;
- following-payload bits consumed 0;
- another-control bits consumed 0;
- no property `while`/`for` loop and no generic public cursor.

## 6. Clean production scope

Preferred exact scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18aa_*.rs`

No contract/doc/workflow/temp tool, Cargo manifest/lockfile, fixture, corpus or support expansion may enter the clean production commit.

## 7. Validation and publication

Require Rust 1.85 focused AA tests, full `mimir-replay`, workspace check/test/clippy, repository verifier, exact clean-candidate SHA CI, PR exact-head CI, fresh-main ancestry audit, force=false publication and published-main CI.

## 8. Hard stop

R3.18AA does not admit the post-W following payload, another property-control bit, repeated/generalized property parsing, generic cursors, next actor/frame/lifecycle behavior, raw state/events, replay slicing, skills, counterfactual execution or runtime/export widening.

## 9. Outcome gate

### Outcome A
Publish exactly one Z-admitted post-W header through `payload_start`. Then open a separate read-only published-AA differential on the immutable 47-row Y lane.

### Outcome B
A bounded contract/composition mismatch is reproducible. Record it and keep production at R3.18W.

### Outcome C
Authority drift, Z-contract widening, R3.18P inheritance, payload/control access, looping/generalization, production-scope drift or validation contradiction. Stop without publication.
