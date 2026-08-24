# MIMIR R3.18AQ — Bounded Post-AN Following-Control Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** `3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38` / `3efcc244bca55623b12bb21eb277753fc61144d4`
**Evidence authority:** R3.18AP `736ac33c099a9183693bfcb2b5f5b74704a8808e` / `32745234196/97489066582` / artifact `9526988237`

## Goal

Publish exactly one boundary-specific composition after a valid R3.18AN payload. The API must validate/recompute the supplied AN prior, begin exactly at `prior.stop_bit`, consume exactly one `property_present` bit, represent both AP-observed values, and stop one bit later. It must read zero following stream/header/payload/second-control bits.

## Frozen evidence semantics

```text
rows                  47
false                  7
true                   40
published AN exact     47/47
oracle-native exact    47/47
mismatch               0
witness reselection    0
adjacent consumption   0/0/0/0
```

**Critical rule:** false is admitted. Do not copy the true-only fail-closed behavior of R3.18M, R3.18W or R3.18AG. Historical similarity does not override the R3.18AP distribution.

## Production contract

The new API must:
1. require enough prior authority to prevent arbitrary cursor advancement;
2. validate/recompute the supplied R3.18AN result;
3. require exact equality of the prior payload stop boundary;
4. consume exactly one LSB-first control bit at that stop;
5. return a boundary-specific typed result containing the observed boolean and exact start/end/stop;
6. accept both false and true;
7. stop at `prior.stop_bit + 1`;
8. consume no next stream ID, header, payload or second control;
9. fail atomically on malformed prior, out-of-range/truncated input or context drift.

No generic chain cursor or repeated property loop is admitted.

## Required focused tests

At minimum:
- all 47 frozen AP rows exact, including the exact 7 false and 40 true witnesses;
- deterministic repeatability;
- truncation before the control bit rejects atomically;
- corrupt/mismatched AN prior rejects;
- wrong actor / unresolved lookup / wrong exact context rejects where prior reconstruction requires them;
- exact start/end/stop equality;
- post-stop poison invariance;
- false path succeeds and consumes no header lookup/stream/payload;
- true path also stops before the following stream/header;
- next stream/header/payload/second-control consumption 0/0/0/0;
- source-scope guard proving exactly one new control read and no generic loop.

## Clean candidate

Expected clean production scope is the minimum `crates/mimir-replay/src/lib.rs` change plus one focused AQ integration test file. No workflow, temporary evidence helper, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup enters the production commit.

## Validation and publication

Require Rust 1.85 formatting, focused test, workspace check, clippy with warnings denied, workspace test, repository verifier, exact clean-candidate normal CI, fresh-main ancestry verification, force=false publication and published-main exact-SHA validation. Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs; if an equivalent run exists, reuse that run ID. Rerun is never polling.

## Hard stop

No following stream/header/payload after the one control bit, no second later control, no generalized/repeated property loop/cursor, no actor/frame/lifecycle advance, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
Publish the exact AP-admitted mixed false/true one-bit semantics with all focused/negative/full validations PASS and adjacent consumption 0/0/0/0. A later separate pass may differentially audit published AQ before any following header evidence.

### Outcome B
Only a narrower safe result representation can be implemented without violating the AP evidence. Publish only that narrower representation and keep the rest closed.

### Outcome C
Authority drift, prior-boundary mismatch, rejection of an AP-admitted boolean class, adjacent-bit access, generic chaining or validation contradiction. Stop without publication.
