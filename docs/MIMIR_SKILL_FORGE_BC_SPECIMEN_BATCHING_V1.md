# MIMIR Skill Forge BC Specimen Batching / Orchestration Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded low-boost-recovery specimen batching / orchestration boundary on
top of the already-refined downstream consumer result.

It defines:

- one exact batching input boundary above `LowBoostRecoveryBcConsumerRefinementResultV1`
- one family-specific grouping rule
- one family-specific deterministic ordering rule
- one minimal batch/orchestration result surface
- one strict admission rule for when a refined specimen may enter batching
- one strict failure rule for malformed, duplicated, or drifted refined input

### Why it exists

The consumer-refinement pass proved that one low-boost-recovery BC specimen can be preserved as a
repo-local downstream result while still carrying:

- artifact identity
- source lineage
- accepted reference window
- carried confidence
- carried unresolved assumptions
- an explicit batching-only disposition

That still left one unresolved question:

- how multiple refined low-boost-recovery specimens should be grouped and ordered without
  widening into `mimir_export`, tensors, or controls

This pass exists to answer that question narrowly and explicitly.

### How it differs from adjacent stages

- Persisted-artifact handoff owns artifact-envelope admission and payload validation.
- Consumer refinement owns the first specimen-scoped downstream consumer result.
- This pass owns only multi-specimen grouping/order preservation on top of that refined result.
- Later work may define a family-specific layout/refinement stage above this batch result, but
  this pass does not.

This pass is not:

- consumer refinement
- `mimir_export` integration
- generic orchestration infrastructure
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

Batching/orchestration remains family-specific because:

- the admitted refined input already carries low-boost-recovery-specific observation semantics
- the admitted refined input already carries low-boost-recovery-specific target semantics
- the only justified grouping key is the low-boost-recovery source recovery context
- no second BC family exists yet to justify a shared batching/orchestration framework

No generic all-family batching abstraction is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcConsumerRefinementResultV1`

The batching/orchestration function consumes:

- `&[LowBoostRecoveryBcConsumerRefinementResultV1]`

Each admitted refined specimen must already preserve:

- `artifact_id`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `accepted_reference_variant_id`
- `observation_binding_kind`
- `supervision_window_role`
- `accepted_reference_window`
- `target_binding_kind`
- `carried_confidence_band`
- `carried_unresolved_assumptions`
- `consumer_disposition`
- `consumer_notes`

### Boundary rule

Direct batching input is no longer:

- raw persisted BC artifacts
- persisted-artifact handoffs
- BC rows
- accepted shells
- planning results

Those earlier boundaries are already frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcConsumerRefinementResultV1`.

## D. BATCHING / ORCHESTRATION ROLE

The first bounded batching/orchestration role is:

- group already-refined low-boost-recovery specimens by shared source recovery context
- impose one deterministic order across groups
- impose one deterministic order within each group
- preserve the refined specimen result unchanged inside the ordered batch output

### What this pass is allowed to group/order/preserve

This pass may:

- group specimens by shared source lineage fields
- preserve the full refined specimen payload inside each ordered group
- preserve the batching-only downstream disposition already carried by each specimen
- add one overall batch disposition that states only the next narrow layout-refinement step is
  justified

### What this pass is not allowed to materialize

This pass is not allowed to materialize:

- replay frames
- raw-state payloads behind `source_raw_state_window_ref`
- tensors
- feature vectors
- normalization outputs
- controls/actions
- labels
- `mimir_export` bundle state

## E. BATCH / ORCHESTRATION OUTPUT V1

The minimum batch/orchestration result is:

- `LowBoostRecoveryBcSpecimenBatchingResultV1`

It contains exactly:

- `specimen_count`
- `groups`
- `batching_disposition`

`batching_disposition` is fixed to exactly:

- `ready_for_low_boost_recovery_layout_refinement_only`

This means only:

- the ordered batch is acceptable input for one later low-boost-recovery-specific layout
  refinement step

It does not mean:

- ready for `mimir_export`
- ready for tensors
- ready for controls/actions
- usefulness proved

Each `groups` entry is:

- `LowBoostRecoveryBcSpecimenBatchGroupV1`

It contains exactly:

- `group_ordinal`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `specimens`

`specimens` is an ordered `Vec<LowBoostRecoveryBcConsumerRefinementResultV1>`.

That preserves:

- specimen identities through `artifact_id`
- lineage references through the preserved refined result and duplicated group key lineage
- accepted reference windows
- carried confidence
- carried unresolved assumptions
- the specimen-scoped batching-only disposition and notes

### Ordering fields

The deterministic order is the concrete order of:

- `groups` across the batch result
- `specimens` within each group

There is no separate metadata bag, manifest, or speculative summary surface in v1.

## F. ADMISSION RULES

A refined specimen may enter batching/orchestration only when all of the following hold:

1. the input item is `LowBoostRecoveryBcConsumerRefinementResultV1`
2. the preserved handoff-derived lineage fields remain present:
   - `artifact_id`
   - `source_slice_id`
   - `source_replay.replay_id`
   - `source_replay.provenance_label`
   - `source_subject`
   - `source_raw_state_window_ref`
   - `accepted_reference_variant_id`
3. `artifact_id == "<accepted_reference_variant_id>:bc_artifact_v1"`
4. `observation_binding_kind == accepted_reference_window_from_raw_state_window_ref`
5. `supervision_window_role == accepted_reference_variant_window`
6. `accepted_reference_window` remains a valid bounded window
7. `target_binding_kind == accepted_reference_variant_control_target_deferred`
8. `carried_confidence_band == boundary_stable`
9. `carried_unresolved_assumptions` remains the exact low-boost-recovery carried set
10. `consumer_disposition == ready_for_specimen_batching_only`
11. `consumer_notes` remains the exact low-boost-recovery consumer-refinement note set
12. every `artifact_id` in the admitted input slice is unique

Admission here means only:

- this refined specimen may be ordered into a low-boost-recovery-specific batch result

Admission here does not mean:

- data usefulness proved
- tensors or controls exist
- `mimir_export` compatibility proved

## G. ORDERING / GROUPING RULES

### Grouping rule

Refined specimens are grouped by the exact low-boost-recovery source recovery context:

- `source_replay.replay_id`
- `source_replay.provenance_label`
- `source_subject`
- `source_slice_id`
- `source_raw_state_window_ref`
- `source_phase_id`

If any one of those fields differs, the specimen belongs to a different group.

This is family-specific because it groups around the preserved low-boost-recovery recovery-context
lineage rather than around a generic dataset or export framework concept.

### Group order

Groups are ordered lexicographically by:

1. `source_replay.replay_id`
2. `source_replay.provenance_label`
3. `source_subject`
4. `source_slice_id`
5. `source_raw_state_window_ref`
6. `source_phase_id`

`group_ordinal` is the zero-based position of each group after that deterministic ordering.

### Specimen order within a group

Within one group, specimens are ordered lexicographically by:

1. `accepted_reference_window.start`
2. `accepted_reference_window.end_exclusive`
3. `accepted_reference_variant_id`
4. `artifact_id`

The concrete order of the `specimens` vector is the deterministic specimen order.

No inferred ranking, score, usefulness tier, or curriculum priority is added.

## H. FAILURE RULES

Batching/orchestration fails explicitly when any of the following occurs:

- the input slice is empty
- any refined specimen fails the admission rules above
- any refined specimen drifts from the exact consumer-refinement note/disposition set
- any refined specimen has malformed lineage or an invalid accepted reference window
- any duplicate `artifact_id` appears in the input

### Failure behavior

- no repair is allowed
- no inferred default is allowed
- no duplicate is silently deduplicated
- no malformed refined specimen is skipped
- no cross-group merge is forced

This pass must fail instead of repairing or inferring.

## I. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic multi-family batching/orchestration framework
- no tensor materialization
- no control/action extraction
- no replay parsing
- no replay ingestion
- no replay mining
- no rollout physics
- no async/background batching system
- no database work
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

The next pass now has one explicit low-boost-recovery batch/orchestration result that:

- starts strictly from refined consumer results
- preserves the refined specimen boundary unchanged inside each ordered group
- preserves source recovery-context lineage explicitly at the group level
- makes deterministic grouping and ordering concrete
- still does not widen into `mimir_export`

### What remains deferred

This pass still does not guarantee:

- a family-specific layout schema above the ordered groups
- `mimir_export` compatibility
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- a low-boost-recovery-specific layout/refinement pass above
  `LowBoostRecoveryBcSpecimenBatchingResultV1`
- still without `mimir_export` widening unless that separate decision is explicitly reopened
