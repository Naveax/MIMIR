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
R3.14A/B/C/D admission chain            |
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
6. [`docs/continuity/MIMIR_R3_14C_DECISION.md`](docs/continuity/MIMIR_R3_14C_DECISION.md)
7. [`docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md`](docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md)
8. [`docs/continuity/MIMIR_PASS_PROTOCOL.md`](docs/continuity/MIMIR_PASS_PROTOCOL.md)
9. [`docs/continuity/MIMIR_BOUNDARY_LOCKS.md`](docs/continuity/MIMIR_BOUNDARY_LOCKS.md)
10. [`docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`](docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md)
11. [`docs/continuity/MIMIR_PROGRESS_LEDGER.md`](docs/continuity/MIMIR_PROGRESS_LEDGER.md)

### B. Multi-source reconstruction second

12. [`MIMIR_ALL_SOURCES_SUPERBOOK.md`](MIMIR_ALL_SOURCES_SUPERBOOK.md)
13. [`docs/chatgpt-archive/README.md`](docs/chatgpt-archive/README.md)
14. [`docs/chatgpt-archive/SOURCE_REGISTRY.md`](docs/chatgpt-archive/SOURCE_REGISTRY.md)
15. [`docs/chatgpt-archive/VALIDATION_MATRIX.md`](docs/chatgpt-archive/VALIDATION_MATRIX.md)
16. [`docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`](docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md)
17. Only then inspect individual archived sources relevant to the active pass.

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
R3.14C — PRODUCTION / ADMITTED
private native bit cursor + bounded integer primitive
Production SHA: bad2db9d5043a7a0087a4fab1d278df5f36c7717
Decision: docs/continuity/MIMIR_R3_14C_DECISION.md
        |
        v
R3.14D — ACTIVE
first actor-envelope production reader through new, then STOP
Spec: docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md
        |
        v
R3.14E — CLOSED UNTIL R3.14D ADMISSION
47-replay native-vs-Boxcars first-envelope differential audit
```

Important capability distinction:

```text
R3.14A oracle evidence
!= native MIMIR actor-envelope parser

R3.14B implementation contract
!= production primitive

R3.14C production primitive
!= actor-envelope production reader

R3.14D reader when implemented
!= 47-replay differential admission; that is R3.14E
```

## R3.14C production identity

```text
pre-pass main             c42836647673cecc47cc9c89908da1de11d8a222
production SHA            bad2db9d5043a7a0087a4fab1d278df5f36c7717
source file               crates/mimir-replay/src/lib.rs
source Git blob           3ff6c7823f45126595e7e59f7b5fb50980d8234c
source SHA256             ac1c2ae2919ad0c5d6d8ea615dd5dac82f4c5e5240f33618ef5e74ef9cb1cb92
focused tests             19
oracle actor-ID vectors   47 / 47 value + end-bit match
clean branch CI           31698938025 SUCCESS
published-main CI         31699241010 SUCCESS
```

The only replay capability opened by R3.14C is the private/internal LSB-first bit cursor and canonical bounded-u32 primitive. Actor-envelope result parsing remains R3.14D work.

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

## Repository reproducibility gate discovered during R3.14C

Before R3.14C publication, a pre-existing stale `Cargo.lock` was repaired separately at:

```text
c42836647673cecc47cc9c89908da1de11d8a222
```

The permanent repository verifier now uses Cargo `--locked`. This is build/reproducibility maintenance, not replay capability expansion.

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

The GitHub workflow `.github/workflows/knowledge-archive.yml` executes the same verification and is configured to trigger for continuity and knowledge-graph changes.

After any admitted replay-decoder milestone, update this graph together with the continuity control plane. A milestone is not fully closed while the graph still points to the previous active pass.


---

## LATEST CANONICAL OVERRIDE — R3.14D PRODUCTION / R3.14E ACTIVE

```text
R3.14C primitives — production
        |
        v
R3.14D first actor envelope reader — PRODUCTION 7b17cb9033b6c71d476e500380d78402cbb3c56d
        |
        v
R3.14E 47-replay native-vs-Boxcars differential audit — ACTIVE / evidence-only
        |
        v
R3.15A NewActor evidence — CLOSED until R3.14E Outcome A
```

Latest mandatory reading order:
1. `MIMIR_CONTINUE_HERE.md`
2. `docs/continuity/MIMIR_CONTINUITY_STATE.json`
3. `docs/continuity/MIMIR_CURRENT_STATE.md`
4. `docs/continuity/MIMIR_R3_14D_DECISION.md`
5. `docs/continuity/MIMIR_R3_14E_EXECUTION_SPEC.md`
6. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
7. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
8. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
9. `docs/continuity/MIMIR_PROGRESS_LEDGER.md`
10. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
11. `docs/chatgpt-archive/README.md`
12. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
13. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
14. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

Current code/tests and exact-SHA evidence still outrank every document.
---

## LATEST CANONICAL OVERRIDE — R3.14E ADMITTED / R3.15A ACTIVE

```text
R3.14D native first actor envelope — PRODUCTION 7b17cb9033b6c71d476e500380d78402cbb3c56d
        |
        v
R3.14E exact 47-replay differential — COMPLETE / OUTCOME A
        |
        v
R3.15A NewActor branch read-only evidence — ACTIVE
        |
        v
R3.15B NewActor contract — CLOSED until R3.15A admission
```

Latest mandatory reading order begins with `MIMIR_CONTINUE_HERE.md`, structured/current continuity state, `MIMIR_R3_14E_DECISION.md`, and `MIMIR_R3_15A_EXECUTION_SPEC.md`, then pass protocol/boundary locks/roadmap/ledger before the superbook and archive registry/matrix/mapping documents.
---

## LATEST CANONICAL OVERRIDE — R3.15A COMPLETE / R3.15B CURRENT

R3.15A completed with Outcome A. Exact evidence is recorded in `docs/continuity/MIMIR_R3_15A_DECISION.md`. The current canonical pass is the docs-only contract pass `R3.15B`, defined by `docs/continuity/MIMIR_R3_15B_EXECUTION_SPEC.md`.
---

## LATEST CANONICAL OVERRIDE — R3.15B ADMITTED / R3.15C ACTIVE

```text
R3.15A NewActor evidence — COMPLETE / OUTCOME A
        |
        v
R3.15B NewActor native contract — ADMITTED / CONTRACT COMPLETE
        |
        v
R3.15C first NewActor native reader — ACTIVE / PRODUCTION IMPLEMENTATION
        |
        v
R3.15D full-lane NewActor differential — CLOSED until R3.15C publication
```

Latest mandatory reading order begins with `MIMIR_CONTINUE_HERE.md`, structured/current continuity state, `MIMIR_R3_15B_DECISION.md`, `MIMIR_R3_15C_EXECUTION_SPEC.md`, then pass protocol, boundary locks, roadmap and ledger before the superbook/archive sources.

---

## LATEST CANONICAL OVERRIDE — R3.15C PRODUCTION / R3.15D ACTIVE

```text
R3.15A NewActor evidence — COMPLETE / OUTCOME A
        |
        v
R3.15B NewActor contract — ADMITTED
        |
        v
R3.15C first NewActor native reader — PRODUCTION bf4bccff82203ed049d33e942681fed07f23beb4
        |
        v
R3.15D 47-replay first-NewActor native-vs-pinned-Boxcars differential — ACTIVE / EVIDENCE ONLY
```

Latest mandatory reading order begins with `MIMIR_CONTINUE_HERE.md`, structured/current continuity state, `MIMIR_R3_15C_DECISION.md`, `MIMIR_R3_15D_EXECUTION_SPEC.md`, then pass protocol, boundary locks, roadmap and ledger before the superbook/archive registry/matrix/mapping sources. Current source/tests and exact-SHA evidence remain authoritative.
