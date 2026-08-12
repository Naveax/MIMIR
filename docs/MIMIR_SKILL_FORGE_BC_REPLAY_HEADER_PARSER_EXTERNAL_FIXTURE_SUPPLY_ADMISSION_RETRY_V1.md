# MIMIR Skill Forge BC Replay Header Parser External Fixture Supply Admission Retry v1

## A. Purpose

This pass retries external fixture supply/admission for the future minimal real Rocket League
replay header parser after the operator supplied a real `.replay` file at the preferred default
local path.

This is an evidence admission pass only. It does not implement parser code, does not implement
parser-success logic, does not add backend dependencies, does not create replay fixture bytes, does
not produce a `ReplayHeader`, and does not parse raw-state payloads, replay frames, or semantic
replay events.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The future reader owner remains:

- `mimir-replay`

The future reader type name remains:

- `RocketLeagueReplayHeaderReader`

The future real reader remains distinct from:

- `UnsupportedReplayReader`

The first admitted parser input remains exactly:

- `ReplayInput::Memory`

`ReplayInput::File` remains rejected or deferred until file support is explicitly reopened.

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Rocket League replay header parsing remains a shared `mimir-replay` capability candidate, not a
low-boost-recovery semantic operation.

This pass does not create or reopen a generic all-family replay, raw-state, frame, event, index,
export, materialization, carrier, locator, database, runtime CLI, async/background, rollout, or
corpus framework.

`mimir-skill` may consume a future real reader only through the existing `ReplayReader` contract
and the already-audited low-boost contract/realization chain.

## C. Current Prior No-Admission Summary

The immediate prior fixture supply/admission artifact selected:

- Outcome B

Prior no-admission facts:

- no real `.replay` fixture bytes were present
- no fixture evidence was admitted
- no fixture files were added
- external fixture supply remained required
- parser implementation remained closed
- parser-success logic remained closed

The trusted boundary before this retry remained:

- valid supported `ReplayInput::Memory` bytes may return a real `ReplayHeader` only after required
  fixture and byte-layout evidence are admitted
- invalid, malformed, insufficient, unsupported, non-memory, or deferred inputs must return
  structured errors only
- `UnsupportedReplayReader` remains truthful scaffold behavior and distinguishable from any future
  real reader
- `mimir_export` widening remains forbidden unless explicitly reopened

## D. Re-Audit Summary

Files re-audited before this retry artifact:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_EXTERNAL_FIXTURE_SUPPLY_ADMISSION_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_external_fixture_supply_admission_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_external_fixture_supply_admission_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_external_fixture_supply_admission_status.txt`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_MATERIALIZATION_ADMISSION_CONTRACT_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_EVIDENCE_ACQUISITION_PLAN_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_MINIMAL_REAL_REPLAY_HEADER_PARSER_IMPLEMENTATION_PLAN_V1.md`
- `docs/MIMIR_SKILL_FORGE_BC_REAL_REPLAY_PARSER_BACKEND_SELECTION_DECISION_V1.md`
- `crates/mimir-replay/src/lib.rs`
- `crates/mimir-replay/Cargo.toml`
- `crates/mimir-skill/src/lib.rs`
- `crates/mimir-skill/Cargo.toml`
- `Cargo.toml`
- `Cargo.lock`
- `docs/ARTIFACT_VERSIONING.md`
- `docs/DATA_CONTRACTS.md`
- `executor_mimir_skill_forge_v1_staged_delivery_rules.txt`

Current code facts re-confirmed:

- `mimir-replay` exposes `ReplayInput`, `ReplayHeader`, `ReplayReader`, and
  `UnsupportedReplayReader`.
- `ReplayInput` has `File(PathBuf)` and `Memory { label, bytes }`.
- `ReplayHeader` contains `replay_id`, `source_label`, `total_frames`, and `metadata`.
- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>` is the only reader contract.
- `UnsupportedReplayReader` is the only current `ReplayReader` implementation in
  `mimir-replay`.
- `UnsupportedReplayReader::read_header` returns an explicit scaffold error and produces no
  header.
- `crates/mimir-replay/Cargo.toml` has no replay parser backend dependency.
- `Cargo.lock` has no audited `boxcars`, `rattletrap`, `rrrocket`, `carball`, `rlreplay`,
  `subtr-actor`, or equivalent parser dependency.
- Existing synthetic opaque-byte arrays remain contract evidence for byte preservation only. They
  are not parser fixture evidence and are not valid Rocket League replay bytes.

## E. Searched Fixture Locations

The fixture search was limited to the allowed local candidate locations plus a repo-wide inventory
for visibility.

| Search target | Result |
| --- | --- |
| `MIMIR_REPLAY_FIXTURE_PATH` | set to `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`; resolves to the preferred fixture path |
| `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | found |
| `D:\RocketLeague bot\MIMIR\external_fixtures\*.replay` | one file found: `sample_001.replay` |
| `D:\RocketLeague bot\MIMIR\fixtures_external\*.replay` | directory missing; no files found |
| `D:\RocketLeague bot\MIMIR\private_fixtures\*.replay` | directory missing; no files found |
| repo-wide `rg --files -g '*.replay'` under `D:\RocketLeague bot\MIMIR` | one file found: `external_fixtures\sample_001.replay` |
| repo-wide recursive `Get-ChildItem -Recurse -Filter '*.replay'` under `D:\RocketLeague bot\MIMIR` | one file found: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |

No other `.replay` files were found under the allowed fixture locations or elsewhere in the MIMIR
repository root.

## F. Byte Length And Hash Verification

Operator-supplied expected facts:

- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`

Verified local facts:

- path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`
- byte length: `3001021`
- SHA-256: `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`

Verification result:

- the file exists
- actual byte length matches the expected byte length
- actual SHA-256 matches the expected SHA-256

The cryptographic hash is fixture integrity evidence only. It is not replay identity, replay id
derivation, header layout evidence, frame-count evidence, metadata evidence, or parser-success
evidence.

## G. Selected Outcome

Selected outcome:

- Outcome A

Outcome A means:

- the real replay fixture exists
- byte length and SHA-256 hash were verified
- the fixture is admitted as private-local future `ReplayInput::Memory` fixture evidence
- fixture bytes are not copied into the repository
- committed fixture bytes are not allowed by this pass
- byte-layout evidence remains missing
- expected `ReplayHeader` evidence remains missing
- parser implementation remains closed
- parser-success logic remains closed

Why Outcome B is not selected:

- the preferred fixture path now exists
- the byte length matches the operator-provided fact
- the SHA-256 hash matches the operator-provided fact

Why Outcome C is not selected:

- private-local admission is allowed with permission, license, and privacy statuses recorded as
  pending or private-local only
- commit permission and privacy review are not sufficient for committed fixture bytes, but this
  pass does not commit or copy bytes

Why Outcome D is not selected:

- fixture admission is bounded by the existing contract, the verified path, byte length, SHA-256
  hash, and private-local storage form

## H. Admitted Fixture Record

Admitted fixture id:

- `rl_replay_header_fixture_001`

Admitted fixture class:

- real Rocket League `.replay` bytes admitted as private-local future parser input evidence
- not admitted as parser-success evidence
- not admitted as supported byte-layout evidence

Admitted local path:

- `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`

Verified byte length:

- `3001021`

Verified SHA-256:

- `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB`

Source/provenance:

- `SUPPLIED_BY_USER_LOCAL_PATH`

Permission status:

- `USER_SUPPLIED_LOCAL_USE_ALLOWED_PENDING_COMMIT_PERMISSION`

License status:

- `UNKNOWN_OR_PRIVATE_LOCAL_ONLY`

Privacy status:

- `PENDING_REVIEW`

Storage/admission form:

- `PRIVATE_LOCAL_PATH_WITH_HASH`

Expected future parser input form:

- `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes: <fixture bytes> }`

Committed fixture bytes:

- no

Copied fixture bytes:

- no

Parser execution:

- no

Expected `ReplayHeader`:

- not admitted

Byte-layout evidence:

- not admitted

## I. Permission, License, And Privacy Record

Private-local admission is recorded with the following statuses:

- source/provenance: `SUPPLIED_BY_USER_LOCAL_PATH`
- permission status: `USER_SUPPLIED_LOCAL_USE_ALLOWED_PENDING_COMMIT_PERMISSION`
- license status: `UNKNOWN_OR_PRIVATE_LOCAL_ONLY`
- privacy status: `PENDING_REVIEW`
- storage/admission form: `PRIVATE_LOCAL_PATH_WITH_HASH`

Commit/copy blocker:

- committed fixture bytes remain blocked until permission and privacy status explicitly allow
  committed fixture bytes

Private-local use limitation:

- the local path may identify the supplied bytes for evidence admission only
- the local path must not become runtime locator logic
- the path, filename, provenance label, and hash must not become parser facts

## J. Storage And Admission Form

No committed fixture storage is created.

No file is copied to:

- `tests/fixtures/replay_header/rl_replay_header_fixture_001.replay`

The admitted storage form is:

- private local path with verified byte length and SHA-256 hash

This pass records enough integrity evidence to identify the supplied private-local bytes for the
next evidence pass, but it does not make CI parser-success tests possible by itself.

## K. Byte-Layout Evidence Status

Byte-layout evidence remains missing.

This pass admits no Rocket League replay header byte layout, including:

- supported format admission rule
- supported version or version family
- header length or header termination rule
- field encodings
- numeric endianness
- string/property encoding
- body/raw-state boundary
- replay id derivation
- total frame derivation
- metadata key map
- insufficient, malformed, or unsupported-if-distinguishable error boundaries

No magic bytes, offsets, lengths, encodings, version fields, replay id source, frame count source, or
metadata source are invented.

## L. Expected `ReplayHeader` Evidence Status

Expected `ReplayHeader` evidence remains missing.

No expected `ReplayHeader.replay_id` is admitted.

No replay id derivation is admitted.

No expected `ReplayHeader.total_frames` value or `None` policy is admitted for this fixture.

No expected `ReplayHeader.metadata` map or explicit empty metadata policy is admitted for this
fixture.

`ReplayHeader.source_label` remains known only as source context copied from
`ReplayInput::Memory.label` in a future implementation. That rule does not create parser-success
evidence.

## M. Insufficient, Malformed, And Unsupported Fixture Derivation Status

Insufficient-byte fixture status:

- missing
- not derived in this pass
- not derivable honestly until byte-layout evidence identifies the required header evidence and a
  truncation point

Malformed-byte fixture status:

- missing
- not derived in this pass
- not derivable honestly until supported-layout validation rules exist

Unsupported-format/version fixture status:

- missing
- deferred unless distinguishability from malformed bytes is proven by byte-layout evidence

No synthetic opaque byte arrays are admitted as valid, insufficient, malformed, or unsupported
parser fixtures.

## N. No-Fake-Fixture Rules

This pass creates no:

- fake `.replay` files
- fake binary fixture files
- synthetic valid parser fixture bytes
- random bytes
- generated replay-like files
- placeholder expected `ReplayHeader`
- filename-derived parser facts
- path-derived parser facts
- provenance-derived parser facts
- hash-derived parser facts
- `source_replay`-derived parser facts
- `source_replay.provenance_label`-derived parser facts
- `audited_family_root_directory`-derived parser facts

Existing opaque-byte contract tests remain byte-preservation evidence only and are not valid parser
fixtures.

## O. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

This retry satisfies only the private-local fixture-byte admission part of the evidence gate. The
implementation reopen gate is still not satisfied because:

1. no byte-layout evidence is admitted
2. no byte-accounting map is admitted
3. no expected `ReplayHeader.replay_id` derivation or byte-backed identity policy is admitted
4. no valid fixture total-frame policy is admitted
5. no valid fixture metadata policy is admitted
6. no insufficient-byte fixture is admitted or derivable
7. no malformed-byte fixture is admitted or derivable
8. no unsupported-format/version fixture is admitted
9. no parser-success fixture expectation is admitted

## P. What Remains Closed

Still closed after this pass:

- parser implementation
- parser-success logic
- backend dependency addition
- `ReplayHeader` production or synthesis
- real fixture materialization
- fixture byte creation
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

## Q. What Remains Forbidden

Still forbidden unless explicitly reopened:

- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- modifying `Cargo.toml`
- modifying `Cargo.lock`
- adding backend dependencies
- implementing parser code
- implementing parser-success logic
- producing or synthesizing `ReplayHeader`
- parsing raw-state payloads
- extracting replay frames
- extracting semantic replay events
- implementing replay-source actual-materialization
- implementing replay-source carrier discovery
- implementing replay-input locator logic
- widening export semantics
- adding corpus-wide replay ingestion
- adding runtime CLI commands
- adding async/background systems
- adding database code
- adding real rollout physics
- changing execution-result cleanup boundaries
- creating generic all-family replay/raw-state/index/export/materialization frameworks
- reinterpreting `source_replay` or `source_replay.provenance_label` as replay paths
- reinterpreting `audited_family_root_directory` as replay storage
- copying or committing this fixture without explicit commit permission and privacy clearance

## R. Next Stage

Immediate next pass:

- byte-layout evidence admission pass

Reason:

- real private-local fixture bytes are now admitted
- byte-layout evidence is still missing
- expected `ReplayHeader` evidence is still missing
- parser implementation remains closed until both fixture evidence and byte-layout evidence are
  admitted

Parser implementation is not the next pass.

Parser implementation may proceed only after both fixture evidence and byte-layout evidence are
admitted by later passes.
