# MIMIR Skill Forge BC Replay Header Parser Fixture 002 Intake Readiness v1

Pass date: 2026-05-04

## Purpose

Plan and admit, if safe, the next replay header fixture target after
`rl_replay_header_fixture_001`.

This is a fixture and evidence readiness planning pass only. It does not broaden parser scope,
modify parser code, modify the `mimir-skill` seam, add export/runtime/CLI integration, add file
input support, add CRC validation, read `content_crc`, parse body/raw-state/frame/event data, or
add a backend replay parser dependency.

## Selected Outcome

Selected outcome:

- Outcome A

`rl_replay_header_fixture_002` is available and identity is verified.

`sample_002.replay` was copied from caller-supplied `MIMIR_REPLAY_FIXTURE_002_PATH` because the
destination did not already exist. It is admitted only as `PRIVATE_LOCAL_PATH_WITH_HASH`.

No parser-success is claimed for fixture_002. The next pass may generate or admit a structural or
header report for fixture_002 without treating this intake as parser support.

## Current Admitted Parser and Seam Boundary

The previously admitted `mimir-skill` seam remains:

- opt-in and parallel to `UnsupportedReplayReader`
- success through the admitted seam means `minimal header parse success only`
- failure through the admitted seam means `minimal header parse failure only`
- `ReplayHeader` remains header-only parser-attempt evidence
- parser-success remains admitted only for `ReplayInput::Memory`, the exact fixture-supported
  tuple, and header-only parsing ending at `8 + header_size`
- parser-success is not admitted broadly

No export/runtime/CLI integration, broad parser expansion, `ReplayInput::File` support,
replay-source materialization, CRC validation, `content_crc` read/validation, body/raw-state/frame/
event parsing, or backend replay parser dependency is admitted by this pass.

## Fixture 001 Identity Confirmation

Fixture_001 was reverified directly:

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_001` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_001.replay` |
| exists | yes |
| byte length | `3001021` |
| SHA-256 | `F33EEFADAE8741DE7AA0CEC6D0BEA0120CDF795D16CAF3953A517B4AC6C6EAEB` |
| matched expected identity | yes |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

The first four bytes read as little-endian `i32` were `13200`. This is recorded only as
bytes-only fixture sanity evidence, not as new parser admission.

## Fixture 002 Availability Result

Candidate fixture id:

- `rl_replay_header_fixture_002`

Candidate destination:

- `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay`

Availability checks:

- destination existed before copy: no
- `MIMIR_REPLAY_FIXTURE_002_PATH` was set: yes
- environment source existed as a file: yes
- environment source extension was `.replay`: yes
- environment source was not the same file path as fixture_001: yes
- environment source SHA-256 differed from fixture_001 SHA-256: yes
- copied to destination: yes
- copied destination identity matched source length and SHA-256: yes

Caller-supplied private local source path:

- `C:\Users\navea\Documents\My Games\Rocket League\TAGame\DemosEpic\D9DA34DA11F0811EAC139A94CBF30AF2.replay`

That source path is recorded only as caller/user-supplied private local provenance for fixture
intake. It is not a parser fact and must not be used as parser evidence.

## Fixture 002 Identity

| Field | Value |
| --- | --- |
| fixture id | `rl_replay_header_fixture_002` |
| path | `D:\RocketLeague bot\MIMIR\external_fixtures\sample_002.replay` |
| byte length | `2632903` |
| SHA-256 | `376B00E023186B41408385AED4DEE1414AD919A40C92D9CE853F327F63FBCEC6` |
| differs from fixture_001 by SHA-256 | yes |
| admission form | `PRIVATE_LOCAL_PATH_WITH_HASH` |

This identity admits only that the private local fixture file exists with the recorded byte length
and SHA-256. It does not admit parser success.

## Fixture Safety Checks

Fixture_002 safety checks:

- extension is `.replay`: yes
- byte length is greater than 8: yes, `2632903`
- first four bytes read as little-endian `i32`: `11273`
- first four bytes recorded only as preliminary bytes-only `header_size` sanity evidence
- SHA-256 differs from fixture_001: yes

No bytes beyond the cheap first-four-byte sanity check were interpreted for fixture_002 in this
pass. No header structure, replay version, supported tuple, `ReplayHeader` mapping, CRC validity,
body data, raw-state data, frame data, or event data is claimed.

## Explicit Non-Claims

This pass does not claim:

- parser success for fixture_002
- supported replay version for fixture_002
- `ReplayHeader` mapping for fixture_002
- broad parser success
- `ReplayInput::File` support
- replay-source materialization
- path/hash/filename/provenance/artifact-id parser facts
- CRC validation
- `content_crc` read or validation
- body parsing
- raw-state parsing
- frame parsing
- event parsing
- export integration
- runtime integration
- CLI integration
- backend replay parser dependency

## What Remains Closed

Still closed after Outcome A:

- broad parser expansion
- any parser-success admission for fixture_002
- any broad version-family support
- `ReplayInput::File`
- replay-source materialization
- CRC validation
- `content_crc`
- body/raw-state/frame/event parsing
- export/runtime/CLI behavior
- backend replay parser dependencies

## Next Stage

Outcome A next stage:

- next pass may generate or admit a fixture_002 structural/header report
- no parser expansion yet
- no export/runtime/CLI integration yet
- no broad parser-success admission yet
