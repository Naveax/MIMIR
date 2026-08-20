# MIMIR R3.18AI — One Following Property-Header Evidence After Published R3.18AG

**Status:** ACTIVE
**Pass type:** read-only structural evidence
**Production authority:** R3.18AG `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`
**Production tree:** `4123820ce6537f2d4942cd0b5f72b52e43b96c1d`
**Production mutation:** forbidden
**Following payload:** forbidden
**Second later control:** forbidden

## 1. Goal

On exactly the immutable 47 R3.18AH/R3.18AF witnesses, reconstruct the valid published R3.18AG one-bit control result, begin at its exact `stop_bit`, decode exactly one following property header with the existing stateless header machinery, record the exact structural result, and stop at that header's `payload_start`.

This pass is evidence-only. It does not create production composition, a chainable cursor or a generalized property loop.

## 2. Frozen authority

```text
canonical admission parent           0e48eebffbd7f54238835e23c177e732cbeb7978 / 627d02ca39ff732e9dd7137d061432c6a67fafd8
production SHA/tree                  2d351e8ceb601e2fbe515d2977b2103a4b2c7976 / 4123820ce6537f2d4942cd0b5f72b52e43b96c1d
production lib/test blobs            db923ebcb419d278f4ab0144fe7ed15b298b60fa / 3f3e1c8f3f6deb7f2558862a1032f8a102131443
R3.18AG execution spec blob          90180dcaddd30ed9a187a0d4332a105d153488d7
R3.18AH execution spec blob          94aec628115f43db549ffec2d52338372a6a7459
R3.18AH evidence head/tree           7389831c626c078d60178c94461ac39e5f427bd5 / 6121bd7d0fab5a5a338a75343d92f11876f71c8b
R3.18AH authority                    32405516670 / 96543562860 SUCCESS
R3.18AH same-head CI                 32406901661 / 96547992406 SUCCESS
R3.18AH artifact                     9420166543 / 11686 bytes / sha256:b7b9100489a7ae20a959450d0d80fbcda281aee288a00d0c7edd18930cc60df1
R3.18AH rows                         47/47
R3.18AH distribution                 false=0 / true=47
R3.18AH mismatch                     0
R3.18AH adjacent consumption         stream/header/payload/second-control = 0/0/0/0
```

Witness reselection is forbidden. Any production/source/artifact/identity drift stops the pass.

## 3. Exact read-only lane

For every one of the 47 frozen witnesses:

1. reconstruct the exact valid published R3.18AD prior through payload end;
2. invoke published R3.18AG under exact `868.32 / net10 / non-RL223` context and require the frozen AH one-bit result;
3. require following-header start == AG `stop_bit`;
4. decode exactly one existing-actor property header using the existing stateless property-header primitive and frozen lookup plan authority;
5. record the exact header start, stream id, resolved object/property identity, resolved attribute tag, payload start and final header stop;
6. require final header stop == payload start;
7. stop. Do not decode any payload bit or read another property-control bit.

Any observed header-context distribution is evidence only. Do not generalize it into a production allowlist in this pass.

## 4. Required negative controls

At minimum:

- truncate within the one header before its exact `payload_start` -> reject atomically;
- wrong K3/replay context -> reject before admitted success where context is required by the reconstructed prior;
- corrupt the prior R3.18AG start/end/stop or true-control invariant -> reject before header success;
- unresolved/incorrect stream or property lookup context -> reject;
- wrong actor/object lookup context -> reject;
- poison bits beginning at the header `payload_start` -> returned header result unchanged;
- repeat identical invocation -> exact equality;
- prove following payload and second-later-control consumption remain `0/0`.

## 5. Independent comparison

Use the pinned Boxcars oracle and/or an independent evidence-only structural observer to cross-check the exact one-header start/end and resolved structural identity for all 47 frozen witnesses. Any mismatch is Outcome B/C material and must not be hidden by witness reselection.

## 6. Evidence artifact

Produce one privacy-safe immutable artifact containing:

- exact production/source/test/spec/CI authorities;
- exact AH evidence/artifact identities;
- exact frozen replay/witness identities;
- per-row reconstructed AG stop and following-header structural result;
- independent/oracle comparison;
- negative-control results;
- aggregate context counts and mismatch counters;
- mutation/privacy counters;
- SHA-256 manifest covering every artifact payload file.

Do not emit private raw payload windows or user-identifying replay metadata beyond the existing privacy-safe identity scheme.

## 7. Validation

Require:

- exact 47/47 witness identities and witness reselection `0`;
- published AG reconstruction exact 47/47;
- one following header exact 47/47 or a precisely isolated bounded mismatch;
- deterministic double-run equality;
- header truncation/prior corruption/unresolved lookup/wrong actor-context/post-payload-start poison negatives PASS;
- following payload bits consumed `0`;
- second later control bits consumed `0`;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`;
- privacy scan PASS;
- relevant focused suites plus full `mimir-replay`, workspace fmt/check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS.

## 8. Hard stop

R3.18AI may not mutate production, decode the following payload, read a second later control bit, create a generalized property loop/cursor, iterate another actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A
One following header is exact on all 47 frozen witnesses with mismatch 0 and all negative/mutation/privacy gates pass. Admit only the observed structural header facts. Any exact-context contract or production composition requires a later separate pass.

### Outcome B
A bounded header mismatch or multiple structural families are isolated. Admit only supported read-only facts and keep production/following payload closed.

### Outcome C
Authority/witness drift, production mutation, privacy failure, payload access, second-control access or unbounded lookup/context ambiguity. Stop without widening.
