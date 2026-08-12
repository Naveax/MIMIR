# MIMIR Skill Forge BC Replay Header Parser Readiness Handoff v1

Pass date: 2026-05-04

## Purpose

This pass defines the narrow readiness and future integration handoff policy for the admitted
`MinimalReplayHeaderReader` implementation for:

- fixture id: `rl_replay_header_fixture_001`
- fixture path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`
- admission form: `PRIVATE_LOCAL_PATH_WITH_HASH`

This is a planning and audit handoff pass only. It does not broaden parser scope, add parser
functionality, wire runtime or CLI behavior, widen export behavior, add dependencies, or change
`UnsupportedReplayReader`.

## Selected Outcome

Selected outcome:

- Outcome A

Narrow readiness and integration planning is complete.

The next implementation pass may add a strictly bounded opt-in consumer seam or handoff adapter
only if that pass explicitly scopes the seam and preserves every guardrail below.

No parser expansion is admitted by this pass.

## Current Admitted Parser Boundary

Parser-success remains admitted only when all of the following hold:

- input is `ReplayInput::Memory`
- memory label is non-empty and maps directly to `ReplayHeader.source_label`
- bytes contain the complete replay header prefix and header region
- parse stops at `8 + header_size`
- the top-level `None` terminator ends exactly at `8 + header_size`
- the exact supported tuple is present:
  - `major_version = 868`
  - `minor_version = 32`
  - `net_version = 10`
  - `game_type = TAGame.Replay_Soccar_TA`
  - `ReplayVersion = 8`
  - `BuildVersion = 241206.55345.468477`
- selected scalar mappings are structurally valid and admitted

Parser-success is not admitted broadly.

`header_crc` is read as layout evidence only. It is not validated or exposed. `content_crc` is not
read. Body, raw-state, frame, footer, and semantic event data are not parsed.

## Re-Audit Inputs

The current implementation audit inputs were rechecked before this handoff artifact was written:

- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- root `Cargo.toml`
- root `Cargo.lock`
- first minimal implementation doc and status artifacts
- first minimal implementation audit doc and status artifacts
- `crates/mimir-core/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

Observed facts:

- `MinimalReplayHeaderReader` remains implemented only in `mimir-replay`.
- `UnsupportedReplayReader` remains the truthful unsupported default.
- `mimir-replay` depends only on `mimir-core`, `mimir-types`, and `serde`.
- `mimir-skill` already depends on `mimir-replay` and has receipt-bound memory replay-input
  contracts, but its current actual parser-attempt realization is explicitly tied to
  `UnsupportedReplayReader`.
- `mimir-cli`, `mimir-io`, and `mimir-export` do not directly depend on `mimir-replay`.
- Artifact and data contract docs keep replay parsing, raw-state materialization, and export
  widening as staged and explicit boundaries.
- The staged-delivery rules prohibit widening replay, runtime, export, and orchestration
  boundaries without a later explicit reopen.

## Consumer Boundary Classification

| Crate | May call `MinimalReplayHeaderReader` in the future? | Would calling it broaden parser-success? | Would it imply replay-source materialization? | Would it imply export widening? | Current disposition |
| --- | --- | --- | --- | --- | --- |
| `mimir-replay` | Yes, as the owning crate for narrow docs, examples, or tests. | No, if it remains an explicit opt-in `ReplayInput::Memory` example/test and does not replace defaults. | No, if bytes are already provided by the caller/test fixture and no path/file reading is added. | No. | Open only for narrow owner-crate docs/example-test work. |
| `mimir-skill` | Yes, later, because it already has a `mimir-replay` dependency and memory replay-input handoff contracts. | Not if a future seam accepts only an already admitted `ReplayInput::Memory` and records header-only success as header-only. Yes if it replaces unsupported-attempt semantics, derives parse facts from provenance, or treats success as raw-state/frame availability. | No if it consumes already admitted bytes. Yes if it discovers, reads, or locates replay sources. | No if the result remains internal planning/attempt evidence. Yes if routed into `mimir-export`. | Closed for this pass; future seam requires explicit reopen and exact scope. |
| `mimir-cli` | No direct call yet. | Yes, because a command would create runtime/CLI parse behavior not currently admitted. | Likely yes, because CLI input usually implies path, file, or source discovery. | Not directly, but it could create user-visible parse semantics. | Closed. |
| `mimir-io` | No. | Yes, because raw artifact I/O would start carrying parser behavior or parser output persistence. | Likely yes, if it reads files or persists replay-source facts. | No direct export, but it would widen persisted data contracts. | Closed. |
| `mimir-export` | No. | Yes, because export consumers would receive replay-header-derived semantics. | Possibly, depending on source handling. | Yes. | Closed. |

## Safe Opt-In Policy

`MinimalReplayHeaderReader` remains an explicit opt-in reader.

Allowed future opt-in boundary:

- A caller may invoke `MinimalReplayHeaderReader.read_header(&ReplayInput::Memory { label, bytes })`
  only after it already has admitted bytes and an admitted non-empty label.
- The caller must import/use `ReplayReader` explicitly and must name the operation as a minimal
  replay-header parse attempt.
- The caller must not derive parser facts from path, hash, filename, fixture identity, provenance
  label, receipt lineage, or artifact id.
- The caller must not construct `ReplayInput::File`.
- The caller must not read replay bytes from disk as part of the parse attempt unless a later pass
  explicitly reopens replay-source materialization.
- The caller must not treat successful header parse as proof of replay-source actual
  materialization.
- The caller must not treat successful header parse as proof of body, raw-state, frame, footer, or
  event parsing.
- The caller must not route header parse success through `mimir-export`.
- The caller must preserve `UnsupportedReplayReader` as the truthful unsupported default unless a
  later pass explicitly selects a different configured reader for a named seam.

Permitted result interpretation:

- A successful call may produce a `ReplayHeader` within the first minimal boundary only.
- A failed call may be recorded as a parser-attempt error only.
- Neither success nor failure may be used to claim broad replay parser readiness.

## Rejected Integration Paths

Rejected for this pass and still closed:

- global default reader replacement
- changing `UnsupportedReplayReader`
- `ReplayInput::File` support
- path/hash/filename/provenance-driven parser admission
- CLI command or runtime behavior
- `mimir-export` integration or bundle/index widening
- `mimir-io` persistence of parser output
- `mimir-types` schema expansion for parser results
- backend replay parser dependency
- body/raw-state/frame/footer/event parsing
- CRC validation
- broad replay version-family support
- nested array semantics
- UTF-16 text support
- unencountered property-kind support

## Next Implementation Candidate

Selected next implementation candidate:

- Option B: add a narrow README/example test in `mimir-replay` only.

This pass does not implement that candidate.

If reopened, the candidate must be limited to demonstrating explicit opt-in use of
`MinimalReplayHeaderReader` with caller-supplied `ReplayInput::Memory` bytes. It must not modify
`mimir-skill`, `mimir-cli`, `mimir-io`, `mimir-export`, `mimir-types`, manifests, lockfiles, or
dependencies.

Rejected next candidates for now:

- Option D: add opt-in integration seam in `mimir-skill`
- Option E: add CLI command
- Option F: add export integration

Option D is plausible only after a separate explicit reopen because it would change the current
unsupported-attempt-only realization path in `mimir-skill`.

## Future Consumer Guardrails

Any future consumer must carry this exact parser-success boundary text:

Parser-success is admitted only for `ReplayInput::Memory`, the exact fixture-supported tuple, and
header-only parsing ending at `8 + header_size`. Parser-success is not admitted broadly.

Forbidden broad claims:

- "MIMIR has a replay parser" without the first-minimal boundary qualifier.
- "Fixture hash/path proves parser success."
- "Replay header parse proves replay-source materialization."
- "Replay header parse proves body/raw-state/frame/event availability."
- "CRC is validated."
- "ReplayInput::File is supported."
- "Export can consume replay headers."
- "The supported tuple represents a broad Rocket League replay version family."

Required limitations to repeat in any consumer artifact:

- fixture-only support limitation remains.
- exact tuple limitation remains.
- no CRC validation.
- no body/raw-state/frame/event parsing.
- no export widening.
- no runtime/CLI behavior without explicit reopen.
- no `ReplayInput::File` support.
- no dependency additions.
- no backend replay parser dependency.

## Exact Non-Goals Preserved

This handoff preserves all prior non-goals:

- no CRC validation
- no content CRC read or validation
- no body parsing
- no raw-state payload parsing
- no replay frame extraction
- no footer parsing
- no semantic event parsing
- no nested array semantics
- no UTF-16 support
- no unencountered property-kind support
- no `ReplayInput::File` support
- no backend replay parser dependency
- no export integration
- no runtime or CLI behavior
- no broad replay version-family support

## Next Stage

Outcome A is admitted for planning only.

The next pass may implement only the selected Option B candidate if it is explicitly reopened:

- a narrow `mimir-replay` README/example test showing explicit opt-in memory parsing.

No consumer integration, CLI behavior, export behavior, file input, dependency change, or parser
scope expansion is admitted yet.
