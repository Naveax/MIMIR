# MIMIR Skill Forge BC Opaque Caller-Admitted Replay-Byte Handoff Realization v1

## Purpose

This pass realizes exactly one low-boost-recovery boundary:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractV1`

The realization preserves already-admitted replay bytes as opaque payload and revalidates that each per-specimen handoff still matches the exact receipt-bound tuple frozen by the contract.

It does not parse replay bytes, locate replay inputs, discover carriers, materialize replay sources, create `mimir_replay::ReplayInput`, or integrate with `mimir_export`.

## Family Scope

The only supported family is:

- `low_boost_recovery`

This pass remains family-specific because the consumed contract, receipt tuple, handoff object, and byte-backed source form below it are all low-boost-recovery BC types.

No generic replay/raw-state/index/export/materialization framework is introduced.

## Input Boundary

The only input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractV1`

The input must already contain:

- the exact opaque handoff contract disposition
- the exact opaque handoff contract note set
- the exact chosen opaque handoff contract shape
- the preserved byte-backed caller-admitted source-form realization lineage below it
- ordered lane/specimen structure
- per-specimen opaque handoff boundary input
- per-specimen opaque handoff boundary output
- per-specimen opaque handoff object

The bytes remain:

- caller-admitted
- opaque
- non-empty
- below `mimir_replay::ReplayInput`

## Realization Role

This realization owns only:

- revalidating the exact opaque handoff contract input
- revalidating the exact lower byte-backed receipt-bound tuple view carried by the contract
- preserving the exact opaque handoff input/output/object tuple per specimen
- marking each preserved opaque handoff object as realized for this handoff boundary only

This realization does not prove replay-source actual-materialization, replay-source carrier discovery, replay-input locator success, replay parsing success, or replay-input creation.

## Exact Realization Shape

The Rust realization surface is owned by `mimir-skill` and consists of:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationResultV1`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_source_actual_materialization_opaque_caller_admitted_replay_byte_handoff_v1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationError`

The single realization disposition is:

- `RealizedForReceiptBoundOpaqueCallerAdmittedReplayByteHandoffOnly`

## Output/Result Shape

The top-level realization result preserves:

- `specimen_count`
- `group_count`
- immediate opaque handoff `source_contract_disposition`
- immediate opaque handoff `source_contract_notes`
- `audited_family_root_directory`
- ordered lane/specimen realization results
- realization disposition
- realization notes
- chosen opaque handoff contract shape

Each per-specimen realization result preserves:

- consumed opaque handoff boundary input
- preserved opaque handoff boundary output
- realized opaque handoff object
- handoff-only realization disposition

The realized object is exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffV1`

No new byte shape or replay-input shape is introduced.

## Admission Rules

The contract is admitted only if all of the following remain true:

- the immediate opaque handoff contract disposition is exact
- the immediate opaque handoff contract notes are exact
- the chosen opaque handoff contract shape is exact
- the preserved byte-backed caller-admitted realization view revalidates through the same strict lower validator used by the contract-definition boundary
- `specimen_count > 0`
- `group_count > 0`
- `group_count` equals ordered lane count
- lane and specimen ordinals match concrete order
- artifact ids are unique
- specimen paths remain below `audited_family_root_directory`
- `audited_family_root_directory` remains a directory named `low_boost_recovery_bc_v1`
- accepted reference windows remain valid and bounded
- replay-input-locator handle kind remains `FutureParserConsumableReplayHandleOnly`
- replay-source-materialization requirement kind remains `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`
- replay-source-actual-materialization handle kind remains `FutureExplicitReplaySourceCarrierOnly`
- carrier-provenance binding handle kind remains `FutureExplicitReplaySourceCarrierProvenanceBindingOnly`
- explicit carrier-provenance/source-binding admission kind remains `FutureAdmittedExplicitReplaySourceCarrierProvenanceSourceBindingOnly`
- opaque byte payloads remain non-empty
- each handoff input exactly matches the byte-backed source form below it
- each handoff output exactly matches its input plus the bound opaque handoff kind
- each handoff object exactly matches its output tuple

## Failure Rules

This realization hard-fails for:

- degraded immediate contract notes
- degraded lower preserved byte-backed contract notes
- degraded lower preserved realization notes
- chosen-shape drift
- disposition drift
- count drift
- lane/specimen order drift
- duplicate artifact ids
- specimen path drift outside the audited root
- invalid accepted reference windows
- empty opaque byte payloads
- drift between byte-backed source form and opaque handoff input
- drift between opaque handoff input and opaque handoff output
- drift between opaque handoff output and opaque handoff object

This realization never repairs, skips, resorts, pads, synthesizes bytes, guesses paths, or falls back to manifests/sidecars.

## Non-Goals

This pass does not implement:

- replay-source actual-materialization
- replay-source carrier discovery
- replay-input locator logic
- replay parsing
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
- generic all-family replay/raw-state/index/export/materialization infrastructure

`source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` remain lineage/receipt anchors only. They are not replay path or replay storage semantics.

## Relation To Next Stages

This pass guarantees only:

- the opaque caller-admitted replay-byte handoff contract can be truthfully realized per specimen
- the exact receipt-bound tuple is revalidated
- opaque bytes are preserved unchanged
- the result remains below replay parsing, replay-input locator logic, replay-source carrier discovery, `mimir_replay::ReplayInput`, and `mimir_export`

The next pass should be narrower than this one and should consume this realization result without reopening `mimir_export`.
