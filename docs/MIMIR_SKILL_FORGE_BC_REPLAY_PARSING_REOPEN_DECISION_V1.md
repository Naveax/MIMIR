# MIMIR Skill Forge BC Replay-Parsing Reopen Decision v1

## A. PURPOSE

### What this pass owns

This pass owns exactly one question above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`

It defines:

- whether replay parsing must now be deliberately reopened at all
- the criteria used to decide that question
- the narrowest honest next contract shape only if reopening is justified

### Why it exists

The boundary below this pass already proved that one admitted low-boost-recovery specimen can now
yield only one truthful result:

- `RealizedForTruthfulNonMaterializedAttemptOnly`

That proof matters because it closes a different question than the one owned here.

The current repo can now prove all of the following above the receipt-bound validated
specimen-file materialization contract:

- the admitted specimen identity and lineage survive into the realization result
- `anchored_bc_specimen_file_path` remains receipt-bound below the audited family root
- `source_raw_state_window_ref` remains preserved but still opaque
- the current implementation does not produce raw-state payload, replay frames, tensors, or
  controls

What this pass must answer is narrower:

- is the remaining missing boundary now truly replay-side raw-state sourcing, such that replay
  parsing must be deliberately reopened?

### How it differs from the materialization-attempt realization boundary below it

- The lower boundary realizes the current truth:
  - only a non-materialized attempt result exists.
- This pass does not realize more output.
- This pass decides whether the next missing boundary must now be a replay-side sourcing /
  parse-attempt boundary.
- This pass is still not replay parsing implementation.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this reopen-decision version.

This replay-parsing reopen decision remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
- the preserved opaque linkage is the family-specific BC field `source_raw_state_window_ref`
- the preserved specimen identity and deferred observation lineage are only the low-boost-recovery
  BC specimen fields already carried by the realization result
- no second family exists that would justify a shared replay/raw-state reopen framework

No generic multi-family replay/raw-state/index/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
- the audited family root directory reference already preserved by that result

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `consumed_materialization_attempt_input.lane_ordinal`
- each `consumed_materialization_attempt_input.specimen_ordinal`
- each `consumed_materialization_attempt_input.artifact_id`
- each `consumed_materialization_attempt_input.anchored_bc_specimen_file_path`
- each `consumed_materialization_attempt_input.source_raw_state_window_ref`
- each `consumed_materialization_attempt_input.source_slice_id`
- each `consumed_materialization_attempt_input.source_replay`
- each `consumed_materialization_attempt_input.source_subject`
- each `consumed_materialization_attempt_input.source_phase_id`
- each `preserved_materialization_attempt_output_boundary.lane_ordinal`
- each `preserved_materialization_attempt_output_boundary.specimen_ordinal`
- each `preserved_materialization_attempt_output_boundary.artifact_id`
- each `preserved_materialization_attempt_output_boundary.anchored_bc_specimen_file_path`
- each `preserved_materialization_attempt_output_boundary.source_raw_state_window_ref`
- each `preserved_materialization_attempt_output_boundary.source_slice_id`
- each `preserved_materialization_attempt_output_boundary.source_replay`
- each `preserved_materialization_attempt_output_boundary.source_subject`
- each `preserved_materialization_attempt_output_boundary.source_phase_id`
- each `preserved_materialization_attempt_output_boundary.preserved_observation_binding_kind`
- each `preserved_materialization_attempt_output_boundary.preserved_accepted_reference_window`
- each `materialization_attempt_disposition`
- `realization_disposition`
- `realization_notes`
- `chosen_materialization_contract_shape`

Direct input is no longer:

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

Those lower layers remain frozen. This pass starts strictly from the truthful
non-materialized-attempt realization result and the audited family root reference already preserved
there.

## D. DECISION QUESTION

The exact question is:

- should replay parsing now be deliberately reopened above the truthful non-materialized attempt
  boundary?

This question exists now only because the current repo can already prove something narrower and
stricter than before:

- the current realization boundary can do no more than emit
  `RealizedForTruthfulNonMaterializedAttemptOnly`

That means the unresolved gap is no longer whether the current contract/result surface is explicit.
The unresolved gap is whether replay-side raw-state sourcing must now be deliberately reopened to
give `source_raw_state_window_ref` any honest next boundary above that truthful non-materialized
attempt.

This is still not replay parsing implementation.

## E. REOPEN CRITERIA

Reopening is justified only if all of the following hold:

1. the admitted input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
2. the source contract disposition and source contract note set remain exact
3. the realization disposition and realization note set remain exact
4. the locator contract shape remains `ReceiptBoundSpecimenFileAnchored`
5. the materialization contract shape remains
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
6. the audited family root remains only the low-boost-recovery BC specimen-tree anchor and is not
   reinterpreted as replay storage or raw-state storage
7. lane order, specimen order, anchored specimen-file path binding, and per-specimen
   input/output-boundary identity still remain exact
8. the remaining missing piece is truly replay-side raw-state sourcing above the truthful
   non-materialized attempt boundary, not another receipt-bound locator/materialization defect
9. the next boundary can remain low-boost-recovery-specific
10. the next boundary can remain receipt-bound
11. the next boundary can avoid sidecars, manifests, and generic indexing
12. the next boundary can avoid `mimir_export`
13. the next boundary can stay below tensor/control materialization
14. the next boundary can still refuse to promise actual replay parsing success, raw-state payload,
    tensors, or controls

The repo-surface audit must also not contradict that conclusion.

In the audited repo state for this pass:

- `mimir-replay` still exposes only:
  - `ReplayInput`
  - `ReplayHeader`
  - `ReplayReader`
  - `UnsupportedReplayReader`
- no replay-side parse-attempt contract exists above the truthful non-materialized attempt result

That matters because reopening is only honest if the remaining missing capability is actually
absent above the current result surface.

## F. DECISION

Decision chosen:

- reopen justified for one narrow replay-side raw-state sourcing boundary

Reopening is justified because the current realization boundary already proves the problem has been
reduced to one narrower missing capability:

- the repo can preserve receipt-bound specimen identity and lineage into the truthful
  non-materialized attempt result
- the repo still cannot turn `source_raw_state_window_ref` into any replay-side sourcing or
  parse-attempt boundary above that result
- `mimir-replay` still does not provide a real parser or even a contract-level parse-attempt
  surface above this boundary

The narrowest honest next boundary shape is:

- one low-boost-recovery-specific, receipt-bound replay-side parse-attempt contract above the
  truthful non-materialized attempt result

That next boundary would consume:

- the truthful non-materialized attempt realization result
- the explicit replay-parsing reopen decision from this pass

That next boundary would expose:

- one contract-only replay-side sourcing / parse-attempt boundary for each admitted specimen

What remains deferred even after reopening is justified:

- actual replay parsing implementation
- actual replay file or byte resolution
- actual raw-state payload materialization
- tensor materialization
- control/action extraction
- `mimir_export` integration
- sidecar/manifest realization

This is the minimum honest reopen because the remaining missing boundary is not:

- another receipt-bound locator fix
- another materialization-contract fix
- a generic replay/index/export framework
- a tensor/control boundary

It is only the next contract needed to bind the already-truthful non-materialized attempt result to
one explicit replay-side sourcing / parse-attempt boundary.

## G. REPLAY-PARSING CONTRACT SHAPE V1

Because reopening is justified, the narrowest contract-only next boundary is defined here.

### Contract name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`

### Exact inputs it would consume from the realization result

The next contract should consume exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `audited_family_root_directory`
- ordered lane/specimen structure
- `realization_disposition`
- `realization_notes`
- `chosen_materialization_contract_shape`
- each specimen's:
  - `consumed_materialization_attempt_input`
  - `preserved_materialization_attempt_output_boundary`
  - `materialization_attempt_disposition`

It should also consume the explicit reopen decision from this pass.

### Exact replay-side sourcing / parse-attempt boundary it would expose

The next contract should expose only:

- one per-specimen replay-side parse-attempt contract boundary keyed by the preserved
  `consumed_materialization_attempt_input`
- one preserved output-boundary view that keeps deferred observation lineage visible only as
  deferred lineage:
  - `preserved_observation_binding_kind`
  - `preserved_accepted_reference_window`

It should not expose:

- parsed replay frames
- replay-derived raw-state payload
- materialized tensor payload
- materialized control payload

### Exact invariant

For one admitted specimen, the next contract must bind exactly one tuple:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`

plus the same specimen's preserved deferred observation lineage:

- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`

to exactly one honest replay-side sourcing / parse-attempt contract boundary.

That invariant is strict:

- no remapping between specimen identity and replay-side attempt identity
- no reinterpretation of the audited family root as replay storage
- no guessed replay path
- no guessed raw-state payload
- no speculative lineage repair

### Exact relationship to deferred observation access

Deferred observation lineage may remain visible only through:

- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`

Those fields may not:

- be treated as already-materialized replay/raw-state payload
- be turned into tensors
- be turned into controls

### What it explicitly refuses to promise

The next contract must explicitly refuse to promise:

- actual replay parsing success
- replay frame availability
- replay file path availability
- replay byte availability
- raw-state payload availability
- tensor availability
- control/action availability
- `mimir_export` widening
- sidecar/manifest necessity

## H. ADMISSION RULES

A realization result may enter this reopen-decision boundary only when all of the following hold:

1. the input is exactly
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
2. `source_contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptOnly`
3. `source_contract_notes` still equal the exact contract-note set frozen below this boundary
4. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
5. `realization_disposition == RealizedForTruthfulNonMaterializedAttemptOnly`
6. `realization_notes` still equal the exact realization-note set frozen below this boundary
7. `chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
8. `specimen_count > 0`
9. `group_count > 0`
10. `group_count` equals the number of preserved ordered lane results
11. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
12. `audited_family_root_directory` still exists as a directory at decision time
13. lane order and specimen order still match concrete lane/specimen position
14. each `consumed_materialization_attempt_input.anchored_bc_specimen_file_path` still remains
    receipt-bound below `audited_family_root_directory`
15. each `preserved_materialization_attempt_output_boundary` still matches the corresponding
    consumed attempt input on:
    - `lane_ordinal`
    - `specimen_ordinal`
    - `artifact_id`
    - `anchored_bc_specimen_file_path`
    - `source_raw_state_window_ref`
    - `source_slice_id`
    - `source_replay`
    - `source_subject`
    - `source_phase_id`
16. each specimen still preserves
    `materialization_attempt_disposition == RealizedForTruthfulNonMaterializedAttemptOnly`
17. no lower boundary is silently reopened to repair or reinterpret the admitted realization input

Admission here means only:

- this reopen decision may rely on the truthful non-materialized attempt result as the last
  trusted pre-replay-parsing layer

Admission here does not mean:

- replay parsing has been implemented
- replay-side sourcing must already succeed
- raw-state payload exists
- tensors or controls are available

## I. FAILURE RULES

This pass must hard-fail for:

- degraded realization input
- count/order/root/path drift
- any input/output-boundary identity drift
- any specimen whose attempt disposition no longer remains truthful non-materialized only
- any attempt to reinterpret the audited family root as replay storage or raw-state storage
- any attempt to widen this pass into actual replay parsing
- any attempt to widen this pass into raw-state payload materialization
- any attempt to widen this pass into tensors, controls, sidecars, manifests, generic indexing, or
  `mimir_export`

This v1 pass does not emit a separate no-reopen disposition for admitted inputs.

Reason:

- once the admitted realization boundary remains exact, the remaining unresolved boundary is
  already replay-side raw-state sourcing / parse-attempt contract shape

So failure behavior is:

- hard-fail on any admission violation
- otherwise emit the single reopen-justified decision defined above

## J. NON-GOALS

This pass does not do any of the following:

- no actual replay parsing
- no actual raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof

## K. RELATION TO NEXT STAGES

This pass now guarantees:

- the repo has an explicit answer to whether replay parsing must now be deliberately reopened
- that answer is tied to the truthful non-materialized attempt result, not guessed from lower
  layers
- the minimum next contract shape is now explicit
- the audited family root still remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual replay-side sourcing
- actual replay parsing
- actual raw-state-window payload materialization
- tensor/control materialization

The immediate next pass should be:

- a first narrow contract-definition pass for
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptContractV1`

That next pass should consume:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptRealizationResultV1`
- the explicit replay-parsing reopen decision produced here

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- implement replay parsing
- implement raw-state payload materialization
- reopen tensor/control materialization
- add sidecars/manifests unless separately proven necessary
