# MIMIR — R3.16A Decision

**Date:** 2026-08-14  
**Pass:** `R3.16A — existing-actor first-property envelope evidence`  
**Outcome:** **A — ADMITTED / COMPLETE**

## Exact identities

```text
canonical base main SHA       = 76cbcc2094189e637e135f8c7d99e999e32311a0
production SHA                = bf4bccff82203ed049d33e942681fed07f23beb4
production source blob        = f64a5e0d66962f41026b2eb10e176219d4529931
evidence head                 = 31b858de7d855cbc32501e03282c8db6bf68ecd0
final exact CI run/job         = 31748905111 / 94609885915
pinned Boxcars SHA            = c70e77df7af81b436cb545d070bb90c82f562d0b
receipt terminal              = R3_16A_RECEIPT_STREAM=PASS
```

The final repository verifier completed successfully on the exact evidence head. The evidence test itself reported `R3_16A_OUTCOME=A` and `R3_16A_EVIDENCE=PASS` before the full repository verifier completed.

## Parent evidence identity

R3.16A reused the exact admitted R3.15D 47-replay selector/identity lineage:

```text
parent pass                    = R3.15D
parent run                     = 31736738234
parent artifact ID             = 9195419601
parent artifact digest         = sha256:f6e11055c11ed0724c45fcc76c13a9da2dbbb285ab3744f9738f0d4a19ecab8a
selector rows                  = 47
identity rows                  = 47
```

Every selected replay was present and replay SHA-256 identity was checked before oracle rows were accepted.

## Evidence publication / receipt

The final R3.16A run did **not** upload a separate GitHub Actions artifact. The immutable publication surface is the exact GitHub Actions job log for run/job `31748905111 / 94609885915`.

That exact job log serializes the evidence bundle as 13 bounded records, each enclosed by `R3_16A_FILE_BEGIN` / `R3_16A_FILE_END`, and terminates with `R3_16A_RECEIPT_STREAM=PASS`:

```text
r3_16a_source_scope.txt
r3_16a_parent_evidence_identity.txt
r3_16a_replay_identity.tsv
r3_16a_paths.txt
r3_16a_boxcars_instrumentation_sha256.txt
r3_16a_boxcars_log_sha256.txt
r3_16a_first_property_oracle.jsonl
r3_16a_oracle_selection_summary.json
r3_16a_mimir_queries.tsv
r3_16a_mimir.log
r3_16a_comparisons.jsonl
r3_16a_summary.json
r3_16a_aggregate.txt
```

No separate artifact ID is claimed for R3.16A.

## Source-scope audit

Production and Cargo remained frozen throughout the admitted run:

```text
production_mutation_count = 0
cargo_mutation_count      = 0
```

The Actions checkout was shallow, so an early diagnostic could not resolve the base commit object locally (`76cbcc...^{commit}`). This did not mutate or widen production. The canonical GitHub compare was therefore also checked independently between base `76cbcc2094189e637e135f8c7d99e999e32311a0` and evidence head `31b858de7d855cbc32501e03282c8db6bf68ecd0`; it reports exactly 11 changed paths, all temporary R3.16A evidence/test tooling, with no production Rust, Cargo manifest, `Cargo.lock`, replay corpus, or fixture change.

## Oracle / instrumentation identity

```text
Boxcars instrumentation patch SHA-256 = 33e8de056b7dcbe003a5f1de13eac8c699693d37807e6b2aaee7522060a7e201
Boxcars evidence log SHA-256           = c50f9a205bab401d782b6f4eccd95f2f45bc2d102df59c32cff5d00dbddb0ffc
```

The oracle remained pinned to Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`.

## Exact result

```text
replays_total                         = 47
oracle_decode_success                 = 47
selected_existing_actor_property_rows = 47
replays_without_candidate             = 0
property_present_true                 = 47
stream_id_resolved                    = 47
stream_id_unresolved                  = 0
property_object_resolved              = 47
property_object_mismatch              = 0
invalid_property_object_id            = 0
payload_start_monotonicity_failures   = 0
oracle_error_count                    = 0
production_mutation_count             = 0
cargo_mutation_count                  = 0
mismatch_count                        = 0
```

All 47 admitted replays expose one reproducible earliest actor update satisfying:

```text
actor_present == true
alive == true
new == false
property_present == true
```

For all 47 selected rows, the bounded stream ID and resolved property context agree with MIMIR's admitted `ReplayNetworkLookupPlanV1` family and the selected oracle row stops at the same unambiguous `payload_start_bit`.

## Observed bounded-stream distribution

```text
stream_id_min = 17
stream_id_max = 42

prop_id_bits distribution:
  4 bits = 7 rows
  5 bits = 38 rows
  6 bits = 2 rows

actual bounded stream-ID bits consumed:
  5 bits = 11 rows
  6 bits = 35 rows
  7 bits = 1 row
```

This distinction matters: `prop_id_bits` is bound context, not permission to replace the canonical value-dependent bounded-integer primitive with a fixed-width read.

## First-property attribute-tag distribution

```text
RigidBody   = 33
ActiveActor = 11
Byte        = 1
Float       = 1
Int         = 1
```

These counts characterize the selected first-property rows only. They do **not** admit any of these attribute payload decoders.

## Hard boundary proved

R3.16A proved only the structural prefix:

```text
existing actor (`new == false`)
→ property_present
→ bounded stream_id
→ inherited/static lookup-plan resolution
→ property object / attribute tag metadata
→ payload_start_bit
→ HARD STOP
```

No selected attribute payload bit was consumed as production capability.

Still closed:

```text
attribute payload decode
property loop iteration / second property
next actor/frame iteration beyond already admitted readers
actor lifecycle mutation
raw state
events
replay slicing
skills
counterfactual execution
training/runtime/export widening
```

## Decision

R3.16A satisfies Outcome A. The exact current 47-replay lane is sufficient to admit the next narrow production implementation decision: **R3.16B may implement only the first existing-actor property-envelope header semantics demonstrated here**.

R3.16B must stop before the selected attribute payload and must not infer permission for a full property loop from one first-property row per replay.

## Next pass

`R3.16B — native existing-actor first-property envelope header implementation`.

The exact execution contract is `docs/continuity/MIMIR_R3_16B_EXECUTION_SPEC.md`.
