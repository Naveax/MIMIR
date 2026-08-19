# MIMIR R3.18AD — Bounded Post-AA Ordinal-3 Payload Production Decision

**Date:** 2026-08-19
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production SHA:** `ccadbf148381c007890d13d5fe8120866a0f40f9`
**Production tree:** `0882601060d0bb6d37fcc03ae7273dcf50dd0be3`
**Production parent:** `671cd19a7d034b1377de5bed1dfd36600f45c8d7`

## Decision

R3.18AD is admitted Outcome A. Production now composes exactly one R3.18AC-admitted ordinal-3 payload after a valid published R3.18AA following-header boundary. It recomputes the existing R3.18AA path, so complete R3.18Z exact-tuple header membership remains authoritative, then decodes only the AC-observed payload shape and stops exactly at payload end.

The admitted payload shapes are boundary-specific and closed:

- `ActiveActor`: exactly 33 bits;
- `Int`: exactly 32 bits;
- `UniqueId`: exactly 80 bits with `system_id=1` and `Steam` remote kind.

Lower-level support for other UniqueId systems/layouts does not widen this production boundary. No another `property_present` bit, generic property loop/cursor, next actor/frame or semantic/runtime/export behavior is admitted.

## Exact authority

```text
pre-pass canonical main/tree         671cd19a7d034b1377de5bed1dfd36600f45c8d7 / a98c6713165ebd2f0553d07787ab51bcfbf3b65f
production SHA/tree                  ccadbf148381c007890d13d5fe8120866a0f40f9 / 0882601060d0bb6d37fcc03ae7273dcf50dd0be3
production parent                    671cd19a7d034b1377de5bed1dfd36600f45c8d7
production lib blob                  1254d5a3b0299677f6661712c371aacf27cdb45d
R3.18AD focused test blob            013ad6da300cd88f7821b18634736e016af63276
R3.18Z contract SHA256               81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18AC authority                    32237834815 / 96021661994 SUCCESS
R3.18AC same-head CI                 32237834813 / 96021661894 SUCCESS
R3.18AC artifact                     9359697636 / sha256:a6914044dfd8991d74b95caeb3507fb2469175c4458c5b50b55395b8ea67b9df
clean builder authority              32241956973 / 96034261394 SUCCESS
exact-head validation PR CI          32242293315 / 96035296746 SUCCESS
exact clean push CI                  __AD_CANDIDATE_CI__ / __AD_CANDIDATE_JOB__ SUCCESS
published-main CI                    __AD_MAIN_CI__ / __AD_MAIN_JOB__ SUCCESS
published receipt helper             __AD_RECEIPT_RUN__ / __AD_RECEIPT_JOB__ SUCCESS
```

The clean production commit is a direct child of the pre-pass canonical main and was published by a fresh-main `force=false` fast-forward. Validation PR #46 was closed without merge.

## Admitted production behavior

```text
input boundary                       valid R3.18T prior, recomposed through published R3.18AA
header authority                     complete R3.18Z exact tuple only
replay context                       868.32 / net10 / non-RL223
ActiveActor payload                  33 bits
Int payload                          32 bits
UniqueId payload                     system_id=1 / Steam / 80 bits
stop                                 exactly decoded payload end
another control bits consumed        0
generic property loop/cursor         none
```

## Validation

The permanent R3.18AD focused suite passed 5/5 using the canonical frozen witnesses already carried by R3.18AA/AC: one ActiveActor, one Int and the exact single system-1/Steam UniqueId row. Repeatability, truncation, post-payload poison invariance and wrong-context rejection passed. A synthetic lower-level K2-valid Epic 312-bit UniqueId was explicitly rejected by the R3.18AD boundary.

Builder validation passed Rust 1.85 formatting, focused AD/AA/K2/scalar tests, full `mimir-replay`, workspace check/test, clippy `-D warnings`, repository verification and clean-scope checks. Exact-head validation PR CI passed. Exact clean push CI and published-main CI are bound above by immutable read-only receipt.

## Clean scope

The clean production commit changes exactly:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_18ad_post_aa_payload.rs`

Cargo manifests/lockfile, docs, workflows, fixtures, corpus and support lanes are unchanged in the production commit.

## Superseded builder attempts

Temporary builder runs `32241318277 / 96032290229` and `32241686993 / 96033430357` were not admitted. Their production patch compiled and clean scope passed, but disposable focused-test witness bootstrap used incorrect paths/coordinates. No production commit from those attempts was published. The final authority builder `32241956973 / 96034261394` passed all gates.

## Hard stop

R3.18AD admits no another property-control bit, no alternate UniqueId system/layout, no repeated/generalized property loop or public cursor, no next actor/frame/lifecycle mutation, no raw-state/event extraction, no replay slicing, no skill mining, no counterfactual execution, and no runtime/export widening.

## Next gate

R3.18AE is a separate read-only published-production differential. It must reuse the exact immutable R3.18AC 47-row lane with zero witness reselection, invoke the published R3.18AD API, require exact equality through one ordinal-3 payload end, and prove another-control consumption remains zero. R3.18AE may not change production.
