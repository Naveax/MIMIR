# MIMIR — R3.16A Execution Spec

**Date:** 2026-08-13  
**Pass:** `R3.16A — existing-actor first-property envelope evidence`  
**Kind:** evidence-only / read-only protocol characterization  
**Production code under test:** `bf4bccff82203ed049d33e942681fed07f23beb4`  
**Pinned oracle:** Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`

## 1. Goal

Prove the exact wire contract for the first admitted existing-actor property envelope before any native property payload reader is implemented.

The evidence lane must find `new == false` actor updates and characterize exactly the prefix:

```text
property_present
stream_id bounded integer
resolved actor/object context
resolved property object ID / property name
attribute tag
payload_start_bit
```

The pass stops **before consuming the attribute payload**.

## 2. Frozen production boundary

R3.16A is evidence-only. It must not modify:

- `crates/mimir-replay/src/lib.rs`;
- any Cargo manifest or `Cargo.lock`;
- replay fixtures/corpus;
- production lookup tables or resolver behavior;
- actor lifecycle state;
- attribute decoders;
- raw state, events, slices, skills, curriculum, runtime, or export surfaces.

The current production reader remains the R3.15C first-NewActor reader. A successful evidence run does not itself admit native property parsing.

## 3. Corpus identity

Use exactly the current 47 production-supported replay identities. Before oracle evidence is accepted:

1. recover the canonical 47-path selector from admitted continuity/evidence;
2. verify every replay exists;
3. verify replay SHA-256 against the admitted identity record;
4. reject duplicates, substitutions, aliases, or missing files.

## 4. Oracle selection rule

For each supported replay, scan the pinned Boxcars network decode in protocol order and select the earliest actor update satisfying all of:

```text
actor_present == true
alive == true
new == false
property_present == true
```

The evidence row must preserve the exact frame index and actor ordinal so the selected update can be reproduced.

If a replay has no such candidate, do not silently substitute another semantic lane. Record the absence and classify the pass according to the outcome rules below.

## 5. Required evidence fields

For every selected row record at minimum:

```text
relative_path
replay_sha256
frame_index
actor_ordinal
frame_time_raw_bits
frame_delta_raw_bits
actor_id
actor_context_object_id
actor_context_object_name
new_bit_end
property_present_start_bit
property_present_end_bit
property_present_value
stream_id_start_bit
stream_id_end_bit
stream_id_value
stream_id_bound
prop_id_bits_or_equivalent_bound_context
resolved_property_object_id
resolved_property_object_name
resolved_attribute_tag
payload_start_bit
```

Also preserve any inherited lookup key/class identity needed to prove that the property resolution came from the same lookup-plan family already admitted in production.

## 6. Questions this pass must answer

The evidence report must explicitly resolve:

1. Does every one of the 47 supported replays expose at least one reproducible `new == false && property_present == true` candidate?
2. What bounded-integer rule and bound are used for the selected `stream_id` values?
3. Does the resolved property object agree with MIMIR's admitted static/inherited lookup plan for the selected actor context?
4. Which attribute tags occur in the 47 first-property rows?
5. Is `payload_start_bit` unambiguous and monotonic for every selected row?
6. Are there any missing actor contexts, unresolved streams, invalid property object IDs, or oracle decode errors?

## 7. Aggregate report

Produce an immutable evidence bundle containing at least:

```text
source-scope audit
oracle/Boxcars identity
47-replay selector + SHA-256 identity report
selected first-property JSONL
per-replay comparison/resolution rows
aggregate tag distribution
stream-id min/max + bound/bit-consumption distribution
unresolved/malformed counters
summary JSON
aggregate text report
```

Required aggregate counters include:

```text
replays_total
oracle_decode_success
selected_existing_actor_property_rows
replays_without_candidate
property_present_true
stream_id_resolved
stream_id_unresolved
property_object_resolved
property_object_mismatch
invalid_property_object_id
payload_start_monotonicity_failures
oracle_error_count
production_mutation_count
cargo_mutation_count
```

## 8. Outcome rules

### Outcome A — evidence sufficient

All 47 replay identities are valid, all 47 produce one selected candidate, all required fields are present, property resolution is exact, no malformed/unresolved condition remains, and production/Cargo mutation counts are zero.

Outcome A permits the next contract/implementation decision for the narrow native existing-actor property-envelope header. It does **not** permit attribute payload decoding.

### Outcome B — protocol evidence reveals an unmodeled branch

The oracle is valid, but one or more supported replays require a materially different property-present/stream-resolution rule. Record the distinct branch family and stop. Do not patch production in the evidence pass.

### Outcome C — evidence infrastructure invalid

Artifact, selector, replay identity, oracle build, instrumentation, or evidence schema is invalid/incomplete. Fix only the evidence lane and rerun. Production remains frozen.

## 9. Hard stop

R3.16A ends after the decision and continuity sync. The following remain closed:

```text
native property-envelope consumption
attribute payload consumption
property loop iteration
next actor/frame iteration beyond existing admitted readers
actor lifecycle mutation
raw state
events
replay slicing
skill mining
counterfactual execution
training/runtime/export widening
```

No capability credit is granted from oracle-only evidence.
