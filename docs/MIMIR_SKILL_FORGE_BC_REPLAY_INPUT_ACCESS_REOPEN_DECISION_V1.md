# MIMIR Skill Forge BC Replay-Input-Access Reopen Decision v1

## A. PURPOSE

### What this pass owns

This pass owns exactly one broader reopen-decision question above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`

It defines:

- whether one receipt-bound replay-input-access / replay-source-binding boundary must now be
  deliberately reopened at all
- the exact criteria used to answer that question
- the narrowest honest next contract shape only if reopening is justified

### Why it exists

The boundary below this pass already fixed the current truthful limit:

- `RealizedForTruthfulBlockedReplaySideParseAttemptOnly`

The parser-success reopen decision above that blocked result already rejected parser work directly:

- `ParserImplementationRemainsClosedPendingReceiptBoundReplayInputAccessBoundary`

That rejection isolated one earlier missing piece:

- the blocked replay-side parse-attempt realization result preserves lineage but carries no
  parser-consumable replay handle

This pass exists to answer whether that earlier missing piece now must be reopened explicitly.

### How it differs from the parser-success no-reopen decision below it

- The parser-success no-reopen decision proves parser implementation is still too early.
- This pass does not reopen parser implementation.
- This pass decides whether one narrower replay-input-access / replay-source-binding boundary must
  be reopened first.
- This pass is still not replay parsing and still not replay-input locator implementation.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this reopen-decision version.

This decision remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
- the preserved lineage tuple is only the low-boost-recovery BC specimen tuple already carried by
  that result
- the audited family root reference is still only the low-boost-recovery BC specimen-tree anchor
- no second family exists that would justify a shared replay-input-access / replay-source-binding
  framework

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
- replay-parsing success reopen decisions below this layer
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

- should one receipt-bound replay-input-access / replay-source-binding boundary now be
  deliberately reopened above the truthful blocked replay-side parse-attempt boundary

This question exists only because the parser-success reopen was already rejected for one exact
reason:

- the blocked replay-side parse-attempt realization result carries no parser-consumable replay
  input handle

That means the unresolved gap is no longer whether replay-side parse-attempt truth is explicit or
whether parser implementation should be reopened directly.

The unresolved gap is narrower:

- whether the repo now needs one explicit replay-input-access / replay-source-binding boundary that
  binds the preserved receipt-bound lineage tuple to one future parser-consumable replay handle

This is still not replay parsing and still not replay-input locator implementation.

## E. REOPEN CRITERIA

Reopening is justified only if all of the following hold:

1. the remaining missing piece is truly replay-input-access / replay-source-binding and not
   another lower-layer defect already below the blocked replay-side attempt boundary
2. the next boundary can stay low-boost-recovery-specific
3. the next boundary can stay strictly receipt-bound
4. the next boundary can avoid sidecars, manifests, and generic indexing because no current
   admitted evidence proves they are required for the binding defect itself
5. the next boundary can avoid `mimir_export` because the defect path remains entirely inside the
   low-boost-recovery receipt-bound BC lineage
6. the next boundary can stay below replay parsing success
7. the next boundary can stay below actual raw-state payload materialization, tensor
   materialization, and control/action materialization
8. the next boundary can introduce one parser-consumable replay handle or equally narrow
   replay-source-binding handle without inventing semantics absent from the admitted blocked result
   by making that handle a new explicit contract output bound to the preserved lineage tuple rather
   than an implicit derivation from `source_replay`, `provenance_label`, or the audited family root

The current repo audit satisfies those criteria.

What the audit still does not show is any existing bound replay handle above the blocked result.

That is exactly why reopening is needed.

## F. DECISION

The decision in v1 is:

- reopen justified for one narrow receipt-bound replay-input-access / replay-source-binding
  boundary

### Why reopening is justified

Reopening is justified because the parser-success no-reopen decision already isolated the missing
piece precisely:

- no parser-consumable replay handle exists above the blocked replay-side parse-attempt result

The current repo also already preserves enough trustworthy receipt-bound identity to define one
contract for that missing piece without widening architecture:

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
- the audited family root directory reference

That means the minimum honest reopen is not parser implementation, not replay locator
implementation, and not sidecar/manifest work.

It is one contract that binds the preserved receipt-bound lineage tuple to one future
parser-consumable replay handle or equally narrow replay-source-binding handle.

### Narrowest honest next boundary shape

The narrowest honest next boundary shape is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`

### What it would consume

It would consume only:

- the admitted blocked replay-side parse-attempt realization result
- the audited family root directory reference already preserved by that result

### What it would expose

It would expose exactly one contract-only output per admitted specimen:

- one receipt-bound replay-input-access / replay-source-binding output that preserves the exact
  lineage tuple and binds it to one future parser-consumable replay handle or equally narrow
  replay-source-binding handle

### What remains deferred

This decision still defers:

- actual replay-input locator implementation
- actual replay parsing
- actual raw-state payload materialization
- tensor materialization
- control/action extraction
- sidecar/manifest realization
- generic indexing
- `mimir_export`

### Why this is the minimum honest reopen

This is the minimum honest reopen because:

- the blocked replay-side parse-attempt result is already truthful and explicit
- parser-success work is already proven too early without a bound handle
- `source_replay` remains opaque lineage only
- the audited family root remains only a BC specimen-tree anchor
- no current evidence proves that sidecars, manifests, generic indexing, or `mimir_export` belong
  in the missing defect path

## G. REPLAY-INPUT-ACCESS / SOURCE-BINDING CONTRACT SHAPE V1

The contract name is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`

### Exact inputs it would consume from the blocked replay-side parse-attempt realization result

For one admitted specimen, the contract would consume exactly:

- `audited_family_root_directory`
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

### Exact replay-input-access / replay-source-binding output boundary it would expose

The contract would expose exactly one per-specimen output boundary that preserves:

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

and adds exactly one new bound element:

- one receipt-bound replay-input-access / replay-source-binding handle whose only admitted meaning
  is that this exact preserved lineage tuple has been bound to one future parser-consumable replay
  handle

This contract shape deliberately does not choose whether that later parser-consumable handle is
file-backed, byte-backed, or realized through another equally narrow binding step.

### Exact invariant

The exact invariant is:

- for one admitted low-boost-recovery blocked replay-side parse-attempt specimen, the tuple
  (`artifact_id`, `anchored_bc_specimen_file_path`, `source_raw_state_window_ref`,
  `source_slice_id`, `source_replay`, `source_subject`, `source_phase_id`) plus preserved
  receipt-bound lane/specimen ordinals and preserved deferred observation lineage binds to exactly
  one honest replay-input-access / replay-source-binding handle
- that handle is authoritative only for this exact preserved tuple
- that handle must not silently rewrite or drop any preserved lineage field
- that handle must not reinterpret `source_replay.provenance_label` as a path contract
- that handle must not reinterpret `audited_family_root_directory` as replay storage

### Exact relationship to deferred observation access

The relationship to deferred observation access remains narrow:

- `preserved_observation_binding_kind` and `preserved_accepted_reference_window` stay preserved as
  deferred lineage only
- the replay-input-access / source-binding contract does not reopen observation materialization
- the contract only guarantees that the preserved deferred observation lineage stays attached to
  the same specimen while replay-input access is bound

### What it explicitly refuses to promise

This contract explicitly refuses to promise:

- actual replay-input locator implementation
- actual replay parsing
- replay frames
- replay bytes
- a replay file path derivation from `source_replay`
- a replay storage derivation from `audited_family_root_directory`
- actual raw-state payload materialization
- tensor materialization
- control/action extraction
- sidecar/manifest realization
- generic index semantics
- `mimir_export` integration

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
7. `realization_notes` still equal the exact blocked replay-side parse-attempt realization note
   set
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
17. each specimen still preserves
    `replay_side_parse_attempt_disposition == RealizedForTruthfulBlockedReplaySideParseAttemptOnly`
18. no lower boundary is silently reopened to repair or reinterpret the admitted blocked result

Admission here means only:

- this reopen question may rely on the blocked replay-side parse-attempt result as the last
  trusted pre-replay-input-access layer

Admission here does not mean:

- replay-input access is implemented
- replay parsing succeeds
- replay files or replay bytes are available
- raw-state payload exists
- tensors or controls are available

## I. FAILURE RULES

This pass must hard-fail for:

- degraded replay-side parse-attempt realization input
- count/order/root/path drift
- duplicate or missing artifact ids
- any input/output-boundary identity drift
- any attempt to reinterpret `source_replay` or `provenance_label` as an implicit replay path
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen this pass into actual replay-input locator implementation
- any attempt to widen this pass into actual replay parsing
- any attempt to widen this pass into actual raw-state payload materialization
- any attempt to widen this pass into tensor/control materialization
- any attempt to widen this pass into sidecars, manifests, generic indexing, or `mimir_export`

This v1 pass produces `reopen justified` when all admission rules hold.

There is no valid-input `no reopen` output in v1.

That is deliberate.

For valid admitted input, the current repo state already proves all of the following:

- parser implementation is still closed directly
- the missing defect is one earlier replay-input-access / source-binding boundary
- the preserved lineage tuple is already sufficient to define that boundary narrowly

Anything weaker would only restate the already-known blocked state without isolating the missing
contract the next pass actually needs.

## J. NON-GOALS

This pass does not do any of the following:

- no actual replay-input locator implementation
- no actual replay parsing
- no actual raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof
- no replay corpus ingestion
- no rollout or physics work
- no async/background system
- no database work

## K. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- the replay-input-access / replay-source-binding reopen decision is explicit and auditable
- the decision stays low-boost-recovery-specific
- the decision stays receipt-bound
- the narrowest honest next contract shape is fixed:
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`
- parser work remains closed until a bound handle contract exists
- sidecars, manifests, generic indexing, and `mimir_export` remain outside the admitted fix

### What remains deferred

This pass still does not guarantee:

- replay-input access is implemented
- replay parsing succeeds
- raw-state payload is materialized
- tensors or controls exist
- sidecars or manifests are required

### Immediate next-stage implication

The immediate next pass should be:

- one first narrow contract-definition pass for
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputAccessSourceBindingContractV1`
- still above
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySideParseAttemptRealizationResultV1`
- still without actual replay-input locator implementation
- still without actual replay parsing
- still without `mimir_export` widening unless that separate boundary is explicitly reopened
