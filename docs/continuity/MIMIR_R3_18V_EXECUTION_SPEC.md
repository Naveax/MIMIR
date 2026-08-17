# MIMIR R3.18V — Next Property-Control Bit Evidence After Published R3.18T Payload

**Status:** ACTIVE
**Pass type:** read-only evidence / differential boundary characterization
**Production authority:** R3.18T `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b`
**Evidence authority:** R3.18U Outcome A
**Production mutation:** forbidden
**Next stream/header/payload:** forbidden
**Repeated/generalized property loop:** forbidden

## 1. Goal

On exactly the immutable 47 R3.18U witnesses, reconstruct the published R3.18T result through its proven following-payload end, then observe and differentially validate exactly one next `property_present` control bit starting at `R3.18T.stop_bit`. Stop exactly one bit later. This pass does not decode the next stream/header/payload and does not create a repeatable property cursor or loop.

## 2. Frozen authority

```text
canonical main before pass           continuity parent containing this spec
production SHA/tree                  c2765ab9f04f9c981a6868cb6503bdf0e339ce1b / a6f27fe606cd3446da02ef1cb8cf53fff071e383
production lib/test blobs            cf992670b461e9d923e773ed375bef2b42aea20d / 430676ec118fa0755a9c64abc0067bf5c5c88d05
R3.18U evidence head/tree            a53d0c8b4c88bab229e5ac9ec2db7dda5f9400b4 / f0c716278ef47665e43572d0129c4e8acd9be182
R3.18U run/job                       32055189778 / 95463604513 SUCCESS
R3.18U same-head CI                  32055189737 / 95463604366 SUCCESS
R3.18U artifact                      9296199852 / 20181 bytes / sha256:13262328812bc56c9ea58bbc42364308fb6c65487c51f062296b14993f3a626e
R3.18P contract SHA-256              0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
frozen source lane                   exact 47 R3.18U rows / 18 exact contexts
published payload classes            Boolean=39×1 bit / ActiveActor=8×33 bits
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh `main`, prove the production source/test blobs remain exact, verify every receipt and artifact digest above, verify the R3.18U manifest, and verify replay/witness identity hashes. Do not reselect witnesses based on the value of the next bit.

## 3. Exact source lane

Use exactly the same 47 R3.18U rows with zero reselection. Every row must first prove:

```text
published R3.18T result exact
embedded R3.18Q header exact
payload start/end/width/semantic exact
R3.18T stop_bit == frozen payload end
R3.18P exact context membership retained
```

Any row that no longer reproduces is authority drift and stops the pass. Do not replace it.

## 4. Differential observation

For every frozen row:

1. invoke the published R3.18T API and require exact R3.18U identity through `stop_bit`;
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
- mutate the prior R3.18T payload-end/stop relationship -> reject before observation;
- repeat identical observation -> exact identical result;
- poison bits beginning at the one-bit control end -> observed control unchanged;
- prove next stream/header/payload consumption counters remain zero;
- prove no second later control bit is read.

## 6. Evidence artifact

Produce one privacy-safe immutable artifact containing:

- exact main/production/lib/test/spec identities;
- R3.18U authority run/job/CI/artifact/digest and frozen identity hashes;
- pinned Boxcars SHA and observation-only instrumentation hash;
- all 47 privacy-safe row identities with prior T stop plus next-control start/value/end;
- full false/true distribution;
- deterministic and negative-control results;
- next stream/header/payload/another-control consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA-256 manifest for every artifact payload file.

Do not emit private raw payload windows or user-identifying replay metadata beyond the existing privacy-safe identity scheme.

## 7. Required validation

- 47/47 replay identities exact and witness reselection `0`;
- 47/47 published R3.18T reconstruction exact before observation;
- 47/47 pinned-oracle / independent-one-bit start/value/end exact;
- complete false/true distribution sums to 47;
- deterministic double-run equality;
- truncation, prior-stop mismatch and post-control poison negatives PASS;
- next stream/header/payload and second-later-control consumption `0/0/0/0`;
- focused R3.18T tests PASS;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS under Rust 1.85;
- repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18V may not resolve or decode the next stream ID, property object, attribute tag, payload boundary or payload. It may not read a second later control bit, build a generalized/repeated property loop/cursor, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen rows reproduce published R3.18T exactly and the one next `property_present` start/value/end matches pinned Boxcars with zero mismatch; all negatives/privacy/mutation gates pass. Record the observed false/true distribution. Only then may a separate bounded production pass be proposed for exactly this one control bit, with admission restricted to evidence-observed forms.

### Outcome B

A reproducible boundary mismatch exists. Record the exact privacy-safe row/bit coordinates and keep next-control production closed.

### Outcome C

Authority drift, witness reselection, production mutation, next stream/header/payload access, second-control or loop widening, privacy failure or validation contradiction. Stop without admission.
