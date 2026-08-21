# MIMIR R3.18AM — Post-AK One Following-Payload Evidence

**Status:** ACTIVE
**Pass type:** read-only structural/value differential evidence
**Production authority:** R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145` / `98c675811cca4e4d7f0122c762f371548c9266c2`
**Published-header authority:** R3.18AL Outcome A / `06b8570a25a989651fc800a4ded900ce5e2f3dbe`
**Production mutation:** forbidden
**Another property-control bit:** forbidden

## 1. Goal

On exactly the immutable R3.18AI/R3.18AL 47-row lane, reconstruct each valid published R3.18AK result, begin exactly at its `payload_start`, decode exactly one following payload, compare the native result against an independently pinned Boxcars oracle, and stop exactly at that payload end. Discover this boundary's payload width/value identity independently rather than inheriting earlier payload contracts by resemblance.

## 2. Frozen authority

```text
canonical parent                     02233c8125e658513dcb068370c48b1e8f15a01c / fc9293d821dd3e6e269763c3c0ab091428c29490
production SHA/tree                  f20f529e3ada6e9a671ea91e5676a17a00770145 / 98c675811cca4e4d7f0122c762f371548c9266c2
R3.18AJ contract                     sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c / exact_tuple_only / 17 contexts / multiplicity 47 / Int=47
R3.18AL evidence head/tree           06b8570a25a989651fc800a4ded900ce5e2f3dbe / 2753baa23be49a819cfceb333977473864a1b02b
R3.18AL authority                    32469442033 / 96732952709 SUCCESS
R3.18AL same-head CI                 32470066272 / 96734795022 SUCCESS
R3.18AL artifact                     9442034802 / 14650 / sha256:5fcb8f796ba365193698d5d27e2e7dc0e8c221dd42d7a901e956522b7ca1f639
rows / contexts / tags               47 / 17 / Int=47
witness reselection                  0
```

## 3. Required evidence

For all 47 frozen rows record at minimum:

- replay identity and frozen frame/actor/header coordinates;
- exact R3.18AK header identity and `payload_start`;
- independently observed oracle payload start/end/width/value;
- native payload start/end/width/value;
- exact native/oracle equality;
- exact stop at one payload end;
- exact R3.18AJ context identity and multiplicity provenance;
- following another-control bits consumed = 0.

All observed headers are currently `Int`, but R3.18AM must prove the payload layout at this boundary. Prior 32-bit Int evidence is a hypothesis, not an inherited contract.

## 4. Required negative controls

At minimum:

1. deterministic repeatability;
2. bit-exact payload truncation before the observed payload end;
3. wrong attribute tag;
4. wrong exact version/context where context applies;
5. corrupt/mismatched R3.18AK prior/header boundary;
6. post-payload-end poison invariance;
7. R3.18AC/R3.18S or any earlier payload contract is not treated as boundary authority;
8. another property-control bit consumed = 0;
9. witness reselection = 0;
10. production/Cargo/fixture/corpus/support mutation = 0/0/0/0/0.

## 5. Oracle

Use pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b` as evidence-only structural/value oracle. Boxcars must not become a production dependency.

## 6. Validation

- exact frozen artifact/replay identities;
- native probe deterministic repeatability;
- focused R3.18AK regression;
- full `mimir-replay` tests;
- workspace check/test/clippy under Rust 1.85;
- repository verifier;
- one ordinary same-head CI run;
- anti-duplicate inspection before any manual dispatch/rerun;
- immutable privacy-safe artifact with internal SHA-256 manifest.

## 7. Hard stop

R3.18AM is evidence only. It must not add a post-AK payload production API, consume another property control, create a generalized/repeated property loop or cursor, advance actor/frame/lifecycle state, or widen raw-state/event/slice/skill/counterfactual/runtime/export layers.

## 8. Outcome gate

### Outcome A
All 47 rows establish one exact boundary-specific payload family with native/oracle mismatch zero and another-control consumption zero. Close R3.18AM and open R3.18AN as a separate bounded production implementation for exactly the proven payload family.

### Outcome B
Only a strict subset or multiple separately identifiable shapes are proven. Admit only the exact supported subset/families and write R3.18AN accordingly.

### Outcome C
Authority drift, unexplained mismatch, witness reselection, unbounded layout, another-control consumption, or production mutation. Stop without widening.
