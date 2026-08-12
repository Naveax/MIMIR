# MIMIR Skill Forge BC Replay Header Parser Fixture 003 Exact Tuple BoolProperty Skip Implementation V1

Pass date: 2026-08-12

## Purpose

Record the implementation evidence for the bounded fixture_003 replay-header parser pass planned by `MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_EXACT_TUPLE_BOOLPROPERTY_SKIP_IMPLEMENTATION_PLANNING_V1.md`.

This artifact records what was actually implemented and verified on GitHub. It does not perform the separate implementation audit/admission pass.

## Result

Implementation result: **PASS**.

Implementation branch:

- `agent/f003-fixture003-bool-skip`

Implementation lineage:

- base `main`: `06e29e3119a165299612a9c78e8b90d81a1e5593`
- implementation commit: `9ff74328229212c9ec50294b6ccabaed98445d2a`
- rustfmt correction: `6d18d76ec210249dd1925ba1d9d38cf616b13d55`
- narrow Clippy policy-name preservation correction: `890642aef864910d63bc61d73b846bdd57d6650b`

GitHub Actions acceptance run:

- workflow: `CI`
- run number: `18`
- run id: `31588274140`
- job id: `94087062936`
- checked-out commit: `890642aef864910d63bc61d73b846bdd57d6650b`
- conclusion: `success`

## Implementation Scope

The implementation changed only:

- `crates/mimir-replay/src/lib.rs`

No Cargo dependency, manifest, CLI, runtime, export, simulation, body parser, raw-state parser, frame parser, or event parser change was made.

The implementation added:

- `SUPPORTED_BUILD_VERSION_FIXTURE_003 = "251020.62592.500294"`
- `SupportedReplayHeaderTupleV1::Fixture003Exact`
- one exact fixture_003 BuildVersion arm in `supported_replay_header_tuple_v1(...)`
- `KIND_BOOL = "BoolProperty"`
- private non-selected BoolProperty skip-only handling
- fixture_003 full-file and header-only regression tests
- exact BoolProperty positive and negative boundary tests
- adjacent unknown BuildVersion rejection coverage

The private enum retains the policy-planned names `Fixture001Exact`, `Fixture002Exact`, and `Fixture003Exact`. A narrow `#[allow(clippy::enum_variant_names)]` is attached to that private enum only so `cargo clippy ... -D warnings` can remain enabled without renaming policy vocabulary.

## Exact Supported Tuple Added

The implementation admits only the third exact tuple:

```text
major_version = 868
minor_version = 32
net_version = 10
game_type = TAGame.Replay_Soccar_TA
ReplayVersion = 8
BuildVersion = 251020.62592.500294
```

The previous fixture_001 and fixture_002 exact tuples remain unchanged.

No wildcard, prefix, range, regex, date-family, broad `ReplayVersion = 8`, or broad `868/32/net10` admission was added.

The near-neighbor unknown BuildVersion `251020.62592.500295` is explicitly tested and remains `unsupported-version`.

## BoolProperty Boundary Implemented

For a top-level **non-selected** `BoolProperty` only:

1. declared `property_size` must be exactly `0`
2. the existing ignored four-byte field remains consumed by the caller
3. exactly one separate bool value byte is consumed
4. value byte `0` is accepted and skipped
5. value byte `1` is accepted and skipped
6. any other value byte is malformed
7. missing bool byte is insufficient/truncated
8. no `FieldValue` is created
9. no metadata entry is created

`KIND_BOOL` was deliberately **not** added to `is_admitted_property_kind(...)`. Therefore selected metadata keys presented as BoolProperty continue to fail through the existing unsupported-property boundary.

## bForfeit Boundary

Fixture_003 contains a non-selected `bForfeit` BoolProperty according to the prior structural evidence.

The implementation does not add `bForfeit` to `is_selected_property(...)` and does not add any `BoolProperty -> FieldValue::Boolean` mapping.

Both fixture_003 real-file tests assert:

```text
ReplayHeader.metadata.get("bForfeit") == None
```

Therefore the implementation consumes the admitted structural BoolProperty without promoting `bForfeit` into MIMIR metadata semantics.

## GitHub-Portable Real Fixture Tests

During implementation, a CI portability defect was identified in `mimir-replay` tests: fixture paths were hard-coded to one developer machine and could silently skip on GitHub-hosted runners.

Within the allowed `crates/mimir-replay/src/lib.rs` scope, fixture_001/002/003 test paths were changed to repository-relative paths derived from `CARGO_MANIFEST_DIR`.

This means the accepted GitHub Actions run actually opened the checked-in `external_fixtures/sample_001.replay`, `sample_002.replay`, and `sample_003.replay` files instead of relying on the developer-machine path.

## Real Replay Header Evidence

GitHub Actions run #18 executed `cargo test -p mimir-replay -- --nocapture` and reported:

```text
running 28 tests
...
test tests::minimal_reader_parses_rl_replay_header_fixture_001_and_header_only_slice ... ok
test tests::minimal_reader_parses_rl_replay_header_fixture_002_exact_happy_path ... ok
test tests::minimal_reader_parses_rl_replay_header_fixture_002_header_only_slice ... ok
test tests::minimal_reader_parses_rl_replay_header_fixture_003_exact_happy_path ... ok
test tests::minimal_reader_parses_rl_replay_header_fixture_003_header_only_slice ... ok
...
test result: ok. 28 passed; 0 failed
```

Fixture_003 assertions lock:

```text
replay_id = DF72482811F0B757082C458D84251EFF
source_label = rl_replay_header_fixture_003
total_frames = Some(8288)
ReplayName = asdasd
Date = 2025-11-01 19-20-48
MapName = cs_day_p
ReplayVersion = 8
BuildVersion = 251020.62592.500294
MaxChannels = 2047
MatchType = Online
TeamSize = 2
RecordFPS = 30.0
bForfeit absent
```

The fixture_003 header-only test locks:

```text
header_size = 11190
header_end = 11198
```

and requires the header-only slice to produce the same `ReplayHeader` as the full checked-in replay bytes.

## BoolProperty Negative and Positive Test Evidence

The same GitHub run passed all of the following:

- non-selected BoolProperty value `0` is skipped without metadata
- non-selected BoolProperty value `1` is skipped without metadata
- selected BoolProperty remains rejected
- non-selected BoolProperty with nonzero declared size is rejected as malformed
- truncated non-selected BoolProperty value is rejected as insufficient
- non-selected BoolProperty value `2` is rejected as malformed
- unknown property kind remains unsupported
- near-neighbor unknown BuildVersion remains unsupported

## Full GitHub Validation Evidence

GitHub Actions run #18 completed the repository verifier successfully:

```text
cargo fmt --all -- --check                              PASS
cargo check --workspace --all-targets --all-features   PASS
cargo test -p mimir-replay -- --nocapture              28 PASS / 0 FAIL
cargo test -p mimir-skill -- --nocapture               273 PASS / 0 FAIL
cargo test --workspace --all-targets --all-features    PASS
cargo clippy --workspace --all-targets --all-features -- -D warnings   PASS
cargo test -p mimir-export -- --list                    173 tests listed
scripts/verify_test_corpus.ps1                          PASS
```

The final repository verifier message was:

```text
PASS: MIMIR repository verification completed with real command arguments.
```

The checked-in largest-100 replay corpus also passed manifest size and SHA-256 verification.

## Discovered Existing Test-Portability Debt

The accepted run exposed a separate pre-existing issue in `crates/mimir-skill/src/lib.rs`:

```text
fixture missing or unreadable at D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay;
skipping rl_replay_header_fixture_001 fixture-specific mimir-skill seam test
```

This does **not** invalidate F003-I1 because the `mimir-replay` fixture_001/002/003 tests themselves now use repository-relative paths and executed successfully on GitHub. The `mimir-skill` seam portability issue is outside the implementation file scope of F003-I1 and is recorded explicitly for later correction/admission rather than being silently widened into this pass.

## Boundaries Still Closed

The implementation does not admit:

- `ReplayInput::File` parser support
- replay-source filesystem materialization
- `BoolProperty -> FieldValue::Boolean`
- selected BoolProperty mapping
- `bForfeit` metadata mapping
- wildcard or family BuildVersion support
- broad `ReplayVersion = 8` support
- header CRC validation
- content CRC read/validation
- replay body parsing
- network/frame decoding
- raw-state extraction
- event extraction
- external replay-parser backend dependency
- CLI integration
- runtime integration
- export widening

The existing `minimal_reader_does_not_validate_header_crc` test remains green, explicitly preserving the CRC non-validation boundary.

## Implementation Outcome

**PASS.**

The implementation evidence is sufficient to proceed to a separate F003-A1 implementation audit/admission pass. This artifact itself does not admit the capability; admission remains a distinct pass.