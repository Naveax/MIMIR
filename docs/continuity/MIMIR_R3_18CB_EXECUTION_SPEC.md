# MIMIR R3.18CB — Exact Post-BU One-Payload Production

**Status:** ACTIVE / BOUNDED PRODUCTION CANDIDATE
**Pass type:** narrow production composition
**Production baseline:** R3.18BY `3b07e223fdf326e8100412fad9410bb1b66d2cb9` / `68b32f61d61c863b25e393cfa77575bac55217d7`
**Evidence authority:** R3.18CA `01ebdf5a8c7b192ef19a280711b3b0947f373647` / run `34989130467` / artifact `10405136702`
**Existing payload decoder authority:** published R3.17O K4 only

## Goal

Extend the published R3.18BY boundary by exactly one payload and nothing else. On the immutable true row, compose the already-published R3.18BY following header with the already-published K4 decoder for the exact CA-observed `LoadoutsOnline` representation. On the false row, terminate before payload access exactly as BY already does.

## Exact production lane

```text
false row       external_fixtures/sample_002.replay
false stop      11240
false payload   none / access 0

true row        test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay
header tuple    (110,6,67,LoadoutsOnline,868,32,10,false)
payload         [3245,4227)
width           982
semantic hash   7641391ebd59828550db4ee24036b07a47a0bf40057c9c34024e5461787eb142
K4 membership   existing published exact membership only
```

Exact structural shape:

```text
LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]
```

## Implementation contract

Add one boundary-specific public result/API in `crates/mimir-replay/src/lib.rs` and one focused integration test `crates/mimir-replay/tests/r3_18cb_post_bu_following_payload.rs`.

The implementation must:

1. recompute the published R3.18BY result from the same frozen prerequisite chain and reject a supplied/fabricated BY result that differs from recomputed authority;
2. preserve BY false termination exactly: `following_header=None`, `following_payload=None`, stop 11240, zero payload decode;
3. on BY=true require the exact R3.18BX/CA header tuple `(110,6,67,LoadoutsOnline,868,32,10,false)` and exact payload start 3245;
4. convert the already-resolved replay context to the existing `ReplayNetworkK4DecodeContextV1` without changing version/net/RL223 semantics;
5. invoke only `decode_replay_network_k4_v1` with tag `LoadoutsOnline`, payload start 3245 and the existing footer object lookup table;
6. require the existing K4 membership to accept the exact observed CA representation;
7. require returned start/end/width/shape to be exactly `3245/4227/982/LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]`;
8. return the existing typed K4 decoded value without introducing a second semantic representation;
9. stop exactly at payload end 4227 and consume zero next property-control bits.

The K4 decoder and admitted-group tables are dependencies of this composition, not edit targets.

## Required focused tests

- exact two-row lane: false terminator 1/1, true payload 1/1;
- exact BY prerequisite equality and fabricated/corrupt BY rejection;
- exact true header context and payload boundary/value shape;
- existing K4 membership accepted without allowlist mutation;
- repeat decode deterministic equality;
- truncation inside materially distinct payload regions fails atomically;
- post-payload-end poison leaves the composed result unchanged;
- unresolved actor/property/object lookup prerequisites fail closed;
- wrong version major/minor, net version and RL223 context fail closed;
- false row proves zero payload access;
- source-scope test proves one BY recomputation, at most one K4 payload decode, zero next-control read and no generalized loop/cursor.

## Clean source scope

The production commit may contain exactly:

1. the minimum `crates/mimir-replay/src/lib.rs` change; and
2. `crates/mimir-replay/tests/r3_18cb_post_bu_following_payload.rs`.

No continuity docs, workflow/helper, Cargo/dependency, fixture/corpus/support, K4 decoder/allowlist, raw-state/event/skill/runtime/export or unrelated cleanup belongs in the production commit.

## Validation and publication

Require Rust 1.85 formatting, focused CB tests, full `mimir-replay` regression, workspace check/test, Clippy with warnings denied, repository verifier, exact two-file scope, clean reconstruction from fresh canonical main, natural exact-head CI, fresh-main ancestry recheck, force=false publication and exact published-main CI/Knowledge Archive readback.

## Outcome gate

### Outcome A

Both immutable rows satisfy the exact contract, all negatives pass, the existing K4 representation remains unchanged, production stops at 11240 or 4227 as appropriate, and no next-control bit is consumed. Publish R3.18CB and open R3.18CC only as a read-only differential over the published CB API.

### Outcome B/C

Any prerequisite drift, K4 rejection, structural/semantic mismatch, truncation/poison failure, false-row payload access, later-control consumption or need for broader source changes stops publication. Open the smallest prerequisite evidence/contract pass; do not widen CB.

## Hard stop

No K4 decoder or allowlist widening; no payload context/tag/shape beyond the exact CA witness; no payload on the false row; no next property-control bit after 4227; no second payload/following header; no generic/repeated cursor/property loop; no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior.
