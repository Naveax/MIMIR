# MIMIR R3.18AE — Published R3.18AD Ordinal-3 Payload Differential Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / published-production differential validation
**Production authority:** R3.18AD `ccadbf148381c007890d13d5fe8120866a0f40f9`
**Production tree:** `0882601060d0bb6d37fcc03ae7273dcf50dd0be3`
**Production mutation:** forbidden
**Another property control / repeated loop:** forbidden

## 1. Goal

Differentially validate the published R3.18AD bounded post-AA payload composition over the exact immutable R3.18AC 47-row lane. Prove the published production API itself, not merely its lower-level K2/scalar primitives, through exactly one ordinal-3 payload end.

R3.18AE must preserve the full R3.18AA/R3.18Z header boundary, the exact R3.18AC payload shapes, witness identity and stop boundary. It may not inspect another `property_present` bit.

## 2. Frozen authority

```text
production SHA/tree                  ccadbf148381c007890d13d5fe8120866a0f40f9 / 0882601060d0bb6d37fcc03ae7273dcf50dd0be3
production parent                    671cd19a7d034b1377de5bed1dfd36600f45c8d7
production lib/test blobs            1254d5a3d16e7b97b1dee87a8b459514d25749ef / 013ad6da94b866ecaca94cd6420e7568d9b4b5ee
R3.18Z contract SHA256               81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18AC evidence head/tree           62bc43dd12dbde48fb503cccd4da46dfcf6ae252 / 9d5b550b4bb93688db9f3a67583067adb32425f6
R3.18AC authority run/job            32237834815 / 96021661994 SUCCESS
R3.18AC same-head CI                 32237834813 / 96021661894 SUCCESS
R3.18AC artifact                     9359697636 / 12010 bytes
R3.18AC artifact digest              sha256:a6914044dfd8991d74b95caeb3507fb2469175c4458c5b50b55395b8ea67b9df
R3.18AD builder                      32241956973 / 96034261394 SUCCESS
R3.18AD validation PR CI             32242293315 / 96035296746 SUCCESS
R3.18AD clean push CI                32242994502 / 96038355071 SUCCESS
R3.18AD published-main CI            32242742010 / 96036666443 SUCCESS
```

Before evidence, fetch fresh `main`, require the exact published R3.18AD SHA/tree/blobs and continuity admission, verify the immutable R3.18AC artifact and its internal manifest, verify the R3.18Z contract byte-for-byte, and prove witness reselection remains zero.

## 3. Required source lane

Reuse exactly the frozen R3.18AC 47 rows. Do not select new replays, actors, properties, coordinates or easier payload classes.

Frozen payload authority:

```text
rows                                47
header contexts                     exact R3.18Z membership only
ActiveActor                         39 × 33 bits
Int                                  7 × 32 bits
UniqueId                             1 × 80 bits
UniqueId layout                      system_id=1 / Steam
version                              868.32 / net10 / non-RL223
oracle/native mismatch               0
witness reselection                  0
another control bits consumed        0
```

## 4. Published-production differential checks

For every frozen row invoke `decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1` and require:

- the embedded/recomputed R3.18AA header composition equals the frozen AC/AB authority through `payload_start`;
- the complete seven-field header tuple belongs to the immutable R3.18Z contract;
- published payload tag equals the frozen AC tag;
- published payload start equals the frozen AC payload start;
- published payload end / stop equals the frozen AC payload end;
- published payload width equals the frozen AC width;
- privacy-safe semantic value equals pinned Boxcars and the direct lower-level native decoder;
- ActiveActor rows are exactly width 33;
- Int rows are exactly width 32;
- the single UniqueId row is exactly system_id=1 / Steam / width 80;
- returned `stop_bit` equals the one payload end exactly;
- zero bits from another property-control boundary are consumed.

Published/frozen/oracle/direct-native mismatch count must be zero on 47/47.

## 5. Negative controls

At minimum:

- prefix truncation before complete required payload -> reject atomically;
- wrong replay/K3 context -> reject before widening;
- wrong or unsupported payload tag -> reject;
- lower-level-valid but R3.18AC-unadmitted UniqueId shape, including Epic 312-bit, -> reject at the R3.18AD boundary;
- post-payload poison -> returned AD result remains identical;
- repeated identical invocation -> exact identical result;
- malformed or non-R3.18Z header context -> reject through the embedded AA gate;
- another `property_present` bit is never read.

Real frozen rows must carry the positive differential. Synthetic negatives may supplement but may not replace the 47-row lane.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing at least:

- exact production SHA/tree/lib/test blobs and validation receipts;
- exact R3.18AC and R3.18Z authority receipts;
- frozen replay/witness identity without private raw payload windows;
- per-row frozen-AC/oracle/direct-native/published-AD comparison;
- exact width/value distributions;
- exact UniqueId system/layout evidence;
- negative-control results;
- another-control consumption counter;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA-256 hashes for every evidence payload file.

## 7. Required validation

- deterministic double-run equality of the frozen selection/comparison;
- permanent R3.18AD focused tests PASS on the evidence head;
- permanent R3.18AA, relevant K2 and scalar tests PASS;
- full `mimir-replay` PASS;
- workspace format/check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18AE may not change production Rust, Cargo files, fixtures, corpus, dependencies or support lanes. It may not inspect another property-control bit, create a repeatable/generalized property loop or public cursor, admit alternate UniqueId layouts, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen rows match the published R3.18AD API exactly through one ordinal-3 payload end, mismatch is zero, the exact AC width/layout facts reconstruct, witness reselection is zero, another-control consumption is zero, privacy passes and production mutation is zero. Admit R3.18AE evidence. Only a later separate pass may inspect the next property-control boundary.

### Outcome B

A reproducible published-AD/frozen-AC/oracle mismatch appears inside an already-admitted R3.18AD shape. Record exact privacy-safe coordinates and keep later-control widening closed.

### Outcome C

Authority drift, witness reselection, privacy failure, another-control access, alternate-layout widening, source mutation or validation contradiction. Stop without admission.
