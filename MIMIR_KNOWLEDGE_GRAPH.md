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
R3.17C production decision              |
R3.17D differential decision            |
R3.17E K2 execution spec                |
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
4. `docs/continuity/MIMIR_R3_17C_DECISION.md`
5. `docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md`
6. `docs/continuity/MIMIR_R3_17D_DECISION.md`
7. `docs/continuity/MIMIR_R3_17E_EXECUTION_SPEC.md`
8. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
9. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
10. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
11. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
12. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
13. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
14. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
 -> R3.14 actor envelope primitives
 -> R3.15 NewActor branch
 -> R3.16 existing-actor first-property header
 -> R3.17A-D K1 primitive scalar wave: EVIDENCE + CONTRACT + PRODUCTION + 96/96 AUDIT CLOSED
      production SHA c3d4c73ca34febb9f0383c59132a8bc8a363b06b
      source blob 54e1bfb918ec1bd42a61cfa0131ca27412082ac5
      R3.17D authority 31798478106 / 94760722134 SUCCESS
      exact comparison f10fa74e2975e1d13c8f23c5a570409667b0c4057428439a414b47f8aaa39f73
 -> R3.17E K2 object/reference/text wire-format evidence: ACTIVE
```

## Current capability lock

MIMIR may natively decode exactly one already-resolved K1 primitive scalar payload for Boolean, Byte, Enum, Float, Int or Int64. K2 (`ActiveActor`, `String`, `QWordString`, `UniqueId`, `PartyLeader`) remains evidence-only and has no native payload permission.

Property-loop continuation, next actor/frame iteration, lifecycle mutation, K3 spatial/physics and K4 gameplay-structured families remain closed.

## R3.17D closure identity

```text
evidence head              e8f1522fb6289368bbd254d2f839091452377e9e
authority run/job          31798478106 / 94760722134 SUCCESS
normal CI                  31798478071 / 94760722233 SUCCESS
artifact                   9218372907
artifact SHA256            db049fbfd8514bb1cd661ab6b73ddf517d9786e961d764e62bc4e6137ce83e6f
identity TSV SHA256        b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
witness JSONL SHA256       b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
witness TSV SHA256         ee7f1baaa7696056172e28da2fed0848975ff1d2440113bb4d242f49d0b9da6e
comparison TSV SHA256      f10fa74e2975e1d13c8f23c5a570409667b0c4057428439a414b47f8aaa39f73
aggregate SHA256           fcc1d93ff55f3cee89211fc77a2842adca33f32f94705390610edf749df1540d
receipt file SHA256        c86e904254c6ce5a1eeeff03df9f9961ffd9169fce391d34849b54ddfccbe268
exact native match         96/96
receipt stream             PASS
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
