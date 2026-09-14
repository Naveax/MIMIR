# MIMIR R3.18CA — One Following-Payload Evidence After Published R3.18BY

**Status:** PREPARED / BLOCKED ON R3.18BZ OUTCOME A  
**Pass type:** read-only payload-boundary evidence  
**Expected production authority:** published R3.18BY  
**Header authority:** R3.18BX exact tuple + R3.18BZ published-production differential  
**Later property-control bit:** forbidden  
**Production mutation:** forbidden  
**Generalized/repeated property loop:** forbidden

## Goal

Observe exactly one payload belonging to the exact published R3.18BY true-row following header. Do not assume payload width or semantic representation before the pinned oracle and native bounded decoder agree.

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

## Evidence procedure

1. Freeze exact published R3.18BY SHA/tree and successful published-main validation receipts.
2. Reconstruct the exact two-row BU/BY lane without witness reselection.
3. Prove the false row terminates at 11240 and performs zero payload access.
4. On the exact true row, require the published BY header to equal the frozen R3.18BX context and stop at 3245.
5. Instrument pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b` at exactly this property/payload boundary.
6. Determine the exact payload representation, bit width, end bit and semantic value from the pinned oracle.
7. Use only an already-admitted native primitive/K2/K3/K4 decoder if the observed tag and representation fall inside its exact existing contract. Do not add a decoder in this evidence pass.
8. Compare native and pinned-oracle payload start/end/width/value representation exactly.
9. Repeat twice and require deterministic equality.
10. Truncate at every materially distinct payload boundary needed to prove atomic rejection.
11. Poison the first bit after payload end and require the observed payload result to remain unchanged.
12. Prove zero next-property-control consumption.
13. Emit the exact observed context/value family and multiplicity without converting multiplicity into a runtime-frequency promise.
14. Keep all production/Cargo/fixture/corpus/support mutation at zero.

## Outcome gate

### Outcome A

The exact BY=true row yields one payload whose complete representation is already supported by an admitted decoder, native and pinned Boxcars agree exactly, payload end is deterministic, all negatives pass, and next-control consumption remains zero. Close CA and open a separate contract or bounded-production pass appropriate to the observed payload family.

### Outcome B

The payload is structurally observable but only a strict subset is representable by existing admitted decoders. Record only that subset; do not widen a decoder in this pass.

### Outcome C

The payload requires an unadmitted decoder family, has ambiguous boundary/semantic interpretation, differs from pinned Boxcars, depends on witness reselection, touches the false terminator, consumes a later control, or otherwise violates the hard stop. Close with no production widening and open the smallest prerequisite decoder/evidence pass.

## Required artifact fields

- published BY SHA/tree and validation run IDs;
- exact false/true source identities and entry coordinates;
- BY header identity and R3.18BX membership result;
- payload start/end/width;
- exact observed tag/value representation;
- native decoder family used, if any;
- native/oracle equality counters;
- repeatability and truncation counters;
- post-payload poison result;
- witness-reselection count;
- next-control bits consumed;
- source-scope and privacy scan results;
- per-file SHA-256 manifest.

## Hard stop

No decoder widening, no production source mutation, no false-row payload access, no next property-control bit, no second payload, no historical-contract inheritance, no generic cursor/property loop, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
