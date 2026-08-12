# MIMIR Skill Forge BC Replay Header Parser Implementation Planning Reopen v1

Pass date: 2026-05-02

## A. Purpose

This pass reopens implementation planning for the first minimal MIMIR Rocket League replay header
parser for the already admitted private-local fixture:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- parser target: `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

This is a planning/admission pass only. It does not implement parser code, does not implement
parser-success logic, does not produce a `ReplayHeader`, does not add a replay parser backend, and
does not widen `mimir_export`.

## B. Current Fixture Summary

Fixture identity was reverified during this pass.

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

Fixture path, filename, provenance, byte length, and SHA-256 remain identity/integrity facts only.
They are not parser facts and must not be used to derive `replay_id`, `source_label`,
`total_frames`, metadata, byte layout, supported version, or CRC validity.

Required evidence inputs were verified:

- prior external parser report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`
- structural report:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_structural_report.txt`
- structural admission:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_STRUCTURAL_REPORT_ADMISSION_V1.md`
- mapping/error-boundary admission:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_MAPPING_GAP_ERROR_BOUNDARY_ADMISSION_V1.md`
- non-mapping byte-layout/error-boundary admission:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_NON_MAPPING_BYTE_LAYOUT_ERROR_BOUNDARY_ADMISSION_V1.md`
- pre-implementation gap closure:
  `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_PRE_IMPLEMENTATION_GAP_CLOSURE_V1.md`
- pre-implementation decision/next/status artifacts

## C. Current Rust Surface Inspection

Inspected source:

- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-core/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `crates/mimir-replay/Cargo.toml`

Current replay surface:

- `ReplayInput` variants:
  - `File(PathBuf)`
  - `Memory { label: String, bytes: Vec<u8> }`
- `ReplayHeader` fields:
  - `replay_id: ReplayId`
  - `source_label: String`
  - `total_frames: Option<u32>`
  - `metadata: Metadata`
- `ReplayReader` trait:
  - `fn read_header(&self, input: &ReplayInput) -> Result<ReplayHeader>`
- `UnsupportedReplayReader`:
  - zero-sized public reader
  - currently always returns `Err(MimirError::message(...))`
  - is used by `mimir-skill` to truthfully record an unsupported parser-attempt result
- current `MimirError` variants:
  - `Io { path, source }`
  - `Json(serde_json::Error)`
  - `TomlSerialize(toml::ser::Error)`
  - `TomlDeserialize(toml::de::Error)`
  - `Message(String)`

Current `mimir-replay` dependencies are only:

- `mimir-core`
- `mimir-types`
- `serde`

No replay backend dependency is present. The planned parser can be implemented in
`crates/mimir-replay/src/lib.rs` using only existing dependencies and the Rust standard library.
No manifest or lockfile change is required.

## D. Selected Outcome

Selected outcome:

- Outcome A

Implementation planning is explicitly reopened because the first implementation can be strictly
bounded to the already admitted minimal header parser:

- one fixture identity/evidence chain
- one public parser surface
- one first input variant
- exact supported version tuple only
- header-only stop boundary
- explicit unsupported/deferred behavior for CRC, selected arrays, UTF-16, unknown kinds, file
  input, body parsing, raw-state parsing, frame extraction, and semantic events

Actual parser code remains deferred to the next implementation pass.

Parser-success logic remains closed in this pass. The next pass may implement and test only the
first minimal `ReplayInput::Memory` header parser admitted here.

## E. Exact Parser Implementation Boundary

Next implementation pass may modify only:

- `crates/mimir-replay/src/lib.rs`

Next implementation pass must not modify:

- `mimir-io`
- `mimir-export`
- `mimir-types`
- `Cargo.toml`
- `Cargo.lock`
- CLI or runtime code
- MIMIR export code

Next implementation pass must add:

- no dependencies
- no new crates
- no backend replay parser dependency
- no manifest change
- no lockfile change

Tests for the first parser must be unit tests inside `crates/mimir-replay/src/lib.rs`. Test helper
functions may be private to the same file only.

## F. Public API Decision

Chosen public API plan:

- add `pub struct MinimalReplayHeaderReader;`
- implement `ReplayReader` for `MinimalReplayHeaderReader`
- keep `UnsupportedReplayReader` unchanged

Rationale:

- `UnsupportedReplayReader` has truthful existing semantics and is used by `mimir-skill` to record
  a no-parser unsupported attempt.
- Changing `UnsupportedReplayReader` into a parser would make existing unsupported-attempt
  contracts misleading.
- A new zero-sized reader provides explicit opt-in to the minimal parser without touching existing
  callers.

Rejected public API plan:

- modifying `UnsupportedReplayReader` into a parser

No public convenience function is admitted in this pass. The admitted public parser entry remains
trait-based: `MinimalReplayHeaderReader.read_header(&ReplayInput)`.

## G. Private Implementation Structure Plan

Private helper functions and types may be module-local inside `crates/mimir-replay/src/lib.rs`.

Admitted private helper structure:

- `struct HeaderCursor<'a>`
  - `bytes: &'a [u8]`
  - `offset: usize`

Admitted private helper methods:

- `remaining() -> usize`
- `position() -> usize`
- `read_exact(len, context) -> Result<&'a [u8]>`
- `read_i32_le(context) -> Result<i32>`
- `read_u32_le(context) -> Result<u32>`
- `read_f32_le(context) -> Result<f32>`
- `read_parse_str_utf8_nul(context) -> Result<String>`
- `read_parse_text_windows1252_nul(context) -> Result<String>`
- `skip_bounded(len, context) -> Result<()>`

Admitted private parser entry:

- `fn parse_replay_header_from_memory(label: &str, bytes: &[u8]) -> Result<ReplayHeader>`

The Windows-1252 text helper may use an explicit in-file byte-to-`char` mapping for the first
minimal parser. UTF-16/negative-length text remains unsupported. No dependency-backed decoder is
admitted.

## H. Exact Parsing Algorithm Plan

### H.1 Input Boundary

The parser must:

- accept only `ReplayInput::Memory`
- reject `ReplayInput::File` with category:
  `replay header parse error: unsupported-input`
- reject empty memory labels with category:
  `replay header mapping error`
- reject empty or too-short bytes with category:
  `replay header parse error: insufficient`

`ReplayInput::Memory.label` maps directly to `ReplayHeader.source_label`. The fixture path,
filename, byte length, SHA-256, and provenance must not be used as source-label fallbacks.

### H.2 Prefix

The parser must read:

- `header_size: i32` at offset `0`
- `header_crc: u32` at offset `4`

The parser must:

- not validate `header_crc`
- not expose `header_crc`
- compute `header_end = 8 + header_size`
- reject negative `header_size` as malformed
- reject `8 + header_size` overflow as malformed
- reject `header_end > bytes.len()` as insufficient
- stop at `header_end`

`content_crc` must not be read or validated by `read_header`.

### H.3 Header Fields

Inside the header region, the parser must read:

- `major_version: i32`
- `minor_version: i32`
- `net_version: i32`
- `game_type: parse_text Windows-1252 NUL`

The first supported tuple is exact only:

- `major_version = 868`
- `minor_version = 32`
- `net_version = Some(10)`
- `game_type = TAGame.Replay_Soccar_TA`
- selected `ReplayVersion = 8`
- selected `BuildVersion = 241206.55345.468477`

If the version/game fields cannot be structurally parsed, the error category is insufficient or
malformed. If the fields and required version properties parse structurally but differ from the
exact admitted tuple, the error category is:

- `replay header parse error: unsupported-version`

No broad Rocket League replay version-family support is admitted.

### H.4 Property Scan

The parser must scan top-level properties until the terminator key `None`.

Admitted top-level property entry shape:

1. key: `parse_str` UTF-8 NUL
2. if key equals `None`, terminator reached and no kind/size/ignored/value follows
3. kind: `parse_str` UTF-8 NUL
4. `property_size: u32`
5. ignored four-byte field: read as `u32`, not semantically interpreted
6. value: parsed or skipped according to kind and selection policy

The parser must:

- reject duplicate top-level property names
- reject duplicate selected property names as mapping errors
- reject unknown/unencountered property kinds with:
  `replay header parse error: unsupported-property`
- reject property value ranges that overflow or exceed `header_end`
- reject missing terminator
- require terminator end offset to equal `header_end`

Admitted encountered kind handling:

| Kind | Selected handling | Non-selected handling |
| --- | --- | --- |
| `StrProperty` | parse as Windows-1252 `parse_text` | may skip bounded `property_size` |
| `NameProperty` | parse as Windows-1252 `parse_text` | may skip bounded `property_size` |
| `IntProperty` | require `property_size == 4`, parse `i32` | may skip bounded `property_size` |
| `FloatProperty` | require `property_size == 4`, parse finite `f32` | may skip bounded `property_size` |
| `QWordProperty` | no selected key admitted in this pass | may skip bounded `property_size` |
| `ArrayProperty` | unsupported if selected | may skip bounded `property_size` only |

Selected `ArrayProperty` is unsupported. Nested array dictionary semantics are not parsed.

### H.5 Selected Mappings

The parser must map only:

- `Id -> ReplayHeader.replay_id`
- `ReplayInput::Memory.label -> ReplayHeader.source_label`
- `NumFrames -> ReplayHeader.total_frames`
- selected metadata keys:
  - `ReplayName`
  - `Date`
  - `MapName`
  - `ReplayVersion`
  - `BuildVersion`
  - `MaxChannels`
  - `MatchType`
  - `TeamSize`
  - `RecordFPS`

Expected fixture output evidence:

| Destination | Expected value |
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

Mapping policies:

- `Id` is required, must be `StrProperty`, and must be exactly 32 ASCII hex digits.
- `NumFrames` is optional. If present, it must be `IntProperty` and non-negative.
- selected metadata keys may be omitted, except `ReplayVersion` and `BuildVersion` are required
  for the exact supported version tuple check.
- selected metadata wrong-kind, malformed values, selected arrays, non-finite selected floats, and
  duplicate selected names are hard errors.
- non-selected properties do not produce metadata.

### H.6 Stop Boundary

The parser must:

- stop at `header_data_end_exclusive = 8 + header_size`
- require the `None` terminator end to equal `header_data_end_exclusive`
- allow trailing bytes after `header_data_end_exclusive`
- not parse body payloads
- not parse raw-state payloads
- not parse replay frames
- not parse footer structures
- not parse semantic replay events
- not read or validate `content_crc`

## I. Exact Error Category Plan

The first implementation tests must assert stable category substrings:

- `replay header parse error: insufficient`
- `replay header parse error: malformed`
- `replay header parse error: unsupported-version`
- `replay header parse error: unsupported-property`
- `replay header parse error: unsupported-text`
- `replay header parse error: unsupported-input`
- `replay header mapping error`

The implementation must use `MimirError::Message(String)` for these boundaries. Typed
replay-specific errors remain deferred.

Message text should include the boundary class and the affected field, property, or offset where
known.

## J. Exact Test Plan

Next implementation pass must add tests in `crates/mimir-replay/src/lib.rs`.

Happy path fixture test:

- read fixture from `MIMIR_REPLAY_FIXTURE_PATH` if set, otherwise:
  `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- construct `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes }`
- call `MinimalReplayHeaderReader.read_header(&input)`
- assert exact:
  - `replay_id`
  - `source_label`
  - `total_frames`
  - selected metadata values
- assert the parser does not require body parsing beyond the header stop boundary, for example by
  parsing a byte slice truncated exactly at `8 + header_size`
- if the fixture path is missing, the fixture-specific test may skip only with an explicit
  fixture-missing message; deterministic synthetic tests must still run

Required synthetic/error tests:

- rejects `ReplayInput::File` with `unsupported-input`
- rejects empty memory label with `replay header mapping error`
- rejects fewer than 4 bytes with `insufficient`
- rejects fewer than 8 bytes with `insufficient`
- rejects negative `header_size` with `malformed`
- rejects `header_size` larger than available bytes with `insufficient`
- rejects unsupported version tuple with `unsupported-version`
- rejects missing terminator with `malformed`
- rejects duplicate selected property with `replay header mapping error`
- rejects duplicate top-level property with `malformed`
- rejects unknown property kind with `unsupported-property`
- rejects UTF-16/negative text if reachable with synthetic bytes, using `unsupported-text`
- rejects selected `ArrayProperty` with `unsupported-property` or mapping error
- rejects malformed selected float non-finite with `replay header mapping error`
- confirms CRC is not validated; no test may claim CRC validation

Synthetic builders must be deterministic and local to `crates/mimir-replay/src/lib.rs`.

## K. Explicit Non-Goals For The Implementation Pass

The next implementation pass must not:

- validate CRC
- add a replay parser backend dependency
- parse body payloads
- parse raw-state payloads
- extract replay frames
- extract semantic replay events
- parse nested array semantics
- support UTF-16
- support unknown/unencountered property kinds
- support `ReplayInput::File`
- widen export
- modify `mimir-types`
- modify `mimir-export`
- modify `mimir-io`
- modify manifests or lockfile
- add runtime CLI commands
- add async/background systems
- add database code
- add real rollout physics

## L. What Remains Closed

Closed in this pass:

- parser implementation
- parser-success logic
- `ReplayHeader` production or synthesis
- CRC validation
- body parsing
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

## M. What Remains Forbidden

Forbidden unless explicitly reopened later:

- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- modifying `Cargo.toml`
- modifying `Cargo.lock`
- adding backend replay parser dependencies
- using `boxcars`, `rattletrap`, `rrrocket`, `carball`, `rlreplay`, `subtr-actor`, or any other
  replay parser dependency
- claiming CRC validation
- claiming broad version-family support
- claiming parser success before implementation tests exist
- treating fixture path, filename, provenance, byte length, or SHA-256 as parser facts

## N. Next Stage

Next pass may implement the first minimal parser, limited to:

- `crates/mimir-replay/src/lib.rs` only
- `MinimalReplayHeaderReader`
- `ReplayInput::Memory` only
- exact fixture tuple only
- header-only parsing ending at `8 + header_size`
- tests required by this artifact

If the next pass attempts to reopen CRC enforcement, UTF-16, nested arrays, unknown property kinds,
`ReplayInput::File`, body parsing, raw-state parsing, frame extraction, semantic events,
replay-source materialization, replay-input locator logic, export widening, or manifest changes,
the minimal parser implementation must remain blocked until that topic is separately admitted.
