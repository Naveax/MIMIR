<!-- naveax-ci-execution-policy:v1 -->
# Agent Execution and CI Policy

Mandatory for all agents and automations in this repository.

- Before any workflow dispatch/rerun/retry, inspect active runs and deduplicate by repository + workflow + ref + HEAD SHA + normalized inputs.
- If an equivalent run is queued, waiting, pending, requested, or in progress, do not create another run. Track/poll the existing run ID. Never rerun as a polling mechanism.
- Same SHA + workflow + inputs has an automatic dispatch budget of 1. A second execution requires a concrete runner/infrastructure/flaky-dependency reason. Prefer rerunning only failed jobs.
- Never make empty/no-op commits merely to retrigger CI. If dispatch rate rises unexpectedly, stop new dispatches and diagnose the loop.
- CI is asynchronous. Maintain RUNNING/READY/BLOCKED/DONE work states. When CI blocks one task, switch to another independent READY task instead of idling or launching duplicate CI.
- Normal scheduler target: up to 10 active independent workstreams and up to 50 queued READY work items, without duplicating work.

## Parallel ownership and collision policy

- Before editing a path, inspect open pull requests, active branches, and known coordination ledgers for an existing owner of the same file or narrowly coupled subsystem.
- If an active workstream already owns the target path, do not create a second implementation branch for the same change. Work on an independent READY area or contribute evidence to the existing owner instead.
- Similar intent under a different branch name is still duplicate work. Deduplicate by affected paths + behavioral goal, not by branch or PR title.
- Keep clean candidates separate from validation-only material. Temporary workflows, probes, logs, synthetic fixtures, or evidence scaffolding belong on a validation child branch and must not leak into the clean candidate unless they are intentionally part of the product/test surface.
- A failed or invalid validation head is immutable evidence. Record the run ID and cause, then fix the issue in a new commit/SHA; do not rewrite history to make the failed evidence disappear and do not rerun the unchanged SHA as a substitute for a fix.
- Before any retained auxiliary candidate is admitted after `main` has moved, fetch fresh `main`, re-check path ownership, and reconstruct/rebase the narrow change on current authority. Prior CI success proves the old exact head only; it does not make a stale merge base canonical.
- When multiple candidate branches overlap, prefer the narrower or better-evidenced candidate and explicitly mark superseded variants rather than validating every variant.

- Only the coordinating workstream may authorize Actions dispatches. Parallel workers report validation needs to the coordinator.
- After a failure, collect complete evidence, determine root cause, make one coherent patch, then start at most one validation run for the new commit.
- When adding/editing workflows, preserve semantics and add top-level `concurrency` when absent. For ordinary branch-scoped validation prefer workflow + ref grouping with `cancel-in-progress: false` unless replacement behavior is explicitly intended.

Goal: bounded CI concurrency, no duplicate validation for one logical target, no parallel path collisions, and continuous useful progress while external jobs run.
