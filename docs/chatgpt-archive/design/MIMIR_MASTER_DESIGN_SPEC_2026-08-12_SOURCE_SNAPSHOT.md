# SOURCE SNAPSHOT — MIMIR Master Design Specification (2026-08-12)

**Source class:** CURATED_SOURCE_SNAPSHOT
**Original:** `MIMIR_MASTER_DESIGN_SPEC_2026-08-12.md`

Core design intent:
- MIMIR is standalone and independent of BC/DAgger/PPO/SAC/runtime.
- Replay states are search seeds, not absolute teacher truth.
- Anchor mining and temporal windows are required.
- Control-Onset Rewind is a first-class concept.
- Counterfactual branching must be bounded.
- Micro-rollouts and multi-dimensional scoring are preferred to a single scalar-only view.
- Skill canonicalization, phases and parameter inference are central.
- Teacher outputs include action, option, ranking, anti-target, confidence and value forms.
- Novelty memory and iterative teacher refresh are required.
- Rare moments should become validated skill families rather than one-shot magic.
- Runtime assist should consume precomputed intelligence, not run huge offline searches live.

Historical implementation notes in the original are superseded by current GitHub source.
