# MIMIR R3.18BM — One Following-Property-Header Evidence After Published R3.18BK Mixed Control

**Status:** ACTIVE
**Pass type:** read-only boundary evidence
**Production authority:** R3.18BK `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`
**Differential authority:** R3.18BL `cd30b3bb4139381ea78a2c8ec0f70c1e162e16a9` / `34215686040/102026758270` / artifact `10051851703` / `sha256:452cb989e2ad9d992c7e8fbb9ff3643d110bee941997fc40f2188b0ce22dcc73`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden
**Witness reselection:** forbidden

## 1. Goal

Preserve exactly the immutable R3.18BL three-row mixed-control lane. The exact one false published-BK row is a terminator and must stop at BK. On only the exact **2 true** rows, observe one following property header through `payload_start`, compare it exactly with native/pinned-Boxcars structural authority, classify the complete observed context, and stop.

This pass characterizes one header boundary only. It does not publish a following-header composition and does not decode the following payload.

## 2. Frozen authority

```text
canonical continuity base             13ec83ae1c34b1cd41f6636e949039886f19d6fe
production SHA/tree                   f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf / 07656c7a43c1afb97903ef33c1109b764fbf8b7d
BL execution spec blob                3e0a69c14e21b1da12acf38e7d61435b935d40af
BL evidence head/tree                 cd30b3bb4139381ea78a2c8ec0f70c1e162e16a9 / 2b233c68444f8886736b28311507d025bdbaeeab
BL authority run/job                  34215686040/102026758270 SUCCESS
BL same-head CI                       34215686044/102027091932 SUCCESS
BL artifact                           10051851703 / 4001 / sha256:452cb989e2ad9d992c7e8fbb9ff3643d110bee941997fc40f2188b0ce22dcc73
BL inner manifest                     sha256:1270cc5cce9e832cc86f1854ff89c9c8c73ce6d78fe4ee61c985c116f057d53d / 9/9 PASS
BL frozen rows                        3
BL false / true                       1 / 2
BL mismatch / reselection             0 / 0
BL adjacent consumption               0/0/0/0
BH artifact                           10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

Header tag/context distribution is **not frozen in advance** and must be discovered from the exact two true rows. Do not infer a Cartesian allowlist.

## 3. Frozen continuation identities

Exactly these BL/BK true witnesses may enter the header lane:

```text
external_fixtures/sample_002.replay                                      BK stop 11232
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay BK stop 3199
```

Exact false terminator:

```text
external_fixtures/sample_003.replay                                       BK stop 7816
```

No other replay/witness may be selected or substituted.

## 4. Witness classification

For all 3 frozen BL rows:
- reconstruct exact published R3.18BI and R3.18BK;
- require BK control value/start/end/stop to equal BL authority;
- if false, classify as terminator and stop with zero following-header access;
- if true, require membership in the exact two-row continuation set and allow exactly one header observation.

Required split: terminator rows 1; continuation rows 2; total 3. Any identity/count drift is Outcome B/C until explained.

## 5. Positive header path — exact 2 true rows

For each true row:
1. build the existing production lookup plan and exact prerequisite chain through published BK;
2. begin the existing stateless existing-actor property-header primitive at the exact BK control boundary required by that primitive;
3. require the property-present state to remain true and equal BL/BK authority;
4. compare stream start/end/value/bound and property-ID width exactly with pinned Boxcars/native structural authority;
5. compare resolved property object and attribute tag exactly;
6. retain complete structural/context identity, including version/net-version/RL223 fields actually required by resolution;
7. compare `payload_start_bit` and header stop exactly;
8. repeat and require deterministic equality 2/2;
9. poison beginning at `payload_start` and require the returned header unchanged 2/2;
10. stop at `payload_start`.

Do not invoke a payload decoder.

## 6. Terminator path — exact 1 false row

For `external_fixtures/sample_003.replay`, published BK control must remain false and exact at `7815 -> 7816`. No following stream/property lookup, header success, payload boundary, or later-control access may be claimed after BK stop.

## 7. Evidence outputs

Produce one privacy-safe immutable evidence artifact containing:
- frozen BL/BK/BH identities and receipts;
- all 3 control-row reconstructions and exact 1/2 terminator/continuation split;
- per-true-row native and pinned-Boxcars header coordinates;
- stream value/bound/property-ID width;
- resolved property object and attribute tag;
- exact replay/version/net-version/RL223 context required to explain resolution;
- complete structural/context tuple multiplicities;
- repeatability and required negative controls;
- following-payload/second-control consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- same-head normal-CI receipt;
- privacy result and SHA-256 inner manifest.

## 8. Required negative controls

At minimum:
- deterministic truncation inside each true-row following header -> fail closed;
- unresolved stream/property lookup -> reject;
- wrong actor object -> reject;
- wrong exact context where required -> reject;
- corrupt/mismatched BK prior -> reject;
- repeatability -> exact equality 2/2;
- poison beginning at `payload_start` -> header unchanged 2/2;
- false sample_003 terminator no-header path -> 1/1;
- fabricated/substituted continuation identity -> reject;
- source-scope guard -> zero following-payload decoder calls and no repeated/generalized property loop;
- following payload / second later control consumption -> 0/0.

## 9. Required gates

```text
BL witness identities                     3/3 exact
published BI/BK reconstruction            3/3 exact
false terminator                          1/1 exact stop
true continuation rows                    2/2
true-row one-header native success        2/2
native/Boxcars header equality            2/2
resolved property object/tag              2/2 exact
payload_start / header stop               2/2 exact
header tuple classification               2/2
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

Run focused BK/BL boundary regressions plus Rust 1.85 fmt/check/test/clippy and the full repository verifier. Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs; reuse an equivalent exact run and never use rerun as polling.

## 10. Hard stop

No following payload decode, no second later property control, no production header composition, no header access on the false row, no witness outside the exact two true rows, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 11. Outcome gate

### Outcome A
Both exact true-row following headers match through `payload_start`; the exact false row remains a terminator; complete header/context classification is exact; mismatch/unclassified/reselection are zero; negatives/full validation/privacy pass; production mutation is zero; following payload/second-control consumption is 0/0. Then a separate smallest exact contract-only pass may freeze only the observed complete header contexts before any production composition.

### Outcome B
A bounded header/context distinction or evidence gap exists. Record it and keep production following-header composition closed.

### Outcome C
Authority/witness drift, native/oracle mismatch, false-row header access, payload/second-control consumption, production mutation, privacy failure, fabricated continuation membership, or generalized chaining. Stop without widening.
