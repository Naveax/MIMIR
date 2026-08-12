# MIMIR Skill Forge Eval Harness v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded eval harness for the Skill Forge v1 low-boost-recovery vertical
slice.

It consumes accepted shell outputs only and emits one narrow, auditable eval result surface.

### Why it exists

The curriculum/export shell pass created a family-specific handoff artifact, but that shell alone
does not say whether the accepted shell is structurally usable as an eval input. This pass exists
to:

- consume only `LowBoostRecoveryCurriculumExportShellV1`
- report whether the shell remains structurally usable, auditable, and bounded
- keep provisional acceptance visible instead of silently upgrading it into proof

### How it differs from adjacent stages

- Shell construction owns accepted-candidate admission from validator output.
- This eval harness owns bounded inspection of the accepted shell surface.
- Later BC/export work may consume the eval result, but this pass does not become BC generation,
  benchmark infrastructure, or proof machinery.

This pass does not prove training value, runtime value, or policy improvement.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

That restriction is required because the current eval criteria are tied to the accepted
low-boost-recovery shell shape:

- one source replay slice
- one accepted source phase window
- one accepted exact reference variant lineage
- one bounded carried confidence band
- one bounded unresolved-assumption burden

No generic all-family eval framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes exactly:

- `LowBoostRecoveryCurriculumExportShellV1`

### Consumed fields

- `family`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `source_phase_window`
- `accepted_reference_variant_id`
- `accepted_reference_variant_window`
- `evaluated_variant_ids`
- `accepted_decision`
- `decision_reason`
- `confidence_band`
- `carried_unresolved_assumptions`
- `shell_notes`
- `consumer_hint`

### Boundary rule

The eval harness consumes accepted shell outputs only. It does not accept parameter bundles,
variant lists, validation results, replay slices, or replay-state windows directly.

If the shell is structurally inconsistent with the declared shell contract, the eval harness must
report that inconsistency as eval input failure rather than bypassing the shell boundary.

## D. EVAL RESULT V1

`LowBoostRecoveryEvalResultV1` is the minimum eval result shape for this pass.

### Fields

- `source_slice_id`
  Replay-slice lineage copied from the shell.
- `source_phase_id`
  Phase lineage copied from the shell.
- `accepted_reference_variant_id`
  Accepted exact-reference lineage when it remains structurally present.
- `eval_status`
  One bounded eval status class.
- `eval_notes`
  One bounded note list describing which shell checks were satisfied or visibly limited.
- `metric_summary`
  One bounded metric summary. These are completeness and consistency signals only.
- `carried_confidence_band`
  The shell-carried validator confidence band, preserved without reinterpretation.
- `carried_unresolved_assumptions`
  The shell-carried unresolved burden, preserved without reinterpretation.

The eval result is intentionally small. It is not a proof artifact, not a benchmark row, and not a
hidden export payload.

## E. EVAL STATUS CLASSES

The minimum status classes in v1 are:

- `unusable_input`
  The shell cannot be trusted as an eval input because required accepted-shell fields or required
  reference-window structure are broken.
- `shell_present`
  A shell surface is present, but lineage is incomplete enough that the harness should not treat it
  as auditable.
- `shell_auditable`
  The shell can be audited as a bounded artifact, but one or more readiness constraints remain
  visibly incomplete.
- `shell_ready_for_future_consumer`
  The shell satisfies the full current bounded eval contract and is ready for later bounded
  consumer-planning work.

`shell_ready_for_future_consumer` does not mean:

- low-boost proof
- contact proof
- recovery success proof
- physics reachability proof
- BC usefulness proof
- policy improvement proof

## F. METRIC MODEL V1

The v1 metric model is intentionally narrow and non-physical.

`LowBoostRecoveryEvalMetricSummaryV1` contains exactly these bounded booleans:

- `lineage_completeness`
  Whether slice, replay, subject, raw-state, and accepted-reference lineage remain structurally
  present and internally linkable.
- `accepted_shell_completeness`
  Whether the shell still carries the expected accepted-only shell notes and `eval_harness_only`
  consumer hint.
- `bounded_evidence_consistency`
  Whether the accepted reference window and bounded variant lineage remain internally consistent
  with the accepted shell contract.
- `unresolved_burden_visibility`
  Whether the known unresolved assumptions remain explicit instead of being hidden or dropped.
- `reference_window_availability`
  Whether the accepted reference window is still structurally available as a bounded time window.

These metrics do not measure physics truth, recovery truth, or downstream learning value.

## G. NON-GOALS

This pass does not do any of the following:

- no physics proof
- no true low-boost proof
- no contact truth
- no recovery success proof
- no policy-improvement proof
- no BC/export generation
- no replay parsing
- no replay mining/search
- no runtime bridge
- no rollout/physics simulation
- no generic benchmark framework
- no generic multi-family eval framework
- no speculative metadata bag

## H. RELATION TO NEXT STAGES

### What this pass guarantees to future BC/export work

If a later low-boost-recovery BC-planning pass chooses to consume this eval result, it can rely
on:

- the shell was consumed through the accepted-shell boundary only
- the result distinguishes unusable shell input from auditable shell input
- the result preserves accepted reference lineage, confidence, and unresolved assumptions
- the result keeps provisional acceptance explicit

### What this pass guarantees to future runtime bridge work

This pass guarantees only that the shell can be inspected as a bounded accepted artifact. It does
not guarantee runtime invocation readiness or runtime fallback value.

### What this pass explicitly does not guarantee yet

This pass does not guarantee:

- that the shell represents a truly low-boost state
- that contact semantics are correct
- that the recovery succeeds
- that the shell is physically reachable
- that the shell is useful for BC
- that the shell improves a policy
