# MIMIR R3.18W — Bounded Native After-Following-Payload Control-Bit Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18V Outcome A
**Production authority before pass:** R3.18T `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b`
**Observed control context:** `true=47 / false=0`
**Following stream/header/payload:** forbidden
**Additional control bit:** forbidden
**Repeated/general property loop:** forbidden

## 1. Goal

Publish the smallest native composition justified by R3.18V. Starting only from an already-valid R3.18T result that contains exactly one admitted following payload, validate its exact payload-end stop, read exactly one following `property_present` bit, admit only `true`, and stop exactly one bit later. Do not decode the next stream/header/payload.

## 2. Frozen authority

```text
production SHA/tree                  c2765ab9f04f9c981a6868cb6503bdf0e339ce1b / a6f27fe606cd3446da02ef1cb8cf53fff071e383
production lib/test blobs            cf992670b461e9d923e773ed375bef2b42aea20d / 430676ec118fa0755a9c64abc0067bf5c5c88d05
R3.18V evidence head/tree            2b0c9f01559e77a6fdf21a097b8ab4d1a27b6ff5 / 229b3d68a82f6dadc19518614e27ff09e8006ad2
R3.18V authority                     32057732310 / 95471639989 SUCCESS
R3.18V same-head CI                  32057732335 / 95471640230 SUCCESS
R3.18V artifact                      9297068554 / 20484 bytes / sha256:e17426aad6d476eba17bb471dc92cd24b4b4d8727ad427ad15fa6e9c1dda9eb2
R3.18V frozen rows                   47/47
R3.18V control distribution          false=0 / true=47
R3.18V native/oracle mismatch        0
R3.18V next stream/header/payload/second-control bits 0/0/0/0
```

Before mutation fetch fresh `main`, prove production source/test blobs remain exact and verify the authority receipts and artifact above.

## 3. Admitted production API shape

Use a deliberately non-generic API tied to an already-valid R3.18T result, conceptually:

```text
input:
  network bytes
  + &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1

precondition:
  prior header composition remains internally consistent
  prior following payload is Boolean or ActiveActor
  prior stop_bit == exact following-payload end

read:
  control_start = prior.stop_bit
  exactly one LSB-first property_present bit

if bit == true:
  return bounded after-following-payload control result
  property_present = true
  start = control_start
  end = start + 1
  stop_bit = end

if bit == false:
  fail closed as evidence-unadmitted context
```

The public API/result names must encode the **after following payload** boundary. Do not expose a generic loop/cursor primitive.

## 4. Exact evidence allowlist

R3.18V observed exactly:

```text
true   47
false   0
```

Therefore R3.18W may succeed only for `true`. A false bit is not a normal terminator in this production context yet because no false real witness exists at this exact boundary.

## 5. Fail-closed rules

Reject atomically on:

- missing or inconsistent nested R3.18T following header/payload composition;
- prior `stop_bit` not equal to the exact Boolean or ActiveActor payload end;
- insufficient data for one control bit;
- observed false control;
- arithmetic/position overflow.

Failure must perform zero next-stream lookup/header decode/payload read and zero additional-control reads.

## 6. Required focused tests

At minimum:

```text
true control -> exact start/end/stop                     positive
Boolean prior payload boundary                           positive
ActiveActor prior payload boundary                       positive
aligned and unaligned prior stop positions               positive
repeat identical invocation                              exact
post-control poison leaves returned control unchanged    positive
false control                                             reject / unadmitted
missing control bit                                       reject atomically
prior stop inconsistent with payload end                 reject before read
malformed/missing prior payload composition              reject
scope lock: next stream/header/payload decoder calls 0   exact
scope lock: second later control reads 0                 exact
scope lock: no property while/for loop                   exact
```

Synthetic byte windows may exercise surgical negatives, but the next differential audit must return to the immutable R3.18V 47-row lane.

## 7. Clean production scope

Preferred exact scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18w_*.rs`

No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file may enter the clean production commit.

## 8. Source-boundary audit

Before publication prove:

- exactly one new control-bit read;
- explicit true-only evidence allowlist and false rejection;
- zero following stream/header/payload decoder calls;
- zero second-later-control reads;
- no `while`/`for` property loop;
- no generic repeatedly-chainable public cursor.

## 9. Validation and publication

Required:

- Rust 1.85 focused R3.18W tests;
- full `mimir-replay` suite;
- workspace check/test/clippy;
- repository verifier;
- exact clean-candidate SHA CI;
- fresh-main ancestry audit;
- force=false fast-forward publication;
- exact published-main readback and CI.

## 10. Hard stop

R3.18W does not admit false control success, the following stream/header/payload, any additional control bit, repeated/generalized property loop/cursor, next actor/frame/lifecycle behavior, raw state/events, replay slicing, skills, counterfactual execution, runtime/export widening, or dependency/fixture/corpus/support expansion.

## 11. Outcome gate

### Outcome A

Publish the true-only one-bit composition with exact stop semantics, false fail-closed behavior and all validation gates PASS. Then open a separate real-replay published-API differential on the immutable R3.18V lane.

### Outcome B

A bounded contract mismatch is reproducible. Record it and keep production at R3.18T.

### Outcome C

Any authority drift, false-context widening, next header/payload access, second control read, loop/generalization, MSRV failure or validation contradiction. Stop without publication.
