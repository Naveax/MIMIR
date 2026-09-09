# MIMIR R3.18BP — Published R3.18BO Mixed Following-Header Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`
**Contract authority:** R3.18BN `sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`
**Production mutation:** forbidden
**Following payload:** forbidden
**Second later property-control bit:** forbidden
**Witness reselection:** forbidden

## 1. Goal

Validate published R3.18BO against exactly the immutable three-row R3.18BM/R3.18BN/R3.18BK authority.

- The exact BK-false row must remain a successful no-header terminator and stop at the validated BK boundary with zero post-BK reads.
- The exact two BK-true rows must return exactly one following header matching frozen R3.18BM identity/boundaries and exact R3.18BN eight-field membership, then stop exactly at `payload_start`.
- No following payload or second later control may be consumed.
- The 7 upstream AU exclusions and 37 intermediate BE exclusions remain outside the BO success lane.

## 2. Frozen authority

```text
production SHA/tree                    cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
parent                                 a07b405ee5bb299b468d6bcfc8e66ba89a69e40d
lib/test blobs                         89359ead38b18e4a71448217561caed97a41b915 / 5bfd9a81e0de21e70f93e24d8b43a4b540724e9c
BO execution spec blob                 3be058d574cf55f3dfaf9e369c37bf3fa42afaa4
BO production builder                  34346270277/102448481752 SUCCESS
BO exact-candidate CI                  34347518210/102452536398 SUCCESS
BO published-main CI                   34348026122/102454170761 SUCCESS
BM evidence head/tree                  689b1a24b57a84c81dc19c9a308fb1423f191c4b / 1d4e95409e1125b01a78aae6a436190b3c1381f4
BM evidence run/job                    34334615939/102410984005 SUCCESS
BM artifact                            10097405795 / sha256:bd51a612be2cdd87d9ce1eb141f3f77f47ae29d42aabc8fc16c260a175f27963
BN contract                            sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
BN membership                          exact_tuple_only / 2 eight-field tuples / multiplicity 2
immutable mixed lane                   3 rows / false=1 / true=2
observed true-header tags              Boolean=1 / ActiveActor=1
property ordinal                       7 on 2/2
upstream exclusions                    AU=7 / BE=37
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

## 3. Exact differential lane

For every exact frozen BK witness:
1. reconstruct the exact valid published prerequisites through R3.18BK;
2. call published R3.18BO once;
3. require embedded BK control equality with the recomputed published BK result;
4. on false, require `following_header == None` and BO stop equal BK stop;
5. on true, require exactly one header matching frozen BM identity/boundaries;
6. require exact R3.18BN membership, multiplicity sum 2 and Boolean=1 / ActiveActor=1;
7. require true BO stop equal frozen `payload_start`;
8. repeat and require bit-exact identical result;
9. poison bits beginning at returned stop and require BO unchanged;
10. stop without payload or later-control access.

Expected totals:

```text
rows                         3/3
false no-header              1
true exact header            2
exact BN contexts            2/2
BN multiplicity sum          2
tag distribution             Boolean=1 / ActiveActor=1
property ordinal             7 on 2/2
mismatch                     0
witness reselection          0
following payload            0 bits
second later control         0 bits
```

## 4. Required negative controls

At minimum: false-row post-stop poison; all 7 AU and 37 BE exclusions remain outside BO success; true-header truncation; true `payload_start` poison; wrong actor; unresolved lookup; wrong exact version/context; corrupt BK prerequisite; RL223 flip/drop; tag/component/Cartesian/versionless widening; older-contract BN-absent tuple; fabricated third tuple; source-scope guard with zero payload decoder and no repeated/generalized loop.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact BO SHA/tree/blob/CI receipts, BM/BN authority receipts, all three frozen witness identities, per-row BK/BO/BM/direct-header comparison, exact context/multiplicity and tag summaries, repeatability and negative controls, payload/later-control counters, production/Cargo/fixture/corpus/support mutation counters, same-head natural-CI receipt, privacy result and SHA-256 manifest.

## 6. Validation

Require frozen identity 3/3; published BO exact 3/3; false=1 / true=2; true frozen header identity/boundary exact 2/2; exact BN contexts 2/2 and multiplicity 2; Boolean=1 / ActiveActor=1; mismatch/reselection 0/0; repeatability and all negatives PASS; following payload/second control 0/0; focused BO regressions; full fmt/check/test/clippy/repository verifier; same-head CI SUCCESS; mutation 0/0/0/0/0; privacy PASS.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs. Reuse an existing exact run if present. Rerun is never polling.

## 7. Hard stop

No following payload, no second later control, no context outside exact R3.18BN, no header on the false terminator, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Published R3.18BO matches all 3 immutable BM/BN/BK witnesses exactly: false=1 no-header, true=2 exact header, exact contexts/multiplicity and tag distribution preserved, mismatch 0, witness reselection 0, all negative/full validations PASS, and following-payload/second-control consumption 0/0. Only then may a separate later evidence pass inspect exactly one following payload on the exact two true rows.

### Outcome B
A bounded mismatch or narrower safe subset is isolated. Record only the exact supported subset and keep following-payload evidence closed.

### Outcome C
Authority/witness drift, false-terminator header access, true-header mismatch, BN widening, adjacent payload/later-control access, production mutation, generic chaining or privacy failure. Stop without widening.
