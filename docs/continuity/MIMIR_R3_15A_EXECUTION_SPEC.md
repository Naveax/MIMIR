# MIMIR — R3.15A Exact Execution Spec

**Pass:** `R3.15A — NewActor branch read-only differential evidence`
**Pass type:** evidence-only / pinned-oracle instrumentation
**Production base:** `7b17cb9033b6c71d476e500380d78402cbb3c56d`
**Production Rust changes:** forbidden

## Goal

Characterize the wire contract immediately after an actor whose `new` bit is true, using the exact pinned Boxcars implementation and the current 47-replay supported corpus. This pass is evidence only. It must not add native NewActor parsing.

## Required source authorities

```text
Boxcars SHA = c70e77df7af81b436cb545d070bb90c82f562d0b
MIMIR production SHA = 7b17cb9033b6c71d476e500380d78402cbb3c56d
```

Pinned Boxcars `parse_new_actor` establishes the sequence:

```text
version-gated name_id: i32 when enabled
unnamed one-bit field
object_id: i32
spawn trajectory selected by object-index spawn plan
trajectory payload according to None / Location / LocationAndRotation
```

The Boxcars name gate to instrument exactly is:

```text
version >= (868,20,0)
OR
(version >= (868,14,0) AND !is_lan)
```

The current MIMIR static lookup plan already admits the same spawn-kind domain:

```text
None
Location
LocationAndRotation
```

R3.15A may compare that static plan with the oracle-selected spawn kind, but it may not consume these fields in production Rust.

## Input identity gate

Use the same exact 47 replay identities admitted by R3.14E. Before oracle instrumentation require:

```text
input_count = 47
unique_sha256 = 47
all replay files exist
all byte lengths match
all SHA-256 values match
BuildVersion identity preserved
```

Any identity mismatch is Outcome C until repaired.

## Evidence selection policy

Decode the supported replays with pinned Boxcars and inspect every encountered `new == true` actor for aggregate counts. Preserve a deterministic exact witness set containing at least:

1. the first NewActor occurrence in every replay;
2. the first occurrence of every observed `(build/version family, is_lan, name_id gate, spawn kind)` family;
3. the first occurrence of every distinct spawn kind;
4. object-id minimum and maximum witnesses;
5. location/rotation payload-length minimum and maximum witnesses for every observed spawn kind that carries payload.

If the full row set is reasonably bounded, preserve all NewActor rows as JSONL. Otherwise preserve aggregate counts plus the deterministic witness set and a digest over the full instrumentation stream.

## Fields to record for every retained witness

### Context

```text
replay path / SHA-256
BuildVersion
network_start / network_size
frame index
actor ordinal within frame
actor_id
new_bit_end
branch_start_bit
version triplet
net_version
is_lan
```

### Name gate

```text
do_parse_name
name_id_present
name_id_value
name_id_start_bit
name_id_end_bit
```

When the gate is false, no name bits may be consumed.

### Opaque one-bit field

```text
opaque_bit_value
opaque_bit_start
opaque_bit_end
```

Do not assign semantics to this bit in R3.15A.

### Object identity

```text
object_id_value
object_id_start_bit
object_id_end_bit
object_table_length
object_id_in_range
object_name when in range
```

Boxcars reads `object_id` as raw signed `i32`; do not silently replace this with a bounded-integer hypothesis.

### Spawn selection

```text
oracle_spawn_kind
mimir_static_spawn_kind
spawn_kind_match
trajectory_start_bit
trajectory_end_bit
```

### Location payload when present

Record the exact decoded integer vector and bit range:

```text
location_start_bit
location_end_bit
location_x_i32
location_y_i32
location_z_i32
```

Pinned Boxcars `Vector3i::decode` uses a variable component width derived from the encoded size prefix and `net_version`; R3.15A records observed bit consumption rather than inventing a fixed-width contract.

### Rotation payload when present

Record:

```text
rotation_start_bit
rotation_end_bit
yaw_present / yaw_i8
pitch_present / pitch_i8
roll_present / roll_i8
```

Pinned Boxcars rotation encoding uses a presence bit per component followed by an `i8` only when present. Preserve raw bit ranges so R3.15B can admit the exact contract.

### Branch endpoint

```text
branch_end_bit
branch_bit_length
```

## Aggregate distributions

At minimum compute:

```text
replays_total
oracle_decode_success
new_actor_total
name_gate_true / false
name_id_present count
spawn_none count
spawn_location count
spawn_location_rotation count
object_id_min / max
invalid_object_id count
mimir_spawn_kind_match / mismatch
location_payload_bit_length min / max
rotation_payload_bit_length min / max
instrumentation_error_count
```

Do not invent expected counts before observing the pinned corpus.

## Hard stop

R3.15A must stop at the end of the NewActor spawn trajectory. It must not instrument or admit as part of this pass:

```text
property_present loop for later existing-actor updates
stream_id
attribute payload semantics
second-frame production iteration
actor lifecycle mutation policy
raw-state mapping
events
skills
```

Oracle decoding may naturally continue so Boxcars can reach later NewActor occurrences, but the retained R3.15A row for each occurrence ends at that NewActor branch endpoint.

## Outcome model

### Outcome A — evidence sufficient

All 47 replay identities are verified; pinned oracle decoding succeeds on the supported lane; the name gate, opaque bit, object-id read, spawn dispatch, payload values/bit ranges, and static-spawn comparison have no unexplained divergence. Then create `R3.15B — NewActor contract admission`.

### Outcome B — bounded format family or mismatch

Preserve the failing replay/witness identities and the first divergent field/bit. Split the smallest additional evidence pass required. Do not change production Rust.

### Outcome C — identity/provenance invalid

No NewActor contract claim is admitted until the oracle/corpus identity gap is repaired.

## Completion artifact

Record at least:

```text
production SHA
oracle SHA
47-replay identity source
instrumentation head / tool SHA
artifact SHA-256
aggregate distributions
deterministic witness-set identity
mismatch/error list
outcome
next exact pass
```

Continuity and `MIMIR_KNOWLEDGE_GRAPH.md` update only after R3.15A is actually admitted.
