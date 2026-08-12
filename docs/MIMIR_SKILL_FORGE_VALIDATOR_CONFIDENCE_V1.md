# MIMIR Skill Forge Validator + Confidence / Abstain Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the first low-boost-recovery-specific decision boundary after parameter solving and
bounded variation:

- consume one `LowBoostRecoveryParameterBundleV1`
- consume one tiny `LowBoostRecoveryGeneratedVariantV1[]` set
- classify the candidate as `malformed`, `reject`, `abstain`, or `accept_candidate`
- attach a bounded confidence band that is explicitly about validator evidence quality only

### Why it exists

The prior pass produced a bounded parameter interpretation plus a tiny boundary-trim probe set, but
it did not decide whether that evidence is good enough to continue Skill Forge compilation. This
pass exists so later curriculum/export work does not quietly treat every structurally valid bundle
as accepted.

### How it differs from adjacent stages

- Parameter solving owns the bounded interpretation surface and variant generation.
- This pass owns bounded evidence judgment on that surface.
- Later curriculum/export work may consume accepted candidates, but does not own acceptance logic.

This pass does not convert replay-derived evidence into physics truth.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

That restriction is intentional because validator criteria are family-specific:

- the current parameter surface is a subject-centric candidate recovery window
- the current variant set probes only one-frame boundary trims
- the current confidence logic is about recovery-window boundary stability, not universal mechanic
  truth

No generic multi-family validator infrastructure is introduced in this pass.

## C. INPUT BOUNDARY

This pass consumes exactly:

- `LowBoostRecoveryParameterBundleV1`
- `LowBoostRecoveryGeneratedVariantV1[]`

### Consumed fields from `LowBoostRecoveryParameterBundleV1`

- `slice_id`
- `family`
- `source_replay`
- `subject`
- `raw_state_window_ref`
- `phase_window_link.phase_id`
- `phase_window_link.phase_label`
- `phase_window_link.window`
- `recovery_window_interpretation`
- `observed_window_duration_frames`
- `boundary_trim_budget_frames`
- `parameter_notes`
- `unresolved_assumptions`

### Consumed fields from `LowBoostRecoveryGeneratedVariantV1`

- `variant_id`
- `source_slice_id`
- `source_phase_id`
- `family`
- `variant_window`
- `window_override.trim_start_frames`
- `window_override.trim_end_frames`
- `difficulty_hint`
- `generation_reason`
- `unresolved_assumptions`

### Boundary assumptions

This pass assumes the upstream canonicalizer and solver already own:

- replay-slice shape validity
- canonical bundle structural consistency
- deterministic generation of exact/start-trim/end-trim variants

This pass still re-checks the parameter bundle and variant set boundary because later stages cannot
trust a caller-supplied bundle by default.

## D. VALIDATION RESULT V1

`LowBoostRecoveryValidationResultV1` is the minimum validation result shape.

### Fields

- `source_slice_id`
  Replay-slice lineage for the evaluated candidate.
- `source_phase_id`
  Phase lineage for the evaluated candidate window family surface.
- `reference_variant_id`
  The exact observed-window variant when one exists and is structurally identifiable.
- `evaluated_variant_ids`
  Deterministic lineage of the variants the validator considered.
- `decision`
  One of the bounded v1 decision classes.
- `reason`
  One bounded family-specific reason code for the decision.
- `confidence_band`
  A bounded validator-confidence label.
- `carried_unresolved_assumptions`
  The unresolved assumptions explicitly carried forward from the parameter bundle.
- `validator_notes`
  A bounded note list describing which family-specific validator checks were exercised.

The result is intentionally small. It is not a generic metadata bag and it is not a hidden proof
channel.

## E. DECISION CLASSES

The minimum decision classes in v1 are:

- `malformed`
  Structural boundary failure in the parameter bundle or variant set.
- `reject`
  Structurally valid candidate, but it fails a bounded validator rule strongly enough that Skill
  Forge should not continue with it.
- `abstain`
  Structurally valid candidate, but current replay-derived evidence is too weak or too boundary
  sensitive for provisional acceptance.
- `accept_candidate`
  Structurally valid candidate with stable enough bounded evidence to move into the next Skill Forge
  stage.

`accept_candidate` is provisional acceptance only. It is not proof that the skill is truly low
boost, reachable, or successful.

## F. CONFIDENCE MODEL V1

The v1 confidence model is intentionally narrow.

### What confidence is allowed to mean

Confidence in this pass is only a bounded claim about:

- whether the parameter bundle remains structurally consistent
- whether the exact and trimmed variants preserve a stable boundary interpretation
- whether the unresolved assumption burden stayed explicit instead of being hidden
- whether the validator rules produced one coherent family-specific outcome

### What confidence is not allowed to mean

Confidence does not mean:

- replay truth
- physics proof
- reachability proof
- contact proof
- low-boost proof
- recovery success proof

### Confidence bands

- `insufficient_evidence`
  Used for malformed or rejected cases where the validator cannot support progression.
- `boundary_sensitive`
  Used for abstain cases where the window interpretation is too sensitive to tiny trims.
- `boundary_stable`
  Used only for provisional acceptance where the exact window clears the minimum evidence floor and
  the trim probes remain stable enough for this bounded contract.

## G. ABSTAIN LOGIC

Abstain must remain a first-class output.

In v1, abstain is mandatory when all of the following hold:

- the parameter bundle is structurally valid
- the exact reference variant is structurally valid
- the tiny trim-probe variant set is structurally valid
- the exact window clears the minimum reject floor
- one-frame boundary trims collapse the evidence surface below the validator stability floor

Concrete v1 abstain trigger:

- exact window duration is `2` frames, so both one-frame trim variants remain legal but each
  trimmed window is only `1` frame long

This is treated as insufficiently stable evidence, not as proof that the candidate is false.

## H. REJECT VS ABSTAIN VS ACCEPT OWNERSHIP

- `malformed`
  The bundle or variant set violates the declared low-boost-recovery validation contract itself.
- `reject`
  The contract shape is intact, but the exact observed-window evidence falls below the minimum
  validator evidence floor.
- `abstain`
  The contract shape is intact and the exact window is not obviously unusable, but trim sensitivity
  is too high to continue honestly.
- `accept_candidate`
  The contract shape is intact, the exact window clears the minimum evidence floor, and the trim
  probes preserve a bounded stable interpretation.

Current bounded evidence floors:

- reject floor: exact window duration less than `2` frames
- abstain floor: any required trim-probe window duration less than `2` frames

## I. NON-GOALS

This pass does not do any of the following:

- no physics proof
- no true low-boost proof
- no contact truth
- no recovery success proof
- no curriculum/export action
- no replay parsing
- no replay mining/search
- no generic validator framework
- no generic confidence framework
- no speculative metadata bags

## J. RELATION TO NEXT STAGES

### Guarantees to curriculum/export shell

If a candidate is `accept_candidate`, later curriculum/export shell work may rely on:

- explicit replay-slice and phase lineage
- explicit variant lineage
- explicit provisional decision status
- explicit bounded confidence label
- explicit unresolved assumptions carried forward

### Guarantees to eval harness work

Later eval work can distinguish:

- malformed boundary failure
- bounded validator rejection
- real abstain because evidence is too weak
- provisional acceptance under the current low-boost-recovery contract

### Explicitly not guaranteed yet

This pass does not guarantee:

- recovery correctness
- low-boost correctness
- contact correctness
- physical reachability
- teachability beyond this bounded provisional surface
- downstream consumer improvement
