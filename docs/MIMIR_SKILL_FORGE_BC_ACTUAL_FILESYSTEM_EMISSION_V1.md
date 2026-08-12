# MIMIR Skill Forge BC Actual Filesystem Emission Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded low-boost-recovery-specific actual filesystem emission boundary
on top of the already-fixed deterministic filesystem / export-emission plan.

It defines:

- one exact input boundary above `LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`
- one exact first actual filesystem emission role
- one exact specimen-file payload contract for emitted low-boost-recovery BC output
- one minimal receipt surface for successful emission
- one strict admission rule for when a plan may enter actual emission
- one strict failure rule for malformed plans, duplicate relative paths, destination conflicts,
  and write failures

### Why it exists

The filesystem / export-emission planning pass already fixed:

- strict input from `LowBoostRecoveryBcDownstreamExportConsumerResultV1`
- preserved ordered recovery-context lanes
- preserved specimen order inside each lane
- deterministic family root directory token
- deterministic lane-directory names
- deterministic specimen file-stem names
- refinement-only disposition and notes

That still left one unresolved question:

- what exact family-specific on-disk contract should be emitted from that plan before any
  `mimir_export` reopen, any generic bundle/index framework, or any tensor/control work

This pass exists to answer that question narrowly and explicitly.

### How it differs from adjacent stages

- Filesystem / export-emission planning owns deterministic naming and ordering only.
- This pass owns the first real write boundary that materializes that plan to disk.
- A later pass may audit or read back emitted output, but this pass does not widen into broader
  export integration.

This pass is not:

- filesystem / export-emission planning
- `mimir_export` integration
- generic manifest/index orchestration
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

Actual filesystem emission remains family-specific because:

- the admitted plan already preserves low-boost-recovery-specific lineage and BC binding semantics
- the emitted specimen payload is derived only from low-boost-recovery preserved specimens
- no second BC family exists yet to justify shared on-disk specimen payload semantics
- generic filesystem/export infrastructure would widen the boundary before a first emitted family
  contract is proven

No generic all-family filesystem/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`

Within that plan result, this pass consumes:

- `specimen_count`
- `group_count`
- `source_consumer_disposition`
- `source_consumer_notes`
- `planned_family_root_directory`
- `planned_recovery_context_lanes`
- `refinement_disposition`
- `refinement_notes`

### Boundary rule

Direct actual filesystem emission input is no longer:

- downstream export-consumer results by themselves
- export-layout results by themselves
- specimen batches by themselves
- refined specimens by themselves
- persisted low-boost-recovery BC artifacts
- BC rows
- accepted shells
- planning results below `LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`

Those earlier boundaries are already frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`.

## D. ACTUAL FILESYSTEM EMISSION ROLE

The first bounded actual filesystem emission role is:

- admit only already-planned low-boost-recovery filesystem/export-emission plans
- revalidate that the plan boundary is still intact without reshaping it
- create exactly one family root directory under a caller-provided existing parent directory
- create exactly one lane directory per planned lane in planned order
- emit exactly one specimen JSON file per planned specimen in planned order
- return only a minimal ordered receipt of what paths were emitted

### What it is allowed to write

This pass may write only:

- one emitted family root directory:
  - `low_boost_recovery_bc_v1`
- one emitted lane directory per planned lane:
  - `recovery_context_lane_{lane_ordinal:04}`
- one emitted specimen JSON file per planned specimen:
  - `specimen_{specimen_ordinal:04}.json`

### What it is not allowed to write or materialize yet

This pass is not allowed to write or materialize:

- root-level sidecar files
- lane-level sidecar files
- manifests
- indexes
- `mimir_export` bundle state
- replay frames or parsed replay payloads
- raw state behind `source_raw_state_window_ref`
- tensors, feature vectors, or normalization outputs
- controls, actions, or labels
- open-ended metadata bags

The role here is concrete filesystem emission only, not broader export orchestration.

## E. EMITTED FILE CONTRACT V1

### Root directory behavior

Actual emission always targets a caller-provided existing parent directory and creates exactly one
child root directory named:

- `low_boost_recovery_bc_v1`

The root directory name is taken from the already-fixed plan. No alternative naming rule is
introduced in v1.

### Lane directory behavior

Each planned lane becomes exactly one child directory under the emitted family root:

- `recovery_context_lane_{lane_ordinal:04}`

Lane-directory order is the plan order. No replay-derived or subject-derived lane naming is
introduced.

### Specimen file naming behavior

Each planned specimen becomes exactly one JSON file inside its emitted lane directory:

- `specimen_{specimen_ordinal:04}.json`

File naming stays ordinal-based only. No replay id, slice id, subject id, phase id, or
`artifact_id` is embedded into filenames in v1.

### Specimen payload shape

Each emitted specimen file is one JSON document with exact shape:

- `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`

It contains exactly:

- `lane_ordinal`
- `specimen_ordinal`
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

### Root-level and lane-level sidecars

There are no root-level sidecar files in v1.

There are no lane-level sidecar files in v1.

### What is preserved in emitted payloads

Each emitted specimen payload preserves exactly:

- explicit lane and specimen ordinals from the emitted plan
- artifact identity
- lineage:
  - `source_slice_id`
  - `source_replay`
  - `source_subject`
  - `source_raw_state_window_ref`
  - `source_phase_id`
- accepted reference variant lineage
- observation binding kind
- supervision window role
- accepted reference window
- target binding kind
- carried confidence band
- carried unresolved assumptions

### What remains deferred

This v1 contract deliberately defers:

- family-wide manifest/index semantics
- bundle-level metadata
- payload version envelopes
- tensor/control materialization
- replay/raw-state materialization
- generic cross-family specimen-file contracts

## F. EMISSION RULES

### Root creation rule

Actual emission requires the caller to provide an already-existing parent directory.

If admitted, the boundary creates the emitted family root directory immediately under that parent.

### Lane directory creation rule

Lane directories are created in `planned_recovery_context_lanes` order.

There is exactly one emitted lane directory for each planned lane. No lane is skipped, merged,
or reordered.

### Specimen emission rule

Within one emitted lane directory:

- specimen files are emitted in `ordered_specimen_plans` order
- each file path is derived only from the already-fixed planned file stem plus `.json`
- each file payload is derived only from the aligned preserved specimen in the plan

### Existing output rule

Pre-existing output at the emitted family root path is rejected.

This pass does not merge into an existing directory and does not overwrite an existing emitted
family root.

### Atomicity / cleanup rule

This pass does not provide a multi-file transaction.

The root directory is created directly in its final location. If a later lane-directory creation
or specimen-file write fails, the pass performs best-effort cleanup by deleting the emitted family
root directory tree it created.

### Partial failure handling

- malformed plan input fails before any write
- duplicate relative paths fail before any write
- invalid output parent directory fails before any write
- pre-existing destination conflict fails before any write
- lane-directory or specimen-file write failure hard-fails and triggers best-effort cleanup of the
  emitted family root directory tree

## G. ADMISSION RULES

A filesystem/export-emission plan may enter actual emission only when all of the following hold:

1. the input is `LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`
2. `source_consumer_disposition ==
   ready_for_low_boost_recovery_filesystem_export_emission_refinement_only`
3. `source_consumer_notes` remains the exact downstream export-consumer note set
4. `specimen_count > 0`
5. `group_count > 0`
6. `planned_family_root_directory == low_boost_recovery_bc_v1`
7. `planned_recovery_context_lanes` is non-empty
8. `group_count` equals the number of planned lanes
9. `refinement_disposition == ready_for_low_boost_recovery_filesystem_emission_boundary_only`
10. `refinement_notes` remains the exact filesystem/export-emission refinement note set
11. every `lane_ordinal` matches the concrete lane position
12. every `planned_relative_lane_directory` matches the deterministic lane-directory naming rule
13. every planned lane preserves the exact downstream lane order
14. every planned lane contains at least one preserved refined specimen
15. every planned lane keeps specimen count aligned between `preserved_lane.specimens` and
    `ordered_specimen_plans`
16. every `specimen_ordinal` matches the concrete specimen position
17. every planned `artifact_id` matches the aligned preserved specimen `artifact_id`
18. every `planned_specimen_file_stem` matches the deterministic specimen file-stem naming rule
19. every preserved specimen still satisfies the earlier batching/consumer invariants
20. every preserved specimen remains aligned with its enclosing planned lane lineage
21. specimen order within each lane remains the exact downstream-preserved order
22. every `artifact_id` remains unique across the full plan
23. every planned relative path remains unique across the full plan
24. `specimen_count` equals the number of preserved specimens across all planned lanes

Admission here means only:

- this deterministic family-specific plan may be materialized to disk as the specimen-file
  contract defined above

Admission here does not mean:

- usefulness proved
- `mimir_export` compatibility proved
- tensor/control materialization exists

## H. FAILURE RULES

Actual filesystem emission fails explicitly for:

- wrong or degraded plan disposition
- wrong or degraded note sets
- count drift
- wrong root token
- wrong lane ordinals
- wrong lane-directory names
- wrong specimen ordinals
- wrong specimen file stems
- lane-order drift
- specimen-order drift
- lane/specimen lineage drift
- duplicate `artifact_id`
- duplicate planned relative paths
- invalid output parent directory
- pre-existing destination conflict
- lane-directory creation failure
- specimen-file write failure

### Failure classification

Hard fail before write:

- malformed plan
- duplicate planned relative path
- invalid output parent directory
- pre-existing destination conflict

Hard fail during write with best-effort cleanup:

- lane-directory creation failure after root creation
- specimen-file write failure after root creation

### Failure behavior

- no repair is allowed
- no inferred path fallback is allowed
- no filename sanitization layer is invented
- no specimen is skipped
- no partial emitted root is treated as success

## I. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic multi-family filesystem/export framework
- no generic manifest/index orchestration
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

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

The next pass now has one explicit low-boost-recovery actual filesystem emission boundary that:

- starts strictly from `LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`
- materializes the already-fixed root/lane/specimen plan without reopening lower BC boundaries
- preserves lane order and specimen order exactly as planned
- emits one real family-specific specimen JSON contract on disk
- returns a minimal ordered receipt of emitted paths
- still does not widen into `mimir_export`

### What remains deferred

This pass still does not guarantee:

- root-level or lane-level manifests
- bundle/index orchestration
- `mimir_export` wiring
- family-agnostic emitted dataset semantics
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- one family-specific emitted-output audit/readback boundary above this actual emission result
- still without `mimir_export` widening unless that separate decision is explicitly reopened
