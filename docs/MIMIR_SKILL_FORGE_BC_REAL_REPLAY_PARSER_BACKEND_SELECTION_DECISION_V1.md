# MIMIR Skill Forge BC Real Replay Parser Backend Selection Decision v1

## A. PURPOSE

This pass selects the future backend direction for the minimal real replay header parser.

This is a decision-only pass. It does not implement a parser, does not add a parser backend
dependency, does not claim parser readiness, does not claim parser success, does not produce a
`ReplayHeader`, and does not parse replay payloads.

The selected future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains exactly:

- `ReplayInput::Memory`

The only allowed future success result remains:

- real `ReplayHeader` for valid supported bytes only

All invalid, malformed, insufficient, unsupported, or deferred inputs must remain structured
errors.

## B. FAMILY SCOPE

The active evidence chain remains scoped to:

- `low_boost_recovery`

The backend owner remains:

- `mimir-replay`

Rocket League replay header parsing may be a shared `mimir-replay` capability later, but this pass
does not create a generic replay, raw-state, frame, event, locator, carrier, materialization,
database, export, corpus, runtime CLI, or all-family framework.

`mimir-skill` may consume a future real reader only through the existing `ReplayReader` contract
and the current low-boost contract/realization chain.

## C. CURRENT BACKEND INTEGRATION CONTRACT SUMMARY

The current trusted integration contract is:

- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_INTEGRATION_CONTRACT_V1.md`

That contract selected:

- Outcome A for the integration contract only
- future real header reader integrated into `mimir-replay`
- no concrete backend or dependency selected
- future backend selection or implementation deferred to a later pass

The current workspace surface remains:

- `ReplayInput::File(PathBuf)`
- `ReplayInput::Memory { label, bytes }`
- `ReplayHeader`
- `ReplayReader`
- `UnsupportedReplayReader`

The current audited implementation remains scaffold-only:

- `UnsupportedReplayReader` is the only `ReplayReader` implementation in `mimir-replay`
- `UnsupportedReplayReader::read_header` returns an explicit error
- no real replay parser reader exists
- no parser-success policy exists
- no valid `ReplayHeader` output exists

`UnsupportedReplayReader` remains truthful scaffold behavior and must remain distinguishable from
any future real reader.

## D. RE-AUDIT SUMMARY

Files re-audited before this decision:

- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_INTEGRATION_CONTRACT_V1.md`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_integration_contract_decision.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_integration_contract_next.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_backend_integration_contract_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_IMPLEMENTATION_EXTERNAL_REQUIREMENT_V1.md`
- `executor_mimir_skill_forge_bc_real_replay_parser_implementation_external_requirement_decision.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_implementation_external_requirement_next.txt`
- `executor_mimir_skill_forge_bc_real_replay_parser_implementation_external_requirement_status.txt`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-skill/Cargo.toml`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

Workspace findings:

- `crates/mimir-replay/Cargo.toml` depends only on `mimir-core`, `mimir-types`, and `serde`.
- `Cargo.toml` has no workspace replay parser dependency.
- `Cargo.lock` search found no existing `boxcars`, `rattletrap`, `rrrocket`, `carball`,
  `rlreplay`, or equivalent Rocket League replay parser dependency.
- `cargo tree -p mimir-replay` shows no replay parser backend.
- `mimir-skill` invokes the existing reader surface only for the truthful unsupported-attempt
  realization through `UnsupportedReplayReader`.
- The staged delivery rules still forbid replay, rollout, runtime, export-bundle, or orchestration
  widening unless a later pass explicitly reopens them.

## E. CANDIDATE BACKEND ANALYSIS

### Candidate A1: Existing Workspace Dependency or Backend

Decision:

- rejected

Reason:

- no current workspace dependency is capable of Rocket League replay header parsing
- no current crate contains a second real `ReplayReader` implementation
- no current dependency is already approved for `mimir-replay` replay parsing
- selecting an already-present backend would be false because no such backend is present

### Candidate A2: External Rust Replay Parser Dependency

Primary external candidate audited:

- `boxcars`

Evidence:

- `cargo search boxcars --limit 5` reports `boxcars = "0.11.1"` as a Rocket League replay parser.
- `cargo info boxcars` reports version `0.11.1`, license `MIT`, repository
  `https://github.com/nickbabcock/boxcars`, and documentation
  `https://docs.rs/boxcars/0.11.1`.
- `boxcars::ParserBuilder::new(data)` accepts `&[u8]`.
- `boxcars::ParserBuilder` exposes `never_parse_network_data()`.
- upstream docs describe `boxcars` as a Rocket League replay parser in Rust and document a
  header-oriented mode that skips network data.

External source references:

- `https://docs.rs/boxcars/latest/boxcars/`
- `https://docs.rs/boxcars/latest/boxcars/struct.ParserBuilder.html`
- `https://github.com/nickbabcock/boxcars`
- `https://crates.io/crates/boxcars`

Positive findings:

- Rust library, not a runtime CLI requirement
- license is MIT, compatible with this workspace license policy
- can parse from memory bytes
- has a documented mode that skips network data parsing
- has a small normal dependency set for a replay parser: `bitter`, `encoding_rs`, `fnv`, `phf`,
  `serde`
- upstream documentation claims stable Rust, no unsafe, fuzzing, and header-oriented parsing

Strict rejection reason for this pass:

- `boxcars` is credible, but it is not the narrowest honest backend direction for the current
  contract.
- It is not already present in the workspace and is not already project-approved.
- Its public `ParserBuilder::parse()` result is `boxcars::Replay`, not a header-only result.
- The audited no-network path still constructs broader replay fields such as keyframes,
  tick marks, names, objects, class indices, network cache metadata, and other body-derived
  structures while setting network frames to `None`.
- A future wrapper could discard those broader fields, but this pass is not allowed to blur the
  difference between "not exposed by MIMIR" and "not parsed by the backend".
- Because raw-state, frame, event, materialization, locator, carrier, corpus, runtime CLI, and
  export domains remain closed, choosing a broad parser dependency now would create unnecessary
  dependency and semantic surface before MIMIR has a proven header-only implementation plan.

Secondary external candidate audited:

- `subtr-actor`

Decision:

- rejected

Reason:

- `cargo info subtr-actor` reports it as a Rocket League replay transformer built on `boxcars`
- it adds broad transformer dependencies and behavior above header parsing
- it is not a minimal header parser backend for `ReplayReader::read_header`

External dependency selection result:

- no external dependency is selected in this pass

### Candidate B: Narrow In-Crate `mimir-replay` Header Parser Direction

Decision:

- selected

Reason:

- `mimir-replay` already owns `ReplayInput`, `ReplayHeader`, `ReplayReader`, and
  `UnsupportedReplayReader`
- a future in-crate reader can be limited to `ReplayInput::Memory`
- a future in-crate reader can parse only the replay header bytes and header properties needed to
  produce MIMIR's `ReplayHeader`
- a future implementation can reject `ReplayInput::File` until file support is explicitly reopened
- a future implementation can keep `UnsupportedReplayReader` truthful and distinct
- a future implementation can expose structured error categories without widening `mimir-io`,
  `mimir-export`, or `mimir-types`
- a future implementation can avoid importing a broad external replay parser API before MIMIR has
  a fixture-backed mapping from Rocket League header bytes to `ReplayHeader`

Required future implementation boundary:

- owner crate: `mimir-replay`
- target function: `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`
- first admitted input: `ReplayInput::Memory`
- byte source: only `ReplayInput::Memory.bytes`
- label use: diagnostics and `ReplayHeader.source_label` source context only
- replay identity: must be byte-backed or documented header-backed, never label-derived
- total frames: `Some` only when supported header evidence exists; otherwise `None`
- metadata: only byte-backed or explicitly documented header-backed metadata
- unsupported, malformed, insufficient, non-memory, invalid-header, and backend/internal failures:
  structured errors
- real reader: distinct from `UnsupportedReplayReader`
- tests: valid supported bytes, invalid or malformed bytes, unsupported format/version when
  distinguishable, deterministic repeated parsing, deterministic repeated error categories

Closed under this direction:

- parser implementation remains closed until a later explicit implementation pass
- parser-success logic remains closed
- raw-state payload parsing remains closed
- replay frame extraction remains closed
- semantic replay event extraction remains closed
- replay-source materialization, carrier discovery, and locator logic remain closed
- `mimir_export` widening remains forbidden

### Candidate C: Stop or No-Op

Decision:

- rejected

Reason:

- the current evidence is sufficient to decide that no current workspace backend exists
- the current evidence is sufficient to reject selecting an external dependency now as broader than
  the minimal header boundary
- the current evidence is sufficient to select a narrow future in-crate direction without
  implementing parser logic
- stopping would leave the next pass without a backend direction despite enough audited evidence
  for a bounded decision

## F. EXACT OUTCOME

Selected outcome:

- Outcome B

Selected backend direction:

- narrow in-crate `mimir-replay` header parser implementation direction

Concrete dependency selected:

- no

Rust/code changes authorized by this decision pass:

- none

Parser implementation authorized by this decision pass:

- no

## G. WHY COMPETING OUTCOMES LOST

Outcome A lost because:

- no existing workspace dependency/backend is present
- the only credible external Rust parser audited, `boxcars`, is broader than the current
  minimal-header-only contract when used through its verified public API
- selecting a new dependency now would imply a backend commitment before a MIMIR-specific
  header-only mapping and fixture plan exists

Outcome C lost because:

- backend direction is not too under-specified for a decision
- the in-crate direction preserves the current contract and forbids parser implementation until a
  later pass
- no-op would add uncertainty, not reduce it

## H. WHAT REMAINS CLOSED

Still closed after this pass:

- parser implementation
- parser-success logic
- backend dependency addition
- `ReplayHeader` production or synthesis
- raw-state payload parsing
- replay frame extraction
- semantic replay event extraction
- replay-source actual materialization
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

## I. WHAT REMAINS FORBIDDEN

Still forbidden unless explicitly reopened by a later pass:

- modifying `mimir-io` for replay parser work
- modifying `mimir-export` for replay parser work
- modifying `mimir-types` for replay parser work
- widening `mimir_export`
- interpreting `source_replay` as a replay path
- interpreting `source_replay.provenance_label` as a replay path
- interpreting `audited_family_root_directory` as replay storage
- reading arbitrary replay files from filesystem paths
- deriving replay identity from labels, paths, or provenance strings
- fabricating, padding, guessing, or synthesizing `ReplayHeader`
- exposing raw-state payloads, frames, semantic events, materialization records, carrier records,
  locator records, export payloads, or corpus records from the header reader

## J. NEXT STAGE

Immediate next pass:

- minimal real parser implementation planning pass

The next pass should remain planning-only unless explicitly reopened for implementation. It must
define exact supported header format assumptions, byte-level field accounting, error taxonomy,
fixture requirements, and validation gates before any parser-success logic or real parser code is
added.
