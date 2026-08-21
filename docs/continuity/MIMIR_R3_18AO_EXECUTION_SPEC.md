# MIMIR R3.18AO — Published R3.18AN Post-AK Following-Payload Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Canonical production:** R3.18AN `3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38` / `3efcc244bca55623b12bb21eb277753fc61144d4`
**Evidence authority:** R3.18AM `842b94ed4c4e57323433585fea48116ecf18989b` / 47 frozen rows
**Production mutation:** forbidden
**Next property-control bit:** forbidden

## 1. Goal

Differentially validate the published R3.18AN bounded post-AK payload API over exactly the immutable R3.18AM witness lane. Prove the published composition itself through one exact `Int/32` payload end after the R3.18AK/R3.18AJ header boundary, then stop before the next `property_present` bit.

## 2. Frozen authority

```text
R3.18AN production                   3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38 / 3efcc244bca55623b12bb21eb277753fc61144d4
R3.18AN lib/test blobs               9d6b5ae2898cee745a17de9d1d7ef4b8fbd0e822 / 8aa48b2b74d0956d1d2e965d056e1cf14a81f703
R3.18AN builder                      32517430779/96882095196 SUCCESS
R3.18AN validation CI                32517915620/96883593252 SUCCESS / PR #192 closed unmerged
R3.18AN published-main CI            32518304295/96884776442 SUCCESS
R3.18AN published discovery          32519544607/96888554951 SUCCESS / CI count 1 / KA count 0
R3.18AJ contract                     sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AM evidence                     842b94ed4c4e57323433585fea48116ecf18989b / artifact 9443581172
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
witness reselection                  0
```

## 3. Frozen lane

Reuse exactly the 47 R3.18AM witnesses. Do not reselect replay, actor, property, bit coordinate, header context or payload. R3.18AM determines the complete observed identities. No Cartesian widening and no inheritance from earlier payload contracts.

## 4. Required per-row checks

For each frozen row:
1. reconstruct the exact prerequisite chain required by published R3.18AN from the same witness;
2. invoke published R3.18AN exactly once;
3. require embedded/recomputed AK identity equal to frozen authority through `payload_start`;
4. require full header tuple exact R3.18AJ membership;
5. require payload tag `Int`, start, end, width 32 and privacy-safe typed value equal R3.18AM plus independent direct-native/oracle observation;
6. require final `stop_bit == payload_end`;
7. repeat and require deterministic equality;
8. prove zero reads of the next property-control bit.

Outcome A requires 47/47 exact and mismatch zero.

## 5. Negative controls

Require atomic rejection for payload truncation, wrong actor, unresolved lookup, wrong exact version/context, malformed/non-AJ header tuple, corrupt AG/control/prior authority, wrong payload start, unsupported payload tag/layout, a fabricated tuple and an older Z/P-valid but AJ-absent context. Poison beginning exactly at R3.18AN `stop_bit`, including the next control bit, must not alter the result.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact recording exact AN/AM/AJ authorities and receipts, frozen witness identities, per-row AM/direct-native/oracle/published-AN comparison, payload coordinates and values, negative controls, repeatability, next-control counter, mutation counters, privacy result and SHA-256 manifest. Production/Cargo/fixture/corpus/support mutation must remain `0/0/0/0/0`.

## 7. Validation

Run focused AO evidence tests, permanent AN and prerequisite regressions, `cargo fmt --check`, workspace check/clippy/test, repository verifier and same exact evidence-head normal CI. Before triggering anything, refuse an equivalent queued/waiting/in-progress run. Use at most one validation-only PR for the exact evidence head and close it unmerged after SUCCESS.

## 8. Hard stop

No production mutation, witness reselection, next property-control read, alternate payload widening, generic/repeated cursor/loop, next actor/frame/lifecycle, raw-state/event/slice/skill/counterfactual/runtime/export widening.

## 9. Outcome gate

### Outcome A
Published R3.18AN matches exact frozen R3.18AM on 47/47 through one payload end; mismatch 0; witness reselection 0; next-control consumption 0; all negatives/validation/privacy gates PASS; production mutation 0. Admit only the differential. A later separate pass may investigate exactly one next property-control bit.

### Outcome B
A reproducible published-AN versus frozen-AM/oracle mismatch exists inside the already-admitted AN shape. Record privacy-safe coordinates and keep later boundaries closed.

### Outcome C
Authority drift, witness reselection, payload/context widening, production mutation, privacy failure, next-control access or validation contradiction. Stop without admission.
