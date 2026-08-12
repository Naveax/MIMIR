# MIMIR Skill Forge BC Replay Header Parser Approved Report Admission v1

## A. Purpose

This pass admits, partially admits, or rejects the generated external parser/tool report for the
already admitted private-local Rocket League replay fixture:

- fixture id: `rl_replay_header_fixture_001`
- report path: `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`

This is an evidence-admission pass only. It does not implement parser code, does not implement
parser-success logic, does not produce or synthesize a `ReplayHeader`, and does not parse
raw-state payloads, replay frames, or semantic replay events.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains exactly:

- `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes: <fixture bytes> }`

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Rocket League replay header parsing remains a shared `mimir-replay` capability candidate. This
pass does not create a generic replay, raw-state, frame, event, export, materialization, carrier,
locator, database, runtime CLI, async/background, rollout, physics, or corpus framework.

`mimir_export` widening remains forbidden.

## C. Current Fixture Summary

The fixture identity was reverified before this admission decision.

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |
| admitted future input | `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes: <fixture bytes> }` |

The fixture path, filename, provenance, byte length, and SHA-256 remain fixture integrity facts
only. They are not parser facts.

## D. Report Identity

The report identity was verified from
`artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`.

| Report field | Report value | Admission status |
| --- | --- | --- |
| fixture id | `rl_replay_header_fixture_001` | admitted as report identity |
| parser tool | `boxcars crate` | admitted as report provenance |
| parser tool version | `0.11.1` | admitted as report provenance |
| parser mode | `ParserBuilder::new(bytes).never_parse_network_data().parse()` | admitted as report provenance and scope limit |
| report is MIMIR parser output | `no` | admitted as a non-claim |
| report is parser success | `no` | admitted as a non-claim |
| report is byte-layout admission | `no` | admitted as a non-claim |

The report is not MIMIR parser output and not MIMIR parser-success evidence.

## E. Selected Outcome

Selected outcome:

- Outcome B

Outcome B means:

- the report is partially admissible
- only report-backed facts are admitted or partially admitted
- complete byte-layout evidence is not admitted
- complete expected `ReplayHeader` evidence is not admitted
- parser implementation remains closed
- parser-success logic remains closed
- the next pass must target the remaining evidence gaps

Outcome A is rejected because the report does not provide complete byte-level accounting, field
encodings, numeric endianness, string/property encoding rules, parser error boundaries, or a full
expected `ReplayHeader` mapping.

Outcome C is rejected because the report has useful bounded fixture-specific external parser facts:
tool identity, fixture identity, network-skip scope, external parse success, a reported
`header_size`, reported version fields, and selected reported header properties.

Outcome D is rejected because admission is bounded by one report path, one fixture id, one
private-local fixture identity, one external parser/tool route, and explicit non-integration rules.

## F. Report Section Classification

| Report section | Report lines/fields | Classification | Admission result |
| --- | --- | --- | --- |
| report metadata | lines 3-13, `REPORT STATUS` | admissible report provenance and non-claims | admitted as report identity/scope only |
| fixture identity | lines 15-22, `FIXTURE IDENTITY` | admissible fixture-integrity cross-check | admitted as fixture identity only, not parser facts |
| external tool recognition | lines 24-27, `TOOL RECOGNITION` | partial external tool recognition evidence | partial; not a MIMIR parser admission rule |
| byte-backed external parse summary | lines 29-50, `BYTE-BACKED EXTERNAL PARSE SUMMARY` | partial external parser field/property evidence | partial; no offsets, encodings, endianness, or MIMIR mapping admitted |
| selected header properties | lines 40-50, selected property fields | partial external header property evidence | partial; not yet a metadata map or `ReplayHeader` output |
| body/footer data read by external tool | lines 52-64, `BODY/FOOTER DATA READ BY EXTERNAL TOOL` | diagnostic-only and explicitly not MIMIR header evidence | rejected for byte-layout and expected-output admission |
| network/frame/event limits | lines 66-71, `NETWORK / FRAME / EVENT LIMITS` | admissible report-scope negative limits | admitted as report boundary facts only |
| sufficiency limits | lines 73-80, `SUFFICIENCY LIMITS` | admissible report limitation evidence | admitted as limitation evidence; confirms remaining gaps |

## G. Admitted Evidence

The following facts are admitted, with narrow scope:

| Evidence | Scope | Destination | Limitation |
| --- | --- | --- | --- |
| report was generated by a temporary external Rust crate outside the MIMIR workspace | report provenance only | evidence chain | not parser code and not a dependency |
| report used `boxcars 0.11.1` | report provenance only | evidence chain | not backend selection |
| report parser mode was `ParserBuilder::new(bytes).never_parse_network_data().parse()` | report provenance and scope only | evidence chain | still a broad external parse, not MIMIR header parsing |
| report says it is not MIMIR parser output, not parser success, and not byte-layout admission | non-claim | evidence chain | prevents false parser-success admission |
| fixture identity in the report matches the verified local path, length, and SHA-256 | fixture identity only | evidence chain | not parser facts |
| report says no network frames, replay frames, raw-state payloads, or semantic replay events were extracted | report boundary only | evidence chain | does not prove MIMIR parser behavior |
| future input label is `rl_replay_header_fixture_001` for admitted `ReplayInput::Memory` | fixture/input contract only | `ReplayHeader.source_label` candidate | source-label evidence only; not a complete `ReplayHeader` |

## H. Partial Or Unapproved Evidence

The following report-backed facts are useful but only partially admitted. They must not be treated
as complete byte-layout or expected-output evidence.

| Evidence target | Report source line/field name | Admitted status | Scope | Destination | Remaining blocker |
| --- | --- | --- | --- | --- | --- |
| external Rocket League replay recognition | line 25 `boxcars_parse_result`, line 26 `recognized_as_rocket_league_replay` | partial | fixture-only | parser admission | external parse success is not a MIMIR admission rule; supported format rule is still missing |
| supported format/version family | lines 32-35 `major_version`, `minor_version`, `net_version`, `game_type`; lines 44-45 `ReplayVersion`, `BuildVersion` | partial | fixture-only | parser admission | no admitted supported-version policy or unsupported-version boundary |
| header boundary | line 30 `header_size: 13200` | partial | fixture-only | parser admission | no byte offset, encoding, termination rule, or independent header/body boundary proof |
| header CRC | line 31 `header_crc: 2370383193` | partial | fixture-only | diagnostic/parser admission candidate | no CRC field layout, byte span, endianness, or validation policy |
| header property count | line 36 `header_property_count: 26` | partial | fixture-only | parser admission | no property table encoding or termination rule |
| property kind counts | line 37 `property_kind_counts` | partial | fixture-only | parser admission | no field encoding map or ordering proof |
| replay id source | line 40 `Id` | partial | fixture-only | `ReplayHeader.replay_id` | no structural path/offset, encoding rule, validation rule, or admitted mapping policy |
| replay display name metadata | line 41 `ReplayName` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no property encoding map |
| replay date metadata | line 42 `Date` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no date/value normalization policy |
| map metadata | line 43 `MapName` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no property encoding map |
| replay version metadata candidate | line 44 `ReplayVersion` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no supported-version policy |
| build version metadata candidate | line 45 `BuildVersion` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no string encoding map |
| total frame source | line 46 `NumFrames` | partial | fixture-only | `ReplayHeader.total_frames` | no admitted mapping policy from `NumFrames` to `total_frames`; no structural path/offset |
| max channels metadata candidate | line 47 `MaxChannels` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no property encoding map |
| match type metadata candidate | line 48 `MatchType` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no property encoding map |
| team size metadata candidate | line 49 `TeamSize` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no property encoding map |
| record FPS metadata candidate | line 50 `RecordFPS` | partial | fixture-only | `ReplayHeader.metadata` | no metadata key policy and no float encoding/range policy |

No byte offsets are admitted by this table.

## I. Rejected Diagnostic-Only Facts

The following report facts are not admitted as byte-layout or expected `ReplayHeader` evidence:

| Report field | Classification | Rejection reason |
| --- | --- | --- |
| line 17 `input_path` | fixture identity only | path is not a parser fact or locator rule |
| lines 18-21 byte length and SHA-256 | fixture integrity only | integrity facts are not layout, replay id, frame count, or metadata |
| lines 53-63 body/footer counts | diagnostic-only | report explicitly says body/footer values are not MIMIR header evidence |
| line 64 `body_footer_values_are_mimir_header_evidence: no` | limitation evidence | confirms rejection of body/footer counts for header admission |
| line 74 `sufficient_for_mimir_byte_layout_admission_now: no` | limitation evidence | confirms incomplete byte-layout evidence |
| line 75 `sufficient_to_implement_mimir_parser_now: no` | limitation evidence | confirms implementation remains blocked |
| lines 76-80 replay id, total frames, metadata, malformed/unsupported policies | limitation evidence | confirms those policies are not admitted by the report itself |

## J. Byte-Accounting Map Status

Byte-accounting status:

- partial only
- no complete byte-accounting map is admitted

Admitted byte-accounting facts:

- none with byte offsets
- none with field byte lengths
- none with numeric endianness
- none with string/property encoding rules
- none with header termination logic
- none with structured parser error boundaries

Partial fixture-only external facts:

| Target | Partial external value | Status |
| --- | --- | --- |
| header size candidate | `13200` | partial, not a termination rule |
| header CRC candidate | `2370383193` | partial, no span or encoding admitted |
| major version | `868` | partial, no encoding or supported-version policy admitted |
| minor version | `32` | partial, no encoding or supported-version policy admitted |
| net version | `Some(10)` | partial, no encoding or supported-version policy admitted |
| game type | `TAGame.Replay_Soccar_TA` | partial, no string encoding or admission policy admitted |
| header property count | `26` | partial, no property encoding or terminator admitted |

## K. Expected ReplayHeader Evidence Status

Expected `ReplayHeader` evidence status:

- partial only

Field status:

| `ReplayHeader` field | Status | Reason |
| --- | --- | --- |
| `replay_id` | partial | `Id` is an external parser-reported property only; no structural path/offset or mapping policy is admitted |
| `source_label` | admitted for the future admitted memory input only | source label can come from `ReplayInput::Memory.label`, expected as `rl_replay_header_fixture_001` |
| `total_frames` | partial | `NumFrames` is an external parser-reported property only; no mapping policy to `ReplayHeader.total_frames` is admitted |
| `metadata` | partial | selected properties are external parser-reported property values only; no metadata key map or empty metadata policy is admitted |

No complete `ReplayHeader` is admitted.

## L. Replay Id Evidence Status

Replay id evidence status:

- partial only

Partial report-backed value:

- line 40 `Id: kind=Str, value="7F59297811EFD8B19C444A81FB07660C"`

This value is not admitted as `ReplayHeader.replay_id` because the report does not provide:

- byte offset or structural path
- string/property encoding rule
- validation rule
- replay id derivation policy
- proof that MIMIR should map `Id` directly to `ReplayHeader.replay_id`

Replay id must not be derived from fixture id, path, filename, provenance, byte length, or SHA-256.

## M. Source Label Evidence Status

Source-label evidence status:

- admitted only from the admitted future input contract

Expected future source label for the first admitted parser input:

- `rl_replay_header_fixture_001`

This is not byte-layout evidence. It does not imply parser success. It only records that a future
successful `ReplayReader::read_header` call over the admitted `ReplayInput::Memory` may copy the
input label into `ReplayHeader.source_label`.

## N. Total Frames Evidence Status

Total-frames evidence status:

- partial only

Partial report-backed value:

- line 46 `NumFrames: kind=Int, value=13555`

This value is not admitted as `ReplayHeader.total_frames` because the report does not provide:

- byte offset or structural path
- integer encoding or endianness
- property encoding rule
- value range policy
- admitted mapping policy from `NumFrames` to `ReplayHeader.total_frames`

No `None` policy is admitted.

## O. Metadata Evidence Status

Metadata evidence status:

- partial only

The selected properties on lines 41-50 are partially admitted as external parser-reported header
property facts. They are not admitted as a MIMIR metadata map.

Missing metadata evidence:

- admitted key map
- admitted key names
- value type mapping to `mimir_types::FieldValue`
- string/name/integer/float encoding rules
- default/empty metadata policy
- omission policy
- unsupported or malformed metadata behavior

Body/footer structural counts are not admitted as metadata.

## P. Error-Boundary Evidence Status

Error-boundary evidence status:

- not admitted

Missing boundaries:

- insufficient bytes
- malformed bytes
- unsupported format/version, if distinguishable
- invalid header field values
- invalid property encodings
- invalid or missing replay id
- invalid or missing total frame source
- invalid metadata mapping

The report's successful external parse of one fixture does not define MIMIR parser failure
semantics.

## Q. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

Implementation may not proceed from this pass because:

1. complete byte-layout evidence is not admitted
2. no byte offsets or field byte lengths are admitted
3. numeric endianness is not admitted
4. string/property encoding rules are not admitted
5. `ReplayHeader.replay_id` mapping remains partial
6. `ReplayHeader.total_frames` mapping remains partial
7. `ReplayHeader.metadata` mapping remains partial
8. insufficient, malformed, and unsupported error boundaries remain missing

## R. No-Fake-Evidence Rules

This pass admits no invented:

- magic bytes
- offsets
- field lengths
- endianness
- version layout
- header termination rule
- property encoding rule
- replay id derivation
- total frame derivation
- metadata key map
- parser-success fixture output
- insufficient-byte fixture
- malformed-byte fixture
- unsupported-format fixture

The external boxcars report is not MIMIR parser output.

The external boxcars parse success is not MIMIR parser success.

## S. What Remains Closed

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
- replay-source actual-materialization implementation
- replay-source carrier discovery implementation
- replay-input locator implementation
- corpus-wide replay ingestion
- runtime CLI commands
- async/background systems
- database code
- real rollout physics
- `mimir_export` widening

## T. What Remains Forbidden

Still forbidden unless explicitly reopened:

- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- modifying `Cargo.toml`
- modifying `Cargo.lock`
- adding backend dependencies to MIMIR
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

## U. Next Stage

Immediate next pass:

- remaining evidence-gap pass for `rl_replay_header_fixture_001`

The next pass should request or generate narrower byte-layout evidence that identifies:

- header field offsets or structural paths
- field lengths
- numeric endianness
- string/property encoding rules
- header termination or body boundary
- supported-version policy
- replay id mapping policy
- total frame mapping policy
- metadata key map or explicit empty metadata policy
- insufficient, malformed, and unsupported-if-distinguishable error boundaries

Parser implementation is not the next pass.

Parser implementation is allowed only after fixture evidence, complete byte-layout evidence, and
complete expected `ReplayHeader` output evidence are admitted by later passes and implementation is
explicitly reopened.
