# MIMIR — R3.15C Exact Execution Spec

**Pass:** `R3.15C — first NewActor native reader through spawn trajectory`
**Pass kind:** narrow production implementation
**Production base:** `7b17cb9033b6c71d476e500380d78402cbb3c56d`
**Contract authority:** `R3.15B — ADMITTED / CONTRACT COMPLETE`

## Goal

Add one native, additive reader that extends the already-admitted first actor envelope only when that first actor has `new == true`, then decodes exactly the NewActor name/object/spawn trajectory contract admitted by R3.15B and stops at the trajectory endpoint.

This pass does not open an actor loop, property loop, second frame, state mutation, events or skills.

## Required production source scope

Default allowed production file:

```text
crates/mimir-replay/src/lib.rs
```

Fresh source truth may justify a smaller refactor elsewhere only if strictly required and separately explained. The following remain forbidden:

```text
Cargo.toml
Cargo.lock
new external dependency
support-lane widening
fixture mutation
property/attribute decoder expansion
raw-state/event/skill changes
```

## Required additive result surface

Use local naming conventions, but expose an independently testable additive result equivalent to:

```text
ReplayNetworkVector3iV1 { x: i32, y: i32, z: i32 }
ReplayNetworkRotationV1 { yaw: Option<i8>, pitch: Option<i8>, roll: Option<i8> }
ReplayNetworkNewActorV1 {
    name_id: i32,
    opaque_post_name_bit: bool,
    object_id: i32,
    spawn_kind: ReplayNetworkSpawnTrajectoryV1,
    location: Option<ReplayNetworkVector3iV1>,
    rotation: Option<ReplayNetworkRotationV1>,
    stop_bit: u64,
}
ReplayNetworkFirstNewActorEnvelopeV1 {
    envelope: ReplayNetworkFirstActorEnvelopeV1,
    new_actor: Option<ReplayNetworkNewActorV1>,
}
```

Existing `ReplayNetworkFirstActorEnvelopeV1` and its reader contract must remain unchanged.

## Branch behavior

Starting from the already-admitted first actor result:

```text
actor_present != true  -> new_actor = None; no extra network bits consumed
alive != true          -> new_actor = None; no extra network bits consumed
is_new != true         -> new_actor = None; no extra network bits consumed
is_new == true         -> decode exactly one NewActor branch below
```

## Name ID

For the currently admitted `868 / 32 / 10` lane, consume exactly one signed i32 after `new == true`.

```text
width = 32 bits
ordering = LSB-first network cursor
alignment = none
```

Do not add LAN parsing or widen the version lane in this pass.

## Opaque post-name bit

Consume exactly one bit and preserve it without semantic interpretation.

## Object ID

Consume exactly one signed i32 through the network bit cursor.

Before lookup:

```text
object_id >= 0
object_id as usize < spawn_trajectories.len()
```

Negative and out-of-range values must return explicit replay-controlled-input errors. No panic, wraparound or unchecked cast/indexing.

## Vector3i

For current `net_version = 10`:

```text
size_bits = canonical bounded-u32(max_exclusive=22, low_width=4)
bias = 1 << (size_bits + 1)
component_width = size_bits + 2
x_raw = read_bits_le(component_width)
y_raw = read_bits_le(component_width)
z_raw = read_bits_le(component_width)
x = x_raw - bias
y = y_raw - bias
z = z_raw - bias
```

Use wide checked intermediates. The whole vector operation must be cursor-atomic on failure: decode against a cloned/checkpoint cursor and commit only after all required bits and checked conversions succeed.

## Rotation

Decode components in exact order:

```text
yaw
pitch
roll
```

For each:

```text
presence bit
if false -> None
if true  -> read exactly 8 bits and interpret as signed i8
```

The whole rotation operation must be cursor-atomic on failure.

## Spawn dispatch

Use only the already-admitted `ReplayNetworkLookupPlanV1.spawn_trajectories` entry for the decoded object ID.

```text
None:
  location = None
  rotation = None
  consume 0 trajectory bits

Location:
  location = Some(Vector3i)
  rotation = None

LocationAndRotation:
  location = Some(Vector3i)
  rotation = Some(Rotation)
```

Do not call or vendor Boxcars in production.

## Hard stop

The new reader stops exactly at the end of the first NewActor spawn trajectory and exposes that endpoint as `stop_bit` or an equivalent exact field.

The next network bit must remain unread.

Still closed:

```text
property_present
stream_id
attribute payload
next actor
next frame
actor lifecycle mutation
raw state
events
skills
```

## Required focused tests

At minimum prove:

1. additive reader preserves every R3.14D first-envelope field.
2. actor-absent branch consumes no NewActor bits.
3. dead actor branch consumes no NewActor bits.
4. non-new actor branch consumes no NewActor bits.
5. signed 32-bit name ID at a non-byte-aligned bit position.
6. opaque post-name bit has exact one-bit width/value.
7. signed 32-bit object ID at a non-byte-aligned bit position.
8. negative object ID returns error without panic.
9. object ID equal/above spawn-plan length returns error without panic.
10. spawn `None` consumes zero trajectory bits.
11. Vector3i bounded prefix discriminator-0 path.
12. Vector3i bounded prefix discriminator-1 path.
13. multiple variable Vector3i component widths and signed bias reconstruction.
14. Vector3i truncation leaves caller cursor unchanged.
15. Rotation all absent consumes exactly 3 bits.
16. Rotation all present consumes exactly 27 bits and preserves signed i8 values.
17. mixed Rotation presence ordering.
18. Rotation truncation leaves caller cursor unchanged.
19. `Location` hard stop equals vector endpoint.
20. `LocationAndRotation` hard stop equals rotation endpoint.
21. File input remains unsupported.
22. existing `mimir-replay` tests remain green.
23. Cargo manifests/lock remain unchanged.
24. no property/next-actor/next-frame capability is introduced.
25. the existing three checked-in replay fixtures still parse through the new endpoint when they remain in the admitted lane.

## Validation sequence

Before admission of R3.15C:

```text
focused mimir-replay tests PASS
full repository verifier PASS
knowledge archive verifier PASS
source scope audit PASS
Cargo drift = 0
production branch CI PASS
published-main exact-SHA readback PASS
```

Implementation success alone is not the full-corpus oracle admission. After R3.15C production publication, the next evidence pass should be `R3.15D — 47-replay native-vs-pinned-Boxcars NewActor differential audit` before any property loop is opened.
