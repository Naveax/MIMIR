# MIMIR R3.18BB — Published R3.18BA Mixed Following-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production mutation:** forbidden
**Frozen control authority:** R3.18AX `465a3f2fc71e5eed6f00c16a04738031bef8d82c` / run `33068572230/98504703417` / artifact `9644869549` / `sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9`
**Following stream/header/payload:** forbidden
**Second later control:** forbidden

## 1. Goal

Differentially validate published R3.18BA against exactly the immutable forty-row R3.18AX one-bit authority. For each frozen witness, reconstruct the exact valid R3.18AY prerequisite, invoke published BA once, and require exact control start, boolean value, end and final stop equality with AX plus an independent native LSB-first observation.

The immutable distribution is **false=37 / true=3**. Both classes are valid BA results. The 37 false rows terminate after BA. The 3 true rows are continuation candidates only; BB itself does not decode a following header.

## 2. Frozen authority

```text
BA production SHA/tree                5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BA parent                              109bad258d43963fd5432317503f99a7e1b8aa1b
BA lib/test blobs                      fe232760e63c3c1b46711084c70049f456ef345b / 41ef1c2c087cc52bf2bcf0fa65c911a31a6ffc13
BA execution spec blob                 3db94f3d559de1a7152a55fa08f7cb4b50d50d74
BA builder                             33091339939/98584661482 SUCCESS
BA validation PR                      #208 closed unmerged
BA PR CI                              33091594385/98585555551 SUCCESS
BA candidate push CI                  33091611038/98585614713 SUCCESS
BA published-main CI                  33092084628/98587299347 SUCCESS
AX evidence head                      465a3f2fc71e5eed6f00c16a04738031bef8d82c
AX authority run/job                  33068572230/98504703417 SUCCESS
AX artifact                           9644869549 / 18070 bytes
AX artifact digest                    sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
AX inner manifest                     15/15 PASS
AX frozen rows                        40
AX distribution                       false=37 / true=3
AX mismatch/reselection               0 / 0
AX adjacent consumption               0/0/0/0
```

Witness reselection is forbidden. Historical AP/AQ or true-only M/W/AG ratios are not authority for this boundary.

## 3. Exact differential lane

For every exact R3.18AX witness:

1. reconstruct the same exact valid published R3.18AY prerequisite;
2. call published R3.18BA exactly once;
3. require BA retained payload composition == reconstructed AY authority;
4. require BA `property_present_start_bit == AY.stop_bit == AX control_start`;
5. require BA boolean == frozen AX boolean == independent native LSB-first observation;
6. require BA `property_present_end_bit == stop_bit == AX control_end == start + 1`;
7. repeat and require exact deterministic equality;
8. poison bits beginning at BA stop and require the BA result unchanged;
9. stop without following stream/header/payload or second-control access.

Expected totals:

```text
frozen rows             40/40
published BA exact      40/40
AY prerequisite exact   40/40
false                    37
true                      3
mismatch                  0
witness reselection       0
adjacent consumption      0/0/0/0
```

## 4. Required negative controls

At minimum:
- all seven upstream AU false terminators remain outside AY/BA and reject before BA control success;
- wrong actor authority -> reject before BA success;
- unresolved lookup -> reject before BA success;
- wrong exact context -> reject;
- corrupt/mismatched AY prior -> reject;
- truncated prerequisite/carrier -> fail closed;
- repeat identical invocation -> exact equality 40/40;
- poison at exact BA stop -> returned BA result unchanged 40/40;
- source-scope guard -> one AY recomputation, one `cursor.read_bit()`, no stream/header/payload decoder and no loop/cursor widening;
- next stream/header/payload/second-control consumption remains 0/0/0/0.

Because both booleans are admitted, flipping a frozen control bit is not an API-malformed negative. If used as a differential mutation it is a frozen-value mismatch, not an expected parser rejection.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact BA SHA/tree/blob/CI receipts, exact AX authority and manifest receipt, forty frozen witness identities, per-row AY/BA/AX/native comparison, repeatability and negative controls, adjacent-consumption counters, production/Cargo/fixture/corpus/support mutation counters, same-head natural-CI receipt, privacy result and SHA-256 manifest.

## 6. Validation

Require frozen identity 40/40, published BA exact 40/40, AY prerequisite exact 40/40, false=37 / true=3, mismatch/reselection 0/0, repeatability and all negatives PASS, adjacent 0/0/0/0, focused BA/prerequisite tests PASS, Rust 1.85 fmt/check/test/clippy with warnings denied, repository verifier PASS, same exact evidence-head natural CI SUCCESS, production/Cargo/fixture/corpus/support mutation 0/0/0/0/0 and privacy PASS.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling. At most one validation-only PR may be used if a natural same-head CI cannot otherwise be obtained.

## 7. Continuation classification

- exact 37 false rows: terminators at BA stop;
- exact 3 true rows: continuation candidates only.

The three AX-observed true witness identities are frozen by the AX artifact. BB does not reinterpret or reselect them.

## 8. Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 9. Outcome gate

### Outcome A
Published R3.18BA is exact on all forty immutable AX witnesses with false=37 / true=3, mismatch/reselection 0/0, all negative/full validations PASS and adjacent consumption 0/0/0/0. Only then may a separate later pass inspect exactly one following header on the exact three true rows.

### Outcome B
A reproducible bounded mismatch or narrower supported subset is isolated. Admit only that subset and keep following-header evidence closed.

### Outcome C
Authority drift, witness reselection, rejection of an AX-admitted boolean class, upstream false-terminator widening, adjacent access, production mutation, privacy failure or generic chaining. Stop without widening.
