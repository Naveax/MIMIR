# MIMIR Replay Header Three-Fixture Lane Closure V1

Pass: HDR-C1
Date: 2026-08-12

## Purpose

Close the first bounded real replay-header parser lane after formal admission of fixture_001, fixture_002, and fixture_003 exact tuples.

This is a closure/capability-state pass. It does not add parser behavior.

## Closure Decision

**Outcome A — CLOSE THE THREE-FIXTURE EXACT HEADER LANE AS A BOUNDED V1 CAPABILITY.**

The current header lane is stable enough to move one architectural layer upward. Further fixture-specific header widening should be evidence-driven by corpus coverage rather than accumulated speculatively.

The next parser-adjacent layer is replay source materialization policy, not body parsing and not broad version wildcarding.

## Admitted Exact Tuples

### Fixture001Exact

```text
major_version = 868
minor_version = 32
net_version = 10
game_type = TAGame.Replay_Soccar_TA
ReplayVersion = 8
BuildVersion = 241206.55345.468477
```

### Fixture002Exact

```text
major_version = 868
minor_version = 32
net_version = 10
game_type = TAGame.Replay_Soccar_TA
ReplayVersion = 8
BuildVersion = 250811.43331.492665
```

### Fixture003Exact

```text
major_version = 868
minor_version = 32
net_version = 10
game_type = TAGame.Replay_Soccar_TA
ReplayVersion = 8
BuildVersion = 251020.62592.500294
```

The BuildVersion policy is an exact allowlist. Shared major/minor/net/game/ReplayVersion values do not independently authorize unknown BuildVersion values.

## Current Parser Capability Matrix

| Capability | State | Notes |
|---|---|---|
| `ReplayInput::Memory` header parsing | ADMITTED_BOUNDED | Current real parser entry |
| `ReplayInput::File` direct parser input | CLOSED | Must be reopened through source-materialization policy |
| Fixture001Exact | ADMITTED | Real checked-in fixture regression |
| Fixture002Exact | ADMITTED | Real checked-in fixture regression |
| Fixture003Exact | ADMITTED | F003-A1 Outcome A |
| Unknown BuildVersion wildcard/family support | CLOSED | Exact allowlist only |
| Broad ReplayVersion=8 support | CLOSED | ReplayVersion alone is not sufficient |
| `Id` -> `ReplayId` | ADMITTED_BOUNDED | Exact selected mapping with 32 ASCII hex validation |
| `NumFrames` -> `total_frames` | ADMITTED_BOUNDED | Non-negative IntProperty |
| ReplayName | ADMITTED_BOUNDED | selected StrProperty -> Text |
| Date | ADMITTED_BOUNDED | selected StrProperty -> Text |
| MapName | ADMITTED_BOUNDED | selected NameProperty -> Text |
| ReplayVersion metadata | ADMITTED_BOUNDED | selected IntProperty |
| BuildVersion metadata | ADMITTED_BOUNDED | selected StrProperty and exact tuple predicate |
| MaxChannels | ADMITTED_BOUNDED | selected IntProperty |
| MatchType | ADMITTED_BOUNDED | selected NameProperty -> Text |
| TeamSize | ADMITTED_BOUNDED | selected IntProperty |
| RecordFPS | ADMITTED_BOUNDED | finite selected FloatProperty |
| non-selected ArrayProperty skip | ADMITTED_BOUNDED | bounded declared-value skip |
| non-selected FloatProperty skip | ADMITTED_BOUNDED | bounded declared-value skip |
| non-selected IntProperty skip | ADMITTED_BOUNDED | bounded declared-value skip |
| non-selected NameProperty skip | ADMITTED_BOUNDED | bounded declared-value skip |
| non-selected QWordProperty skip | ADMITTED_BOUNDED | bounded declared-value skip |
| non-selected StrProperty skip | ADMITTED_BOUNDED | bounded declared-value skip |
| non-selected BoolProperty skip | ADMITTED_BOUNDED | size=0 + one separate byte, values 0/1 only |
| selected BoolProperty mapping | CLOSED | unsupported-property |
| BoolProperty -> FieldValue::Boolean | CLOSED | not admitted for replay header |
| `bForfeit` metadata mapping | CLOSED | structural skip only |
| negative-length UTF-16 replay text | CLOSED | explicit unsupported-text boundary |
| header CRC validation | CLOSED | CRC currently read as layout only |
| content CRC | CLOSED | unopened |
| body parsing | CLOSED | unopened |
| network/frame decoding | CLOSED | unopened |
| raw-state extraction | CLOSED | unopened |
| event extraction | CLOSED | unopened |
| external replay-parser backend | CLOSED | no dependency added |
| CLI/runtime/export parser widening | CLOSED | unchanged |

## Real GitHub Verification

The admitted lane was validated on GitHub-hosted Windows runners rather than relying on one developer-machine checkout.

F003 implementation acceptance:

- branch: `agent/f003-fixture003-bool-skip`
- code head: `890642aef864910d63bc61d73b846bdd57d6650b`
- GitHub Actions CI run: `#18`
- run id: `31588274140`
- conclusion: success

Key results:

```text
mimir-replay: 28 passed / 0 failed
mimir-skill: 273 passed / 0 failed
full workspace tests: passed
cargo fmt --check: passed
cargo check workspace/all-targets/all-features: passed
cargo clippy workspace/all-targets/all-features -D warnings: passed
mimir-export --list: 173 tests listed
largest-100 replay corpus manifest size/SHA-256 verification: passed
```

The `mimir-replay` fixture paths are repository-relative, so the GitHub runner visibly executed the checked-in fixture_001, fixture_002, and fixture_003 tests.

## Closure Invariants

After this closure:

1. Three exact replay-header tuples are admitted, no more.
2. Unknown BuildVersion values remain rejected until new evidence/policy/admission exists.
3. Header parsing remains memory-backed.
4. File IO is not parser semantics.
5. `bForfeit` remains structural evidence only, not selected metadata.
6. BoolProperty remains non-selected skip-only.
7. CRC correctness is not claimed.
8. No body/frame/raw-state/event correctness is claimed.
9. No RocketSim or external parser backend is implied by this lane.
10. Every future widening must use a separate evidence/policy/planning/implementation/audit path.

## Existing Test-Portability Debt Carried Forward

One `mimir-skill` cross-crate fixture seam still uses the historical absolute developer-machine path for `sample_001.replay` and therefore skips on GitHub-hosted runners.

This debt is separate from the admitted `mimir-replay` header lane because the authoritative parser fixture tests are repository-relative and executed successfully. The debt should nevertheless be corrected before relying on that cross-crate seam as CI evidence in later Skill Forge integration work.

## Header Lane Closure Answer

Question:

> Is the header parser lane sufficiently stable to stop speculative fixture accumulation and move upward?

Answer:

**Yes, within the explicitly bounded three-exact-tuple V1 surface.**

This does not mean the parser covers the corpus generally. It means the first exact header lane has enough audited real-fixture behavior to support the next architectural boundary.

## Next Architectural Pass

Proceed to:

**SRC-P1 — replay source materialization policy.**

Preferred design question:

```text
filesystem/materializer
→ bounded bytes + provenance
→ ReplayInput::Memory
→ MinimalReplayHeaderReader
```

The next pass should decide this boundary before implementation.

Do not jump directly to:

- ReplayInput::File parser widening
- body parsing
- frame decoding
- raw-state extraction
- 100-replay compatibility scanning

The 100-replay compatibility scanner belongs after an admitted source materialization path exists.