# MIMIR R3.18BA — Bounded Post-AY Mixed Following-Control Production Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / PRODUCTION**
**Canonical production:** `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Parent:** `109bad258d43963fd5432317503f99a7e1b8aa1b`

## Decision

R3.18BA publishes exactly one boundary-specific mixed following-control result after one validated R3.18AY payload. The implementation recomputes and requires exact equality of the supplied AY authority, initializes the private LSB-first cursor at the validated AY stop, consumes exactly one `property_present` bit, accepts both immutable R3.18AX-observed boolean classes, and stops exactly one bit later.

On the exact frozen forty-row lane the distribution is false=37 / true=3. All seven upstream AU false terminators remain outside BA because no valid AY payload exists for them. No following stream ID, header, payload or second later control is consumed.

## Exact authority

```text
canonical parent                       109bad258d43963fd5432317503f99a7e1b8aa1b
production SHA/tree                    5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
fixed helper                           ce5e27641cb0240e7440b93092be69a8fc5b7a11
builder run/job                        33091339939/98584661482 SUCCESS
builder helper-head CI                 33091339935 SUCCESS
validation-only PR                     #208 CLOSED / UNMERGED
exact-candidate PR CI                  33091594385/98585555551 SUCCESS
validation-branch CI                   33091611038 SUCCESS
published-main CI                      33092084628/98587299347 SUCCESS
R3.18AX evidence head/tree             465a3f2fc71e5eed6f00c16a04738031bef8d82c / b164a8566c6ac57ddee1aed0a7edbf9f44250488
R3.18AX run/job                        33068572230/98504703417 SUCCESS
R3.18AX same-head CI                   33068572200/98504703614 SUCCESS
R3.18AX artifact                       9644869549 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
```

## Frozen result

```text
valid AY/BA rows                       40/40
upstream AU false terminators          7/7 excluded
BA false                               37
BA true                                3
AY recomputation                       exactly 1 per BA call
new LSB-first control read             exactly 1 per BA call
repeatability                          PASS
post-stop poison isolation             PASS
wrong actor / lookup / context         PASS
corrupt AY authority                   PASS
next stream/header/payload/second      0/0/0/0
production source scope                exactly 2 files
```

The focused BA plus directly affected prerequisite regression target passed 18/18 under Rust 1.85. `cargo check -p mimir-replay` and `cargo clippy -p mimir-replay --all-targets -- -D warnings` passed on the fixed builder. The repository's normal exact-candidate and published-main verifiers also passed.

## Superseded scaffolding

The first builder run `33090827273` is historical non-authority. Its focused behavior tests passed, but Clippy rejected the original eight-argument BA API as `too_many_arguments (8/7)`. That run was not rerun. The correction removed redundant `au_prior` authority from the public boundary-specific API and recomputes AU through `ay_prior.header_composition`; the fixed helper and all later validation receipts above are authoritative.

A separate `builder/r318ba-production-v2` branch carried temporary helper files and is not clean production authority. The admitted production commit is the exact two-file clean candidate `5d2bca711f528ab1bb607104379af503ff175697`.

## Truncation precision

R3.18AX's immutable evidence receipt already proves exact bit-level `TRUNCATION_BEFORE_CONTROL=PASS 40/40`. All forty frozen BA control starts are non-byte-aligned. Therefore the production `&[u8]` carrier cannot express an EOF that preserves every AY payload bit while removing only the immediately following control bit. BA correctly remains a byte-slice API rather than widening with a new bit-length transport parameter solely for a test fixture. Carrier truncation remains fail-closed; exact-before-bit truncation remains AX evidence authority.

## Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no BA access on seven upstream false terminators, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18BB is a separate read-only published-production differential. It must replay exactly the immutable forty R3.18AX witnesses against published R3.18BA, require exact start/value/end/stop 40/40, preserve false=37 / true=3 with mismatch/reselection 0/0, and consume nothing adjacent. The 37 false rows are terminators. Only the exact three true rows may be considered by a later separate following-header evidence pass.
