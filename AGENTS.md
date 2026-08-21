<!-- naveax-ci-execution-policy:v1 -->
# Agent Execution and CI Policy

Mandatory for all agents and automations in this repository.

- Before any workflow dispatch/rerun/retry, inspect active runs and deduplicate by repository + workflow + ref + HEAD SHA + normalized inputs.
- If an equivalent run is queued, waiting, pending, requested, or in progress, do not create another run. Track/poll the existing run ID. Never rerun as a polling mechanism.
- Same SHA + workflow + inputs has an automatic dispatch budget of 1. A second execution requires a concrete runner/infrastructure/flaky-dependency reason. Prefer rerunning only failed jobs.
- Never make empty/no-op commits merely to retrigger CI. If dispatch rate rises unexpectedly, stop new dispatches and diagnose the loop.
- CI is asynchronous. Maintain RUNNING/READY/BLOCKED/DONE work states. When CI blocks one task, switch to another independent READY task instead of idling or launching duplicate CI.
- Normal scheduler target: up to 10 active independent workstreams and up to 50 queued READY work items, without duplicating work.
- Only the coordinating workstream may authorize Actions dispatches. Parallel workers report validation needs to the coordinator.
- After a failure, collect complete evidence, determine root cause, make one coherent patch, then start at most one validation run for the new commit.
- When adding/editing workflows, preserve semantics and add top-level `concurrency` when absent. For ordinary branch-scoped validation prefer workflow + ref grouping with `cancel-in-progress: false` unless replacement behavior is explicitly intended.

## Path and workstream ownership

- Before mutating a path, inspect active branches/PRs/issues for an equivalent behavioral target and overlapping files. If an active workstream already owns the same behavior or path, reuse/adopt it instead of starting a competing implementation.
- Deduplicate by **behavior**, not only branch name. Two branches that solve the same contract problem with different names are duplicates unless the coordinator explicitly records independent alternatives.
- Canonical pass ownership outranks auxiliary work. An auxiliary lane must not mutate canonical replay/continuity/source paths currently owned by an active canonical pass unless that pass explicitly hands the path off.
- Prefer atomic ownership: one candidate should own the smallest coherent file set needed for its contract. Do not casually combine unrelated hardening surfaces merely because they touch the same subsystem.
- When two independent candidates must touch the same file, keep them separate and record their ordering/reconstruction requirement rather than silently stacking one stale candidate on the other.
- A failed validation head is immutable evidence. Do not rewrite/force-move it or rerun it as polling. Fixes require a new commit/head so the failure remains attributable.
- A validation-only clean candidate is not publication authority. Close it unmerged after exact-head validation when canonical work must remain isolated, retain the branch/receipt, and reconstruct from fresh `main` before any later admission.
- Before reconstructing or publishing an old candidate, fetch fresh `main`, re-check current source/tests/continuity and overlapping active work. Do not cherry-pick stale capability claims merely because an earlier CI run was green.
- Temporary builder/evidence workflows, patch helpers, triggers and generated inspection material must not leak into a clean production/admission candidate unless their permanent inclusion is explicitly part of the contract.
- If a stronger parallel candidate appears while a weaker equivalent lane is active, freeze/supersede the weaker lane rather than racing both to publication.

Goal: bounded CI concurrency, no duplicate validation for one logical target, collision-safe parallel execution, and continuous useful progress while external jobs run.
