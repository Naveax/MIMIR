# MIMIR R3.18BZ — Published-R3.18BY Mixed Following-Header Differential

**Status:** PREPARED / BLOCKED ON R3.18BY PUBLICATION  
**Pass type:** read-only published-production differential  
**Expected production authority:** R3.18BY bounded post-BU mixed-continuation following header  
**Frozen evidence authority:** R3.18BW + R3.18BX  
**Following payload decode:** forbidden  
**Second later property-control bit:** forbidden  
**Generalized/repeated property loop:** forbidden

## Goal

Audit the exact published R3.18BY API against the immutable two-row R3.18BW/R3.18BX authority without widening the production surface.

- Preserve both published R3.18BU control identities.
- Verify the BU=false Boolean row remains a successful terminator with no header access.
- Verify the BU=true ActiveActor row returns exactly one following existing-actor header through `payload_start`.
- Compare the true-row published BY result against the frozen R3.18BW structural/oracle row and the shared stateless header primitive.
- Consume zero following-payload bits and zero second-later-control bits.

## Frozen lane

```text
rows                                  2
false terminator                      sample_002 / control [11239,11240) / stop 11240
true continuation                     largest_100/079... / control [3238,3239) / stop 3239
true following stream                 [3239,3245) / id 61 / bound 110 / prop bits 6
true property                         object 67 / TAGame.PRI_TA:ClientLoadoutsOnline
true attribute tag                    LoadoutsOnline
true property ordinal                 8
true payload_start / BY stop          3245
true exact context                    (110,6,67,LoadoutsOnline,868,32,10,false)
expected false/true                   1/1
expected native-oracle mismatch       0
following payload bits                0
second later control bits             0
```

## Required differential checks

1. Freeze the exact published R3.18BY main SHA/tree before execution.
2. Reconstruct the exact two R3.18BU prerequisite rows from published code; no witness reselection.
3. Call only the published R3.18BY API for the candidate result.
4. False row: `following_header=None`, stop exactly `11240`, and no post-BU header read.
5. True row: exact control/header coordinates, stream id/bound/prop bits, actor identity, property object/name/tag, context and `payload_start=3245`.
6. Independently decode the same true header with the shared stateless existing-actor header suffix and require structural equality.
7. Reconcile the result with the immutable R3.18BW evidence artifact and R3.18BX admitted tuple.
8. Repeat the full two-row observation twice and require deterministic equality.
9. Truncate within the true-row header and require atomic rejection.
10. Poison the bit at `payload_start` and require the BY result to remain unchanged.
11. Corrupt supplied BU authority and require rejection.
12. Remove required actor/property lookup material and require rejection.
13. Mutate version/net/RL223 and require rejection.
14. Prove the false row never reaches the header-suffix path.
15. Prove no following payload decoder and no later property-control read occur.
16. Prove no generic/repeated property loop or exported chainable cursor is introduced.

## Expected artifact

Emit a compact evidence artifact containing:

- published BY SHA/tree;
- exact two source rows and control coordinates;
- false/true counts;
- true header structural identity;
- exact eight-field context and membership result;
- stateless-header equality result;
- R3.18BW oracle equality result;
- repeatability counters;
- negative-control counters;
- witness-reselection count;
- following-payload and second-control consumption counters;
- SHA-256 digests for row, aggregate, negative and validation summaries.

## Outcome gate

### Outcome A

Exact 2/2 published rows match; false terminator 1/1; true following header 1/1; exact R3.18BX context 1/1; native/stateless/oracle mismatch 0; witness reselection 0; payload/second-control consumption `0/0`; all negatives pass. Close BZ and open R3.18CA as one-following-payload read-only evidence on only the exact BY=true row.

### Outcome B

Only a stricter safe subset of the published surface remains reproducible. Record the subset and do not open payload evidence beyond it.

### Outcome C

Published-source drift, false-row header access, context widening, lookup ambiguity, payload/later-control access, nondeterminism, oracle mismatch or generalized chaining. Stop without capability widening.

## Hard stop

No following payload, no second later property-control bit, no new contract, no production source change, no repeated/generalized property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
