# MIMIR Skill Forge BC Downstream Export Consumer Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded low-boost-recovery downstream export-consumer boundary on top of
the already-refined export-layout result.

It defines:

- one exact downstream export-consumer input boundary above `LowBoostRecoveryBcExportLayoutResultV1`
- one exact first downstream export-consumer role
- one minimal family-specific downstream export-consumer result surface
- one strict admission rule for when an export-layout result may enter that boundary
- one strict failure rule for malformed, drifted, or reordered layout content

### Why it exists

The export-layout pass already fixed:

- strict input from `LowBoostRecoveryBcSpecimenBatchingResultV1`
- preserved ordered recovery-context lanes
- preserved specimen order inside each lane
- preserved lineage, accepted reference windows, confidence, and unresolved assumptions
- layout-only downstream disposition and notes

That still left one unresolved question:

- what the first downstream export consumer is actually allowed to inspect from those preserved
  lanes before any family-specific filesystem emission work or any deliberate `mimir_export`
  reopen

This pass exists to answer that question narrowly and explicitly.

### How it differs from adjacent stages

- Export-layout/refinement owns the first logical lane shape above ordered groups.
- This pass owns the first downstream consumer admission and preservation boundary above that
  logical lane shape.
- A later pass may define a low-boost-recovery-specific filesystem/export-emission refinement on
  top of this consumer result, but this pass does not.

This pass is not:

- export-layout/refinement
- `mimir_export` integration
- filesystem bundle or manifest emission
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

Downstream export-consumer work remains family-specific because:

- the admitted input already carries low-boost-recovery-specific observation semantics
- the admitted input already carries low-boost-recovery-specific target semantics
- the only justified logical downstream unit is the preserved low-boost-recovery recovery-context
  lane
- no second BC family exists yet to justify a shared downstream export-consumer framework

No generic all-family downstream export-consumer abstraction is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcExportLayoutResultV1`

Within that layout result, this pass consumes:

- `specimen_count`
- `group_count`
- `source_batching_disposition`
- `ordered_recovery_context_lanes`
- `layout_disposition`
- `layout_notes`

### Boundary rule

Direct downstream export-consumer input is no longer:

- specimen batches by themselves
- refined specimens by themselves
- persisted-artifact handoffs
- persisted low-boost-recovery BC artifacts
- BC rows
- accepted shells
- planning results

Those earlier boundaries are already frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcExportLayoutResultV1`.

## D. FIRST DOWNSTREAM EXPORT-CONSUMER ROLE

The first bounded downstream export-consumer role is:

- admit only already-laid-out low-boost-recovery recovery-context lanes
- revalidate that the export-layout boundary is still intact without reshaping it
- preserve those ordered lanes unchanged as the downstream consumer-owned result
- mark the result ready only for a later low-boost-recovery filesystem/export-emission refinement

### What it is allowed to inspect from ordered recovery-context lanes

The first downstream export consumer may inspect only:

- preserved batch/layout counts
- source layout disposition and notes
- the concrete lane order
- `source_group_ordinal`
- preserved recovery-context lineage per lane:
  - `source_slice_id`
  - `source_replay`
  - `source_subject`
  - `source_raw_state_window_ref`
  - `source_phase_id`
- preserved specimen order within each lane
- per-specimen audit identity and accepted reference lineage:
  - `artifact_id`
  - `accepted_reference_variant_id`
  - `accepted_reference_window`
- carried confidence
- carried unresolved assumptions

### What it is not allowed to materialize yet

This pass is not allowed to materialize:

- replay frames or parsed replay payloads
- raw state behind `source_raw_state_window_ref`
- filesystem paths, directories, manifests, or bundle files
- tensors, feature vectors, or normalization outputs
- controls, actions, or labels
- `mimir_export` bundle state

Its role is downstream admission and preservation only, not emission or materialization.

## E. DOWNSTREAM EXPORT-CONSUMER OUTPUT V1

The minimum downstream export-consumer result is:

- `LowBoostRecoveryBcDownstreamExportConsumerResultV1`

It contains exactly:

- `specimen_count`
- `group_count`
- `source_layout_disposition`
- `source_layout_notes`
- `preserved_recovery_context_lanes`
- `consumer_disposition`
- `consumer_notes`

### Preserved layout context

The preserved layout context is exactly:

- `specimen_count`
- `group_count`
- `source_layout_disposition`
- `source_layout_notes`

### Preserved lane shape

`preserved_recovery_context_lanes` remains:

- `Vec<LowBoostRecoveryBcExportLayoutLaneV1>`

No new lane DTO is introduced in v1. Each preserved lane still carries exactly:

- `source_group_ordinal`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- ordered `specimens: Vec<LowBoostRecoveryBcConsumerRefinementResultV1>`

That preserves:

- ordered recovery-context lanes
- specimen ordering inside each lane
- lineage through lane fields and specimen fields
- accepted reference windows
- carried confidence
- carried unresolved assumptions

### Bounded downstream disposition

`consumer_disposition` is fixed to exactly:

- `ready_for_low_boost_recovery_filesystem_export_emission_refinement_only`

That means only:

- the preserved downstream consumer result is acceptable input for one later
  low-boost-recovery-specific filesystem/export-emission refinement pass

It does not mean:

- ready for actual filesystem writes
- ready for `mimir_export`
- ready for tensors
- ready for controls/actions
- usefulness proved

### Bounded downstream notes

`consumer_notes` are fixed to exactly:

- `export_layout_boundary_preserved`
- `recovery_context_lane_inspection_only`
- `filesystem_emission_deferred`
- `tensor_and_control_materialization_deferred`
- `mimir_export_integration_deferred`

There is no generic metadata bag.

## F. ADMISSION RULES

An export-layout result may enter this downstream export-consumer boundary only when all of the
following hold:

1. the input is `LowBoostRecoveryBcExportLayoutResultV1`
2. `source_batching_disposition == ready_for_low_boost_recovery_layout_refinement_only`
3. `layout_disposition == ready_for_low_boost_recovery_downstream_export_consumer_only`
4. `specimen_count > 0`
5. `group_count > 0`
6. `ordered_recovery_context_lanes` is non-empty
7. `group_count` equals the number of preserved recovery-context lanes
8. `layout_notes` remains the exact low-boost-recovery export-layout note set
9. every `source_group_ordinal` matches the concrete lane position
10. lanes remain in the exact export-layout order:
    - `source_replay.replay_id`
    - `source_replay.provenance_label`
    - `source_subject`
    - `source_slice_id`
    - `source_raw_state_window_ref`
    - `source_phase_id`
11. every preserved lane contains at least one preserved refined specimen
12. every preserved specimen still satisfies the batching admission invariants
13. every specimen remains aligned with its enclosing lane lineage
14. specimen order within each lane remains the exact export-layout order:
    - `accepted_reference_window.start`
    - `accepted_reference_window.end_exclusive`
    - `accepted_reference_variant_id`
    - `artifact_id`
15. every `artifact_id` remains unique across the full layout result
16. `specimen_count` equals the number of preserved specimens across all lanes

Admission here means only:

- this preserved export-layout result may be preserved as one downstream consumer-owned
  low-boost-recovery lane set

Admission here does not mean:

- filesystem emission is implemented
- `mimir_export` compatibility is proved
- tensors or controls exist

## G. FAILURE / DEFER RULES

The downstream export-consumer boundary fails explicitly when any admission invariant above is
violated.

Fail when:

- source batching disposition drifts
- layout disposition drifts
- counts drift
- layout notes drift
- lane order drifts
- lane ordinals drift
- a lane is empty
- a preserved specimen is malformed
- a specimen no longer matches its enclosing lane lineage
- specimen order within a lane drifts
- any duplicate `artifact_id` appears

### Failure behavior

- no repair is allowed
- no inferred fallback lane is allowed
- no regrouping is allowed
- no resorting is allowed
- no specimen is skipped
- no filesystem hint is invented

### Defer behavior

There is no soft defer path in v1.

This is deliberate. The export-layout boundary already fixed the only honest uncertainty this pass
is allowed to preserve, and that uncertainty is already carried explicitly in the preserved
specimen unresolved-assumption fields. This pass adds no new evidence gate that would justify a
separate defer disposition.

## H. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic multi-family downstream export-consumer framework
- no filesystem bundle or manifest emission
- no tensor materialization
- no control/action extraction
- no usefulness proof
- no policy-improvement proof
- no replay parsing
- no replay ingestion
- no replay mining
- no rollout or physics work
- no async/background system
- no database work

## I. RELATION TO NEXT STAGES

### What this pass now guarantees

The next pass now has one explicit low-boost-recovery downstream export-consumer result that:

- starts strictly from `LowBoostRecoveryBcExportLayoutResultV1`
- preserves the layout boundary instead of reopening batching or lower BC stages
- preserves ordered recovery-context lanes unchanged as the consumer-owned result
- preserves specimen order, lineage, accepted reference windows, confidence, and unresolved
  assumptions inside each lane
- marks the result ready only for family-specific filesystem/export-emission refinement
- still does not widen into `mimir_export`

### What remains deferred

This pass still does not guarantee:

- actual filesystem emission
- manifests or bundle directories
- any `mimir_export` wiring
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- one low-boost-recovery-specific filesystem/export-emission refinement pass above
  `LowBoostRecoveryBcDownstreamExportConsumerResultV1`
- still without `mimir_export` widening unless that separate decision is explicitly reopened
