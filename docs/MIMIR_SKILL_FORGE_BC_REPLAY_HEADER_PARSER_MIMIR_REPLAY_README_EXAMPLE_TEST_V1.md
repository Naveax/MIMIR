# MIMIR Skill Forge BC Replay Header Parser mimir-replay README / Example Test v1

Pass date: 2026-05-04

## Purpose

This pass implements only the selected Option B candidate from the parser-readiness handoff:

- add a narrow `mimir-replay` README and/or example-style test showing explicit opt-in use of
  `MinimalReplayHeaderReader`

No parser expansion is admitted by this pass.

## Selected Outcome

Selected outcome:

- Outcome A

Narrow `mimir-replay` README/example test implementation is complete.

The implementation documents explicit opt-in use only, does not change parser behavior, and does
not broaden parser-success.

## Files Changed

Changed implementation/doc file:

- `crates/mimir-replay/README.md`

Added pass artifacts:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_MIMIR_REPLAY_README_EXAMPLE_TEST_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_replay_readme_example_test_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_replay_readme_example_test_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_mimir_replay_readme_example_test_status.txt`

No Rust source file was changed.

## README Content Summary

The new `crates/mimir-replay/README.md` states:

- `MinimalReplayHeaderReader` is explicit opt-in only.
- `UnsupportedReplayReader` remains the truthful unsupported default.
- Parser-success is admitted only for `ReplayInput::Memory`, the exact fixture-supported tuple,
  and header-only parsing ending at `8 + header_size`.
- Parser-success is not admitted broadly.
- Callers must provide already admitted bytes and a non-empty admitted label.
- Callers must not derive parser facts from path, hash, filename, provenance, artifact id, fixture
  id, or label convention.
- Successful header parse is not replay-source materialization.
- Successful header parse is not body, raw-state, frame, footer, or event parsing.
- CRC validation is not performed.
- `ReplayInput::File` is unsupported.
- No export, runtime, or CLI behavior is implied.
- No backend parser dependency is used or implied.

The README includes a small explicit opt-in Rust usage sketch that calls:

- `MinimalReplayHeaderReader.read_header(&ReplayInput::Memory { label, bytes })`

The sketch is explicitly scoped to callers that already hold admitted bytes and a non-empty
admitted label.

## Example Test Decision

No new example-style test was added.

Reason:

- `crates/mimir-replay/src/lib.rs` already contains a sufficiently clear explicit opt-in fixture
  happy-path test:
  - `minimal_reader_parses_rl_replay_header_fixture_001_and_header_only_slice`
- That test directly constructs `MinimalReplayHeaderReader`.
- It directly calls `read_header` with `ReplayInput::Memory`.
- It verifies the fixture-specific happy path.
- It verifies that a complete header-only slice ending at `8 + header_size` parses without body
  bytes.

Adding another test would duplicate existing coverage without increasing the admitted boundary.

## Why Parser Scope Was Not Broadened

This pass changed documentation only. It did not modify parser code, traits, reader selection,
tests, manifests, lockfiles, dependencies, CLI/runtime code, export code, or data contracts.

The README repeats the required guardrail:

Parser-success is admitted only for ReplayInput::Memory, the exact fixture-supported tuple, and header-only parsing ending at 8 + header_size. Parser-success is not admitted broadly.

The README also states that path, hash, filename, provenance, artifact id, fixture id, or labels do
not create parser facts.

## Forbidden Boundaries Preserved

Preserved boundaries:

- no `mimir-skill` change
- no `mimir-cli` change
- no `mimir-io` change
- no `mimir-export` change
- no `mimir-types` change
- no root `Cargo.toml` change
- no root `Cargo.lock` change
- no dependency addition
- no backend replay parser dependency
- no CLI/runtime behavior
- no export behavior
- no `ReplayInput::File` support
- no `UnsupportedReplayReader` behavior change
- no CRC validation
- no body/raw-state/frame/event parsing
- no nested array semantic parsing
- no UTF-16 support
- no broad version-family support
- no unencountered property-kind support

## Next Stage

Outcome A next stage:

- move to the next evidence/fixture/parser-readiness target, or
- separately reopen a future `mimir-skill` seam only with a new explicit planning pass

No broad parser expansion is admitted yet.
