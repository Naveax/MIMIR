# MIMIR R3.18BQ — One Following Payload Evidence Decision

**Date:** 2026-09-10
**Outcome:** **A — CLOSED / ADMITTED READ-ONLY EVIDENCE**

**Canonical production:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`
**Evidence head/tree:** `16c43f38e740c57ae9cb90c92084002ec83815e7` / `58248877a59fb0ddad707e32f92b2cec91f6b434`
**Evidence run/job:** `34457725716/102807933610` SUCCESS
**Same-head CI:** `34457725700/102808516101` SUCCESS / count 1
**Artifact:** `10144392560` / 9464 bytes / `sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c`
**Inner manifest SHA-256:** `332447c57f92f6f9af84e12bf74124adfe478d225e82cdb5d4cf8e925f7a97c9`
**Pinned Boxcars:** `c70e77df7af81b436cb545d070bb90c82f562d0b`

## Decision

R3.18BQ closes Outcome A on exactly the immutable R3.18BP three-row authority. The BP false terminator stayed outside payload decode. The two BP-true rows reproduced the published R3.18BO header prerequisite, decoded exactly one payload natively, and matched independently instrumented pinned Boxcars for row identity, tag, semantic value, payload start/end and width.

```text
BP authority rows                         3/3
false terminators excluded                1/1
true payload rows                         2/2
Boolean rows / width                      1 / 1 bit
ActiveActor rows / width                  1 / 33 bits
property ordinal 7                        2/2
native/oracle mismatch                    0
witness reselection                       0
false-row payload access                  0
next-control bits consumed                0
historical value/coordinate inheritance   0
production/Cargo/fixture/corpus/support   0/0/0/0/0
privacy + full validation                 PASS
```

Exact admitted payloads: `external_fixtures/sample_002.replay` at `[11238,11239)` is Boolean `true`; `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay` at `[3205,3238)` is ActiveActor `active=true, actor=1`. `external_fixtures/sample_003.replay` remains the BP false no-header terminator and never entered payload decode.

Repeatability, truncation, wrong-tag/start/context, post-payload poison, corrupt prerequisite, wrong actor/unresolved/RL223/context widening, source scope, privacy, fmt/check/clippy/test/repository verifier/diff-check all passed.

## Hard stop

BQ admits read-only payload evidence only. It does not add payload production composition to R3.18BO, read the next control bit, resolve another stream/header/payload, read a second later control, or create a generalized/repeated cursor.

## Next gate

R3.18BR may observe exactly one next `property_present` bit beginning at each exact BQ `payload_end_bit` on the same two BQ payload rows only. The BP false terminator remains inaccessible. Native and pinned Boxcars must match start/value/end exactly; the false/true distribution is an output and must not be inherited. Stop exactly one bit later; no next stream/header/payload or second later control is opened.
