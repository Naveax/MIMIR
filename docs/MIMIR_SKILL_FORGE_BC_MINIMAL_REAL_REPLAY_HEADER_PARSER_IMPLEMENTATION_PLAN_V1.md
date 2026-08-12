# MIMIR Skill Forge BC Minimal Real Replay Header Parser Implementation Plan v1

## A. PURPOSE

This pass defines the future implementation plan for a narrow in-crate `mimir-replay` real replay
header reader.

This is a planning-only pass. It does not implement a parser, does not add a parser backend
dependency, does not claim parser readiness, does not claim parser success, does not produce a
`ReplayHeader`, and does not parse replay payloads.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains exactly:

- `ReplayInput::Memory`

The only future successful output remains:

- real `ReplayHeader` for valid supported bytes only

All invalid, malformed, insufficient, unsupported, non-memory, or deferred inputs must remain
structured errors.

## B. FAMILY SCOPE

The active evidence chain remains scoped first to:

- `low_boost_recovery`

The parser owner remains shared because Rocket League replay header parsing is not a
low-boost-recovery-specific semantic operation:

- `mimir-replay`

This plan does not create a generic all-family replay, raw-state, frame, event, index, export,
materialization, carrier, locator, database, runtime CLI, async/background, rollout, or corpus
framework.

`mimir-skill` may consume a future real reader only through the existing `ReplayReader` contract
and the current low-boost contract/realization chain.

## C. CURRENT BACKEND SELECTION SUMMARY

The current trusted backend-selection artifact is:

- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_SELECTION_DECISION_V1.md`

That pass selected:

- Outcome B
- narrow in-crate `mimir-replay` header parser implementation direction
- no concrete external dependency
- no dependency added
- no parser implemented

The prior selected direction remains valid for this plan:

- parser target: `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`
- first admitted input: `ReplayInput::Memory`
- valid output: real `ReplayHeader` for valid supported bytes only
- invalid, malformed, insufficient, unsupported, or deferred output: structured error only
- `UnsupportedReplayReader` remains truthful scaffold behavior and must remain distinguishable from
  any future real reader

## D. RE-AUDIT FINDINGS

Files re-audited before this planning artifact:

- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_SELECTION_DECISION_V1.md`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_selection_decision.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_selection_next.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_selection_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_INTEGRATION_CONTRACT_V1.md`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_integration_contract_decision.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_integration_contract_next.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_integration_contract_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_IMPLEMENTATION_EXTERNAL_REQUIREMENT_V1.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-skill/Cargo.toml`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

Additional context checked:

- current `ReplayReader` call sites and `UnsupportedReplayReader` use in `mimir-skill`
- current `ReplayId` and `Metadata` definitions in `mimir-types`
- current fixture-like file search for replay/parser evidence
- current manifest and lockfile search for replay parser dependencies

Current findings:

- `mimir-replay` exposes `ReplayInput`, `ReplayHeader`, `ReplayReader`, and
  `UnsupportedReplayReader`.
- `ReplayInput` currently allows `ReplayInput::File(PathBuf)` and
  `ReplayInput::Memory { label, bytes }`.
- `ReplayHeader` currently requires `replay_id: ReplayId`, `source_label: String`,
  `total_frames: Option<u32>`, and `metadata: Metadata`.
- `ReplayReader` currently requires `fn read_header(&self, input: &ReplayInput)
  -> Result<ReplayHeader>`.
- `UnsupportedReplayReader` is the only audited `ReplayReader` implementation in `mimir-replay`.
- `UnsupportedReplayReader::read_header` returns an explicit scaffold error and does not produce a
  header.
- `mimir-skill` currently invokes `read_header` only for truthful unsupported-attempt realization
  through `UnsupportedReplayReader`.
- `crates/mimir-replay/Cargo.toml` has no replay parser backend dependency.
- `Cargo.lock` has no audited `boxcars`, `rattletrap`, `rrrocket`, `carball`, `rlreplay`,
  `subtr-actor`, or equivalent parser dependency.
- No local audited Rocket League replay header byte-layout evidence was found.
- No valid supported `.replay` fixture was found in the audited workspace evidence.

## E. FUTURE IN-CRATE READER DESIGN

Future ownership:

- owner crate: `mimir-replay`
- public contract consumed by callers: existing `ReplayReader`
- source location option: a new reader type in `crates/mimir-replay/src/lib.rs`, or a private
  module re-exported from that file if the implementation grows past a small helper boundary
- no ownership in `mimir-skill`, `mimir-io`, `mimir-export`, or `mimir-types`

Selected future reader type name:

- `RocketLeagueReplayHeaderReader`

Rejected names:

- `ReplayReader`: already the trait name and would blur the contract surface
- `RealReplayReader`: too vague and likely to imply more than header parsing
- `MinimalReplayReader`: too generic and not explicit about Rocket League replay bytes
- `UnsupportedReplayReader`: must remain the scaffold-only reader and must not be converted into a
  real parser

Future coexistence rule:

- `RocketLeagueReplayHeaderReader` must be a distinct struct next to `UnsupportedReplayReader`.
- `UnsupportedReplayReader` must keep returning explicit unsupported scaffold errors.
- Tests must make the configured reader identity visible so unsupported-attempt evidence cannot be
  mistaken for real parser success.
- A future low-boost realization that uses the real reader must record that the configured reader
  is not `UnsupportedReplayReader`.

Possible future private helpers, not authorized in this pass:

- a private byte cursor with offset accounting
- a private header-field accumulator
- a private parser error kind
- private tests or fixtures under `mimir-replay`

These helper shapes are planning notes only. They are not implemented here.

## F. EXACT IMPLEMENTATION BOUNDARY

The future implementation may do only this:

- implement `ReplayReader` for `RocketLeagueReplayHeaderReader`
- admit `ReplayInput::Memory { label, bytes }`
- parse only enough supported Rocket League replay header bytes to construct a real
  `ReplayHeader`
- return structured errors for all invalid, malformed, insufficient, unsupported, non-memory, or
  deferred inputs
- keep all parsing deterministic and side-effect-free

The future implementation must not:

- parse raw-state payloads
- extract replay frames
- extract semantic replay events
- implement parser-success policy outside the direct `Result<ReplayHeader>`
- implement replay-source actual materialization
- implement replay-source carrier discovery
- implement replay-input locator logic
- read paths from `source_replay`, `source_replay.provenance_label`, or
  `audited_family_root_directory`
- read files through `ReplayInput::File` in the first implementation
- add corpus-wide ingestion, runtime CLI, async/background systems, database code, rollout
  physics, export widening, or generic replay frameworks

## G. INPUT BOUNDARY

First admitted input:

- `ReplayInput::Memory { label, bytes }`

Admission rules for memory input:

- `bytes` are the only parser data source.
- `bytes` must be used exactly as supplied by the caller.
- no byte synthesis, padding, truncation, repair, fallback lookup, filesystem read, or sidecar read
  is allowed.
- `label` may be used only for diagnostics and for `ReplayHeader.source_label`.
- `label` must not be interpreted as a path.
- `label` must not be used to infer replay identity, replay version, frame count, metadata, or
  support status.

Non-memory behavior:

- `ReplayInput::File(_)` must be rejected or deferred with the structured category
  `non_memory_input_rejected`.
- The first implementation must not read the file path.
- File support remains closed unless a later pass explicitly reopens it.

Empty or very short memory bytes:

- empty bytes and any prefix shorter than the minimum required supported header evidence must
  return `insufficient_bytes`, not a synthetic header.

## H. OUTPUT BOUNDARY

Allowed successful output:

- `Ok(ReplayHeader)` only for valid supported bytes whose required fields are byte-backed and
  fixture-proven.

Required field mapping:

| `ReplayHeader` field | Future allowed source | Current evidence status | Planning rule |
| --- | --- | --- | --- |
| `replay_id` | Verified Rocket League replay header field, or a separately approved byte-backed replay identifier policy documented and fixture-tested before implementation | Missing | Required for success. If no byte-backed identity rule is proven, the reader must return a structured error instead of `Ok`. Never derive from label, path, provenance, fixture filename, or test name. |
| `source_label` | Exact `ReplayInput::Memory.label` clone | Present as input context only | May be copied as source context. It is not replay identity and not parser evidence. |
| `total_frames` | Verified supported header field only | Missing | `Some(u32)` only when byte-backed header evidence proves the field and range. `None` is allowed when valid supported header bytes do not provide fixture-proven total-frame evidence. Never compute by parsing frames in this header reader. |
| `metadata` | `Metadata::new()` or explicitly documented byte-backed/header-backed fields | Missing | Empty metadata is allowed. Non-empty metadata requires a key-by-key byte accounting map. No placeholder, label-derived, path-derived, provenance-derived, or guessed metadata. |

Forbidden successful output:

- no raw-state payload
- no frame list
- no semantic event list
- no materialization record
- no carrier discovery record
- no locator record
- no export payload
- no success policy classification beyond `Ok(ReplayHeader)`

## I. BYTE-LEVEL EVIDENCE REQUIREMENTS

No exact Rocket League replay header byte layout is currently available in the audited repo/local
evidence for this pass.

A future implementation pass must obtain or verify byte-layout evidence before writing parser
success logic. The evidence must include:

- exact supported file/header signature or other format admission rule
- exact supported version family or version range
- exact byte ordering and integer/string/property encodings used by supported header fields
- exact header length or header termination rule
- exact offset, width, encoding, and semantic source for every field used to build
  `ReplayHeader`
- exact proof of how `ReplayHeader.replay_id` is derived
- exact proof of whether `ReplayHeader.total_frames` can be read from header bytes
- exact list of metadata keys, with each key mapped to source bytes and value interpretation
- exact body/raw-state boundary where header parsing stops
- exact unsupported-version detection rule when distinguishable from malformed bytes

For every future byte read, the implementation pass must account for:

- starting offset
- byte length
- expected encoding
- endianness if numeric
- validation rule
- destination field, if any
- failure category if the read cannot be completed or validated
- whether the read is required for success or optional metadata

The future reader must not claim a field offset, magic value, version layout, replay id derivation,
frame count derivation, or property ordering without fixture-backed evidence.

## J. SUPPORTED HEADER-FORMAT ASSUMPTIONS

Current supported format assumptions:

- none proven in this pass

Future supported format assumptions must be written down before parser implementation:

- supported replay/header version family
- minimum byte length for admission
- header structure and termination
- identity field source
- optional frame-count field source, if supported
- metadata field set, if any
- unsupported format/version detection boundaries
- malformed-vs-insufficient-vs-unsupported separation rules

Until those assumptions are supported by fixtures and byte accounting, the real parser
implementation remains closed.

## K. FIXTURE REQUIREMENTS

A later parser implementation pass must have fixture evidence before writing real parser code.

Required valid fixture:

- at least one real Rocket League replay byte sample admitted as `ReplayInput::Memory`
- known fixture provenance that does not depend on `source_replay` as a path
- expected byte-level map for every `ReplayHeader` field that will be produced
- expected `ReplayHeader.replay_id` source and value
- expected `ReplayHeader.source_label` copied from the memory input label
- expected `ReplayHeader.total_frames` value if and only if header-backed evidence exists
- expected metadata map, or explicit empty metadata if no metadata fields are proven

Required insufficient-byte fixture:

- at least one deterministic prefix or empty byte vector that ends before required header evidence
  can be validated
- expected error category: `insufficient_bytes`
- no `ReplayHeader`

Required malformed fixture:

- at least one byte sample with enough length to avoid the insufficient category but invalid
  header structure under the supported evidence rules
- expected error category: `malformed_bytes`
- no `ReplayHeader`

Required unsupported fixture, if distinguishable:

- at least one byte sample that can be identified as a Rocket League replay or replay-like header
  but outside the documented supported version/format boundary
- expected error category: `unsupported_format_or_version`
- no `ReplayHeader`

Deterministic repeated parse tests:

- parse the same valid memory bytes at least twice in one process
- assert equal `ReplayHeader`
- assert equal `metadata` ordering and contents
- assert no mutation of input bytes

Deterministic repeated error-category tests:

- parse the same insufficient, malformed, and unsupported-if-distinguishable bytes at least twice
- assert equal error category
- assert no `ReplayHeader`
- do not assert on unstable free-form diagnostic text unless the message is part of the contract

Fixture non-goals:

- no corpus-wide ingestion
- no replay-source materialization
- no carrier discovery
- no locator logic
- no `mimir-export`
- no raw-state payload or frame extraction

## L. ERROR TAXONOMY

The future implementation must expose or preserve enough structured information to distinguish at
least these categories:

- `unsupported_format_or_version`
- `malformed_bytes`
- `insufficient_bytes`
- `non_memory_input_rejected`
- `invalid_header_fields`
- `backend_or_internal_parser_error`
- `synthetic_header_fabrication_forbidden`

Category semantics:

- `unsupported_format_or_version`: bytes are identifiable enough to separate unsupported
  format/version from malformed bytes, but outside the documented supported boundary.
- `malformed_bytes`: bytes violate required header structure after enough bytes exist to make that
  judgment.
- `insufficient_bytes`: input ends before required header evidence can be read or validated.
- `non_memory_input_rejected`: caller supplied `ReplayInput::File` before file support was opened.
- `invalid_header_fields`: parsed header fields violate MIMIR invariants, such as missing required
  replay identity, non-finite or out-of-range values, invalid strings, or frame count overflow.
- `backend_or_internal_parser_error`: an unexpected internal failure occurred after input admission
  and before a valid structured category could otherwise be assigned.
- `synthetic_header_fabrication_forbidden`: implementation detects a path that would produce a
  guessed, label-derived, path-derived, placeholder, padded, or non-byte-backed header.

The exact Rust error type is not selected by this pass. A later implementation may add a narrow
error type inside `mimir-replay` if it remains behind the same reader contract and does not require
changes to `mimir-io`, `mimir-export`, or `mimir-types`.

## M. DETERMINISM REQUIREMENTS

The future reader must be deterministic:

- no wall-clock time
- no filesystem access for memory input
- no global mutable parser state
- no randomized ids
- no network access
- no environment-dependent parsing
- no locale-dependent text handling
- no input byte mutation
- no order instability in metadata

For identical valid bytes and identical labels:

- `ReplayHeader` must be equal across repeated calls.

For identical invalid bytes and identical labels:

- error category must be equal across repeated calls.

Diagnostics may include the input label, but diagnostic labels must not alter parser decisions.

## N. NO-FAKE-HEADER RULES

A future real reader must never:

- fabricate `ReplayHeader`
- guess `ReplayHeader.replay_id`
- derive `ReplayHeader.replay_id` from label, path, provenance, fixture name, or test name
- derive `total_frames` from filename, label, path, provenance, or frame extraction
- pad bytes to reach a target layout
- truncate bytes to hide malformed structure
- repair bytes silently
- convert unsupported bytes into a placeholder success
- hide a parser error behind empty metadata
- treat calmer logs or fewer errors as parser correctness

Because `ReplayHeader.replay_id` is currently required, no successful header may be produced until
the replay identity source is byte-backed and fixture-proven.

## O. UNSUPPORTED READER COEXISTENCE

`UnsupportedReplayReader` must remain truthful scaffold behavior.

Future coexistence requirements:

- keep `UnsupportedReplayReader` as a distinct type
- keep its tests proving explicit unsupported scaffold failure
- do not alias it to the real reader
- do not change unsupported-attempt realization into parser success
- keep unsupported-attempt records distinguishable from real-reader records
- ensure future real-reader tests name `RocketLeagueReplayHeaderReader` explicitly

If a future low-boost path consumes a real reader:

- it must still call through `ReplayReader::read_header(&ReplayInput)`
- it must preserve the existing low-boost contract/realization chain
- it must not bypass `mimir-replay` internals
- it must not reinterpret lineage anchors as replay locations

## P. VALIDATION GATES FOR A LATER IMPLEMENTATION PASS

Parser implementation remains closed until all gates below are satisfied or explicitly supplied in
the implementation pass.

Gate 1: evidence gate

- audited byte-layout evidence exists for the supported Rocket League replay header boundary
- `ReplayHeader.replay_id` derivation is byte-backed and documented
- `total_frames` source is documented, or the plan explicitly requires `None`
- metadata keys are documented field-by-field, or metadata is explicitly empty

Gate 2: fixture gate

- valid supported memory fixture exists
- insufficient-byte fixture exists
- malformed-byte fixture exists
- unsupported-format fixture exists if distinguishable
- expected success and error-category outputs are documented before code is written

Gate 3: implementation boundary gate

- code changes are limited to `mimir-replay` unless a later pass explicitly reopens manifests for a
  dependency or tests
- `mimir-io`, `mimir-export`, and `mimir-types` remain unchanged
- `Cargo.toml` and `Cargo.lock` remain unchanged unless a later pass explicitly reopens dependency
  selection
- first input remains `ReplayInput::Memory`
- `ReplayInput::File` returns `non_memory_input_rejected`

Gate 4: behavior gate

- valid fixture returns real `ReplayHeader`
- invalid/malformed/insufficient/unsupported/deferred inputs return structured errors
- deterministic success tests pass
- deterministic error-category tests pass
- no fake header path exists
- `UnsupportedReplayReader` behavior remains explicit and distinct

Gate 5: closure gate

- no raw-state payload parsing
- no replay frames
- no semantic events
- no replay-source materialization
- no carrier discovery
- no locator logic
- no corpus ingestion
- no runtime CLI
- no async/background system
- no database code
- no rollout physics
- no execution-result cleanup boundary changes
- no `mimir_export` widening

## Q. SELECTED PLANNING OUTCOME

Selected outcome:

- Outcome B

Implementation-planning result:

- the future narrow in-crate reader boundary is bounded enough to know what evidence is required
- exact byte-level Rocket League replay header layout is not available in the audited local repo
  evidence
- valid supported replay fixture evidence is not available in the audited local repo evidence
- therefore parser implementation is still blocked by fixture and byte-layout evidence

Why Outcome A is not selected:

- the plan can define gates, but the next pass cannot honestly be implementation unless valid
  fixtures and byte-layout evidence are available or explicitly supplied
- current local evidence does not prove replay id derivation, supported header layout, total frame
  derivation, metadata field mapping, or unsupported-version detection

Why Outcome C is not selected:

- implementation planning itself is not premature
- the reader ownership, input boundary, output boundary, error taxonomy, fixture requirements,
  determinism rules, no-fake-header rules, and closure rules can be bounded now

## R. WHAT REMAINS CLOSED

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

## S. WHAT REMAINS FORBIDDEN

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

## T. NEXT STAGE

Immediate next pass:

- fixture/evidence acquisition planning pass

Reason:

- the future implementation boundary is now bounded
- byte-layout evidence is still missing
- valid fixture evidence is still missing
- implementation remains closed until those missing evidence items are obtained, verified, or
  explicitly supplied under the gates in this plan

The next pass must not implement parser code unless implementation is explicitly reopened after
the evidence gate is satisfied.
