# MIMIR Skill Forge BC Replay Header Parser ReplayHeader Mapping Policy Admission v1

Pass date: 2026-05-02

## A. Purpose

This pass admits, partially admits, rejects, or defers mapping policy from already admitted
structural Rocket League replay header evidence to the future `mimir-replay` `ReplayHeader`
surface for one private-local fixture:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- prior external parser report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`
- structural report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_structural_report.txt`
- structural admission artifact:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_STRUCTURAL_REPORT_ADMISSION_V1.md`

This is a policy/evidence admission pass only. It does not implement parser code, does not
implement parser-success logic, does not produce or synthesize `ReplayHeader`, and does not parse
body/raw-state payloads, replay frames, or semantic replay events.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains limited to:

- `ReplayInput::Memory`

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Rocket League replay header parsing remains only a shared `mimir-replay` capability candidate.
This pass does not create replay-source actual materialization, carrier discovery, locator logic,
corpus ingestion, runtime CLI behavior, async/background systems, database code, rollout physics,
or export widening.

`mimir_export` widening remains forbidden.

## C. Fixture Summary

The fixture identity was reverified before this admission decision.

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |
| first parser input boundary | `ReplayInput::Memory` only |

The fixture path, filename, provenance, byte length, and SHA-256 remain fixture identity and
integrity facts only. They are not parser facts, replay id sources, source-label sources, total
frame sources, or metadata sources.

## D. Structural Admission Summary

The prior structural admission pass selected Outcome B and partially admitted the structural
report only.

Admitted or partially admitted structural facts relevant to this pass include:

| Target | Admitted structural evidence |
| --- | --- |
| `header_size` | offset `0`, byte length `4`, `i32_little_endian`, fixture value `13200` |
| `header_crc` | offset `4`, byte length `4`, `u32_little_endian`, fixture value `2370383193` |
| header data start | offset `8` |
| header data end candidate | exclusive offset `13208` |
| `major_version` | offset `8`, `i32_little_endian`, value `868` |
| `minor_version` | offset `12`, `i32_little_endian`, value `32` |
| `net_version` | offset `16`, `i32_little_endian`, value `Some(10)` |
| `game_type` | offset `20`, `windows1252_parse_text_null_terminated`, value `TAGame.Replay_Soccar_TA` |
| header properties start | offset `48` |
| top-level property count | `26` |
| top-level property kind counts | `Array=3`, `Float=3`, `Int=12`, `Name=2`, `QWord=1`, `Str=5` |
| property terminator | key offset `13199`, end offset `13208` |
| first body boundary candidates | `content_size` offset `13208`, `content_crc` offset `13212`, content data start `13216` |

Relevant selected property routes from the structural report:

| Property | Structural path | Kind | Value range | Encoding | Generated fixture value |
| --- | --- | --- | --- | --- | --- |
| `Id` | `header.properties[20]` | `Str` | `[12880,12917)` | `windows1252_parse_text_null_terminated` | `7F59297811EFD8B19C444A81FB07660C` |
| `NumFrames` | `header.properties[24]` | `Int` | `[13145,13149)` | `i32_little_endian_4_bytes` | `13555` |
| `ReplayName` | `header.properties[8]` | `Str` | `[12285,12324)` | `windows1252_parse_text_null_terminated` | `Frestyle double touch but not ball` |
| `Date` | `header.properties[23]` | `Str` | `[13083,13107)` | `windows1252_parse_text_null_terminated` | `2025-01-22 11-10-32` |
| `MapName` | `header.properties[22]` | `Name` | `[13029,13050)` | `windows1252_parse_text_null_terminated` | `Stadium_Winter_P` |
| `ReplayVersion` | `header.properties[9]` | `Int` | `[12366,12370)` | `i32_little_endian_4_bytes` | `8` |
| `BuildVersion` | `header.properties[14]` | `Str` | `[12592,12616)` | `windows1252_parse_text_null_terminated` | `241206.55345.468477` |
| `MaxChannels` | `header.properties[18]` | `Int` | `[12797,12801)` | `i32_little_endian_4_bytes` | `2047` |
| `MatchType` | `header.properties[25]` | `Name` | `[13188,13199)` | `windows1252_parse_text_null_terminated` | `Online` |
| `TeamSize` | `header.properties[0]` | `Int` | `[85,89)` | `i32_little_endian_4_bytes` | `3` |
| `RecordFPS` | `header.properties[16]` | `Float` | `[12705,12709)` | `f32_little_endian_4_bytes` | `30` |

These values are not MIMIR parser output and are not parser-success evidence.

## E. ReplayHeader Type Summary

Inspected source:

- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-types/src/lib.rs` through visible imports and type definitions

Current `ReplayHeader` fields:

| Field | Type | Relevant type behavior |
| --- | --- | --- |
| `replay_id` | `mimir_types::ReplayId` | transparent string newtype created by `ReplayId::new(...)`; no built-in shape validation was found |
| `source_label` | `String` | plain string field |
| `total_frames` | `Option<u32>` | optional unsigned frame count |
| `metadata` | `mimir_types::Metadata` | deterministic `BTreeMap<String, FieldValue>` wrapper |

Relevant `mimir_types::FieldValue` variants found:

| Variant | Admission relevance |
| --- | --- |
| `Text(String)` | can carry `Str` and `Name` header property values if metadata mapping is admitted |
| `Integer(i64)` | can carry `Int` and non-overflowing `QWord` values if metadata mapping is admitted |
| `Float(f64)` | can carry finite float values if metadata mapping is admitted |
| `Boolean(bool)` | not used by selected fixture metadata candidates |
| `StringList(Vec<String>)` | not used by selected fixture metadata candidates |

No `ReplayHeader` constructor, parser implementation, or parser-success path was found in
`mimir-replay`. `UnsupportedReplayReader` still returns an explicit unsupported error.

## F. Selected Outcome

Selected outcome:

- Outcome B

Outcome B is selected because the mapping policy is partially admissible:

- `ReplayInput::Memory.label` to `ReplayHeader.source_label` is admitted for the first input
  boundary.
- The exact fixture `Id` value can be admitted as the only evidence-backed replay id source
  candidate for the future header output, but complete replay-id failure behavior remains partial.
- The exact fixture `NumFrames` value can be admitted as a non-negative `i32` value that can safely
  convert to `Some(13555u32)`, but complete `None`/invalid behavior remains partial.
- The selected metadata key map can be admitted only for same-name selected header properties and
  currently visible `FieldValue` carriers, but full duplicate/wrong-kind/malformed behavior remains
  partial.

Outcome A is rejected because complete mapping and error behavior is not fully admitted:

- no complete MIMIR error taxonomy exists for mapping failures
- no complete duplicate property policy is admitted beyond rejecting ambiguity as a future parser
  boundary candidate
- no complete missing/invalid `NumFrames` `None` policy is admitted
- no complete malformed replay id shape policy is admitted beyond the exact fixture shape
- no complete full-property validation policy is admitted
- supported-version, CRC, and parser stop/error boundaries remain incomplete

Outcome C is rejected because some source-backed and policy-backed mappings are now bounded enough
to admit partially.

Outcome D is rejected because admission remains bounded by one fixture, one structural report, one
existing `ReplayHeader` type, and explicit closed implementation boundaries.

## G. Replay Id Mapping Decision

Mapping target:

- `ReplayHeader.replay_id`

Admitted source for this fixture:

- property key: `Id`
- structural path: `header.properties[20]`
- key offset: `12849`
- required kind: `Str`
- required encoding: `windows1252_parse_text_null_terminated`
- value range: `[12880,12917)`
- fixture value: `7F59297811EFD8B19C444A81FB07660C`

Admitted fixture-level mapping policy:

- when exactly one selected top-level `Id` property is present with kind `Str`
- and the parsed value exactly matches the admitted fixture evidence
  `7F59297811EFD8B19C444A81FB07660C`
- and the value is non-empty and uppercase ASCII hex-like for this fixture
- the future expected `ReplayHeader.replay_id` candidate is
  `ReplayId::new("7F59297811EFD8B19C444A81FB07660C")`

Not admitted:

- deriving replay id from fixture id, path, filename, provenance, byte length, SHA-256, or report
  identity
- deriving replay id from body/frame data
- treating external parser report output as MIMIR parser output
- global replay id shape validation beyond this fixture value

Policy status for blocked cases:

| Case | Status in this pass |
| --- | --- |
| missing `Id` | partial; non-optional destination implies future parse cannot produce a valid `ReplayHeader`, but exact MIMIR error boundary is not admitted |
| duplicate `Id` | partial; deterministic first/last selection is rejected, but exact duplicate-property error boundary is not admitted |
| non-`Str` `Id` | partial; wrong-kind mapping is rejected for `replay_id`, but exact MIMIR error boundary is not admitted |
| empty `Id` | partial; empty replay id is rejected for this mapping, but exact MIMIR error boundary is not admitted |
| malformed `Id` | partial; value outside the admitted fixture shape is not admitted as a replay id, but complete shape policy is not admitted |

## H. Source Label Mapping Decision

Mapping target:

- `ReplayHeader.source_label`

Admitted source:

- `ReplayInput::Memory.label`

Admitted fixture-level mapping policy:

- for the first admitted parser input boundary, `ReplayInput::Memory.label` maps directly to
  `ReplayHeader.source_label`
- fixture expected label:
  `rl_replay_header_fixture_001`

Explicit non-sources:

- fixture path
- fixture filename
- fixture provenance
- fixture byte length
- fixture SHA-256
- `Id`

Blocked cases:

| Case | Status in this pass |
| --- | --- |
| empty memory label | partial; rejected as an admitted fixture input shape, but exact MIMIR error boundary is not admitted |
| duplicate labels | not applicable to a single `ReplayInput::Memory` input |
| `ReplayInput::File` | deferred/rejected for first parser input boundary; file-label derivation is not admitted for the minimal parser |

## I. Total Frames Mapping Decision

Mapping target:

- `ReplayHeader.total_frames`

Admitted source for this fixture:

- property key: `NumFrames`
- structural path: `header.properties[24]`
- key offset: `13107`
- required kind: `Int`
- source type: signed `i32`
- value range: `[13145,13149)`
- value encoding: `i32_little_endian_4_bytes`
- fixture value: `13555`

Admitted fixture-level conversion:

- the exact fixture `NumFrames` value `13555` is non-negative
- `13555i32` can be represented as `13555u32`
- the future expected `ReplayHeader.total_frames` candidate for this fixture is `Some(13555)`

Not admitted:

- deriving total frames from body frame extraction
- deriving total frames from packet/body/footer counts
- using fixture byte length as frame count evidence
- a complete `None` policy for all missing or invalid `NumFrames` cases

Policy status for blocked cases:

| Case | Status in this pass |
| --- | --- |
| missing `NumFrames` | deferred; `None` remains plausible because the field is `Option<u32>`, but no complete missing-property policy is admitted |
| duplicate `NumFrames` | partial; deterministic first/last selection is rejected, but exact MIMIR error boundary is not admitted |
| wrong-kind `NumFrames` | deferred; no complete policy admits either hard error or `None` |
| negative `NumFrames` | partial; signed-to-unsigned conversion is rejected for negative values, but exact hard-error versus `None` policy is not admitted |
| malformed `NumFrames` bytes | partial; invalid integer bytes cannot map, but exact MIMIR error boundary is not admitted |

## J. Metadata Mapping Decision

Mapping target:

- `ReplayHeader.metadata`

Selected keys for this fixture:

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

- destination metadata keys use the same case-sensitive property names as the selected header
  property keys
- no normalized or renamed metadata keys are admitted
- body/footer values are not admitted as metadata

Admitted value carrier candidates:

| Header kind | `FieldValue` carrier | Status |
| --- | --- | --- |
| `Str` | `FieldValue::Text(String)` | admitted for selected fixture `Str` values |
| `Name` | `FieldValue::Text(String)` | admitted for selected fixture `Name` values |
| `Int` | `FieldValue::Integer(i64)` | admitted for selected fixture `Int` values |
| `Float` | `FieldValue::Float(f64)` | admitted for selected fixture finite `Float` values |
| `QWord` | `FieldValue::Integer(i64)` only if non-overflowing | candidate only; no selected metadata key uses `QWord` in this pass |
| `Array` | none | not admitted for metadata |

Fixture metadata candidates admitted as partial expected-output evidence:

| Metadata key | Source kind | `FieldValue` candidate |
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

Not admitted:

- normalized metadata key names
- metadata values from non-selected properties
- metadata values from arrays, body/footer data, frames, or events
- date/time parsing or timezone normalization
- map-name semantic normalization
- build-version semantic interpretation

Policy status for blocked cases:

| Case | Status in this pass |
| --- | --- |
| selected property missing | deferred; omission is plausible for optional metadata, but a complete omission/default policy is not admitted |
| all selected properties missing | deferred; empty `Metadata::new()` is possible through the type, but empty metadata output policy is not fully admitted |
| duplicate selected property | partial; first/last overwrite into `BTreeMap` is rejected, but exact MIMIR error boundary is not admitted |
| wrong kind for selected key | partial; wrong-kind conversion is rejected for the selected key map, but exact error versus omission behavior is not admitted |
| malformed selected value | partial; malformed values cannot be silently converted, but exact MIMIR error boundary is not admitted |
| empty selected string/name value | deferred; no complete preserve-empty versus omit/error policy is admitted |
| non-finite selected float | partial; `FieldValue::Float` requires finite values, but exact MIMIR error boundary is not admitted |

## K. Expected Fixture ReplayHeader Evidence Status

Expected `ReplayHeader` evidence status:

- partial

No complete `ReplayHeader` output is admitted.

Partial expected fixture field evidence:

| Field | Expected fixture evidence status | Candidate value |
| --- | --- | --- |
| `replay_id` | partial | `ReplayId::new("7F59297811EFD8B19C444A81FB07660C")` |
| `source_label` | admitted for the memory-input boundary | `"rl_replay_header_fixture_001"` |
| `total_frames` | partial | `Some(13555)` |
| `metadata` | partial | same-name selected metadata map listed in this document |

Why complete expected output is not admitted:

- replay id failure behavior remains partial
- total frame missing/invalid/negative behavior remains partial
- metadata missing/duplicate/wrong-kind/malformed behavior remains partial
- MIMIR error boundaries remain incomplete
- parser implementation and parser-success logic remain closed

This is expected-output evidence only. It is not MIMIR parser output.

## L. Outcome B Mapping Policy Table

| ReplayHeader field | Source evidence | Admitted status | Expected fixture value if admitted/partial | Missing behavior | Duplicate behavior | Malformed/wrong-kind behavior | Remaining blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `replay_id` | top-level `Id`, `header.properties[20]`, `Str`, `[12880,12917)`, Windows-1252 text | partial | `7F59297811EFD8B19C444A81FB07660C` | partial; no valid non-optional output without `Id`, exact error not admitted | partial; reject first/last choice, exact error not admitted | partial; reject non-`Str`, empty, or outside admitted fixture shape, exact error not admitted | complete replay id validation and MIMIR error boundary |
| `source_label` | `ReplayInput::Memory.label` input contract | admitted for first memory input boundary | `rl_replay_header_fixture_001` | partial; empty label rejected for fixture boundary, exact error not admitted | not applicable to one input | non-memory input deferred/rejected for first parser target | non-memory and empty-label error boundary |
| `total_frames` | top-level `NumFrames`, `header.properties[24]`, `Int`, `[13145,13149)`, `i32` value `13555` | partial | `Some(13555)` | deferred; `None` not fully admitted | partial; reject first/last choice, exact error not admitted | partial; negative conversion rejected; wrong kind and invalid bytes lack complete error/`None` policy | missing/invalid/negative `NumFrames` policy |
| `metadata` | selected same-name top-level properties | partial | selected map using `Text`, `Integer`, and finite `Float` carriers | deferred; omission/empty map policy not fully admitted | partial; reject silent `BTreeMap` overwrite, exact error not admitted | partial; reject silent wrong-kind/malformed conversion, exact error or omission not admitted | metadata omission/default and mapping failure policy |

## M. Missing, Wrong-Kind, Duplicate, And Malformed Policy Status

Overall policy status:

- partial

Admitted principles:

- silent first/last duplicate selection is not admitted for `replay_id`, `total_frames`, or selected
  metadata keys
- silent wrong-kind conversion is not admitted
- silent malformed-value conversion is not admitted
- parser output must not be synthesized from fixture identity or report identity

Still missing:

- exact MIMIR error categories/messages for missing required `Id`
- exact MIMIR error categories/messages for duplicate selected properties
- exact MIMIR error categories/messages for wrong-kind selected properties
- exact `None` versus error policy for missing `NumFrames`
- exact `None` versus error policy for invalid or negative `NumFrames`
- exact omission/default/empty policy for selected metadata
- exact behavior for empty selected metadata strings

## N. What Is Complete, Partial, Missing, Or Rejected

Complete/admitted:

- fixture identity verification
- prior report existence verification
- structural report/admission existence verification
- `ReplayHeader` field/type inspection
- `ReplayInput::Memory.label` to `ReplayHeader.source_label` for the admitted memory-input
  boundary
- same-name metadata key policy as a candidate for the selected fixture keys
- visible `FieldValue` carrier candidates for selected fixture values

Partial:

- `Id` to `ReplayHeader.replay_id`
- `NumFrames` to `ReplayHeader.total_frames`
- selected properties to `ReplayHeader.metadata`
- expected fixture `ReplayHeader` evidence
- missing/duplicate/wrong-kind/malformed mapping behavior
- byte-layout evidence
- error-boundary evidence

Missing:

- complete expected `ReplayHeader` output admission
- complete signed `i32` to `Option<u32>` policy for all `NumFrames` edge cases
- complete metadata omission/default/empty policy
- complete duplicate selected property policy with MIMIR error boundary
- complete supported-version policy
- complete CRC policy
- complete full property validation policy
- complete parser stop/error behavior
- complete MIMIR error taxonomy

Rejected:

- replay id derivation from fixture id, path, filename, hash, provenance, or byte length
- source label derivation from fixture path, filename, hash, or provenance
- total frame derivation from body frame extraction, footer counts, byte length, or external parser
  success
- metadata derivation from unselected properties, arrays, body/footer data, raw-state payloads,
  frames, or events
- external report success as MIMIR parser success

## O. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

Implementation may not proceed from this pass because:

1. expected `ReplayHeader` evidence remains partial
2. byte-layout evidence remains partial
3. complete MIMIR mapping error boundaries remain missing
4. supported-version policy remains missing
5. CRC policy remains missing
6. full property validation policy remains missing
7. parser implementation has not been explicitly reopened

## P. No-Fake-Evidence Rules

This pass admits no invented:

- replay id derivation
- source label derivation from storage identity
- total frame derivation
- metadata key normalization
- metadata values from non-selected or body/footer data
- parser-success fixture output
- raw-state payload output
- replay-frame output
- semantic-event output
- CRC validation result
- supported-version result
- parser error taxonomy

The structural report is not MIMIR parser output.

External tool success is not MIMIR parser success.

## Q. What Remains Closed

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

## R. What Remains Forbidden

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

## S. Next Stage

Immediate next pass:

- remaining ReplayHeader mapping gap and error-boundary derivation/admission pass

The next pass must target:

- exact missing/invalid/negative `NumFrames` behavior
- exact metadata omission/default/empty behavior
- exact duplicate/wrong-kind/malformed selected-property behavior
- exact MIMIR error boundaries for mapping failures

Parser implementation is allowed only if fixture evidence, complete byte-layout evidence, complete
expected output evidence, and required error boundaries are admitted, and implementation is
explicitly reopened.
