# MIMIR R3.18H — Production Second-Property Header Real-Replay Differential Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / differential validation
**Production authority:** R3.18G `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`
**Production mutation:** forbidden
**Second-property payload decode:** forbidden
**Third property / repeated loop:** forbidden

## 1. Goal

Differentially validate the published R3.18G optional second-property-header composition over the frozen 47-replay R3.18F lane. Prove production behavior, not the lower-level header primitive in isolation.

## 2. Frozen authority

```text
production SHA/tree                 2b608aafae97b10ecbc884f99e4bd4a73abf7a5c / b130caf211ce72577870c70d6c0d87cd006e1b29
production parent                   289c9cec0b709a27665370871dc7480b5df93270
lib.rs blob                         5e2b9e5be9c6692e499abc97a89655c603728cef
R3.18G focused test blob            d56bf97d250b426e23fec4610cbb9ead6ec8a142
R3.18G implementation               31957142924 / 95189376563 SUCCESS
R3.18G same-trigger normal CI       31957142895 / 95189376551 SUCCESS
R3.18G exact candidate validator    31957646865 / 95190626723 SUCCESS
R3.18G published-main validator     31957892048 / 95191254798 SUCCESS
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
R3.18F evidence head/tree           27a855a9cfb82a0294dd1601e4da01c9fdfad264 / 4058b67da82e9fbfcc078e975b26d186ec68e6f0
R3.18F artifact                     9264673141
R3.18F artifact digest              sha256:e31e09abf322b6458f9034b06efe5502bb3b7f1011dfb08c9ffd6d1b1cd1b361
R3.18F source-scope SHA256          492f63c3cfcb27967426816f97858c8f4ad1d9ebb6ce40719f6d829ff3f0ea55
R3.18F replay-identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
R3.18F witnesses SHA256             99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
R3.18F aggregate SHA256             57c90cb3617461aea1a078a7b0f72ae301fd35fc9d7c4f9fe56de6d7633a4a04
```

Before evidence, fetch fresh `main`, prove production source blobs unchanged from `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`, verify every receipt above, and verify the 47 replay identities against the frozen lane.

## 3. Required source lane

Reuse the frozen R3.18F 94-row boundary set:

```text
47 terminator rows
47 continuation rows
continuation second-header tags: Int=46 / String=1
```

Do not silently reselect easier witnesses. If any frozen replay or boundary no longer reproduces, that is evidence drift and must stop the pass.

## 4. Production differential checks

For every terminator row, invoke the published R3.18G composition and require:

- the first R3.18B property is exact;
- R3.18D control coordinates/value are exact;
- `next_property_present == false`;
- `second_header == None`;
- stop equals the one-bit control end;
- no second-header lookup or payload access occurs after the false bit.

For every continuation row, require:

- the first R3.18B property is exact;
- R3.18D control coordinates/value are exact and true;
- a second header is returned;
- second `property_present` start/end exact;
- stream start/end/value, stream bound and prop-id bits exact;
- resolved property object exact;
- resolved tag exact, with aggregate distribution exactly `Int=46 / String=1`;
- `payload_start_bit` exact;
- returned `stop_bit == payload_start_bit` exact;
- zero second-payload bits consumed;
- zero third-property bits consumed.

Native/oracle mismatch count must be zero.

## 5. Negative controls

At minimum:

- truncation before all required continuation header bits -> reject atomically;
- unresolved second stream -> reject before payload;
- second-header tag outside exact `Int/String` -> reject before payload;
- terminator with poisoned/missing lookup plan after first property -> still return `None` without lookup;
- bits at and after continuation `payload_start` may be poisoned without changing the returned header;
- repeated identical invocation -> exact identical result.

Where a real frozen row can exercise truncation, prefer it. Synthetic controls may supplement but may not replace real-lane differential checks.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing at least:

- exact production SHA/tree/blobs and validation receipts;
- pinned Boxcars SHA;
- frozen replay identity/source-scope hashes;
- per-row oracle/native comparison without raw private payload windows;
- aggregate terminator/continuation counts;
- exact tag counts;
- negative-control results;
- second-payload / third-property consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- hashes for every evidence file in the artifact.

## 7. Required validation

- deterministic double-run equality of the evidence selection/comparison;
- production focused R3.18G tests PASS on the evidence head;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18H may not change production Rust, Cargo files, fixtures, corpus, dependencies or support lanes. It may not decode or semantically claim the second payload, inspect a third property, create a property loop, widen second-header tags, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 94 frozen rows match the published R3.18G production composition exactly, negatives pass, mismatch is zero, second-payload/third-property consumption remains `0/0`, privacy passes and production mutation is zero. Admit R3.18H evidence and only then define the next separate bounded pass.

### Outcome B

A reproducible production/oracle mismatch appears within the already-admitted R3.18G boundary. Record exact privacy-safe coordinates and keep any further payload/loop widening closed.

### Outcome C

Authority drift, source mutation, witness reselection, privacy failure, second-payload access, third-property access, tag widening or validation contradiction. Stop without admission.
