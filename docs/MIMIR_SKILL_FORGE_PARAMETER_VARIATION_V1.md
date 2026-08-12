# MIMIR Skill Forge Parameter Solver + Variation Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the minimum family-specific transformation from the canonical low-boost-recovery
bundle into:

- `LowBoostRecoveryParameterBundleV1`
- `LowBoostRecoveryGeneratedVariantV1[]`

### Why it exists

Canonicalization stabilizes identity, provenance, and one candidate recovery window, but it does
not yet produce a bounded parameter surface that later validator work can inspect. This pass
exists to:

- preserve the canonical window as an auditable parameter seed
- expose the smallest bounded interpretation surface around that seed
- carry forward unresolved semantics explicitly instead of hiding them in later heuristics

### How it differs from adjacent stages

- Canonicalization owns slice-shape validity plus one deterministic candidate window.
- This pass owns a bounded parameter interpretation of that window plus bounded variation around
  that interpretation.
- Later validator work owns confidence, abstain, and any stronger claim about whether the slice is
  truly low-boost, physically reachable, or a successful recovery.

This pass does not upgrade replay evidence into replay truth.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

The solver and variation decisions are family-specific because the current canonical boundary is a
single subject-centric candidate recovery window. The chosen parameters and variants are therefore
about recovery-window interpretation only. They are not a generic skill-family parameter system and
they are not reusable proof that other families should share the same fields.

## C. INPUT BOUNDARY

This pass consumes exactly:

- `LowBoostRecoveryCanonicalStateV1`
- `LowBoostRecoveryEventContactGraphV1`
- `LowBoostRecoveryPhasePlanV1`

### Consumed fields from `LowBoostRecoveryCanonicalStateV1`

- `slice_id`
- `source_replay`
- `subject`
- `frame_window`
- `raw_state_window_ref`
- `canonicalization_notes`

### Consumed fields from `LowBoostRecoveryEventContactGraphV1`

- `slice_id`
- `frame_window`
- `nodes`
- `edges`
- `contact_semantics`

### Consumed fields from `LowBoostRecoveryPhasePlanV1`

- `slice_id`
- `phases[0].phase_id`
- `phases[0].label`
- `phases[0].start`
- `phases[0].end_exclusive`

### Boundary assumptions

The pass accepts the canonical bundle only if:

- all three artifacts share the same `slice_id`
- the event graph still matches the canonical frame window boundary
- the phase plan still contains exactly one `candidate_recovery_window`
- that phase window still matches the canonical frame window

Anything beyond those checks remains unresolved and is carried forward explicitly.

## D. PARAMETER BUNDLE V1

`LowBoostRecoveryParameterBundleV1` is the minimum bounded parameter contract for this pass.

### Fields

- `slice_id`
  Stable linkage back to the replay slice seed.
- `family`
  Always `low_boost_recovery`.
- `source_replay`
  Replay id plus provenance label copied unchanged from canonical state.
- `subject`
  Replay-local subject handle copied unchanged from canonical state.
- `raw_state_window_ref`
  Bounded linkage to the raw replay state window. This pass still does not materialize replay
  frames.
- `phase_window_link`
  - `phase_id`
  - `phase_label`
  - `window`
  This is the auditable linkage from solver output back to the canonical phase boundary.
- `recovery_window_interpretation`
  `candidate_recovery_window_only`
  Meaning: the phase window is treated as an observed candidate recovery window, not as proof of
  exact recovery onset, exact recovery completion, or true control regain.
- `observed_window_duration_frames`
  Closed range derived from the canonical phase window length. In v1 the range is exact because the
  observed window length is copied from the canonical boundary.
- `boundary_trim_budget_frames`
  Closed range defining how much later variation is allowed to trim each side of the candidate
  window. In v1 this is bounded to `0..1` frame per side and never grows into generic search.
- `parameter_notes`
  Fixed notes for this pass:
  - `observed_window_derived_from_canonical_phase`
  - `boundary_variation_limited_to_single_frame_trims`
- `unresolved_assumptions`
  Explicit carry-forward list:
  - `low_boost_threshold_unproven`
  - `contact_truth_unproven`
  - `recovery_success_unproven`
  - `replay_orientation_normalization_deferred`
  - `physics_reachability_unproven`

### What the bundle deliberately does not contain

- no guessed boost amount
- no guessed contact labels
- no guessed landing or detach frames
- no solved control trajectory
- no rollout-backed reachability score
- no generic metadata bag

## E. VARIATION SURFACE V1

`LowBoostRecoveryGeneratedVariantV1` is the minimum family-specific generated variant shape.

### Fields

- `variant_id`
  Deterministic variant identity derived from slice id, phase label, and variant suffix.
- `source_slice_id`
  Replay-slice lineage.
- `source_phase_id`
  Parameter/phase lineage.
- `family`
  Always `low_boost_recovery`.
- `variant_window`
  The concrete time window that later validator work should inspect for this variant candidate.
- `window_override`
  - `trim_start_frames`
  - `trim_end_frames`
  These are the only allowed v1 overrides.
- `difficulty_hint`
  One of:
  - `reference_seed_window`
  - `stricter_start_boundary`
  - `stricter_end_boundary`
- `generation_reason`
  One of:
  - `preserve_observed_window`
  - `probe_start_boundary_ambiguity`
  - `probe_end_boundary_ambiguity`
- `unresolved_assumptions`
  The same carry-forward unresolved assumptions from the parameter bundle.

### Variant set in v1

The generator emits only these bounded variants:

1. exact observed window
2. one-frame trim on the start boundary, if the observed window is long enough
3. one-frame trim on the end boundary, if the observed window is long enough

These are interpretation probes, not alternate replay truths.

## F. REQUIRED VS UNRESOLVED SOLVER OUTPUTS

### Required outputs this pass can derive now

- slice lineage
- replay provenance linkage
- subject linkage
- raw-state linkage
- one phase-window linkage
- exact observed window duration
- one bounded trim budget
- deterministic narrow variant list
- explicit unresolved carry-forward assumptions

### Still unresolved after this pass

- whether the slice is actually below a low-boost threshold
- whether any contact semantics are correct
- whether the candidate window contains a successful recovery
- whether the generated variants are physically reachable
- whether the seed is useful enough for teaching rather than abstaining

## G. FAILURE / ABSTAIN OWNERSHIP

### Reject in this pass

Reject the canonical bundle as malformed if any of these occur:

- `slice_id` mismatch across canonical state, graph, and phase plan
- event-graph boundary no longer matches canonical frame ownership
- phase count differs from one
- phase label differs from `candidate_recovery_window`
- phase window no longer matches canonical frame ownership
- event graph shape differs from the current narrow contract

These are structural boundary failures, not semantic abstains.

### Pass forward as unresolved for validator ownership

Pass forward with unresolved assumptions when the bundle is structurally valid but still does not
prove:

- low-boost truth
- contact truth
- recovery success
- replay orientation normalization sufficiency
- physical reachability

Validator ownership starts where this pass stops.

## H. NON-GOALS

This pass does not do any of the following:

- physics proof
- true low-boost confirmation
- contact truth
- recovery success proof
- generic search or optimizer infrastructure
- replay parsing or replay mining
- rollout/physics simulation
- curriculum/export/runtime logic
- generic all-family parameter frameworks
- speculative metadata bags

## I. RELATION TO NEXT STAGES

### Guarantees to validator

- validator receives one auditable parameter bundle tied to the canonical boundary
- validator receives a deterministic, tiny variant set instead of open-ended search
- validator can distinguish malformed canonical-boundary failures from unresolved semantic claims

### Guarantees to curriculum/export shell

- later stages can consume explicit lineage and bounded variant identities
- later stages do not need to guess what the solver believed it solved

### Explicitly not guaranteed yet

- validator acceptance
- confidence scores
- recovery correctness
- reachability proof
- export readiness beyond structural lineage
