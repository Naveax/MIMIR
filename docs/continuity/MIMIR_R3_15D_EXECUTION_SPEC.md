# MIMIR — R3.15D Execution Spec

Pass: R3.15D — 47-replay first-NewActor native-vs-pinned-Boxcars differential audit.
Kind: evidence-only. Production Rust changes are forbidden.
Production SHA under test: bf4bccff82203ed049d33e942681fed07f23beb4.

## Goal

Compare the additive R3.15C native reader against the exact pinned R3.15A Boxcars evidence for exactly one deterministic NewActor row per admitted replay. R3.15C exposes only the first actor branch, so R3.15D selects the R3.15A oracle row with frame_index=0 and actor_ordinal=0 for each of the 47 admitted replay identities. It must not claim comparison of all 169,538 oracle NewActor rows.

## Frozen authorities

- Native production SHA: bf4bccff82203ed049d33e942681fed07f23beb4
- Native source blob: f64a5e0d66962f41026b2eb10e176219d4529931
- R3.15A evidence head: 1e27674625fdff26e05436e882014db5c7c5116d
- R3.15A workflow run: 31708322309
- R3.15A artifact ID: 9184200143
- R3.15A artifact SHA-256: a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d
- R3.15A full-stream SHA-256: ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba
- Pinned Boxcars SHA: c70e77df7af81b436cb545d070bb90c82f562d0b
- Supported replay count: 47

The runner must verify evidence/artifact identity before using oracle rows.

## Replay and oracle lane

Use r3_15a_paths.txt from the exact artifact. Require 47 unique paths, all present in the checkout, and replay SHA-256 equality with the corresponding oracle records. From r3_15a_new_actor_all.jsonl retain exactly one row per path where frame_index=0 and actor_ordinal=0. Require exactly 47 rows and one row per path.

## Native probe

For each replay, load ReplayInput::Memory and call only MinimalReplayNetworkFirstNewActorEnvelopeReader.read_network_first_new_actor_envelope. Emit relative path, replay SHA-256, envelope stop_bit, name_id, opaque_post_name_bit, object_id, spawn_kind, optional location x/y/z, optional rotation yaw/pitch/roll, and NewActor stop_bit.

No production mutation, secondary parser, actor/frame loop, or property decode is allowed.

## Exact equality gates

For all 47 replays require:

- native envelope.stop_bit == oracle branch_start_bit
- native name_id == oracle name_id_value
- native opaque_post_name_bit == oracle opaque_bit_value
- native object_id == oracle object_id_value
- native spawn_kind == oracle oracle_spawn_kind after lexical normalization only: none=none, location=location, location_rotation=location_and_rotation
- native location presence and x/y/z == oracle location presence and values
- native rotation presence and yaw/pitch/roll presence/value == oracle fields
- native NewActor stop_bit == oracle trajectory_end_bit

No tolerance is permitted because compared values are integer, boolean, enum, or bit-offset fields.

## Outcome A

Requires 47 oracle rows, 47 native successes, 47/47 identity equality, 47/47 equality for first-envelope stop, name ID, opaque bit, object ID, spawn kind, location presence/values, rotation presence/components, and trajectory stop; mismatch_count=0; native_error_count=0; identity_error_count=0; production_source_mutation=0; Cargo/dependency mutation=0.

Outcome B is any native/oracle value or offset mismatch. Stop and repair/re-plan R3.15C before widening. Outcome C is evidence/artifact/identity failure; treat it as evidence infrastructure failure, not a parser defect.

## Hard stop

R3.15D must not change production Rust or admit property_present, stream/property IDs, attribute payloads, another actor/frame, lifecycle mutation, raw state, events, or skills. The pass ends after its exact 47-row decision and continuity/knowledge synchronization.
