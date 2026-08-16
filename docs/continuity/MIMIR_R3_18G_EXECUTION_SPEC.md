# MIMIR R3.18G — Minimal Native Existing-Actor Second-Property Header Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18F Outcome A
**Second-property payload decode:** forbidden
**Third property / repeated loop:** forbidden
**Generic chainable property cursor:** forbidden

## 1. Goal

Publish the smallest production composition justified by R3.18F: after one already-valid R3.18B K1 first property, compose the existing R3.18D next-property control with the existing property-header primitive and return either a terminator or exactly one second header through `payload_start`.

This pass does not decode the second payload and does not create a general property loop.

## 2. Frozen authority

```text
canonical main before pass           3a10ee59ba42722b59ca6c5b816205f6e5d603ea
canonical tree                       ff8049a18431977e054652a0836217fcc39d84a7
production SHA/tree                  4adadd185783954c7fb6ad67db14b77b377cdde5 / 67b1969eaff49d2913b88b3921f27b1bd7fe8193
production lib blob                  42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662
R3.18B focused test blob             927e9a2c834115d1c918fa96fb6d0690bd03965e
R3.18D focused test blob             2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b
R3.18F spec blob                     e6b92ea5628f107112a088421f318cd45a384e87
R3.18F authority head/tree           27a855a9cfb82a0294dd1601e4da01c9fdfad264 / 4058b67da82e9fbfcc078e975b26d186ec68e6f0
R3.18F run/job                       31951039411 / 95174417526 SUCCESS
R3.18F same-head normal CI           31951039378 / 95174417478 SUCCESS
R3.18F artifact                      9264673141
R3.18F artifact digest               sha256:e31e09abf322b6458f9034b06efe5502bb3b7f1011dfb08c9ffd6d1b1cd1b361
continuation second headers          47/47 exact
terminator negatives                 47/47 exact
native/oracle mismatch               0
second payload / third property bits 0 / 0
```

Before mutation, fetch fresh `main`; prove every commit after `4adadd185783954c7fb6ad67db14b77b377cdde5` is continuity-only; verify source/test/spec blobs and both R3.18F SUCCESS receipts; verify the artifact ID/digest.

## 3. Admitted production API shape

Prefer a non-generic API explicitly tied to one first primitive property, conceptually:

```text
input:
  network bytes
  + &ReplayNetworkExistingActorSinglePrimitivePropertyV1
  + &ReplayNetworkLookupPlanV1

internally:
  validate the R3.18B first-property invariants
  control = existing R3.18D after-first-primitive control decoder

if control.next_property_present == false:
  return control
  second_header = None
  stop_bit = control.stop_bit
  perform no property lookup/header/payload read after the false bit

if control.next_property_present == true:
  header = existing property-header primitive at control.property_present_start_bit
  require header.property_present == true
  require header.property_present_start/end == control.property_present_start/end
  require header actor object == first_property.header.actor_object_index
  require resolved tag in {Int, String}
  second_header = Some(header)
  stop_bit = header.payload_start_bit == header.stop_bit
```

A result type may contain the R3.18D control result, an optional second header and exact stop bit. Its name must encode **after first primitive** / **second property header** semantics. Do not expose a generic cursor intended for repeated chaining.

## 4. Exact second-header tag allowlist

R3.18F observed and validated exactly:

```text
Int     46
String   1
```

Therefore this new composition admits only `Int` and `String` for a present second header, matching the exact R3.18F continuation lane. `String` here is header resolution only: the K2 String payload decoder is not called or admitted. Any other second-header tag fails closed before any second payload read. This does not change the lower-level header primitive's existing independent capabilities.

## 5. Fail-closed rules

Reject atomically on:

- malformed or internally inconsistent R3.18B first-property boundary;
- R3.18D control truncation or inconsistency;
- continuation header whose present-bit coordinates do not exactly agree with the R3.18D control;
- unresolved second stream ID/property mapping;
- arithmetic/bit-range failure inside the second header;
- present second header resolving to a tag outside the exact R3.18F Int/String header set;
- any impossible stop/payload-start relationship.

Failure exposes no successful second-header composition and performs no second payload decode.

## 6. Required focused tests

At minimum:

```text
false terminator -> None / exact control stop                 positive
false terminator performs no lookup after control             positive
continuation Int                                               positive
continuation String header                                     positive / payload unconsumed
aligned and unaligned second-header starts                     positive
R3.18F-shaped real boundary witnesses                          positive
control/header present-coordinate agreement                    exact
header stop == second payload_start                            exact
second payload poison / absence after payload_start            no effect
post-header poison                                             no effect
missing control bit                                            reject atomically
truncation inside second stream/header                         reject atomically
unresolved second stream                                       reject
tag outside exact Int/String second-header set                 reject before payload
repeatability                                                  exact
```

Use synthetic/R3.18F-shaped byte windows in tests. Do not check raw oracle windows into the clean production commit.

## 7. Source reuse rule

Reuse the published R3.18D control decoder and existing property-header primitive. Do not duplicate bounded stream decoding, lookup resolution or bit-cursor rules. Do not call scalar/K2/K3/K4 payload decoders from the new composition.

## 8. Clean production scope

Preferred clean scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18g_*.rs`

A tiny isolated source module is allowed only if direct inspection materially improves boundary enforcement. No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file may enter the clean production commit.

## 9. Source-boundary audit

Before publication, independently prove in the new composition block:

- exactly one call to the R3.18D control decoder;
- at most one call to the existing property-header primitive;
- zero scalar/K2/K3/K4 payload decoder calls;
- no `while` or `for` property loop;
- explicit exact Int/String second-header allowlist;
- terminator returns before any second-header lookup path;
- no third-property access.

## 10. Validation and publication

Required before publication:

- focused R3.18G tests;
- full `mimir-replay` suite;
- workspace check/test/clippy under the Rust 1.85 floor;
- full repository verifier;
- exact clean-candidate SHA validator;
- fresh-main ancestry audit;
- force-free fast-forward publication;
- fresh `main` readback;
- exact published-main validator.

## 11. Hard stop

R3.18G does not admit:

- any second-property payload bit or semantic value;
- a third property control/header;
- repeated/generalized property loops;
- a generic repeatedly-chainable public property cursor;
- second-header tag context outside exact R3.18F Int/String widening;
- K2/K3/K4 composition through R3.18B;
- next actor / next frame iteration;
- actor lifecycle mutation;
- raw-state/event/replay-slice/skill/runtime/export widening;
- Cargo/fixture/corpus/support/dependency expansion.

## 12. Outcome gate

### Outcome A

The bounded optional second-header composition is published with exactly the constraints above and every validation gate passes. Then run a separate real-replay differential audit of the production second-header composition before any second-property payload admission.

### Outcome B

Implementation reveals a bounded contract mismatch between first-property/control/header semantics. Record it and keep production at R3.18D.

### Outcome C

Any source drift, loop/generalization, non-observed tag admission, second-payload consumption, third-property access, scope widening, MSRV failure or validation contradiction. Stop without publication.
