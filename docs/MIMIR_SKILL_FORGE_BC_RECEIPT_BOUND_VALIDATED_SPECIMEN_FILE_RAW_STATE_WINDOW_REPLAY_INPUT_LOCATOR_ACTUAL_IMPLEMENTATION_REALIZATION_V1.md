# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Input Locator Actual-Implementation Realization v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual replay-input locator implementation realization boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationContractV1`

It defines:

- the first truthful realized result surface above the replay-input locator actual-implementation
  contract
- the narrowest honest per-specimen actual-implementation result the current repo can emit
- the exact admission and failure rules for realizing that result

### Why it exists

The boundary below this pass already fixed:

- one admitted specimen yields one exact replay-input locator actual-implementation boundary input
  tuple
- one admitted specimen yields one exact replay-input locator actual-implementation output
  boundary
- preserved receipt-bound identity and deferred observation lineage remain explicit
- `FutureParserConsumableReplayHandleOnly` remains contract-only and not actual implementation or
  locator success

What was still missing was the first truthful realized result above that contract:

- can the repo currently realize any honest `mimir_replay::ReplayInput`, or
- can it only emit a bounded blocked / unavailable actual-implementation result?

### How it differs from the actual-implementation contract-definition boundary below it

- The lower boundary defines the contract shape only.
- This pass realizes the first truthful result above that contract.
- The lower boundary still leaves actual implementation result semantics unchosen.
- This pass chooses the result semantics and makes them explicit.
- Neither boundary implements replay parsing, raw-state payload materialization, tensor
  materialization, or control extraction.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this realization version.

This realization boundary remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationContractV1`
- the preserved lineage tuple and deferred observation lineage are only the low-boost-recovery BC
  specimen fields already carried by that contract
- no second family exists that would justify a generic replay-input locator actual-implementation
  realization framework

No generic multi-family replay/raw-state/index/export/materialization framework is introduced
here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationContractV1`
- the audited family root directory reference already preserved by that contract

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationContractV1`,
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
- `audited_family_root_directory`
- `source_realization_disposition`
- `source_realization_notes`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `admitted_replay_input_locator_implementation_boundary_input`
- each `admitted_replay_input_locator_implementation_output_boundary`
- each `admitted_replay_input_locator_implementation_disposition`
- each `replay_input_locator_actual_implementation_boundary_input`
- each `replay_input_locator_actual_implementation_output_boundary`
- `contract_disposition`
- `contract_notes`
- `chosen_replay_input_locator_actual_implementation_contract_shape`

The following are no longer direct input at this boundary:

- lower replay-input locator implementation contracts and reopen decisions
- lower replay-input locator realization results
- replay-input-access/source-binding realizations
- blocked replay-side parse-attempt results
- parse-attempt contracts
- materialization-attempt realizations
- replay-parsing reopen decisions
- replay-parsing-success reopen decisions
- materialization-contract results
- validation results
- lower locator-contract results
- lower planning boundaries
- emitted-output audit/readback results
- actual emission receipts
- persisted artifacts
- `mimir_export`

Those lower layers remain frozen. This pass starts strictly from the actual-implementation
contract and the already-preserved audited family root reference.

## D. IMPLEMENTATION ROLE

This realization owns exactly one thing:

- realizing the first honest replay-input locator actual-implementation result for one admitted
  contract specimen

This pass is allowed to realize only:

- preserved receipt-bound specimen identity and lineage
- the admitted replay-input locator actual-implementation boundary input tuple
- the admitted replay-input locator actual-implementation output boundary
- one truthful bounded blocked / unavailable actual-implementation disposition above that contract

This pass is not allowed to realize:

- replay file discovery
- replay file paths
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

## E. ACTUAL IMPLEMENTATION SHAPE V1

### Exact realization types

This pass defines exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationRealizationError`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_input_locator_actual_implementation_v1(...)`

### Exact per-specimen contract input consumed

For one admitted specimen, this realization consumes exactly:

- `replay_input_locator_actual_implementation_boundary_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationBoundaryInputV1`
- `replay_input_locator_actual_implementation_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationOutputBoundaryV1`

Those fields are consumed from the admitted contract result. They are not recomputed from lower
layers.

### Exact truthful realization decision

The current implementation can only emit:

- one truthful blocked / unavailable replay-input locator actual-implementation result

The exact disposition is:

- `RealizedForTruthfulBlockedReplayInputLocatorActualImplementationOnly`

The current repo cannot honestly emit `mimir_replay::ReplayInput` in this pass because:

- the admitted contract does not carry a replay file path
- the admitted contract does not carry replay bytes
- the admitted contract does not carry replay frames
- the admitted contract does not carry an already-admitted `mimir_replay::ReplayInput`
- `source_replay` remains opaque lineage only
- `source_replay.provenance_label` remains opaque lineage only and is not a replay path contract
- the audited family root may not be reinterpreted as replay storage

This pass therefore makes the negative fact explicit instead of faking progress:

- `mimir_replay::ReplayInput` materialization is unavailable from the current admitted contract
  without violating the opacity/root rules

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

The realization must hard-fail on any drift across:

- `admitted_replay_input_locator_implementation_boundary_input`
- `admitted_replay_input_locator_implementation_output_boundary`
- `replay_input_locator_actual_implementation_boundary_input`
- `replay_input_locator_actual_implementation_output_boundary`
- the preserved receipt-bound root/path binding

### What it explicitly refuses to promise

This realization explicitly refuses to promise:

- replay file location
- replay path derivation from `source_replay`
- replay path derivation from `source_replay.provenance_label`
- replay storage derivation from `audited_family_root_directory`
- actual `mimir_replay::ReplayInput`
- replay parsing
- raw-state payload availability
- tensor availability
- control/action availability
- `mimir_export` widening
- sidecar/manifest realization

## F. REALIZATION OUTPUT V1

The minimum family-specific replay-input locator actual-implementation realization result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationRealizationResultV1`

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
- preserved `audited_family_root_directory`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- preserved per-specimen actual-implementation results
- bounded `realization_disposition`
- bounded `realization_notes`
- preserved `chosen_replay_input_locator_actual_implementation_contract_shape`

Each per-specimen result contains exactly:

- `specimen_ordinal`
- `consumed_replay_input_locator_actual_implementation_boundary_input`
- `preserved_replay_input_locator_actual_implementation_output_boundary`
- `replay_input_locator_actual_implementation_disposition`

The exact top-level disposition is:

- `RealizedForTruthfulBlockedReplayInputLocatorActualImplementationOnly`

The exact note set is:

- `ReplayInputLocatorActualImplementationContractBoundaryPreserved`
- `ContractInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForBlockedReplayInputLocatorActualImplementationOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `AuditedFamilyRootReferenceRemainsBcSpecimenTreeAnchorOnly`
- `FutureParserConsumableReplayHandleKindPreservedWithoutReplayInputMaterialization`
- `MimirReplayReplayInputMaterializationUnavailableWithoutAdmittedReplayPathOrBytes`
- `SourceReplayProvenanceLabelAndAuditedFamilyRootNotReinterpretedAsReplayLocator`
- `ReplayInputLocatorActualImplementationStillUnavailableForTruthfulResultOnly`
- `TruthfulBlockedReplayInputLocatorActualImplementationResultOnly`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The actual-implementation contract may enter this realization boundary only when all of the
following hold:

1. the input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationContractV1`
2. `source_contract_disposition ==
   ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationOnly`
3. `source_realization_disposition ==
   RealizedForTruthfulBlockedReplayInputLocatorImplementationOnly`
4. `contract_disposition ==
   ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorActualImplementationOnly`
5. all three exact note sets remain frozen:
   - the replay-input locator implementation contract note set
   - the replay-input locator implementation realization note set
   - the replay-input locator actual-implementation contract note set
6. the chosen contract shapes remain frozen:
   - `ReceiptBoundSpecimenFileAnchored`
   - `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
   - `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
   - `ReceiptBoundReplayInputAccessSourceBindingOnly`
   - `ReceiptBoundReplayInputLocatorOnly`
   - `ReceiptBoundReplayInputLocatorImplementationOnly`
   - `ReceiptBoundReplayInputLocatorActualImplementationOnly`
7. the audited family root still exists, is a directory, and still ends in `low_boost_recovery_bc_v1`
8. every preserved specimen still stays receipt-bound below that audited family root
9. every preserved specimen still keeps the exact identity tuple and deferred observation lineage
10. every preserved handle kind still remains
    `FutureParserConsumableReplayHandleOnly`

## H. FAILURE RULES

This boundary must hard-fail on any of the following:

- degraded contract input
- degraded upstream contract-note, realization-note, or actual-contract-note sets
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
- any attempt to reinterpret `source_replay` as an implicit replay locator
- any attempt to reinterpret `source_replay.provenance_label` as an implicit replay locator
- any attempt to reinterpret `audited_family_root_directory` as replay storage
- any attempt to widen this pass into replay parsing
- any attempt to widen this pass into actual raw-state payload materialization
- any attempt to widen this pass into tensor/control materialization

## I. NON-GOALS

This pass does not do any of the following:

- replay parsing
- actual raw-state payload materialization
- tensor materialization
- control/action extraction
- `mimir_export` integration
- sidecar/manifest realization
- generic manifest/index framework work
- generic all-family replay/raw-state/index/export/materialization work
- usefulness proof
- policy-improvement proof

## J. RELATION TO NEXT STAGES

This pass guarantees exactly this to the next step:

- the repo now has one machine-verifiable actual-implementation realization boundary above the
  actual-implementation contract
- the preserved receipt-bound tuple and deferred observation lineage remain intact
- the current truthful limit is explicit:
  - no honest `mimir_replay::ReplayInput` can be materialized from the admitted contract
  - only a truthful blocked / unavailable result is admissible

What remains deferred:

- any boundary that would admit explicit replay storage semantics
- any honest replay path or replay bytes boundary
- replay parsing
- raw-state payload materialization
- tensor/control materialization

The next pass is therefore not another parser-adjacent pass. The next pass must decide whether to
broaden the reopen surface enough to admit one explicit replay-source materialization boundary
without violating the current opacity/root rules. `mimir_export` remains closed unless a later
explicit reopen says otherwise.
