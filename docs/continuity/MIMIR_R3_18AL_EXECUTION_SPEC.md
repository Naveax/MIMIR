# MIMIR R3.18AL — Published R3.18AK Following-Header Differential Audit

**Status:** ACTIVE
**Pass type:** read-only differential evidence
**Production authority:** R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145` / `98c675811cca4e4d7f0122c762f371548c9266c2`
**Frozen parent evidence:** R3.18AI 47-row immutable lane
**Contract authority:** R3.18AJ `sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c`
**Production mutation:** forbidden

## 1. Goal

Validate the published R3.18AK API on exactly the immutable R3.18AI 47-row lane. Reconstruct the already-admitted R3.18AG prior/control for every row, call published R3.18AK, compare the returned following header through `payload_start` against the frozen R3.18AI authority and the existing stateless native header primitive, and admit no bytes/bits after that boundary.

## 2. Frozen authority

```text
production SHA/tree          f20f529e3ada6e9a671ea91e5676a17a00770145 / 98c675811cca4e4d7f0122c762f371548c9266c2
AK builder                    32454544283/96689214219 SUCCESS
AK validation PR CI          32454918857/96690251188 SUCCESS
AK published-main CI         32459617440/96703744791 SUCCESS
AI evidence head             9d424dae2ed8cc7a0a6868111805a48763131196
AI authority run/job         32418184036/96584056481 SUCCESS
AI artifact                  9424764320 / sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5
AI exact rows                47
AI exact contexts            17
AI tags                      Int=47
witness reselection          0
AJ contract                  sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
```

## 3. Required evidence

- verify all replay identities and frozen witness coordinates before decoding;
- reconstruct valid published R3.18AG priors/true controls exactly;
- invoke published R3.18AK once for each frozen row;
- require control identity and header field/boundary equality 47/47;
- require returned `stop_bit == payload_start_bit` 47/47;
- compare to the direct stateless native header primitive without selecting new witnesses;
- reconstruct the exact 17 AJ complete tuples and their observed multiplicities summing to 47;
- require native/oracle mismatch 0;
- consume zero following-payload bits and zero another-control bits.

## 4. Negative controls

Require deterministic repeatability and fail-closed behavior for header truncation, corrupt AG/prior/control, wrong actor, unresolved lookup, wrong exact version context, Cartesian `(60,5,68,Int,868,32,10)`, fabricated `(60,5,39,Int,868,32,10)`, old-Z-only `(60,5,34,ActiveActor,868,32,10)`, and post-`payload_start` poison. R3.18Z/R3.18P inheritance remains forbidden.

## 5. Evidence artifact

Produce privacy-safe immutable evidence with exact source/production/oracle/replay identities, frozen witness manifest, per-row comparison, negative-control summary, mutation/consumption counters, internal manifest and SHA-256 receipts. Witness reselection must remain zero.

## 6. Validation

Run focused AK regression, full `mimir-replay`, workspace check/test/clippy and repository verifier, plus same-head normal CI. Before any workflow dispatch or PR, reuse an equivalent queued/in-progress run for the same SHA/workflow/input. Production/Cargo/fixture/corpus/support mutation must be `0/0/0/0/0`.

## 7. Hard stop

R3.18AL admits no production change and no post-AK payload. Another property-control bit, repeated/generalized property loop/cursor, next actor/frame/lifecycle, raw state/events/slices/skills/counterfactual/runtime/export remain closed.

## 8. Outcome gate

### Outcome A
Published R3.18AK matches the immutable 47-row authority exactly through `payload_start`; a later separate pass may investigate exactly one post-AK following payload.

### Outcome B
A bounded differential or harness gap exists; preserve evidence and open only the smallest targeted follow-up.

### Outcome C
Production/source drift, witness reselection, contract widening, payload/control access, loop/generalization, mutation, or unexplained differential contradiction. Stop and do not widen.
