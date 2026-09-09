# MIMIR R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** R3.18BK `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`
**Contract authority:** R3.18BN Outcome A / `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`
**Following payload decode:** forbidden
**Second later property-control bit:** forbidden
**Generalized/repeated property loop:** forbidden

## 1. Goal

Publish the minimum boundary-specific composition after one valid published R3.18BK mixed-control result.

- If the validated BK result is `property_present == false`, preserve it as a successful terminator and perform **no following-header lookup or wire consumption**.
- If the validated BK result is `property_present == true`, decode exactly one following existing-actor property header with the existing stateless header primitive, require exact R3.18BN eight-field tuple membership, expose that header identity, and stop exactly at `payload_start`.

No following payload or later control may be consumed.

## 2. Frozen authority

```text
canonical continuity parent           0e36965d2f469f8d2411535b359ac22f9e480fd6 / fc87430df448aff995a4a59c6c87b2cb196da52e
production SHA/tree                   f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf / 07656c7a43c1afb97903ef33c1109b764fbf8b7d
BM evidence head/tree                 689b1a24b57a84c81dc19c9a308fb1423f191c4b / 1d4e95409e1125b01a78aae6a436190b3c1381f4
BM evidence run/job                   34334615939/102410984005 SUCCESS
BM artifact                           10097405795 / sha256:bd51a612be2cdd87d9ce1eb141f3f77f47ae29d42aabc8fc16c260a175f27963
BN exact contract                     sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
BN membership                         exact_tuple_only / 2 eight-field tuples / multiplicity 2
frozen mixed lane                     3 rows / false=1 / true=2
observed true-header tags             Boolean=1 / ActiveActor=1
property ordinal                      7 on 2/2
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

R3.18BN, not resemblance to older contracts, is the sole following-header context authority at this boundary.

## 3. Production contract

The new boundary-specific API must:

1. validate/recompute the supplied published R3.18BK prior instead of trusting arbitrary caller coordinates;
2. require exact equality of BK control start/end/stop with the recomputed prior;
3. branch on the validated BK boolean without re-reading that control;
4. on `false`, return a terminator/no-header result and perform zero stream/header/payload/later-control reads;
5. on `true`, invoke the existing stateless existing-actor header primitive exactly once at the validated BK stop;
6. retain all eight R3.18BN context fields, including `is_rl_223`;
7. require exact membership in the R3.18BN contract, with no tag/component/Cartesian/versionless/RL223-dropped membership;
8. require returned header `property_present == true` and exact alignment to the BK control boundary;
9. expose exact stream/header/property/tag/context coordinates and set final stop exactly to `payload_start`;
10. consume zero following-payload bits and zero second-later-control bits.

The API must not expose a repeatedly-chainable cursor or generic property loop.

## 4. Required focused tests

At minimum:

- exact immutable three-row mixed lane: 1 false terminator + 2 true headers;
- false path succeeds 1/1 without header lookup and without any post-BK bit consumption;
- true path succeeds 2/2 and exact BN membership is 2/2;
- both exact contexts exercised with multiplicity one each;
- observed tags remain Boolean=1 / ActiveActor=1; property ordinal remains 7 on 2/2;
- deterministic repeatability;
- truncation inside a true-row following header rejects atomically;
- wrong actor object rejects;
- unresolved stream/property lookup rejects;
- wrong exact version/context rejects;
- `is_rl_223` false→true mutation rejects;
- tag-only/component-only/Cartesian/versionless candidate rejects;
- BD-valid but BN-absent `(72,6,92,Boolean,868,32,10,false)` rejects;
- fabricated third tuple rejects;
- post-`payload_start` poison leaves the true-path header result unchanged;
- following payload and second later control consumption remain `0/0`;
- source-scope guard proves at most one header primitive call, zero payload decoders and no generalized/repeated property loop.

Synthetic tests supplement but do not widen immutable BM/BN authority.

## 5. Clean candidate

The clean production commit must contain only the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18BO integration test file. No workflow/helper, evidence artifact, Cargo/dependency, fixture/corpus, continuity, raw-state/event/skill/runtime/export or unrelated cleanup may enter the production commit.

## 6. Validation and publication

Require Rust 1.85 formatting, focused BO tests, directly affected BK/BI/header prerequisite regressions, workspace check/test, clippy with warnings denied, repository verifier, exact clean-candidate normal CI, fresh-main ancestry verification, force-free publication, exact published-main SHA/tree readback, and published-main validation on the exact published SHA.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs. Reuse the existing run ID when equivalent. Rerun is never polling.

## 7. Hard stop

No following payload after the one admitted header, no second later property-control bit, no context outside exact R3.18BN membership, no following-header synthesis for a false terminator, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A

The exact false terminator remains a no-header success; the two true rows compose one header matching R3.18BN; all focused/negative/full validations pass; payload/second-control consumption stays `0/0`. Publish only this bounded composition. Then open a separate **R3.18BP published-production differential** pass.

### Outcome B

Only a strict safe subset or narrower result representation can be implemented without violating R3.18BN. Publish only that exact subset/representation and rewrite the next differential accordingly.

### Outcome C

Authority drift, false-terminator header access, context/RL223 widening, payload/later-control access, generic chaining, production-scope drift or validation contradiction. Stop without publication.
