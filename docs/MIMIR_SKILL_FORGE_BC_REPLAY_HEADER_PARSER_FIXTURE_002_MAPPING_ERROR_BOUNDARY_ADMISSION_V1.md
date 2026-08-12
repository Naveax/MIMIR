# MIMIR Skill Forge BC Replay Header Parser Fixture 002 Mapping Error Boundary Admission v1

Pass date: 2026-05-04

## Purpose

Admit, reject, or defer `rl_replay_header_fixture_002` selected `ReplayHeader` mapping candidates
and mapping/error-boundary policies from already admitted external/report evidence.

This is a docs/artifacts-only policy and evidence admission pass. It does not implement parser
code, modify `MinimalReplayHeaderReader`, run the MIMIR parser as proof of fixture_002 support,
admit fixture_002 parser success, admit fixture_002 supported-version policy, broaden parser scope,
add file input support, add CRC validation, parse body/raw-state/frame/event data, or wire
export/runtime/CLI behavior.

## Selected Outcome

Selected outcome:

- Outcome A

Fixture_002 mapping/error-boundary admission is complete enough for the currently admitted
external/report evidence.

Selected fixture_002 field values are admitted only as candidate expected-output evidence for a
future explicitly reopened support pass. Mapping-specific missing, duplicate, wrong-kind,
malformed, empty, and conversion policies can carry over from the admitted fixture_001 mapping
policy as candidate policy because they are tied to the same `ReplayHeader`, `ReplayId`,
`Metadata`, and `FieldValue` surfaces rather than to the fixture_001 BuildVersion.

No parser-success is claimed for fixture_002. No fixture_002 supported-version policy is admitted.
No broad parser-success or version-family support is admitted.

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

Path, filename, fixture id, artifact id, byte length, hash, and provenance remain fixture identity
facts only. They are not parser facts and are not sources for `ReplayHeader` fields.

## Evidence Inputs

Re-audited evidence inputs:

- `artifacts/replay_header_reports/rl_replay_header_fixture_002_report.txt`
- `artifacts/replay_header_reports/rl_replay_header_fixture_002_structural_report.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_REPORT_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_report_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_report_admission_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_report_admission_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_REPORT_GENERATION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_INTAKE_READINESS_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_MIMIR_SKILL_SEAM_IMPLEMENTATION_AUDIT_V1.md`
- `crates/mimir-replay/README.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

Fixture_001 mapping/error-boundary inputs inspected:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REPLAYHEADER_MAPPING_POLICY_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_replayheader_mapping_policy_admission_decision.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_MAPPING_GAP_ERROR_BOUNDARY_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_remaining_mapping_gap_error_boundary_admission_decision.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_NON_MAPPING_BYTE_LAYOUT_ERROR_BOUNDARY_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_remaining_non_mapping_byte_layout_error_boundary_admission_decision.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_PRE_IMPLEMENTATION_GAP_CLOSURE_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_pre_implementation_gap_closure_decision.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIRST_MINIMAL_IMPLEMENTATION_V1.md`

Evidence input status:

- fixture_002 parser/header report is admitted as external parser/header evidence-only
- fixture_002 structural report is admitted as external structural/report evidence-only
- selected property routes are admitted only as candidate mapping evidence
- structural byte-layout values are admitted only as external/report structural evidence
- neither report is MIMIR parser output
- neither report is fixture_002 MIMIR parser-success evidence

## Mapping Policy Carryover Analysis

Source/type surfaces inspected:

- `ReplayHeader` fields in `crates/mimir-replay/src/lib.rs`:
  - `replay_id: ReplayId`
  - `source_label: String`
  - `total_frames: Option<u32>`
  - `metadata: Metadata`
- `ReplayId` in `crates/mimir-types/src/lib.rs` is a transparent string newtype created by
  `ReplayId::new(...)`.
- `Metadata` is a deterministic `BTreeMap<String, FieldValue>` wrapper.
- `FieldValue` selected carriers remain:
  - `Text(String)`
  - `Integer(i64)`
  - finite `Float(f64)`

Carryover accepted as candidate mapping policy only:

| Policy | Carryover result |
| --- | --- |
| `Id -> ReplayHeader.replay_id` | accepted as candidate policy for fixture_002 selected-field expected evidence |
| `ReplayInput::Memory.label -> ReplayHeader.source_label` | accepted for a future admitted memory-input boundary; fixture_002 label candidate is not a parser fact |
| `NumFrames -> ReplayHeader.total_frames` | accepted as candidate policy for present non-negative `Int` and mapped `None`/hard-error boundaries |
| selected same-name metadata keys | accepted for the same selected key set |
| `Str`/`Name -> FieldValue::Text` | accepted for selected metadata |
| `Int -> FieldValue::Integer` | accepted for selected metadata |
| finite `Float -> FieldValue::Float` | accepted for selected metadata |

Carryover explicitly not accepted:

- fixture_001 exact supported-version tuple
- fixture_001 BuildVersion support
- broad version-family support
- parser-success behavior for fixture_002
- broad parser behavior from fixture_001 tests
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- body/raw-state/frame/event parsing
- export/runtime/CLI integration

The current `MinimalReplayHeaderReader` source still uses the fixture_001 exact supported
BuildVersion `241206.55345.468477`. Fixture_002 report evidence has BuildVersion
`250811.43331.492665`. Therefore fixture_002 remains unsupported by `MinimalReplayHeaderReader`.

## Fixture 002 ReplayHeader Candidate Expected-Output Evidence

The following selected fields are admitted only as candidate expected-output evidence. They are not
MIMIR parser output and are not a parser-success claim.

| `ReplayHeader` field | Candidate expected evidence |
| --- | --- |
| `replay_id` | `ReplayId::new("D9DA34DA11F0811EAC139A94CBF30AF2")` |
| `source_label` | `"rl_replay_header_fixture_002"` |
| `total_frames` | `Some(10351)` |
| `metadata.ReplayName` | `FieldValue::Text("asdasd")` |
| `metadata.Date` | `FieldValue::Text("2025-08-24 19-16-35")` |
| `metadata.MapName` | `FieldValue::Text("NeoTokyo_Standard_P")` |
| `metadata.ReplayVersion` | `FieldValue::Integer(8)` |
| `metadata.BuildVersion` | `FieldValue::Text("250811.43331.492665")` |
| `metadata.MaxChannels` | `FieldValue::Integer(2047)` |
| `metadata.MatchType` | `FieldValue::Text("Online")` |
| `metadata.TeamSize` | `FieldValue::Integer(3)` |
| `metadata.RecordFPS` | `FieldValue::Float(30.0)` |

This evidence may be used later as expected candidate output only if fixture_002 support is
explicitly reopened through a supported-version policy and implementation planning pass.

## Replay Id Policy Status

Policy status:

- admitted as candidate mapping/error-boundary policy for fixture_002 expected evidence
- not admitted as fixture_002 MIMIR parser behavior

Fixture_002 `Id` candidate:

| Field | Value |
| --- | --- |
| key | `Id` |
| structural path | `header.properties[21]` |
| kind | `StrProperty` |
| value range | `[10950,10987)` |
| value | `D9DA34DA11F0811EAC139A94CBF30AF2` |
| shape | exactly 32 ASCII hexadecimal digits |

Admitted candidate policy:

- exactly one top-level `Id` property is required for `ReplayHeader.replay_id`
- required kind is `Str`
- value must be non-empty and exactly 32 ASCII hexadecimal digits
- source case is preserved; no uppercase normalization is admitted
- lowercase ASCII hex remains valid under the admitted ASCII-hex policy
- non-ASCII, non-hex, overlength, underlength, empty, or otherwise malformed `Id` is a hard
  replay-header mapping error
- missing `Id` is a hard replay-header mapping error
- duplicate `Id` is a hard replay-header mapping error; first/last selection is forbidden
- wrong-kind `Id` is a hard replay-header mapping error
- no fallback to `MatchGUID`, fixture id, path, filename, hash, or provenance is admitted

## Total Frames Policy Status

Policy status:

- admitted as candidate mapping/error-boundary policy for fixture_002 expected evidence
- not admitted as fixture_002 MIMIR parser behavior

Fixture_002 `NumFrames` candidate:

| Field | Value |
| --- | --- |
| key | `NumFrames` |
| structural path | `header.properties[25]` |
| kind | `IntProperty` |
| source type | signed `i32` |
| value range | `[11218,11222)` |
| value | `10351` |

Admitted candidate policy:

- present `NumFrames` with kind `Int` and value `>= 0` maps to `Some(value as u32)`
- fixture_002 candidate maps to `Some(10351)`
- missing `NumFrames` maps to `None`
- duplicate `NumFrames` is a hard replay-header mapping error
- wrong-kind `NumFrames` is a hard replay-header mapping error and is not treated as missing
- negative `NumFrames` is a hard replay-header mapping error; no signed-to-unsigned wrap, clamp,
  or saturation is admitted
- malformed `NumFrames` bytes are a hard malformed-property error
- overflow beyond `u32::MAX` is impossible for the admitted signed `i32` source; any different
  source shape remains unadmitted
- no total-frame derivation from body frame extraction, footer/body counts, byte length, or
  external parser success is admitted

## Metadata Policy Status

Policy status:

- admitted as candidate mapping/error-boundary policy for fixture_002 expected evidence
- not admitted as fixture_002 MIMIR parser behavior

Selected same-name metadata candidates:

| Metadata key | Source kind | Candidate `FieldValue` |
| --- | --- | --- |
| `ReplayName` | `Str` | `Text("asdasd")` |
| `Date` | `Str` | `Text("2025-08-24 19-16-35")` |
| `MapName` | `Name` | `Text("NeoTokyo_Standard_P")` |
| `ReplayVersion` | `Int` | `Integer(8)` |
| `BuildVersion` | `Str` | `Text("250811.43331.492665")` |
| `MaxChannels` | `Int` | `Integer(2047)` |
| `MatchType` | `Name` | `Text("Online")` |
| `TeamSize` | `Int` | `Integer(3)` |
| `RecordFPS` | `Float` | `Float(30.0)` |

Admitted candidate policy:

- destination metadata keys use the same case-sensitive selected property names
- no key normalization or renaming is admitted
- selected `Str` and `Name` values map to `FieldValue::Text`
- selected `Int` values map to `FieldValue::Integer`
- selected finite `Float` values map to `FieldValue::Float`
- selected missing key omits that metadata entry
- all selected keys missing yields `Metadata::new()`
- duplicate selected key is a hard replay-header mapping error; silent `BTreeMap` overwrite is
  forbidden
- wrong-kind selected key is a hard replay-header mapping error
- malformed selected value is a hard malformed-property error
- empty selected string/name is preserved as empty `FieldValue::Text(String::new())`
- non-finite selected float is a hard replay-header mapping error
- arrays, body/footer data, raw-state payloads, replay frames, semantic events, and non-selected
  properties are excluded from `ReplayHeader.metadata`
- date/time parsing, map-name normalization, and BuildVersion semantic interpretation remain
  closed

## Structural And Error-Boundary Policy Status

Structural/error-boundary status:

- partial overall
- admitted only as external/report structural candidate evidence for fixture_002
- not admitted as fixture_002 MIMIR parser behavior

Admitted fixture_002 external/report structural candidates:

| Target | Candidate evidence |
| --- | --- |
| `header_size` | offset `0`, `i32_little_endian`, value `11273` |
| `header_crc` | offset `4`, `u32_little_endian`, value `3202895499` |
| header data range | `[8, 11281)` |
| `major_version` | offset `8`, value `868` |
| `minor_version` | offset `12`, value `32` |
| `net_version` | offset `16`, value `Some(10)` |
| `game_type` | offset `20`, value `TAGame.Replay_Soccar_TA` |
| property table start | offset `48` |
| top-level property count | `27` |
| property kind counts | `Array=3; Float=3; Int=13; Name=2; QWord=1; Str=5` |
| terminator offset/end | `11272` / `11281` |
| terminator matches header end | `true` |
| content_size first body boundary candidate | offset `11281`, value `2621614` |
| content_crc first body boundary candidate | offset `11285`, value `3734167123` |
| content data start candidate | offset `11289` |

Admitted candidate structural conclusions:

- `header_size` is positive for the fixture_002 report evidence
- candidate `header_end` is `8 + 11273 = 11281`
- candidate property terminator end equals candidate header end
- selected property routes exist in the external structural table
- first body boundary values are report-only boundary candidates and are not MIMIR parser evidence

Not admitted:

- fixture_002 supported-version policy
- fixture_002 parser-success
- broad version-family support
- CRC validation
- MIMIR `content_crc` read or validation
- body/footer parsing
- raw-state parsing
- frame parsing
- event parsing

## Deferred Policies And Blockers

No selected-field mapping-specific blockers remain for this evidence-only admission pass.

Remaining blockers before any fixture_002 parser-support or implementation claim:

1. Fixture_002 supported-version policy is not admitted. The report-level tuple differs from the
   current exact fixture_001-supported tuple only at `BuildVersion = 250811.43331.492665`, and
   admitting that value requires a separate supported-version policy planning reopen.
2. Fixture_002 MIMIR parser behavior is unproven and intentionally not tested as proof here.
3. Fixture_002 structural evidence is external/report evidence only, not MIMIR parser evidence.
4. CRC validation remains closed; no header CRC or content CRC validation is admitted.
5. `content_crc` remains outside MIMIR parser code and must not be read or validated by this pass.
6. Body/raw-state/frame/event parsing remains closed.
7. `ReplayInput::File`, replay-source materialization, export integration, runtime integration, and
   CLI integration remain closed.

## Explicit Non-Claims

This pass does not claim:

- MIMIR parser success for fixture_002
- broad parser success
- fixture_002 support by `MinimalReplayHeaderReader`
- supported replay version policy for fixture_002
- broad version-family support
- fixture_002 `ReplayHeader` mapping as MIMIR parser output
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
- broad version-family support
- `ReplayInput::File`
- replay-source materialization
- CRC validation
- MIMIR `content_crc` read or validation
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Next Stage

Outcome A next stage:

- next pass may be fixture_002 supported-version policy planning reopen
- no parser implementation yet
- no parser expansion yet
- no export/runtime/CLI integration yet
- no broad parser-success admission yet

If the next pass does not reopen supported-version policy, it should remain docs/artifacts-only and
must target one of the explicitly closed blockers above without treating this admission as parser
support.
