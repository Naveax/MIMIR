# MIMIR R3.18BW — One Following-Property-Header Evidence After Published R3.18BU Mixed Control

**Status:** ACTIVE
**Pass type:** read-only boundary evidence
**Production authority:** R3.18BU `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`
**Differential authority:** R3.18BV `45c6a5b57ee96c8e4b8b472e548c6b1f2d4c426c` / `34830085977/103932439559` / artifact `10341754652` / `sha256:d63f87d75c9c745cfab9b04116cbb3249bcdede7329a0ec8ea5371379548b982`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden
**Witness reselection:** forbidden

## 1. Goal
Preserve exactly the immutable R3.18BV two-row mixed-control lane. The exact false published-BU Boolean row is a terminator and must stop at BU. On only the exact **1 true** ActiveActor row, observe one following property header through `payload_start`, compare it exactly with native/pinned-Boxcars structural authority, classify the complete observed context, and stop.

This pass characterizes one header boundary only. It does not publish a following-header composition and does not decode the following payload.

## 2. Frozen authority
```text
canonical continuity base             58d7e0ac79e4e098215c06e0bc1d365cd5720d61 / 2c7768c9dcac5d96781e8c6d583d75b66bda66b1
production SHA/tree                   43c5d6248e2ea606b2eb0fd95f5c50758c372356 / d1b7b40ed4e361d9c047e0494fb821688ef7d7b4
production parent                     9a86252e02d383ebc2ff9665e678f4c2319f47d9
lib / BU focused-test blobs           1c4db09cff43e0ab56f5efb5e8078da3a1189937 / e6170f90b47e3f04bd798edbc61f2fa59e5213dd
BU execution spec blob                ac1ce2120320bd552e5be24e2309fea23d5a2a50
BV execution spec blob                f6d37f928e7171ac1d100447d1f4775b948abb2a
BV evidence head/tree                 45c6a5b57ee96c8e4b8b472e548c6b1f2d4c426c / 68da2ace745390781ea7e5ade25aaf2c051098d3
BV authority run/job                  34830085977/103932439559 SUCCESS
BV same-head CI                       34830086065/103931122833 SUCCESS
BV artifact                           10341754652 / 2596 / sha256:d63f87d75c9c745cfab9b04116cbb3249bcdede7329a0ec8ea5371379548b982
BV frozen rows                        2
BV false / true                       1 / 1
BV mismatch / reselection             0 / 0
BV adjacent consumption               0/0/0/0
BR authority                          ff1daab35e2e75bf7446a98a07a1db67e5196dbd / artifact 10267123608 / sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

Header tag/context distribution is **not frozen in advance** and must be discovered from the exact one true row. Do not infer a Cartesian allowlist or inherit an older header contract.

## 3. Frozen identities
Exact true continuation:
```text
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay BU stop 3239
```
Exact false terminator:
```text
external_fixtures/sample_002.replay                                      BU stop 11240
```
No other replay/witness may be selected or substituted.

## 4. Witness classification
For both frozen BV rows:
- reconstruct exact published R3.18BS and R3.18BU;
- require BU control value/start/end/stop to equal BV/BR authority;
- if false, classify as terminator and stop with zero following-header access;
- if true, require identity equal to the exact one-row continuation set and allow exactly one header observation.

Required split: terminator 1; continuation 1; total 2. Any identity/count drift is Outcome B/C until explained.

## 5. Positive header path — exact 1 true row
For the exact ActiveActor continuation:
1. reconstruct the existing production lookup plan and exact prerequisite chain through published BU;
2. invoke the existing stateless existing-actor property-header primitive at the exact BU control boundary required by that primitive;
3. require property-present state true and equal BV/BU authority;
4. compare stream start/end/value/bound and property-ID width exactly with pinned Boxcars/native structural authority;
5. compare resolved property object and attribute tag exactly;
6. retain complete structural/context identity, including replay/version/net-version/RL223 fields actually required by resolution;
7. compare `payload_start_bit` and header stop exactly;
8. repeat and require deterministic equality;
9. poison beginning at `payload_start` and require the returned header unchanged;
10. stop at `payload_start`.

Do not invoke a payload decoder.

## 6. Terminator path — exact 1 false row
For `external_fixtures/sample_002.replay`, published BU control must remain false and exact at `11239 -> 11240`. No following stream/property lookup, header success, payload boundary or later-control access may be claimed after BU stop.

## 7. Evidence outputs
Produce one privacy-safe immutable evidence artifact containing BV/BU/BR receipts, both control-row reconstructions, exact 1/1 terminator/continuation split, the true-row native and pinned-Boxcars header coordinates, stream bound/property-ID width, resolved property/tag, complete replay/version/net-version/RL223 context, complete tuple multiplicity, repeatability/negative controls, zero payload/later-control counters, zero mutation counters, same-head natural CI receipt, privacy result and SHA-256 inner manifest.

## 8. Required negative controls
At minimum:
- deterministic truncation inside the true-row following header -> fail closed;
- unresolved stream/property lookup -> reject;
- wrong actor object/context -> reject;
- corrupt/mismatched BU prior -> reject;
- repeatability -> exact equality;
- poison beginning at `payload_start` -> header unchanged;
- false Boolean terminator no-header path -> 1/1;
- fabricated/substituted continuation identity -> reject;
- source-scope guard -> zero following-payload decoder calls and no repeated/generalized property loop;
- following payload / second later control consumption -> 0/0.

## 9. Required gates
```text
BV witness identities                     2/2 exact
published BS/BU reconstruction            2/2 exact
false terminator                          1/1 exact stop
true continuation rows                    1/1
true-row one-header native success        1/1
native/Boxcars header equality            1/1
resolved property object/tag              1/1 exact
payload_start / header stop               1/1 exact
header tuple classification               1/1
unclassified / mismatch                   0 / 0
witness reselection                       0
following payload bits consumed           0
second later control bits consumed        0
negative controls                         PASS
repeatability                             PASS
privacy                                   PASS
production/Cargo/fixture/corpus/support   0/0/0/0/0
same exact evidence-head natural CI       SUCCESS
```

Run focused BU/BV boundary regressions plus Rust 1.85 fmt/check/test/clippy and the full repository verifier. Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs; reuse an equivalent exact run and never use rerun as polling.

## 10. Hard stop
No following payload decode, no second later property control, no production header composition, no header access on the false row, no witness outside the exact one true row, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 11. Outcome gate
### Outcome A
The exact true-row following header matches through `payload_start`; the exact false row remains a terminator; complete header/context classification is exact; mismatch/unclassified/reselection are zero; negatives/full validation/privacy pass; production mutation is zero; following payload/second-control consumption is 0/0. Then a separate smallest exact contract-only pass may freeze only the observed complete header context before any production composition.

### Outcome B
A bounded header/context distinction or evidence gap exists. Record it and keep production following-header composition closed.

### Outcome C
Authority/witness drift, native/oracle mismatch, false-row header access, payload/second-control consumption, production mutation, privacy failure, fabricated continuation membership or generalized chaining. Stop without widening.
