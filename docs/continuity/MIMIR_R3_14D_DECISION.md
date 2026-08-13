# MIMIR — R3.14D Production Admission Decision

**Date:** 2026-08-13
**Pass:** `R3.14D — first actor envelope header native reader`
**Outcome:** **ADMITTED / PRODUCTION**

## Production identity

```text
pre-pass main SHA   = 9c0f81a084b2df0e64496af87c0edc50814bcbc6
production SHA      = 7b17cb9033b6c71d476e500380d78402cbb3c56d
production tree     = 9252b8f48fb89beda9f4ea63e1367365a1434a20
source file         = crates/mimir-replay/src/lib.rs
source Git blob     = 67752868807c0b7169e46f22762c7a0ea9efce40
source SHA-256      = 06b767622108ca1aea82ee5c0aad6cc503fbcfddaba05012cf022dd901a5a385
```

The clean production commit changes exactly one file: `crates/mimir-replay/src/lib.rs`.

## Capability admitted

Production now contains:

- `ReplayNetworkFirstActorEnvelopeV1`;
- `ReplayNetworkFirstActorEnvelopeReader`;
- `MinimalReplayNetworkFirstActorEnvelopeReader`;
- a private decoder that consumes first-frame time/delta through the R3.14C cursor;
- raw timing-bit equality checks against `ReplayNetworkTimingPreambleV1`;
- one first `actor_present` branch;
- canonical bounded actor-ID decode;
- `alive` branch;
- `new` branch;
- hard stop immediately after the branch endpoint.

Branch state is preserved with `Option`: fields not consumed by the wire branch remain `None`.

R3.14D does not set the cursor to bit 64 as a shortcut. It reads the two 32-bit timing fields through the native LSB-first cursor and checks their raw bits against the already-admitted timing preamble.

## Validation evidence

```text
workflow run        = 31701754758
validation head     = 77a5f0f24ee309d6216f7f7bb4bbeb1bfbc6b4ca
validated bot SHA   = 7555acf7f47cbda639a91c649c807797d0eaa57a
artifact ID         = 9181561121
artifact SHA-256    = dab3a48ef1b58cbbbd39c832009fc722d047c21f84c12cb4e8f7cc69313a935d
focused tests       = 17 PASS
verify_repo_locked  = PASS
knowledge verifier  = PASS
hard-stop scope     = PASS
Cargo drift         = 0
```

Focused tests cover timing raw-bit consumption/mismatch, actor-absent, alive-false, new-false/new-true, discriminator 0/1, threshold/no-discriminator, actor-ID truncation, missing discriminator, missing alive/new, File unsupported, terminal-first-frame rejection, and all three historical admitted fixtures through the `new` boundary.

## Clean reconstruction / publication

```text
clean commit        = 7b17cb9033b6c71d476e500380d78402cbb3c56d
clean branch CI     = 31702049792 SUCCESS
published-main CI   = 31702341993 SUCCESS
publication         = force-free
published readback  = exact 7b17cb9033b6c71d476e500380d78402cbb3c56d
```

## Boundaries still closed

```text
name_id
post-name one-bit field
object_id
spawn trajectory payload
property loop
stream_id / attribute payload
second actor / second frame
actor lifecycle state mutation
raw state / events / skills
```

R3.14D implementation success is not the 47-replay oracle admission. That is the next exact pass.

## Next exact pass

`R3.14E — native first-envelope differential audit`.
