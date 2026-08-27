# MIMIR R3.18BA — Bounded Post-AY Mixed Following-Control Production Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Parent:** `109bad258d43963fd5432317503f99a7e1b8aa1b`

## Decision

R3.18BA closes Outcome A. Published production validates/recomputes one exact R3.18AY Int/32 payload authority, begins exactly at the validated AY `stop_bit`, consumes exactly one LSB-first `property_present` bit, accepts both R3.18AX-observed boolean classes and stops exactly one bit later.

The immutable forty-row lane is preserved without witness reselection: **false=37 / true=3**. All seven upstream R3.18AU false terminators remain outside BA because they do not possess a valid AY payload. No following stream ID, following header, following payload, second later control bit, generalized/repeated property cursor, or wider actor/frame/semantic/runtime capability is admitted.

## Exact authority

```text
production SHA/tree                    5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
production parent                      109bad258d43963fd5432317503f99a7e1b8aa1b
lib / focused-test blobs               fe232760e63c3c1b46711084c70049f456ef345b / 41ef1c2c087cc52bf2bcf0fa65c911a31a6ffc13
BA execution spec blob                 3db94f3d559de1a7152a55fa08f7cb4b50d50d74
clean helper head                      ce5e27641cb0240e7440b93092be69a8fc5b7a11
builder                                33091339939/98584661482 SUCCESS
validation-only PR                     #208 CLOSED UNMERGED
PR exact-head CI                       33091594385/98585555551 SUCCESS
candidate push CI                      33091611038/98585614713 SUCCESS
published-main CI                      33092084628/98587299347 SUCCESS
R3.18AX evidence head                  465a3f2fc71e5eed6f00c16a04738031bef8d82c
R3.18AX authority                      33068572230/98504703417 SUCCESS
R3.18AX artifact                       9644869549 / 18070 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
```

The clean production commit is exactly one commit ahead of the prior canonical main and contains only `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs` (129 + 167 additions, no deletions). Temporary builder workflow/script material did not enter production.

## Admitted production behavior

```text
valid AY/BA rows                       40/40
upstream AU false terminators excluded 7/7
control false                          37
control true                           3
AY authority recomputed                40/40
control start                          AY stop on 40/40
control end / BA stop                  start + 1 on 40/40
repeatability                          PASS
post-stop poison isolation             PASS
wrong actor / unresolved lookup        PASS
wrong exact context / corrupt AY       PASS
source scope                           one AY recompute + one read_bit
next stream/header/payload/second      0/0/0/0
```

The fixed builder passed the focused BA plus prerequisite regression target 18/18, `cargo check -p mimir-replay`, and Clippy with `-D warnings`. The exact clean SHA then passed both validation-only PR CI and candidate push CI, was published with `force=false`, and the exact published-main SHA passed repository CI again.

A superseded helper attempt failed only on the public API arity Clippy lint after the focused semantics had passed; it is not authority and was not rerun. The admitted API instead removes the redundant AU argument and recomputes through the AU authority embedded in the supplied AY composition.

## Hard stop

The 37 false BA rows terminate at BA stop. The 3 true rows are only continuation candidates; BA does not inspect what follows. The seven upstream AU false terminators remain outside the AY/BA lane entirely. Following stream/header/payload, another control, generalized cursor, next actor/frame/lifecycle, raw state, events, replay slices, skills, counterfactuals, runtime and export remain closed.

## Next gate

R3.18BB is a separate read-only published-production differential. It must compare published R3.18BA against exactly the immutable forty-row R3.18AX authority, preserve false=37 / true=3 with mismatch and witness reselection at zero, prove AY prerequisite plus control start/value/end/stop identity, and prove adjacent consumption remains 0/0/0/0. Only after BB Outcome A may a later separate pass inspect one following header on exactly the three frozen true continuation rows.
