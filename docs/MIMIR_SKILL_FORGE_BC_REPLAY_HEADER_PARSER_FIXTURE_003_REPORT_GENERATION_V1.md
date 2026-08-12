# MIMIR Skill Forge BC Replay Header Parser Fixture 003 Report Generation V1

Pass date: 2026-05-05

## Purpose

Generate bounded external fixture_003 header and structural evidence for a later admission pass.

This is a report-generation and evidence-readiness pass only. It does not implement parser code,
does not run the MIMIR parser as proof of fixture_003 support, does not admit parser success for
fixture_003, and does not broaden the current minimal replay parser boundary.

## Selected Outcome

Selected outcome:

- Outcome A

A bounded external report route was available and successfully generated fixture_003 report
artifacts. The generated reports are evidence-only and require a later fixture_003 report admission
pass.

## Re-Audited Inputs

Inspected directly before report generation:

- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_intake_readiness_status.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_intake_readiness_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_intake_readiness_next.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_INTAKE_READINESS_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_exact_supported_tuple_implementation_audit_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_AUDIT_V1.md`
- `crates/mimir-replay/README.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

The re-audit confirmed that `MinimalReplayHeaderReader` remains an exact two-tuple allowlist for
fixture_001 and fixture_002 only. No third supported tuple was present before this pass.

## Fixture 001 Identity Confirmation

Fixture_001 was reverified directly:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| first four bytes as little-endian i32 | `13200` |
| extension | `.replay` |
| byte length greater than 8 | yes |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

## Fixture 002 Identity Confirmation

Fixture_002 was reverified directly:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_002` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` |
| byte length | `2632903` |
| SHA-256 | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` |
| first four bytes as little-endian i32 | `11273` |
| extension | `.replay` |
| byte length greater than 8 | yes |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

## Fixture 003 Identity Confirmation

Fixture_003 was reverified directly:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_003` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay` |
| byte length | `1638538` |
| SHA-256 | `20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC` |
| first four bytes as little-endian i32 | `11190` |
| extension | `.replay` |
| byte length greater than 8 | yes |
| differs from fixture_001 by SHA-256 | yes |
| differs from fixture_002 by SHA-256 | yes |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

Fixture identity remains file identity evidence only. Path, filename, byte length, hash, and
fixture id are not parser facts.

## External Tool Route

The report route used a temporary external Rust crate outside the MIMIR workspace/dependency graph:

- external tool path: `D:\Temp\mimir_fixture_003_header_report_v1`
- external tool name/version: `mimir_fixture_003_header_report_v1` / `0.1.0`
- external parser dependency: `boxcars 0.11.1`
- external parser mode: `ParserBuilder::new(bytes).never_parse_network_data().parse()`
- structural scanner: external Rust scanner reading fixture bytes for header offsets, top-level
  property boundaries, nested header property boundary consumption where needed, and first body
  size/CRC boundary candidates

The external tool hard-checked fixture_003 byte length and SHA-256 before writing reports.

The copied fixture_002 structural scanner initially failed on fixture_003 because fixture_003 has a
top-level `BoolProperty` whose declared property size is not the number of bytes consumed. The
external scanner was narrowed outside MIMIR to consume header property values by the same
kind-specific boundary route documented from `boxcars` header parsing. This change was confined to
`D:\Temp\mimir_fixture_003_header_report_v1` and did not modify MIMIR source, manifests, lockfile,
or dependencies.

## Generated Reports

| Path | Size |
| --- | ---: |
| `artifacts/replay_header_reports/rl_replay_header_fixture_003_report.txt` | `4167` bytes |
| `artifacts/replay_header_reports/rl_replay_header_fixture_003_structural_report.txt` | `21787` bytes |

Both reports explicitly state that they are generated outside MIMIR, are not MIMIR parser output,
are not fixture_003 parser-success evidence, are not broad parser support, and do not claim
body/raw-state/frame/event parsing or export/runtime/CLI integration.

## Evidence Summary

External parser/tool report evidence for fixture_003:

| Field | Reported value |
| --- | --- |
| external boxcars parse result | success |
| header_size | `11190` |
| header_crc | `3547804793` |
| major_version | `868` |
| minor_version | `32` |
| net_version | `Some(10)` |
| game_type | `TAGame.Replay_Soccar_TA` |
| header_property_count | `27` |
| property_kind_counts | `Array=3; Bool=1; Float=3; Int=12; Name=2; QWord=1; Str=5` |
| Id | `DF72482811F0B757082C458D84251EFF` |
| ReplayName | `asdasd` |
| Date | `2025-11-01 19-20-48` |
| MapName | `cs_day_p` |
| ReplayVersion | `8` |
| BuildVersion | `251020.62592.500294` |
| NumFrames | `8288` |
| MaxChannels | `2047` |
| MatchType | `Online` |
| TeamSize | `2` |
| RecordFPS | `30.0` |

Structural report evidence for fixture_003:

| Field | Reported value |
| --- | --- |
| header_size offset/encoding | offset `0`, `i32_little_endian` |
| header_crc offset/encoding | offset `4`, `u32_little_endian` |
| header data range candidate | `[8, 11198)` |
| major/minor/net offsets | `8`, `12`, `16` |
| game_type offset | `20` |
| property table start | `48` |
| top-level property count | `27` |
| top-level property kind counts | `Array=3; Bool=1; Float=3; Int=12; Name=2; QWord=1; Str=5` |
| terminator offset/end | offset `11189`, end `11198` |
| terminator matches header end | `true` |
| content_size candidate | offset `11198`, value `1627332` |
| content_crc candidate | offset `11202`, value `3991282011` |
| content data start candidate | `11206` |

Body/footer fields in the external parser report are diagnostic-only and are not admitted as MIMIR
header evidence in this pass.

## Fixture 001/002/003 Report-Level Comparison

| Field | fixture_001 | fixture_002 | fixture_003 | Report-level comparison |
| --- | ---: | ---: | ---: | --- |
| byte length | `3001021` | `2632903` | `1638538` | fixture_003 is `1362483` bytes shorter than fixture_001 and `994365` bytes shorter than fixture_002 |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` | `20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC` | all different |
| first four bytes/header_size sanity | `13200` | `11273` | `11190` | fixture_003 header is `2010` bytes smaller than fixture_001 and `83` bytes smaller than fixture_002 |
| major_version | `868` | `868` | `868` | same |
| minor_version | `32` | `32` | `32` | same |
| net_version | `Some(10)` | `Some(10)` | `Some(10)` | same |
| game_type | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` | same |
| property count | `26` | `27` | `27` | fixture_003 matches fixture_002 count and has one more top-level property than fixture_001 |
| property kind counts | `Array=3; Float=3; Int=12; Name=2; QWord=1; Str=5` | `Array=3; Float=3; Int=13; Name=2; QWord=1; Str=5` | `Array=3; Bool=1; Float=3; Int=12; Name=2; QWord=1; Str=5` | fixture_003 includes one top-level Bool property and one fewer Int than fixture_002 |
| BuildVersion | `241206.55345.468477` | `250811.43331.492665` | `251020.62592.500294` | all different |
| selected key availability | all 11 selected keys present | all 11 selected keys present | all 11 selected keys present | same selected-key availability |

Report-level structural assessment:

- fixture_003 appears structurally similar to fixture_001 and fixture_002 at the top-level header
  layout level.
- fixture_003 is not admitted as supported by MIMIR.
- fixture_003 `BuildVersion` differs from both currently admitted exact tuples.
- fixture_003 has a top-level `BoolProperty` (`bForfeit`) that is external report evidence only and
  is not a MIMIR parser support claim.
- no parser expansion is admitted by this comparison.

## Explicit Non-Claims

This pass does not claim:

- MIMIR parser success for fixture_003
- broad parser success
- supported replay version for fixture_003
- fixture_003 `ReplayHeader` output as MIMIR parser output
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

- parser expansion for fixture_003
- parser-success admission for fixture_003
- broad version-family support
- replay-source materialization
- `ReplayInput::File`
- CRC validation and `content_crc`
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Next Stage

Outcome A next stage:

- next pass must be fixture_003 report admission
- no parser expansion yet
- no export/runtime/CLI integration yet
- no broad parser-success admission yet
