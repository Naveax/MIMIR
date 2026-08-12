# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Side Parse-Attempt Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the first replay-side parse-attempt contract-definition boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
- `LowBoostRecoveryBcReplayParsingReopenDecisionResultV1`

It defines:

- one exact contract-only replay-side parse-attempt boundary for one admitted low-boost-recovery specimen
- one exact rule for what a truthful non-materialized materialization-attempt specimen contributes to that boundary
- one minimal family-specific contract result surface above the replay-parsing reopen decision
- one strict admission rule for realization + reopen-decision inputs
- one strict failure rule for degraded, mismatched, or widened inputs

### Why it exists

The boundary below this pass already proved two things:

- the current repo can only realize `RealizedForTruthfulNonMaterializedAttemptOnly`
- replay parsing must now be deliberately reopened and the next narrow shape is
  `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`

What was still missing was the actual contract surface that binds those truths together without
quietly implementing parsing.

### How it differs from the replay-parsing reopen-decision boundary below it

- The lower boundary decides that replay parsing must be reopened and chooses the next narrow shape.
- This pass defines the contract surface for that chosen shape.
- The lower boundary emits a decision only.
- This pass emits a contract only.
- Neither boundary implements real replay parsing.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This replay-side parse-attempt contract remains family-specific because:

- the admitted source input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
- the admitted reopen input is only `LowBoostRecoveryBcReplayParsingReopenDecisionResultV1`
- the preserved lineage and deferred observation binding are the low-boost-recovery BC specimen
  fields already carried by those boundaries
- no second family exists that would justify a shared replay/raw-state parse-attempt contract

No generic all-family replay/raw-state/index/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
- `LowBoostRecoveryBcReplayParsingReopenDecisionResultV1`
- the audited family root directory reference already preserved by those results

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`,
this pass consumes exactly:

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
- each `consumed_materialization_attempt_input`
- each `preserved_materialization_attempt_output_boundary`
- each `materialization_attempt_disposition`
- `realization_disposition`
- `realization_notes`
- `chosen_materialization_contract_shape`

From `LowBoostRecoveryBcReplayParsingReopenDecisionResultV1`, this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_realization_disposition`
- `source_realization_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `audited_family_root_directory`
- `decision_disposition`
- `decision_notes`
- `chosen_replay_parsing_contract_shape`

Direct input is no longer:

- materialization-contract results
- validation results
- locator-contract results
- locator-realization results
- planning results
- proof results
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

Those lower layers remain frozen. This pass starts strictly from the truthful non-materialized
attempt realization result, the replay-parsing reopen decision, and the already-preserved audited
family root directory reference.

## D. CONTRACT ROLE

This contract owns exactly one thing:

- defining the honest replay-side sourcing / parse-attempt boundary for one admitted specimen
  without claiming parse success, payload success, or downstream materialization

This pass is allowed to bind only:

- preserved receipt-bound specimen identity and lineage
- one replay-side parse-attempt input tuple per admitted specimen
- one replay-side parse-attempt output-boundary shape per admitted specimen
- deferred observation lineage only as deferred lineage

This pass is not allowed to parse or materialize:

- replay files
- replay bytes
- replay frames
- replay-derived raw-state payload
- tensors
- controls/actions
- sidecars
- manifests
- generic indexes
- `mimir_export` outputs

## E. CONTRACT SHAPE V1

### Contract name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`

### Exact per-specimen admitted inputs

For one admitted specimen, this contract consumes exactly:

- `admitted_materialization_attempt_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptInputV1`
- `admitted_materialization_attempt_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptOutputBoundaryV1`

Those admitted inputs are preserved from the truthful non-materialized realization result. They are
not recomputed from lower layers.

### Exact replay-side parse-attempt boundary input tuple

For one admitted specimen, the replay-side parse-attempt input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptInputV1`

It contains exactly:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`

### Exact replay-side parse-attempt output-boundary shape

For one admitted specimen, the replay-side parse-attempt output boundary is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptOutputBoundaryV1`

It contains exactly:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`
- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`

### Exact per-specimen contract result shape

Each preserved specimen result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractSpecimenResultV1`

It contains exactly:

- `specimen_ordinal`
- admitted `materialization_attempt_input`
- admitted `materialization_attempt_output_boundary`
- `replay_side_parse_attempt_input`
- `replay_side_parse_attempt_output_boundary`

### Exact invariant

For one admitted specimen, this contract must bind exactly one tuple:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`

plus the same specimen's deferred observation lineage:

- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`

to exactly one honest replay-side parse-attempt boundary.

That invariant is strict:

- no remapping between receipt-bound specimen identity and replay-side attempt identity
- no lane/specimen reordering
- no artifact-id drift
- no reinterpretation of the audited family root as replay storage
- no replay-path guessing
- no replay-byte guessing
- no raw-state payload guessing

### Exact relationship to deferred observation lineage

Deferred observation lineage remains visible only through:

- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`

Those fields may not be treated as:

- parsed replay frames
- raw-state payload
- tensors
- controls/actions

## F. CONTRACT OUTPUT V1

The minimum family-specific contract-definition result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_realization_disposition`
- preserved `source_realization_notes`
- preserved `source_reopen_decision_disposition`
- preserved `source_reopen_decision_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `source_chosen_materialization_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- chosen `contract_disposition`
- bounded `contract_notes`
- chosen replay-side parse-attempt contract shape

The exact contract disposition is:

- `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptOnly`

The exact contract notes are:

- `MaterializationAttemptRealizationBoundaryPreserved`
- `ReplayParsingReopenDecisionBoundaryPreserved`
- `RealizationAndReopenInputsCrossValidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForReplaySideParseAttemptOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `ReplaySideParseAttemptContractOnlyBoundaryDefined`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

Realization + replay-parsing reopen-decision inputs may enter this contract-definition boundary
only when all of the following hold:

1. the realization input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
2. the reopen input remains an exact `LowBoostRecoveryBcReplayParsingReopenDecisionResultV1`
3. `source_contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptOnly`
4. `source_contract_notes` remain the exact frozen materialization-contract note set
5. `realization_disposition == RealizedForTruthfulNonMaterializedAttemptOnly`
6. `realization_notes` remain the exact frozen truthful non-materialized attempt note set
7. `decision_disposition ==`
   `ReopenJustifiedForReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptContract`
8. `decision_notes` remain the exact frozen replay-parsing reopen note set
9. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
10. `source_chosen_materialization_contract_shape ==`
    `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
11. `chosen_replay_parsing_contract_shape ==`
    `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
12. `specimen_count > 0`
13. `group_count > 0`
14. `group_count` equals the number of preserved ordered lane results in the realization input
15. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
16. `audited_family_root_directory` still exists and is a directory at contract-definition time
17. lane order and specimen order remain exact in the realization input
18. every `anchored_bc_specimen_file_path` remains receipt-bound below
    `audited_family_root_directory`
19. every admitted materialization-attempt output boundary still matches its corresponding admitted
    materialization-attempt input on:
    - `lane_ordinal`
    - `specimen_ordinal`
    - `artifact_id`
    - `anchored_bc_specimen_file_path`
    - `source_raw_state_window_ref`
    - `source_slice_id`
    - `source_replay`
    - `source_subject`
    - `source_phase_id`
20. every admitted specimen still preserves
    `materialization_attempt_disposition == RealizedForTruthfulNonMaterializedAttemptOnly`

Admission here means only:

- the repo may define one explicit replay-side parse-attempt contract boundary

Admission here does not mean:

- replay parsing exists
- replay-side sourcing already succeeds
- replay files/bytes are resolved
- raw-state payload exists
- tensors or controls are available
- `mimir_export` may be widened

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded realization input
- degraded replay-parsing reopen-decision input
- mismatched counts
- mismatched audited family root
- mismatched chosen locator/materialization shapes
- mismatched source realization disposition or note set
- lane/specimen order drift
- artifact-id drift
- anchored path drift outside the audited family root
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen this boundary into actual replay parsing
- any attempt to widen this boundary into actual raw-state payload materialization

This v1 boundary is intentionally strict:

- no repair
- no specimen skipping
- no resorting
- no replay-path guessing
- no replay-byte guessing
- no payload synthesis
- no sidecar/manifest/index fallback

## I. NON-GOALS

This pass does not do any of the following:

- no actual replay parsing
- no actual raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no sidecar/manifest realization
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- one explicit replay-side parse-attempt contract exists above the truthful non-materialized
  materialization-attempt result
- one admitted specimen now yields one exact replay-side parse-attempt input tuple and one exact
  replay-side parse-attempt output boundary
- preserved receipt-bound identity and deferred observation lineage remain visible without
  inventing replay payload semantics
- the audited family root remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual replay-side sourcing success
- actual replay parsing
- replay byte or replay frame access
- actual raw-state-window payload materialization
- tensor/control materialization

The immediate next pass should now be:

- a first replay-side parse-attempt realization pass above
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`
  that still does not promise actual replay parsing success

That next pass is now obvious because the remaining gap is no longer contract shape. The remaining
gap is the first truthful realized result above this contract while replay parsing itself remains
deferred.
