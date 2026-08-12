# MIMIR Skill Forge BC Replay Header Parser Fixture 003 Exact Tuple BoolProperty Skip Implementation Planning V1

Pass date: 2026-05-06

## Purpose

Plan the later implementation of fixture_003 support without changing parser code in this pass.

The planned future implementation requires both:

- exact third supported tuple allowlist support for `Fixture003Exact`
- exact non-selected top-level `BoolProperty` skip-only handling

This pass is docs/artifacts-only. It does not modify `MinimalReplayHeaderReader`, add
`Fixture003Exact` in code, add `BoolProperty` parser support in code, claim fixture_003 parser
success, broaden parser scope, add file support, validate CRCs, parse body/raw-state/frame/event
data, add dependencies, or wire CLI/runtime/export behavior.

## Selected Outcome

Outcome A.

Exact Fixture003Exact plus non-selected BoolProperty skip-only implementation planning is complete.
The next pass may implement only the exact scoped changes in `crates/mimir-replay/src/lib.rs`.

No parser-success is claimed now. No parser code changes occur now. No broad parser expansion is
admitted. No `BoolProperty` metadata mapping is admitted.

## Fixture Identity Verification

Fixture identities were reverified directly from local bytes before this artifact was written.

| Fixture | Path | Byte length | SHA-256 | First four bytes as LE i32 | Extension | > 8 bytes |
| --- | --- | ---: | --- | ---: | --- | --- |
| `rl_replay_header_fixture_001` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | `3001021` | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `13200` | `.replay` | yes |
| `rl_replay_header_fixture_002` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` | `2632903` | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` | `11273` | `.replay` | yes |
| `rl_replay_header_fixture_003` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay` | `1638538` | `20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC` | `11190` | `.replay` | yes |

Fixture_003 differs from fixture_001 by SHA-256: yes.

Fixture_003 differs from fixture_002 by SHA-256: yes.

These are identity and audit facts only. They must not become parser support predicates.

## Re-Audited Inputs

Inspected before writing this artifact:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_SUPPORTED_VERSION_POLICY_PLANNING_REOPEN_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_supported_version_policy_planning_reopen_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_supported_version_policy_planning_reopen_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_supported_version_policy_planning_reopen_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_BOOLPROPERTY_NON_SELECTED_ERROR_BOUNDARY_CLOSURE_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_MAPPING_ERROR_BOUNDARY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_REPORT_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_AUDIT_V1.md`
- `crates/mimir-replay/README.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

The supported-version policy planning input was verified as Outcome A. The selected future policy
there is exact three-tuple allowlist only:

- `SupportedReplayHeaderTupleV1::Fixture001Exact`
- `SupportedReplayHeaderTupleV1::Fixture002Exact`
- `SupportedReplayHeaderTupleV1::Fixture003Exact`

The BoolProperty closure input was verified as Outcome A. `bForfeit` remains report-only,
excluded from metadata, excluded from `ReplayHeader` output, and not mapped through
`BoolProperty -> FieldValue::Boolean`.

## Current Implementation Audit

Current parser file: `crates/mimir-replay/src/lib.rs`.

Current input boundary:

- `MinimalReplayHeaderReader` accepts `ReplayInput::Memory { label, bytes }` only.
- `ReplayInput::File(_)` returns `replay header parse error: unsupported-input`.
- `ReplayInput::Memory.label` must be non-empty.

Current constants:

- `SUPPORTED_MAJOR_VERSION = 868`
- `SUPPORTED_MINOR_VERSION = 32`
- `SUPPORTED_NET_VERSION = 10`
- `SUPPORTED_GAME_TYPE = "TAGame.Replay_Soccar_TA"`
- `SUPPORTED_REPLAY_VERSION = 8`
- `SUPPORTED_BUILD_VERSION_FIXTURE_001 = "241206.55345.468477"`
- `SUPPORTED_BUILD_VERSION_FIXTURE_002 = "250811.43331.492665"`

Current private enum:

- `SupportedReplayHeaderTupleV1::Fixture001Exact`
- `SupportedReplayHeaderTupleV1::Fixture002Exact`

Current `supported_replay_header_tuple_v1(...)` behavior:

- rejects any major/minor/net/game_type/ReplayVersion mismatch before matching `BuildVersion`
- accepts only the fixture_001 exact BuildVersion
- accepts only the fixture_002 exact BuildVersion
- rejects any other BuildVersion by returning `None`
- caller converts `None` to `replay header parse error: unsupported-version`

Current header parse flow:

- reads `header_size` at offset 0
- reads `header_crc` at offset 4 as layout only
- computes `header_end = 8 + header_size`
- parses only `bytes[8..header_end]`
- reads major/minor/net/game_type
- parses top-level properties before the version allowlist check because `ReplayVersion` and
  `BuildVersion` are selected properties
- requires the `None` terminator to end exactly at the header boundary
- performs the unsupported-version check after selected property parsing and before constructing
  `ReplayHeader`
- permits trailing bytes after `header_end`

Current selected property set:

- `Id`
- `NumFrames`
- `ReplayName`
- `Date`
- `MapName`
- `ReplayVersion`
- `BuildVersion`
- `MaxChannels`
- `MatchType`
- `TeamSize`
- `RecordFPS`

Current selected property parsing flow:

- selected dispatch is key based
- selected property value bytes are first bounded by declared `property_size`
- selected `StrProperty` and `NameProperty` map to `FieldValue::Text`
- selected `IntProperty` maps to `FieldValue::Integer`
- selected finite `FloatProperty` maps to `FieldValue::Float`
- `Id` maps to `ReplayHeader.replay_id` after exact 32 ASCII-hex validation
- `NumFrames` maps to `ReplayHeader.total_frames` if present and non-negative
- selected duplicate keys are mapping errors
- selected wrong admitted kinds are mapping errors
- selected unadmitted kinds are `unsupported-property`

Current non-selected property skipping flow:

- non-selected `ArrayProperty`, `FloatProperty`, `IntProperty`, `NameProperty`, `QWordProperty`,
  and `StrProperty` are skipped by declared `property_size`
- any other property kind returns `replay header parse error: unsupported-property`
- `BoolProperty` is currently not an admitted skipped kind
- the current synthetic BoolProperty test uses non-selected key `Unselected`, kind
  `BoolProperty`, value byte `1`, and expects `unsupported-property`

Current test shape:

- fixture_001 happy path and header-only stop-boundary are covered in one regression test
- fixture_002 exact happy path is covered
- fixture_002 header-only stop-boundary is covered with `header_size == 11273` and
  `header_end == 11281`
- unknown BuildVersion rejection is covered
- `ReplayInput::File` unsupported-input is covered
- `header_crc` non-validation is covered
- malformed, truncated, duplicate, wrong-kind, selected-array, non-finite float, and unsupported
  property boundaries are covered

Current closed behavior:

- no fixture_003 BuildVersion constant exists in source
- no `Fixture003Exact` enum variant exists in source
- no fixture_003 label/path/test exists in source
- no `bForfeit` marker exists in source
- no `content_crc` read or validation exists in the MIMIR parser
- no body/raw-state/frame/event parsing exists
- no backend replay parser dependency exists in manifests/lockfile

## Exact Future Tuple Code Plan

Future implementation file boundary:

- parser code changes may touch only `crates/mimir-replay/src/lib.rs`
- no root `Cargo.toml` change
- no root `Cargo.lock` change
- no `crates/mimir-skill/src/lib.rs` change
- no `crates/mimir-types/src/lib.rs` change
- no `crates/mimir-cli`, `crates/mimir-io`, `crates/mimir-export`, or dependency change

Future tuple patch shape:

- add `const SUPPORTED_BUILD_VERSION_FIXTURE_003: &str = "251020.62592.500294";`
- add private enum variant `SupportedReplayHeaderTupleV1::Fixture003Exact`
- extend `supported_replay_header_tuple_v1(...)` with exactly one new match arm:
  `SUPPORTED_BUILD_VERSION_FIXTURE_003 => Some(SupportedReplayHeaderTupleV1::Fixture003Exact)`

The function must continue to accept only these exact tuples:

| Variant | major | minor | net | game_type | ReplayVersion | BuildVersion |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| `Fixture001Exact` | `868` | `32` | `10` | `TAGame.Replay_Soccar_TA` | `8` | `241206.55345.468477` |
| `Fixture002Exact` | `868` | `32` | `10` | `TAGame.Replay_Soccar_TA` | `8` | `250811.43331.492665` |
| `Fixture003Exact` | `868` | `32` | `10` | `TAGame.Replay_Soccar_TA` | `8` | `251020.62592.500294` |

Required rejection behavior:

- reject any other `BuildVersion`
- reject any other major version
- reject any other minor version
- reject any other net version
- reject any other game type
- reject any other `ReplayVersion`
- keep the same `unsupported-version` error category for non-allowlisted tuples

Forbidden future tuple predicates:

- do not inspect path/hash/filename/provenance/artifact id
- do not inspect fixture id
- do not inspect `ReplayInput::Memory.label`
- do not inspect body bytes
- do not inspect `header_crc` or `content_crc` as support predicates
- do not add wildcard, prefix, range, regex, date-family, or version-family BuildVersion logic
- do not admit all `ReplayVersion = 8`

## Exact Future BoolProperty Skip-Only Code Plan

Future behavior:

- add support for skipping top-level non-selected `BoolProperty` only
- do not map `BoolProperty` to metadata
- do not add `bForfeit` to the selected property set
- do not add `BoolProperty -> FieldValue::Boolean` mapping
- do not allow selected BoolProperty parsing unless separately reopened
- do not use declared `property_size` alone for BoolProperty
- keep parser header-only; do not parse body/raw-state/frame/event data

Required byte-layout boundary:

- property key is already read by `parse_top_level_properties`
- property kind is `BoolProperty`
- declared `property_size` must be exactly `0` for this admitted shape
- ignored field handling must remain exactly where it is now: the caller reads the existing
  four-byte ignored field before selected/non-selected dispatch
- exactly one value byte must be consumed after the ignored field for non-selected BoolProperty
- accepted value bytes are only `0` and `1`
- any other value byte must fail as malformed-property through the existing malformed parse
  boundary or equivalent existing error category
- insufficient byte for the one value byte must fail through the existing insufficient parse
  boundary or equivalent existing error category

Recommended helper shape:

```rust
const KIND_BOOL: &str = "BoolProperty";

fn skip_non_selected_bool_property(
    key: &str,
    cursor: &mut HeaderCursor<'_>,
    value_len: usize,
) -> Result<()> {
    if value_len != 0 {
        return Err(malformed(format!(
            "non-selected BoolProperty {key} has declared size {value_len}, expected 0"
        )));
    }

    let raw = cursor.read_exact(1, format!("property {key} BoolProperty value"))?;
    match raw[0] {
        0 | 1 => Ok(()),
        value => Err(malformed(format!(
            "non-selected BoolProperty {key} has invalid value byte {value}"
        ))),
    }
}
```

Recommended integration point:

- add a dedicated `KIND_BOOL` arm in `skip_non_selected_property(...)`
- call the helper only after `is_selected_property(&key)` has returned false
- keep `KIND_BOOL` out of `is_admitted_property_kind(...)` unless a separate policy intentionally
  changes the selected wrong-kind error boundary

This preserves selected BoolProperty as unsupported. If a selected metadata key appears with
`BoolProperty`, it must still fail as `unsupported-property` or equivalent existing unsupported
boundary and must not produce a `FieldValue`.

Generic unknown BoolProperty may be skipped only if it is top-level, non-selected, and exactly
matches the admitted byte-layout constraints. Nested arrays, body data, and semantic BoolProperty
mapping remain closed.

## Exact Future Test Plan

Future tests must be added only in `crates/mimir-replay/src/lib.rs`.

### A. Fixture 001 Regression

- existing fixture_001 happy path still passes
- existing fixture_001 expected `ReplayHeader` remains unchanged
- fixture_001 header-only stop-boundary still passes
- no fixture_001 metadata key changes are admitted

### B. Fixture 002 Regression

- existing fixture_002 happy path still passes
- existing fixture_002 expected `ReplayHeader` remains unchanged
- fixture_002 header-only stop-boundary still passes
- no fixture_002 metadata key changes are admitted

### C. Fixture 003 Exact Happy Path

- add `FIXTURE_003_LABEL = "rl_replay_header_fixture_003"`
- add `FIXTURE_003_PATH = r"D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay"`
- read fixture bytes through the same fixture helper pattern
- use `ReplayInput::Memory`
- if the file is missing or unreadable, skip with an explicit fixture-missing message and do not
  claim fixture_003 parser success

Expected assertions:

- `replay_id = ReplayId::new("DF72482811F0B757082C458D84251EFF")`
- `source_label = "rl_replay_header_fixture_003"`
- `total_frames = Some(8288)`
- `metadata.ReplayName = FieldValue::Text("asdasd")`
- `metadata.Date = FieldValue::Text("2025-11-01 19-20-48")`
- `metadata.MapName = FieldValue::Text("cs_day_p")`
- `metadata.ReplayVersion = FieldValue::Integer(8)`
- `metadata.BuildVersion = FieldValue::Text("251020.62592.500294")`
- `metadata.MaxChannels = FieldValue::Integer(2047)`
- `metadata.MatchType = FieldValue::Text("Online")`
- `metadata.TeamSize = FieldValue::Integer(2)`
- `metadata.RecordFPS = FieldValue::Float(30.0)`
- `metadata.get("bForfeit").is_none()`

### D. Fixture 003 Header-Only Stop-Boundary

- compute `header_size` from fixture_003 first four bytes
- assert `header_size == 11190`
- compute `header_end = 8 + header_size`
- assert `header_end == 11198`
- slice fixture_003 bytes to exactly `bytes[..11198]`
- parser must return the same fixture_003 `ReplayHeader` candidate output as the full byte input
- no body bytes are required
- `bForfeit` remains absent from metadata

### E. Non-Selected BoolProperty Skip-Only Regression

- add a synthetic header helper that can encode declared property size separately from actual
  emitted value bytes
- build an otherwise allowlisted synthetic header, preferably using fixture_001 BuildVersion to
  isolate BoolProperty skip behavior from fixture_003 file availability
- add a non-selected property with:
  - key: any non-selected key such as `UnselectedBool`
  - kind: `BoolProperty`
  - declared size: `0`
  - ignored field: current synthetic zero ignored field
  - value byte: `1` or `0`
- assert the parser succeeds
- assert no metadata key is produced for that BoolProperty
- assert selected metadata remains limited to the selected scalar keys in the synthetic header

### F. Selected BoolProperty Remains Unsupported

- build a synthetic header where a selected key uses `BoolProperty`
- use the admitted BoolProperty byte layout: declared size `0`, ignored field present, one value
  byte
- recommended selected key: `Id` in a `minimal_without_id` synthetic header
- assert the parser fails with `unsupported-property` or equivalent existing unsupported boundary
- assert no `FieldValue::Boolean` is produced
- assert no selected BoolProperty mapping is admitted by the test name or assertion text

### G. Malformed BoolProperty Tests

Required malformed tests:

- non-selected `BoolProperty` with declared `property_size != 0` fails unless a separate policy
  admits another layout
- non-selected `BoolProperty` with missing one-byte value fails cleanly through the existing
  insufficient boundary or equivalent
- non-selected `BoolProperty` with invalid value byte not `0` or `1` fails through the existing
  malformed boundary or equivalent

Test construction notes:

- the missing-value test should construct a header that ends immediately after the BoolProperty
  ignored field so the helper attempts to read the required one value byte and fails cleanly
- the invalid-value test should use declared size `0` plus value byte such as `2`
- malformed BoolProperty tests must not claim body parsing or content CRC behavior

### H. Unknown BuildVersion Rejection

- preserve the existing unknown BuildVersion rejection test
- ensure an otherwise-supported tuple with unallowlisted BuildVersion still returns
  `unsupported-version`
- this must prove no wildcard BuildVersion support was introduced by fixture_003 addition

### I. Preserve Existing Boundaries

Existing tests must continue to prove:

- `ReplayInput::File` remains unsupported
- `header_crc` non-validation remains unchanged
- no `content_crc` read/validation is added
- no body/raw-state/frame/event parser success is claimed
- unsupported, duplicate, wrong-kind, non-finite, selected-array, malformed, and truncated
  selected-property tests remain

Synthetic tuple and BoolProperty tests must still run even if fixture_003 file-specific tests skip.

## Exact Future Artifact And Status Plan

The next implementation pass should create:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_EXACT_TUPLE_BOOLPROPERTY_SKIP_IMPLEMENTATION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_exact_tuple_boolproperty_skip_implementation_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_exact_tuple_boolproperty_skip_implementation_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_exact_tuple_boolproperty_skip_implementation_status.txt`

The implementation pass must validate:

- `cargo fmt --all`
- `cargo check --workspace --all-targets --all-features`
- `cargo test -p mimir-replay -- --nocapture`
- `cargo test -p mimir-skill -- --nocapture`
- `cargo test --workspace --all-targets --all-features`
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`
- `cargo test -p mimir-export -- --list`

The implementation status artifact must state whether fixture_003 tests ran or skipped. If a
fixture-specific fixture_003 test skips because the file is missing, the implementation pass must
not claim fixture_003 parser success.

## Direct Implementation Safety

Direct implementation is safe next, but only within this exact boundary:

- future parser code file: `crates/mimir-replay/src/lib.rs`
- exact three-tuple allowlist only
- exact non-selected BoolProperty skip-only helper or dedicated arm only
- exact BoolProperty byte layout: declared size `0`, ignored field already read, consume one
  value byte, value byte must be `0` or `1`
- no BoolProperty metadata mapping
- no `bForfeit` metadata
- fixture_001 regression
- fixture_002 regression
- fixture_003 exact happy path
- fixture_003 header-only stop-boundary
- unknown BuildVersion rejection
- selected BoolProperty unsupported test
- malformed BoolProperty tests
- no manifest/lockfile/dependency change

One more planning pass is not required unless a future implementer refuses the exact helper shape
or wants to broaden BoolProperty, version, input, CRC, replay-source, body, runtime, CLI, export, or
dependency behavior. Any such broadening must be separately reopened and is not authorized here.

## Explicit Non-Claims

This pass does not claim:

- fixture_003 parser success
- fixture_003 is supported by `MinimalReplayHeaderReader` now
- fixture_003 tuple is implemented now
- a third supported tuple exists in code now
- BoolProperty skip is implemented now
- `BoolProperty -> FieldValue::Boolean` metadata mapping
- `bForfeit` metadata mapping
- broad parser success
- broad version-family support
- wildcard BuildVersion support
- all `ReplayVersion = 8` support
- future unknown build support
- `ReplayInput::File` support
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- `content_crc` read or validation
- body/raw-state/frame/event parsing
- export/runtime/CLI integration
- backend replay parser dependency in MIMIR

## What Remains Closed

Still closed after this pass:

- parser source changes
- `MinimalReplayHeaderReader` behavior changes
- fixture_003 parser-success admission
- fixture_003 tuple implementation
- BoolProperty skip implementation
- BoolProperty metadata mapping
- `bForfeit` metadata mapping
- broad parser-success admission
- broad version-family support
- wildcard BuildVersion support
- all `ReplayVersion = 8` support
- future unknown build support
- `ReplayInput::File`
- replay-source materialization
- CRC validation
- `content_crc` read/validation in MIMIR parser code
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Affected Files

This pass creates only:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_EXACT_TUPLE_BOOLPROPERTY_SKIP_IMPLEMENTATION_PLANNING_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_exact_tuple_boolproperty_skip_implementation_planning_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_exact_tuple_boolproperty_skip_implementation_planning_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_exact_tuple_boolproperty_skip_implementation_planning_status.txt`

No Rust source, manifests, lockfile, dependency graph, runtime, CLI, export, IO, or type files are
changed.

## Invariants Preserved

- Current parser remains exact two-tuple allowlist gated for fixture_001 and fixture_002 only.
- Fixture_003 remains unsupported by current `MinimalReplayHeaderReader`.
- Unknown BuildVersion remains rejected by current parser behavior.
- `ReplayInput::Memory` remains the only admitted input path.
- `ReplayInput::File` remains unsupported.
- Header-only parsing remains the admitted parser scope.
- CRC validation remains absent.
- Body/raw-state/frame/event parsing remains absent.
- `bForfeit` remains excluded from metadata.
- `BoolProperty -> FieldValue::Boolean` remains closed.
- No backend replay parser dependency is added.

## Rollback Strategy

Rollback is deletion of the four docs/executor artifacts created by this pass. No parser source,
manifest, lockfile, dependency, runtime, CLI, IO, export, or types rollback is required because no
such files are modified.

## Next Stage

Outcome A next pass may directly implement only the exact Fixture003Exact tuple plus exact
non-selected BoolProperty skip-only handling in `crates/mimir-replay/src/lib.rs`, along with the
exact tests and implementation artifacts listed above.

No broad parser expansion is authorized.
