# MIMIR Skill Forge BC Replay Header Parser Fixture 002 Supported-Version Policy Planning Reopen V1

Pass date: 2026-05-05

## Purpose

This is a docs/artifacts-only policy planning pass for fixture_002 supported-version handling.
It decides whether fixture_002 may be planned as a later exact supported replay-header tuple while
keeping parser implementation, parser-success admission, broad version-family support, file input,
CRC validation, and body/raw-state/frame/event parsing closed.

No parser code is changed by this artifact.

## Selected Outcome

Outcome A.

fixture_002 supported-version policy planning is reopened and complete for the admitted evidence.
The selected future policy is an additional exact fixture_002-supported tuple beside the existing
fixture_001 exact tuple. This is not broad version-family support.

The next pass may target exact supported tuple implementation planning. A later implementation pass
may implement only that exact policy if separately scoped. No parser-success is claimed in this
pass.

## Fixture Identity Verification

fixture_001 was verified from `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`:

| Field | Verified value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| extension | `.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| first four bytes, little-endian i32 | `13200` |
| byte length greater than 8 | yes |

fixture_002 was verified from `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay`:

| Field | Verified value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_002` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` |
| extension | `.replay` |
| byte length | `2632903` |
| SHA-256 | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` |
| first four bytes, little-endian i32 | `11273` |
| byte length greater than 8 | yes |
| differs from fixture_001 by SHA-256 | yes |

These are fixture identity facts only. They are not parser facts and do not participate in the
selected supported-version policy.

## Current Supported-Version Implementation Audit

Audited files:

- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/README.md`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- prior fixture_002 report, mapping/error-boundary, implementation audit, readiness, artifact
  versioning, data contract, and staged-delivery artifacts required by this pass

Current `MinimalReplayHeaderReader` implementation facts:

| Boundary | Current implementation |
| --- | --- |
| owning crate | `crates/mimir-replay/src/lib.rs` |
| reader selection | explicit opt-in `MinimalReplayHeaderReader` |
| accepted input variant | `ReplayInput::Memory { label, bytes }` |
| rejected input variant | `ReplayInput::File(_)` returns `unsupported-input` |
| parser stop boundary | header-only, ending at `8 + header_size` |
| `header_crc` | read as layout only, not validated or exposed |
| `content_crc` | not read and not validated |
| body/raw-state/frame/event parsing | not implemented |
| backend replay parser dependency | not present |
| path/hash/filename/provenance support decision | not used by version policy |

Current exact supported tuple constants or equivalent logic:

| Component | Current value |
| --- | --- |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `10` / `Some(10)` at evidence level |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| `ReplayVersion` | `8` |
| `BuildVersion` | `241206.55345.468477` |

`BuildVersion` is currently a single exact value. The unsupported-version error is produced after
the reader has parsed top-level selected properties enough to obtain `ReplayVersion` and
`BuildVersion`, and before a `ReplayHeader` is returned. The current policy does not depend on
fixture path, hash, filename, provenance, or artifact id.

Adding a second exact tuple would not require broad parser logic, manifest changes, lockfile
changes, new dependencies, `ReplayInput::File`, CRC validation, or body/raw-state/frame/event
parsing.

## Fixture 001 vs Fixture 002 Version Tuple Comparison

Only report/type-level evidence is compared here.

| Component | fixture_001 | fixture_002 | Classification |
| --- | --- | --- | --- |
| `major_version` | `868` | `868` | same |
| `minor_version` | `32` | `32` | same |
| `net_version` | `Some(10)` | `Some(10)` | same |
| `game_type` | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` | same |
| `ReplayVersion` | `8` | `8` | same |
| `BuildVersion` | `241206.55345.468477` | `250811.43331.492665` | different |

fixture_002 may be planned as an additional exact supported tuple because the admitted evidence
isolates the support delta to one exact `BuildVersion` component while keeping the other tuple
components equal at report level.

This does not imply wildcard `BuildVersion` support. It does not imply all
`868/32/net10/soccar/ReplayVersion=8` builds are supported. It does not imply parser-success for
future unknown fixtures.

## Supported-Version Policy Options Considered

1. Keep fixture_001 only.
   - Rejected for the selected future policy because the admitted fixture_002 evidence is sufficient
     to plan a second exact tuple in a later pass.

2. Add fixture_002 as a second exact allowlisted tuple.
   - Selected. This preserves the exact tuple invariant and avoids false broad support.

3. Wildcard `BuildVersion` for `major=868, minor=32, net=10, game_type=Soccar, ReplayVersion=8`.
   - Rejected. Two fixtures do not prove all builds in that family share parser-compatible selected
     property behavior or stable semantics.

4. Version-range or broad `ReplayVersion = 8` support.
   - Rejected. Current evidence is fixture-specific and report-level only.

5. Path/hash/provenance/fixture-id based support.
   - Rejected. Fixture identity proves which bytes were audited externally; it must not become a
     parser admission rule.

6. Backend parser dependency or broad parser framework.
   - Rejected. The future exact tuple policy does not require it and this pass forbids dependency
     expansion.

## Selected Future Policy

Exact allowlist only:

| Future policy label | Exact tuple |
| --- | --- |
| `SupportedReplayHeaderTupleV1::Fixture001Exact` | `major_version=868`, `minor_version=32`, `net_version=Some(10)`, `game_type=TAGame.Replay_Soccar_TA`, `ReplayVersion=8`, `BuildVersion=241206.55345.468477` |
| `SupportedReplayHeaderTupleV1::Fixture002Exact` | `major_version=868`, `minor_version=32`, `net_version=Some(10)`, `game_type=TAGame.Replay_Soccar_TA`, `ReplayVersion=8`, `BuildVersion=250811.43331.492665` |

The labels are planning labels only. No enum or implementation is created in this pass.

Selected future policy constraints:

- no wildcard `BuildVersion`
- no version-range support
- no broad `ReplayVersion = 8` support
- no future unknown build support
- no path/hash/filename/provenance/artifact-id based support
- no parser-success admission from this planning artifact alone

## Future Implementation Boundary

If a later implementation pass is opened, its minimal boundary is:

- modify only `crates/mimir-replay/src/lib.rs`
- no `Cargo.toml` or `Cargo.lock` changes
- no `mimir-skill` changes in the first parser policy implementation pass unless separately
  reopened
- no `mimir-export`, `mimir-io`, `mimir-types`, or `mimir-cli` changes
- replace the single supported `BuildVersion` check with an exact supported tuple allowlist or
  equivalent exact predicate
- keep `ReplayInput::Memory` only
- keep `ReplayInput::File` unsupported
- keep header-only parsing ending at `8 + header_size`
- keep CRC non-validation
- keep `content_crc`, body, raw-state, frame, and event parsing closed
- do not add a backend replay parser dependency
- do not add a broad parser framework

The future implementation may compare fixture_002 output against the admitted candidate
expected-output evidence only after the exact tuple support code and tests exist.

## Future Test Boundary

A later exact tuple implementation pass should add only focused tests:

- fixture_001 regression proving the existing exact fixture_001 tuple still parses
- fixture_002 happy-path test proving only the exact fixture_002 tuple is newly admitted
- unsupported-version regression proving an unknown `BuildVersion` remains rejected
- existing `ReplayInput::File` unsupported test remains valid
- existing header-only stop-boundary test remains valid
- existing CRC non-validation boundary remains valid

The future tests must not claim file input, source materialization, CRC validation, body parsing,
raw-state parsing, frame extraction, event parsing, runtime integration, CLI integration, or export
integration.

## Explicit Non-Claims

This pass does not claim:

- parser-success for fixture_002
- fixture_002 support by `MinimalReplayHeaderReader`
- broad parser-success
- broad version-family support
- all `ReplayVersion = 8` builds
- all `BuildVersion` values
- `ReplayInput::File` support
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- `content_crc` read or validation in MIMIR parser code
- body/raw-state/frame/event parsing
- export/runtime/CLI integration
- backend replay parser dependency in MIMIR

## What Remains Closed

Still closed after this pass:

- parser implementation for fixture_002
- parser-success admission for fixture_002
- broad parser-success admission
- broad version-family support
- parser expansion beyond selected exact tuple policy
- `ReplayInput::File`
- replay-source materialization
- CRC validation
- MIMIR `content_crc` read or validation
- body parsing
- raw-state parsing
- frame parsing
- event parsing
- export integration
- runtime integration
- CLI integration
- dependency expansion

## Next Stage

Recommended next pass: fixture_002 exact supported tuple implementation planning.

A direct implementation pass is acceptable only if separately scoped to the exact future boundary
above. That pass may implement an exact two-tuple allowlist in `crates/mimir-replay/src/lib.rs` and
the focused tests listed above. It must not broaden parser scope.
