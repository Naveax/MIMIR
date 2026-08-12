# MIMIR Skill Forge Replay Slice Contract v1

## A. Purpose

### What this contract is

This contract defines the bounded input shape for one Skill Forge seed occurrence before any
canonicalization, event extraction, or phase segmentation happens.

The v1 replay slice is not a parsed replay, not a mined dataset row, and not a universal gameplay
ontology. It is the minimum auditable seed boundary for one candidate low-boost-recovery
occurrence.

### Why it exists

Downstream Skill Forge stages cannot be trusted until the seed boundary is explicit about:

- which replay occurrence is being referenced
- which subject the occurrence belongs to
- which frame window is in scope
- which bounded raw-state window later stages are allowed to depend on
- which prototype family this slice claims to target

### Why v1 keeps it bounded and family-specific

The first vertical slice must prove one clean family-specific seed path before the project opens
broader replay ingestion semantics. A narrow contract reduces fake completeness, guessed replay
semantics, and silent cross-family drift.

## B. V1 Target Family

`low_boost_recovery` is the only valid target family for this contract version.

This contract is intentionally not universal yet because:

- low boost recovery is the chosen first prototype family
- later families may need different subject, contact, or context semantics
- forcing a universal replay-slice schema now would invite speculative fields with no first
  consumer

Any future multi-family contract must be a later explicit boundary change, not a quiet extension of
this v1 seed.

## C. Replay Slice Boundary

A contract-valid replay slice must contain exactly these bounded elements:

### 1. Slice identity

- `slice_id`
  Stable caller-assigned identity for this candidate slice.

### 2. Source replay reference and provenance

- `source_replay_ref`
  Stable replay identifier within the MIMIR workspace boundary.
- `provenance_label`
  Human-auditable provenance handle that identifies the concrete source replay material used to
  produce this slice reference. In v1 this is a bounded label, not a full parser transcript.

### 3. Frame / time window

- `frame_window.start`
- `frame_window.end_exclusive`

The window must be bounded and non-empty. It defines the only frame interval this slice claims as
its seed evidence window.

### 4. Subject entity identity

- `subject`

This identifies the one replay subject for which the low-boost-recovery occurrence is claimed.
V1 treats it as an opaque replay-local subject handle. The contract does not yet universalize
player-id, actor-id, or roster semantics.

### 5. Family hint

- `family_hint`

The only valid value in v1 is `low_boost_recovery`.

### 6. Raw-state-window linkage

- `raw_state_window_ref`

This is a bounded reference to the raw state material that later canonicalizer and event/phase
passes are allowed to inspect. It is intentionally a linkage handle, not a parser implementation or
storage design.

### 7. Optional audit notes

- `audit_note`

Optional single-note field for bounded human review context. This is not a generic metadata escape
hatch.

## D. Required Vs Optional Fields

### Required now

- `slice_id`
- `source_replay_ref`
- `provenance_label`
- `frame_window.start`
- `frame_window.end_exclusive`
- `subject`
- `family_hint`
- `raw_state_window_ref`

### Optional now

- `audit_note`

### Explicitly not optional-by-default

- provenance
- frame window
- subject identity
- family hint
- bounded state linkage

If any of those are missing, the slice is invalid and must be rejected at the ingestor boundary.

## E. Non-Goals

This contract does not provide:

- real replay parsing
- corpus-wide replay mining or search
- universal multi-family replay semantics
- rollout or physics proof
- tactic-wide inference about intent, pressure, or outcome
- hidden runtime consumer logic
- export bundle widening
- persistence format expansion by implication

## F. Validity Rules

A replay slice is contract-valid only if all of the following hold:

1. `slice_id` is present and non-empty.
2. `source_replay_ref` is present and non-empty.
3. `provenance_label` is present and non-empty.
4. `frame_window.start < frame_window.end_exclusive`.
5. `subject` is present and non-empty.
6. `family_hint == low_boost_recovery`.
7. `raw_state_window_ref` is present and non-empty.

The slice is invalid if any of the following occur:

- missing provenance
- empty or inverted frame window
- ambiguous or missing subject handle
- missing bounded raw-state linkage
- family hint outside `low_boost_recovery`
- a slice that tries to imply multiple subjects or multiple family intents through one contract

## G. Failure / Abstain Boundary

### Reject at ingestor contract boundary

Reject the slice immediately when the contract itself is malformed or under-specified:

- required field missing
- frame window invalid
- family hint invalid for this contract version
- subject handle absent
- raw-state-window linkage absent

### Defer to later-stage abstain

Later stages may abstain when the contract is valid but the skill seed is still unusable for
family-specific reasoning, for example:

- canonicalized low-boost-recovery interpretation is ambiguous
- extracted events do not support a coherent recovery phase structure
- the slice is valid but not actually a usable low-boost-recovery seed

The ingestor boundary owns shape validity. Later stages own semantic sufficiency.

## H. Low Boost Recovery-Specific Assumptions

Downstream stages may rely only on these narrow assumptions from this contract:

- the slice claims one candidate low-boost-recovery occurrence
- the slice points to one subject, not a team-level or tactic-level aggregate
- the evidence window is bounded
- later stages have one bounded raw-state linkage they may inspect

Downstream stages may not rely on this contract alone to prove:

- boost amount thresholds
- contact correctness
- orientation normalization
- landing quality
- tactical value
- recovery success

Those belong to later canonicalizer, extractor, and validator work.

## I. Relation To Downstream Stages

### Canonicalizer

Guaranteed:

- stable slice identity
- replay provenance handle
- bounded frame window
- one subject handle
- one family hint
- one bounded raw-state linkage

Not guaranteed:

- normalized coordinates
- low-boost confirmation
- subject/world orientation
- complete state materialization

### Event / contact extractor

Guaranteed:

- the extractor can anchor its work to one validated seed boundary

Not guaranteed:

- contact truth
- boost transitions
- landing events
- event ordering beyond the bounded frame window itself

### Phase segmenter

Guaranteed:

- one family-specific seed boundary exists for later segmentation work

Not guaranteed:

- valid phase transitions
- controllable phase boundaries
- recovery-family success/failure interpretation

## J. Out-Of-Scope Fields For Now

The following tempting fields are intentionally excluded until a later pass proves a concrete need:

- parsed per-frame state payloads inside the contract itself
- ball or opponent semantic annotations
- universal player-id / actor-id / roster schemas
- boost values, contact labels, or landing labels
- inferred tactic name or tactical outcome
- confidence scores
- curriculum/export metadata
- database identifiers
- runtime invocation hints
- multi-note metadata bags
