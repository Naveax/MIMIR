# MIMIR Skill Forge BC Actual Replay Parsing Unsupported Attempt Realization v1

## A. Purpose

This pass realizes exactly one boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`

The realization is intentionally limited to an unsupported parser-attempt result. It proves that the
contract-defined attempt boundary can be revalidated, preserved, and exercised through the only
available configured reader without claiming parser success.

This pass does not implement replay parsing, does not produce `ReplayHeader`, does not define
parser-success policy, and does not parse raw-state payloads.

## B. Family Scope

The only supported family is:

- `low_boost_recovery`

The pass remains tied to the existing receipt-bound low-boost-recovery BC chain. It does not add a
generic all-family replay parser, raw-state, index, export, locator, carrier, or materialization
framework.

## C. Input Boundary

The input is exactly:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`

The realization consumes and revalidates:

- top-level contract disposition and note set
- selected actual replay parsing contract shape
- ordered lane/specimen structure
- artifact ids
- receipt-bound tuple fields
- `ReplayInput` creation bridge lineage
- parser attempt boundary input
- parser attempt boundary output
- parser attempt object
- exact `ReplayInput::Memory { label, bytes }`

The following remain lineage or receipt anchors only:

- `source_replay`
- `source_replay.provenance_label`
- `audited_family_root_directory`

They are not replay paths or replay storage.

## D. Realization Role

This realization owns only:

- revalidating the exact actual replay parsing contract result
- preserving the exact receipt-bound tuple
- preserving the exact `ReplayInput::Memory` label and bytes
- invoking the configured `ReplayReader::read_header(&ReplayInput)` only through
  `UnsupportedReplayReader`
- recording the returned unsupported/error behavior
- recording that no `ReplayHeader` was produced
- recording that parser-success logic and raw-state parsing remain closed

The selected configured reader is:

- `UnsupportedReplayReader`

That reader is invoked because the readiness decision selected Outcome B and the workspace contains
no real replay parser implementation. The invocation is evidence of unsupported-attempt plumbing
only.

## E. Unsupported-Attempt Realization Shape

The realization adds a low-boost-recovery-specific result surface in `mimir-skill`:

- `LowBoostRecoveryBcActualReplayParsingUnsupportedAttemptConfiguredReaderV1`
- `LowBoostRecoveryBcActualReplayParsingUnsupportedAttemptStatusV1`
- `LowBoostRecoveryBcActualReplayParsingUnsupportedAttemptReplayHeaderOutcomeV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingUnsupportedAttemptRealizationDispositionV1`
- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingUnsupportedAttemptRealizationNoteV1`
- per-specimen, lane, and top-level unsupported-attempt realization result structs

The selected configured reader value is:

- `UnsupportedReplayReader`

The selected attempt status is:

- `ConfiguredUnsupportedReplayReaderReturnedError`

The selected header outcome is:

- `NoReplayHeaderProduced`

The selected realization disposition is:

- `RealizedForUnsupportedParserAttemptOnly`

The per-specimen result preserves:

- contract parser attempt boundary input
- contract parser attempt boundary output
- contract parser header-attempt object
- exact memory-backed replay input carried by the attempt object
- configured reader marker
- unsupported attempt status
- no-header outcome
- returned parser-attempt error message
- deterministic unsupported reason

## F. Output Result Shape

The top-level result preserves:

- `specimen_count`
- `group_count`
- lower source contract disposition and notes
- audited family root directory as receipt anchor only
- lower source realization disposition and notes
- replay-input creation realization disposition and notes
- selected replay-input creation contract shape
- actual replay parsing contract disposition and notes
- selected actual replay parsing contract shape
- lane/specimen order
- all artifact ids
- all receipt-bound tuple fields through each per-specimen attempt object
- exact `ReplayInput::Memory` labels and bytes
- configured reader marker
- unsupported-attempt realization disposition and notes

It adds no replay header, no parser-success result, no raw-state payload, no frame list, no semantic
event list, no locator output, no carrier output, and no export output.

## G. Admission Rules

An actual replay parsing contract result is admitted only when all conditions hold:

1. source contract disposition and notes remain exact
2. source realization disposition and notes remain exact
3. replay-input creation realization disposition and notes remain exact
4. selected replay-input creation contract shape remains exact
5. selected actual replay parsing contract disposition, notes, and shape remain exact
6. `specimen_count > 0`
7. `group_count > 0`
8. `group_count` equals ordered lane count
9. every lane is non-empty
10. lane and specimen ordinals match concrete order
11. artifact ids remain unique
12. audited family root exists, is a directory, and ends in `low_boost_recovery_bc_v1`
13. each anchored specimen path remains below the audited family root and is not the root itself
14. each accepted reference window remains valid and bounded
15. each opaque replay byte payload remains non-empty
16. preserved deferred handle kinds remain exact
17. replay-input creation input, output, and bridge remain exact
18. actual replay parsing attempt input, output, and header-attempt object remain exact
19. every replay input involved in the attempt remains `ReplayInput::Memory`
20. every memory label is receipt-derived from artifact id, lane ordinal, and specimen ordinal
21. every memory byte payload equals the preserved opaque caller-admitted replay bytes

Admission means only that an unsupported configured-reader attempt may be recorded.

## H. Failure Rules

This realization hard-fails for:

- degraded notes
- disposition drift
- chosen-shape drift
- count drift
- empty lanes
- lane/specimen order drift
- duplicate artifact ids
- audited-root drift
- specimen path drift outside the audited root
- invalid accepted windows
- empty opaque replay bytes
- preserved handle-kind drift
- replay-input creation boundary or bridge drift
- actual replay parsing attempt boundary or object drift
- file-backed `ReplayInput`
- replay-input label drift
- replay-input byte drift
- any unexpected `ReplayHeader` from `UnsupportedReplayReader`
- any attempt to reinterpret lineage anchors as paths or replay storage

There is no repair behavior:

- no specimen skipping
- no lane resorting
- no byte synthesis
- no path guessing
- no fallback parser
- no success conversion

## I. Non-Goals

This pass does not implement:

- real replay parser support
- parser-success policy
- `ReplayHeader` production
- raw-state payload parsing
- replay frame extraction
- semantic replay event extraction
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- `mimir_export` integration or widening
- runtime CLI commands
- corpus-wide replay ingestion
- async/background systems
- database code
- real rollout physics
- execution-result cleanup changes
- generic all-family replay/raw-state/index/export/materialization infrastructure

This pass does not modify `mimir-replay`, `mimir-io`, `mimir-export`, or `mimir-types`.

## J. Relation To Next Stages

This pass proves only that the contract-defined header attempt boundary can be preserved and that
the configured unsupported reader behavior can be recorded truthfully.

It still does not prove:

- parser readiness
- parser success
- `ReplayHeader` availability
- raw-state payload availability
- replay frame extraction
- semantic event extraction
- replay-source actual materialization
- replay-source carrier discovery
- replay-input locator success
- export readiness

The immediate next pass should be a narrow post-unsupported-attempt boundary decision pass.

`mimir_export` widening remains forbidden unless explicitly reopened.
