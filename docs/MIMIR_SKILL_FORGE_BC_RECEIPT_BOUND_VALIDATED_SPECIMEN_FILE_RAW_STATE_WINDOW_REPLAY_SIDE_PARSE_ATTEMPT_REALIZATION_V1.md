# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Side Parse-Attempt Realization v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual replay-side parse-attempt realization boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`

It defines:

- the first truthful realized result surface above the replay-side parse-attempt contract
- the narrowest honest per-specimen replay-side parse-attempt result the current repo can emit
- the exact admission and failure rules for realizing that result

### Why it exists

The boundary below this pass already fixed the contract shape for one admitted specimen:

- one exact replay-side parse-attempt input tuple
- one exact replay-side parse-attempt output boundary
- preserved receipt-bound identity and deferred observation lineage

What was still missing was the first realized result above that contract.

### How it differs from the replay-side parse-attempt contract-definition boundary below it

- The lower boundary defines the contract shape only.
- This pass realizes the first truthful result above that contract.
- The lower boundary still leaves result semantics unchosen.
- This pass chooses the result semantics and makes them explicit.
- Neither boundary implements actual replay parsing success.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this realization version.

This realization boundary remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`
- the preserved lineage fields and deferred observation lineage are the low-boost-recovery BC
  specimen fields already carried by that contract
- no second family exists that would justify a generic replay-side realization framework

No generic multi-family replay/raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`
- the audited family root directory reference already preserved by that contract

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_realization_disposition`
- `source_realization_notes`
- `source_reopen_decision_disposition`
- `source_reopen_decision_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `admitted_materialization_attempt_input`
- each `admitted_materialization_attempt_output_boundary`
- each `replay_side_parse_attempt_input`
- each `replay_side_parse_attempt_output_boundary`
- `contract_disposition`
- `contract_notes`
- `chosen_replay_parsing_contract_shape`

Direct input is no longer:

- materialization-attempt realization results
- replay-parsing reopen decisions
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

Those lower layers remain frozen. This pass starts strictly from the replay-side parse-attempt
contract and the already-preserved audited family root reference.

## D. REALIZATION ROLE

This realization owns exactly one thing:

- realizing the first honest replay-side parse-attempt result for one admitted contract specimen

This pass is allowed to realize only:

- preserved receipt-bound specimen identity and lineage
- the admitted replay-side parse-attempt input tuple
- the admitted replay-side parse-attempt output boundary
- one truthful bounded attempt disposition above that contract

This pass is not allowed to realize:

- replay file resolution
- replay bytes
- replay frames
- replay parsing success
- replay-derived raw-state payload
- tensor payload
- control/action payload
- sidecars
- manifests
- generic indexes
- `mimir_export` outputs

## E. REPLAY-SIDE PARSE-ATTEMPT REALIZATION SHAPE V1

### Exact realization types

This pass defines exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationError`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_side_parse_attempt_v1(...)`

### Exact per-specimen contract input consumed

For one admitted specimen, this realization consumes exactly:

- `replay_side_parse_attempt_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptInputV1`
- `replay_side_parse_attempt_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptOutputBoundaryV1`

Those fields are consumed from the admitted contract result. They are not recomputed from lower
layers.

### Exact truthful attempt-result shape

The current implementation can only emit:

- one truthful blocked / unavailable replay-side parse-attempt result

The exact disposition is:

- `RealizedForTruthfulBlockedReplaySideParseAttemptOnly`

That is the narrowest honest result because the admitted contract preserves only replay lineage:

- `source_replay` remains provenance, not replay storage access
- `source_raw_state_window_ref` remains lineage, not replay payload
- `audited_family_root_directory` remains only the BC specimen-tree anchor

The current repo therefore cannot honestly claim any narrower replay-side access result below parse
success because:

- the admitted contract does not carry a replay file path
- the admitted contract does not carry replay bytes
- the audited family root may not be reinterpreted as replay storage
- `mimir-replay` still exposes no real parser success surface

### Exact identity checks that must still hold

For one admitted specimen, this realization requires the exact same preserved identity tuple:

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

- the admitted materialization-attempt input
- the replay-side parse-attempt input
- the replay-side parse-attempt output boundary
- the preserved receipt-bound root/path binding

### What it explicitly refuses to promise

This realization explicitly refuses to promise:

- actual replay parsing success
- replay frame availability
- replay file path availability
- replay byte availability
- raw-state payload availability
- tensor availability
- control/action availability
- `mimir_export` widening
- sidecar/manifest realization

## F. REALIZATION OUTPUT V1

The minimum family-specific replay-side parse-attempt realization result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_contract_disposition`
- preserved `source_contract_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `source_chosen_materialization_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- preserved per-specimen replay-side parse-attempt results
- bounded `realization_disposition`
- bounded `realization_notes`
- preserved `chosen_replay_parsing_contract_shape`

Each per-specimen result contains exactly:

- `specimen_ordinal`
- `consumed_replay_side_parse_attempt_input`
- `preserved_replay_side_parse_attempt_output_boundary`
- `replay_side_parse_attempt_disposition`

The exact top-level disposition is:

- `RealizedForTruthfulBlockedReplaySideParseAttemptOnly`

The exact note set is:

- `ReplaySideParseAttemptContractBoundaryPreserved`
- `ContractInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForBlockedReplaySideParseAttemptOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `ReplaySideAccessStillUnavailableForTruthfulAttemptOnly`
- `TruthfulBlockedReplaySideParseAttemptResultOnly`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The replay-side parse-attempt contract may enter this realization boundary only when all of the
following hold:

1. the input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`
2. `source_realization_disposition == RealizedForTruthfulNonMaterializedAttemptOnly`
3. `source_realization_notes` remain the exact frozen truthful non-materialized realization note
   set
4. `source_reopen_decision_disposition ==`
   `ReopenJustifiedForReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptContract`
5. `source_reopen_decision_notes` remain the exact frozen replay-parsing reopen note set
6. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
7. `source_chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
8. `contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptOnly`
9. `contract_notes` remain the exact frozen replay-side parse-attempt contract note set
10. `chosen_replay_parsing_contract_shape ==`
    `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
11. `specimen_count > 0`
12. `group_count > 0`
13. `group_count` equals the number of preserved ordered lane results
14. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
15. `audited_family_root_directory` still exists and is a directory at realization time
16. lane order and specimen order remain exact
17. every `anchored_bc_specimen_file_path` remains receipt-bound below
    `audited_family_root_directory`
18. every replay-side parse-attempt input still matches the admitted materialization-attempt input
    on the preserved identity tuple
19. every replay-side parse-attempt output boundary still matches the replay-side parse-attempt
    input on the preserved identity tuple
20. every replay-side parse-attempt output boundary still matches the admitted output boundary on:
    - `preserved_observation_binding_kind`
    - `preserved_accepted_reference_window`

Admission here means only:

- the repo may realize one truthful blocked/unavailable replay-side parse-attempt result above the
  admitted contract

Admission here does not mean:

- replay-side access succeeds
- replay parsing succeeds
- replay files or bytes are available
- raw-state payload exists
- tensors or controls exist

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded contract input
- mismatched counts/root/order/artifact ids
- any drift between admitted materialization identity and replay-side parse-attempt identity
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen into actual replay parsing success
- any attempt to widen into actual raw-state payload materialization
- any attempt to widen into tensor/control materialization

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

- no actual replay parsing success
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

- one explicit replay-side parse-attempt realization result exists above the contract
- that result is truthful about the current blocked/unavailable state
- preserved receipt-bound identity and deferred observation lineage remain visible without
  inventing replay storage or replay payload semantics
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual replay-side access
- actual replay parsing
- replay bytes or replay frames
- actual raw-state-window payload materialization
- tensor/control materialization

The immediate next pass should be:

- a replay-parsing success / parser-implementation reopen decision

That next pass should consume:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- implement `mimir_export` integration
- implement raw-state payload materialization
- implement tensor/control materialization
- add sidecars/manifests unless separately proven necessary
