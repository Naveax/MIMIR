# MIMIR Skill Forge BC Actual Replay Parsing Contract v1

## A. PURPOSE

This pass owns exactly one contract-definition boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationResultV1`

The selected downstream domain is actual replay parsing because the immediately lower trusted
boundary now carries a concrete parser-consumable input:

- `mimir_replay::ReplayInput::Memory { label, bytes }`

This pass is contract-definition only. It defines the first parser-facing boundary for the
low-boost-recovery family, but it does not execute a parser, does not classify parser success, and
does not parse raw-state payloads.

The narrow parser-facing surface named by this contract is a future header-level attempt:

- `mimir_replay::ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

Naming that surface does not prove that the current `UnsupportedReplayReader` can parse replay
bytes. It only defines the exact attempt boundary that a later realization pass may decide to
exercise.

## B. FAMILY SCOPE

The only supported family is:

- `low_boost_recovery`

This remains family-specific because the admitted result, receipt-bound tuple, accepted reference
window, replay-input creation bridge, and opaque caller-admitted replay bytes are all
low-boost-recovery BC surfaces.

No generic all-family replay, raw-state, index, export, parser, locator, or materialization
framework is introduced.

## C. INPUT BOUNDARY

This pass consumes exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationResultV1`

From that realized result, this boundary consumes:

- `specimen_count`
- `group_count`
- source opaque caller-admitted replay-byte consumer-intake contract disposition and notes
- audited family root directory as a BC specimen-tree receipt anchor only
- source opaque caller-admitted replay-byte consumer-intake realization disposition and notes
- chosen opaque caller-admitted replay-byte consumer-intake contract shape
- ReplayInput-creation realization disposition and notes
- chosen ReplayInput-creation contract shape
- ordered lane/specimen realization results
- each consumed ReplayInput-creation boundary input
- each preserved ReplayInput-creation output boundary
- each preserved ReplayInput-creation bridge object
- each per-specimen ReplayInput-creation realization disposition

Older lower layers are not direct parser proof. They remain lineage and receipt context only.
Specifically:

- `source_replay` is not a replay path
- `source_replay.provenance_label` is not a replay path
- `audited_family_root_directory` is not replay storage

## D. CONTRACT ROLE

This contract owns only:

- revalidating the realized ReplayInput-creation result
- preserving the exact receipt-bound tuple
- preserving the exact `ReplayInput::Memory` bridge
- defining one exact header parse-attempt contract shape
- defining one exact parser attempt boundary input tuple
- defining one exact parser attempt boundary output tuple
- defining one exact parser attempt object shape
- naming `ReplayReader::read_header(&ReplayInput)` as the future parser-attempt surface

This contract is allowed to define a future attempt to read a `ReplayHeader` from the preserved
memory-backed `ReplayInput`.

This contract is not allowed to:

- execute replay parsing
- define parser-success policy
- parse raw-state payloads
- extract replay frames
- extract semantic events
- materialize replay sources
- discover replay-source carriers
- locate replay inputs
- derive replay paths
- widen `mimir_export`
- add runtime CLI, database, async/background, corpus ingestion, or rollout physics behavior

## E. EXACT CONTRACT SHAPE V1

### Contract Name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`

### Parser Contract Shape Enum

- `LowBoostRecoveryBcActualReplayParsingContractShapeV1`
- exact chosen value:
  `ReceiptBoundReplayHeaderParseAttemptFromMimirReplayMemoryInputOnly`

### Parser Attempt Kind Enum

- `LowBoostRecoveryBcActualReplayParsingAttemptKindV1`
- exact chosen value:
  `MimirReplayReaderReadHeaderFromReplayInputOnly`

### Future Parser Surface Enum

- `LowBoostRecoveryBcActualReplayParsingFutureParserSurfaceV1`
- exact chosen value:
  `MimirReplayReplayReaderReadHeaderOfReplayInput`

This names the future use of:

- `mimir_replay::ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

It is not parser execution and not parser-success logic.

### Exact Parser Attempt Boundary Input Tuple

For one specimen, the parser attempt boundary input is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingAttemptBoundaryInputV1`

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
- `preserved_replay_input_creation_bridge_kind`
- `preserved_replay_input`

`preserved_replay_input` must be the exact memory-backed `ReplayInput` preserved by the lower
ReplayInput-creation bridge.

### Exact Parser Attempt Boundary Output Tuple

For one specimen, the parser attempt boundary output is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingAttemptOutputBoundaryV1`

It preserves the parser attempt boundary input tuple and adds only:

- `bound_actual_replay_parsing_attempt_kind`
- `future_parser_surface`

This output tuple is not a parser result. It carries no `ReplayHeader`, no error classification,
and no parser-success signal.

### Exact Parser Attempt Object Shape

For one specimen, the parser attempt object is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingHeaderAttemptV1`

It carries exactly:

- the preserved receipt-bound tuple
- `opaque_caller_admitted_replay_bytes`
- `preserved_replay_input_creation_bridge_kind`
- `attempt_replay_input`
- `actual_replay_parsing_attempt_kind`
- `future_parser_surface`

`attempt_replay_input` must remain `ReplayInput::Memory` with:

- label:
  `low_boost_recovery_bc_v1:replay_input:artifact:{artifact_id}:lane:{lane_ordinal}:specimen:{specimen_ordinal}`
- bytes exactly equal to `opaque_caller_admitted_replay_bytes`

### Exact Relation to ReplayInput::Memory

The contract consumes the already-realized memory bridge only. It does not create a new
file-backed `ReplayInput`, does not derive a path, and does not use lineage fields as storage
coordinates.

The parser attempt object binds the exact preserved memory input to a future header attempt. It
does not inspect the bytes.

### Exact Preservation Requirements

For every admitted specimen, the following must be preserved:

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
- ReplayInput-creation bridge lineage
- ReplayInput-creation bridge kind
- `ReplayInput::Memory` label
- `ReplayInput::Memory` bytes

This contract must not claim:

- parser success
- raw-state payload availability
- frame extraction
- semantic event extraction
- replay-input locator success
- replay-source carrier discovery
- replay-source actual-materialization implementation
- export readiness

## F. CONTRACT OUTPUT V1

The minimum family-specific contract-definition result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`

It preserves:

- counts and ordered lane/specimen structure
- lower consumer-intake contract disposition and notes
- lower consumer-intake realization disposition and notes
- audited family root directory as a receipt anchor only
- lower consumer-intake chosen contract shape
- ReplayInput-creation realization disposition and notes
- chosen ReplayInput-creation contract shape
- each consumed ReplayInput-creation boundary input
- each preserved ReplayInput-creation output boundary
- each preserved ReplayInput-creation bridge
- each ReplayInput-creation per-specimen disposition

It adds only:

- one parser attempt boundary input per specimen
- one parser attempt boundary output per specimen
- one parser header-attempt object per specimen
- one top-level actual replay parsing contract disposition
- one top-level actual replay parsing contract note set
- one chosen actual replay parsing contract shape

The exact top-level disposition is:

- `ContractDefinedForReceiptBoundActualReplayParsingHeaderAttemptOnly`

## G. ADMISSION RULES

A ReplayInput-creation realization result may enter this boundary only when all conditions hold:

1. source consumer-intake contract disposition and notes remain exact
2. source consumer-intake realization disposition and notes remain exact
3. chosen source consumer-intake contract shape remains exact
4. ReplayInput-creation realization disposition and notes remain exact
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
21. each ReplayInput-creation output boundary exactly matches the consumed ReplayInput-creation input
22. each ReplayInput-creation bridge exactly matches the ReplayInput-creation output boundary
23. every created replay input is exactly `ReplayInput::Memory`
24. every memory label is receipt-derived only from artifact id, lane ordinal, and specimen ordinal
25. every memory byte payload equals the preserved opaque caller-admitted replay bytes

Admission means only that a header parse-attempt contract may be defined over the preserved memory
input.

## H. FAILURE RULES

This boundary hard-fails for:

- degraded lower contract or realization notes
- disposition drift
- chosen-shape drift
- count drift
- empty lanes
- lane/specimen order drift
- duplicate artifact ids
- audited-root drift
- specimen path drift outside the audited root
- invalid accepted windows
- empty opaque replay bytes
- preserved handle-kind drift
- ReplayInput-creation boundary input/output drift
- ReplayInput-creation bridge drift
- file-backed `ReplayInput`
- replay-input label drift
- replay-input byte drift
- any attempt to reinterpret `source_replay` as a replay path
- any attempt to reinterpret `source_replay.provenance_label` as a replay path
- any attempt to reinterpret `audited_family_root_directory` as replay storage
- any parser execution, parser-success classification, raw-state parsing, carrier discovery,
  locator logic, actual-materialization implementation, or export widening

There is no repair behavior:

- no specimen skipping
- no lane resorting
- no byte synthesis
- no path guessing
- no sidecar or manifest fallback

## I. NON-GOALS

This pass does not implement:

- actual parser execution
- parser-success logic
- raw-state payload parsing
- frame extraction
- semantic replay event extraction
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- `mimir_export` integration or widening
- runtime CLI commands
- corpus-wide replay ingestion
- async/background systems
- database code
- real rollout physics
- execution-result cleanup changes
- generic all-family replay/raw-state/index/export/materialization infrastructure

This pass does not modify `mimir-replay`, `mimir-io`, `mimir-export`, or `mimir-types`.

## J. RELATION TO NEXT STAGES

This contract guarantees only:

- the low-boost-recovery ReplayInput-creation realization result is revalidated
- the receipt-bound tuple is preserved
- the memory-backed ReplayInput bridge is preserved
- one exact future header parse-attempt boundary is defined
- parser attempt remains separate from parser-success policy
- raw-state payload parsing remains deferred
- locator, carrier, materialization, and export semantics remain closed

This contract still does not guarantee:

- parser readiness
- parser success
- `ReplayHeader` availability
- replay frame extraction
- raw-state payload availability
- replay-source actual materialization
- replay-source carrier discovery
- replay-input locator success
- export readiness

The immediate next pass should be one of:

- the first realization pass for this exact actual replay parsing contract
- a narrow implementation-readiness decision if parser execution is not yet justified

`mimir_export` widening remains forbidden unless explicitly reopened.
