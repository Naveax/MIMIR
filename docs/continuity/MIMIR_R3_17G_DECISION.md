# MIMIR — R3.17G Native K2 Decoder Production Decision

**Date:** 2026-08-14
**Pass:** `R3.17G — direct native K2 decoder implementation for contract-admitted variants only`
**Outcome:** **A — ADMITTED / PRODUCTION PUBLISHED**
**Production Rust changed:** **YES, exact two-file scope**

## Frozen authority

```text
pre-pass main                 4638aeabca8e971805d2e294fea0f24543e9e5a8
production SHA                9bfa837c69c4751f70ca63a17c65f0f89877ff32
production tree               86f4419e5cce7f6264119a7530b67177e5ecd08d
production source blob        7288238cfb5338653552435be6af41f0dd7a4e85
focused test blob             92033a72a8a737605ac3bf91e10d130082277e04
R3.17F contract               Outcome A
R3.17E evidence head          19db534a3668f84f1c5ce36ef1252c52841d890f
pinned Boxcars SHA            c70e77df7af81b436cb545d070bb90c82f562d0b
implementation run/job        31805820332 / 94784362093 SUCCESS
clean-candidate CI            31806206582 / 94785622371 SUCCESS
published-main CI             31806554445 / 94786777798 SUCCESS
```

## Exact production scope

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs
```

No Cargo manifest/lockfile, fixture, replay corpus, support-lane or unrelated crate change was admitted.

## Production capability admitted

`decode_replay_network_k2_v1` directly decodes exactly one already-resolved K2 payload using the existing LSB-first `NetworkBitCursor` semantics. The public result retains exact start/end/width identity and typed semantics. The caller supplies the already-resolved attribute tag plus `net_version` / `is_rl_223` context.

Admitted variants are exactly the R3.17F surface:

```text
ActiveActor
  active:1 + actor:i32 => 33 bits

String
  signed-i32 Empty / positive Windows1252 / negative UTF16LE

QWordString
  !RL223 => u64
  RL223  => positive Windows1252 only

UniqueId at net_version 10
  Steam
  PlayStation in observed RL223 context
  PsyNet in observed RL223 context
  Epic Windows1252 declared length 33

PartyLeader
  only net10 + RL223 + Some(Epic Windows1252 declared=33)
```

Unobserved systems, context combinations and text forms fail closed.

## Failure / stop semantics

Stable failure categories include `invalid-start`, `insufficient-bits`, `invalid-text-length`, `unadmitted-context`, `unadmitted-k2-shape`, and `unsupported-k2-tag`.

The implementation snapshots the payload start and restores the internal cursor on decode failure. Success returns the exact first bit after one K2 value. No success or failure grants permission to decode a second property.

## Text semantics

Windows-1252 decoding is implemented locally without adding a dependency. UTF-16LE uses deterministic lossy surrogate replacement. As frozen by R3.17F, the final declared terminator byte/code unit is omitted semantically but is not required to be numerically zero.

## Validation

The focused R3.17G integration suite contains 8 privacy-safe synthetic tests covering admitted shapes, unaligned starts, exact end bits, truncation, malformed lengths, wrong contexts, unadmitted systems/shapes, unsupported tag and invalid start behavior.

```text
focused tests                         8 / 8 PASS
cargo test -p mimir-replay            189 PASS
cargo clippy --workspace --all-targets -- -D warnings
                                      PASS
scripts/verify_repo.ps1               PASS
clean candidate exact-SHA CI          PASS
published main exact-SHA CI           PASS
```

An initial disposable validation attempt was not admitted because clippy found only two hygiene defects: an empty line after a doc comment and an unread rollback assignment. The corrected v2 retained the same passing behavior tests, removed those lint defects, and is the sole implementation authority listed above.

## Still closed

```text
unobserved K2 variants
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
K3 / K4
raw state / events / replay slices / skills
runtime / export widening
support-lane widening
```

## Next exact pass

`R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses`.
