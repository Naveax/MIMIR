# Contributing to MIMIR

MIMIR uses a truth-first development rule:

> A capability is not considered complete without code, tests, and evidence.

## Required local checks

Run:

```powershell
pwsh -File scripts/verify_repo.ps1
```

The verification gate covers formatting, locked workspace checking, replay/skill/workspace tests,
clippy, export surface enumeration, checked-in replay-corpus verification, a 100-row replay
compatibility matrix plus summary, and replay-version-tuple ranking consistency checks.

## Repository boundaries

Do not commit:

- `target/` build output
- IDE state
- full replay corpora
- training checkpoints
- generated caches
- transient logs
- credentials or secrets

The small checked-in replay corpus exists for deterministic regression/stress testing only.

Do not silently widen MIMIR capability claims. Unsupported or unproven boundaries should remain explicit.

## External contributions

MIMIR is proprietary and is not an open-source or source-available project.

External contributions are not accepted for incorporation. Do not submit patches or pull requests for incorporation into MIMIR.

Opening an issue, discussion, suggestion, patch, pull request, or other communication grants no right to use, copy, modify, compile, execute, distribute, study, benchmark, train on, or otherwise exploit MIMIR or any part of this repository.

See `LICENSE` for the controlling terms.
