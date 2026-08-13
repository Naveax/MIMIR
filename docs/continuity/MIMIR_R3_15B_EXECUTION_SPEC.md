# MIMIR — R3.15B Execution Spec

**Pass:** `R3.15B — NewActor native contract admission`
**Pass kind:** planning / contract / docs-only
**Production Rust changes in this pass:** **FORBIDDEN**
**Prerequisite:** `R3.15A Outcome A`
**Next implementation pass if admitted:** `R3.15C — first NewActor native reader through spawn trajectory`

## 1. Purpose

R3.15A produced exact read-only evidence for 169,538 NewActor branches across the exact 47-replay supported lane. R3.15B converts only those admitted observations plus exact pinned-source behavior into a narrow native implementation contract.

R3.15B does not consume additional production network bits and does not add replay capability.

## 2. Authorities

```text
production SHA        = 7b17cb9033b6c71d476e500380d78402cbb3c56d
R3.15A evidence head  = 1e27674625fdff26e05436e882014db5c7c5116d
R3.15A run            = 31708322309
R3.15A artifact ID    = 9184200143
R3.15A artifact SHA   = a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d
Boxcars SHA           = c70e77df7af81b436cb545d070bb90c82f562d0b
full stream SHA       = ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba
```

## 3. Current production integration point

Current production has:

```text
ReplayNetworkFirstActorEnvelopeV1
MinimalReplayNetworkFirstActorEnvelopeReader
private NetworkBitCursor
ReplayNetworkLookupPlanV1
ReplayNetworkSpawnTrajectoryV1
```

The current first-actor reader stops after the `new` bit. R3.15C must preserve that reader's behavior and add a separate narrow extension rather than silently changing the admitted R3.14D result contract.

Recommended additive shape:

```text
ReplayNetworkVector3iV1
ReplayNetworkRotationV1
ReplayNetworkNewActorV1
ReplayNetworkFirstNewActorEnvelopeV1
ReplayNetworkFirstNewActorEnvelopeReader
MinimalReplayNetworkFirstNewActorEnvelopeReader
```

Exact names may follow local naming conventions, but the capability must remain additive and independently testable.

## 4. Branch behavior

R3.15C begins from the already-admitted first actor envelope.

```text
actor_present != true  -> new_actor = None; consume no further bits
alive != true          -> new_actor = None; consume no further bits
is_new != true         -> new_actor = None; consume no further bits
is_new == true         -> decode exactly one NewActor branch below
```

No actor loop is opened.

## 5. Name ID contract

Pinned Boxcars gate:

```text
version >= (868,20,0)
OR
(version >= (868,14,0) AND !is_lan)
```

Current MIMIR production already rejects header tuples outside:

```text
major_version = 868
minor_version = 32
net_version   = 10
```

Therefore `do_parse_name` is always true for every currently admitted MIMIR input, even if LAN status were true. R3.15C may therefore consume one raw signed little-endian `i32` name ID after `new == true` without adding a LAN detector or a broader version gate.

This is intentionally scoped to the current supported tuple. If MIMIR later widens version support below 868.20, the name gate must be reopened as its own compatibility pass.

Required semantics:

```text
name_id width   = 32 bits
signed type     = i32
byte alignment  = none; read through the LSB-first bit cursor
```

## 6. Opaque post-name bit

Immediately after `name_id`, consume exactly one bit.

The field may be preserved as a neutral boolean such as `post_name_bit` / `opaque_post_name_bit`.

Forbidden in R3.15C:

```text
assigning gameplay meaning
renaming it to a semantic property unsupported by evidence
branching into new behavior based on guessed semantics
```

## 7. Object ID contract

Consume exactly one raw signed `i32` through the network bit cursor.

```text
object_id width = 32 bits
object_id type  = i32
```

This is not a bounded integer.

Before static lookup:

```text
object_id >= 0
object_id as usize < ReplayNetworkLookupPlanV1.spawn_trajectories.len()
```

Out-of-range or negative IDs must return an explicit replay-controlled-input error. No panic and no unchecked signed-to-usize indexing.

## 8. Spawn-kind dispatch

Use only the already-admitted static lookup plan:

```text
ReplayNetworkSpawnTrajectoryV1::None
ReplayNetworkSpawnTrajectoryV1::Location
ReplayNetworkSpawnTrajectoryV1::LocationAndRotation
```

R3.15A exact comparison:

```text
169538 / 169538 static spawn-kind matches
0 mismatches
```

Do not vendor or call Boxcars in production.

## 9. Vector3i contract

Current supported `net_version = 10`, so the pinned source uses:

```text
size_bits = bounded integer(max_exclusive=22, low_width=4)
bias      = 1 << (size_bits + 1)
component_width = size_bits + 2
x_raw = read_bits_le(component_width)
y_raw = read_bits_le(component_width)
z_raw = read_bits_le(component_width)
x = x_raw - bias
y = y_raw - bias
z = z_raw - bias
```

Use sufficiently wide intermediates before the final checked signed conversion.

R3.15A observed location payload lengths from 11 through 46 bits, so a fixed-width vector decoder is forbidden.

The complete vector decode must be cursor-atomic on truncation. Use a cloned/checkpoint cursor and commit only after all prefix/component reads succeed.

## 10. Rotation contract

For each component in exact order:

```text
yaw
pitch
roll
```

consume:

```text
presence: 1 bit
if presence == 1: signed i8 payload, 8 bits
if presence == 0: no payload bits
```

The complete rotation consumes between 3 and 27 bits; R3.15A observed both endpoints.

Rotation decoding must also be cursor-atomic on truncation.

## 11. Trajectory contract

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

The R3.15C public result should preserve the selected spawn kind together with the decoded values so differential tests can prove dispatch and payload equality separately.

## 12. R3.15C source scope

Unless fresh source truth proves otherwise, production changes are restricted to:

```text
crates/mimir-replay/src/lib.rs
```

Allowed:

- additive NewActor result/reader types;
- private raw signed bit-read helper if required;
- private atomic Vector3i / Rotation helpers;
- minimal refactor to share the already-admitted first-envelope parse without changing its output;
- focused tests.

Forbidden:

```text
Cargo.toml / Cargo.lock changes
external parser dependency
property_present consumption
stream/property ID decode
attribute payload decode
second actor / second frame iteration
actor state table
raw-state / event / skill changes
support-lane widening
```

## 13. Required R3.15C tests

At minimum:

1. additive reader preserves exact R3.14D envelope fields.
2. non-present / dead / non-new branches consume no NewActor bits.
3. raw signed 32-bit name ID across non-byte-aligned cursor.
4. opaque post-name bit exact width/value.
5. raw signed 32-bit object ID across non-byte-aligned cursor.
6. negative object ID rejected without panic.
7. object ID >= spawn-plan length rejected without panic.
8. spawn `None` consumes zero trajectory bits.
9. Vector3i bounded size-prefix discriminator-0 path.
10. Vector3i bounded size-prefix discriminator-1 path.
11. Vector3i variable component widths and signed bias reconstruction.
12. Vector3i truncation is atomic.
13. rotation all components absent -> 3 bits.
14. rotation all components present -> 27 bits with signed i8 values.
15. mixed rotation presence ordering.
16. rotation truncation is atomic.
17. `Location` exact hard stop at vector end.
18. `LocationAndRotation` exact hard stop at rotation end.
19. File input remains unsupported.
20. existing `mimir-replay` tests remain green.
21. no production dependency/Cargo drift.
22. no property-present/second-actor/second-frame capability introduced.

The implementation pass should also run the existing three checked-in historical replay fixtures through the new reader when they remain within the admitted tuple.

## 14. R3.15C hard stop

The cursor stops exactly at the end of the first NewActor spawn trajectory.

It must not consume the next network bit, including any later actor/property control bit.

Still closed:

```text
property_present
stream_id
attribute payload
next actor
next frame
actor lifecycle state mutation
raw state
events
skills
```

## 15. R3.15B admission criteria

R3.15B may be admitted only when:

```text
R3.15A Outcome A decision exists
artifact identities are exact
name-gate/current-version scope is explicit
raw signed name/object widths are explicit
opaque bit remains semantically opaque
Vector3i algorithm is unambiguous
Rotation algorithm is unambiguous
composite failure atomicity is explicit
R3.15C source scope/tests/hard stop are explicit
production Rust unchanged
continuity and knowledge graph synchronized
normal CI passes
knowledge archive verifier passes
```

Until those gates are satisfied, R3.15C remains closed.
