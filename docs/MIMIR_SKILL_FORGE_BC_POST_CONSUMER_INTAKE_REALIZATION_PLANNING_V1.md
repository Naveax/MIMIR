# MIMIR Skill Forge BC Post-Consumer-Intake Realization Planning v1

## Purpose

This pass chooses the next single boundary after:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationResultV1`

The purpose is planning only. This pass does not implement replay-source actual-materialization, replay-source carrier discovery, replay-input locator logic, replay parsing, parser-success logic, raw-state payload parsing, `mimir_replay::ReplayInput` creation, or `mimir_export` widening.

## Family Scope

This planning pass is limited to the first prototype family:

- `low_boost_recovery`

The boundary remains receipt-bound to the already frozen low-boost-recovery BC specimen tuple. No generic all-family replay, raw-state, index, export, materialization, parser, or locator framework is introduced.

## Current Frozen Chain Summary

The trusted chain now establishes exactly these facts:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormContractV1` freezes the caller-admitted byte-backed source-form contract.
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationByteBackedCallerAdmittedSourceFormRealizationResultV1` binds non-empty caller-admitted replay bytes to the exact receipt-bound tuple.
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffContractV1` freezes an opaque replay-byte handoff below `mimir_replay::ReplayInput`.
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffRealizationResultV1` realizes that opaque handoff without parsing or locating anything.
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeContractV1` freezes downstream consumer intake of the already-realized opaque handoff.
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationOpaqueCallerAdmittedReplayByteHandoffConsumerIntakeRealizationResultV1` realizes only that consumer-intake marker.

The chain preserves:

- exact receipt-bound tuple identity
- lane and specimen ordering
- artifact ids
- anchored BC specimen file paths below the audited family root
- accepted reference windows
- opaque caller-admitted replay bytes
- deferred replay/materialization handle lineage

The chain does not prove:

- replay-source actual-materialization implementation success
- replay-source carrier discovery
- replay-input locator logic
- actual replay parsing
- parser-success semantics
- raw-state payload parsing
- `mimir_replay::ReplayInput` creation
- tensor/control materialization
- export-bundle integration

`source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` remain lineage and receipt anchors only. They are not replay paths or replay storage.

## Still-Closed Domains

The following domains remain closed:

- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- actual replay parsing
- parser-success logic
- raw-state payload parsing
- `mimir_replay::ReplayInput` creation
- export widening

The audit found no new Rust or artifact evidence that safely selects one of those domains for a contract-definition or realization pass.

## Exact Decision

Chosen outcome:

- Outcome A: a no-op planning boundary is still the most honest next step.

The exact next boundary chosen by this pass is:

- `post_consumer_intake_realization_planning_no_op_v1`

This is a planning boundary only. It records that the consumer-intake realization is the current truthful stopping point and that no still-closed domain is reopened in this pass.

## Why Only This Single Boundary Is Justified

The consumer-intake realization proves only that an opaque handoff object can be consumed as opaque bytes while preserving the receipt-bound tuple. It does not establish that the bytes are parser-ready, replay-file-equivalent, locatable, discoverable through a carrier, convertible into `mimir_replay::ReplayInput`, or exportable.

The current crate audit reinforces that stop:

- `mimir-skill` owns the family-specific opaque handoff and consumer-intake chain.
- `mimir-replay` exposes `ReplayInput` and an `UnsupportedReplayReader`, but no bundled parser and no justified bridge from this consumer-intake result to `ReplayInput`.
- `mimir-io` remains raw artifact read/write support and has no opaque caller-admitted replay-byte handoff surface.
- `mimir-export` remains export-bundle and execution-result infrastructure with no low-boost-recovery replay-byte handoff integration.
- `mimir-types` has no opaque caller-admitted replay-byte handoff DTO.

Choosing a contract-definition boundary now would require selecting one still-closed domain without a proven consumer semantics. Choosing a reopen-decision boundary for one domain would also be premature because the audit does not distinguish which domain should be first without inventing ordering:

- parser attempt from opaque bytes
- replay-source actual-materialization implementation from opaque bytes
- carrier discovery despite caller-admitted bytes
- locator logic despite no path contract
- raw-state payload parsing despite no parser-success boundary
- `ReplayInput` creation despite explicit closure
- export widening despite explicit prohibition

Therefore a no-op planning boundary is narrower and more truthful than a fake precise contract.

## Rust / Code Decision

No Rust changes are added.

Docs-only is more honest here because the next semantic boundary is not proven. Adding Rust would create public API surface without a defensible domain selection and would risk silently implying parser, locator, carrier, `ReplayInput`, or export semantics that remain closed.

## What Remains Deferred

Deferred until explicitly reopened:

- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- actual replay parsing
- parser-success logic
- raw-state payload parsing
- `mimir_replay::ReplayInput` creation
- corpus-wide replay ingestion
- tensor/control materialization
- runtime CLI commands
- async/background systems
- database code
- real rollout physics
- export-bundle integration

## What Remains Forbidden

Forbidden in this pass and not reopened by this planning artifact:

- reinterpreting `source_replay` as a replay path
- reinterpreting `source_replay.provenance_label` as a replay path
- reinterpreting `audited_family_root_directory` as replay storage
- creating replay-source carrier discovery
- creating replay-input locator logic
- creating actual replay parsing
- creating parser-success logic
- creating raw-state payload parsing
- creating `mimir_replay::ReplayInput`
- widening `mimir_export`
- modifying `mimir-replay`
- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- reopening deterministic-family closure work
- creating a generic all-family replay/raw-state/index/export/materialization framework

## Relation To Next Stages

The immediate next pass should be another planning/reopen decision pass, not a contract-definition pass and not a realization pass.

That next pass must either:

- justify exactly one reopen-decision boundary for exactly one still-closed domain, or
- explicitly stop again if no single domain can be selected without inventing semantics.

`mimir_export` widening remains forbidden unless explicitly reopened.
