# MIMIR — R3.17E Execution Spec

**Date:** 2026-08-14
**Pass:** `R3.17E — object/reference/text attribute wire-format evidence`
**Kind:** evidence-only / pinned oracle instrumentation
**Production Rust change:** forbidden

## 1. Goal

Begin roadmap wave K2 only after K1 primitive scalar closure. Candidate tags:

```text
ActiveActor
String
QWordString
UniqueId
PartyLeader
```

Measure real supported-corpus behavior before admitting any native contract. A candidate tag with zero usable observations or unresolved multiple shapes remains unadmitted.

## 2. Frozen production and corpus

```text
production SHA             c3d4c73ca34febb9f0383c59132a8bc8a363b06b
source blob                54e1bfb918ec1bd42a61cfa0131ca27412082ac5
supported replay lane      exact existing 47 replays
oracle                     nickbabcock/boxcars
oracle SHA                 c70e77df7af81b436cb545d070bb90c82f562d0b
```

The oracle is observation-only and must not become a production dependency.

## 3. Evidence procedure

Scan the full exact 47-replay lane and record complete occurrence counts for all five candidate K2 tags before witness selection. Freeze bounded witnesses per actually observed shape, preserving replay identity and stable frame/actor/property context.

For each usable occurrence capture enough information to reproduce independently:

```text
replay identity
frame/actor/property stable context
actor context object ID/name
property object ID/name
attribute tag
payload start bit
payload end bit
exact consumed width
lossless raw bytes/bits or structural field values
oracle decoded value
version/build/net-version fields relevant to shape
next structural cursor bit
```

## 4. Questions that evidence must answer

Do not infer these from names:

- `ActiveActor`: exact flag/reference structure, actor-ID representation/bounds, null/absent forms and build gates;
- `String`: exact length/encoding/termination rules, narrow vs wide text branches, empty string behavior and malformed lengths;
- `QWordString`: whether the observed form is fixed-width, string-like, integer-backed or version/context dependent;
- `UniqueId`: exact platform/type discriminants, payload branches, optional fields, lengths and version gates;
- `PartyLeader`: exact optional/null behavior and whether it reuses `UniqueId` encoding identically in all observed contexts;
- exact truncation boundaries for every observed shape;
- whether any tag has more than one wire shape across the supported lane.

## 5. Required aggregate

At minimum:

```text
replays_total = 47
oracle_decode_success count
per-tag occurrence count
per-tag replay count
per-tag usable witness count
per-tag unique wire shapes / widths
identity_error_count
oracle_error_count
bit_monotonicity_failure_count
shape_mismatch_or_unclassified_count
production_mutation_count = 0
Cargo_mutation_count = 0
corpus_mutation_count = 0
```

## 6. Hard stop

R3.17E may observe K2 payloads through the pinned oracle but must not:

```text
change production Rust
implement any native K2 decoder
decode or implement K3 Location/RigidBody/ReplicatedBoost/PickupNew
decode or implement K4 gameplay structured family
consume a native second property
iterate native next actor/frame
mutate lifecycle state
materialize raw game state or semantic events
open replay slicing / skill / teacher / runtime / export surfaces
change Cargo dependencies
change replay fixtures/corpus/support lane
```

## 7. Outcome rules

### Outcome A
At least one K2 tag has reproducible exact wire evidence sufficient for a narrow contract, every observed candidate shape is classified, and mutation counts remain zero. Open `R3.17F — object/reference/text attribute contract admission` for evidence-supported tags only.

### Outcome B
Evidence is valid but one or more observed tags have ambiguous/multiple shapes or insufficient support. Split the smallest tag/shape-specific evidence follow-up. Do not generalize.

### Outcome C
Oracle identity, cursor accounting or prior property-header assumptions contradict the current native boundary. Stop and reopen the smallest earlier contract before implementation.

## 8. Publication policy

Evidence branch only. Temporary oracle instrumentation, workflows and analyzers do not enter canonical production history. After Outcome A/B/C, admit only bounded decision/spec/continuity artifacts; production source remains frozen.
