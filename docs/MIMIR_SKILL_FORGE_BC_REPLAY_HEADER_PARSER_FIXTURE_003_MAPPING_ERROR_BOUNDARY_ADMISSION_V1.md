# MIMIR Skill Forge BC Replay Header Parser Fixture 003 Mapping Error Boundary Admission V1

Pass date: 2026-05-06

## Purpose

Admit, reject, or defer `rl_replay_header_fixture_003` selected `ReplayHeader` mapping candidates
and mapping/error-boundary policies from the already admitted external/report evidence.

This is a docs/artifacts-only policy and evidence admission pass. It does not implement parser
code, modify `MinimalReplayHeaderReader`, run the MIMIR parser as proof of fixture_003 support,
admit fixture_003 parser success, admit fixture_003 supported-version policy, broaden parser
scope, add file input support, add CRC validation, parse body/raw-state/frame/event data, or wire
export/runtime/CLI behavior.

## Selected Outcome

Selected outcome:

- Outcome A

Fixture_003 mapping/error-boundary admission is complete enough for the currently available
external/report evidence.

Selected fixture_003 field values are admitted only as candidate expected-output evidence for a
future explicitly reopened support pass. Mapping-specific missing, duplicate, wrong-kind,
malformed, empty, and conversion policies can carry over from the admitted fixture_001 and
fixture_002 mapping policies for the selected scalar `ReplayHeader` fields because they are tied to
the same `ReplayHeader`, `ReplayId`, `Metadata`, and `FieldValue` surfaces rather than to either
prior fixture BuildVersion.

`bForfeit` is classified as report-only evidence. It is excluded from the selected metadata
candidate output. BoolProperty to `FieldValue::Boolean` mapping remains closed and deferred to a
later explicit BoolProperty policy pass.

No parser-success is claimed for fixture_003. No fixture_003 supported-version policy is admitted.
No third supported tuple is added. No broad parser-success or version-family support is admitted.

## Fixture Identity Verification

Fixture identities were reverified directly from disk.

| Fixture | Path | Byte length | SHA-256 | First four bytes as LE i32 | Extension | > 8 bytes |
| --- | --- | ---: | --- | ---: | --- | --- |
| `rl_replay_header_fixture_001` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | `3001021` | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `13200` | `.replay` | yes |
| `rl_replay_header_fixture_002` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` | `2632903` | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` | `11273` | `.replay` | yes |
| `rl_replay_header_fixture_003` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay` | `1638538` | `20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC` | `11190` | `.replay` | yes |

Fixture_003 differs from fixture_001 by SHA-256: yes.

Fixture_003 differs from fixture_002 by SHA-256: yes.

These are fixture identity facts only. Path, filename, byte length, SHA-256, fixture id,
artifact id, and provenance are not parser facts and are not sources for `ReplayHeader` fields.

## Evidence Inputs

Re-audited before writing this artifact:

- `artifacts/replay_header_reports/rl_replay_header_fixture_003_report.txt`
- `artifacts/replay_header_reports/rl_replay_header_fixture_003_structural_report.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_REPORT_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_report_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_report_admission_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_report_admission_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_REPORT_GENERATION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_INTAKE_READINESS_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_AUDIT_V1.md`
- `crates/mimir-replay/README.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

Existing fixture_001 and fixture_002 mapping inputs inspected:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REPLAYHEADER_MAPPING_POLICY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_MAPPING_GAP_ERROR_BOUNDARY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_NON_MAPPING_BYTE_LAYOUT_ERROR_BOUNDARY_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_remaining_mapping_gap_error_boundary_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_remaining_mapping_gap_error_boundary_admission_status.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_remaining_non_mapping_byte_layout_error_boundary_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_remaining_non_mapping_byte_layout_error_boundary_admission_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_MAPPING_ERROR_BOUNDARY_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_mapping_error_boundary_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_mapping_error_boundary_admission_status.txt`

Evidence input status:

- fixture_003 parser/header report is admitted as external parser/header evidence-only
- fixture_003 structural report is admitted as external structural/report evidence-only
- selected property routes are admitted only as candidate mapping evidence
- structural byte-layout values are admitted only as external/report structural evidence
- neither report is MIMIR parser output
- neither report is fixture_003 MIMIR parser-success evidence

## Current MIMIR Boundary Inspection

Current `ReplayHeader` fields in `crates/mimir-replay/src/lib.rs`:

| Field | Type | Boundary relevance |
| --- | --- | --- |
| `replay_id` | `ReplayId` | transparent string newtype from `ReplayId::new(...)`; parser code separately checks 32 ASCII hex digits |
| `source_label` | `String` | current minimal reader preserves non-empty `ReplayInput::Memory.label` |
| `total_frames` | `Option<u32>` | current mapping can represent present non-negative `NumFrames` or missing `NumFrames` |
| `metadata` | `Metadata` | deterministic `BTreeMap<String, FieldValue>` wrapper |

Current `FieldValue` variants in `crates/mimir-types/src/lib.rs`:

- `Text(String)`
- `Integer(i64)`
- `Float(f64)` with finite serialization/deserialization constraint
- `Boolean(bool)`
- `StringList(Vec<String>)`

Current `MinimalReplayHeaderReader` boundary inspection:

- `ReplayInput::Memory` is the only parsing input path.
- `ReplayInput::File` remains `unsupported-input`.
- Supported BuildVersion constants remain only:
  - `241206.55345.468477`
  - `250811.43331.492665`
- No `251020.62592.500294` fixture_003 tuple exists.
- No third supported tuple exists.
- `BoolProperty` is not an admitted property kind in the parser boundary.
- The only `BoolProperty` occurrence in `crates/mimir-replay/src/lib.rs` is an unsupported
  property-kind test.
- `header_crc` is read as layout only and is not validated.
- `content_crc` is not read or validated.
- Body/raw-state/frame/event parsing remains absent.

## Mapping Policy Carryover Analysis

Carryover accepted as candidate mapping/error-boundary policy only:

| Policy | Carryover result |
| --- | --- |
| `Id -> ReplayHeader.replay_id` | accepted for fixture_003 selected candidate expected evidence |
| `ReplayInput::Memory.label -> ReplayHeader.source_label` | accepted only for a future admitted memory-input boundary; fixture_003 label candidate is not a parser fact |
| `NumFrames -> ReplayHeader.total_frames` | accepted for present non-negative `Int` and existing missing/error policies |
| selected same-name metadata keys | accepted for the same selected scalar key set |
| `Str` and `Name -> FieldValue::Text` | accepted for selected metadata |
| `Int -> FieldValue::Integer` | accepted for selected metadata |
| finite `Float -> FieldValue::Float` | accepted for selected metadata |

Carryover explicitly not accepted:

- fixture_001 supported-version tuple
- fixture_002 supported-version tuple
- fixture_003 supported-version policy
- parser-success behavior for fixture_003
- broad parser behavior from fixture_001 or fixture_002 tests
- broad `ReplayVersion = 8` support
- wildcard or family `BuildVersion` support
- BoolProperty parser support
- BoolProperty to `FieldValue::Boolean` mapping
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- body/raw-state/frame/event parsing
- export/runtime/CLI integration

Carryover status is partial because selected scalar mapping/error policies carry over, while
BoolProperty mapping and fixture_003 parser support do not.

## Fixture 003 ReplayHeader Candidate Expected-Output Evidence

The following selected fields are admitted only as candidate expected-output evidence. They are not
MIMIR parser output and are not a parser-success claim.

| `ReplayHeader` field | Candidate expected evidence |
| --- | --- |
| `replay_id` | `ReplayId::new("DF72482811F0B757082C458D84251EFF")` |
| `source_label` | `"rl_replay_header_fixture_003"` |
| `total_frames` | `Some(8288)` |
| `metadata.ReplayName` | `FieldValue::Text("asdasd")` |
| `metadata.Date` | `FieldValue::Text("2025-11-01 19-20-48")` |
| `metadata.MapName` | `FieldValue::Text("cs_day_p")` |
| `metadata.ReplayVersion` | `FieldValue::Integer(8)` |
| `metadata.BuildVersion` | `FieldValue::Text("251020.62592.500294")` |
| `metadata.MaxChannels` | `FieldValue::Integer(2047)` |
| `metadata.MatchType` | `FieldValue::Text("Online")` |
| `metadata.TeamSize` | `FieldValue::Integer(2)` |
| `metadata.RecordFPS` | `FieldValue::Float(30.0)` |

This evidence may be used later as expected candidate output only if fixture_003 support is
explicitly reopened through supported-version policy planning and implementation planning.

No complete MIMIR parser `ReplayHeader` output is admitted by this table.

## BoolProperty bForfeit Policy Status

Status:

- report-only

External/report evidence for `bForfeit`:

| Field | Value |
| --- | --- |
| key | `bForfeit` |
| structural path | `header.properties[1]` |
| kind | `BoolProperty` |
| byte range | `[89,128)` |
| declared size | `0` |
| scanner consumed | `1` |
| generated value summary | `true` |

Admission decision:

- `bForfeit` is admitted only as external report evidence.
- `bForfeit` is excluded from fixture_003 selected metadata candidate output.
- `bForfeit` absence from selected expected metadata is not data loss. It is a deliberately closed
  mapping boundary.
- `FieldValue::Boolean(bool)` exists in `mimir-types`, but no prior replay-header mapping policy
  admits `BoolProperty -> FieldValue::Boolean`.
- No BoolProperty parser support is admitted.
- No BoolProperty skip policy is admitted for fixture_003 parser success.
- A later BoolProperty policy pass must decide whether to reject, skip, or map top-level
  BoolProperty values before any parser implementation can honestly claim fixture_003 support.

## Replay Id Policy Status

Policy status:

- admitted as candidate mapping/error-boundary policy only
- not admitted as fixture_003 MIMIR parser behavior

Fixture_003 `Id` candidate:

| Field | Value |
| --- | --- |
| key | `Id` |
| structural path | `header.properties[21]` |
| kind | `StrProperty` |
| value range | `[10878,10915)` |
| value | `DF72482811F0B757082C458D84251EFF` |
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

- admitted as candidate mapping/error-boundary policy only
- not admitted as fixture_003 MIMIR parser behavior

Fixture_003 `NumFrames` candidate:

| Field | Value |
| --- | --- |
| key | `NumFrames` |
| structural path | `header.properties[25]` |
| kind | `IntProperty` |
| source type | signed `i32` |
| value range | `[11135,11139)` |
| value | `8288` |

Admitted candidate policy:

- present `NumFrames` with kind `Int` and value `>= 0` maps to `Some(value as u32)`
- fixture_003 candidate maps to `Some(8288)`
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

- admitted as candidate mapping/error-boundary policy only
- not admitted as fixture_003 MIMIR parser behavior

Selected same-name metadata candidates:

| Metadata key | Source kind | Candidate `FieldValue` |
| --- | --- | --- |
| `ReplayName` | `Str` | `Text("asdasd")` |
| `Date` | `Str` | `Text("2025-11-01 19-20-48")` |
| `MapName` | `Name` | `Text("cs_day_p")` |
| `ReplayVersion` | `Int` | `Integer(8)` |
| `BuildVersion` | `Str` | `Text("251020.62592.500294")` |
| `MaxChannels` | `Int` | `Integer(2047)` |
| `MatchType` | `Name` | `Text("Online")` |
| `TeamSize` | `Int` | `Integer(2)` |
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
- arrays, body/footer data, raw-state payloads, replay frames, semantic events, non-selected
  properties, and `bForfeit` are excluded from `ReplayHeader.metadata`
- date/time parsing, map-name normalization, and BuildVersion semantic interpretation remain
  closed

## Structural And Error-Boundary Policy Status

Structural/error-boundary status:

- partial overall
- admitted only as external/report structural candidate evidence for fixture_003
- not admitted as fixture_003 MIMIR parser behavior

Admitted fixture_003 external/report structural candidates:

| Target | Candidate evidence |
| --- | --- |
| `header_size` | offset `0`, `i32_little_endian`, value `11190` |
| `header_crc` | offset `4`, `u32_little_endian`, value `3547804793` |
| header data range | `[8, 11198)` |
| `major_version` | offset `8`, value `868` |
| `minor_version` | offset `12`, value `32` |
| `net_version` | offset `16`, value `Some(10)` |
| `game_type` | offset `20`, value `TAGame.Replay_Soccar_TA` |
| property table start | offset `48` |
| top-level property count | `27` |
| property kind counts | `Array=3; Bool=1; Float=3; Int=12; Name=2; QWord=1; Str=5` |
| selected property routes | present for all selected scalar candidate fields |
| `bForfeit` route | present as report-only BoolProperty evidence |
| terminator offset/end | `11189` / `11198` |
| terminator matches header end | `true` |
| content_size first body boundary candidate | offset `11198`, value `1627332` |
| content_crc first body boundary candidate | offset `11202`, value `3991282011` |
| content data start candidate | offset `11206` |

Admitted candidate structural conclusions:

- `header_size` is positive for the fixture_003 report evidence
- candidate `header_end` is `8 + 11190 = 11198`
- candidate property terminator end equals candidate header end
- selected property routes exist in the external structural table
- top-level `bForfeit` route exists only as report evidence
- first body boundary values are report-only boundary candidates and are not MIMIR parser evidence

Not admitted:

- fixture_003 supported-version policy
- fixture_003 parser-success
- broad version-family support
- BoolProperty parser support
- BoolProperty to metadata mapping
- CRC validation
- MIMIR `content_crc` read or validation
- body/footer parsing
- raw-state parsing
- frame parsing
- event parsing

## Deferred Policies And Blockers

No selected scalar field mapping-specific blockers remain for this evidence-only admission pass.

Remaining blockers before any fixture_003 parser-support or implementation claim:

1. Fixture_003 supported-version policy is not admitted. The report-level tuple differs from the
   current exact fixture_001 and fixture_002 supported tuples at
   `BuildVersion = 251020.62592.500294`.
2. BoolProperty handling remains closed. The top-level `bForfeit` property is report-only evidence,
   and the current parser does not admit BoolProperty support or skip semantics.
3. Fixture_003 MIMIR parser behavior is unproven and intentionally not tested as proof here.
4. Fixture_003 structural evidence is external/report evidence only, not MIMIR parser evidence.
5. CRC validation remains closed; no header CRC or content CRC validation is admitted.
6. `content_crc` remains outside MIMIR parser code and must not be read or validated by this pass.
7. Body/raw-state/frame/event parsing remains closed.
8. `ReplayInput::File`, replay-source materialization, export/runtime/CLI integration, and backend
   parser dependencies remain closed.

## Explicit Non-Claims

This pass does not claim:

- MIMIR parser success for fixture_003
- broad parser success
- fixture_003 support by `MinimalReplayHeaderReader`
- supported replay version policy for fixture_003
- a third supported tuple
- broad version-family support
- broad `ReplayVersion = 8` support
- wildcard `BuildVersion` support
- future unknown build support
- fixture_003 `ReplayHeader` mapping as MIMIR parser output
- BoolProperty parser support
- BoolProperty mapping as MIMIR parser output
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
- parser expansion for fixture_003
- parser-success admission for fixture_003
- broad parser-success admission
- fixture_003 supported-version policy
- third supported tuple addition
- broad version-family support
- BoolProperty parser support and BoolProperty metadata mapping
- `ReplayInput::File`
- replay-source materialization
- CRC validation
- MIMIR `content_crc` read or validation
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Affected Files

This pass adds only docs/executor admission artifacts:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_MAPPING_ERROR_BOUNDARY_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_mapping_error_boundary_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_mapping_error_boundary_admission_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_mapping_error_boundary_admission_status.txt`

No Rust source, manifest, lockfile, CLI, IO, export, or type crate file is modified.

## Invariants Preserved

- `MinimalReplayHeaderReader` remains exact two-tuple allowlist gated for fixture_001 and
  fixture_002 only.
- `ReplayInput::File` remains unsupported.
- No MIMIR backend replay parser dependency is added.
- CRC validation remains absent.
- Body/raw-state/frame/event parsing remains absent.
- Fixture identity facts are not parser facts.
- External parser/report success is not MIMIR parser success.

## Rollback Strategy

Rollback is deletion of the four docs/executor artifacts created by this pass. No parser source,
manifest, lockfile, dependency graph, runtime behavior, or fixture file rollback is required.

## Next Stage

Recommended next pass:

- fixture_003 BoolProperty/non-selected property structural error-boundary closure pass

That pass should decide whether top-level BoolProperty remains a hard unsupported-property
boundary, can be skipped as a non-selected property, or can be mapped only after a separate
BoolProperty metadata policy. It must still avoid parser implementation and parser-success claims.

Supported-version policy planning may proceed only after that pass, or in parallel as a
docs-only planning pass that explicitly treats BoolProperty support as a non-parser-support caveat
and implementation blocker.

No parser expansion is authorized by this admission.
