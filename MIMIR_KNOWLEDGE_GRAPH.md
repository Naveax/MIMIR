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
R3.17G K2 production decision           |
R3.17H K2 differential decision         |
R3.17I active K3 evidence spec           |
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
12. `docs/continuity/MIMIR_R3_17G_DECISION.md`
13. `docs/continuity/MIMIR_R3_17H_EXECUTION_SPEC.md`
14. `docs/continuity/MIMIR_R3_17H_DECISION.md`
15. `docs/continuity/MIMIR_R3_17I_EXECUTION_SPEC.md`
16. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
17. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
18. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
19. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
20. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
21. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
22. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

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
 -> R3.17G direct native K2 decoder implementation: PRODUCTION / CLOSED
      production 9bfa837c69c4751f70ca63a17c65f0f89877ff32
      implementation 31805820332 / 94784362093 SUCCESS
      candidate CI 31806206582 / 94785622371 SUCCESS
      published CI 31806554445 / 94786777798 SUCCESS
 -> R3.17H native K2 differential audit: OUTCOME A / CLOSED
      authority 9b8e8fe82ab5bdc663eecc3f5d3cd1e3b8ee38ac
      run/job 31809282874 / 94795704797 SUCCESS
      exact-head CI 31809282903 / 94795705073 SUCCESS
      artifact 9222624242 / sha256:d6c773d593c3c50957507a19056e85aef8b769fdc03fd88c6d693b1258c0af28
      469/469 exact on decode/variant/width/end/context/semantic; 7/7 negatives PASS
 -> R3.17I K3 spatial/physics wire evidence: ACTIVE
```

## Current capability lock

Production can natively decode exactly one already-resolved K1 scalar or one R3.17F-admitted K2 payload. K2 success stops exactly at its payload end bit and does not authorize another property, actor, frame or lifecycle mutation.

R3.17H closed Outcome A without widening production: all 469 immutable K2 witnesses matched exactly and all seven negative controls failed closed. PartyLeader `None`, non-Epic PartyLeader and every other unseen K2 variant remain closed.

R3.17I is evidence-only for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; native K3 decode remains closed. Property-loop continuation, next actor/frame iteration, lifecycle mutation and K4 gameplay-structured families remain closed.

## R3.17G production closure

```text
production SHA              9bfa837c69c4751f70ca63a17c65f0f89877ff32
source blob                 7288238cfb5338653552435be6af41f0dd7a4e85
focused test blob           92033a72a8a737605ac3bf91e10d130082277e04
implementation run/job      31805820332 / 94784362093 SUCCESS
clean candidate CI          31806206582 / 94785622371 SUCCESS
published main CI           31806554445 / 94786777798 SUCCESS
focused tests               8/8 PASS
mimir-replay tests          189 PASS
workspace clippy            PASS
scope                       lib.rs + r3_17g test only
Cargo/corpus/support        unchanged
```


## R3.17H differential closure

```text
authority head              9b8e8fe82ab5bdc663eecc3f5d3cd1e3b8ee38ac
authority run/job           31809282874 / 94795704797 SUCCESS
exact-head normal CI        31809282903 / 94795705073 SUCCESS
artifact                    9222624242
artifact digest             sha256:d6c773d593c3c50957507a19056e85aef8b769fdc03fd88c6d693b1258c0af28
witness selection           469/469
native decode               469/469
variant / width / end       469/469 exact
context / semantic          469/469 exact
negative controls           7/7 PASS
privacy scan                PASS
production/Cargo/corpus     0/0/0 mutations
outcome                     A
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
