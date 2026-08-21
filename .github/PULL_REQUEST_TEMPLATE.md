<!--
Maintainer / automation workflow only.
MIMIR is proprietary and external contributions are not accepted for incorporation.
See CONTRIBUTING.md and LICENSE.
-->

## Scope

- Base `main` SHA:
- Head SHA:
- Lane: canonical / non-canonical auxiliary / governance
- Exact files or directories owned by this PR:
- Explicit non-goals:

## Parallel-work safety

- [ ] Fresh `main` was checked before the candidate was built.
- [ ] Existing open branches/PRs were checked for overlapping ownership.
- [ ] This PR does not skip or overtake an earlier canonical pass.
- [ ] Changes from unrelated parallel lanes are not bundled into this candidate.

## Capability truth

- [ ] No unsupported or unproven capability is presented as production-ready.
- [ ] Fail-closed / scaffold / deterministic-fake boundaries remain explicit where applicable.
- [ ] Persisted schema, runtime, replay, export, or CLI semantics are unchanged unless this PR explicitly owns and proves that change.

## Repository hygiene

- [ ] No credentials, secrets, private keys, private replay data, transient logs, build output, caches, models, or checkpoints are included.
- [ ] Generated evidence is committed only when the repository contract explicitly admits it.
- [ ] The diff contains no accidental formatting, unrelated documentation, or drive-by refactors.

## Validation

- Existing equivalent queued / waiting / in-progress run checked before triggering CI: yes / no / n/a
- Authoritative CI run ID:
- Exact candidate SHA validated:

- [ ] `cargo fmt --all -- --check`
- [ ] `cargo check --locked --workspace --all-targets --all-features`
- [ ] relevant focused tests
- [ ] `cargo test --locked --workspace --all-targets --all-features`
- [ ] `cargo clippy --locked --workspace --all-targets --all-features -- -D warnings`
- [ ] repository-specific replay/corpus verification when applicable

Do not rerun or redispatch CI merely to poll status. Track the existing run ID. While CI is active, independent non-conflicting work may continue.

## Admission / handoff

- [ ] `main` freshness was rechecked after validation.
- [ ] If `main` moved, ancestry/mergeability was re-evaluated and revalidation was performed when required.
- [ ] Canonical continuity / knowledge graph files are updated only for an admitted canonical milestone.
- [ ] Auxiliary or validation-only PRs are clearly marked and are not merged while their owning canonical boundary is active.
