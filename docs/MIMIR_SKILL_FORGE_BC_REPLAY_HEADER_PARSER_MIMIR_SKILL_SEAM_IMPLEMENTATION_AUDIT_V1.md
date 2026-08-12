# MIMIR Skill Forge BC Replay Header Parser mimir-skill Seam Implementation Audit v1

Pass date: 2026-05-04

## Purpose

Audit the implemented `mimir-skill` narrow parallel minimal-header-attempt seam against the
previously planned boundary.

This is an audit/admission pass only. It does not broaden parser scope, add parser functionality,
wire export/runtime/CLI behavior, add file input support, add dependencies, or change
`mimir-replay` parser behavior.

## Selected Outcome

Selected outcome:

- Outcome A

The implemented `mimir-skill` seam is admitted.

Admission is only for the explicit opt-in, parallel minimal-header-attempt seam:

- success means `minimal header parse success only`
- failure means `minimal header parse failure only`
- `ReplayHeader` is carried only as header-only parser-attempt evidence
- parser-success remains admitted only for the first minimal boundary
- no broad replay parser expansion is admitted

## Fixture Verification

Fixture identity was verified directly:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

The seam does not use fixture path, hash, filename, provenance, artifact id, or fixture id as
parser facts. Fixture bytes are read only by the test helper.

## Actual Source Audit

Direct source content was inspected in:

- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-skill/Cargo.toml`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- root `Cargo.toml`
- root `Cargo.lock`

The implementation imports:

- `MinimalReplayHeaderReader` only for the new minimal-header-attempt seam
- `ReplayHeader` only for the header-only evidence enum
- `ReplayInput` and `ReplayReader` for existing and new replay attempt boundaries
- `UnsupportedReplayReader`, which remains used by the existing unsupported-attempt realization

`mimir-skill` already depended on `mimir-replay`; no manifest or lockfile change was needed.

`crates/mimir-replay/src/lib.rs` was inspected directly. The parser behavior remains the existing
first minimal `MinimalReplayHeaderReader` behavior:

- `ReplayInput::Memory` only
- exact supported fixture tuple
- header parsing stops at `8 + header_size`
- `header_crc` read as layout only
- `content_crc` not read
- `ReplayInput::File` rejected

No `mimir-replay` parser behavior change is admitted by this pass.

## Public/API Surface Audit

The new public/API surface in `mimir-skill` is family-specific and explicitly named:

- `LowBoostRecoveryBcActualReplayParsingMinimalHeaderAttemptConfiguredReaderV1`
- `LowBoostRecoveryBcActualReplayParsingMinimalHeaderAttemptClassificationV1`
- `LowBoostRecoveryBcActualReplayParsingMinimalHeaderAttemptReplayHeaderEvidenceV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingMinimalHeaderAttemptRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingMinimalHeaderAttemptRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingMinimalHeaderAttemptRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingMinimalHeaderAttemptRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingMinimalHeaderAttemptRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingMinimalHeaderAttemptRealizationError`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_actual_replay_parsing_minimal_header_attempt_v1`

No generic parser framework abstraction was introduced.

## Seam Implementation Logic Audit

The admitted function consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`

The seam reuses the existing actual replay parsing contract validation through the unsupported
attempt validation path, mapped into the minimal-header-attempt error type.

Observed implementation facts:

- lane order is preserved from `contract.preserved_ordered_lane_results`
- specimen order is preserved from each lane's `ordered_specimen_results`
- `specimen_count` and `group_count` are copied from the validated contract
- per-specimen parser input is only
  `actual_replay_parsing_header_attempt.attempt_replay_input`
- `ReplayInput::Memory` is required before `MinimalReplayHeaderReader` invocation
- `ReplayInput::File` is rejected before parser invocation
- `MinimalReplayHeaderReader.read_header(...)` is called only after the memory requirement
- the seam does not construct `ReplayInput::File`
- the seam does not read files
- the seam does not derive parser facts from path, hash, filename, provenance, artifact id, or
  fixture id
- the seam is not routed through `mimir-export`, runtime, or CLI

The existing unsupported-attempt realization remains present and parallel:

- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_actual_replay_parsing_unsupported_attempt_v1`

It still uses `UnsupportedReplayReader`, records unsupported status, and records no replay header.

## Result Classification Audit

The admitted classifications are exactly:

- `minimal header parse success only`
- `minimal header parse failure only`

Success carries:

- `HeaderOnlyParserAttemptEvidence(ReplayHeader)`

Failure carries:

- `NoReplayHeaderProducedBecauseMinimalHeaderParseFailed`
- parser-attempt error message evidence
- no `ReplayHeader`

Result notes include:

- `ReplaySourceMaterializationNotClaimed`
- `BodyRawStateFrameAndEventParsingNotClaimed`
- `MimirExportIntegrationStillForbidden`
- `BroadParserSuccessRemainsClosed`

No result field or note claims raw-state parsing, frame parsing, event parsing, export readiness,
source materialization, or broad parser success.

## Test Audit

`crates/mimir-skill/src/lib.rs` tests cover the required seam behavior:

- fixture/header-only success path
- caller-supplied `ReplayInput::Memory` bytes and label
- `MinimalReplayHeaderReader` as the configured reader
- `minimal header parse success only`
- `ReplayHeader` only as header-only evidence
- no source materialization claim
- no body/raw-state/frame/event claim
- malformed memory failure path
- `minimal header parse failure only`
- file-backed attempt input rejected before parser invocation
- unsupported-attempt realization preserved
- `UnsupportedReplayReader` still records unsupported status
- `UnsupportedReplayReader` still records no replay header
- broad parser-success remains not admitted through result notes

The fixture-specific seam test skips only when the fixture is missing or unreadable. Its helper reads
fixture bytes only in tests, slices them to header-only bytes ending at `8 + header_size`, does not
claim CRC validation, and does not require body/raw-state/frame/event bytes.

`crates/mimir-replay/src/lib.rs` tests still cover the first minimal parser boundary, including
file-input rejection, unsupported tuple rejection, header-only success, and CRC non-validation.

## Forbidden Boundary Audit

No support was added for:

- `ReplayInput::File`
- file locator/materialization
- CRC validation
- `content_crc`
- body parsing
- raw-state payload parsing
- replay frames
- semantic replay events
- UTF-16 support
- nested array semantics
- broad version-family support
- unknown property-kind support
- export integration
- runtime/CLI behavior
- backend replay parser dependency

Direct forbidden crate/manifest checks found no `mimir-replay` parser integration in:

- `crates/mimir-cli`
- `crates/mimir-io`
- `crates/mimir-export`
- `crates/mimir-types`

`crates/mimir-cli/Cargo.toml`, `crates/mimir-io/Cargo.toml`,
`crates/mimir-export/Cargo.toml`, and `crates/mimir-types/Cargo.toml` were inspected directly and
do not add a `mimir-replay` dependency. The `mimir-skill` dependency on `mimir-replay` already
existed and is admitted for this seam.

## Git Boundary Caveat Audit

Actual source content was inspected directly.

Broad git status is unreliable for MIMIR-only boundary evidence because:

- `git rev-parse --show-toplevel` reports `D:/`
- broad `git status --short` reports unrelated files outside `D:\RocketLeague bot\MIMIR`

Therefore this audit does not rely on broad git status as proof.

Scoped command checks were still used as supporting tracked-file evidence:

- no tracked diff was reported for forbidden crates/manifests
- no tracked diff was reported for `crates/mimir-replay/src/lib.rs`
- parser backend dependency scan found no backend parser dependency matches

Those command checks are secondary to the direct file-content inspection.

## Exact Admitted Seam-Success Boundary

The admitted `mimir-skill` seam-success boundary is:

- caller explicitly invokes
  `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_actual_replay_parsing_minimal_header_attempt_v1`
- input is the already existing actual replay parsing contract
- each parser attempt consumes only the preserved `attempt_replay_input`
- each attempt input must be `ReplayInput::Memory`
- `MinimalReplayHeaderReader.read_header(...)` returns `ReplayHeader`
- the result records `minimal header parse success only`
- the `ReplayHeader` is carried only as header-only parser-attempt evidence

Parser-success remains admitted only for the first minimal parser boundary:

- `ReplayInput::Memory`
- exact fixture-supported tuple
- header-only parsing ending at `8 + header_size`

Parser-success is not admitted broadly.

## Exact Remaining Limitations

Still unadmitted:

- broad parser success
- `ReplayInput::File`
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- `content_crc` read or validation
- body parsing
- raw-state payload parsing
- replay frame extraction
- semantic replay events
- nested array semantics
- UTF-16 support
- broad replay version-family support
- unencountered property-kind support
- export integration
- runtime/CLI integration
- backend replay parser dependency

## Next Stage

Outcome A next stage:

- next pass may move to the next evidence/fixture/parser-readiness target or explicitly plan a later
  seam
- no export/runtime/CLI integration yet
- no broad parser expansion yet
