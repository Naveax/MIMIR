# MIMIR Skill Forge BC Export Layout / Refinement Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded low-boost-recovery export-layout / refinement boundary on top of
the already-deterministic specimen batching result.

It defines:

- one exact layout/refinement input boundary above `LowBoostRecoveryBcSpecimenBatchingResultV1`
- one exact first layout/refinement role
- one minimal family-specific layout/refinement result surface
- one strict admission rule for when a batching result may enter layout/refinement
- one strict failure rule for malformed, drifted, or reordered batching content

### Why it exists

The specimen batching pass already fixed:

- refined specimen admission
- grouping by shared low-boost-recovery source recovery context
- deterministic order across groups
- deterministic order within each group
- preservation of lineage, accepted reference windows, confidence, and unresolved assumptions

That still left one unresolved question:

- what minimal low-boost-recovery-specific export layout should exist above those ordered groups
  before any downstream export consumer, `mimir_export`, tensor work, or control extraction is
  reopened

This pass exists to answer that question narrowly and explicitly.

### How it differs from adjacent stages

- Consumer refinement owns specimen-scoped downstream admission.
- Specimen batching owns grouping and deterministic ordering.
- This pass owns only the first logical layout shape above the already-ordered groups.
- A later pass may define a downstream family-specific export consumer on top of this layout, but
  this pass does not.

This pass is not:

- specimen batching/orchestration
- `mimir_export` integration
- file/directory/manifest materialization
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

Export-layout/refinement remains family-specific because:

- the admitted batching result already carries low-boost-recovery-specific observation semantics
- the admitted batching result already carries low-boost-recovery-specific target semantics
- the only justified logical layout unit is the low-boost-recovery source recovery context
- no second BC family exists yet to justify a shared export-layout framework

No generic all-family export-layout framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcSpecimenBatchingResultV1`

Within that batching result, this pass consumes:

- `specimen_count`
- `groups`
- `batching_disposition`

Each admitted `groups` entry already preserves:

- `group_ordinal`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- ordered `specimens: Vec<LowBoostRecoveryBcConsumerRefinementResultV1>`

### Boundary rule

Direct layout/refinement input is no longer:

- refined specimens by themselves
- persisted-artifact handoffs
- persisted low-boost-recovery BC artifacts
- BC rows
- accepted shells
- planning results

Those earlier boundaries are already frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcSpecimenBatchingResultV1`.

## D. EXPORT-LAYOUT / REFINEMENT ROLE

The first bounded export-layout / refinement role is:

- revalidate the already-batched result without regrouping or resorting it
- preserve each ordered batch group as one ordered logical recovery-context lane
- preserve the full refined specimen payload unchanged inside each lane
- add one explicit layout-only downstream disposition and bounded layout notes

### What this pass is allowed to arrange/preserve

This pass may:

- preserve `specimen_count`
- preserve the concrete group order
- preserve each `group_ordinal`
- preserve each group's low-boost-recovery recovery-context lineage
- preserve specimen order inside each group exactly as admitted by batching
- represent each preserved group as one ordered recovery-context lane

### What this pass is not allowed to materialize

This pass is not allowed to materialize:

- replay frames
- raw state behind `source_raw_state_window_ref`
- filesystem paths
- directories
- manifests
- `mimir_export` bundle state
- tensors
- feature vectors
- controls/actions
- labels

## E. LAYOUT / REFINEMENT OUTPUT V1

The minimum layout/refinement result is:

- `LowBoostRecoveryBcExportLayoutResultV1`

It contains exactly:

- `specimen_count`
- `group_count`
- `source_batching_disposition`
- `ordered_recovery_context_lanes`
- `layout_disposition`
- `layout_notes`

### Preserved batch identity/count context

The preserved batch identity/count context is exactly:

- `specimen_count`
- `group_count`
- `source_batching_disposition`

No synthetic batch id is introduced because the batching boundary did not create one.

### Ordered lane shape

Each `ordered_recovery_context_lanes` entry is:

- `LowBoostRecoveryBcExportLayoutLaneV1`

It contains exactly:

- `source_group_ordinal`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `specimens`

`specimens` remains an ordered `Vec<LowBoostRecoveryBcConsumerRefinementResultV1>`.

### Layout disposition

`layout_disposition` is fixed to exactly:

- `ready_for_low_boost_recovery_downstream_export_consumer_only`

That means only:

- the logical lane layout is acceptable input for one later low-boost-recovery-specific downstream
  export-consumer boundary

It does not mean:

- ready for `mimir_export`
- ready for file emission
- ready for tensors
- ready for controls/actions
- usefulness proved

### Layout notes

`layout_notes` are fixed to exactly:

- `batching_boundary_preserved`
- `recovery_context_lane_layout_only`
- `tensor_and_control_materialization_deferred`
- `mimir_export_integration_deferred`

There is no generic metadata bag.

## F. LAYOUT RULES

### One lane per preserved ordered group

Layout/refinement is one-to-one with the already-admitted ordered groups:

- each batching `groups[i]` becomes exactly one `ordered_recovery_context_lanes[i]`
- `source_group_ordinal` must equal the incoming `group_ordinal`
- lane vector order must remain the incoming group order

### Lane lineage preservation

Each lane preserves exactly the same recovery-context lineage as its source group:

- `source_replay`
- `source_subject`
- `source_slice_id`
- `source_raw_state_window_ref`
- `source_phase_id`

### Specimen preservation inside a lane

Within one lane:

- `specimens` must preserve the exact incoming specimen vector order
- no regrouping is allowed
- no resorting is allowed
- no flattening is allowed
- no specimen payload reshaping is allowed

This is a logical lane layout only. It is not a filesystem or bundle layout.

## G. ADMISSION RULES

A batching result may enter layout/refinement only when all of the following hold:

1. the input is `LowBoostRecoveryBcSpecimenBatchingResultV1`
2. `batching_disposition == ready_for_low_boost_recovery_layout_refinement_only`
3. `specimen_count > 0`
4. `groups` is non-empty
5. `specimen_count` equals the number of preserved specimens across all groups
6. every `group_ordinal` matches its concrete position in `groups`
7. groups remain in the exact batching order:
   - `source_replay.replay_id`
   - `source_replay.provenance_label`
   - `source_subject`
   - `source_slice_id`
   - `source_raw_state_window_ref`
   - `source_phase_id`
8. every group contains at least one preserved refined specimen
9. every preserved specimen still satisfies the batching admission invariants
10. every specimen remains aligned with its enclosing group lineage
11. specimen order within each group remains the exact batching order:
    - `accepted_reference_window.start`
    - `accepted_reference_window.end_exclusive`
    - `accepted_reference_variant_id`
    - `artifact_id`
12. every `artifact_id` remains unique across the full batching result

Admission here means only:

- this ordered batch may be preserved as a logical low-boost-recovery recovery-context lane layout

Admission here does not mean:

- downstream consumer usefulness proved
- `mimir_export` compatibility proved
- tensors or controls exist

## H. FAILURE RULES

Layout/refinement fails explicitly when any admission invariant above is violated.

Fail when:

- `batching_disposition` drifts
- `specimen_count` drifts
- `groups` is empty
- any `group_ordinal` drifts from concrete order
- group order drifts
- a group is empty
- any preserved specimen is malformed
- any specimen no longer matches its enclosing group lineage
- specimen order within a group drifts
- any duplicate `artifact_id` appears

### Failure behavior

- no regrouping is allowed
- no resorting is allowed
- no inferred fallback lane is allowed
- no specimen is skipped
- no synthetic batch id is invented
- no missing lineage is repaired

This pass must fail instead of repairing or inferring.

## I. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic multi-family export-layout framework
- no file/directory/manifest materialization
- no tensor materialization
- no control/action extraction
- no replay parsing
- no replay ingestion
- no replay mining
- no rollout or physics work
- no async/background system
- no database work
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

The next pass now has one explicit low-boost-recovery export-layout result that:

- starts strictly from `LowBoostRecoveryBcSpecimenBatchingResultV1`
- preserves the batching boundary instead of reopening it
- preserves ordered groups as ordered logical recovery-context lanes
- preserves specimen order and payloads unchanged inside each lane
- still does not widen into `mimir_export`

### What remains deferred

This pass still does not guarantee:

- a downstream family-specific export-consumer boundary
- any `mimir_export` wiring
- any filesystem layout or manifest emission
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- one low-boost-recovery-specific downstream export-consumer boundary above
  `LowBoostRecoveryBcExportLayoutResultV1`
- still without `mimir_export` widening unless that separate decision is explicitly reopened
