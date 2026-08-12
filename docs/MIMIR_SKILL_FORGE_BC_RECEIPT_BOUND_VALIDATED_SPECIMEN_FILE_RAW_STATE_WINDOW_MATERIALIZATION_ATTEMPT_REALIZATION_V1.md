# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Materialization Attempt Realization v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual raw-state materialization-attempt realization boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`

It defines:

- one exact realization input boundary above the materialization contract
- one exact realization role for the first low-boost-recovery raw-state materialization attempt
- one exact decision about what the current repo can honestly realize without replay parsing
- one minimal family-specific realization result surface
- one strict admission rule for when a materialization contract may enter this realization boundary
- one strict failure rule for degraded or manually-constructed contract inputs

### Why it exists

`LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`
already fixed:

- one admitted validated specimen contributes one exact materialization-attempt input tuple
- one admitted validated specimen contributes one exact materialization-attempt output-boundary
  shape
- preserved receipt-bound identity and lineage stay frozen through:
  - `lane_ordinal`
  - `specimen_ordinal`
  - `artifact_id`
  - `anchored_bc_specimen_file_path`
  - `source_raw_state_window_ref`
  - `source_slice_id`
  - `source_replay`
  - `source_subject`
  - `source_phase_id`
- deferred observation lineage stays preserved only through:
  - `observation_binding_kind`
  - `accepted_reference_window`

What was still missing was the first truthful result surface above that contract:

- can the repo currently realize any actual raw-state payload access without replay parsing, or
  can it only emit a truthful non-materialized attempt result?

### How it differs from the materialization contract-definition boundary below it

- The lower boundary defines what an admitted attempt is allowed to consume and expose.
- This pass defines what the repo can currently realize from that admitted attempt.
- The lower boundary is contract-only.
- This pass is still bounded realization, but it remains below replay parsing and below
  tensor/control materialization.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this realization version.

This realization boundary remains family-specific because:

- the admitted input is one low-boost-recovery-specific materialization contract only
- the admitted specimen view is one low-boost-recovery BC materialization-attempt boundary only
- the remaining opaque handle is the family-specific BC field `source_raw_state_window_ref`
- no second family exists that would justify a shared raw-state materialization realization
  abstraction

No generic all-family raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`
- the audited family root directory reference already preserved by that contract

Within `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_validation_disposition`
- `source_validation_notes`
- `source_reopen_decision_disposition`
- `source_reopen_decision_notes`
- `source_chosen_locator_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `admitted_validated_specimen`
- each `materialization_attempt_input`
- each `materialization_attempt_output_boundary`
- `contract_disposition`
- `contract_notes`
- `chosen_materialization_contract_shape`

Direct input is no longer:

- validation results
- raw-state materialization reopen-decision results
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

Those lower layers remain frozen. This pass starts strictly from the materialization contract plus
the preserved audited family root directory reference already carried by that contract.

## D. REALIZATION ROLE

This realization boundary owns exactly one thing:

- determining the first truthful result shape for one admitted receipt-bound raw-state
  materialization attempt without inventing replay parsing or raw-state payload semantics

This pass is allowed to realize only:

- preserved contract identity and lineage
- one per-specimen attempt result surface
- one explicit statement that the current repo can only emit a truthful non-materialized attempt
  result

This pass is not allowed to realize yet:

- replay parsing
- raw-state-window frames
- raw-state payload bytes or structured payloads
- any storage mapping from `source_raw_state_window_ref` to replay content
- observation tensors
- control/action payloads
- sidecars or manifests
- generic indexes
- `mimir_export` outputs

## E. MATERIALIZATION-ATTEMPT REALIZATION SHAPE V1

### Exact realization types

This pass defines:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationError`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_materialization_attempt_v1(...)`

### Exact per-specimen contract input consumed

For one admitted specimen, this realization pass consumes exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptInputV1`
- the corresponding admitted-specimen identity/lineage view already frozen by the contract
- the corresponding
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptOutputBoundaryV1`

### Exact truthful attempt-result decision

The current implementation can only emit:

- a truthful non-materialized attempt result

It does **not** emit:

- a raw-state payload
- a parsed replay-frame window
- a narrowed successful raw-state access result

That decision is exact because:

- `source_raw_state_window_ref` still remains an opaque linkage handle
- the audited family root is still only a BC specimen-tree anchor
- no repo-local contract maps that opaque handle to a concrete raw-state payload source above this
  boundary
- replay parsing remains deferred and forbidden in this pass

### Exact per-specimen attempt result

For one admitted specimen, the realization result preserves:

- `specimen_ordinal`
- the consumed materialization-attempt input unchanged
- the preserved materialization-attempt output boundary unchanged
- `materialization_attempt_disposition ==
  RealizedForTruthfulNonMaterializedAttemptOnly`

### Identity checks that must still hold

This realization boundary must keep all of the following exact for each specimen:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`

The output-boundary preservation checks must also remain exact for:

- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`

### What it explicitly refuses to promise

This pass refuses to promise:

- that raw state has been located
- that raw state has been materialized
- that `source_raw_state_window_ref` now resolves to replay storage
- that replay parsing is available
- that tensors or controls exist
- that a useful learning signal has been proven

## F. REALIZATION OUTPUT V1

The minimum family-specific realization result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_contract_disposition`
- preserved `source_contract_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane/specimen results
- chosen `realization_disposition`
- bounded `realization_notes`
- preserved `chosen_materialization_contract_shape`

Each preserved specimen result contains exactly:

- preserved `specimen_ordinal`
- preserved consumed materialization-attempt input
- preserved materialization-attempt output boundary
- one truthful non-materialized attempt disposition

The exact realization disposition is:

- `RealizedForTruthfulNonMaterializedAttemptOnly`

The exact realization notes are:

- `ReceiptBoundValidatedSpecimenFileMaterializationContractBoundaryPreserved`
- `ContractInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreserved`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceRawStateWindowRefRemainsOpaqueMaterializationReferenceOnly`
- `TruthfulNonMaterializedAttemptResultOnly`
- `ReplayParsingStillDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The materialization contract may enter this realization boundary only when all of the following
hold:

1. the admitted input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`
2. `source_validation_disposition ==`
   `ValidatedForReceiptBoundBcSpecimenFileExistenceAndIdentityPreservingReadbackOnly`
3. `source_validation_notes` remain the exact frozen validation note set
4. `source_reopen_decision_disposition ==`
   `ReopenJustifiedForReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationContract`
5. `source_reopen_decision_notes` remain the exact frozen reopen-decision note set
6. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
7. `contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptOnly`
8. `contract_notes` remain the exact frozen contract note set
9. `chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
10. `specimen_count > 0`
11. `group_count > 0`
12. `group_count` equals the number of preserved ordered lane results
13. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
14. `audited_family_root_directory` still exists and is a directory at realization time
15. lane order and specimen order remain exact
16. every `anchored_bc_specimen_file_path` remains receipt-bound below
    `audited_family_root_directory`
17. admitted specimen identity and lineage still match the preserved materialization-attempt input
18. preserved output-boundary identity and deferred observation lineage still match the admitted
    specimen and the preserved materialization-attempt input

Admission here means only:

- the repo may emit one truthful non-materialized attempt result surface

Admission here does not mean:

- raw-state materialization exists
- replay parsing exists
- tensors or controls are available
- `mimir_export` may be widened

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded contract input
- mismatched counts
- mismatched audited family root
- lane/specimen order drift
- artifact-id drift
- anchored path drift outside the audited family root
- any mismatch between admitted specimen identity and preserved materialization-attempt input
- any mismatch between preserved materialization-attempt input and preserved output boundary
- any attempt to reinterpret the audited family root as raw-state storage
- any attempt to widen this boundary into replay parsing
- any attempt to widen this boundary into tensor/control materialization

This v1 boundary is intentionally strict:

- no repair
- no specimen skipping
- no resorting
- no guessed raw-state source recovery
- no replay-path guessing
- no payload synthesis
- no sidecar/manifest/index fallback

## I. NON-GOALS

This pass does not do any of the following:

- no replay parsing implementation
- no raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no sidecar/manifest realization
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- one explicit truthful result surface exists above the raw-state materialization contract
- one admitted specimen now yields one exact non-materialized materialization-attempt result
- preserved receipt-bound identity and lineage remain visible without inventing raw-state payload
  semantics
- the audited family root remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual raw-state access
- replay-frame access
- raw-state-window payload materialization
- tensor/control materialization

The immediate next pass should now be:

- a replay-parsing reopen decision above this truthful non-materialized attempt result

That next pass is now obvious because the current realization boundary proves the remaining gap is
no longer contract shape. The remaining gap is whether the project must deliberately reopen replay
parsing to supply a truthful raw-state source for `source_raw_state_window_ref`.
