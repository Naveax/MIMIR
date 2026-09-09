# MIMIR R3.18BN — Exact Following-Header Context Contract Decision

**Date:** 2026-09-09
**Outcome:** **A — ADMITTED / BOUNDARY-SPECIFIC EXACT-EIGHT-FIELD CONTRACT**
**Production changed:** **NO**
**Canonical production:** R3.18BK `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`
**Contract:** `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`

## Decision

R3.18BN closes Outcome A. Exactly the two complete eight-field contexts proven by R3.18BM are admitted with exact tuple equality and multiplicity one each. The sole BK-false row remains a terminator outside header membership.

No tag-only, component-only, property-ordinal-only, Cartesian, versionless, RL223-dropped/flipped, R3.18BD/AT/AJ/Z/P inherited, or fabricated third-tuple membership is admitted. Multiplicity is evidence provenance, not a runtime-frequency promise.

## Frozen contract

```text
membership policy                     exact_tuple_only
frozen lane rows                      3
false terminators                     1
observed header rows                  2
unique exact contexts                 2
multiplicity                          1 + 1 = 2
property ordinal                      7 on 2/2
production/Cargo/fixture/corpus/support 0/0/0/0/0
```

Exact admitted contexts:

```text
(72,  6, 95, Boolean,     868, 32, 10, false) x1
(110, 6, 66, ActiveActor, 868, 32, 10, false) x1
```

## Validation receipts

```text
canonical contract base               0e36965d2f469f8d2411535b359ac22f9e480fd6 / fc87430df448aff995a4a59c6c87b2cb196da52e
base exact-SHA CI                     34339899692/102427972308 SUCCESS
candidate head/tree                   c2c25c6b3e6a1c68636b60c444baa608238b2b95 / 50668fe5745bcc349a5e92bb9508992bd74f5f1a
candidate contract sha256             b60329891d7bddd34901bb8a9a423954a930173d597c0a9296d04d6b8a9b1e03
exact contract validation             34340205828/102428959672 SUCCESS
knowledge archive                     34340205835/102428960213 SUCCESS
BM evidence                           689b1a24b57a84c81dc19c9a308fb1423f191c4b / 34334615939/102410984005 SUCCESS
BM same-head CI                       34334615886/102411487443 SUCCESS
BM artifact                           10097405795 / sha256:bd51a612be2cdd87d9ce1eb141f3f77f47ae29d42aabc8fc16c260a175f27963
final admitted contract sha256        904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
```

Required negatives passed for Cartesian recombination, version mutation/drop, RL223 false→true, fabricated third tuple, tag/component-only widening, and an R3.18BD-valid but BN-absent tuple `(72,6,92,Boolean,868,32,10,false)`.

## Sequencing consequence

The next pass is **R3.18BO — Bounded Post-BK Mixed-Continuation Following-Header Production**.

R3.18BO may validate/recompute one exact published BK result. A false BK result must return a successful no-header terminator with zero post-BK reads. A true result may decode exactly one following existing-actor header using the stateless primitive, require exact R3.18BN membership, and stop exactly at `payload_start`.

## Hard stop

No following payload, no second later property-control bit, no header synthesis on the false terminator, no context outside exact R3.18BN membership, no repeated/generalized property loop/cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
