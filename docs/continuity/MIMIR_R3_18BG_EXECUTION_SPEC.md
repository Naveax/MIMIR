# MIMIR R3.18BG — One Following Primitive Payload Evidence

**Status:** ACTIVE
**Pass type:** read-only one-payload boundary evidence
**Production authority:** R3.18BE `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`
**Direct row authority:** admitted R3.18BF artifact `10009534065` / `sha256:79a5d254876d19d90e03dcfeff650755d8b816d8a6869e13b8468eebd7d60bdc`
**Production mutation:** forbidden
**Next property-control bit:** forbidden
**Witness reselection:** forbidden

## 1. Goal

On exactly the three R3.18BF true continuation rows, reconstruct the published prerequisites through R3.18BE, require exact equality with the admitted BF following-header row, decode exactly one current primitive scalar beginning at the proven `payload_start_bit`, independently measure the same scalar with pinned Boxcars at the same current replay coordinates, require exact native/oracle equality, and stop exactly at payload end.

All thirty-seven BF-false terminators are excluded before payload decoding. The seven upstream AU false terminators remain outside the BA/BE/BF/BG lane entirely.

## 2. Frozen authority

```text
production SHA/tree                    1d717d3e82179edd85b197968f46b8f951a3e828 / 72cf2b907437a1ba62cc9deebd7608f7d0372f81
continuity base SHA/tree               cbfc861e1b570fcb2e9e1faf8b6bd16149b549b9 / cec0a3bbc64834b9288fe3effb7474387eb024ed
BF evidence head/tree                  5a3f875a445f9a3a2176788555089562948c3676 / d4b0b0510d24f5c0ba0f3d748201d9fed4ea7e0f
BF run/job                             34098102185 / 101666129830 SUCCESS
BF same-head CI                        34098102183 / 101666129957 SUCCESS
BF artifact                            10009534065 / 9998 / sha256:79a5d254876d19d90e03dcfeff650755d8b816d8a6869e13b8468eebd7d60bdc
BF inner manifest                     sha256:35747c9813f56e58c1515dc301cf6a0d3d3a86fd0b068fba609948016d0e45ce
BF row split                           false=37 / true=3
BF exact BD contexts / multiplicity    3 / 3
BF observed true-header tags           Boolean=2 / Float=1
BD contract                            sha256:33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

The admitted BF artifact is the direct BG row authority. R3.18AW/R3.18AM/R3.18AN are methodology references only.

## 3. No historical value inheritance

BG must not inherit any historical property ordinal, payload start/end position, semantic value, fixed replay coordinate, or old target row merely because an earlier payload pass used the same primitive machinery. Expected `payload_start_bit` must never be used as an oracle selector input.

## 4. Exact target materialization

Consume all forty admitted BF rows in frozen order:
- exactly 37 false rows must have no following header and are excluded before payload decode;
- exactly 3 true rows must have complete current header fields;
- require published BE/header identity and exact R3.18BD membership before payload access;
- require `header_stop_bit == payload_start_bit`;
- preserve replay identity, frame index, actor ordinal, actor object, stream/header coordinates and version context;
- require exact BF context multiset equality: 3 contexts / multiplicity 3;
- witness reselection = 0.

## 5. Native one-scalar evidence

Use published `decode_replay_network_primitive_scalar_v1` only after the exact published R3.18BE header has matched the admitted BF true row.

Before payload read require requested payload start equal the proven BE header stop and requested tag equal the proven resolved header tag. Current BF authority admits exactly:
- `Boolean`: width 1 bit, two rows;
- `Float`: width 32 bits, one row.

For `Float`, preserve raw IEEE-754 bits losslessly in addition to interpreted value. Require `payload_end_bit == payload_start_bit + payload_width` and stop there.

## 6. Independent Boxcars oracle

Pin Boxcars exactly at `c70e77df7af81b436cb545d070bb90c82f562d0b`. Target selection may use only current replay coordinates available before payload interpretation: frame index, actor ordinal, actor context object id and current property-present start bit. Property ordinal is diagnostic only. Expected payload start, width and semantic value are oracle outputs, never selector inputs.

For exactly one matched property per target record replay/frame/actor identity, property/header coordinates, observed tag/version context, payload start/end/width and lossless primitive value.

## 7. Native/oracle equality

Require exactly three native payload rows and exactly three oracle payload rows with identical frozen labels. Per row require exact equality of replay/frame/actor identity, property/stream/header identity, property object, tag, version context, payload start/end/width and lossless primitive value.

```text
targets                       3
Boolean rows                  2 / width 1
Float rows                    1 / width 32
native/oracle mismatch        0
witness reselection           0
next-control consumption      0
```

## 8. Required negative controls

- all 37 BF-false rows are absent from the payload target table and never invoke a payload decoder;
- all 7 upstream AU false terminators remain outside the lane;
- repeat native scalar decode and require exact equality 3/3;
- truncate inside scalar payload -> atomic reject 3/3;
- wrong tag -> reject before payload read 3/3;
- request `payload_start + 1` -> reject before payload read 3/3;
- mutate bits beginning at payload end -> decoded scalar unchanged 3/3;
- corrupt/mismatch published BE/header prerequisite -> reject;
- wrong actor, unresolved lookup, wrong exact version/context and BD widening remain rejected;
- component-only/Cartesian/versionless/fabricated-context widening remains rejected;
- source-scope guard proves one scalar decode only, no next-control decoder and no generalized/repeated property loop.

## 9. Validation

Require BF artifact identity/digest/inner manifest; frozen rows 40/40; false excluded 37/37; true materialized 3/3; exact BD contexts 3/3; native payload rows 3/3; Boxcars rows 3/3; Boolean=2 / Float=1 with widths 1/1/32; native/oracle mismatch 0; all negative controls PASS; witness reselection 0; next-control consumption 0; focused/full fmt/check/test/clippy/repository verifier PASS; unique same-head normal CI SUCCESS; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## 10. Hard stop

No next property-control bit, following header after this payload, second payload, payload access on the 37 BF false rows, generalized property loop/cursor, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 11. Outcome gate

### Outcome A
All exact three BF-true rows produce one native primitive scalar exactly matching pinned Boxcars; all negatives/full validation pass; false terminators remain excluded; next-control consumption is zero. A separate later pass may investigate exactly one next property-control bit at the proven payload ends.

### Outcome B
A narrower exact payload subset is isolated without witness reselection or historical coordinate/value inheritance. Record only that subset and keep the next control closed.

### Outcome C
Authority drift, false-row payload access, header mismatch, native/oracle mismatch, unsupported tag, payload over-read, next-control access, production mutation, generic chaining or privacy failure. Stop without widening.
