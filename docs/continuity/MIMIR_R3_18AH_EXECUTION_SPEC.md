# MIMIR R3.18AH — Published R3.18AG Post-AD True-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-API differential
**Production authority:** R3.18AG `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`
**Production tree:** `4123820ce6537f2d4942cd0b5f72b52e43b96c1d`
**Production mutation:** forbidden
**Next stream/header/payload:** forbidden
**Second later control:** forbidden

## 1. Goal

Validate the published R3.18AG true-only post-AD property-control API against exactly the immutable R3.18AF 47-row authority lane. Prove that published AG accepts the exact frozen R3.18AD prior boundary, reads only the frozen one control bit, returns the same start/value/end/stop, and consumes nothing adjacent.

## 2. Frozen authority

```text
production SHA/tree                 2d351e8ceb601e2fbe515d2977b2103a4b2c7976 / 4123820ce6537f2d4942cd0b5f72b52e43b96c1d
parent                              037a10a41848ca2621e1b64567c3c1bd7b2f6808
lib/test blobs                      db923ebcb419d278f4ab0144fe7ed15b298b60fa / 3f3e1c8f3f6deb7f2558862a1032f8a102131443
R3.18AG execution spec blob         90180dcaddd30ed9a187a0d4332a105d153488d7
R3.18AG builder                     32401660279 / 96531043622 SUCCESS
R3.18AG validation PR               #55 closed unmerged
R3.18AG PR CI                       32402596061 / 96534073576 SUCCESS
R3.18AG published-main CI           32402933798 / 96535174390 SUCCESS
R3.18AF evidence head/tree          30286c07727539d68f551140838fb2ef6802a26e / be808ad1ea757a095e37ccfe8f25b03e074dd732
R3.18AF authority                   32344981062 / 96351720877 SUCCESS
R3.18AF same-head CI                32345376481 / 96352906609 SUCCESS
R3.18AF artifact                    9397743505 / 12204 bytes / sha256:d7edeab657928c94c35c852ae302fd614cab92a52b7e44f671310200af4b268f
R3.18AF frozen rows                 47/47
R3.18AF control distribution        false=0 / true=47
R3.18AF native/oracle mismatch      0
R3.18AF adjacent consumption        stream/header/payload/second-control = 0/0/0/0
```

Any production-source, witness, artifact or receipt drift stops the pass. Witness reselection is forbidden.

## 3. Exact lane and comparison

Reuse exactly the 47 R3.18AF witnesses. For every row:

1. reconstruct the exact valid published R3.18AD prior through its frozen payload-end `stop_bit`;
2. call the published R3.18AG API once under exact `868.32 / net10 / non-RL223` context;
3. require AG `property_present_start_bit` == frozen AF control start == prior AD stop;
4. require AG value `true` == frozen AF value;
5. require AG end and final stop == frozen AF control end == start + 1;
6. repeat the invocation and require exact identical result;
7. stop. Do not resolve/read the next stream/header/payload or a second later control.

The expected immutable distribution is `true=47 / false=0`. This is not permission to widen false into success.

## 4. Required negative controls

At minimum:

- truncate exactly before the AG control bit -> reject atomically;
- flip the observed control bit to false -> explicit `unadmitted-false-control` rejection;
- use a wrong K3 context -> reject before control success;
- corrupt prior AD payload-end/stop or nested header/payload consistency -> reject before success;
- forge an unadmitted prior tag/width or UniqueId layout -> reject before success;
- repeat identical invocation -> exact equality;
- poison bits beginning at AG stop -> returned one-bit result unchanged;
- prove next stream/header/payload/second-control consumption remains `0/0/0/0`.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact AG production/source/test/CI authorities, exact AF evidence/artifact identities, frozen replay/witness identity, per-row published-AG versus frozen-AF comparison, negative results, aggregate counters, mutation counters and a SHA-256 manifest for every evidence payload file.

No private raw payload windows or user-identifying replay metadata may be emitted beyond the existing privacy-safe identity scheme.

## 6. Validation

Require:

- exact 47/47 frozen identities and witness reselection `0`;
- published AG versus frozen AF mismatch `0`;
- prior published AD reconstruction exact `47/47`;
- control false `0`, true `47`;
- start/value/end/stop equality `47/47`;
- deterministic double-run equality;
- truncation/false/wrong-context/prior-boundary/unadmitted-shape/post-stop-poison negatives PASS;
- next stream/header/payload/second-control consumption `0/0/0/0`;
- focused R3.18AG tests PASS;
- full `mimir-replay`, workspace fmt/check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`;
- privacy scan PASS.

## 7. Hard stop

R3.18AH may not mutate production, decode the next stream/header/payload, read a second later control bit, generalize into a property loop/cursor, iterate another actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 8. Outcome gate

### Outcome A
Published R3.18AG is exact on all 47 frozen R3.18AF rows with mismatch 0 and all negative/mutation/privacy gates pass. Admit only the published differential. Then a separate R3.18AI read-only pass may investigate exactly one following property header beginning at the R3.18AG stop and must stop at that header's payload start.

### Outcome B
A bounded mismatch is isolated. Admit only supported facts and keep the next-header boundary closed.

### Outcome C
Authority/witness drift, production mutation, privacy failure, false-context widening, next-header/payload access or second-control access. Stop without widening.
