# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State-Window Replay-Input Locator Implementation Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the first contract-definition boundary for:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`

It defines only:

- the exact admitted boundary above:
  - `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`
  - `LowBoostRecoveryBcReceiptBoundReplayInputLocatorImplementationReopenDecisionResultV1`
- the exact per-specimen admitted truthful non-located replay-input locator evidence
- the exact replay-input locator implementation-facing boundary input tuple
- the exact replay-input locator implementation-facing output-boundary shape
- the exact bounded contract-definition output, disposition, notes, and failure rules

### Why it exists

The replay-input locator implementation reopen-decision boundary already fixed:

- reopen is justified
- the minimum honest next shape is exactly:
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`
- the next pass must stay:
  - low-boost-recovery-specific
  - strictly receipt-bound
  - contract-only
  - below actual replay-input locator implementation
  - below actual replay parsing
  - below actual raw-state payload, tensor, and control materialization

This pass exists because that reopened shape must be made machine-verifiable before any later pass
tries to realize even a first replay-input locator implementation-facing result.

### How it differs from the replay-input locator implementation reopen-decision boundary below it

- The reopen-decision boundary answers whether replay-input locator implementation work must be
  reopened at all.
- This pass defines the reopened implementation-facing contract surface itself.
- This pass still does not implement replay-input locator logic.
- This pass still does not locate replay input.
- This pass still does not parse replay input.
- This pass still does not materialize raw-state payloads, tensors, or controls.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This replay-input locator implementation contract remains family-specific because:

- the admitted realization boundary is low-boost-recovery-specific
- the admitted lineage tuple is only the low-boost-recovery BC specimen tuple already preserved by
  that realization
- the preserved deferred observation lineage is only the low-boost-recovery BC observation-binding
  pair already carried by that realization
- no second family exists yet to justify a shared replay-input locator implementation contract
  framework

No generic all-family replay/raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundReplayInputLocatorImplementationReopenDecisionResultV1`
- the audited family root directory reference already preserved by those results

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `source_chosen_replay_parsing_contract_shape`
- `source_chosen_replay_input_access_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `consumed_replay_input_locator_boundary_input`
- each `preserved_replay_input_locator_output_boundary`
- each `replay_input_locator_disposition`
- `realization_disposition`
- `realization_notes`
- `chosen_replay_input_locator_contract_shape`

From `LowBoostRecoveryBcReceiptBoundReplayInputLocatorImplementationReopenDecisionResultV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_realization_disposition`
- `source_realization_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `source_chosen_replay_parsing_contract_shape`
- `source_chosen_replay_input_access_contract_shape`
- `source_chosen_replay_input_locator_contract_shape`
- `audited_family_root_directory`
- `decision_disposition`
- `decision_notes`
- `chosen_replay_input_locator_implementation_contract_shape`

The following are no longer direct input at this boundary:

- replay-input locator contracts below this layer
- replay-input locator reopen decisions below this layer
- replay-input-access/source-binding realizations
- blocked replay-side parse-attempt results
- parse-attempt contracts
- materialization-attempt realizations
- replay-parsing reopen decisions
- replay-parsing-success reopen decisions
- materialization-contract results
- validation results
- lower locator-contract results
- lower locator-realization results
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

Those lower layers remain frozen. This pass starts strictly from the truthful non-located
replay-input locator realization result, the replay-input locator implementation reopen decision,
and the already-preserved audited family root directory reference.

## D. CONTRACT ROLE

This contract owns exactly one thing:

- defining one honest future replay-input locator implementation-facing handle contract for one
  admitted truthful non-located replay-input locator specimen

This contract is allowed to bind only:

- the exact preserved receipt-bound lineage tuple already carried by the realization result
- the exact preserved deferred observation lineage already carried by the realization result
- one new replay-input locator implementation boundary input tuple
- one new replay-input locator implementation output-boundary shape

This contract is not allowed to implement, locate, parse, or materialize:

- actual replay-input locator logic
- replay-path discovery
- replay byte access
- replay frame access
- actual replay parsing
- actual raw-state payload materialization
- tensor materialization
- control/action extraction
- sidecars
- manifests
- generic indexes
- `mimir_export`

## E. CONTRACT SHAPE V1

The contract name is fixed to exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`

### Exact per-specimen admitted inputs

For one admitted specimen, this contract preserves exactly:

- `admitted_replay_input_locator_boundary_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorBoundaryInputV1`
- `admitted_replay_input_locator_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorOutputBoundaryV1`
- `admitted_replay_input_locator_disposition:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationDispositionV1`

Those preserved admitted inputs remain the only truthful non-located replay-input locator specimen
evidence this pass is allowed to use.

This pass does not recompute those values from lower layers.

### Exact replay-input locator implementation-facing boundary input tuple

For one admitted specimen, the replay-input locator implementation-facing boundary input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationBoundaryInputV1`

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

This input tuple is copied only from the admitted truthful non-located replay-input locator output
boundary after exact realization validation has already frozen the identity and lineage tuple.

### Exact replay-input locator implementation-facing output-boundary shape

For one admitted specimen, the replay-input locator implementation-facing output boundary is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationOutputBoundaryV1`

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
- `bound_replay_input_locator_handle_kind`

`bound_replay_input_locator_handle_kind` is fixed to exactly:

- `LowBoostRecoveryBcReceiptBoundReplayInputLocatorHandleKindV1::FutureParserConsumableReplayHandleOnly`

### Exact invariant

The invariant in v1 is:

- for one admitted truthful non-located replay-input locator specimen, the tuple
  (`lane_ordinal`, `specimen_ordinal`, `artifact_id`, `anchored_bc_specimen_file_path`,
  `source_raw_state_window_ref`, `source_slice_id`, `source_replay`, `source_subject`,
  `source_phase_id`, `preserved_observation_binding_kind`,
  `preserved_accepted_reference_window`)
  plus preserved receipt-bound lineage and the preserved admitted
  `FutureParserConsumableReplayHandleOnly` contract-only handle kind binds to exactly one honest
  replay-input locator implementation-facing handle contract
- that contract is authoritative only for that exact preserved tuple
- that contract must not silently rewrite, drop, pad, reorder, or widen any preserved lineage
- that contract must keep the admitted truthful non-located replay-input locator output boundary
  aligned with the new replay-input locator implementation output boundary on the full tuple above
- that contract must not reinterpret `source_replay.provenance_label` as a path contract
- that contract must not reinterpret `audited_family_root_directory` as replay storage

### Exact relationship to `preserved_observation_binding_kind`

`preserved_observation_binding_kind` remains:

- preserved from the admitted truthful non-located replay-input locator boundary
- fixed to `AcceptedReferenceWindowFromRawStateWindowRef`
- deferred observation lineage only

This contract does not reopen observation materialization.

### Exact relationship to `preserved_accepted_reference_window`

`preserved_accepted_reference_window` remains:

- preserved from the admitted truthful non-located replay-input locator boundary
- attached to the same specimen as deferred observation lineage only
- a carried contract window, not a materialized payload

This contract does not materialize that window from replay or raw state.

### Exact opacity rule for `source_replay`

`source_replay` remains opaque lineage only unless and until a later explicit boundary says
otherwise.

This contract must not:

- derive a replay path from `source_replay`
- derive replay storage from `source_replay`
- treat `source_replay.provenance_label` as an implicit locator

### Exact audited-root rule

`audited_family_root_directory` remains only a BC specimen-tree anchor.

This contract must not:

- reinterpret `audited_family_root_directory` as replay storage
- search below `audited_family_root_directory` for replay input
- claim replay locator success from audited-root presence alone

### Exact `FutureParserConsumableReplayHandleOnly` rule

`FutureParserConsumableReplayHandleOnly` remains contract-only and is still not locator success.

In v1 that means:

- the admitted replay-input locator output boundary still carries only a contract-only future
  parser-consumable replay handle
- the new replay-input locator implementation output boundary also carries only a contract-only
  future parser-consumable replay handle
- neither handle means replay input was located
- neither handle means replay bytes, replay frames, or parser-success output exists

### Exact future `mimir_replay::ReplayInput` acknowledgment rule

This contract may acknowledge future `mimir_replay::ReplayInput` targeting only as deferred
implementation intent.

In v1 that means:

- the contract notes may state that later explicit replay-input locator implementation work could
  target `mimir_replay::ReplayInput`
- the contract does not materialize a `mimir_replay::ReplayInput`
- the contract does not promise a `mimir_replay::ReplayInput`
- the contract does not add a new replay crate dependency to make that acknowledgment

## F. CONTRACT OUTPUT V1

The minimum family-specific contract-definition output is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_realization_disposition`
- preserved `source_realization_notes`
- preserved `source_reopen_decision_disposition`
- preserved `source_reopen_decision_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `source_chosen_materialization_contract_shape`
- preserved `source_chosen_replay_parsing_contract_shape`
- preserved `source_chosen_replay_input_access_contract_shape`
- preserved `source_chosen_replay_input_locator_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- bounded `contract_disposition`
- bounded `contract_notes`
- chosen `chosen_replay_input_locator_implementation_contract_shape`

Each lane result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractLaneResultV1`

It contains exactly:

- `lane_ordinal`
- ordered `ordered_specimen_results`

Each specimen result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractSpecimenResultV1`

It contains exactly:

- `specimen_ordinal`
- `admitted_replay_input_locator_boundary_input`
- `admitted_replay_input_locator_output_boundary`
- `admitted_replay_input_locator_disposition`
- `replay_input_locator_implementation_boundary_input`
- `replay_input_locator_implementation_output_boundary`

### Exact contract disposition

`contract_disposition` is fixed to exactly:

- `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationOnly`

### Exact contract notes

`contract_notes` are fixed to exactly:

- `ReplayInputLocatorRealizationBoundaryPreserved`
- `ReplayInputLocatorImplementationReopenDecisionBoundaryPreserved`
- `RealizationAndReopenInputsCrossValidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForReplayInputLocatorImplementationContractOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `FutureParserConsumableReplayHandleRemainsContractOnlyAndIsNotLocatorSuccess`
- `FutureMimirReplayReplayInputTargetMayBeAcknowledgedWithoutMaterializationOrPromise`
- `ReplayInputLocatorImplementationContractOnlyBoundaryDefined`
- `ReplayInputLocatorImplementationStillDeferred`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The truthful non-located replay-input locator realization result plus replay-input locator
implementation reopen-decision result may enter this contract-definition boundary only when all of
the following hold:

1. the inputs are exactly:
   - `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`
   - `LowBoostRecoveryBcReceiptBoundReplayInputLocatorImplementationReopenDecisionResultV1`
2. the realization result still satisfies the exact replay-input locator implementation reopen-
   decision admission rules
3. `source_realization_disposition ==
   RealizedForTruthfulNonLocatedReplayInputLocatorOnly`
4. `source_realization_notes` still equal the exact truthful non-located replay-input locator
   realization note set
5. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
6. `source_chosen_materialization_contract_shape ==
   ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
7. `source_chosen_replay_parsing_contract_shape ==
   ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
8. `source_chosen_replay_input_access_contract_shape ==
   ReceiptBoundReplayInputAccessSourceBindingOnly`
9. `source_chosen_replay_input_locator_contract_shape == ReceiptBoundReplayInputLocatorOnly`
10. `decision_disposition ==
    ReopenJustifiedForReceiptBoundReplayInputLocatorImplementationContract`
11. `decision_notes` still equal the exact replay-input locator implementation reopen-decision
    note set
12. `chosen_replay_input_locator_implementation_contract_shape ==
    ReceiptBoundReplayInputLocatorImplementationOnly`
13. `specimen_count > 0`
14. `group_count > 0`
15. realization and reopen counts match exactly
16. realization and reopen audited family root directory references match exactly
17. the audited family root directory still ends in `low_boost_recovery_bc_v1`
18. the audited family root directory still exists and is a directory at contract-definition time
19. per-specimen lane/specimen order, artifact ids, anchored specimen-file paths, source lineage,
    deferred observation lineage, admitted handle kind, and truthful non-located disposition still
    satisfy the exact realization validator
20. no lower boundary is silently reopened to repair or reinterpret the admitted realization input

Admission here means only:

- this contract surface may be defined from trusted truthful non-located replay-input locator
  evidence plus the trusted replay-input locator implementation reopen decision

Admission here does not mean:

- replay input was located
- replay files or replay bytes are available
- replay parsing succeeded
- raw-state payload exists
- tensors or controls exist

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded realization input
- degraded replay-input locator implementation reopen-decision input
- mismatched counts, root, order, or artifact ids
- any attempt to reinterpret `source_replay` or `provenance_label` as an implicit replay locator
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen into actual replay-input locator implementation
- any attempt to widen into actual replay parsing
- any attempt to widen into actual raw-state payload materialization
- any attempt to widen into tensor/control materialization
- any attempt to widen into sidecars, manifests, generic indexing, or `mimir_export`

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

- no actual replay-input locator implementation
- no actual replay parsing
- no actual raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no sidecar/manifest realization
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof
- no replay corpus ingestion
- no rollout or physics work
- no async/background system
- no database work

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- one machine-verifiable replay-input locator implementation contract exists above the truthful
  non-located replay-input locator realization result
- one admitted truthful non-located specimen now contributes one exact implementation-facing
  boundary input tuple
- one admitted truthful non-located specimen now contributes one exact implementation-facing
  output-boundary shape
- the binding remains low-boost-recovery-specific
- the binding remains strictly receipt-bound
- `source_replay` remains opaque lineage only
- `audited_family_root_directory` remains only a BC specimen-tree anchor
- `FutureParserConsumableReplayHandleOnly` remains contract-only and not locator success
- `mimir_export` remains untouched and forbidden

### What remains deferred

This pass still does not guarantee:

- actual replay-input locator implementation
- actual replay-input location
- actual `mimir_replay::ReplayInput`
- actual replay parsing
- replay bytes or replay frames
- actual raw-state-window payload materialization
- tensor/control materialization
- sidecar/manifest necessity

### Immediate next-stage implication

The immediate next pass should be:

- a first replay-input locator implementation realization pass above this contract, still without
  actual replay-input locator implementation

That next pass should consume:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`
- the preserved audited family root directory reference already carried by that contract

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- implement actual replay-input locator logic
- implement actual replay parsing
- implement actual raw-state payload materialization
- implement tensor/control materialization
- reopen sidecars/manifests/generic indexing unless a later explicit defect-driven decision proves
  one is required
