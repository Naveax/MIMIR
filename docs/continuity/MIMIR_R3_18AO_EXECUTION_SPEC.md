# MIMIR R3.18AO — Published R3.18AN Post-AK Following-Payload Differential (Preparatory)

**Status:** PREPARATORY / NON-CANONICAL / DEPENDENCY-GATED
**Parallel slot:** 5/5
**Target offset:** 4 from the R3.18AK frontier
**Preparation base:** published R3.18AK source commit `f20f529e3ada6e9a671ea91e5676a17a00770145` / tree `98c675811cca4e4d7f0122c762f371548c9266c2`
**Pass type:** read-only evidence / published-production differential validation
**Canonical publication:** FORBIDDEN until R3.18AK continuity plus R3.18AL, R3.18AM and R3.18AN are each canonically CLOSED on fresh `main`
**Production mutation:** forbidden
**Later property control:** forbidden

> Preparation only. This branch is not authority. The published R3.18AK source is now on `main`, but continuity at this base still names R3.18AK active and R3.18AG as the last admitted production milestone. Do not treat AK as canonically CLOSED until its decision/continuity/knowledge-graph publication is admitted.

## 1. Dependency chain

```text
R3.18AK  bounded post-AG following-header production
   -> R3.18AL  published-AK following-header differential
   -> R3.18AM  post-AK following-payload evidence
   -> R3.18AN  bounded post-AK following-payload production
   -> R3.18AO  published-AN following-payload differential  [TARGET]
```

This structure is supported by the already-admitted method patterns `AA->AB->AC->AD->AE`, `Q->R->S->T->U`, and `G->H->I->J->K`. Those passes provide method analogues only. They do not supply AO payload classes, widths, layouts or contexts.

## 2. Goal

Differentially validate the published R3.18AN bounded post-AK following-payload production API over the exact immutable R3.18AM authority lane. Prove the published composition itself through exactly one payload end after the R3.18AK/R3.18AJ header boundary, then stop before the next `property_present` bit.

R3.18AO must preserve exact R3.18AK header identity through `payload_start`, exact R3.18AJ seven-field membership, exact R3.18AM payload identities, zero witness reselection, exact `stop_bit == payload_end`, and zero next-control consumption.

## 3. Authority freeze before execution

Once prerequisites are canonical, fetch fresh `main` and freeze:

```text
R3.18AK canonical decision + production SHA/tree/blobs   <REQUIRED>
R3.18AJ contract SHA-256                                 cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AL exact evidence receipts                          <REQUIRED>
R3.18AM exact evidence head/tree/run/job/artifact        <REQUIRED>
R3.18AM frozen rows/contexts/payload distributions       <DISCOVER, DO NOT INFER>
R3.18AN production SHA/tree/lib/test blobs               <REQUIRED>
R3.18AN builder/clean-head/PR/published-main receipts    <REQUIRED>
pinned Boxcars oracle                                    c70e77df7af81b436cb545d070bb90c82f562d0b
witness reselection                                      0
```

Any disagreement between fresh authority and this planned pass shape stops execution and requires spec repair. Never inherit payload classes, widths or layouts from R3.18AC, R3.18S, R3.18I, R3.18Z or R3.18P.

## 4. Frozen lane

Reuse exactly the immutable R3.18AM witnesses. Zero replay, actor, property, coordinate, header-context or payload reselection is permitted. R3.18AM alone determines row count, observed R3.18AJ contexts, payload tags, widths/layout discriminators, privacy-safe semantic values, payload coordinates and oracle/native baseline.

Do not derive a Cartesian allowlist from component fields. Complete observed identities remain complete identities.

## 5. Published differential checks

For every frozen R3.18AM row:

1. reconstruct the exact prerequisite chain required by the published R3.18AN API from the same witness coordinates;
2. invoke the published R3.18AN API once;
3. require embedded/recomputed R3.18AK identity to equal frozen R3.18AL/R3.18AM authority through `payload_start`;
4. require the full header tuple to belong to exact R3.18AJ;
5. require payload tag, start, end, width, layout/version discriminators and privacy-safe typed value to equal R3.18AM plus the independent oracle/native observation;
6. require final `stop_bit` to equal exactly one payload end;
7. repeat identically and require deterministic equality;
8. stop without reading the next property-control bit.

Mismatch must be zero across the complete frozen lane for Outcome A.

## 6. Negative controls

At minimum require atomic rejection for prefix truncation through required payload boundaries, wrong actor, unresolved lookup, wrong exact replay/version context, malformed/non-R3.18AJ header tuple, and any payload tag/layout/context outside exact R3.18AM/R3.18AN admission even if a lower decoder can parse it. An older Z/P-valid context absent from AJ must reject.

Poison beginning at exact R3.18AN `stop_bit`, including the next `property_present` bit, must not change the one-payload result. Repeated invocation must be exactly identical. Synthetic negatives supplement but never replace the real frozen lane.

## 7. Immutable evidence artifact

Produce a privacy-safe artifact containing exact AK/AJ/AL/AM/AN authorities and receipts, frozen witness identities and zero-reselection proof, per-row AM/oracle/direct-native/published-AN comparison, discovered payload distributions, boundary checks, negative controls, next-control counter, mutation counters, privacy result, internal manifest and SHA-256 for every payload file.

Production/Cargo/fixture/corpus/support mutation must remain `0/0/0/0/0`.

## 8. Validation

Require deterministic double-run equality, full frozen AM identity, published AN versus AM mismatch `0`, exact AJ membership, exact AM payload distributions without widening, all negatives PASS, next-control bits consumed `0`, permanent AN and AK focused regressions PASS, full `mimir-replay`, workspace format/check/test/clippy, repository verifier, same exact evidence-head normal CI SUCCESS and privacy PASS.

Before any workflow trigger or validation-only PR, search the same SHA/workflow/input for queued/waiting/in_progress runs and reuse them. Use only one validation PR for an exact head and close it unmerged after SUCCESS.

## 9. Hard stop

R3.18AO may not mutate production, select new witnesses, widen AJ contexts, infer payload forms absent from AM, read/admit another property-control bit, expose a generic property loop/cursor, iterate next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactuals or widen runtime/export behavior.

## 10. Outcome gate

### Outcome A
Published R3.18AN matches exact frozen R3.18AM through one payload end with mismatch 0, witness reselection 0, next-control consumption 0, all negative/validation/privacy gates PASS and production mutation 0. Admit only the published-production differential. A later separate pass may investigate exactly one next property-control bit.

### Outcome B
A reproducible published-AN versus frozen-AM/oracle mismatch exists inside an already-admitted AN shape. Record privacy-safe coordinates and keep every later boundary closed.

### Outcome C
Authority drift, prerequisite contradiction, witness reselection, payload/context widening, production mutation, privacy failure, next-control access or validation contradiction. Stop without admission.

## 11. Revalidation before use

When R3.18AN becomes canonical, discard this branch as authority, fetch fresh `main`, read newly admitted AK through AN decisions/specs/receipts, compare this preparation against exact facts, replace every placeholder, and reconstruct the real target branch directly from the then-canonical parent. Do not cherry-pick stale-base authority claims.
