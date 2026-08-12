# Contributing to MIMIR

MIMIR uses a truth-first development rule:

> A capability is not considered complete without code, tests, and evidence.

## Required local checks

Run:

```powershell
pwsh -File scripts/verify_repo.ps1
```

The verification gate covers formatting, workspace checking, tests, clippy, replay tests, skill tests, and export surface enumeration.

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