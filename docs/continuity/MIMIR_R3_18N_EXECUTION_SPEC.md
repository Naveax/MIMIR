# MIMIR R3.18N — Published After-Second-Payload Control Real-Replay Differential Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / production differential
**Production authority:** R3.18M `fd74ba8c520ab83b808730572c41e45d6dc616e6`
**Production mutation:** forbidden
**Following stream/header/payload:** forbidden

## 1. Goal

Differentially validate the published R3.18M true-only following-control composition over the exact frozen R3.18L 47-row lane. Invoke the production R3.18M API, not a lower-level bit reader, and prove exact start/value/end/stop behavior without consuming the following stream ID or any later property data.

## 2. Frozen authority

```text
production SHA/tree                 fd74ba8c520ab83b808730572c41e45d6dc616e6 / 6285928b3ca724c77b761e70c54f7bd0763f11f0
lib.rs blob                         029c48e38ea0257f8cdb3fa8715bde5a789213e7
R3.18M focused test blob            a9bd2d0a8007c8cae76a0d14ad0c11ed387fe5a6
implementation v3                   31999687944 / 95297550306 SUCCESS
clean-candidate CI                  31999898754 / 95298116788 SUCCESS
published-main CI                   32000211020 / 95298954375 SUCCESS
R3.18L evidence head                9205ac1616e686589938f952782a32f03d0d1488
R3.18L artifact                     9271817700
R3.18L artifact digest              sha256:db5d2db96429a4f2b699dca5176fc4d218f9eb9e4faa8dee813b766896f70c1c
frozen rows                         47 continuation rows
control distribution                false=0 / true=47
R3.18L native/oracle mismatch       0
following stream/header/payload     0 / 0 / 0
```

Before evidence, fetch fresh main, verify production source/test blobs and every receipt above, then reuse the exact R3.18L witnesses without reselection.

## 3. Required differential checks

For each of 47 rows:

- reconstruct the exact valid R3.18J second-payload result used by R3.18L;
- invoke `decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1`;
- require `property_present_start_bit == R3.18J stop == oracle control start`;
- require value `true`;
- require exact control end and `stop_bit == start + 1`;
- require oracle/native mismatch zero;
- require zero following stream/header/payload bits consumed.

No false production success is expected or admitted.

## 4. Negative controls

At minimum: missing/truncated following control bit; malformed prior R3.18J stop; missing/inconsistent prior second header/payload; synthetic false following-control rejection; repeated identical invocation; and poison beginning at returned stop. All must fail closed or remain invariant as appropriate.

## 5. Evidence artifact

Emit a privacy-safe immutable artifact containing exact production receipts, frozen replay/witness identities, per-row control comparison without raw private payload windows, aggregate counts, negative controls, following stream/header/payload consumption counters, mutation counters and hashes of every evidence file.

## 6. Required validation

Focused R3.18M regression, full `mimir-replay`, workspace check/test/clippy, repository verifier, deterministic repeatability, same-head normal CI, privacy scan and production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 7. Hard stop

No production Rust/Cargo/fixture/corpus/support mutation. Do not consume or semantically claim the following stream ID, header, payload or another control bit. No repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening.

## 8. Outcome gate

### Outcome A
All 47 frozen rows match the published R3.18M API exactly with value true, zero mismatch and zero following stream/header/payload bits consumed. Admit R3.18N evidence, then define a separate evidence pass for exactly the following property header through its payload start.

### Outcome B
A reproducible production/authority mismatch appears. Record it and keep the following-property header boundary closed.

### Outcome C
Authority drift, witness reselection, source mutation, privacy failure, following-stream access or validation contradiction. Stop without admission.
