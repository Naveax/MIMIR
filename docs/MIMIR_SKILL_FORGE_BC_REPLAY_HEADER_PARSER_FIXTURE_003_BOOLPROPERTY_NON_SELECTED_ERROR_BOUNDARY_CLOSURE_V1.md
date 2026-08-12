# MIMIR Skill Forge BC Replay Header Parser Fixture 003 BoolProperty Non-Selected Error-Boundary Closure V1

## Purpose

Close the fixture_003 top-level non-selected `BoolProperty` policy direction without changing parser
code, admitting parser success, adding a supported-version tuple, or mapping `BoolProperty` to
`ReplayHeader.metadata`.

This pass is docs/artifacts-only. It classifies `bForfeit` for future fixture_003 planning and keeps
the current MIMIR parser behavior unchanged.

## Selected Outcome

Outcome A.

BoolProperty/non-selected property structural error-boundary closure is complete for the currently
admitted external/report evidence. `bForfeit` is classified as a non-selected `BoolProperty` that
may be planned for future skip-only handling, not metadata mapping.

This is a future policy direction only. Current `MinimalReplayHeaderReader` behavior is unchanged and
still rejects `BoolProperty` as an unsupported property kind.

## Fixture Identity Verification

Fixture identity was reverified from local bytes before this artifact was written.

| fixture | path | byte length | SHA-256 | first four bytes as i32 LE | status |
| --- | --- | ---: | --- | ---: | --- |
| `rl_replay_header_fixture_001` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | 3001021 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | 13200 | verified |
| `rl_replay_header_fixture_002` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` | 2632903 | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` | 11273 | verified |
| `rl_replay_header_fixture_003` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay` | 1638538 | `20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC` | 11190 | verified |

Additional fixture_003 identity checks:

- extension is `.replay`
- byte length is greater than 8
- fixture_003 SHA-256 differs from fixture_001 SHA-256
- fixture_003 SHA-256 differs from fixture_002 SHA-256
- path, hash, filename, provenance, and fixture id remain external audit facts only, not parser facts

## Evidence Inputs

The required inputs were inspected before classification:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_MAPPING_ERROR_BOUNDARY_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_mapping_error_boundary_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_mapping_error_boundary_admission_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_mapping_error_boundary_admission_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_REPORT_ADMISSION_V1.md`
- `artifacts/replay_header_reports/rl_replay_header_fixture_003_report.txt`
- `artifacts/replay_header_reports/rl_replay_header_fixture_003_structural_report.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_AUDIT_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REPLAYHEADER_MAPPING_POLICY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_MAPPING_GAP_ERROR_BOUNDARY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_REMAINING_NON_MAPPING_BYTE_LAYOUT_ERROR_BOUNDARY_ADMISSION_V1.md`
- `crates/mimir-replay/README.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

The fixture_003 report and structural report both state that they are external/report evidence, not
MIMIR parser output and not parser-success evidence.

## Current Parser Behavior Inspection

Current selected property set in `crates/mimir-replay/src/lib.rs`:

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

`bForfeit` is not selected.

Current non-selected property behavior:

- non-selected `ArrayProperty`, `FloatProperty`, `IntProperty`, `NameProperty`, `QWordProperty`, and
  `StrProperty` are skipped by bounded `property_size`
- unknown or unadmitted property kinds return `replay header parse error: unsupported-property`
- `BoolProperty` is not defined as an admitted kind
- a synthetic test currently proves non-selected `BoolProperty` is rejected as
  `unsupported-property`

Current selected property behavior:

- selected fields are parsed by key-specific branches
- no selected key maps from `BoolProperty`
- no selected key maps to `FieldValue::Boolean`
- a selected key with unadmitted kind `BoolProperty` would still be rejected, not mapped

Structural separation for future work:

- top-level dispatch already separates selected keys from non-selected keys before value handling
- therefore a future `crates/mimir-replay/src/lib.rs` change could add skip-only handling for
  non-selected `BoolProperty` without adding `BoolProperty` metadata mapping
- this pass does not implement that change

## FieldValue And Mapping Policy Inspection

`mimir-types::FieldValue` includes:

- `Text(String)`
- `Integer(i64)`
- finite `Float(f64)`
- `Boolean(bool)`
- `StringList(Vec<String>)`

`FieldValue::Boolean` existence is not authorization to map replay-header `BoolProperty` values.

Existing replay-header mapping policy admits selected metadata carriers for:

- `StrProperty` and `NameProperty` to `FieldValue::Text`
- `IntProperty` to `FieldValue::Integer`
- finite `FloatProperty` to `FieldValue::Float`

Existing policy does not admit `BoolProperty -> FieldValue::Boolean` for replay-header metadata.
Existing fixture_003 mapping admission deliberately excludes `bForfeit` from selected metadata
candidate output.

## bForfeit Classification

Admitted fixture_003 structural report evidence for `bForfeit`:

| item | value |
| --- | --- |
| property key | `bForfeit` |
| kind | `BoolProperty` |
| structural path | `header.properties[1]` |
| byte range | `[89,128)` |
| declared size | `0` |
| scanner consumed | `1` |
| generated value summary | `true` |
| selected metadata key | no |
| selected `ReplayHeader` field | no |

Classification:

- selected metadata mapping: excluded
- `ReplayHeader` mapping output: excluded
- report-only evidence: admitted
- `BoolProperty -> FieldValue::Boolean`: closed and deferred
- current parser behavior: hard `unsupported-property`
- future parser policy direction: may plan non-selected `BoolProperty` skip-only handling

The `declared size = 0` plus `scanner consumed = 1` shape is critical. A future implementation must
not skip by declared size alone for `BoolProperty`; it must support the exact one-byte value layout
or fail cleanly.

## Options Considered

Option 1: hard unsupported-property remains.

- safest current behavior
- blocks fixture_003 support even though `bForfeit` is not selected metadata
- remains true for current parser behavior
- rejected as the future policy direction because the selected/non-selected boundary allows a
  narrower skip-only plan

Option 2: non-selected `BoolProperty` skip-only policy.

- future parser may skip top-level non-selected `BoolProperty` values using exact byte-layout
  semantics
- `bForfeit` is not mapped
- selected `BoolProperty` remains unsupported unless separately reopened
- `BoolProperty -> FieldValue::Boolean` remains closed
- admits a narrow future planning direction without parser expansion in this pass
- selected as the future policy direction

Option 3: `BoolProperty` metadata mapping policy.

- would map `BoolProperty` to `FieldValue::Boolean`
- requires a separate replay-header metadata policy and implementation pass
- higher scope than needed for fixture_003 selected metadata
- rejected for this pass

## Selected Future Policy Direction

Future fixture_003 planning may use a non-selected `BoolProperty` skip-only boundary.

The selected policy direction is:

- `bForfeit` remains excluded from selected metadata
- `bForfeit` remains excluded from `ReplayHeader` output
- `BoolProperty -> FieldValue::Boolean` remains closed
- selected `BoolProperty` remains unsupported unless a separate metadata policy reopens it
- fixture_003 supported-version policy planning may proceed next as a docs-only planning reopen
- actual fixture_003 parser support remains blocked until a later implementation pass adds exact
  non-selected `BoolProperty` skip-only handling and separately admits the fixture_003 supported
  tuple

## Future Implementation Boundary

If this policy is later implemented, the allowed implementation boundary is:

- allowed future code file: `crates/mimir-replay/src/lib.rs` only
- allow skip-only handling for top-level non-selected `BoolProperty`
- do not map `BoolProperty` to metadata
- do not add `bForfeit` to selected metadata
- selected `BoolProperty` remains hard unsupported unless separately reopened
- unknown top-level non-selected `BoolProperty` may be skipped only if exact `BoolProperty` byte
  layout is supported
- malformed `BoolProperty` remains a malformed-property or insufficient-property error
- duplicate selected metadata rules remain unchanged
- supported-version tuple still requires separate policy and implementation
- no body/raw-state/frame/event parsing
- no CRC validation
- no dependencies
- no `ReplayInput::File` support

Future implementation must not silently use generic `property_size` skipping for `BoolProperty`
because fixture_003 evidence reports `declared size = 0` and `scanner consumed = 1`.

## Future Test Boundary

No tests are implemented in this pass. Required future tests for an implementation pass:

- fixture_003 parser support test must fail until both supported-version and skip-only
  `BoolProperty` implementation are actually added
- future fixture_003 happy path must assert `bForfeit` is absent from metadata
- future fixture_003 header-only slice must pass only after exact tuple plus skip-only
  `BoolProperty` support
- future non-selected `BoolProperty` skip test must prove parser can skip `bForfeit` without mapping
  it
- future selected `BoolProperty` regression must prove selected `BoolProperty` mapping is still
  unsupported unless separately reopened
- future malformed `BoolProperty` test must fail cleanly
- future unknown `BuildVersion` rejection must remain unchanged
- fixture_001 and fixture_002 regressions must remain unchanged

## Deferred Policies And Blockers

Still deferred or blocked:

- fixture_003 supported-version policy
- third supported tuple
- parser-success for fixture_003
- broad parser-success
- broad `ReplayVersion = 8` support
- wildcard or version-family `BuildVersion` support
- `BoolProperty` parser implementation
- `BoolProperty -> FieldValue::Boolean` metadata mapping
- body/raw-state/frame/event parsing
- CRC validation
- `ReplayInput::File`
- replay-source materialization
- export/runtime/CLI integration
- backend replay parser dependency in MIMIR

## Explicit Non-Claims

This pass does not claim:

- fixture_003 is supported by `MinimalReplayHeaderReader`
- fixture_003 parser success
- broad parser success
- fixture_003 supported-version policy admission
- a third supported tuple
- parser behavior changed
- `BoolProperty` parser support exists today
- `BoolProperty` skip behavior exists today
- `BoolProperty -> FieldValue::Boolean` mapping
- `bForfeit` metadata mapping
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- content CRC read/validation in MIMIR parser code
- body/raw-state/frame/event parsing
- export/runtime/CLI integration
- backend replay parser dependency in MIMIR

## What Remains Closed

Closed after this pass:

- selected ReplayHeader metadata remains unchanged
- `bForfeit` remains report-only evidence
- `bForfeit` remains excluded from metadata
- `BoolProperty -> FieldValue::Boolean` remains closed
- current parser implementation remains unchanged
- fixture_003 supported-version policy remains closed
- third supported tuple remains absent
- parser-success for fixture_003 remains unclaimed
- broad parser scope remains closed

## Affected Files

This pass creates only:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_BOOLPROPERTY_NON_SELECTED_ERROR_BOUNDARY_CLOSURE_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_boolproperty_non_selected_error_boundary_closure_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_boolproperty_non_selected_error_boundary_closure_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_boolproperty_non_selected_error_boundary_closure_status.txt`

No Rust source, manifests, lockfile, runtime, CLI, export, IO, or type files are changed.

## Invariants Preserved

- `MinimalReplayHeaderReader` remains exact two-tuple allowlist gated for fixture_001 and fixture_002
- `ReplayInput::File` remains unsupported
- fixture_003 remains unsupported by current parser behavior
- selected metadata key set remains unchanged
- non-selected metadata values remain excluded from `ReplayHeader.metadata`
- no backend replay parser dependency is added
- no CRC validation is added
- no body/raw-state/frame/event parsing is added

## Rollback Strategy

Rollback is deletion of the four docs/executor artifacts created by this pass. No source or manifest
rollback is required because no parser code, manifests, lockfile, dependency, CLI, IO, export, or
types file is modified.

## Next Stage

The safer next pass is fixture_003 supported-version policy planning reopen as a docs-only planning
pass.

That next pass must carry this caveat explicitly:

- future implementation still requires exact non-selected `BoolProperty` skip-only parser boundary
- no `BoolProperty` metadata mapping is admitted
- no parser implementation occurs during supported-version policy planning
- no parser-success is claimed until supported-version and skip-only implementation are both
  actually implemented and verified
