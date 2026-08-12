# MIMIR Skill Forge BC Replay Header Parser Fixture 003 Intake Readiness V1

Pass date: 2026-05-05

## Purpose

Plan and admit, or reject, `rl_replay_header_fixture_003` as the next narrow replay-header parser
boundary target.

This is a fixture/evidence intake and planning pass only. It does not implement parser code, add a
third supported tuple, broaden replay parsing, add file input support, validate CRCs, parse replay
body bytes, or wire export, runtime, CLI, IO, or backend parser behavior.

## Selected Outcome

Outcome A.

The fixture_003 target is available and its file identity was verified. It is admitted only as
`PRIVATE_LOCAL_PATH_WITH_HASH`. Parser success is not claimed for fixture_003.

## Current Admitted Exact Parser Boundary

The current admitted parser success boundary remains unchanged:

- `MinimalReplayHeaderReader` is explicit opt-in only.
- Parser success is admitted only through `ReplayInput::Memory`.
- Fixture_001 regression is admitted.
- Fixture_002 exact happy path is admitted.
- Fixture_002 header-only stop-boundary is admitted.
- Unknown `BuildVersion` rejection is admitted.
- Broad parser success is not admitted.
- `ReplayInput::File` support is not admitted.

The exact admitted tuples remain:

| Fixture | `major_version` | `minor_version` | `net_version` | `game_type` | `ReplayVersion` | `BuildVersion` |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| fixture_001 | 868 | 32 | 10 | `TAGame.Replay_Soccar_TA` | 8 | `241206.55345.468477` |
| fixture_002 | 868 | 32 | 10 | `TAGame.Replay_Soccar_TA` | 8 | `250811.43331.492665` |

No third tuple is admitted by this pass.

## Re-Audited Inputs

Inspected directly before writing this artifact:

- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_exact_supported_tuple_implementation_audit_status.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_exact_supported_tuple_implementation_audit_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_exact_supported_tuple_implementation_audit_next.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_AUDIT_V1.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/README.md`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

## Fixture 001 Identity Confirmation

fixture_001 was reverified from
`D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`:

- extension: `.replay`
- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`
- first four bytes little-endian i32: `13200`
- byte length greater than 8: yes

These are file identity facts only. They are not parser predicates.

## Fixture 002 Identity Confirmation

fixture_002 was reverified from
`D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay`:

- extension: `.replay`
- byte length: `2632903`
- SHA-256: `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6`
- first four bytes little-endian i32: `11273`
- byte length greater than 8: yes

These are file identity facts only. They are not parser predicates.

## Fixture 003 Availability Result

`D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay` did not exist at the start of this
pass.

`MIMIR_REPLAY_FIXTURE_003_PATH` was set to a caller/user-supplied private local path:

- source path:
  `C:\Users\navea\Documents\My Games\Rocket League\TAGame\DemosEpic\DF72482811F0B757082C458D84251EFF.replay`
- source existed as a file: yes
- source extension: `.replay`
- source path differed from fixture_001 path: yes
- source path differed from fixture_002 path: yes
- source SHA-256 differed from fixture_001 SHA-256: yes
- source SHA-256 differed from fixture_002 SHA-256: yes

The source was copied to:

- destination path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay`

The source path is recorded only as a user-supplied private local path. It is not a parser fact.

## Fixture 003 Identity

fixture_003 is admitted only as `PRIVATE_LOCAL_PATH_WITH_HASH`:

- fixture id: `rl_replay_header_fixture_003`
- destination path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay`
- source/admission form: `PRIVATE_LOCAL_PATH_WITH_HASH`
- copied from `MIMIR_REPLAY_FIXTURE_003_PATH`: yes
- extension: `.replay`
- byte length: `1638538`
- SHA-256: `20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC`
- first four bytes little-endian i32: `11190`
- differs from fixture_001 by SHA-256: yes
- differs from fixture_002 by SHA-256: yes
- byte length greater than 8: yes

## Fixture Safety Checks

The fixture_003 intake safety checks passed:

- destination exists: yes
- destination is a file: yes
- extension is `.replay`: yes
- byte length is greater than 8: yes
- SHA-256 was recorded: yes
- SHA-256 is distinct from fixture_001 and fixture_002: yes
- first four bytes were read as cheap bytes-only header-size sanity evidence: yes

The first four bytes were not treated as parser success, version support, header mapping, CRC
validation, body parsing, or semantic replay evidence.

## Explicit Non-Claims

This pass does not claim:

- parser success for fixture_003
- fixture_003 support in `MinimalReplayHeaderReader`
- fixture_003 `ReplayHeader` mapping
- fixture_003 supported version tuple
- fixture_003 `BuildVersion`
- fixture_003 `ReplayVersion`
- broad parser success
- broad `ReplayVersion = 8` support
- wildcard `BuildVersion` support
- future unknown build support
- `ReplayInput::File` support
- CRC validation
- `content_crc` read or validation
- body parsing
- raw-state parsing
- frame parsing
- event parsing
- export integration
- runtime integration
- CLI integration
- backend replay parser dependency

Path, hash, filename, provenance, source path, destination path, and fixture id are file intake
facts only. They are not parser facts.

## What Remains Closed

The following remain closed:

- modifying `crates/mimir-replay/src/lib.rs`
- modifying `MinimalReplayHeaderReader`
- adding a third supported tuple
- adding a backend replay parser dependency
- adding `ReplayInput::File` support
- adding CRC validation
- reading or validating `content_crc`
- parsing body/raw-state/frame/event data
- adding broad version-family support
- adding wildcard `BuildVersion` support
- adding all-`ReplayVersion = 8` support
- adding future unknown build support
- adding export/runtime/CLI integration

## Next Stage

Outcome A next pass may generate and admit a fixture_003 structural/header report.

No parser expansion is authorized yet. No fixture_003 parser success is admitted by this pass.
