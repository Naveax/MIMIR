# MIMIR R3.18BL — Published R3.18BK Mixed Next-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BK `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`
**Production mutation:** forbidden
**Control authority:** immutable R3.18BH artifact `10023482583`
**Witness reselection:** forbidden

## 1. Goal

Validate published R3.18BK against exactly the three immutable R3.18BH control rows. Prove that published BK reconstructs the exact published BI prerequisite, starts at the frozen BH control start, returns the exact frozen boolean, ends/stops exactly one bit later, and consumes nothing adjacent.

The immutable distribution is **false=1 / true=2**. Both boolean classes are successful published BK results. BL itself must not decode a following stream ID, property header, payload or second later control.

## 2. Frozen authority

```text
production SHA/tree                  f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf / 07656c7a43c1afb97903ef33c1109b764fbf8b7d
production parent                    de8df0b2bb36454c97863d4078ce7829fd4ecb77
lib/test blobs                       0bfff19a7d285e07508b648dbcd5af95a31838f6 / 1938707e60f7893768747931bf84e3bbac792d1b
BK execution spec blob               12d3c92db43433871deaf2d86889b770bfd4af3d
BK builder                           34211911298/102014640422 SUCCESS
BK validation PR                     #216 closed unmerged
BK exact-head PR CI                  34212312983/102015924320 SUCCESS
BK published-main CI                 34212774993/102017408925 SUCCESS
BH artifact                          10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH manifest                          sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
BH rows                              3
BH distribution                      false=1 / true=2
BE false terminators                 37
upstream AU false terminators        7
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

Exact BH rows:

```text
external_fixtures/sample_002.replay                                      11231 -> 11232  true
external_fixtures/sample_003.replay                                       7815 -> 7816   false
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay 3198 -> 3199   true
```

No filename/hash/path is a production support predicate. These identities are frozen differential witnesses only.

## 3. Exact differential lane

For each exact BH authority row:

1. reconstruct all published prerequisites through R3.18BI;
2. call published R3.18BK exactly once;
3. require BK embedded BI composition to equal the independently recomputed published BI result;
4. require `property_present_start_bit == BI.stop_bit == frozen BH control_start_bit`;
5. require BK boolean == frozen BH boolean;
6. require `property_present_end_bit == stop_bit == frozen BH control_end_bit == start + 1`;
7. repeat and require exact identical output;
8. poison bits beginning at BK stop and require the BK result unchanged;
9. stop without reading any following structure.

Expected totals:

```text
published BK exact                   3/3
published BI prerequisite            3/3
false / true                         1 / 2
boundary/value mismatch              0
witness reselection                  0
BE false excluded                    37/37
upstream AU false excluded           7/7
following stream/header/payload      0/0/0 bits
second later control                 0 bits
production mutation                  0
```

## 4. Required negative controls

At minimum:
- truncate exactly before the BK control bit -> reject atomically;
- corrupt/mismatch the supplied BI prior -> reject;
- wrong actor authority -> reject before BK control success;
- unresolved lookup -> reject before BK control success;
- wrong exact context -> reject;
- repeat identical invocation -> exact equality;
- poison bits beginning at BK stop -> returned one-bit result unchanged;
- all 37 BE-false terminators remain outside BK success;
- all 7 upstream AU-false terminators remain outside BK success;
- source-scope guard -> one published BI recomputation plus one control read, no generic loop/header/payload decode.

Because both booleans are admitted, flipping a frozen control bit is not an API-malformed negative. If used as a differential mutation, report it as frozen-value mismatch rather than expected API rejection.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing:
- exact BK SHA/tree/lib/test/spec identities and CI receipts;
- exact BH artifact/digest/manifest authority;
- the three frozen witness identities and 37+7 negative-lane counts;
- per-row published-BK versus frozen-BH and independently recomputed published-BI comparison;
- exact boolean/start/end/stop summaries;
- repeatability and required negative-control results;
- adjacent-consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- same-head normal-CI receipt;
- privacy result and SHA-256 inner manifest.

## 6. Validation

Require exact witness identity 3/3; published BK exact 3/3; published BI prerequisite exact 3/3; false=1 / true=2; mismatch/reselection 0/0; repeatability PASS; all negatives PASS; 37 BE-false rejected/excluded and 7 AU-false excluded; following stream/header/payload/second-control consumption 0/0/0/0; focused BK regressions PASS; full `mimir-replay` plus workspace fmt/check/test/clippy and repository verifier PASS; same-head normal CI SUCCESS with no duplicate equivalent run; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy scan PASS.

Before dispatch or rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## 7. Continuation classification

The frozen boolean controls continuation:
- the exact one false row is a terminator and must stop after BK;
- the exact two true rows are continuation candidates.

BL does not decode any following header. Only if BL closes Outcome A may a separate later pass investigate exactly one following property header on the exact two true rows, stopping at that header's payload start.

## 8. Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening, and no production mutation.

## 9. Outcome gate

### Outcome A
Published R3.18BK is exact on all three immutable BH witnesses with false=1 / true=2, published BI prerequisite exact 3/3, mismatch/reselection 0/0, all negative/full validations PASS and adjacent consumption 0/0/0/0. A later separate read-only pass may investigate one following header on exactly the two true continuation rows.

### Outcome B
A bounded mismatch or narrower supported subset is isolated. Admit only supported facts and keep following-header evidence closed.

### Outcome C
Authority/witness drift, published mismatch, rejection of a BH-admitted boolean class, adjacent access, production mutation, privacy failure or generic chaining. Stop without widening.
