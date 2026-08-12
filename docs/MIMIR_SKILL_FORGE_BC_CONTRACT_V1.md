# MIMIR Skill Forge BC Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the first real low-boost-recovery BC contract-definition boundary.

Its job is to define:

- the first low-boost-recovery BC row/schema
- the exact lineage and binding fields that row must carry
- the strict admission rule for when a planning result may become a BC contract row
- the narrow family-specific DTO surface, if any, that makes the contract auditable in Rust

### Why it exists

The prior consumer / BC-planning pass stopped on purpose before row semantics existed. That left
the project with:

- one accepted-shell lineage carrier
- one eval-readiness result
- one planning-only readiness disposition

That was enough to justify contract definition, but not enough to justify export semantics.

### How it differs from adjacent stages

- Consumer / BC-planning work decides whether BC contract definition may begin.
- This pass defines the first real low-boost-recovery BC contract row.
- A later BC serialization/export boundary pass may decide how that row is serialized or persisted.

This pass is not BC dataset generation, not BC export execution, and not `mimir_export`
integration.

## B. BC MILESTONE

This pass is the BC milestone.

That matters because the first real BC row contract is harder to change casually than the earlier
planning boundary:

- row fields start constraining later serialization/export work
- binding choices start constraining later observation/target export work
- mistaken lineage assumptions would become sticky if export work started without a contract

Contract definition is allowed now because the repo already has:

- an accepted low-boost-recovery shell boundary
- a bounded eval harness result
- a planning result that can explicitly say
  `bc_candidate_ready_for_contract_definition`

Export implementation remains deferred because this pass still does not define:

- serialized observation payloads
- serialized target payloads
- export files
- persistence format
- `mimir_export` integration

## C. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

The BC contract remains family-specific because every upstream Skill Forge v1 boundary is still
family-specific:

- one replay slice family
- one accepted shell family
- one eval harness family
- one consumer-planning family

Defining a generic all-family BC row now would introduce fake universality before a second family
exists.

## D. INPUT BOUNDARY

This BC contract-definition pass conceptually consumes exactly:

- `LowBoostRecoveryConsumerPlanningResultV1`
- `LowBoostRecoveryCurriculumExportShellV1`

### Consumed fields from `LowBoostRecoveryConsumerPlanningResultV1`

- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `accepted_reference_variant_id`
- `eval_readiness_status`
- `carried_confidence_band`
- `carried_unresolved_assumptions`
- `disposition`

### Consumed fields from `LowBoostRecoveryCurriculumExportShellV1`

- `family`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `source_phase_window`
- `accepted_reference_variant_id`
- `accepted_reference_variant_window`
- `accepted_decision`
- `decision_reason`
- `confidence_band`
- `carried_unresolved_assumptions`
- `shell_notes`
- `consumer_hint`

### Boundary rule

This pass uses the planning result as the permission gate and the accepted shell as the reference
lineage carrier.

This pass does not:

- bypass planning by reaching back into eval or validator internals
- bypass the shell by reaching back into parameter bundles or raw variants
- execute BC export

## E. BC ROW / SCHEMA V1

`LowBoostRecoveryBcRowV1` is the first real BC row/schema for low boost recovery.

### Required fields

- `family`
  Always `low_boost_recovery`.
- `source_slice_id`
  Replay-slice lineage for the accepted specimen.
- `source_replay`
  Replay id plus provenance label copied unchanged from the aligned planning/shell boundary.
- `source_subject`
  Replay-local subject lineage.
- `source_raw_state_window_ref`
  Bounded raw-state linkage. This stays a reference, not an inlined state payload.
- `source_phase_id`
  Accepted phase lineage.
- `accepted_reference_variant_id`
  Accepted exact reference-variant lineage.
- `supervision_window_role`
  `accepted_reference_variant_window`
- `observation_binding_kind`
  `accepted_reference_window_from_raw_state_window_ref`
- `target_binding_kind`
  `accepted_reference_variant_control_target_deferred`
- `carried_confidence_band`
  Provisional validator/eval confidence carried forward without reinterpretation.
- `carried_unresolved_assumptions`
  Explicit unresolved-assumption burden carried forward without reinterpretation.
- `bc_contract_notes`
  Exact bounded notes:
  - `contract_definition_only`
  - `accepted_shell_planning_boundary_aligned`
  - `observation_binding_deferred_to_later_serialization`
  - `target_binding_deferred_to_later_serialization`
  - `provisional_confidence_carried_forward`
  - `unresolved_assumptions_carried_forward`
  - `not_bc_usefulness_proof`

### Why this row is real enough now

The row is a real contract because it fixes:

- the lineage that a later BC export row must preserve
- the exact accepted-evidence anchor
- the observation/target binding direction
- the carried confidence and unresolved-assumption burden

### What this row intentionally does not contain

- no serialized observation tensor
- no serialized target tensor or action payload
- no inlined `source_phase_window`
- no inlined `accepted_reference_variant_window`
- no evaluated-variant list
- no open-ended metadata bag
- no export path, file id, or persistence handle
- no usefulness score or policy-improvement claim

## F. BINDING RULES

### Observation source binding

Observation source is referenced, not materialized.

The row binds observations through:

- `source_raw_state_window_ref`
- `source_phase_id`
- `accepted_reference_variant_id`
- `supervision_window_role = accepted_reference_variant_window`
- `observation_binding_kind = accepted_reference_window_from_raw_state_window_ref`

Meaning:

- the accepted shell remains the authority for the concrete accepted reference window
- later serialization/export work must derive the observation payload from that aligned shell
  window inside the bounded raw-state window reference
- this pass does not define feature vectors, tensor layout, normalization, or actor-visible slot
  ordering

### Target source binding

Target source is also referenced, not materialized.

The row binds targets through:

- `accepted_reference_variant_id`
- `target_binding_kind = accepted_reference_variant_control_target_deferred`

Meaning:

- the contract fixes that the target must come from the accepted low-boost-recovery reference
  variant lineage
- this pass does not define whether later export emits discrete actions, logits, control records,
  or another concrete serialization

### Accepted reference window lineage

Accepted reference-window lineage is represented by:

- the explicit `accepted_reference_variant_id`
- the explicit `supervision_window_role`
- the required alignment with the accepted shell that still carries
  `accepted_reference_variant_window`

The reference window is therefore contract-bound without being copied into the BC row.

### What remains deferred

Deferred until the later BC serialization/export boundary pass:

- concrete observation schema
- concrete target schema
- observation normalization
- action/control serialization
- file format and persistence semantics
- any `mimir_export` integration

## G. ADMISSION RULES

A planning result may become a BC contract row/specimen only when all of the following hold:

1. `disposition == bc_candidate_ready_for_contract_definition`
2. `eval_readiness_status == shell_ready_for_future_consumer`
3. `accepted_reference_variant_id` is present in the planning result
4. planning and shell lineage align for:
   - `source_slice_id`
   - `source_replay`
   - `source_subject`
   - `source_raw_state_window_ref`
   - `source_phase_id`
5. planning and shell carried-boundary fields align for:
   - `accepted_reference_variant_id`
   - `carried_confidence_band`
   - `carried_unresolved_assumptions`
6. the shell still satisfies the accepted low-boost-recovery boundary:
   - `family == low_boost_recovery`
   - `accepted_decision == accept_candidate`
   - `decision_reason == provisional_candidate_accepted`
   - `confidence_band == boundary_stable`
   - `consumer_hint == eval_harness_only`
   - accepted shell notes remain the bounded accepted-only note set
   - accepted reference window and phase window remain structurally consistent

### Strict consequence

If the planning result is not ready, no BC row is emitted.

If the planning result claims readiness but shell/planning lineage has drifted, that is a contract
failure, not a deferred BC row.

### What admission does not mean

Admission into `LowBoostRecoveryBcRowV1` does not mean:

- BC usefulness is proven
- low-boost truth is proven
- contact truth is proven
- recovery success is proven
- policy improvement is proven
- export readiness is proven

## H. NON-GOALS

This pass does not do any of the following:

- no BC export serialization
- no BC export files
- no `mimir_export` integration
- no runtime bridge
- no DAgger export
- no PPO auxiliary export
- no usefulness proof
- no policy-improvement proof
- no replay parsing
- no replay mining
- no rollout or physics work
- no observation tensor implementation
- no target-action implementation
- no generic BC framework
- no generic dataset framework

## I. RELATION TO NEXT STAGES

### What this pass guarantees to the first BC serialization/export boundary pass

The next pass now has:

- one real low-boost-recovery BC row contract
- one exact admission rule for when a row may exist
- one explicit binding decision for how observation and target supervision are referenced
- one explicit statement of what must still stay deferred

That makes the first BC serialization/export boundary pass obvious:

- consume aligned `LowBoostRecoveryBcRowV1` plus the accepted shell boundary
- define concrete serialization/persistence semantics without inventing new lineage fields

### What this pass explicitly does not guarantee yet

This pass does not guarantee:

- concrete serialized observations
- concrete serialized targets
- export bundle changes
- persistence format
- `mimir_export` compatibility
- BC usefulness
- runtime usefulness
- policy improvement
