# MIMIR R3.18B — Minimal Native Existing-Actor Single-Property K1 Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18A Outcome A
**Property loop:** forbidden

## 1. Goal

Publish the smallest production composition that starts at an existing actor's first `property_present` bit, resolves one property with the already-published R3.16B header logic, decodes exactly one already-admitted K1 primitive scalar with the already-published R3.17C decoder, returns the exact payload end cursor, and stops.

This pass is glue between two already-authoritative native boundaries. It must not fork or reimplement either wire codec.

## 2. Frozen authority

```text
canonical main before pass   c5878cf755302fe52e9e67741486306cd30db059
production SHA               492cc8218be7abc6db8f75acaea33d009ab2f175
R3.18A authority head        12ee215fd843260d5ece14f27aa1171cb862f49e
R3.18A run/job               31941400273 / 95151024131 SUCCESS
R3.18A exact-head CI         31941400276 / 95151024211 SUCCESS
R3.18A artifact              9262129856
R3.18A artifact digest       sha256:295247a5f73159ac74539ffc5abf1eb2273fb6dc07a57f8b16976552a17b3ab8
selected real tag/value      Int / 62
selected payload bits        [10234,10266)
next property bits consumed  0
```

Before mutation, re-read fresh `main`. If production blobs differ from R3.17O or canonical main is no longer the R3.18A continuity parent, stop and re-audit ancestry.

## 3. Admitted production composition

The new narrow API may:

```text
input: network bytes + first-property start bit + existing actor object index + current lookup plan
→ call the existing R3.16B first-property header decoder
→ require property_present == true
→ require a resolved property object + resolved attribute tag + payload_start_bit
→ accept only Boolean / Byte / Enum / Float / Int / Int64
→ call the existing R3.17C primitive scalar decoder at that exact payload_start_bit
→ return header identity + scalar result + stop_bit
→ require stop_bit == scalar.payload_end_bit
```

It may not independently decode bounded stream IDs, reinterpret lookup inheritance, or copy the scalar wire implementation.

## 4. Fail-closed rules

Reject without successful composition on:

- `property_present == false`;
- unresolved/missing stream or property;
- resolved non-K1 tag, including every K2/K3/K4 tag;
- header truncation;
- payload truncation;
- start/range arithmetic failure.

The API must not read or inspect the bit at its returned `stop_bit`; poison bits after the payload must not affect the result.

## 5. Required tests

Focused tests must include:

```text
all six K1 tags                       positive
aligned + unaligned property start    positive
R3.18A-shaped Int=62 composition      positive
header fields preserved               exact
payload start/end/width/value         exact
stop_bit == payload_end_bit           exact
poison next-property/trailing bits     no effect
property absent                        reject
K2/K3/K4 resolved tag                  reject before payload dispatch
header truncation                      reject
payload truncation                     reject atomically
repeatability                          exact
```

Run the full `mimir-replay` suite, workspace check/test/clippy, and full repository verifier on the exact clean candidate SHA.

## 6. Production scope

Preferred clean production scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused R3.18B integration test under `crates/mimir-replay/tests/`

A separate source module is allowed only if direct source inspection shows it materially improves isolation without widening the API. No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane, runtime/export, or continuity file may enter the clean production commit.

## 7. Hard stop

R3.18B does **not** admit:

- a second property;
- reading the next `property_present` bit;
- a `property_present` loop;
- K2/K3/K4 dispatch through the new composition API;
- next actor or next frame;
- actor lifecycle table mutation;
- new attribute family/shape/context;
- raw-state/event/replay-slice/skill/runtime/export widening.

## 8. Outcome gate

### Outcome A

Clean production code implements only the boundary above, focused and full validation pass, exact production scope is audited, and publication is force-free. Then update continuity and open a separate **read-only property-loop evidence** pass.

### Outcome B

Implementation exposes a missing composition contract. Record it and keep production at R3.17O.

### Outcome C

Any native/oracle contradiction, source drift, unexpected mutation, or inability to preserve the hard stop. Stop without publication.
