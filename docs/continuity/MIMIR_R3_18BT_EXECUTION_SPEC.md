# MIMIR R3.18BT — Published R3.18BS One-Following-Payload Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BS `5ab14575d0a698d752db35db76f3dbb300cdec8d` / `1c0b4c0a50385a34ba730a52a98a89423ff56869`
**Payload evidence authority:** R3.18BQ `16c43f38e740c57ae9cb90c92084002ec83815e7` / artifact `10144392560` / `sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c`
**Header contract:** R3.18BN `sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`
**Later-control evidence:** R3.18BR false=1 / true=1; evidence only, consumption forbidden
**Production mutation:** forbidden

## 1. Goal

Differentially validate published R3.18BS against exactly the immutable two-row R3.18BQ payload authority. Reconstruct each exact valid prerequisite through R3.18BO, invoke published BS exactly once, require exact payload start/end/width/value identity, and stop at the published payload end.

The R3.18BP false terminator must remain excluded before payload decoding. R3.18BT must not consume the R3.18BR control bit or any next stream/header/payload/second-control data.

## 2. Frozen authority

```text
production SHA/tree                  5ab14575d0a698d752db35db76f3dbb300cdec8d / 1c0b4c0a50385a34ba730a52a98a89423ff56869
production parent                    2f4f536d52a10a28a66bcc7b9b9dc84f7e29b2a6
lib/test blobs                       3428608283d6d0022d466671f90afc9304726dd0 / 706bbdee62a09f04af7bcf70e22567793084d0d6
BS builder                           34617577982/103323236248 SUCCESS
BS exact-head CI                     34617945689/103324450173 SUCCESS
BS published-main CI                 34618640843/103326748345 SUCCESS
BN contract                          sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c / 2 contexts / multiplicity 2
BQ authority                         16c43f38e740c57ae9cb90c92084002ec83815e7 / artifact 10144392560
BQ payload rows                      2
Boolean witness                      [11238,11239) / width1 / true
ActiveActor witness                  [3205,3238) / width33 / active=true actor=1
BP false terminator                  1 / excluded
BR next-control split                false=1 / true=1 / evidence only
```

## 3. Exact differential lane

For each immutable BQ payload witness:
1. reconstruct the exact valid published prerequisites through R3.18BO;
2. invoke published `decode_replay_network_post_bo_following_payload_v1` once;
3. require exact retained BO header composition;
4. require exact payload tag/start/end/width/value equality with the frozen BQ witness;
5. require returned `stop_bit == payload_end_bit`;
6. repeat and require bit-exact identical result;
7. poison bits beginning at returned stop, including the BR control bit, and require BS output unchanged;
8. stop without control/stream/header/payload access beyond BS.

Separately reconstruct the BP/BO false terminator and require BS rejection before payload decoding.

Expected totals:

```text
true payload rows                    2/2
Boolean                              1
ActiveActor                          1
BP false terminator excluded         1/1
BQ identity exact                    2/2
mismatch                             0
witness reselection                  0
following BR control consumed        0
next stream/header/payload           0/0/0
second later control                 0
```

## 4. Required negative controls

At minimum: BP false-terminator exclusion; corrupt BO prerequisite; wrong actor; unresolved lookup; wrong exact version/context; wrong/fabricated resolved tag; payload truncation; payload-start/header-stop mismatch; fabricated Cartesian BN context; historical BD/AT/AJ/Z/P-only context; repeatability; post-payload-end poison including the BR control bit; source-scope guard proving no generic/repeated cursor or later-control read.

## 5. Validation

Require exact production SHA/tree/blobs, exact BQ authority identity, two successful published payload rows, one false terminator excluded, mismatch/reselection 0/0, all negative controls PASS, following-control consumption 0, production/Cargo/fixture/corpus/support mutation 0/0/0/0/0, focused BS regression, full repository verification and same-head natural CI. Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## 6. Hard stop

No R3.18BR control production, no next stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 7. Outcome gate

### Outcome A
Published R3.18BS matches both immutable BQ payload witnesses exactly, the BP false terminator remains excluded, mismatch/reselection are zero, all negative/full validations pass and following-control consumption is zero. Only then may a separate later pass consider whether the already-observed R3.18BR control bit should receive its own production gate.

### Outcome B
A bounded mismatch or narrower safe subset is isolated. Record only the exact supported subset and keep control-bit production closed.

### Outcome C
Authority drift, payload identity mismatch, false-terminator payload access, BR control consumption, generic chaining, mutation leakage or validation contradiction. Stop without widening.
