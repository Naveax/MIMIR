# MIMIR Skill Forge BC Replay Header Parser Fixture 002 Exact Supported Tuple Implementation Planning V1

Pass date: 2026-05-05

## Purpose

This is a docs/artifacts-only implementation-planning pass for adding fixture_002 as a second exact
supported replay-header tuple in `MinimalReplayHeaderReader`.

No parser code is changed by this artifact. No parser-success is claimed for fixture_002 in this
pass. This pass plans only a later exact two-tuple allowlist implementation.

## Selected Outcome

Outcome A.

Exact supported tuple implementation planning is complete. The next pass may implement only the
exact two-tuple allowlist in `crates/mimir-replay/src/lib.rs`.

This pass does not claim fixture_002 parser-success, does not implement fixture_002 support, and
does not admit broad parser expansion.

## Assumptions

- The current trusted boundary is the fixture_002 supported-version policy planning reopen pass that
  selected Outcome A.
- The admitted fixture_002 expected output remains candidate expected-output evidence only until a
  later implementation pass changes parser code and verifies it.
- Fixture path, byte length, hash, filename, provenance, and fixture id are identity/audit facts
  only. They must not become parser support predicates.

## Required Inputs Re-Audited

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_SUPPORTED_VERSION_POLICY_PLANNING_REOPEN_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_supported_version_policy_planning_reopen_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_supported_version_policy_planning_reopen_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_002_supported_version_policy_planning_reopen_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_MAPPING_ERROR_BOUNDARY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIRST_MINIMAL_IMPLEMENTATION_AUDIT_V1.md`
- `crates/mimir-replay/README.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`

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

These fixture identity facts are not parser facts and must not be used by the later parser predicate.

## Current Reader Findings

Current implementation facts from `crates/mimir-replay/src/lib.rs`:

| Area | Current state |
| --- | --- |
| public reader | `MinimalReplayHeaderReader` |
| input accepted by reader | `ReplayInput::Memory { label, bytes }` only |
| input rejected by reader | `ReplayInput::File(_)` with `unsupported-input` |
| parse boundary | header-only through `8 + header_size` |
| `header_crc` | read for layout only, not validated or exposed |
| `content_crc` | not read and not validated |
| body/raw-state/frame/event parsing | not implemented |
| backend replay parser dependency | absent |
| current version predicate | single exact fixture_001 tuple |

Current exact tuple:

| Component | Current supported value |
| --- | --- |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `Some(10)` at evidence level, represented as `10` in current code |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| `ReplayVersion` | `8` |
| `BuildVersion` | `241206.55345.468477` |

The current unsupported-version decision is made after selected property parsing obtains
`ReplayVersion` and `BuildVersion`, and before `ReplayHeader` is returned.

## Failure Model

The later implementation can fail silently or misleadingly if it:

- replaces exact tuple support with a wildcard `BuildVersion`
- treats all `ReplayVersion = 8` replays as supported
- admits all `major=868/minor=32/net=10/Soccar` tuples
- makes support depend on fixture path, hash, filename, provenance, or fixture id
- changes `ReplayInput::File` behavior
- reads or validates `content_crc`
- changes the header-only stop boundary
- adds a replay parser backend dependency or manifest change
- changes `mimir-skill`, `mimir-types`, export, runtime, CLI, or IO behavior
- updates tests so fixture_002 can appear supported without checking the exact expected header
- removes fixture_001 regression coverage while adding fixture_002
- proves only compilation while leaving unknown `BuildVersion` behavior untested

## Exact Later Code Plan

The next implementation pass may modify only `crates/mimir-replay/src/lib.rs`.

The intended code shape is:

1. Keep the shared exact constants unchanged for:
   - `SUPPORTED_MAJOR_VERSION = 868`
   - `SUPPORTED_MINOR_VERSION = 32`
   - `SUPPORTED_NET_VERSION = 10`
   - `SUPPORTED_GAME_TYPE = "TAGame.Replay_Soccar_TA"`
   - `SUPPORTED_REPLAY_VERSION = 8`

2. Replace the single `SUPPORTED_BUILD_VERSION` policy with exact fixture-specific build constants:
   - `SUPPORTED_FIXTURE_001_BUILD_VERSION = "241206.55345.468477"`
   - `SUPPORTED_FIXTURE_002_BUILD_VERSION = "250811.43331.492665"`

3. Add a private exact allowlist marker:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SupportedReplayHeaderTupleV1 {
    Fixture001Exact,
    Fixture002Exact,
}
```

4. Add a private exact predicate with no path/hash/provenance inputs:

```rust
fn supported_replay_header_tuple_v1(
    major_version: i32,
    minor_version: i32,
    net_version: i32,
    game_type: &str,
    replay_version: i32,
    build_version: &str,
) -> Option<SupportedReplayHeaderTupleV1> {
    if major_version != SUPPORTED_MAJOR_VERSION
        || minor_version != SUPPORTED_MINOR_VERSION
        || net_version != SUPPORTED_NET_VERSION
        || game_type != SUPPORTED_GAME_TYPE
        || replay_version != SUPPORTED_REPLAY_VERSION
    {
        return None;
    }

    match build_version {
        SUPPORTED_FIXTURE_001_BUILD_VERSION => Some(SupportedReplayHeaderTupleV1::Fixture001Exact),
        SUPPORTED_FIXTURE_002_BUILD_VERSION => Some(SupportedReplayHeaderTupleV1::Fixture002Exact),
        _ => None,
    }
}
```

5. Replace the current single inline tuple `if` with a call to this predicate:

```rust
let _supported_tuple = supported_replay_header_tuple_v1(
    major_version,
    minor_version,
    net_version,
    &game_type,
    replay_version,
    build_version,
)
.ok_or_else(|| {
    parse_error(
        "unsupported-version",
        format!(
            "unsupported tuple major={major_version}, minor={minor_version}, net={net_version}, game_type={game_type}, ReplayVersion={replay_version}, BuildVersion={build_version}"
        ),
    )
})?;
```

The local `_supported_tuple` is only an auditable proof that exactly one allowlisted tuple matched.
It must not change mapping behavior, metadata content, source labels, file input, CRC behavior, or
body parsing.

## Exact Later Test Plan

The next implementation pass may add or adjust only tests inside `crates/mimir-replay/src/lib.rs`.

Required tests:

1. Preserve fixture_001 regression:
   - existing `minimal_reader_parses_rl_replay_header_fixture_001_and_header_only_slice` remains
     valid
   - it must still assert fixture_001 replay id, source label, total frames, and selected metadata
   - it must still prove a complete header-only slice parses without body bytes

2. Add fixture_002 exact happy path:
   - load `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay`
   - call `MinimalReplayHeaderReader.read_header` using
     `ReplayInput::Memory { label: "rl_replay_header_fixture_002", bytes }`
   - assert:
     - `ReplayId::new("D9DA34DA11F0811EAC139A94CBF30AF2")`
     - `source_label == "rl_replay_header_fixture_002"`
     - `total_frames == Some(10351)`
     - `metadata.ReplayName == FieldValue::Text("asdasd")`
     - `metadata.Date == FieldValue::Text("2025-08-24 19-16-35")`
     - `metadata.MapName == FieldValue::Text("NeoTokyo_Standard_P")`
     - `metadata.ReplayVersion == FieldValue::Integer(8)`
     - `metadata.BuildVersion == FieldValue::Text("250811.43331.492665")`
     - `metadata.MaxChannels == FieldValue::Integer(2047)`
     - `metadata.MatchType == FieldValue::Text("Online")`
     - `metadata.TeamSize == FieldValue::Integer(3)`
     - `metadata.RecordFPS == FieldValue::Float(30.0)`

3. Add unknown `BuildVersion` rejection:
   - build a synthetic otherwise-supported tuple
   - set `BuildVersion` to a value not equal to either exact allowed string
   - assert `replay header parse error: unsupported-version`
   - this proves no wildcard `BuildVersion` support is admitted by the implementation

4. Preserve existing negative tests:
   - `ReplayInput::File` remains `unsupported-input`
   - malformed/truncated header tests remain unchanged
   - duplicate selected property tests remain unchanged
   - selected wrong-kind/non-finite/array tests remain unchanged
   - CRC non-validation boundary remains unchanged

Allowed helper changes inside the same file:

- make the fixture loader accept a fixture path and fixture id so fixture_001 and fixture_002 tests
  share the same skip-on-missing behavior
- add a `build_version: String` field to the synthetic `HeaderSpec` test helper so the unknown
  `BuildVersion` regression can be precise
- keep all helpers private to the test module

## Affected Files For Later Implementation

Allowed:

- `crates/mimir-replay/src/lib.rs`

Forbidden unless separately reopened:

- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-cli`
- `crates/mimir-io`
- `crates/mimir-export`
- `crates/mimir-types/src/lib.rs`
- root `Cargo.toml`
- root `Cargo.lock`
- any new dependency or backend replay parser crate

## Invariants Preserved By The Plan

- exact allowlist only
- `ReplayInput::Memory` only
- `ReplayInput::File` remains unsupported
- parser stops at `8 + header_size`
- `header_crc` remains non-validating layout read only
- `content_crc` remains unread and unvalidated
- body/raw-state/frame/event parsing remains closed
- no source materialization
- no path/hash/filename/provenance/artifact-id parser facts
- no broad `ReplayVersion = 8` support
- no wildcard `BuildVersion` support
- no future unknown build support
- no export/runtime/CLI behavior
- no backend replay parser dependency

## Verification For Later Implementation

The later implementation pass must run:

- `cargo check --workspace --all-targets --all-features`
- `cargo test -p mimir-replay -- --nocapture`
- `cargo test -p mimir-skill -- --nocapture`
- `cargo test --workspace --all-targets --all-features`
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`
- `cargo test -p mimir-export -- --list`

Acceptance requires:

- fixture_001 regression passes
- fixture_002 exact happy path passes
- unknown `BuildVersion` remains rejected
- existing unsupported-input, header-only, and CRC non-validation tests still pass
- no manifest or lockfile change
- no new replay parser dependency

## Rollback Strategy For Later Implementation

If the later implementation fails validation, revert only the changes in
`crates/mimir-replay/src/lib.rs` from that implementation pass. Because the plan forbids manifest,
lockfile, and cross-crate changes, rollback should be a single-file reversal.

## Explicit Non-Claims

This pass does not claim:

- parser-success for fixture_002
- fixture_002 support by `MinimalReplayHeaderReader`
- broad parser-success
- broad version-family support
- wildcard `BuildVersion` support
- all `ReplayVersion = 8` builds
- future unknown build support
- `ReplayInput::File` support
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- `content_crc` read or validation in MIMIR parser code
- body/raw-state/frame/event parsing
- export/runtime/CLI integration
- backend replay parser dependency in MIMIR

## Residual Risks

- fixture_002 candidate expected output remains external/report evidence until a later parser-code
  implementation and test run verify it through `MinimalReplayHeaderReader`.
- The later implementation can still accidentally broaden support if the exact predicate is changed
  from the planned match to a prefix/range/family check.
- The fixture-specific tests can skip if local fixture files are missing or unreadable, so validation
  must record fixture presence when claiming the exact fixture tests actually executed.

## Next Stage

The next pass may implement only the exact two-tuple allowlist in
`crates/mimir-replay/src/lib.rs`, with the tests described above.

No parser-success is claimed now. No parser code changed now. No broad parser expansion is admitted.
