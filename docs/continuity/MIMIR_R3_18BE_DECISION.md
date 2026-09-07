# MIMIR R3.18BE — Bounded Post-BA Mixed-Continuation Following-Header Production Decision

**Date:** 2026-09-07
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`
**Parent:** `3fa88f27201ee91c51a3bb7a623c00b46204c1e0`

## Decision

R3.18BE closes Outcome A. On the exact immutable forty-row R3.18BA/R3.18BC/R3.18BD authority lane, all thirty-seven BA-false rows remain successful no-header terminators with zero post-BA reads. On the exact three BA-true rows, production composes exactly one existing-actor following header with the existing stateless primitive, requires exact R3.18BD eight-field membership, and stops exactly at `payload_start`.

The exact true-header contexts remain the three R3.18BD tuples with observed tags **Boolean=2 / Float=1**. No following payload or second later property-control bit is consumed. The seven upstream R3.18AU false terminators remain outside the BA/BE lane because they do not possess a valid BA prior.

This admission is boundary-specific. It does not admit header synthesis on false BA terminators, any context outside R3.18BD, following payload, later control, a generalized/repeated property cursor, or wider actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior.

## Exact authority

```text
canonical main before production       3fa88f27201ee91c51a3bb7a623c00b46204c1e0 / f193ee65fcc677178891fe5cb006f2fb2903cae9
production SHA/tree                    1d717d3e82179edd85b197968f46b8f951a3e828 / 72cf2b907437a1ba62cc9deebd7608f7d0372f81
lib / focused-test blobs               92d9d1893d75f9f0bd5ca921d8cf80455b88f0c3 / 78f32c79a3526cbfeac4e32ccc06e5965cd3e97b
BE execution spec blob                 c5f708fbc88732402bf057bd1274dc11f90669a2
production builder head                5ae76da91fb21ec9b62201673f6434fa2203cf6d
production builder                     33129018318/98713908063 SUCCESS
validation-only PR                     #209 CLOSED / UNMERGED
exact-candidate PR CI                  34094630343/101655343287 SUCCESS
published-main CI                      34095061141/101656732728 SUCCESS
BC evidence head/tree                  0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
BC evidence run/job                    33122152803/98691409657 SUCCESS
BC artifact                            9666964713 / sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
BD contract blob                       b0c2610b3d36e25302f35037518990fa3bc9fe69
BD contract                            sha256:33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27
BD membership                          exact_tuple_only / 3 eight-field tuples / multiplicity 3
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted production behavior

```text
frozen BA/BE rows                      40/40
BA false terminators                   37/37
false-path following header            none 37/37
false post-BA reads                    0
BA true continuations                  3/3
true following headers                 exact 3/3
exact R3.18BD contexts                 3/3
observed true-header tags              Boolean=2 / Float=1
upstream AU false terminators          7/7 excluded
following payload bits consumed        0
second later control bits consumed     0
generalized/repeated cursor            0
```

The builder passed the focused R3.18BE target plus BA/AY/header prerequisite regressions, workspace check/test, Clippy with warnings denied, and the repository verifier under Rust 1.85. The exact clean candidate then passed validation-only PR CI. PR #209 was closed unmerged, fresh `main` ancestry was rechecked, publication used `force=false`, exact SHA/tree readback matched, and the published-main SHA passed repository CI again.

## Clean publication

The production commit contains only:
- `crates/mimir-replay/src/lib.rs`;
- `crates/mimir-replay/tests/r3_18be_post_ba_following_header.rs`.

The exact diff is 775 additions / 2 deletions across those two files. No Cargo/dependency, continuity, workflow, fixture, corpus, support, raw-state/event/skill/runtime/export or unrelated mutation entered production.

## Hard stop

No following payload after the one admitted true-path header, no second later property-control bit, no header on any of the thirty-seven BA-false terminators, no context outside exact R3.18BD membership, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18BF is a separate read-only published-production differential. It must compare published R3.18BE against exactly the immutable forty-row BA/BC/BD authority, preserve false=37 and true=3, require exact true-header identity/boundaries and BD context equality, keep mismatch and witness reselection at zero, and consume no following payload or second later control. Only BF Outcome A may open a separate R3.18BG one-following-payload evidence pass on the exact three true rows.
