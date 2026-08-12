# MIMIR Skill Forge BC Replay Header Parser mimir-skill Seam Planning Reopen v1

Pass date: 2026-05-04

## Purpose

This is a planning-only reopen pass for a future `mimir-skill` opt-in seam that may later call
`MinimalReplayHeaderReader`.

This pass does not implement the seam. It does not modify Rust source, parser behavior, runtime
behavior, CLI behavior, export behavior, manifests, lockfiles, or dependencies.

The question answered here is narrow:

- Can a future `mimir-skill` seam be planned without broadening parser-success, replay-source
  materialization, runtime behavior, CLI behavior, or export behavior?

## Selected Outcome

Selected outcome:

- Outcome A

`mimir-skill` seam planning is reopened and complete.

The next pass may implement only the exact planned seam, if separately scoped. The seam remains
strictly opt-in and header-only. No parser expansion is admitted.

## Current Admitted Parser Boundary

The current admitted parser-success boundary remains unchanged.

Parser-success is admitted only when all of the following hold:

- input is `ReplayInput::Memory`
- `ReplayInput::Memory.label` is non-empty and already admitted by the caller
- `ReplayInput::Memory.bytes` are already admitted by the caller
- parsing stops at `8 + header_size`
- the top-level `None` terminator ends exactly at `8 + header_size`
- the exact fixture-supported tuple is present:
  - `major_version = 868`
  - `minor_version = 32`
  - `net_version = 10`
  - `game_type = TAGame.Replay_Soccar_TA`
  - `ReplayVersion = 8`
  - `BuildVersion = 241206.55345.468477`
- the result is only a `ReplayHeader`

Parser-success is not admitted broadly.

No CRC validation is admitted. `header_crc` is read as layout only by the existing parser and is not
validated. `content_crc` is not read or validated. Body, raw-state, frame, footer, event, nested
array semantic parsing, UTF-16 text, unencountered property kinds, `ReplayInput::File`, runtime,
CLI, export, and backend parser dependency support remain unadmitted.

## Re-audit Inputs

The following inputs were inspected before this artifact was written:

- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-skill/Cargo.toml`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- `crates/mimir-replay/README.md`
- root `Cargo.toml`
- root `Cargo.lock`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_READINESS_HANDOFF_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_MIMIR_REPLAY_README_EXAMPLE_TEST_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIRST_MINIMAL_IMPLEMENTATION_AUDIT_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_readiness_handoff_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_readiness_handoff_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_readiness_handoff_status.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_replay_readme_example_test_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_replay_readme_example_test_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_replay_readme_example_test_status.txt`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

Fixture identity was verified:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`
- admission form: `PRIVATE_LOCAL_PATH_WITH_HASH`

The fixture path, byte length, hash, and fixture id remain external evidence about supplied bytes.
They are not parser facts and do not widen parser admission.

## Current mimir-skill Replay/Parser-attempt Surface

Observed `mimir-skill` facts:

- `crates/mimir-skill/src/lib.rs` imports `mimir_replay::{ReplayInput, ReplayReader,
  UnsupportedReplayReader}`.
- `mimir-skill` already depends on `mimir-replay` through `crates/mimir-skill/Cargo.toml`.
- Root `Cargo.toml` and `Cargo.lock` already contain `mimir-replay` and `mimir-skill`; no manifest
  or lockfile change is needed for a future seam.
- `mimir-skill` does not currently import or use `MinimalReplayHeaderReader`.
- `mimir-skill` already has a byte-backed caller-admitted source-form boundary:
  `caller_admitted_replay_bytes` are validated as non-empty before being carried upward.
- That byte payload is later preserved as `opaque_caller_admitted_replay_bytes`.
- Replay-input creation constructs only:
  `ReplayInput::Memory { label, bytes }`
- The label is derived by
  `low_boost_recovery_bc_replay_input_creation_label_from_boundary_input_v1(...)`.
- The bytes are exactly the preserved `opaque_caller_admitted_replay_bytes`.
- The actual replay parsing contract carries a preserved `ReplayInput` and a
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingHeaderAttemptV1`.
- The header-attempt object has `attempt_replay_input: ReplayInput` and names the future parser
  surface as `MimirReplayReplayReaderReadHeaderOfReplayInput`.
- The only executed current parser-attempt realization is
  `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_actual_replay_parsing_unsupported_attempt_v1(...)`.
- That realization instantiates `UnsupportedReplayReader`, calls
  `.read_header(&actual_replay_parsing_header_attempt.attempt_replay_input)`, requires an error,
  records `ConfiguredUnsupportedReplayReaderReturnedError`, and records
  `NoReplayHeaderProduced`.
- Existing tests assert that the unsupported attempt preserves the memory label, preserves the byte
  payload, records unsupported status, records no replay header, rejects identity drift, and remains
  deterministic.

Current conclusion:

- `mimir-skill` has an already admitted `ReplayInput::Memory` / byte-backed caller-admitted source
  boundary.
- The current parser-attempt realization is tied to `UnsupportedReplayReader`.
- A future header seam can be added only as a parallel explicitly named path. It must not replace,
  weaken, or silently change the existing unsupported-attempt semantics.

## Seam Design Classification

Option A - docs-only seam planning, no implementation next:

- Classification: safe but not selected.
- Reason: current architecture evidence is sufficient to plan a narrower future `mimir-skill` seam.
- This remains a fallback if a later implementation pass is not desired.

Option B - narrow parallel header-attempt seam in `mimir-skill`:

- Classification: selected future seam.
- The future seam may call `MinimalReplayHeaderReader` only with already admitted
  `ReplayInput::Memory` bytes and a non-empty label.
- It must preserve the current unsupported-attempt result as a separate truthful path.
- It may record header-only parser-attempt evidence.
- It must not treat success as replay-source materialization.
- It must not route to export.
- It must not read files.
- It must not construct `ReplayInput::File`.

Option C - replace existing `UnsupportedReplayReader` attempt:

- Classification: rejected.
- Reason: it would silently change the current truthful unsupported behavior and could turn a
  parser-readiness seam into a default parser-success path.

Option D - CLI/runtime seam:

- Classification: rejected in this pass.
- Reason: it would create user-visible CLI/runtime behavior and likely replay-source
  materialization semantics.

Option E - export seam:

- Classification: rejected in this pass.
- Reason: it would route header parse success into `mimir-export` and widen export semantics.

Option F - replay-source materialization/file locator seam:

- Classification: rejected in this pass.
- Reason: it would conflate header parsing with source discovery, file loading, or actual
  replay-source materialization.

## Selected Future Seam

Selected design:

- Option B - narrow parallel header-attempt seam in `mimir-skill`

Exact future function boundary:

- Add a separately named function in `crates/mimir-skill/src/lib.rs`, with a name at least as
  explicit as:
  `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_actual_replay_parsing_minimal_header_attempt_v1`
- The function must consume only the already existing
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`
  or a stricter internal object derived from it.
- For each specimen, the function must use only the existing
  `actual_replay_parsing_header_attempt.attempt_replay_input`.
- Before invoking the reader, it must require the attempt input to be `ReplayInput::Memory`.
- It must call:
  `MinimalReplayHeaderReader.read_header(&ReplayInput::Memory { label, bytes })`
- The `label` and `bytes` in that call must be the caller-admitted memory label and bytes already
  preserved by the contract.
- The call must not use fixture id, path, hash, filename, artifact id, source replay provenance,
  audited family root, or receipt lineage to derive parser facts.

Allowed result classification:

- success: `minimal header parse success only`
- failure: `minimal header parse failure only`

The future result may carry `ReplayHeader` evidence only as header-only parser-attempt evidence. It
must not carry or imply body bytes, raw-state payloads, frames, events, export readiness, broad
parser readiness, source materialization, file validation, path validation, hash validation, or
provenance proof.

## Exact Future Implementation File Boundary

If Outcome A is used by a later implementation pass, the allowed write boundary is:

- `crates/mimir-skill/src/lib.rs`

The future implementation pass must not modify:

- `crates/mimir-cli`
- `crates/mimir-io`
- `crates/mimir-export`
- `crates/mimir-types`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- root `Cargo.toml`
- root `Cargo.lock`

No manifest changes are required because `mimir-skill` already depends on `mimir-replay`.

No dependency additions are allowed. No backend replay parser dependency is allowed. Tests must stay
inside `crates/mimir-skill/src/lib.rs`. No fixture copying, external fixture addition, export
integration, CLI behavior, runtime behavior, or file input support is allowed.

## Exact Future Test Boundary

Future implementation tests must prove the following and nothing broader:

- the new seam uses caller-supplied `ReplayInput::Memory` bytes and label
- the reader invocation is explicitly `MinimalReplayHeaderReader`
- success is recorded only as `minimal header parse success only`
- failure is recorded only as `minimal header parse failure only`
- success preserves header-only semantics and does not require body bytes beyond `8 + header_size`
- the current unsupported-attempt realization remains unchanged where required
- the unsupported path still records `UnsupportedReplayReader`, unsupported status, and no replay
  header
- a file-backed attempt input is rejected and does not add `ReplayInput::File` support
- failure does not imply source/materialization failure
- no export routing occurs
- no body/raw-state/frame/event parsing is exposed or claimed
- no dependency, manifest, or lockfile addition is required
- broad parser-success remains not admitted

Test inputs may be preloaded bytes supplied by the test harness or minimal in-memory bytes that
match the admitted tuple. The seam itself must never read files and must never derive parser facts
from path, hash, fixture id, filename, provenance, or artifact id.

## Rejected Seam Designs

Rejected for this pass and any next implementation pass under this artifact:

- replacing `UnsupportedReplayReader`
- changing `UnsupportedReplayReader`
- changing the global/default replay reader behavior
- adding `ReplayInput::File` support
- adding file/path locator behavior
- adding replay-source actual materialization
- adding CLI behavior
- adding runtime behavior
- adding export behavior
- modifying `mimir-export`
- modifying `mimir-io`
- modifying `mimir-types`
- modifying root `Cargo.toml`
- modifying root `Cargo.lock`
- adding dependencies
- adding backend replay parser dependencies
- adding CRC validation
- reading or validating `content_crc`
- parsing body/raw-state/frame/event data
- adding nested array semantic parsing
- adding UTF-16 support
- adding broad version-family support
- adding unencountered property-kind support
- deriving parser facts from path/hash/filename/provenance/artifact id

## Forbidden Boundaries Preserved

This planning pass preserves the following boundaries:

- parser behavior changed: no
- parser-success broadened: no
- `MinimalReplayHeaderReader` defaulted globally: no
- `UnsupportedReplayReader` changed: no
- `ReplayInput::File` support added: no
- CRC validation added: no
- body/raw-state/frame/event parsing added: no
- replay-source materialization added: no
- CLI/runtime behavior added: no
- export behavior added: no
- backend replay parser dependency added: no
- manifests changed: no
- lockfile changed: no
- Rust source changed: no

## Next Stage

Outcome A next stage:

- A later pass may implement only the selected Option B `mimir-skill` narrow parallel
  minimal-header-attempt seam.
- That implementation pass may modify only `crates/mimir-skill/src/lib.rs`.
- The seam must remain opt-in, header-only, and parallel to the current unsupported-attempt
  realization.
- No broad parser expansion is admitted yet.
