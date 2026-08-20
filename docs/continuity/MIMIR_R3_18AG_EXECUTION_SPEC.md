# MIMIR R3.18AG — Bounded True-Only Property-Control Production After Published R3.18AD Payload

**Status:** ACTIVE
**Pass type:** production implementation / one-bit only
**Production parent:** R3.18AD `ccadbf148381c007890d13d5fe8120866a0f40f9`
**Evidence authority:** R3.18AF Outcome A
**Observed control allowlist:** `true` only (`true=47`, `false=0`)
**Next stream/header/payload:** forbidden
**Second later control:** forbidden
**Repeated/generalized property loop:** forbidden

## 1. Goal

Implement one production function that accepts one already-valid published R3.18AD ordinal-3 payload result, proves its internal payload/header stop invariants, reads exactly one following `property_present` bit beginning at that result's `stop_bit`, admits **true only**, and stops exactly one bit later. False must return an explicit fail-closed error.

## 2. Frozen authority

```text
production SHA/tree                  ccadbf148381c007890d13d5fe8120866a0f40f9 / 0882601060d0bb6d37fcc03ae7273dcf50dd0be3
production lib/test blobs            1254d5a3d16e7b97b1dee87a8b459514d25749ef / 013ad6da94b866ecaca94cd6420e7568d9b4b5ee
R3.18AF spec blob                    fd3e4debac1c40756c37f106fc68440576678d6c
R3.18AF evidence head/tree           30286c07727539d68f551140838fb2ef6802a26e / be808ad1ea757a095e37ccfe8f25b03e074dd732
R3.18AF authority                    32344981062 / 96351720877 SUCCESS
R3.18AF same-head CI                 32345376481 / 96352906609 SUCCESS
R3.18AF artifact                     9397743505 / 12204 bytes / sha256:d7edeab657928c94c35c852ae302fd614cab92a52b7e44f671310200af4b268f
R3.18AF distribution                 false=0 / true=47
R3.18AF native-oracle mismatch       0
R3.18AF adjacent consumption         stream/header/payload/second-control = 0/0/0/0
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
Boxcars instrumentation SHA-256      de5fecb234e4a53798ce8e59b728078c7719ae04ef5fa2966b2c3b67072e7adf
```

## 3. Required production contract

The public API must take the already-decoded R3.18AD result rather than reconstructing later stream state. Before success it must fail closed unless all prior invariants are coherent, including at minimum:

- `prior.stop_bit` equals the exact end of the admitted AD payload;
- `prior.header_composition.stop_bit` equals the AD payload start;
- the prior payload shape remains one of AD's closed allowlist: ActiveActor/33, Int/32, UniqueId system1-Steam/80;
- the network contains the one requested control bit at `prior.stop_bit`.

Then:

1. set `property_present_start_bit = prior.stop_bit`;
2. perform exactly one LSB-first bit read;
3. if the bit is false, return an explicit `unadmitted-false-control`-class error and expose no success result;
4. if true, return a result whose property-present value is true;
5. set `property_present_end_bit = start + 1`;
6. set `stop_bit = property_present_end_bit`;
7. perform no further read.

## 4. Required tests

Permanent focused tests must cover at least:

- one real ActiveActor prior row;
- one real Int prior row;
- the real UniqueId system1-Steam prior row;
- at least one byte-aligned prior stop when available;
- false-bit mutation fails closed;
- truncation before the control bit fails atomically;
- forged/mutated prior stop fails before success;
- forged prior payload/header boundary fails before success;
- repeatability on identical input;
- post-control poison leaves the one-bit result unchanged;
- source-scope proof: exactly one `read_bit()`, no lookup-plan access, no following header/payload decoder, no `while`/`for` property loop.

## 5. Validation and clean publication

Run under Rust 1.85:

- focused R3.18AD + R3.18AG tests;
- full `cargo test -p mimir-replay`;
- workspace `cargo fmt --all -- --check`;
- `cargo check --workspace`;
- `cargo test --workspace`;
- `cargo clippy --workspace --all-targets -- -D warnings`;
- `scripts/verify_mimir_knowledge_archive.ps1`;
- exact source-scope and privacy checks.

The final production candidate must contain only the minimal production source modification and permanent focused R3.18AG test file. Temporary helpers/workflows must not enter the clean commit. Validate the exact clean SHA and publish only by fresh-main `force=false` fast-forward.

## 6. Hard stop

R3.18AG may not resolve/decode the next stream ID, property object, attribute tag or payload; read a second later control bit; accept false success semantics; add a generalized/repeated property cursor or loop; widen UniqueId systems/layouts; iterate the next actor/frame; mutate lifecycle state; materialize raw state/events; slice replays; mine skills; run counterfactuals; or widen runtime/export behavior.

## 7. Next gate after publication

Even a successful R3.18AG production publication does not open the following header. A separate published-production differential must first prove the R3.18AG API itself on the immutable AF lane, preserving false=0/true=47, mismatch 0 and adjacent-consumption 0/0/0/0.
