# MIMIR — R3.15D Decision

**Date:** 2026-08-13  
**Pass:** `R3.15D — 47-replay first-NewActor native-vs-pinned-Boxcars differential audit`  
**Outcome:** **A — ADMITTED / COMPLETE**

## Exact identities

```text
pre-pass main SHA          = c59453812b8399aca8056b77c3ae4f45da33e44a
production SHA             = bf4bccff82203ed049d33e942681fed07f23beb4
production source blob     = f64a5e0d66962f41026b2eb10e176219d4529931
evidence head              = 10e5d05383dbc09e19af997e896a825d8d16e3ae
exact differential run/job = 31736738234 / 94570077736
normal repository CI run   = 31736738075
evidence artifact ID       = 9195419601
evidence artifact digest   = sha256:f6e11055c11ed0724c45fcc76c13a9da2dbbb285ab3744f9738f0d4a19ecab8a
```

## Oracle provenance

```text
R3.15A artifact ID          = 9184200143
R3.15A artifact digest      = sha256:a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d
R3.15A full stream rows     = 169538
R3.15A full stream SHA-256  = ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba
R3.15D selected rows        = 47
R3.15D selected lane SHA256 = a5acaea07b636aac3cfab5de9fcdfd9669a0233242084c2bd6adc793d269b5cc
```

The exact R3.15A artifact digest was revalidated through the GitHub Actions artifact API before use. Its 169,538-row NewActor JSONL was rehashed and row-count checked. Exactly one `frame_index == 0 && actor_ordinal == 0` row was selected for each of the exact 47 admitted replay paths, and every replay byte stream was SHA-256 checked against its oracle identity.

**Scope clarification:** the 169,538-row parent stream is provenance evidence. R3.15D native-differentially compared exactly 47 selected first-NewActor rows.

## Differential result

```text
replays_total        = 47
oracle_rows_selected = 47
native_success       = 47
identity_error_count = 0
native_error_count   = 0
mismatch_count       = 0
```

All 21 admitted comparison gates matched **47/47**:

```text
actor_present
actor_id
alive
is_new
envelope_stop
name_id
opaque
object_id
spawn_kind
location_presence
location_x
location_y
location_z
rotation_presence
yaw_presence
yaw
pitch_presence
pitch
roll_presence
roll
trajectory_stop
```

The evidence run also re-audited the source boundary after the differential: production mutation count `0`, Cargo mutation count `0`, fixture/corpus mutation count `0`.

## Pre-canonical attempts

Runs `31719341428` and `31735271685` are **not parser mismatch evidence**. The first stopped at rustfmt before the differential; the second used a malformed copied TSV harness and stopped on its own field-count assertion. Neither changed production. They are superseded by exact run `31736738234`, which derives the 47 oracle rows directly from the verified R3.15A artifact at runtime.

## Decision

R3.15C first-NewActor parsing is admitted across the exact current 47-replay first-NewActor surface. R3.15D is closed with Outcome A. This does not admit property decoding, lifecycle state, raw state, events, slicing, skills, or runtime widening.

## Next pass

`R3.16A — existing-actor first-property envelope evidence`, evidence-only. The roadmap-defined hard stop is `payload_start_bit`, before attribute payload consumption.
