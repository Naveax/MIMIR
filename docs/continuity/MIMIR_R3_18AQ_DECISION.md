# MIMIR R3.18AQ — Bounded Post-AN Mixed Following-Control Production Decision

**Date:** 2026-08-25
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production:** `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`
**Parent:** `ec2d6c29f90863d9e312856043d01fb98a0c2d2d`

## Decision

R3.18AQ is admitted as the minimum production composition after R3.18AN. It revalidates/recomputes the exact supplied AN payload composition, requires the admitted Int/32 payload-end boundary, reads exactly one following LSB-first `property_present` bit, accepts both R3.18AP-observed boolean classes, and stops exactly one bit later.

Unlike R3.18M, R3.18W and R3.18AG, false is not an error here. The immutable evidence distribution is false=7 / true=40.

## Exact authority

```text
production SHA/tree                  e1ccbef95c8424b689dee7d77fd8fde2af3e0204 / 4e7100625096594bcc5c5b4c6a8054c283643b13
parent                               ec2d6c29f90863d9e312856043d01fb98a0c2d2d
lib blob                             b886c58400de0efe0a6a6113d79e6f78e751a213
focused test blob                    983cbda666f40cbc739b250eac87bc4ce0c9eb99
AQ execution spec blob               fa8e5f6798a42fbeeed86b3b14ea7e4f39b35ebb
final builder helper                 4fee8974780fa2f8897bf0fea14ce13333a2dac4
final builder run/job                32860339919/97842469079 SUCCESS
builder receipt artifact             9568109670 / 1183 bytes
builder receipt SHA-256              1d865740559cb0748f840b3cca3d4ab9c627ac251bc15f6f99dbabb20c2e3afe
validation-only PR                   #197 closed unmerged
exact-head validation CI             32861522922/97846413853 SUCCESS
published-main CI                    32861924684/97847764026 SUCCESS
AP evidence head/tree                736ac33c099a9183693bfcb2b5f5b74704a8808e / 840011b603b5bb330e018bd060650cfb3af29b73
AP authority run/job                 32745234196/97489066582 SUCCESS
AP artifact                          9526988237 / sha256:b50b01bd87c0b61ca2e407abe43ac5db9fb15290f7cd3e908332d2ac2a26c4cc
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Published behavior

```text
frozen rows                          47
false                                7
true                                 40
both boolean classes accepted        PASS
new control reads                    1
start/end/stop exact                 PASS
next stream bits consumed            0
next header bits consumed            0
next payload bits consumed           0
second later control bits consumed   0
wrong actor negative                 PASS
unresolved lookup negative           PASS
truncation negative                  PASS
corrupt AN prior negative            PASS
wrong exact context negative         PASS
repeatability                        PASS
post-stop poison invariance          PASS
source-scope one-read/no-loop guard  PASS
```

## Clean scope

Exactly two files changed from parent to production:
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/tests/r3_18aq_post_an_payload_control.rs`

The commit contains 657 insertions and no Cargo/dependency, continuity, workflow, fixture, corpus or unrelated production changes.

## Validation and publication

The final builder passed Rust 1.85 formatting, focused AQ tests, boundary regressions, workspace check/test/clippy with warnings denied, and repository verification. PR #197 provided exact-head normal CI and was closed unmerged. Fresh main still equaled the candidate parent, so `main` was fast-forwarded to the exact clean candidate with `force=false`. Exact published-main readback and natural CI then succeeded.

## Hard stop

No following stream/header/payload is admitted after the AQ one-control result. No second later control, repeated/generalized property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted.

The seven false rows are terminators; they do not authorize any following-header decode.

## Next gate

R3.18AR is a separate read-only published-production differential over exactly the immutable R3.18AP 47-row lane. It must prove published AQ value/start/end/stop equality with false=7 / true=40, mismatch zero, witness reselection zero, production mutation zero and adjacent consumption 0/0/0/0. It may not decode a following header.
