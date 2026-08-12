# MIMIR

MIMIR is a Rust-first scaffold for trustworthy Rocket League replay research tooling.

This repository intentionally avoids fake replay parsing, fake physics, and fake mining
logic. The current workspace provides explicit data contracts, crate boundaries, honest
stubs, deterministic test plumbing, and a small CLI surface that validates configuration
and orchestration wiring.

## Workspace goals

- Keep Rust as the core language and integration surface.
- Preserve clear extension points for replay ingestion, anchor discovery, branching,
  rollout execution, scoring, skill canonicalization, teacher synthesis, and caching.
- Make every current implementation narrow and auditable.

## Current boundaries

- No bundled Rocket League replay parser.
- No bundled RocketSim integration.
- No disguised intelligence or placeholder heuristics.
- A deterministic fake sim backend exists only for tests and CLI smoke validation.

Exported anchor and branch batches can now be validated, loaded, adapted into consumer items,
converted into deterministic candidate-request batches, and projected into deterministic
processing plans. Those plans can be converted into deterministic execution-result batches that
can be persisted, reloaded, indexed through a deterministic execution-result ledger, and later
re-opened through ledger-driven inspection so downstream history tracking can validate ledger
summaries against the authoritative batch files on disk without inventing replay, rollout,
scoring, teacher, or skill semantics. That inspected history can then flow through narrow,
deterministic selection/query helpers so downstream orchestration can pick explicit subsets
without re-implementing ledger filtering logic. Selected history entries can also be projected
into deterministic execution-result handoff bundles, downstream execution-result run requests,
and downstream execution-result job specs without re-opening files or re-scanning ledger state.
A minimal deterministic `StubExecutionResultJobExecutor` can project validated job specs into
explicit stub reports, and the crate exposes one matching convenience execute path for that stub
flow only. Execution-result job reports can also now be persisted and reloaded explicitly. No real execution behavior is
implemented. Explicit persisted execution-result job reports can now also be registered in an
explicit JSON index file, and a stub execute-persist-load-register wrapper now exists for
explicit report and index paths, and a stub execute-persist-load-register/indexed-load wrapper now
exists for those same explicit report and index paths. Explicit persisted execution-result job
reports can now also be looked up and loaded through that explicit report index.
Explicit persisted execution-result job report indexes can now also be queried deterministically after load.
Explicit persisted execution-result job reports can now be queried from the explicit index and loaded in deterministic order.
A stub execute/persist/load/register/query/load-selected wrapper now also exists for explicit report and index paths only.
Queried persisted execution-result job reports can now be summarized deterministically after
load, with those summaries available through explicit persist/load helpers, explicit summary
index persist/load/query/load-selected helpers, and the narrow report-query to
summary-persist/register/index-load bridge only. No async execution, workers, scheduling,
replay logic, or autonomous orchestration is implemented.
Loaded or queried execution-result job report collection summaries can now be aggregated
deterministically in memory, and built summaries can be persisted, registered, queried, and
reloaded explicitly through the summary index.
Default stub execution results can now also flow through explicit report indexing into persisted
summaries, queried summary loads, indexed-loaded aggregate summaries, persisted aggregate
summaries, and final in-memory aggregates through explicit summary index query/load helpers only.

## Canonical execution-result surface

- Report foundations: persist/load reports, then persist/load/query the report index and load selected reports.
- Summary foundations: persist/load summaries, then persist/load/query the summary index, load selected summaries, and aggregate queried summaries.
- Stub bridge: build and execute job specs through the canonical query/execute helpers, then use the canonical report and summary boundaries for persistence, indexing, and reloads.
- Focused canonical contract tests lock this supported surface without relying on higher-level compatibility wrappers.
- New composition should use the canonical lower-level helpers directly.
- The README migration guidance now points only to canonical report and summary lanes.
- Any remaining legacy/overlap wrappers should be treated as non-canonical and reviewed independently before removal.

## Execution-result migration map

- Publish a report: `persist_execution_result_job_report` + `register_execution_result_job_report_in_index` + `load_indexed_execution_result_job_report`.
- Load queried reports: `load_and_query_execution_result_job_reports`.
- Publish a summary: `persist_execution_result_job_report_collection_summary` + `register_execution_result_job_report_collection_summary_in_index` + `load_indexed_execution_result_job_report_collection_summary`.
- Load or aggregate queried summaries: `load_and_query_execution_result_job_report_collection_summaries` or `load_query_and_aggregate_execution_result_job_report_collection_summaries`.
- Stub bridge: `query_stub_execute_persist_load_and_register_execution_result_job_report`, then `load_indexed_execution_result_job_report` when an indexed reload is required, and `query_stub_execute_register_report_and_index_load_summary`.
- Canonical aggregate-then-publish lane: `query_stub_execute_register_report_and_index_load_summary` + `load_query_and_aggregate_execution_result_job_report_collection_summaries` + `persist_register_and_index_load_execution_result_job_report_collection_summary`.

## Quick validation

From PowerShell:

```powershell
.\scripts\fmt.ps1
.\scripts\check.ps1
.\scripts\test.ps1
.\scripts\clippy.ps1
.\scripts\smoke.ps1
```
