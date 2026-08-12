# MIMIR Skill Forge BC Consumer Refinement Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded downstream low-boost-recovery BC consumer-definition refinement on
top of the already-validated persisted-artifact handoff.

It defines:

- one exact consumer input boundary above
  `LowBoostRecoveryBcArtifactConsumerHandoffV1`
- one exact first consumer role
- one minimal family-specific refinement result surface
- one strict admission rule for when a handoff may enter that refinement boundary
- one strict failure rule for malformed or drifted handoff content

### Why it exists

The persisted-artifact handoff pass proved that one stored low-boost-recovery BC specimen can be
validated and admitted into one repo-local handoff without reaching back into BC rows, accepted
shells, or `mimir_export`.

That still left one unresolved question:

- what is the first downstream consumer actually allowed to do with that handoff now

This pass exists to answer that question narrowly and honestly before any batching, orchestration,
tensor work, or control extraction is introduced.

### How it differs from adjacent stages

- Persisted-artifact handoff owns artifact-envelope admission and payload validation.
- This pass owns the first downstream consumer contract on top of that validated handoff.
- A later pass may define specimen batching or orchestration for this family, but this pass does
  not.

This pass is not:

- persisted-artifact definition
- batch export orchestration
- `mimir_export` integration
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This consumer definition remains family-specific because:

- the handoff already carries low-boost-recovery-specific observation binding semantics
- the handoff already carries low-boost-recovery-specific target binding semantics
- the carried confidence and unresolved-assumption burden are still the fixed low-boost-recovery
  set
- no second BC family exists yet to justify a shared downstream consumer contract

No generic all-family BC consumer framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes exactly one:

- `LowBoostRecoveryBcArtifactConsumerHandoffV1`

Within that handoff, this pass consumes:

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

### Boundary rule

At this stage, direct downstream consumer input is no longer:

- BC rows
- accepted shells
- persisted artifact envelopes
- serialized BC artifact payloads

Those earlier boundaries have already done their job. This pass starts strictly from
`LowBoostRecoveryBcArtifactConsumerHandoffV1`.

## D. FIRST CONSUMER ROLE

The first bounded downstream consumer role is:

- one specimen-scoped readiness/refinement step for future low-boost-recovery specimen batching

### What it is allowed to inspect

The first consumer may inspect only:

- audit identity through `artifact_id`
- preserved source lineage
- `source_raw_state_window_ref` as an opaque lookup boundary
- `source_phase_id`
- `accepted_reference_variant_id`
- observation binding direction
- target binding direction
- the concrete accepted reference window
- carried confidence band
- carried unresolved assumptions

### What it is not allowed to inspect yet

The first consumer is not allowed to inspect:

- replay frames or parsed replay payloads
- raw state behind `source_raw_state_window_ref`
- artifact header metadata
- artifact note bags
- BC rows, shells, or planning results
- tensors, feature vectors, or normalization outputs
- controls, actions, or labels
- multi-specimen batch state
- `mimir_export`

Its role is definition refinement only, not materialization or orchestration.

## E. CONSUMER OUTPUT / REFINEMENT RESULT V1

The minimum refined consumer result is:

- `LowBoostRecoveryBcConsumerRefinementResultV1`

It contains exactly:

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

### Bounded disposition

`consumer_disposition` is fixed to exactly:

- `ready_for_specimen_batching_only`

That means:

- this specimen is admitted for future low-boost-recovery specimen batching work only

It does not mean:

- ready for tensor materialization
- ready for control extraction
- ready for `mimir_export`
- useful BC data proved

### Bounded notes

`consumer_notes` are fixed to:

- `handoff_boundary_preserved`
- `specimen_scoped_batching_only`
- `tensor_and_control_materialization_deferred`

There is no generic metadata bag.

## F. ADMISSION RULES

A handoff may enter this refined consumer boundary only when all of the following hold:

1. the input is `LowBoostRecoveryBcArtifactConsumerHandoffV1`
2. `artifact_id == "<accepted_reference_variant_id>:bc_artifact_v1"`
3. preserved lineage remains present:
   - `source_slice_id`
   - `source_replay.replay_id`
   - `source_replay.provenance_label`
   - `source_subject`
   - `source_raw_state_window_ref`
   - `accepted_reference_variant_id`
4. `observation_binding_kind == accepted_reference_window_from_raw_state_window_ref`
5. `supervision_window_role == accepted_reference_variant_window`
6. `accepted_reference_window` remains a valid bounded window
7. `target_binding_kind == accepted_reference_variant_control_target_deferred`
8. `carried_confidence_band == boundary_stable`
9. `carried_unresolved_assumptions` remains the exact low-boost-recovery carried set

Admission here means only:

- this one specimen is ready to be preserved as a downstream low-boost-recovery batching candidate

Admission here does not mean:

- control targets exist
- tensors exist
- the specimen is useful
- a batch exists

## G. FAILURE / DEFER RULES

The refined consumer boundary fails explicitly when any admission invariant above is violated.

Fail when:

- the handoff is blank or partially blank
- `artifact_id` drifts from accepted-reference lineage
- observation binding drifts
- supervision role drifts
- the accepted reference window is empty or inverted
- target binding drifts
- confidence drifts away from `boundary_stable`
- unresolved assumptions drift away from the exact low-boost-recovery set

### Failure behavior

- no repair is allowed
- no inferred fallback is allowed
- no missing field may be filled from older boundaries

### Defer behavior

There is no soft defer path in v1.

This is deliberate. The persisted-artifact handoff already fixed the only honest uncertainty this
boundary is allowed to carry forward, and that uncertainty is preserved explicitly in
`carried_unresolved_assumptions`. This pass does not add any new evidence gate that would justify
a separate defer disposition.

## H. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no batching/orchestration
- no tensor materialization
- no control/action extraction
- no replay parsing
- no replay mining
- no replay ingestion
- no rollout or physics work
- no usefulness proof
- no policy-improvement proof
- no generic multi-family consumer framework

## I. RELATION TO NEXT STAGES

### What this pass now guarantees

The next pass now has one explicit family-specific downstream result surface on top of the
validated handoff:

- a refined specimen result that preserves lineage
- a refined specimen result that preserves the accepted reference window
- a refined specimen result that preserves confidence and unresolved assumptions
- an explicit disposition showing that only specimen batching is justified now

### What remains deferred

This pass still does not guarantee:

- multi-specimen batching semantics
- directory/layout orchestration
- `mimir_export` compatibility
- tensor materialization
- control/action extraction
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be low-boost-recovery specimen batching/orchestration without
`mimir_export`, consuming the refined consumer result instead of raw BC artifacts, rows, or shells.
