# MIMIR R3.18I — Second-Property Payload Contract / Evidence Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / payload boundary and semantic characterization
**Production authority:** R3.18G `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`
**Prior differential authority:** R3.18H `1db03fddabf84bfa189f983fa4a3b9110d105442`
**Production mutation:** forbidden
**Third property / repeated loop:** forbidden

## 1. Goal

Characterize exactly one second-property payload after the already-proven R3.18G second header on the frozen real-replay lane. Establish exact payload end and semantic agreement separately for the observed `Int=46` and `String=1` continuation classes. Do not compose that payload into production yet.

## 2. Frozen authority

```text
canonical continuity base           63f5de4e49abaf76fe6441a255a1a6770388a63c
production SHA/tree                 2b608aafae97b10ecbc884f99e4bd4a73abf7a5c / b130caf211ce72577870c70d6c0d87cd006e1b29
production lib.rs blob              5e2b9e5be9c6692e499abc97a89655c603728cef
R3.18G focused test blob            d56bf97d250b426e23fec4610cbb9ead6ec8a142
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
R3.18F evidence head                27a855a9cfb82a0294dd1601e4da01c9fdfad264
R3.18F artifact                     9264673141 / sha256:e31e09abf322b6458f9034b06efe5502bb3b7f1011dfb08c9ffd6d1b1cd1b361
R3.18F replay identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
R3.18F frozen witnesses SHA256      99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
R3.18H evidence head/tree           1db03fddabf84bfa189f983fa4a3b9110d105442 / be84d7709d60477bcbb916a11b4496dbddac2ab2
R3.18H run/job                      31960174729 / 95196833572 SUCCESS
R3.18H same-head CI                 31960174713 / 95196833409 SUCCESS
R3.18H artifact                     9267045757 / sha256:340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645
```

Fresh-read all authorities before running. Any drift or witness reselection stops the pass.

## 3. Exact source lane

Reuse exactly the frozen 94 rows:

```text
47 terminators
47 continuations
continuation tags: Int=46 / String=1
```

Terminators remain negative controls. They have no admitted second payload and must not cause a lookup or payload read after the false control bit.

## 4. Continuation payload evidence

For every continuation row:

1. reconstruct and verify the already-admitted first property + R3.18G second header exactly;
2. begin payload work only at that second header's proven `payload_start_bit`;
3. obtain pinned-oracle second payload start/end/semantic value without consuming the next property-control bit;
4. invoke an existing native lower-level decoder only if the exact already-admitted tag/context contract applies;
5. compare native/oracle payload width, end bit and semantic value exactly under that decoder's existing comparison rules;
6. stop at the second payload end and record zero third-property bits consumed.

`Int` and `String` are separate evidence classes. The single String row cannot be generalized from the 46 Int rows. If its exact context falls outside the already-admitted K2 String production contract, record that fact and split the next pass instead of widening by analogy.

## 5. Required negative controls

At minimum:

- all 47 terminators: no second payload access;
- truncation at each required payload boundary: atomic reject;
- wrong tag/native decoder pairing: reject;
- wrong/unadmitted context: reject;
- post-payload poison: returned one-payload result unchanged;
- repeated identical invocation: byte-for-byte/field-for-field identical summary;
- third `property_present` bit poison or removal must not matter because R3.18I may not read it.

Real frozen rows should exercise truncation wherever possible. Synthetic controls may supplement but not replace real-lane checks.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact with:

- exact authority SHAs/trees/blobs/runs/artifacts;
- frozen replay/witness hashes;
- per-row class, payload start/end/width and privacy-safe semantic comparison result;
- separate Int and String aggregates;
- negative controls;
- zero third-property consumption counter;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA256 for every artifact file.

Do not emit private raw payload windows or replay-identifying user data beyond the already-approved replay identity scheme.

## 7. Validation

Require:

- exact 94-row frozen identity set;
- deterministic double-run equality;
- all applicable native/oracle payload comparisons exact;
- focused existing decoder tests PASS;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18I may not change production Rust/Cargo/lockfile/fixtures/corpus/support lanes. It may not publish a second-payload composition, read a third `property_present` bit/header/payload, create a repeated/generalized property loop, widen second-header tag contexts, iterate next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 continuation payloads are exactly characterized through payload end, applicable existing native decoders match pinned oracle semantics/end bits, the 46 Int and 1 String classes are both resolved under already-admitted contracts, negatives pass, third-property consumption is zero and mutation counters are zero. Admit evidence and open only a **separate bounded production second-property payload composition** pass.

### Outcome B

The Int class is exact but the String row is unresolved, outside the admitted K2 String context, or needs additional wire evidence. Admit only the supported evidence facts and open a narrower String payload evidence/contract pass. Production second-payload composition remains closed unless a separately scoped subset is explicitly admitted.

### Outcome C

Authority drift, witness reselection, native/oracle mismatch inside an already-admitted decoder contract, privacy failure, production mutation, or any third-property access. Stop without widening.
