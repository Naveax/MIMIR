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

## Contribution authorization

MIMIR is proprietary and is not an open-source project. External contributions are not accepted for incorporation unless the repository owner has expressly authorized the contribution in writing under separate terms sufficient to permit incorporation. Opening an issue, discussion, suggestion, patch, or pull request does not grant any right to use MIMIR or any part of the repository. See `LICENSE`.
