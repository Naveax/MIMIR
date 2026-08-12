# MIMIR Skill Forge BC Receipt-Bound Specimen-File Existence/Readback Validation v1

## A. PURPOSE

### What this pass owns

This pass owns the first filesystem-truth boundary above:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorRealizationResultV1`

It defines and implements exactly:

- one family-specific existence/readback validation result:
  - `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
- one family-specific validation disposition:
  - `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationDispositionV1`
- one family-specific validation note set:
  - `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationNoteV1`
- one family-specific per-specimen validation surface:
  - `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationSpecimenResultV1`
- one family-specific error surface:
  - `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationError`
- one family-specific entry function:
  - `validate_low_boost_recovery_bc_receipt_bound_specimen_file_existence_readback_v1(...)`

### Why it exists

The realized-locator boundary below this pass already fixed:

- one anchored BC specimen-file path per admitted specimen
- the exact deterministic relative path rule
- the exact path-only receipt-bound identity tuple carried with that path

What was still missing was proof that:

- the anchored path actually exists on disk
- the anchored path is a readable specimen file
- the read-back specimen-file content still agrees with the realized locator on the identity fields
  this boundary is allowed to audit

### How it differs from the path-only locator-realization boundary below it

- The lower boundary realizes only `PathBuf` locator state.
- This pass verifies filesystem truth for those realized paths.
- This pass performs only narrow family-specific JSON readback and identity alignment checks.
- This pass still does not materialize raw state, tensors, or controls.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this validation version.

This boundary remains family-specific because:

- the only admitted source input is
  `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorRealizationResultV1`
- the on-disk specimen-file contract being read back is the low-boost-recovery-specific JSON
  contract:
  - `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
- the deterministic lane/specimen path rule remains the low-boost-recovery BC rule:
  - `recovery_context_lane_{lane_ordinal:04}`
  - `specimen_{specimen_ordinal:04}.json`
- no second family exists that would justify a shared readback or validation framework

No generic all-family locator/index/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorRealizationResultV1`
- the audited family root directory reference already preserved by that result

Within `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorRealizationResultV1`,
this pass consumes:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `realized_locator.lane_ordinal`
- each `realized_locator.specimen_ordinal`
- each `realized_locator.artifact_id`
- each `realized_locator.source_raw_state_window_ref`
- each `realized_locator.deterministic_bc_specimen_file_relative_path`
- each `realized_locator.anchored_bc_specimen_file_path`
- `realization_disposition`
- `realization_notes`

Direct input is no longer:

- contract-definition results
- planning results
- proof results
- reopen decisions
- first concrete specimen consumer results
- continued receipt-bound downstream results
- emitted-output audit/readback results
- actual emission receipts
- plans
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- shells
- lower planning boundaries

Those lower layers remain frozen. This pass starts strictly from the realized locator result and
its preserved audited family root anchor.

## D. VALIDATION ROLE

This pass owns exactly one thing:

- validating that one realized receipt-bound BC specimen-file locator points at a real readable
  low-boost-recovery specimen file whose read-back content still agrees with the realized locator
  on the identity fields this boundary is allowed to audit

This pass is allowed to verify:

- the realized locator input is still well-formed
- the deterministic relative path shape is still correct
- `anchored_bc_specimen_file_path ==
  audited_family_root_directory.join(deterministic_bc_specimen_file_relative_path)`
- the anchored path exists
- the anchored path is a file
- the anchored file can be deserialized with the existing repo-local readback helper
- the read-back specimen file remains compatible with the existing family-specific emitted specimen
  contract
- the read-back specimen file still matches the realized locator on:
  - `lane_ordinal`
  - `specimen_ordinal`
  - `artifact_id`
  - `source_raw_state_window_ref`

This pass is not allowed to materialize yet:

- raw-state payloads
- replay data
- raw-state-window frames
- observation tensors
- control/action payloads
- sidecars or manifests
- generic indexes
- `mimir_export` integration

## E. EXISTENCE / READBACK VALIDATION SHAPE V1

The exact boundary is:

- existence plus narrow contract-preserving readback

It is not filesystem-existence-only.

### Exact per-specimen input consumed

For one realized specimen, this pass consumes exactly:

- enclosing `lane_ordinal`
- enclosing `specimen_ordinal`
- `realized_locator.lane_ordinal`
- `realized_locator.specimen_ordinal`
- `realized_locator.artifact_id`
- `realized_locator.source_raw_state_window_ref`
- `realized_locator.deterministic_bc_specimen_file_relative_path`
- `realized_locator.anchored_bc_specimen_file_path`
- `audited_family_root_directory`

### Exact readback helper used

Readback uses exactly the existing repo-local helper:

- `mimir_io::read_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(...)`

After deserialization, compatibility with the existing emitted specimen-file contract is checked
with the existing family-specific validator already present in `mimir-skill`:

- `validate_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_for_audit(...)`

### Exact identity checks

For one admitted realized locator, all of the following must hold:

1. the deterministic relative path must still equal:
   - `recovery_context_lane_{lane_ordinal:04}/specimen_{specimen_ordinal:04}.json`
2. `anchored_bc_specimen_file_path` must still equal:
   - `audited_family_root_directory.join(deterministic_bc_specimen_file_relative_path)`
3. the anchored path must exist
4. the anchored path must be a file
5. the read-back specimen file must deserialize as
   `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
6. the read-back specimen file must pass the existing emitted-specimen compatibility validator
7. `readback.lane_ordinal == realized_locator.lane_ordinal`
8. `readback.specimen_ordinal == realized_locator.specimen_ordinal`
9. `readback.artifact_id == realized_locator.artifact_id`
10. `readback.source_raw_state_window_ref ==
    realized_locator.source_raw_state_window_ref`

Because the deterministic relative path is already bound to the realized locator ordinals, and the
read-back ordinals must match the realized locator ordinals, this boundary also detects content-vs-
path drift for lane/specimen identity without inventing any new path semantics.

### What this boundary explicitly refuses to promise

This pass still does not promise:

- that raw state is present in the specimen file
- that replay frames have been parsed
- that `source_raw_state_window_ref` can yet be resolved to live raw-state payloads
- that tensors are available
- that controls are available
- that the specimen file is useful for policy improvement

## F. VALIDATION OUTPUT V1

The minimum family-specific output is:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_realization_disposition`
- preserved `source_realization_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane/specimen results
- chosen `validation_disposition`
- bounded `validation_notes`

The lane/specimen result types are:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationSpecimenResultV1`

Each lane result contains:

- `lane_ordinal`
- ordered `ordered_specimen_results`

Each specimen result contains:

- `specimen_ordinal`
- preserved `preserved_realized_locator`
- `specimen_file_exists`
- `readback_matches_realized_locator_identity`
- `readback_specimen`

The exact validation disposition is fixed to:

- `ValidatedForReceiptBoundBcSpecimenFileExistenceAndIdentityPreservingReadbackOnly`

The exact validation notes are fixed to:

- `ReceiptBoundSpecimenFileAnchoredLocatorRealizationBoundaryPreserved`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `DeterministicRelativeSpecimenFilePathShapeRevalidated`
- `AnchoredBcSpecimenFileExistenceVerified`
- `FamilySpecificSpecimenFileReadbackValidated`
- `ReadbackIdentityAlignedWithRealizedLocator`
- `RawStateMaterializationDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The realized locator result may enter this boundary only when all of the following hold:

1. the input is exactly
   `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorRealizationResultV1`
2. `source_contract_disposition ==
   ContractDefinedForReceiptBoundSpecimenFileLookupSourceOnly`
3. `source_contract_notes` still equal the exact contract-note set frozen below this boundary
4. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
5. `realization_disposition == RealizedForReceiptBoundAnchoredBcSpecimenFilePathOnly`
6. `realization_notes` still equal the exact realization-note set frozen below this boundary
7. `specimen_count > 0`
8. `group_count > 0`
9. `group_count` equals the number of preserved ordered lane results
10. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
11. `audited_family_root_directory` exists and is a directory at validation time
12. lane order and specimen order still match concrete lane/specimen position
13. the realized locator path semantics still match the deterministic low-boost-recovery
    lane/specimen rule
14. no lower boundary is silently reopened to repair or reinterpret the admitted realized locator

Admission here means only:

- this family-specific existence/readback validation boundary may run on the trusted realized
  locator result

Admission here does not mean:

- raw-state materialization is legal
- sidecar/manifest realization is justified
- `mimir_export` may be widened

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded realization input
- missing file
- anchored path that exists but is not a file
- path drift
- identity drift
- invalid or incompatible readback content
- readback deserialization failure
- any attempt to reinterpret the audited family root as raw-state storage
- any attempt to widen this boundary into raw-state materialization

### Failure behavior

- no repair is allowed
- no file recreation is allowed
- no specimen is skipped
- no resorting is allowed
- no guessed path repair is allowed
- no partial validation result is returned
- no read-back field beyond the validated identity tuple is promoted into new semantics

## I. NON-GOALS

This pass does not do any of the following:

- no raw-state payload materialization
- no replay parsing
- no raw-state locator/index implementation beyond existence/readback validation above the realized
  locator
- no `mimir_export` integration
- no sidecar/manifest realization
- no generic manifest/index framework
- no tensor materialization
- no control/action extraction
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- each admitted realized locator has been checked against actual filesystem truth
- each admitted realized locator now has one bounded family-specific read-back specimen result
- the realized locator remains aligned with the read-back specimen on the exact audited identity
  tuple
- the audited family root still remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual raw-state-window materialization
- raw-state lookup success from `source_raw_state_window_ref`
- replay-frame access
- observation/tensor/control materialization

The immediate next pass should be:

- a raw-state materialization reopen decision above this existence/readback validation result

That is the next honest step because:

- locator shape is already fixed
- filesystem truth is now validated
- specimen-file content has now been read back as far as this boundary may legally go
- the remaining unresolved problem is no longer file existence or identity alignment
- the remaining unresolved problem is whether the project should explicitly reopen the next
  boundary required to turn `source_raw_state_window_ref` into actual raw-state access

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- reopen sidecar/manifest realization unless a separate defect-driven decision proves one is
  required
- materialize tensors or controls
