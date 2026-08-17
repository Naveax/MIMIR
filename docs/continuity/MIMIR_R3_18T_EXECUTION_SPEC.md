# MIMIR R3.18T — Bounded Following-Property Payload Production Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18S Outcome A
**Production authority before pass:** `f41c59d26ed6c810a640b4fa8cd76129decb32aa`
**Allowed following-payload tags:** exactly `Boolean | ActiveActor`
**Another property control / repeated loop:** forbidden

## 1. Goal

Publish the smallest production composition justified by R3.18S. Starting from the published R3.18Q result after one valid R3.18M true following-property control and exact R3.18P following header, decode exactly one following payload and return its typed value plus exact payload-end stop cursor.

This pass is deliberately not a generic property cursor and not a property loop.

## 2. Frozen evidence authority

```text
R3.18S evidence head/tree           7fed9a90d2cb1e356b2a388503650b434d7f3f87 / c552e5ef2cb8e7d1cb3b4022b3ff1ec6dc763989
R3.18S run/job                      32047433925 / 95438466699 SUCCESS
R3.18S same-head normal CI          32047433876 / 95438466663 SUCCESS
R3.18S artifact                     9293436309 / 18955 bytes
R3.18S artifact digest              sha256:dac07647e288bfc3b177000e1bfa6b9cfd892b80fd77d46c2f4974a3832cf422
frozen rows                         47/47
exact contexts                      18/18
following-payload tags              Boolean=39 / ActiveActor=8
payload widths                      Boolean=1 / ActiveActor=33
native/oracle mismatch              0
another-control bits consumed       0
```

Before mutation, fetch fresh `main`; prove production source/tests are unchanged from `f41c59d26ed6c810a640b4fa8cd76129decb32aa` or re-audit any production drift. Verify the R3.18S authority and artifact identity above plus R3.18P contract SHA256 `0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b`.

## 3. Admitted implementation shape

Reuse existing production primitives rather than duplicating wire logic:

- published R3.18Q bounded following-header composition;
- `decode_replay_network_primitive_scalar_v1` for exact admitted `Boolean` payloads;
- `decode_replay_network_k2_v1` for exact admitted `ActiveActor` payloads, deriving the K2 context from the already-required replay version context without widening it.

The new API/result name must encode bounded **after-first-primitive second-property-payload following-property payload** semantics clearly enough that it cannot be mistaken for a generic property iterator. It may return the existing R3.18Q result plus one typed following payload and exact stop bit.

Continuation only:

```text
R3.18Q valid following_header
-> require exact R3.18P membership already enforced by Q
-> require resolved tag Boolean or ActiveActor
-> start exactly at following_header.payload_start_bit
-> decode exactly one payload with the already-published lower-level decoder
-> Boolean: exactly 1 bit
-> ActiveActor: exactly 33 bits (active:1 + actor:32)
-> stop exactly at returned payload end
-> do not read another property_present bit
```

## 4. Required value identity

For `Boolean`, preserve the existing primitive-scalar typed boolean plus exact payload start/end/width identity. For `ActiveActor`, preserve the K2 `active: bool` and signed actor-id semantic value plus exact payload start/end/width identity. Do not invent duplicate decoders or reinterpret actor identifiers.

## 5. Fail-closed rules

Reject atomically on any R3.18Q composition failure, missing payload start, tag outside exact `Boolean | ActiveActor`, lower-level decoder failure, truncation, wrong exact structural/version context, impossible stop/end inconsistency or any attempted context widening. A failure must not be converted into partial successful following-payload composition.

## 6. Required focused tests

At minimum:

- Boolean success with exact 1-bit width/end/value and representative aligned/unaligned starts;
- ActiveActor success with exact 33-bit width/end/active/actor identity and representative starts;
- R3.18S-shaped real boundary witnesses from both classes without embedding private replay data;
- truncation at every required Boolean/ActiveActor payload boundary;
- tag outside `Boolean | ActiveActor` rejects before payload decode;
- wrong exact R3.18P structural/version context rejects through the Q boundary;
- bytes/bits after payload end may be poisoned without changing the result;
- result is exactly repeatable;
- explicit proof that no another `property_present` bit is read.

Because both admitted forms have total fixed-width value domains, do not fabricate a nonexistent invalid full-width value. Truncation and wrong-decoder/context negatives are the structural malformed controls.

## 7. Clean production scope

Preferred clean scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18t_*.rs`

No Cargo manifest/lockfile, fixture, corpus, continuity file, temporary workflow/tool or support-lane change may enter the clean production commit.

## 8. Validation and publication

Require focused tests, full `mimir-replay`, workspace check/test/clippy at Rust 1.85 floor, repository verifier, exact clean-candidate SHA validation, fresh-main ancestry audit, force-free publication, fresh-main readback and exact published-main validation.

## 9. Hard stop

R3.18T does not admit another `property_present` bit, another property header/payload, repeated/generalized property loops, generic cursor chaining, following-header tags outside `Boolean | ActiveActor`, R3.18P context widening, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening or dependency/corpus/support expansion.

## 10. Outcome gate

### Outcome A
The exact bounded following payload composition is published and all validation gates pass. Then run a separate real-replay differential audit of the published R3.18T API before opening any later property-control boundary.

### Outcome B
A bounded mismatch appears. Record it and keep production at R3.18Q.

### Outcome C
Any scope drift, another-control access, generalized loop, dependency widening, validation contradiction or unadmitted payload/context form. Stop without publication.
