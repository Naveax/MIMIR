# MIMIR R3.18AU — Bounded Post-AQ Mixed-Continuation Following-Header Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** R3.18AQ `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`
**Contract authority:** R3.18AT Outcome A / `docs/continuity/MIMIR_R3_18AT_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5`
**Following payload decode:** forbidden
**Second later property-control bit:** forbidden
**Generalized/repeated property loop:** forbidden

## 1. Goal

Publish the minimum boundary-specific composition after one valid published R3.18AQ mixed control result.

- If the validated AQ result is `property_present == false`, preserve it as a successful terminator and perform **no following-header lookup or wire consumption**.
- If the validated AQ result is `property_present == true`, decode exactly one following existing-actor property header with the existing stateless header primitive, require exact R3.18AT eight-field tuple membership, expose that header identity, and stop exactly at `payload_start`.

No following payload or later control may be consumed.

## 2. Frozen authority

```text
canonical continuity parent           b8e9bb465bd49974ca23e00c42ea29d59beecb39 / 7480a997259b5f77a88e1326da2ccfbebe801f80
production SHA/tree                   e1ccbef95c8424b689dee7d77fd8fde2af3e0204 / 4e7100625096594bcc5c5b4c6a8054c283643b13
production parent                     ec2d6c29f90863d9e312856043d01fb98a0c2d2d
production lib / AQ test blobs        b886c58400de0efe0a6a6113d79e6f78e751a213 / 983cbda666f40cbc739b250eac87bc4ce0c9eb99
AS evidence head/tree                 475650fea59332f74b9f69da50e3e4471622ab7e / 1303071ad3031f4095e29d775afd243286a67b64
AS authority run/job                  32959321642/98147938829 SUCCESS
AS artifact                           9603335255 / sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
AT exact contract                     sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
AT membership                         exact_tuple_only / 16 eight-field tuples / multiplicity 40
frozen mixed lane                     47 rows / false=7 / true=40
observed true-header tags              Int=40
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

R3.18AT, not resemblance to R3.18AJ/Z/P, is the sole following-header context authority at this boundary.

## 3. Production contract

The new boundary-specific API must:

1. validate/recompute the supplied published R3.18AQ prior instead of trusting arbitrary caller coordinates;
2. require exact equality of AQ control start/end/stop with the recomputed prior;
3. branch on the validated AQ boolean without re-reading that control;
4. on `false`, return a terminator/no-header result and perform zero stream/header/payload/later-control reads;
5. on `true`, invoke the existing stateless existing-actor header primitive exactly once at the validated AQ stop;
6. retain all eight R3.18AT context fields, including `is_rl_223`;
7. require exact membership in the R3.18AT contract, with no tag/component/Cartesian/versionless/RL223-dropped membership;
8. require returned header `property_present == true` and exact alignment to the AQ control boundary;
9. expose exact stream/header/property/tag/context coordinates and set final stop exactly to `payload_start`;
10. consume zero following-payload bits and zero second-later-control bits.

The API must not expose a repeatedly-chainable cursor or generic property loop.

## 4. Required focused tests

At minimum:

- exact immutable 47-row mixed lane: 7 false terminators + 40 true headers;
- false path succeeds without header lookup and without any post-AQ bit consumption;
- true path succeeds 40/40 and exact AT membership is 40/40;
- all 16 exact contexts exercised with multiplicities matching frozen evidence;
- deterministic repeatability;
- truncation inside a true-row following header rejects atomically;
- wrong actor object rejects;
- unresolved stream/property lookup rejects;
- wrong exact version/context rejects;
- `is_rl_223` false->true mutation rejects;
- tag-only/component-only/Cartesian/versionless candidate rejects;
- AJ-valid but AT-absent `(60,5,38,Int,868,32,10,false)` rejects;
- fabricated seventeenth tuple rejects;
- post-`payload_start` poison leaves the true-path header result unchanged;
- following payload and second later control consumption remain `0/0`;
- source-scope guard proves at most one header primitive call, zero payload decoders and no generalized/repeated property loop.

Synthetic tests supplement but do not widen the immutable AS/AT authority.

## 5. Clean candidate

The clean production commit must contain only the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18AU integration test file. No workflow/helper, evidence artifact, Cargo/dependency, fixture/corpus, continuity, raw-state/event/skill/runtime/export or unrelated cleanup may enter the production commit.

## 6. Validation and publication

Require:

- Rust 1.85 formatting;
- focused AU tests;
- directly affected AQ/AN/header prerequisite regressions;
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

No following payload after the one admitted header, no second later property-control bit, no context outside the exact R3.18AT contract, no following-header synthesis for a false terminator, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A

The exact 7 false terminators remain no-header successes; the exact 40 true rows compose one header matching the R3.18AT contract; all focused/negative/full validations pass; payload/second-control consumption stays `0/0`. Publish only this bounded mixed-continuation composition. Then open a separate published-production differential pass.

### Outcome B

Only a strict safe subset or narrower result representation can be implemented without violating R3.18AT. Publish only that exact subset/representation and rewrite the next differential accordingly.

### Outcome C

Authority drift, false-terminator header access, context/RL223 widening, payload/later-control access, generic chaining, production-scope drift or validation contradiction. Stop without publication.
