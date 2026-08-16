# MIMIR R3.18D — Minimal Native Existing-Actor Next-Property Control Bit

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18C Outcome A
**Second property decode:** forbidden
**Repeated property loop:** forbidden

## 1. Goal

Publish the smallest production boundary justified by R3.18C: after one already-valid R3.18B K1 first-property result, read exactly the next `property_present` bit at the first property's stop bit, report terminator versus continuation, and stop one bit later.

This pass implements one loop-control observation. It does not implement the loop body for another property.

## 2. Frozen authority

```text
canonical main before pass          f8f6467f2ee652892329f08a3e532b1e1f834fb3
production SHA/tree                 de7a2ba40663bb619ca7bd8654846ce87670d023 / d1889038ca2eaeb8bb0f05e44b811d906f84cf6e
production lib blob                 478ae5b70514fcff79117b834733849517c48500
R3.18B focused test blob            927e9a2c834115d1c918fa96fb6d0690bd03965e
R3.18C authority head               a4b71ad43e5cf55c44c9518b24622ce29214acd2
R3.18C run/job                      31944102614 / 95157425239 SUCCESS
R3.18C same-head normal CI          31944102575 / 95157425128 SUCCESS
R3.18C artifact                     9262820284
R3.18C artifact digest              sha256:95e89cb350cc4c274d2b7a53198d78941bef54ff1b3f6a165b2ba9710659ec07
terminator candidates               47
continuation candidates             47
native/oracle mismatch              0
second stream/payload bits          0 / 0
```

Before mutation, fetch fresh `main` and verify that the production source/test blobs still match the R3.18B authority and that only continuity commits exist after `de7a2ba40663bb619ca7bd8654846ce87670d023`.

## 3. Admitted production API shape

Prefer an API structurally tied to the already-decoded first property, for example conceptually:

```text
input:
  network bytes
  + &ReplayNetworkExistingActorSinglePrimitivePropertyV1

validate:
  first_property.header.stop_bit == first_property.scalar.payload_start_bit
  first_property.stop_bit == first_property.scalar.payload_end_bit
  first_property.scalar.stop_bit == first_property.scalar.payload_end_bit

read:
  exactly one LSB-first bit at first_property.stop_bit

return:
  next_property_present: bool
  property_present_start_bit: u64
  property_present_end_bit: u64
  stop_bit: u64

require:
  property_present_start_bit == first_property.stop_bit
  property_present_end_bit == property_present_start_bit + 1
  stop_bit == property_present_end_bit
```

The function name/type should explicitly encode **after first primitive property** semantics rather than expose a generic repeatedly chainable property-loop cursor.

## 4. Fail-closed rules

Reject atomically on:

- malformed/internally inconsistent R3.18B first-property boundary;
- arithmetic overflow computing the one-bit end;
- missing next bit / truncated bytes;
- any start beyond the provided byte range.

On failure, expose no successful control result and consume no observable cursor state.

## 5. Required focused tests

At minimum:

```text
false terminator                         positive
true continuation                       positive
aligned first-property end               positive
unaligned first-property end             positive
R3.18C Float terminator shape            positive
R3.18C Int=62 continuation shape         positive
exact start/end/stop                     exact
post-control poison bits                 no effect
missing next bit                         reject atomically
malformed first-property boundary        reject
repeatability                            exact
```

Tests may construct R3.18C-shaped first-property results through the existing R3.18B production API; do not check in raw oracle payload windows merely to satisfy a regression.

## 6. Source reuse rule

Reuse existing private/native bit primitives where practical. Do not reimplement bounded stream decoding, property resolution, scalar payload decoding, or Boxcars behavior. This pass needs only one bit after an already-complete R3.18B result.

## 7. Clean production scope

Preferred clean scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18d_*.rs`

A separate tiny source module is allowed only if direct inspection shows it materially improves isolation. No `Cargo.toml`, `Cargo.lock`, fixture, corpus, workflow, temporary tool, support lane, or continuity file may enter the clean production commit.

## 8. Hard stop

R3.18D does **not** admit:

- decoding the second property stream ID;
- resolving the second property header/tag;
- decoding the second property payload;
- calling the control-bit reader repeatedly as a property loop;
- a `while` / `for` production property loop;
- K2/K3/K4 composition through the R3.18B wrapper;
- next actor / next frame iteration;
- actor lifecycle table mutation;
- raw-state/event/replay-slice/skill/runtime/export widening.

## 9. Validation and publication

Required before publication:

- exact source-boundary audit proving one-bit-only behavior;
- focused R3.18D tests;
- full `mimir-replay` suite;
- workspace check/test/clippy under the Rust 1.85 floor;
- full repository verifier;
- exact clean-candidate SHA validator;
- fresh-main ancestry audit;
- force-free fast-forward publication;
- exact published-main validator/readback.

## 10. Outcome gate

### Outcome A

The one-bit API is published with the exact boundary above and every validation gate passes. Then run a separate real-replay differential audit of the production control result before any second-property header/body admission.

### Outcome B

Implementation reveals an unresolved first-property/control-boundary contract. Record it and keep production at R3.18B.

### Outcome C

Any source drift, cursor ambiguity, scope widening, second-property consumption, MSRV failure, or validation contradiction. Stop without publication.
