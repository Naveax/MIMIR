# Test Strategy

## Current test layers

- Unit tests in each major crate cover deterministic, honest behavior:
  config loading, serialization, stub conversion, bounded filtering, scoring,
  canonicalization, label passthrough, cache novelty, and fake backend determinism.
- A CLI integration smoke test runs the `loop` command with the deterministic fake backend.

## What the tests prove

- The workspace compiles end to end on stable Rust.
- Stub implementations do only the narrow work they claim to do.
- The fake backend is deterministic and is wired through the real CLI binary.

## Future work

- Replay parser fixture tests once a real parser exists.
- Golden artifact tests for serialized pipeline outputs.
- Differential tests between future simulation backends and expected contracts.
