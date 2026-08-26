# MIMIR R3.18AV — Published R3.18AU Mixed Following-Header Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18AU `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef`
**Production mutation:** forbidden
**Following payload:** forbidden
**Second later property-control bit:** forbidden
**Witness reselection:** forbidden

## Goal

Validate the published R3.18AU mixed following-header API against exactly the immutable 47-row R3.18AS/R3.18AT authority lane.

- The exact 7 AQ-false rows must remain successful no-header terminators and stop at the already-published AQ/AU terminator boundary with zero post-AQ reads.
- The exact 40 AQ-true rows must return exactly one following header matching the frozen R3.18AS header identity/boundaries and exact R3.18AT eight-field membership, then stop exactly at `payload_start`.
- No following payload or second later control may be consumed.

## Frozen authority

```text
production SHA/tree                    6a9f456c78ffccab177823234a8d9fe4ba59a850 / cbda5db96e88cc208f872c2237cf4741b8fcfaef
parent                                 7068884bd1982a99ea68647156addc5b381f9613
lib / focused-test blobs               d7b18acd7ea832acc73e94921b994fa1b341e006 / 5455121b2f0eafad09e031a66aa70178691c28fe
AU execution spec blob                 48e78daa50cb2724691fce09514d535a739f124f
AU clean-candidate CI                  32976370318/98201978533 SUCCESS
AU published-main CI                   32977973145/98207283247 SUCCESS
AS evidence head                       475650fea59332f74b9f69da50e3e4471622ab7e
AS artifact                            9603335255 / sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
AT contract                            sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
AT membership                          exact_tuple_only / 16 eight-field tuples / multiplicity 40
immutable mixed lane                   47 rows / false=7 / true=40
observed true-header tags              Int=40
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

R3.18AS and R3.18AT are immutable authorities. R3.18AV may not reselect witnesses, infer a larger tuple set, or inherit R3.18AJ/Z/P membership.

## Exact differential lane

For every exact frozen witness:

1. reconstruct the exact valid published prerequisites through R3.18AQ;
2. call published R3.18AU once;
3. require the returned embedded control to equal the exact recomputed AQ result;
4. on false, require `following_header == None` and AU stop equal AQ stop;
5. on true, require one header whose stream/property/tag/context coordinates and boundary equal frozen R3.18AS authority;
6. require every true header to be an exact R3.18AT member and exact context multiplicities to sum to 40;
7. require true AU stop equal the frozen header `payload_start`;
8. repeat and require bit-exact identical result;
9. stop without payload or later-control access.

Expected totals:

```text
rows                         47/47
false no-header              7
true exact header            40
exact AT contexts            16/16
AT multiplicity sum          40
tag distribution             Int=40
mismatch                     0
witness reselection          0
following payload            0 bits
second later control         0 bits
```

## Required negative controls

At minimum:
- false-row poison beginning at AQ/AU stop leaves the false terminator result unchanged;
- truncate a true row after AQ but inside its following header -> reject atomically;
- poison at true-row `payload_start` -> published AU header result unchanged;
- wrong actor object -> reject;
- unresolved lookup -> reject;
- wrong exact version/context -> reject;
- corrupt or mismatched published prerequisite -> reject;
- flip/drop `is_rl_223` -> reject unless the complete resulting tuple is independently an exact AT member;
- tag-only/component-only/Cartesian/versionless membership -> reject;
- AJ-valid but AT-absent tuple -> reject;
- fabricated seventeenth tuple -> reject;
- source-scope guard -> at most one following-header primitive, zero payload decoders, no generalized/repeated loop.

## Validation

Require:
- frozen witness identity 47/47;
- published AU exact 47/47;
- false=7 / true=40;
- true frozen header identity/boundary exact 40/40;
- exact AT context identity 16/16 and multiplicity sum 40;
- mismatch 0 and witness reselection 0;
- repeatability PASS;
- all negative controls PASS;
- following payload / second later control 0/0;
- focused AU regressions PASS;
- full mimir-replay/workspace fmt/check/test/clippy and repository verifier PASS;
- same-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy scan PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs. Reuse an existing exact run if present. Rerun is never polling.

## Hard stop

No following payload, no second later control, no context outside exact R3.18AT, no header on false terminators, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
Published R3.18AU matches all 47 immutable AS/AT witnesses exactly: false=7 no-header, true=40 exact header, exact contexts/multiplicity preserved, mismatch 0, witness reselection 0, all negative/full validations PASS, and following-payload/second-control consumption 0/0. A separate R3.18AW evidence pass may then inspect exactly one following payload on the exact forty true rows only.

### Outcome B
A bounded differential mismatch or narrower safe subset is isolated. Record only the exact supported subset and keep following-payload evidence closed.

### Outcome C
Authority/witness drift, false-terminator header access, true-header mismatch, AT membership widening, adjacent payload/later-control access, production mutation, generic chaining or privacy failure. Stop without widening.
