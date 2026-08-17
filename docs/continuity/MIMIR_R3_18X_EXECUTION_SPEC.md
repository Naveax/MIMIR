# MIMIR R3.18X — Published R3.18W After-Following-Payload Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-API differential
**Production authority:** R3.18W `58872e94f00ef094807f21ab2ff984ac66b97d91`
**Production tree:** `d6965d77903ea99dad0465bb350b6a673ee7dd00`
**Production mutation:** forbidden
**Next stream/header/payload:** forbidden
**Second later control:** forbidden

## 1. Goal

Validate the published R3.18W true-only after-following-payload control API against exactly the immutable R3.18V 47-row authority lane. Prove that published W reconstructs the exact prior R3.18T payload boundary, reads only the frozen one control bit, returns the same start/value/end/stop, and consumes nothing adjacent.

## 2. Frozen authority

```text
production SHA/tree                 58872e94f00ef094807f21ab2ff984ac66b97d91 / d6965d77903ea99dad0465bb350b6a673ee7dd00
lib/test blobs                      d997ae8c3ad2d201b3f43c6ccca7ded2ef03b73b / ac176135c2e6ed56f0b91bdde8c7548f17641cf0
R3.18W implementation authority     32060501395 / 95480474127 SUCCESS
R3.18W candidate CI                 32062120856 / 95485540552 SUCCESS
R3.18W PR CI                        32062533181 / 95486877308 SUCCESS
R3.18W published CI                 32062965119 / 95488256583 SUCCESS
R3.18V evidence head/tree           2b0c9f01559e77a6fdf21a097b8ab4d1a27b6ff5 / 229b3d68a82f6dadc19518614e27ff09e8006ad2
R3.18V authority                    32057732310 / 95471639989 SUCCESS
R3.18V same-head CI                 32057732335 / 95471640230 SUCCESS
R3.18V artifact                     9297068554 / 20484 bytes / sha256:e17426aad6d476eba17bb471dc92cd24b4b4d8727ad427ad15fa6e9c1dda9eb2
R3.18V Boxcars instrumentation      198096b6693c91cc146aae10fb0a5d3729dd778b7038e3915ede59fd246032b3
R3.18V frozen rows                  47/47
R3.18V control distribution         false=0 / true=47
R3.18V native/oracle mismatch       0
R3.18V adjacent consumption         stream/header/payload/second-control = 0/0/0/0
```

Any production-source, witness, artifact or receipt drift stops the pass. Witness reselection is forbidden.

## 3. Exact lane and comparison

Reuse exactly the 47 R3.18V witnesses. For every row:

1. reconstruct the exact valid published R3.18T prior result through its frozen payload-end `stop_bit`;
2. call the published R3.18W API once;
3. require W `property_present_start_bit` == frozen V control start == prior T stop;
4. require W value `true` == frozen V value;
5. require W end and final stop == frozen V control end == start + 1;
6. repeat the invocation and require exact identical result;
7. stop. Do not resolve/read the next stream/header/payload or a second later control.

The expected immutable distribution is `true=47 / false=0`. This is not permission to widen false into success.

## 4. Required negative controls

At minimum:

- truncate exactly before the W control bit -> reject atomically;
- flip the observed control bit to false -> explicit `unadmitted-false-control` rejection;
- corrupt prior T payload-end/stop or nested header/payload consistency -> reject before success;
- repeat identical invocation -> exact equality;
- poison bits beginning at W stop -> returned one-bit result unchanged;
- prove next stream/header/payload/second-control consumption remains `0/0/0/0`.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact W production/source/test/CI authorities, exact V evidence/artifact identities, frozen replay/witness identity, per-row published-W versus frozen-V comparison, negative results, aggregate counters, mutation counters and a SHA-256 manifest for every evidence payload file.

No private raw payload windows or user-identifying replay metadata may be emitted beyond the existing privacy-safe identity scheme.

## 6. Validation

Require:

- exact 47/47 frozen identities and witness reselection `0`;
- published W versus frozen V mismatch `0`;
- prior published T reconstruction exact `47/47`;
- control false `0`, true `47`;
- start/value/end/stop equality `47/47`;
- deterministic double-run equality;
- truncation/false/prior-boundary/post-stop-poison negatives PASS;
- next stream/header/payload/second-control consumption `0/0/0/0`;
- focused R3.18W tests PASS;
- full `mimir-replay`, workspace check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`;
- privacy scan PASS.

## 7. Hard stop

R3.18X may not mutate production, decode the next stream/header/payload, read a second later control bit, generalize into a property loop/cursor, iterate another actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 8. Outcome gate

### Outcome A
Published R3.18W is exact on all 47 frozen R3.18V rows with mismatch 0 and all negative/mutation/privacy gates pass. Admit only the published differential. Then a separate R3.18Y read-only pass may investigate exactly one following property header beginning at the R3.18W stop and must stop at that header's payload start.

### Outcome B
A bounded mismatch is isolated. Admit only supported facts and keep the next-header boundary closed.

### Outcome C
Authority/witness drift, production mutation, privacy failure, false-context widening, next-header/payload access or second-control access. Stop without widening.
