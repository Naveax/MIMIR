# Contributing to MIMIR

MIMIR uses a truth-first development rule:

> A capability is not considered complete without code, tests, and evidence.

## Start from current authority

Before changing code or documentation:

1. Read `MIMIR_CONTINUE_HERE.md` for the current canonical pass, production hard stop, and required reading order.
2. Read `AGENTS.md` for repository execution rules, including parallel work ownership and GitHub Actions de-duplication.
3. Inspect fresh `main` and the source/tests directly related to the intended change.
4. Treat historical executor/status documents and archived planning material as evidence and design history, not as stronger authority than fresh source, tests, current continuity, and exact validation receipts.

Do not silently widen MIMIR capability claims. Unsupported or unproven boundaries must remain explicit.

## Required local verification

Run the canonical repository gate from PowerShell:

```powershell
pwsh -NoProfile -File scripts/verify_repo.ps1
```

The gate currently covers:

- formatting checks;
- locked workspace checking across all targets and features;
- focused replay and skill tests;
- the full workspace test suite;
- clippy with warnings denied;
- export test-surface enumeration;
- checked-in replay corpus integrity verification;
- replay compatibility matrix generation and its 100-row summary invariants;
- deterministic replay-version tuple ranking and coverage invariants.

Do not replace the canonical gate with a shorter convenience wrapper when producing admission or validation evidence.

## GitHub Actions discipline

Before dispatching, rerunning, or otherwise causing equivalent CI work, check for an existing queued, waiting, requested, pending, or in-progress run for the same workflow identity and exact head SHA/input. If one exists, reuse and monitor that run instead of creating another.

A rerun is a retry mechanism, not a polling mechanism. While CI is running, use independent workstreams rather than repeatedly creating equivalent Actions runs.

Validation-only pull requests must stay unmerged unless the applicable canonical process explicitly admits their contents. Close them unmerged after their exact-head validation purpose is complete.

## Repository boundaries

Do not commit:

- `target/` build output;
- IDE state;
- training checkpoints;
- generated caches;
- transient logs;
- credentials or secrets;
- replay data outside the explicitly admitted checked-in fixture/corpus sets.

The checked-in historical replay fixtures and the bounded regression/stress corpus are deliberate repository evidence. Do not replace, regenerate, broaden, or normalize them casually; their identity and admission status matter to replay validation.

## External contributions

MIMIR is proprietary and is not an open-source or source-available project.

External contributions are not accepted for incorporation. Do not submit patches or pull requests for incorporation into MIMIR.

Opening an issue, discussion, suggestion, patch, pull request, or other communication grants no right to use, copy, modify, compile, execute, distribute, study, benchmark, train on, or otherwise exploit MIMIR or any part of this repository.

See `LICENSE` for the controlling terms.
