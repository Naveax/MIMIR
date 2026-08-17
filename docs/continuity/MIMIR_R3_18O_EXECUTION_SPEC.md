# MIMIR R3.18O Execution Spec — Following-Property Header Evidence

## Status

**ACTIVE after R3.18N Outcome A admission. Evidence-only. Production frozen.**

## Purpose

Characterize exactly one following existing-actor property header after the published R3.18M true-only control on the exact immutable R3.18N/R3.18L 47-row lane. Stop at that following property's `payload_start` boundary.

This pass may establish a narrow evidence-supported header boundary. It may not modify production Rust or admit any following payload or repeated property loop.

## Frozen authority

- R3.18N admission base: `1992ec94ab6a368e4143aad403ad6a223e3d3e5a`
- last production code SHA: `fd74ba8c520ab83b808730572c41e45d6dc616e6`
- R3.18N evidence head: `9bbf59745c950b7be5a5a592724f41db80874973`
- R3.18N evidence run/job: `32007040663` / `95318554719` — SUCCESS
- R3.18N exact-head CI: `32007040500` / `95318554225` — SUCCESS
- R3.18N artifact: `9280430420`
- R3.18N artifact digest: `sha256:772447a31e174355b3848605357667936ca522777d601dda504896aa0f663102`
- exact witness lane: `47` rows, reselection forbidden
- inherited following-control distribution: `false=0`, `true=47`

Before any evidence run, fresh-read `main` and fail closed if production source, R3.18M API identity, N receipt, or frozen witness identity has drifted.

## Required evidence

For every one of the 47 frozen rows:

1. Reconstruct the exact admitted R3.18J second-payload boundary.
2. Invoke/validate the published R3.18M following-control composition and require `true` at the exact one-bit boundary.
3. Independently establish the following header oracle from the pinned evidence lane.
4. Decode/measure exactly the following header fields required to reach `payload_start`:
   - stream-id start/end/value,
   - stream-id bound,
   - prop-id bit width/context,
   - resolved property object/index,
   - resolved attribute tag,
   - payload-start bit.
5. Require exact native/evidence-oracle equality for all admitted header fields and cursor boundaries.
6. Stop at `payload_start`.

## Hard stop / forbidden widening

R3.18O must consume:

- following payload bits: `0`
- another property-control bit: `0`
- next actor/frame bits: `0`

It must not add a production decoder, generalized cursor/loop API, new dependency, support-lane expansion, fixture/corpus mutation, raw-state/event/skill/runtime/export behavior, or infer acceptance outside exact observed structural contexts.

## Required negative controls

- truncation at each observed following-header field boundary,
- prior R3.18M stop mismatch,
- unresolved/wrong stream context,
- property/tag/context outside the exact observed lane,
- repeatability,
- poison/invariance immediately after `payload_start`, proving no payload or later-control consumption.

## Validation

- frozen replay identity: `47/47`
- witness reselection: `0`
- independent oracle/native mismatch: `0` for Outcome A
- privacy-safe artifact only
- same-head normal CI: SUCCESS
- full `mimir-replay` regression: PASS
- workspace check/test/clippy: PASS
- repository verifier: PASS
- production/Cargo/fixture/corpus/support mutation: `0/0/0/0/0`

## Outcomes

### Outcome A

All 47 frozen rows are exact, observed header domains are bounded/contractable, all negatives pass, and the decoder stops at `payload_start`. Admit R3.18O as read-only evidence and open only the next narrowly justified canonical pass. Production remains unchanged until a separately specified production candidate is validated and published.

### Outcome B

Any mismatch, unbounded/heterogeneous structural context, negative-control failure, identity drift, or post-`payload_start` consumption keeps production frozen. Record the narrowed boundary and investigate before opening another pass.
