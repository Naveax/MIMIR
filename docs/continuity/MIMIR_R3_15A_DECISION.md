# MIMIR — R3.15A NewActor Evidence Decision

**Date:** 2026-08-13
**Pass:** `R3.15A — NewActor branch read-only differential evidence`
**Outcome:** **ADMITTED / OUTCOME A**
**Production Rust changed:** **NO**

## Frozen identities

```text
production SHA              = 7b17cb9033b6c71d476e500380d78402cbb3c56d
continuity base / main      = a51c0c1bf8c8927f4e2f39691ec63403d70bb0a8
pinned Boxcars SHA          = c70e77df7af81b436cb545d070bb90c82f562d0b
R3.14A oracle run           = 31690714121
R3.14A oracle artifact ID   = 9177314099
R3.14A artifact SHA-256     = d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b
```

The exact 47 replay identities from R3.14A/R3.14E were reused. Every replay byte length and SHA-256 remained exact.

## R3.15A evidence identity

```text
evidence head               = 1e27674625fdff26e05436e882014db5c7c5116d
workflow run                = 31708322309
workflow job/check          = 94474438951 SUCCESS
artifact ID                 = 9184200143
artifact ZIP SHA-256        = a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d
instrumentation patch SHA   = 79010fb8923b365db0764bc56d2cadc48a6d257f2936fbd928fc24c08dc090e8
evidence driver SHA-256     = 44ddbd3f22f60b2959b889b46c68b57d9ef0bc8285ca97ba501ed1fd355e66ba
full NewActor stream SHA    = ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba
witness count               = 59
witness SHA-256             = e7dc38f64cee7b458517211e601cdc0133a6a5a799c1f718ab51d330b0e16573
```

The downloaded artifact byte digest independently matched GitHub's artifact digest.

## Exact aggregate result

```text
replays_total                       = 47
replays_with_new_actor              = 47
oracle_decode_success               = 47
new_actor_total                     = 169538
name_gate_true                      = 169538
name_gate_false                     = 0
name_id_present                     = 169538
spawn_none                          = 93136
spawn_location                      = 66948
spawn_location_rotation             = 9454
object_id_min                       = 23
object_id_max                       = 432
invalid_object_id                   = 0
mimir_static_spawn_kind_match       = 169538
mimir_static_spawn_kind_mismatch    = 0
location_payload_bit_length_min     = 11
location_payload_bit_length_max     = 46
rotation_payload_bit_length_min     = 3
rotation_payload_bit_length_max     = 27
instrumentation_error_count         = 0
production_source_mutation          = 0
```

All 169,538 retained rows were independently rechecked after artifact download for exact name/object widths, opaque-bit width, branch start/end alignment and spawn-kind equality; zero invariant violations were found.

## Admitted wire facts for the current supported lane

Pinned Boxcars and the evidence agree on this NewActor sequence after `new == true`:

```text
name_id            raw i32 / 32 bits on the current supported lane
opaque post-name   exactly 1 bit; semantics intentionally unknown
object_id          raw signed i32 / 32 bits
spawn kind         resolved from the admitted object-index static spawn plan
trajectory         None | Location | LocationAndRotation
hard stop          end of the spawn trajectory
```

The current MIMIR supported header tuple is `868 / 32 / 10`. Therefore the pinned Boxcars name gate is true for every currently admitted MIMIR input regardless of LAN status. The 47-replay evidence itself also observed only the gate-true family. R3.15A does **not** claim empirical coverage of the gate-false branch outside the current supported tuple.

Observed trajectory payloads confirm all three static spawn families. Location payloads are variable-width `Vector3i`; rotation payloads use one presence bit plus an optional signed byte per yaw/pitch/roll component.

## Still closed in production

R3.15A is evidence-only. Production remains stopped immediately after the first actor `new` bit. Still closed:

```text
name_id consumption in native production
opaque post-name bit
object_id
spawn trajectory values
property-present loop
stream_id / attributes
second actor / second frame iteration
actor lifecycle mutation
raw state / events / skills
```

## Next exact pass

`R3.15B — NewActor native contract admission`.
