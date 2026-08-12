# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Input Locator Implementation Realization v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual replay-input locator implementation realization boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`

It defines:

- the first truthful realized result surface above the replay-input locator implementation contract
- the narrowest honest per-specimen implementation-facing result the current repo can emit
- the exact admission and failure rules for realizing that result

### Why it exists

The boundary below this pass already fixed:

- one admitted specimen yields one exact replay-input locator implementation boundary input tuple
- one admitted specimen yields one exact replay-input locator implementation output boundary
- preserved receipt-bound identity and deferred observation lineage remain explicit
- `FutureParserConsumableReplayHandleOnly` remains contract-only and not locator success

What was still missing was the first truthful realized result above that contract:

- can the repo currently realize any actual replay-input locator implementation-facing success, or
  can it only emit a bounded blocked/unavailable implementation result?

### How it differs from the replay-input locator implementation contract-definition boundary below it

- The lower boundary defines the contract shape only.
- This pass realizes the first truthful result above that contract.
- The lower boundary leaves implementation result semantics unchosen.
- This pass chooses the result semantics and makes them explicit.
- Neither boundary implements actual replay-input locator logic, replay parsing, raw-state
  materialization, tensor materialization, or control extraction.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this realization version.

This realization boundary remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`
- the preserved lineage tuple and deferred observation lineage are only the low-boost-recovery BC
  specimen fields already carried by that contract
- no second family exists that would justify a generic replay-input locator implementation
  realization framework

No generic multi-family replay/raw-state/index/export/materialization framework is introduced
here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`
- the audited family root directory reference already preserved by that contract

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`,
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
- `source_chosen_replay_input_locator_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `admitted_replay_input_locator_boundary_input`
- each `admitted_replay_input_locator_output_boundary`
- each `admitted_replay_input_locator_disposition`
- each `replay_input_locator_implementation_boundary_input`
- each `replay_input_locator_implementation_output_boundary`
- `contract_disposition`
- `contract_notes`
- `chosen_replay_input_locator_implementation_contract_shape`

The following are no longer direct input at this boundary:

- replay-input locator contracts and reopen decisions below this layer
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

Those lower layers remain frozen. This pass starts strictly from the replay-input locator
implementation contract and the already-preserved audited family root reference.

## D. REALIZATION ROLE

This realization owns exactly one thing:

- realizing the first honest replay-input locator implementation-facing result for one admitted
  contract specimen

This pass is allowed to realize only:

- preserved receipt-bound specimen identity and lineage
- the admitted replay-input locator implementation boundary input tuple
- the admitted replay-input locator implementation output boundary
- one truthful bounded blocked/unavailable implementation disposition above that contract

This pass is not allowed to realize:

- actual replay-input locator implementation
- replay file discovery
- replay file paths
- replay bytes
- replay frames
- actual `mimir_replay::ReplayInput`
- actual replay parsing
- raw-state payload materialization
- tensor payloads
- control/action payloads
- sidecars
- manifests
- generic indexes
- `mimir_export` outputs

## E. REPLAY-INPUT LOCATOR IMPLEMENTATION REALIZATION SHAPE V1

### Exact realization types

This pass defines exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationRealizationError`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_input_locator_implementation_v1(...)`

### Exact per-specimen contract input consumed

For one admitted specimen, this realization consumes exactly:

- `replay_input_locator_implementation_boundary_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationBoundaryInputV1`
- `replay_input_locator_implementation_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationOutputBoundaryV1`

Those fields are consumed from the admitted contract result. They are not recomputed from lower
layers.

### Exact truthful realization decision

The current implementation can only emit:

- one truthful blocked / unavailable replay-input locator implementation result

The exact disposition is:

- `RealizedForTruthfulBlockedReplayInputLocatorImplementationOnly`

That is the narrowest honest result because the admitted contract still exposes only:

- preserved receipt-bound lineage
- one contract-only future parser-consumable replay handle kind,
  `FutureParserConsumableReplayHandleOnly`
- one deferred acknowledgment that later explicit implementation work could target
  `mimir_replay::ReplayInput` without materializing or promising one now

The current repo therefore cannot honestly claim any successful implementation-facing replay-input
locator result because:

- the admitted contract does not carry a replay file path
- the admitted contract does not carry replay bytes
- the admitted contract does not carry replay frames
- the admitted contract does not carry an actual `mimir_replay::ReplayInput`
- `source_replay` remains opaque lineage only
- the audited family root may not be reinterpreted as replay storage
- the implementation output boundary still carries only a contract-only future handle and not a
  located input

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

- `admitted_replay_input_locator_boundary_input`
- `admitted_replay_input_locator_output_boundary`
- `replay_input_locator_implementation_boundary_input`
- `replay_input_locator_implementation_output_boundary`
- the preserved receipt-bound root/path binding

### What it explicitly refuses to promise

This realization explicitly refuses to promise:

- actual replay-input locator implementation
- actual replay-input location
- replay files
- replay file paths
- replay bytes
- replay frames
- actual `mimir_replay::ReplayInput`
- actual replay parsing
- raw-state payload availability
- tensor availability
- control/action availability
- `mimir_export` widening
- sidecar/manifest realization

## F. REALIZATION OUTPUT V1

The minimum family-specific replay-input locator implementation realization result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationRealizationResultV1`

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
- preserved `audited_family_root_directory`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- preserved per-specimen replay-input locator implementation results
- bounded `realization_disposition`
- bounded `realization_notes`
- preserved `chosen_replay_input_locator_implementation_contract_shape`

Each per-specimen result contains exactly:

- `specimen_ordinal`
- `consumed_replay_input_locator_implementation_boundary_input`
- `preserved_replay_input_locator_implementation_output_boundary`
- `replay_input_locator_implementation_disposition`

The exact top-level disposition is:

- `RealizedForTruthfulBlockedReplayInputLocatorImplementationOnly`

The exact note set is:

- `ReplayInputLocatorImplementationContractBoundaryPreserved`
- `ContractInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForBlockedReplayInputLocatorImplementationOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `FutureParserConsumableReplayHandleRemainsContractOnlyWithoutImplementationOrLocatorSuccess`
- `FutureMimirReplayReplayInputTargetRemainsAcknowledgedOnlyWithoutMaterializationOrPromise`
- `ReplayInputLocatorImplementationStillUnavailableForTruthfulResultOnly`
- `TruthfulBlockedReplayInputLocatorImplementationResultOnly`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The replay-input locator implementation contract may enter this realization boundary only when all
of the following hold:

1. the input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`
2. `source_realization_disposition == RealizedForTruthfulNonLocatedReplayInputLocatorOnly`
3. `source_realization_notes` remain the exact frozen replay-input locator realization note set
4. `source_reopen_decision_disposition ==`
   `ReopenJustifiedForReceiptBoundReplayInputLocatorImplementationContract`
5. `source_reopen_decision_notes` remain the exact frozen replay-input locator implementation
   reopen-decision note set
6. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
7. `source_chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
8. `source_chosen_replay_parsing_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
9. `source_chosen_replay_input_access_contract_shape ==`
   `ReceiptBoundReplayInputAccessSourceBindingOnly`
10. `source_chosen_replay_input_locator_contract_shape == ReceiptBoundReplayInputLocatorOnly`
11. `contract_disposition ==`
    `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationOnly`
12. `contract_notes` remain the exact frozen replay-input locator implementation contract note set
13. `chosen_replay_input_locator_implementation_contract_shape ==`
    `ReceiptBoundReplayInputLocatorImplementationOnly`
14. `specimen_count > 0`
15. `group_count > 0`
16. `group_count` equals the number of preserved ordered lane results
17. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
18. `audited_family_root_directory` still exists and is a directory at realization time
19. lane order and specimen order remain exact
20. every `anchored_bc_specimen_file_path` remains receipt-bound below
    `audited_family_root_directory`
21. every admitted replay-input locator boundary input still matches the admitted replay-input
    locator output boundary on the preserved identity tuple and deferred observation lineage
22. every replay-input locator implementation boundary input still matches the admitted replay-input
    locator output boundary on the preserved identity tuple and deferred observation lineage
23. every replay-input locator implementation output boundary still matches the replay-input
    locator implementation boundary input on the preserved identity tuple and deferred observation
    lineage
24. every admitted and implementation output boundary still preserves
    `FutureParserConsumableReplayHandleOnly`
25. every admitted specimen still preserves
    `admitted_replay_input_locator_disposition == RealizedForTruthfulNonLocatedReplayInputLocatorOnly`
26. no lower boundary is silently reopened to repair or reinterpret the admitted contract input

Admission here means only:

- the repo may realize one truthful blocked/unavailable replay-input locator implementation result
  above the admitted contract

Admission here does not mean:

- replay-input locator implementation succeeds
- replay-input location succeeds
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

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- one explicit replay-input locator implementation realization result exists above the contract
- that result is truthful about the current blocked/unavailable implementation state
- preserved receipt-bound identity and deferred observation lineage remain visible without
  inventing replay storage, replay payload, or parser-success semantics
- `FutureParserConsumableReplayHandleOnly` remains preserved without pretending implementation or
  locator success
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual replay-input locator implementation
- actual replay-input location
- actual `mimir_replay::ReplayInput`
- actual replay parsing
- replay bytes or replay frames
- actual raw-state-window payload materialization
- tensor/control materialization

The immediate next pass should be:

- a replay-input locator actual-implementation reopen decision above this truthful blocked
  implementation realization result

That next pass should consume:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationRealizationResultV1`

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- implement actual replay-input locator logic
- implement actual replay parsing
- implement actual raw-state payload materialization
- implement tensor/control materialization
- add sidecars/manifests unless separately proven necessary
