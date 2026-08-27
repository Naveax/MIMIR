# MIMIR R3.18AX — Next Property-Control Bit Evidence After Exact AW Payload End

**Status:** ACTIVE
**Pass type:** read-only one-bit boundary evidence
**Production authority:** R3.18AU `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef`
**Direct payload authority:** R3.18AW Outcome A / artifact `9643254651` / `sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc`
**Production mutation:** forbidden
**Next stream/header/payload:** forbidden
**Second later property-control bit:** forbidden
**Repeated/generalized property loop:** forbidden

## 1. Goal

On exactly the forty admitted R3.18AW payload rows, reconstruct the current R3.18AU/AV header prerequisites and the exact R3.18AW Int/32 scalar through its proven `payload_end_bit`, then observe and differentially validate exactly one next `property_present` bit beginning at that exact payload end. Stop exactly one bit later.

All seven R3.18AV false terminators remain outside the AX lane and must never reach payload or control observation.

## 2. Frozen authority

```text
canonical main before AX             continuity parent containing this spec
production SHA/tree                  6a9f456c78ffccab177823234a8d9fe4ba59a850 / cbda5db96e88cc208f872c2237cf4741b8fcfaef
AW evidence head/tree                5f1d983a7b67f84293f337f23b7e7c25fee48795 / 63cbbb752100ef6944b1ecf366e89854e0f2376a
AW run/job                           33064535889/98491267256 SUCCESS
AW same-head CI                      33064535850/98491266948 SUCCESS / count 1 / rerun 0
AW artifact                          9643254651 / 23599 / sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc
frozen source lane                   exact 40 AW rows; 7 AV-false rows excluded
payload identity                     Int=40 / width32=40 / semantic range 5..300
native/oracle mismatch               0
witness reselection                  0
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh `main`, verify exact production/source/spec identities, AW run/CI/artifact digest and downloaded inner manifest, and all forty replay/witness identities. Do not reselect rows based on the value of the next bit.

## 3. Exact source lane

Use exactly the same forty R3.18AW rows with zero reselection. Each row must first prove:

```text
R3.18AU true following-header prerequisite exact
R3.18AT exact context membership exact
AW tag/start/end/width/value exact
payload_end_bit == payload_start_bit + 32
AV-false rows absent from target table
```

Any row that no longer reproduces is authority drift and stops the pass. It must not be replaced.

## 4. Differential one-bit observation

For every frozen row:

1. reconstruct the exact current header and AW scalar through `payload_end_bit`;
2. require the reconstructed payload end equal the frozen AW payload end;
3. with observation-only pinned Boxcars instrumentation, identify exactly the next property-loop `property_present` bit at that same global bit offset;
4. independently read exactly one LSB-first bit at the same offset with evidence-only native logic;
5. require exact start/value/end equality between oracle and independent observation;
6. record the boolean value without filtering either class and without inheriting an expected distribution from R3.18AP or any earlier boundary;
7. stop exactly one bit later.

Report the complete false/true distribution discovered on the forty rows.

## 5. Required negative controls

At minimum:

- all seven AV-false terminators absent from AX target rows and never invoke payload/control observation;
- truncate exactly before the one next control bit -> explicit failure with no fabricated value;
- mutate the AW payload-end relationship -> reject before control observation;
- corrupt the current header/payload prerequisite -> reject;
- repeat identical observation -> exact identical result;
- poison bits beginning at the one-bit control end -> observed control unchanged;
- wrong replay/actor/exact context -> reject through published prerequisite chain;
- prove next stream/header/payload and second later control consumption remain `0/0/0/0`;
- prove witness reselection 0 and production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 6. Evidence artifact

Produce one privacy-safe immutable artifact containing exact main/production/AW authority receipts; downloaded AW artifact/manifest verification; pinned Boxcars SHA and one-bit instrumentation hash; all forty privacy-safe control rows; complete false/true distribution; negatives; zero-consumption counters; mutation counters; privacy result; unique same-head CI receipt; and a SHA-256 inner manifest.

## 7. Validation

Require:

- exact AW artifact identity/digest/inner manifest;
- replay/witness identities exact 40/40; AV-false exclusion 7/7;
- exact AW payload reconstruction 40/40 before observation;
- pinned Boxcars versus independent native one-bit start/value/end exact 40/40;
- false + true distribution sums to 40 with no prior expected ratio;
- repeatability/truncation/prior-end-mismatch/post-control-poison negatives PASS;
- next stream/header/payload/second-control consumption `0/0/0/0`;
- witness reselection 0;
- focused regressions and full repository verifier PASS;
- workspace fmt/check/test/clippy PASS under Rust 1.85 floor;
- unique same-head natural CI SUCCESS;
- privacy PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## 8. Hard stop

R3.18AX may not resolve/decode the next stream ID, property object, attribute header or payload. It may not read a second later control bit, create a generalized/repeated property loop/cursor, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All forty frozen AW rows reproduce exactly and the one next `property_present` start/value/end matches pinned Boxcars with zero mismatch; all negatives/privacy/mutation gates pass. Record the complete observed false/true distribution. Only then may a separate bounded production or next-boundary pass be proposed according to the observed semantics and current canonical boundary.

### Outcome B

A reproducible next-control boundary mismatch exists. Record exact privacy-safe row/bit coordinates and keep the next-control boundary closed.

### Outcome C

Authority drift, witness reselection, AV-false-row access, production mutation, next stream/header/payload access, second-control/loop widening, privacy failure or validation contradiction. Stop without admission.
