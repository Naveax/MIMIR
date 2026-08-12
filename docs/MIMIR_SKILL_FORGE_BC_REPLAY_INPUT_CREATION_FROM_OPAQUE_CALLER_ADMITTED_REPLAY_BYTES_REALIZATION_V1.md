# MIMIR Skill Forge BC ReplayInput Creation From Opaque Caller-Admitted Replay Bytes Realization v1

## A. PURPOSE

This pass realizes exactly one contract boundary:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesContractV1`

The realized fact is intentionally narrow:

- each contract-defined bridge is revalidated as exactly one memory-backed `mimir_replay::ReplayInput`
- each label is revalidated as receipt-derived only
- each byte payload is revalidated as exactly the preserved opaque caller-admitted replay bytes

This is not replay parsing, parser success, replay-source actual-materialization, replay-source carrier discovery, replay-input locator logic, raw-state payload parsing, or export widening.

## B. FAMILY SCOPE

The only supported family is:

- `low_boost_recovery`

The realization remains low-boost-recovery-specific because it consumes only the low-boost-recovery ReplayInput-creation contract and preserves that contract's receipt-bound lane/specimen/artifact tuple.

No generic all-family replay/raw-state/index/export/materialization framework is introduced.

## C. INPUT BOUNDARY

The only input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesContractV1`

The realization revalidates:

- top-level source consumer-intake contract disposition and notes
- top-level source consumer-intake realization disposition and notes
- chosen source consumer-intake contract shape
- top-level ReplayInput-creation contract disposition and notes
- chosen ReplayInput-creation contract shape
- non-empty ordered lane/specimen structure
- receipt-bound audited family root as a BC specimen-tree anchor only
- every consumed consumer-intake boundary input and output boundary
- every ReplayInput-creation boundary input and output boundary
- every ReplayInput-creation bridge object

`source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` remain lineage/receipt anchors only. They are not replay paths, replay storage roots, locator inputs, or parser-readiness proof.

## D. REALIZATION ROLE

The realization owns only:

- consuming the exact contract result
- revalidating the exact contract result
- revalidating the exact bridge object per specimen
- revalidating that every created replay input is `ReplayInput::Memory`
- revalidating that every replay-input label is derived only from `artifact_id`, `lane_ordinal`, and `specimen_ordinal`
- revalidating that every replay-input byte payload equals `opaque_caller_admitted_replay_bytes`
- emitting one truthful realization result for this contract only

The realization does not open any downstream parser, locator, carrier, raw-state, materialization, or export behavior.

## E. EXACT REALIZATION SHAPE V1

### Realization Disposition

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationDispositionV1`
- exact realized value:
  `RealizedForReceiptBoundReplayInputCreationFromOpaqueCallerAdmittedReplayBytesOnly`

### Realization Notes

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationNoteV1`

The notes state that the contract boundary, receipt-bound tuple, memory bridge, receipt-derived labels, byte equality, and closed downstream domains were preserved.

### Per-Specimen Result

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationSpecimenResultV1`

It carries only:

- `specimen_ordinal`
- consumed ReplayInput-creation boundary input
- preserved ReplayInput-creation output boundary
- preserved ReplayInput-creation bridge
- per-specimen realization disposition

### Lane Result

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationLaneResultV1`

It carries only:

- `lane_ordinal`
- ordered per-specimen realization results

### Top-Level Result

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationResultV1`

It preserves:

- `specimen_count`
- `group_count`
- source consumer-intake contract disposition and notes
- audited family root directory as receipt anchor only
- source consumer-intake realization disposition and notes
- chosen source consumer-intake contract shape
- ordered lane/specimen realization structure
- chosen ReplayInput-creation contract shape

It adds only:

- top-level ReplayInput-creation realization disposition
- top-level ReplayInput-creation realization notes

## F. OUTPUT / RESULT SHAPE

For every specimen, the realization output preserves the contract-defined:

- ReplayInput-creation boundary input
- ReplayInput-creation output boundary
- ReplayInput-creation bridge object

It revalidates that:

- `bound_replay_input_creation_bridge_kind == MimirReplayMemoryInputFromOpaqueCallerAdmittedReplayBytesOnly`
- `bridge.replay_input_creation_bridge_kind == MimirReplayMemoryInputFromOpaqueCallerAdmittedReplayBytesOnly`
- `created_replay_input == ReplayInput::Memory { label, bytes }`
- `label == low_boost_recovery_bc_v1:replay_input:artifact:{artifact_id}:lane:{lane_ordinal}:specimen:{specimen_ordinal}`
- `bytes == opaque_caller_admitted_replay_bytes`

No path is derived. No file-backed replay input is accepted. No parser is invoked.

## G. ADMISSION RULES

A contract may enter this realization only when all conditions hold:

1. source consumer-intake contract disposition and notes remain exact
2. source consumer-intake realization disposition and notes remain exact
3. chosen source consumer-intake contract shape remains exact
4. ReplayInput-creation contract disposition and notes remain exact
5. chosen ReplayInput-creation contract shape remains exact
6. `specimen_count > 0`
7. `group_count > 0`
8. `group_count` equals ordered lane count
9. every lane is non-empty
10. lane and specimen ordinals match concrete order
11. every artifact id remains unique
12. audited family root exists, is a directory, and ends in `low_boost_recovery_bc_v1`
13. each anchored specimen path remains below the audited family root and is not the root itself
14. each accepted reference window remains valid and bounded
15. each opaque byte payload remains non-empty
16. each preserved replay-input-locator handle kind remains `FutureParserConsumableReplayHandleOnly`
17. each preserved replay-source-materialization requirement kind remains `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`
18. each preserved replay-source-actual-materialization handle kind remains `FutureExplicitReplaySourceCarrierOnly`
19. each preserved carrier-provenance/source-binding handle kind remains `FutureExplicitReplaySourceCarrierProvenanceBindingOnly`
20. each preserved explicit-admission kind remains `FutureAdmittedExplicitReplaySourceCarrierProvenanceSourceBindingOnly`
21. each consumer-intake output boundary exactly matches its input plus the consumer-intake kind
22. each ReplayInput-creation boundary input exactly matches the consumed consumer-intake input
23. each ReplayInput-creation output boundary exactly matches the ReplayInput-creation input
24. each ReplayInput-creation bridge exactly matches the ReplayInput-creation output boundary
25. every created replay input is exactly `ReplayInput::Memory`

Admission means only that the contract-defined memory replay input exists and is revalidated.

## H. FAILURE RULES

This boundary hard-fails for:

- degraded source consumer-intake contract notes
- degraded source consumer-intake realization notes
- degraded ReplayInput-creation contract notes
- disposition drift
- chosen-shape drift
- count drift
- empty lanes
- lane/specimen order drift
- duplicate artifact ids
- audited-root drift
- specimen path drift outside the audited root
- invalid accepted windows
- empty opaque byte payloads
- preserved handle-kind drift
- consumer-intake input/output drift
- ReplayInput-creation boundary input drift
- ReplayInput-creation output boundary drift
- ReplayInput-creation bridge drift
- file-backed `ReplayInput` creation
- replay-input label drift
- replay-input byte drift

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

This pass does not modify `mimir-replay`, `mimir-io`, `mimir-export`, or `mimir-types`.

## J. RELATION TO NEXT STAGES

This realization proves only:

- the exact contract-defined `ReplayInput::Memory` bridge is present and internally consistent
- the receipt-bound tuple is preserved through the realization result
- the label is receipt-derived only
- the byte payload is exactly the preserved opaque caller-admitted replay bytes

It still does not prove:

- parser readiness
- replay parsing success
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator success
- raw-state payload availability
- export readiness

The immediate next pass should be a narrower post-realization boundary decision that chooses whether to stop or explicitly reopen one downstream domain. `mimir_export` widening remains forbidden unless explicitly reopened.
