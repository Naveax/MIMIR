# MIMIR Skill Forge BC Opaque Caller-Admitted Replay-Byte Handoff Consumer-Intake Realization v1

## Purpose

This pass defines the first truthful realization boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeContractV1`

The realization consumes that exact consumer-intake contract, revalidates the receipt-bound tuple for each ordered specimen, preserves the same opaque caller-admitted replay bytes, and emits a concrete consumer-intake realization result.

This is not replay parsing, replay-source carrier discovery, replay-input locator success, `mimir_replay::ReplayInput` creation, replay-source actual-materialization success, or `mimir_export` widening.

## Family Scope

The only supported family is:

- `low_boost_recovery`

The realization is intentionally family-specific. It does not create a generic replay, raw-state, index, export, or materialization framework.

## Input Boundary

The only input boundary is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeContractV1`

The input contract must already contain:

- exact opaque handoff source contract disposition and notes
- exact opaque handoff source realization disposition and notes
- exact consumer-intake contract disposition and notes
- exact chosen opaque handoff contract shape
- exact chosen consumer-intake contract shape
- audited low-boost-recovery BC specimen-tree root
- ordered lane/specimen structure
- per-specimen realized opaque caller-admitted replay-byte handoff object
- per-specimen consumer-intake boundary input
- per-specimen consumer-intake output boundary

The opaque bytes remain caller-admitted opaque payload only.

## Realization Role

This realization owns only:

- revalidating the exact consumer-intake contract
- revalidating that every consumer-intake boundary input is derived from the realized opaque handoff object
- revalidating that every consumer-intake output boundary is derived from the consumer-intake boundary input plus the bounded consumer-intake kind
- preserving lane order, specimen order, artifact ids, receipt-bound lineage, accepted reference windows, and opaque byte payloads
- emitting one concrete per-specimen consumer-intake realization result

It does not infer replay paths, discover carriers, locate replay input, parse bytes, or produce materialized replay-source success.

## Exact Realization Shape

### Realization Disposition

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationDispositionV1`
- exact value:
  `RealizedForReceiptBoundOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeOnly`

### Realization Notes

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationNoteV1`

The notes state that the consumer-intake contract boundary is preserved, inputs are revalidated, opaque bytes stay opaque, replay parsing is still deferred, carrier discovery is still deferred, replay-input locator logic is still deferred, and `mimir_export` integration remains forbidden.

### Per-Specimen Realization Result

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationSpecimenResultV1`

It preserves:

- `specimen_ordinal`
- consumed consumer-intake boundary input
- preserved consumer-intake output boundary
- per-specimen consumer-intake realization disposition

No parser object, replay input object, carrier object, replay path, sidecar, manifest, tensor, or control payload is created.

### Lane Realization Result

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationLaneResultV1`

It preserves:

- `lane_ordinal`
- ordered per-specimen realization results

### Top-Level Realization Result

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationResultV1`

It preserves:

- `specimen_count`
- `group_count`
- source consumer-intake contract disposition
- source consumer-intake contract notes
- audited family root directory
- ordered lane/specimen realization results
- chosen consumer-intake contract shape

It adds only:

- top-level consumer-intake realization disposition
- top-level consumer-intake realization notes

## Output/Result Shape

The output is a concrete consumer-intake realization result. The per-specimen result is the realized instance. It contains the exact consumed consumer-intake boundary input and exact preserved consumer-intake output boundary from the contract.

The output does not claim:

- replay-source actual-materialization success
- replay-source carrier discovery
- replay-input locator success
- actual replay parsing
- parser-success logic
- `mimir_replay::ReplayInput`
- `mimir_export` integration

## Admission Rules

The consumer-intake contract may enter this realization only when all of the following hold:

1. the input is exactly `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeContractV1`
2. the preserved opaque handoff source contract disposition remains exact
3. the preserved opaque handoff source contract notes remain exact
4. the preserved opaque handoff realization disposition remains exact
5. the preserved opaque handoff realization notes remain exact
6. the consumer-intake contract disposition remains exact
7. the consumer-intake contract notes remain exact
8. the chosen opaque handoff contract shape remains exact
9. the chosen consumer-intake contract shape remains exact
10. `specimen_count > 0`
11. `group_count > 0`
12. `group_count` equals ordered lane count
13. each lane remains non-empty
14. lane and specimen ordinals match concrete order
15. every artifact id remains unique
16. the audited family root exists, is a directory, and ends in `low_boost_recovery_bc_v1`
17. each specimen path remains below the audited family root and is not the root itself
18. each accepted reference window remains valid and bounded
19. each opaque byte payload remains non-empty
20. each preserved opaque handoff output exactly matches its consumed opaque handoff input plus the opaque handoff kind
21. each realized opaque handoff object exactly matches its preserved opaque handoff output tuple
22. each consumer-intake boundary input exactly matches the realized opaque handoff object
23. each consumer-intake output boundary exactly matches its consumer-intake input plus the consumer-intake kind

## Failure Rules

This realization hard-fails for:

- degraded source opaque handoff contract notes
- degraded source opaque handoff realization notes
- degraded consumer-intake contract notes
- source disposition drift
- consumer-intake contract disposition drift
- chosen-shape drift
- count drift
- lane/specimen order drift
- empty lane results
- duplicate artifact ids
- audited root drift
- specimen path drift outside the audited root
- accepted-window invalidity
- empty opaque byte payloads
- drift between opaque handoff input, output, and realized handoff object
- drift between realized handoff object and consumer-intake boundary input
- drift between consumer-intake boundary input and consumer-intake output boundary

This realization does not repair, skip, resort, pad, synthesize bytes, guess paths, parse bytes, discover carriers, locate replay input, or fall back to sidecars or manifests.

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
- generic all-family replay/raw-state/index/export/materialization infrastructure

`source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` remain lineage/receipt anchors only.

## Relation To Next Stages

This pass guarantees only:

- one exact consumer-intake realization boundary exists above the consumer-intake contract
- the same receipt-bound tuple is revalidated
- the same opaque caller-admitted replay bytes are preserved
- the realized consumer-intake marker is bounded and auditable
- the boundary remains below replay parsing, replay-input locator logic, replay-source carrier discovery, `mimir_replay::ReplayInput`, and `mimir_export`

The next pass should be narrower than this one and must not silently reopen export, replay parsing, replay-source carrier discovery, or replay-input locator logic.

`mimir_export` widening remains forbidden unless explicitly reopened.
