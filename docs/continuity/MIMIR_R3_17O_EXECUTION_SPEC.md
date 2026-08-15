# MIMIR R3.17O — Direct Native Exact-Contract K4 Decoder Implementation Execution Spec

**Pass type:** production implementation
**Contract authority:** R3.17N Outcome A
**Evidence authority:** R3.17M Outcome A
**Current production authority:** R3.17K / `7390e3b145372252caaa8fa1fe3e0cd13b83336c`

## Goal

Implement a direct native Rust one-value decoder for the exact 161 R3.17N K4 structural/context groups. The implementation must not infer additional combinations from independently observed fields and must stop at the exact end of one already-resolved attribute payload.

## Frozen contract identities

```text
contract commit                  c8ebb872e510574bb69ab28c719f415ece8b7665
contract tree                    61e36d40e6af3853a887e840b22f759dda26ed75
admitted-group SHA256            80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
admitted-group blob              b5fa6aaa729772ab3d113703952effe2346c9866
contract document blob           76deabf8241b419ca224645106d2a19b041e20f8
exact admitted rows              161
cross-product widening           0
production parent authority      7390e3b145372252caaa8fa1fe3e0cd13b83336c
```

The checked-in `docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl` is the source of truth for structural acceptance. Production code may use a generated/static Rust representation, but CI must independently prove exact tuple equality with all 161 rows and zero extras.

## Allowed production scope

Keep changes narrowly inside `crates/mimir-replay`:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/src/k4_admitted_groups.rs          optional generated/static exact allowlist
crates/mimir-replay/tests/r3_17o_k4_attribute_decoder.rs
```

A different similarly narrow file split is acceptable only if the clean diff remains within `crates/mimir-replay`. `Cargo.toml`, `Cargo.lock`, fixtures, corpus and supported replay lane must remain unchanged.

## Required public one-value surface

Expose a K4-specific API separate from K1/K2/K3, following existing naming/style conventions. It must carry the caller-resolved replay context needed by the contract and return:

- the decoded K4 value/variant,
- exact structural identity sufficient to prove admitted-group membership,
- exact payload end bit / consumed width,
- no continuation into another property.

Do not broaden existing K1/K2/K3 APIs merely to make K4 convenient.

## Decoder requirements

1. LSB-first bit order; arbitrary unaligned payload start is legal.
2. Checked arithmetic for all cursor movement, signed text lengths, nested counts and byte/bit multiplications.
3. Success only when the decoded exact tuple exists in the 161-row allowlist.
4. On failure, no successful partial value or admitted end position escapes.
5. Extra trailing bits stay unconsumed.
6. Source-known but R3.17M-unobserved branches fail closed.
7. No cross-product construction across `Reservation`, vector-pair or `LoadoutsOnline` substructures.
8. Preserve existing K1/K2/K3 behavior and tests exactly.

## Family surface

Implement only the R3.17N-admitted shapes:

```text
CamSettings          2 group rows / 1 shape / observed f32x7 width 224
ClubColors           1 / 1 / bit+u8+bit+u8 width 18
DemolishExtended     5 / 5
DemolishFx          19 / 12
ExtendedExplosion    2 / 1 / width 112
LoadoutsOnline      79 / 73 nested shapes
PlayerHistoryKey     1 / 1 / u14 width 14
Reservation         46 / 35
StatEvent            2 / 1 / bit+i32 width 33
TeamLoadout          2 / 1 / observed v28 branch width 1040
TeamPaint            2 / 1 / u8x3+u32x2 width 88
TOTAL              161 exact rows
```

For variable families, the allowlist tuple is decisive. A field branch appearing somewhere in evidence does not legalize a new combination.

## Positive gates

Create deterministic synthetic/materialized positives covering every admitted row:

```text
161/161 admitted rows decode successfully
returned K4 tag/variant exact
context exact
structural shape exact
payload width/end exact
allowlist membership exact
trailing poison bits consumed 0
repeatability exact
```

The test builder may derive vectors from the admitted-group artifact or a checked-in generated table, but private real replay payloads must not be added to the repository.

## Structural acceptance gate

Independently enumerate the production K4 allowlist and compare it against the R3.17N artifact:

```text
missing groups                  0
extra groups                    0
cross-product widening          0
161/161 equality                PASS
```

For feasible bounded branch dimensions, add explicit negative enumeration around admitted groups rather than testing only a few hand-picked rejects.

## Required negative / malformed gates

At minimum cover:

```text
unknown/non-K4 tag
invalid start bit
wrong major/minor/net_version/RL223 context
truncation at fixed primitive boundaries
representative one-bit truncation of variable-width groups
malformed signed text length / i32::MIN / checked overflow
Reservation unobserved identifier/name/text-length/context combination
DemolishFx unobserved attacker/victim vector-pair combination
DemolishExtended unobserved vector-pair combination
LoadoutsOnline unobserved outer/group/product combination
LoadoutsOnline malformed nested count/length
LoadoutsOnline unknown product-attribute object branch
unobserved TeamLoadout version branch
source-known but evidence-unobserved branch
extra trailing bits remain unconsumed
```

Map failures deterministically into the established fail-closed style, including invalid-start, insufficient-bits, invalid-length-or-count, unadmitted-context, unadmitted-k4-shape and unsupported-k4-tag semantics.

## Validation gates

```text
cargo fmt --all -- --check                            PASS
focused R3.17O tests                                  PASS
all 161 synthetic positives                          PASS
exact structural acceptance equality                 161/161
cross-product widening                               0
cargo test --locked -p mimir-replay                  PASS
cargo check --locked --workspace --all-targets --all-features PASS
cargo test --locked --workspace --all-targets --all-features  PASS
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings PASS
scripts/verify_repo.ps1                              PASS
Cargo/fixture/corpus/support-lane mutation            0/0/0/0
```

The clean production candidate must be rebuilt directly from fresh canonical `main`, contain only the intended `crates/mimir-replay` production/test changes, pass exact-SHA normal CI, and publish with `force=false`.

## Hard stop

R3.17O implements exactly one already-resolved K4 value only. Do not consume a second property, continue the property loop, advance to another actor/frame, mutate actor lifecycle state, materialize raw state/events, slice replay windows, mine skills, or widen runtime/export.

Do not perform the real-replay differential audit inside R3.17O.

## Next pass

Only if R3.17O closes Outcome A, open `R3.17P — Native K4 Real-Replay Differential Audit` as a separate read-only pass against regenerated pinned-Boxcars witnesses. R3.18 remains closed until that audit is separately complete or evidence explicitly revises the roadmap.
