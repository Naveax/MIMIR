# MIMIR Skill Forge BC Replay Header Parser mimir-skill Seam Implementation v1

Pass date: 2026-05-04

## Purpose

Implement only the selected narrow parallel `mimir-skill` minimal-header-attempt seam from the
reopened planning pass.

This pass adds an explicit opt-in path in `crates/mimir-skill/src/lib.rs` that can call
`MinimalReplayHeaderReader` using only the already preserved
`actual_replay_parsing_header_attempt.attempt_replay_input`.

It does not replace the existing unsupported-attempt realization. It does not broaden parser scope,
replay-source materialization, export behavior, CLI behavior, runtime behavior, dependency surface,
or `mimir-replay` parser behavior.

## Selected Outcome

Selected outcome:

- Outcome A

The exact planned seam was implemented.

## Files Changed

Rust source changed:

- `crates/mimir-skill/src/lib.rs`

Artifacts added:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_MIMIR_SKILL_SEAM_IMPLEMENTATION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_skill_seam_implementation_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_skill_seam_implementation_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_skill_seam_implementation_status.txt`

Forbidden Rust/manifest/parser files were not modified.

## Public/API Surface Added in mimir-skill

The pass added the explicit opt-in seam:

- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_actual_replay_parsing_minimal_header_attempt_v1`

It also added family-specific result, note, classification, evidence, configured-reader, disposition,
and error types for that seam only.

The success/failure classification enum exposes exact labels:

- `minimal header parse success only`
- `minimal header parse failure only`

## Exact Seam Implemented

The seam consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`

For each specimen it uses only:

- `actual_replay_parsing_header_attempt.attempt_replay_input`

Before invoking the reader, it requires:

- `ReplayInput::Memory`

It invokes:

- `MinimalReplayHeaderReader.read_header(...)`

The call is made against the preserved memory `ReplayInput`; no file path, hash, filename, fixture
id, source replay provenance, artifact id, audited family root, or receipt lineage is used as a
parser fact.

## Exact Result Classification

Success is recorded only as:

- `minimal header parse success only`

Failure is recorded only as:

- `minimal header parse failure only`

A successful result may carry `ReplayHeader` only as:

- `HeaderOnlyParserAttemptEvidence`

A failed result carries only parser-attempt error evidence and no replay header.

Neither success nor failure implies replay-source materialization, file/path/hash/provenance proof,
raw-state availability, frame availability, event availability, export readiness, runtime readiness,
or broad parser readiness.

## Tests Added

Tests were added only inside `crates/mimir-skill/src/lib.rs`.

They cover:

- caller-supplied `ReplayInput::Memory` bytes and label are used
- `MinimalReplayHeaderReader` is the configured reader for the new seam
- fixture-backed header-only memory records `minimal header parse success only`
- success carries `ReplayHeader` only as header-only parser-attempt evidence
- success does not claim replay-source materialization
- success does not claim body/raw-state/frame/event parsing
- malformed memory records `minimal header parse failure only`
- file-backed attempt input is rejected
- existing unsupported-attempt realization still uses `UnsupportedReplayReader`
- existing unsupported-attempt realization still records unsupported status and no replay header
- export integration remains explicitly forbidden
- broad parser-success remains closed

## Fixture Behavior

Fixture-specific success testing reads bytes from:

- `$env:MIMIR_REPLAY_FIXTURE_PATH`, if set
- otherwise `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`

The test derives a header-only byte slice ending at `8 + header_size` and supplies those bytes as
caller-admitted memory through the existing contract object. The seam itself does not read files and
does not derive parser facts from fixture path, hash, filename, or fixture id.

Verified fixture identity for this pass:

- fixture id: `rl_replay_header_fixture_001`
- path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`
- admission form: `PRIVATE_LOCAL_PATH_WITH_HASH`

## Unsupported-Attempt Preservation

The existing function remains present and unchanged in behavior:

- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_actual_replay_parsing_unsupported_attempt_v1`

It still uses:

- `UnsupportedReplayReader`

It still records:

- unsupported status
- no replay header
- unsupported reason

The new seam is parallel and opt-in. It does not replace the unsupported path or alter default
reader behavior.

## Why Parser Scope Was Not Broadened

The implementation does not modify `mimir-replay`.

The only parser-success path remains the existing `MinimalReplayHeaderReader` boundary:

- `ReplayInput::Memory`
- exact fixture-supported tuple
- header-only parse ending at `8 + header_size`

No CRC validation was added. `content_crc` is not read. Body, raw-state, frame, event, nested array,
UTF-16, broad version-family, and unencountered property-kind parsing remain unadmitted.

## Forbidden Boundaries Preserved

Preserved:

- no `ReplayInput::File` support
- no file reading in the seam
- no replay-source materialization
- no export routing
- no CLI/runtime behavior
- no backend parser dependency
- no manifest or lockfile change
- no `mimir-replay` parser behavior change
- no `mimir-cli`, `mimir-io`, `mimir-export`, or `mimir-types` change

## Next Stage

Next pass should be a seam implementation audit/admission pass.

No broad parser expansion, export integration, runtime integration, CLI integration, replay-source
materialization, or body/raw-state/frame/event parsing is admitted yet.
