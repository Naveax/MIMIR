# MIMIR Skill Forge BC Replay Header Parser Remaining Non-Mapping Byte-Layout Error Boundary Admission v1

Pass date: 2026-05-02

## A. Purpose

This pass admits, partially admits, or rejects the remaining non-mapping byte-layout and parser
error-boundary evidence for the admitted private-local Rocket League replay fixture:

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
`total_frames`, metadata, byte-layout semantics, version support, or CRC validity.

Report and policy inputs verified for this pass:

- prior external parser report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`
- structural report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_structural_report.txt`
- structural admission artifact:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_STRUCTURAL_REPORT_ADMISSION_V1.md`
- mapping/error-boundary admission artifact:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_MAPPING_GAP_ERROR_BOUNDARY_ADMISSION_V1.md`

## D. Expected ReplayHeader Evidence Summary

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

## E. Current Byte-Layout And Error Status Summary

Before this pass:

- top-level prefix, version fields, game type, top-level property table, selected property routes,
  terminator position, and first body boundary candidates were partially admitted by the structural
  admission pass
- `ReplayHeader` field mapping and mapping-specific errors were fully admitted by the mapping pass
- supported-version policy was missing
- CRC policy was missing
- full property validation policy was partial
- parser stop behavior was partial
- non-mapping insufficient-byte and malformed-byte boundaries were partial
- unsupported-version boundary was missing if distinguishable
- typed replay-specific MIMIR error taxonomy was missing
- parser implementation and parser-success logic remained closed

This pass narrows those gaps but does not close all of them.

## F. Current Error Surface Summary

Inspected source:

- `crates/mimir-core/src/lib.rs`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`

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

- the current `MimirError::Message(String)` surface is sufficient for the first minimal parser
  implementation boundary if future messages use stable replay-header category text
- typed replay-specific error matching is not available
- a typed replay error taxonomy is not required before the first minimal implementation reopen
- a typed replay error taxonomy remains deferred and should be reconsidered before broad replay
  ingestion, corpus parsing, or downstream typed recovery logic

Required future message categories for the first minimal parser boundary:

- `replay header parse error: insufficient: ...`
- `replay header parse error: malformed: ...`
- `replay header parse error: unsupported-version: ...`
- `replay header parse error: unsupported-input: ...`
- `replay header mapping error: ...`

This pass does not modify the error type.

## G. Selected Outcome

Selected outcome:

- Outcome B

Outcome B is selected because remaining non-mapping byte-layout and error-boundary evidence is
partially admissible. This pass admits only bounded evidence-backed and policy-backed behavior and
records the exact gaps that remain. Parser implementation remains closed.

Why Outcome A is rejected:

- CRC validation cannot be honestly admitted as enforced because no MIMIR CRC implementation,
  fixture CRC validation result, or project dependency is admitted
- content/body CRC is outside minimal header parsing
- top-level `Array` value byte ranges are admitted, but nested array/property semantics remain
  unadmitted
- malformed-boundary evidence remains partial for unadmitted text forms, nested array semantics,
  and CRC mismatch behavior
- no parser implementation reopen decision is made by this pass

Why Outcome C is rejected:

- current structural evidence and deterministic policy choices are sufficient to admit exact
  top-level byte layout, exact fixture supported-version policy, read-but-defer CRC policy,
  minimal stop behavior, and many hard insufficient/malformed boundaries

Why Outcome D is rejected:

- admission remains bounded by one fixture, one parser surface, one first input variant, admitted
  structural reports, and explicit no-implementation rules

## H. Byte-Layout Admission Decision

Byte-layout evidence status after this pass:

- partial overall

Admitted as complete for the fixture and first minimal header reader:

| Target | Admission |
| --- | --- |
| `header_size` | offset `0`, length `4`, encoding `i32_little_endian`, fixture value `13200` |
| `header_crc` | offset `4`, length `4`, encoding `u32_little_endian`, fixture value `2370383193` |
| header data start | offset `8` |
| header data end exclusive | `8 + header_size`, fixture candidate `13208` |
| `major_version` | offset `8`, length `4`, encoding `i32_little_endian`, fixture value `868` |
| `minor_version` | offset `12`, length `4`, encoding `i32_little_endian`, fixture value `32` |
| `net_version` | offset `16`, length `4`, encoding `i32_little_endian`, fixture value `Some(10)` for the admitted exact tuple |
| `game_type` | offset `20`, non-negative `parse_text` Windows-1252 bytes with trailing NUL, fixture value `TAGame.Replay_Soccar_TA` |
| property table start | fixture offset `48` |
| top-level generated property count | fixture count `26` |
| property terminator | key offset `13199`, terminator end `13208`, matches `header_data_end_exclusive` |
| selected property routes | admitted from the structural table and mapping pass |
| first body boundary candidate | `content_size` offset `13208`, `content_crc` offset `13212`, content data start `13216`, stop-boundary candidate only |

Admitted property entry shape for the first minimal top-level property scan:

1. key: `parse_str`, UTF-8 bytes with length prefix and trailing NUL
2. terminator: key text exactly `None`; no kind, size, ignored field, or value follows the terminator
3. kind: `parse_str`, UTF-8 bytes with length prefix and trailing NUL
4. `property_size`: `u32_little_endian`
5. ignored four-byte field: must exist, remains semantically ignored, no zero-value requirement is admitted
6. value: interpreted or skipped according to kind and selection policy

Admitted kind texts for the first minimal top-level header reader:

| Source kind text | Report shorthand | First minimal handling |
| --- | --- | --- |
| `StrProperty` | `Str` | parse selected values as text; non-selected may be skipped if size-bounded |
| `NameProperty` | `Name` | parse selected values as text; non-selected may be skipped if size-bounded |
| `IntProperty` | `Int` | parse selected values as 4-byte little-endian `i32`; non-selected may be skipped if size-bounded |
| `FloatProperty` | `Float` | parse selected values as 4-byte little-endian `f32`; finite required for selected metadata |
| `QWordProperty` | `QWord` | parse or skip as 8-byte little-endian `u64`; selected mapping only if explicitly admitted and non-overflowing |
| `ArrayProperty` | `Array` | non-selected top-level values may be skipped by bounded `property_size`; nested array semantics remain unadmitted |

Still partial or missing:

- nested `ArrayProperty` dictionary semantics
- support for unencountered property kinds such as `BoolProperty`, `ByteProperty`, or
  `StructProperty`
- UTF-16 `parse_text` support for the MIMIR first parser
- broad Rocket League replay version families
- CRC enforcement

## I. Supported-Version Policy Decision

Supported-version policy status:

- partially admitted

Admitted exact fixture-supported policy:

| Field | Required value |
| --- | --- |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `Some(10)` |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| selected `ReplayVersion` property | kind `Int`, value `8` |
| selected `BuildVersion` property | kind `Str`, value `241206.55345.468477` |

Admitted boundary behavior:

- if version/game fields cannot be structurally parsed, return an insufficient or malformed
  replay-header error, not unsupported-version
- if version/game fields and required version properties parse structurally but the tuple is not
  the exact admitted tuple above, return an unsupported-version replay-header error
- if required version properties are missing, wrong-kind, or malformed, return malformed property
  or mapping error rather than silently accepting the version
- no broad future Rocket League version support is admitted
- no version-family support beyond the exact tuple is admitted

Remaining blocker:

- version-family support remains missing; only the exact fixture tuple is admitted

## J. CRC Policy Decision

CRC policy status:

- partially admitted as read-but-defer

Admitted:

- `header_crc` field layout is admitted at offset `4`, length `4`, `u32_little_endian`, fixture
  value `2370383193`
- the external source-derived covered header range candidate is the header data region
  `[8, 8 + header_size)`
- the external source-derived CRC algorithm exists in cached `boxcars 0.11.1` source, but it is
  not a MIMIR implementation and is not a project dependency
- the first body/content CRC candidate at offset `13212` remains outside minimal header parsing

Policy admitted for first minimal implementation planning:

- the minimal MIMIR header reader may read and expose neither CRC value; it only uses
  `header_size` to bound the header region
- header CRC validation is deferred unless a later pass explicitly admits the exact algorithm,
  covered byte range, and fixture validation result or implements a verified in-project checker
- content/body CRC validation is outside `ReplayReader::read_header(&ReplayInput)` and must not
  be enforced by the minimal header reader
- while validation is deferred, CRC mismatch behavior is not observable and must not be claimed
- if CRC validation is later reopened and enforced, CRC mismatch must be a hard error; silent CRC
  mismatch acceptance under an enforced policy is forbidden

Remaining blocker:

- enforced CRC validation remains unadmitted

## K. Property Validation Policy Decision

Property validation policy status:

- partial

Admitted for first minimal top-level header parsing:

| Target | Admitted policy |
| --- | --- |
| duplicate selected mapping keys | hard replay-header mapping error, inherited from mapping pass |
| duplicate top-level property names | hard malformed-property error for the first minimal parser; first/last overwrite is forbidden |
| selected property names | only admitted selected keys may map to `ReplayHeader` fields or metadata |
| non-selected property names | may be skipped if kind is admitted and `property_size` stays within header bounds |
| unknown property kind | hard unsupported-property or malformed-property error |
| property size field | must be present; value range must stay within `header_data_end_exclusive`; selected scalar kinds must consume exactly the expected bytes |
| ignored four-byte field | must be present; value is not interpreted; nonzero is not a failure under current evidence |
| `StrProperty` / `NameProperty` | selected values use non-negative Windows-1252 `parse_text` with trailing NUL; malformed length or missing NUL is hard malformed-text |
| `IntProperty` | selected values require exactly four bytes and are read as `i32_little_endian` |
| `FloatProperty` | selected values require exactly four bytes and must be finite before mapping to `FieldValue::Float` |
| `QWordProperty` | value shape is eight bytes; mapping to `FieldValue::Integer` is admitted only for future selected keys if non-overflowing |
| `ArrayProperty` | non-selected top-level value may be skipped by bounded `property_size`; selected arrays are not admitted |
| terminator | key text exactly `None`; terminator end must equal `header_data_end_exclusive` |

Rejected:

- silent duplicate overwrite
- silent unsupported kind skip
- silent wrong-kind conversion
- selected-value omission after malformed selected bytes
- interpreting array payloads as ReplayHeader metadata
- treating property-size overflow as recoverable

Remaining blockers:

- nested array/property semantics are not fully validated
- unencountered property kinds remain unsupported
- UTF-16 text value support remains unadmitted for the first minimal parser

## L. Parser Stop Behavior Decision

Parser stop behavior status:

- admitted for the first minimal header reader

Admitted minimal stop policy:

- `ReplayReader::read_header(&ReplayInput)` reads only enough bytes to parse the admitted header
  region and selected mappings
- the parser stops at `header_data_end_exclusive = 8 + header_size`
- the parser must not parse raw-state payloads
- the parser must not parse replay frames
- the parser must not parse semantic replay events
- the parser must not parse body/footer structures
- the parser does not need to read `content_size` or `content_crc` to produce a minimal
  `ReplayHeader`
- trailing bytes after `header_data_end_exclusive` are allowed and do not cause failure
- an input that contains the complete admitted header region but no body bytes is not rejected by
  the minimal header stop policy
- the first body boundary candidate is retained only to show that the fixture header end aligns
  with the next externally reported body field

Header-size consistency policy:

- `header_size` must be non-negative
- `8 + header_size` must not overflow `usize`
- `8 + header_size` must be no greater than the input byte length
- the terminator end must equal `8 + header_size`
- `header_size` smaller than the required parsed header region is a hard malformed or
  insufficient error
- `header_size` larger than available bytes is a hard insufficient error

## M. Insufficient-Byte Boundary Decision

Insufficient-byte boundary status:

- policy admitted for admitted fields; evidence remains partial overall

Admitted hard insufficient behavior:

| Boundary | Behavior |
| --- | --- |
| fewer than 4 bytes for `header_size` | hard insufficient replay-header error |
| fewer than 8 bytes for `header_size + header_crc` | hard insufficient replay-header error |
| `header_size` larger than available bytes after prefix | hard insufficient replay-header error |
| insufficient bytes for version fields | hard insufficient replay-header error |
| insufficient bytes for required `net_version` under exact tuple parsing | hard insufficient replay-header error |
| insufficient bytes for game type text length or bytes | hard insufficient replay-header error |
| insufficient bytes for property key length or bytes | hard insufficient replay-header error |
| insufficient bytes for property kind length or bytes | hard insufficient replay-header error |
| insufficient bytes for property size field | hard insufficient property error |
| insufficient bytes for ignored four-byte field | hard insufficient property error |
| insufficient bytes for selected property values | hard insufficient property error |
| insufficient bytes to reach terminator before header end | hard insufficient or malformed header error, depending on the exact boundary reached |
| property value range extends beyond header end | hard malformed property boundary error |
| `header_size` smaller than required parsed region | hard malformed header error |

No recovery, padding, or zero-fill is admitted for insufficient bytes.

Remaining blocker:

- no MIMIR malformed/insufficient fixture suite exists yet; this is policy admission, not tested
  parser behavior

## N. Malformed-Byte Boundary Decision

Malformed-byte boundary status:

- partial

Admitted hard malformed behavior:

| Boundary | Behavior |
| --- | --- |
| negative `header_size` | hard malformed header error |
| `8 + header_size` overflow | hard malformed header error |
| impossible `header_size` that cannot contain version/game/property terminator | hard malformed header error |
| malformed UTF-8 property key or kind | hard malformed text/property error |
| missing NUL terminator in admitted key, kind, game type, `Str`, or `Name` text | hard malformed text/property error |
| `parse_text` length outside admitted bounds | hard malformed text/property error |
| negative UTF-16 `parse_text` length | unsupported text encoding for first minimal parser unless a later pass admits UTF-16 support |
| malformed property size or value range overflow | hard malformed property error |
| unsupported property kind | hard unsupported-property error |
| malformed `Int`, `Float`, or `QWord` byte length | hard malformed property error |
| non-finite selected `Float` | hard replay-header mapping error |
| missing terminator before header end | hard malformed header error |
| terminator end before or after `header_data_end_exclusive` | hard malformed header error |
| contradictory body boundary if body fields are read in a later pass | hard malformed boundary error; not read in the minimal parser |

Remaining blockers:

- nested array malformed semantics remain unadmitted
- CRC mismatch semantics remain unadmitted while CRC validation is deferred
- UTF-16 text support remains unadmitted

## O. Unsupported-Version Boundary Decision

Unsupported-version boundary status:

- admitted for distinguishable exact-tuple rejection

Distinguishing policy:

- if prefix, version fields, game type, terminator, and required version properties cannot be
  structurally parsed, the error is insufficient or malformed
- if those fields parse structurally and the tuple is outside the exact admitted supported tuple,
  the error is unsupported-version
- no broad Rocket League version compatibility is admitted from external parser success
- no fallback to best-effort parsing for unsupported versions is admitted
- no silent acceptance of unknown version or game type is admitted

## P. Typed Replay Error Taxonomy Decision

Typed replay error taxonomy decision:

- not required before the first minimal parser implementation reopen
- still deferred

Rationale:

- the current public parser target is already `Result<ReplayHeader>`
- the current workspace uses `MimirError::Message(String)` for domain validation failures in
  nearby crates
- no current consumer can type-match replay parse failures
- this pass is forbidden from modifying `mimir_core::MimirError`

Required compensating policy:

- future first-pass parser errors must use stable message category prefixes
- message text must include the boundary class and the affected field, property, or offset where
  known
- parser implementation tests must assert the intended boundary category text if typed errors
  remain unavailable

Typed replay errors should be reopened before broad replay ingestion, retry/recovery logic, or any
consumer that needs machine-actionable replay failure classification.

## Q. Complete, Partial, Missing, And Rejected Status

| Evidence or policy target | Status | Notes |
| --- | --- | --- |
| fixture identity | complete | path exists, byte length and SHA-256 match |
| report identities | complete | prior report, structural report, and mapping/error-boundary artifact exist |
| current error surface inspection | complete | `MimirError::Message` is the only domain carrier |
| expected fixture `ReplayHeader` evidence | complete | expected-output evidence only, not parser output |
| top-level prefix byte layout | complete for fixture/minimal target | offsets, lengths, encodings, values admitted |
| header version/game byte layout | complete for exact fixture tuple | broad version-family support not admitted |
| property table start and terminator | complete for fixture/minimal target | terminator must match header end |
| selected property byte ranges | complete for fixture expected-output mapping | inherited from structural and mapping admissions |
| property entry structure | partial | top-level structure admitted; nested arrays and unencountered kinds remain unadmitted |
| property key and kind encoding | partial | UTF-8 parse_str admitted; malformed policy admitted; UTF-16 text values remain unadmitted |
| property size policy | partial | bounded top-level skip/consume admitted; source says size cannot be trusted broadly |
| ignored four-byte field policy | complete for minimal target | field must exist; no semantic validation |
| value encoding for `Str`, `Name`, `Int`, `Float`, `QWord` | complete for admitted top-level selected/scalar use | selected mapping already admitted |
| value encoding for `Array` | partial | top-level skip by size admitted; nested semantics missing |
| body boundary | partial | stop candidate only; no body parse |
| supported-version policy | partial | exact fixture tuple admitted; broad family missing |
| CRC policy | partial | read-but-defer admitted; enforced validation missing |
| full property validation policy | partial | top-level minimal policy admitted; nested arrays/unencountered kinds missing |
| parser stop behavior | complete for minimal header reader | stop at `8 + header_size`, do not read body payload |
| insufficient-byte boundaries | partial | policy admitted for admitted fields; no MIMIR parser tests or implementation |
| malformed-byte boundaries | partial | policy admitted for many boundaries; nested arrays, UTF-16, CRC mismatch remain unadmitted |
| unsupported-version boundary | complete for exact-tuple distinction | only after structural version fields parse |
| typed replay error taxonomy | deferred | not required before first minimal implementation |
| parser implementation | closed | not reopened by this pass |
| parser-success logic | closed | not reopened by this pass |

## R. Outcome B Policy Table

| Target | Valid input policy | Insufficient behavior | Malformed behavior | Unsupported behavior if applicable | Admitted status | Remaining blocker |
| --- | --- | --- | --- | --- | --- | --- |
| `ReplayInput` | `ReplayInput::Memory` with non-empty label and bytes | empty or too-short bytes fail at first missing field | empty label is input/mapping error | `ReplayInput::File` unsupported for first parser | partial | file input remains closed |
| `header_size`/`header_crc` prefix | 8-byte prefix, `i32` size, `u32` CRC | fewer than 8 bytes hard insufficient | negative size or overflow hard malformed | not applicable | complete for minimal target | CRC enforcement deferred |
| header region | `header_end = 8 + header_size`, available in memory | header region beyond input hard insufficient | header too small or contradictory hard malformed | not applicable | complete for minimal target | no parser code yet |
| version/game tuple | exact admitted tuple `868/32/Some(10)/TAGame.Replay_Soccar_TA` plus `ReplayVersion=8`, `BuildVersion=241206.55345.468477` | missing version bytes hard insufficient | malformed game/version properties hard malformed | structurally parsed different tuple hard unsupported-version | partial | broad version-family support missing |
| property key/kind text | length-prefixed UTF-8 with trailing NUL | truncated length or bytes hard insufficient | invalid UTF-8 or missing NUL hard malformed | unsupported kind hard unsupported-property | partial | unencountered kind support missing |
| selected scalar values | exact admitted kinds and sizes | truncated value hard insufficient | wrong size, wrong kind, non-finite selected float hard error | selected `Array` unsupported for mapping | complete for selected mappings | parser implementation closed |
| non-selected properties | recognized kind, bounded `property_size`, no duplicate name | truncated value hard insufficient | overflow or duplicate hard malformed | unrecognized kind hard unsupported-property | partial | nested array validation missing |
| arrays | top-level non-selected value may be skipped by bounded `property_size` | truncated array range hard insufficient | range overflow hard malformed | selected array unsupported | partial | nested array semantics missing |
| terminator | key exactly `None`, end equals header end | missing bytes before terminator hard insufficient | missing/misplaced terminator hard malformed | not applicable | complete for minimal target | no parser code yet |
| CRC | fields read as layout only | truncated prefix/body field if read hard insufficient | not enforced while deferred | not applicable | partial | no admitted MIMIR CRC validation |
| parser stop | stop at header end; body ignored | complete header only is enough | terminator/header-end mismatch hard malformed | not applicable | complete for minimal target | body parsing remains closed |
| error surface | `MimirError::Message` with stable category text | category text must say insufficient | category text must say malformed | category text must say unsupported | partial | typed taxonomy deferred |

## S. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

Implementation may not proceed from this pass because the selected outcome is Outcome B and these
gaps remain:

1. enforced CRC validation is not admitted
2. nested `ArrayProperty` semantics remain unadmitted
3. unencountered property kinds remain unsupported by policy
4. malformed-boundary evidence remains partial for UTF-16 text, nested arrays, and CRC mismatch
5. no parser implementation reopen decision has been made

## T. No-Fake-Evidence Rules

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
- silent duplicate overwrite
- silent unsupported-kind skip
- silent malformed-value omission

External parser/tool success is not MIMIR parser success.

The structural report is not MIMIR parser output.

## U. What Remains Closed

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

## V. What Remains Forbidden

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

## W. Next Stage

The next pass must target the remaining precise gaps before parser implementation can be reopened:

1. decide whether the first implementation may permanently defer CRC validation or must first
   admit an in-project CRC algorithm/range check
2. decide whether top-level `ArrayProperty` skip-by-size is sufficient for the first minimal
   parser or whether nested array dictionary validation must be admitted first
3. decide whether UTF-16 `parse_text` remains unsupported for the first implementation or must be
   admitted before parser code
4. decide whether unsupported unencountered property kinds are acceptable first-pass hard errors
   or need fixture-backed support
5. only after those gaps are closed, run an explicit parser implementation planning reopen pass

Parser implementation is allowed only if fixture evidence, complete byte-layout evidence, complete
expected output evidence, and required error boundaries are admitted, and implementation is
explicitly reopened.
