# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Input-Access Source-Binding Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the first explicit replay-input-access / replay-source-binding contract-definition boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundReplayInputAccessReopenDecisionResultV1`

It defines:

- the exact contract-only surface for one admitted truthful blocked replay-side parse-attempt specimen
- the exact per-specimen replay-input-access / replay-source-binding boundary input tuple
- the exact per-specimen replay-input-access / replay-source-binding output boundary
- the minimum family-specific result the repo may now expose above the blocked replay-side parse-attempt realization result

### Why it exists

The reopen-decision boundary below this pass already answered two narrower questions:

- replay-input-access / replay-source-binding reopening is justified
- the narrowest honest next shape is `ReceiptBoundReplayInputAccessSourceBindingOnly`

What still did not exist was the contract itself.

This pass creates that contract without claiming replay-input location, replay parsing, replay bytes, raw-state payloads, or parser success.

### How it differs from the replay-input-access reopen-decision boundary below it

- The lower boundary decides that reopening is required.
- This pass defines the exact contract surface reopened by that decision.
- The lower boundary names the next shape but does not formalize one contract result.
- This pass formalizes that shape as one explicit contract artifact.
- Neither boundary implements actual replay-input locator logic or replay parsing.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This replay-input-access / replay-source-binding contract remains family-specific because:

- the admitted input is only `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
- the admitted reopen-decision input is only `LowBoostRecoveryBcReceiptBoundReplayInputAccessReopenDecisionResultV1`
- the preserved lineage tuple is the low-boost-recovery BC specimen tuple already carried by those results
- no second family exists that would justify a shared replay-input-access / replay-source-binding framework

No generic all-family replay/raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundReplayInputAccessReopenDecisionResultV1`
- the audited family root directory reference already preserved by those results

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`, this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `consumed_replay_side_parse_attempt_input`
- each `preserved_replay_side_parse_attempt_output_boundary`
- each `replay_side_parse_attempt_disposition`
- `realization_disposition`
- `realization_notes`
- `chosen_replay_parsing_contract_shape`

From `LowBoostRecoveryBcReceiptBoundReplayInputAccessReopenDecisionResultV1`, this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_realization_disposition`
- `source_realization_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `source_chosen_replay_parsing_contract_shape`
- `audited_family_root_directory`
- `decision_disposition`
- `decision_notes`
- `chosen_replay_input_access_contract_shape`

Direct input is no longer:

- parse-attempt contract results
- materialization-attempt realization results
- replay-parsing reopen decisions below this layer
- replay-parsing-success reopen decisions below this layer
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

Those lower layers remain frozen. This pass starts strictly from the blocked replay-side parse-attempt realization result, the replay-input-access reopen decision, and the already-preserved audited family root reference.

## D. CONTRACT ROLE

This contract owns exactly one thing:

- defining the receipt-bound replay-input-access / replay-source-binding contract surface for one admitted truthful blocked replay-side parse-attempt specimen

This pass is allowed to bind only:

- preserved receipt-bound lane/specimen identity
- preserved artifact identity
- preserved BC specimen-file anchoring
- preserved raw-state-window lineage
- preserved replay lineage
- preserved deferred observation lineage
- one contract-only future replay-handle kind attached to that exact preserved tuple

This pass is not allowed to implement:

- actual replay-input locator logic
- replay file discovery
- replay path derivation from `source_replay` or `provenance_label`
- replay storage derivation from `audited_family_root_directory`
- actual replay parsing
- actual raw-state payload materialization
- tensor materialization
- control/action extraction
- sidecars
- manifests
- generic indexes
- `mimir_export`

## E. CONTRACT SHAPE V1

### Contract name

The contract name is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`

### Exact family-specific types defined here

This pass defines exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractNoteV1`
- `LowBoostRecoveryBcReceiptBoundReplayInputAccessSourceBindingHandleKindV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingBoundaryInputV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingOutputBoundaryV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractDefinitionError`
- `define_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_input_access_source_binding_contract_v1(...)`

### Exact per-specimen admitted inputs

For one admitted specimen, this contract consumes exactly:

- `admitted_replay_side_parse_attempt_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptInputV1`
- `admitted_replay_side_parse_attempt_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptOutputBoundaryV1`

Those values are consumed from the truthful blocked replay-side parse-attempt realization result. They are not recomputed from lower layers.

### Exact replay-input-access / replay-source-binding boundary input tuple

The exact boundary input tuple for one admitted specimen is:

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

In code, that tuple is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingBoundaryInputV1`

### Exact replay-input-access / replay-source-binding output-boundary shape

The exact output boundary preserves the full boundary input tuple and adds exactly one new contract-only element:

- `bound_replay_input_access_source_binding_handle_kind`

In code, that output boundary is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingOutputBoundaryV1`

The only admitted handle kind in v1 is:

- `LowBoostRecoveryBcReceiptBoundReplayInputAccessSourceBindingHandleKindV1::FutureParserConsumableReplayHandleOnly`

That handle kind means only:

- this exact preserved lineage tuple requires exactly one future parser-consumable replay handle to be bound at a later explicit boundary

That handle kind does not mean:

- replay access exists now
- replay location exists now
- replay bytes exist now
- replay parsing is available now

### Exact invariant

For one admitted low-boost-recovery truthful blocked replay-side parse-attempt specimen, the tuple:

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

binds to exactly one honest future parser-consumable replay handle contract slot.

That slot is authoritative only for this exact preserved tuple.

The contract must not:

- rewrite lane/specimen ordinals
- rewrite artifact identity
- rewrite BC specimen-file anchoring
- rewrite replay lineage
- rewrite deferred observation lineage
- drop or reorder preserved lineage fields

### Exact relationship to deferred observation lineage

`preserved_observation_binding_kind` and `preserved_accepted_reference_window` stay preserved as deferred lineage only.

This contract does not reopen observation materialization.

It guarantees only that deferred observation lineage remains attached to the same specimen while replay-input access / replay-source-binding is being defined.

### Exact opaque-lineage rule for `source_replay`

`source_replay` remains opaque lineage unless and until a later explicit boundary says otherwise.

In v1:

- `source_replay.replay_id` is not a path
- `source_replay.provenance_label` is not a path
- `source_replay` is not an implicit replay-input locator

### Exact BC specimen-tree rule for `audited_family_root_directory`

`audited_family_root_directory` remains only a BC specimen-tree anchor.

In v1:

- it is allowed to prove receipt-bound anchoring of BC specimen files
- it is not allowed to imply replay storage
- it is not allowed to imply replay lookup success

## F. CONTRACT OUTPUT V1

The minimum family-specific contract-definition result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`

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
- preserved `audited_family_root_directory`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- preserved per-specimen admitted replay-side parse-attempt input/output-boundary data
- chosen replay-input-access / replay-source-binding contract shape
- bounded contract-definition disposition
- bounded contract-definition notes

The exact top-level disposition is:

- `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingOnly`

The exact chosen contract shape is:

- `ReceiptBoundReplayInputAccessSourceBindingOnly`

The exact note set is:

- `ReplaySideParseAttemptRealizationBoundaryPreserved`
- `ReplayInputAccessReopenDecisionBoundaryPreserved`
- `RealizationAndReopenInputsCrossValidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForReplayInputAccessSourceBindingOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `ReplayInputAccessSourceBindingContractOnlyBoundaryDefined`
- `FutureParserConsumableReplayHandleContractOnlyOutputBoundaryDefined`
- `ReplayInputLocatorImplementationStillDeferred`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The blocked replay-side parse-attempt realization result plus replay-input-access reopen decision may enter this contract-definition boundary only when all of the following hold:

1. the realization input is exactly `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
2. the reopen input is exactly `LowBoostRecoveryBcReceiptBoundReplayInputAccessReopenDecisionResultV1`
3. the realization input still satisfies the exact blocked replay-side parse-attempt realization invariant set
4. the reopen input still satisfies the exact replay-input-access reopen-decision invariant set
5. `specimen_count > 0`
6. `group_count > 0`
7. realization and reopen counts match exactly
8. realization and reopen audited family root references match exactly
9. realization and reopen preserved lower-shape references match exactly
10. lane order and specimen order remain exact
11. artifact ids remain unique across admitted specimens
12. each admitted BC specimen file path remains receipt-bound below `audited_family_root_directory`
13. each admitted output boundary still matches the admitted replay-side parse-attempt input on the preserved identity tuple
14. `chosen_replay_input_access_contract_shape == ReceiptBoundReplayInputAccessSourceBindingOnly`

Admission here means only:

- the repo may define one explicit contract-only replay-input-access / replay-source-binding boundary above the truthful blocked replay-side parse-attempt realization result

Admission here does not mean:

- replay-input access succeeds
- replay locator logic exists
- replay parsing succeeds
- replay files or bytes are available
- raw-state payload exists
- tensors or controls exist

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded realization input
- degraded replay-input-access reopen-decision input
- mismatched counts/root/order/artifact ids
- any realization/reopen cross-input drift
- any attempt to reinterpret `source_replay` or `provenance_label` as an implicit replay locator
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen into actual replay-input locator implementation
- any attempt to widen into actual replay parsing
- any attempt to widen into actual raw-state payload materialization

This v1 boundary is intentionally strict:

- no repair
- no specimen skipping
- no resorting
- no replay-path guessing
- no replay-byte guessing
- no handle synthesis beyond the one contract-only handle kind
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

- one explicit replay-input-access / replay-source-binding contract artifact exists
- that contract stays low-boost-recovery-specific
- that contract stays strictly receipt-bound
- `source_replay` is still explicit opaque lineage only
- `audited_family_root_directory` is still explicit BC specimen-tree anchoring only
- the only newly admitted output element is one contract-only future parser-consumable replay-handle kind
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual replay-input access
- actual replay-input location
- actual replay parsing
- replay bytes or replay frames
- actual raw-state-window payload materialization
- tensor/control materialization

The immediate next pass should be:

- one first replay-input-access / replay-source-binding realization pass above this contract
- still without actual replay-input locator implementation
- still without actual replay parsing
- still without actual raw-state payload materialization

That next pass should still not:

- widen `mimir_export` unless explicitly reopened
- implement sidecars/manifests/generic indexing
- implement tensor/control materialization
