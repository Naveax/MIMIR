# MIMIR — R3.15B NewActor Contract Decision

**Date:** 2026-08-13
**Pass:** `R3.15B — NewActor native contract admission`
**Outcome:** **ADMITTED / COMPLETE**
**Pass kind:** planning / contract / docs-only
**Production Rust changed:** **NO**

## Authorities

```text
production SHA              = 7b17cb9033b6c71d476e500380d78402cbb3c56d
continuity base/main        = fb2bbdec739b440ebbc2465db09bdcc9faac2ce1
R3.15A evidence head        = 1e27674625fdff26e05436e882014db5c7c5116d
R3.15A workflow run         = 31708322309
R3.15A artifact ID          = 9184200143
R3.15A artifact SHA-256     = a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d
pinned Boxcars SHA          = c70e77df7af81b436cb545d070bb90c82f562d0b
R3.15B execution spec       = docs/continuity/MIMIR_R3_15B_EXECUTION_SPEC.md
```

## Admission decision

The R3.15B contract is admitted without production-code changes. The contract is sufficiently narrow and unambiguous for the next implementation pass:

```text
current supported tuple     = 868 / 32 / 10
name_id                     = raw signed i32 / 32 bits on every admitted input
opaque post-name field      = exactly one bit, semantics remain unknown
object_id                   = raw signed i32 / 32 bits
spawn dispatch              = existing ReplayNetworkLookupPlanV1 static table only
Vector3i                    = bounded size prefix + three variable-width signed-biased components
Rotation                    = yaw/pitch/roll; one presence bit + optional signed i8 each
trajectory                  = None | Location | LocationAndRotation
failure policy              = fail closed; composite reads cursor-atomic
hard stop                   = exact end of first NewActor spawn trajectory
```

R3.15A established 169,538 / 169,538 static spawn-kind equality across all 47 supported replays, with all three trajectory families observed and zero production mutation. The corpus observed only the name-gate-true family; the contract therefore relies on the already-admitted current version tuple and pinned-source gate for that rule and does not claim empirical coverage of older gate-false tuples.

## R3.15C allowed production scope

Unless fresh source truth requires a smaller support refactor, R3.15C may change only:

```text
crates/mimir-replay/src/lib.rs
```

The implementation must be additive. The already-admitted `ReplayNetworkFirstActorEnvelopeV1` behavior remains unchanged.

Still forbidden in R3.15C:

```text
Cargo.toml / Cargo.lock changes
external parser dependency
property_present consumption
stream/property ID decoding
attribute payload decoding
second actor / second frame iteration
actor lifecycle table
raw state / events / skills
support-lane widening
```

## Validation gate

R3.15C must pass focused tests plus the repository gates on the exact candidate SHA before publication:

```text
cargo fmt --all -- --check
cargo check --workspace --all-targets --all-features --locked
cargo test -p mimir-replay --locked -- --nocapture
cargo test --workspace --all-targets --all-features --locked
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
git diff --check
pwsh -NoProfile -File ./scripts/verify_repo.ps1
```

## Next exact pass

`R3.15C — first NewActor native reader through spawn trajectory`.
