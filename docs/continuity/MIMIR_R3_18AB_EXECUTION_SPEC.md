# MIMIR R3.18AB — Published R3.18AA Post-W Following-Header Differential Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / differential validation
**Production authority:** R3.18AA `9392240c49f95766c214afee9865fed4155a87a4`
**Production tree:** `968520d480f78c528086e4e31b2ce307f4f8d232`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Another property control / repeated loop:** forbidden

## 1. Goal

Differentially validate the published R3.18AA bounded post-W following-header composition over the exact immutable 47-row R3.18Y lane. Prove the published production API itself, not merely the lower-level stateless header primitive, while preserving the boundary-specific R3.18Z exact-tuple contract.

## 2. Frozen authority

```text
production SHA/tree                 9392240c49f95766c214afee9865fed4155a87a4 / 968520d480f78c528086e4e31b2ce307f4f8d232
production parent                   ac24d29edeacd04152afe318e25ae296385159c3
production lib.rs blob              46523f47f94231362b60f8aee038e943e41c7972
R3.18AA focused test blob           7df8f84af37d771b12da1334bd195634e4cc6a54
R3.18AA builder authority           32142503228/95728286216 SUCCESS
R3.18AA clean-candidate CI          32143161309/95730448274 SUCCESS
R3.18AA published-main CI           32143631391/95731995111 SUCCESS
R3.18Z contract SHA-256             81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18Y evidence head                413d6c24f8f390a57c21ed345f3f868c263f413c
R3.18Y authority                    32076198677/95529856476 SUCCESS
R3.18Y artifact                     9303584468 / sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh `main`, require the exact production SHA/tree/blobs above, verify the immutable R3.18Y artifact and its internal manifest, verify the R3.18Z contract byte-for-byte, and prove witness reselection remains zero.

## 3. Required source lane

Reuse exactly the frozen R3.18Y 47 rows. Do not reselect easier replays, actors or coordinates.

Frozen aggregate identity:

```text
rows                                47
R3.18W following control true       47
exact R3.18Z contexts               18
ActiveActor / Int / UniqueId        39 / 7 / 1
version                             868.32 / net10
following payload bits consumed     0
another control bits consumed       0
```

Every row must reconstruct the same upstream published boundary used by R3.18Y and begin the one following header at the exact frozen R3.18W control coordinate.

## 4. Published-production differential checks

For every frozen row invoke the published `decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1` API and require:

- embedded/recomputed R3.18W control start/value/end/stop equals the frozen Y authority exactly;
- `following_property_present == true`;
- following header `property_present` start/end exact;
- stream start/end/value exact;
- `stream_id_bound` and `prop_id_bits` exact;
- resolved property-object index exact;
- resolved attribute tag exact;
- replay `(version_major, version_minor, net_version)` exact;
- complete seven-field tuple belongs to the immutable R3.18Z contract;
- returned `following_header` equals both the frozen R3.18Y header row and the direct stateless native header result;
- returned `stop_bit == following_header.payload_start_bit` exact;
- zero following-payload bits and zero another-control bits consumed.

Published/native/oracle mismatch count must be zero on 47/47.

## 5. Negative controls

At minimum:

- truncation before all required following-header bits -> reject atomically;
- prior actor-object mismatch -> reject;
- unresolved or invalid following stream/property lookup -> reject before payload;
- complete tuple outside the exact R3.18Z set -> reject before payload;
- fabricated Cartesian tuple from individually observed components -> reject;
- wrong replay version with otherwise matching components -> reject;
- R3.18P-valid but Z-absent `(60,5,102,Boolean,868,32,10)` -> reject;
- bits at and after `payload_start` may be poisoned without changing the returned header;
- repeated identical invocation -> exact identical result.

Real frozen rows must carry the positive differential; synthetic negatives may supplement but may not replace the 47-row lane.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing at least:

- exact production SHA/tree/lib/test blobs and validation receipts;
- exact R3.18Z contract hash and immutable R3.18Y evidence receipts;
- frozen replay/witness identity without private raw payload windows;
- per-row frozen-Y/direct-native/published-AA comparison;
- exact tuple and multiplicity reconstruction;
- negative-control results;
- following-payload / another-control consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- hashes for every evidence file in the artifact.

## 7. Required validation

- deterministic double-run equality of the frozen selection/comparison;
- permanent focused R3.18AA tests PASS on the evidence head;
- full `mimir-replay` PASS;
- workspace format/check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18AB may not change production Rust, Cargo files, fixtures, corpus, dependencies or support lanes. It may not decode or semantically claim the post-W following payload, inspect another `property_present` bit, create a repeatable/generalized property loop or public cursor, widen R3.18Z membership, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactual rollouts or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen rows match the published R3.18AA production API exactly, all negatives pass, mismatch is zero, following-payload/another-control consumption remains `0/0`, witness reselection is zero, privacy passes and production mutation is zero. Admit R3.18AB evidence. Only a later separate R3.18AC pass may characterize the one post-AA following payload; R3.18AB itself admits no payload.

### Outcome B

A reproducible published-AA/frozen-Y/native mismatch appears inside the already-admitted R3.18AA boundary. Record exact privacy-safe coordinates and keep payload/loop widening closed.

### Outcome C

Authority drift, production/source mutation, witness reselection, privacy failure, payload/later-control access, exact-contract widening or validation contradiction. Stop without admission.
