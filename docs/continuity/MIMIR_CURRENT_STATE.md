# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical main / production checkpoint:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`
**Production milestone:** `R3.16B — native existing-actor first-property envelope header implementation`
**Completed continuity check:** `R3.16C`
**Next exact pass:** `R3.17A — primitive scalar attribute wire-format evidence`

---

## 1. Current truthful production boundary

MIMIR can natively advance through the admitted replay network prefix far enough to:

```text
frame time/delta
first actor present/id/alive/new envelope
NewActor name/object/spawn trajectory branch
existing-actor one-property-present decision
one canonical bounded stream_id
existing static/inherited property lookup resolution
resolved property object/tag metadata
payload_start_bit
```

Production then **stops before the first attribute payload bit**.

The R3.16B production result is intentionally a header/context primitive. It does not scan for later existing actors, iterate a property loop, mutate actor lifecycle state, or decode attribute values.

## 2. R3.16B admitted identity

```text
pre-pass canonical main       fc020729396ad9f62ee4b8fd8fe6808f5bdb5489
clean production SHA          ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
production source             crates/mimir-replay/src/lib.rs
source Git blob               625ab2322e35f5f835871d42b9efeb04f5c299ab
source SHA-256                186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28
permanent focused test        crates/mimir-replay/tests/r3_16b_property_header.rs
test Git blob                 0fea53e1758e7b0b5f8d2a14b98cbce5feb400c2
clean diff                    2 files, +331 / -0
focused tests                 8 / 8 PASS
frozen oracle rows            47
native differential           47 / 47 PASS
```

R3.16B reuses the canonical bounded-u32 primitive. `prop_id_bits` is not treated as a fixed-width permission; actual stream-ID consumption remains value/bound dependent.

## 3. R3.16B hosted validation and publication closure

```text
disposable full verifier + differential run/job  31787682424 / 94727174844  SUCCESS
candidate PR CI run/job                           31788230442 / 94728918384  SUCCESS
candidate Knowledge Archive run/job               31788291777 / 94729116078  SUCCESS
published-main CI run/job                         31788526050 / 94729854512  SUCCESS
published-main Knowledge Archive run/job           31788566184 / 94729983908  SUCCESS
publication                                        force=false fast-forward
```

The clean production commit contains only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_16b_property_header.rs` relative to its parent. Temporary evidence/publisher machinery did not enter canonical production history.

## 4. Current closed boundaries

Still closed:

```text
native attribute payload decoding of every tag
second property / property loop
complete existing-actor update parsing
next actor iteration
next frame iteration
actor lifecycle state-table mutation
raw-state materialization
semantic ball/car/player reconstruction
event extraction
replay slicing
skill mining
counterfactual rollout execution
training/runtime/export widening
support-lane expansion
```

Observed tag names are not payload contracts. In particular, seeing `RigidBody`, `ActiveActor`, `Byte`, `Float`, or `Int` in oracle evidence does not mean MIMIR can natively decode those payloads.

## 5. R3.17A exact next pass

R3.17A is evidence-only and begins the roadmap's attribute decoder family program with primitive scalar payloads:

```text
Boolean
Byte
Int
Int64
Float
Enum
```

The pass must use the pinned Boxcars revision and the exact supported 47-replay lane. It should measure actual occurrences first, then collect exact payload start/end bits, raw/decoded values, tag/object identity, and enough surrounding structure to define truncation/fail-closed rules later.

A tag with zero usable observations is **not admitted by analogy**. It remains closed or receives a targeted evidence follow-up.

R3.17A changes no production Rust. Outcome A may open `R3.17B — primitive scalar attribute contract admission`.
