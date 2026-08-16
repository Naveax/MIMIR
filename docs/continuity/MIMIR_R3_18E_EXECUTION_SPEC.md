# MIMIR R3.18E — Production Control-Bit Real-Replay Differential Audit

**Status:** ACTIVE
**Pass type:** read-only differential audit
**Production mutation:** forbidden
**Second property decode:** forbidden
**Repeated property loop:** forbidden

## 1. Goal

Differentially validate the published R3.18D after-first-K1-property one-bit control result against pinned Boxcars on real replay witnesses. The pass may observe only the next `property_present` bit after one production-decoded R3.18B first property and must stop at the one-bit end.

## 2. Frozen production authority

```text
production SHA/tree                 4adadd185783954c7fb6ad67db14b77b377cdde5 / 67b1969eaff49d2913b88b3921f27b1bd7fe8193
production lib blob                 42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662
R3.18D focused test blob            2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b
implementation run/job              31945358707 / 95160386174 SUCCESS
exact candidate validator           31947511554 / 95165765329 SUCCESS
published main CI                   31947695046 / 95166220676 SUCCESS
published-main validator            31947722626 / 95166287502 SUCCESS
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane               47
R3.18C target classes               terminator + continuation
R3.18C frozen target rows           94 = 47 + 47
```

Before evidence work, fetch fresh `main`, verify the production SHA/tree/source/test blobs, and prove that any newer commits are continuity-only.

## 3. Oracle/witness policy

Use the same exact 47-replay identity lane and pinned Boxcars policy as R3.18C. Reconstruct deterministically, per replay, at most one eligible terminator witness and one eligible continuation witness after an R3.18B-compatible K1 first property. The expected reproduced target is 94 rows if the frozen corpus remains identical.

For every selected row record privacy-safe structural facts only: replay identity hash/path-relative identifier, frame/actor/property ordinals, actor context object, stream ID/bound, property object/tag, first-property payload start/end, oracle next-bit start/value/end, and the production result.

## 4. Native differential path

For each witness:

1. build the production lookup plan using existing admitted code;
2. run `decode_replay_network_existing_actor_single_primitive_property_v1` at the exact first-property start;
3. require its stop equals the oracle next `property_present` start;
4. run `decode_replay_network_existing_actor_after_first_primitive_property_control_v1`;
5. compare control start, boolean value, end and stop exactly;
6. stop. Do not read a second stream/header/payload bit.

## 5. Required aggregate gates

```text
replay identity / oracle parse      47/47
terminator target rows              47
continuation target rows            47
total selected rows                 94
native first-property success       94/94
native control success              94/94
first stop == oracle next start     94/94
control start exact                 94/94
control boolean exact               94/94
control end/stop exact              94/94
native/oracle mismatch              0
second stream/header/payload bits   0/0/0
privacy                             PASS
production/Cargo/fixture/corpus/
support mutation                    0/0/0/0/0
```

If deterministic reconstruction of the frozen 94 rows differs, stop and classify the drift before changing the target.

## 6. Negative controls

At minimum prove:

- truncate exactly before the next control bit: fail closed;
- mutate bits strictly after the one-bit stop: result unchanged;
- repeat the same selected witness: result exact;
- malformed first-property boundary: reject before the control read.

No negative may be used as a pretext to decode a second property.

## 7. Evidence artifact

Emit an immutable privacy-safe artifact containing source/production authority receipts, replay identity manifest, pinned Boxcars instrumentation receipt, selected witnesses, native/oracle comparison rows, aggregate summary, negatives and file hashes. Record the GitHub artifact ID and digest.

## 8. Validation

Required:

- exact authority-head workflow SUCCESS;
- same-head normal CI SUCCESS;
- production/Cargo/fixture/corpus/support mutation zero;
- privacy scan PASS;
- exact 94-row aggregate gates above;
- full repository verifier PASS where the evidence workflow uses repository code.

## 9. Outcome gate

### Outcome A

All 94 reproduced real-replay rows match the published R3.18D result exactly with zero mismatch and zero second-property consumption. Close R3.18E and only then define a separate read-only second-property-header evidence pass.

### Outcome B

A bounded production/oracle discrepancy exists. Record the exact class and keep second-property admission closed.

### Outcome C

Authority drift, corpus drift, privacy failure, production mutation, scope widening, or any second-property consumption. Stop without admission.

## 10. Hard stop

R3.18E does not admit second-property stream/header/payload decoding, repeated property loops, K2/K3/K4 wrapper widening, actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill/runtime/export behavior, or production dependency changes.
