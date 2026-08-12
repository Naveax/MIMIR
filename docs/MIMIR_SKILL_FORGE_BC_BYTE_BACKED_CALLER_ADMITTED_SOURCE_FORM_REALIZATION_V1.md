# MIMIR Skill Forge BC Byte-Backed Caller-Admitted Source-Form Realization v1

## A. PURPOSE

This pass owns the first truthful realization boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormContractV1`

It consumes concrete caller-provided instances of:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormV1`

It realizes only one new truth:

- non-empty caller-admitted replay bytes may now be bound to the exact frozen receipt-bound tuple for low-boost-recovery BC specimens

It does not claim:

- replay parsing success
- replay-source actual-materialization success beyond caller-byte admission
- replay-source carrier discovery
- replay-input locator success
- `mimir_replay::ReplayInput` creation

## B. FAMILY SCOPE

This realization is low-boost-recovery-specific only.

It remains family-specific because:

- the consumed contract is low-boost-recovery-specific
- the preserved tuple is the low-boost-recovery BC specimen tuple
- no second family justifies generic caller-byte realization infrastructure

No generic replay/raw-state/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormContractV1`
- one lane-ordered caller input matrix:
  - `&[Vec<LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormV1>]`

For each specimen, the caller-provided object must match the frozen output tuple from:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormOutputBoundaryV1`

and may add only:

- `caller_admitted_replay_bytes: Vec<u8>`

## D. REALIZATION ROLE

This pass does exactly four things:

1. revalidate the byte-backed caller-admitted contract result
2. revalidate the preserved receipt-bound tuple for every specimen
3. admit non-empty caller-provided replay bytes for that exact tuple
4. emit a truthful realization result that still treats those bytes as opaque

This pass does not interpret `source_replay`, `source_replay.provenance_label`, or `audited_family_root_directory` as replay storage or replay paths.

## E. EXACT REALIZATION SHAPE

The narrow Rust realization surface is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationNoteV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationSpecimenResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationResultV1`
- `realize_low_boost_recovery_bc_receipt_bound_validated_specimen_file_raw_state_window_replay_source_actual_materialization_byte_backed_caller_admitted_source_form_v1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationError`

The exact realization disposition is:

- `RealizedForReceiptBoundByteBackedCallerAdmittedReplayBytesOnly`

Per specimen, the realization result preserves:

- consumed contract boundary input
- preserved contract output boundary
- the realized caller-admitted source-form object
- the per-specimen realization disposition

## F. OUTPUT / RESULT SHAPE

The top-level truthful result is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationResultV1`

It preserves:

- specimen and lane counts
- the immediate byte-backed contract disposition and note set
- all lower chosen contract shapes already frozen below
- the audited family root directory
- the lower explicit-admission realization disposition and notes
- ordered lane/specimen structure

It adds:

- realized caller-admitted source-form objects carrying opaque replay bytes
- realization disposition and realization notes proving the new truth boundary

## G. ADMISSION RULES

Realization is allowed only when all of the following hold:

1. the input contract remains the exact byte-backed caller-admitted source-form contract
2. the contract note set remains exact
3. the lower explicit-admission contract note set remains exact
4. the lower explicit-admission realization note set remains exact
5. all chosen shapes remain the frozen receipt-bound shapes
6. `specimen_count > 0`
7. `group_count > 0`
8. `group_count` matches both the preserved contract lanes and caller lane matrix length
9. lane order and specimen order match concrete position
10. every anchored specimen path remains receipt-bound below the audited family root
11. every accepted reference window remains valid
12. every preserved handle kind remains the exact frozen deferred kind
13. every caller object matches the exact tuple preserved by the contract output boundary
14. `caller_admitted_replay_bytes` is non-empty for every realized specimen
15. artifact ids remain unique across the preserved receipt-bound set

Admission here means only:

- the caller has supplied opaque replay bytes for the exact tuple
- those bytes are now bound to that tuple in a truthful realization result

Admission here does not mean:

- bytes were parsed
- bytes were discovered from storage
- bytes were converted into `ReplayInput`
- bytes proved replay-source actual-materialization success

## H. FAILURE RULES

This pass hard-fails for:

- degraded contract notes or dispositions
- degraded lower note sets or chosen shapes
- lane/specimen count drift
- lane/specimen order drift
- receipt-bound path drift
- invalid accepted reference windows
- handle-kind drift
- caller object tuple drift
- duplicate artifact ids
- empty caller-admitted byte payloads
- any attempt to reinterpret lineage fields as replay paths or replay storage

There is no repair behavior:

- no specimen skipping
- no lane resorting
- no byte synthesis
- no path guessing
- no parser fallback

## I. NON-GOALS

This pass does not do any of the following:

- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- replay parsing
- parser-success logic
- raw-state payload parsing
- tensor/control materialization
- corpus ingestion
- async/background systems
- database code
- runtime CLI work
- `mimir_export` widening

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- one truthful realization result exists for exact receipt-bound caller-admitted replay bytes
- the realized bytes remain bound to the frozen low-boost-recovery receipt tuple
- the result remains below replay parsing and below `mimir_replay::ReplayInput`
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- replay-source actual-materialization success
- replay-source carrier discovery success
- replay-input locator success
- replay parsing success
- raw-state payload materialization

The immediate next pass should therefore be:

- the contract-definition pass for an exact receipt-bound opaque caller-admitted replay-byte handoff below `mimir_replay::ReplayInput`

