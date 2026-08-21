# MIMIR R3.18AP — Next Property-Control Bit Evidence After Published AN (Preparatory)

**Status:** PREPARATORY / NON-CANONICAL / DEPENDENCY-GATED
**Parallel slot:** 4/5
**Preparation base:** `02233c8125e658513dcb068370c48b1e8f15a01c`
**Current production authority:** R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145`
**Pass type:** read-only one-bit evidence
**Canonical publication:** forbidden until R3.18AL, R3.18AM, R3.18AN and R3.18AO are canonically CLOSED

## Dependency chain

```text
R3.18AK header production
 -> R3.18AL published header differential
 -> R3.18AM payload evidence
 -> R3.18AN payload production
 -> R3.18AO published payload differential
 -> R3.18AP exactly one next property_present bit evidence [TARGET]
```

Method analogues are R3.18AF, R3.18V and R3.18L only. Their observed false/true distributions are not inherited.

## Goal

On exactly the immutable R3.18AO authority lane, begin at the exact published R3.18AN payload `stop_bit`, read exactly one following `property_present` bit, compare against an independently pinned Boxcars oracle, and stop one bit later. Do not consume stream id, header, payload or a second control bit.

## Authority freeze before execution

When prerequisites close, fetch fresh `main` and freeze:

```text
R3.18AN production SHA/tree/lib/test blobs        <REQUIRED>
R3.18AO authority head/run/job/artifact            <REQUIRED>
R3.18AO exact frozen rows and payload-stop bits    <REQUIRED>
R3.18AJ exact-context contract                     cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
pinned Boxcars                                     c70e77df7af81b436cb545d070bb90c82f562d0b
witness reselection                                0
```

Do not assume the next control is true because earlier lanes observed true-only families. AP must measure this boundary independently.

## Required evidence

For every frozen R3.18AO row record:

- exact published AN payload identity and stop bit;
- oracle next-control bit and bit coordinate;
- native one-bit result and stop bit;
- exact equality native/oracle;
- observed false/true distribution;
- repeated invocation equality;
- next stream/header/payload/second-control consumption = `0/0/0/0`.

Outcome A requires mismatch zero across the entire frozen lane, not a sampled subset.

## Negative controls

At minimum:

1. truncation before the target control bit rejects;
2. corrupt/mismatched AN prior rejects before trusting its stop coordinate;
3. wrong actor / unresolved lookup / wrong exact replay-version context rejects where required by the prior chain;
4. post-control poison beginning at the first stream/header bit leaves the one-bit result invariant;
5. repeated invocation is byte/bit-identical;
6. no stream id, header, payload or second-control access;
7. witness reselection 0;
8. production/Cargo/fixture/corpus/support mutation 0/0/0/0/0.

## Validation

Use the immutable AO lane, pinned Boxcars only as evidence oracle, Rust 1.85 repository verification, focused permanent AN regressions, deterministic evidence artifact with internal SHA-256 manifest, and one same-head ordinary CI receipt. Check for equivalent queued/waiting/in-progress runs before any dispatch or validation PR; never rerun to poll.

## Hard stop

R3.18AP is evidence only. It does not publish a control API. No stream/header/payload after the bit, no second later control, no generalized property loop/cursor, no next actor/frame/lifecycle/raw-state/event/slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
One-bit native/oracle equality across the exact frozen lane with mismatch 0 and adjacent consumption 0/0/0/0. Record the actual false/true distribution. Open R3.18AQ as a separate bounded production pass whose success semantics must be derived only from AP evidence.

### Outcome B
A reproducible subset/branch distinction exists. Admit only the observed evidence and write AQ around that exact partition if a bounded production contract is possible.

### Outcome C
Authority drift, witness reselection, unexplained bit mismatch, adjacent-bit access or production mutation. Stop without widening.

## Revalidation before use

This document is planning evidence only. Rebuild the actual AP execution spec from canonical R3.18AO receipts once AO is closed; never treat this stale-base preparation as pass authority.
