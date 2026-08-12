# MIMIR Skill Forge BC Replay Header Parser Fixture Materialization Admission Contract v1

## A. Purpose

This pass defines the admission and materialization contract for future fixture evidence needed by
the minimal real Rocket League replay header parser.

This is a contract-definition pass only. It does not implement parser code, does not implement
parser-success logic, does not add backend dependencies, does not add replay fixture bytes, does not
produce a `ReplayHeader`, and does not parse raw-state payloads, replay frames, or semantic replay
events.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The future reader owner remains:

- `mimir-replay`

The future reader type name remains:

- `RocketLeagueReplayHeaderReader`

The future real reader must remain distinct from:

- `UnsupportedReplayReader`

The first admitted parser input remains exactly:

- `ReplayInput::Memory`

`ReplayInput::File` remains rejected or deferred until file support is explicitly reopened.

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Rocket League replay header parsing remains a shared `mimir-replay` capability candidate, not a
low-boost-recovery semantic operation. This contract does not create a generic all-family replay,
raw-state, frame, event, index, export, materialization, carrier, locator, database, runtime CLI,
async/background, rollout, or corpus framework.

`mimir-skill` may consume a future real reader only through the existing `ReplayReader` contract
and the already-audited low-boost contract/realization chain.

## C. Re-Audit Boundary

Files re-audited before this contract:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_EVIDENCE_ACQUISITION_PLAN_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_evidence_acquisition_plan_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_evidence_acquisition_plan_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_evidence_acquisition_plan_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_MINIMAL_REAL_REPLAY_HEADER_PARSER_IMPLEMENTATION_PLAN_V1.md`
- `executor_mimir_skill_forge_bc_minimal_real_replay_header_parser_implementation_plan_decision.txt`
- `executor_mimir_skill_forge_bc_minimal_real_replay_header_parser_implementation_plan_next.txt`
- `executor_mimir_skill_forge_bc_minimal_real_replay_header_parser_implementation_plan_status.txt`
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

Current code facts:

- `mimir-replay` exposes `ReplayInput`, `ReplayHeader`, `ReplayReader`, and
  `UnsupportedReplayReader`.
- `ReplayInput` has `File(PathBuf)` and `Memory { label, bytes }`.
- `ReplayHeader` contains `replay_id`, `source_label`, `total_frames`, and `metadata`.
- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>` is the only reader contract.
- `UnsupportedReplayReader` is the only current `ReplayReader` implementation in
  `mimir-replay`.
- `UnsupportedReplayReader::read_header` returns an explicit scaffold error and produces no
  header.
- `crates/mimir-replay/Cargo.toml` has no replay parser backend dependency.
- `Cargo.lock` has no audited `boxcars`, `rattletrap`, `rrrocket`, `carball`, `rlreplay`,
  `subtr-actor`, or equivalent parser dependency.
- Existing synthetic opaque byte arrays such as `0x01, 0x02, 0x03, 0x04` are contract evidence for
  byte preservation only. They are not parser fixture evidence and must not be admitted as valid
  replay bytes.

## D. Current Evidence State

The audited repo evidence currently shows:

| Evidence question | Current answer |
| --- | --- |
| Are any `.replay` files present in the repo? | No. |
| Are any real replay-byte fixtures present under tests, docs, corpus, examples, assets, fixtures, or similar paths? | No. `tests/fixtures`, `tests/golden`, and `tests/integration` contain only `.gitkeep` files. |
| Are any approved Rocket League replay header byte-layout evidence docs present locally? | No. |
| Is expected `ReplayHeader.replay_id` evidence present? | No. |
| Is expected `ReplayHeader.total_frames` evidence present? | No. |
| Is expected `ReplayHeader.metadata` map evidence present? | No. |
| Are insufficient-byte fixtures present? | No. |
| Are malformed-byte fixtures present? | No. |
| Are unsupported-format/version fixtures present? | No. |
| Are fixture hashes or provenance artifacts present? | No fixture-backed hash/provenance artifact exists for real replay bytes. |
| Are local external parser docs or generated reports present that can be admitted as byte-layout evidence? | No exact local byte-layout docs or generated parser reports were found. Prior `boxcars`/external parser mentions are backend-selection context only. |
| Are existing opaque-byte arrays valid parser fixture evidence? | No. They remain synthetic contract evidence only. |

No real fixture bytes are present. No approved byte-layout evidence is present. No parser
implementation may be reopened from current repo evidence alone.

## E. Selected Outcome

Selected outcome:

- Outcome B

Outcome B means:

- no real fixture bytes or approved byte-layout evidence are present
- an external fixture supply/admission contract is required
- the next pass must wait for real fixture bytes or approved evidence to be supplied and admitted
- parser implementation remains closed
- parser-success logic remains closed

Why Outcome A is not selected:

- no real `.replay` bytes are present
- no exact Rocket League replay header byte-layout evidence is present
- no fixture-backed `ReplayHeader` expectation is present

Why Outcome C is not selected:

- this pass can define admission surfaces, but current repo evidence is not enough for another
  docs-only progression toward implementation
- the next productive pass requires externally supplied or externally approved evidence to be
  admitted

Why Outcome D is not selected:

- admission can be bounded without inventing bytes, offsets, headers, or parser semantics

## F. Valid Supported Replay Fixture Admission Contract

A valid supported replay fixture may be admitted only if all of the following are present:

- real Rocket League replay bytes
- admitted future parser input form:
  `ReplayInput::Memory { label, bytes }`
- fixture id
- byte length
- cryptographic hash, preferably SHA-256 or BLAKE3, with the hash algorithm named
- source/provenance record
- permission/license status
- privacy status
- storage/admission rule
- expected `ReplayHeader` evidence before parser implementation
- byte-accounting map before parser implementation

Allowed storage/admission forms:

- committed fixture bytes under a future narrow fixture path, for example
  `tests/fixtures/replay_header/<fixture_id>.replay`, if permission and privacy review allow
  commit
- private local fixture path recorded only in a future admission artifact, with byte length and
  hash, if raw bytes must not be committed
- redacted or withheld bytes with separately supplied byte length, hash, provenance, and enough
  independently reviewable evidence to keep expected output auditable
- another explicitly approved storage/admission form documented by a later pass before use

Storage rules:

- fixture bytes must not be invented or synthesized
- fixture bytes must not be padded or truncated to make a layout fit
- fixture labels, filenames, paths, provenance strings, `source_replay`,
  `source_replay.provenance_label`, and `audited_family_root_directory` are not parser facts
- cryptographic fixture hashes are fixture integrity evidence only; they are not automatically
  `ReplayHeader.replay_id`
- a private local path may be used only by a future evidence-admission pass to identify supplied
  bytes; it must not become runtime locator logic

Valid fixture success expectation:

- valid supported bytes may return `Ok(ReplayHeader)` only after every required output field is
  byte-backed or admitted by an explicit byte-backed policy
- no filename/path/provenance-derived parser fact is allowed
- no valid fixture may be admitted from the current synthetic opaque-byte arrays

## G. Byte-Layout Evidence Admission Contract

Before parser implementation can reopen, byte-layout evidence must be admitted from at least one
approved route:

- a real Rocket League `.replay` sample plus a trusted external parser/tool report that identifies
  the fields needed by `ReplayHeader`
- a real Rocket League `.replay` sample plus authoritative or source-audited documentation for the
  supported header structure
- a real Rocket League `.replay` sample plus independently reviewed manual byte-accounting analysis
  that maps the required header fields to bytes

The admitted evidence artifact must identify:

- evidence source
- evidence author or tool
- evidence generation date or acquisition date
- exact fixture id(s) covered
- supported format admission rule
- supported version or version family, if version-gated
- header length or header termination rule
- field encoding rules
- endianness for numeric fields
- string/property encoding rules if used
- body/raw-state boundary where this header reader must stop
- replay id derivation, or an explicit later byte-backed identity policy requirement
- whether `total_frames` is header-backed or must be `None`
- metadata key map, or explicit empty metadata policy
- insufficient, malformed, and unsupported-if-distinguishable error boundaries

Forbidden byte-layout admissions:

- no fake offsets
- no fake magic bytes
- no fake version layout
- no fake header boundary
- no fake replay id derivation
- no fake total frame derivation
- no fake metadata mapping
- no field ordering invented to satisfy an expected `ReplayHeader`
- no layout inferred from filenames, labels, paths, provenance strings, or low-boost lineage

## H. Byte-Accounting Map Admission Rules

Every future parsed or admission-only field must have a byte-accounting entry before
parser-success code is written.

Required columns:

| Column | Required meaning |
| --- | --- |
| `field_name` | Human-readable parsed or admission-only field name. |
| `source_byte_offset_or_structural_path` | Exact byte offset, byte range, or structural parser path. |
| `byte_length` | Exact byte length or derivation rule. |
| `encoding` | Integer, string, property, UUID/GUID, blob, or other exact encoding. |
| `endianness` | Required for numeric or binary multi-byte fields; otherwise `not_applicable`. |
| `validation_rule` | Validation required before the field may be consumed. |
| `destination_replay_header_field` | `replay_id`, `source_label`, `total_frames`, `metadata.<key>`, or `parser_admission_only`. |
| `required_or_optional` | Required for success, optional for metadata, or admission-only. |
| `failure_category_if_absent_or_invalid` | `insufficient_bytes`, `malformed_bytes`, `unsupported_format_or_version`, or `invalid_header_fields`. |
| `fixture_proof_reference` | Fixture id plus evidence artifact section proving the mapping. |

Minimum rows that must be either filled with evidence or explicitly marked by an admitted policy:

- `supported_format_admission`
- `supported_version`, if version-gated
- `header_boundary`
- `replay_id_source`
- `total_frames_source`, or `NONE_BY_POLICY`
- each admitted `metadata.<key>`, or `EMPTY_METADATA_BY_POLICY`

`TO_BE_SUPPLIED_BY_FIXTURE_EVIDENCE` remains the only honest value until real evidence is admitted.
Rows containing fake offsets, fake lengths, guessed encodings, or fake fixture references are not
admissible.

## I. Expected `ReplayHeader` Evidence Contract

### `replay_id`

Admission requirements:

- exact expected value for the valid fixture
- exact byte-backed derivation, or a later explicitly approved byte-backed identity policy
- evidence artifact section proving that derivation
- proof that the value is non-empty and fits `ReplayId`

Forbidden sources:

- `ReplayInput::Memory.label`
- filename
- file path
- fixture id
- test name
- provenance string
- cryptographic fixture hash unless separately approved by a later byte-backed identity policy
- `source_replay`
- `source_replay.provenance_label`
- `audited_family_root_directory`

Current status:

- missing

### `source_label`

Admission requirements:

- may be copied exactly from `ReplayInput::Memory.label`
- must be identified as source context only
- must not be used as replay identity, format evidence, version evidence, frame evidence, metadata
  evidence, or support-status evidence

Current status:

- input rule known, but no parser-success fixture exists

### `total_frames`

Admission requirements:

- `Some(u32)` requires byte-backed evidence proving source bytes, encoding, range, and expected
  value
- `None` is allowed only by explicit admitted policy when valid supported header bytes do not
  provide fixture-proven total-frame evidence for the minimal header reader
- must not be computed by parsing frames in this header reader
- must not be derived from filename, label, path, provenance, replay slice windows, or test data

Current status:

- missing

### `metadata`

Admission requirements:

- empty metadata is allowed only by explicit admitted policy for the minimal header reader
- non-empty metadata requires key-by-key byte accounting
- each metadata key must have source bytes, encoding, validation, destination key, and expected
  value for the valid fixture

Forbidden metadata:

- placeholder metadata
- label-derived metadata
- path-derived metadata
- provenance-derived metadata
- fixture-name-derived metadata
- guessed metadata
- empty metadata used to hide a failed or incomplete required parse

Current status:

- missing

## J. Insufficient-Byte Fixture Contract

An insufficient-byte fixture may be admitted only after a valid supported fixture exists.

Derivation rule:

- derive by truncating the admitted valid fixture bytes
- the truncation point must be documented
- the truncation point must end before required header evidence can be read or validated
- the derived byte length and hash must be recorded
- the parent valid fixture id must be recorded

Expected category:

- `insufficient_bytes`

Expected output:

- structured error only
- no `ReplayHeader`

Forbidden:

- no arbitrary synthetic insufficient bytes claimed as replay-derived
- no padding
- no successful header
- no parser facts inferred from the truncation filename or label

Current status:

- missing and not derivable because no valid fixture exists

## K. Malformed-Byte Fixture Contract

A malformed-byte fixture may be synthetic only under a documented mutation rule.

Derivation/admission rule:

- mutation must start from an admitted valid fixture or from proven supported-layout bytes
- mutation must be documented byte-for-byte at the changed range
- mutation must leave enough bytes to avoid the `insufficient_bytes` category
- mutation must violate a known supported-layout validation rule
- mutated byte length and hash must be recorded
- parent fixture id or evidence source must be recorded

Expected category:

- `malformed_bytes`

Expected output:

- structured error only
- no `ReplayHeader`

Forbidden:

- no random byte arrays labeled malformed without a supported-layout validation rule
- no fake magic/version bytes
- no fake offsets
- no successful header

Current status:

- missing and not derivable because no valid fixture and no supported-layout evidence exists

## L. Unsupported-Format/Version Fixture Contract

An unsupported-format/version fixture is required only if distinguishability from malformed bytes is
proven.

Admission rule:

- bytes must be identifiable enough to separate unsupported format/version from malformed bytes
- the distinguishability rule must be documented by byte-layout evidence
- byte length and hash must be recorded
- provenance and permission status must be recorded

Expected category:

- `unsupported_format_or_version`

Expected output:

- structured error only
- no `ReplayHeader`

If distinguishability is not proven:

- do not invent an unsupported fixture
- classify such evidence gap as missing or deferred
- use `malformed_bytes` only when the supported-layout validation rule justifies it

Current status:

- missing and deferred unless distinguishability is proven

## M. External Fixture Supply Contract

Because no real fixture bytes or approved byte-layout evidence are present, a future pass must
supply or admit external evidence before parser implementation can reopen.

The user or future approved source must supply at least:

- path or bytes of one real Rocket League `.replay`
- permission to use it as a local fixture
- explicit statement whether raw bytes may be committed or must stay private
- source/provenance label for audit display only
- fixture provider/source
- acquisition date
- byte length, computed during admission
- cryptographic hash, computed during admission
- privacy review status

Optional but admissible supporting evidence:

- known metadata from an external trusted parser/tool
- generated parser report from an approved external tool
- byte-layout notes
- authoritative or source-audited byte-layout documentation
- known supported version/format information

External supply rules:

- a supplied path is not runtime locator logic
- a supplied path is not `ReplayInput::File` support
- a supplied provenance label is not replay identity
- private local bytes may support local admission only if hash/provenance and expected output
  evidence remain auditable
- if bytes cannot be committed, the future pass must state whether CI/parser tests are blocked,
  local-only, or backed by another approved fixture form

## N. Permission, License, and Privacy Rules

Before any fixture bytes may be committed:

- permission to store and use the replay fixture in this repository must be documented
- license or usage status must be documented
- privacy review must explicitly consider player names, platform identifiers, chat-like metadata if
  present, replay title, match identifiers, and any other personal or sensitive data carried by the
  replay
- if privacy cannot be cleared, raw bytes must remain private or be replaced by an approved
  redacted/withheld evidence form

Before any private fixture may be used for parser implementation:

- byte length and hash must be recorded
- reproducible local materialization instructions must be recorded
- expected output evidence must be independently reviewable
- limitations of non-committed evidence must be stated

## O. No-Fake-Fixture Rules

This project must not admit:

- fake `.replay` files
- fake binary fixture files
- synthetic opaque byte arrays as valid parser fixtures
- guessed Rocket League replay magic bytes
- guessed version layouts
- guessed header boundaries
- guessed replay id derivation
- guessed total frame derivation
- guessed metadata maps
- placeholder `ReplayHeader` values
- fixture facts inferred from filenames, labels, paths, provenance strings, or lineage anchors
- bytes generated only to satisfy a target dimension, parser branch, or expected output

Synthetic bytes are allowed only for malformed fixtures after a real valid fixture or proven
supported-layout bytes exist and after the mutation rule is documented.

## P. Implementation Reopen Gate

Parser implementation may be reopened only after all required gates are satisfied:

1. At least one valid supported real Rocket League replay fixture is admitted.
2. Valid fixture provenance is documented.
3. Fixture byte length and hash are documented.
4. Permission/license/privacy status is documented.
5. Storage/admission form is documented.
6. Byte-layout evidence is admitted.
7. Exact byte-accounting map entries are admitted.
8. Expected `ReplayHeader.replay_id` derivation is admitted, or a later explicit byte-backed
   identity policy is approved.
9. `ReplayHeader.source_label` remains label-copy source context only.
10. `ReplayHeader.total_frames` policy is admitted as byte-backed `Some(u32)` or explicit `None`.
11. `ReplayHeader.metadata` policy is admitted as key-by-key byte-backed metadata or explicit empty
    metadata.
12. Insufficient-byte fixture is admitted or derivable from the valid fixture with a documented
    truncation point.
13. Malformed-byte fixture is admitted or derivable from the valid fixture or proven
    supported-layout bytes with a documented mutation rule.
14. Unsupported-format/version fixture is admitted if distinguishability is proven.
15. No-fake-fixture and no-fake-header rules remain satisfied.
16. `ReplayInput::Memory` remains the first admitted input.
17. `ReplayInput::File` remains rejected or deferred.
18. `UnsupportedReplayReader` remains truthful and distinct.
19. No parser-success, raw-state, frame, event, export, replay-source materialization, carrier, or
    locator boundary is silently opened.

Until these gates are met, parser implementation and parser-success logic remain closed.

## Q. What Remains Closed

Still closed after this contract pass:

- parser implementation
- parser-success logic
- backend dependency addition
- `ReplayHeader` production or synthesis
- real fixture materialization
- fixture byte creation
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
- execution-result cleanup boundary changes
- generic all-family replay/raw-state/index/export/materialization frameworks
- `mimir_export` widening

## R. What Remains Forbidden

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
- changing execution-result cleanup boundaries
- creating generic all-family replay/raw-state/index/export/materialization frameworks
- reinterpreting `source_replay` or `source_replay.provenance_label` as replay paths
- reinterpreting `audited_family_root_directory` as replay storage

## S. Next Stage

Immediate next pass:

- external fixture supply/admission pass

The next pass must supply or admit real fixture bytes and approved byte-layout evidence under this
contract. If no real bytes or approved evidence are supplied, the next pass must stop or remain an
evidence-supply contract and must not implement parser code.

Parser implementation remains closed unless explicitly reopened after the implementation reopen
gate is satisfied.
