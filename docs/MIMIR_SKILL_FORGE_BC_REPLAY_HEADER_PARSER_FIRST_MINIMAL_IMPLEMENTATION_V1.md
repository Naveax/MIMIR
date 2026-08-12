# MIMIR Skill Forge BC Replay Header Parser First Minimal Implementation v1

Pass date: 2026-05-02

## Purpose

This pass implements the first minimal MIMIR Rocket League replay header parser for the admitted
private-local fixture:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`
- admission form: `PRIVATE_LOCAL_PATH_WITH_HASH`

This implementation is header-only and bounded to the first admitted `ReplayInput::Memory`
surface. It does not parse replay bodies, raw-state payloads, frames, footers, or events.

## File Boundary

Rust source changed:

- `crates/mimir-replay/src/lib.rs`

Required artifacts added:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIRST_MINIMAL_IMPLEMENTATION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_first_minimal_implementation_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_first_minimal_implementation_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_first_minimal_implementation_status.txt`

No manifests, lockfiles, `mimir-io`, `mimir-export`, or `mimir-types` files were modified.

## Public API Added

Added:

- `pub struct MinimalReplayHeaderReader;`
- `impl ReplayReader for MinimalReplayHeaderReader`

Preserved unchanged:

- `UnsupportedReplayReader`

No convenience API, CLI path, runtime caller, export integration, or backend parser dependency was
added.

## Parser Algorithm Implemented

The parser accepts only:

- `ReplayInput::Memory { label, bytes }`

It rejects:

- `ReplayInput::File(_)` with `replay header parse error: unsupported-input`
- empty memory labels with `replay header mapping error`
- insufficient prefix/header bytes with `replay header parse error: insufficient`

Implemented header flow:

1. Read `header_size: i32` at offset `0`.
2. Read `header_crc: u32` at offset `4` as layout evidence only.
3. Do not validate or expose CRC.
4. Compute `header_end = 8 + header_size`.
5. Reject negative, overflowing, or unavailable header regions.
6. Parse only `[8, header_end)`.
7. Read `major_version`, `minor_version`, `net_version`, and `game_type`.
8. Scan top-level properties until `None`.
9. Reject duplicate top-level names, with duplicate selected names classified as mapping errors.
10. Parse only selected scalar fields.
11. Skip non-selected admitted top-level properties by bounded `property_size`.
12. Skip non-selected top-level `ArrayProperty` only by bounded `property_size`.
13. Reject selected arrays and unknown/unencountered property kinds.
14. Reject negative-length/UTF-16 text as unsupported text.
15. Require the `None` terminator to end exactly at `header_end`.
16. Allow trailing bytes after `header_end`.

The exact supported tuple is:

- `major_version = 868`
- `minor_version = 32`
- `net_version = Some(10)`
- `game_type = TAGame.Replay_Soccar_TA`
- `ReplayVersion = 8`
- `BuildVersion = 241206.55345.468477`

Selected mappings implemented:

- `Id -> ReplayHeader.replay_id`
- `ReplayInput::Memory.label -> ReplayHeader.source_label`
- `NumFrames -> ReplayHeader.total_frames`
- selected metadata keys:
  - `ReplayName`
  - `Date`
  - `MapName`
  - `ReplayVersion`
  - `BuildVersion`
  - `MaxChannels`
  - `MatchType`
  - `TeamSize`
  - `RecordFPS`

## Tests Implemented

Unit tests were added inside `crates/mimir-replay/src/lib.rs`.

Fixture tests:

- parse `rl_replay_header_fixture_001` from `ReplayInput::Memory`
- assert exact replay id, source label, total frames, and selected metadata
- parse a byte slice truncated exactly to `8 + header_size`
- assert the header-only parse returns the same `ReplayHeader`
- skip only the fixture-specific test if the fixture path is missing or unreadable

Synthetic tests:

- reject `ReplayInput::File` with `unsupported-input`
- reject empty memory label with `replay header mapping error`
- reject fewer than 4 bytes with `insufficient`
- reject fewer than 8 bytes with `insufficient`
- reject negative `header_size` with `malformed`
- reject `header_size` larger than bytes with `insufficient`
- reject unsupported version tuple with `unsupported-version`
- reject missing terminator with `malformed`
- reject duplicate selected property with `replay header mapping error`
- reject duplicate top-level property with `malformed`
- reject unknown property kind with `unsupported-property`
- reject negative-length/UTF-16 text with `unsupported-text`
- reject selected `ArrayProperty` with mapping error
- reject selected non-finite float with `replay header mapping error`
- confirm changing only `header_crc` still parses the same header

## Fixture Result

Fixture identity was reverified before status creation:

- observed byte length: `3001021`
- observed SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`

`cargo test -p mimir-replay -- --nocapture` passed:

- `17 passed`
- fixture happy path passed
- complete-header-only stop-boundary test passed
- synthetic error-boundary tests passed

Expected parsed header for the fixture:

- `ReplayId::new("7F59297811EFD8B19C444A81FB07660C")`
- `source_label = "rl_replay_header_fixture_001"`
- `total_frames = Some(13555)`
- selected metadata values exactly matched the admitted evidence.

## Non-Goals Preserved

The implementation intentionally does not:

- validate header CRC
- expose CRC
- read or validate `content_crc`
- parse body payloads
- parse raw-state payloads
- parse replay frames
- parse footer structures
- parse semantic replay events
- parse nested array semantics
- support UTF-16 text
- support unknown/unencountered property kinds
- support `ReplayInput::File`
- add any backend replay parser dependency
- broaden Rocket League replay version support beyond the exact admitted tuple

## Forbidden Boundaries Preserved

Forbidden changes were not made:

- `mimir-io` unchanged
- `mimir-export` unchanged
- `mimir-types` unchanged
- `Cargo.toml` unchanged
- `Cargo.lock` unchanged
- no backend parser dependency added
- no `mimir_export` widening
- no CLI/runtime code added

Dependency scan over MIMIR manifests and lockfile found no matches for:

- `boxcars`
- `rattletrap`
- `rrrocket`
- `carball`
- `rlreplay`
- `subtr-actor`

## Validation

Commands run:

- `cargo fmt --all`
- `cargo check --workspace --all-targets --all-features`
- `cargo test -p mimir-replay -- --nocapture`
- `cargo test --workspace --all-targets --all-features`
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`
- `cargo test -p mimir-export -- --list`

All commands succeeded.

`cargo test -p mimir-export -- --list` result:

- `173 tests, 0 benchmarks`
- doc-tests: `0 tests, 0 benchmarks`

## Next Stage

Next pass should be a parser implementation admission/audit pass.

No broad parser expansion is admitted yet. CRC validation, body parsing, raw-state payloads, frame
extraction, event extraction, nested array semantics, UTF-16 support, file input, additional
property kinds, and broad version-family support remain closed.
