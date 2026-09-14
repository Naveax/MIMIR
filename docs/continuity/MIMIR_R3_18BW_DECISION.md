# MIMIR R3.18BW Decision — One Following-Property-Header Evidence After Published R3.18BU

**Date:** 2026-09-14
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**
**Production changed:** **NO**
**Canonical production:** R3.18BU `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`

## Decision

R3.18BW closes Outcome A. The immutable R3.18BV/R3.18BU two-row mixed-control lane remained exact: the Boolean=false row terminated at BU stop 11240 with zero following-header access, while the ActiveActor=true row exposed exactly one following existing-actor property header and stopped at `payload_start=3245`.

Native MIMIR and pinned Boxcars matched 1/1 through the full header boundary. Mismatch, unclassified rows and witness reselection are zero. Following-payload and second-later-control consumption are both zero. Production/Cargo/fixture/corpus/support mutation remained `0/0/0/0/0`.

## Immutable receipts

```text
canonical continuity base             64f81e106338493476954f207a997a2bc7c25c9a / 3f023aa0fb0f4d1c695b5d1e3eaab7b3321ff797
production SHA/tree                   43c5d6248e2ea606b2eb0fd95f5c50758c372356 / d1b7b40ed4e361d9c047e0494fb821688ef7d7b4
BW evidence head/tree                 778b12988046da4d186248877bd577eb2a533a58 / 5a6e7bd95c95f3e38db34a543b396aec747db985
BW evidence run/job                   34843377101/103973337631 SUCCESS
BW same-head natural CI               34843377045/103976995152 SUCCESS
BW artifact                           10346819501 / 3582 bytes / sha256:ee8a1878241b45765a7fa57c64c179c40090836096055fc5626a58724b5796fd
BW header rows                        sha256:003d956cd7b4a8eb266c51d4514f9533a3c147eb4923f3113e08673323fb3a38
BW aggregate                          sha256:12abc510fe9821c6fe3ef21e1ecdc3dc53a9b4235b75ca318a6ba77cd574fa4d
BW negatives                          sha256:f47d318ecfdf47098a697ea2f94e2fdd4a37221925dd260496107ac133858edc
BW validation                         sha256:8dd144e6f69992f8c8a31ac0c196c04a59a2ecea199164fe4860f2e50479f445
BW source scope                       sha256:d91a11794cabcb5e001fe59e66c8b5fcd75ea70a73ce7bf4d925c6af723a8582
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Exact frozen result

```text
frozen BU control rows                2/2
false terminators                     1/1
true continuation rows                1/1
one following header exact            1/1
unique exact contexts                 1
property ordinal                      8 on 1/1
native/oracle mismatch                0
unclassified                          0
witness reselection                   0
false terminator header access        0
following payload bits                0
second later control bits             0
production/Cargo/fixture/corpus/support 0/0/0/0/0
```

Exact observed context:

```text
(110, 6, 67, LoadoutsOnline, 868, 32, 10, false) x1
```

Exact true-row coordinates:

```text
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay
  BU true             3238 -> 3239
  stream_id           61 / bound 110
  stream end          3245
  property index/tag  67 / LoadoutsOnline
  payload_start       3245
```

False terminator:

```text
external_fixtures/sample_002.replay
  BU false            11239 -> 11240
  following header    forbidden / zero access
```

## Sequencing consequence

The next contract pass is **R3.18BX — Exact Following-Header Context Contract After R3.18BW**. R3.18BX may admit only the single complete eight-field tuple above. Production following-header composition remains closed until that exact contract is separately admitted.

## Hard stop

No following payload, no second later property-control bit, no false-row header access, no historical-contract inheritance, no production mutation, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
