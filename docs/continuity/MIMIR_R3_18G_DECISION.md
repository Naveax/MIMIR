# MIMIR R3.18G — Bounded Second-Property Header Production Decision

**Date:** 2026-08-16
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production SHA:** `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`
**Production tree:** `b130caf211ce72577870c70d6c0d87cd006e1b29`

## Decision

R3.18G is admitted. The clean production commit adds one deliberately non-generic composition after an already-valid R3.18B first primitive property. It reuses the published R3.18D control decoder and existing property-header primitive, returns `None` immediately for a false next-property control, or returns exactly one second header for a true control and stops at that header's `payload_start`.

The composition admits only the exact R3.18F-observed second-header contexts `Int` and `String`. `String` is a resolved header tag only. No scalar/K2/K3/K4 payload decoder is invoked for the second property. No third-property access or property loop exists.

## Exact authority

```text
pre-pass main                       289c9cec0b709a27665370871dc7480b5df93270
production SHA/tree                 2b608aafae97b10ecbc884f99e4bd4a73abf7a5c / b130caf211ce72577870c70d6c0d87cd006e1b29
lib.rs blob                         5e2b9e5be9c6692e499abc97a89655c603728cef
focused test blob                   d56bf97d250b426e23fec4610cbb9ead6ec8a142
implementation run/job              31957142924 / 95189376563 SUCCESS
same-trigger normal CI              31957142895 / 95189376551 SUCCESS
exact live candidate validator      31957646865 / 95190626723 SUCCESS
published-main validator            31957892048 / 95191254798 SUCCESS
```

The publication authority is the fresh live clean branch SHA `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`. An earlier log receipt named `fc59508291c43a6f08b3667f92cd1c7b665dc3d4`; it was superseded by live branch truth and was not used for publication.

## Clean scope

Exactly two production files changed from `289c9cec0b709a27665370871dc7480b5df93270`:

1. `crates/mimir-replay/src/lib.rs` — +157 / -0
2. `crates/mimir-replay/tests/r3_18g_second_property_header.rs` — +363 / -0

Cargo manifests/lockfile, fixtures, corpus, docs, workflows and support tooling were absent from the clean production commit.

## Admitted behavior

- false next-property control -> `second_header=None`, exact one-bit control stop, no second-header lookup;
- true next-property control -> exactly one property-header primitive at the same control bit;
- exact control/header present-coordinate agreement;
- same actor-object agreement with the first property;
- exact second-header tag allowlist `Int | String`;
- exact stop `header.stop_bit == payload_start_bit`;
- zero second-payload decoder calls;
- zero property loops / third-property access.

Focused R3.18G tests, full `mimir-replay`, workspace check/test/clippy and full repository verification passed on the exact live candidate and again on the exact published main.

## Hard stop

R3.18G does **not** admit second-property payload bits or semantic values, a third property, a repeated/generalized loop, generic cursor chaining, any second-header tag context outside `Int/String`, K2/K3/K4 wrapper composition, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening, or dependency/scope expansion.

## Next gate

R3.18H is a separate read-only real-replay differential audit of the **published R3.18G production API** on the frozen R3.18F terminator/continuation lane. No second-property payload admission may occur until that evidence closes and a later pass explicitly opens a new contract.
