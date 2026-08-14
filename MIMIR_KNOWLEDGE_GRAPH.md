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
R3.17E K2 evidence decision             |
R3.17F K2 contract decision             |
R3.17G active implementation spec       |
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
8. `docs/continuity/MIMIR_R3_17E_DECISION.md`
9. `docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md`
10. `docs/continuity/MIMIR_R3_17F_DECISION.md`
11. `docs/continuity/MIMIR_R3_17G_EXECUTION_SPEC.md`
12. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
13. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
14. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
15. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
16. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
17. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
18. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
 -> R3.14 actor envelope primitives
 -> R3.15 NewActor branch
 -> R3.16 existing-actor first-property header
 -> R3.17A-D K1 primitive scalar wave: CLOSED
      production c3d4c73ca34febb9f0383c59132a8bc8a363b06b
      R3.17D 31798478106 / 94760722134 SUCCESS / 96/96 exact
 -> R3.17E K2 object/reference/text evidence: OUTCOME A / CLOSED
      evidence 19db534a3668f84f1c5ce36ef1252c52841d890f
      authority 31801482588 / 94770260529 SUCCESS
      artifact 9219554878 / sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
      47/47 / 110539 K2 occurrences / 0 structural failures
 -> R3.17F evidence-supported K2 contract admission: OUTCOME A / CLOSED
 -> R3.17G direct native K2 decoder implementation: ACTIVE
```

## Current capability lock

Production remains exactly at R3.17C: one already-resolved K1 primitive scalar payload may be decoded natively. R3.17E admitted K2 evidence, not native K2 production capability.

R3.17F admitted atomic contracts only for evidence-supported K2 shapes. R3.17G may implement exactly one already-resolved K2 payload under those contracts; native K2 capability is not claimed until production publication succeeds. PartyLeader `None`, non-Epic PartyLeader and other unseen K2 variants remain closed.

Property-loop continuation, next actor/frame iteration, lifecycle mutation, K3 spatial/physics and K4 gameplay-structured families remain closed.

## R3.17E closure identity

```text
evidence head              19db534a3668f84f1c5ce36ef1252c52841d890f
authority run/job          31801482588 / 94770260529 SUCCESS
normal CI                  31801482499 / 94770260054 SUCCESS
artifact                   9219554878
artifact digest            sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
aggregate SHA256           335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751
summary SHA256             9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e
oracle JSONL SHA256        196f4e4d2a588137ad12372cb2f0af79d7fca422c0bc2c5dea95506fa72cac4d
witness JSONL SHA256       7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
receipt manifest SHA256    400aa0b52a5e120b7791e34e9a364d4e40a2362c46d6770dad3c5292db8dc7cc
47/47 oracle decode        PASS
K2 occurrences             110539
shape/unclassified         0
bit monotonicity failures  0
raw-payload shape failures 0
privacy-safe output        PASS
production/Cargo/corpus    0/0/0 mutations
outcome                    A
```

## R3.17F contract closure

```text
outcome                    A / contract complete
production Rust            unchanged at c3d4c73ca34febb9f0383c59132a8bc8a363b06b
contract base              b4b4449a99dabbb97120d5393c3d5b1462b6f81e
ActiveActor                33-bit exact reference contract
String                     Empty / Windows1252 / UTF16 atomic contract
QWordString                legacy QWord64 / RL223 positive Windows1252
UniqueId                   Steam / PlayStation / PsyNet / Epic(declared=33), net10
PartyLeader                Some(Epic declared=33) only, net10 + RL223 true
atomic failure             0-bit consumption from payload start
privacy-safe G vectors     synthetic only
next pass                  R3.17G production implementation
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
