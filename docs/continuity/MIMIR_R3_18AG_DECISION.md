# MIMIR R3.18AG — Bounded Post-AD True-Control Production Decision

**Date:** 2026-08-20
**Outcome:** **A — PUBLISHED / BOUNDED TRUE-ONLY CONTROL COMPOSITION**
**Production SHA:** `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`
**Production tree:** `4123820ce6537f2d4942cd0b5f72b52e43b96c1d`

## Decision

R3.18AG is published Outcome A. Production accepts one already-valid published R3.18AD ordinal-3 payload result, requires exact `868.32 / net10 / non-RL223` context, revalidates the closed R3.18AD header/payload boundary and shape allowlist, reads exactly one LSB-first `property_present` bit at `prior.stop_bit`, admits only `true`, and stops exactly one bit later. `false` fails closed.

The true-only allowlist remains evidence-bound to R3.18AF: false=0 / true=47 on the immutable 47-row lane. No next stream ID, header, payload, second later control, generalized property loop/cursor, alternate UniqueId layout, actor/frame iteration or semantic/runtime widening is admitted.

## Exact production authority

```text
production SHA/tree                 2d351e8ceb601e2fbe515d2977b2103a4b2c7976 / 4123820ce6537f2d4942cd0b5f72b52e43b96c1d
parent                              037a10a41848ca2621e1b64567c3c1bd7b2f6808
lib/test blobs                      db923ebcb419d278f4ab0144fe7ed15b298b60fa / 3f3e1c8f3f6deb7f2558862a1032f8a102131443
R3.18AG execution spec blob         90180dcaddd30ed9a187a0d4332a105d153488d7
builder authority                   32401660279 / 96531043622 SUCCESS
validation PR                       #55 closed unmerged
PR #55 exact-head CI                32402596061 / 96534073576 SUCCESS
published-main CI                   32402933798 / 96535174390 SUCCESS
continuity authority                32404006084 / 96538654038
clean production scope              lib.rs + r3_18ag_post_ad_payload_control.rs only
Cargo/lock/fixture/corpus/docs/support mutation 0/0/0/0/0/0
```

Knowledge Archive did not trigger on the production-only PR because its path filter covers continuity/archive paths rather than production Rust/test paths. Normal CI plus the builder's full Rust 1.85 validation and repository/archive verification are the applicable production gates.

## Admitted behavior

```text
input: one valid published R3.18AD result
context: exactly 868.32 / net10 / non-RL223
prior shape: ActiveActor/33 OR Int/32 OR UniqueId system1-Steam/80
require exact header payload_start == prior payload_start
require prior.stop_bit == exact payload end
read exactly one LSB-first bit at prior.stop_bit
true: return start/end/stop where end=stop=start+1
false: fail closed as unadmitted-false-control
consume zero next stream/header/payload/second-control bits
```

## Validation

Builder `32401660279/96531043622` passed the permanent R3.18AG focused suite, including the frozen R3.18AF 47-row lane, context and prior-boundary mutations, false/truncation/repeatability/post-stop-poison negatives and source-scope locks. R3.18AD/R3.18AA/R3.18W/R3.18T/K2/scalar regressions, full `mimir-replay`, workspace fmt/check/test, clippy `-D warnings`, knowledge-archive verifier and clean-scope verification all passed before the clean rewrite. PR #55 then passed exact-head CI and was closed unmerged before publication.

## Hard stop

False success semantics, the following stream/header/payload, any second later control bit, repeated/generalized property loops, generic chainable cursors, alternate UniqueId systems/layouts, next actor/frame/lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual execution and runtime/export widening remain closed.

## Next gate

R3.18AH is a separate read-only published-API differential. It must run the published R3.18AG API on exactly the immutable R3.18AF 47-row lane and require exact control start/value/end/stop equality, false=0 / true=47, mismatch 0, witness reselection 0 and adjacent stream/header/payload/second-control consumption 0/0/0/0. Only R3.18AH Outcome A may allow a later separate pass to investigate one following property header at the R3.18AG stop.
