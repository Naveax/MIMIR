# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

> **Role:** Root cross-link and verification graph for all MIMIR knowledge sources.
>
> This file does not replace `MIMIR_CONTINUE_HERE.md`. The continuation handbook remains the
> active execution manual. This graph connects that execution truth to current pass decisions,
> exact evidence, the ChatGPT-storage provenance archive, and the all-source synthesis.

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
docs/continuity/               MIMIR_ALL_SOURCES_SUPERBOOK.md
CURRENT STATE + PASS SPECS              |
        |                              |
        v                              |
R3.14A/B/C admission chain             |
        |                              |
        +--------------+---------------+
                       |
                       v
docs/chatgpt-archive/SOURCE_REGISTRY.md
                       |
                       v
archived exact/sanitized sources
                       |
                       v
VALIDATION_MATRIX.md
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

### A. Current execution truth first

1. [`MIMIR_CONTINUE_HERE.md`](MIMIR_CONTINUE_HERE.md)
2. [`docs/continuity/MIMIR_CONTINUITY_STATE.json`](docs/continuity/MIMIR_CONTINUITY_STATE.json)
3. [`docs/continuity/MIMIR_CURRENT_STATE.md`](docs/continuity/MIMIR_CURRENT_STATE.md)
4. [`docs/continuity/MIMIR_R3_14A_DECISION.md`](docs/continuity/MIMIR_R3_14A_DECISION.md)
5. [`docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md`](docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md)
6. [`docs/continuity/MIMIR_R3_14C_EXECUTION_SPEC.md`](docs/continuity/MIMIR_R3_14C_EXECUTION_SPEC.md)
7. [`docs/continuity/MIMIR_PASS_PROTOCOL.md`](docs/continuity/MIMIR_PASS_PROTOCOL.md)
8. [`docs/continuity/MIMIR_BOUNDARY_LOCKS.md`](docs/continuity/MIMIR_BOUNDARY_LOCKS.md)
9. [`docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`](docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md)
10. [`docs/continuity/MIMIR_PROGRESS_LEDGER.md`](docs/continuity/MIMIR_PROGRESS_LEDGER.md)

### B. Multi-source reconstruction second

11. [`MIMIR_ALL_SOURCES_SUPERBOOK.md`](MIMIR_ALL_SOURCES_SUPERBOOK.md)
12. [`docs/chatgpt-archive/README.md`](docs/chatgpt-archive/README.md)
13. [`docs/chatgpt-archive/SOURCE_REGISTRY.md`](docs/chatgpt-archive/SOURCE_REGISTRY.md)
14. [`docs/chatgpt-archive/VALIDATION_MATRIX.md`](docs/chatgpt-archive/VALIDATION_MATRIX.md)
15. [`docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`](docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md)
16. Only then inspect individual archived sources relevant to the active pass.

## Current replay-decoder admission chain

```text
R3.13 — PRODUCTION
static replay network lookup plan
ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
        |
        v
R3.14 — COMPLETE READ-ONLY AUDIT
network bitstream order + bounded-int warning
        |
        v
R3.14A — COMPLETE / OUTCOME A
47/47 pinned Boxcars first-frame + first-actor envelope evidence
Decision: docs/continuity/MIMIR_R3_14A_DECISION.md
Evidence head: f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
        |
        v
R3.14B — COMPLETE / ADMITTED CONTRACT
private LSB-first cursor + canonical bounded-u32 contract
Spec: docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md
        |
        v
R3.14C — ACTIVE
native private bit cursor + bounded integer primitive implementation
Spec: docs/continuity/MIMIR_R3_14C_EXECUTION_SPEC.md
        |
        v
R3.14D — CLOSED UNTIL R3.14C ADMISSION
first actor-envelope production reader
```

Important capability distinction:

```text
R3.14A oracle evidence
!= native MIMIR actor-envelope parser

R3.14B implementation contract
!= production primitive

R3.14C primitive implementation when completed
!= actor-envelope production reader
```

The production replay capability remains R3.13 until a later production pass is implemented, audited, published, and continuity-synced.

## R3.14A evidence identity

```text
production code SHA       ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
evidence head             f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
oracle                    nickbabcock/boxcars
oracle SHA                c70e77df7af81b436cb545d070bb90c82f562d0b
supported lane            47 / 47
selector manifest SHA256  28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55
artifact ZIP SHA256       d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b
production mutation       0
```

Observed common first-envelope boundary across the current supported lane:

```text
network bit 0       frame start
bit 64              after f32 time + f32 delta
bit 64              actor_present
bit 65..76          bounded actor_id
bit 76              alive
bit 77              new
bit 78              R3.14A hard stop
```

## Authority rule

```text
current code/tests
> exact-SHA evidence
> MIMIR_CONTINUE_HERE.md current override
> structured continuity state
> admitted decision / active pass specs
> boundary locks
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

After any admitted replay-decoder milestone, update this graph together with the continuity control plane. A milestone is not fully closed while the graph still points to the previous active pass.
