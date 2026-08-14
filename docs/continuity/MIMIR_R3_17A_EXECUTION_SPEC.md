# MIMIR — R3.17A Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17A — primitive scalar attribute wire-format evidence`
**Kind:** evidence-only / pinned oracle instrumentation
**Frozen production base:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`

## 1. Goal

Begin the roadmap's attribute-decoder family program with the smallest low-ambiguity scalar family. Measure real supported-corpus behavior before admitting a native payload contract.

Candidate tags:

```text
Boolean
Byte
Int
Int64
Float
Enum
```

A candidate tag with no usable observations remains unadmitted. Do not infer its wire format from naming similarity.

## 2. Corpus and oracle

```text
MIMIR production base: ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
supported replay lane: 47 exact replays
checked-in corpus identity rules: unchanged
oracle: nickbabcock/boxcars
oracle SHA: c70e77df7af81b436cb545d070bb90c82f562d0b
```

The oracle is observation-only and must not become a production dependency.

## 3. Evidence selection

Scan the exact supported lane for existing-actor property updates resolving to the candidate scalar tags. Record full occurrence counts before selecting bounded witness rows.

For each usable witness capture at least:

```text
replay identity
frame index / actor index or equivalent stable position
actor context object ID/name
property object ID/name
attribute tag
property payload start bit
property payload end bit
exact consumed width
raw bits or lossless raw value representation
decoded oracle value
any build/version gate relevant to wire shape
next structural cursor position needed to prove exact end
```

Preserve enough identity to reproduce each row independently.

## 4. Required questions

For every observed candidate tag determine, from evidence rather than assumption:

- exact bit width or value-dependent width;
- signedness / integer representation where relevant;
- endianness / bit order interaction;
- float representation and whether raw IEEE bits must be preserved for exact differential comparison;
- enum/object lookup dependence if `Enum` is not a simple scalar in all builds;
- truncation points that a future native decoder must fail closed on;
- whether the wire shape changes by build/version/object context.

## 5. Required aggregate report

At minimum:

```text
replays_total = 47
oracle_decode_success count
per-tag occurrence count
per-tag usable witness count
per-tag unique consumed widths
per-tag min/max or representative value distribution when meaningful
identity_error_count
oracle_error_count
bit_monotonicity_failure_count
unexpected_tag_shape_count
production_mutation_count = 0
Cargo_mutation_count = 0
corpus_mutation_count = 0
```

## 6. Hard stop

R3.17A may inspect payloads through the pinned oracle but must not:

```text
change production Rust
decode payloads natively in MIMIR
implement RigidBody / ActiveActor / Location / spatial families
iterate a native second property
advance native actor/frame loops
mutate lifecycle state
materialize raw game state or semantic events
open replay slicing / skill / teacher / runtime / export surfaces
change Cargo dependencies
change replay fixtures/corpus
```

## 7. Outcome rules

### Outcome A

At least one candidate scalar tag has reproducible, exact, non-contradictory wire evidence sufficient for a narrow contract; all observed candidate shapes are classified; production/Cargo/corpus mutation remains zero.

Proceed to `R3.17B — primitive scalar attribute contract admission`. The contract may admit only the tags actually supported by evidence.

### Outcome B

Evidence is real but one or more candidate tags have multiple/unclear shapes or insufficient observations. Split the smallest tag-specific evidence follow-up. Do not generalize.

### Outcome C

Oracle identity, cursor accounting, or prior property-header assumptions contradict current evidence. Stop and reopen the relevant earlier contract before any payload implementation.

## 8. Publication policy

Evidence branch only. Temporary instrumentation/scripts/workflows are not production. After Outcome A/B/C, admit only bounded decision/spec/continuity artifacts; production source remains exactly the frozen R3.16B SHA.
