# MIMIR Skill Forge BC Receipt-Bound Specimen-File-Anchored Raw-State-Window Locator Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the first contract-definition boundary for:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`

It defines only:

- the exact admitted boundary above:
  - `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
  - `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`
  - `LowBoostRecoveryBcReceiptBoundRawStateWindowLocatorReopenDecisionResultV1`
- the exact per-specimen contract input preserved from the planning result
- the exact deterministic BC specimen-file lookup source exposed by the contract
- the exact bounded contract-definition output, disposition, notes, and failure rules

### Why it exists

The realization-proof boundary already proved the current planning-owned view is insufficient for
actual raw-state-window lookup realization.

The reopen-decision boundary already fixed:

- reopen is justified
- the missing next shape is exactly:
  `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`
- the next pass must stay:
  - low-boost-recovery-specific
  - strictly receipt-bound
  - specimen-file-anchored
  - contract-only

This pass exists because the reopened shape must be made machine-verifiable before any later pass
tries to realize even a first locator.

### How it differs from the reopen-decision boundary below it

- The reopen-decision boundary answers whether reopening is justified at all.
- This pass defines the reopened contract surface itself.
- This pass still does not realize raw-state lookup.
- This pass still does not materialize raw state, tensors, or controls.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This locator contract remains family-specific because:

- the admitted planning boundary is low-boost-recovery-specific
- the admitted specimen view is still low-boost-recovery BC lineage only
- the deterministic lane/specimen naming rules already fixed below this boundary are:
  - `recovery_context_lane_{lane_ordinal:04}`
  - `specimen_{specimen_ordinal:04}.json`
- no second family exists yet to justify a shared locator contract framework

No generic all-family locator/index/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
- `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`
- `LowBoostRecoveryBcReceiptBoundRawStateWindowLocatorReopenDecisionResultV1`
- the audited family root directory reference preserved by the planning result and echoed by the
  proof result and reopen decision result

Within `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`, this pass
consumes:

- `specimen_count`
- `group_count`
- `source_consumer_disposition`
- `source_consumer_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `lookup_planning_consumed_specimen_view.artifact_id`
- each `lookup_planning_consumed_specimen_view.source_raw_state_window_ref`
- each `lookup_planning_consumed_specimen_view.source_slice_id`
- each `lookup_planning_consumed_specimen_view.source_replay`
- each `lookup_planning_consumed_specimen_view.source_subject`
- each `lookup_planning_consumed_specimen_view.source_phase_id`
- each `lookup_planning_consumed_specimen_view.accepted_reference_variant_id`
- each `lookup_planning_consumed_specimen_view.observation_binding_kind`
- each `lookup_planning_consumed_specimen_view.accepted_reference_window`
- `planning_disposition`
- `planning_notes`

Within `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`, this pass consumes:

- `specimen_count`
- `group_count`
- `source_planning_disposition`
- `source_planning_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `artifact_id`
- `proof_disposition`
- `proof_notes`
- `exact_insufficiency_marker`

Within `LowBoostRecoveryBcReceiptBoundRawStateWindowLocatorReopenDecisionResultV1`, this pass
consumes:

- `specimen_count`
- `group_count`
- `source_planning_disposition`
- `source_planning_notes`
- `source_proof_disposition`
- `source_proof_notes`
- `source_exact_insufficiency_marker`
- `audited_family_root_directory`
- `decision_disposition`
- `decision_notes`
- `chosen_locator_contract_shape`

### Boundary rule

Direct input is no longer:

- first concrete specimen consumer results
- continued receipt-bound downstream results
- emitted-output audit/readback results
- actual emission receipts
- filesystem/export-emission plans
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- accepted shells
- lower planning boundaries

Those lower layers remain frozen. This pass starts strictly from planning, proof, reopen decision,
and the preserved audited family root directory reference.

## D. CONTRACT ROLE

This contract owns exactly one thing:

- binding one admitted planning specimen to one deterministic receipt-bound BC specimen-file lookup
  source under the audited family root

This contract is allowed to bind:

- `audited_family_root_directory`
- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `source_raw_state_window_ref`
- the preserved planning-owned lineage needed to keep that binding auditable

This contract is not allowed to realize:

- raw-state payload lookup
- replay parsing
- raw-state materialization
- observation materialization
- tensor materialization
- control/action extraction
- sidecar/manifest/index authority
- `mimir_export` integration

## E. CONTRACT SHAPE V1

The contract name is fixed to exactly:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`

### Exact per-specimen admitted inputs

For one admitted specimen, this contract preserves exactly:

- enclosing `lane_ordinal`
- enclosing `specimen_ordinal`
- `artifact_id`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`
- `accepted_reference_variant_id`
- `observation_binding_kind`
- `accepted_reference_window`

Those specimen-scoped fields are materialized in Rust as:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractAdmittedSpecimenV1`

The proof result is an admission precondition only. It is not a per-specimen locator operand.

### Exact deterministic emitted specimen-file path shape

For one admitted specimen, the deterministic emitted specimen-file path shape is fixed to:

- `audited_family_root_directory/recovery_context_lane_{lane_ordinal:04}/specimen_{specimen_ordinal:04}.json`

The contract stores only the deterministic relative path component:

- `recovery_context_lane_{lane_ordinal:04}/specimen_{specimen_ordinal:04}.json`

That relative path is emitted in Rust as:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorLookupSourceV1.deterministic_bc_specimen_file_relative_path`

### Exact locator output shape

The contract exposes exactly one locator output per admitted specimen:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorLookupSourceV1`

It contains exactly:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `source_raw_state_window_ref`
- `deterministic_bc_specimen_file_relative_path`

This is a receipt-bound BC specimen-file lookup source only.

It is not:

- a raw-state payload
- a replay-frame locator
- a tensor locator
- a control locator
- a manifest/index entry

### Exact invariant

The invariant in v1 is:

- for one admitted specimen, the tuple
  (`audited_family_root_directory`, `lane_ordinal`, `specimen_ordinal`, `artifact_id`,
  `source_raw_state_window_ref`) binds to exactly one deterministic BC specimen-file lookup source
  under:
  `audited_family_root_directory/recovery_context_lane_{lane_ordinal:04}/specimen_{specimen_ordinal:04}.json`
- that lookup source remains receipt-bound to the already-admitted low-boost-recovery BC specimen
  tree
- the contract must preserve the same `artifact_id` and `source_raw_state_window_ref` in both:
  - the admitted specimen view
  - the deterministic lookup source

### Exact relationship to `observation_binding_kind`

`observation_binding_kind` remains:

- an admitted planning-owned contract input
- fixed to
  `AcceptedReferenceWindowFromRawStateWindowRef`
- preserved to constrain later observation-access semantics

This contract does not reinterpret `observation_binding_kind` into lookup realization.

### Exact relationship to `accepted_reference_window`

`accepted_reference_window` remains:

- an admitted planning-owned contract input
- preserved unchanged from the planning boundary
- bound only as the observation-access window paired with the admitted
  `source_raw_state_window_ref`

This contract does not materialize that window from raw state.

## F. CONTRACT OUTPUT V1

The minimum family-specific contract-definition output is:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_planning_disposition`
- preserved `source_planning_notes`
- preserved `source_proof_disposition`
- preserved `source_proof_notes`
- preserved `source_reopen_decision_disposition`
- preserved `source_reopen_decision_notes`
- preserved `source_exact_insufficiency_marker`
- preserved `audited_family_root_directory`
- preserved ordered lane/specimen results
- chosen `contract_disposition`
- bounded `contract_notes`
- chosen `chosen_locator_contract_shape`

### Lane/specimen output shape

Each lane result is:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractLaneResultV1`

It contains exactly:

- `lane_ordinal`
- ordered `ordered_specimen_results`

Each specimen result is:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractSpecimenResultV1`

It contains exactly:

- `specimen_ordinal`
- `admitted_planning_specimen`
- `deterministic_lookup_source`

### Exact contract disposition

`contract_disposition` is fixed to exactly:

- `ContractDefinedForReceiptBoundSpecimenFileLookupSourceOnly`

### Exact contract notes

`contract_notes` are fixed to exactly:

- `RawStateWindowLookupObservationAccessPlanningBoundaryPreserved`
- `RawStateWindowLookupRealizationProofBoundaryPreserved`
- `ReceiptBoundRawStateWindowLocatorReopenDecisionBoundaryPreserved`
- `PlanningProofAndReopenInputsCrossValidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `DeterministicReceiptBoundBcSpecimenFileLookupSourceDefined`
- `SourceRawStateWindowRefPreservedAsOpaqueLocatorBindingInput`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `ActualRawStateWindowLookupRealizationDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

Planning, proof, and reopen-decision inputs may enter this boundary only when all of the
following hold:

1. the inputs are exactly:
   - `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
   - `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`
   - `LowBoostRecoveryBcReceiptBoundRawStateWindowLocatorReopenDecisionResultV1`
2. planning plus proof still satisfy the exact reopen-decision admission and mismatch checks
3. the reopen decision still satisfies its exact disposition, note, marker, root, and shape checks
4. `decision_disposition ==
   ReopenJustifiedForReceiptBoundSpecimenFileAnchoredLocatorContract`
5. `chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
6. planning, proof, and reopen counts match exactly
7. planning, proof, and reopen audited family root directory references match exactly
8. planning and proof lane/specimen order still match exactly
9. planning and proof artifact ids still match exactly at every lane/specimen position
10. no lower boundary is silently reopened to recreate or repair admitted input

Admission here means only:

- this contract surface may be defined from trusted planning/proof/reopen evidence

Admission here does not mean:

- actual raw-state lookup realization is now legal
- BC specimen files contain raw state
- sidecar/manifest realization is justified
- `mimir_export` may be widened

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded planning input
- degraded proof input
- degraded reopen decision input
- mismatched counts between planning/proof/reopen
- mismatched audited family root references
- mismatched lane/specimen order
- mismatched artifact ids
- any attempt to reinterpret the audited family root as raw-state storage
- any attempt to widen this boundary into actual lookup realization
- any attempt to widen this boundary into sidecars, manifests, generic indexing, or
  `mimir_export`

### Failure behavior

- no repair is allowed
- no receipt regeneration is allowed
- no filesystem re-audit is allowed
- no specimen is skipped
- no resorting is allowed
- no guessed path repair is allowed
- no partial contract result is returned

## I. NON-GOALS

This pass does not do any of the following:

- no actual raw-state lookup realization
- no raw-state locator/index implementation beyond contract definition
- no `mimir_export` integration
- no sidecar/manifest realization
- no generic manifest/index framework
- no generic multi-family locator/index/export framework
- no tensor materialization
- no control/action extraction
- no usefulness proof
- no policy-improvement proof
- no replay parsing
- no replay ingestion
- no rollout or physics work
- no async/background system
- no database work

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- one machine-verifiable contract exists for the reopened shape
- one admitted planning specimen now contributes one exact contract input view
- one admitted planning specimen now yields one exact deterministic BC specimen-file lookup source
- the binding remains low-boost-recovery-specific
- the binding remains strictly receipt-bound
- the audited family root remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

### What remains deferred

This pass still does not guarantee:

- actual raw-state lookup realization
- BC specimen-file existence validation
- emitted specimen-file readback at this contract boundary
- raw-state materialization
- observation/tensor/control materialization

### Immediate next-stage implication

The immediate next pass should be:

- a first actual locator-realization pass above this contract, still without raw-state
  materialization

That next pass should consume this contract and realize only the deterministic BC specimen-file
locator path and its receipt-bound identity checks.

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- reinterpret the audited family root as raw-state storage
- materialize raw state, tensors, or controls
- reopen sidecars/manifests/generic indexing unless a new explicit defect-driven decision proves
  one is required
