# MIMIR Skill Forge BC Real Replay Parser Backend Integration Contract v1

## A. PURPOSE

This pass defines the backend integration contract for the future minimal real replay header
parser.

It follows:

- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_IMPLEMENTATION_EXTERNAL_REQUIREMENT_V1.md`

That requirement selected parser requirement scope Outcome A:

- minimal real header parser backend only
- first parser target:
  `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`
- first admitted input:
  valid supported `ReplayInput::Memory` replay bytes

This artifact is contract-definition only. It does not implement a parser, does not select a
concrete backend dependency, does not claim parser readiness, does not claim parser success, does
not produce a `ReplayHeader`, and does not parse replay payloads.

The purpose of this contract is to make the future backend boundary explicit before any parser code
is added. The current trusted chain proves only truthful scaffold unsupported-reader behavior.

## B. FAMILY SCOPE

The active chain remains scoped to:

- `low_boost_recovery`

The reason is narrow: the admitted evidence comes from the low-boost-recovery BC chain, including
receipt-bound specimen ordering, preserved opaque caller-admitted replay bytes, and
`ReplayInput::Memory` values created under that chain.

The future backend capability may live in shared `mimir-replay` because Rocket League replay
header parsing is not a low-boost-recovery-specific semantic operation. That shared placement does
not widen this chain. The low-boost-recovery chain may consume the future real reader only through
the existing `mimir-replay` reader surface and the already-defined low-boost contract/realization
chain.

This contract does not create a generic all-family replay, raw-state, frame, event, index, export,
locator, carrier, or materialization framework.

## C. CURRENT REQUIREMENT SUMMARY

The current requirement is exactly:

- minimal real header parser only
- input limited first to `ReplayInput::Memory`
- parser target limited to `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The current workspace surface is:

- `ReplayInput::File(PathBuf)`
- `ReplayInput::Memory { label, bytes }`
- `ReplayHeader`
- `ReplayReader`
- `UnsupportedReplayReader`

The audited implementation surface remains scaffold-only:

- `UnsupportedReplayReader` implements `ReplayReader`
- `UnsupportedReplayReader::read_header` returns an explicit error
- no real reader implementation exists
- no parser backend dependency is present in the workspace manifest or lockfile

## D. EXACT BACKEND INTEGRATION CONTRACT

Selected backend integration scope:

- Outcome A: contract only for a real header reader integrated into `mimir-replay`
- no backend dependency is selected in this pass
- a future implementation pass must separately select or implement the backend

Backend owner crate:

- default and expected owner: `mimir-replay`

Allowed future crate/source modifications, only in a later implementation or planning pass:

- `crates/mimir-replay/src/lib.rs` may add a real reader type and narrowly scoped parser support
- `crates/mimir-replay/Cargo.toml` may add a narrow replay-header parser backend dependency if
  justified
- workspace dependency metadata may change only if required by the selected backend
- parser fixtures or tests may be added only to prove the minimal header reader contract

Disallowed ownership:

- `mimir-skill` must not own replay parser implementation
- `mimir-io` must not become a parser owner
- `mimir-export` must not be widened for parser output
- `mimir-types` must not be modified for this contract

Dependency policy:

- no concrete backend is selected now
- no dependency is added in this pass
- future backend selection must be explicit, justified, and limited to header parsing first
- a future dependency must not pull in a broad replay ingestion, export, database, runtime CLI, or
  corpus framework unless a later pass separately reopens that domain
- a future hand-written backend is allowed only if the implementation planning pass documents why
  using an existing backend is not the narrower or safer choice

Supported-header capability boundary:

- the first real reader may inspect only enough bytes to produce `ReplayHeader` for valid supported
  replay bytes
- supported replay format and version assumptions must be documented by the implementation pass
- unsupported format/version cases must return structured errors, not fabricated headers
- `ReplayHeader.replay_id` must be derived from replay bytes or a documented header-backed source,
  not from `ReplayInput::Memory.label`
- `ReplayHeader.source_label` may carry the input label as source context only; it must not be used
  as replay identity or parser evidence
- `ReplayHeader.total_frames` may be `Some` only when supported header evidence exists; otherwise
  it must remain `None`
- `ReplayHeader.metadata` may contain only byte-backed or explicitly documented header-backed
  metadata; no placeholder metadata is allowed

`UnsupportedReplayReader` coexistence:

- `UnsupportedReplayReader` remains valid scaffold behavior
- its existing truth is that no bundled scaffold parser exists for that reader
- future real reader work must not erase the unsupported-attempt evidence
- future unsupported-reader tests must still prove explicit unsupported behavior, or be adapted
  without converting unsupported behavior into parser success

Future real-reader distinguishability:

- the real reader must be a distinct implementation path from `UnsupportedReplayReader`
- tests and/or type names must make it impossible to confuse scaffold unsupported behavior with
  real parser behavior
- a future low-boost realization that consumes the real reader must record that the configured
  reader is not `UnsupportedReplayReader`

`mimir-skill` consumption:

- `mimir-skill` may consume the future real reader only through the existing
  `ReplayReader::read_header(&ReplayInput)` surface
- any low-boost consumption must preserve the existing receipt-bound contract/realization chain
- parser-success policy remains separate and closed unless explicitly reopened
- `mimir-skill` must not bypass `ReplayReader` to call backend internals

## E. INPUT BOUNDARY

Allowed first input:

- `ReplayInput::Memory { label, bytes }`

Byte semantics:

- `bytes` are the only parser data source
- `bytes` must be the exact caller-admitted replay byte payload already preserved by the lower
  chain
- no byte synthesis, padding, truncation, repair, or fallback lookup is allowed

Label semantics:

- `label` may be used only for diagnostics, provenance display, and error context
- `label` may be copied into `ReplayHeader.source_label` as source context
- `label` must not be interpreted as a filesystem path
- `label` must not be used to derive `ReplayHeader.replay_id`
- `label` must not be used to infer format, version, frame count, or metadata

Forbidden input forms and semantics:

- no `ReplayInput::File` support is opened by the first parser target
- no `source_replay` path
- no `source_replay.provenance_label` path
- no `audited_family_root_directory` replay storage
- no corpus directory
- no runtime CLI locator
- no replay-source actual materialization
- no replay-source carrier discovery
- no replay-input locator logic
- no database lookup
- no export-directory lookup

Non-memory input behavior:

- if a future real reader receives `ReplayInput::File` before file support is explicitly opened, it
  must reject or defer that input with a structured non-memory-input error
- it must not silently read a file path or reinterpret lineage as storage

## F. OUTPUT BOUNDARY

Allowed output:

- `Ok(ReplayHeader)` only for valid supported replay bytes
- structured `Err(...)` for invalid, malformed, insufficient, unsupported, or deferred inputs

Forbidden output:

- no raw-state payload
- no replay frames
- no semantic replay events
- no replay-source materialization records
- no carrier discovery records
- no replay-input locator records
- no export payload
- no parser-success policy record outside the direct `Result<ReplayHeader>` call

No-fake-header rule:

- a future implementation must never fabricate, guess, pad, or synthesize a `ReplayHeader`
- a valid-looking header produced from invalid bytes is a contract violation
- a header derived from label/path/provenance instead of replay bytes is a contract violation
- a fallback header for unsupported bytes is a contract violation

## G. ERROR TAXONOMY

A future implementation must expose or preserve enough structured error information to distinguish
at least these categories:

- unsupported format/version
- malformed bytes
- insufficient bytes
- backend/internal parser error
- non-memory input rejected or deferred, if applicable
- invalid header fields
- synthetic/header fabrication forbidden

Minimum category semantics:

- `unsupported format/version` means bytes may be well-formed enough to identify a replay format,
  but the format or version is outside the supported boundary
- `malformed bytes` means the bytes fail required replay/header structure validation
- `insufficient bytes` means the byte payload ends before required header data can be validated
- `backend/internal parser error` means the selected parser backend failed unexpectedly after input
  admission
- `non-memory input rejected or deferred` means the caller supplied a `ReplayInput` form outside
  the first admitted boundary
- `invalid header fields` means parsed header fields violate required invariants
- `synthetic/header fabrication forbidden` means the implementation detected a path that would
  produce a guessed or non-byte-backed header and rejected it

The exact Rust error type is not selected in this pass. A later implementation may add a
contract-facing replay parser error type if needed, but it must remain inside the narrow parser
boundary and must not require changes to `mimir-io`, `mimir-export`, or `mimir-types`.

## H. FIXTURE EVIDENCE REQUIREMENT

A future implementation must include fixture evidence before claiming parser progress:

- at least one valid supported `ReplayInput::Memory` sample
- at least one invalid or malformed byte sample
- at least one unsupported-format sample if the backend can distinguish unsupported format/version
  from malformed bytes
- deterministic repeated parsing checks for the same valid bytes
- deterministic repeated error-category checks for the same invalid or unsupported bytes

Fixture constraints:

- fixtures must not rely on `source_replay` as a path
- fixtures must not rely on `source_replay.provenance_label` as a path
- fixtures must not rely on `audited_family_root_directory` as replay storage
- fixtures must not require corpus directory discovery
- fixtures must not require runtime CLI locator behavior
- fixtures must not require `mimir-export`
- fixture labels are diagnostic only

Valid fixture evidence must prove:

- the input is `ReplayInput::Memory`
- the valid sample returns a real `ReplayHeader`
- the returned fields are byte-backed or explicitly documented as source context
- repeated parsing returns equal `ReplayHeader` output

Invalid/malformed/unsupported fixture evidence must prove:

- invalid bytes do not produce a `ReplayHeader`
- malformed or insufficient bytes return structured error categories
- unsupported format/version returns the unsupported category when distinguishable
- no fake header fallback exists

## I. ACCEPTANCE CRITERIA FOR FUTURE IMPLEMENTATION

A future minimal real header parser implementation may claim only header-parser progress if all of
these hold:

1. A real reader implementation exists in or behind `mimir-replay`.
2. The real reader is distinguishable from `UnsupportedReplayReader`.
3. `UnsupportedReplayReader` remains truthful scaffold behavior.
4. A valid supported `ReplayInput::Memory` sample returns a real `ReplayHeader`.
5. Invalid, malformed, insufficient, unsupported, or deferred input returns a structured error.
6. Repeated parsing of identical valid bytes is deterministic.
7. Repeated parsing of identical invalid or unsupported bytes is deterministic by error category.
8. No fake, synthetic, guessed, placeholder, padded, label-derived, or path-derived header is
   produced.
9. Supported replay header format/version assumptions are documented.
10. Tests cover valid, invalid/malformed, and unsupported-if-distinguishable fixtures.
11. Existing unsupported-attempt truth is preserved.
12. Full workspace validation passes.
13. `mimir-export` remains untouched and unwidened.
14. No raw-state payload parsing, frame extraction, semantic event extraction, replay-source
    materialization, carrier discovery, locator logic, corpus ingestion, runtime CLI, database, or
    export behavior is added.

These criteria prove only the first real header parsing step. They do not prove parser-success
policy, raw-state parsing, frame/event extraction, replay-source materialization, carrier discovery,
locator correctness, export readiness, or training readiness.

## J. STILL FORBIDDEN

Still forbidden in this pass:

- parser implementation
- backend dependency addition
- parser-success policy
- `ReplayHeader` production or synthesis
- raw-state payload parsing
- replay frame extraction
- semantic replay event extraction
- replay-source actual materialization
- replay-source carrier discovery
- replay-input locator logic
- replay-source actual-materialization implementation
- replay-source carrier discovery implementation
- replay-input locator implementation
- `mimir_export` widening
- corpus ingestion
- runtime CLI commands
- async/background systems
- database code
- real rollout physics
- execution-result cleanup boundary changes
- generic all-family replay/raw-state/index/export/materialization frameworks
- interpreting `source_replay` as a replay path
- interpreting `source_replay.provenance_label` as a replay path
- interpreting `audited_family_root_directory` as replay storage

Still closed even after this integration contract is defined:

- backend implementation
- backend dependency selection
- parser-success policy
- raw-state payload parsing
- frame extraction
- semantic event extraction
- replay-source materialization
- carrier discovery
- replay-input locator logic
- export readiness
- export widening
- corpus-wide replay ingestion
- runtime CLI

## K. NEXT STAGE

Immediate next pass:

- backend selection decision pass

Reason:

This contract has intentionally selected Outcome A and deferred the concrete backend. A minimal
real parser backend implementation planning pass would still be premature without first deciding
whether to use an existing dependency or a narrow in-crate implementation. The narrower next pass is
therefore a backend selection decision pass.

The next pass must remain decision-only unless explicitly reopened. Parser implementation,
parser-success logic, raw-state payload parsing, frame/event extraction, replay-source
materialization, carrier discovery, locator logic, and `mimir_export` widening remain closed.
