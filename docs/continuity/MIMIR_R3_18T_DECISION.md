# MIMIR R3.18T — Bounded Following-Property Payload Production Decision

**Date:** 2026-08-17
**Outcome:** **A — PUBLISHED / BOUNDED PRODUCTION COMPOSITION**
**Production SHA:** `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b`
**Production tree:** `a6f27fe606cd3446da02ef1cb8cf53fff071e383`

## Decision

R3.18T is published Outcome A. Production now composes exactly one R3.18S-admitted following payload after the already-published R3.18Q following-property header. Exact R3.18P seven-field context membership remains enforced by R3.18Q. The composition is deliberately closed to `Boolean | ActiveActor`, reuses the existing lower-level decoders, and stops exactly at the one payload end.

No another `property_present` bit is read. No generic property loop/cursor, context widening, next actor/frame or later semantic/runtime layer is admitted.

## Exact production authority

```text
production SHA/tree                 c2765ab9f04f9c981a6868cb6503bdf0e339ce1b / a6f27fe606cd3446da02ef1cb8cf53fff071e383
parent                              ac1b284099a01be895c3e9d644a9d98b6dfe3da2
lib/test blobs                      cf992670b461e9d923e773ed375bef2b42aea20d / 430676ec118fa0755a9c64abc0067bf5c5c88d05
implementation authority            32049639448 / 95445637593 SUCCESS
clean-candidate CI                  32049893219 / 95446478223 SUCCESS
PR #23 exact-head CI                32050205389 / 95447503058 SUCCESS
published-main CI                   32050650336 / 95448937493 SUCCESS
continuity authority                32051158916 / 95450585726
clean production scope              lib.rs + r3_18t_following_payload.rs only
Cargo/lock/fixture/corpus/docs/support mutation 0/0/0/0/0/0
```

Knowledge Archive did not trigger on the R3.18T production-only diff because its workflow path filter does not include production Rust/test paths. This is expected and is not represented as a missing production check; normal CI and repository verification are the applicable production gates.

## Admitted behavior

```text
valid R3.18Q following header
-> exact R3.18P context already enforced
-> resolved tag must be Boolean or ActiveActor
-> start exactly at following_header.payload_start_bit
-> Boolean: decode with primitive scalar, exact width 1 bit
-> ActiveActor: decode with K2, exact width 33 bits = active:1 + actor:32
-> preserve typed lower-decoder result
-> stop exactly at payload end
-> consume zero another-control bits
```

The result carries the bounded R3.18Q header composition, exactly one typed following payload, and the exact payload-end `stop_bit`.

## Focused validation

The permanent R3.18T focused test covers:

- real Boolean witness and exact lower-decoder identity;
- real ActiveActor witness and exact lower-decoder identity (`active=false`, actor `342` on the selected frozen corpus witness);
- Boolean and ActiveActor truncation rejection;
- wrong exact replay context rejection;
- fabricated R3.18P tuple rejection;
- deterministic repeatability;
- poisoning bits starting at the payload end without changing the result, proving the composition does not read a later property control.

Focused R3.18T, full `mimir-replay`, workspace check/test/clippy and repository verification all passed under the implementation authority before the clean candidate was published.

## Hard stop

Another property-control bit, another property header/payload, repeated/generalized property loops or generic cursors, following payload tags outside exact admitted `Boolean | ActiveActor`, R3.18P context widening, next actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual runtime and export widening remain closed.

## Next gate

R3.18U is a separate read-only published-API real-replay differential. It must run the published R3.18T API on the exact immutable R3.18S 47-row lane and compare header, payload boundary, typed semantics and final stop to the frozen R3.18S authority. Only after that published differential is admitted may a later pass investigate another property-control boundary.
