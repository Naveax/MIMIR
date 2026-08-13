# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

> **Role:** Root cross-link and verification graph for all MIMIR knowledge sources.
>
> This file does not replace `MIMIR_CONTINUE_HERE.md`. The continuation handbook remains the
> active execution manual. This graph connects that execution truth to the ChatGPT-storage
> provenance archive and the all-source synthesis.

## Canonical graph

```text
fresh GitHub source/tests + exact-SHA evidence
        |
        v
MIMIR_CONTINUE_HERE.md
        |
        +------------------------------+
        |                              |
        v                              v
docs/chatgpt-archive/          MIMIR_ALL_SOURCES_SUPERBOOK.md
SOURCE_REGISTRY.md                     |
        |                              |
        v                              |
archived exact/sanitized sources       |
        |                              |
        v                              |
VALIDATION_MATRIX.md <-----------------+
        |
        v
migration/HISTORICAL_TO_CURRENT_MAPPING.md
        |
        v
scripts/verify_mimir_knowledge_archive.ps1
        |
        v
.github/workflows/knowledge-archive.yml
```

## Mandatory reading order for a zero-context future chat

1. [`MIMIR_CONTINUE_HERE.md`](MIMIR_CONTINUE_HERE.md)
2. [`MIMIR_ALL_SOURCES_SUPERBOOK.md`](MIMIR_ALL_SOURCES_SUPERBOOK.md)
3. [`docs/chatgpt-archive/README.md`](docs/chatgpt-archive/README.md)
4. [`docs/chatgpt-archive/SOURCE_REGISTRY.md`](docs/chatgpt-archive/SOURCE_REGISTRY.md)
5. [`docs/chatgpt-archive/VALIDATION_MATRIX.md`](docs/chatgpt-archive/VALIDATION_MATRIX.md)
6. [`docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`](docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md)
7. Only then inspect individual archived sources relevant to the active pass.

## Authority rule

```text
current code/tests
> exact-SHA evidence
> MIMIR_CONTINUE_HERE.md current-state block
> admitted repo artifacts
> source registry / archive
> all-source superbook design synthesis
> historical sources
```

Historical code is evidence and migration material, not current capability merely because it once ran.

## Archive classes

- `EXACT_ARCHIVE_COPY`: full source content could be recovered and was copied intact.
- `CURATED_SOURCE_SNAPSHOT`: verified source metadata/facts/fragments; not a byte-exact copy.
- `REDACTED_EXTRACT`: MIMIR-only material extracted from a mixed/private container.
- `CANONICAL_SYNTHESIS`: derived multi-source document.

## Public repository privacy gate

The public archive deliberately does **not** mirror mixed ChatGPT exports or unresolved files
containing private/account identifiers wholesale. Their MIMIR-relevant facts are represented by
redacted extracts or migration notes. This is intentional, not missing archival work.

## Verification

Run:

```powershell
pwsh -NoProfile -File ./scripts/verify_mimir_knowledge_archive.ps1
```

The GitHub workflow `.github/workflows/knowledge-archive.yml` executes the same verification.
