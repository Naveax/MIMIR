# MIMIR R3.18D — Production Decision

**Outcome:** **A — ADMITTED / PRODUCTION COMPLETE**
**Production SHA:** `4adadd185783954c7fb6ad67db14b77b377cdde5`
**Production tree:** `67b1969eaff49d2913b88b3921f27b1bd7fe8193`
**Previous canonical main:** `e9f3c4d34ebd84fc9c51431ad4489c4d407b1535`

## 1. Decision

R3.18D publishes the smallest production capability justified by R3.18C. After one already-valid R3.18B first K1 property result, MIMIR may read exactly the next `property_present` bit at the first property's stop bit and stop one bit later.

This is a control observation, not a second-property decoder and not a generalized property loop.

## 2. Published API boundary

Production now exposes an after-first-primitive-property control result containing:

```text
next_property_present
property_present_start_bit
property_present_end_bit
stop_bit
```

The implementation validates the R3.18B first-property boundary, requires header/scalar/end invariants to agree, reads exactly one bit with the existing private LSB-first cursor, and requires `stop_bit == property_present_end_bit == property_present_start_bit + 1`.

## 3. Exact production identity

```text
production SHA                     4adadd185783954c7fb6ad67db14b77b377cdde5
production tree                    67b1969eaff49d2913b88b3921f27b1bd7fe8193
lib.rs blob                        42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662
focused test blob                  2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b
clean production files             2
Cargo/fixture/corpus/support/
workflow/continuity mutation       0/0/0/0/0/0
```

## 4. Validation receipts

```text
implementation                     31945358707 / 95160386174 SUCCESS
exact clean-candidate validator    31947511554 / 95165765329 SUCCESS
published main normal CI           31947695046 / 95166220676 SUCCESS
published-main validator           31947722626 / 95166287502 SUCCESS
```

All required focused R3.18D tests, full `mimir-replay`, workspace check/test/clippy and full repository verifier passed.

## 5. Source boundary audit

The new control function contains exactly one `NetworkBitCursor::read_bit()` and no `read_bits_le`, bounded stream decoder, first-property-header decoder, single-property decoder, primitive scalar decoder, K2/K3/K4 decoder, or production `while`/`for` loop call.

Therefore the admitted consumption is exactly one next control bit. Second stream/header/payload consumption is `0/0/0`.

## 6. Still closed

- second property stream ID;
- second property header/tag resolution;
- second property payload;
- repeated/generalized property loop;
- K2/K3/K4 composition through the R3.18B wrapper;
- next actor/frame iteration;
- lifecycle/raw-state/event/replay-slice/skill/runtime/export widening.

## 7. Next pass

`R3.18E` is a separate read-only real-replay differential audit of the published one-bit control result. It must prove exact native/oracle start/value/end parity before any second-property header evidence is considered.
