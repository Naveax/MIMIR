# Security Policy

## Scope and authorization

MIMIR is proprietary software. This security policy does not grant permission to use, execute, compile, copy, modify, reverse engineer, benchmark, train on, probe, attack, or otherwise test MIMIR or systems associated with it.

Only report security issues you discovered through lawful activity for which you already had authorization. See `LICENSE` and `CONTRIBUTING.md` for the controlling repository terms.

## What to report

Security-relevant reports include, for example:

- exposed credentials, tokens, private keys, or other secrets;
- path traversal, unintended file access, or unsafe artifact/replay path handling;
- malformed replay, artifact, or configuration input causing a trust-boundary bypass;
- schema/version/hash validation bypasses that allow corrupted data to be accepted as trusted;
- dependency or build-chain compromise affecting repository integrity;
- GitHub Actions privilege, credential-persistence, or untrusted-input execution issues;
- unexpected code execution or privilege escalation in MIMIR tooling.

A missing feature, unsupported replay version, intentionally unavailable rollout backend, incomplete research capability, or documented fail-closed behavior is not by itself a security vulnerability.

## Reporting

Do not publish a live secret, exploit payload, private replay, credential, or sensitive proof of concept in a public issue or pull request.

Use GitHub's private vulnerability reporting / **Report a vulnerability** flow on the repository Security tab when that option is available. If private vulnerability reporting is unavailable, contact the repository owner through an existing private channel. If no private channel is available, a public issue may be used only to request a private contact path; do not include sensitive technical details in that issue.

Include enough non-sensitive information to reproduce and triage the problem:

- affected commit SHA or release/tag, if known;
- affected component or file boundary;
- expected versus observed behavior;
- minimal reproduction steps using non-sensitive data;
- impact and required preconditions;
- whether any credential or private data may have been exposed.

## Secret exposure

If a credential or secret is found in repository history, treat the secret as compromised even if the file is later deleted. The correct response is rotation/revocation plus repository cleanup where appropriate; deleting the visible file alone is not sufficient.

Do not copy exposed secret values into reports, logs, test fixtures, screenshots, continuity documents, or replacement commits.

## Security boundaries

MIMIR deliberately distinguishes deterministic scaffolding and admitted capabilities from future or unavailable functionality. Security fixes must not silently widen capability claims or convert documented fail-closed boundaries into permissive behavior.

Changes affecting replay parsing, persisted artifact validation, filesystem access, GitHub Actions permissions, dependency execution, or credential handling should remain narrow, auditable, and covered by focused negative tests where practical.

## Supported development state

MIMIR is under active development. The authoritative current production boundary is recorded in `MIMIR_CONTINUE_HERE.md` and the continuity/knowledge-graph documents it references. Historical planning documents may describe superseded behavior and must not be treated as the current security boundary without cross-checking the active continuity chain.
