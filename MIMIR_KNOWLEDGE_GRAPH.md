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
R3.17A evidence/decision                |
R3.17B contract decision                |
R3.17C production decision              |
R3.17D execution spec                   |
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
4. `docs/continuity/MIMIR_R3_17A_DECISION.md`
5. `docs/continuity/MIMIR_R3_17B_DECISION.md`
6. `docs/continuity/MIMIR_R3_17C_EXECUTION_SPEC.md`
7. `docs/continuity/MIMIR_R3_17C_DECISION.md`
8. `docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md`
9. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
10. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
11. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
12. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
13. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
14. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
15. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
 -> R3.14 actor envelope primitives
 -> R3.15 NewActor branch
 -> R3.16 existing-actor first-property header, hard stop payload_start_bit
 -> R3.17A primitive scalar evidence: Outcome A / 2,141,139 observations
 -> R3.17B primitive scalar contract: Outcome A
 -> R3.17C native one-scalar decoder: PUBLISHED
      production SHA c3d4c73ca34febb9f0383c59132a8bc8a363b06b
      source blob 54e1bfb918ec1bd42a61cfa0131ca27412082ac5
      11/11 focused tests
      hard stop payload_end_bit after one scalar
 -> R3.17D exact 96-witness native differential: ACTIVE
```

## Current capability lock

MIMIR may natively decode exactly one already-resolved primitive scalar payload for Boolean, Byte, Enum, Float, Int or Int64. The decoder starts at caller-supplied `payload_start_bit`, returns exact start/end/width/value metadata, and stops at that scalar's `payload_end_bit`.

It still cannot iterate a second property, next actor or next frame, mutate lifecycle state, or decode `RigidBody`, `ActiveActor`, spatial or other compound attribute families.

## R3.17C publication identity

```text
base                       85430b9eedb3bf16d66abcd895d68fbc7217818e
production SHA             c3d4c73ca34febb9f0383c59132a8bc8a363b06b
source blob                54e1bfb918ec1bd42a61cfa0131ca27412082ac5
test blob                  0293831df88723d6cf1e7fd13870bec6108d383a
focused                    11/11 PASS
disposable implementation  31795745652 / 94752360261 SUCCESS
candidate CI               31796122522 / 94753517283 SUCCESS
candidate knowledge        31796266602 / 94753955749 SUCCESS
published-main CI          31796509896 / 94754670068 SUCCESS
published-main knowledge   31796560814 / 94754827522 SUCCESS
```

## Authority rule

```text
current code/tests
> exact-SHA CI/evidence + immutable receipt streams
> MIMIR_CONTINUE_HERE.md
> docs/continuity/MIMIR_CONTINUITY_STATE.json
> docs/continuity/MIMIR_CURRENT_STATE.md
> admitted decision / active pass specs
> boundary locks
> roadmap
> historical artifacts/chat memory
```

## Verification

Run `scripts/verify_mimir_knowledge_archive.ps1`.
