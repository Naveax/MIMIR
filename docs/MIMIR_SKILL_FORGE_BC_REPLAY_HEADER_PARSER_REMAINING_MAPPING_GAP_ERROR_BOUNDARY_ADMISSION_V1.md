# MIMIR Skill Forge BC Replay Header Parser Remaining Mapping Gap Error Boundary Admission v1

Pass date: 2026-05-02

## A. Purpose

This pass closes the remaining `ReplayHeader` field-mapping and mapping-specific error-boundary
policy gaps for the admitted private-local Rocket League replay fixture:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`

This is a policy and evidence admission pass only. It does not implement parser code, does not
implement parser-success logic, does not produce a MIMIR `ReplayHeader`, and does not parse body
payloads, replay frames, raw-state payloads, or semantic replay events.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains limited to:

- `ReplayInput::Memory`

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Replay header parsing remains only a narrow shared `mimir-replay` capability candidate. This pass
does not open replay-source actual materialization, replay-source carrier discovery, replay-input
locator logic, corpus ingestion, runtime CLI behavior, async/background systems, database code,
rollout physics, or export widening.

`mimir_export` widening remains forbidden.

## C. Current Fixture Summary

Fixture identity was reverified before admission.

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |
| first parser input boundary | `ReplayInput::Memory` only |

The fixture path, filename, provenance, byte length, and SHA-256 remain identity and integrity facts
only. They are not parser facts and are not sources for `replay_id`, `source_label`,
`total_frames`, or metadata.

Report and policy inputs verified for this pass:

- prior external parser report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`
- structural report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_structural_report.txt`
- structural admission artifact:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_STRUCTURAL_REPORT_ADMISSION_V1.md`
- ReplayHeader mapping policy admission artifact:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REPLAYHEADER_MAPPING_POLICY_ADMISSION_V1.md`

## D. Current Mapping Policy Admission Summary

The previous ReplayHeader mapping policy admission pass selected Outcome B. It partially admitted:

- `ReplayInput::Memory.label -> ReplayHeader.source_label`
- same-name selected metadata key policy as a candidate for selected fixture properties
- `Str` and `Name` selected metadata carriers as `FieldValue::Text`
- `Int` selected metadata carriers as `FieldValue::Integer`
- finite `Float` selected metadata carriers as `FieldValue::Float`
- exact fixture candidates for `Id`, `NumFrames`, and selected metadata values

The previous pass left missing, duplicate, wrong-kind, malformed, omission/default, and
`None`-versus-error behavior incomplete. This pass resolves those mapping-specific gaps as policy
without reopening implementation.

## E. Current Error Surface Summary

Inspected source:

- `crates/mimir-core/src/lib.rs`
- `crates/mimir-replay/src/lib.rs`
- relevant current uses in `mimir-io`, `mimir-export`, and `mimir-skill`

Current `mimir_core::Result<T>` is:

- `std::result::Result<T, MimirError>`

Current `mimir_core::MimirError` variants are:

| Variant | Relevance |
| --- | --- |
| `Io { path, source }` | file I/O only |
| `Json(serde_json::Error)` | JSON boundary only |
| `TomlSerialize(toml::ser::Error)` | TOML serialization boundary only |
| `TomlDeserialize(toml::de::Error)` | TOML deserialization boundary only |
| `Message(String)` | only current general domain error carrier |

Current `mimir-replay` behavior:

- `UnsupportedReplayReader::read_header` returns `Err(MimirError::message(...))`
- no real parser exists
- no replay-specific typed error taxonomy exists
- no parser-success path exists

Admission consequence:

- mapping-specific failures are admitted as hard `Err(MimirError::Message(_))` boundaries on the
  current public `Result<ReplayHeader>` surface
- future messages must identify the boundary as a replay-header mapping failure and include the
  affected `ReplayHeader` field or selected metadata key plus the reason
- this pass does not admit a richer typed replay error taxonomy
- typed matching on replay parse/mapping failures remains unavailable until a later explicit error
  taxonomy pass

## F. Selected Outcome

Selected outcome:

- Outcome A

Outcome A is selected for mapping-specific policy only because the remaining `ReplayHeader` field
mapping and mapping-specific missing, duplicate, wrong-kind, malformed, omission/default, and
`None`-versus-error behaviors can be admitted without inventing parser success or implementing a
parser.

What Outcome A admits:

- complete expected fixture `ReplayHeader` evidence for `rl_replay_header_fixture_001`
- complete mapping policy for:
  - `Id -> ReplayHeader.replay_id`
  - `ReplayInput::Memory.label -> ReplayHeader.source_label`
  - `NumFrames -> ReplayHeader.total_frames`
  - selected properties -> `ReplayHeader.metadata`
- complete mapping-specific hard error boundaries on the existing `Result<ReplayHeader>` surface

What Outcome A does not admit:

- parser implementation
- parser-success logic
- complete byte-layout evidence
- supported-version policy
- CRC policy
- parser stop/error behavior
- full property validation policy
- complete non-mapping insufficient-byte or malformed-byte boundaries
- typed replay-specific `MimirError` variants

Outcome B is rejected for this pass because the remaining mapping-specific policies can now be
bounded by explicit deterministic choices. Broader non-mapping parser gates remain separate.

Outcome C is rejected because current evidence is sufficient for policy-level field mapping and
mapping-specific error admission.

Outcome D is rejected because admission remains bounded by one fixture, the existing type surface,
the admitted structural evidence, and explicit implementation closure.

## G. Replay Id Mapping And Error Boundary Decision

Target:

- `ReplayHeader.replay_id`

Required source:

- exactly one top-level property named `Id`
- required kind: `Str`
- required value encoding: `windows1252_parse_text_null_terminated`
- required value shape for the minimal parser boundary: exactly 32 ASCII hex digits
- no case normalization is admitted; the parsed source string is preserved
- fixture value:
  `7F59297811EFD8B19C444A81FB07660C`

Admitted fixture structural route:

| Field | Value |
| --- | --- |
| structural path | `header.properties[20]` |
| key offset | `12849` |
| kind | `Str` |
| value range | `[12880,12917)` |
| encoding | `windows1252_parse_text_null_terminated` |

Admitted destination:

- `ReplayHeader.replay_id = ReplayId::new("7F59297811EFD8B19C444A81FB07660C")`

Mapping-specific error policy:

| Case | Admitted behavior |
| --- | --- |
| missing `Id` | hard replay-header mapping error; no `ReplayHeader` may be produced |
| duplicate `Id` | hard replay-header mapping error; first/last selection is forbidden |
| non-`Str` `Id` | hard replay-header mapping error |
| empty `Id` | hard replay-header mapping error |
| malformed `Id` | hard replay-header mapping error if not exactly 32 ASCII hex digits |
| non-ASCII or non-hex-like `Id` | hard replay-header mapping error |
| multiple replay-id-like properties | ignored unless the key is exactly `Id`; no fallback to `MatchGuid` or any other key |

Explicit non-sources:

- fixture id
- path or filename
- provenance label
- byte length
- SHA-256
- external parser success
- body/footer/frame/event data

## H. Source Label Mapping And Error Boundary Decision

Target:

- `ReplayHeader.source_label`

Required source:

- `ReplayInput::Memory.label`

Admitted destination:

- `ReplayHeader.source_label = memory_label`

Fixture expected source label:

- `rl_replay_header_fixture_001`

Mapping-specific error policy:

| Case | Admitted behavior |
| --- | --- |
| non-empty memory label | map directly and preserve exact string |
| empty memory label | hard input/mapping error; no empty `source_label` is admitted |
| `ReplayInput::File` | hard unsupported-input boundary for the first minimal parser implementation |
| duplicate labels | not applicable to one `ReplayInput::Memory` value |

Explicit non-sources:

- fixture path
- fixture filename
- fixture provenance
- byte length
- SHA-256
- `Id`

## I. Total Frames Mapping And Error Boundary Decision

Target:

- `ReplayHeader.total_frames`

Required source:

- optional top-level property named `NumFrames`
- required kind if present: `Int`
- source type: signed `i32`
- value encoding: `i32_little_endian_4_bytes`
- fixture value: `13555`

Admitted fixture structural route:

| Field | Value |
| --- | --- |
| structural path | `header.properties[24]` |
| key offset | `13107` |
| kind | `Int` |
| value range | `[13145,13149)` |
| encoding | `i32_little_endian_4_bytes` |

Admitted destination:

- `ReplayHeader.total_frames = Some(13555)`

Mapping-specific error policy:

| Case | Admitted behavior |
| --- | --- |
| present `NumFrames`, kind `Int`, value `>= 0` | `Some(value as u32)` |
| missing `NumFrames` | `None` |
| duplicate `NumFrames` | hard replay-header mapping error; first/last selection is forbidden |
| wrong-kind `NumFrames` | hard replay-header mapping error; present but unmappable is not treated as missing |
| negative `NumFrames` | hard replay-header mapping error; no signed-to-unsigned wrap or clamp is admitted |
| malformed `NumFrames` bytes | hard malformed-property error; no `ReplayHeader` may be produced |
| value greater than `u32::MAX` | impossible for admitted signed `i32` source values; if encountered through a different source shape, treat as malformed/unadmitted |

Explicit non-sources:

- body frame extraction
- packet/body/footer counts
- fixture byte length
- external parser success

## J. Metadata Mapping And Error Boundary Decision

Target:

- `ReplayHeader.metadata`

Selected metadata keys:

- `ReplayName`
- `Date`
- `MapName`
- `ReplayVersion`
- `BuildVersion`
- `MaxChannels`
- `MatchType`
- `TeamSize`
- `RecordFPS`

Admitted key policy:

- destination keys are the same case-sensitive property names
- no key normalization is admitted
- no renamed metadata keys are admitted
- non-selected properties are ignored for `ReplayHeader.metadata`

Admitted value mapping:

| Header kind | Destination carrier | Status |
| --- | --- | --- |
| `Str` | `FieldValue::Text(String)` | admitted for selected keys |
| `Name` | `FieldValue::Text(String)` | admitted for selected keys |
| `Int` | `FieldValue::Integer(i64)` | admitted for selected keys |
| finite `Float` | `FieldValue::Float(f64)` | admitted for selected keys |
| `QWord` | `FieldValue::Integer(i64)` if non-overflowing | admitted only for future selected keys that explicitly choose `QWord` |
| `Array` | none | not admitted for selected metadata |

Admitted fixture metadata entries:

| Metadata key | Source kind | Admitted `FieldValue` |
| --- | --- | --- |
| `ReplayName` | `Str` | `Text("Frestyle double touch but not ball")` |
| `Date` | `Str` | `Text("2025-01-22 11-10-32")` |
| `MapName` | `Name` | `Text("Stadium_Winter_P")` |
| `ReplayVersion` | `Int` | `Integer(8)` |
| `BuildVersion` | `Str` | `Text("241206.55345.468477")` |
| `MaxChannels` | `Int` | `Integer(2047)` |
| `MatchType` | `Name` | `Text("Online")` |
| `TeamSize` | `Int` | `Integer(3)` |
| `RecordFPS` | `Float` | `Float(30.0)` |

Mapping-specific error and omission policy:

| Case | Admitted behavior |
| --- | --- |
| selected key present with expected/admitted kind | include same-name metadata entry |
| selected key missing | omit that metadata entry |
| all selected keys missing | `Metadata::new()` is admitted |
| duplicate selected key | hard replay-header mapping error; silent `BTreeMap` overwrite is forbidden |
| selected key wrong kind | hard replay-header mapping error |
| selected key malformed value | hard malformed-property error |
| selected string/name empty | preserve as empty `FieldValue::Text(String::new())` |
| selected float non-finite | hard replay-header mapping error because `FieldValue::Float` requires finite values |
| unknown non-selected property | ignored for `ReplayHeader.metadata` |
| future selected `QWord` overflow into `i64` | hard replay-header mapping error |

Explicit non-sources:

- arrays
- body/footer data
- raw-state payloads
- replay frames
- semantic replay events
- normalized date/time semantics
- normalized map-name semantics
- build-version interpretation

## K. Expected Fixture ReplayHeader Evidence Status

Expected fixture `ReplayHeader` evidence status:

- complete

The complete expected output evidence for `rl_replay_header_fixture_001` is:

| `ReplayHeader` field | Expected fixture evidence |
| --- | --- |
| `replay_id` | `ReplayId::new("7F59297811EFD8B19C444A81FB07660C")` |
| `source_label` | `"rl_replay_header_fixture_001"` |
| `total_frames` | `Some(13555)` |
| `metadata.ReplayName` | `FieldValue::Text("Frestyle double touch but not ball")` |
| `metadata.Date` | `FieldValue::Text("2025-01-22 11-10-32")` |
| `metadata.MapName` | `FieldValue::Text("Stadium_Winter_P")` |
| `metadata.ReplayVersion` | `FieldValue::Integer(8)` |
| `metadata.BuildVersion` | `FieldValue::Text("241206.55345.468477")` |
| `metadata.MaxChannels` | `FieldValue::Integer(2047)` |
| `metadata.MatchType` | `FieldValue::Text("Online")` |
| `metadata.TeamSize` | `FieldValue::Integer(3)` |
| `metadata.RecordFPS` | `FieldValue::Float(30.0)` |

This is expected-output evidence only. It is not MIMIR parser output, not parser success, and not a
synthetic `ReplayHeader` produced by this pass.

## L. Outcome A Policy Table

| Target field | Valid input policy | Missing behavior | Duplicate behavior | Wrong-kind behavior | Malformed behavior | Admitted status | Remaining blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `replay_id` | exactly one top-level `Id`, kind `Str`, non-empty 32 ASCII hex digits | hard mapping error | hard mapping error | hard mapping error | hard mapping error for empty, non-ASCII, non-hex, or wrong length | complete for mapping | parser byte layout and implementation still closed |
| `source_label` | non-empty `ReplayInput::Memory.label`, preserved exactly | empty label is hard input/mapping error | not applicable | `ReplayInput::File` is hard unsupported input for first parser boundary | not applicable beyond empty string rejection | complete for mapping | non-memory parser support remains closed |
| `total_frames` | optional top-level `NumFrames`; if present, kind `Int`, signed `i32`, value `>= 0` | `None` | hard mapping error | hard mapping error | hard malformed-property error; negative value hard mapping error | complete for mapping | parser byte layout and implementation still closed |
| `metadata` | selected same-name keys with admitted `Str`, `Name`, `Int`, finite `Float` carriers | omit selected key; all missing yields empty metadata | hard mapping error | hard mapping error | hard malformed-property error; non-finite float hard mapping error | complete for mapping | broader metadata expansion remains closed |

## M. Complete, Partial, Missing, And Rejected Status

| Evidence or policy target | Status | Notes |
| --- | --- | --- |
| fixture identity | complete | path exists, byte length and SHA-256 match |
| report identities | complete | prior report, structural report, and mapping policy artifact exist |
| `ReplayHeader` type surface inspection | complete | current fields and carriers inspected |
| current error surface inspection | complete | mapping errors admitted on `MimirError::Message` only |
| `Id -> replay_id` mapping policy | complete | mapping-specific missing/duplicate/wrong-kind/malformed boundaries admitted |
| `ReplayInput::Memory.label -> source_label` policy | complete | empty label and file input boundaries admitted |
| `NumFrames -> total_frames` policy | complete | valid, missing, duplicate, wrong-kind, negative, and malformed behavior admitted |
| selected metadata policy | complete | present, missing, empty, duplicate, wrong-kind, malformed, and non-finite behavior admitted |
| expected fixture `ReplayHeader` evidence | complete | expected-output evidence only, not parser output |
| byte-layout evidence | partial | inherited from structural admission Outcome B |
| supported-version policy | missing | outside this mapping pass |
| CRC policy | missing | outside this mapping pass |
| full property validation policy | partial | selected-property mapping behavior is admitted; full parser validation is not |
| parser stop/error behavior | partial | first body boundary remains a stop candidate only |
| non-mapping insufficient-byte boundaries | partial | outside this mapping pass |
| non-mapping malformed-byte boundaries | partial | outside this mapping pass |
| typed replay error taxonomy | missing | current surface remains `MimirError::Message` for domain errors |
| parser implementation | missing and closed | not reopened by this pass |
| parser-success logic | missing and closed | not reopened by this pass |

Rejected as parser facts or mapping sources:

- fixture id, path, filename, provenance, byte length, and SHA-256
- external parser success
- structural report generation success
- body/footer counts
- raw-state payloads
- replay frames
- semantic replay events
- non-selected metadata properties
- silent duplicate overwrite
- silent wrong-kind conversion
- silent malformed-value omission

## N. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

Implementation may not proceed from this pass alone because these required non-mapping gates remain
incomplete:

1. complete byte-layout admission
2. supported-version policy
3. CRC policy
4. full property validation policy
5. parser stop/error behavior
6. non-mapping insufficient-byte and malformed-byte boundaries
7. explicit parser implementation reopen decision

## O. No-Fake-Evidence Rules

This pass admits no invented:

- replay id derivation from fixture identity
- source label derivation from path, filename, hash, or provenance
- total frame derivation from body or footer counts
- metadata key normalization
- metadata values from unselected properties
- parser-success fixture output
- raw-state payload output
- replay-frame output
- semantic-event output
- CRC validation result
- supported-version result
- parser stop behavior
- typed replay error taxonomy

The structural report is not MIMIR parser output.

External tool success is not MIMIR parser success.

## P. What Remains Closed

Still closed after this pass:

- parser implementation
- parser-success logic
- `ReplayHeader` production or synthesis
- raw-state payload parsing
- replay frame extraction
- semantic replay event extraction
- replay-source actual materialization
- replay-source carrier discovery
- replay-input locator logic
- corpus-wide replay ingestion
- runtime CLI commands
- async/background systems
- database code
- real rollout physics
- `mimir_export` widening

## Q. What Remains Forbidden

Still forbidden unless explicitly reopened:

- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- modifying `Cargo.toml`
- modifying `Cargo.lock`
- adding project backend dependencies
- implementing parser code
- implementing parser-success logic
- producing or synthesizing `ReplayHeader`
- parsing raw-state payloads
- extracting replay frames
- extracting semantic replay events
- implementing replay-source actual materialization
- implementing replay-source carrier discovery
- implementing replay-input locator logic
- widening export semantics
- adding corpus-wide replay ingestion
- adding runtime CLI commands
- adding async/background systems
- adding database code
- adding real rollout physics
- treating fixture path, filename, provenance, byte length, or SHA-256 as parser facts

## R. Next Stage

The next pass must target remaining non-mapping byte-layout and parser error-boundary admission:

- complete byte-layout evidence
- supported-version policy
- CRC policy
- full property validation policy
- parser stop/error behavior
- insufficient-byte boundaries
- malformed-byte boundaries
- unsupported-version boundaries, if distinguishable

Parser implementation remains closed until fixture evidence, complete byte-layout evidence, complete
expected output evidence, and required error boundaries are admitted, and implementation is
explicitly reopened.
