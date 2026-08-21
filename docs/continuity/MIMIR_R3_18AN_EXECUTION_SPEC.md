# MIMIR R3.18AN — Bounded Post-AK Following-Payload Production (Preparatory)

**Status:** PREPARATORY / NON-CANONICAL / DEPENDENCY-GATED
**Parallel slot:** 2/5
**Preparation base:** `02233c8125e658513dcb068370c48b1e8f15a01c`
**Current production authority:** R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145`
**Pass type:** bounded production implementation
**Canonical publication:** forbidden until R3.18AL and R3.18AM are canonically CLOSED on fresh `main`

## Dependency chain

```text
R3.18AK production
 -> R3.18AL published-header differential
 -> R3.18AM one following-payload evidence
 -> R3.18AN bounded one-payload production [TARGET]
```

This preparation borrows only method shape from R3.18AD, R3.18T and R3.18J. It inherits no payload width, tag, value layout or context from those passes.

## Goal

Publish exactly one boundary-specific payload composition after a valid R3.18AK header result. The implementation may consume only the payload family/families proven by the final immutable R3.18AM authority, must begin exactly at the supplied/recomputed R3.18AK `payload_start`, and must stop exactly at one payload end. It must consume zero bits of the following `property_present` control.

## Authority freeze before implementation

After R3.18AM admission, re-read fresh `main` and replace every placeholder below with exact receipts:

```text
R3.18AK production SHA/tree/lib/test blobs      <REQUIRED>
R3.18AJ exact-context contract SHA256            cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AL authority head/run/job/artifact          <REQUIRED>
R3.18AM authority head/run/job/artifact          <REQUIRED>
R3.18AM exact rows/contexts/payload families     <DISCOVER; DO NOT INFER>
R3.18AM exact payload widths/layouts/values      <DISCOVER; DO NOT INFER>
```

If R3.18AM proves anything other than the expected single Int family, this spec must be repaired before code. Prior 32-bit Int evidence is not authority at this boundary.

## Production contract

The new API must be explicitly named for the post-AK one-payload boundary and require enough prior authority to prevent generic chaining. It must:

1. validate/recompute the supplied R3.18AK header result rather than trust arbitrary caller coordinates;
2. require exact R3.18AJ seven-field membership;
3. begin exactly at validated `payload_start`;
4. decode exactly one payload using only R3.18AM-admitted tag/layout/context identities;
5. return exact `payload_start`, `payload_end`, width and typed value/provenance required by the existing replay API style;
6. stop at exactly `payload_end`;
7. read zero following-control bits.

No generic cursor or repeatedly chainable loop surface is admitted.

## Required focused tests

At minimum:

- every frozen R3.18AM row exact through payload end;
- deterministic repeatability;
- exact truncation rejection at all required payload boundaries;
- wrong actor / unresolved lookup rejection;
- malformed or non-R3.18AJ header tuple rejection;
- wrong replay/version/context rejection where applicable;
- any tag/layout/context absent from R3.18AM rejected even if a lower decoder can parse it;
- post-stop poison invariance including the following property-control bit;
- exact stop equality with one payload end;
- following-control consumption = 0.

Synthetic tests supplement, never replace, frozen real-replay rows.

## Clean candidate

Expected clean production scope is only the minimum `mimir-replay` source plus one focused AN test file. No workflow/helper, evidence artifact, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup may enter the production commit.

Validation requires Rust 1.85 format/check/test/clippy, focused and full `mimir-replay` tests, repository verification, exact clean candidate CI, force-free publication after fresh-main ancestry verification, then published-main exact-SHA validation.

## Hard stop

No next `property_present` bit, no second payload/header/control, no generalized property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
Exact R3.18AM family is implemented over the complete frozen authority with all negatives PASS and following-control consumption 0. Publish only the bounded payload composition, then open R3.18AO as a separate published-production differential.

### Outcome B
Only an exact supported subset can be safely implemented. Publish only that subset and rewrite AO to the actual production contract.

### Outcome C
Authority drift, payload/context widening, unexplained mismatch, later-control access, generic chaining or validation contradiction. Stop without publication.

## Revalidation before use

This preparatory branch is never admission authority. When R3.18AM closes, reconstruct the real AN candidate from then-current canonical `main`; do not cherry-pick this stale-base document as evidence or production authority.
