# MIMIR Skill Forge Curriculum / Export Shell v1

## A. PURPOSE

### What this pass owns

This pass owns the first narrow curriculum/export shell boundary for Skill Forge v1:

- consume one `LowBoostRecoveryParameterBundleV1`
- consume one bounded `LowBoostRecoveryGeneratedVariantV1[]` set
- consume one `LowBoostRecoveryValidationResultV1`
- emit one bounded shell artifact only when the validator result is provisionally accepted

### Why it exists

The validator pass decides whether a low-boost-recovery candidate may continue. Later BC/export,
runtime, or broader curriculum work does not exist yet and must not be implied by weak acceptance.
This shell exists to preserve the minimum evidence context that the immediate next consumer needs
without widening existing export-bundle semantics.

### How it differs from adjacent stages

- Validator work owns `malformed` / `reject` / `abstain` / `accept_candidate`.
- This shell pass does not re-decide candidate quality.
- Later full export work may consume this shell, but this pass does not become a full export
  framework, BC pipeline, or runtime bridge.

This shell is a bounded handoff surface, not proof upgrade.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

The shell remains family-specific and narrow because:

- the upstream replay slice, canonicalizer, solver, and validator are all currently scoped to
  low boost recovery only
- the accepted evidence shape is tied to one candidate recovery window plus one-frame boundary trim
  probes
- generalizing now would invite fake universality before a second family exists

No generic all-family curriculum/export framework is introduced in this pass.

## C. INPUT BOUNDARY

This pass consumes exactly:

- `LowBoostRecoveryParameterBundleV1`
- `LowBoostRecoveryGeneratedVariantV1[]`
- `LowBoostRecoveryValidationResultV1`

### Consumed fields from `LowBoostRecoveryParameterBundleV1`

- `slice_id`
- `family`
- `source_replay`
- `subject`
- `raw_state_window_ref`
- `phase_window_link.phase_id`
- `phase_window_link.phase_label`
- `phase_window_link.window`
- `unresolved_assumptions`

### Consumed fields from `LowBoostRecoveryGeneratedVariantV1[]`

- `variant_id`
- `source_slice_id`
- `source_phase_id`
- `family`
- `variant_window`
- `window_override`
- `difficulty_hint`
- `generation_reason`
- `unresolved_assumptions`

### Consumed fields from `LowBoostRecoveryValidationResultV1`

- `source_slice_id`
- `source_phase_id`
- `reference_variant_id`
- `evaluated_variant_ids`
- `decision`
- `reason`
- `confidence_band`
- `carried_unresolved_assumptions`
- `validator_notes`

### Boundary assumptions

The shell pass must re-check the bounded lineage and structure it depends on. It must not trust a
caller-supplied accepted result without confirming:

- parameter bundle family and phase lineage remain low-boost-recovery-specific
- variant set still matches the declared parameter bundle
- validation lineage still matches the parameter bundle and exact reference variant

## D. SHELL OUTPUT V1

`LowBoostRecoveryCurriculumExportShellV1` is the minimum shell output shape.

### Fields

- `family`
  Always `low_boost_recovery`.
- `source_slice_id`
  Replay-slice lineage.
- `source_replay`
  Replay id plus provenance label copied from the parameter bundle.
- `source_subject`
  Replay-local subject lineage copied from the parameter bundle.
- `source_raw_state_window_ref`
  Bounded raw-state linkage copied from the parameter bundle.
- `source_phase_id`
  Accepted phase lineage.
- `source_phase_window`
  Accepted phase window copied from the parameter bundle.
- `accepted_reference_variant_id`
  The exact accepted reference variant lineage.
- `accepted_reference_variant_window`
  The exact accepted reference variant window.
- `evaluated_variant_ids`
  Deterministic lineage of the bounded variant set the validator considered.
- `accepted_decision`
  The preserved validator decision status. In v1 shell output this must remain
  `accept_candidate`.
- `decision_reason`
  The preserved validator reason code.
- `confidence_band`
  The preserved validator confidence band.
- `carried_unresolved_assumptions`
  Explicit unresolved assumptions carried forward unchanged.
- `shell_notes`
  Bounded notes:
  - `accepted_candidate_only`
  - `provisional_acceptance_only`
  - `unresolved_assumptions_carried_forward`
- `consumer_hint`
  Bounded consumer hint:
  - `eval_harness_only`

### Shape discipline

This output is intentionally bounded. It does not carry a generic metadata bag, does not become a
full curriculum graph, and does not create a broader export package.

## E. ADMISSION RULES

Shell output may be emitted only when all of the following hold:

1. the parameter bundle remains structurally valid
2. the variant set remains structurally valid
3. validation lineage matches the parameter bundle
4. `decision == accept_candidate`
5. `reason == provisional_candidate_accepted`
6. `confidence_band == boundary_stable`
7. `reference_variant_id` is present and matches the exact observed-window variant
8. `evaluated_variant_ids` matches the deterministic bounded variant lineage

### Non-emitting decisions

The shell must not emit output for:

- `abstain`
- `reject`
- `malformed`

Those outcomes remain explicit non-exportable states in this pass.

## F. WHAT THE SHELL PRESERVES

The shell must preserve, without silent upgrade:

- slice lineage
- replay provenance lineage
- subject lineage
- bounded raw-state linkage
- phase lineage
- accepted exact-variant lineage
- bounded validator decision status
- bounded validator confidence
- unresolved assumptions

The shell must not silently reinterpret provisional acceptance as:

- low-boost proof
- contact proof
- recovery-success proof
- physics reachability proof
- teachability proof

## G. NON-GOALS

This pass does not do any of the following:

- no full BC export
- no DAgger export
- no PPO auxiliary export
- no runtime bridge
- no generic export framework
- no generic curriculum framework
- no proof upgrade
- no replay parsing
- no replay mining/search
- no rollout or physics verification
- no widening of existing export bundle semantics

## H. RELATION TO NEXT STAGES

### What this shell guarantees to future BC/export work

If future BC/export work chooses to consume this shell, it can rely on:

- strict exclusion of `malformed`, `reject`, and `abstain`
- explicit accepted-candidate lineage
- explicit provisional confidence
- explicit unresolved-assumption burden

### What this shell guarantees to the immediate eval harness pass

The next low-boost-recovery eval harness pass can consume:

- the accepted reference window
- the accepted reference variant id
- replay and raw-state lineage needed to locate the bounded seed evidence
- the validator decision context needed to keep provisional acceptance visible

### What this shell explicitly does not guarantee yet

This shell does not guarantee:

- true low-boost confirmation
- contact correctness
- recovery correctness
- physics reachability
- downstream training usefulness
- runtime invocation readiness
- improvement over baseline
