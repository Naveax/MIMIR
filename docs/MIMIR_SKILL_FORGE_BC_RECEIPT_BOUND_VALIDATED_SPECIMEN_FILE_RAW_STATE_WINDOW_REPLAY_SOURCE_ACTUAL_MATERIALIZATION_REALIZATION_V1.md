# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Source Actual-Materialization Realization v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual replay-source actual-materialization realization boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`

It defines:

- the first truthful realized result surface above the replay-source actual-materialization contract
- the narrowest honest per-specimen replay-source actual-materialization result the current repo can emit
- the exact admission and failure rules for realizing that result

### Why it exists

The contract boundary below this pass already fixed:

- one admitted specimen yields one exact replay-source-actual-materialization-facing boundary input tuple
- one admitted specimen yields one exact replay-source-actual-materialization-facing output boundary
- the only admitted replay-source actual-materialization handle kind is
  `FutureExplicitReplaySourceCarrierOnly`
- preserved receipt-bound identity and deferred observation lineage remain explicit
- preserved replay-input-locator handle kind and replay-source-materialization requirement kind remain explicit
- `source_replay` remains opaque lineage only
- `source_replay.provenance_label` remains opaque lineage only and is not a replay path contract
- the audited family root remains only a BC specimen-tree anchor

What was still missing was the first truthful realized result above that contract:

- can the repo currently realize any honest explicit replay-source carrier from the admitted contract, or
- can it only emit a bounded blocked / unavailable replay-source actual-materialization result?

### How it differs from the replay-source actual-materialization contract-definition boundary below it

- The lower boundary defines the contract shape only.
- This pass realizes the first truthful result above that contract.
- The lower boundary introduces one contract-only explicit replay-source-carrier handle kind.
- This pass states what the repo can honestly realize from that handle kind today.
- Neither boundary implements replay-source actual-materialization, replay parsing, raw-state payload materialization, tensor materialization, or control extraction.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this realization version.

This realization boundary remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`
- the preserved lineage tuple and deferred observation lineage are only the low-boost-recovery BC specimen fields already carried by that contract
- no second family exists that would justify a generic replay-source actual-materialization realization framework

No generic multi-family replay/raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`
- the audited family root directory reference already preserved by that contract

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`, this pass consumes exactly:

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
- `source_chosen_replay_source_materialization_contract_shape`
- `audited_family_root_directory`
- `source_realization_disposition`
- `source_realization_notes`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `admitted_replay_source_materialization_boundary_input`
- each `admitted_replay_source_materialization_output_boundary`
- each `admitted_replay_source_materialization_disposition`
- each `replay_source_actual_materialization_boundary_input`
- each `replay_source_actual_materialization_output_boundary`
- `contract_disposition`
- `contract_notes`
- `chosen_replay_source_actual_materialization_contract_shape`

Lower contract, reopen, and realization layers are no longer direct input here, including:

- replay-source-materialization contracts and realizations below this layer
- replay-input locator actual-implementation contracts and realizations below this layer
- replay-input locator implementation contracts and realizations below this layer
- replay-input locator contracts and realizations below this layer
- replay-input-access / source-binding contracts and realizations below this layer
- replay-side parse-attempt contracts and realizations below this layer
- raw-state materialization reopen, contract, and realization layers below this layer
- replay parsing reopen and success-reopen layers below this layer
- sidecars, manifests, generic indexes, persisted artifacts, and `mimir_export`

Those lower layers remain frozen. This pass starts strictly from the replay-source actual-materialization contract and the already-preserved audited family root reference.

## D. REALIZATION ROLE

This realization owns exactly one thing:

- realizing the first honest replay-source actual-materialization result for one admitted contract specimen

This pass is allowed to realize only:

- preserved receipt-bound specimen identity and lineage
- the admitted replay-source actual-materialization boundary input tuple
- the admitted replay-source actual-materialization output boundary
- one truthful bounded blocked / unavailable replay-source actual-materialization disposition above that contract

This pass is not allowed to realize:

- explicit replay-source carriers
- replay file discovery
- replay source paths
- replay bytes
- replay frames
- actual `mimir_replay::ReplayInput`
- replay parsing
- raw-state payload materialization
- tensor payloads
- control/action payloads
- sidecars
- manifests
- generic indexes
- `mimir_export`

## E. REPLAY-SOURCE ACTUAL-MATERIALIZATION REALIZATION SHAPE V1

### Exact realization types

This pass defines exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationRealizationError`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_source_actual_materialization_v1(...)`

### Exact per-specimen contract input consumed

For one admitted specimen, this realization consumes exactly:

- `replay_source_actual_materialization_boundary_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationBoundaryInputV1`
- `replay_source_actual_materialization_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOutputBoundaryV1`

Those fields are consumed from the admitted contract result. They are not recomputed from lower layers.

### Exact truthful realization decision

The current implementation can only emit:

- one truthful blocked / unavailable replay-source actual-materialization result

The exact disposition is:

- `RealizedForTruthfulBlockedReplaySourceActualMaterializationOnly`

This is the correct result because the admitted contract still does not carry any admissible explicit replay-source carrier beyond a contract-only handle kind:

- the contract does not carry an actual explicit replay-source carrier
- the contract does not carry a replay path
- the contract does not carry replay bytes
- the contract does not carry replay frames
- the contract does not carry actual `mimir_replay::ReplayInput`
- `source_replay` remains opaque lineage only
- `source_replay.provenance_label` remains opaque lineage only and is not a replay path contract
- the audited family root may not be reinterpreted as replay storage
- `FutureExplicitReplaySourceCarrierOnly` remains a handle kind only and is not a realized carrier
- the preserved requirement kind still says explicit replay-source materialization is required before replay-input or replay-parsing claims can exist

This pass therefore makes the negative fact explicit instead of faking progress:

- replay-source actual-materialization is still unavailable from the current admitted contract without violating the opacity/root rules

### Exact identity checks that must still hold

For one admitted specimen, this realization requires the exact preserved identity tuple:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`

plus the same deferred observation lineage:

- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`

plus the same deferred replay/materialization constraints:

- `preserved_replay_input_locator_handle_kind`
- `preserved_replay_source_materialization_requirement_kind`
- `bound_replay_source_actual_materialization_handle_kind`

The realization must hard-fail on any drift across:

- `admitted_replay_source_materialization_boundary_input`
- `admitted_replay_source_materialization_output_boundary`
- `replay_source_actual_materialization_boundary_input`
- `replay_source_actual_materialization_output_boundary`
- the preserved receipt-bound root/path binding

### What it explicitly refuses to promise

This realization explicitly refuses to promise:

- explicit replay-source carrier discovery
- replay source path derivation from `source_replay`
- replay path derivation from `source_replay.provenance_label`
- replay storage derivation from `audited_family_root_directory`
- replay bytes
- replay frames
- actual `mimir_replay::ReplayInput`
- replay parsing
- raw-state payload availability
- tensor availability
- control/action availability
- `mimir_export` widening
- sidecar/manifest realization

## F. REALIZATION OUTPUT V1

The minimum family-specific replay-source actual-materialization realization result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationRealizationResultV1`

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
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- preserved per-specimen replay-source actual-materialization results
- bounded `realization_disposition`
- bounded `realization_notes`
- preserved `chosen_replay_source_actual_materialization_contract_shape`

Each per-specimen result contains exactly:

- `specimen_ordinal`
- `consumed_replay_source_actual_materialization_boundary_input`
- `preserved_replay_source_actual_materialization_output_boundary`
- `replay_source_actual_materialization_disposition`

The exact top-level disposition is:

- `RealizedForTruthfulBlockedReplaySourceActualMaterializationOnly`

The exact note set is:

- `ReplaySourceActualMaterializationContractBoundaryPreserved`
- `ContractInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForBlockedReplaySourceActualMaterializationOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `SourceReplayProvenanceLabelRemainsOpaqueLineageOnlyWithoutReplayPathContract`
- `AuditedFamilyRootReferenceRemainsBcSpecimenTreeAnchorOnly`
- `FutureParserConsumableReplayHandleKindPreservedWithoutReplaySourceActualMaterialization`
- `ExplicitReplaySourceMaterializationRequirementKindPreservedWithoutReplaySourceActualMaterialization`
- `FutureExplicitReplaySourceCarrierHandleKindPreservedWithoutExplicitCarrierMaterialization`
- `ExplicitReplaySourceCarrierUnavailableWithoutAdmittedCarrierSource`
- `ReplaySourceActualMaterializationStillUnavailableForTruthfulResultOnly`
- `TruthfulBlockedReplaySourceActualMaterializationResultOnly`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The replay-source actual-materialization contract may enter this realization boundary only when all of the following hold:

1. the input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`
2. `source_contract_disposition ==
   ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationOnly`
3. `source_contract_notes` remain the exact frozen replay-source-materialization contract note set
4. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
5. `source_chosen_materialization_contract_shape ==
   ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
6. `source_chosen_replay_parsing_contract_shape ==
   ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
7. `source_chosen_replay_input_access_contract_shape ==
   ReceiptBoundReplayInputAccessSourceBindingOnly`
8. `source_chosen_replay_input_locator_contract_shape == ReceiptBoundReplayInputLocatorOnly`
9. `source_chosen_replay_input_locator_implementation_contract_shape ==
   ReceiptBoundReplayInputLocatorImplementationOnly`
10. `source_chosen_replay_input_locator_actual_implementation_contract_shape ==
    ReceiptBoundReplayInputLocatorActualImplementationOnly`
11. `source_chosen_replay_source_materialization_contract_shape ==
    ReceiptBoundReplaySourceMaterializationOnly`
12. `source_realization_disposition ==
    RealizedForTruthfulBlockedReplaySourceMaterializationOnly`
13. `source_realization_notes` remain the exact frozen replay-source-materialization realization note set
14. `contract_disposition ==
    ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOnly`
15. `contract_notes` remain the exact frozen replay-source actual-materialization contract note set
16. `chosen_replay_source_actual_materialization_contract_shape ==
    ReceiptBoundReplaySourceActualMaterializationOnly`
17. `specimen_count > 0`
18. `group_count > 0`
19. `group_count` equals the number of preserved ordered lane results
20. the audited family root still exists, is a directory, and still ends in `low_boost_recovery_bc_v1`
21. every preserved specimen still stays receipt-bound below that audited family root
22. every admitted replay-source-materialization output boundary still matches the admitted replay-source-materialization input on the preserved identity tuple, deferred observation lineage, preserved replay-input-locator handle kind, and preserved replay-source-materialization requirement kind
23. every replay-source actual-materialization boundary input still matches the admitted replay-source-materialization output tuple, deferred observation lineage, preserved replay-input-locator handle kind, and preserved replay-source-materialization requirement kind
24. every replay-source actual-materialization output boundary still matches the replay-source actual-materialization boundary input on the preserved identity tuple and deferred observation lineage
25. every replay-source actual-materialization output boundary still preserves
    `bound_replay_source_actual_materialization_handle_kind ==
    FutureExplicitReplaySourceCarrierOnly`
26. every admitted replay-source-materialization disposition still remains
    `RealizedForTruthfulBlockedReplaySourceMaterializationOnly`
27. every preserved replay-input-locator handle kind still remains
    `FutureParserConsumableReplayHandleOnly`
28. every preserved replay-source-materialization requirement kind still remains
    `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`

Admission here means only:

- the repo may realize one truthful blocked / unavailable replay-source actual-materialization result above the admitted contract

Admission here does not mean:

- explicit replay source exists
- replay-source actual-materialization succeeds
- replay-input access succeeds
- replay parsing succeeds
- replay files, replay bytes, or replay frames are available
- raw-state payload exists
- tensors or controls exist

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded contract input
- degraded upstream source-contract-note, source-realization-note, or actual-materialization-contract-note sets
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
  - `bound_replay_source_actual_materialization_handle_kind`
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
- no carrier synthesis
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

- one explicit replay-source actual-materialization realization result exists above the contract
- that result is truthful about the current blocked / unavailable state
- preserved receipt-bound identity and deferred observation lineage remain visible without inventing replay storage, replay paths, replay bytes, replay frames, or replay payload semantics
- the preserved future parser-consumable replay handle kind remains visible without being overstated as replay source
- the preserved explicit replay-source-materialization requirement remains visible without being overstated as actual-materialization success
- `FutureExplicitReplaySourceCarrierOnly` remains visible without being overstated as a realized explicit carrier
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual explicit replay-source carrier materialization
- actual replay-input access
- actual replay parsing
- replay bytes or replay frames
- actual raw-state-window payload materialization
- tensor/control materialization

The immediate next pass should be:

- a broader replay-source actual-materialization reopen decision above
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationRealizationResultV1`

That next pass is now obvious because this realization boundary proves the remaining gap is no longer contract shape and no longer realization-result shape. The remaining gap is whether the project must deliberately reopen a broader boundary that can admit explicit replay-source carrier provenance or source binding without cheating through opaque lineage or audited-root presence alone. `mimir_export` remains closed unless a later explicit reopen says otherwise.
