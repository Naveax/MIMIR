# MIMIR R3.18N Decision — Published Following-Control Differential

## Status

**Outcome A — ADMITTED / COMPLETE / READ-ONLY.**

R3.18N differentially validated the published R3.18M after-second-payload following-`property_present` API on the exact immutable R3.18L 47-row continuation lane. Production Rust remains frozen at `fd74ba8c520ab83b808730572c41e45d6dc616e6`.

## Authority

- pre-pass `main`: `1992ec94ab6a368e4143aad403ad6a223e3d3e5a`
- production SHA: `fd74ba8c520ab83b808730572c41e45d6dc616e6`
- evidence head: `9bbf59745c950b7be5a5a592724f41db80874973`
- evidence run/job: `32007040663` / `95318554719` — SUCCESS
- exact-head normal CI run/job: `32007040500` / `95318554225` — SUCCESS
- artifact: `9280430420` / `21060` bytes
- artifact digest: `sha256:772447a31e174355b3848605357667936ca522777d601dda504896aa0f663102`
- artifact name: `r318n-published-following-control-evidence`
- frozen witness reselection: `0`

## Admitted evidence

- frozen rows: `47/47`
- R3.18J reconstruction exact: `47/47`
- following control distribution: `false=0`, `true=47`
- published R3.18M / oracle mismatch: `0`
- exact following control start/value/end/stop: `47/47`
- truncated/missing following control negative: `47/47 PASS`
- prior R3.18J stop mismatch negative: `47/47 PASS`
- missing second header negative: `47/47 PASS`
- missing second payload negative: `47/47 PASS`
- synthetic false following control rejection: `47/47 PASS`
- repeatability: `47/47 PASS`
- post-stop poison/invariance: `47/47 PASS`
- following stream bits consumed: `0`
- following header bits consumed: `0`
- following payload bits consumed: `0`
- another control bit consumed: `0`
- privacy gate: `PASS`
- production/Cargo/fixture/corpus/support mutation: `0/0/0/0/0`

## Decision

The published R3.18M true-only one-bit composition is admitted on the exact frozen 47-row lane. This does **not** admit a following stream ID, following property header, following payload, another control bit, generalized property loop, next actor/frame, lifecycle state, raw state, events, replay slicing, skills, runtime, or export widening.

Outcome A opens only a separate **R3.18O following-property header evidence** pass. R3.18O is evidence-only and must stop at the following property's `payload_start` boundary without consuming payload bits or another property-control bit.
