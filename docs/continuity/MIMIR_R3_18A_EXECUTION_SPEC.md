# MIMIR R3.18A — Existing-Actor Single-Property Boundary Evidence

**Status:** ACTIVE
**Pass type:** read-only real-replay evidence
**Production mutation:** forbidden
**Roadmap parent:** R3.18 — one complete existing-actor property update

## 1. Goal

Prove one complete real existing-actor property update boundary end-to-end before any property-loop implementation is attempted.

The selected witness must have:

```text
new == false
property_present == true
already-resolved actor/class/cache context
bounded stream_id
resolved property object ID + admitted tag
payload_start_bit
exactly one already-admitted K1/K2/K3/K4 payload
payload_end_bit
```

Native and pinned Boxcars must agree on the resolved property identity/tag, payload start, semantic value under the already-admitted decoder contract, and exact payload end cursor.

## 2. Frozen authority

```text
continuity base main         19e3f558bd343372c7fe863822ab961fb10976ad
production SHA               492cc8218be7abc6db8f75acaea33d009ab2f175
production tree              a66c47d7fb58da508188e64d42141987a0021a07
R3.17P authority head        f2d87b732ad3103d50e2c047351f1017d4f3613f
R3.17P run/job               31937527114 / 95141677175 SUCCESS
R3.17P artifact              9261118033
R3.17P artifact digest       sha256:bc366b75e003531ba17351e880f259457ceba7cda702d912580c686990ba1beb
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47 exact replays
```

Before execution, fresh `main` must be re-read and the production source/test blobs must still match R3.17O. Any production drift requires re-audit before this spec may be executed.

## 3. Witness selection

Use the exact frozen supported replay lane and pinned Boxcars oracle. Scan read-only and deterministically choose a real existing-actor update whose first property tag is already admitted by current production.

Selection must be reproducible from privacy-safe coordinates such as replay identity hash/path, frame index, actor ordinal/ID, property ordinal, stream ID, resolved property object ID/tag and exact bit offsets. Do not persist sensitive account/player/title clear text.

One canonical witness is sufficient for R3.18A because this pass proves the **single-property composition boundary**, not property-loop corpus coverage. Broader encountered-tag/loop requirements remain for the later R3.18 loop step.

## 4. Exact comparison contract

For the selected witness require:

```text
existing-actor branch             exact
property_present                  true / exact
bounded stream_id                 exact
resolved property object ID       exact
resolved attribute tag            exact
payload_start_bit                 exact
native one-value decode success   true
semantic value                    exact under its already-admitted family rule
payload_end_bit                   exact
cursor monotonicity               PASS
```

If the selected payload is a floating/vector family, reuse the already-frozen equality rule of the family that admitted it; do not invent a looser tolerance in R3.18A.

## 5. Atomicity and hard stop

The R3.18A probe must stop at `payload_end_bit` **before reading the next `property_present` bit**.

Forbidden in this pass:

- second property consumption;
- `property_present` loop continuation;
- next actor or next frame;
- actor-table/lifecycle mutation;
- new attribute family/shape/context admission;
- production Rust changes;
- Cargo, fixture, corpus or support-lane changes;
- raw-state, event, replay-slice, skill, runtime or export widening.

Malformed/truncated selected-property probes must fail atomically without reporting a successful end cursor.

## 6. Durable evidence

Persist only privacy-safe evidence:

```text
frozen source/oracle identities
selected replay identity hash/path from the frozen lane
frame + actor/property coordinates
stream/property/tag identity
payload start/end/width
payload hash, not private clear text
native/oracle equality booleans
negative-control result
mutation counters
artifact digest / receipt hashes
```

## 7. Outcome gate

### Outcome A

All of the following are required:

```text
fresh production identity                 PASS
selected real existing-actor witness      reproducible
property header identity                  exact
payload start                             exact
native one-value decode                   PASS
semantic comparison                       exact
payload end cursor                        exact
next property_present consumed            0 bits
malformed/truncated atomic negative        PASS
privacy                                   PASS
production/Cargo/fixture/corpus/support   0/0/0/0/0 mutations
normal CI on exact evidence head          SUCCESS
```

Only Outcome A may close R3.18A. The next pass may then admit the minimal production composition for one property update. **Property-loop continuation remains separately gated.**

### Outcome B

Evidence is valid but the selected boundary exposes an unresolved contract detail. Record it and keep production closed.

### Outcome C

Native/oracle disagreement, non-reproducible evidence, privacy failure, mutation, or invalid source identity. Stop and do not widen.
