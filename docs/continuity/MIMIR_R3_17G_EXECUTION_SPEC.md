# MIMIR — R3.17G Direct Native K2 Decoder Execution Spec

**Pass type:** production implementation
**Input authority:** R3.17F Outcome A
**External parser dependency:** forbidden

## Goal

Implement a direct native one-value K2 decoder for only the contract-admitted R3.17F shapes, preserving exact bit boundaries and atomic failure semantics.

## Required production seam

Add an additive API in `mimir-replay` equivalent to:

```text
ReplayNetworkK2DecodeContextV1 { net_version: i32, is_rl_223: bool }
ReplayNetworkUniqueIdV1
ReplayNetworkK2ValueV1
ReplayNetworkK2DecodeV1 {
    attribute_tag,
    payload_start_bit,
    payload_end_bit,
    payload_width,
    value,
}

decode_replay_network_k2_v1(network_bytes, payload_start_bit, attribute_tag, context)
```

Exact Rust naming may vary only if the resulting API preserves this data and the focused tests remain explicit.

## Admitted implementation surface

- ActiveActor: exact 33-bit `{active, actor:i32}`.
- String: signed-i32 Empty / positive Windows-1252 / negative UTF-16LE branches per R3.17F.
- QWordString: legacy QWord64 when `is_rl_223=false`; positive Windows-1252 text only when true.
- UniqueId at `net_version=10`: Steam, PlayStation, PsyNet, Epic declared=33 only, with R3.17F observed context matrix.
- PartyLeader: only `net_version=10`, `is_rl_223=true`, Some(Epic Windows-1252 declared=33).

## Atomicity

Use `NetworkBitCursor` and snapshot the start position before any branch read. Every failure must restore the internal cursor to the starting position. No partial decode may expose an advanced end bit.

Checked arithmetic is mandatory for bit/byte lengths. `i32::MIN` text length fails closed.

## Text semantics

Implement deterministic decoding without adding Cargo dependencies.

- Windows-1252 uses the standard byte-to-Unicode mapping; omit the final declared terminator slot without requiring it to equal zero.
- UTF-16LE decodes complete 16-bit units before the final declared terminator slot and uses deterministic U+FFFD replacement for malformed surrogate structure.
- QWordString RL223 admits only the positive Windows-1252 branch.
- Epic IDs admit only positive Windows-1252 declared length 33.

## Focused tests

Create `crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs` with synthetic privacy-safe vectors covering every admitted shape and every rejection family from R3.17F. Include unaligned payload starts and exact end-bit assertions.

At minimum test:

```text
ActiveActor success x4 + truncation
String empty / Windows-1252 / UTF-16LE / i32::MIN / truncation
QWordString legacy / RL223 text / RL223 empty reject / RL223 UTF-16 reject
UniqueId Steam / PlayStation / PsyNet / Epic success
UniqueId wrong net version / systems 0,4,5,6 / unknown system / wrong Epic shape reject
PartyLeader Epic success / None reject / non-Epic reject / wrong context reject
non-K2 tag reject
payload_start beyond network reject
```

## Validation gates

```text
cargo fmt --all -- --check
cargo test -p mimir-replay --test r3_17g_k2_attribute_decoder
cargo test -p mimir-replay
cargo clippy --workspace --all-targets -- -D warnings
scripts/verify_repo.ps1
clean-tree / exact diff scope audit
published-main CI + Knowledge Archive
```

Production diff should remain limited to:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs
```

Any required Cargo, corpus, fixture or unrelated crate change stops R3.17G and requires a new contract/evidence decision.

## Hard stop

R3.17G decodes exactly one already-resolved K2 payload and stops at its `payload_end_bit`. It does not continue the property loop or mutate actor/frame state.

Still closed: unobserved K2 forms, K3/K4, second property, next actor/frame, lifecycle mutation, raw state, events, replay slices, skill mining, runtime/export and support-lane widening.

## Next pass on successful production publication

`R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses`.
