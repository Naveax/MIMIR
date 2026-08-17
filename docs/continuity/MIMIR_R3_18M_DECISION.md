# MIMIR R3.18M — Bounded After-Second-Payload Control Production Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / PRODUCTION PUBLISHED**
**Production SHA:** `fd74ba8c520ab83b808730572c41e45d6dc616e6`
**Production tree:** `6285928b3ca724c77b761e70c54f7bd0763f11f0`

## Decision

R3.18M is admitted. Given one already-valid R3.18J second-property payload result, production validates the prior second-header/payload boundary, reads exactly one following `property_present` bit, and stops exactly one bit later. R3.18L observed `true` on all 47 frozen rows and no `false` witness, so production admits only `true`; `false` fails closed.

The new API does not decode a following stream ID, property header, payload, another control bit, or a generalized property loop.

## Exact authority

```text
pre-pass main                       346f5596c1ad38dd944cc50404206aab508ba951
production SHA/tree                 fd74ba8c520ab83b808730572c41e45d6dc616e6 / 6285928b3ca724c77b761e70c54f7bd0763f11f0
lib.rs blob                         029c48e38ea0257f8cdb3fa8715bde5a789213e7
focused test blob                   a9bd2d0a8007c8cae76a0d14ad0c11ed387fe5a6
implementation v3                   31999687944 / 95297550306 SUCCESS
same-head temp CI                   31999687880 / 95297550231 SUCCESS
clean-candidate CI                  31999898754 / 95298116788 SUCCESS
published-main CI                   32000211020 / 95298954375 SUCCESS
R3.18L evidence head                9205ac1616e686589938f952782a32f03d0d1488
R3.18L run/job                      31978791346 / 95242213413 SUCCESS
R3.18L artifact                     9271817700
R3.18L artifact digest              sha256:db5d2db96429a4f2b699dca5176fc4d218f9eb9e4faa8dee813b766896f70c1c
```

## Clean scope

Exactly two production files changed from the pre-pass main:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_18m_following_control.rs`

No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file entered the clean production commit.

## Validation

- 6 focused R3.18M tests PASS;
- full `mimir-replay` regression PASS;
- workspace check/test PASS;
- workspace clippy with warnings denied PASS;
- repository verifier PASS;
- exact clean-candidate Windows CI PASS;
- exact published-main Windows CI PASS;
- source audit: exactly one `read_bit`, zero following stream/header/payload decoder calls, zero property loops.

The v1 and v2 branches are non-authority orchestration attempts. v2 proved the production patch through repository verification; its final scope check failed only because `git diff --name-only` omits an untracked newly-created test file. v3 corrected the audit by combining tracked diff and untracked-file enumeration; the production patch itself was unchanged.

## Hard stop

R3.18M does not admit `false` in this context, a following stream ID/header/payload, another property-control bit, repeated/generalized property iteration, a chainable public cursor, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening, or support/dependency expansion.

## Next exact pass

`R3.18N — published R3.18M after-second-payload control real-replay differential audit` over the immutable 47-row R3.18L lane. Only a clean Outcome A may open a separate evidence pass for the following property header.
