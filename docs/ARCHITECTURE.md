# Architecture

## Dependency shape

- `mimir-types` contains shared DTOs and ID newtypes, including the bounded Skill Forge replay
  slice seed contract.
- `mimir-core` provides common error handling, config loading, small shared traits, and
  hashing helpers.
- Domain crates depend downward on `mimir-types` and `mimir-core`, not sideways unless the
  dependency is narrow and explicit.
- `mimir-cli` is an orchestration shell that validates configs and exercises deterministic
  plumbing; it is not the home of domain logic.

## Extension points

- `mimir-replay` exposes replay input abstractions so a real parser can be added later.
- Skill Forge replay-slice work is currently bounded to shared contract types only. Real replay
  parsing, corpus mining, and broader ingestion orchestration remain deferred.
- `mimir-skill` now owns the first family-specific Skill Forge transformation logic:
  low-boost-recovery replay-slice canonicalization plus the minimum event/contact and phase
  extraction boundary. That logic is deliberately narrow and does not add parser, rollout, export,
  or runtime behavior.
- `mimir-anchor`, `mimir-branch`, `mimir-rollout`, and `mimir-teacher` define traits whose
  current implementations only transform explicit caller-provided data.
- `mimir-sim-bridge` isolates the future simulation boundary behind `SimBackend`.
- `mimir-cache` centralizes cache keys and novelty bookkeeping.

## Design posture

- Prefer data-first contracts over speculative behavior.
- Make deferred work visible through narrow traits and explicit errors.
- Keep fake test infrastructure quarantined and deterministic.
