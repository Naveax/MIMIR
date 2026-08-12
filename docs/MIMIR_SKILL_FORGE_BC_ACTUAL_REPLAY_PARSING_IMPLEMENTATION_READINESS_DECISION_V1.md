# MIMIR Skill Forge BC Actual Replay Parsing Implementation Readiness Decision v1

## A. Purpose

This pass is a narrow implementation-readiness decision above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`

The pass decides whether the next low-boost-recovery pass should realize the actual replay parsing
contract, and if so, what kind of realization is honest.

This pass does not implement replay parsing, does not execute `ReplayReader::read_header`, does not
produce `ReplayHeader`, does not classify parser success, and does not parse raw-state payloads.

## B. Family Scope

The only family in scope is:

- `low_boost_recovery`

The decision is limited to the existing receipt-bound low-boost-recovery BC chain above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationResultV1`

No generic all-family replay, parser, raw-state, index, export, materialization, or locator
framework is opened.

## C. Current Contract Summary

The current trusted boundary defines only a header-level parser-attempt contract:

- selected contract:
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`
- selected shape:
  `ReceiptBoundReplayHeaderParseAttemptFromMimirReplayMemoryInputOnly`
- selected attempt kind:
  `MimirReplayReaderReadHeaderFromReplayInputOnly`
- selected future parser surface:
  `mimir_replay::ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The contract preserves:

- the receipt-bound low-boost-recovery tuple
- ordered lane/specimen structure
- opaque caller-admitted replay bytes
- exact `ReplayInput::Memory { label, bytes }`
- lineage anchors including `source_replay`, `source_replay.provenance_label`, and
  `audited_family_root_directory`

The contract does not:

- execute replay parsing
- prove parser readiness
- produce `ReplayHeader`
- define parser-success policy
- parse raw-state payloads
- extract frames or semantic events
- implement carrier discovery, locator logic, or replay-source actual materialization
- widen `mimir_export`

## D. Audited Parser Implementation Surface

Audited files included:

- `docs/MIMIR_SKILL_FORGE_BC_ACTUAL_REPLAY_PARSING_CONTRACT_V1.md`
- `executor_mimir_skill_forge_bc_actual_replay_parsing_contract_decision.txt`
- `executor_mimir_skill_forge_bc_actual_replay_parsing_contract_next.txt`
- `executor_mimir_skill_forge_bc_actual_replay_parsing_contract_status.txt`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- `crates/mimir-skill/Cargo.toml`
- `crates/mimir-io/src/lib.rs`
- `crates/mimir-export/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- root `Cargo.toml`
- current `cargo tree -p mimir-skill`
- current `cargo tree -p mimir-replay`
- current `cargo metadata --format-version 1 --no-deps`

The actual `mimir-replay` surface is:

- `ReplayInput::File(PathBuf)`
- `ReplayInput::Memory { label, bytes }`
- `ReplayHeader`
- `ReplayReader`
- `UnsupportedReplayReader`

The only audited implementation of `ReplayReader` is:

- `impl ReplayReader for UnsupportedReplayReader`

Its `read_header` implementation always returns an explicit error:

- no replay parser is bundled in this scaffold

No real parser implementation was found in `mimir-replay` or the workspace crate sources.

Current dependency edges relevant to this decision:

- `mimir-skill` depends on `mimir-replay`, `mimir-io`, `mimir-types`, `mimir-core`, and `serde`
- `mimir-replay` depends only on `mimir-core`, `mimir-types`, and `serde`
- `mimir-replay` has no parser backend dependency
- no audited crate provides a second `ReplayReader` implementation

## E. Readiness Analysis

### A. Is there a real parser implementation available?

No.

The workspace search found only `UnsupportedReplayReader` implementing `ReplayReader`. There is no
real replay parser, no parser backend crate, and no alternate header reader.

`UnsupportedReplayReader` does not prove parser readiness.

### B. Can `ReplayReader::read_header(&ReplayInput)` be invoked truthfully in the next pass?

Yes, but only as an unsupported parser-attempt realization if the configured reader is explicitly
`UnsupportedReplayReader`.

That invocation would mean:

- a header parse was attempted through the configured reader surface
- the reader returned unsupported/error
- the result records the unsupported/error behavior
- no `ReplayHeader` is produced
- no parser-success policy is applied

It would not mean actual replay parsing is available.

### C. Can a realization result be truthful without parser success?

Yes.

A truthful unsupported parser-attempt realization can record exactly:

- the preserved contract attempt input
- the preserved `ReplayInput::Memory`
- the attempted configured reader surface
- the unsupported/error result from `read_header`
- that no header was produced
- that parser-success classification remains closed
- that raw-state payload parsing remains closed

The realization must not synthesize `ReplayHeader`, classify errors as success/failure policy, or
produce raw-state, frame, event, export, locator, or materialization outputs.

### D. Is a real parser implementation required before any realization?

No, not before an unsupported parser-attempt realization.

A real parser implementation is required before any real parser invocation realization, parser
success claim, `ReplayHeader` availability claim, raw-state parsing, frame extraction, semantic
event extraction, or export widening.

Stopping with no realization would also be honest, but it is not the narrowest useful next move
because the contract already binds a concrete memory-backed `ReplayInput` and a configured reader
surface can truthfully report unsupported behavior. The next pass may prove the attempt plumbing
without pretending a parser exists.

### E. Are parser-success, raw-state parsing, locator, carrier discovery, and export still downstream?

Yes.

The following remain downstream and closed:

- parser-success logic
- raw-state payload parsing
- replay frame extraction
- semantic event extraction
- replay-source actual materialization
- replay-source carrier discovery
- replay-input locator logic
- `mimir_export` widening

## F. Decision

Outcome B is selected.

A first realization pass is justified, but only as an unsupported parser-attempt realization that
records unsupported/error behavior truthfully and does not claim parser success.

## G. Allowed Realization Type

The next pass may realize only:

- `Unsupported parser-attempt realization for low_boost_recovery actual replay parsing contract v1`

The allowed behavior is:

- consume `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingContractV1`
- revalidate the contract-defined receipt-bound attempt objects
- preserve the exact `ReplayInput::Memory` labels and bytes
- invoke the configured `ReplayReader::read_header(&ReplayInput)` only if the realization result
  names that this is an attempted configured-reader call
- when the configured reader is `UnsupportedReplayReader`, record the returned unsupported/error
  result as unsupported parser-attempt behavior
- produce no `ReplayHeader`
- produce no parser-success classification

## H. Why Outcome C Is Rejected

Outcome C is rejected because no real parser implementation is available.

The existence of `ReplayReader::read_header` and `UnsupportedReplayReader` is not parser readiness.
Calling `UnsupportedReplayReader` would only prove that the unsupported reader returns unsupported
error behavior.

## I. Why Outcome A Is Not Selected

Outcome A would be honest, but it would leave the contract unexercised even though a truthful
unsupported-attempt realization can be narrowly defined.

The next pass can add audit value by proving the attempt boundary preserves its input and records
unsupported behavior without claiming parsing success.

## J. Why Outcome D Is Not Selected

Outcome D is not needed for unsupported-attempt realization.

An explicit external parser implementation requirement is required before real parser invocation,
parser success, `ReplayHeader` production, raw-state parsing, frame extraction, semantic event
extraction, or export widening. It is not required before recording unsupported behavior from the
only currently available reader.

## K. Rust Changes

No Rust changes are added in this pass.

Docs-only is more honest because this pass is a decision/planning pass. The existing Rust contract
already defines the header-attempt boundary. Adding Rust now would either duplicate the next
realization pass or risk implying parser execution that this pass explicitly does not perform.

## L. Deferred

Deferred explicitly:

- real parser implementation
- actual parser invocation with a real parser
- parser-success logic
- `ReplayHeader` production
- raw-state payload parsing
- replay frame extraction
- semantic event extraction
- replay-source actual materialization
- replay-source carrier discovery
- replay-input locator logic
- replay-source materialization from lineage anchors
- corpus-wide replay ingestion
- runtime CLI commands
- async/background systems
- database code
- real rollout physics
- execution-result cleanup boundary changes
- `mimir_export` widening

## M. Forbidden

Still forbidden unless explicitly reopened:

- modifying `mimir-replay`
- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- pretending `UnsupportedReplayReader` can parse
- producing fake `ReplayHeader`
- interpreting `source_replay` as a replay path
- interpreting `source_replay.provenance_label` as a replay path
- interpreting `audited_family_root_directory` as replay storage
- classifying parser success or failure policy
- parsing raw-state payloads
- extracting frames or events
- widening `mimir_export`
