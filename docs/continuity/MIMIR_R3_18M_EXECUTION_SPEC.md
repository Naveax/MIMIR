# MIMIR R3.18M — Bounded Native After-Second-Payload Control-Bit Composition

**Status:** ACTIVE  
**Pass type:** production implementation  
**Evidence authority:** R3.18L Outcome A  
**Production authority before pass:** R3.18J `330ab01890a7c09eff1805e437584fb3be0a1134`  
**Observed control context:** `true=47 / false=0`  
**Following stream/header/payload:** forbidden  
**Repeated/general property loop:** forbidden

## 1. Goal

Publish the smallest native composition justified by R3.18L. Starting only from an already-valid R3.18J result that contains one successfully decoded second payload, validate its exact stop boundary, read exactly one following `property_present` bit and stop one bit later. The only admitted success context is `true`, because R3.18L observed 47 true rows and zero false rows.

## 2. Frozen authority

```text
production SHA/tree                 330ab01890a7c09eff1805e437584fb3be0a1134 / 5540b6a86e53d243dabbabea223a5afa8657521c
production lib blob                 ee9b0c71871df7ff52275581eb7ad4c023b8ba79
R3.18J focused test blob            c5a97c5a17ae2ea292790a020673dd26a0150024
R3.18J implementation               31975731621 / 95234808797 SUCCESS
R3.18J candidate CI                 31975907582 / 95235253244 SUCCESS
R3.18J published CI                 31976100231 / 95235742210 SUCCESS
R3.18L evidence head                9205ac1616e686589938f952782a32f03d0d1488
R3.18L run/job                      31978791346 / 95242213413 SUCCESS
R3.18L same-head CI                 31978791304 / 95242213357 SUCCESS
R3.18L artifact                     9271817700
R3.18L artifact digest              sha256:db5d2db96429a4f2b699dca5176fc4d218f9eb9e4faa8dee813b766896f70c1c
R3.18L rows                         47/47 exact
R3.18L control distribution         false=0 / true=47
R3.18L mismatch                     0
R3.18L following stream/header/payload bits 0/0/0
```

Before mutation, fetch fresh `main`; prove all post-production commits are continuity-only and verify the exact source/test/evidence receipts above.

## 3. Admitted production API shape

Use a deliberately non-generic API tied to an already-valid R3.18J result, conceptually:

```text
input:
  network bytes
  + &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1

precondition:
  prior result contains Some(second_header)
  prior result contains Some(second_payload)
  prior stop_bit == exact second payload end/stop

read:
  control_start = prior.stop_bit
  one LSB-first property_present bit

if bit == true:
  return bounded control result
  property_present = true
  start = control_start
  end = start + 1
  stop_bit = end

if bit == false:
  fail closed as evidence-unadmitted after-second-payload false context
```

The result/API name must encode **after second payload** and **following control** semantics. Do not expose a generic cursor or chainable loop primitive.

## 4. Exact evidence allowlist

R3.18L observed:

```text
true   47
false   0
```

Therefore this composition admits success only for `true`. A false bit must not be treated as a normal terminator yet; no false witness exists for this after-second-payload boundary. A future evidence pass may separately characterize false if real frozen evidence exposes it.

## 5. Fail-closed rules

Reject atomically on:

- missing or internally inconsistent R3.18J second header/payload;
- prior `stop_bit` not equal to the exact second-payload end;
- insufficient bits at the following control position;
- observed false following bit;
- arithmetic/position overflow.

Failure must not perform any following stream lookup/header decode/payload read.

## 6. Required focused tests

At minimum:

```text
true following control -> exact start/end/stop             positive
aligned and unaligned prior stop positions                  positive
post-control poison leaves returned control unchanged       positive
repeat identical invocation                                 exact
false following control                                     reject / unadmitted context
missing control bit                                         reject atomically
prior stop inconsistent with second payload end             reject before bit read
missing second payload / malformed prior composition        reject
scope lock: zero following stream/header/payload calls      exact
scope lock: no while/for property loop in new composition   exact
```

Synthetic byte windows may exercise surgical failure cases, but the next differential audit must return to the immutable R3.18L real lane.

## 7. Clean production scope

Preferred exact scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18m_*.rs`

No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file may enter the clean production commit.

## 8. Source-boundary audit

Before publication prove the new composition contains:

- exactly one following-bit read;
- explicit true-only evidence allowlist;
- explicit false rejection;
- zero following stream/header/payload decoder calls;
- no `while` or `for` property loop;
- no generic repeatedly-chainable public cursor.

## 9. Validation and publication

Required before publication:

- Rust 1.85 focused R3.18M tests;
- full `mimir-replay` suite;
- workspace check/test/clippy;
- full repository verifier;
- exact clean-candidate SHA CI;
- fresh-main ancestry audit;
- force=false fast-forward publication;
- exact published-main readback and CI.

## 10. Hard stop

R3.18M does not admit:

- false following-control success/terminator semantics in this after-second-payload context;
- following stream ID/header/payload;
- any additional `property_present` bit;
- repeated/generalized property loop;
- generic chainable property cursor;
- next actor/frame iteration;
- actor lifecycle mutation;
- raw-state/event/replay-slice/skill/runtime/export widening;
- dependency/fixture/corpus/support expansion.

## 11. Outcome gate

### Outcome A

The true-only one-bit composition is published with exact stop semantics, false fail-closed behavior, no adjacent widening and all validation gates pass. Then run a separate real-replay differential of the published R3.18M API on the immutable R3.18L 47-row lane.

### Outcome B

Implementation reveals a bounded contract mismatch. Record it and keep production at R3.18J.

### Outcome C

Any source drift, false-context widening, following header/payload access, loop/generalization, MSRV failure or validation contradiction. Stop without publication.
