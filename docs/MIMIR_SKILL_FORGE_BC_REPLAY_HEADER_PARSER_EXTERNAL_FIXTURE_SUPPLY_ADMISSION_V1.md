# MIMIR Skill Forge BC Replay Header Parser External Fixture Supply Admission v1

## A. Purpose

This pass performs the external fixture supply/admission check for the future minimal real Rocket
League replay header parser.

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

## C. Current Contract Summary

The current trusted boundary is:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_MATERIALIZATION_ADMISSION_CONTRACT_V1.md`

That contract selected:

- Outcome B
- no real `.replay` fixture bytes present
- no approved Rocket League replay header byte-layout evidence present
- external fixture supply/admission required before parser implementation can be reopened
- parser implementation closed
- parser-success logic closed

The selected future parser boundary remains:

- valid supported `ReplayInput::Memory` bytes may return a real `ReplayHeader` only after required
  fixture and byte-layout evidence are admitted
- invalid, malformed, insufficient, unsupported, non-memory, or deferred inputs must return
  structured errors only
- `UnsupportedReplayReader` remains truthful scaffold behavior and distinguishable from any future
  real reader
- `mimir_export` widening remains forbidden unless explicitly reopened

## D. Re-Audit Summary

Files re-audited before this admission artifact:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_MATERIALIZATION_ADMISSION_CONTRACT_V1.md`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_materialization_admission_contract_decision.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_materialization_admission_contract_next.txt`
- `executor_mimir_skill_forge_bc_replay_header_parser_fixture_materialization_admission_contract_status.txt`
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
| `MIMIR_REPLAY_FIXTURE_PATH` | unset |
| `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` | missing |
| `D:\RocketLeague bot\MIMIR\external_fixtures\*.replay` | directory missing; no files found |
| `D:\RocketLeague bot\MIMIR\fixtures_external\*.replay` | directory missing; no files found |
| `D:\RocketLeague bot\MIMIR\private_fixtures\*.replay` | directory missing; no files found |
| repo-wide `rg --files -g '*.replay'` under `D:\RocketLeague bot\MIMIR` | no files found |
| repo-wide recursive `Get-ChildItem -Recurse -Filter '*.replay'` under `D:\RocketLeague bot\MIMIR` | no files found |

No fixture was found at the preferred default candidate path:

- `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`

No path was supplied through:

- `MIMIR_REPLAY_FIXTURE_PATH`

No real `.replay` bytes were found under any allowed external fixture directory.

No `.replay` file was found elsewhere under the MIMIR repository root.

## F. Selected Outcome

Selected outcome:

- Outcome B

Outcome B means:

- no real fixture bytes were supplied or found
- no fixture evidence is admitted
- no fixture files are added
- external fixture supply remains required
- parser implementation remains closed
- parser-success logic remains closed

Why Outcome A is not selected:

- no real Rocket League `.replay` file or equivalent real replay byte payload was found
- no byte length or SHA-256 hash can be recorded for an admitted fixture
- no provenance, permission, license, or privacy record can be attached to actual bytes

Why Outcome C is not selected:

- no candidate real fixture file exists, so admission is not blocked by missing legal/privacy
  information for a found file

Why Outcome D is not selected:

- fixture admission remains bounded by the existing contract and by the allowed search locations

## G. Admitted Fixture Record

No fixture is admitted in this pass.

No fixture id is assigned.

No future parser input is admitted.

No value of the form below is admitted:

- `ReplayInput::Memory { label: <fixture_id>, bytes: <fixture bytes> }`

No fixture bytes are copied into the repository.

No private-local fixture path is admitted.

## H. Missing Fixture Record

Missing required valid fixture evidence:

- one real Rocket League `.replay` or equivalent real replay byte payload
- fixture id
- byte length
- SHA-256 hash
- source/provenance
- permission status
- license status
- privacy status
- storage/admission form
- expected `ReplayInput::Memory` fixture label and byte source

External fixture supply remains required before parser implementation can be reconsidered.

## I. Byte Length And Hash Record

No byte length is recorded because no fixture bytes were admitted.

No SHA-256 hash is recorded because no fixture bytes were admitted.

No cryptographic hash is parser evidence by itself. A future hash may prove fixture integrity only;
it must not be treated as replay identity, replay id derivation, header layout, frame count, or
metadata evidence.

## J. Permission, License, And Privacy Record

No permission, license, or privacy record is admitted because no fixture bytes were supplied or
found.

The default future private-local admission statuses remain:

- permission status: `USER_SUPPLIED_LOCAL_USE_ALLOWED_PENDING_COMMIT_PERMISSION`, unless a stronger
  permission statement is supplied
- license status: `UNKNOWN_OR_PRIVATE_LOCAL_ONLY`, unless a stronger license statement is supplied
- privacy status: `PENDING_REVIEW`, unless a stronger review is supplied

Those statuses are not attached to any fixture in this pass.

## K. Storage And Admission Form

No committed fixture storage is created.

No private-local fixture admission is created.

No file is copied to:

- `tests/fixtures/replay_header/<fixture_id>.replay`

If a later pass finds real bytes, the default policy remains private-local admission first. Committed
fixture bytes require explicit permission and privacy clearance before copy.

## L. Byte-Layout Evidence Status

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

## M. Expected `ReplayHeader` Evidence Status

Expected `ReplayHeader` evidence remains missing.

No expected `ReplayHeader.replay_id` is admitted.

No replay id derivation is admitted.

No expected `ReplayHeader.total_frames` value or `None` policy is admitted for a valid fixture.

No expected `ReplayHeader.metadata` map or explicit empty metadata policy is admitted for a valid
fixture.

`ReplayHeader.source_label` remains known only as source context copied from
`ReplayInput::Memory.label` in a future implementation. That rule does not create parser success
evidence.

## N. Insufficient, Malformed, And Unsupported Fixture Status

Insufficient-byte fixture status:

- missing
- not derivable because no admitted valid fixture exists

Malformed-byte fixture status:

- missing
- not derivable because no admitted valid fixture or proven supported-layout bytes exist

Unsupported-format/version fixture status:

- missing
- deferred unless distinguishability from malformed bytes is proven by byte-layout evidence

No synthetic opaque byte arrays are admitted as valid, insufficient, malformed, or unsupported
parser fixtures.

## O. No-Fake-Fixture Rules

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

## P. Parser Implementation Reopen Status

Parser implementation remains closed.

Parser-success logic remains closed.

The implementation reopen gate is not satisfied because:

1. no valid supported real Rocket League replay fixture is admitted
2. no valid fixture provenance is documented
3. no fixture byte length or hash is documented
4. no fixture permission/license/privacy status is documented
5. no fixture storage/admission form is documented
6. no byte-layout evidence is admitted
7. no byte-accounting map is admitted
8. no expected `ReplayHeader.replay_id` derivation or byte-backed identity policy is admitted
9. no valid fixture total-frame policy is admitted
10. no valid fixture metadata policy is admitted
11. no insufficient-byte fixture is admitted or derivable
12. no malformed-byte fixture is admitted or derivable
13. no unsupported-format/version fixture is admitted

## Q. What Remains Closed

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

## R. What Remains Forbidden

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

## S. Next Stage

Immediate next pass:

- fixture supply retry pass

That pass must supply or find a real Rocket League `.replay` or equivalent real replay byte payload
under an explicitly allowed fixture location, then record byte length, SHA-256 hash, provenance,
permission, license, privacy, and storage/admission form.

Parser implementation is not the next pass.

Parser implementation may proceed only after both fixture evidence and byte-layout evidence are
admitted by later passes.
