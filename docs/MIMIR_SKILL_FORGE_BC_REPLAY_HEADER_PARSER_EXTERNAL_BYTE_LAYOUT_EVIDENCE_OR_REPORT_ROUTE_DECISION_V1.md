# MIMIR Skill Forge BC Replay Header Parser External Byte-Layout Evidence Or Report Route Decision v1

## A. Purpose

This pass decides the next route for obtaining byte-layout evidence for the admitted private-local
Rocket League replay fixture:

- fixture id: `rl_replay_header_fixture_001`
- path: `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay`

This is a decision and evidence-report generation pass only. It does not implement MIMIR parser
code, does not implement parser-success logic, does not produce a `ReplayHeader`, and does not
admit byte-layout evidence.

The future parser target remains exactly:

- `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`

The first admitted parser input remains exactly:

- `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes: <fixture bytes> }`

## B. Family Scope

The active evidence chain remains scoped first to:

- `low_boost_recovery`

Rocket League replay header parsing remains a shared `mimir-replay` capability candidate. This
pass does not create a generic replay, raw-state, frame, event, export, materialization, carrier,
locator, database, runtime CLI, async/background, rollout, physics, or corpus framework.

`mimir_export` widening remains forbidden.

## C. Current Fixture Summary

The fixture identity was reverified in this pass before route selection:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |
| admitted future input | `ReplayInput::Memory { label: "rl_replay_header_fixture_001", bytes: <fixture bytes> }` |

The fixture path, filename, provenance, byte length, and SHA-256 remain fixture integrity facts
only. They are not parser facts.

## D. Current Byte-Layout Evidence Gap

The previous byte-layout evidence admission pass selected Outcome B and found no admitted:

- supported Rocket League replay header admission rule
- supported version or version family
- header boundary or header termination rule
- field encodings
- numeric endianness
- string/property encoding rules
- body/raw-state boundary
- replay id derivation
- total frame derivation or explicit fixture-backed `None` policy
- metadata mapping or explicit fixture-backed empty metadata policy
- insufficient-byte boundary
- malformed-byte boundary
- unsupported-if-distinguishable boundary
- expected `ReplayHeader`

Parser implementation remains closed because fixture identity alone does not prove byte layout or
expected output semantics.

## E. Existing Local Evidence Search Result

Local searches found no already-approved parser report or byte-layout artifact.

Search classes checked:

- existing `docs` replay-header parser artifacts
- existing `executor_*` replay-header parser artifacts
- `artifacts` report directory
- parser report, byte-layout, byte-accounting, generated report, and metadata dump filenames
- `boxcars`, `rattletrap`, `carball`, `rrrocket`, `rlreplay`, and `subtr-actor` local references
- workspace manifests and lockfile
- installed parser CLIs

Candidate classifications:

| Candidate | Classification | Result |
| --- | --- | --- |
| verified fixture path, byte length, and SHA-256 | fixture integrity evidence | already admitted; not byte-layout evidence |
| prior fixture admission retry artifacts | fixture admission artifacts | not byte-layout evidence |
| prior byte-layout evidence admission artifact | gap record | confirms missing evidence; not byte-layout evidence |
| backend selection docs referencing `boxcars` | backend/context evidence | not fixture-backed byte-layout evidence |
| `crates/mimir-replay` scaffold | source scaffold | not parser implementation and not byte-layout evidence |
| `Cargo.toml` / `Cargo.lock` | dependency inventory | no MIMIR replay parser dependency present |
| `artifacts` directory | report search | directory was missing before this pass |
| installed `carball.exe` | available external CLI | rejected as too broad for report generation through its normal CLI path |
| local/generated parser reports | approved evidence | none found before this pass |

Outcome A is therefore not available.

## F. One-Off Report Generation Route Analysis

### Route 1: Existing Approved Local Evidence

Rejected for Outcome A.

Reason:

- no approved local byte-layout evidence artifact exists
- no approved parser/tool report exists before this pass
- no expected `ReplayHeader` evidence exists

### Route 2: Installed `carball.exe` CLI

Rejected as the selected route.

Reason:

- `carball.exe` is installed at `C:\Program Files\Python38\Scripts\carball.exe`
- `pip show carball` reports version `0.7.5`
- the normal CLI performs replay analysis and can emit JSON/proto/gzip outputs
- the CLI path is broader than this pass because it is designed to analyze replay frames and derived
  gameplay data
- using that path would risk crossing the raw-state/frame/event boundary for a header evidence
  route

### Route 3: Temporary External Rust Crate Using `boxcars`

Selected for Outcome B.

Reason:

- the route is outside the MIMIR Cargo workspace
- it does not modify MIMIR `Cargo.toml` or `Cargo.lock`
- it does not add a MIMIR backend dependency
- it uses Rust for the one-off parser report tool
- `boxcars 0.11.1` is an external Rocket League replay parser crate
- the report generator invokes:
  - `ParserBuilder::new(bytes).never_parse_network_data().parse()`
- network frames are explicitly skipped
- no raw-state payload is decoded
- no replay frames are extracted
- no semantic replay events are extracted
- body/footer structural counts read by `boxcars` are quarantined in the report as limitations and
  are not admitted as MIMIR header evidence

Boundary caveat:

- `boxcars::ParserBuilder::parse()` returns a broad `boxcars::Replay`, not a MIMIR header-only
  object
- this route is acceptable only as an external evidence-report generator
- it remains unacceptable as MIMIR parser implementation in this pass

## G. Selected Outcome

Selected outcome:

- Outcome B

Outcome B means:

- generate a bounded external parser/tool report from the admitted fixture
- treat the report as evidence only
- do not integrate the tool into MIMIR
- do not claim MIMIR parser success
- do not admit byte-layout evidence in this pass
- next pass should be an approved parser-report admission pass

Why Outcome A is not selected:

- no approved existing local report/evidence artifact was present before this pass

Why Outcome C is not selected:

- a bounded one-off external Rust report route was available and was successfully run outside the
  MIMIR dependency graph

Why Outcome D is not selected:

- the route is bounded by the admitted fixture, a temporary external crate path, explicit network
  skip mode, a single report output path, and non-integration constraints

## H. Exact Report-Generation Route

Temporary external tool path:

- `D:\Temp\mimir_boxcars_report_rl_fixture_001_v1`

Report output path:

- `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`

Allowed command used:

```powershell
cargo run --manifest-path 'D:\Temp\mimir_boxcars_report_rl_fixture_001_v1\Cargo.toml' -- 'D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay' 'D:\RocketLeague bot\MIMIR\artifacts\replay_header_reports\rl_replay_header_fixture_001_report.txt'
```

Report generator behavior:

- reads the admitted `.replay` file as bytes
- verifies expected byte length and SHA-256 before parsing
- invokes `boxcars 0.11.1`
- requests `never_parse_network_data()`
- emits a text report
- marks all parser output as external tool report evidence only

Report contents include:

- tool name/version/source
- fixture id/path/length/hash
- external parser recognition result
- header-size and header-property summary
- selected header properties when available:
  - `Id`
  - `ReplayName`
  - `Date`
  - `MapName`
  - `ReplayVersion`
  - `BuildVersion`
  - `NumFrames`
  - `MaxChannels`
  - `MatchType`
  - `TeamSize`
  - `RecordFPS`
- body/footer structural counts read by the external tool, marked as not MIMIR header evidence
- explicit network/frame/raw-state/event limits
- explicit insufficiency statement for MIMIR admission and implementation

## I. Non-Integration Constraints

The generated report is not:

- MIMIR parser output
- parser-success evidence
- byte-layout admission
- expected `ReplayHeader` admission
- a backend selection for MIMIR
- a dependency addition to MIMIR
- a runtime CLI command
- a replay-source locator
- a replay-source materialization path
- corpus ingestion

The temporary external tool must not be copied into the MIMIR source tree as parser code.

## J. What Remains Closed

Still closed after this pass:

- parser implementation
- parser-success logic
- `ReplayHeader` production or synthesis
- raw-state payload parsing
- replay frame extraction
- semantic replay event extraction
- replay-source actual materialization
- replay-source carrier discovery
- replay-input locator logic
- replay-source actual-materialization implementation
- replay-source carrier discovery implementation
- replay-input locator implementation
- corpus-wide replay ingestion
- runtime CLI commands
- async/background systems
- database code
- real rollout physics
- `mimir_export` widening

## K. What Remains Forbidden

Still forbidden unless explicitly reopened:

- modifying `mimir-io`
- modifying `mimir-export`
- modifying `mimir-types`
- modifying `Cargo.toml`
- modifying `Cargo.lock`
- adding backend dependencies to MIMIR
- implementing parser code
- implementing parser-success logic
- producing or synthesizing `ReplayHeader`
- parsing raw-state payloads
- extracting replay frames
- extracting semantic replay events
- implementing replay-source actual materialization
- implementing replay-source carrier discovery
- implementing replay-input locator logic
- widening export semantics
- adding corpus-wide replay ingestion
- adding runtime CLI commands
- adding async/background systems
- adding database code
- adding real rollout physics
- treating fixture path, filename, provenance, byte length, or SHA-256 as parser facts

## L. Next Stage

Immediate next pass:

- approved parser-report admission pass for
  `artifacts/replay_header_reports/rl_replay_header_fixture_001_report.txt`

The next pass must decide whether the generated external report is admissible as byte-layout and
expected-output evidence, partial evidence, or insufficient evidence.

Parser implementation is not the next pass.

Parser implementation is allowed only after fixture evidence, byte-layout evidence, and expected
`ReplayHeader` output evidence are admitted by later passes.
