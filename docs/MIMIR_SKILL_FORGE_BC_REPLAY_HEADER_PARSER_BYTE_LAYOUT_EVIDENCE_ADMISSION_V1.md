# MIMIR Skill Forge BC Replay Header Parser Byte-Layout Evidence Admission v1

## A. Purpose

This pass attempts to admit byte-layout evidence for the already admitted private-local Rocket
League replay fixture:

- fixture id: `rl_replay_header_fixture_001`
- local path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`

This is an evidence admission and planning pass only. It does not implement parser code, does not
implement parser-success logic, does not produce or synthesize a `ReplayHeader`, and does not parse
raw-state payloads, replay frames, or semantic replay events.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains exactly:

- `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes: <fixture bytes> }`

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Rocket League replay header parsing remains a shared `mimir-replay` capability candidate. This pass
does not create a generic replay, raw-state, frame, event, export, materialization, carrier, locator,
database, runtime CLI, async/background, rollout, physics, or corpus framework.

`mimir_export` widening remains forbidden.

## C. Current Admitted Fixture Summary

Prior trusted fixture admission selected Outcome A in:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_EXTERNAL_FIXTURE_SUPPLY_ADMISSION_RETRY_V1.md`

Current admitted private-local fixture record:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| provenance | `SUPPLIED_BY_USER_LOCAL_PATH` |
| permission status | `USER_SUPPLIED_LOCAL_USE_ALLOWED_PENDING_COMMIT_PERMISSION` |
| license status | `UNKNOWN_OR_PRIVATE_LOCAL_ONLY` |
| privacy status | `PENDING_REVIEW` |
| storage/admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |
| admitted future input | `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes: <fixture bytes> }` |

The fixture hash remains fixture integrity evidence only. It is not replay identity, byte layout,
version evidence, frame-count evidence, metadata evidence, or parser-success evidence.

## D. Fixture Identity Verification

The fixture identity was reverified in this pass without parsing the replay bytes.

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| path exists | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | file found | pass |
| byte length | `3001021` | `3001021` | pass |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | pass |

No `ReplayHeader` was produced. No byte offsets, field values, frame counts, metadata keys, or
layout facts were derived from the fixture bytes.

## E. Evidence Search Scope

Local search scope included:

- required prior replay-header parser admission and planning artifacts
- `docs`
- previous `executor_*` artifacts
- `crates`
- `tests`
- `external_fixtures` inventory only, excluding parsing or reading the replay payload as evidence
- local parser-report, generated-parser, byte-layout, byte-accounting, and layout-note filename
  searches
- `Cargo.toml`
- `Cargo.lock`
- crate manifests

Required re-audit files inspected before editing:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_EXTERNAL_FIXTURE_SUPPLY_ADMISSION_RETRY_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_external_fixture_supply_admission_retry_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_external_fixture_supply_admission_retry_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_external_fixture_supply_admission_retry_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_EXTERNAL_FIXTURE_SUPPLY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_MATERIALIZATION_ADMISSION_CONTRACT_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_EVIDENCE_ACQUISITION_PLAN_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_MINIMAL_REAL_REPLAY_HEADER_PARSER_IMPLEMENTATION_PLAN_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_SELECTION_DECISION_V1.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-skill/Cargo.toml`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

## F. Evidence Candidate Classification

| Candidate | Classification | Admission result |
| --- | --- | --- |
| Verified fixture path, byte length, and SHA-256 | fixture integrity evidence | admitted previously and reverified; not byte-layout evidence |
| `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_EXTERNAL_FIXTURE_SUPPLY_ADMISSION_RETRY_V1.md` | fixture admission artifact | confirms byte-layout evidence remains missing; not byte-layout evidence |
| `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_MATERIALIZATION_ADMISSION_CONTRACT_V1.md` | admission contract | defines requirements and states no approved local byte-layout evidence; not byte-layout evidence |
| `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_EVIDENCE_ACQUISITION_PLAN_V1.md` | acquisition plan | defines future byte-accounting requirements; not fixture-backed byte-layout evidence |
| `docs/MIMIR_SKILL_FORGE_BC_MINIMAL_REAL_REPLAY_HEADER_PARSER_IMPLEMENTATION_PLAN_V1.md` | implementation plan | records missing byte-layout evidence; not byte-layout evidence |
| `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_SELECTION_DECISION_V1.md` | parser dependency docs/context | discusses `boxcars` as a rejected broader dependency; not admitted byte-layout evidence |
| `crates/mimir-replay/src/lib.rs` | source code | exposes scaffold contracts and `UnsupportedReplayReader`; no parser implementation or layout evidence |
| `crates/mimir-skill/src/lib.rs` | source code | consumes scaffold replay surface for unsupported-attempt plumbing; no byte-layout evidence |
| `Cargo.toml`, crate manifests, `Cargo.lock` | dependency inventory | no replay parser dependency found; not byte-layout evidence |
| `tests` | fixture inventory | only `.gitkeep` files found; no parser fixture or report evidence |
| `external_fixtures\sample_001.replay` | private-local fixture bytes | admitted as future memory input only; raw bytes were not parsed and are not self-describing approved layout evidence |
| local parser-report or generated-parser files | generated parser report | none found |
| local byte-layout or byte-accounting notes | approved byte-layout evidence | none found |

No approved byte-layout evidence exists locally.

## G. Selected Outcome

Selected outcome:

- Outcome B

Outcome B means:

- no approved byte-layout evidence exists locally
- byte-layout evidence remains missing
- expected `ReplayHeader` evidence remains missing
- next pass must be external byte-layout evidence supply/admission or approved parser-report
  generation/admission
- parser implementation remains closed
- parser-success logic remains closed

Why Outcome A is not selected:

- no local approved evidence identifies a supported Rocket League replay header admission rule
- no local approved evidence identifies supported version or version family
- no local approved evidence identifies header boundary or header termination
- no local approved evidence identifies field encodings, numeric endianness, or string/property
  encoding rules
- no local approved evidence identifies the body/raw-state boundary where header parsing stops
- no local approved evidence identifies replay id derivation or an admitted blocked policy
- no local approved evidence identifies `total_frames` as byte-backed `Some(u32)` or an admitted
  `None` policy for this fixture
- no local approved evidence identifies metadata as key-by-key byte-backed metadata or an admitted
  empty metadata policy for this fixture
- no local approved evidence defines insufficient, malformed, or unsupported-if-distinguishable
  error boundaries

Why Outcome C is not selected:

- no candidate local byte-layout evidence artifact exists that is partially admissible but unsafe;
  the local hits are fixture integrity, planning, contract, dependency-context, or scaffold-code
  artifacts

Why Outcome D is not selected:

- the admission boundary is bounded by the existing fixture-admission contract and the search scope
  above

## H. Admitted Byte-Layout Evidence

No byte-layout evidence is admitted in this pass.

The following remain unadmitted:

- supported Rocket League replay header admission rule
- supported version or version family
- header boundary or header termination rule
- field encodings
- numeric endianness
- string/property encoding rules
- body/raw-state boundary
- replay id derivation
- total frame derivation or explicit fixture-backed `None` policy
- metadata mapping or explicit fixture-backed empty metadata policy
- insufficient-byte error boundary
- malformed-byte error boundary
- unsupported-if-distinguishable error boundary

## I. Rejected Or Non-Admitted Evidence

Rejected or non-admitted evidence categories:

- fixture path, filename, provenance, byte length, and SHA-256 are not parser facts
- prior `boxcars` references are parser dependency docs and backend-selection context only
- planning skeletons and byte-accounting table formats are not field evidence
- existing synthetic opaque byte tests are byte-preservation contract evidence only
- `UnsupportedReplayReader` errors are truthful scaffold behavior only
- absence of parser dependencies in manifests and lockfile is not layout evidence

No field values were filled from these sources.

## J. Byte-Accounting Map Status

Because Outcome B was selected, this pass admits no byte offsets, structural paths, lengths,
encodings, endianness, validation rules, destination mappings, or fixture proof references.

| field_name | source_byte_offset_or_structural_path | byte_length | encoding | endianness | validation_rule | destination_replay_header_field | required_or_optional | failure_category_if_absent_or_invalid | fixture_proof_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| supported_format_admission | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| supported_version_or_family | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| header_boundary_or_termination | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| field_encoding_rules | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| numeric_endianness | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| string_or_property_encoding | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| body_or_raw_state_boundary | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| replay_id_source | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `replay_id` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| total_frames_source_or_none_policy | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `total_frames` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| metadata_key_map_or_empty_policy | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `metadata` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| insufficient_error_boundary | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| malformed_error_boundary | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |
| unsupported_if_distinguishable_boundary | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | parser_admission_only | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` | `BLOCKED_PENDING_EVIDENCE` |

## K. Replay Id Evidence Status

Replay id evidence status:

- not admitted

No replay id may be derived from:

- fixture id
- `ReplayInput::Memory.label`
- filename
- file path
- provenance
- SHA-256
- byte length
- low-boost lineage
- `source_replay`
- `source_replay.provenance_label`
- `audited_family_root_directory`

Parser success remains blocked because `ReplayHeader.replay_id` is required and no byte-backed
identity rule or explicit admitted blocked policy exists.

## L. Total Frames Evidence Status

`total_frames` evidence status:

- not admitted

No `Some(u32)` value is admitted.

No explicit fixture-backed `None` policy is admitted.

`total_frames` must not be derived from filename, label, path, provenance, hash, replay frame
extraction, or raw-state parsing.

## M. Metadata Evidence Status

Metadata evidence status:

- not admitted

No key-by-key metadata map is admitted.

No explicit fixture-backed empty metadata policy is admitted.

Empty metadata must not be used to hide missing header evidence.

## N. Error-Boundary Evidence Status

Error-boundary evidence status:

- not admitted

Missing boundaries:

- insufficient bytes
- malformed bytes
- unsupported format/version if distinguishable
- invalid header fields

No insufficient, malformed, or unsupported fixtures are derivable from this pass because no
supported byte layout or validation boundary is admitted.

## O. Expected `ReplayHeader` Evidence Status

Expected `ReplayHeader` evidence status:

- not admitted

Missing expected output evidence:

- expected `ReplayHeader.replay_id`
- byte-backed replay id derivation or explicit admitted blocked policy
- expected `ReplayHeader.source_label` success context for an admitted parser-success fixture
- expected `ReplayHeader.total_frames` value or explicit admitted `None` policy
- expected `ReplayHeader.metadata` map or explicit admitted empty metadata policy

`source_label` remains known only as source context copied from `ReplayInput::Memory.label` in a
future implementation. That rule does not create byte-layout evidence or parser-success evidence.

## P. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

Implementation may not proceed from this pass because:

1. fixture identity is admitted, but byte-layout evidence is not admitted
2. no byte-accounting map entries are admitted
3. no expected `ReplayHeader` evidence is admitted
4. no success or structured error expectations are admitted
5. no insufficient, malformed, or unsupported-if-distinguishable fixtures are derivable

## Q. No-Fake-Layout Rules

This pass admits no:

- magic bytes
- offsets
- field lengths
- version layout
- endianness
- string or property encoding
- header boundary
- body/raw-state boundary
- replay id derivation
- total frame derivation
- metadata mapping
- error-boundary classifications
- parser-success fixture outputs

The fixture path, filename, provenance, byte length, and SHA-256 must not be treated as parser
facts.

## R. What Remains Closed

Still closed after this pass:

- parser implementation
- parser-success logic
- backend dependency addition
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

## S. What Remains Forbidden

Still forbidden unless explicitly reopened:

- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- modifying `Cargo.toml`
- modifying `Cargo.lock`
- adding backend dependencies
- implementing parser code
- implementing parser-success logic
- producing or synthesizing `ReplayHeader`
- parsing raw-state payloads
- extracting replay frames
- extracting semantic replay events
- implementing replay-source actual-materialization
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

Immediate next pass:

- external byte-layout evidence supply/admission or approved parser-report generation/admission

The next pass must supply approved byte-layout evidence for `rl_replay_header_fixture_001`, or an
approved parser/tool report that can be admitted under the existing contract.

Parser implementation is not the next pass.

Parser implementation is allowed only after fixture evidence, byte-layout evidence, and expected
`ReplayHeader` output evidence are admitted by later passes.
