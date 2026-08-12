# MIMIR Skill Forge BC Replay Header Parser Fixture 002 Exact Supported Tuple Implementation Audit V1

Pass date: 2026-05-05

## Purpose

Audit and admit or reject the implemented `MinimalReplayHeaderReader` exact two-tuple allowlist for
fixture_001 and fixture_002.

This is an audit/admission pass. It does not broaden parser scope, add parser functionality, add
tuple support, add source materialization, add CRC validation, parse body bytes, or wire export,
runtime, CLI, IO, or skill behavior.

## Selected Outcome

Outcome A.

The implementation is admitted. Parser success is admitted only for exact allowlisted tuples through
`ReplayInput::Memory`. Broad parser expansion remains closed.

## Re-Audited Inputs

Inspected directly:

- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/README.md`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- prior fixture_002 exact implementation artifacts
- prior fixture_002 exact implementation planning artifacts
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_SUPPORTED_VERSION_POLICY_PLANNING_REOPEN_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_MAPPING_ERROR_BOUNDARY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIRST_MINIMAL_IMPLEMENTATION_AUDIT_V1.md`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

## Fixture Identity Verification

fixture_001 was verified from `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`:

- extension: `.replay`
- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`
- first four bytes little-endian i32: `13200`
- byte length greater than 8: yes

fixture_002 was verified from `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay`:

- extension: `.replay`
- byte length: `2632903`
- SHA-256: `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6`
- first four bytes little-endian i32: `11273`
- byte length greater than 8: yes
- differs from fixture_001 by SHA-256: yes

These identity facts remain audit facts only. They are not parser support predicates.

## Exact Tuple Predicate Audit

`crates/mimir-replay/src/lib.rs` defines:

- `SUPPORTED_BUILD_VERSION_FIXTURE_001 = "241206.55345.468477"`
- `SUPPORTED_BUILD_VERSION_FIXTURE_002 = "250811.43331.492665"`
- private `SupportedReplayHeaderTupleV1`
- private `supported_replay_header_tuple_v1(...)`

The shared required tuple values are exact:

| Component | Required value |
| --- | --- |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `10` |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| `ReplayVersion` | `8` |

The `BuildVersion` match is exact string equality only:

- `241206.55345.468477` -> `SupportedReplayHeaderTupleV1::Fixture001Exact`
- `250811.43331.492665` -> `SupportedReplayHeaderTupleV1::Fixture002Exact`
- any other value -> `None`

Any other major, minor, net, game type, or replay version returns `None` before the `BuildVersion`
match. The caller maps `None` to `replay header parse error: unsupported-version`.

The predicate does not use prefix, range, contains, regex, wildcard, date-family, or version-family
logic. It does not inspect fixture path, SHA-256, filename, provenance, artifact id, fixture id,
`ReplayInput` label, body bytes, `header_crc`, `content_crc`, or any replay-source fact.

## Parse Boundary Audit

`ReplayInput::Memory { label, bytes }` remains the only accepted input variant for
`MinimalReplayHeaderReader`.

`ReplayInput::File(_)` still returns `replay header parse error: unsupported-input`.

The parser still:

- reads `header_size` at offset 0
- reads `header_crc` at offset 4 as layout only
- computes `header_end = 8 + header_size`
- parses only `bytes[8..header_end]`
- requires the top-level `None` terminator to end exactly at the header boundary
- permits trailing bytes after `header_end`

fixture_002 header-only parsing is admitted for the exact slice length `11281` bytes
(`8 + 11273`). No fixture_002 body bytes are required for the admitted header parse.

`header_crc` remains non-validating. `content_crc` is not read or validated. Body, raw-state,
frame, and event parsing remain absent.

## Test Audit

`cargo test -p mimir-replay -- --nocapture` reported:

- `20 passed`
- `0 failed`
- `0 ignored`

The required tests exist and passed:

- `minimal_reader_parses_rl_replay_header_fixture_001_and_header_only_slice`
- `minimal_reader_parses_rl_replay_header_fixture_002_exact_happy_path`
- `minimal_reader_parses_rl_replay_header_fixture_002_header_only_slice`
- `minimal_reader_rejects_unknown_build_version_for_otherwise_supported_tuple`

The `ReplayInput::File` unsupported-input test remains. The CRC non-validation test remains.
Malformed, truncated, duplicate, wrong-kind, non-finite, and selected-array tests remain.

fixture_002 selected metadata assertions match the admitted expected-output evidence:

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

## Fixture Helper And Env Override Audit

`load_fixture_bytes_or_skip(default_path, fixture_id)` uses only the explicit `default_path`
argument. It does not read `MIMIR_REPLAY_FIXTURE_PATH` or any other environment override.

The helper can skip a fixture-specific test only if the hardcoded fixture path is missing or
unreadable. In this audit pass both fixture paths were verified before tests ran, and the
`mimir-replay` test output had no skip message. The helper behavior is admitted for this pass.

The specific risk of fixture_002 accidentally loading fixture_001 would fail loudly: the
fixture_002 header-only test asserts `header_size == 11273` and `header_end == 11281`, and both
fixture_002 tests assert the fixture_002 replay id, source label, total frames, `BuildVersion`, and
selected metadata. The fixture SHA-256 verification in this audit is still the proof of exact
fixture identity.

## Forbidden Boundary Audit

No support was added for:

- `ReplayInput::File`
- wildcard `BuildVersion`
- broad `ReplayVersion = 8`
- broad version-family support
- future unknown build support
- CRC validation
- `content_crc` read or validation
- body parsing
- raw-state parsing
- frame parsing
- event parsing
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- export/runtime/CLI integration
- backend parser dependencies

Direct file inspection and hash checks showed no audit-pass changes to:

- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `crates/mimir-cli`
- `crates/mimir-io`
- `crates/mimir-export`
- `Cargo.toml`
- `Cargo.lock`

`crates/mimir-replay/Cargo.toml` remains dependency-limited to `mimir-core`, `mimir-types`, and
`serde`. Root manifests contain no replay parser backend dependency added by this pass.

## Validation Results

All required validation commands passed:

- `cargo fmt --all`
- `cargo check --workspace --all-targets --all-features`
- `cargo test -p mimir-replay -- --nocapture`
- `cargo test -p mimir-skill -- --nocapture`
- `cargo test --workspace --all-targets --all-features`
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`
- `cargo test -p mimir-export -- --list`

Observed key validation facts:

- `cargo test -p mimir-replay -- --nocapture`: `20 passed; 0 failed; 0 ignored`
- `cargo test -p mimir-skill -- --nocapture`: `273 passed; 0 failed; 0 ignored`
- `cargo test -p mimir-export -- --list`: `173 tests, 0 benchmarks`
- pre/post validation hashes for forbidden source, manifest, lockfile, and forbidden crate
  directories matched

## Exact Admitted Parser-Success Boundary

Parser success is admitted only when all of the following hold:

- caller explicitly uses `MinimalReplayHeaderReader`
- input is `ReplayInput::Memory`
- memory label is non-empty and maps directly to `ReplayHeader.source_label`
- bytes contain the complete header prefix and header region
- parsing stops at `8 + header_size`
- top-level terminator ends exactly at the header boundary
- selected scalar mappings are structurally valid
- tuple is exactly one of:
  - `major_version=868`, `minor_version=32`, `net_version=10`,
    `game_type=TAGame.Replay_Soccar_TA`, `ReplayVersion=8`,
    `BuildVersion=241206.55345.468477`
  - `major_version=868`, `minor_version=32`, `net_version=10`,
    `game_type=TAGame.Replay_Soccar_TA`, `ReplayVersion=8`,
    `BuildVersion=250811.43331.492665`

## Explicit Non-Claims

This audit does not claim:

- broad Rocket League replay support
- broad parser success
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

## Residual Risks

The admitted parser remains intentionally minimal. It still does not prove replay body semantics,
raw-state availability, frame/event extraction, CRC validity, runtime integration, CLI loading, or
export behavior. The exact two-tuple allowlist should not be treated as version-family support.

## Next Stage

Outcome A next pass may plan the next narrow replay-header parser boundary.

No broad parser expansion is authorized. No export/runtime/CLI integration is authorized by this
audit.
