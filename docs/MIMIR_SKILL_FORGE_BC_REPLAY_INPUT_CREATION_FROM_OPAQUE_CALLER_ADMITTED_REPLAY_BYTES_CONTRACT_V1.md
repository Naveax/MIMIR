# MIMIR Skill Forge BC ReplayInput Creation From Opaque Caller-Admitted Replay Bytes Contract v1

## A. PURPOSE

This pass owns exactly one narrow contract-definition boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationResultV1`

It defines the first low-boost-recovery-specific bridge toward:

- `mimir_replay::ReplayInput`

This pass exists because a new explicit external architecture/product requirement reopens exactly one previously closed domain:

- `mimir_replay::ReplayInput` creation from already-realized opaque caller-admitted replay bytes

This is not justified by repo-only evidence. The prior audited prioritization selected Outcome A and no domain because the repo-only chain did not uniquely justify parser, locator, carrier, actual-materialization, raw-state parsing, `ReplayInput`, or export widening as the next closed domain. This pass intentionally imposes `ReplayInput` creation as the chosen domain by external requirement.

This pass does not claim replay parsing, parser success, replay-source actual-materialization implementation success, replay-source carrier discovery, replay-input locator success, raw-state payload parsing, or `mimir_export` readiness.

## B. FAMILY SCOPE

The only supported family is:

- `low_boost_recovery`

This remains family-specific because the consumed realization result, receipt tuple, accepted reference window, opaque bytes, and deferred replay/materialization lineage are all low-boost-recovery BC surfaces.

No generic all-family replay/raw-state/index/export/materialization framework is introduced.

## C. INPUT BOUNDARY

This pass consumes exactly two inputs:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationResultV1`
- the explicit external requirement choosing `mimir_replay::ReplayInput` creation as the next reopened domain

From the realized consumer-intake result, this boundary consumes:

- `specimen_count`
- `group_count`
- source consumer-intake contract disposition and notes
- audited family root directory as a BC specimen-tree receipt anchor only
- source consumer-intake realization disposition and notes
- chosen consumer-intake contract shape
- ordered lane/specimen realization results
- each consumed consumer-intake boundary input
- each preserved consumer-intake output boundary
- each per-specimen consumer-intake realization disposition

Older blocked/deferred replay-input locator, parser, replay-source, sidecar, manifest, raw-state, and export surfaces are not direct proof and are not direct input to this boundary.

`source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` remain lineage/receipt anchors only. They are not replay paths, replay storage roots, locator inputs, or parser-readiness proof.

## D. CONTRACT ROLE

This contract owns only:

- revalidating the realized opaque caller-admitted replay-byte consumer-intake result
- preserving the exact low-boost-recovery receipt-bound tuple
- preserving the exact opaque replay-byte payload
- defining one exact `mimir_replay::ReplayInput` creation bridge
- creating only a memory-backed `mimir_replay::ReplayInput` from the preserved opaque bytes

This contract is allowed to create:

- `mimir_replay::ReplayInput::Memory { label, bytes }`

The label is deterministic receipt metadata only. The bytes are a byte-for-byte clone of the preserved opaque caller-admitted replay bytes.

This contract is not allowed to:

- implement replay-source actual-materialization
- discover replay-source carriers
- locate replay inputs
- derive replay paths
- parse replay bytes
- define parser-success logic
- parse raw-state payloads
- create tensor/control materialization
- ingest a corpus
- widen `mimir_export`

Creating `ReplayInput::Memory` here does not prove that a parser can read the bytes.

## E. EXACT CONTRACT SHAPE V1

### Contract Name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesContractV1`

### Contract-Shape Enum

- `LowBoostRecoveryBcReplayInputCreationFromOpaqueCallerAdmittedReplayBytesContractShapeV1`
- exact chosen value:
  `ReceiptBoundMimirReplayMemoryInputCreationFromOpaqueCallerAdmittedReplayBytesOnly`

### Bridge-Kind Enum

- `LowBoostRecoveryBcReceiptBoundReplayInputCreationFromOpaqueCallerAdmittedReplayBytesBridgeKindV1`
- exact bound value:
  `MimirReplayMemoryInputFromOpaqueCallerAdmittedReplayBytesOnly`

### Exact ReplayInput-Creation Bridge Object Shape

The exact bridge object is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesBridgeV1`

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
- `replay_input_creation_bridge_kind`
- `created_replay_input`

### Exact Contract Boundary Input Tuple

For one specimen, the boundary input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesBoundaryInputV1`

It is derived only from the realized consumer-intake boundary input and preserves:

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

### Exact Contract Boundary Output Tuple

For one specimen, the boundary output is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesOutputBoundaryV1`

It preserves the input tuple and adds only:

- `bound_replay_input_creation_bridge_kind`
- `created_replay_input`

### Exact ReplayInput Creation Semantics

The created `mimir_replay::ReplayInput` must be:

- `ReplayInput::Memory { label, bytes }`

The exact label format is:

- `low_boost_recovery_bc_v1:replay_input:artifact:{artifact_id}:lane:{lane_ordinal}:specimen:{specimen_ordinal}`

The exact byte rule is:

- `bytes == opaque_caller_admitted_replay_bytes`

No path is derived. No file-backed `ReplayInput` is created. `source_replay.provenance_label` is not used as a path or storage locator. `audited_family_root_directory` is not used as replay storage.

### Exact Binding Statement

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

binds to exactly one ReplayInput-creation bridge:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesBridgeV1`

That bridge binds the tuple to exactly one memory-backed `mimir_replay::ReplayInput`.

It does not mean:

- replay parsing
- parser success
- replay-source carrier discovery
- replay-source actual-materialization implementation
- replay path resolution
- replay-input locator success
- raw-state payload parsing
- export integration

## F. CONTRACT OUTPUT V1

The contract-definition result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesContractV1`

It preserves:

- `specimen_count`
- `group_count`
- source consumer-intake contract disposition and notes
- audited family root directory as receipt anchor only
- source consumer-intake realization disposition and notes
- chosen consumer-intake contract shape
- ordered lane/specimen structure
- each consumed consumer-intake boundary input
- each preserved consumer-intake output boundary
- each per-specimen consumer-intake realization disposition

It adds only:

- one per-specimen ReplayInput-creation boundary input
- one per-specimen ReplayInput-creation boundary output
- one per-specimen ReplayInput-creation bridge object
- top-level contract disposition
- top-level contract notes
- chosen ReplayInput-creation contract shape

The exact top-level disposition is:

- `ContractDefinedForReceiptBoundReplayInputCreationFromOpaqueCallerAdmittedReplayBytesOnly`

## G. ADMISSION RULES

A realized consumer-intake result may enter this boundary only when all conditions hold:

1. the input is exactly `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationResultV1`
2. the source consumer-intake contract disposition and notes remain exact
3. the source consumer-intake realization disposition and notes remain exact
4. the chosen consumer-intake contract shape remains exact
5. `specimen_count > 0`
6. `group_count > 0`
7. `group_count` equals ordered lane count
8. each lane remains non-empty
9. lane and specimen ordinals match concrete order
10. every artifact id remains unique
11. the audited family root exists, is a directory, and ends in `low_boost_recovery_bc_v1`
12. each anchored specimen path remains below the audited family root and is not the root itself
13. each accepted reference window remains valid and bounded
14. each opaque byte payload remains non-empty
15. each preserved replay-input-locator handle kind remains `FutureParserConsumableReplayHandleOnly`
16. each preserved replay-source-materialization requirement kind remains `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`
17. each preserved replay-source-actual-materialization handle kind remains `FutureExplicitReplaySourceCarrierOnly`
18. each preserved carrier-provenance/source-binding handle kind remains `FutureExplicitReplaySourceCarrierProvenanceBindingOnly`
19. each preserved explicit-admission kind remains `FutureAdmittedExplicitReplaySourceCarrierProvenanceSourceBindingOnly`
20. each consumer-intake output boundary exactly matches its input plus the consumer-intake kind

Admission means only that the exact bridge may create `ReplayInput::Memory` from the preserved opaque bytes.

## H. FAILURE RULES

This boundary hard-fails for:

- degraded source consumer-intake contract notes
- degraded source consumer-intake realization notes
- disposition drift
- chosen-shape drift
- count drift
- empty lanes
- lane/specimen order drift
- duplicate artifact ids
- audited-root drift
- specimen path drift outside the audited root
- accepted-window invalidity
- empty opaque byte payloads
- preserved handle-kind drift
- consumer-intake input/output drift
- any file-backed ReplayInput creation attempt
- any attempt to reinterpret `source_replay` as a replay path
- any attempt to reinterpret `source_replay.provenance_label` as a replay path
- any attempt to reinterpret `audited_family_root_directory` as replay storage
- any replay parsing, parser-success, raw-state parsing, locator, carrier-discovery, actual-materialization implementation, or export widening attempt

There is no repair behavior:

- no specimen skipping
- no lane resorting
- no byte synthesis
- no path guessing
- no sidecar or manifest fallback

## I. NON-GOALS

This pass does not implement:

- replay-source actual-materialization
- replay-source carrier discovery
- replay-input locator logic
- actual replay parsing
- parser-success logic
- raw-state payload parsing
- corpus-wide replay ingestion
- real rollout physics
- async/background systems
- database code
- runtime CLI commands
- execution-result cleanup changes
- `mimir_export` integration or widening
- generic all-family replay/raw-state/index/export/materialization infrastructure

This pass also does not modify `mimir-replay`, `mimir-io`, `mimir-export`, or `mimir-types`.

## J. RELATION TO NEXT STAGES

This pass guarantees only:

- the chain was reopened by explicit external requirement, not repo-only proof
- one exact low-boost-recovery ReplayInput-creation contract exists
- the exact receipt-bound tuple is revalidated
- opaque caller-admitted replay bytes are preserved byte-for-byte
- one exact memory-backed `mimir_replay::ReplayInput` creation bridge is defined
- the bridge remains below replay parsing, parser success, raw-state payload parsing, replay-source carrier discovery, replay-input locator logic, and `mimir_export`

This pass still does not guarantee:

- parser readiness
- replay parsing success
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator success
- raw-state payload availability
- export readiness

The immediate next pass is:

- the first realization pass for this exact ReplayInput-creation contract

`mimir_export` widening remains forbidden unless explicitly reopened.
