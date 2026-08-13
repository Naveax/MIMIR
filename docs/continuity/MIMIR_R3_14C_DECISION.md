# MIMIR — R3.14C Production Admission Decision

**Date:** 2026-08-13  
**Pass:** `R3.14C — native bit cursor + bounded integer primitive implementation`  
**Outcome:** **ADMITTED / PRODUCTION**

## 1. Production identity

```text
pre-pass main SHA  = c42836647673cecc47cc9c89908da1de11d8a222
production SHA     = bad2db9d5043a7a0087a4fab1d278df5f36c7717
production tree    = 88057e47c96d98e6034e8066f320de2ebebef912
source file        = crates/mimir-replay/src/lib.rs
source Git blob    = 3ff6c7823f45126595e7e59f7b5fb50980d8234c
source SHA-256     = ac1c2ae2919ad0c5d6d8ea615dd5dac82f4c5e5240f33618ef5e74ef9cb1cb92
```

The clean production commit changes exactly one file: `crates/mimir-replay/src/lib.rs`.
No Cargo manifest, dependency, fixture, corpus, workflow, or temporary evidence tool entered the production commit.

## 2. Capability admitted

R3.14C opens only the private/internal replay-network primitive layer:

```text
NetworkBitCursor
  new
  position_bits
  remaining_bits
  read_bit
  read_bits_le
  read_bounded_u32
```

Admitted semantics:

- LSB-first bit order within each byte;
- exact bit-position accounting;
- `read_bits_le` width `0..=64`;
- zero-width read is a no-op;
- width above 64 is rejected;
- insufficient reads fail without advancing the cursor;
- bounded integer maximum zero is rejected;
- maximum one / low-width zero yields zero without consuming bits;
- bounded decoding uses low bits plus the value/bound-dependent discriminator bit;
- discriminator truncation rolls the cursor back to the bounded-read start;
- no actor semantics are embedded in the primitive.

The primitive remains private. This pass does **not** add a public actor-envelope result or reader.

## 3. Validation evidence

Successful disposable validation run:

```text
workflow run       = 31698608640
validation head    = 349f20328cef6e7f0a3c46b279a787583442a652
validated bot SHA  = 8ccd629f9e6eba749b234afe0a80b2b4df7eca7d
artifact ID        = 9180345101
artifact SHA-256   = 0f64e842d0ced4c5566717954be2a684f6735080e9eb8edac9c03e2218d295d7
```

Validation receipt:

```text
focused_tests                    = PASS
focused_test_count               = 19
oracle_vector_rows               = 47
oracle_vector_value_match        = 47/47
oracle_vector_end_bit_match      = 47/47
mimir_replay_regression          = PASS
workspace_check                  = PASS
workspace_tests                  = PASS
workspace_clippy                 = PASS
export_inventory                 = PASS
corpus_verifier                  = PASS
knowledge_archive_verifier       = PASS
cargo_locked                     = PASS
hard_stop_scope                  = PASS
production_files_changed         = crates/mimir-replay/src/lib.rs
```

The 47 R3.14A first-actor vectors all decode actor ID `0` from bound `2047`, low width `10`, and finish the bounded integer at 11 consumed bits.
Synthetic tests additionally cover discriminator-one, threshold/no-discriminator, truncation, cross-byte reads, width boundaries, atomic failure, and back-to-back alignment.

## 4. Clean reconstruction and publication

The validated `lib.rs` blob was reconstructed onto fresh published main ancestry rather than publishing the disposable validation branch.

Clean commit:

```text
bad2db9d5043a7a0087a4fab1d278df5f36c7717
```

Clean branch CI:

```text
run 31698938025 = SUCCESS
```

Publication was force-free from fresh main `c42836647673cecc47cc9c89908da1de11d8a222`.
Published-main readback resolved exactly to `bad2db9d5043a7a0087a4fab1d278df5f36c7717`.

Published-main CI:

```text
run 31699241010 = SUCCESS
```

Therefore R3.14C is a production milestone, not merely branch evidence.

## 5. Precursor repository-hygiene maintenance

R3.14C validation exposed a pre-existing stale `Cargo.lock`: `mimir-cli` already depended on `mimir-replay`, while the committed lock package dependency list omitted that workspace dependency.

This was repaired separately before R3.14C and is **not** counted as replay capability expansion.

Maintenance production SHA:

```text
c42836647673cecc47cc9c89908da1de11d8a222
```

Maintenance changed only:

- the exact missing `mimir-replay` lock dependency row;
- `scripts/verify_repo.ps1` so dependency-resolving Cargo commands use `--locked`.

This permanently prevents the same stale-lock condition from hiding behind a green verifier.

## 6. Boundaries still closed

R3.14C does not admit:

```text
ReplayNetworkFirstActorEnvelopeV1
native first actor-envelope reader
actor_present replay parsing
actor_id replay parsing as a public result
alive/new replay parsing as a public result
name_id
post-name one-bit field
object_id
spawn trajectory payload
property-present loop
stream_id production path
attribute payload
actor lifecycle mutation
multi-actor iteration
multi-frame iteration
raw state
events
replay slices
skills
```

## 7. Next exact pass

```text
R3.14D — first actor envelope header native reader
```

R3.14D may use the admitted private primitives to consume only:

```text
first frame time
first frame delta
actor_present
bounded actor_id, if present
alive, if present
new, if alive
STOP
```

The hard stop remains before `name_id` and every spawn/property/attribute field.
