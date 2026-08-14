# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

> **Role:** Root cross-link and verification graph for all MIMIR knowledge sources.
>
> Current source/tests and exact-SHA evidence outrank prose. `MIMIR_CONTINUE_HERE.md` remains the execution handbook.

## Canonical graph

```text
fresh GitHub source/tests + exact-SHA evidence
        |
        v
MIMIR_CONTINUE_HERE.md
        |
        +-------------------------------+
        |                               |
        v                               v
docs/continuity/                MIMIR_ALL_SOURCES_SUPERBOOK.md
CURRENT_STATE + STATE.json              |
R3.17A decision                         |
R3.17B execution spec                   |
        |                               |
        +---------------+---------------+
                        |
                        v
docs/chatgpt-archive/SOURCE_REGISTRY.md
                        |
                        v
docs/chatgpt-archive/VALIDATION_MATRIX.md
                        |
                        v
docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md
                        |
                        v
scripts/verify_mimir_knowledge_archive.ps1
```

## Mandatory reading order

1. `MIMIR_CONTINUE_HERE.md`
2. `docs/continuity/MIMIR_CONTINUITY_STATE.json`
3. `docs/continuity/MIMIR_CURRENT_STATE.md`
4. `docs/continuity/MIMIR_R3_17A_EXECUTION_SPEC.md`
5. `docs/continuity/MIMIR_R3_17A_DECISION.md`
6. `docs/continuity/MIMIR_R3_17B_EXECUTION_SPEC.md`
7. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
8. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
9. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
10. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
11. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
12. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
13. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
  -> R3.14A-E bit cursor + first actor envelope evidence/production/audit
  -> R3.15A-D NewActor evidence/contract/implementation/differential
  -> R3.16A first existing-actor property-header evidence: 47/47
  -> R3.16B production property-header reader: ADMITTED
       production SHA ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
       exact hard stop payload_start_bit
  -> R3.16C continuity/check: CLOSED / Outcome A
  -> R3.17A primitive scalar wire-format evidence: CLOSED / Outcome A
       2,141,139 scalar observations
       47 replay identities + 96 bounded witnesses frozen in immutable job log
  -> R3.17B primitive scalar wire contract: ACTIVE
```

## R3.17A observed scalar shapes

```text
Boolean   1 bit    84,545 occurrences    47 replays
Byte      8 bits   1,730,595 occurrences 47 replays
Enum      11 bits  180,624 occurrences   47 replays
Float     32 bits  33,857 occurrences    47 replays
Int       32 bits  109,920 occurrences   47 replays
Int64     64 bits  1,598 occurrences     14 replays
```

There were zero scalar shape mismatches, zero bit-monotonicity failures and zero unexpected scalar widths on the exact supported lane.

## Current capability lock

MIMIR still stops at `payload_start_bit`. R3.17A proves wire evidence; it does not add a native payload decoder.

R3.17B is contract-only. It may admit the six observed scalar wire contracts, exact LSB-first widths, value representations and atomic truncation behavior. It cannot admit spatial/compound tags or production decoding.

## R3.17A evidence identity

```text
evidence head             4cd21ea6db14c9becc11c17149af9201071859bc
run/job                    31792028292 / 94740870175 SUCCESS
artifact                   9216016802
artifact SHA256            59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
full oracle SHA256         af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1
witness SHA256             b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
aggregate SHA256           b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e
receipt stream             PASS
```

## Authority rule

```text
current code/tests
> exact-SHA CI/evidence + immutable receipt stream
> MIMIR_CONTINUE_HERE.md
> docs/continuity/MIMIR_CONTINUITY_STATE.json
> docs/continuity/MIMIR_CURRENT_STATE.md
> admitted decision / active pass specs
> boundary locks
> roadmap
> historical artifacts/chat memory
```

## Verification

Run `scripts/verify_mimir_knowledge_archive.ps1`. The root graph intentionally preserves links to `MIMIR_ALL_SOURCES_SUPERBOOK.md`, `docs/chatgpt-archive/SOURCE_REGISTRY.md`, `docs/chatgpt-archive/VALIDATION_MATRIX.md`, `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`, and the verifier itself.
