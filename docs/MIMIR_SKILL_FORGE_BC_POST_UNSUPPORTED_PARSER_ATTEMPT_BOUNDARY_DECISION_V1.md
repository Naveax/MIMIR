# MIMIR Skill Forge BC Post-Unsupported Parser-Attempt Boundary Decision v1

## A. Purpose

This pass decides exactly one boundary above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingUnsupportedAttemptRealizationResultV1`

The decision is deliberately narrow. The current trusted result records an unsupported parser
attempt through the only available reader, but it does not create parser success, a replay header,
raw-state payloads, replay frames, semantic replay events, export data, replay-source carrier
materialization, carrier discovery, or replay-input locator output.

This pass chooses what can honestly happen next without pretending that unsupported reader behavior
is replay parsing.

## B. Family Scope

The only family in scope is:

- `low_boost_recovery`

This pass does not introduce a generic all-family replay, raw-state, index, export, parser,
locator, materialization, diagnostic, or reporting framework.

## C. Current Trusted Chain Summary

The current trusted boundary is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingUnsupportedAttemptRealizationResultV1`

That boundary sits above:

- the actual replay parsing contract
- the implementation-readiness decision
- the replay-input creation realization from opaque caller-admitted replay bytes
- the receipt-bound low-boost-recovery specimen/raw-state-window chain

The prior unsupported-attempt realization consumed the actual replay parsing contract and preserved:

- the ordered lane/specimen structure
- the exact receipt-bound tuple
- the exact `ReplayInput::Memory { label, bytes }`
- the exact opaque caller-admitted replay bytes
- the lineage anchors `source_replay`, `source_replay.provenance_label`, and
  `audited_family_root_directory` as lineage/receipt anchors only
- the configured reader marker `UnsupportedReplayReader`
- the unsupported/error result returned by `ReplayReader::read_header(&ReplayInput)`
- the explicit no-header outcome

The audited replay crate still exposes only:

- `ReplayInput::File(PathBuf)`
- `ReplayInput::Memory { label, bytes }`
- `ReplayHeader`
- `ReplayReader`
- `UnsupportedReplayReader`

The only audited `ReplayReader` implementation is:

- `impl ReplayReader for UnsupportedReplayReader`

That implementation returns an explicit error and produces no `ReplayHeader`.

## D. What The Unsupported-Attempt Realization Proves

The unsupported-attempt realization proves only:

- the actual replay parsing contract was consumed
- the contract-defined attempt input, output, and header-attempt object were revalidated
- the receipt-bound tuple was preserved
- exact `ReplayInput::Memory` labels were preserved
- exact `ReplayInput::Memory` bytes were preserved
- `UnsupportedReplayReader` was invoked through `ReplayReader::read_header(&ReplayInput)`
- unsupported/error behavior was recorded truthfully
- no `ReplayHeader` was produced
- parser-success logic remained closed
- raw-state payload parsing remained closed
- replay-source actual-materialization, carrier discovery, replay-input locator logic, and
  `mimir_export` widening remained closed

## E. What The Unsupported-Attempt Realization Does Not Prove

The unsupported-attempt realization does not prove:

- a real parser exists
- parser backend readiness
- parser success
- parser failure policy
- `ReplayHeader` availability
- raw-state payload availability
- replay frame availability
- semantic replay event availability
- replay-source actual materialization
- replay-source carrier discovery
- replay-input locator correctness
- export readiness
- corpus-wide replay ingestion readiness
- any runtime CLI or live runtime behavior

It also does not authorize treating:

- `source_replay` as a replay path
- `source_replay.provenance_label` as a replay path
- `audited_family_root_directory` as replay storage

## F. Candidate Downstream Domain Analysis

### 1. Real Parser Implementation External Requirement

- concrete input evidence from unsupported-attempt result: yes
- concrete output expectation: yes, an explicit external requirement for a real parser
  implementation before parser progress continues
- can open without fake parser readiness: yes
- can open without producing `ReplayHeader`: yes
- can open without parser-success policy: yes
- can open without raw-state parsing: yes
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: yes

Reason:

The chain has consumed and exercised the current scaffold reader. The result is unsupported/error.
The audited workspace still has no real parser backend. Any useful parser progress now requires a
deliberate external real-parser implementation requirement before code, backend contracts,
parser-success policy, raw-state parsing, frames, events, or export can honestly move.

### 2. Parser Backend Integration Contract

- concrete input evidence from unsupported-attempt result: partial, only that a reader surface was
  attempted and returned unsupported
- concrete output expectation: no, because no real backend candidate, capability model, ownership
  boundary, dependency policy, or parser product requirement is authorized here
- can open without fake parser readiness: only if extremely constrained
- can open without producing `ReplayHeader`: yes
- can open without parser-success policy: yes
- can open without raw-state parsing: yes
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

A backend integration contract before an explicit real-parser requirement would risk designing
around a nonexistent backend. The unsupported result proves the absence of parser capability, not
the shape of a future parser integration.

### 3. Parser-Success Policy

- concrete input evidence from unsupported-attempt result: no
- concrete output expectation: no
- can open without fake parser readiness: no
- can open without producing `ReplayHeader`: no useful policy can be grounded without parser output
- can open without parser-success policy: not applicable
- can open without raw-state parsing: yes, but still unjustified
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

Unsupported/error behavior is not parser-success input and must not be converted into success or
failure policy. There is no `ReplayHeader` and no parser output to classify.

### 4. Raw-State Payload Parsing

- concrete input evidence from unsupported-attempt result: no
- concrete output expectation: no
- can open without fake parser readiness: no
- can open without producing `ReplayHeader`: no
- can open without parser-success policy: no
- can open without raw-state parsing: not applicable
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

No parser output, replay frames, payload schema, or parsed replay state exists. Opening raw-state
payload parsing would be fake completeness.

### 5. Replay Frame Extraction

- concrete input evidence from unsupported-attempt result: no
- concrete output expectation: no
- can open without fake parser readiness: no
- can open without producing `ReplayHeader`: no
- can open without parser-success policy: no
- can open without raw-state parsing: no
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

No frame source exists because the only reader returned unsupported/error.

### 6. Semantic Replay Event Extraction

- concrete input evidence from unsupported-attempt result: no
- concrete output expectation: no
- can open without fake parser readiness: no
- can open without producing `ReplayHeader`: no
- can open without parser-success policy: no
- can open without raw-state parsing: no
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

Semantic events require parsed replay state or frame semantics. Unsupported reader behavior provides
neither.

### 7. Replay-Source Actual-Materialization Implementation

- concrete input evidence from unsupported-attempt result: no
- concrete output expectation: no
- can open without fake parser readiness: no useful parser-related output can depend on it here
- can open without producing `ReplayHeader`: yes, but unjustified
- can open without parser-success policy: yes, but unjustified
- can open without raw-state parsing: yes, but unjustified
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

The current chain is intentionally memory-backed through caller-admitted bytes. The unsupported
attempt does not create a replay-source carrier requirement or storage coordinate.

### 8. Carrier Discovery

- concrete input evidence from unsupported-attempt result: no
- concrete output expectation: no
- can open without fake parser readiness: yes, but unrelated to the proven unsupported result
- can open without producing `ReplayHeader`: yes
- can open without parser-success policy: yes
- can open without raw-state parsing: yes
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

No carrier source was admitted. The lineage fields remain lineage only.

### 9. Replay-Input Locator Logic

- concrete input evidence from unsupported-attempt result: no
- concrete output expectation: no
- can open without fake parser readiness: yes, but unrelated to the current input form
- can open without producing `ReplayHeader`: yes
- can open without parser-success policy: yes
- can open without raw-state parsing: yes
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

The preserved parser input is already `ReplayInput::Memory`. Locator logic is not needed to explain
or advance the unsupported-attempt result.

### 10. Export Widening

- concrete input evidence from unsupported-attempt result: no
- concrete output expectation: no
- can open without fake parser readiness: no
- can open without producing `ReplayHeader`: no useful export widening is justified
- can open without parser-success policy: no
- can open without raw-state parsing: no
- can open without forbidden crate changes in this pass: no, because `mimir_export` widening is
  explicitly forbidden
- more justified than competing candidates: no

Reason:

There is no parsed payload, header, frame list, event list, tensor, manifest extension, or
consumer-ready export surface.

### 11. Unsupported-Attempt Diagnostic/Reporting Boundary

- concrete input evidence from unsupported-attempt result: yes
- concrete output expectation: partial, a report could summarize the unsupported evidence only
- can open without fake parser readiness: yes
- can open without producing `ReplayHeader`: yes
- can open without parser-success policy: yes
- can open without raw-state parsing: yes
- can open without forbidden crate changes in this pass: yes
- more justified than competing candidates: no

Reason:

The unsupported-attempt realization result already records the configured reader, error message,
unsupported reason, no-header outcome, preserved memory identity, and closed downstream domains.
A separate diagnostic/reporting contract would mostly restate that evidence and would not address
the actual blocker: no real parser exists.

## G. Decision

Outcome B is selected.

A new explicit external requirement is needed for real replay parser implementation.

Reason:

The chain has reached the limit of scaffold-only `UnsupportedReplayReader`. The unsupported-attempt
realization is truthful, but it proves only unsupported behavior. Real parser work now requires
deliberate architecture/product authorization before any backend integration, parser-success
policy, `ReplayHeader` production, raw-state parsing, frame extraction, semantic event extraction,
or export widening can be opened.

## H. Why Competing Outcomes Lost

Outcome A loses because stopping is honest but less precise than recording the actual next
requirement. The useful conclusion from this pass is not silent no-op; it is that real parser
implementation must be explicitly required and authorized before parser progress continues.

Outcome C loses because a parser-backend integration contract before a real-parser requirement
would overfit a nonexistent backend. The unsupported result does not provide backend capability,
backend ownership, dependency policy, or parser output semantics.

Outcome D loses because a diagnostic/reporting boundary would duplicate evidence already carried by
the unsupported-attempt realization. It would not remove the blocker and would risk adding another
artifact layer that sounds like progress while the parser capability remains absent.

## I. Deferred

Deferred explicitly:

- real parser implementation
- parser backend integration contract definition
- parser-success policy
- `ReplayHeader` production
- raw-state payload parsing
- replay frame extraction
- semantic replay event extraction
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- corpus-wide replay ingestion
- runtime CLI commands
- async/background systems
- database code
- real rollout physics
- execution-result cleanup boundary changes
- generic all-family replay/raw-state/index/export/materialization frameworks
- `mimir_export` widening

## J. Forbidden Unless Explicitly Reopened

Still forbidden unless explicitly reopened:

- modifying `mimir-replay`
- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- widening `mimir_export`
- implementing a real parser in this pass
- implementing parser-success logic in this pass
- producing or synthesizing `ReplayHeader`
- parsing raw-state payloads
- extracting replay frames
- extracting semantic replay events
- implementing replay-source actual-materialization
- implementing replay-source carrier discovery
- implementing replay-input locator logic
- interpreting `source_replay` as a replay path
- interpreting `source_replay.provenance_label` as a replay path
- interpreting `audited_family_root_directory` as replay storage
- treating unsupported/error behavior as parser failure policy
- treating unsupported/error behavior as parser-success input

## K. Rust Or Code Changes

Rust/code changes are not justified for this pass.

Reason:

Outcome B is a boundary decision that declares the need for an explicit external real-parser
implementation requirement. Adding Rust here would either implement part of a future parser
integration boundary, duplicate the existing unsupported-attempt realization, or imply parser
readiness that does not exist.

This pass is docs/artifacts only.
