# MIMIR Skill Forge v1

## A. Purpose

### What Skill Forge is

Skill Forge is the MIMIR subsystem that turns a narrow replay-derived slice into a reusable,
auditable skill artifact plus the minimum downstream teaching outputs needed to train or consume
that skill later.

### Why it exists

MIMIR needs a path from observed high-value play fragments to repeatable teaching assets without
pretending that one replay snippet is enough by itself. Skill Forge exists to:

- capture a concrete skill seed from a replay slice
- normalize that seed into a canonical form
- expand it through structured, bounded variation
- reject variants that are not physically or operationally credible
- emit a curriculum/export surface that later training or runtime consumers can use

### How it differs from a generic replay analyzer

A generic replay analyzer tries to describe or summarize what happened. Skill Forge is narrower
and more operational:

- it is not a full replay-universe parser
- it is not a statistics dashboard
- it is not a passive labeler
- it exists to compile a replay slice into a skill object with downstream teaching value

### Key principle

Skill Forge v1 is one-shot skill extraction plus structured expansion.

It is not miracle one-shot learning.

The replay slice provides a seed, not a finished policy. Generalization comes from
canonicalization, phase extraction, parameter solving, bounded variation, validation, curriculum,
and export.

## B. Position In The Overall MIMIR System

Skill Forge sits between raw evidence and downstream consumers.

- Teacher factory
  Skill Forge produces skill objects and teaching surfaces that later teacher systems can consume.
- Skill compiler
  Its primary role is compilation: replay slice to canonical skill representation.
- Curriculum generator
  It emits staged practice structure rather than only a single artifact.
- Runtime bridge
  It defines the future handoff boundary for runtime option/fallback consumers, but v1 does not
  implement that live bridge.
- Training export bridge
  It defines what later BC, DAgger, PPO-auxiliary, or other training exporters will consume.

Relation to deterministic-family work already completed:

- deterministic fake-backend vertical-slice work remains closed infrastructure
- Skill Forge v1 is additive and downstream of that closure discipline
- the closed deterministic family remains a contract seed for how MIMIR documents boundaries,
  evidence, staged delivery, and no-change rules
- Skill Forge v1 does not rewrite deterministic-family scope, export-bundle semantics, or runtime
  cleanup boundaries

## C. V1 Scope

### Included now

- a narrow architecture/spec for replay-slice-to-skill compilation
- one first prototype skill family
- one first vertical slice through the full pipeline shape
- minimal canonical artifacts required for that slice
- explicit confidence, abstain, and anti-target roles
- explicit consumer paths and evaluation gates

### Not included now

- full replay ingestion across arbitrary matches or large corpora
- real replay parsing implementation
- real rollout physics implementation
- async/background orchestration
- database/storage systems beyond existing explicit artifact discipline
- runtime CLI expansion
- broadened export-bundle semantics
- broad multi-skill, multi-family orchestration
- speculative metadata or abstraction layers without a first vertical-slice consumer

## D. Core Pipeline

The first Skill Forge vertical slice is:

`replay slice -> canonical skill state -> event/contact graph -> phase plan -> parameter bundle -> generated variants -> validated skill object -> curriculum -> export package -> eval hook`

### 1. Replay Slice Ingestor

- Input
  A narrow replay-slice payload referencing one candidate skill occurrence plus the minimum state
  window needed around it.
- Output
  `ReplaySlice`
- Responsibility
  Admit a bounded slice with explicit provenance and frame/state boundaries.
- Out-of-scope
  Real replay parsing, corpus search, automatic slice mining across large datasets.
- Likely failure modes
  wrong frame window, stale provenance, incomplete state window, ambiguous slice ownership,
  hidden dependency on unavailable replay semantics.

### 2. State Canonicalizer

- Input
  `ReplaySlice`
- Output
  `CanonicalSkillState`
- Responsibility
  Transform slice-local state into a normalized, orientation-stable, phase-ready representation
  for the chosen skill family.
- Out-of-scope
  Full universal game-state normalization for every future skill family.
- Likely failure modes
  inconsistent frame orientation, mixed local/world coordinates, hidden side bias,
  normalization drift, omitted state needed by downstream phase extraction.

### 3. Event / Contact Graph Extractor

- Input
  `CanonicalSkillState`
- Output
  `EventContactGraph`
- Responsibility
  Extract the minimal event graph needed to describe support contacts, detach points, landing
  transitions, boost state changes, and other family-relevant transitions.
- Out-of-scope
  Full semantic replay annotation, opponent intent inference, broad tactical labeling.
- Likely failure modes
  missed contacts, duplicated contact edges, wrong temporal ordering, family-irrelevant graph
  bloat, inferred semantics disguised as observed events.

### 4. Phase Segmenter

- Input
  `CanonicalSkillState` and `EventContactGraph`
- Output
  `PhasePlan`
- Responsibility
  Split the skill seed into explicit phases that downstream solving and validation can reason
  about.
- Out-of-scope
  Generic universal phase libraries for all mechanics.
- Likely failure modes
  over-segmentation, under-segmentation, phase boundaries that do not line up with controllable
  transitions, hidden dependence on future physics rollout.

### 5. Skill Parameter Solver

- Input
  `CanonicalSkillState`, `PhasePlan`
- Output
  `ParameterBundle`
- Responsibility
  Solve the minimum family-relevant parameters that explain the skill seed in a reusable way.
- Out-of-scope
  High-dimensional policy fitting, broad learned latent inference.
- Likely failure modes
  overfitting to one seed, guessed parameters with no audit trail, underconstrained solutions,
  parameter sets that are not controllable by downstream consumers.

### 6. Variation Engine

- Input
  `ParameterBundle`
- Output
  `GeneratedVariant[]`
- Responsibility
  Produce bounded, structured variations around the solved skill, not unlimited search.
- Out-of-scope
  Open-ended novelty search, broad procedural content generation, policy learning.
- Likely failure modes
  feature sprawl, invalid parameter combinations, semantically duplicated variants, family drift
  beyond the original skill intent.

### 7. Feasibility / Reachability Validator

- Input
  `GeneratedVariant[]`
- Output
  `ValidatedVariant[]` plus rejection reasons
- Responsibility
  Reject unreachable, contradictory, or unsafe variants before synthesis/export.
- Out-of-scope
  Full RocketSim-backed proof search, high-fidelity rollout verification.
- Likely failure modes
  false acceptance, false rejection, validator criteria hidden inside opaque heuristics,
  silent fallback to accepting unknown cases.

### 8. Skill Synthesizer

- Input
  validated variants, provenance, phase and parameter outputs
- Output
  `SkillObjectV1`
- Responsibility
  Assemble one reusable skill artifact with explicit preconditions, phase plan, bounded
  parameterization, and failure/recovery surfaces.
- Out-of-scope
  broad ontology building, multi-skill clustering, generic abstraction layers.
- Likely failure modes
  bloated object shape, ambiguous provenance, mixing seed facts with generated facts, fake
  completeness in omitted fields.

### 9. Curriculum Builder

- Input
  `SkillObjectV1`
- Output
  `CurriculumSpec`
- Responsibility
  Emit a small staged progression from easier validated instances toward harder ones.
- Out-of-scope
  full training-plan orchestration, large-scale lesson graph generation.
- Likely failure modes
  difficulty ordering not tied to actual parameters, impossible early tasks, no abstain path for
  unreachable tasks.

### 10. Export Bridge

- Input
  `SkillObjectV1`, `CurriculumSpec`
- Output
  `ExportPackage`
- Responsibility
  Package the vertical-slice outputs for the first downstream consumer shell without widening
  export-bundle semantics.
- Out-of-scope
  broad adapter matrix, new runtime CLI commands, generalized external schema sprawl.
- Likely failure modes
  widened bundle semantics, speculative fields for consumers that do not exist yet, unstable
  artifact identity.

### 11. Eval Hook

- Input
  `ExportPackage` and chosen prototype-family eval definition
- Output
  reproducible eval record
- Responsibility
  Provide the minimum proof surface that the vertical slice produced a reusable teaching asset.
- Out-of-scope
  final production benchmarking suite, full multi-family leaderboards.
- Likely failure modes
  measuring only artifact existence, no baseline comparison, no rejection metrics, success claims
  without intervention evidence.

## E. Canonical Data Model

The v1 data model stays minimal and tied to one prototype family.

### ReplaySlice

- `slice_id`
- `source_replay_ref`
- `frame_window`
- `subject_car_ref`
- `family_hint`
- `raw_state_window_ref`

### SkillSeed

- `seed_id`
- `slice_id`
- `seed_family`
- `trigger_summary`
- `seed_quality_note`

### CanonicalSkillState

- `seed_id`
- `canonical_frame`
- `normalized_subject_state`
- `normalized_environment_state`
- `normalization_notes`

### EventContactGraph

- `seed_id`
- `nodes`
- `edges`
- `time_order`

### PhasePlan

- `seed_id`
- `phase_family`
- `phases`
- `phase_transitions`

### ParameterBundle

- `seed_id`
- `family`
- `solved_parameters`
- `parameter_bounds`
- `solver_notes`

### GeneratedVariant

- `variant_id`
- `seed_id`
- `parameter_overrides`
- `difficulty_hint`
- `generation_reason`

### SkillObjectV1

- `skill_id`
- `skill_family`
- `provenance`
- `preconditions`
- `phase_plan`
- `control_hints`
- `parameter_ranges`
- `failure_modes`
- `recovery_hooks`
- `generated_variants`
- `quality_axes`

### CurriculumSpec

- `curriculum_id`
- `skill_id`
- `tiers`
- `promotion_rules`
- `abstain_rules`

### ExportPackage

- `export_id`
- `skill_id`
- `consumer_kind`
- `artifact_refs`
- `export_notes`

## F. Skill Object V1

`SkillObjectV1` is the minimum reusable unit Skill Forge produces.

### Required fields

- `skill_id`
  Stable artifact identity for this compiled skill object.
- `skill_family`
  First vertical slice uses one prototype family only.
- `provenance`
  Source replay slice reference, seed id, and generation lineage.
- `preconditions`
  Minimum state assumptions under which the skill is intended to fire.
- `phase_plan`
  Ordered controllable phases with phase transition criteria.
- `control_hints`
  Narrow hints describing controllable intent per phase. These are not policy outputs.
- `parameter_ranges`
  Solved parameters plus bounded variation ranges actually used by generated variants.
- `failure_modes`
  Explicit known ways the skill can fail.
- `recovery_hooks`
  What the consumer should do when a failure mode or abstain boundary is hit.
- `generated_variants`
  Only validated variants tied to the same family and seed lineage.
- `quality_axes`
  Minimum v1 scored axes:
  - transferability
  - repeatability
  - controllability
  - tactical_value
  - execution_cost
  - recovery_safety
  - confidence

### Fields intentionally not required in v1

- broad taxonomic tags with no first consumer
- opaque embedding vectors
- universal opponent-model fields
- speculative runtime policy parameters
- database identifiers
- multi-consumer adapter payloads for consumers that do not exist yet

## G. Confidence / Abstain / Anti-Target Logic

### Confidence

Confidence in v1 is a bounded claim about whether the compiled skill object and its generated
variants remain faithful, controllable, and reusable for the chosen family.

What must exist in v1:

- confidence recorded on the skill object
- confidence informed by provenance quality, phase stability, parameter solver stability, and
  validator acceptance quality
- confidence visible to export and eval consumers

What comes later:

- learned confidence calibration
- large-scale cross-replay statistical confidence models

### Abstain

Abstain is mandatory in v1.

Skill Forge must be able to say:

- the seed is too ambiguous to compile
- the parameter solution is underconstrained
- a generated variant is outside the validated family envelope
- the prototype consumer should not teach or invoke this skill in the current state

Abstain is not failure to build the system. It is the guardrail against fake completeness.

### Anti-targets / negative teaching

Anti-targets define what the system should explicitly avoid teaching as if it were part of the
target skill family.

What must exist in v1:

- a narrow anti-target list per prototype family
- explicit rejection or abstain reasons for variants that cross into that list

What comes later:

- richer negative example mining
- adversarial family-boundary discovery

## H. First Prototype Skill Family Decision Criteria

The first prototype family should be chosen for vertical-slice clarity, not highlight-reel value.

Required criteria:

- frequent enough to source replay slices without a rare-data hunt
- mechanically structured enough to phase cleanly
- narrow enough to canonicalize without a universal replay ontology
- useful enough that success matters beyond the demo
- evaluable without full real-physics infrastructure in v1
- recoverable when the skill fails or abstains

Why recovery-style skills fit first:

- they rely more on car-state transitions than on high-entropy ball/opponent context
- they expose clear preconditions, controllability, and failure boundaries
- they allow bounded variation without pretending the whole game is solved

Why rare flicks come later:

- rarer slice acquisition
- heavier ball-car coupling
- stronger tactical-context dependence
- more ambiguous anti-target boundaries
- higher risk of turning one impressive replay seed into fake generalization claims

The companion artifact `executor_mimir_skill_forge_v1_first_prototype.txt` records the actual v1
choice and ranking.

## I. Eval Requirements

The first vertical slice is only successful if all of the following are true:

- a reusable `SkillObjectV1` exists for the chosen prototype family
- the skill object retains explicit provenance to the seed replay slice
- validated variants are produced and rejected variants are recorded with reasons
- at least one curriculum spec is emitted from the same skill object
- an export shell is emitted for the first intended consumer path
- abstain conditions are exercised, not just success cases
- baseline vs intervention task metrics exist for the chosen family
- the eval record can distinguish:
  - seed compilation succeeded
  - variant generation succeeded
  - validator rejected unsafe variants
  - curriculum/export emitted
  - downstream consumer baseline improved or did not improve

Artifact existence alone is not success.

## J. Export / Consumer Paths

Intended consumers for Skill Forge output are:

- BC export
  Special milestone later. Not the first implementation target in this pass.
- DAgger teacher support
  Skill objects can supply structured teacher examples or recovery targets.
- PPO auxiliary support
  Skill objects can later provide auxiliary objectives, curriculum tiers, or anti-target shaping.
- runtime option/fallback support
  Skill objects can later support narrow runtime option/fallback invocation.

V1 staging rule:

- define the handoff shape
- implement only the first consumer shell that the chosen vertical slice immediately needs
- do not build all adapters at once

## K. BC Milestone Note

Behavior cloning integration is a special milestone.

When the roadmap reaches a real BC consumer phase, that milestone must be flagged explicitly and
treated as a boundary change:

- the consumer contract becomes materially more important
- dataset/export semantics become harder to change casually
- confidence/anti-target handling becomes more consequential

Do not let BC arrive implicitly through gradual adapter sprawl.

## L. Out-Of-Scope For V1

- no full replay-universe ingestion
- no all-at-once multi-skill mining
- no full real-time runtime bridge
- no full real-physics rollout engine
- no broad live orchestration
- no database systems
- no async/background workers
- no runtime CLI expansion
- no export-bundle semantic widening
- no reopening of deterministic-family closure work as if it were the active roadmap
- no all-at-once framework expansion
