# MIMIR R3.18Q Execution Spec — Bounded Following-Property Header Production Composition

Date: 2026-08-17  
Pass type: **production / bounded composition**

## Goal

Compose exactly one following existing-actor property header after a valid R3.18M true control, using the already-published stateless header primitive and the exact R3.18P admitted structural-context contract.

## Frozen authority

- production base: `fd74ba8c520ab83b808730572c41e45d6dc616e6` (R3.18M)
- R3.18P contract SHA-256: `0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b`
- admitted domain: exactly 18 full structural tuples / 47 observed rows
- R3.18O evidence hard stop: following `payload_start`

## Allowed production behavior

1. accept only a previously valid R3.18J second-payload result;
2. reuse the published R3.18M following-control composition and require its admitted true result;
3. decode exactly one following header starting at that control stop;
4. require exact R3.18P tuple membership including version context;
5. stop exactly at the header `payload_start`;
6. preserve atomic fail-closed behavior on any boundary/context error.

## Forbidden widening

- no tag-only/component-only/Cartesian-product support;
- no following payload decode;
- no another `property_present` control bit;
- no generic/repeatable property cursor or property loop;
- no next actor/frame/lifecycle state;
- no raw-state/event/slice/skill/runtime/export widening;
- no Boxcars production dependency.

## Required validation

- focused unit tests for all 18 admitted tuple identities plus outside-contract failures;
- exact frozen 47-row native reconstruction through `payload_start`;
- truncation before header completion fails closed;
- wrong actor context and fabricated tuple fail closed;
- post-`payload_start` poison cannot affect header result;
- existing R3.18M behavior remains unchanged;
- full fmt/test/check/clippy/repository verification on exact clean candidate SHA;
- production/Cargo/fixture/corpus/support scope audit.

## Outcome rule

- **A:** bounded one-header composition is admitted and published; next pass is a published API differential before any payload widening.
- **B:** any scope/context/boundary/regression gate fails; publish nothing.
