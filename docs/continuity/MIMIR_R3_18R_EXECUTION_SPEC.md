# MIMIR R3.18R — Published Following-Property Header Real-Replay Differential Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / differential validation
**Production authority:** R3.18Q `f41c59d26ed6c810a640b4fa8cd76129decb32aa`
**Production mutation:** forbidden
**Following-property payload decode:** forbidden
**Another property control / repeated loop:** forbidden

## 1. Goal

Differentially validate the published R3.18Q bounded following-property-header composition over the exact immutable 47-row R3.18O lane. Prove the production API itself, not merely the lower-level header primitive, and preserve the R3.18P exact-tuple boundary.

## 2. Frozen authority

```text
production SHA/tree                 f41c59d26ed6c810a640b4fa8cd76129decb32aa / 606db4b5778e5218f2bd0117cc5dd72d7f3e37a5
production parent                   1a3f89e7256c7c7ff4bf6b747a434504f1f2e572
production lib.rs blob              b01b1e8629a4f4bc2452e67024ffb0d064bf58fb
R3.18Q focused test blob            4bb65af1d533752edc062202192232d6f1d4239c
R3.18Q implementation authority     32026722346 / 95377559363 SUCCESS
R3.18Q same-trigger ops CI          32026722356 / 95377559490 SUCCESS
R3.18Q exact candidate CI           32027055064 / 95378560725 SUCCESS
R3.18Q published-main CI            32027421491 / 95379649817 SUCCESS
R3.18P contract SHA256              0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
R3.18O evidence head/tree           5046e1594b87ce2828db5faa48aceba456c3166f / 74fb036dfde837e3ecb7e459da00df9ff6c22e28
R3.18O authority run/job            32017369100 / 95349613184 SUCCESS
R3.18O artifact                     9284144768 / 25129 bytes
R3.18O artifact digest              sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d
R3.18O source-summary SHA256        f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc
R3.18O header-rows SHA256           599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4
R3.18O aggregate SHA256             170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233
```

Before evidence, fetch fresh `main`, require exact production SHA/tree/blobs above, verify the immutable R3.18O artifact and 11/11 inner manifest, verify R3.18P contract SHA256, and prove witness reselection remains zero.

## 3. Required source lane

Reuse exactly the frozen R3.18O 47 rows. Do not reselect easier replays or coordinates.

Frozen aggregate identity:

```text
rows                                47
following control true              47
exact structural/version tuples     18
Boolean rows                        39
ActiveActor rows                    8
version                             868.32 / net10 on all 47
following payload bits consumed     0
another control bits consumed       0
```

All 47 witnesses must reconstruct the same valid R3.18J prior and R3.18M true control used by R3.18O.

## 4. Published-production differential checks

For every frozen row invoke the published `decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1` API and require:

- the R3.18J prior reconstructs exactly at the frozen second-payload end;
- embedded R3.18M control start/value/end/stop equals the frozen control exactly;
- `following_property_present == true`;
- following header `property_present` start/end exact;
- stream start/end/value exact;
- `stream_id_bound` and `prop_id_bits` exact;
- resolved property-object index exact;
- resolved attribute tag exact;
- replay `(version_major, version_minor, net_version)` exact;
- the full seven-field tuple is a member of the immutable R3.18P contract;
- returned `following_header` equals the direct stateless native header result;
- returned `stop_bit == following_header.payload_start_bit` exact;
- zero following-payload bits and zero another-control bits consumed.

Native/oracle mismatch count must be zero on 47/47.

## 5. Negative controls

At minimum:

- truncation before all required following-header bits -> reject atomically;
- prior actor-object mismatch -> reject;
- unresolved/invalid following stream or property lookup -> reject before payload;
- resolved tuple outside the exact R3.18P set -> reject before payload;
- fabricated Cartesian tuple from individually observed components -> reject;
- wrong replay version with otherwise matching components -> reject;
- bits at and after `payload_start` may be poisoned without changing the returned production header;
- repeated identical invocation -> exact identical result.

Real frozen rows should exercise truncation and production equality wherever possible. Synthetic negatives may supplement but may not replace the 47-row real-lane differential.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing at least:

- exact production SHA/tree/lib/test blobs and validation receipts;
- exact R3.18P contract hash and immutable R3.18O evidence receipts;
- frozen replay/witness identity without private raw payload windows;
- per-row oracle/published-Q comparison;
- exact tuple and multiplicity summary;
- negative-control results;
- following-payload / another-control consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- hashes for every evidence file in the artifact.

## 7. Required validation

- deterministic double-run equality of the frozen selection/comparison;
- permanent focused R3.18Q tests PASS on the evidence head;
- full `mimir-replay` PASS;
- workspace format/check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18R may not change production Rust, Cargo files, fixtures, corpus, dependencies or support lanes. It may not decode or semantically claim the following payload, inspect another `property_present` bit, create a repeatable/generalized property loop or public cursor, widen R3.18P membership, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactual rollouts or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen rows match the published R3.18Q production API exactly, all negatives pass, mismatch is zero, following-payload/another-control consumption remains `0/0`, witness reselection is zero, privacy passes and production mutation is zero. Admit R3.18R evidence. A later **separate** pass may then define a bounded following-payload evidence/contract boundary; R3.18R itself admits no payload.

### Outcome B

A reproducible published-Q/oracle mismatch appears inside the already-admitted R3.18Q boundary. Record exact privacy-safe coordinates and keep payload/loop widening closed.

### Outcome C

Authority drift, production/source mutation, witness reselection, privacy failure, payload/later-control access, exact-contract widening or validation contradiction. Stop without admission.
