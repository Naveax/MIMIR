# MIMIR R3.18L — Following-Property Control-Bit Evidence After One Published Second Payload

**Status:** ACTIVE  
**Pass type:** read-only evidence / differential boundary characterization  
**Production authority:** R3.18J `330ab01890a7c09eff1805e437584fb3be0a1134`  
**Evidence authority:** R3.18K Outcome A  
**Production mutation:** forbidden  
**Following stream/header/payload:** forbidden  
**Repeated/general property loop:** forbidden

## 1. Goal

On the exact 47 R3.18K continuation rows, first reconstruct the published R3.18J composition through the already-proven second-payload end, then observe and differentially validate exactly one following `property_present` control bit. Stop one bit later. This pass does not decode the following stream/header/payload and does not create a loop.

## 2. Frozen authority

```text
canonical main before pass          continuity parent containing this spec
production SHA/tree                 330ab01890a7c09eff1805e437584fb3be0a1134 / 5540b6a86e53d243dabbabea223a5afa8657521c
production lib blob                 ee9b0c71871df7ff52275581eb7ad4c023b8ba79
R3.18J focused test blob            c5a97c5a17ae2ea292790a020673dd26a0150024
R3.18J implementation               31975731621 / 95234808797 SUCCESS
R3.18J candidate CI                 31975907582 / 95235253244 SUCCESS
R3.18J published CI                 31976100231 / 95235742210 SUCCESS
R3.18K evidence head                926ddd88331ef0372b17b495cb06502010ab39ac
R3.18K run/job                      31977860600 / 95239932737 SUCCESS
R3.18K same-head CI                 31977860563 / 95239932564 SUCCESS
R3.18K artifact                     9271561853
R3.18K artifact digest              sha256:a455984c1149cb8f186eedb34d3e148fe45b8592c928cd9246d36cd52843262f
frozen source lane                  exact 47 R3.18K continuation rows
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh `main`, prove production source/test blobs remain exact, verify every receipt above and verify the replay/witness identity hashes. Do not reselect rows based on the value of the following bit.

## 3. Exact source lane

Use exactly the 47 R3.18K continuation rows. Each row already proves:

```text
first property reconstruction exact
second header exact
second payload exact
R3.18J stop == frozen second payload end
second tag distribution Int=46 / String=1
```

A row that no longer reproduces is authority drift and stops the pass. Do not replace it.

## 4. Differential observation

For every frozen row:

1. invoke the published R3.18J API and require its exact frozen result through `stop_bit`;
2. require `stop_bit == R3.18K payload_end_bit`;
3. with observation-only pinned Boxcars instrumentation, identify the next property-loop `property_present` bit at that exact global bit offset;
4. record its exact start, boolean value and end;
5. independently read exactly that one bit with evidence-only cursor logic and require exact value/end equality;
6. stop immediately after the bit.

Report the complete false/true distribution. Neither class may be dropped or preferred.

## 5. Negative controls

At minimum:

- truncate exactly before the following control bit -> explicit failure with no fabricated value;
- poison bits after the one-bit control end -> observed control result unchanged;
- repeat identical invocation -> byte-identical/equal evidence result;
- mutate the prior R3.18J stop/end relationship -> reject evidence row before following-bit observation;
- prove following stream/header/payload consumption counters remain zero.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing:

- exact main/production/source/test/spec identities;
- R3.18K authority run/job/artifact/digest and frozen replay/witness hashes;
- pinned Boxcars SHA plus observation-only instrumentation hash;
- all 47 row identities with prior R3.18J stop and following control start/value/end, but no raw private payload windows;
- false/true distribution;
- negative-control results;
- following stream/header/payload consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA-256 for every artifact file.

## 7. Required validation

- 47/47 replay identities exact;
- 47/47 published R3.18J reconstruction exact before observation;
- 47/47 oracle/evidence following-control start/value/end exact;
- deterministic double-run equality;
- R3.18J focused tests PASS;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS under Rust 1.85;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18L may not read or resolve the following stream ID, property object, attribute tag, payload start or payload. It may not read another control bit after the one observed here, create any repeated/generalized loop, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen continuation rows reproduce R3.18J exactly and the following `property_present` start/value/end matches pinned Boxcars with zero mismatch; negatives, privacy and mutation gates pass. Then define a separate bounded production pass for exactly this one after-second-payload control bit.

### Outcome B

A reproducible boundary mismatch appears. Record the exact privacy-safe row/bit coordinates and keep the following control production boundary closed.

### Outcome C

Authority drift, witness reselection, production mutation, following stream/header/payload access, loop widening, privacy failure or validation contradiction. Stop without admission.
