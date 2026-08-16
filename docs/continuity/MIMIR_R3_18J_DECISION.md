# MIMIR R3.18J — Bounded Second-Property Payload Production Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / PRODUCTION PUBLISHED**
**Production SHA:** `330ab01890a7c09eff1805e437584fb3be0a1134`
**Production tree:** `5540b6a86e53d243dabbabea223a5afa8657521c`

## Decision

R3.18J is admitted. Production now composes at most one second-property payload after the already-bounded R3.18G second header. A terminator still returns immediately with no second header/payload. A continuation decodes exactly one second payload and stops at its exact payload end.

The admitted surface is deliberately narrow: `Int` reuses `decode_replay_network_primitive_scalar_v1`; `String` reuses `decode_replay_network_k2_v1` and is additionally restricted by the R3.18J composition to the exact R3.18I-observed context `net_version=10`, `is_rl_223=false`. The following `property_present` bit is not read.

## Exact authority

```text
pre-pass main                       9fc863114b22b72ec56a606075f7a8e87fa6fd5c
production SHA/tree                 330ab01890a7c09eff1805e437584fb3be0a1134 / 5540b6a86e53d243dabbabea223a5afa8657521c
lib.rs blob                         ee9b0c71871df7ff52275581eb7ad4c023b8ba79
focused test blob                   c5a97c5a17ae2ea292790a020673dd26a0150024
implementation run/job              31975731621 / 95234808797 SUCCESS
clean candidate CI                  31975907582 / 95235253244 SUCCESS
published-main CI                   31976100231 / 95235742210 SUCCESS
R3.18I evidence head                45090a2c18fb517088bb411782bbaed0d7d68199
R3.18I artifact                     9270842140
R3.18I artifact digest              sha256:9890ed33780412a8900692a627b212d80428a08229f9f691d914c8def31e06e2
```

## Clean scope

Exactly two production files changed from `9fc863114b22b72ec56a606075f7a8e87fa6fd5c`:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_18j_second_property_payload.rs`

No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file entered the clean production commit.

## Admitted behavior

- terminator: `second_payload=None`, exact R3.18G control end, no post-control lookup/payload decode;
- continuation `Int`: exact 32-bit primitive scalar value/end;
- continuation `String`: exact existing K2 String decoder, additionally gated to net10 / non-RL223;
- result retains the R3.18G header composition plus optional typed second payload and exact stop bit;
- stop equals exactly the one second payload end;
- bits after payload end do not affect the result;
- truncation and malformed/wrong-context String fail closed;
- no third-control access and no property loop.

## Hard stop

R3.18J does not admit the following `property_present` bit, a third header/payload, repeated/generalized property iteration, generic chainable cursor behavior, second tags outside exact `Int|String`, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening or dependency/corpus/support expansion.

## Next exact pass

`R3.18K — published second-property payload real-replay differential audit` over the immutable R3.18I 94-row lane. Only a clean Outcome A may open evidence for the control bit after the second payload.
