# MIMIR R3.18AU — Bounded Post-AQ Mixed-Continuation Following-Header Production Decision

**Date:** 2026-08-26
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef`
**Parent:** `7068884bd1982a99ea68647156addc5b381f9613`

## Decision

R3.18AU closes Outcome A. On the immutable 47-row R3.18AS/R3.18AT authority lane, the published production boundary preserves all seven AQ-false rows as successful no-header terminators with zero post-AQ reads. On all forty AQ-true rows it composes exactly one stateless following header, requires exact R3.18AT eight-field membership, exposes the exact header boundary, and stops at `payload_start` without consuming the following payload or a second later property-control bit.

This admission is boundary-specific. It does not admit a following payload, second later control, header synthesis on false terminators, context outside R3.18AT, generalized/repeated property cursor, or wider actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior.

## Exact authority

```text
canonical main before production       7068884bd1982a99ea68647156addc5b381f9613 / c87e7ac1cca37cb1b569fbaf78181149e75881c6
production SHA/tree                    6a9f456c78ffccab177823234a8d9fe4ba59a850 / cbda5db96e88cc208f872c2237cf4741b8fcfaef
lib / focused-test blobs               d7b18acd7ea832acc73e94921b994fa1b341e006 / 5455121b2f0eafad09e031a66aa70178691c28fe
AU execution spec blob                 48e78daa50cb2724691fce09514d535a739f124f
clean-candidate CI                     32976370318/98201978533 SUCCESS
published-main CI                      32977973145/98207283247 SUCCESS
R3.18AT contract                       sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
R3.18AS evidence head                  475650fea59332f74b9f69da50e3e4471622ab7e
R3.18AS artifact                       9603335255 / sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted production behavior

```text
frozen rows                            47/47
AQ false terminators                   7/7
false-path following header            none 7/7
false post-AQ reads                    0
AQ true continuations                  40/40
true following headers                 exact 40/40
exact R3.18AT contexts                 16
observed true-header tag               Int=40
following payload bits consumed        0
second later control bits consumed     0
generalized/repeated cursor            0
```

The focused `r3_18au_post_aq_following_header` target passed 12/12 on the exact candidate and again through the full repository verifier. The frozen mixed-lane test exercises all 47 witnesses, false-path post-AQ poison isolation, true-path payload poison isolation, true-header truncation, exact membership rejection and source-scope guards. Workspace check/test and Clippy with warnings denied passed on the exact candidate and on published `main`.

## Clean publication

The production commit contains only:
- `crates/mimir-replay/src/lib.rs`;
- `crates/mimir-replay/tests/r3_18au_post_aq_following_header.rs`.

No Cargo/dependency, documentation, workflow, fixture, corpus, support, raw-state, event, skill, runtime or export mutation entered the production commit. Fresh-main ancestry was rechecked immediately before publication; `main` was advanced with `force=false`; exact SHA/tree readback matched; published-main CI succeeded.

## Hard stop

No following payload after the one admitted true-path header, no second later property-control bit, no header on the seven false terminators, no context outside exact R3.18AT membership, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18AV is a separate read-only published-production differential. It must compare published R3.18AU against exactly the immutable 47-row AS/AT authority, preserve false=7 and true=40, require exact true-header identity/boundaries and AT context/multiplicity equality, keep mismatch and witness reselection at zero, and consume no following payload or second later control. Only AV Outcome A may open a separate R3.18AW one-following-payload evidence pass on the exact forty true rows.
