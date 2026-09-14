# MIMIR R3.18BU Execution Spec — Bounded Post-BS Next Property-Control Production

**Date:** 2026-09-14
**Status:** ACTIVE
**Pass type:** bounded production composition
**Production base:** R3.18BS `5ab14575d0a698d752db35db76f3dbb300cdec8d` / `1c0b4c0a50385a34ba730a52a98a89423ff56869`
**Gate:** R3.18BT Outcome A

## Exact authority

R3.18BU is restricted to the two exact BT/BQ/BR rows:

1. `external_fixtures/sample_002.replay` — BS Boolean payload `[11238,11239)` value=true; one following control bit is **false**.
2. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay` — BS ActiveActor payload `[3205,3238)` active=true actor=1; one following control bit is **true**.

The R3.18BP false terminator remains outside membership. No witness reselection is allowed.

## Required production behavior

- Recompute R3.18BS exactly once and require exact equality with the supplied BS result.
- Require the admitted row/context/tag and exact payload boundary/value identity.
- Require `control_start_bit == bs.stop_bit == payload_end_bit`.
- Read exactly one checked LSB-first property-control bit.
- Require the read bit to equal immutable R3.18BR authority for that row.
- Return `control_end_bit = control_start_bit + 1` and `stop_bit = control_end_bit`.
- Read nothing after that bit.

## Exact clean source scope

Only these production-candidate files may change:

- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/tests/r3_18bu_post_bs_following_control.rs`

Temporary builder/evidence files must not enter the clean production commit.

## Required negatives

Reject or remain invariant under: corrupt/mismatched BS prerequisite, wrong actor/context/tag, fabricated authority row, BP false terminator, truncation at control start, altered payload bounds/semantic/stop, wrong expected control value, and poison after returned stop. The two valid rows must be repeatable.

## Validation gate

Run focused BU tests, `cargo fmt --all -- --check`, workspace check, workspace Clippy with `-D warnings`, full workspace tests, repository verification and `git diff --check`. Reconstruct a clean two-file candidate on fresh main, require exact-head natural CI SUCCESS, publish by non-force fast-forward only, then require published-main exact-SHA CI SUCCESS before continuity admission.

## Hard stop

No BP-false control access, no success outside exact two-row authority, no next stream/header/payload, no second later control, no generic/repeated cursor, no actor-state/runtime widening.
