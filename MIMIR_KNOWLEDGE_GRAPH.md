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
R3.16B decision                         |
R3.16C continuity decision              |
R3.17A execution spec                   |
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
4. `docs/continuity/MIMIR_R3_16B_DECISION.md`
5. `docs/continuity/MIMIR_R3_16C_EXECUTION_SPEC.md`
6. `docs/continuity/MIMIR_R3_16C_DECISION.md`
7. `docs/continuity/MIMIR_R3_17A_EXECUTION_SPEC.md`
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
  -> R3.14A-E bit cursor + first actor envelope evidence/production/audit
  -> R3.15A-D NewActor evidence/contract/implementation/differential
  -> R3.16A first existing-actor property-header evidence: 47/47
  -> R3.16B production property-header reader: ADMITTED
       production SHA ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
       exact hard stop payload_start_bit
  -> R3.16C continuity/check: CLOSED / Outcome A
  -> R3.17A primitive scalar attribute wire-format evidence: ACTIVE
```

## Current capability lock

MIMIR can resolve one existing-actor property header through `stream_id`, property lookup and tag identity, then stops at `payload_start_bit`.

It still **cannot natively decode any attribute payload**. Oracle visibility into `RigidBody`, `ActiveActor`, `Byte`, `Float`, `Int`, or any other tag is not production capability.

R3.17A is evidence-only for the primitive scalar family (`Boolean`, `Byte`, `Int`, `Int64`, `Float`, `Enum`). Zero-observation tags remain closed.

## R3.16B closure identity

```text
base main                 fc020729396ad9f62ee4b8fd8fe6808f5bdb5489
production SHA            ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
source blob               625ab2322e35f5f835871d42b9efeb04f5c299ab
source SHA256             186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28
focused tests             8/8 PASS
native differential       47/47 PASS
post-main CI              31788526050 / 94729854512 SUCCESS
post-main knowledge       31788566184 / 94729983908 SUCCESS
```

## Authority rule

```text
current code/tests
> exact-SHA CI/evidence
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
