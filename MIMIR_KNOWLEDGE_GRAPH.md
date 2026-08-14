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
R3.17B decision                         |
R3.17C execution spec                   |
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
7. `docs/continuity/MIMIR_R3_17B_DECISION.md`
8. `docs/continuity/MIMIR_R3_17C_EXECUTION_SPEC.md`
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
  -> R3.17B primitive scalar wire contract: CLOSED / Outcome A
       Boolean=1, Byte=8, Enum=11, Float=32, Int=32, Int64=64 bits
       LSB-first, unaligned starts allowed, atomic truncation failure
  -> R3.17C primitive scalar native decoder: ACTIVE
```

## R3.17B admitted scalar contract

```text
Boolean   1 bit   bool
Byte      8 bits  u8
Enum      11 bits u16 numeric 0..=2047
Float     32 bits raw u32 identity + f32::from_bits interpretation
Int       32 bits signed i32 from identical two's-complement bit pattern
Int64     64 bits signed i64 from identical two's-complement bit pattern
```

All values begin exactly at `payload_start_bit`, use the existing LSB-first network cursor, require no byte alignment, consume exactly the admitted width on success, and fail without cursor advance on truncation. Unsupported/compound tags are outside the contract and must not consume payload bits.

## Current capability lock

MIMIR production still stops at `payload_start_bit`. R3.17B admits a contract only; it does not itself decode payload bits.

R3.17C may add exactly one scalar decoder for the six admitted tags. It may not continue to a second property, actor or frame, and may not decode spatial or compound attribute families.

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
