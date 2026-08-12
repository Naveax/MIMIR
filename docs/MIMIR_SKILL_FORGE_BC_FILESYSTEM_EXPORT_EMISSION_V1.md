# MIMIR Skill Forge BC Filesystem / Export-Emission Refinement Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded low-boost-recovery filesystem / export-emission refinement
boundary on top of the already-preserved downstream export-consumer result.

It defines:

- one exact filesystem / export-emission refinement input boundary above
  `LowBoostRecoveryBcDownstreamExportConsumerResultV1`
- one exact first deterministic family-specific filesystem / export-emission planning role
- one minimal family-specific planning result surface
- one strict admission rule for when a downstream export-consumer result may enter this boundary
- one strict failure rule for malformed, drifted, or reordered downstream consumer content

### Why it exists

The downstream export-consumer pass already fixed:

- strict input from `LowBoostRecoveryBcExportLayoutResultV1`
- preserved ordered recovery-context lanes
- preserved specimen order inside each lane
- preserved lineage, accepted reference windows, confidence, and unresolved assumptions
- downstream-consumer-only disposition and notes

That still left one unresolved question:

- what the first deterministic low-boost-recovery filesystem / export-emission planning shape
  should be above that preserved downstream result before any actual filesystem writes, any
  `mimir_export` reopen, or any tensor/control work

This pass exists to answer that question narrowly and explicitly.

### How it differs from adjacent stages

- Downstream export-consumer owns admission and preservation above the logical export-layout result.
- This pass owns only deterministic family-specific filesystem / export-emission planning.
- A later pass may materialize that plan to the filesystem, but this pass does not.

This pass is not:

- downstream export-consumer admission
- actual filesystem emission
- `mimir_export` integration
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

Filesystem / export-emission refinement remains family-specific because:

- the admitted downstream result already carries low-boost-recovery-specific observation semantics
- the admitted downstream result already carries low-boost-recovery-specific target semantics
- the preserved unit is still the low-boost-recovery recovery-context lane
- the first deterministic filesystem planning shape is still tied to that lane concept
- no second BC family exists yet to justify a shared filesystem / export-emission framework

No generic all-family filesystem / export-emission framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcDownstreamExportConsumerResultV1`

Within that consumer result, this pass consumes:

- `specimen_count`
- `group_count`
- `source_layout_disposition`
- `source_layout_notes`
- `preserved_recovery_context_lanes`
- `consumer_disposition`
- `consumer_notes`

### Boundary rule

Direct filesystem / export-emission refinement input is no longer:

- export-layout results by themselves
- specimen batches by themselves
- refined specimens by themselves
- persisted-artifact handoffs
- persisted low-boost-recovery BC artifacts
- BC rows
- accepted shells
- consumer-planning results

Those earlier boundaries are already frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcDownstreamExportConsumerResultV1`.

## D. FILESYSTEM / EXPORT-EMISSION REFINEMENT ROLE

The first bounded filesystem / export-emission refinement role is:

- admit only already-preserved low-boost-recovery downstream consumer lanes
- revalidate that the downstream consumer boundary is still intact without reshaping it
- preserve each ordered recovery-context lane unchanged
- derive one deterministic family root directory name
- derive one deterministic lane-directory name per preserved lane
- derive one deterministic specimen file-stem plan per preserved specimen inside each lane
- mark the result ready only for one later low-boost-recovery-specific actual filesystem emission
  boundary

### What it is allowed to arrange / plan

This pass may:

- preserve `specimen_count`
- preserve `group_count`
- preserve downstream-consumer disposition and notes
- preserve ordered recovery-context lanes unchanged
- preserve specimen order inside each lane unchanged
- derive one fixed family root directory token:
  - `low_boost_recovery_bc_v1`
- derive one fixed lane-directory pattern relative to that root:
  - `recovery_context_lane_{lane_ordinal:04}`
- derive one fixed specimen file-stem pattern inside each lane:
  - `specimen_{specimen_ordinal:04}`

### What it is not allowed to materialize or emit yet

This pass is not allowed to materialize or emit:

- directories on disk
- files on disk
- file extensions
- manifests or bundle indexes
- replay frames or parsed replay payloads
- raw state behind `source_raw_state_window_ref`
- tensors, feature vectors, or normalization outputs
- controls, actions, or labels
- `mimir_export` bundle state

The role here is deterministic planning only, not actual emission.

## E. FILESYSTEM / EXPORT-EMISSION REFINEMENT OUTPUT V1

The minimum filesystem / export-emission planning result is:

- `LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`

It contains exactly:

- `specimen_count`
- `group_count`
- `source_consumer_disposition`
- `source_consumer_notes`
- `planned_family_root_directory`
- `planned_recovery_context_lanes`
- `refinement_disposition`
- `refinement_notes`

### Preserved downstream context

The preserved downstream context is exactly:

- `specimen_count`
- `group_count`
- `source_consumer_disposition`
- `source_consumer_notes`

### Family root planning field

`planned_family_root_directory` is fixed to exactly:

- `low_boost_recovery_bc_v1`

This is a deterministic root planning token only. It does not create a directory.

### Lane-level emission planning shape

Each `planned_recovery_context_lanes` entry is:

- `LowBoostRecoveryBcFilesystemExportEmissionLanePlanV1`

It contains exactly:

- `lane_ordinal`
- `planned_relative_lane_directory`
- `preserved_lane`
- `ordered_specimen_plans`

`preserved_lane` remains:

- `LowBoostRecoveryBcExportLayoutLaneV1`

That preserves:

- `source_group_ordinal`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- ordered `specimens: Vec<LowBoostRecoveryBcConsumerRefinementResultV1>`

### Specimen-level emission planning shape

Each `ordered_specimen_plans` entry is:

- `LowBoostRecoveryBcFilesystemExportEmissionSpecimenPlanV1`

It contains exactly:

- `specimen_ordinal`
- `artifact_id`
- `planned_specimen_file_stem`

This preserves specimen order through the vector order and the explicit ordinal while keeping the
full refined specimen payload inside `preserved_lane.specimens`.

### Bounded refinement disposition

`refinement_disposition` is fixed to exactly:

- `ready_for_low_boost_recovery_filesystem_emission_boundary_only`

That means only:

- the deterministic plan is acceptable input for one later low-boost-recovery-specific actual
  filesystem emission boundary

It does not mean:

- ready for actual filesystem writes now
- ready for `mimir_export`
- ready for tensors
- ready for controls/actions
- usefulness proved

### Bounded refinement notes

`refinement_notes` are fixed to exactly:

- `downstream_export_consumer_boundary_preserved`
- `recovery_context_lane_filesystem_emission_plan_only`
- `actual_filesystem_emission_deferred`
- `tensor_and_control_materialization_deferred`
- `mimir_export_integration_deferred`

There is no generic metadata bag.

## F. EMISSION-PLANNING RULES

### Root planning rule

The root planning token is always:

- `low_boost_recovery_bc_v1`

No alternative root naming is inferred from replay ids, subjects, or external configuration in
v1.

### One lane plan per preserved lane

Filesystem / export-emission refinement is one-to-one with the already-preserved ordered lanes:

- each `preserved_recovery_context_lanes[i]` becomes exactly one `planned_recovery_context_lanes[i]`
- `lane_ordinal` must equal the concrete lane position
- `preserved_lane.source_group_ordinal` must remain unchanged
- lane-plan vector order must remain the downstream consumer lane order

### Lane directory derivation rule

Each lane-directory name is derived only from the concrete lane ordinal:

- `planned_relative_lane_directory = format!("recovery_context_lane_{lane_ordinal:04}")`

No replay id, subject id, slice id, phase id, or artifact id is embedded into the directory name
in v1. That avoids invented filesystem sanitization rules and keeps the planning shape narrow.

### Specimen planning rule inside one lane

Within one lane:

- `ordered_specimen_plans[j]` corresponds exactly to `preserved_lane.specimens[j]`
- `specimen_ordinal` must equal the concrete specimen position in that lane
- `artifact_id` must equal the preserved specimen `artifact_id`
- `planned_specimen_file_stem = format!("specimen_{specimen_ordinal:04}")`

### What is deliberately deferred from path planning

This pass does not decide:

- file extensions
- manifest file names
- lane descriptor file names
- payload encoding
- cross-family directory structure

Those choices stay deferred to the next explicit pass.

## G. ADMISSION RULES

A downstream export-consumer result may enter this refinement boundary only when all of the
following hold:

1. the input is `LowBoostRecoveryBcDownstreamExportConsumerResultV1`
2. `source_layout_disposition ==
   ready_for_low_boost_recovery_downstream_export_consumer_only`
3. `source_layout_notes` remains the exact low-boost-recovery export-layout note set
4. `consumer_disposition ==
   ready_for_low_boost_recovery_filesystem_export_emission_refinement_only`
5. `consumer_notes` remains the exact low-boost-recovery downstream export-consumer note set
6. `specimen_count > 0`
7. `group_count > 0`
8. `preserved_recovery_context_lanes` is non-empty
9. `group_count` equals the number of preserved lanes
10. every `source_group_ordinal` matches the concrete lane position
11. lanes remain in the exact downstream consumer order:
    - `source_replay.replay_id`
    - `source_replay.provenance_label`
    - `source_subject`
    - `source_slice_id`
    - `source_raw_state_window_ref`
    - `source_phase_id`
12. every preserved lane contains at least one preserved refined specimen
13. every preserved specimen still satisfies the downstream consumer admission invariants
14. every specimen remains aligned with its enclosing lane lineage
15. specimen order within each lane remains the exact downstream consumer order:
    - `accepted_reference_window.start`
    - `accepted_reference_window.end_exclusive`
    - `accepted_reference_variant_id`
    - `artifact_id`
16. every `artifact_id` remains unique across the full consumer result
17. `specimen_count` equals the number of preserved specimens across all lanes

Admission here means only:

- this preserved downstream result may be refined into the deterministic low-boost-recovery
  filesystem / export-emission planning shape described above

Admission here does not mean:

- actual filesystem emission is implemented
- `mimir_export` compatibility is proved
- tensors or controls exist

## H. FAILURE RULES

Filesystem / export-emission refinement fails explicitly when any admission invariant above is
violated.

Fail when:

- source layout disposition drifts
- source layout notes drift
- consumer disposition drifts
- consumer notes drift
- counts drift
- lane order drifts
- lane ordinals drift
- a lane is empty
- a preserved specimen is malformed
- a specimen no longer matches its enclosing lane lineage
- specimen order within a lane drifts
- any duplicate `artifact_id` appears

### Failure behavior

- no repair is allowed
- no regrouping is allowed
- no resorting is allowed
- no specimen is skipped
- no inferred filesystem path from lineage fields is allowed
- no filename sanitization layer is invented
- no filesystem output is emitted

This pass must fail instead of repairing or inferring.

## I. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic multi-family filesystem / export-emission framework
- no actual `mimir_export` bundle emission
- no actual filesystem writes
- no manifest or bundle-index orchestration framework
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

The next pass now has one explicit low-boost-recovery filesystem / export-emission planning result
that:

- starts strictly from `LowBoostRecoveryBcDownstreamExportConsumerResultV1`
- preserves the downstream consumer boundary instead of reopening lower BC stages
- preserves ordered recovery-context lanes unchanged
- preserves specimen order, lineage, accepted reference windows, confidence, and unresolved
  assumptions unchanged inside those lanes
- adds only deterministic family root, lane-directory, and specimen file-stem planning
- still does not widen into `mimir_export`

### What remains deferred

This pass still does not guarantee:

- actual filesystem emission
- manifest files
- bundle directories in `mimir_export`
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- one low-boost-recovery-specific actual filesystem emission boundary above
  `LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`
- still without `mimir_export` widening unless that separate decision is explicitly reopened
