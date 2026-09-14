# MIMIR R3.18BY — Bounded Post-BU Mixed-Continuation Following-Header Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** R3.18BU `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`
**Contract authority:** R3.18BX Outcome A / `docs/continuity/MIMIR_R3_18BX_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `37cd43677a3523811ebd24179a5e2aec4699fa11457e078ec6e20f8998cc2576`
**Following payload decode:** forbidden
**Second later property-control bit:** forbidden
**Generalized/repeated property loop:** forbidden

## Goal

Publish the minimum boundary-specific composition after one valid published R3.18BU mixed control.

- For the validated BU=false row, return a successful terminator/no-header result with zero post-BU reads.
- For the validated BU=true row, decode exactly one following existing-actor property-header suffix, require exact R3.18BX eight-field membership, expose the header identity, and stop exactly at `payload_start`.
- Do not consume the following payload or any later control bit.

## Frozen lane

```text
published BU rows                     2
false terminator                      sample_002 / [11239,11240) / stop 11240
true continuation                     largest_100/079... / [3238,3239) / stop 3239
expected following stream             start 3239 / end 3245 / id 61 / bound 110
expected property                     object 67 / TAGame.PRI_TA:ClientLoadoutsOnline
expected attribute tag                LoadoutsOnline
expected property ordinal             8
expected payload_start                3245
admitted context                      (110,6,67,LoadoutsOnline,868,32,10,false)
following payload bits                0
second later control bits             0
```

## Production contract

The new boundary-specific API must:

1. validate/recompute the supplied R3.18BU authority rather than trusting caller coordinates;
2. require exact equality of BU control value/start/end/stop with the recomputed prior;
3. branch on validated `property_control` without re-reading that control bit;
4. on false, return a no-header terminator at BU stop with zero stream/header/payload/later-control reads;
5. on true, invoke `decode_replay_network_existing_actor_property_header_suffix_v1` exactly once starting at validated BU stop;
6. retain the complete eight-field R3.18BX context including `is_rl_223`;
7. require exact R3.18BX tuple membership with no historical-contract inheritance;
8. expose exact property-present/control alignment, stream coordinates, property object/tag identity and payload start;
9. stop exactly at `payload_start=3245` on the immutable true witness;
10. consume zero following-payload bits and zero second-later-control bits;
11. expose no generic repeatedly-chainable cursor or loop.

The suffix primitive is preferred because it does not re-read the already validated BU control bit.

## Expected result shape

A boundary-specific result should contain, at minimum:

- the validated/recomputed R3.18BU result;
- the exact K3 context;
- `following_header: Option<ReplayNetworkExistingActorFirstPropertyHeaderV1>`;
- `stop_bit`.

False path: `following_header=None`, `stop_bit=bu.stop_bit`.

True path: `following_header=Some(...)`, `stop_bit=header.payload_start_bit`.

## Required focused tests

At minimum prove:

- exact immutable two-row lane: false=1, true=1;
- false path succeeds 1/1 with no header lookup and no post-BU bit read;
- true path succeeds 1/1 and exact R3.18BX membership is 1/1;
- exact stream/header coordinates `3239..3245`, stream id `61`, bound `110`, prop bits `6`;
- exact property object `67`, name `TAGame.PRI_TA:ClientLoadoutsOnline`, tag `LoadoutsOnline`;
- exact context `(110,6,67,LoadoutsOnline,868,32,10,false)`;
- deterministic repeatability;
- truncation inside the true-row header rejects atomically;
- wrong actor object rejects;
- unresolved actor/property lookup rejects;
- wrong version/context rejects;
- `is_rl_223` false-to-true rejects;
- tag-only/object-only/versionless/historical-contract candidate rejects;
- R3.18BN-valid `(110,6,66,ActiveActor,868,32,10,false)` rejects here;
- fabricated tuple rejects;
- post-`payload_start` poison leaves the true-path result unchanged;
- following payload and second later control consumption remain `0/0`;
- source-scope guard proves one BU recomputation, one header-suffix invocation, no payload decoder, no extra bit read and no generic loop.

## Clean candidate scope

The clean production commit must contain only:

1. the minimum `crates/mimir-replay/src/lib.rs` change; and
2. one focused `crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs` integration test.

No temporary workflow/helper, continuity docs, Cargo/dependency, fixture/corpus, raw-state/event/skill/runtime/export or unrelated cleanup belongs in the production commit.

## Validation and publication

Require Rust 1.85 formatting, focused BY tests, directly affected BU/BS/BO/header-prerequisite regressions, workspace check/test, Clippy with warnings denied, repository verifier, exact clean-candidate normal CI, fresh-main ancestry verification, force-free publication, exact published-main SHA/tree readback, and published-main validation on the exact published SHA.

Before any dispatch or rerun, inspect queued/waiting/in-progress equivalent runs and reuse the existing run ID. Rerun is never polling.

## Outcome gate

### Outcome A

The false BU row remains a no-header success; the true BU row composes exactly one header matching R3.18BX; all focused/negative/full validations pass; payload/second-control consumption stays `0/0`. Publish only this bounded composition, then open a separate published-production differential.

### Outcome B

Only a strict safe subset or narrower result representation can be implemented without violating R3.18BX. Publish only that exact subset/representation and rewrite the next differential accordingly.

### Outcome C

Authority drift, false-terminator header access, context/RL223 widening, payload/later-control access, generic chaining, production-scope drift or validation contradiction. Stop without publication.

## Hard stop

No following payload, no second later property-control bit, no context outside exact R3.18BX membership, no false-terminator header synthesis, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
