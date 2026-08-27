# MIMIR R3.18AY — Bounded Post-AU One-Following-Payload Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production parent:** R3.18AU `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef`
**Header contract:** R3.18AT `sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5` / 16 exact eight-field tuples / multiplicity 40
**Payload evidence authority:** R3.18AW Outcome A / artifact `9643254651` / `sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc`
**Later-control evidence:** R3.18AX Outcome A / false=37 true=3 / artifact `9644869549` (evidence only; consumption forbidden in AY)
**Admitted payload family:** `Int / 32 bits` only

## 1. Goal

Publish exactly one boundary-specific payload composition after a valid R3.18AU true following-header result. The API must validate or recompute the supplied AU/AT authority, begin exactly at the validated `payload_start`, decode exactly one R3.18AW-admitted signed `Int` payload of 32 bits using existing primitive scalar machinery, return exact payload boundary/value identity, and stop exactly at payload end.

All seven R3.18AQ/AU false terminators remain outside the AY payload lane. The R3.18AX-observed following control bit must not be consumed. No generic cursor or repeatedly-chainable property loop is admitted.

## 2. Frozen authority

```text
R3.18AU production SHA/tree           6a9f456c78ffccab177823234a8d9fe4ba59a850 / cbda5db96e88cc208f872c2237cf4741b8fcfaef
R3.18AT exact-context contract        3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
R3.18AT contexts / multiplicity       16 / 40
R3.18AW evidence head                 5f1d983a7b67f84293f337f23b7e7c25fee48795
R3.18AW artifact                      9643254651 / sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc
R3.18AW payload identity              Int=40 / width32=40 / semantic range 5..300
R3.18AW native/oracle mismatch        0
R3.18AX evidence head                 465a3f2fc71e5eed6f00c16a04738031bef8d82c
R3.18AX artifact                      9644869549 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
R3.18AX next-control distribution     false=37 / true=3
R3.18AX control production authority  NONE
```

R3.18AW, not resemblance to R3.18AM/R3.18AN, is the payload authority for AY. R3.18AX proves the boundary after that payload but does not authorize AY to cross it.

## 3. Production contract

The new boundary-specific API must:

1. accept only a valid R3.18AU true following-header composition under exact R3.18AT membership;
2. reject the seven AU false-terminator results before any payload decode;
3. validate/recompute supplied AU prerequisites instead of trusting arbitrary caller coordinates;
4. require the resolved header tag to be exactly `ReplayNetworkAttributeTagV1::Int`;
5. require payload start to equal the validated AU header/composition stop;
6. call the existing primitive scalar decoder for exactly one `Int` payload;
7. require exact 32-bit width and `ReplayNetworkPrimitiveScalarValueV1::Int` identity;
8. expose exact payload start/end/width/value while retaining the validated AU header composition;
9. set final `stop_bit` to exactly payload end;
10. consume zero following `property_present` bits.

Every other payload tag/layout and every context outside exact AU/AT authority is fail-closed even if a lower-level primitive can decode it elsewhere.

## 4. Required focused tests

At minimum:

- exact 40 frozen AW true rows reproduce the admitted AU header and Int/32 payload boundary/value;
- all seven AU false terminators are rejected/excluded before payload decode;
- exact start/end/width/value and final stop equality;
- deterministic repeatability;
- truncation before all 32 payload bits rejects atomically;
- wrong resolved tag rejects;
- payload-start/header-stop mismatch rejects;
- corrupt/mismatched AU prior rejects;
- wrong actor / unresolved lookup / wrong exact version context rejects through prerequisite recomputation;
- fabricated Cartesian AT tuple and historical AJ/Z/P-only context reject;
- post-payload-end poison, including the AX control bit, leaves the AY result unchanged;
- following-control consumption remains 0;
- source-scope guard proves no generic/repeated loop or later-control read.

## 5. Clean candidate

Expected clean production scope is the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18AY integration test file. No workflow/helper/evidence artifact, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup enters the production commit.

## 6. Validation and publication

Require Rust 1.85 formatting, focused AY tests, workspace check, clippy with warnings denied, workspace test, repository verifier, exact clean-candidate natural CI, fresh-main ancestry verification, force=false publication and published-main exact-SHA validation. Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs; if an equivalent run exists, reuse that run ID. Rerun is never polling.

## 7. Hard stop

No R3.18AX following-control bit, next stream/header/payload, second later control, generalized/repeated property loop/cursor, next actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Publish exactly one AW-admitted Int/32 payload composition after valid AU/AT authority, with all focused/negative/full validations PASS and following-control consumption zero. Then open R3.18AZ as a separate published-production differential before any control-bit production is considered.

### Outcome B
Only a strict safe subset of the AW payload authority can be implemented without widening. Publish only that subset and rewrite the next differential pass to the actual production contract.

### Outcome C
Authority drift, unexplained payload mismatch, context/layout widening, AX control-bit access, generic chaining or validation contradiction. Stop without publication.
