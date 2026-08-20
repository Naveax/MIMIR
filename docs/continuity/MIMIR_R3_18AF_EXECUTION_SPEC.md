# MIMIR R3.18AF — Next Property-Control Bit Evidence After Published R3.18AD Payload

**Status:** ACTIVE
**Pass type:** read-only evidence / differential boundary characterization
**Production authority:** R3.18AD `ccadbf148381c007890d13d5fe8120866a0f40f9`
**Evidence authority:** R3.18AE Outcome A
**Production mutation:** forbidden
**Next stream/header/payload:** forbidden
**Repeated/generalized property loop:** forbidden

## 1. Goal

On exactly the immutable 47 R3.18AE witnesses, reconstruct the published R3.18AD result through its proven ordinal-3 payload end, then observe and differentially validate exactly one next `property_present` control bit starting at `R3.18AD.stop_bit`. Stop exactly one bit later. This pass does not decode the next stream/header/payload and does not create a repeatable property cursor or loop.

## 2. Frozen authority

```text
canonical main before pass           continuity parent containing this spec
production SHA/tree                  ccadbf148381c007890d13d5fe8120866a0f40f9 / 0882601060d0bb6d37fcc03ae7273dcf50dd0be3
production lib/test blobs            1254d5a3d16e7b97b1dee87a8b459514d25749ef / 013ad6da94b866ecaca94cd6420e7568d9b4b5ee
R3.18AE evidence head/tree           d72b20275f55c44b97d9ec516f2dffbff84a2d6a / a24b6360bf8cace5dfc6fb0ecec4e31f12c986b8
R3.18AE run/job                      32282584789 / 96164550815 SUCCESS
R3.18AE same-head CI                 32342929705 / 96345500068 SUCCESS
R3.18AE artifact                     9376466530 / 11057 bytes / sha256:0eacd0b43929699145a961825de2dbeb6b31342d1cacfa1c68c71cbdd9fc43f4
R3.18AC artifact                     9359697636 / sha256:a6914044dfd8991d74b95caeb3507fb2469175c4458c5b50b55395b8ea67b9df
R3.18Z contract SHA-256              81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
frozen source lane                   exact 47 R3.18AE rows
published payload classes            ActiveActor=39×33 / Int=7×32 / UniqueId=1×80 system1-Steam
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh `main`, prove the production source/test blobs remain exact, verify every receipt and artifact digest above, verify the R3.18AE manifest, and verify replay/witness identity hashes. Do not reselect witnesses based on the value of the next bit.

## 3. Exact source lane

Use exactly the same 47 R3.18AE rows with zero reselection. Every row must first prove:

```text
published R3.18AD result exact
embedded R3.18AA/R3.18Z header exact
payload start/end/width/semantic exact
R3.18AD stop_bit == frozen payload end
ActiveActor/Int/UniqueId admitted shape retained
```

Any row that no longer reproduces is authority drift and stops the pass. Do not replace it.

## 4. Differential observation

For every frozen row:

1. invoke the published R3.18AD API and require exact R3.18AE identity through `stop_bit`;
2. require `stop_bit` to equal the frozen payload end;
3. with observation-only pinned Boxcars instrumentation, identify the next property-loop `property_present` bit at that exact global bit offset;
4. independently read exactly one LSB-first bit at the same offset with evidence-only logic;
5. require exact start/value/end equality between the two observations;
6. record the boolean value without filtering either class;
7. stop exactly one bit later.

Report the full false/true distribution discovered on the 47 witnesses. No expected distribution is admitted in advance.

## 5. Required negative controls

At minimum:

- truncate exactly before the one next control bit -> explicit failure with no fabricated value;
- mutate the prior R3.18AD payload-end/stop relationship -> reject before observation;
- repeat identical observation -> exact identical result;
- poison bits beginning at the one-bit control end -> observed control unchanged;
- prove next stream/header/payload consumption counters remain zero;
- prove no second later control bit is read.

## 6. Evidence artifact

Produce one privacy-safe immutable artifact containing:

- exact main/production/lib/test/spec identities;
- R3.18AE authority run/job/CI/artifact/digest and frozen identity hashes;
- pinned Boxcars SHA and observation-only instrumentation hash;
- all 47 privacy-safe row identities with prior AD stop plus next-control start/value/end;
- full false/true distribution;
- deterministic and negative-control results;
- next stream/header/payload/another-control consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA-256 manifest for every artifact payload file.

Do not emit private raw payload windows or user-identifying replay metadata beyond the existing privacy-safe identity scheme.

## 7. Required validation

- 47/47 replay identities exact and witness reselection `0`;
- 47/47 published R3.18AD reconstruction exact before observation;
- 47/47 pinned-oracle / independent-one-bit start/value/end exact;
- complete false/true distribution sums to 47;
- deterministic double-run equality;
- truncation, prior-stop mismatch and post-control poison negatives PASS;
- next stream/header/payload and second-later-control consumption `0/0/0/0`;
- focused R3.18AD tests PASS;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS under Rust 1.85;
- repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18AF may not resolve or decode the next stream ID, property object, attribute tag, payload boundary or payload. It may not read a second later control bit, build a generalized/repeated property loop/cursor, admit alternate UniqueId layouts, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen rows reproduce published R3.18AD exactly and the one next `property_present` start/value/end matches pinned Boxcars with zero mismatch; all negatives/privacy/mutation gates pass. Record the observed false/true distribution. Only then may a separate bounded production pass be proposed for exactly this one control bit, with admission restricted to evidence-observed forms.

### Outcome B

A reproducible boundary mismatch exists. Record the exact privacy-safe row/bit coordinates and keep next-control production closed.

### Outcome C

Authority drift, witness reselection, production mutation, next stream/header/payload access, second-control or loop widening, privacy failure or validation contradiction. Stop without admission.
