# Full Replay Corpus

The production-scale replay corpus is intentionally not stored in Git.

Local audit snapshot (2026-08-12):

- corpus directory: `RLCS_REPLAYS_1V1`
- replay count: 212,339
- approximate size: 148.14 GB

The checked-in replay corpus is only a small deterministic regression/stress set.

Future production ingestion should receive the full-corpus location through an explicit configuration/CLI/environment contract once that contract is implemented. Do not hard-code one developer machine path into core MIMIR logic.

Generated parse caches, training exports, checkpoints, and large derived datasets should remain outside ordinary Git history.