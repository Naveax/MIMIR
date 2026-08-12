# MIMIR Skill Forge BC Opaque Caller-Admitted Replay-Byte Handoff Contract v1

## A. PURPOSE

### What this pass owns

This pass owns exactly one contract-definition boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationResultV1`

It defines exactly one new family-specific handoff seam in `mimir-skill`:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractV1`

It freezes only:

- one exact opaque caller-admitted replay-byte handoff contract
- one exact opaque handoff object shape
- one exact receipt-bound binding from the frozen tuple to that handoff object shape
- one exact bounded contract result above the truthful byte-backed caller-admitted realization

### Why it exists

The prior truthful realization now proves one narrow thing:

- non-empty caller-admitted replay bytes are already bound to the exact frozen low-boost-recovery receipt tuple

That realization still stops below:

- replay-source carrier discovery
- replay-input locator logic
- replay parsing
- `mimir_replay::ReplayInput`

This pass exists to define the next honest boundary above that realization while keeping those bytes opaque and while refusing to reinterpret lineage fields as replay storage or replay paths.

### How it differs from the byte-backed caller-admitted source-form realization below it

The lower realization proves caller-byte admission only.

This pass does not re-prove caller admission and does not parse anything.

Instead it freezes:

- one exact opaque replay-byte handoff boundary
- one exact opaque replay-byte handoff object shape
- one exact bounded contract result for that handoff

The lower realization is therefore the source of truth for admitted bytes.

This pass is the contract-definition boundary that preserves those already-admitted bytes as opaque payload below `mimir_replay::ReplayInput`.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This remains family-specific because:

- the consumed realization result is low-boost-recovery-specific
- the preserved receipt tuple is the low-boost-recovery BC specimen tuple already frozen below
- the preserved observation and deferred replay/materialization lineage are the low-boost-recovery BC lineage already carried below
- no second family exists that justifies a generic replay/raw-state/index/export/materialization opaque-handoff framework

No generic all-family replay/raw-state/index/export/materialization handoff framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationResultV1`

From that realization result, this pass consumes exactly:

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
- `source_chosen_replay_source_actual_materialization_contract_shape`
- `source_chosen_replay_source_actual_materialization_carrier_provenance_binding_contract_shape`
- `source_chosen_replay_source_actual_materialization_explicit_carrier_provenance_source_binding_admission_contract_shape`
- `source_realization_disposition`
- `source_realization_notes`
- `realization_disposition`
- `realization_notes`
- `chosen_replay_source_actual_materialization_byte_backed_caller_admitted_source_form_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each preserved byte-backed boundary input/output pair
- each preserved realized byte-backed caller-admitted source-form object
- each preserved byte-backed realization disposition

Lower contract, reopen, and realization layers are no longer direct input here.

They matter only through the already-preserved low-boost-recovery realization result that this pass consumes.

## D. CONTRACT ROLE

This contract owns exactly one thing:

- freezing one exact opaque caller-admitted replay-byte handoff contract for the already-admitted low-boost-recovery receipt tuple

This contract is allowed to bind only:

- preserved receipt-bound specimen identity
- preserved source lineage
- preserved observation lineage
- preserved replay/materialization handle lineage
- preserved explicit-admission lineage
- already-admitted caller bytes carried only as opaque payload
- one exact opaque replay-byte handoff object shape

This contract is not allowed to implement, discover, locate, parse, or materialize:

- replay-source actual-materialization
- replay-source carrier discovery
- replay-input locator logic
- replay path derivation
- replay parsing
- raw-state payload parsing
- tensor/control materialization
- corpus ingestion
- `mimir_export` integration
- `mimir_replay::ReplayInput`

This contract stays below `mimir_replay::ReplayInput` and below `mimir_export`.

## E. EXACT CONTRACT SHAPE V1

### Contract name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractV1`

### Exact contract-shape enum

- `LowBoostRecoveryBcReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractShapeV1`
- exact chosen shape:
  `ReceiptBoundReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffOnly`

### Exact handoff kind enum

- `LowBoostRecoveryBcReceiptBoundReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffKindV1`
- exact bound kind:
  `OpaqueCallerAdmittedReplayBytesBelowReplayInputOnly`

### Exact contract boundary input tuple

For one specimen, the contract boundary input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffBoundaryInputV1`

It preserves exactly:

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
- `preserved_replay_source_actual_materialization_handle_kind`
- `preserved_replay_source_actual_materialization_carrier_provenance_binding_handle_kind`
- `preserved_explicit_replay_source_carrier_provenance_source_binding_admission_kind`
- `opaque_caller_admitted_replay_bytes`

That tuple is derived only from the realized byte-backed caller-admitted source-form object already preserved by the truthful realization result.

### Exact contract boundary output tuple

For one specimen, the contract boundary output is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffOutputBoundaryV1`

It preserves the exact same tuple and adds only:

- `bound_opaque_caller_admitted_replay_byte_handoff_kind`

That bound kind means only:

- the opaque replay-byte handoff boundary is now frozen for this exact receipt tuple
- the opaque bytes remain below `mimir_replay::ReplayInput`
- the bytes remain opaque and unparsed

It does not mean:

- replay parsing
- replay-source carrier discovery
- replay path resolution
- replay-input locator success
- `mimir_replay::ReplayInput` creation

### Exact handoff object shape

The exact opaque handoff object is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffV1`

It carries exactly:

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
- `preserved_replay_source_actual_materialization_handle_kind`
- `preserved_replay_source_actual_materialization_carrier_provenance_binding_handle_kind`
- `preserved_explicit_replay_source_carrier_provenance_source_binding_admission_kind`
- `opaque_caller_admitted_replay_bytes`

### How opaque replay bytes are carried

Opaque replay bytes are carried only as:

- `opaque_caller_admitted_replay_bytes: Vec<u8>`

Those bytes are:

- already caller-admitted
- preserved as opaque payload only
- not replay parsing success
- not replay-source actual-materialization success beyond opaque byte preservation
- not replay-input locator success
- not `mimir_replay::ReplayInput`

### How receipt-bound identity is carried

Receipt-bound identity is carried directly through:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`

### How preserved lineage is carried

Preserved lineage is carried directly through:

- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`
- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`
- `preserved_replay_input_locator_handle_kind`
- `preserved_replay_source_materialization_requirement_kind`
- `preserved_replay_source_actual_materialization_handle_kind`
- `preserved_replay_source_actual_materialization_carrier_provenance_binding_handle_kind`
- `preserved_explicit_replay_source_carrier_provenance_source_binding_admission_kind`

### Exact binding statement

For one specimen, the exact preserved tuple:

- `artifact_id`
- `lane_ordinal`
- `specimen_ordinal`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`
- preserved observation binding
- preserved accepted reference window
- preserved replay-input-locator handle kind
- preserved replay-source-materialization requirement kind
- preserved replay-source-actual-materialization handle kind
- preserved carrier-provenance/source-binding handle kind
- preserved explicit-admission kind
- opaque caller-admitted replay bytes

binds to exactly one opaque replay-byte handoff contract/object family:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffV1`

That binding does not mean:

- replay parsing
- replay-source carrier discovery
- replay path
- replay file location
- replay-input locator success
- replay-source actual-materialization success
- `mimir_replay::ReplayInput`

### Exact opacity rules

`source_replay` remains opaque lineage only.

`source_replay.provenance_label` remains opaque lineage only and is not a replay path contract.

`audited_family_root_directory` remains only a BC specimen-tree anchor and is not replay storage.

## F. CONTRACT OUTPUT V1

The minimum contract-definition result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractV1`

It preserves exactly:

- specimen and lane counts
- the immediate byte-backed caller-admitted source-form contract disposition and note set
- the lower chosen shapes already frozen below
- the lower explicit-admission realization disposition and note set already preserved by the consumed realization result
- the immediate byte-backed caller-admitted source-form realization disposition and note set
- the audited family root directory
- ordered lane/specimen structure
- artifact ids
- the realized byte-backed caller-admitted source-form objects

It adds only:

- one per-specimen opaque replay-byte handoff boundary input/output pair
- one per-specimen opaque replay-byte handoff object
- bounded `contract_disposition`
- bounded `contract_notes`
- `chosen_replay_source_actual_materialization_opaque_caller_admitted_replay_byte_handoff_contract_shape`

The exact top-level disposition is:

- `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffOnly`

## G. ADMISSION RULES

The byte-backed caller-admitted realization result may enter this contract-definition boundary only when all of the following hold:

1. the input remains exactly `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationResultV1`
2. the immediate byte-backed caller-admitted source-form contract disposition remains frozen
3. the immediate byte-backed caller-admitted source-form contract notes remain exact
4. the lower chosen shapes remain the exact frozen receipt-bound shapes
5. the lower explicit-admission realization disposition and notes still remain the exact preserved lineage carried by the consumed realization result
6. the immediate byte-backed caller-admitted source-form realization disposition remains the truthful byte-backed realization disposition
7. the immediate byte-backed caller-admitted source-form realization notes remain exact
8. the immediate byte-backed caller-admitted source-form chosen shape remains the exact frozen chosen shape
9. `specimen_count > 0`
10. `group_count > 0`
11. `group_count` equals the number of preserved ordered lane results
12. `audited_family_root_directory` still exists, is still a directory, and still ends in `low_boost_recovery_bc_v1`
13. lane order and specimen order still match concrete position
14. each anchored specimen path still remains receipt-bound below the audited family root
15. each accepted reference window still remains valid and bounded
16. each preserved replay-input-locator handle kind still remains `FutureParserConsumableReplayHandleOnly`
17. each preserved replay-source-materialization requirement kind still remains `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`
18. each preserved replay-source-actual-materialization handle kind still remains `FutureExplicitReplaySourceCarrierOnly`
19. each preserved carrier-provenance/source-binding handle kind still remains `FutureExplicitReplaySourceCarrierProvenanceBindingOnly`
20. each preserved explicit-admission kind still remains `FutureAdmittedExplicitReplaySourceCarrierProvenanceSourceBindingOnly`
21. each preserved byte-backed caller-admitted source-form object still matches the exact frozen byte-backed boundary output
22. each preserved byte payload is still non-empty
23. every artifact id remains unique

Admission here means only:

- the byte-backed realization may be revalidated
- the exact opaque handoff boundary may be frozen
- the exact opaque handoff object shape may be frozen while keeping the bytes opaque

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded source contract notes
- degraded source realization notes
- degraded immediate byte-backed realization notes
- chosen-shape drift
- disposition drift
- mismatched counts
- mismatched lane order
- mismatched specimen order
- duplicate artifact ids
- audited root drift
- specimen path drift outside the audited root
- accepted-window invalidity
- any drift in the preserved tuple fields
- any drift in the preserved explicit-admission kind
- empty preserved byte payloads
- any attempt to reinterpret `source_replay` as replay path or replay storage
- any attempt to reinterpret `source_replay.provenance_label` as replay path
- any attempt to reinterpret `audited_family_root_directory` as replay storage
- any attempt to widen this pass into replay-source actual-materialization implementation
- any attempt to widen this pass into replay-source carrier discovery
- any attempt to widen this pass into replay-input locator logic
- any attempt to widen this pass into replay parsing
- any attempt to widen this pass into raw-state payload parsing or tensor/control materialization

This v1 boundary is intentionally strict:

- no repair
- no specimen skipping
- no resorting
- no replay-path guessing
- no byte synthesis
- no sidecar or manifest fallback

## I. NON-GOALS

This pass does not do any of the following:

- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- replay parsing
- raw-state payload parsing
- tensor/control materialization
- `mimir_export` integration
- `mimir_replay::ReplayInput` creation
- replay-input or export framework widening
- generic all-family opaque handoff infrastructure

It also does not add:

- parser-success logic
- corpus-wide replay ingestion
- real rollout physics
- async/background systems
- database code
- runtime CLI work

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- one exact opaque caller-admitted replay-byte handoff contract exists in `mimir-skill`
- one exact opaque replay-byte handoff object shape exists
- the exact preserved low-boost-recovery receipt tuple that the opaque bytes bind to is frozen
- the bytes remain opaque payload only
- the contract remains low-boost-recovery-specific
- the contract remains receipt-bound
- the contract remains below `mimir_replay::ReplayInput`
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- replay-source actual-materialization success
- replay-source carrier discovery success
- replay-input locator success
- replay parsing success
- raw-state payload materialization
- tensor/control materialization
- `mimir_replay::ReplayInput`

The immediate next pass is now:

- the first realization pass for this exact opaque caller-admitted replay-byte handoff contract

That next pass must still keep:

- `mimir_export` widening forbidden unless explicitly reopened
- replay parsing deferred unless separately reopened
- replay-input locator logic deferred unless separately reopened
