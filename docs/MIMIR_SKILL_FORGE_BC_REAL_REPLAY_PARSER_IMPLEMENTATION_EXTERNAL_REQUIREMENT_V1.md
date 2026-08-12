# MIMIR Skill Forge BC Real Replay Parser Implementation External Requirement v1

## A. PURPOSE

This pass defines the external requirement above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowActualReplayParsingUnsupportedAttemptRealizationResultV1`

It follows Outcome B from the post-unsupported-attempt boundary decision:

- an explicit external requirement is needed for real replay parser implementation before parser
  progress continues.

This artifact opens only the requirement boundary for future real parser implementation work. It
does not implement the parser, does not define parser-success policy, does not produce a
`ReplayHeader`, and does not parse replay payloads.

The parser requirement scope selected by this pass is:

- Outcome A: require only a minimal real header parser backend.

The selected first parser target is exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

This requirement exists because the current chain has truthfully proven only scaffold unsupported
reader behavior. It has not proven parser readiness, parser success, header availability,
raw-state payload availability, frame extraction, semantic event extraction, replay-source
materialization, carrier discovery, locator correctness, or export readiness.

## B. FAMILY SCOPE

The current requirement is scoped to the low-boost-recovery chain first.

The admitted input evidence is low-boost-recovery-specific:

- receipt-bound low-boost-recovery BC specimen ordering
- accepted reference windows
- opaque caller-admitted replay bytes
- preserved `ReplayInput::Memory` labels and bytes
- unsupported-attempt realization results

The parser backend itself may later be implemented as a narrow shared `mimir-replay` capability
because Rocket League replay header parsing is not intrinsically a low-boost-recovery semantic
operation. That possible shared parser-crate or backend seam is justified only if it remains behind
the existing `mimir-replay` reader contract and does not create a generic all-family replay,
raw-state, frame, event, index, export, locator, carrier, or materialization framework.

The current requirement remains low-boost-recovery-scoped even if a later parser backend is shared.

## C. CURRENT BLOCKER

The current audited parser surface is scaffold-only.

`mimir-replay` exposes:

- `ReplayInput::File(PathBuf)`
- `ReplayInput::Memory { label, bytes }`
- `ReplayHeader`
- `ReplayReader`
- `UnsupportedReplayReader`

The only audited `ReplayReader` implementation is:

- `UnsupportedReplayReader`

The unsupported-attempt realization recorded that `UnsupportedReplayReader` was invoked through
`ReplayReader::read_header(&ReplayInput)` and returned an error. That result is truthful
unsupported behavior only.

No real parser output exists:

- no parser backend readiness
- no parser success
- no `ReplayHeader`
- no raw-state payload
- no replay frames
- no semantic replay events
- no replay-source materialization
- no carrier discovery
- no replay-input locator output
- no export-ready data

## D. EXACT REQUIREMENT

The exact external requirement is:

- implement or integrate a real replay parser backend capable of reading `ReplayInput::Memory`
- the first target is header-level parsing only
- the first parser implementation must make
  `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>` capable of returning a real
  `ReplayHeader` for valid supported replay bytes
- invalid, malformed, or unsupported bytes must return a structured error
- no fake, guessed, placeholder, padded, or synthetic `ReplayHeader` is allowed
- no raw-state payload parsing is required yet
- no frame extraction is required yet
- no semantic event extraction is required yet

The parser is allowed to read only:

- the byte payload carried by `ReplayInput::Memory`
- the `ReplayInput::Memory` label for diagnostics, provenance display, or error context

The first implementation is not authorized to read:

- `source_replay` as a path
- `source_replay.provenance_label` as a path
- `audited_family_root_directory` as replay storage
- arbitrary filesystem replay locations
- corpus directories
- export directories
- database state
- runtime CLI-provided locator state

The parser is allowed to output only:

- `Ok(ReplayHeader)` through the existing `ReplayReader::read_header(&ReplayInput)` surface for
  valid supported replay bytes
- `Err(...)` for invalid, malformed, or unsupported bytes

The first implementation is not authorized to output:

- raw-state payloads
- replay frame lists
- semantic replay events
- parser-success policy classifications outside the direct `Result<ReplayHeader>` call result
- replay-source materialization records
- carrier discovery records
- replay-input locator records
- export records
- corpus ingestion records

## E. ALLOWED FUTURE CRATE BOUNDARY REOPENING

The default future owner of real parser implementation is:

- `mimir-replay`

A later implementation pass may reopen:

- `crates/mimir-replay/src/lib.rs` to add a real reader implementation
- `crates/mimir-replay/Cargo.toml` to add a narrow parser backend dependency, if justified
- workspace dependency metadata only if the selected backend or narrow parser crate requires it

A later pass may introduce a narrow shared parser backend crate only if all of these hold:

- the crate is owned as a parser backend implementation detail or explicit dependency of
  `mimir-replay`
- the crate serves header-level replay parsing first
- the crate does not create all-family raw-state, frame, event, index, export, locator, carrier, or
  materialization infrastructure
- the low-boost-recovery chain still consumes parser behavior only through the existing
  `mimir-replay` reader contract

`mimir-skill` may later consume the real reader only through the existing contract and realization
chain. It must not own replay parser implementation.

## F. STILL FORBIDDEN

These remain forbidden in this pass:

- parser implementation
- parser-success policy
- raw-state payload parsing
- frame extraction
- semantic event extraction
- replay-source actual-materialization
- carrier discovery
- replay-input locator logic
- `mimir_export` widening
- runtime CLI commands
- corpus-wide ingestion
- async/background systems
- database code
- real rollout physics
- execution-result cleanup boundary changes
- generic all-family replay/raw-state/index/export/materialization frameworks
- modifications to `mimir-replay`
- modifications to `mimir-io`
- modifications to `mimir-export`
- modifications to `mimir-types`

These remain closed even after this requirement is accepted unless a later pass explicitly reopens
them:

- parser-success policy beyond the direct `Result<ReplayHeader>` behavior of a header read
- raw-state payload parsing
- replay frame extraction
- semantic event extraction
- replay-source actual-materialization
- replay-source carrier discovery
- replay-input locator implementation
- export widening
- corpus ingestion
- runtime CLI
- database-backed replay indexing
- generic replay/raw-state/export frameworks

## G. MINIMAL ACCEPTANCE CRITERIA FOR FUTURE IMPLEMENTATION PASS

A future real parser implementation pass must satisfy all of these before claiming parser progress:

1. A real parser reader exists and is distinguishable from `UnsupportedReplayReader`.
2. A valid `ReplayInput::Memory` sample containing supported replay bytes can return a real
   `ReplayHeader`.
3. Invalid, malformed, or unsupported bytes return a structured error.
4. No fake, synthetic, guessed, placeholder, or padded `ReplayHeader` is produced.
5. Header output is deterministic for the same input bytes.
6. The implementation makes no raw-state payload parsing claim.
7. The implementation makes no frame extraction claim.
8. The implementation makes no semantic event extraction claim.
9. Tests prove valid and invalid behavior.
10. Existing unsupported-attempt tests still pass or are explicitly adapted without losing the
    truthful unsupported-reader evidence.
11. Full workspace validation passes.
12. `mimir_export` remains untouched and unwidened.
13. The implementation documents the supported replay header format assumptions and unsupported
    cases.
14. The implementation records enough diagnostics to distinguish invalid bytes, unsupported replay
    format, and backend/internal parser errors.

These criteria prove only the first header parser step. They do not prove parser-success policy,
raw-state parsing, frame/event extraction, replay-source materialization, carrier discovery,
locator correctness, or export readiness.

## H. NON-GOALS

This pass does not implement any parser.

This pass does not:

- add Rust source
- add parser dependencies
- add parser-success policy
- produce or synthesize `ReplayHeader`
- parse raw-state payloads
- extract replay frames
- extract semantic replay events
- materialize replay sources
- discover replay-source carriers
- implement replay-input locator logic
- widen `mimir_export`
- add corpus ingestion
- add runtime CLI
- add async/background systems
- add database code
- add rollout physics
- change execution-result cleanup boundaries

## I. NEXT STAGE

The immediate next pass should be:

- parser backend integration contract-definition

Reason:

The requirement now authorizes a future real parser implementation, but it still does not choose a
backend, dependency policy, supported replay header format boundary, error taxonomy, test fixture
source, or integration ownership details. A contract-definition pass is narrower than an
implementation planning pass and keeps parser implementation, parser-success policy,
raw-state parsing, frame/event extraction, replay-source materialization, carrier discovery,
locator logic, and export widening closed.

