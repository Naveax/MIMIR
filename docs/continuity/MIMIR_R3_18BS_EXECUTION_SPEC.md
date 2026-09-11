# MIMIR R3.18BS — Bounded Post-BO One-Following-Payload Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production parent:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`
**Header contract:** R3.18BN `sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c` / 2 exact eight-field tuples / multiplicity 2
**Payload evidence authority:** R3.18BQ Outcome A / artifact `10144392560` / `sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c`
**Later-control evidence:** R3.18BR Outcome A / false=1 true=1 / artifact `10267123608` (evidence only; consumption forbidden in BS)
**Admitted payload families:** `Boolean / 1 bit` and `ActiveActor / 33 bits` only

## 1. Goal

Publish exactly one boundary-specific payload composition after a valid R3.18BO true following-header result. The API must validate or recompute the supplied BO/BN authority, begin exactly at the validated `payload_start`, decode exactly one R3.18BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload using existing admitted primitive machinery, return exact payload boundary/value identity, and stop exactly at payload end.

The one R3.18BP false terminator remains outside the BS payload lane. The R3.18BR-observed following control bit must not be consumed. No generic cursor or repeatedly-chainable property loop is admitted.

## 2. Frozen authority

```text
R3.18BO production SHA/tree              cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
R3.18BN exact-context contract            904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
R3.18BN contexts / multiplicity           2 / 2
R3.18BQ evidence head                     16c43f38e740c57ae9cb90c92084002ec83815e7
R3.18BQ artifact                          10144392560 / sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c
R3.18BQ payload identity                  Boolean=1x1 / ActiveActor=1x33
R3.18BQ native/oracle mismatch            0
R3.18BR evidence head                     ff1daab35e2e75bf7446a98a07a1db67e5196dbd
R3.18BR artifact                          10267123608 / sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1
R3.18BR next-control distribution         false=1 / true=1
R3.18BR control production authority      NONE
```

R3.18BQ, not resemblance to older payload ordinals, is the payload authority for BS. R3.18BR proves the boundary after those payloads but does not authorize BS to cross it.

## 3. Production contract

The new boundary-specific API must:

1. accept only a valid R3.18BO true following-header composition under exact R3.18BN membership;
2. reject the BP/BO false-terminator result before any payload decode;
3. validate/recompute supplied BO prerequisites instead of trusting arbitrary caller coordinates;
4. require the resolved header tag to be exactly the BQ-admitted Boolean or ActiveActor tag for its frozen context;
5. require payload start to equal the validated BO header/composition stop;
6. call existing primitive payload machinery for exactly one admitted payload;
7. require exact width and semantic identity: Boolean=1 bit or ActiveActor=33 bits;
8. expose exact payload start/end/width/value while retaining the validated BO header composition;
9. set final `stop_bit` to exactly payload end;
10. consume zero following `property_present` bits.

Every other payload tag/layout and every context outside exact BO/BN/BQ authority is fail-closed even if a lower-level primitive can decode it elsewhere.

## 4. Required focused tests

At minimum:

- exact two frozen BQ true rows reproduce the admitted BO header and payload boundary/value;
- Boolean row reproduces `[11238,11239)` and semantic `true`;
- ActiveActor row reproduces `[3205,3238)` and semantic `active=true, actor=1`;
- the BP false terminator is rejected/excluded before payload decode;
- exact start/end/width/value and final stop equality;
- deterministic repeatability;
- truncation before complete payload rejects atomically;
- wrong resolved tag rejects;
- payload-start/header-stop mismatch rejects;
- corrupt/mismatched BO prior rejects;
- wrong actor / unresolved lookup / wrong exact version context rejects through prerequisite recomputation;
- fabricated Cartesian BN tuple and historical BD/AT/AJ/Z/P-only context reject;
- post-payload-end poison, including the BR control bit, leaves the BS result unchanged;
- following-control consumption remains 0;
- source-scope guard proves no generic/repeated loop or later-control read.

## 5. Clean candidate

Expected clean production scope is the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18BS integration test file. No workflow/helper/evidence artifact, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup enters the production commit.

## 6. Validation and publication

Require Rust 1.85 formatting, focused BS tests, workspace check, clippy with warnings denied, workspace test, repository verifier, exact clean-candidate natural CI, fresh-main ancestry verification, force=false publication and published-main exact-SHA validation. Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs; if an equivalent run exists, reuse that run ID. Rerun is never polling.

## 7. Hard stop

No R3.18BR following-control bit, next stream/header/payload, second later control, generalized/repeated property loop/cursor, next actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Publish exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload composition after valid BO/BN authority, with all focused/negative/full validations PASS and following-control consumption zero. Then open R3.18BT as a separate published-production differential before any control-bit production is considered.

### Outcome B
Only a strict safe subset of the BQ payload authority can be implemented without widening. Publish only that subset and rewrite the next differential pass to the actual production contract.

### Outcome C
Authority drift, unexplained payload mismatch, context/layout widening, BR control-bit access, generic chaining or validation contradiction. Stop without publication.
