# MIMIR V1 Spec

## Purpose

MIMIR is a Rust-first scaffold for future Rocket League replay analysis, counterfactual
branching, skill mining, and teacher synthesis. V1 is intentionally narrow: it defines
trustworthy crate boundaries, stable data contracts, deterministic plumbing, and explicit
deferred areas.

## Included in V1

- Workspace organization for replay, anchors, branching, rollout, scoring, skill,
  teacher, cache, and CLI concerns.
- Serializable core records with explicit ID newtypes.
- Honest stub traits and deterministic test fixtures where no production backend exists.
- A deterministic fake sim backend used only for tests and CLI smoke coverage.

## Explicitly not included in V1

- A Rocket League replay parser.
- A physics rollout engine.
- RocketSim integration.
- Learned anchor detection, branch generation, scoring, skill mining, or teacher logic.

## Acceptance bar

- Stable Rust only.
- Clean `cargo check`, `cargo test`, and `cargo clippy -D warnings`.
- No placeholder heuristics presented as real replay intelligence.
