# MIMIR R3.18BK — Bounded Post-BI Next Property-Control Production Decision

**Date:** 2026-09-08
**Outcome:** **A — ADMITTED / PRODUCTION CLOSED**
**Canonical production:** `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`
**Parent:** `de8df0b2bb36454c97863d4078ce7829fd4ecb77`

## Decision

R3.18BK closes Outcome A. Production now validates/recomputes one exact published R3.18BI payload result and consumes exactly one already-evidenced R3.18BH `property_present` control bit immediately at the BI payload end, on only the three immutable BI/BG/BH authority rows.

Both observed boolean classes are production data at this boundary: **false=1 / true=2**. The control starts exactly at `BI.stop_bit == BI.following_payload.payload_end_bit`, consumes one LSB-first bit, and ends/stops exactly one bit later. Earlier true-only control semantics are not inherited.

The 37 R3.18BE false terminators and 7 upstream R3.18AU false terminators remain outside success. Production reads no following stream ID, header, payload or second later control and exposes no repeated/generalized property cursor.

## Exact authority

```text
production SHA/tree                   f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf / 07656c7a43c1afb97903ef33c1109b764fbf8b7d
parent                                de8df0b2bb36454c97863d4078ce7829fd4ecb77
lib blob                              0bfff19a7d285e07508b648dbcd5af95a31838f6
focused BK test blob                  1938707e60f7893768747931bf84e3bbac792d1b
BK execution spec blob                12d3c92db43433871deaf2d86889b770bfd4af3d
builder                               34211911298/102014640422 SUCCESS
validation PR                         #216 closed unmerged
exact-head PR CI                      34212312983/102015924320 SUCCESS
published-main CI                     34212774993/102017408925 SUCCESS
BH artifact                           10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH manifest                           sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
BJ artifact                           10042480960 / sha256:e9ec49453dc69c384042b67ee6e459881999478f4ab5e6fe978ce171299ff24d
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Frozen production result

```text
authority rows                        3/3
false / true                          1 / 2
control width                         1 bit each
sample_002                            11231 -> 11232 / true
sample_003                            7815 -> 7816 / false
079_1f838...                          3198 -> 3199 / true
published BI prerequisite             exact 3/3
BE false excluded                     37/37
upstream AU false excluded            7/7
following stream/header/payload       0/0/0 bits
second later control                  0 bits
production scope                      exactly 2 files
```

Focused BK plus BI/BE regressions passed in the builder, full repository verification passed, exact-head PR CI passed, and published-main exact-SHA CI passed. The clean canonical commit contains no workflow/helper, Cargo/dependency, fixture/corpus, support, continuity, skill/runtime/export, or unrelated mutation.

## Sequencing consequence

The next pass is **R3.18BL — Published R3.18BK Mixed Next-Control Differential**. It is read-only and must compare the published BK result against immutable BH authority on exactly the three rows before any following-header evidence is allowed.

The false row is a terminator. The two true rows are only continuation candidates; a later separate pass may inspect one following header on those two rows only after BL Outcome A.

## Hard stop

No following stream/header/payload during BL, no second later control, no production mutation, no witness reselection, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
