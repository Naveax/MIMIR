# MIMIR R3.18BL — Published R3.18BK Mixed Next-Control Differential Decision

**Date:** 2026-09-08
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**
**Production changed:** **NO**
**Canonical production:** `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`

## Decision

R3.18BL closes Outcome A. The published R3.18BK API independently matches immutable R3.18BH control authority on all three frozen rows. The published R3.18BI prerequisite is exact 3/3; the BK result is exact 3/3; the immutable mixed distribution is **false=1 / true=2**; boundary/value mismatch and witness reselection are both zero.

The one false row remains a terminator. The two true rows become continuation candidates for one later header-evidence pass only. BL itself consumed zero following stream/header/payload/second-control bits and made zero production/Cargo/fixture/corpus/support mutations.

## Immutable receipts

```text
canonical pre-pass base                13ec83ae1c34b1cd41f6636e949039886f19d6fe
production SHA/tree                    f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf / 07656c7a43c1afb97903ef33c1109b764fbf8b7d
BL execution spec blob                 3e0a69c14e21b1da12acf38e7d61435b935d40af
BL evidence head/tree                  cd30b3bb4139381ea78a2c8ec0f70c1e162e16a9 / 2b233c68444f8886736b28311507d025bdbaeeab
BL evidence run/job                    34215686040/102026758270 SUCCESS
BL same-head normal CI                 34215686044/102027091932 SUCCESS
BL artifact                            10051851703 / 4001 bytes / sha256:452cb989e2ad9d992c7e8fbb9ff3643d110bee941997fc40f2188b0ce22dcc73
BL inner manifest                      sha256:1270cc5cce9e832cc86f1854ff89c9c8c73ce6d78fe4ee61c985c116f057d53d / 9/9 PASS
BH evidence head                       c728658afa6c55749976c5f30cb5ca4daafe066f
BH evidence run/job                    34132181073/101774645567 SUCCESS
BH artifact                            10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH inner manifest                      sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

The BL ZIP SHA-256 was independently recomputed against fresh GitHub artifact metadata and all 9 manifest-listed files were independently hashed. The frozen BL authority rows match the BH native authority rows exactly.

## Exact frozen result

```text
published BK exact                     3/3
published BI prerequisite              3/3
false / true                           1 / 2
boundary/value mismatch                0
witness reselection                    0
BE false rejected                      37/37
upstream AU false excluded             7/7
following stream/header/payload        0/0/0 bits
second later control                   0 bits
production/Cargo/fixture/corpus/support 0/0/0/0/0
repeatability                          PASS
negative controls                      PASS
full repository validation             PASS
privacy                                PASS
```

Exact rows:

```text
external_fixtures/sample_002.replay                                      11231 -> 11232  true
external_fixtures/sample_003.replay                                       7815 -> 7816   false
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay 3198 -> 3199   true
```

## Sequencing consequence

The next pass is **R3.18BM — One Following-Property-Header Evidence After Published R3.18BK Mixed Control**.

Only the exact two BL/BK true rows may enter its header lane: `sample_002` and `079_1f838...`. `sample_003` is the exact false terminator and must perform zero following-header access.

R3.18BM is read-only and may observe exactly one following property header through `payload_start`. It must classify complete evidence-supported structural/context tuples without decoding the following payload. Any production composition requires a later exact contract pass.

## Hard stop

No following header on the false row, no continuation identity outside the exact two true rows, no following payload, no second later control, no production mutation, no witness reselection, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
