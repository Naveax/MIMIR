# MIMIR Skill Forge BC Replay Header Parser Pre-Implementation Gap Closure v1

Pass date: 2026-05-02

## A. Purpose

This pass closes or explicitly accepts the remaining precise non-mapping parser readiness gaps for
the admitted private-local Rocket League replay fixture:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`

This is a policy and evidence admission pass only. It does not implement parser code, does not
implement parser-success logic, does not produce a MIMIR `ReplayHeader`, and does not parse body
payloads, raw-state payloads, replay frames, or semantic replay events.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains limited to:

- `ReplayInput::Memory`

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Replay header parsing remains only a narrow shared `mimir-replay` capability candidate. This pass
does not open replay-source actual materialization, replay-source carrier discovery,
replay-input locator logic, corpus ingestion, runtime CLI behavior, async/background systems,
database code, rollout physics, or export widening.

`mimir_export` widening remains forbidden.

## C. Current Fixture Summary

Fixture identity was reverified before this admission decision.

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
`total_frames`, metadata, byte-layout semantics, version support, or CRC validity.

Verified report and admission inputs:

- prior external parser report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`
- structural report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_structural_report.txt`
- structural admission artifact:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_STRUCTURAL_REPORT_ADMISSION_V1.md`
- mapping/error-boundary admission artifact:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_MAPPING_GAP_ERROR_BOUNDARY_ADMISSION_V1.md`
- non-mapping byte-layout/error-boundary admission artifact:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_NON_MAPPING_BYTE_LAYOUT_ERROR_BOUNDARY_ADMISSION_V1.md`

## D. Current Expected ReplayHeader Evidence Summary

Expected fixture `ReplayHeader` evidence is complete as expected-output evidence only:

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

This remains expected-output evidence only. It is not MIMIR parser output, not parser success, and
not a synthetic `ReplayHeader` produced by this pass.

## E. Current Admitted Byte Layout Summary

The first minimal parser boundary may rely only on the admitted top-level fixture/header layout:

| Target | Admission |
| --- | --- |
| `header_size` | offset `0`, length `4`, `i32_little_endian`, fixture value `13200` |
| `header_crc` | offset `4`, length `4`, `u32_little_endian`, fixture value `2370383193` |
| header data start | offset `8` |
| header data end exclusive | `8 + header_size`, fixture candidate `13208` |
| `major_version` | offset `8`, length `4`, `i32_little_endian`, fixture value `868` |
| `minor_version` | offset `12`, length `4`, `i32_little_endian`, fixture value `32` |
| `net_version` | offset `16`, length `4`, `i32_little_endian`, fixture value `Some(10)` for the admitted exact tuple |
| `game_type` | offset `20`, non-negative Windows-1252 `parse_text`, fixture value `TAGame.Replay_Soccar_TA` |
| property table start | offset `48` |
| top-level property count | fixture count `26` |
| property terminator | key offset `13199`, terminator end `13208`, equal to `header_data_end_exclusive` |
| selected property routes | admitted by the structural report and mapping pass |
| first body boundary candidate | `content_size` offset `13208`, `content_crc` offset `13212`, diagnostic stop candidate only |

Parser stop policy remains:

- stop at `header_data_end_exclusive = 8 + header_size`
- do not read `content_size` or `content_crc` to produce `ReplayHeader`
- do not parse body payloads, raw-state payloads, replay frames, footer structures, or semantic
  events
- allow trailing bytes after `header_data_end_exclusive`

## F. Current Error Surface Summary

Inspected source:

- `crates/mimir-core/src/lib.rs`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`

Current `mimir_core::Result<T>` is:

- `std::result::Result<T, MimirError>`

Current domain error carrier for a replay parser is:

- `MimirError::Message(String)`

Current `mimir-replay` behavior:

- `UnsupportedReplayReader::read_header` returns `Err(MimirError::message(...))`
- no real parser exists
- no replay-specific typed error taxonomy exists
- no parser-success path exists

Admission consequence:

- `MimirError::Message(String)` is sufficient for the first minimal parser implementation tests if
  stable replay-header category text is required
- typed replay-specific errors remain deferred until broad ingestion or typed recovery requires
  them
- this pass does not modify the error type

## G. Selected Outcome

Selected outcome:

- Outcome A

Outcome A is selected because all remaining precise gaps are now either closed for the first
minimal implementation boundary or explicitly accepted as hard unsupported/deferred behavior.

What Outcome A admits for a later parser implementation planning reopen pass:

- CRC validation may be deferred for the first minimal parser
- top-level non-selected `ArrayProperty` may be skipped by bounded `property_size`
- selected `ArrayProperty` remains unsupported
- UTF-16 or negative-length `parse_text` remains unsupported
- unencountered property kinds remain unsupported
- `MimirError::Message(String)` with stable category text is sufficient for first implementation
  tests

What Outcome A does not admit:

- parser implementation in this pass
- parser-success logic in this pass
- `ReplayHeader` production or synthesis in this pass
- enforced CRC validation
- nested array semantics
- UTF-16 decode support
- broad unencountered property-kind support
- broad Rocket League replay version-family support
- typed replay-specific `MimirError` variants

Parser implementation remains closed until a later explicit implementation planning reopen pass.

## H. CRC Closure Decision

CRC gap status for first implementation:

- closed by explicit deferral

First-implementation policy:

- the minimal `ReplayReader::read_header(&ReplayInput)` reads `header_crc` as layout evidence only
- it does not validate header CRC
- it does not expose CRC in `ReplayHeader`
- it does not read or validate content/body CRC
- CRC mismatch is not observable in the first minimal parser

Rationale:

- expected `ReplayHeader` evidence is complete without CRC enforcement
- the parser is minimal-header scoped and fixture-supported, not broad replay ingestion
- enforced CRC validation requires a separately admitted in-project checker or dependency-backed
  proof of algorithm, byte range, and fixture result
- no project backend dependency is added by this pass

Hard boundary:

- if a later pass enforces CRC, mismatch must be a hard replay-header parse error
- silent CRC enforcement, guessed algorithm selection, or claimed CRC validation without an
  admitted checker is forbidden

Remaining non-blocking deferred work:

- exact in-project CRC checker admission or implementation
- header CRC covered-range proof
- content/body CRC policy outside minimal header parsing

## I. ArrayProperty Closure Decision

`ArrayProperty` gap status for first implementation:

- closed by bounded skip policy

First-implementation policy:

- top-level non-selected `ArrayProperty` values may be skipped using bounded `property_size`
- nested array dictionary semantics are not parsed
- selected `ArrayProperty` is unsupported
- if an array declared range exceeds `header_data_end_exclusive`, return a hard malformed-property
  error
- if a future required or selected field is inside an array, the first implementation must reject
  or defer rather than parse it

Rationale:

- current expected `ReplayHeader` fields do not require array contents
- admitted fixture arrays are top-level non-selected properties
- bounded skip avoids inventing nested semantics while still allowing the selected scalar fields
  after arrays to be reached

Hard boundary:

- no nested array parse success may be claimed
- no metadata may be derived from arrays
- no selected array may be silently skipped and still produce parser success

Remaining non-blocking deferred work:

- nested array dictionary semantics
- malformed nested array fixture coverage
- future selected array mapping policy, if ever needed

## J. UTF-16 Text Closure Decision

UTF-16 text gap status for first implementation:

- closed by hard unsupported-text boundary

First-implementation policy:

- the first minimal parser supports only admitted non-negative Windows-1252 `parse_text` strings
  used by this fixture for selected text/name fields and game type
- UTF-16 or negative-length `parse_text` is unsupported for the first implementation
- if UTF-16 or negative-length text is encountered in required fields or selected metadata, return
  a hard `unsupported-text` or malformed-text boundary
- no silent fallback, lossy decode, guessed conversion, or replacement-character decode is
  admitted

Rationale:

- fixture evidence does not require UTF-16
- expected `ReplayHeader` evidence is complete with admitted non-negative text values
- UTF-16 support requires a separate encoding behavior admission before claiming support

Hard boundary:

- UTF-16 text support must not be claimed by the first minimal parser
- unsupported text must not be accepted by producing partial metadata or default strings

Remaining non-blocking deferred work:

- UTF-16 `parse_text` decoding semantics
- malformed UTF-16 boundary fixture coverage

## K. Unencountered Property Kind Closure Decision

Unencountered property kind gap status for first implementation:

- closed by hard unsupported-property boundary

First-implementation policy:

- the first minimal parser supports only admitted encountered top-level property kinds:
  - `StrProperty`
  - `NameProperty`
  - `IntProperty`
  - `FloatProperty`
  - `QWordProperty`
  - `ArrayProperty` as non-selected bounded skip only
- any unencountered property kind, including `BoolProperty`, `ByteProperty`, `StructProperty`, or
  unknown kind text, is a hard unsupported-property boundary
- no silent skipping of unknown kinds is admitted
- no parser success is admitted after an unsupported unknown kind is encountered before the header
  terminator

Rationale:

- fixture evidence does not require these kinds
- supporting unencountered kinds without fixture/source-backed boundary tests would invent parser
  semantics
- hard rejection is safer than silent skip for a minimal auditable parser

Remaining non-blocking deferred work:

- fixture-backed support for additional property kinds, if future selected fields require them
- dedicated malformed/unsupported property-kind tests in the implementation pass

## L. Error Surface Closure Decision

Error surface gap status for first implementation:

- closed by stable `MimirError::Message(String)` category policy

First-implementation policy:

- `MimirError::Message(String)` is sufficient for the first minimal parser implementation
- first implementation tests must assert stable category substrings:
  - `replay header parse error: insufficient`
  - `replay header parse error: malformed`
  - `replay header parse error: unsupported-version`
  - `replay header parse error: unsupported-property`
  - `replay header parse error: unsupported-text`
  - `replay header parse error: unsupported-input`
  - `replay header mapping error`
- message text should include the boundary class and the affected field, property, or offset where
  known

Rationale:

- current public parser target is already `Result<ReplayHeader>`
- current workspace has no replay-specific typed error taxonomy
- no current consumer can type-match replay parser failures
- modifying `mimir-core` is outside this pass and unnecessary for the first minimal parser

Remaining non-blocking deferred work:

- typed replay-specific error taxonomy before broad replay ingestion, retry/recovery logic, or
  consumers requiring machine-actionable parse failure categories

## M. Implementation-Readiness Decision

Implementation-readiness decision:

- byte-layout and error-boundary readiness is sufficient for a later explicit parser implementation
  planning reopen pass
- parser implementation code remains closed in this pass
- parser-success logic remains closed in this pass
- the next pass may be an explicit parser implementation planning reopen pass

The later implementation planning reopen pass must still restate:

- first parser surface: `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`
- first parser input: `ReplayInput::Memory` only
- first supported tuple: `major_version=868`, `minor_version=32`, `net_version=Some(10)`,
  `game_type=TAGame.Replay_Soccar_TA`, `ReplayVersion=8`,
  `BuildVersion=241206.55345.468477`
- CRC validation deferred
- non-selected top-level arrays skipped by bounded size only
- selected arrays unsupported
- UTF-16 text unsupported
- unencountered property kinds unsupported
- stable `MimirError::Message` category text required in tests

## N. Outcome A Policy Table

| Gap | First-implementation policy | Allowed behavior | Hard error behavior | Admitted status | Remaining blocker |
| --- | --- | --- | --- | --- | --- |
| CRC validation | defer validation | read `header_crc` as bounded layout field only; do not expose it | no CRC mismatch error because CRC mismatch is not observable while deferred | accepted for first implementation | no implementation blocker; enforced CRC remains deferred |
| Content/body CRC | out of minimal header scope | do not read or validate `content_crc` in `read_header` | if a later body parser reads it, mismatch policy must be separately admitted | accepted for first implementation | body parsing remains closed |
| Top-level non-selected `ArrayProperty` | skip by bounded `property_size` only | advance over value range if range stays within header bounds | malformed-property if range exceeds header bounds or overflows | accepted for first implementation | nested array semantics deferred |
| Selected `ArrayProperty` | unsupported | none | unsupported-property or mapping error if selected/required field is an array | accepted for first implementation | selected array mapping deferred |
| UTF-16 `parse_text` | unsupported | parse admitted non-negative Windows-1252 text only | unsupported-text or malformed-text for negative-length/UTF-16 text in required or selected fields | accepted for first implementation | UTF-16 support deferred |
| Unencountered property kinds | unsupported | parse only encountered admitted kinds; skip non-selected properties only when kind is admitted and bounded | unsupported-property for `BoolProperty`, `ByteProperty`, `StructProperty`, or unknown kind | accepted for first implementation | additional kind support deferred |
| Error surface | use `MimirError::Message(String)` with stable category text | return existing `Result<ReplayHeader>` errors with stable substrings | tests fail if categories drift or unsupported conditions produce success | accepted for first implementation | typed taxonomy deferred |
| Unsupported input | only `ReplayInput::Memory` | memory input with non-empty label and bytes may be parsed | unsupported-input for `ReplayInput::File`; mapping/input error for empty label | accepted for first implementation | file input remains closed |
| Parser stop | stop at `8 + header_size` | complete header-only byte slice may be enough | malformed if terminator does not end exactly at header end; insufficient if header bytes unavailable | admitted for first implementation | body parsing remains closed |
| Supported version | exact fixture tuple only | parse only exact admitted tuple | unsupported-version for structurally parsed different tuple | admitted for first implementation | broad version families deferred |

## O. Complete, Partial, Missing, And Rejected Status

| Evidence or policy target | Status | Notes |
| --- | --- | --- |
| fixture identity | complete | path exists; byte length and SHA-256 match |
| report identities | complete | prior report and structural report exist |
| non-mapping admission input | complete | prior non-mapping admission artifact exists and was inspected |
| current error surface inspection | complete | `MimirError::Message` is current domain carrier |
| expected fixture `ReplayHeader` evidence | complete | expected-output evidence only, not parser output |
| top-level prefix byte layout | complete for first minimal target | offsets, lengths, encodings, values admitted |
| header version/game byte layout | complete for exact fixture tuple | broad version-family support not admitted |
| property table start and terminator | complete for first minimal target | terminator must end exactly at header end |
| selected property byte ranges | complete for expected-output mapping | inherited from structural and mapping admissions |
| property entry structure | complete for top-level first minimal policy | nested array internals deferred |
| selected scalar value encodings | complete for admitted selected keys | `Str`, `Name`, `Int`, `Float` admitted; finite float required |
| `ArrayProperty` | accepted for first minimal target | top-level non-selected skip only; nested/selected arrays unsupported |
| UTF-16 text | accepted unsupported | hard unsupported-text/malformed-text boundary |
| unencountered property kinds | accepted unsupported | hard unsupported-property boundary |
| CRC validation | accepted deferred | no CRC mismatch observability in first parser |
| parser stop behavior | complete for first minimal target | stop at `8 + header_size`; do not parse body |
| insufficient-byte boundaries | complete for first minimal policy | implementation tests still required later |
| malformed-byte boundaries | complete for first minimal policy | nested array/UTF-16/CRC enforcement behaviors remain deferred because unsupported/deferred |
| unsupported-version boundary | complete for exact-tuple distinction | only after structural version fields parse |
| error surface | complete for first minimal policy | stable message categories required |
| parser implementation | closed | not reopened by this pass |
| parser-success logic | closed | not reopened by this pass |
| broad replay ingestion | closed | no corpus-wide parser admission |

Rejected as parser facts or success evidence:

- fixture path, filename, provenance, byte length, and SHA-256
- external parser success
- structural report generation success
- body/footer counts
- raw-state payloads
- replay frames
- semantic replay events
- CRC validity
- nested array semantic values
- unencountered property-kind semantics

## P. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

Parser implementation may not proceed directly from this pass. The next pass may be an explicit
parser implementation planning reopen pass. Only that later pass may decide whether code changes
for a first minimal parser may start.

Implementation-blocking gap status for the first minimal boundary:

- CRC: closed by explicit validation deferral
- `ArrayProperty`: closed by top-level non-selected skip policy and selected-array hard rejection
- UTF-16: closed by hard unsupported-text boundary
- unencountered property kinds: closed by hard unsupported-property boundary
- error surface: closed by stable `MimirError::Message` category policy

Residual deferred work remains, but it is not a blocker for the later implementation planning
reopen:

- enforced CRC validation
- nested array semantics
- UTF-16 decode support
- additional property-kind support
- typed replay error taxonomy
- broad version-family support

## Q. No-Fake-Evidence Rules

This pass admits no invented:

- parser-success output
- `ReplayHeader` production or synthesis
- CRC validation result
- broad Rocket League version support
- body/footer parse semantics
- raw-state payload parse semantics
- replay frame extraction
- semantic replay event extraction
- replay id derivation from fixture identity
- source label derivation from path, filename, hash, or provenance
- metadata values from unselected properties
- metadata values from arrays
- nested array semantics
- UTF-16 decode behavior
- unencountered property-kind behavior
- silent duplicate overwrite
- silent unsupported-kind skip
- silent malformed-value omission

External parser/tool success is not MIMIR parser success.

The structural report is not MIMIR parser output.

## R. What Remains Closed

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

## S. What Remains Forbidden

Still forbidden unless explicitly reopened:

- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- modifying `Cargo.toml`
- modifying `Cargo.lock`
- adding project backend dependencies
- implementing parser code in this pass
- implementing parser-success logic in this pass
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

## T. Next Stage

The next pass may be:

- explicit parser implementation planning reopen pass

That next pass must still be planning/reopen scoped before code starts. Parser implementation code
is allowed only after the later explicit implementation reopen pass admits the implementation plan
and restates all first-boundary restrictions from this artifact.

If the next pass instead reopens CRC enforcement, nested arrays, UTF-16 support, additional
property kinds, typed replay errors, file input, or broad version families, parser implementation
must remain blocked until that reopened topic is resolved.
