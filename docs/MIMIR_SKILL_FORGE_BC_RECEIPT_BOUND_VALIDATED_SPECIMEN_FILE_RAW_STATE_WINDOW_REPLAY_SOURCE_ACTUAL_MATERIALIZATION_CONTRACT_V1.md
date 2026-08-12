# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Source Actual-Materialization Contract v1

## A. PURPOSE

### What this pass owns

This pass owns exactly one first narrow contract-definition boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`

It defines:

- the first contract-only replay-source-actual-materialization boundary for one admitted truthful
  blocked replay-source-materialization specimen
- the exact per-specimen admitted input that may enter that boundary
- the exact replay-source-actual-materialization-facing boundary input and output shapes
- the minimum family-specific contract-definition result surface needed now

### Why it exists

The reopen-decision boundary below this pass already fixed all of the following:

- reopen is justified
- the next shape must be
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`
- the next pass must stay low-boost-recovery-specific
- the next pass must stay receipt-bound
- the next pass must stay contract-only
- the next pass must stay below replay-source actual-materialization implementation
- the next pass must stay below replay parsing
- the next pass must stay below raw-state payload, tensor, and control materialization
- `source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` must not
  be reinterpreted into replay-source semantics

What was still missing was the actual contract surface above the truthful blocked
replay-source-materialization realization result.

### How it differs from the replay-source actual-materialization reopen-decision boundary below it

- The lower boundary decides that reopening is justified.
- This pass does not decide reopening again.
- This pass freezes the contract surface that the justified reopen pointed to.
- The lower boundary is audit guidance only for this pass.
- This pass is still not replay-source actual-materialization implementation.
- This pass is still not replay parsing.
- This pass is still not raw-state payload materialization.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This replay-source actual-materialization contract remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`
- the preserved lineage tuple is only the low-boost-recovery BC specimen tuple already carried by
  that realization result
- the preserved deferred observation lineage is only the low-boost-recovery BC observation-binding
  pair already carried by that realization result
- no second family exists that would justify a shared replay/raw-state/index/export/materialization
  framework

No generic all-family replay/raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`
- the audited family root directory reference already preserved by that realization result
- the replay-source-actual-materialization reopen-decision docs/artifacts as audit guidance only

From
`LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `source_chosen_replay_parsing_contract_shape`
- `source_chosen_replay_input_access_contract_shape`
- `source_chosen_replay_input_locator_contract_shape`
- `source_chosen_replay_input_locator_implementation_contract_shape`
- `source_chosen_replay_input_locator_actual_implementation_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `consumed_replay_source_materialization_boundary_input`
- each `preserved_replay_source_materialization_output_boundary`
- each `replay_source_materialization_disposition`
- `realization_disposition`
- `realization_notes`
- `chosen_replay_source_materialization_contract_shape`

The following are no longer direct input at this boundary:

- replay-source-materialization contracts below this layer
- replay-input locator actual-implementation contracts and realizations below this layer
- replay-input locator implementation contracts and realizations below this layer
- replay-input locator contracts and realizations below this layer
- replay-input-access/source-binding contracts and realizations below this layer
- raw-state materialization reopen, contract, and realization layers below this layer
- replay parsing reopen, contract, and realization layers below this layer
- sidecars, manifests, generic indexes, persisted artifacts, and `mimir_export`

Those lower layers remain frozen. This pass starts strictly from the truthful blocked
replay-source-materialization realization result plus the already-preserved audited family root
reference. The reopen-decision docs/artifacts remain audit guidance only and are not part of the
runtime contract input surface.

## D. CONTRACT ROLE

This contract owns exactly one thing:

- defining the first honest replay-source-actual-materialization-facing contract surface above the
  truthful blocked replay-source-materialization realization result

This pass is allowed to bind only:

- preserved receipt-bound specimen identity and lineage
- preserved deferred observation lineage
- preserved replay-input-locator handle-kind lineage
- preserved replay-source-materialization requirement-kind lineage
- one new replay-source-actual-materialization-facing contract-only handle that says this exact
  preserved tuple may later bind to one explicit replay-source carrier admitted by a later actual
  materialization boundary

This pass is not allowed to implement, discover, parse, or materialize:

- replay files
- replay file paths
- replay bytes
- replay frames
- actual `mimir_replay::ReplayInput`
- replay-source actual-materialization implementation
- replay-input locator logic
- replay parsing
- actual raw-state payload materialization
- tensor payloads
- control/action payloads
- sidecars
- manifests
- generic indexes
- `mimir_export`

## E. CONTRACT SHAPE V1

### Contract name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`

### Exact per-specimen admitted inputs

For one admitted specimen, this contract consumes exactly:

- `admitted_replay_source_materialization_boundary_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationBoundaryInputV1`
- `admitted_replay_source_materialization_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationOutputBoundaryV1`
- `admitted_replay_source_materialization_disposition:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationDispositionV1`

Those values are consumed only from the truthful blocked replay-source-materialization realization
result. They are not recomputed from lower layers.

### Exact replay-source-actual-materialization-facing boundary input tuple

For one admitted specimen, the contract defines exactly:

- `replay_source_actual_materialization_boundary_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationBoundaryInputV1`

Its fields are exactly:

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
- `preserved_replay_input_locator_handle_kind`
- `preserved_replay_source_materialization_requirement_kind`

### Exact replay-source-actual-materialization-facing output-boundary shape

For one admitted specimen, the contract defines exactly:

- `replay_source_actual_materialization_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOutputBoundaryV1`

Its fields are exactly:

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
- `preserved_replay_input_locator_handle_kind`
- `preserved_replay_source_materialization_requirement_kind`
- `bound_replay_source_actual_materialization_handle_kind`

The exact new handle kind introduced here is:

- `LowBoostRecoveryBcReceiptBoundReplaySourceActualMaterializationHandleKindV1::FutureExplicitReplaySourceCarrierOnly`

Its admitted meaning is only:

- this exact preserved tuple may later bind to one explicit replay-source carrier admitted by a
  later replay-source actual-materialization realization or implementation pass
- lineage and audited-root presence are not that carrier

### Exact invariant

The exact invariant is:

- for one admitted truthful blocked replay-source-materialization specimen, the tuple
  (`lane_ordinal`, `specimen_ordinal`, `artifact_id`, `anchored_bc_specimen_file_path`,
  `source_raw_state_window_ref`, `source_slice_id`, `source_replay`, `source_subject`,
  `source_phase_id`, `preserved_observation_binding_kind`,
  `preserved_accepted_reference_window`, `preserved_replay_input_locator_handle_kind`,
  `preserved_replay_source_materialization_requirement_kind`) binds to exactly one honest
  replay-source-actual-materialization-facing contract
- that contract is authoritative only for that exact preserved tuple
- that contract must not silently rewrite, drop, pad, reorder, or widen preserved lineage
- that contract must not reinterpret `source_replay` as replay source
- that contract must not reinterpret `source_replay.provenance_label` as a replay path contract
- that contract must not reinterpret `audited_family_root_directory` as replay storage

### Exact relationship to `preserved_observation_binding_kind`

`preserved_observation_binding_kind` remains:

- preserved deferred observation lineage only
- not replay source
- not replay path
- not parser success
- not raw-state payload materialization

### Exact relationship to `preserved_accepted_reference_window`

`preserved_accepted_reference_window` remains:

- preserved deferred observation lineage only
- not replay source
- not replay bytes
- not replay frames
- not raw-state payload materialization

### Exact `FutureParserConsumableReplayHandleOnly` rule

`preserved_replay_input_locator_handle_kind` must remain:

- `LowBoostRecoveryBcReceiptBoundReplayInputLocatorHandleKindV1::FutureParserConsumableReplayHandleOnly`

Its meaning here is still limited to:

- a preserved contract-only replay-handle fact from lower layers
- not replay source
- not replay-source actual-materialization success
- not replay-input materialization
- not replay parsing

### Exact `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing` rule

`preserved_replay_source_materialization_requirement_kind` must remain:

- `LowBoostRecoveryBcReceiptBoundReplaySourceMaterializationRequirementKindV1::ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`

Its meaning here is still limited to:

- replay-source actual-materialization remains required before replay-input or replay-parsing claims
- not replay-source actual-materialization success
- not replay parsing
- not raw-state payload materialization

### Exact opacity and root-anchor rules

The exact rules are:

- `source_replay` remains opaque lineage unless and until a later explicit boundary says otherwise
- `source_replay.provenance_label` remains opaque lineage and is not a replay path contract
- `audited_family_root_directory` remains only a BC specimen-tree anchor

### Exact future-target acknowledgment rule

This contract may acknowledge that later work could target:

- file-backed replay-source carriers
- byte-backed replay-source carriers
- `mimir_replay::ReplayInput`-backed carriers

But this contract must not:

- materialize any of them
- promise any of them
- imply that any one of them already exists

In v1, that acknowledgment exists only through the contract note set and the new
`FutureExplicitReplaySourceCarrierOnly` handle kind.

## F. CONTRACT OUTPUT V1

The minimum family-specific contract-definition result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_contract_disposition`
- preserved `source_contract_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `source_chosen_materialization_contract_shape`
- preserved `source_chosen_replay_parsing_contract_shape`
- preserved `source_chosen_replay_input_access_contract_shape`
- preserved `source_chosen_replay_input_locator_contract_shape`
- preserved `source_chosen_replay_input_locator_implementation_contract_shape`
- preserved `source_chosen_replay_input_locator_actual_implementation_contract_shape`
- preserved `source_chosen_replay_source_materialization_contract_shape`
- preserved `audited_family_root_directory`
- preserved `source_realization_disposition`
- preserved `source_realization_notes`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- bounded `contract_disposition`
- bounded `contract_notes`
- chosen replay-source actual-materialization contract shape

Each per-specimen result contains exactly:

- `specimen_ordinal`
- `admitted_replay_source_materialization_boundary_input`
- `admitted_replay_source_materialization_output_boundary`
- `admitted_replay_source_materialization_disposition`
- `replay_source_actual_materialization_boundary_input`
- `replay_source_actual_materialization_output_boundary`

The exact top-level disposition is:

- `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOnly`

The exact chosen shape is:

- `LowBoostRecoveryBcReplaySourceActualMaterializationContractShapeV1::ReceiptBoundReplaySourceActualMaterializationOnly`

The exact note set is:

- `ReplaySourceMaterializationRealizationBoundaryPreserved`
- `ReplaySourceMaterializationRealizationInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `TruthfulBlockedReplaySourceMaterializationBoundaryPreserved`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForReplaySourceActualMaterializationContractOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `SourceReplayProvenanceLabelRemainsOpaqueLineageOnlyWithoutReplayPathContract`
- `AuditedFamilyRootReferenceRemainsBcSpecimenTreeAnchorOnly`
- `FutureParserConsumableReplayHandleRemainsContractOnlyAndIsStillNotReplaySource`
- `ExplicitReplaySourceMaterializationRequirementKindPreservedWithoutReplaySourceActualMaterialization`
- `ReplaySourceActualMaterializationContractOnlyBoundaryDefined`
- `FutureExplicitReplaySourceCarrierRemainsContractOnlyPendingActualMaterializationRealization`
- `FutureFileBackedByteBackedOrMimirReplayReplayInputTargetsMayBeAcknowledgedWithoutMaterializationOrPromise`
- `ReplaySourceActualMaterializationStillDeferred`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The truthful blocked replay-source-materialization realization result may enter this
contract-definition boundary only when all of the following hold:

1. the input is exactly
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`
2. `source_contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationOnly`
3. `source_contract_notes` remain the exact replay-source-materialization contract note set
4. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
5. `source_chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
6. `source_chosen_replay_parsing_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
7. `source_chosen_replay_input_access_contract_shape ==`
   `ReceiptBoundReplayInputAccessSourceBindingOnly`
8. `source_chosen_replay_input_locator_contract_shape == ReceiptBoundReplayInputLocatorOnly`
9. `source_chosen_replay_input_locator_implementation_contract_shape ==`
   `ReceiptBoundReplayInputLocatorImplementationOnly`
10. `source_chosen_replay_input_locator_actual_implementation_contract_shape ==`
    `ReceiptBoundReplayInputLocatorActualImplementationOnly`
11. `chosen_replay_source_materialization_contract_shape ==`
    `ReceiptBoundReplaySourceMaterializationOnly`
12. `realization_disposition ==`
    `RealizedForTruthfulBlockedReplaySourceMaterializationOnly`
13. `realization_notes` remain the exact truthful blocked replay-source-materialization
    realization note set
14. `specimen_count > 0`
15. `group_count > 0`
16. `group_count` equals the number of preserved ordered lane results
17. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
18. `audited_family_root_directory` still exists as a directory at contract-definition time
19. lane order and specimen order still match concrete lane/specimen position
20. each `consumed_replay_source_materialization_boundary_input.anchored_bc_specimen_file_path`
    still remains receipt-bound below `audited_family_root_directory`
21. each `preserved_replay_source_materialization_output_boundary` still matches the
    corresponding consumed replay-source-materialization boundary input on:
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
    - `preserved_replay_input_locator_handle_kind`
22. each preserved output boundary still preserves
    `bound_replay_source_materialization_requirement_kind ==`
    `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`
23. each specimen still preserves
    `replay_source_materialization_disposition ==`
    `RealizedForTruthfulBlockedReplaySourceMaterializationOnly`
24. no lower boundary is silently reopened to repair or reinterpret the admitted realization input

Admission here means only:

- this contract-definition boundary may rely on the truthful blocked replay-source-materialization
  realization result as the last trusted pre-actual-materialization layer

Admission here does not mean:

- replay source is materialized
- replay-source actual-materialization succeeds
- replay-input access succeeds
- replay parsing succeeds
- replay files, replay bytes, or replay frames are available
- raw-state payload exists
- tensors or controls are available

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded realization input
- mismatched counts
- mismatched lane order
- mismatched specimen order
- mismatched artifact ids
- duplicate artifact ids
- audited family root drift
- audited family root missing or not a directory
- anchored specimen-file path drift outside the audited family root
- any drift in:
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
  - `preserved_replay_input_locator_handle_kind`
  - `preserved_replay_source_materialization_requirement_kind`
- any attempt to reinterpret `source_replay` as an implicit replay source
- any attempt to reinterpret `source_replay.provenance_label` as an implicit replay path
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen this pass into replay-source actual-materialization implementation
- any attempt to widen this pass into replay parsing
- any attempt to widen this pass into actual raw-state payload materialization
- any attempt to widen this pass into tensor/control materialization

This v1 boundary is intentionally strict:

- no repair
- no specimen skipping
- no resorting
- no replay-path guessing
- no replay-byte guessing
- no replay-carrier synthesis
- no sidecar/manifest/index fallback

## I. NON-GOALS

This pass does not do any of the following:

- no replay-source actual-materialization implementation
- no replay parsing
- no actual raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no sidecar/manifest realization unless separately justified
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- one explicit replay-source-actual-materialization contract exists above the truthful blocked
  replay-source-materialization realization result
- that contract is machine-checkable and auditable
- preserved receipt-bound identity and deferred observation lineage remain visible
- preserved `FutureParserConsumableReplayHandleOnly` and preserved
  `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing` remain visible without
  being overstated as replay source or actual materialization success
- one new contract-only handle,
  `FutureExplicitReplaySourceCarrierOnly`, now fixes the exact meaning of the next boundary
- `source_replay` remains opaque lineage only
- `source_replay.provenance_label` remains opaque lineage only
- `audited_family_root_directory` remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- replay-source actual-materialization succeeds
- replay file paths, replay bytes, or replay frames exist
- actual `mimir_replay::ReplayInput` exists
- replay parsing
- raw-state payload materialization
- tensor/control materialization
- sidecar/manifest necessity

The immediate next pass should be:

- a first replay-source actual-materialization realization pass above
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`
- still without replay-source actual-materialization implementation
- still without replay parsing
- still without raw-state payload materialization
- still without `mimir_export` widening unless that separate boundary is explicitly reopened
