# MIMIR R3.18BR — Next Property-Control Bit Evidence After Exact BQ Payload End

**Status:** ACTIVE
**Pass type:** read-only exactly-one-control-bit differential evidence
**Production authority:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`
**Direct payload authority:** R3.18BQ Outcome A artifact `10144392560` / `sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c`
**Pinned oracle:** Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`
**Production mutation:** forbidden
**Next stream/header/payload:** forbidden
**Second later property-control bit:** forbidden
**Repeated/generalized property loop:** forbidden

## 1. Goal

On exactly the two immutable R3.18BQ payload rows, reconstruct the current R3.18BO/R3.18BP prerequisite and exact BQ payload through its proven `payload_end_bit`, require the native cursor to equal that end, then observe and differentially validate exactly one next `property_present` bit at the same bit offset. Stop exactly one bit later.

The one R3.18BP false terminator remains outside the BR lane. The BR false/true distribution is an output and must not be guessed or inherited from R3.18BH, R3.18AX, R3.18V, or any older ordinal.

## 2. Frozen authority

```text
continuity base before BQ admission       e9028143f2bca342c58d88d9302d8e10702c6798 / 9d636c7fe2c150ecec1c1d25b2b8a7441789fd03
production SHA/tree                       cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
BQ evidence head/tree                     16c43f38e740c57ae9cb90c92084002ec83815e7 / 58248877a59fb0ddad707e32f92b2cec91f6b434
BQ run/job                                34457725716/102807933610 SUCCESS
BQ same-head CI                           34457725700/102808516101 SUCCESS / count 1
BQ artifact                               10144392560 / 9464 bytes / sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c
BQ inner manifest SHA-256                 332447c57f92f6f9af84e12bf74124adfe478d225e82cdb5d4cf8e925f7a97c9
BQ rows                                   BP=3 / false excluded=1 / true payloads=2
BQ payload classes                        Boolean=1x1 bit / ActiveActor=1x33 bits
BQ native/oracle mismatch                 0
BQ witness reselection                    0
pinned Boxcars                            c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh main and verify the exact continuity parent containing this spec, production identities, BQ run/job/CI/artifact digest plus downloaded inner manifest, and both replay/witness identities. Never reselect rows based on the next bit value.

## 3. Exact source lane

Use exactly the same two BQ payload rows with zero reselection. Each row must first prove the published R3.18BO header prerequisite, admitted R3.18BP row identity, and R3.18BQ tag/value/start/end/width. The BP false terminator is excluded before BR entry. Any authority drift stops the pass; do not replace a row.

## 4. Allowed read

```text
start = exact BQ payload_end_bit
read exactly one property_present bit
end = start + 1
```

For each frozen row, independently observe the bit with evidence-only native logic and pinned Boxcars, require exact start/value/end equality, record the boolean without filtering either class, then stop one bit later.

## 5. Required assertions and negatives

- target BQ payload rows exact 2/2; BP false terminator excluded 1/1;
- BQ payload reconstruction exact before control observation;
- native/oracle one-bit start/value/end exact 2/2;
- false + true distribution sums to 2 with no inherited expected ratio;
- witness reselection 0;
- truncation before the bit fails explicitly;
- mutated prior payload-end relation rejects before observation;
- corrupt BO/BP/BQ prerequisite rejects;
- repeated observation is identical;
- poison beginning at control end leaves result unchanged;
- wrong replay/actor/context rejects;
- next stream/header/payload/second-control consumption `0/0/0/0`;
- BP-false payload/control access `0/0`;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

Historical control values, distributions, and coordinates are not authority.

## 6. Evidence artifact and validation

Produce one privacy-safe immutable artifact with exact authority receipts, downloaded BQ manifest verification, pinned Boxcars plus instrumentation hash, both BR rows, complete observed distribution, negative controls, zero-consumption counters, mutation/privacy results, unique same-head CI receipt, and inner SHA-256 manifest. Require focused BR tests, workspace fmt/check/test/clippy under Rust 1.85, repository verifier, diff-check, privacy PASS, unique same-head natural CI SUCCESS, and artifact receipt verification. Reuse equivalent queued/waiting/in-progress exact-SHA runs; rerun is not polling.

## 7. Hard stop

BR may not resolve/decode the next stream ID, property object, attribute header or payload; read a second later control; build a generalized/repeated property loop; iterate actor/frame; mutate lifecycle state; materialize raw state/events; slice replays; mine skills; run counterfactuals; or widen runtime/export behavior.

## 8. Outcome gate

### Outcome A
Both immutable BQ payload rows reproduce exactly and the one next `property_present` start/value/end matches pinned Boxcars with zero mismatch; all negative/privacy/mutation gates pass. Record the observed false/true distribution. Only then may a separate bounded production or next-boundary pass be proposed from the observed semantics.

### Outcome B
A reproducible boundary mismatch exists. Record exact privacy-safe row/bit coordinates and keep the control boundary closed.

### Outcome C
Authority drift, reselection, BP-false access, production mutation, adjacent read widening, privacy failure or validation contradiction. Stop without admission.
