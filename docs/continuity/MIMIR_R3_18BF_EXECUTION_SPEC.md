# MIMIR R3.18BF — Published R3.18BE Mixed Following-Header Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BE `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`
**Production mutation:** forbidden
**Following payload:** forbidden
**Second later property-control bit:** forbidden
**Witness reselection:** forbidden

## 1. Goal

Validate published R3.18BE against exactly the immutable forty-row R3.18BA/R3.18BC/R3.18BD authority lane.

- The exact 37 BA-false rows must remain successful no-header terminators and stop at the validated BA/BE terminator boundary with zero post-BA reads.
- The exact 3 BA-true rows must return exactly one following header matching the frozen R3.18BC identity/boundaries and exact R3.18BD eight-field membership, then stop exactly at `payload_start`.
- No following payload or second later control may be consumed.
- The seven upstream R3.18AU false terminators remain outside the BA/BE/BF lane and may not be promoted into a successful BE result.

## 2. Frozen authority

```text
production SHA/tree                    1d717d3e82179edd85b197968f46b8f951a3e828 / 72cf2b907437a1ba62cc9deebd7608f7d0372f81
parent                                 3fa88f27201ee91c51a3bb7a623c00b46204c1e0
lib / focused-test blobs               92d9d1893d75f9f0bd5ca921d8cf80455b88f0c3 / 78f32c79a3526cbfeac4e32ccc06e5965cd3e97b
BE execution spec blob                 c5f708fbc88732402bf057bd1274dc11f90669a2
BE production builder                  33129018318/98713908063 SUCCESS
BE validation PR                       #209 closed unmerged
BE exact-head PR CI                    34094630343/101655343287 SUCCESS
BE published-main CI                   34095061141/101656732728 SUCCESS
BC evidence head/tree                  0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
BC evidence run/job                    33122152803/98691409657 SUCCESS
BC artifact                            9666964713 / sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
BD contract                            sha256:33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27
BD membership                          exact_tuple_only / 3 eight-field tuples / multiplicity 3
immutable mixed lane                   40 rows / false=37 / true=3
observed true-header tags              Boolean=2 / Float=1
upstream AU false terminators          7 rows excluded
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

R3.18BC and R3.18BD are immutable authorities. R3.18BF may not reselect witnesses, infer a larger tuple set, or inherit R3.18AT/AJ/Z/P membership.

## 3. Exact differential lane

For every exact frozen BA/BC/BD witness:

1. reconstruct the exact valid published prerequisites through R3.18BA;
2. call published R3.18BE once;
3. require the returned embedded BA control to equal the exact recomputed published BA result;
4. on false, require `following_header == None` and BE stop equal BA stop;
5. on true, require exactly one header whose stream/property/tag/context coordinates and boundary equal frozen R3.18BC authority;
6. require every true header to be an exact R3.18BD member, with exact context multiplicity sum 3 and tag distribution Boolean=2 / Float=1;
7. require true BE stop equal frozen header `payload_start`;
8. repeat and require bit-exact identical result;
9. poison bits beginning at the returned stop and require the returned BE result unchanged;
10. stop without payload or later-control access.

Expected totals:

```text
rows                         40/40
false no-header              37
true exact header            3
exact BD contexts            3/3
BD multiplicity sum          3
tag distribution             Boolean=2 / Float=1
mismatch                     0
witness reselection          0
following payload            0 bits
second later control         0 bits
```

## 4. Required negative controls

At minimum:
- all seven upstream AU false terminators remain outside BA/BE success;
- false-row poison beginning at BA/BE stop leaves the false terminator result unchanged;
- truncate a true row after BA but inside its following header -> reject atomically;
- poison at true-row `payload_start` -> published BE header result unchanged;
- wrong actor object -> reject;
- unresolved lookup -> reject;
- wrong exact version/context -> reject;
- corrupt or mismatched published BA prerequisite -> reject;
- flip/drop `is_rl_223` -> reject unless the complete resulting tuple is independently an exact BD member;
- tag-only/component-only/Cartesian/versionless membership -> reject;
- AT-valid but BD-absent `(60,5,107,Int,868,32,10,false)` -> reject;
- fabricated fourth tuple -> reject;
- source-scope guard -> at most one following-header primitive, zero payload decoders, no generalized/repeated loop.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact BE SHA/tree/blob/CI receipts, exact BC/BD authority receipts, all forty frozen witness identities, per-row BA/BE/BC/direct-header comparison, exact context/multiplicity and tag summaries, repeatability and negative controls, payload/later-control consumption counters, production/Cargo/fixture/corpus/support mutation counters, same-head natural-CI receipt, privacy result and SHA-256 manifest.

## 6. Validation

Require:
- frozen witness identity 40/40;
- published BE exact 40/40;
- false=37 / true=3;
- true frozen header identity/boundary exact 3/3;
- exact BD context identity 3/3 and multiplicity sum 3;
- Boolean=2 / Float=1;
- mismatch 0 and witness reselection 0;
- repeatability PASS;
- all negative controls PASS;
- following payload / second later control 0/0;
- focused BE regressions PASS;
- full mimir-replay/workspace fmt/check/test/clippy and repository verifier PASS;
- same-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy scan PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse an existing exact run if present. Rerun is never polling.

## 7. Hard stop

No following payload, no second later control, no context outside exact R3.18BD, no header on false terminators, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Published R3.18BE matches all 40 immutable BA/BC/BD witnesses exactly: false=37 no-header, true=3 exact header, exact contexts/multiplicity and tag distribution preserved, mismatch 0, witness reselection 0, all negative/full validations PASS, and following-payload/second-control consumption 0/0. A separate R3.18BG evidence pass may then inspect exactly one following payload on the exact three true rows only.

### Outcome B
A bounded differential mismatch or narrower safe subset is isolated. Record only the exact supported subset and keep following-payload evidence closed.

### Outcome C
Authority/witness drift, false-terminator header access, true-header mismatch, BD membership widening, adjacent payload/later-control access, production mutation, generic chaining or privacy failure. Stop without widening.
