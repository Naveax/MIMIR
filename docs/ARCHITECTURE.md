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

- `mimir-replay` owns the first bounded real replay-header parser lane: `ReplayInput::Memory`
  input, three exact admitted version/build tuples, selected header-field mapping, and explicit
  unsupported/malformed boundaries. Replay source materialization, direct file-backed parser
  input, body/network/frame decoding, raw-state extraction, and event extraction remain deferred.
- Skill Forge replay-slice work is currently bounded to shared contract types plus the existing
  family-specific low-boost-recovery transformation surfaces. Real corpus mining and broader
  replay ingestion orchestration remain deferred.
- `mimir-skill` now owns the first family-specific Skill Forge transformation logic:
  low-boost-recovery replay-slice canonicalization plus the minimum event/contact and phase
  extraction boundary. That logic is deliberately narrow and does not add rollout, export,
  runtime, or general replay-body parsing behavior.
- `mimir-anchor`, `mimir-branch`, `mimir-rollout`, and `mimir-teacher` define traits whose
  current implementations only transform explicit caller-provided data.
- `mimir-io` owns raw persisted-artifact serialization, format selection, and artifact
  schema/version validation. It intentionally does not own producer-coupled batch orchestration.
- `mimir-export` owns persisted anchor/branch bundle orchestration, including staged artifact
  writes, `manifest.json` / `index.json` metadata, bundle inspection/loading, and the current
  deterministic candidate/execution-result plumbing. It does not add replay parsing, simulation,
  or inferred game semantics.
- `mimir-sim-bridge` isolates the future simulation boundary behind `SimBackend`.
- `mimir-cache` centralizes cache keys and novelty bookkeeping.

## Design posture

- Prefer data-first contracts over speculative behavior.
- Make deferred work visible through narrow traits and explicit errors.
- Keep fake test infrastructure quarantined and deterministic.
