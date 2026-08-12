# MIMIR Skill Forge BC Replay Header Parser Fixture 003 Supported Version Policy Planning Reopen V1

Pass date: 2026-05-06

## Purpose

Reopen fixture_003 supported-version policy planning from the admitted fixture_003 report,
mapping, and BoolProperty closure evidence.

This is a docs/artifacts-only planning pass. It does not implement parser code, modify
`MinimalReplayHeaderReader`, add fixture_003 as a supported tuple, claim fixture_003 parser
success, broaden parser scope, add file input support, validate CRCs, parse body/raw-state/frame
or event data, add dependencies, or wire CLI/runtime/export behavior.

The question for this pass is only whether fixture_003 can be safely planned as a future exact
supported tuple, with fixture_003 parser success still blocked until exact non-selected
`BoolProperty` skip-only parser handling is also implemented.

## Selected Outcome

Outcome A.

Fixture_003 supported-version policy planning is reopened and complete for the current evidence.
The selected future policy is an exact three-tuple allowlist:

- `SupportedReplayHeaderTupleV1::Fixture001Exact`
- `SupportedReplayHeaderTupleV1::Fixture002Exact`
- `SupportedReplayHeaderTupleV1::Fixture003Exact`

`Fixture003Exact` is planned only as exact tuple support. It is not broad version-family support,
not wildcard `BuildVersion` support, not all-`ReplayVersion = 8` support, and not future unknown
build support.

No parser-success is claimed for fixture_003 now. No parser code changed now. No third tuple was
implemented now. Fixture_003 parser success remains blocked until a later implementation pass adds
both exact tuple support and exact non-selected `BoolProperty` skip-only handling.

## Fixture Identity Verification

Fixture identities were reverified from local bytes before this artifact was written.

| Fixture | Path | Byte length | SHA-256 | First four bytes as LE i32 | Extension | > 8 bytes |
| --- | --- | ---: | --- | ---: | --- | --- |
| `rl_replay_header_fixture_001` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | `3001021` | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` | `13200` | `.replay` | yes |
| `rl_replay_header_fixture_002` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` | `2632903` | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` | `11273` | `.replay` | yes |
| `rl_replay_header_fixture_003` | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_003.replay` | `1638538` | `20444C8352123637212A752783A5D4A446A4235985E6530CD2030362F142E2DC` | `11190` | `.replay` | yes |

Fixture_003 differs from fixture_001 by SHA-256: yes.

Fixture_003 differs from fixture_002 by SHA-256: yes.

These are identity and audit facts only. Path, filename, byte length, SHA-256, fixture id,
artifact id, and provenance are not parser facts and must not become support predicates.

## Re-Audited Inputs

Inspected before writing this artifact:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_BOOLPROPERTY_NON_SELECTED_ERROR_BOUNDARY_CLOSURE_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_boolproperty_non_selected_error_boundary_closure_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_boolproperty_non_selected_error_boundary_closure_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_boolproperty_non_selected_error_boundary_closure_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_MAPPING_ERROR_BOUNDARY_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_REPORT_ADMISSION_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_AUDIT_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_002_EXACT_SUPPORTED_TUPLE_IMPLEMENTATION_V1.md`
- `crates/mimir-replay/README.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-types/src/lib.rs`
- `crates/mimir-skill/src/lib.rs`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

The fixture_003 report and structural report remain external/report evidence only. They are not
MIMIR parser output and not fixture_003 parser-success evidence.

## Current Supported-Version Implementation Audit

Current `MinimalReplayHeaderReader` implementation in `crates/mimir-replay/src/lib.rs` remains an
explicit opt-in reader for `ReplayInput::Memory` only. `ReplayInput::File(_)` returns
`replay header parse error: unsupported-input`.

Current exact tuple constants and policy shape:

| Component | Current exact value |
| --- | --- |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `10` |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| `ReplayVersion` | `8` |
| fixture_001 `BuildVersion` | `241206.55345.468477` |
| fixture_002 `BuildVersion` | `250811.43331.492665` |

Current private enum:

- `SupportedReplayHeaderTupleV1::Fixture001Exact`
- `SupportedReplayHeaderTupleV1::Fixture002Exact`

Current `supported_replay_header_tuple_v1(...)` behavior:

- rejects any major/minor/net/game type/ReplayVersion mismatch before `BuildVersion` matching
- maps `BuildVersion = "241206.55345.468477"` to `Fixture001Exact`
- maps `BuildVersion = "250811.43331.492665"` to `Fixture002Exact`
- maps any other `BuildVersion` to `None`
- caller converts `None` to `replay header parse error: unsupported-version`

The current version policy does not depend on fixture path, hash, filename, provenance, artifact
id, fixture id, label, header CRC, content CRC, body bytes, or any replay-source fact.

Adding fixture_003 as a third exact tuple would not require a broad version-family predicate,
manifest change, lockfile change, backend replay parser dependency, `ReplayInput::File` support,
CRC validation, or body/raw-state/frame/event parsing. It would require a code change in
`crates/mimir-replay/src/lib.rs`, but that implementation is not performed in this pass.

Adding fixture_003 parser success would also require exact non-selected `BoolProperty` skip-only
handling because fixture_003 contains top-level `bForfeit` and current parser behavior still
rejects `BoolProperty` as `unsupported-property`.

## Fixture Tuple Comparison

Only report/type-level evidence is used for this comparison.

| Component | fixture_001 | fixture_002 | fixture_003 |
| --- | --- | --- | --- |
| `major_version` | `868` | `868` | `868` |
| `minor_version` | `32` | `32` | `32` |
| `net_version` | `Some(10)` | `Some(10)` | `Some(10)` |
| `game_type` | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` | `TAGame.Replay_Soccar_TA` |
| `ReplayVersion` | `8` | `8` | `8` |
| `BuildVersion` | `241206.55345.468477` | `250811.43331.492665` | `251020.62592.500294` |

Classification:

- fixture_003 may be planned as an additional exact supported tuple.
- this does not imply wildcard `BuildVersion` support.
- this does not imply all `868/32/net10/soccar/ReplayVersion=8` builds are supported.
- this does not imply parser success for future unknown fixtures.
- this does not imply broad parser-success.
- `BoolProperty` skip-only remains a separate implementation prerequisite for fixture_003.

## BoolProperty Skip-Only Prerequisite

Prior BoolProperty closure selected Outcome A:

- `bForfeit` is report-only evidence
- `bForfeit` is excluded from selected metadata
- `bForfeit` is excluded from `ReplayHeader` output
- `BoolProperty -> FieldValue::Boolean` remains closed
- current parser behavior remains `unsupported-property` for `BoolProperty`
- future non-selected `BoolProperty` skip-only handling may be planned

Fixture_003 `bForfeit` evidence:

| Field | Value |
| --- | --- |
| key | `bForfeit` |
| structural path | `header.properties[1]` |
| kind | `BoolProperty` |
| byte range | `[89,128)` |
| declared size | `0` |
| scanner consumed | `1` |
| generated value summary | `true` |
| selected metadata mapping | excluded |
| `ReplayHeader` output | excluded |

The declared size and consumed-byte shape is a hard implementation caveat. A future
implementation must not skip `BoolProperty` by declared size alone because declared size is `0`
while the scanner consumed `1` byte. It must either implement the exact one-byte non-selected
`BoolProperty` value layout or fail cleanly.

Fixture_003 parser success may not be claimed until both conditions are true:

1. `Fixture003Exact` is implemented in the exact supported tuple allowlist.
2. Exact non-selected `BoolProperty` skip-only parser handling is implemented and verified.

## Supported-Version Policy Options Considered

Option A: exact three-tuple allowlist.

- add a future `Fixture003Exact` variant for `BuildVersion = "251020.62592.500294"`
- keep all shared tuple components exact
- keep unknown builds rejected
- keep path/hash/provenance out of parser predicates
- keep fixture_003 parser success blocked on `BoolProperty` skip-only implementation
- selected

Option B: partial reopen due to policy ambiguity.

- would be required if `BuildVersion` allowlist shape, `BoolProperty` prerequisite,
  broad `ReplayVersion = 8` risk, or parser-success boundary remained ambiguous
- rejected because the current evidence is sufficient to plan exact tuple support without
  broadening support or claiming parser success

Option C: cannot safely reopen.

- would be required if fixture identity or tuple evidence were insufficient even for exact tuple
  planning
- rejected because fixture identity and report/type-level tuple evidence are sufficient for a
  planning-only exact tuple decision

Option D: stop/no-op.

- would be required if the pass could not be bounded
- rejected because the boundary is narrow: docs/artifacts-only planning, no implementation

## Selected Future Policy

The selected future supported-version policy is exact allowlist only:

- `SupportedReplayHeaderTupleV1::Fixture001Exact`
- `SupportedReplayHeaderTupleV1::Fixture002Exact`
- `SupportedReplayHeaderTupleV1::Fixture003Exact`

Planned exact fixture_003 tuple:

| Component | Exact planned value |
| --- | --- |
| `major_version` | `868` |
| `minor_version` | `32` |
| `net_version` | `10` |
| `game_type` | `TAGame.Replay_Soccar_TA` |
| `ReplayVersion` | `8` |
| `BuildVersion` | `251020.62592.500294` |

This future policy is not implemented now.

## Rejected Policies

Rejected for this pass and for the selected future policy:

- wildcard `BuildVersion`
- `BuildVersion` prefix, date-family, regex, range, contains, or version-family matching
- all `ReplayVersion = 8` support
- all `major=868/minor=32/net=10/game_type=TAGame.Replay_Soccar_TA` support
- future unknown build support
- path/hash/filename/provenance/artifact-id/fixture-id based parser support
- `ReplayInput::File` support
- replay-source materialization
- CRC validation
- `content_crc` read or validation in MIMIR parser code
- body/raw-state/frame/event parsing
- `BoolProperty -> FieldValue::Boolean` replay-header metadata mapping
- adding `bForfeit` to selected metadata
- export/runtime/CLI integration
- backend replay parser dependency in MIMIR

## Future Implementation Boundary

If Outcome A is later implemented, the allowed future implementation boundary is:

- modify only `crates/mimir-replay/src/lib.rs`
- no `Cargo.toml` changes
- no `Cargo.lock` changes
- no `crates/mimir-skill` changes
- no `crates/mimir-types` changes
- no `crates/mimir-export`, `crates/mimir-io`, or `crates/mimir-cli` changes
- extend the exact tuple allowlist with `Fixture003Exact`
- keep `ReplayInput::Memory` only
- keep `ReplayInput::File` unsupported
- keep header-only parsing ending at `8 + header_size`
- keep `header_crc` layout-read only
- keep CRC non-validation
- do not read or validate `content_crc`
- keep body/raw-state/frame/event parsing closed
- do not map `BoolProperty` to metadata
- do not add `bForfeit` to selected metadata
- add exact non-selected `BoolProperty` skip-only handling before fixture_003 parser success is
  claimed
- no backend replay parser dependency
- no broad parser framework

## Future Test Boundary

Future tests should be added only after tuple support and skip-only implementation are both scoped.

Required future test boundary:

- fixture_003 exact happy-path test after tuple plus skip-only implementation
- fixture_003 header-only stop-boundary test ending at `8 + header_size`
- fixture_003 expected candidate output comparison against admitted evidence
- explicit assertion that `bForfeit` is absent from metadata
- non-selected `BoolProperty` skip-only regression
- selected `BoolProperty` remains unsupported regression
- malformed `BoolProperty` failure regression
- unknown `BuildVersion` rejection regression proving unknown builds remain rejected
- fixture_001 regression preserved
- fixture_002 regression preserved
- `ReplayInput::File` remains unsupported regression preserved
- CRC non-validation boundary preserved

## Explicit Non-Claims

This pass does not claim:

- fixture_003 parser success
- fixture_003 is supported by `MinimalReplayHeaderReader` now
- fixture_003 supported-version policy is implemented now
- a third supported tuple exists in code now
- broad parser success
- broad version-family support
- all `ReplayVersion = 8` support
- wildcard `BuildVersion` support
- future unknown build support
- `ReplayInput::File` support
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- `content_crc` read or validation
- body/raw-state/frame/event parsing
- `BoolProperty` parser support today
- `BoolProperty -> FieldValue::Boolean` metadata mapping
- `bForfeit` metadata mapping
- export/runtime/CLI integration
- backend replay parser dependency in MIMIR

## What Remains Closed

Still closed after this pass:

- parser code changes
- `MinimalReplayHeaderReader` behavior changes
- fixture_003 parser-success admission
- fixture_003 supported-version implementation
- third supported tuple in code
- broad parser-success admission
- broad version-family support
- broad `ReplayVersion = 8` support
- wildcard `BuildVersion` support
- current `BoolProperty` parser support
- `BoolProperty` metadata mapping
- `ReplayInput::File`
- replay-source materialization
- CRC validation
- `content_crc` read/validation in MIMIR parser code
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Affected Files

This pass creates only:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_SUPPORTED_VERSION_POLICY_PLANNING_REOPEN_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_supported_version_policy_planning_reopen_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_supported_version_policy_planning_reopen_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_003_supported_version_policy_planning_reopen_status.txt`

No Rust source, manifests, lockfile, dependency graph, runtime, CLI, export, IO, or type files are
changed.

## Invariants Preserved

- Current parser remains exact two-tuple allowlist gated for fixture_001 and fixture_002 only.
- Fixture_003 remains unsupported by current `MinimalReplayHeaderReader`.
- Unknown `BuildVersion` remains rejected by current parser behavior.
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

Outcome A next pass may be fixture_003 exact supported tuple plus non-selected `BoolProperty`
skip-only implementation planning.

Preferred sequencing is one implementation-planning pass before code. That planning pass must
specify:

- exact tuple allowlist shape
- exact non-selected `BoolProperty` skip-only byte-layout boundary
- fixture_003 happy-path and header-only tests
- malformed `BoolProperty` tests
- selected `BoolProperty` unsupported tests
- unknown `BuildVersion` rejection tests
- fixture_001 and fixture_002 regression preservation

No broad parser expansion is authorized.
