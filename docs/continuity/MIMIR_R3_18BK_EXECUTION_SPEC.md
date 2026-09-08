# MIMIR R3.18BK — Bounded Post-BI Next Property-Control Production

**Status:** ACTIVE
**Pass type:** bounded production composition
**Production base:** R3.18BI `def8e959239106e25d95091fcfcf468fec59e228` / `61ca1c3cdf504f4c1eaef3001cbe81984414c537`
**Published differential gate:** R3.18BJ Outcome A, `fa75bb265eed9909047076d4a35e55e65dd27838` / run `34191528993`
**Control authority:** immutable R3.18BH artifact `10023482583`
**Witness reselection:** forbidden

## 1. Goal

Publish exactly one already-evidenced R3.18BH `property_present` control bit immediately after a valid published R3.18BI payload result, on only the three immutable BI/BG/BH authority rows.

R3.18BK must validate/recompute the supplied BI prior, require the exact BI payload-end boundary, consume exactly one bit, accept both boolean values observed by BH (`false=1 / true=2`), and stop exactly one bit later.

This is not a property loop. It does not decode a following stream ID, property header, payload or a second later control.

## 2. Frozen authority

```text
production base SHA/tree              def8e959239106e25d95091fcfcf468fec59e228 / 61ca1c3cdf504f4c1eaef3001cbe81984414c537
BI lib/test blobs                     2307ea008176d27208e2354c9706f09dc447fd5f / 16b15e1fa5dc71d295837578dff861635679ffc9
BJ evidence SHA/tree                  fa75bb265eed9909047076d4a35e55e65dd27838 / 877f783c665215a56f43a71aec0abfe23acb99ce
BJ evidence run/job                   34191528993/101950417302 SUCCESS
BJ same-head natural CI               34191528959/101950417219 SUCCESS / count=1
BJ artifact                           10042480960 / sha256:e9ec49453dc69c384042b67ee6e459881999478f4ab5e6fe978ce171299ff24d
BJ manifest                           sha256:ac1ec9da8053f21e54bb4ff4e42d63c46058a281374412a9e31a87e6228012c4
BH evidence head                      c728658ac237a45f34b3af002c27f704f5293fb5
BH artifact                           10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH manifest                           sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
BH exact rows                         3/3
BH observed distribution              false=1 / true=2
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## 3. Exact production contract

For an R3.18BK call:

1. recompute the published R3.18BI result from the supplied published prerequisites;
2. require field equality between the recomputed BI result and the supplied BI prior;
3. require `control_start_bit == BI.stop_bit == BI.following_payload.payload_end_bit`;
4. read exactly one checked bit at `control_start_bit`;
5. materialize that bit as `property_present: bool` without true-only filtering;
6. require `control_end_bit == control_start_bit + 1` with checked arithmetic;
7. return with `stop_bit == control_end_bit`;
8. perform no read at or after `control_end_bit`.

The production implementation must not consult replay paths, hashes, fixture names, evidence artifacts or the external Boxcars oracle at runtime. Exact lane membership is inherited only through the already-published BI/BE/BD authority and the validated BI prior.

Expected frozen production lane:

```text
successful authority rows             3/3
false / true                          1 / 2
new bits consumed per success         1
BI boundary mismatch                  0
BE false success                      0/37
AU false success                      0/7
following stream/header/payload       0/0/0 bits
second later control                  0 bits
generalized property loop             0
```

## 4. Required negative controls

At minimum:
- supplied BI prior differs from recomputed published BI -> reject atomically;
- wrong actor / unresolved lookup / wrong exact upstream context -> reject through the published prerequisite chain;
- truncate exactly at `control_start_bit` -> reject without partial result;
- corrupt BI payload start/end/stop or payload semantic identity -> reject before the new control result is returned;
- poison any bit strictly after `control_end_bit` -> BK result unchanged 3/3;
- all 37 BE false terminators -> no BK success;
- all 7 upstream AU false terminators -> no BK success;
- fabricated fourth BI/BG/BH authority row -> reject;
- source-scope guard -> exactly one new control-bit read and zero following stream/header/payload/second-control reads.

## 5. Production construction rule

Evidence helpers and temporary workflow/probe code are not production. Construct the clean production change from verified source edits only.

Expected source scope is exactly:
- `crates/mimir-replay/src/lib.rs`;
- one focused `crates/mimir-replay/tests/r3_18bk_post_bi_following_control.rs` test target.

Cargo, fixture, corpus, scripts/support, generated artifacts and unrelated crates remain unchanged unless a concrete blocker is separately admitted.

## 6. Validation

Require focused BK tests plus the BI/BE and primitive-scalar prerequisite regressions; `cargo fmt --all -- --check`; workspace `cargo check --locked`; workspace tests; workspace clippy with warnings denied; repository verifier; clean-source scope audit; exact-head normal CI; fresh-main ancestry audit; force=false publication; published-main readback and CI.

Before dispatch or rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Never dispatch a duplicate merely to poll.

## 7. Hard stop

No following stream ID, following property header, following payload, second later property-control bit, wider payload/header context, generalized/repeated property cursor, next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Exactly 3/3 immutable authority rows produce one new control bit with the frozen false=1 / true=2 distribution, exact BI boundary validation, one-bit stop semantics, all negatives and full validation PASS, source scope remains exact, and no adjacent structure is consumed. Publish the clean production SHA, then open a separate published-R3.18BK differential before any following-header evidence or production.

### Outcome B/C
Any authority drift, BI mismatch, false-lane success, value filtering, overread, source-scope widening, validation failure or privacy/provenance defect keeps R3.18BK unadmitted and all later structure closed.
