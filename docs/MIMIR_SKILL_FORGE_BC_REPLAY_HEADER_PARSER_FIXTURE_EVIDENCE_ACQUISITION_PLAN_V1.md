# MIMIR Skill Forge BC Replay Header Parser Fixture Evidence Acquisition Plan v1

## A. Purpose

This pass defines the fixture and byte-evidence acquisition plan required before any real
`mimir-replay` header parser implementation can be written.

This is a planning-only pass. It does not implement a parser, does not add dependencies, does not
modify Rust source, does not claim parser readiness, does not produce a `ReplayHeader`, and does
not parse replay payloads.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The future reader owner remains:

- `mimir-replay`

The future reader type name remains:

- `RocketLeagueReplayHeaderReader`

The first admitted input remains exactly:

- `ReplayInput::Memory`

`ReplayInput::File` remains rejected or deferred until file support is explicitly reopened.

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Rocket League replay header parsing itself remains a shared `mimir-replay` capability candidate,
not a low-boost-recovery semantic operation. This pass does not create a generic all-family replay,
raw-state, frame, event, index, export, materialization, carrier, locator, database, runtime CLI,
async/background, rollout, or corpus framework.

`mimir-skill` may consume a future real reader only through the existing `ReplayReader` contract
and the already-audited low-boost contract/realization chain.

## C. Current Implementation-Plan Summary

The trusted implementation-planning artifact is:

- `docs/MIMIR_SKILL_FORGE_BC_MINIMAL_REAL_REPLAY_HEADER_PARSER_IMPLEMENTATION_PLAN_V1.md`

That pass selected:

- Outcome B for implementation planning
- bounded future implementation ownership in `mimir-replay`
- reader name `RocketLeagueReplayHeaderReader`
- a distinct reader beside `UnsupportedReplayReader`
- no parser implementation
- no parser-success logic
- no backend dependency addition

The selected future boundary remains:

- valid supported `ReplayInput::Memory` bytes may return a real `ReplayHeader`
- invalid, malformed, insufficient, unsupported, non-memory, or deferred inputs must return
  structured errors only
- `UnsupportedReplayReader` must remain truthful scaffold behavior and distinguishable from any
  future real reader
- `mimir_export` widening remains forbidden unless explicitly reopened

## D. Re-Audit Findings

Files re-audited before this planning artifact:

- `docs/MIMIR_SKILL_FORGE_BC_MINIMAL_REAL_REPLAY_HEADER_PARSER_IMPLEMENTATION_PLAN_V1.md`
- `executor_mimir_skill_forge_bc_minimal_real_replay_header_parser_implementation_plan_decision.txt`
- `executor_mimir_skill_forge_bc_minimal_real_replay_header_parser_implementation_plan_next.txt`
- `executor_mimir_skill_forge_bc_minimal_real_replay_header_parser_implementation_plan_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_SELECTION_DECISION_V1.md`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_selection_decision.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_selection_next.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_selection_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_INTEGRATION_CONTRACT_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_IMPLEMENTATION_EXTERNAL_REQUIREMENT_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_INPUT_CREATION_FROM_OPAQUE_CALLER_ADMITTED_REPLAY_BYTES_CONTRACT_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_INPUT_CREATION_FROM_OPAQUE_CALLER_ADMITTED_REPLAY_BYTES_REALIZATION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_ACTUAL_REPLAY_PARSING_IMPLEMENTATION_READINESS_DECISION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_ACTUAL_REPLAY_PARSING_UNSUPPORTED_ATTEMPT_REALIZATION_V1.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-skill/Cargo.toml`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

Current code facts:

- `mimir-replay` exposes `ReplayInput`, `ReplayHeader`, `ReplayReader`, and
  `UnsupportedReplayReader`.
- `ReplayInput` has `File(PathBuf)` and `Memory { label, bytes }`.
- `ReplayHeader` contains `replay_id`, `source_label`, `total_frames`, and `metadata`.
- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>` is the only reader contract.
- `UnsupportedReplayReader` is the only current `ReplayReader` implementation.
- `UnsupportedReplayReader::read_header` returns an explicit scaffold error and produces no
  header.
- `crates/mimir-replay/Cargo.toml` has no replay parser backend dependency.
- `Cargo.lock` has no audited `boxcars`, `rattletrap`, `rrrocket`, `carball`, `rlreplay`,
  `subtr-actor`, or equivalent parser dependency.
- The low-boost opaque-byte chain preserves `ReplayInput::Memory` bytes but does not prove that
  those bytes are Rocket League replay bytes.
- Existing low-boost tests include synthetic opaque byte arrays, for example
  `0x01,0x02,0x03,0x04`; those are not valid replay fixture evidence and must not be used as
  parser-success fixtures.

## E. Current Evidence Gap Summary

The audited repo evidence currently shows:

| Question | Current answer |
| --- | --- |
| Are any `.replay` fixtures present in the repo? | No. |
| Are any replay-byte fixtures present under tests, docs, corpus, examples, or assets? | No real replay-byte fixtures were found. Existing opaque-byte tests are synthetic contract fixtures only. |
| Is any Rocket League replay header byte-layout documentation present locally? | No exact local byte-layout evidence was found. |
| Is any expected `ReplayHeader` mapping documented? | Planning rules exist, but no fixture-backed expected mapping exists. |
| Is replay id derivation documented? | No byte-backed replay id derivation is documented. |
| Is total frame derivation documented? | No byte-backed total frame derivation is documented. |
| Is metadata mapping documented? | No byte-backed metadata key map is documented. |
| Are insufficient-byte fixtures present? | No. They may be derived only after a valid fixture exists. |
| Are malformed-byte fixtures present? | No. A mutation rule may be defined only after supported layout evidence exists. |
| Are unsupported-format/version fixtures present? | No. They are required only if distinguishability from malformed bytes is proven. |
| Are parser-related fixtures from previous passes present? | Only synthetic opaque-byte and unsupported-reader scaffolds; no real replay parser fixtures. |
| Are external dependency docs cached locally as byte-layout evidence? | No exact cached byte-layout documentation was found. Prior artifacts cite external parser docs for backend selection only; those citations are not fixture-backed layout evidence for this parser. |

No labels, paths, filenames, provenance strings, source replay lineage, or audited family root paths
are parser evidence.

## F. Byte-Layout Evidence Acquisition Route

Before implementation, a later evidence materialization pass must obtain auditable byte-layout
evidence from at least one approved route:

1. A real Rocket League `.replay` sample plus a trusted external parser/tool report that identifies
   the fields needed by `ReplayHeader`.
2. A real Rocket League `.replay` sample plus authoritative or source-audited documentation for the
   supported header structure.
3. A real Rocket League `.replay` sample plus an independently reviewed manual byte-accounting
   analysis that maps the required header fields to bytes.

The route must produce concrete evidence for:

- supported format admission rule
- supported version or version family
- header length or header termination rule
- field encoding rules
- endianness for numeric fields
- string/property encoding rules if used
- body/raw-state boundary where this header reader must stop
- replay id derivation
- whether total frames is header-backed or must be `None`
- metadata key map, or explicit empty metadata
- insufficient, malformed, and unsupported-if-distinguishable error boundaries

This plan does not supply those facts. Values such as magic bytes, offsets, version encodings,
termination rules, property order, replay id source, total frame source, and metadata fields remain
`TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE`.

## G. Fixture Class Definitions

### A. Valid Supported Replay Fixture

Required before implementation.

Requirements:

- real Rocket League replay bytes
- admitted as `ReplayInput::Memory { label, bytes }`
- fixture provenance recorded before use
- expected `ReplayHeader` mapping recorded before parser code is written
- byte-accounting map for every produced field
- deterministic expected output
- no dependence on filename, path, label, provenance string, source replay lineage, or audited
  family root for parser facts

Expected category:

- valid supported bytes

Expected output:

- `Ok(ReplayHeader)` only after every required `ReplayHeader` field is byte-backed or explicitly
  allowed by this plan

Current status:

- missing

### B. Insufficient-Byte Fixture

Required before implementation.

Derivation rule:

- may be derived only from a valid supported fixture prefix after the valid fixture exists
- the prefix must end before required header evidence can be read or validated
- the prefix length and truncation point must be documented

Expected category:

- `insufficient_bytes`

Expected output:

- structured error only
- no `ReplayHeader`

Current status:

- missing

### C. Malformed-Byte Fixture

Required before implementation.

Derivation rule:

- may be synthetic only if the mutation rule is documented
- mutation must start from a real valid supported fixture or a documented supported-layout byte
  region
- mutation must leave enough bytes to avoid the insufficient category
- mutation must violate a known supported-layout validation rule

Expected category:

- `malformed_bytes`

Expected output:

- structured error only
- no `ReplayHeader`

Current status:

- missing

### D. Unsupported-Format/Version Fixture

Required only if distinguishable from malformed bytes.

Admission rule:

- bytes must be identifiable enough to separate unsupported format or version from malformed bytes
- the distinguishability rule must be documented by byte-layout evidence

Expected category:

- `unsupported_format_or_version`

Expected output:

- structured error only
- no `ReplayHeader`

Current status:

- missing and deferred unless distinguishability is proven

## H. Byte-Accounting Map Format

Every future parsed field must have an entry with this exact information before parser-success code
is written:

| Required map column | Meaning |
| --- | --- |
| `field_name` | Human-readable parsed field name. |
| `source_byte_offset_or_structural_path` | Exact byte offset, byte range, or structural parser path. Use `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` until proven. |
| `byte_length` | Exact byte length or length derivation rule. Use `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` until proven. |
| `encoding` | Integer, string, property, UUID/GUID, blob, or other exact encoding. |
| `endianness` | Required for numeric or binary multi-byte fields; otherwise `not_applicable`. |
| `validation_rule` | Required validation before the field may be consumed. |
| `destination_replay_header_field` | `replay_id`, `source_label`, `total_frames`, `metadata.<key>`, or `parser_admission_only`. |
| `required_or_optional` | Required for success, optional for metadata, or admission-only. |
| `failure_category_if_absent_or_invalid` | `insufficient_bytes`, `malformed_bytes`, `unsupported_format_or_version`, or `invalid_header_fields`. |
| `fixture_proof_reference` | Fixture id plus evidence artifact section proving the mapping. |

Initial unfilled map skeleton:

| field_name | source_byte_offset_or_structural_path | byte_length | encoding | endianness | validation_rule | destination_replay_header_field | required_or_optional | failure_category_if_absent_or_invalid | fixture_proof_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| supported_format_admission | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | parser_admission_only | required | `malformed_bytes` or `unsupported_format_or_version`, depending on proven distinguishability | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` |
| supported_version | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | parser_admission_only | required if version-gated | `unsupported_format_or_version` if distinguishable, else `malformed_bytes` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` |
| header_boundary | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | parser_admission_only | required | `insufficient_bytes` or `malformed_bytes` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` |
| replay_id_source | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` | must produce non-empty `ReplayId` without label/path/provenance derivation | `replay_id` | required for success | `invalid_header_fields` or earlier structural category | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` |
| total_frames_source | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or `NONE_BY_POLICY` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or `not_applicable` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or `not_applicable` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or `not_applicable` | if present, must fit `u32`; if absent by policy, output `None` | `total_frames` | optional | `invalid_header_fields` if present but invalid | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or explicit `NONE_BY_POLICY` |
| metadata_key | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or `EMPTY_METADATA_BY_POLICY` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or `not_applicable` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or `not_applicable` | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or `not_applicable` | key-by-key evidence required for non-empty metadata | `metadata.<key>` | optional | `invalid_header_fields` if present but invalid | `TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` or explicit `EMPTY_METADATA_BY_POLICY` |

No fake offsets, lengths, encodings, endianness values, validation rules, or fixture references may
be filled to satisfy a target dimension or expected output.

## I. Expected `ReplayHeader` Evidence Rules

### `replay_id`

Rules:

- required for successful `ReplayHeader`
- must be byte-backed by supported replay header evidence, or separately approved later by an
  explicit byte-backed identity policy
- must not be derived from `ReplayInput::Memory.label`
- must not be derived from filename, path, fixture name, test name, provenance string,
  `source_replay`, `source_replay.provenance_label`, or `audited_family_root_directory`
- if no byte-backed identity rule is proven, valid-looking bytes must not return `Ok`

Current status:

- missing

### `source_label`

Rules:

- may be copied exactly from `ReplayInput::Memory.label`
- source label is source context only
- source label is not replay identity, format evidence, version evidence, frame evidence, metadata
  evidence, or support-status evidence

Current status:

- input rule known, but no parser-success fixture exists

### `total_frames`

Rules:

- may be `Some(u32)` only if header byte evidence proves a total-frame field and its range
- may be `None` if valid supported header bytes do not provide fixture-proven total-frame evidence
- must not be computed by parsing frames in this header reader
- must not be derived from filename, label, path, provenance, replay slice windows, or test data

Current status:

- total-frame byte evidence missing; default allowed policy for future implementation is `None`
  unless evidence is supplied

### `metadata`

Rules:

- may be empty via `Metadata::new()`
- non-empty metadata requires key-by-key byte accounting
- each metadata key must define source bytes, encoding, validation, destination key, and expected
  value for the valid fixture
- metadata must not be placeholder, label-derived, path-derived, provenance-derived, fixture-name
  derived, or guessed

Current status:

- metadata field map missing; default allowed policy for future implementation is empty metadata
  unless key-by-key evidence is supplied

## J. Fixture Provenance Rules

Every admitted fixture must record:

- fixture id
- fixture class
- origin route
- provider or source
- license/permission status if external
- acquisition date
- byte length
- cryptographic hash
- whether raw bytes may be stored in repo
- whether only a private/local path or redacted hash may be stored
- evidence artifact that maps expected output to bytes
- reason the fixture is valid, insufficient, malformed, or unsupported

Forbidden provenance use:

- no parser fact may be inferred from fixture filename
- no parser fact may be inferred from fixture path
- no parser fact may be inferred from `ReplayInput::Memory.label`
- no parser fact may be inferred from source replay lineage or provenance strings
- no parser fact may be inferred from audited family root paths

If fixture bytes cannot be committed for licensing or size reasons, the admission contract must
still record enough hash/provenance and local materialization instructions to make expected outputs
auditable without inventing parser facts.

## K. Deterministic Validation Rules

For valid supported bytes:

- parse the same `ReplayInput::Memory` bytes at least twice in one process
- assert equal `ReplayHeader`
- assert `source_label` equals the input label
- assert `replay_id` equals the fixture-backed expected value
- assert `total_frames` equals fixture evidence or `None` by explicit policy
- assert metadata equals fixture evidence or empty metadata by explicit policy
- assert input bytes are not mutated

For insufficient, malformed, and unsupported-if-distinguishable bytes:

- parse the same bytes at least twice in one process
- assert equal structured error category
- assert no `ReplayHeader`
- assert input bytes are not mutated
- do not assert unstable free-form diagnostic text unless it is made part of the contract

Validation must not use calmer logs, fewer errors, or successful compilation as parser correctness.

## L. No-Fake-Header Rules

A future parser must never:

- fabricate `ReplayHeader`
- synthesize `ReplayHeader` from placeholder values
- guess `ReplayHeader.replay_id`
- derive `ReplayHeader.replay_id` from label, path, provenance, fixture name, or test name
- derive `total_frames` from filename, label, path, provenance, replay slice windows, or frame
  extraction
- pad bytes to satisfy a layout
- truncate bytes to hide malformed structure
- silently repair bytes
- convert unsupported bytes into success
- hide parser uncertainty behind empty metadata
- use existing opaque synthetic bytes as valid replay fixture evidence

Because `ReplayHeader.replay_id` is required, no success result may be produced until replay id
evidence is byte-backed or an explicit later byte-backed identity policy is approved.

## M. Implementation Reopen Gate

Parser implementation may be reopened only after all required items exist:

1. At least one valid supported real Rocket League replay fixture is admitted.
2. Valid fixture provenance is documented.
3. Expected `ReplayHeader` output for the valid fixture is documented before parser code is
   written.
4. Replay id derivation is byte-backed or explicitly approved by a later byte-backed policy.
5. Header byte-layout evidence documents admission, version, header boundary, field encodings,
   endianness, and validation rules.
6. Total-frame policy is explicit: byte-backed `Some(u32)` or allowed `None`.
7. Metadata policy is explicit: key-by-key byte-backed metadata or allowed empty metadata.
8. Insufficient-byte fixture is derived and documented.
9. Malformed-byte fixture is derived or admitted with a documented mutation/validation rule.
10. Unsupported-format/version fixture is admitted if distinguishability is proven.
11. Deterministic success and error-category expectations are documented.
12. `ReplayInput::File` remains rejected or deferred.
13. `UnsupportedReplayReader` remains distinct and truthful.

Until these gates are met, parser implementation and parser-success logic remain closed.

## N. Selected Evidence-Planning Outcome

Selected outcome:

- Outcome A

Evidence-planning result:

- the acquisition plan is bounded enough for a later evidence materialization/admission pass
- no parser implementation is authorized
- no actual valid fixture bytes are present in the repo
- exact byte-layout evidence remains missing
- implementation remains blocked until fixture and byte-layout evidence are materially admitted

Why Outcome B is not selected:

- repo work can continue with a narrow fixture materialization/admission contract
- this plan can define the exact required fixture classes, byte-accounting map, provenance rules,
  deterministic expectations, no-fake-header rules, and implementation reopen gate without actual
  fixture bytes
- external fixture supply or approved external evidence is still required before implementation,
  but the next repo pass can be the contract that admits or materializes that evidence

Why Outcome C is not selected:

- fixture/evidence acquisition is bounded
- the valid, insufficient, malformed, and unsupported-if-distinguishable classes are definable
- the byte-accounting map format is definable
- the implementation reopen gate is definable

## O. What Remains Closed

Still closed after this planning pass:

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
- execution-result cleanup boundary changes
- generic all-family replay/raw-state/index/export/materialization frameworks
- `mimir_export` widening

## P. What Remains Forbidden

Still forbidden unless explicitly reopened:

- modifying `mimir-replay` source for parser implementation
- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- modifying `Cargo.toml`
- modifying `Cargo.lock`
- adding backend dependencies
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
- changing execution-result cleanup boundaries
- creating generic all-family replay/raw-state/index/export/materialization frameworks
- reinterpreting `source_replay` as a replay path
- reinterpreting `source_replay.provenance_label` as a replay path
- reinterpreting `audited_family_root_directory` as replay storage

## Q. Next Stage

Immediate next pass:

- fixture materialization/admission contract pass

The next pass should acquire or admit real valid replay fixture evidence and byte-layout evidence
under the rules in this plan. If no real fixture bytes or approved external evidence are supplied,
that pass must remain an external fixture supply/admission contract and must not implement parser
code.

Parser implementation remains closed unless explicitly reopened after the evidence gate is
satisfied.
