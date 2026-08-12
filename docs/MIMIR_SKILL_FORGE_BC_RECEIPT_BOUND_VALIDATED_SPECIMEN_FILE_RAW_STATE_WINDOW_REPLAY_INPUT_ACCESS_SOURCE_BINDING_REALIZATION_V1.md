# MIMIR Skill Forge BC Receipt-Bound Validated Specimen-File Raw-State Window Replay-Input-Access Source-Binding Realization v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual replay-input-access / replay-source-binding realization boundary
above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`

It defines:

- the first truthful realized result surface above the replay-input-access / replay-source-binding
  contract
- the narrowest honest per-specimen replay-input-access / replay-source-binding result the current
  repo can emit
- the exact admission and failure rules for realizing that result

### Why it exists

The contract boundary below this pass already fixed:

- one admitted specimen yields one exact replay-input-access / replay-source-binding boundary input
  tuple
- one admitted specimen yields one exact replay-input-access / replay-source-binding output
  boundary
- the only admitted output-side handle kind is
  `FutureParserConsumableReplayHandleOnly`

What was still missing was the first truthful realized result above that contract:

- can the repo currently realize any actual replay-input-access result without locator or parser
  implementation, or can it only emit a truthful non-located / non-parsed result?

### How it differs from the replay-input-access / replay-source-binding contract-definition boundary below it

- The lower boundary defines the contract shape only.
- This pass realizes the first truthful result above that contract.
- The lower boundary introduces one contract-only future replay-handle kind.
- This pass states what the repo can honestly realize from that contract today.
- Neither boundary implements replay-input locator logic or replay parsing.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this realization version.

This realization boundary remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`
- the preserved lineage tuple and deferred observation lineage are the low-boost-recovery BC
  specimen fields already carried by that contract
- no second family exists that would justify a generic replay-input-access / replay-source-binding
  realization framework

No generic multi-family replay/raw-state/index/export/materialization framework is introduced
here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`
- the audited family root directory reference already preserved by that contract

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`,
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
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `admitted_replay_side_parse_attempt_input`
- each `admitted_replay_side_parse_attempt_output_boundary`
- each `replay_input_access_source_binding_boundary_input`
- each `replay_input_access_source_binding_output_boundary`
- `contract_disposition`
- `contract_notes`
- `chosen_replay_input_access_contract_shape`

The following are no longer direct input at this boundary:

- blocked replay-side parse-attempt results
- replay-input-access reopen decisions
- parse-attempt contract results
- materialization-attempt realization results
- replay-parsing reopen decisions
- replay-parsing-success reopen decisions
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

Those lower layers remain frozen. This pass starts strictly from the replay-input-access /
replay-source-binding contract and the already-preserved audited family root reference.

## D. REALIZATION ROLE

This realization owns exactly one thing:

- realizing the first honest replay-input-access / replay-source-binding result for one admitted
  contract specimen

This pass is allowed to realize only:

- preserved receipt-bound specimen identity and lineage
- the admitted replay-input-access / replay-source-binding boundary input tuple
- the admitted replay-input-access / replay-source-binding output boundary
- one truthful bounded non-located / non-parsed disposition above that contract

This pass is not allowed to realize:

- replay-input locator implementation
- replay file discovery
- replay file paths
- replay bytes
- replay frames
- replay parsing success
- raw-state payload materialization
- tensor payloads
- control/action payloads
- sidecars
- manifests
- generic indexes
- `mimir_export` outputs

## E. REPLAY-INPUT-ACCESS / SOURCE-BINDING REALIZATION SHAPE V1

### Exact realization types

This pass defines exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingRealizationError`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_input_access_source_binding_v1(...)`

### Exact per-specimen contract input consumed

For one admitted specimen, this realization consumes exactly:

- `replay_input_access_source_binding_boundary_input:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingBoundaryInputV1`
- `replay_input_access_source_binding_output_boundary:
  LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingOutputBoundaryV1`

Those fields are consumed from the admitted contract result. They are not recomputed from lower
layers.

### Exact truthful realization decision

The current implementation can only emit:

- one truthful non-located / non-parsed replay-input-access / replay-source-binding result

The exact disposition is:

- `RealizedForTruthfulNonLocatedReplayInputAccessSourceBindingOnly`

That is the narrowest honest result because the admitted contract still exposes only:

- preserved receipt-bound lineage
- one contract-only handle kind,
  `FutureParserConsumableReplayHandleOnly`

The current repo therefore cannot honestly claim any narrower successful replay-input-access
result because:

- the admitted contract does not carry a replay file path
- the admitted contract does not carry replay bytes
- the admitted contract does not carry replay frames
- `source_replay` remains opaque lineage only
- the audited family root may not be reinterpreted as replay storage
- the contract handle kind remains a contract-only future handle requirement, not a realized
  locator result

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

- the admitted replay-side parse-attempt input
- the admitted replay-side parse-attempt output boundary
- the replay-input-access / replay-source-binding boundary input
- the replay-input-access / replay-source-binding output boundary
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

The minimum family-specific replay-input-access / replay-source-binding realization result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingRealizationResultV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_contract_disposition`
- preserved `source_contract_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `source_chosen_materialization_contract_shape`
- preserved `source_chosen_replay_parsing_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane results
- preserved lane order
- preserved specimen order
- preserved artifact ids
- preserved per-specimen replay-input-access / replay-source-binding results
- bounded `realization_disposition`
- bounded `realization_notes`
- preserved `chosen_replay_input_access_contract_shape`

Each per-specimen result contains exactly:

- `specimen_ordinal`
- `consumed_replay_input_access_source_binding_boundary_input`
- `preserved_replay_input_access_source_binding_output_boundary`
- `replay_input_access_source_binding_disposition`

The exact top-level disposition is:

- `RealizedForTruthfulNonLocatedReplayInputAccessSourceBindingOnly`

The exact note set is:

- `ReplayInputAccessSourceBindingContractBoundaryPreserved`
- `ContractInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `AnchoredBcSpecimenFilePathsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `ReceiptBoundSourceLineagePreservedForNonLocatedReplayInputAccessSourceBindingOnly`
- `ObservationBindingKindAndAcceptedReferenceWindowPreservedForDeferredObservationAccess`
- `SourceReplayReferenceRemainsOpaqueLineageOnly`
- `FutureParserConsumableReplayHandleKindPreservedWithoutLocatorRealization`
- `TruthfulNonLocatedReplayInputAccessSourceBindingResultOnly`
- `ReplayInputLocatorImplementationStillDeferred`
- `ReplayParsingStillDeferred`
- `ActualRawStatePayloadMaterializationDeferred`
- `TensorAndControlMaterializationStillDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The replay-input-access / replay-source-binding contract may enter this realization boundary only
when all of the following hold:

1. the input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`
2. `source_realization_disposition == RealizedForTruthfulBlockedReplaySideParseAttemptOnly`
3. `source_realization_notes` remain the exact frozen blocked replay-side parse-attempt
   realization note set
4. `source_reopen_decision_disposition ==`
   `ReopenJustifiedForReceiptBoundReplayInputAccessSourceBindingContract`
5. `source_reopen_decision_notes` remain the exact frozen replay-input-access reopen note set
6. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
7. `source_chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
8. `source_chosen_replay_parsing_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
9. `contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingOnly`
10. `contract_notes` remain the exact frozen replay-input-access / replay-source-binding contract
    note set
11. `chosen_replay_input_access_contract_shape == ReceiptBoundReplayInputAccessSourceBindingOnly`
12. `specimen_count > 0`
13. `group_count > 0`
14. `group_count` equals the number of preserved ordered lane results
15. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
16. `audited_family_root_directory` still exists and is a directory at realization time
17. lane order and specimen order remain exact
18. every `anchored_bc_specimen_file_path` remains receipt-bound below
    `audited_family_root_directory`
19. every admitted replay-side parse-attempt output boundary still matches the admitted
    replay-side parse-attempt input on the preserved identity tuple
20. every replay-input-access / replay-source-binding boundary input still matches the admitted
    replay-side parse-attempt identity tuple and deferred observation lineage
21. every replay-input-access / replay-source-binding output boundary still matches the boundary
    input on the preserved identity tuple and deferred observation lineage
22. every replay-input-access / replay-source-binding output boundary still preserves
    `bound_replay_input_access_source_binding_handle_kind ==
    FutureParserConsumableReplayHandleOnly`

Admission here means only:

- the repo may realize one truthful non-located / non-parsed replay-input-access /
  replay-source-binding result above the admitted contract

Admission here does not mean:

- replay-input access succeeds
- replay-input locator logic exists
- replay parsing succeeds
- replay files or bytes are available
- raw-state payload exists
- tensors or controls exist

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded contract input
- mismatched counts/root/order/artifact ids
- any drift between admitted replay-side parse-attempt identity and replay-input-access /
  replay-source-binding identity
- any attempt to reinterpret `source_replay` or `provenance_label` as an implicit replay locator
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen into actual replay-input locator implementation
- any attempt to widen into actual replay parsing
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

- one explicit replay-input-access / replay-source-binding realization result exists above the
  contract
- that result is truthful about the current non-located / non-parsed state
- preserved receipt-bound identity and deferred observation lineage remain visible without
  inventing replay storage, replay bytes, or replay payload semantics
- the contract-only future parser-consumable replay-handle kind remains visible without being
  overstated as actual locator success
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual replay-input access
- actual replay-input location
- actual replay parsing
- replay bytes or replay frames
- actual raw-state-window payload materialization
- tensor/control materialization

The immediate next pass should be:

- a replay-input locator reopen decision above this truthful non-located
  replay-input-access / replay-source-binding realization result

That next pass should consume:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingRealizationResultV1`

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- implement replay-input locator logic directly
- implement replay parsing
- implement raw-state payload materialization
- implement tensor/control materialization
- add sidecars/manifests unless separately proven necessary
