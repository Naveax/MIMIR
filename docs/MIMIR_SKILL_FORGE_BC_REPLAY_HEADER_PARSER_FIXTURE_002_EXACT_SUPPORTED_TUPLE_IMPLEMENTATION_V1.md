# MIMIR Skill Forge BC Replay Header Parser Fixture 002 Exact Supported Tuple Implementation V1

## Purpose

Implement the previously planned exact two-tuple allowlist for `MinimalReplayHeaderReader` in
`crates/mimir-replay/src/lib.rs`.

This pass admits parser success only for the exact fixture-supported header tuples listed below. It
does not broaden replay parsing, input support, source materialization, body parsing, CRC validation,
or downstream integration.

## Selected Outcome

Outcome A.

The exact two-tuple allowlist was implemented and validated. The next pass should be exact supported
tuple implementation audit/admission. No broad parser expansion is admitted yet.

## Files Changed

- `crates/mimir-replay/src/lib.rs`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_exact_supported_tuple_implementation_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_exact_supported_tuple_implementation_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_exact_supported_tuple_implementation_status.txt`

No Rust source outside `crates/mimir-replay/src/lib.rs` was modified by this pass.

## Exact Code Change Summary

- Replaced the single `BuildVersion` support constant with two exact fixture-specific constants:
  - `SUPPORTED_BUILD_VERSION_FIXTURE_001 = "241206.55345.468477"`
  - `SUPPORTED_BUILD_VERSION_FIXTURE_002 = "250811.43331.492665"`
- Added private enum `SupportedReplayHeaderTupleV1` with variants:
  - `Fixture001Exact`
  - `Fixture002Exact`
- Added private helper `supported_replay_header_tuple_v1(...)`.
- Replaced the previous inline unsupported-version check with the exact helper.
- Kept the unsupported-version error category unchanged:
  - `replay header parse error: unsupported-version`
- Added fixture_002 exact happy-path and header-only tests.
- Added synthetic unknown `BuildVersion` rejection coverage.
- Preserved fixture_001 happy-path/header-only coverage and existing negative boundary tests.

## Exact Supported Tuple Allowlist

Shared required tuple components:

| Component | Exact admitted value |
| --- | --- |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `10` |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| `ReplayVersion` | `8` |

Exact fixture-specific `BuildVersion` values:

| Variant | `BuildVersion` |
| --- | --- |
| `SupportedReplayHeaderTupleV1::Fixture001Exact` | `241206.55345.468477` |
| `SupportedReplayHeaderTupleV1::Fixture002Exact` | `250811.43331.492665` |

The predicate does not inspect path, hash, filename, provenance, artifact id, fixture id, label, or
body bytes.

## Fixture Identity Verification

fixture_001 was verified from `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`:

- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`
- first four bytes little-endian i32: `13200`

fixture_002 was verified from `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay`:

- byte length: `2632903`
- SHA-256: `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6`
- first four bytes little-endian i32: `11273`

## Fixture 001 Regression Result

Passed.

`cargo test -p mimir-replay -- --nocapture` passed with 20 tests. Fixture_001 regression coverage
remained in:

- `minimal_reader_parses_rl_replay_header_fixture_001_and_header_only_slice`

The fixture_001 expected `ReplayHeader` values remained unchanged, including:

- `replay_id = 7F59297811EFD8B19C444A81FB07660C`
- `source_label = rl_replay_header_fixture_001`
- `total_frames = Some(13555)`
- `BuildVersion = Text("241206.55345.468477")`

The fixture_001 header-only stop boundary still passed.

## Fixture 002 Exact Happy-Path Result

Passed.

The fixture_002 test reads
`D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` using
`ReplayInput::Memory { label: "rl_replay_header_fixture_002", bytes }`.

The admitted parser output was verified as:

- `replay_id = D9DA34DA11F0811EAC139A94CBF30AF2`
- `source_label = rl_replay_header_fixture_002`
- `total_frames = Some(10351)`
- `ReplayName = Text("asdasd")`
- `Date = Text("2025-08-24 19-16-35")`
- `MapName = Text("NeoTokyo_Standard_P")`
- `ReplayVersion = Integer(8)`
- `BuildVersion = Text("250811.43331.492665")`
- `MaxChannels = Integer(2047)`
- `MatchType = Text("Online")`
- `TeamSize = Integer(3)`
- `RecordFPS = Float(30.0)`

The fixture_002 header-only stop-boundary also passed by slicing to exactly `8 + header_size =
11281` bytes. No body bytes were required.

## Unknown BuildVersion Rejection Result

Passed.

`minimal_reader_rejects_unknown_build_version_for_otherwise_supported_tuple` builds an otherwise
supported synthetic tuple and sets:

- `BuildVersion = "250812.43331.492665"`

The parser rejects it with:

- `replay header parse error: unsupported-version`

This proves the implementation did not add wildcard `BuildVersion` support.

## Tests Added Or Changed

Added:

- `minimal_reader_parses_rl_replay_header_fixture_002_exact_happy_path`
- `minimal_reader_parses_rl_replay_header_fixture_002_header_only_slice`
- `minimal_reader_rejects_unknown_build_version_for_otherwise_supported_tuple`

Adjusted:

- Fixture constants and fixture loader inside `crates/mimir-replay/src/lib.rs` tests.
- Synthetic `HeaderSpec` now carries an explicit `build_version` so the unknown build regression can
  be precise.
- Fixture_001 assertion helper was renamed to `assert_fixture_001_header`.
- Added `assert_fixture_002_header`.

Preserved:

- `ReplayInput::File` unsupported-input test
- CRC non-validation boundary test
- malformed and truncated header tests
- duplicate selected property behavior
- selected wrong-kind, non-finite, and array behavior
- unsupported property/text cases

## Boundaries Preserved

- `ReplayInput::File` remains unsupported.
- No CRC validation was added.
- `header_crc` remains layout-read only.
- `content_crc` is not read or validated.
- Body, raw-state, frame, and event parsing remain closed.
- No replay-source materialization was added.
- No path, hash, filename, provenance, artifact id, or fixture id parser predicates were added.
- No CLI, export, runtime, or mimir-skill integration was added.
- No backend replay parser dependency was added.
- No manifest or lockfile change was made.
- No broad version-family support was added.
- No wildcard `BuildVersion` support was added.
- No all-`ReplayVersion = 8` support was added.
- No future unknown build support was added.

## Explicit Non-Claims

This pass does not claim:

- broad parser success
- broad Rocket League replay support
- broad `ReplayVersion = 8` support
- wildcard `BuildVersion` support
- future unknown build support
- `ReplayInput::File` support
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- `content_crc` read or validation
- body/raw-state/frame/event parsing
- export/runtime/CLI integration
- backend replay parser dependency in MIMIR

Parser success is now admitted only for exact allowlisted tuples through explicit
`ReplayInput::Memory` bytes.

## Validation

All required validation commands passed:

- `cargo fmt --all`
- `cargo check --workspace --all-targets --all-features`
- `cargo test -p mimir-replay -- --nocapture`
- `cargo test -p mimir-skill -- --nocapture`
- `cargo test --workspace --all-targets --all-features`
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`
- `cargo test -p mimir-export -- --list`

## Next Stage

Outcome A next pass:

- exact supported tuple implementation audit/admission
- no broad parser expansion yet
- no export/runtime/CLI integration yet
- no replay-source materialization yet
