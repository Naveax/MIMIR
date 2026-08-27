# MIMIR R3.18BE — Bounded Post-BA Mixed-Continuation Following-Header Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Contract authority:** R3.18BD Outcome A / `docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`
**Following payload decode:** forbidden
**Second later property-control bit:** forbidden
**Generalized/repeated property loop:** forbidden

## 1. Goal

Publish the minimum boundary-specific composition after one valid published R3.18BA mixed control result.

- If the validated BA result is `property_present == false`, preserve it as a successful terminator and perform **no following-header lookup or wire consumption**.
- If the validated BA result is `property_present == true`, decode exactly one following existing-actor property header with the existing stateless header primitive, require exact R3.18BD eight-field tuple membership, expose that header identity, and stop exactly at `payload_start`.

No following payload or later control may be consumed.

## 2. Frozen authority

```text
canonical continuity parent           387e1693279dec062d3ef565cc5bc597de3a5a13 / a0dedfb8de603cc4e000a1777ed074eaed1c3163
production SHA/tree                   5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BC evidence head/tree                 0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
BC authority run/job                  33122152803/98691409657 SUCCESS
BC artifact                           9666964713 / sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
BD exact contract                     sha256:33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27
BD membership                         exact_tuple_only / 3 eight-field tuples / multiplicity 3
frozen mixed lane                     40 rows / false=37 / true=3
observed true-header tags             Boolean=2 / Float=1
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

R3.18BD, not resemblance to R3.18AT/AJ/Z/P, is the sole following-header context authority at this boundary.

## 3. Production contract

The new boundary-specific API must:

1. validate/recompute the supplied published R3.18BA prior instead of trusting arbitrary caller coordinates;
2. require exact equality of BA control start/end/stop with the recomputed prior;
3. branch on the validated BA boolean without re-reading that control;
4. on `false`, return a terminator/no-header result and perform zero stream/header/payload/later-control reads;
5. on `true`, invoke the existing stateless existing-actor header primitive exactly once at the validated BA stop;
6. retain all eight R3.18BD context fields, including `is_rl_223`;
7. require exact membership in the R3.18BD contract, with no tag/component/Cartesian/versionless/RL223-dropped membership;
8. require returned header `property_present == true` and exact alignment to the BA control boundary;
9. expose exact stream/header/property/tag/context coordinates and set final stop exactly to `payload_start`;
10. consume zero following-payload bits and zero second-later-control bits.

The API must not expose a repeatedly-chainable cursor or generic property loop.

## 4. Required focused tests

At minimum:

- exact immutable 40-row mixed lane: 37 false terminators + 3 true headers;
- false path succeeds 37/37 without header lookup and without any post-BA bit consumption;
- true path succeeds 3/3 and exact BD membership is 3/3;
- all 3 exact contexts exercised with multiplicity one each;
- observed tags remain Boolean=2 / Float=1;
- deterministic repeatability;
- truncation inside a true-row following header rejects atomically;
- wrong actor object rejects;
- unresolved stream/property lookup rejects;
- wrong exact version/context rejects;
- `is_rl_223` false->true mutation rejects;
- tag-only/component-only/Cartesian/versionless candidate rejects;
- AT-valid but BD-absent `(60,5,107,Int,868,32,10,false)` rejects;
- fabricated fourth tuple rejects;
- post-`payload_start` poison leaves the true-path header result unchanged;
- following payload and second later control consumption remain `0/0`;
- source-scope guard proves at most one header primitive call, zero payload decoders and no generalized/repeated property loop.

Synthetic tests supplement but do not widen the immutable BC/BD authority.

## 5. Clean candidate

The clean production commit must contain only the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18BE integration test file. No workflow/helper, evidence artifact, Cargo/dependency, fixture/corpus, continuity, raw-state/event/skill/runtime/export or unrelated cleanup may enter the production commit.

## 6. Validation and publication

Require:

- Rust 1.85 formatting;
- focused BE tests;
- directly affected BA/AY/header prerequisite regressions;
- workspace check;
- workspace test;
- clippy with warnings denied;
- repository verifier;
- exact clean-candidate normal CI;
- fresh-main ancestry verification;
- force-free publication;
- exact published-main SHA/tree readback;
- published-main validation on the exact published SHA.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse the existing run ID when equivalent. Rerun is never polling.

## 7. Hard stop

No following payload after the one admitted header, no second later property-control bit, no context outside the exact R3.18BD contract, no following-header synthesis for a false terminator, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A

The exact 37 false terminators remain no-header successes; the exact 3 true rows compose one header matching the R3.18BD contract; all focused/negative/full validations pass; payload/second-control consumption stays `0/0`. Publish only this bounded mixed-continuation composition. Then open a separate R3.18BF published-production differential pass.

### Outcome B

Only a strict safe subset or narrower result representation can be implemented without violating R3.18BD. Publish only that exact subset/representation and rewrite the next differential accordingly.

### Outcome C

Authority drift, false-terminator header access, context/RL223 widening, payload/later-control access, generic chaining, production-scope drift or validation contradiction. Stop without publication.
