# MIMIR — R3.14E Differential Admission Decision

**Date:** 2026-08-13
**Pass:** `R3.14E — native first-envelope differential audit`
**Outcome:** **ADMITTED / OUTCOME A**
**Production Rust changed:** **NO**

## Frozen production identity

```text
production SHA      = 7b17cb9033b6c71d476e500380d78402cbb3c56d
continuity base     = b06a967b31e971431caa415721661088c630fdbc
production reader   = MinimalReplayNetworkFirstActorEnvelopeReader
hard stop           = after new / bit 78 on the supported lane
```

## Immutable oracle identity

```text
oracle repo                 = nickbabcock/boxcars
oracle SHA                  = c70e77df7af81b436cb545d070bb90c82f562d0b
R3.14A evidence head        = f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
R3.14A workflow run         = 31690714121
R3.14A artifact ID          = 9177314099
R3.14A artifact SHA-256     = d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b
selector manifest SHA-256   = 28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55
oracle rows                 = 47
```

The preserved R3.14A artifact was recovered by exact run/artifact identity. Its GitHub digest and independently downloaded ZIP byte digest both matched the canonical SHA-256 above.

## R3.14E evidence identity

```text
evidence branch head        = 96b5a2ee298bfa4dc88d320b13459646931b82a6
workflow run                = 31705946564
workflow job/check          = 94466421975 SUCCESS
artifact ID                 = 9183181430
artifact SHA-256            = 8cdbf0d3d9e96ff4f508e3da8fa913f53c76bb27061805f2059ddf72d4d06bed
preparer SHA-256            = a57b45fd727b1d9a38fb551c260aa6ba75896ccfcd1707eba2be41c73acdb559
native probe SHA-256        = 01398ac47faf9dd4a279f7d127de0c978693f9687459540e08f16f4178a4589c
```

The R3.14E artifact ZIP byte digest independently matched the GitHub artifact digest.

## Exact aggregate result

```text
replays_total               = 47
replays_unique_sha          = 47
native_parse_success        = 47
oracle_rows                 = 47
time_raw_match              = 47
delta_raw_match             = 47
actor_present_match         = 47
actor_id_match              = 47
alive_match                 = 47
new_match                   = 47
stop_bit_match              = 47
structural_context_match    = 47
build_version_match         = 47
mismatch_count              = 0
native_error_count          = 0
identity_error_count        = 0
production_source_mutation  = 0
```

The temporary native probe executed one integration test over the exact 47 replay identities and reported `R3_14E_NATIVE_PARSE_SUCCESS=47` and `R3_14E_EXACT_MATCH=47`.

## Admission decision

R3.14D is now differentially admitted across the current 47-replay supported lane through the first actor `new` bit. No production capability beyond that bit is implied.

Still closed:

```text
name_id
unnamed post-new bit
object_id
spawn location / rotation payload
property loop
stream_id / attribute payload
second actor / second frame production iteration
actor lifecycle state mutation
raw state / events / skills
```

## Next exact pass

`R3.15A — NewActor branch read-only differential evidence`.
