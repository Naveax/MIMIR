# MIMIR R3.18AW — One Following Primitive Payload Evidence

**Status:** ACTIVE
**Pass type:** read-only one-payload boundary evidence
**Production authority:** R3.18AU `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef`
**Direct row authority:** admitted R3.18AV artifact `9640472993` / `sha256:26082be08c8644a17076d9df2138128df110bbf39b4b3bceefdc823a9492d456`
**Production mutation:** forbidden
**Next property-control bit:** forbidden
**Witness reselection:** forbidden

## Goal

On exactly the forty R3.18AV true continuation rows, reconstruct the published prerequisites through R3.18AU, require exact equality with the admitted AV following-header row, decode exactly one current primitive scalar beginning at the proven `payload_start_bit`, independently measure the same scalar with pinned Boxcars at the same current replay coordinates, require exact native/oracle equality, and stop at payload end.

All seven AV-false terminators are excluded before payload decoding and remain no-header/no-payload terminators.

## Frozen authority

```text
AV evidence head/tree                  fcbabd6953b4bade41f49b767f0dd73524e190d8 / 922e7fb45de33b1803027e6cdcbbe55467a1bc2e
AV run/job                             33057596762 / 98468171016 SUCCESS
AV same-head CI                        33057596712 / 98468756735 SUCCESS / count 1
AV artifact                            9640472993 / 10256 / sha256:26082be08c8644a17076d9df2138128df110bbf39b4b3bceefdc823a9492d456
AV row split                           false=7 / true=40
AV exact AT contexts / multiplicity    16 / 40
AV observed header tags                Int=40
AT contract                            sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
AS source artifact                     9603335255 / sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

The admitted AV artifact, not historical R3.18AM/R3.18AN payload evidence, is the direct AW row authority.

## No historical value inheritance

R3.18AM/R3.18AN are methodology references only. AW must not inherit historical property ordinal `4`, historical payload start/end positions, historical semantic values, a fixed following-header width, or a historical tag merely because an earlier boundary was `Int`.

Current AV observes `Int=40`, but AW still rematerializes the tag and boundary from the admitted AV artifact. Expected `payload_start_bit` must not be used as an oracle selector input.

## Exact target materialization

- consume all 47 admitted AV rows in frozen order;
- require exactly 7 false rows with no following-header fields and exclude them before payload decode;
- require exactly 40 true rows with complete current header fields;
- require `control_end == stream_start` and `header_stop_bit == payload_start_bit`;
- require exact R3.18AT context multiset equality: 16 contexts / multiplicity 40;
- preserve replay identity, frame index, actor ordinal, actor object, control/header coordinates and version context;
- witness reselection = 0.

## Native one-scalar evidence

Use published `decode_replay_network_primitive_scalar_v1` only after published R3.18AU has been reconstructed and its following header has matched the admitted AV row.

Before payload read require requested payload start equal the proven AU header stop, requested tag equal the proven resolved header tag, and the tag belong to the production primitive scalar family. Production widths are Boolean=1, Byte=8, Enum=11, Float=32, Int=32 and Int64=64; unsupported/compound tags reject before payload read.

Require `payload_end_bit == payload_start_bit + payload_width` and stop there.

## Independent Boxcars oracle

Pin Boxcars exactly at `c70e77df7af81b436cb545d070bb90c82f562d0b`. Target selection may use only current replay coordinates: frame index, actor ordinal, actor context object id, and current property-present start bit. Property ordinal is diagnostic only. Expected payload start is an oracle output, never selector input.

For exactly one matched property per target record property/header coordinates, observed tag, version context, payload start/end/width and a lossless primitive value.

## Native/oracle equality

Require exactly 40 native rows and exactly 40 oracle rows with identical frozen labels. For every row require exact equality of frame/actor identity, property-present boundary, stream identity/bounds, property object, tag, version context, payload start, payload end, payload width and lossless primitive value. Mismatch = 0.

## Required negative controls

- all 7 false rows absent from the payload target table and never invoke a payload decoder;
- repeat native scalar decode and require exact equality 40/40;
- truncate inside scalar payload -> atomic reject 40/40;
- request a tag different from the proven header tag -> reject before payload read 40/40;
- request `payload_start + 1` -> reject before payload read 40/40;
- mutate bits beginning at payload end -> decoded scalar unchanged 40/40;
- corrupt/mismatch published AU/header prerequisite -> reject;
- wrong actor, unresolved lookup, wrong exact context and RL223 widening remain rejected by the published prerequisite chain;
- AT component-only/Cartesian/versionless/AJ-only/fabricated-context widening remains rejected;
- source-scope guard proves one scalar decode only, no next-control decoder and no generalized/repeated property loop.

## Validation

Require independently verified AV artifact identity/digest/inner manifest; exact target materialization 40/40 with false excluded 7/7; replay identity 40/40; native payload rows 40/40; Boxcars rows 40/40; native/oracle mismatch 0; repeatability/truncation/wrong-tag/wrong-boundary/post-payload-poison 40/40 each; witness reselection 0; next-control consumption 0; focused regressions PASS; full fmt/check/test/clippy/repository verifier PASS; unique same-head normal CI SUCCESS; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## Hard stop

No next property-control bit, no following header after this payload, no second payload, no generalized property loop/cursor, no next actor/frame/lifecycle, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A
All exact forty current AV-true rows produce one native primitive scalar exactly matching pinned independent Boxcars; all negatives/full validation pass; false terminators remain excluded; next-control consumption is zero. A separate later pass may then investigate exactly one next property-control bit.

### Outcome B
A narrower exact payload subset is isolated without witness reselection or context/value inheritance. Record only that exact subset and keep the next control closed.

### Outcome C
Authority drift, false-row payload access, current-header mismatch, native/oracle mismatch, unsupported current tag, payload over-read, next-control access, production mutation, generic chaining or privacy failure. Stop without widening.
