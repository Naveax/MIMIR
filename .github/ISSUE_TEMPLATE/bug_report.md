---
name: Bug report
about: Report a reproducible MIMIR defect without publishing secrets or private data
title: "[Bug] "
labels: []
assignees: []
---

## Before posting

Do **not** paste passwords, API tokens, cookies, private keys, `.env` contents, account credentials, private repository URLs, personal data, or unrelated local files into a public issue.

Do not upload a replay, corpus file, log bundle, crash dump, screenshot, or generated artifact merely because it exists. First reduce the report to the minimum evidence needed. If the evidence may contain sensitive/security-relevant material, follow `SECURITY.md` instead of publishing it here.

## Exact repository state

- MIMIR commit SHA:
- Branch/ref:
- Local modifications (`git status --short`), if any:

## Environment

- OS and version:
- Rust version (`rustc --version`):
- Cargo version (`cargo --version`):
- PowerShell version, if relevant:
- Other directly relevant runtime/tool versions:

## Reproduction

Provide the smallest deterministic reproduction you can.

1.
2.
3.

Command(s):

```text
<minimal command sequence>
```

## Expected behavior

Describe the exact contract/result you expected.

## Actual behavior

Describe the exact observed result. Include the smallest relevant error excerpt rather than an entire unrestricted log.

```text
<minimal error excerpt>
```

## Evidence identity

If a file is genuinely required to reproduce the defect, provide identity first rather than blindly uploading it:

- file role/purpose:
- byte length:
- SHA-256 or existing repository receipt:
- whether it is already checked into this public repository:
- whether it may contain personal, credential, proprietary, or security-sensitive data:

For replay/corpus/artifact defects, identify the already-admitted checked-in fixture/corpus row when possible instead of attaching a new private file.

## Regression boundary

- Last known good SHA, if known:
- First known bad SHA, if known:
- Does the problem reproduce on fresh `main` with a clean worktree?

## Validation already attempted

- `pwsh -NoProfile -File scripts/verify_repo.ps1` result:
- Focused test/command result:
- Existing GitHub Actions run ID, if one already covers the same SHA/workflow/input:

Do not start duplicate workflow runs just to fill this field. Reuse the existing run ID when an equivalent run is queued, waiting, or in progress.

## Scope notes

List anything that should **not** be inferred from this report. For example, a deterministic fake-backend failure is not automatically evidence about RocketSim/physics, and an auxiliary branch failure is not canonical replay authority.
