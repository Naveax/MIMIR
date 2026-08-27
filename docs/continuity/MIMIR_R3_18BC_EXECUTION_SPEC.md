# MIMIR R3.18BC — One Following-Property-Header Evidence After Published R3.18BA Mixed Control

**Status:** ACTIVE
**Pass type:** read-only boundary evidence
**Production authority:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Differential authority:** R3.18BB `91595db2970ad395ec048ebd9326cfa97b01b38a` / `33104207616/98629573433` / artifact `9659874105` / `sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden

## Goal

Preserve exactly the immutable R3.18BB forty-row mixed-control lane. The **37 false** published-BA rows are terminators and must stop at BA. On only the exact **3 true** rows, observe one following property header through `payload_start`, compare it exactly with pinned Boxcars/native structural authority, classify the complete observed context, and stop.

This pass characterizes one header boundary only. It does not publish a following-header composition and does not decode the following payload.

## Frozen authority

```text
canonical continuity base             2bb5c48b3f627d6fe4f8ae6cb2eb2ea87408342e / 7958e09ee5756d826307ac8b122fd748f43b8a23
production SHA/tree                   5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BB evidence head/tree                 91595db2970ad395ec048ebd9326cfa97b01b38a / 40672cd1b546bca2b73ca252d727aa88ca9faec1
BB authority run/job                  33104207616 / 98629573433 SUCCESS
BB same-head CI                       33104207621 / 98629573926 SUCCESS
BB artifact                           9659874105 / 9295 / sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e
BB manifest file SHA-256              469e5e09e4299dad9d5c7990a8672b931530de68504b29a083d0dd50535d3894
BB frozen rows                        40
BB false / true                       37 / 3
BB mismatch / reselection             0 / 0
BB adjacent consumption               0/0/0/0
AX source artifact                    9644869549 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

Witness reselection is forbidden. Header tag/context distribution is **not** frozen in advance and must be discovered from these exact three true rows.

## Frozen continuation identities

Exactly these BB/AX true witnesses may enter the header lane:

```text
external_fixtures/sample_002.replay                                      BA stop 11224
external_fixtures/sample_003.replay                                      BA stop 7808
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay BA stop 3160
```

Every other BB witness is a false terminator and must perform zero following-header access.

## Witness classification

For all 40 BB rows:

- reconstruct the exact published R3.18BA result;
- require its control value/start/end/stop to equal BB;
- if false, classify as a terminator and stop;
- if true, require identity membership in the exact three-row continuation set above and allow exactly one header observation.

Required split: terminator rows 37; continuation rows 3; total 40. Any count or identity drift is Outcome B/C until explained.

## Positive header path — exact 3 true rows

For each true row:

1. build the existing production lookup plan;
2. reconstruct the valid published BA boundary;
3. invoke only the existing stateless existing-actor property-header primitive at the exact BA control position required by that primitive;
4. require the observed property-present bit to be true and equal the BA authority;
5. compare stream start/end/value/bound and property-ID width exactly with pinned Boxcars;
6. compare resolved property object and resolved attribute tag exactly;
7. compare complete structural/context identity, retaining version/net-version/RL223 fields actually required by the boundary;
8. compare `payload_start_bit` and header stop exactly;
9. repeat and require deterministic equality;
10. poison beginning at `payload_start` and require the returned header unchanged;
11. stop at `payload_start`.

Do not invoke any payload decoder.

## Terminator path — exact 37 false rows

For every false row, BA control must remain false and exact. No following-header success, stream/property lookup for a later property, payload boundary, or later-control access may be claimed after BA stop. Header/payload/second-control consumption remains zero.

## Evidence outputs

Report:

- all forty frozen BB identities and control reconstruction;
- exact 37 terminator identities;
- exact 3 continuation identities;
- per-true-row native and pinned-Boxcars header coordinates;
- resolved property object and attribute tag;
- stream bound and property-ID width;
- exact replay/version/net-version/RL223 context required to explain resolution;
- multiplicities of complete structural/context tuples;
- unclassified/mismatch counts.

Do not infer a Cartesian allowlist. If one or more exact header contexts appear, a later contract pass must freeze only those evidence-supported complete tuples before production composition.

## Required negative controls

At minimum:

- deterministic truncation inside a true-row following header -> fail closed;
- unresolved stream/property lookup -> reject;
- wrong actor object -> reject;
- wrong exact context where required -> reject;
- corrupt/mismatched BA prior -> reject;
- repeatability -> exact equality 3/3;
- poison beginning at `payload_start` -> header unchanged 3/3;
- false terminator no-header path -> 37/37;
- fabricated continuation identity -> reject;
- source-scope guard -> zero following-payload decoder calls and no repeated/generalized property loop;
- following payload / second later control consumption -> 0/0.

## Required gates

```text
BB witness identities                     40/40 exact
published BA reconstruction               40/40 exact
false terminators                         37/37 exact stop
true continuation rows                    3/3
true-row one-header native success        3/3
native/Boxcars header equality            3/3
resolved property object/tag              3/3 exact
payload_start / header stop               3/3 exact
header tuple classification               3/3
unclassified / mismatch                   0 / 0
witness reselection                       0
following payload bits consumed           0
second later control bits consumed        0
negative controls                         PASS
privacy                                   PASS
production/Cargo/fixture/corpus/support   0/0/0/0/0
same exact evidence-head natural CI       SUCCESS
```

Run focused boundary regressions plus Rust 1.85 fmt/check/test/clippy and the full repository verifier. Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs; reuse an equivalent exact run and never use rerun as polling.

## Hard stop

No following payload decode, no second later property control, no production header composition, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A

All three exact true-row following headers match through `payload_start`; all 37 false rows remain terminators; complete header/context classification is exact; mismatch/unclassified/reselection are zero; negatives/full validation/privacy pass; production mutation is zero; payload/second-control consumption is 0/0. Then a separate R3.18BD contract-only pass may freeze exactly the observed complete header contexts before any production composition.

### Outcome B

A bounded header/context distinction or evidence gap exists. Record it and keep production following-header composition closed.

### Outcome C

Authority/witness drift, native/oracle mismatch, false-row header access, payload/second-control consumption, production mutation, privacy failure, fabricated continuation membership, or generalized chaining. Stop without widening.
