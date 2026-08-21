# MIMIR R3.18AQ — Bounded Post-AN Following-Control Production (Preparatory)

**Status:** PREPARATORY / NON-CANONICAL / DEPENDENCY-GATED
**Parallel slot:** 5/5
**Preparation base:** `02233c8125e658513dcb068370c48b1e8f15a01c`
**Current production authority:** R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145`
**Pass type:** bounded production implementation
**Canonical publication:** forbidden until R3.18AP is canonically CLOSED

## Dependency chain

```text
R3.18AK -> R3.18AL -> R3.18AM -> R3.18AN -> R3.18AO -> R3.18AP -> R3.18AQ [TARGET]
```

Historical method analogues are R3.18AG, R3.18W and R3.18M. Their true-only behavior is not inherited. AQ's success/false semantics must be derived strictly from the final R3.18AP distribution.

## Goal

Publish exactly one boundary-specific next-property-control composition after a valid published R3.18AN payload result. The implementation must validate/recompute the supplied AN prior, begin exactly at its payload `stop_bit`, consume exactly one `property_present` bit, and stop one bit later. It must read zero following stream/header/payload/second-control bits.

## Authority freeze before implementation

After AP closes, fetch fresh `main` and freeze:

```text
R3.18AN production SHA/tree/lib/test blobs      <REQUIRED>
R3.18AO differential authority                   <REQUIRED>
R3.18AP one-bit evidence head/run/job/artifact   <REQUIRED>
R3.18AP exact false/true distribution            <DISCOVER; DO NOT INFER>
R3.18AP exact frozen lane and stop coordinates   <REQUIRED>
```

If AP observes both false and true, this spec must be repaired to represent those exact semantics. Do not force a true-only API merely because AG/W/M were true-only on different boundaries.

## Production contract

The new API must be explicitly tied to the post-AN payload boundary and require enough prior evidence to prevent arbitrary cursor advancement. It must:

1. validate/recompute the supplied R3.18AN result;
2. require exact equality of the prior payload stop boundary;
3. consume exactly one following control bit;
4. expose only the exact semantics admitted by R3.18AP;
5. stop at `prior.stop_bit + 1`;
6. consume no stream id, header, payload or second control;
7. fail closed for every control/state combination not admitted by AP.

No generic chain cursor or repeated property loop is admitted.

## Required focused tests

At minimum:

- every frozen AP row exact;
- deterministic repeatability;
- truncation before the control bit rejects;
- corrupt/mismatched AN prior rejects;
- wrong actor / unresolved lookup / wrong exact context rejects where the prior chain requires them;
- all AP-unadmitted bit/semantic branches fail closed;
- post-stop poison invariance beginning at the next stream/header bit;
- exact stop one bit after AN payload end;
- next stream/header/payload/second-control consumption 0/0/0/0.

Synthetic negatives supplement, never replace, the complete frozen lane.

## Clean candidate

Expected clean production scope is the minimum `mimir-replay` source plus one focused AQ test file. No workflow, temporary evidence helper, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup enters the production commit.

Validation requires Rust 1.85 fmt/check/test/clippy, focused and full `mimir-replay`, repository verifier, exact clean-candidate CI, force-free publication after fresh-main ancestry verification, and published-main exact-SHA validation. Inspect equivalent queued/waiting/in-progress runs before any manual dispatch or rerun.

## Hard stop

No following stream/header/payload after the one control bit, no second later control, no generalized/repeated property loop/cursor, no actor/frame/lifecycle advance, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
Publish the exact AP-admitted one-bit control semantics with all focused/negative/full validations PASS and adjacent consumption 0/0/0/0. A later separate pass may differentially audit published AQ before any further header or payload evidence.

### Outcome B
Only a narrower branch can be safely implemented. Publish only that branch and keep every other control semantic closed.

### Outcome C
Authority drift, prior-boundary mismatch, unadmitted false/true semantics, adjacent-bit access, generic chaining or validation contradiction. Stop without publication.

## Revalidation before use

This preparatory branch is never authority. When AP closes, reconstruct the real AQ production candidate from then-current canonical `main` and AP receipts. Do not cherry-pick this stale-base document as production evidence.
