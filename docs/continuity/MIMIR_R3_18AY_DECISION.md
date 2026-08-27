# MIMIR R3.18AY — Bounded Post-AU One-Following-Payload Production Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `2558cc0559422a3e6695e1501f20d96d83b23e6d` / `93198ad2a4f929ac62b87beddbc9d5b5665f08d1`
**Parent:** `dae58bc2d27aef2daac02b626ae37dbd309706bc`

## Decision

R3.18AY closes Outcome A. On exactly the immutable forty-row R3.18AW payload authority, published production validates/recomputes the supplied R3.18AU true-header composition, begins exactly at the validated payload start, decodes exactly one signed Int/32 payload using the existing primitive scalar machinery, preserves exact payload boundary/value identity, and stops exactly at payload end. All seven R3.18AU false terminators are rejected before payload decoding.

This admission does not consume or authorize the R3.18AX-observed next `property_present` bit. The AX distribution false=37 / true=3 remains evidence-only. No next stream/header/payload, second later control, generalized/repeated property cursor or wider actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior is admitted.

## Exact authority

```text
canonical main before production       dae58bc2d27aef2daac02b626ae37dbd309706bc / 06f5cb02daa94be784e7ab31aac101493bc8e959
production SHA/tree                    2558cc0559422a3e6695e1501f20d96d83b23e6d / 93198ad2a4f929ac62b87beddbc9d5b5665f08d1
lib / focused-test blobs               3742a0e856f51e50fd56ea963bb0bd6bac2d4b50 / f78956a22d0b2bb83e621cce24d88bce9484788b
AY execution spec blob                 d636344a63854b25f2be89540cf3dbf672a28b5c
builder                                33074574884/98525314306 SUCCESS
builder-head natural CI                33074574882/98525439235 SUCCESS
validation-only PR                     #206 CLOSED UNMERGED
clean-candidate CI                     33075136792/98527244393 SUCCESS
published-main CI                      33075583682/98528794945 SUCCESS
R3.18AT contract                       sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
R3.18AW evidence head                  5f1d983a7b67f84293f337f23b7e7c25fee48795
R3.18AW artifact                       9643254651 / sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc
R3.18AX evidence head                  465a3f2fc71e5eed6f00c16a04738031bef8d82c
R3.18AX artifact                       9644869549 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted production behavior

```text
AW true payload rows                    40/40
AU false terminators rejected           7/7
payload tag                             Int=40
payload width                           32 bits on 40/40
semantic range                          5..300
exact low-value witness                 1 row = 5
remaining observed values               39 rows = 300
header/payload authority recomputation  exact
deterministic repeatability             PASS
post-payload poison isolation           PASS
R3.18AX control bits consumed           0
generalized/repeated cursor             0
```

The focused `r3_18ay_post_au_payload` target passed 15/15 on the exact builder validation. Workspace check and Clippy with warnings denied passed there; the repository's full Windows verifier then passed on the exact clean candidate and again on published `main`.

## Clean publication

The production commit contains only:
- `crates/mimir-replay/src/lib.rs`;
- `crates/mimir-replay/tests/r3_18ay_post_au_payload.rs`.

The compare from parent is one commit ahead, two changed files and 293 additions. No Cargo/dependency, documentation, workflow, fixture, corpus, support, raw-state, event, skill, runtime or export mutation entered the production commit. The candidate was validated through PR #206 and that PR was closed unmerged. Fresh-main ancestry was rechecked immediately before publication; `main` advanced with `force=false`; exact SHA/tree readback matched; published-main CI succeeded. The source-only publish correctly produced no Knowledge Archive run because its path filter excludes production source.

## Hard stop

No R3.18AX following-control production, no payload/control success on the seven false terminators, no next stream/header/payload, no second later property-control bit, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18AZ is a separate read-only published-production differential. It must reuse exactly the immutable forty-row R3.18AW payload authority, compare published R3.18AY against AW plus independent direct-native/oracle identity, require exact Int/32 tag/start/end/width/value equality and deterministic repeatability, keep mismatch and witness reselection at zero, and consume no R3.18AX following-control bit. Only a separate later pass may consider control production.
