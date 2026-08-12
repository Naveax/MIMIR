# MIMIR Skill Forge BC Replay Header Parser Fixture 003 Exact Tuple BoolProperty Skip Implementation Audit V1

Pass: F003-A1
Date: 2026-08-12

## Audit Purpose

Audit the already-implemented bounded fixture_003 exact replay-header tuple plus non-selected BoolProperty skip-only behavior. This pass performs admission only. It does not widen parser behavior.

## Audited Evidence

Repository branch:

- `agent/f003-fixture003-bool-skip`

Base main before this lane:

- `06e29e3119a165299612a9c78e8b90d81a1e5593`

Accepted implementation code head:

- `890642aef864910d63bc61d73b846bdd57d6650b`

Implementation evidence artifact:

- `docs/MIMIR_SKILL_FORGE_BC_REPLAY_HEADER_PARSER_FIXTURE_003_EXACT_TUPLE_BOOLPROPERTY_SKIP_IMPLEMENTATION_V1.md`

GitHub Actions code acceptance evidence:

- CI run `#18`
- run id `31588274140`
- job id `94087062936`
- conclusion `success`

GitHub Actions evidence/status HEAD verification:

- CI run `#22`
- run id `31588780524`
- conclusion `success`

Repository diff audit from the original base showed exactly:

- one implementation Rust file: `crates/mimir-replay/src/lib.rs`
- the four F003-I1E implementation evidence/status/decision/next artifacts
- no Cargo manifest or dependency changes
- no other crate source changes

## Audit Checklist

### Exact fixture_003 tuple

PASS.

The implementation contains exactly:

```text
major_version = 868
minor_version = 32
net_version = 10
game_type = TAGame.Replay_Soccar_TA
ReplayVersion = 8
BuildVersion = 251020.62592.500294
```

`SupportedReplayHeaderTupleV1` contains:

- `Fixture001Exact`
- `Fixture002Exact`
- `Fixture003Exact`

The BuildVersion match remains an exact allowlist.

### Unknown BuildVersion remains rejected

PASS.

A near-neighbor synthetic BuildVersion:

```text
251020.62592.500295
```

is explicitly tested and rejected with the existing `unsupported-version` boundary.

No wildcard, range, prefix, regex, date-family, or generic ReplayVersion=8 acceptance was introduced.

### BoolProperty is skip-only and non-selected only

PASS.

`KIND_BOOL` is handled only inside `skip_non_selected_property(...)` through the private `skip_non_selected_bool_property(...)` helper.

`KIND_BOOL` is not added to `is_admitted_property_kind(...)` and is not handled by `parse_selected_property(...)`.

Therefore selected BoolProperty remains outside the admitted selected-property mapping surface.

### BoolProperty structural rules

PASS.

The bounded helper requires:

- declared size exactly `0`
- exactly one separate value byte
- value byte only `0` or `1`

Negative tests prove:

- nonzero declared size -> malformed
- missing separate bool byte -> insufficient
- value byte `2` -> malformed

### bForfeit remains non-semantic metadata

PASS.

`bForfeit` is not present in `is_selected_property(...)`.

There is no `BoolProperty -> FieldValue::Boolean` mapping.

Both real fixture_003 tests assert `ReplayHeader.metadata.get("bForfeit").is_none()`.

### Selected BoolProperty remains unsupported

PASS.

The synthetic selected BoolProperty test passes only when the parser rejects it through `unsupported-property`.

### fixture_001 regression

PASS.

GitHub Actions run #18 executed the repo-relative checked-in fixture_001 test and reported:

```text
test tests::minimal_reader_parses_rl_replay_header_fixture_001_and_header_only_slice ... ok
```

The test also locks `header_size = 13200` and `header_end = 13208`.

### fixture_002 regression

PASS.

GitHub Actions run #18 reported both:

```text
test tests::minimal_reader_parses_rl_replay_header_fixture_002_exact_happy_path ... ok
test tests::minimal_reader_parses_rl_replay_header_fixture_002_header_only_slice ... ok
```

### fixture_003 real full replay

PASS.

GitHub Actions run #18 reported:

```text
test tests::minimal_reader_parses_rl_replay_header_fixture_003_exact_happy_path ... ok
```

The test locks the expected replay id, total frames, selected metadata, BuildVersion, TeamSize=2, RecordFPS=30.0, and `bForfeit` absence.

### fixture_003 header-only

PASS.

GitHub Actions run #18 reported:

```text
test tests::minimal_reader_parses_rl_replay_header_fixture_003_header_only_slice ... ok
```

The test locks:

```text
header_size = 11190
header_end = 11198
```

and requires equality between the full-replay header result and the exact header-only slice result.

### ReplayInput::File remains closed

PASS.

`MinimalReplayHeaderReader::read_header(...)` still returns `unsupported-input` for `ReplayInput::File`.

The corresponding rejection test remains green.

### Header CRC validation remains closed

PASS.

The parser still reads `_header_crc` only as layout. It does not validate it.

`minimal_reader_does_not_validate_header_crc` remains green.

### content_crc / body / network / frame / raw-state / event boundaries remain closed

PASS.

No implementation for those surfaces was introduced in the F003 lane.

### External parser backend remains closed

PASS.

No Cargo manifest or dependency change was made. No replay parser backend dependency was introduced.

### CLI/runtime/export widening remains closed

PASS.

No source outside `crates/mimir-replay/src/lib.rs` changed in the implementation lane.

### Full GitHub validation

PASS.

GitHub Actions run #18 completed:

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

The largest-100 corpus verification reported all 100 checked-in replay fixtures matching manifest size and SHA-256.

## Separate Existing Test-Portability Debt

The audit confirms one pre-existing issue outside F003-I1 implementation scope:

`mimir-skill` contains a fixture-specific cross-crate seam test that still references:

```text
D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay
```

On GitHub-hosted runners that one seam test prints a skip message.

This does not weaken the F003 parser admission because:

1. the authoritative `mimir-replay` fixture tests now use repository-relative checked-in files;
2. fixture_001, fixture_002, and fixture_003 parser tests visibly executed and passed on GitHub Actions;
3. the skipped `mimir-skill` seam result is not counted as F003 evidence.

The portability debt must be corrected in a separate test-harness pass rather than widening this audit.

## Admission Decision

**Outcome A — ADMITTED.**

The following bounded parser capabilities are now admitted:

1. exact fixture_003 supported replay-header tuple:
   - major 868
   - minor 32
   - net 10
   - `TAGame.Replay_Soccar_TA`
   - ReplayVersion 8
   - BuildVersion `251020.62592.500294`
2. exact non-selected top-level BoolProperty skip-only semantics:
   - declared size 0
   - one separate bool byte
   - values 0/1 only
   - no metadata output
3. fixture_003 full checked-in replay header parse at the existing minimal Memory-input boundary
4. fixture_003 exact header-only parse at `header_end = 11198`

No broader replay parser capability is admitted.

## Boundaries Explicitly Still Closed

- wildcard/family BuildVersion
- broad ReplayVersion=8 support
- path/hash/filename parser predicates
- ReplayInput::File parser behavior
- source materialization
- BoolProperty selected mapping
- BoolProperty -> FieldValue::Boolean header mapping
- bForfeit metadata mapping
- CRC validation
- content_crc
- replay body parsing
- network/frame decoding
- raw-state extraction
- event extraction
- backend parser dependency
- CLI/runtime/export widening

## Next Pass

Proceed to:

**HDR-C1 — three-fixture header lane closure.**

That closure should consolidate the exact fixture_001/002/003 lane, publish a current parser capability matrix, carry forward the mimir-skill fixture-path portability debt, and decide whether the header lane is stable enough to move upward to replay source materialization.