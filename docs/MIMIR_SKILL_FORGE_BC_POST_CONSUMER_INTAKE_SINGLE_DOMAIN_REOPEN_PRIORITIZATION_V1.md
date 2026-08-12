# MIMIR Skill Forge BC Post-Consumer-Intake Single-Domain Reopen Prioritization v1

## Purpose

This pass is a narrow planning and reopen-decision pass after:

- `post_consumer_intake_realization_planning_no_op_v1`

Its sole job is to decide whether exactly one still-closed domain can now be justified as the
uniquely correct next reopen target for the low-boost-recovery prototype family.

This pass does not implement replay-source actual-materialization, replay-source carrier
discovery, replay-input locator logic, actual replay parsing, parser-success logic, raw-state
payload parsing, `mimir_replay::ReplayInput` creation, corpus-wide ingestion, rollout physics,
runtime commands, database code, async/background systems, or export widening.

## Family Scope

The only family in scope is:

- `low_boost_recovery`

The boundary remains receipt-bound to the already audited low-boost-recovery BC specimen tuple.
No generic all-family replay, raw-state, locator, parser, materialization, index, or export
framework is reopened.

## Current Frozen Chain Summary

The trusted chain currently establishes exactly this ordered receipt-bound path:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormContractV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationResultV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeContractV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationResultV1`

That chain proves only:

- exact receipt-bound tuple preservation
- lane and specimen order preservation
- artifact-id preservation
- anchored BC specimen paths under the audited low-boost-recovery family root
- accepted reference-window preservation
- non-empty caller-admitted replay bytes preserved as opaque payload
- consumer-intake realization of that opaque handoff

That chain still does not prove:

- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- actual replay parsing
- parser-success logic
- raw-state payload parsing
- `mimir_replay::ReplayInput` creation
- export widening

`source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` remain
lineage and receipt anchors only. They are not replay paths, replay storage, locator inputs, or
parser-readiness proof.

## Re-Audit Notes

The pre-edit audit inspected the required frozen-chain docs, executor decision/next/status
artifacts, staged-delivery rules, artifact-versioning and data-contract docs, current crate
surfaces, and dependency edges.

The crate audit found:

- `mimir-skill` owns the family-specific low-boost-recovery chain through opaque caller-admitted
  replay-byte handoff consumer-intake realization.
- `mimir-skill` also contains older blocked or deferred replay-input, replay-source, and parse
  surfaces, but those older surfaces are not evidence that the current post-consumer-intake chain
  proves parser readiness, locator success, carrier discovery, actual materialization, or
  `ReplayInput` creation.
- `mimir-replay` exposes `ReplayInput` and `UnsupportedReplayReader`; it does not expose a bundled
  parser or a proven bridge from the consumer-intake realization result.
- `mimir-io` owns raw artifact read/write helpers and family-specific low-boost-recovery BC
  specimen-file IO. It has no opaque replay-byte handoff parser, locator, carrier discovery, or
  export integration surface.
- `mimir-export` owns export-bundle and execution-result infrastructure. It has no
  low-boost-recovery opaque replay-byte handoff bundle semantics, and widening it remains
  forbidden.
- `mimir-types` contains lineage DTOs and low-boost-recovery BC persisted/emitted artifact DTOs,
  but no shared DTO that turns opaque caller-admitted bytes into parser output, raw-state payload,
  `ReplayInput`, or export entries.
- Current dependency edges keep `mimir-skill` dependent on `mimir-core`, `mimir-io`,
  `mimir-types`, and `serde`; it does not depend on `mimir-replay` or `mimir-export`.

## Still-Closed Domains

The still-closed candidate domains are:

- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- actual replay parsing
- parser-success logic
- raw-state payload parsing
- `mimir_replay::ReplayInput` creation
- export widening

At most one of these may be selected by this pass.

## Prioritization Criteria

Each still-closed domain is evaluated against all criteria below:

1. Does the current audited chain provide a concrete input surface for that domain?
2. Does the current audited chain provide a concrete output expectation for that domain?
3. Can the domain be opened without silently opening another domain first?
4. Can the domain be opened without modifying forbidden crates?
5. Can the domain be opened without inventing replay path or storage semantics?
6. Can the domain be opened while staying strictly below parsing, locator, `ReplayInput`, or
   export if those are not the chosen domain?
7. Is this domain more directly justified than every competing domain?

## Per-Domain Analysis

### Replay-Source Actual-Materialization Implementation

- Concrete input surface: partial only. The current chain provides receipt-bound opaque
  caller-admitted bytes through consumer-intake realization.
- Concrete output expectation: no. The chain does not define what an implemented actual
  materialized replay source is above opaque bytes.
- Can open without silently opening another domain first: no. A true implementation would need a
  carrier, parser-consumable object, `ReplayInput`, or some other actual source semantics.
- Can open without modifying forbidden crates: not proven. The likely consumers would touch
  `mimir-replay`, `mimir-io`, or `mimir-export`, none of which may be changed here.
- Can open without inventing replay path or storage semantics: only if it stays byte-backed, but
  byte-backed actual-materialization semantics are not selected or proven by the chain.
- Can stay below parsing, locator, `ReplayInput`, and export: not cleanly. Actual-materialization
  implementation would need to define an actual consumer-visible source form.
- More directly justified than all competitors: no. It competes with direct byte parsing,
  `ReplayInput::Memory` creation, and a narrower carrier contract, and the current evidence does
  not distinguish them.

Result: not selected.

### Replay-Source Carrier Discovery

- Concrete input surface: no. The chain contains caller-admitted opaque bytes, not discoverable
  storage, carrier classes, manifests, sidecars, or paths.
- Concrete output expectation: no. No discovered-carrier shape is proven.
- Can open without silently opening another domain first: no. Discovery requires carrier semantics
  and likely locator/storage rules.
- Can open without modifying forbidden crates: not proven.
- Can open without inventing replay path or storage semantics: no. Discovery would be forced to
  reinterpret `source_replay`, `source_replay.provenance_label`, `audited_family_root_directory`,
  or an unproven sidecar/manifest as storage.
- Can stay below parsing, locator, `ReplayInput`, and export: only by becoming a placeholder,
  which would not be a real discovery domain.
- More directly justified than all competitors: no. Caller-admitted bytes reduce the need for
  carrier discovery rather than uniquely justifying it.

Result: not selected.

### Replay-Input Locator Logic

- Concrete input surface: no. The chain has no replay path, replay storage root, file candidate,
  or `ReplayInput` object to locate.
- Concrete output expectation: no. The only existing `ReplayInput` type is in `mimir-replay`, but
  this chain does not justify producing it.
- Can open without silently opening another domain first: no. Locator logic needs path/storage or
  byte-to-input semantics first.
- Can open without modifying forbidden crates: not proven. `mimir-skill` currently has no
  `mimir-replay` dependency, and modifying `mimir-replay` is forbidden.
- Can open without inventing replay path or storage semantics: no if file-backed; unproven if
  memory-backed.
- Can stay below parsing, `ReplayInput`, and export: no. Locator logic is directly adjacent to
  `ReplayInput` semantics.
- More directly justified than all competitors: no. It is less direct than the existing opaque
  bytes and would require semantics the chain explicitly refuses to infer.

Result: not selected.

### Actual Replay Parsing

- Concrete input surface: partial only. Non-empty bytes exist, but they are explicitly opaque and
  not parser-ready by contract.
- Concrete output expectation: no. No parsed replay shape, header guarantee, event stream,
  raw-state window, error taxonomy, or parser-success schema is proven.
- Can open without silently opening another domain first: no. Parsing requires a parser surface and
  success/failure semantics.
- Can open without modifying forbidden crates: no honest route is proven. `mimir-replay` contains
  only `UnsupportedReplayReader`, and modifying it is forbidden.
- Can open without inventing replay path or storage semantics: yes for byte parsing in principle,
  but byte parser-readiness is not proven.
- Can stay below locator, `ReplayInput`, and export: possibly for a byte-only parse attempt, but
  the current chain does not choose that over other candidates.
- More directly justified than all competitors: no. Opaque bytes could feed parsing, but they could
  also feed `ReplayInput::Memory` creation or an actual-materialization boundary. The audit does
  not break that tie.

Result: not selected.

### Parser-Success Logic

- Concrete input surface: no. There is no actual parser attempt result in the trusted current
  chain.
- Concrete output expectation: no. Parser success cannot be defined without a parser result shape.
- Can open without silently opening another domain first: no. Actual replay parsing must precede
  parser-success logic.
- Can open without modifying forbidden crates: not proven.
- Can open without inventing replay path or storage semantics: maybe, but irrelevant because no
  parser attempt exists.
- Can stay below parsing: no. Parser-success logic is downstream of parsing.
- More directly justified than all competitors: no. It is downstream of actual replay parsing.

Result: not selected.

### Raw-State Payload Parsing

- Concrete input surface: no. The current chain has opaque replay bytes but no parsed replay data
  or raw-state payload.
- Concrete output expectation: no. No raw-state payload schema, ordering, frame semantics,
  normalization, or failure taxonomy is proven.
- Can open without silently opening another domain first: no. It needs replay parsing and
  parser-success semantics first.
- Can open without modifying forbidden crates: not proven.
- Can open without inventing replay path or storage semantics: not enough; it would invent
  payload semantics instead.
- Can stay below parsing: no. It is downstream of parsing.
- More directly justified than all competitors: no. It is downstream of parser success.

Result: not selected.

### `mimir_replay::ReplayInput` Creation

- Concrete input surface: partial only. The chain has non-empty opaque bytes and receipt-bound
  lineage.
- Concrete output expectation: partial only. `mimir-replay` exposes `ReplayInput::Memory`, but the
  trusted chain does not define a label, ownership rule, creation boundary, or bridge from
  consumer-intake realization to `mimir_replay::ReplayInput`.
- Can open without silently opening another domain first: not proven. Creating `ReplayInput` from
  bytes would compete with actual-materialization and parser-entry semantics.
- Can open without modifying forbidden crates: it might avoid modifying `mimir-replay`, but it
  would require new dependency/interface choices in `mimir-skill` that are not justified by this
  pass.
- Can open without inventing replay path or storage semantics: yes for memory input in principle,
  but the required label and semantics are not frozen by the chain.
- Can stay below parsing, locator, and export: possibly, but only by creating a new semantic bridge
  that the current audit does not uniquely justify.
- More directly justified than all competitors: no. It is a plausible future domain but not more
  directly justified than byte parsing or actual-materialization semantics.

Result: not selected.

### Export Widening

- Concrete input surface: no export input surface is proven by the current chain.
- Concrete output expectation: no. No bundle, manifest, index, sidecar, or schema widening is
  selected.
- Can open without silently opening another domain first: no. Export would need a consumer-ready
  payload semantics, not just opaque bytes.
- Can open without modifying forbidden crates: no. It would modify `mimir-export`, which remains
  forbidden unless explicitly reopened.
- Can open without inventing replay path or storage semantics: not enough; it would invent export
  semantics.
- Can stay below parsing, locator, `ReplayInput`, and export: no. It is export.
- More directly justified than all competitors: no. It is explicitly downstream and forbidden.

Result: not selected.

## Exact Decision

Chosen outcome:

- Outcome A: no single closed domain is yet uniquely justified; remain at a planning/no-op stop
  again.

No domain is selected.

This pass records that the current consumer-intake realization is still the truthful stopping
point. The available evidence does not distinguish one still-closed domain as uniquely prior
without inventing semantics.

## Why No Domain Wins Honestly

The current chain provides one concrete thing: receipt-bound opaque caller-admitted bytes consumed
through a family-specific consumer-intake realization.

That fact is insufficient to choose exactly one next domain because:

- opaque bytes do not prove parser readiness
- opaque bytes do not prove replay-file equivalence
- opaque bytes do not prove carrier discovery semantics
- opaque bytes do not prove locator semantics
- opaque bytes do not prove `ReplayInput` readiness
- opaque bytes do not prove raw-state payload availability
- opaque bytes do not prove export semantics
- existing older blocked `mimir-skill` surfaces do not override the current trusted boundary
- `mimir-replay`, `mimir-io`, `mimir-export`, and `mimir-types` do not contain a current bridge
  that selects one candidate over the others

Outcome B would require selecting exactly one reopen-decision domain, but every candidate either
lacks a concrete output expectation, silently opens another domain, touches forbidden crate
territory, invents storage/path semantics, or fails to outrank competitors.

Outcome C would require an already-justified direct contract-definition boundary. No such boundary
is proven by the current chain.

Docs-only is therefore more honest than Rust changes. Adding Rust here would create API surface
for a domain that this pass refuses to select.

## What Remains Deferred

Deferred until explicitly reopened:

- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- actual replay parsing
- parser-success logic
- raw-state payload parsing
- `mimir_replay::ReplayInput` creation
- tensor/control materialization
- corpus-wide replay ingestion
- real rollout physics
- async/background systems
- database code
- runtime CLI commands
- execution-result cleanup boundary changes
- export-bundle integration

## What Remains Forbidden

Forbidden by this pass:

- reinterpreting `source_replay` as a replay path
- reinterpreting `source_replay.provenance_label` as a replay path
- reinterpreting `audited_family_root_directory` as replay storage
- implementing replay-source actual-materialization
- implementing replay-source carrier discovery
- implementing replay-input locator logic
- implementing actual replay parsing
- implementing parser-success logic
- implementing raw-state payload parsing
- creating `mimir_replay::ReplayInput`
- widening `mimir_export`
- modifying `mimir-replay`
- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- reopening deterministic-family closure work
- silently reopening sidecar or manifest realization
- creating a generic all-family replay/raw-state/index/export/materialization framework

## Relation To Next Stages

The immediate next pass should be another planning/no-op stop unless new explicit evidence or a
new explicit external requirement is introduced.

That next pass must not silently choose a domain. It must either:

- stop again with no selected domain, or
- justify exactly one selected domain under an explicit reopen-decision pass.

`mimir_export` widening remains forbidden unless explicitly reopened.
