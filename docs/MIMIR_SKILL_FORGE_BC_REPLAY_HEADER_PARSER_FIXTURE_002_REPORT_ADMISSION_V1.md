# MIMIR Skill Forge BC Replay Header Parser Fixture 002 Report Admission v1

Pass date: 2026-05-04

## Purpose

Admit or reject the generated fixture_002 external parser/header report and structural report as
evidence-only inputs.

This is a report admission pass only. It does not implement parser code, run the MIMIR parser as
proof of fixture_002 support, broaden supported-version policy, add replay file input support, add
CRC validation, parse body/raw-state/frame/event data, or wire export/runtime/CLI behavior.

## Selected Outcome

Selected outcome:

- Outcome A

The fixture_002 external parser/header report is admitted as evidence-only. The fixture_002
external structural report is admitted as evidence-only. Selected property evidence is admitted
only as candidate mapping evidence, and byte-layout evidence is admitted only as external
structural/report evidence.

No MIMIR parser-success is claimed for fixture_002. No broad parser-success is admitted.

## Fixture Identity Verification

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

Fixture_002 was reverified directly:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_002` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` |
| byte length | `2632903` |
| SHA-256 | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` |
| first four bytes as little-endian i32 | `11273` |
| differs from fixture_001 by SHA-256 | yes |
| extension | `.replay` |
| byte length greater than 8 | yes |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

Fixture path, filename, byte length, hash, fixture id, provenance, and artifact id remain fixture
identity facts only. They are not parser facts.

## Report File Verification

Generated report files were rechecked:

| Path | Current size | Admission result |
| --- | ---: | --- |
| `artifacts/replay_header_reports/rl_replay_header_fixture_002_report.txt` | `4167` bytes | admitted as external parser/header evidence-only |
| `artifacts/replay_header_reports/rl_replay_header_fixture_002_structural_report.txt` | `13885` bytes | admitted as external structural/report evidence-only |

Both reports identify `rl_replay_header_fixture_002`, the fixture_002 path, byte length
`2632903`, SHA-256 `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6`, and
admission form `PRIVATE_LOCAL_PATH_WITH_HASH`.

Both reports state that they were generated outside MIMIR, are not MIMIR parser output, are not
parser-success evidence, do not admit fixture_002 MIMIR parser success, do not admit broad parser
success, do not claim body/raw-state/frame/event parsing as MIMIR evidence, and do not claim
export/runtime/CLI integration.

## Parser/Header Report Admission

The parser/header report is admitted only as external/report evidence:

| Field | Admitted external/report value |
| --- | --- |
| external boxcars parse result | `success` |
| header_size | `11273` |
| header_crc | `3202895499` |
| major_version | `868` |
| minor_version | `32` |
| net_version | `Some(10)` |
| game_type | `TAGame.Replay_Soccar_TA` |
| header_property_count | `27` |
| property_kind_counts | `Array=3; Float=3; Int=13; Name=2; QWord=1; Str=5` |

The report's external parser success is not MIMIR parser success. It does not prove
`MinimalReplayHeaderReader` support for fixture_002.

## Structural Report Admission

The structural report is admitted only as external structural/report evidence:

| Field | Admitted external/report candidate |
| --- | --- |
| header_size offset/value | offset `0`, `11273`, `i32_little_endian` |
| header_crc offset/value | offset `4`, `3202895499`, `u32_little_endian` |
| header data range | `[8, 11281)` |
| major_version offset/value | offset `8`, `868` |
| minor_version offset/value | offset `12`, `32` |
| net_version offset/value | offset `16`, `Some(10)` |
| game_type offset/value | offset `20`, `TAGame.Replay_Soccar_TA` |
| property table start | offset `48` |
| top-level property count | `27` |
| top-level property kind counts | `Array=3; Float=3; Int=13; Name=2; QWord=1; Str=5` |
| terminator offset/end | offset `11272`, end `11281` |
| terminator matches header end | `true` |
| content_size first body boundary candidate | offset `11281`, value `2621614` |
| content_crc first body boundary candidate | offset `11285`, value `3734167123` |
| content data start candidate | offset `11289` |

The calculated header data end is `8 + 11273 = 11281`, matching the structural report terminator
end. `content_size`, `content_crc`, and `content_data_start` are admitted only as first body
boundary candidates from the external structural report. They are not MIMIR parser evidence, and
CRC validation remains closed.

## Cross-Report Consistency

The parser/header report and structural report agree on:

- fixture id, path, byte length, SHA-256, and admission form
- `header_size = 11273`
- `header_crc = 3202895499`
- `major_version = 868`
- `minor_version = 32`
- `net_version = Some(10)`
- `game_type = TAGame.Replay_Soccar_TA`
- `header_property_count = 27`
- property kind counts: `Array=3; Float=3; Int=13; Name=2; QWord=1; Str=5`
- selected property values listed below

The property kind count formatting differs only by presentation: the parser/header report uses a
JSON-like map, while the structural report uses `Array=3; Float=3; Int=13; Name=2; QWord=1;
Str=5`. The counts are semantically identical.

## Selected Property Candidate Evidence

The following values are admitted only as external/report candidate mapping evidence:

| Candidate field | External/report candidate value |
| --- | --- |
| replay_id candidate from `Id` | `D9DA34DA11F0811EAC139A94CBF30AF2` |
| source_label candidate | `rl_replay_header_fixture_002` |
| total_frames candidate from `NumFrames` | `10351` |
| `ReplayName` | `Text("asdasd")` |
| `Date` | `Text("2025-08-24 19-16-35")` |
| `MapName` | `Text("NeoTokyo_Standard_P")` |
| `ReplayVersion` | `Integer(8)` |
| `BuildVersion` | `Text("250811.43331.492665")` |
| `MaxChannels` | `Integer(2047)` |
| `MatchType` | `Text("Online")` |
| `TeamSize` | `Integer(3)` |
| `RecordFPS` | `Float(30.0)` |

These values are not admitted as MIMIR parser output. Full `ReplayHeader` output for fixture_002 is
not admitted in this pass.

## Structural Byte-Layout Candidate Evidence

The following structural byte-layout evidence is admitted only as external/report candidate
evidence for later mapping/error-boundary work:

- `header_size` offset/value candidate
- `header_crc` offset/value candidate
- header data range candidate `[8, 11281)`
- version and game_type offset/value candidates
- property table start candidate `48`
- top-level property count candidate `27`
- selected property routes and value ranges from the structural table
- terminator offset/end/matches-header-end candidate
- first body boundary candidates for `content_size`, `content_crc`, and `content_data_start`

The first body boundary candidates do not admit MIMIR body parsing, MIMIR `content_crc` reads,
MIMIR `content_crc` validation, or CRC validation policy.

## Fixture 001 vs Fixture 002 Implications

Report-level comparison:

| Field | fixture_001 | fixture_002 | Implication |
| --- | ---: | ---: | --- |
| byte length | `3001021` | `2632903` | different files |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` | different files |
| first four bytes as little-endian i32 | `13200` | `11273` | different header_size sanity values |
| major_version | `868` | `868` | same at report level |
| minor_version | `32` | `32` | same at report level |
| net_version | `Some(10)` | `Some(10)` | same at report level |
| game_type | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` | same at report level |
| ReplayVersion | `8` | `8` | same at report level |
| BuildVersion | `241206.55345.468477` | `250811.43331.492665` | different supported tuple component |

Fixture_002 appears structurally similar at report level, but the current admitted
`MinimalReplayHeaderReader` policy is still fixture_001-only because it requires the exact
supported tuple with `BuildVersion = 241206.55345.468477`. Fixture_002 has
`BuildVersion = 250811.43331.492665`, so fixture_002 is not admitted as supported by
`MinimalReplayHeaderReader`.

Any future fixture_002 support requires a separate version-policy or implementation-planning reopen.

## Explicit Non-Claims

This pass does not claim:

- MIMIR parser success for fixture_002
- broad parser success
- fixture_002 support by `MinimalReplayHeaderReader`
- supported replay version policy for fixture_002
- broad version-family support
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

- parser code changes
- parser behavior changes
- parser expansion for fixture_002
- parser-success admission for fixture_002
- broad parser-success admission
- fixture_002 supported-version policy
- `ReplayInput::File`
- replay-source materialization
- CRC validation
- MIMIR `content_crc` read or validation
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Next Stage

Outcome A next stage:

- next pass may be fixture_002 mapping/error-boundary admission, preferably before supported-version
  policy planning
- a later pass may instead perform fixture_002 supported-version policy planning if explicitly
  reopened
- no parser expansion yet
- no export/runtime/CLI integration yet
- no broad parser-success admission yet
