# MIMIR R3.18AP — Next Property-Control Bit Evidence After Published R3.18AN Payload

**Status:** ACTIVE
**Pass type:** read-only evidence / differential boundary characterization
**Production authority:** R3.18AN `3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38` / `3efcc244bca55623b12bb21eb277753fc61144d4`
**Evidence authority:** R3.18AO Outcome A / `0f5ecb5b1dccf35aaabf6a45645bc70ad8a68a1c`
**Production mutation:** forbidden
**Next stream/header/payload:** forbidden
**Second later property-control bit:** forbidden
**Repeated/generalized property loop:** forbidden

## 1. Goal

On exactly the immutable 47 R3.18AO witnesses, first reconstruct the published R3.18AN composition through its proven `Int/32` payload end, then observe and differentially validate exactly one next `property_present` bit beginning at `R3.18AN.stop_bit`. Stop exactly one bit later.

R3.18AP does not resolve or decode the following stream ID, property header or payload and does not build a repeatable property cursor/loop.

## 2. Frozen authority

```text
canonical main before AP            continuity parent containing this spec
production SHA/tree                 3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38 / 3efcc244bca55623b12bb21eb277753fc61144d4
production lib/test blobs           9d6b5ae2898cee745a17de9d1d7ef4b8fbd0e822 / 8aa48b2b74d0956d1d2e965d056e1cf14a81f703
R3.18AO evidence head/tree          0f5ecb5b1dccf35aaabf6a45645bc70ad8a68a1c / 59126fe2757ecc500a5cc6f822d76fbc380ef85b
R3.18AO run/job                     32734420624/97453768432 SUCCESS
R3.18AO same-head CI                32734946566/97455429462 SUCCESS
R3.18AO artifact                    9522750814 / 4619 bytes / sha256:2e34f3be6963b2b6031a395e85e9699b64df7413d62dd9809fa8fd9794547d73
frozen source lane                  exact 47 R3.18AO rows
published payload identity          Int=47 / width32=47 / semantic range 1..415
published/native/oracle mismatch    0
witness reselection                 0
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh `main`, verify the exact production source/test blobs, AO run/CI/artifact digest and manifest, and replay/witness identities. Do not reselect witnesses based on the value of the next bit.

## 3. Exact source lane

Use exactly the same 47 R3.18AO rows with zero reselection. Each row must first prove:

```text
published R3.18AN result exact
embedded R3.18AK/R3.18AJ header exact
payload tag/start/end/width/value exact
R3.18AN stop_bit == frozen payload end
```

Any row that no longer reproduces is authority drift and stops the pass. It must not be replaced.

## 4. Differential observation

For every frozen row:

1. invoke published R3.18AN and require exact R3.18AO identity through `stop_bit`;
2. require `stop_bit == frozen payload_end_bit`;
3. with observation-only pinned Boxcars instrumentation, identify exactly the next property-loop `property_present` bit at that same global bit offset;
4. independently read exactly one LSB-first bit at the same offset with evidence-only logic;
5. require exact start/value/end equality between oracle and independent observation;
6. record the boolean value without filtering either class;
7. stop exactly one bit later.

Report the complete false/true distribution discovered on the 47 witnesses. No expected distribution is admitted in advance.

## 5. Required negative controls

At minimum:

- truncate exactly before the one next control bit -> explicit failure with no fabricated value;
- mutate the prior R3.18AN payload-end/stop relationship -> reject before observation;
- repeat identical observation -> exact identical result;
- poison bits beginning at the one-bit control end -> observed control unchanged;
- require the prerequisite published AN reconstruction and AO identity before observation;
- prove next stream/header/payload and second later control consumption remain `0/0/0/0`.

## 6. Evidence artifact

Produce one privacy-safe immutable artifact containing exact main/production/lib/test/AP-spec identities; complete R3.18AO authority receipts and hashes; pinned Boxcars SHA plus observation instrumentation hash; all 47 privacy-safe next-control rows; full false/true distribution; negatives; zero-consumption counters; mutation counters; privacy result; and a SHA-256 manifest.

## 7. Required validation

- 47/47 replay/witness identities exact; witness reselection 0;
- 47/47 published R3.18AN reconstruction exact before observation;
- 47/47 pinned-oracle versus independent one-bit start/value/end exact;
- false + true distribution sums to 47;
- deterministic repeatability PASS;
- truncation, prior-stop mismatch and post-control poison negatives PASS;
- next stream/header/payload/second-control consumption `0/0/0/0`;
- focused R3.18AN regressions PASS;
- full `mimir-replay` PASS;
- workspace format/check/test/clippy PASS under the repository Rust floor;
- repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18AP may not resolve/decode the next stream ID, property object, attribute tag, header or payload. It may not read a second later control bit, create a generalized/repeated property loop/cursor, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen rows reproduce published R3.18AN exactly and the one next `property_present` start/value/end matches pinned Boxcars with zero mismatch; all negatives/privacy/mutation gates pass. Record the observed false/true distribution. Only then may a separate bounded production pass be proposed for exactly the observed control semantics.

### Outcome B

A reproducible next-control boundary mismatch exists. Record exact privacy-safe row/bit coordinates and keep next-control production closed.

### Outcome C

Authority drift, witness reselection, production mutation, next stream/header/payload access, second-control/loop widening, privacy failure or validation contradiction. Stop without admission.
