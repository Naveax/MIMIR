# MIMIR Skill Forge Consumer / BC-Planning Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first bounded low-boost-recovery consumer / BC-planning boundary that sits on
top of accepted shell output plus bounded eval output.

Its job is to:

- flag that the roadmap is now approaching the BC milestone
- preserve the minimum accepted lineage and readiness context needed for the next pass
- classify whether a bounded low-boost-recovery shell/eval pair is not a BC candidate yet,
  deferred, or ready for BC contract definition

### Why it exists

The eval harness established whether an accepted shell is structurally unusable, merely present,
auditable, or ready for future bounded consumer work. That is still not permission to shape BC
dataset or export semantics.

This pass exists so the project can cross the BC-approach threshold explicitly instead of letting
BC arrive implicitly through shell reuse, eval reuse, or `mimir_export` drift.

### How it differs from adjacent stages

- Eval harness work inspects the accepted shell and produces a bounded readiness result.
- This pass consumes that readiness result plus the accepted shell as planning input only.
- The next real BC contract-definition pass will define the first actual low-boost-recovery BC
  consumer contract. This pass does not.

This pass is a planning boundary only. It is not BC export, not BC dataset generation, and not a
proof upgrade.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

Consumer planning remains family-specific here because:

- every upstream Skill Forge v1 boundary is currently low-boost-recovery-specific
- the carried lineage is one replay slice, one source phase, and one accepted reference variant
  from the low-boost-recovery shell only
- forcing a generic consumer framework now would silently widen semantics before a second family
  exists

Any multi-family consumer planning surface must be a later explicit boundary change.

## C. INPUT BOUNDARY

This pass conceptually consumes exactly:

- `LowBoostRecoveryEvalResultV1`
- `LowBoostRecoveryCurriculumExportShellV1`

### Consumed readiness fields from `LowBoostRecoveryEvalResultV1`

- `source_slice_id`
- `source_phase_id`
- `accepted_reference_variant_id`
- `eval_status`
- `carried_confidence_band`
- `carried_unresolved_assumptions`

### Consumed lineage fields from `LowBoostRecoveryCurriculumExportShellV1`

- `family`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `accepted_reference_variant_id`
- `accepted_decision`
- `decision_reason`
- `confidence_band`
- `carried_unresolved_assumptions`
- `consumer_hint`

### Boundary rule

This pass is planning-boundary work only. It does not execute a real consumer, does not generate a
dataset row, and does not bypass the eval harness by reaching back into parameter bundles or
variant lists.

The eval result is the readiness authority. The accepted shell is the lineage carrier that the eval
result must still align with.

## D. BC MILESTONE FLAG

The project is now at the BC-approach threshold.

That milestone must be flagged before any BC-facing contract starts shaping dataset or export
semantics because:

- BC row semantics become harder to change casually once the first contract exists
- mistaken lineage or readiness assumptions would otherwise leak into later export work
- `shell_ready_for_future_consumer` is only a bounded shell-readiness signal and must not be
  allowed to read like proof of BC usefulness

### Allowed in this pass

- one planning-only contract artifact
- one explicit milestone flag artifact
- one bounded planning disposition surface
- one tiny low-boost-recovery-specific DTO / constructor surface, if useful

### Not allowed in this pass

- real BC dataset rows
- real BC export payloads
- export bundle widening
- `mimir_export` contract growth
- runtime bridge work
- usefulness proof or policy-improvement claims

## E. CONSUMER / BC-PLANNING OUTPUT V1

The planning output stays deliberately small:

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
- `planning_notes`

### Why this shape is justified

- it preserves slice lineage without carrying replay payloads
- it preserves phase lineage without turning the planning result into a training row
- it preserves accepted-reference lineage through the eval result instead of bypassing it
- it preserves confidence and unresolved assumptions so the next BC contract-definition pass does
  not need to rediscover boundary limits

### What is intentionally excluded

- no phase-window payload
- no reference-window payload
- no evaluated-variant list
- no state tensors
- no label fields
- no action targets
- no generic metadata bag

The planning output is a BC-contract-shaping boundary marker, not a dataset specimen.

## F. DISPOSITION CLASSES

The minimum planning dispositions are:

- `not_bc_candidate`
  The shell/eval pair is too broken or too weak to use as BC-contract-shaping input.
- `bc_candidate_deferred`
  The pair is still bounded and auditable enough to keep, but it is not yet ready to define the
  first BC contract.
- `bc_candidate_ready_for_contract_definition`
  The pair is bounded, aligned, and ready for the next pass to define the first real BC contract.

None of these dispositions mean BC export exists. None of them prove BC usefulness.

## G. ADMISSION RULES

### `not_bc_candidate`

Use `not_bc_candidate` when any of the following hold:

- `eval_status == unusable_input`
- `eval_status == shell_present`
- shell/eval slice lineage does not align
- shell/eval phase lineage does not align
- accepted reference variant lineage does not align
- carried confidence does not align
- carried unresolved assumptions do not align
- the shell has drifted away from the accepted low-boost-recovery shell boundary
  (`accept_candidate`, `provisional_candidate_accepted`, `boundary_stable`,
  `eval_harness_only`)

Meaning:

- do not use the pair to shape BC contract semantics
- do not reinterpret the pair as deferred BC readiness

### `bc_candidate_deferred`

Use `bc_candidate_deferred` only when all of the following hold:

- shell/eval lineage and carried boundary fields still align
- the shell still presents the accepted low-boost-recovery boundary
- `eval_status == shell_auditable`

Meaning:

- the pair is still auditable planning input
- readiness is not yet strong enough for real BC contract definition

### `bc_candidate_ready_for_contract_definition`

Use `bc_candidate_ready_for_contract_definition` only when all of the following hold:

- shell/eval lineage and carried boundary fields still align
- the shell still presents the accepted low-boost-recovery boundary
- `eval_status == shell_ready_for_future_consumer`
- accepted reference variant lineage remains present

Meaning:

- the pair is ready for the next pass to define the first real low-boost-recovery BC contract
- this still does not prove BC usefulness, policy improvement, or export readiness

## H. NON-GOALS

This pass does not do any of the following:

- real BC dataset generation
- real BC export contract definition
- DAgger export
- PPO auxiliary export
- runtime bridge work
- generic consumer framework work
- generic metrics framework work
- replay parsing or replay mining
- rollout or physics work
- proof upgrade
- export bundle widening

## I. RELATION TO NEXT STAGES

### What this pass guarantees to the first real BC contract-definition pass

- the BC milestone has been explicitly flagged before contract shaping starts
- the next pass can consume one bounded planning disposition instead of inferring readiness from
  raw shell reuse
- slice lineage, phase lineage, accepted-reference lineage, confidence, and unresolved assumptions
  remain explicit
- the next pass does not need to bypass eval results to decide whether BC contract work may begin

### What this pass does not guarantee yet

This pass does not guarantee:

- a BC row schema
- BC serialization format
- export bundle changes
- low-boost truth
- contact truth
- recovery success
- physics reachability
- BC usefulness
- policy improvement
