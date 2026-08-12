# MIMIR Skill Forge BC Emitted-Output Audit / Readback Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded low-boost-recovery-specific emitted-output audit/readback
boundary on top of the already-emitted actual filesystem output.

It defines:

- one exact input boundary above `LowBoostRecoveryBcActualFilesystemEmissionReceiptV1`
- one exact first emitted-output audit/readback role
- one minimal family-specific audit/readback success result surface
- one strict admission rule for when an actual filesystem emission receipt may enter audit/readback
- one strict hard-failure rule for malformed receipts, missing output, invalid emitted JSON, or
  readback/ordering mismatch

### Why it exists

The actual filesystem emission pass already fixed:

- strict input from `LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`
- deterministic root/lane/specimen path emission
- one real family-specific specimen JSON contract on disk
- ordered emission receipts
- destination-conflict handling
- hard failure on malformed plan input
- best-effort cleanup on write failure after root creation

That still left one unresolved question:

- how to re-open and audit emitted low-boost-recovery output through the actual filesystem
  boundary, without reopening lower planning layers, without touching `mimir_export`, and without
  pretending emitted JSON has already become tensors, controls, or bundle semantics

This pass exists to answer that question narrowly and explicitly.

### How it differs from adjacent stages

- Actual filesystem emission owns writing deterministic output and returning the ordered receipt.
- This pass owns verifying that the emitted output still exists exactly where the receipt says and
  that family-specific JSON readback still matches the emitted contract.
- A later pass may decide whether a family-specific sidecar or manifest is required for later
  consumers, but this pass does not add one.

This pass is not:

- actual filesystem emission
- `mimir_export` integration
- generic manifest/index orchestration
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

Emitted-output audit/readback remains family-specific because:

- the receipt being audited comes only from the low-boost-recovery actual filesystem emission
  boundary
- the readback helper re-opens one low-boost-recovery specimen JSON contract only:
  `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
- the audit still reasons about low-boost-recovery lane ordinals, specimen ordinals, artifact ids,
  lineage fields, and bounded confidence/assumption semantics
- no second BC family exists yet to justify a shared emitted-output audit framework

No generic all-family emitted-output audit/readback framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcActualFilesystemEmissionReceiptV1`
- the emitted family root directory and descendant lane/specimen paths referenced by that receipt
- `read_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(...)` in `mimir-io`

Within the receipt, this pass consumes:

- `emitted_family_root_directory`
- ordered `ordered_lane_receipts`
- each `lane_ordinal`
- each `emitted_lane_directory`
- each ordered `ordered_specimen_receipts`
- each `specimen_ordinal`
- each `artifact_id`
- each `emitted_specimen_file_path`

### Boundary rule

Direct emitted-output audit/readback input is no longer:

- filesystem/export-emission plans
- downstream consumer results
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- accepted shells
- lower planning boundaries

Those earlier boundaries are already frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcActualFilesystemEmissionReceiptV1` plus the emitted filesystem output it
points to.

## D. EMITTED-OUTPUT AUDIT / READBACK ROLE

The first bounded emitted-output audit/readback role is:

- admit only already-emitted low-boost-recovery actual filesystem emission receipts
- revalidate that the receipt boundary is still intact without recreating it from lower layers
- verify that the emitted family root directory exists exactly where the receipt says
- verify that every emitted lane directory exists exactly where the receipt says
- verify that every emitted specimen file exists exactly where the receipt says
- re-open every emitted specimen JSON file through the family-specific readback helper
- verify that each read-back payload still satisfies the emitted specimen contract and still
  matches the receipt's ordinals and artifact identity
- return only a bounded audit/readback success result when all of those checks pass

### What it is allowed to verify

This pass may verify only:

- receipt shape and deterministic path expectations
- family root existence
- lane directory existence
- specimen file existence
- family-specific specimen JSON parse/readback success
- read-back specimen contract validity
- lane order and specimen order as represented by receipt order plus emitted ordinals
- artifact identity alignment between receipt and read-back specimen payload

### What it is not allowed to materialize yet

This pass is not allowed to materialize or infer:

- generic manifests or indexes
- `mimir_export` bundle state
- replay/raw-state payloads behind references
- tensors, feature vectors, or normalization outputs
- controls, actions, or labels
- usefulness claims
- policy-improvement claims
- replay/physics truth upgrades

The role here is audit/readback only, not consumer materialization.

## E. AUDIT / READBACK OUTPUT V1

The minimum family-specific emitted-output audit/readback success result is:

- `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`

It contains exactly:

- `specimen_count`
- `group_count`
- `emitted_family_root_directory`
- `family_root_directory_exists`
- `ordered_lane_results`
- `audit_disposition`
- `audit_notes`

### Lane-level audit/readback shape

Each `ordered_lane_results` entry is:

- `LowBoostRecoveryBcEmittedOutputAuditReadbackLaneResultV1`

It contains exactly:

- `lane_ordinal`
- `emitted_lane_directory`
- `lane_directory_exists`
- ordered `ordered_specimen_results`

### Specimen-level audit/readback shape

Each `ordered_specimen_results` entry is:

- `LowBoostRecoveryBcEmittedOutputAuditReadbackSpecimenResultV1`

It contains exactly:

- `specimen_ordinal`
- `artifact_id`
- `emitted_specimen_file_path`
- `specimen_file_exists`
- `readback_matches_receipt_contract`
- `readback_specimen`

`readback_specimen` is the re-opened
`LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`.

### Preserved receipt counts and ordering

`group_count` is the number of ordered lane receipts admitted into audit/readback.

`specimen_count` is the number of ordered specimen receipts admitted into audit/readback across
all lanes.

Lane order is preserved through `ordered_lane_results` vector order.

Specimen order is preserved through each lane's `ordered_specimen_results` vector order.

### Bounded audit/readback disposition

`audit_disposition` is fixed to exactly:

- `ready_for_low_boost_recovery_emitted_output_refinement_only`

That means only:

- the emitted output has passed this bounded receipt/path/readback audit
- the next pass may refine or decide the next family-specific emitted-output boundary

It does not mean:

- ready for `mimir_export`
- ready for generic manifests
- ready for tensors
- ready for controls/actions
- usefulness proved

### Bounded audit/readback notes

`audit_notes` are fixed to exactly:

- `actual_filesystem_emission_receipt_boundary_preserved`
- `emitted_root_lane_specimen_paths_verified`
- `family_specific_specimen_readback_verified`
- `no_additional_semantics_inferred_beyond_emitted_contract`
- `tensor_and_control_materialization_deferred`
- `mimir_export_integration_deferred`

There is no generic metadata bag.

## F. AUDIT / READBACK RULES

### Receipt-shape rule

The receipt must remain internally aligned with the deterministic actual emission boundary:

- emitted family root directory basename must remain `low_boost_recovery_bc_v1`
- lane receipt vector must be non-empty
- each `lane_ordinal` must match the concrete lane position
- each `emitted_lane_directory` must equal:
  `emitted_family_root_directory/recovery_context_lane_{lane_ordinal:04}`
- each lane receipt must contain at least one ordered specimen receipt
- each `specimen_ordinal` must match the concrete specimen position
- each `artifact_id` must be present and unique across the full receipt
- each `emitted_specimen_file_path` must equal:
  `emitted_lane_directory/specimen_{specimen_ordinal:04}.json`
- emitted lane directory paths and specimen file paths must remain unique across the full receipt

### Filesystem existence rule

Audit/readback verifies all of the following:

- emitted family root directory exists and is a directory
- every emitted lane directory exists and is a directory
- every emitted specimen path exists and is a file

### Readback rule

Every emitted specimen JSON file is re-opened only through:

- `read_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(...)`

No alternate parser, lower-level source reconstruction, or generic export loader is used.

### Read-back contract rule

For every read-back specimen payload, audit/readback verifies:

- the payload parses as `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
- the payload still satisfies the family-specific emitted contract:
  - `artifact_id` present and still derived from `accepted_reference_variant_id`
  - lineage ids/references present
  - `accepted_reference_window` remains a valid bounded window
  - observation binding kind remains
    `accepted_reference_window_from_raw_state_window_ref`
  - supervision window role remains `accepted_reference_variant_window`
  - target binding kind remains `accepted_reference_variant_control_target_deferred`
  - confidence band remains `boundary_stable`
  - unresolved assumptions remain the exact low-boost-recovery bounded set
- `lane_ordinal` matches the enclosing lane receipt
- `specimen_ordinal` matches the specimen receipt
- `artifact_id` matches the specimen receipt

### Ordering rule

Audit/readback verifies lane order and specimen order only against the admitted receipt boundary:

- lane receipt vector order must align with `lane_ordinal`
- specimen receipt vector order within each lane must align with `specimen_ordinal`
- read-back `lane_ordinal` and `specimen_ordinal` must still align with that receipt order

This pass does not reopen lower planning layers to infer another ordering source.

### No-semantic-widening rule

This pass verifies emitted JSON only as the emitted specimen contract already states.

It does not infer:

- tensors from observation binding
- controls from target binding
- replay truth from raw-state references
- generic dataset semantics from the emitted filesystem layout

## G. ADMISSION RULES

An actual filesystem emission receipt may enter audit/readback only when all of the following hold:

1. the input is `LowBoostRecoveryBcActualFilesystemEmissionReceiptV1`
2. `emitted_family_root_directory` basename remains `low_boost_recovery_bc_v1`
3. `ordered_lane_receipts` is non-empty
4. every lane receipt remains aligned with deterministic lane ordinals and lane-directory naming
5. every lane receipt contains at least one ordered specimen receipt
6. every specimen receipt remains aligned with deterministic specimen ordinals and specimen file
   naming
7. every specimen `artifact_id` remains present and unique
8. no lower boundary is silently re-opened to recreate or repair the receipt
9. the emitted family root directory used for audit/readback is exactly the directory referenced by
   the receipt

Admission here means only:

- this receipt plus the emitted filesystem output it points to may be audited and re-opened
  through the family-specific readback helper

Admission here does not mean:

- usefulness proved
- a later consumer can work without the receipt
- `mimir_export` compatibility proved

## H. FAILURE RULES

Audit/readback fails explicitly for:

- malformed actual filesystem emission receipt
- malformed lane receipt
- malformed specimen receipt
- missing or non-directory emitted family root
- missing or non-directory emitted lane directory
- missing or non-file emitted specimen path
- unreadable or invalid emitted specimen JSON
- read-back specimen payload that violates the emitted contract
- read-back lane ordinal mismatch
- read-back specimen ordinal mismatch
- read-back artifact id mismatch

### Failure classification

Hard fail before readback:

- malformed receipt
- malformed lane receipt
- malformed specimen receipt
- missing/invalid emitted root directory
- missing/invalid emitted lane directory
- missing/invalid emitted specimen file

Hard fail during readback:

- readback helper failure
- invalid emitted specimen JSON contract
- read-back mismatch against receipt ordinals or artifact id

### Failure behavior

- no repair is allowed
- no receipt regeneration from plans or lower boundaries is allowed
- no directory recreation is allowed
- no specimen is skipped
- no resorting is allowed
- no inferred manifest/index is added
- no partial audit success result is returned

This pass hard-fails instead of repairing or inferring.

## I. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic multi-family emitted-output audit/readback framework
- no generic manifest/index semantics
- no tensor materialization
- no control/action extraction
- no usefulness proof
- no policy-improvement proof
- no replay parsing
- no replay ingestion
- no replay mining
- no rollout or physics work
- no async/background system
- no database work

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

The next pass now has one explicit low-boost-recovery emitted-output audit/readback boundary that:

- starts strictly from `LowBoostRecoveryBcActualFilesystemEmissionReceiptV1`
- consumes the real emitted filesystem output instead of reopening lower BC stages
- verifies that emitted root/lane/specimen paths still exist exactly where the receipt says
- re-opens every emitted specimen JSON file through the family-specific `mimir-io` readback helper
- verifies emitted specimen payload contract validity plus receipt-order alignment
- still does not widen into `mimir_export`

### What remains deferred

This pass still does not guarantee:

- receipt-independent reopen semantics
- family-specific sidecar or manifest semantics
- generic bundle/index orchestration
- `mimir_export` wiring
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- one low-boost-recovery-specific emitted-output refinement or sidecar/manifest decision pass
- still without `mimir_export` widening unless that separate decision is explicitly reopened
