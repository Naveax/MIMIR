# MIMIR R3.18AN — Bounded Post-AK One Following-Payload Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production parent:** R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145` / `98c675811cca4e4d7f0122c762f371548c9266c2`
**Evidence authority:** R3.18AM Outcome A / `842b94ed4c4e57323433585fea48116ecf18989b`
**Admitted payload family:** `Int / 32 bits` only
**Another property-control bit:** forbidden

## 1. Goal

Publish exactly one boundary-specific payload composition after a valid R3.18AK following-header result. The API must validate or recompute the supplied R3.18AK/AJ authority, begin exactly at the validated `payload_start`, decode exactly one R3.18AM-admitted signed `Int` payload of 32 bits with the existing primitive scalar machinery, return the exact payload boundary/value identity, and stop exactly at payload end.

No generic cursor or repeatedly-chainable property loop is admitted.

## 2. Frozen authority

```text
R3.18AK production SHA/tree          f20f529e3ada6e9a671ea91e5676a17a00770145 / 98c675811cca4e4d7f0122c762f371548c9266c2
R3.18AJ exact-context contract       sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c / 17 tuples / multiplicity 47 / Int=47
R3.18AL published-header authority   06b8570a25a989651fc800a4ded900ce5e2f3dbe
R3.18AM evidence head/tree           842b94ed4c4e57323433585fea48116ecf18989b / 486d0a0f3833dcb8872f062ae1927c9aefde87ba
R3.18AM authority run/job            32473716883 / 96745647750 SUCCESS
R3.18AM same-head CI                 32474038136 / 96746590106 SUCCESS
R3.18AM artifact                     9443581172 / sha256:2f65de5207bd96787fd7d1527a55991f08d5da614a0ddfce22a7aa267968e3c8
R3.18AM frozen rows                  47
R3.18AM payload identity             Int=47 / width32=47 / semantic range 1..415
R3.18AM native/oracle mismatch       0
R3.18AM witness reselection          0
```

R3.18AM, not resemblance to earlier boundaries, is the authority for `Int/32` here.

## 3. Production contract

The new boundary-specific API must:

1. reject any replay/version/context outside the exact existing R3.18AK/AJ authority;
2. validate/recompute the supplied R3.18AK result instead of trusting arbitrary caller coordinates;
3. require the resolved header tag to be exactly `ReplayNetworkAttributeTagV1::Int`;
4. require the payload start to equal the validated R3.18AK header/composition stop;
5. call the existing primitive scalar decoder for exactly one `Int` payload;
6. require exact 32-bit width and `ReplayNetworkPrimitiveScalarValueV1::Int` identity;
7. expose the exact payload start/end/width/value and retain the validated header composition;
8. set final `stop_bit` to exactly the payload end;
9. consume zero following `property_present` bits.

Every other payload tag/layout is fail-closed even if a lower-level decoder can parse it elsewhere.

## 4. Required focused tests

At minimum:

- exact real frozen witness coverage sufficient to prove the admitted boundary plus deterministic equality with the existing lower scalar decoder;
- `Int/32` exact start/end/value and final stop equality;
- deterministic repeatability;
- truncation before all required payload bits rejects;
- wrong resolved tag rejects;
- payload-start/header-stop mismatch rejects;
- corrupt/mismatched R3.18AK prior rejects;
- wrong actor / unresolved lookup / wrong exact version context rejects through prerequisite recomputation;
- fabricated Cartesian AJ tuple and old Z/P-only context reject;
- post-payload-end poison, including the following control bit, leaves the result unchanged;
- following-control consumption remains 0.

Synthetic tests supplement but do not widen beyond the frozen AM authority.

## 5. Clean candidate

The clean production commit must contain only the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18AN test file. No workflow/helper, evidence artifact, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup may enter the production commit.

## 6. Validation and publication

Require Rust 1.85 format/check/test/clippy, focused AN tests, full `mimir-replay`, workspace tests, repository verification, exact clean-candidate CI, a single validation PR for the exact head, and force-free publication only after fresh-main ancestry verification. After publication require exact published-main SHA/tree readback and the unique natural push CI receipt. Before every dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse them instead of creating duplicates.

## 7. Hard stop

No following property-control bit, next header/payload, second control, generalized/repeated property loop/cursor, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
The bounded `Int/32` post-AK composition matches the R3.18AM authority, all focused/negative/full validation passes, and following-control consumption remains zero. Publish only this one-payload composition, then open R3.18AO as a separate published-production differential.

### Outcome B
Only a strict safe subset of the R3.18AM authority can be implemented without widening. Publish only that exact subset and rewrite AO to the actual production contract.

### Outcome C
Authority drift, unexplained payload mismatch, context/layout widening, later-control access, generic chaining or validation contradiction. Stop without publication.
