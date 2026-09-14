# MIMIR R3.18CA — One Following-Payload Evidence After Published R3.18BY

**Status:** PREPARED / BLOCKED ON R3.18BZ OUTCOME A  
**Pass type:** read-only payload-boundary evidence  
**Expected production authority:** published R3.18BY  
**Header authority:** R3.18BX exact tuple + R3.18BZ published-production differential  
**Primary existing native payload candidate:** R3.17O K4 `LoadoutsOnline` decoder  
**Later property-control bit:** forbidden  
**Production mutation:** forbidden  
**Generalized/repeated property loop:** forbidden

## Goal

Observe exactly one payload belonging to the exact published R3.18BY true-row following header. Do not assume payload width, exact admitted K4 shape, or semantic value before the pinned oracle and the existing bounded native decoder agree.

The BU=false row remains a terminator and is outside the payload lane. Only the immutable true continuation row may enter this pass.

## Frozen entry boundary

```text
source rows                            2
false terminator                      sample_002 / BY stop 11240 / no payload access
true continuation                     largest_100/079... / BY stop 3245
true header context                   (110,6,67,LoadoutsOnline,868,32,10,false)
property                              TAGame.PRI_TA:ClientLoadoutsOnline
attribute tag                         LoadoutsOnline
property ordinal                      8
payload_start                         3245
later control access                  0
```

## Existing native decoder constraint

`ReplayNetworkAttributeTagV1::LoadoutsOnline` is already implemented by the bounded R3.17O K4 decoder. That fact permits **attempting** the existing decoder in this evidence pass; it does not admit a new K4 shape.

The CA evidence runner must:

1. call the existing `decode_replay_network_k4_v1` at the exact `payload_start=3245` with the exact replay context and lookup objects;
2. accept a native result only if the decoder's existing R3.17N/R3.17O exact shape allowlist already admits the observed `LoadoutsOnline` representation;
3. record the exact K4 width and shape returned by the existing admission machinery;
4. treat `unadmitted-k4-shape` as Outcome B/C evidence, never as permission to edit or widen `k4_admitted_groups.rs` in CA;
5. keep all K4 source, admitted groups, Cargo/dependencies and production APIs unchanged.

No width from another `LoadoutsOnline` row may be inherited. Existing widths such as 726/854/1080/1352 are historical examples only until this exact witness is measured.

## Evidence procedure

1. Freeze exact published R3.18BY SHA/tree and successful published-main validation receipts.
2. Freeze exact R3.18BZ Outcome A artifact/runner identity before opening payload observation.
3. Reconstruct the exact two-row BU/BY lane without witness reselection.
4. Prove the false row terminates at 11240 and performs zero payload access.
5. On the exact true row, require the published BY header to equal the frozen R3.18BX context and stop at 3245.
6. Instrument pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b` at exactly this property/payload boundary.
7. Determine the exact payload representation, bit width, end bit and semantic value from the pinned oracle.
8. Invoke only the already-published K4 decoder as the primary native candidate. Do not add or widen a decoder in this evidence pass.
9. Compare native and pinned-oracle payload start/end/width/value representation exactly when K4 existing membership admits the row.
10. Repeat twice and require deterministic equality.
11. Truncate at every materially distinct payload boundary needed to prove atomic rejection.
12. Poison the first bit after payload end and require the observed payload result to remain unchanged.
13. Prove zero next-property-control consumption.
14. Emit the exact observed context/value family and multiplicity without converting multiplicity into a runtime-frequency promise.
15. Keep all production/Cargo/fixture/corpus/support mutation at zero.

## Required native/oracle checks

At minimum record:

- exact K4 input context and `LoadoutsOnline` tag;
- whether existing K4 membership accepts or rejects the exact row;
- native payload start/end/width when accepted;
- native K4 semantic fields (`blue`, `orange`, `unknown1`, `unknown2`) in a deterministic digest-safe representation;
- pinned Boxcars payload start/end/width and corresponding structural value representation;
- exact native/oracle equality or the exact fail-closed rejection category;
- zero lookup/witness substitution;
- zero later-control read.

## Outcome gate

### Outcome A

The exact BY=true row yields one `LoadoutsOnline` payload whose complete K4 representation is already supported by the published exact K4 allowlist, native and pinned Boxcars agree exactly, payload end is deterministic, all negatives pass, and next-control consumption remains zero. Close CA and open a separate bounded-production pass for exactly that observed K4 shape.

### Outcome B

The payload is structurally observable but the exact row is not in existing K4 admitted membership, or only a stricter safe subset is representable by existing admitted decoders. Record the exact shape/width and stop. A separate K4 evidence/contract pass is required before any production composition.

### Outcome C

The payload has ambiguous boundary/semantic interpretation, differs from pinned Boxcars, depends on witness reselection, touches the false terminator, consumes a later control, or otherwise violates the hard stop. Close with no production widening and open the smallest prerequisite evidence pass.

## Required artifact fields

- published BY SHA/tree and validation run IDs;
- exact R3.18BZ artifact/run/digest authority;
- exact false/true source identities and entry coordinates;
- BY header identity and R3.18BX membership result;
- payload start/end/width;
- exact observed `LoadoutsOnline` K4 shape/value representation;
- existing K4 membership accepted/rejected result and category;
- native/oracle equality counters;
- repeatability and truncation counters;
- post-payload poison result;
- witness-reselection count;
- next-control bits consumed;
- source-scope and privacy scan results;
- per-file SHA-256 manifest.

## Hard stop

No K4 decoder or allowlist widening, no production source mutation, no false-row payload access, no next property-control bit, no second payload, no historical payload-width/shape inheritance, no generic cursor/property loop, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
