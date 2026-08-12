# MIMIR Skill Forge BC Replay Header Parser First Minimal Implementation Audit v1

Pass date: 2026-05-04

## Purpose

This pass audits the first minimal `MinimalReplayHeaderReader` implementation against the
previously admitted parser boundary for:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- admission form: `PRIVATE_LOCAL_PATH_WITH_HASH`

This is an audit/admission pass only. It does not broaden parser scope, add parser functionality,
modify runtime callers, widen export behavior, add CRC validation, or parse body/raw-state/frame/event
data.

## Selected Outcome

Selected outcome:

- Outcome A

The implementation is admitted as matching the first minimal parser boundary.

Parser-success remains admitted only for:

- `ReplayInput::Memory`
- the exact fixture-supported tuple
- header-only parsing ending at `8 + header_size`

Parser-success is not admitted broadly.

## Fixture Verification

Fixture identity was reverified during this audit:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |

The implementation does not use the fixture path, filename, byte length, or SHA-256 as parser facts.
The fixture path is used only by the fixture-specific test loader to read bytes.

## Public API Audit

Admitted API facts:

- `pub struct MinimalReplayHeaderReader;` exists.
- `impl ReplayReader for MinimalReplayHeaderReader` exists.
- The implementation accepts only `ReplayInput::Memory`.
- `ReplayInput::File` returns `replay header parse error: unsupported-input`.
- `UnsupportedReplayReader` still returns the existing unsupported parser message and was not turned
  into a parser.

No convenience API, CLI API, export API, runtime caller, or broad parser interface was added.

## File And Dependency Boundary Audit

Current implementation artifacts match the admitted file boundary:

- Rust implementation is contained in `crates/mimir-replay/src/lib.rs`.
- `crates/mimir-replay/Cargo.toml` remains dependency-limited to `mimir-core`, `mimir-types`, and
  `serde`.
- Root `Cargo.toml` and `Cargo.lock` contain no replay parser backend dependency.
- `mimir-io`, `mimir-export`, and `mimir-types` were not modified by this audit pass.

Dependency scan found no matches for:

- `boxcars`
- `rattletrap`
- `rrrocket`
- `carball`
- `rlreplay`
- `subtr-actor`

Scoped Git diff reported no tracked diffs for the forbidden crate/manifests paths. Caveat: the
workspace is inside a broader Git root at `D:/`, so broad `git status` is not useful evidence for
this MIMIR directory.

## String And Property Encoding Audit

The implementation matches the admitted first minimal string/property evidence:

- Property keys and kinds use length-prefixed trailing-NUL UTF-8 `parse_str`.
- `game_type`, selected `StrProperty`, and selected `NameProperty` values use length-prefixed
  trailing-NUL Windows-1252 `parse_text`.
- Negative length text is rejected with `replay header parse error: unsupported-text`.
- Missing trailing NUL is rejected as malformed.
- Oversized text is rejected before allocation or unbounded read.
- Unsupported text formats are not silently accepted.

The Windows-1252 decoder is local and dependency-free. The fixture values are ASCII within the
admitted Windows-1252 boundary; broader non-ASCII coverage is not admitted by this audit.

`Id` validation accepts exactly 32 ASCII hexadecimal digits. The implementation permits lowercase
hex via `is_ascii_hexdigit`; this remains within the admitted ASCII-hex policy because no
uppercase-only policy was admitted and no case normalization is performed.

## Byte-Layout Audit

The parser byte-layout algorithm matches the admitted boundary:

- `header_size` is read at offset `0` as `i32` little-endian.
- `header_crc` is read at offset `4` as `u32` little-endian.
- `header_crc` is not validated or exposed.
- `header_end = 8 + header_size`.
- Negative `header_size` is rejected as malformed.
- Overflowing or unavailable header regions are rejected.
- Only the header region `[8, header_end)` is parsed.
- The top-level `None` terminator end must equal the header region end.
- Trailing bytes after `header_end` are allowed.
- `content_crc` is not read or validated.

The complete-header-only fixture test proves the current implementation does not require body bytes
to produce the admitted minimal `ReplayHeader`.

## Version Policy Audit

The implementation enforces the exact admitted tuple only:

| Field | Required value |
| --- | --- |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `10` |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| `ReplayVersion` | `8` |
| `BuildVersion` | `241206.55345.468477` |

Structurally parsed but unsupported tuples return:

- `replay header parse error: unsupported-version`

No broad version-family support was added.

## Property And Mapping Audit

The property scan and selected mapping match the admitted first minimal policy:

- Top-level properties are scanned until key `None`.
- Duplicate selected property names are mapping errors.
- Duplicate non-selected top-level property names are malformed parse errors.
- Selected scalar properties are parsed for:
  - `Id`
  - `NumFrames`
  - `ReplayName`
  - `Date`
  - `MapName`
  - `ReplayVersion`
  - `BuildVersion`
  - `MaxChannels`
  - `MatchType`
  - `TeamSize`
  - `RecordFPS`
- Non-selected admitted kinds are skipped only by bounded `property_size`.
- Non-selected top-level `ArrayProperty` is skipped only by bounded `property_size`.
- Selected `ArrayProperty` is rejected.
- Unknown property kinds are rejected.
- Selected wrong-kind, malformed, negative-frame, and non-finite-float values are rejected.
- `QWordProperty` is only recognized for bounded non-selected skip; it is not interpreted for this
  boundary.

Fixture-specific assertions include the exact replay id:

- `7F59297811EFD8B19C444A81FB07660C`

`RecordFPS` is parsed from the admitted four-byte fixture value and asserted as `FieldValue::Float(30.0)`.

## Test Audit

`cargo test -p mimir-replay -- --nocapture` passed:

- `17 passed`
- fixture happy path passed
- complete-header-only stop-boundary passed
- deterministic synthetic error tests passed

Audited tests cover:

- fixture happy path
- complete-header-only stop boundary
- unsupported input
- empty memory label
- fewer than 4 bytes
- fewer than 8 bytes
- negative `header_size`
- `header_size` larger than bytes
- unsupported version tuple
- missing terminator
- duplicate selected property
- duplicate top-level property
- unknown property kind
- UTF-16/negative text
- selected `ArrayProperty`
- selected non-finite float
- CRC non-validation boundary

The fixture-specific test may skip only when the fixture path is missing or unreadable. Synthetic
tests remain deterministic and do not require the external fixture.

## Error Category Audit

Stable category substrings are present and tested:

- `replay header parse error: insufficient`
- `replay header parse error: malformed`
- `replay header parse error: unsupported-version`
- `replay header parse error: unsupported-property`
- `replay header parse error: unsupported-text`
- `replay header parse error: unsupported-input`
- `replay header mapping error`

The implementation uses `MimirError::Message(String)` as admitted for the first minimal boundary.
Typed replay errors remain deferred.

## Non-Goal Audit

The implementation does not add support for:

- CRC validation
- content CRC validation
- body parsing
- raw-state payload parsing
- replay frame extraction
- footer parsing
- semantic event parsing
- nested array semantics
- UTF-16 text support
- `ReplayInput::File` support
- backend parser dependencies
- export integration
- runtime or CLI behavior
- broad replay version support

## Exact Accepted Parser-Success Boundary

Parser-success is admitted only when all of the following hold:

- input is `ReplayInput::Memory`
- memory label is non-empty and maps directly to `ReplayHeader.source_label`
- bytes contain the complete header prefix and header region
- parse stops at `8 + header_size`
- the top-level terminator ends exactly at `8 + header_size`
- the exact supported tuple is present:
  - `major_version = 868`
  - `minor_version = 32`
  - `net_version = 10`
  - `game_type = TAGame.Replay_Soccar_TA`
  - `ReplayVersion = 8`
  - `BuildVersion = 241206.55345.468477`
- selected scalar mappings are structurally valid and admitted

## Exact Remaining Limitations

Still unadmitted:

- broad parser success
- CRC validation
- body parsing
- raw-state payload parsing
- replay frame extraction
- semantic replay events
- nested array semantics
- UTF-16 text decoding
- additional property-kind support
- `ReplayInput::File`
- export widening
- runtime/CLI integration
- broad Rocket League replay version families

## Next Stage

Next pass may be a narrow parser-readiness handoff or integration-planning pass.

No broad parser expansion is admitted yet.
