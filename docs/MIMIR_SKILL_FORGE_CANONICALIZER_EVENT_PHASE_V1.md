# MIMIR Skill Forge Canonicalizer + Event / Phase Contract v1

## A. PURPOSE

### What this pass owns

This pass owns the minimum family-specific transformation from `ReplaySliceRef` into:

- `LowBoostRecoveryCanonicalStateV1`
- `LowBoostRecoveryEventContactGraphV1`
- `LowBoostRecoveryPhasePlanV1`

### Why it exists

The replay-slice ingestor contract proves only bounded seed shape validity. Downstream solver and
validator stages still need one stable, auditable state boundary that:

- preserves slice identity and provenance
- preserves bounded frame ownership
- states what was normalized versus what is still unresolved
- exposes the minimum event and phase scaffolding needed for later low-boost-recovery reasoning

### How it differs from adjacent stages

- Replay ingestion owns shape validity of `ReplaySliceRef`.
- This pass owns family-specific canonicalization and the minimum deterministic extraction surface.
- Later solver, variation, and validator passes own semantic sufficiency, family fitness, and any
  stronger claims about low boost recovery truth.

This pass does not prove replay truth. It stabilizes the bounded seed boundary for the chosen
family only.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this pass.

That matters because the canonicalization choices here are intentionally biased toward a
subject-centric recovery seed:

- one subject only
- one bounded candidate recovery window
- no universal ball/opponent semantics
- no generic all-mechanics event graph
- no claim that the same canonical frame is correct for other families

Any broader family support is a later explicit boundary change.

## C. INPUT BOUNDARY

### Assumed from `ReplaySliceRef`

Guaranteed input fields:

- `slice_id`
- `source_replay.replay_id`
- `source_replay.provenance_label`
- `frame_window.start`
- `frame_window.end_exclusive`
- `subject`
- `family_hint`
- `raw_state_window_ref`
- optional `audit_note`

### What is guaranteed versus unresolved

Guaranteed now:

- one bounded seed identity
- one bounded replay provenance handle
- one bounded frame window
- one replay-local subject handle
- one bounded raw-state-window linkage
- one declared family hint

Explicitly unresolved at this boundary:

- raw-state materialization details
- boost amount truth
- contact truth
- orientation truth
- landing truth
- recovery success truth
- tactical value or outcome

## D. CANONICAL STATE V1

`LowBoostRecoveryCanonicalStateV1` is the minimum canonical state shape for this pass.

### Fields

- `slice_id`
  Canonical state remains anchored to the input replay slice.
- `source_replay`
  Replay id plus provenance label are preserved unchanged.
- `subject`
  The replay-local subject handle is preserved unchanged.
- `frame_window`
  The canonical window is exactly the bounded replay slice window.
- `raw_state_window_ref`
  Canonical state keeps the bounded raw-state linkage without materializing parser payloads.
- `orientation_note`
  `subject_anchored_window_only`
- `subject_state_envelope`
  - `subject`
  - `frame_window`
  - `semantics = raw_state_window_reference_only`
- `environment_state_envelope`
  - `frame_window`
  - `semantics = raw_state_window_reference_only`
- `canonicalization_notes`
  Fixed unresolved-note list for this pass:
  - `boost_amount_unresolved`
  - `contact_truth_unresolved`
  - `recovery_success_unresolved`
  - `replay_orientation_normalization_deferred`

### Canonical frame note meaning

`subject_anchored_window_only` means:

- the canonicalizer stabilizes ownership around one subject and one bounded window
- it does not claim a global left/right field flip or a full coordinate transform
- it does not claim numeric normalization from replay state into solved parameters

## E. EVENT / CONTACT GRAPH V1

`LowBoostRecoveryEventContactGraphV1` is intentionally narrow.

### Goal

Expose the minimum deterministic event structure that later stages can depend on without
inventing contact truth.

### Fields

- `slice_id`
- `frame_window`
- `nodes`
  Exactly two nodes in this pass:
  - `slice_window_start` at `frame_window.start`
  - `slice_window_end_exclusive` at `frame_window.end_exclusive`
- `edges`
  Exactly one edge in this pass:
  - `observed_slice_window` from start node to end node
- `contact_semantics`
  `unresolved_from_replay_slice_contract`

### What this graph means

It is a bounded event scaffold, not a universal replay event graph. It records only:

- where the candidate recovery window begins
- where the candidate recovery window ends
- that no stronger contact claim is made yet

## F. PHASE PLAN V1

`LowBoostRecoveryPhasePlanV1` is the minimum deterministic phase representation for this pass.

### Fields

- `slice_id`
- `phases`
  Exactly one phase:
  - `candidate_recovery_window`
    - `start = frame_window.start`
    - `end_exclusive = frame_window.end_exclusive`

### Why phase count is one

This pass does not have enough trusted semantics to split the seed into subphases such as detach,
landing, or stable regain without pretending to know contact, boost, or recovery truth. One phase
is the narrow auditable representation that keeps the next solver/validator stages honest.

## G. REQUIRED VS OPTIONAL SEMANTICS

### Explicitly derivable now

- seed identity linkage
- replay provenance linkage
- bounded subject linkage
- bounded frame ownership
- bounded raw-state linkage
- family-specific canonical ownership
- deterministic event-boundary scaffold
- deterministic one-phase candidate window

### Intentionally unresolved now

- whether the subject is actually below a low-boost threshold
- whether any support, wall, floor, or ball contact occurred
- whether the slice contains a successful recovery
- whether the chosen window is semantically sufficient for later solving
- any tactic-wide or outcome-wide interpretation

## H. FAILURE / ABSTAIN OWNERSHIP

### Reject in this pass

Reject the input as malformed when:

- `family_hint != low_boost_recovery`
- `slice_id` is blank
- `source_replay.replay_id` is blank
- `source_replay.provenance_label` is blank after trimming
- `subject` is blank
- `raw_state_window_ref` is blank
- `frame_window.start >= frame_window.end_exclusive`

These are malformed boundary failures, not abstains.

### Pass through as semantically incomplete

Allow the input through with unresolved notes when:

- low-boost threshold is not proven
- contacts are not proven
- orientation normalization is not proven
- recovery success is not proven

Those remain validator/solver ownership questions later.

## I. NON-GOALS

This pass does not do any of the following:

- real replay parsing
- corpus-wide replay ingestion or mining
- real rollout or physics proof
- generalized all-family canonicalization
- universal contact truth
- low-boost threshold proof
- tactical value inference
- recovery success proof
- runtime invocation hints
- curriculum or export logic
- confidence scoring beyond explicit unresolved-boundary notes
- speculative metadata bags

## J. RELATION TO NEXT STAGES

### Guarantees to parameter solver

- one family-specific canonical state boundary exists
- one deterministic event scaffold exists
- one deterministic candidate phase window exists
- malformed boundary inputs were already rejected

### Guarantees to variation engine

- generated variations can anchor themselves to one bounded candidate recovery window
- variation work does not need to rediscover slice identity or window ownership

### Guarantees to validator

- validator can distinguish malformed boundary failures from unresolved semantic questions
- validator receives an explicit list of unresolved claims that this pass did not pretend to solve

### Explicitly not guaranteed yet

- parameter solvability
- semantic sufficiency of the replay slice
- physical reachability
- contact correctness
- recovery correctness
- consumer/export readiness
