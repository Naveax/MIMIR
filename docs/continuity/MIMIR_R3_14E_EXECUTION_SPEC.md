# MIMIR — R3.14E Exact Execution Spec

**Pass:** `R3.14E — native first-envelope differential audit`
**Pass type:** evidence-only differential audit
**Production base:** `7b17cb9033b6c71d476e500380d78402cbb3c56d`
**Production Rust changes:** forbidden

## Goal

Prove the R3.14D native reader against the already-pinned Boxcars first-envelope oracle over exactly the 47 currently supported replays.

## Oracle identity

Reuse and independently verify the immutable R3.14A oracle evidence:

```text
Boxcars SHA                 = c70e77df7af81b436cb545d070bb90c82f562d0b
R3.14A evidence head        = f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
selector manifest SHA-256   = 28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55
R3.14A artifact SHA-256     = d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b
oracle rows                 = 47
```

Do not substitute latest Boxcars. Do not edit oracle rows to make native output match.

A fresh Boxcars instrumentation run is optional if the preserved exact oracle evidence passes identity/readback. The preserved evidence is sufficient because R3.14E compares exactly the fields already observed by R3.14A.

## Exact 47-input identity

The audit must use the 47 replay identities carried by `r3_14a_first_actor_envelope.jsonl`, including:

- relative replay path;
- byte length;
- replay SHA-256;
- BuildVersion;
- network_start / network_size;
- max_channels / channel_bits.

Before native parsing:

```text
input_count = 47
unique_sha256 = 47
all replay files exist
all byte lengths match
all SHA-256 values match
```

Any identity mismatch fails the pass.

## Native fields to compare

For every replay require exact equality for:

```text
first_frame_time_raw_u32
first_frame_delta_raw_u32
actor_present
actor_id
alive
new
stop_bit
```

Also cross-check the native reader's admitted structural context against the oracle row when available:

```text
network_start
network_size
max_channels
channel_bits
```

The float comparison is raw-u32 equality, not decimal-string equality.

## Expected aggregate gates

```text
replays_total = 47
replays_unique_sha = 47
native_parse_success = 47
oracle_rows = 47
time_raw_match = 47
delta_raw_match = 47
actor_present_match = 47
actor_id_match = 47
alive_match = 47
new_match = 47
stop_bit_match = 47
structural_context_match = 47
mismatch_count = 0
native_error_count = 0
identity_error_count = 0
```

Do not invent branch-distribution expectations beyond what the preserved oracle evidence actually contains.

## Evidence implementation policy

Temporary evidence tooling may be added on a disposable branch, for example:

- a small `mimir-replay` probe binary that calls `MinimalReplayNetworkFirstActorEnvelopeReader`;
- a Python/PowerShell orchestrator that verifies replay identity and compares native output to the preserved R3.14A JSONL;
- a temporary GitHub Actions workflow.

Temporary tooling must not enter the clean production commit.

No production Rust behavior changes are allowed in R3.14E.

## Hard stop

The native audit must not consume or compare:

```text
name_id
post-name one-bit field
object_id
spawn trajectory
property_present
stream_id
attribute payload
second actor
second frame
actor lifecycle state
raw state
events
skills
```

The current 47-row oracle evidence stops at bit 78.

## Outcome model

### Outcome A — exact match

All aggregate gates above pass with zero mismatch/error.

Then R3.14D is differentially admitted across the current supported lane and the next exact pass is:

`R3.15A — NewActor branch read-only differential evidence`.

### Outcome B — bounded mismatch/gap

At least one replay differs, but the divergence is localized and reproducible.

Then:

- preserve failing replay identities;
- classify first divergent field/bit;
- do not widen production;
- create the smallest evidence/fix pass required;
- rerun affected/all 47 as appropriate.

### Outcome C — invalid evidence/identity

Oracle identity, replay identity, or evidence provenance cannot be proven.

Then no native differential claim is admitted until the identity gap is repaired.

## Completion artifact

The final decision must record at least:

```text
production SHA
oracle SHA
oracle artifact identity
47-replay manifest identity
native probe/tool identity
aggregate exact-match counts
mismatch list, if any
outcome
next exact pass
```

Continuity and `MIMIR_KNOWLEDGE_GRAPH.md` update only after this pass is actually admitted.
