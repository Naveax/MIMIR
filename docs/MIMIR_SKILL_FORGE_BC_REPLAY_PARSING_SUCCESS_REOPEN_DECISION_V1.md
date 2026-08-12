# MIMIR Skill Forge BC Replay-Parsing Success Reopen Decision v1

## A. PURPOSE

### What this pass owns

This pass owns exactly one question above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`

It defines:

- whether replay-parsing success / parser-implementation work should now be deliberately reopened
  at all
- the exact criteria used to answer that question
- the minimum honest next step only if parser-success reopening is justified

### Why it exists

The boundary below this pass already proved the current repo can do no more than:

- `RealizedForTruthfulBlockedReplaySideParseAttemptOnly`

That closes one question and leaves another open.

The lower realization boundary already fixed:

- one admitted specimen yields one exact replay-side parse-attempt result
- receipt-bound specimen identity and lineage survive into that result
- deferred observation lineage remains explicit only as deferred lineage
- the audited family root remains only a BC specimen-tree anchor

What this pass must answer is narrower:

- is the remaining missing piece now honestly parser-success / parser-implementation work
- or is the repo still missing a stricter receipt-bound replay-input-access boundary before parser
  work can be reopened honestly

### How it differs from the replay-side parse-attempt realization boundary below it

- The lower boundary realizes the current truth:
  - only a blocked / unavailable replay-side parse-attempt result exists.
- This pass does not realize a stronger attempt result.
- This pass decides whether actual parser-success / parser-implementation work is now the minimum
  honest reopen above that blocked result.
- This pass is still not parser implementation.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this reopen-decision version.

This decision remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
- the preserved lineage tuple and deferred observation lineage are only the low-boost-recovery BC
  specimen fields already carried by that result
- the audited family root is still only the low-boost-recovery BC specimen-tree anchor
- no second family exists that would justify a shared replay-parser-success reopen framework

No generic all-family replay/raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
- the audited family root directory reference already preserved by that result

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `consumed_replay_side_parse_attempt_input.lane_ordinal`
- each `consumed_replay_side_parse_attempt_input.specimen_ordinal`
- each `consumed_replay_side_parse_attempt_input.artifact_id`
- each `consumed_replay_side_parse_attempt_input.anchored_bc_specimen_file_path`
- each `consumed_replay_side_parse_attempt_input.source_raw_state_window_ref`
- each `consumed_replay_side_parse_attempt_input.source_slice_id`
- each `consumed_replay_side_parse_attempt_input.source_replay`
- each `consumed_replay_side_parse_attempt_input.source_subject`
- each `consumed_replay_side_parse_attempt_input.source_phase_id`
- each `preserved_replay_side_parse_attempt_output_boundary.lane_ordinal`
- each `preserved_replay_side_parse_attempt_output_boundary.specimen_ordinal`
- each `preserved_replay_side_parse_attempt_output_boundary.artifact_id`
- each `preserved_replay_side_parse_attempt_output_boundary.anchored_bc_specimen_file_path`
- each `preserved_replay_side_parse_attempt_output_boundary.source_raw_state_window_ref`
- each `preserved_replay_side_parse_attempt_output_boundary.source_slice_id`
- each `preserved_replay_side_parse_attempt_output_boundary.source_replay`
- each `preserved_replay_side_parse_attempt_output_boundary.source_subject`
- each `preserved_replay_side_parse_attempt_output_boundary.source_phase_id`
- each `preserved_replay_side_parse_attempt_output_boundary.preserved_observation_binding_kind`
- each `preserved_replay_side_parse_attempt_output_boundary.preserved_accepted_reference_window`
- each `replay_side_parse_attempt_disposition`
- `realization_disposition`
- `realization_notes`
- `chosen_replay_parsing_contract_shape`

Direct input is no longer:

- parse-attempt contract results
- materialization-attempt realization results
- replay-parsing reopen decisions below this layer
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

Those lower layers remain frozen. This pass starts strictly from the blocked replay-side
parse-attempt realization result and the already-preserved audited family root reference.

## D. DECISION QUESTION

The exact question is:

- should replay-parsing success / parser-implementation work now be deliberately reopened above the
  truthful blocked replay-side parse-attempt boundary

This question exists now only because the current repo can already prove something narrower:

- the current realization boundary can do no more than emit
  `RealizedForTruthfulBlockedReplaySideParseAttemptOnly`

That means the unresolved gap is no longer whether the replay-side parse-attempt contract exists or
whether the first truthful result above it is explicit.

The unresolved gap is whether the remaining missing piece is now truly parser-success /
parser-implementation work, or whether the repo is still missing a stricter receipt-bound
replay-input-access boundary above the blocked result.

This is still not parser implementation.

## E. REOPEN CRITERIA

Reopening parser-success / parser-implementation work is justified only if all of the following
hold:

1. the admitted input remains an exact
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
2. the source contract disposition and source contract note set remain exact
3. the realization disposition and realization note set remain exact
4. the chosen locator shape remains `ReceiptBoundSpecimenFileAnchored`
5. the chosen materialization shape remains
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
6. the chosen replay-parsing contract shape remains
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
7. the remaining missing piece is truly parser-success / parser-implementation work and not the
   absence of a receipt-bound replay input handle above the blocked replay-side attempt boundary
8. the next boundary could consume only the blocked replay-side parse-attempt realization result
   plus the already-preserved audited family root reference
9. the next boundary could remain low-boost-recovery-specific
10. the next boundary could remain receipt-bound
11. the next boundary could avoid sidecars, manifests, and generic indexing
12. the next boundary could avoid `mimir_export`
13. the next boundary could stay below raw-state payload materialization
14. the next boundary could stay below tensor/control materialization
15. the next boundary could expose something stricter than the current blocked replay-side
    parse-attempt result without inventing replay-path, replay-byte, or replay-storage semantics
16. the repo-surface audit must show that a parser-consumable replay input handle already exists
    above the admitted blocked result, or can be derived from it without widening the boundary

The current repo audit does not satisfy the last two criteria.

In the audited repo state for this pass:

- `mimir-replay` exposes:
  - `ReplayInput`
  - `ReplayHeader`
  - `ReplayReader`
  - `UnsupportedReplayReader`
- no crate surface binds the admitted blocked replay-side parse-attempt realization result to a
  concrete `ReplayInput`
- the admitted blocked result preserves only `source_replay` provenance, not a replay file path,
  replay bytes, or another parser-consumable replay handle

That matters because parser-success reopening is only honest if the next boundary can parse
something concrete rather than restate the already-known blocked state.

## F. DECISION

Decision chosen:

- reopen not justified yet

The exact v1 disposition for this pass is:

- `ParserImplementationRemainsClosedPendingReceiptBoundReplayInputAccessBoundary`

Parser-success / parser-implementation work is not justified yet because the remaining missing
piece is still narrower and earlier than parser logic itself:

- the admitted blocked result preserves `source_replay` only as opaque lineage
- the admitted blocked result does not preserve a replay file path
- the admitted blocked result does not preserve replay bytes
- the admitted blocked result does not preserve another parser-consumable replay handle
- the audited family root remains only the BC specimen-tree anchor and may not be reinterpreted as
  replay storage
- `mimir-replay` exposes replay input abstractions, but no admitted bridge from the blocked result
  into `ReplayInput`

Because of that, a parser-success contract consuming only the blocked replay-side parse-attempt
realization result would do one of two dishonest things:

- duplicate the current blocked replay-side parse-attempt boundary without adding a new executable
  parser-success surface
- invent replay-input-access semantics that are not present in the admitted input

So parser implementation remains closed in this pass.

### Evidence still missing

The missing evidence is exact:

- one honest receipt-bound replay input handle above the blocked replay-side parse-attempt result
- proof that such a handle preserves:
  - `lane_ordinal`
  - `specimen_ordinal`
  - `artifact_id`
  - `anchored_bc_specimen_file_path`
  - `source_raw_state_window_ref`
  - `source_slice_id`
  - `source_replay`
  - `source_subject`
  - `source_phase_id`
- proof that such a handle does not reinterpret the audited family root as replay storage
- proof that such a handle does not require silent sidecar/manifest/generic-index reopening
- proof that parser-success work could remain below raw-state payload, tensor, and control
  materialization

### Immediate next-step implication

The next pass must not be a parser-success contract-definition pass.

The next pass should instead answer a broader but still narrow question:

- whether one receipt-bound replay-input-access / replay-source-binding boundary must be
  deliberately reopened above the blocked replay-side parse-attempt realization result

That broader decision is now the minimum honest next step because the current repo still lacks the
parser-consumable replay handle that parser-success work would need.

## G. REPLAY-PARSING SUCCESS CONTRACT SHAPE V1

No replay-parsing success contract shape is defined in this pass.

Reason:

- reopening is not justified yet
- the admitted blocked result does not carry a receipt-bound replay input handle
- defining a contract shape here would either duplicate the current blocked replay-side
  parse-attempt boundary or invent replay-input semantics that are not present

## H. ADMISSION RULES

A replay-side parse-attempt realization result may enter this reopen-decision boundary only when
all of the following hold:

1. the input is exactly
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
2. `source_contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptOnly`
3. `source_contract_notes` still equal the exact replay-side parse-attempt contract note set
4. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
5. `source_chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
6. `realization_disposition == RealizedForTruthfulBlockedReplaySideParseAttemptOnly`
7. `realization_notes` still equal the exact blocked replay-side parse-attempt realization note set
8. `chosen_replay_parsing_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
9. `specimen_count > 0`
10. `group_count > 0`
11. `group_count` equals the number of preserved ordered lane results
12. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
13. `audited_family_root_directory` still exists as a directory at decision time
14. lane order and specimen order still match concrete lane/specimen position
15. each `consumed_replay_side_parse_attempt_input.anchored_bc_specimen_file_path` still remains
    receipt-bound below `audited_family_root_directory`
16. each `preserved_replay_side_parse_attempt_output_boundary` still matches the corresponding
    consumed replay-side parse-attempt input on:
    - `lane_ordinal`
    - `specimen_ordinal`
    - `artifact_id`
    - `anchored_bc_specimen_file_path`
    - `source_raw_state_window_ref`
    - `source_slice_id`
    - `source_replay`
    - `source_subject`
    - `source_phase_id`
17. each `preserved_replay_side_parse_attempt_output_boundary` still preserves:
    - `preserved_observation_binding_kind`
    - `preserved_accepted_reference_window`
18. each specimen still preserves
    `replay_side_parse_attempt_disposition == RealizedForTruthfulBlockedReplaySideParseAttemptOnly`
19. no lower boundary is silently reopened to repair or reinterpret the admitted blocked result

Admission here means only:

- this decision may rely on the blocked replay-side parse-attempt result as the last trusted
  pre-parser-success layer

Admission here does not mean:

- parser implementation is justified
- replay-side access succeeds
- replay parsing succeeds
- raw-state payload exists
- tensors or controls are available

## I. FAILURE RULES

This pass must hard-fail for:

- degraded replay-side parse-attempt realization input
- count/order/root/path drift
- any input/output-boundary identity drift
- duplicate or missing artifact ids
- any attempt to reinterpret the audited family root as replay storage
- any attempt to derive a replay path, replay bytes, or another replay handle from the admitted
  input without an explicit new boundary
- any attempt to widen this pass into actual replay parsing
- any attempt to widen this pass into actual raw-state payload materialization
- any attempt to widen this pass into tensor/control materialization
- any attempt to widen this pass into sidecars, manifests, generic indexing, or `mimir_export`

This pass must produce the explicit no-reopen decision when all of the following hold:

- all admission rules hold
- the current repo surface still shows no receipt-bound replay input handle above the admitted
  blocked result
- a parser-success contract would therefore either duplicate the blocked replay-side attempt
  boundary or invent missing replay-input semantics

This pass would produce a reopen-justified decision only if all of the following became true in a
future repo state:

- all admission rules still hold
- the admitted blocked result already carries, or an audited repo surface already exposes, one
  parser-consumable replay input handle above that result
- that handle remains low-boost-recovery-specific and receipt-bound
- that handle avoids sidecars/manifests/generic indexing unless separately reopened
- that handle avoids `mimir_export`
- that handle stays below raw-state payload, tensor, and control materialization

Those conditions are not satisfied in the current repo state.

## J. NON-GOALS

This pass does not do any of the following:

- no actual replay parsing implementation
- no actual raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof
- no sidecar/manifest realization
- no replay-input locator implementation
- no replay corpus ingestion
- no rollout or physics work

## K. RELATION TO NEXT STAGES

This pass now guarantees:

- the repo has an explicit answer to whether parser-success / parser-implementation work must be
  reopened above the blocked replay-side parse-attempt result
- that answer is negative in the current repo state
- the negative answer is tied to one exact cause:
  - no receipt-bound replay input handle exists above the admitted blocked result
- the audited family root still remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- replay-input access
- replay parsing success
- replay byte or replay frame access
- raw-state payload materialization
- tensor/control materialization

The immediate next pass should be:

- a deliberate broader reopen decision for one receipt-bound replay-input-access /
  replay-source-binding boundary above
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- implement replay parsing
- implement raw-state payload materialization
- reopen tensor/control materialization
- add sidecars/manifests unless separately proven necessary
