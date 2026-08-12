# MIMIR Skill Forge BC Replay Header Parser Fixture 002 Report Generation v1

Pass date: 2026-05-04

## Purpose

Generate bounded external fixture_002 header and structural evidence for a later admission pass.

This is a report-generation and evidence-readiness pass only. It does not implement parser code,
does not run the MIMIR parser as proof of fixture_002 support, does not admit parser success for
fixture_002, and does not broaden the current minimal replay parser boundary.

## Selected Outcome

Selected outcome:

- Outcome A

A bounded external report route was available and successfully generated fixture_002 report
artifacts. The reports are evidence-only and require a later fixture_002 report admission pass.

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
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

## Fixture 002 Identity Confirmation

Fixture_002 was reverified directly:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_002` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` |
| byte length | `2632903` |
| SHA-256 | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` |
| differs from fixture_001 by SHA-256 | yes |
| first four bytes as little-endian i32 | `11273` |
| extension | `.replay` |
| byte length greater than 8 | yes |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

Fixture identity remains file identity evidence only. Path, filename, byte length, hash, and
fixture id are not parser facts.

## External Tool Route

The report route used a temporary external Rust crate outside the MIMIR workspace/dependency graph:

- external tool path: `D:\Temp\mimir_fixture_002_header_report_v1`
- external tool name/version: `mimir_fixture_002_header_report_v1` / `0.1.0`
- external parser dependency: `boxcars 0.11.1`
- external parser mode: `ParserBuilder::new(bytes).never_parse_network_data().parse()`
- structural scanner: external Rust scanner reading fixture bytes for header offsets and first
  body boundary candidates

The external tool hard-checked fixture_002 byte length and SHA-256 before writing reports.

This route did not add dependencies to MIMIR, did not modify MIMIR parser code, and did not modify
MIMIR manifests or lockfile.

## Generated Reports

| Path | Size |
| --- | ---: |
| `artifacts/replay_header_reports/rl_replay_header_fixture_002_report.txt` | `4167` bytes |
| `artifacts/replay_header_reports/rl_replay_header_fixture_002_structural_report.txt` | `13885` bytes |

Both reports explicitly state that they are generated outside MIMIR, are not MIMIR parser output,
are not fixture_002 parser-success evidence, are not broad parser support, and do not claim
body/raw-state/frame/event parsing or export/runtime/CLI integration.

## Evidence Summary

External parser/tool report evidence for fixture_002:

| Field | Reported value |
| --- | --- |
| external boxcars parse result | success |
| header_size | `11273` |
| header_crc | `3202895499` |
| major_version | `868` |
| minor_version | `32` |
| net_version | `Some(10)` |
| game_type | `TAGame.Replay_Soccar_TA` |
| header_property_count | `27` |
| property_kind_counts | `Array=3; Float=3; Int=13; Name=2; QWord=1; Str=5` |
| Id | `D9DA34DA11F0811EAC139A94CBF30AF2` |
| ReplayName | `asdasd` |
| Date | `2025-08-24 19-16-35` |
| MapName | `NeoTokyo_Standard_P` |
| ReplayVersion | `8` |
| BuildVersion | `250811.43331.492665` |
| NumFrames | `10351` |
| MaxChannels | `2047` |
| MatchType | `Online` |
| TeamSize | `3` |
| RecordFPS | `30.0` |

Structural report evidence for fixture_002:

| Field | Reported value |
| --- | --- |
| header_size offset/encoding | offset `0`, `i32_little_endian` |
| header_crc offset/encoding | offset `4`, `u32_little_endian` |
| header data range candidate | `[8, 11281)` |
| major/minor/net offsets | `8`, `12`, `16` |
| game_type offset | `20` |
| property table start | `48` |
| top-level property count | `27` |
| terminator offset/end | offset `11272`, end `11281` |
| terminator matches header end | `true` |
| content_size candidate | offset `11281`, value `2621614` |
| content_crc candidate | offset `11285`, value `3734167123` |
| content data start candidate | `11289` |

Body/footer fields in the external parser report are diagnostic-only and are not admitted as MIMIR
header evidence in this pass.

## Fixture 001 vs Fixture 002 Report-Level Comparison

| Field | fixture_001 | fixture_002 | Report-level comparison |
| --- | ---: | ---: | --- |
| byte length | `3001021` | `2632903` | fixture_002 is `368118` bytes shorter |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` | different |
| header_size | `13200` | `11273` | fixture_002 header is `1927` bytes smaller |
| major_version | `868` | `868` | same |
| minor_version | `32` | `32` | same |
| net_version | `Some(10)` | `Some(10)` | same |
| game_type | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` | same |
| property count | `26` | `27` | fixture_002 has one additional top-level property |
| property kind counts | `Array=3; Float=3; Int=12; Name=2; QWord=1; Str=5` | `Array=3; Float=3; Int=13; Name=2; QWord=1; Str=5` | fixture_002 has one additional Int property |
| BuildVersion | `241206.55345.468477` | `250811.43331.492665` | different |
| selected key availability | all 11 selected keys present | all 11 selected keys present | same selected-key availability |

Report-level structural assessment:

- fixture_002 appears structurally similar to fixture_001 at the header-layout/report level.
- fixture_002 is not admitted as supported by MIMIR.
- fixture_002 BuildVersion differs from the currently admitted fixture_001-supported tuple.
- no parser expansion is admitted by this comparison.

## Explicit Non-Claims

This pass does not claim:

- MIMIR parser success for fixture_002
- broad parser success
- supported replay version for fixture_002
- fixture_002 `ReplayHeader` output as MIMIR parser output
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

- parser expansion for fixture_002
- parser-success admission for fixture_002
- broad version-family support
- replay-source materialization
- `ReplayInput::File`
- CRC validation and `content_crc`
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Next Stage

Outcome A next stage:

- next pass must be fixture_002 report admission
- no parser expansion yet
- no export/runtime/CLI integration yet
- no broad parser-success admission yet
