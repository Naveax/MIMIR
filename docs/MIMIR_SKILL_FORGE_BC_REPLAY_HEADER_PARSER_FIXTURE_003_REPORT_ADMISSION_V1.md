# MIMIR Skill Forge BC Replay Header Parser Fixture 003 Report Admission V1

Pass date: 2026-05-06

## Purpose

Admit or reject the generated fixture_003 external parser/header report and structural report as
evidence-only inputs for a later mapping/error-boundary admission pass.

This pass is report admission only. It does not implement parser code, does not run the MIMIR
parser as proof of fixture_003 support, does not add fixture_003 as a supported tuple, and does not
broaden replay parser support.

## Selected Outcome

Outcome A.

The fixture_003 external parser/header report and external structural report are internally
consistent, bounded to fixture_003 identity, and safe to admit as evidence-only inputs. The selected
property evidence is admitted only as candidate mapping evidence. The byte-layout evidence is
admitted only as external structural/report evidence.

No parser-success is claimed for fixture_003. No broad parser-success is admitted.

## Re-Audited Inputs

Inspected before writing this artifact:

- `artifacts/replay_header_reports/rl_replay_header_fixture_003_report.txt`
- `artifacts/replay_header_reports/rl_replay_header_fixture_003_structural_report.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_REPORT_GENERATION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_report_generation_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_report_generation_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_report_generation_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_INTAKE_READINESS_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_intake_readiness_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_AUDIT_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_exact_supported_tuple_implementation_audit_status.txt`
- `crates/mimir-replay/README.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

The re-audit confirmed that `MinimalReplayHeaderReader` remains exact allowlist gated for
fixture_001 and fixture_002 only. `crates/mimir-replay/src/lib.rs` still contains no fixture_003
supported tuple and no `BoolProperty` support in the admitted MIMIR parser path.

## Fixture Identity Verification

Fixture identities were reverified directly from disk.

| Fixture | Path | Byte length | SHA-256 | First four bytes as LE i32 | Extension | > 8 bytes |
| --- | --- | ---: | --- | ---: | --- | --- |
| `rl_replay_header_fixture_001` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | `3001021` | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `13200` | `.replay` | yes |
| `rl_replay_header_fixture_002` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` | `2632903` | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` | `11273` | `.replay` | yes |
| `rl_replay_header_fixture_003` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay` | `1638538` | `20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC` | `11190` | `.replay` | yes |

Fixture_003 differs from fixture_001 by SHA-256: yes.

Fixture_003 differs from fixture_002 by SHA-256: yes.

These are fixture identity facts only. Path, filename, byte length, SHA-256, fixture id, and
provenance are not parser facts.

## Report File Verification

| Report | Current size | Size matches recorded summary | Fixture identity present | Non-claim language present |
| --- | ---: | --- | --- | --- |
| `artifacts/replay_header_reports/rl_replay_header_fixture_003_report.txt` | `4167` bytes | yes | yes | yes |
| `artifacts/replay_header_reports/rl_replay_header_fixture_003_structural_report.txt` | `21787` bytes | yes | yes | yes |

Both reports identify fixture_003 with byte length `1638538` and SHA-256
`20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC`.

Both reports state that they were generated outside MIMIR, are not MIMIR parser output, are not
parser-success evidence, do not admit broad parser support, do not claim body/raw-state/frame/event
parsing as MIMIR evidence, do not claim export/runtime/CLI integration, and do not add or imply a
third supported tuple.

## Parser/Header Report Admission

The parser/header report is admitted as evidence-only.

Admitted report-level facts from the external report:

| Field | Value |
| --- | --- |
| external parse result | `success` |
| header_size | `11190` |
| header_crc | `3547804793` |
| major_version | `868` |
| minor_version | `32` |
| net_version | `Some(10)` |
| game_type | `TAGame.Replay_Soccar_TA` |
| header_property_count | `27` |
| property_kind_counts | `Array=3; Bool=1; Float=3; Int=12; Name=2; QWord=1; Str=5` |

This is external parser evidence only. It is not MIMIR parser output and not fixture_003
parser-success evidence.

## Structural Report Admission

The structural report is admitted as evidence-only.

Cross-checks against the parser/header report passed:

| Field | Parser/header report | Structural report | Status |
| --- | --- | --- | --- |
| header_size | `11190` | `11190` | match |
| header_crc | `3547804793` | `3547804793` | match |
| major_version | `868` | `868` | match |
| minor_version | `32` | `32` | match |
| net_version | `Some(10)` | `Some(10)` | match |
| game_type | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` | match |
| property count | `27` | `27` | match |
| property kind counts | `Array=3; Bool=1; Float=3; Int=12; Name=2; QWord=1; Str=5` | `Array=3; Bool=1; Float=3; Int=12; Name=2; QWord=1; Str=5` | match |

Structural boundary checks:

- header data range candidate: `[8, 11198)`
- header data end formula: `8 + 11190 = 11198`
- property table start candidate: `48`
- terminator key offset: `11189`
- terminator end offset: `11198`
- terminator matches header end: `true`
- content_size candidate: offset `11198`, value `1627332`
- content_crc candidate: offset `11202`, value `3991282011`
- content data start candidate: `11206`

The content boundary fields are admitted only as first body boundary candidates from external
structural/report evidence. They are not MIMIR parser evidence. CRC validation remains closed.

## Selected Property Candidate Evidence

The following selected values are admitted only as external/report candidate evidence for a later
mapping/error-boundary pass:

| Candidate field | Candidate value |
| --- | --- |
| replay_id candidate from `Id` | `DF72482811F0B757082C458D84251EFF` |
| source_label candidate | `rl_replay_header_fixture_003` |
| total_frames candidate from `NumFrames` | `8288` |
| `ReplayName` | `Text("asdasd")` |
| `Date` | `Text("2025-11-01 19-20-48")` |
| `MapName` | `Text("cs_day_p")` |
| `ReplayVersion` | `Integer(8)` |
| `BuildVersion` | `Text("251020.62592.500294")` |
| `MaxChannels` | `Integer(2047)` |
| `MatchType` | `Text("Online")` |
| `TeamSize` | `Integer(2)` |
| `RecordFPS` | `Float(30.0)` |

These values are not admitted as MIMIR parser output. Full `ReplayHeader` output for fixture_003 is
not admitted. Parser-success for fixture_003 is not admitted.

## Structural Byte-Layout Candidate Evidence

The following are admitted only as external structural/report evidence:

- `header_size` offset/value candidate: offset `0`, `11190`
- `header_crc` offset/value candidate: offset `4`, `3547804793`
- header data range candidate: `[8, 11198)`
- version/game_type offset/value candidates:
  - `major_version`: offset `8`, value `868`
  - `minor_version`: offset `12`, value `32`
  - `net_version`: offset `16`, value `Some(10)`
  - `game_type`: offset `20`, value `TAGame.Replay_Soccar_TA`
- property table start candidate: `48`
- top-level property count candidate: `27`
- selected property routes and ranges from the structural report
- top-level `BoolProperty` route as report evidence only
- terminator offset/end/matches-header-end candidate: `11189` / `11198` / `true`
- first body boundary candidates:
  - `content_size`: offset `11198`, value `1627332`
  - `content_crc`: offset `11202`, value `3991282011`
  - `content_data_start`: `11206`

No body, raw-state, frame, or event parsing is admitted.

## BoolProperty Evidence Treatment

Fixture_003 contains top-level `bForfeit`:

- structural path: `header.properties[1]`
- kind: `BoolProperty`
- byte range: `[89,128)`
- declared size: `0`
- scanner consumed: `1`
- generated value summary: `true`

This is admitted as external report evidence only.

It is not admitted as MIMIR parser support. Code inspection showed that the current MIMIR parser
does not include `BoolProperty` in admitted property kinds and still supports only the existing
minimal selected/non-selected property boundary. No parser behavior was changed in this pass.

## Fixture 001/002/003 Implications

Report-level comparison:

| Field | fixture_001 | fixture_002 | fixture_003 |
| --- | --- | --- | --- |
| major_version | `868` | `868` | `868` |
| minor_version | `32` | `32` | `32` |
| net_version | `Some(10)` | `Some(10)` | `Some(10)` |
| game_type | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` |
| ReplayVersion | `8` | `8` | `8` |
| BuildVersion | `241206.55345.468477` | `250811.43331.492665` | `251020.62592.500294` |

Fixture_003 appears structurally similar at report level, but its `BuildVersion` differs from both
currently admitted exact tuples. Fixture_003 also contains a top-level `BoolProperty` not admitted
by the current MIMIR parser boundary.

The current admitted `MinimalReplayHeaderReader` policy does not support fixture_003. Future
fixture_003 support requires a separate mapping/error-boundary admission and explicit
supported-version policy planning/implementation reopen.

## Explicit Non-Claims

This pass does not claim:

- MIMIR parser success for fixture_003
- broad parser success
- fixture_003 support in `MinimalReplayHeaderReader`
- a third supported tuple
- broad version-family support
- broad `ReplayVersion = 8` support
- wildcard `BuildVersion` support
- future unknown build support
- `ReplayHeader` mapping for fixture_003 as MIMIR parser output
- `ReplayInput::File` support
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- `content_crc` read or validation in MIMIR parser code
- body parsing
- raw-state parsing
- frame parsing
- event parsing
- export integration
- runtime integration
- CLI integration
- backend replay parser dependency in MIMIR

## What Remains Closed

Still closed after this pass:

- parser code changes
- `MinimalReplayHeaderReader` changes
- fixture_003 parser-success admission
- fixture_003 supported-version policy admission
- third supported tuple addition
- broad parser-success admission
- parser expansion for `BoolProperty`
- `ReplayInput::File`
- replay-source materialization
- CRC validation and `content_crc`
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Next Stage

Outcome A next stage:

- next pass may be fixture_003 mapping/error-boundary admission
- no parser expansion yet
- no export/runtime/CLI integration yet
- no broad parser-success admission yet
