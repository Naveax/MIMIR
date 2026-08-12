# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Materialization Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the first contract-definition boundary above:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
- `LowBoostRecoveryBcRawStateMaterializationReopenDecisionResultV1`

It defines exactly one narrow contract-only surface:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`

with the minimum supporting family-specific surface needed to make that contract machine-checkable:

- one contract disposition
- one contract note set
- one per-specimen admitted validated-specimen view
- one explicit materialization-attempt input boundary shape
- one explicit materialization-attempt output-boundary shape
- one contract-definition error surface
- one contract-definition entry function

### Why it exists

The boundary below this pass already proved:

- the anchored BC specimen file exists
- the anchored BC specimen file is readable
- the read-back specimen still matches the realized locator on:
  - `lane_ordinal`
  - `specimen_ordinal`
  - `artifact_id`
  - `source_raw_state_window_ref`

The reopen-decision boundary above that already proved:

- reopening is justified
- the next shape must remain
  `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`

What was still missing was the exact contract surface that turns one admitted validated specimen
into one honest raw-state materialization-attempt boundary without yet performing materialization.

### How it differs from the raw-state materialization reopen-decision boundary below it

- The reopen-decision boundary answers whether reopening is justified.
- This pass defines the exact contract shape after that answer.
- The reopen-decision boundary does not define the per-specimen attempt input/output surfaces.
- This pass does define those surfaces.
- This pass is still contract-only and still does not materialize raw state.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This contract remains family-specific because:

- the admitted validation input is only
  `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
- the admitted reopen input is only
  `LowBoostRecoveryBcRawStateMaterializationReopenDecisionResultV1`
- the specimen-file contract being preserved is only
  `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
- the unresolved opaque reference remains the family-specific BC field
  `source_raw_state_window_ref`
- the deferred observation lineage remains the family-specific pair:
  - `observation_binding_kind`
  - `accepted_reference_window`

No generic all-family raw-state, index, manifest, or export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
- `LowBoostRecoveryBcRawStateMaterializationReopenDecisionResultV1`
- the audited family root directory reference already preserved by those results

From `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`, this pass
consumes exactly:

- `specimen_count`
- `group_count`
- `source_chosen_locator_contract_shape`
- `audited_family_root_directory`
- `validation_disposition`
- `validation_notes`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `preserved_realized_locator.lane_ordinal`
- each `preserved_realized_locator.specimen_ordinal`
- each `preserved_realized_locator.artifact_id`
- each `preserved_realized_locator.source_raw_state_window_ref`
- each `preserved_realized_locator.deterministic_bc_specimen_file_relative_path`
- each `preserved_realized_locator.anchored_bc_specimen_file_path`
- each `specimen_file_exists`
- each `readback_matches_realized_locator_identity`
- each `readback_specimen.source_slice_id`
- each `readback_specimen.source_replay`
- each `readback_specimen.source_subject`
- each `readback_specimen.source_phase_id`
- each `readback_specimen.accepted_reference_variant_id`
- each `readback_specimen.observation_binding_kind`
- each `readback_specimen.accepted_reference_window`

From `LowBoostRecoveryBcRawStateMaterializationReopenDecisionResultV1`, this pass consumes
exactly:

- `specimen_count`
- `group_count`
- `source_validation_disposition`
- `source_validation_notes`
- `source_chosen_locator_contract_shape`
- `audited_family_root_directory`
- `decision_disposition`
- `decision_notes`
- `chosen_materialization_contract_shape`

Direct input is no longer:

- locator-contract results
- locator-realization results
- planning results
- proof results
- reopen decisions below this layer
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

Those layers remain frozen. This pass starts strictly from the validated specimen-file boundary
plus the reopen decision above it.

## D. CONTRACT ROLE

This contract owns exactly one thing:

- defining the admitted per-specimen identity, lineage, and deferred observation-access fields that
  one honest raw-state materialization-attempt boundary would consume and expose

This contract is allowed to bind:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- preserved receipt-bound lineage:
  - `source_slice_id`
  - `source_replay`
  - `source_subject`
  - `source_phase_id`
- preserved deferred observation lineage:
  - `accepted_reference_variant_id`
  - `observation_binding_kind`
  - `accepted_reference_window`

This contract is not allowed to materialize yet:

- raw-state payloads
- replay-frame data
- raw-state-window frames
- observation tensors
- control/action payloads
- sidecars or manifests
- generic indexes
- `mimir_export` outputs

## E. CONTRACT SHAPE V1

### Contract name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`

### Exact per-specimen admitted inputs

For one admitted validated specimen, the contract preserves exactly:

- enclosing `lane_ordinal`
- enclosing `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`
- `accepted_reference_variant_id`
- `observation_binding_kind`
- `accepted_reference_window`

The admitted-specimen view is intentionally family-specific and still receipt-bound.

### Exact materialization-attempt boundary input tuple

The honest attempt input tuple is:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`

This is the minimum input needed to attempt raw-state access without inventing new storage,
manifest, or export semantics.

### Exact materialization-attempt output boundary shape

The honest attempt output-boundary shape is:

- the full materialization-attempt input tuple above, preserved unchanged
- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`

This output boundary shape still does not expose:

- materialized raw-state payload
- replay frames
- tensor payload
- control payload
- success proof

It is a boundary shape, not an executed materialization result.

### Exact invariant

For one admitted specimen, this contract binds exactly one tuple:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`

to exactly one honest raw-state materialization-attempt boundary.

That invariant is strict:

- no remapping between lane/specimen position and artifact identity
- no path rewriting
- no root reinterpretation
- no alternate raw-state lookup root
- no speculative lineage repair

### Exact relationship to `observation_binding_kind`

`observation_binding_kind` is preserved only as deferred observation-access lineage.

It may:

- remain visible on the admitted validated specimen
- remain visible on the attempt output-boundary shape

It may not:

- trigger tensor materialization
- reinterpret the attempt as observation materialization
- widen the boundary into control extraction

### Exact relationship to `accepted_reference_window`

`accepted_reference_window` is preserved only as deferred observation-access lineage tied to the
same admitted specimen.

It may:

- remain visible on the admitted validated specimen
- remain visible on the attempt output-boundary shape

It may not:

- be treated as already materialized raw-state payload
- be turned into tensors
- be turned into controls

`accepted_reference_variant_id` is also preserved on the admitted validated specimen, but in this
v1 contract it is not promoted into the attempt input tuple because raw-state materialization is
still below variant/tensor/control realization.

## F. CONTRACT OUTPUT V1

The minimum family-specific contract-definition result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`

It contains:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_validation_disposition`
- preserved `source_validation_notes`
- preserved `source_reopen_decision_disposition`
- preserved `source_reopen_decision_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane/specimen results
- chosen `contract_disposition`
- bounded `contract_notes`
- chosen `chosen_materialization_contract_shape`

The exact contract disposition is:

- `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptOnly`

The exact contract notes are:

- `SpecimenFileExistenceReadbackValidationBoundaryPreserved`
- `RawStateMaterializationReopenDecisionBoundaryPreserved`
- `ValidationAndReopenInputsCrossValidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForMaterializationAttemptOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `ActualRawStateMaterializationDeferred`
- `ReplayParsingStillDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

Validation plus reopen inputs may enter this boundary only when all of the following hold:

1. the validation input remains an exact
   `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
2. the reopen input remains an exact
   `LowBoostRecoveryBcRawStateMaterializationReopenDecisionResultV1`
3. `validation_disposition ==`
   `ValidatedForReceiptBoundBcSpecimenFileExistenceAndIdentityPreservingReadbackOnly`
4. `validation_notes` remain the exact frozen validation note set
5. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
6. `decision_disposition ==`
   `ReopenJustifiedForReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationContract`
7. `decision_notes` remain the exact frozen reopen-decision note set
8. `chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
9. `specimen_count > 0`
10. `group_count > 0`
11. `group_count` equals the number of preserved ordered lane results in the validation input
12. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
13. `audited_family_root_directory` still exists and is a directory at contract-definition time
14. lane order and specimen order remain exact in the validation input
15. `specimen_file_exists == true` for every admitted specimen
16. `readback_matches_realized_locator_identity == true` for every admitted specimen
17. reopen `specimen_count`, `group_count`, and `audited_family_root_directory` still match the
    validation input exactly
18. no lower boundary is silently reopened to repair or reinterpret the admitted validation input

Admission here means only:

- this contract-definition boundary may define the per-specimen materialization-attempt shape

Admission here does not mean:

- raw-state materialization is implemented
- replay parsing exists
- tensors or controls are available
- `mimir_export` may be widened

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded validation input
- degraded reopen input
- mismatched counts between validation and reopen inputs
- mismatched audited family root between validation and reopen inputs
- any lane/specimen order drift inside the validation input
- any artifact-id drift inside the validation input
- any attempt to reinterpret the audited family root as raw-state storage
- any attempt to widen this boundary into actual raw-state materialization

This v1 boundary is intentionally strict:

- no repair
- no specimen skipping
- no resorting
- no guessed path repair
- no payload synthesis
- no manifest/sidecar fallback
- no generic index fallback

Cross-input lane/specimen order or artifact-id mismatch is not separately representable in the
reopen result because the reopen-decision boundary does not duplicate per-specimen structure.
Therefore, any such drift must surface as degraded validation input and hard-fail here.

## I. NON-GOALS

This pass does not do any of the following:

- no actual raw-state materialization
- no replay parsing implementation
- no raw-state payload exposure
- no `mimir_export` integration
- no sidecar/manifest realization
- no generic manifest/index framework
- no tensor materialization
- no control/action extraction
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- one explicit contract-definition boundary exists above the validated specimen-file boundary
- one admitted validated specimen now has one explicit attempt input tuple
- one admitted validated specimen now has one explicit attempt output-boundary shape
- preserved receipt-bound identity, lineage, and deferred observation lineage remain visible
  without inventing raw-state payload semantics
- the audited family root still remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual raw-state access
- raw-state-window payload materialization
- replay-frame access
- tensor/control materialization

The immediate next pass should now be:

- a first actual raw-state materialization-attempt realization pass that consumes
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`
  while still avoiding replay parsing, tensor materialization, and control extraction

That next pass should define whether the attempt boundary currently produces only a truthful
non-materialized or failed attempt result, or whether some narrower raw-state access can already be
honestly realized without reopening forbidden layers.
