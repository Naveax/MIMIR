# MIMIR R3.18W — Bounded After-Following-Payload Control Production Decision

**Date:** 2026-08-17
**Outcome:** **A — PUBLISHED / BOUNDED TRUE-ONLY CONTROL COMPOSITION**
**Production SHA:** `58872e94f00ef094807f21ab2ff984ac66b97d91`
**Production tree:** `d6965d77903ea99dad0465bb350b6a673ee7dd00`

## Decision

R3.18W is published Outcome A. Production now accepts one already-valid R3.18T following-payload result, validates the exact nested header/payload-end relationship, reads exactly one LSB-first `property_present` bit at `prior.stop_bit`, admits only `true`, and stops exactly one bit later.

The true-only allowlist is evidence-bound: R3.18V observed `true=47 / false=0` on the immutable lane. `false` therefore fails closed. No next stream ID, header, payload, second later control bit, generic property cursor/loop, actor/frame iteration or wider semantic/runtime behavior is admitted.

## Exact production authority

```text
production SHA/tree                 58872e94f00ef094807f21ab2ff984ac66b97d91 / d6965d77903ea99dad0465bb350b6a673ee7dd00
parent                              49011a8be77e59b1834c0ecbb648ee6d699ca6c8
lib/test blobs                      d997ae8c3ad2d201b3f43c6ccca7ded2ef03b73b / ac176135c2e6ed56f0b91bdde8c7548f17641cf0
R3.18W execution spec blob          4252804b2b1edb22a6e729e953681844a25d9ef9
implementation authority            32060501395 / 95480474127 SUCCESS
clean-candidate CI                  32062120856 / 95485540552 SUCCESS
PR #27 exact-head CI                32062533181 / 95486877308 SUCCESS
published-main CI                   32062965119 / 95488256583 SUCCESS
continuity authority                32063782318 / 95490862312
clean production scope              lib.rs + r3_18w_following_payload_control.rs only
Cargo/lock/fixture/corpus/docs/support mutation 0/0/0/0/0/0
```

Knowledge Archive did not trigger on the R3.18W production-only diff because its path filter does not include production Rust/test paths. Normal CI and repository verification are the applicable production gates for that commit.

## Admitted behavior

```text
input: one valid R3.18T following-payload result
-> require following header property_present=true
-> require following header payload_start == composed header stop
-> Boolean prior: tag Boolean / exact width 1 / exact payload end+stop
-> ActiveActor prior: tag ActiveActor / exact width 33 / exact payload end
-> require prior.stop_bit == exact following-payload end
-> read exactly one LSB-first bit at prior.stop_bit
-> true: return start/end/stop where end=stop=start+1
-> false: fail closed as unadmitted-false-control
-> consume zero next stream/header/payload/second-control bits
```

## Focused validation

The permanent focused R3.18W test covers real Boolean and ActiveActor boundaries, true-control start/end/stop, byte-aligned and unaligned starts, repeatability, post-control poison, false-control rejection, missing control bit, prior-stop corruption, malformed prior header/payload relationships and source-scope locks. Focused R3.18W, full `mimir-replay`, workspace check/test/clippy and repository verification passed under the implementation authority before clean publication.

## Hard stop

False success semantics, the following stream/header/payload, any second later control bit, repeated/generalized property loops, generic chainable cursors, next actor/frame/lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual execution and runtime/export widening remain closed.

## Next gate

R3.18X is a separate read-only published-API differential. It must run the published R3.18W API on exactly the immutable R3.18V 47-row lane and require exact control start/value/end/stop equality with the frozen one-bit evidence. Only after R3.18X Outcome A may a later separate pass investigate the next property header at the R3.18W stop.
