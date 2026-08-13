# MIMIR Knowledge Archive — Multi-stage Validation Matrix

## Layer 1 — Current repository truth
Fresh `main` source/tests and exact-SHA evidence outrank every archived document.

## Layer 2 — Source identity
Each archive item records its original File Library filename and source class.

## Layer 3 — Exact vs snapshot
`EXACT_ARCHIVE_COPY`, `CURATED_SOURCE_SNAPSHOT`, and `REDACTED_EXTRACT` are deliberately different labels.
No snapshot may claim byte-for-byte identity.

## Layer 4 — Capability reconciliation
Historical implemented behavior is mapped to current Rust capability in
`migration/HISTORICAL_TO_CURRENT_MAPPING.md`.

## Layer 5 — Canonical synthesis
`/MIMIR_ALL_SOURCES_SUPERBOOK.md` merges current state, history and target design,
but explicitly defers to fresh source/tests.

## Layer 6 — Link graph
The verification script checks:
- every manifest path exists;
- every source registry snapshot exists;
- the superbook links to registry/validation/migration;
- `MIMIR_KNOWLEDGE_GRAPH.md` links the active `MIMIR_CONTINUE_HERE.md`, superbook, registry, validation matrix and migration map;
- raw mixed conversation exports are not copied into the public archive.

## Layer 7 — Publication
Docs/archive changes are reviewed on a dedicated branch and published force-free.
