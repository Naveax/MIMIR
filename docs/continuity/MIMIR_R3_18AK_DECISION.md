# MIMIR R3.18AK Decision — Bounded Post-R3.18AG Following-Header Production

**Date:** 2026-08-21
**Pass type:** production implementation
**Outcome:** **A — ADMITTED / PRODUCTION / CLOSED**

## Authority

```text
canonical parent           5e26e7d3ceceac9752c35dde9c5074a1cd15262d
production SHA             f20f529e3ada6e9a671ea91e5676a17a00770145
production tree            98c675811cca4e4d7f0122c762f371548c9266c2
R3.18AJ contract SHA-256   cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AI immutable rows     47
R3.18AI tags               Int=47
```

## Production behavior admitted

Starting from one already-valid published R3.18AG true-control result, R3.18AK recomputes and requires exact control identity, derives the actor context from the already-valid prior, reuses the existing stateless existing-actor property-header primitive, resolves exactly one following header, requires complete seven-field R3.18AJ exact-tuple membership, and stops exactly at `payload_start`.

No following payload or another control bit is decoded or admitted. No repeated/generalized property loop or generic public cursor is introduced.

## Validation

```text
corrected builder          32454544283/96689214219 SUCCESS
builder artifact           9436810006
builder ZIP SHA-256        12926d7eff084c691d4430629fc135e54fa644e60ed92c7becc91af22e68b937
focused AK tests           5/5 PASS
full mimir-replay          PASS
validation PR              #62 / CLOSED UNMERGED
exact-head PR CI           32454918857/96690251188 SUCCESS
published-main CI          32459617440/96703744791 SUCCESS
published push CI count    1
duplicate guard            PASS
discovery receipt          32459835105/96704374410 SUCCESS
discovery artifact         9438546068 / sha256:b952c9e8fd4deda3eb99a0b8c1b3f9d2e5c8938a2d45224e7120d7bf2df233ba
```

Clean production scope is exactly `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18ak_post_ag_following_header.rs`; Cargo/fixture/corpus/workflow/support mutation is `0/0/0/0/0`.

Focused negative controls reject Cartesian `(60,5,68,Int,868,32,10)`, fabricated `(60,5,39,Int,868,32,10)`, old-Z-only `(60,5,34,ActiveActor,868,32,10)`, wrong version, wrong actor, unresolved lookup, truncation, and prior/control inconsistency. Repeatability and post-`payload_start` poison invariance pass.

## Hard stop

Still closed: post-AK following payload, another property-control bit, false success semantics, alternate unadmitted layouts, repeated/generalized property iteration or generic cursor, next actor/frame/lifecycle, raw state, events, slices, skills, counterfactual execution and runtime/export widening.

## Next exact pass

`R3.18AL — read-only published-R3.18AK following-header differential on the exact immutable R3.18AI 47-row lane.`
