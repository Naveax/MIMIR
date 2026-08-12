# MIMIR Skill Forge BC Replay Header Parser Remaining Evidence Gap v1

## A. Purpose

This pass narrows the remaining evidence gaps for the admitted private-local Rocket League replay
fixture:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- prior external report path:
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`

This is an evidence-gap pass only. It does not implement MIMIR parser code, does not implement
parser-success logic, does not produce or synthesize a `ReplayHeader`, and does not parse
raw-state payloads, replay frames, or semantic replay events.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains exactly:

- `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes: <fixture bytes> }`

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Rocket League replay header parsing remains only a shared `mimir-replay` capability candidate.
This pass does not create replay-source materialization, carrier discovery, locator logic,
corpus ingestion, runtime CLI behavior, async/background systems, database code, rollout physics,
or export widening.

`mimir_export` widening remains forbidden.

## C. Current Partial Evidence Summary

The previous approved parser-report admission pass selected Outcome B and partially admitted only
fixture/tool/report facts from the generated external `boxcars 0.11.1` report.

Partially retained external facts include:

| Target | Partial value |
| --- | --- |
| `header_size` | `13200` |
| `header_crc` | `2370383193` |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `Some(10)` |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| `header_property_count` | `26` |
| property kind counts | `{"Array": 3, "Float": 3, "Int": 12, "Name": 2, "QWord": 1, "Str": 5}` |
| `Id` | `Str`, `7F59297811EFD8B19C444A81FB07660C` |
| `ReplayName` | `Str`, `Frestyle double touch but not ball` |
| `Date` | `Str`, `2025-01-22 11-10-32` |
| `MapName` | `Name`, `Stadium_Winter_P` |
| `ReplayVersion` | `Int`, `8` |
| `BuildVersion` | `Str`, `241206.55345.468477` |
| `NumFrames` | `Int`, `13555` |
| `MaxChannels` | `Int`, `2047` |
| `MatchType` | `Name`, `Online` |
| `TeamSize` | `Int`, `3` |
| `RecordFPS` | `Float`, `30.0` |

These remain external parser/tool report facts only. They are not MIMIR parser output and not
MIMIR parser-success evidence.

## D. Remaining Gaps Before This Pass

The open evidence gaps before this pass were:

- supported Rocket League replay header admission rule
- supported version or version-family policy
- header boundary or termination rule
- body/raw-state boundary for minimal header parsing
- byte offsets or structural paths
- field byte lengths
- numeric endianness
- string and property encoding rules
- replay id derivation or explicit blocked policy
- `total_frames` derivation or explicit `None` policy
- metadata key map or explicit empty metadata policy
- insufficient-byte boundary
- malformed-byte boundary
- unsupported-format/version boundary, if distinguishable

## E. Re-Audit Result

Required local files were re-audited before this pass changed artifacts:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_APPROVED_REPORT_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_approved_report_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_approved_report_admission_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_approved_report_admission_status.txt`
- `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_EXTERNAL_BYTE_LAYOUT_EVIDENCE_OR_REPORT_ROUTE_DECISION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_BYTE_LAYOUT_EVIDENCE_ADMISSION_V1.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-skill/Cargo.toml`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

The crate surface remains a scaffold. `mimir-replay` exposes `ReplayInput`, `ReplayHeader`,
`ReplayReader`, and `UnsupportedReplayReader`; it does not contain a real parser.

## F. Identity Verification

The fixture and prior report identities were reverified.

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| fixture path exists | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | yes | pass |
| fixture byte length | `3001021` | `3001021` | pass |
| fixture SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | pass |
| prior report path exists | `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt` | yes | pass |

The fixture path, filename, byte length, provenance, and SHA-256 remain fixture identity facts only.
They are not parser facts.

## G. Selected Outcome

Selected outcome:

- Outcome B

Outcome B is selected because the remaining gaps cannot be closed from the prior report alone, but
a bounded external structural report route exists from local cached `boxcars 0.11.1` source and the
already admitted fixture.

Why Outcome A is rejected:

- the prior report does not contain byte offsets, field lengths, complete encodings, complete
  structural paths, or MIMIR mapping policies

Why Outcome C is rejected:

- local cached `boxcars 0.11.1` source is available and supports a narrower source/fixture
  structural report route outside the MIMIR dependency graph

Why Outcome D is rejected:

- the pass remains bounded by one fixture, one prior report, one cached external parser source, one
  generated structural report path, and explicit non-integration rules

## H. Local Boxcars Source Inspection Result

Local cached source was found at:

- `C:\Users\navea\.cargo\registry\src\index.crates.io-1949cf8c6b5b557f\boxcars-0.11.1\src`

Inspected source files:

- `parser.rs`
- `core_parser.rs`
- `header.rs`
- `parsing_utils.rs`
- `models.rs`
- `errors.rs`
- `crc.rs`
- crate `Cargo.toml`

Source-derived evidence classification:

| Source-derived target | Classification | Reason |
| --- | --- | --- |
| parser entrypoint and `never_parse_network_data()` behavior | admissible structural route evidence | source shows `ParserBuilder::parse()` and network parse mode selection |
| top-level header size and CRC read order | admissible structural route evidence | source reads `header_size` then `header_crc` before header parsing |
| primitive integer endianness | admissible structural route evidence | source uses `from_le_bytes` for i32/u32/u64 and f32 |
| header field order | admissible structural route evidence | source reads major, minor, optional net version, game type, then properties |
| property dictionary shape | admissible structural route evidence | source reads key, terminator `None`, kind, property size, ignored 4 bytes, then value by kind |
| string/text decoding rules | admissible structural route evidence | source distinguishes `parse_str` UTF-8 and `parse_text` Windows-1252/UTF-16LE |
| header terminator and body boundary for this fixture | partial generated-only evidence | source plus fixture scan can produce candidates, but later admission must verify them |
| CRC validation policy | partial evidence | source shows external CRC behavior; MIMIR CRC policy remains unadmitted |
| error boundaries | partial evidence | source categories exist, but MIMIR insufficient/malformed/unsupported boundaries remain unadmitted |
| supported Rocket League version policy | not complete | source has a net-version condition and quirks mode, but no MIMIR supported-version policy |
| `Id` to `ReplayHeader.replay_id` mapping | not admitted | source can expose property structure but not MIMIR mapping policy |
| `NumFrames` to `ReplayHeader.total_frames` mapping | not admitted | source comments and property helpers are not an admitted MIMIR field policy |
| metadata key map | not admitted | no MIMIR metadata map is established by source inspection |

## I. Additional Structural Report Route Result

A narrower structural report was generated:

- `artifacts/replay_header_reports/rl_replay_header_fixture_001_structural_report.txt`

Report route:

- temporary external PowerShell structural scanner
- run outside the MIMIR source/dependency graph
- inspected cached `boxcars 0.11.1` source and the admitted fixture bytes
- wrote only a text report artifact under `artifacts/replay_header_reports`
- did not modify MIMIR source code, manifests, lockfile, or forbidden crates

Generated report size:

- `13790` bytes

The structural report explicitly states:

- not MIMIR parser output
- not parser-success evidence
- not parser implementation
- not full byte-layout admission
- later structural report admission pass required
- no raw-state payloads parsed
- no replay frames extracted
- no semantic events extracted
- no `ReplayHeader` synthesized

## J. Generated Structural Evidence Status

The new structural report is generated for later admission only.

Generated report candidates include:

- top-level field offsets for `header_size` and `header_crc`
- header data range candidate `[8, 13208)`
- offsets and raw bytes for major, minor, and net version
- `game_type` offset and string encoding
- top-level property table start offset
- top-level property structural table for 26 properties
- terminator offset and candidate match with the header data end
- first body size/CRC candidate offsets
- selected `Id`, `NumFrames`, and metadata-candidate property structural paths
- source-derived error/boundary candidates

These are not admitted as complete MIMIR byte-layout evidence in this pass.

## K. Newly Admitted Facts

Newly admitted facts in this pass are limited to route and artifact facts:

- fixture identity was reverified
- prior report identity was reverified
- local cached `boxcars 0.11.1` source was available for inspection
- the cached source supports a bounded external structural report route
- a new structural report was generated at
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_structural_report.txt`
- the structural report is generated-only evidence requiring a later admission pass
- parser implementation remains closed

No complete byte-layout facts are admitted here.

No complete expected `ReplayHeader` is admitted here.

## L. Partial Facts Retained

The prior partial fixture-only external facts remain retained, including:

- `header_size: 13200`
- `header_crc: 2370383193`
- `major_version: 868`
- `minor_version: 32`
- `net_version: Some(10)`
- `game_type: TAGame.Replay_Soccar_TA`
- `header_property_count: 26`
- property kind counts: `Array=3`, `Float=3`, `Int=12`, `Name=2`, `QWord=1`, `Str=5`
- selected header properties from the prior external report

The new structural report adds generated candidate offsets and encodings for later admission. It
does not by itself complete the byte-layout or expected-output gate.

## M. Gaps Still Open

Still open after this pass:

- complete supported Rocket League replay header admission rule
- complete supported version or version-family policy
- admitted header boundary or termination rule
- admitted body/raw-state boundary for minimal header parsing
- admitted byte offsets and field lengths
- admitted numeric endianness policy
- admitted string and property encoding rules
- admitted replay id derivation or explicit blocked policy
- admitted `total_frames` derivation or explicit `None` policy
- admitted metadata key map or explicit empty metadata policy
- admitted insufficient-byte boundary
- admitted malformed-byte boundary
- admitted unsupported-format/version boundary, if distinguishable
- complete expected `ReplayHeader` evidence

Several of these now have generated candidates in the structural report, but candidate evidence is
not admission.

## N. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

Implementation may not proceed from this pass because:

1. the new structural report has not been admitted
2. complete MIMIR byte-layout evidence is still not admitted
3. complete expected `ReplayHeader` evidence is still not admitted
4. MIMIR replay id, total frames, and metadata policies are still missing
5. MIMIR insufficient, malformed, and unsupported boundaries are still missing
6. implementation has not been explicitly reopened

## O. What Remains Closed

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

## P. What Remains Forbidden

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

## Q. Next Stage

Immediate next pass:

- structural report admission pass for
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_structural_report.txt`

The next pass must decide which generated structural facts can be admitted, which remain partial,
and which must be rejected. Parser implementation is not the next pass.

Parser implementation is allowed only after fixture evidence, complete byte-layout evidence, and
complete expected `ReplayHeader` evidence are admitted, and implementation is explicitly reopened.
