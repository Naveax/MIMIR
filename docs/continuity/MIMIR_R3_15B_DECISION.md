# MIMIR — R3.15B Contract Admission Decision

**Date:** 2026-08-13
**Pass:** `R3.15B — NewActor native contract admission`
**Outcome:** **ADMITTED / CONTRACT COMPLETE**
**Pass kind:** docs-only contract admission
**Production Rust changed:** **NO**

## Frozen authorities

```text
production SHA              = 7b17cb9033b6c71d476e500380d78402cbb3c56d
continuity base / main      = fb2bbdec739b440ebbc2465db09bdcc9faac2ce1
R3.15A evidence head        = 1e27674625fdff26e05436e882014db5c7c5116d
R3.15A workflow run         = 31708322309
R3.15A artifact ID          = 9184200143
R3.15A artifact SHA-256     = a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d
R3.15A full stream SHA-256  = ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba
pinned Boxcars SHA          = c70e77df7af81b436cb545d070bb90c82f562d0b
```

R3.15A admitted 169,538 NewActor rows across all 47 supported replays with 169,538/169,538 static spawn-kind equality, zero invalid object IDs, zero mismatch and zero instrumentation error.

## Contract admitted

For the currently admitted MIMIR support lane, the first `new == true` actor extension is now specified as:

```text
name_id                  raw signed i32, 32 network bits
opaque post-name field   exactly 1 bit, semantics intentionally unknown
object_id                raw signed i32, 32 network bits
spawn dispatch           admitted ReplayNetworkSpawnTrajectoryV1 static plan
trajectory               None | Location | LocationAndRotation
hard stop                end of that first NewActor spawn trajectory
```

Current MIMIR production accepts the exact replay-header tuple `868 / 32 / 10`. The pinned Boxcars name gate is therefore true throughout the current admitted lane. The R3.15A corpus also observed only the gate-true family. This decision does not widen version support and does not claim empirical coverage of a gate-false family.

`object_id` is not a bounded integer. Negative or out-of-range values must fail explicitly before indexing the static spawn plan.

For the current `net_version = 10`, Vector3i uses the canonical bounded size prefix with `max_exclusive = 22` and `low_width = 4`, followed by three variable-width components and signed bias reconstruction. Composite Vector3i decode must be cursor-atomic on truncation.

Rotation consumes yaw, pitch and roll in that order. Each component has one presence bit and, when present, one signed i8 payload. Composite Rotation decode must be cursor-atomic on truncation.

R3.15A observed location payload lengths from 11 through 46 bits and rotation payload lengths from 3 through 27 bits. Fixed-width trajectory decoding is forbidden.

## Integration policy

R3.15C must be additive. Existing R3.14D first-envelope behavior remains independently testable and unchanged. Unless fresh source truth proves otherwise, the only production source file allowed to change is:

```text
crates/mimir-replay/src/lib.rs
```

Forbidden in R3.15C:

```text
Cargo.toml / Cargo.lock changes
external parser dependency
support-lane widening
property_present consumption
stream/property ID decoding
attribute payload decoding
second actor or second frame iteration
actor lifecycle state
raw state / events / skills
```

## Validation basis

The R3.15B execution spec was present on exact commit `fb2bbdec739b440ebbc2465db09bdcc9faac2ce1`. That exact commit passed repository CI (`31710371570`) and Knowledge Archive verification (`31710371562`) before publication, then was read back as `main` after a force-free fast-forward. The publication used `GITHUB_TOKEN`, so GitHub did not create a second recursive `main` push workflow run; no nonexistent run is claimed here.

## Next exact pass

`R3.15C — first NewActor native reader through spawn trajectory`.
