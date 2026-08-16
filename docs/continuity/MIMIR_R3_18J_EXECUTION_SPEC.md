# MIMIR R3.18J — Bounded Native Second-Property Payload Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18I Outcome A
**Production authority before pass:** `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`
**Allowed second-payload tags:** exactly `Int | String`
**Third property / repeated loop:** forbidden

## 1. Goal

Publish the smallest production composition justified by R3.18I. Starting from the published R3.18G result after one valid R3.18B first primitive property, preserve the terminator path unchanged or decode exactly one present second payload and return its typed value plus exact payload end/stop cursor.

This pass is deliberately not a generic property cursor and not a property loop.

## 2. Frozen evidence authority

```text
R3.18I evidence head                45090a2c18fb517088bb411782bbaed0d7d68199
R3.18I run/job                      31975063743 / 95233164711 SUCCESS
R3.18I same-head normal CI          31975063703 / 95233164610 SUCCESS
R3.18I artifact                     9270842140
R3.18I artifact digest              sha256:9890ed33780412a8900692a627b212d80428a08229f9f691d914c8def31e06e2
frozen rows                         94/94
terminator / continuation           47 / 47
second-payload tags                 Int=46 / String=1
native/oracle mismatch              0
third-property bits consumed        0
```

Before mutation, fetch fresh `main`; prove production source/tests are unchanged from `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c` or re-audit any production drift. Verify the evidence receipts and artifact identity above.

## 3. Admitted implementation shape

Reuse existing production primitives rather than duplicating wire logic:

- R3.18G bounded optional second-header composition;
- `decode_replay_network_primitive_scalar_v1` for the exact `Int` second payload;
- `decode_replay_network_k2_v1` for the exact observed `String` second payload with the same admitted context required by the existing K2 decoder.

The new API/result name must encode bounded **after-first-primitive second property payload** semantics. It may return the existing R3.18G result plus an optional typed second payload and exact stop bit.

Terminator:

```text
R3.18G control false
-> second_header=None
-> second_payload=None
-> stop exactly at control end
-> no payload decoder call
```

Continuation:

```text
R3.18G second_header present
-> require resolved tag Int or String
-> start exactly at header.payload_start_bit
-> decode exactly one payload with the already-published lower-level decoder
-> stop exactly at returned payload end
-> do not read the following property_present bit
```

## 4. Required value identity

For `Int`, preserve native signed integer semantics and raw/start/end/width identity from the primitive-scalar result. For `String`, preserve the existing K2 String typed semantic value and exact payload start/end/width identity. Do not invent a second text decoder.

## 5. Fail-closed rules

Reject atomically on malformed/inconsistent first property, R3.18G composition failure, missing payload start, tag outside exact `Int | String`, scalar/K2 decode failure, truncation, invalid String length/context or any stop/end inconsistency. A failure must not be converted into partial successful second-payload composition.

## 6. Required focused tests

At minimum:

- terminator returns no header/no payload and performs zero payload lookup/decode;
- Int second payload success, aligned and unaligned starts, exact 32-bit width/end/value;
- String second payload success in the exact admitted context, exact length/encoding/end/value;
- R3.18I-shaped real boundary witnesses;
- truncation at every required Int payload boundary;
- String truncation / malformed length / wrong context;
- tag outside `Int | String` rejects before payload;
- bytes after payload end may be poisoned without changing the result;
- result is exactly repeatable;
- explicit proof that no third `property_present` bit is read.

## 7. Clean production scope

Preferred clean scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18j_*.rs`

No Cargo manifest/lockfile, fixture, corpus, continuity file, temporary workflow/tool or support-lane change may enter the clean production commit.

## 8. Validation and publication

Require focused tests, full `mimir-replay`, workspace check/test/clippy at Rust 1.85 floor, repository verifier, exact clean-candidate SHA validation, fresh-main ancestry audit, force-free publication, fresh-main readback and exact published-main validation.

## 9. Hard stop

R3.18J does not admit the third `property_present` bit, a third property header/payload, repeated/generalized property loops, generic cursor chaining, second-header tags outside `Int | String`, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening or dependency/corpus/support expansion.

## 10. Outcome gate

### Outcome A
The exact bounded second payload composition is published and all validation gates pass. Then run a separate real-replay differential audit of the published R3.18J API before opening the next property-control boundary.

### Outcome B
A bounded mismatch appears. Record it and keep production at R3.18G.

### Outcome C
Any scope drift, third-control access, generalized loop, dependency widening, validation contradiction or unadmitted payload form. Stop without publication.
