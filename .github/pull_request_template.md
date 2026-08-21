## Scope

- [ ] Canonical pass
- [ ] Non-canonical auxiliary hardening
- [ ] Validation/evidence only — **DO NOT MERGE**
- [ ] Documentation/repository hygiene only

Base authority SHA: `________________`

Head SHA: `________________`

Changed paths:

- `________________`

## Boundary check

- [ ] I inspected fresh `main` immediately before preparing this candidate.
- [ ] I checked for an existing branch/PR owning the same logical scope.
- [ ] This change does not silently widen replay, runtime, rollout, scoring, teacher, skill, export, or simulator capability claims.
- [ ] Canonical continuity/knowledge-graph files are changed only when this PR is the authoritative admitted canonical milestone.
- [ ] Temporary validation workflows/evidence files are not mixed into a clean production candidate.
- [ ] Fixtures/corpus bytes and persisted schema/version contracts are unchanged unless explicitly listed and justified below.

## Validation

Commands or workflow evidence:

```text
<exact commands, run IDs, job IDs, artifact IDs, or N/A>
```

- [ ] Validation targets the exact head SHA above.
- [ ] Before any dispatch/rerun/retry, active equivalent runs were checked per `AGENTS.md`.
- [ ] No equivalent queued/waiting/pending/requested/in-progress run was duplicated.
- [ ] No empty/no-op commit was created to retrigger CI.
- [ ] Failed validation, if any, is described below with root cause rather than hidden by reruns.

## Negative controls / fail-closed evidence

Describe the boundary that must remain rejected or unavailable, or write `N/A` for a pure documentation/hygiene change.

```text
<negative controls>
```

## Explicit non-goals

List nearby behavior this PR intentionally does **not** change.

- `________________`

## Admission / disposition

- [ ] Clean candidate: keep unmerged until separately admitted.
- [ ] Validation-only: close unmerged after evidence is recorded.
- [ ] Canonical admission: continuity + knowledge graph + next execution spec are updated only after the milestone is admitted.
