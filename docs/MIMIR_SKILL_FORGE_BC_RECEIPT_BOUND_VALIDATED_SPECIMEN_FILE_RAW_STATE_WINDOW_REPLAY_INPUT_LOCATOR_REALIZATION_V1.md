# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Input Locator Realization v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual replay-input locator realization boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorContractV1`

It defines:

- the first truthful realized result surface above the replay-input locator contract
- the narrowest honest per-specimen replay-input locator result the current repo can emit
- the exact admission and failure rules for realizing that result

### Why it exists

The replay-input locator contract-definition boundary already fixed:

- one admitted specimen yields one exact replay-input locator boundary input tuple
- one admitted specimen yields one exact replay-input locator output boundary
- the only admitted locator handle kind is
  `FutureParserConsumableReplayHandleOnly`

What was still missing was the first truthful result above that contract:

- can the repo currently realize any actual replay-input locator success, or can it only emit a
  truthful non-located locator result?

### How it differs from the replay-input locator contract-definition boundary below it

- The lower boundary defines the contract shape only.
- This pass realizes the first truthful result above that contract.
- The lower boundary introduces one contract-only future parser-consumable locator handle kind.
- This pass states what the repo can honestly realize from that contract today.
- Neither boundary implements actual replay-input locator logic, replay parsing, or raw-state
  materialization.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this realization version.

This realization boundary remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorContractV1`
- the preserved lineage tuple and deferred observation lineage are only the low-boost-recovery BC
  specimen fields already carried by that contract
- no second family exists that would justify a generic replay-input locator realization framework

No generic multi-family replay/raw-state/index/export/materialization framework is introduced
here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorContractV1`
- the audited family root directory reference already preserved by that contract

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorContractV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_realization_disposition`
- `source_realization_notes`
- `source_reopen_decision_disposition`
- `source_reopen_decision_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `source_chosen_replay_parsing_contract_shape`
- `source_chosen_replay_input_access_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `admitted_replay_input_access_source_binding_boundary_input`
- each `admitted_replay_input_access_source_binding_output_boundary`
- each `replay_input_locator_boundary_input`
- each `replay_input_locator_output_boundary`
- `contract_disposition`
- `contract_notes`
- `chosen_replay_input_locator_contract_shape`

The following are no longer direct input at this boundary:

- replay-input-access/source-binding realizations
- replay-input locator reopen decisions
- blocked replay-side parse-attempt results
- parse-attempt contracts
- materialization-attempt realizations
- replay-parsing reopen decisions
- replay-parsing-success reopen decisions
- materialization-contract results
- validation results
- locator-contract results below this layer
- locator-realization results below this layer
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

Those lower layers remain frozen. This pass starts strictly from the replay-input locator contract
and the already-preserved audited family root reference.

## D. REALIZATION ROLE

This realization owns exactly one thing:

- realizing the first honest replay-input locator result for one admitted contract specimen

This pass is allowed to realize only:

- preserved receipt-bound specimen identity and lineage
- the admitted replay-input locator boundary input tuple
- the admitted replay-input locator output boundary
- one truthful bounded non-located replay-input locator disposition above that contract

This pass is not allowed to realize:

- actual replay-input locator implementation
- replay file discovery
- replay file paths
- replay bytes
- replay frames
- actual replay parsing
- raw-state payload materialization
- tensor payloads
- control/action payloads
- sidecars
- manifests
- generic indexes
- `mimir_export` outputs

## E. REPLAY-INPUT LOCATOR REALIZATION SHAPE V1

### Exact realization types

This pass defines exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationError`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_input_locator_v1(...)`

### Exact per-specimen contract input consumed

For one admitted specimen, this realization consumes exactly:

- `replay_input_locator_boundary_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorBoundaryInputV1`
- `replay_input_locator_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorOutputBoundaryV1`

Those fields are consumed from the admitted contract result. They are not recomputed from lower
layers.

### Exact truthful realization decision

The current implementation can only emit:

- one truthful non-located replay-input locator result

The exact disposition is:

- `RealizedForTruthfulNonLocatedReplayInputLocatorOnly`

That is the narrowest honest result because the admitted contract still exposes only:

- preserved receipt-bound lineage
- one contract-only locator handle kind,
  `FutureParserConsumableReplayHandleOnly`

The current repo therefore cannot honestly claim any narrower successful replay-input locator
result because:

- the admitted contract does not carry a replay file path
- the admitted contract does not carry replay bytes
- the admitted contract does not carry replay frames
- `source_replay` remains opaque lineage only
- the audited family root may not be reinterpreted as replay storage
- the contract handle kind remains a contract-only future parser-consumable handle, not realized
  locator success

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

- the admitted replay-input-access/source-binding boundary input
- the admitted replay-input-access/source-binding output boundary
- the replay-input locator boundary input
- the replay-input locator output boundary
- the preserved receipt-bound root/path binding

### What it explicitly refuses to promise

This realization explicitly refuses to promise:

- actual replay-input location
- replay files
- replay file paths
- replay bytes
- replay frames
- actual replay parsing
- raw-state payload availability
- tensor availability
- control/action availability
- `mimir_export` widening
- sidecar/manifest realization

## F. REALIZATION OUTPUT V1

The minimum family-specific replay-input locator realization result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_contract_disposition`
- preserved `source_contract_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `source_chosen_materialization_contract_shape`
- preserved `source_chosen_replay_parsing_contract_shape`
- preserved `source_chosen_replay_input_access_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- preserved per-specimen replay-input locator results
- bounded `realization_disposition`
- bounded `realization_notes`
- preserved `chosen_replay_input_locator_contract_shape`

Each per-specimen result contains exactly:

- `specimen_ordinal`
- `consumed_replay_input_locator_boundary_input`
- `preserved_replay_input_locator_output_boundary`
- `replay_input_locator_disposition`

The exact top-level disposition is:

- `RealizedForTruthfulNonLocatedReplayInputLocatorOnly`

The exact note set is:

- `ReplayInputLocatorContractBoundaryPreserved`
- `ContractInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForNonLocatedReplayInputLocatorOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `FutureParserConsumableReplayHandleKindPreservedWithoutLocatorSuccess`
- `TruthfulNonLocatedReplayInputLocatorResultOnly`
- `ReplayInputLocatorImplementationStillDeferred`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The replay-input locator contract may enter this realization boundary only when all of the
following hold:

1. the input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorContractV1`
2. `source_realization_disposition ==`
   `RealizedForTruthfulNonLocatedReplayInputAccessSourceBindingOnly`
3. `source_realization_notes` remain the exact frozen replay-input-access/source-binding
   realization note set
4. `source_reopen_decision_disposition ==`
   `ReopenJustifiedForReceiptBoundReplayInputLocatorContract`
5. `source_reopen_decision_notes` remain the exact frozen replay-input locator reopen decision
   note set
6. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
7. `source_chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
8. `source_chosen_replay_parsing_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
9. `source_chosen_replay_input_access_contract_shape ==`
   `ReceiptBoundReplayInputAccessSourceBindingOnly`
10. `contract_disposition ==`
    `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorOnly`
11. `contract_notes` remain the exact frozen replay-input locator contract note set
12. `chosen_replay_input_locator_contract_shape == ReceiptBoundReplayInputLocatorOnly`
13. `specimen_count > 0`
14. `group_count > 0`
15. `group_count` equals the number of preserved ordered lane results
16. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
17. `audited_family_root_directory` still exists and is a directory at realization time
18. lane order and specimen order remain exact
19. every `anchored_bc_specimen_file_path` remains receipt-bound below
    `audited_family_root_directory`
20. every replay-input locator boundary input still matches the admitted replay-input-access /
    source-binding boundary input on the preserved identity tuple and deferred observation lineage
21. every replay-input locator output boundary still matches the replay-input locator boundary input
    on the preserved identity tuple and deferred observation lineage
22. every admitted replay-input-access/source-binding output boundary still preserves
    `FutureParserConsumableReplayHandleOnly`
23. every replay-input locator output boundary still preserves
    `FutureParserConsumableReplayHandleOnly`
24. no lower boundary is silently reopened to repair or reinterpret the admitted contract input

Admission here means only:

- the repo may realize one truthful non-located replay-input locator result above the admitted
  contract

Admission here does not mean:

- replay-input locator succeeds
- replay parsing succeeds
- replay files or replay bytes are available
- raw-state payload exists
- tensors or controls are available

## H. FAILURE RULES

This pass must hard-fail for:

- degraded contract input
- mismatched counts, root, order, or artifact ids
- any attempt to reinterpret `source_replay` or `provenance_label` as an implicit replay locator
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen this pass into actual replay-input locator implementation
- any attempt to widen this pass into actual replay parsing
- any attempt to widen this pass into actual raw-state payload materialization
- any attempt to widen this pass into tensor/control materialization
- any admitted/input/output boundary identity drift on:
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

## J. RELATION TO NEXT STAGES

This pass guarantees to the next step that:

- the replay-input locator contract is now consumable through one machine-checkable realization
  result
- the current truthful limit is explicit:
  `RealizedForTruthfulNonLocatedReplayInputLocatorOnly`
- the preserved receipt-bound identity tuple, deferred observation lineage, lane/specimen order,
  artifact ids, and audited family root remain frozen across realization
- `FutureParserConsumableReplayHandleOnly` remains preserved without pretending locator success

What remains deferred:

- any actual replay-input locator implementation
- any actual replay parsing
- any actual raw-state payload materialization
- any tensor/control materialization
- any `mimir_export` widening

That makes the next pass obvious:

- an explicit replay-input locator implementation reopen decision above this truthful non-located
  replay-input locator realization result
