# MIMIR Skill Forge BC Opaque Caller-Admitted Replay-Byte Handoff Consumer-Intake Contract v1

## Purpose

This pass defines exactly one narrow consumer contract above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationResultV1`

The contract consumes realized opaque caller-admitted replay-byte handoff objects and admits them into a downstream consumer-intake boundary without changing their meaning.

This is not replay parsing, replay-source carrier discovery, replay-input locator success, `mimir_replay::ReplayInput` creation, or export widening.

## Family Scope

The only supported family is:

- `low_boost_recovery`

This remains family-specific because the consumed realization result, receipt tuple, opaque handoff object, and deferred replay/materialization lineage are all low-boost-recovery BC surfaces.

No generic all-family replay/raw-state/index/export/materialization framework is introduced.

## Input Boundary

The only input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationResultV1`

The input must already contain:

- exact opaque handoff source contract disposition and notes
- exact opaque handoff realization disposition and notes
- exact chosen opaque handoff contract shape
- audited low-boost-recovery BC specimen-tree root
- ordered lane/specimen structure
- consumed opaque handoff boundary input per specimen
- preserved opaque handoff output boundary per specimen
- realized opaque caller-admitted replay-byte handoff object per specimen

The input bytes remain:

- caller-admitted
- non-empty
- opaque payload only
- below `mimir_replay::ReplayInput`

## Contract Role

This contract owns only:

- revalidating the realized opaque handoff result
- preserving the exact receipt-bound tuple and opaque byte payload
- adding one consumer-intake boundary marker for downstream handoff consumption

This is the narrowest honest next seam because the previous pass already realized the opaque handoff object, but no downstream consumer boundary may honestly consume it yet without first freezing what "consume" means. The minimum truthful consumer action is intake of the already-realized object as opaque bytes, not parsing, locating, discovering, materializing, exporting, or tensor/control construction.

## Exact Contract Shape v1

### Contract Name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeContractV1`

### Exact Contract-Shape Enum

- `LowBoostRecoveryBcReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeContractShapeV1`
- exact chosen shape:
  `ReceiptBoundReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeOnly`

### Exact Consumer-Intake Kind Enum

- `LowBoostRecoveryBcReceiptBoundReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeKindV1`
- exact bound kind:
  `OpaqueCallerAdmittedReplayBytesConsumerIntakeOnly`

### Exact Consumer-Intake Boundary Input

For one specimen, the consumer-intake boundary input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeBoundaryInputV1`

It is derived only from the realized opaque handoff object and preserves:

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

### Exact Consumer-Intake Boundary Output

For one specimen, the consumer-intake boundary output is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeOutputBoundaryV1`

It preserves the exact same tuple and adds only:

- `bound_opaque_caller_admitted_replay_byte_handoff_consumer_intake_kind`

That bound kind means only that a downstream consumer-intake seam has accepted the already-realized opaque handoff object as opaque bytes.

It does not mean:

- replay parsing
- replay-source carrier discovery
- replay-source actual-materialization implementation
- replay-input locator success
- replay path resolution
- `mimir_replay::ReplayInput`
- `mimir_export` integration

## Contract Output v1

The contract-definition result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeContractV1`

It preserves:

- `specimen_count`
- `group_count`
- immediate opaque handoff source contract disposition and notes
- audited family root directory
- immediate opaque handoff realization disposition and notes
- chosen opaque handoff contract shape
- ordered lane/specimen structure
- per-specimen consumed handoff boundary input
- per-specimen preserved handoff output boundary
- per-specimen realized opaque handoff object
- per-specimen opaque handoff realization disposition

It adds only:

- per-specimen consumer-intake boundary input
- per-specimen consumer-intake boundary output
- top-level consumer-intake contract disposition
- top-level consumer-intake contract notes
- chosen consumer-intake contract shape

The exact top-level disposition is:

- `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeOnly`

## Admission Rules

The opaque handoff realization result may enter this contract-definition boundary only when all of the following hold:

1. the input is exactly `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationResultV1`
2. the source opaque handoff contract disposition remains exact
3. the source opaque handoff contract notes remain exact
4. the opaque handoff realization disposition remains exact
5. the opaque handoff realization notes remain exact
6. the chosen opaque handoff contract shape remains exact
7. `specimen_count > 0`
8. `group_count > 0`
9. `group_count` equals ordered lane count
10. each lane remains non-empty
11. lane and specimen ordinals match concrete order
12. every artifact id remains unique
13. the audited family root exists, is a directory, and ends in `low_boost_recovery_bc_v1`
14. each specimen path remains below the audited family root and is not the root itself
15. each accepted reference window remains valid and bounded
16. each opaque byte payload remains non-empty
17. each preserved handoff output exactly matches its consumed handoff input plus the opaque handoff kind
18. each realized handoff object exactly matches its preserved handoff output tuple

Admission here means only that the already-realized opaque handoff objects may be consumed by this consumer-intake contract.

## Failure Rules

This boundary must hard-fail for:

- degraded source contract notes
- degraded source realization notes
- source disposition drift
- realization disposition drift
- chosen-shape drift
- count drift
- lane/specimen order drift
- empty lane results
- duplicate artifact ids
- audited root drift
- specimen path drift outside the audited root
- accepted-window invalidity
- empty opaque byte payloads
- drift between consumed handoff input and preserved handoff output
- drift between preserved handoff output and realized handoff object
- any attempt to reinterpret `source_replay` as a replay path
- any attempt to reinterpret `source_replay.provenance_label` as a replay path
- any attempt to reinterpret `audited_family_root_directory` as replay storage

This boundary does not repair, skip, resort, pad, synthesize bytes, guess paths, parse bytes, discover carriers, locate replay input, or fall back to sidecars or manifests.

## Non-Goals

This pass does not implement:

- replay-source actual-materialization
- replay-source carrier discovery
- replay-input locator logic
- actual replay parsing
- parser-success logic
- raw-state payload parsing
- tensor/control materialization
- corpus-wide replay ingestion
- real rollout physics
- async/background systems
- database code
- runtime CLI commands
- `mimir_replay::ReplayInput`
- `mimir_export` integration or widening
- generic replay/raw-state/index/export/materialization infrastructure

`source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` remain lineage/receipt anchors only.

## Relation To Next Stages

This pass guarantees only:

- one exact consumer-intake contract exists above the realized opaque handoff result
- the same receipt-bound tuple is revalidated
- the same opaque caller-admitted replay bytes are preserved
- the consumer-intake marker is bounded and auditable
- the boundary remains below replay parsing, replay-input locator logic, replay-source carrier discovery, `mimir_replay::ReplayInput`, and `mimir_export`

The immediate next pass is:

- the first realization pass for this exact opaque caller-admitted replay-byte handoff consumer-intake contract

`mimir_export` widening remains forbidden unless explicitly reopened.
