# MIMIR Skill Forge BC Raw-State-Window Lookup Realization Proof v1

## A. PURPOSE

### What this pass owns

This pass owns the first proof-of-sufficiency / insufficiency boundary above
`LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`.

It defines:

- one exact input boundary above the raw-state-window lookup / observation-access planning result
- one exact sufficiency criterion for a first actual receipt-bound raw-state-window lookup
  realization pass
- one exact contract-only proof method
- one exact proof decision
- one minimal family-specific proof result surface
- one strict admission rule for when a planning result may enter this proof boundary
- one strict failure rule for degraded or manually-constructed planning results

### Why it exists

`LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1` already fixed:

- strict input from `LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1`
- preservation of the audited family root directory reference
- preservation of lane/specimen order
- preservation of artifact identity
- explicit visibility of `source_raw_state_window_ref` as an opaque lookup reference only
- explicit visibility of `observation_binding_kind` for planning only
- continued deferral of raw-state lookup realization, tensor/control materialization, sidecars,
  manifests, and `mimir_export`

That still left one unresolved question:

- whether the current planning-owned view already contains enough honest receipt-bound information
  for actual raw-state-window lookup realization

This pass exists to answer that question explicitly before any later pass claims that real lookup
work is now legal.

### How it differs from the lookup / observation-access planning boundary below it

- The lower planning boundary defines what a future lookup-realization pass is allowed to inspect.
- This pass decides whether that planning-owned view is already sufficient for actual
  receipt-bound realization.
- This pass remains proof-only. It does not realize lookup, materialize observations, or widen the
  repo into sidecars, manifests, indexes, tensors, controls, or `mimir_export`.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This proof boundary remains family-specific because:

- the admitted input is one low-boost-recovery-specific planning result only
- the admitted specimen view is one low-boost-recovery BC handoff only:
  `LowBoostRecoveryBcArtifactConsumerHandoffV1`
- the proof reasons about low-boost-recovery BC lineage, `source_raw_state_window_ref`,
  `accepted_reference_window`, and audited family-root semantics already fixed by the current
  repo-local chain
- no second family exists yet to justify a shared lookup-realization proof abstraction

No generic all-family lookup/index/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
- the audited family root directory reference preserved by that result

Within `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`, this pass
consumes:

- `specimen_count`
- `group_count`
- `source_consumer_disposition`
- `source_consumer_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `lookup_planning_consumed_specimen_view`
- `planning_disposition`
- `planning_notes`

### Boundary rule

Direct input is no longer:

- first concrete specimen consumer results
- continued receipt-bound downstream results
- emitted-output audit/readback results
- actual emission receipts
- filesystem/export-emission plans
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- accepted shells
- lower planning boundaries

Those lower layers are frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1` plus the preserved
audited family root directory reference.

## D. SUFFICIENCY QUESTION

The exact question is:

- does the current planning-owned view contain enough honest receipt-bound information for actual
  raw-state-window lookup realization?

In this repo-local context, "enough" means all of the following are already true without adding a
new contract:

1. for every admitted specimen, the preserved planning result plus the preserved audited family
   root already determine one concrete raw-state lookup source
2. that lookup source is receipt-bound to the currently admitted boundary rather than to reopened
   lower layers or uncontracted external state
3. the repo already exposes one exact invariant that maps `source_raw_state_window_ref` to that
   lookup source
4. once the source is located, the already-preserved
   `observation_binding_kind == accepted_reference_window_from_raw_state_window_ref` plus
   `accepted_reference_window` are enough to define observation access without inventing more
   lookup semantics

This pass counts the current planning-owned view as insufficient if any of the following hold:

- `source_raw_state_window_ref` remains only an opaque handle with no current locator contract
- the audited family root cannot honestly be interpreted as a raw-state storage root
- realization would require a new locator/index/sidecar/manifest contract or a reopen of lower
  boundaries
- realization would require guessing storage semantics from provenance labels, artifact ids,
  specimen ordinals, or directory names

## E. PROOF METHOD

This pass uses contract/proof reasoning only. It does not perform lookup realization.

### Allowed repo-local evidence

The only evidence allowed to count is:

- the current Rust surfaces in `mimir-skill`, `mimir-types`, `mimir-io`, and `mimir-export`
- the replay-slice contract statement that `raw_state_window_ref` is a linkage handle rather than
  a storage design
- the serialization/export statement that raw state stays out of the serialized BC artifact
- the actual filesystem emission contract that only the family root, lane directories, and
  specimen JSON files are written
- the emitted-output audit/readback, continued receipt-bound downstream, first concrete specimen
  consumer, and planning boundaries that preserve order, artifact identity, lineage, and the
  audited family root without adding locator semantics

### Proof steps

1. Re-admit the planning result and verify that its exact dispositions, notes, counts, order,
   artifact ids, and handoff invariants are still intact.
2. Inventory the receipt-bound information that remains visible above the planning boundary.
3. Compare that inventory against the sufficiency criterion above.
4. Ask whether any existing repo-local contract maps `source_raw_state_window_ref` plus the
   preserved family root / lineage to one concrete raw-state lookup source.
5. If no such contract exists, return a bounded insufficiency proof result instead of attempting
   realization.

### What this proof method explicitly does not do

- no replay parsing
- no replay-path recovery from `provenance_label`
- no raw-state materialization
- no locator/index implementation
- no filesystem inference beyond the meanings already fixed by current contracts
- no sidecar or manifest synthesis

## F. PROOF DECISION

The exact decision in v1 is:

- insufficient for a first actual receipt-bound raw-state-window lookup realization pass

### Why the current planning-owned view is insufficient

The current planning-owned view is insufficient because:

- `source_raw_state_window_ref` still remains only an opaque linkage handle
- the replay-slice contract explicitly describes that handle as linkage, not storage design
- `ReplaySourceRef.provenance_label` is a bounded provenance label, not a parser transcript or
  loader path contract
- the serialized BC artifact explicitly keeps raw state out of the artifact
- the actual filesystem emission boundary writes only:
  - `low_boost_recovery_bc_v1`
  - `recovery_context_lane_{lane_ordinal:04}`
  - `specimen_{specimen_ordinal:04}.json`
- the emitted specimen JSON contract preserves `source_raw_state_window_ref` but does not
  materialize raw state or define a raw-state locator
- the planning boundary preserves the audited family root reference, but that root is still only a
  BC specimen tree, not a raw-state storage root

### Exact missing piece

The exact missing piece is:

- one receipt-bound raw-state-window locator contract

More precisely, the repo is still missing one contract that takes the admitted planning-owned
specimen view and yields one concrete raw-state lookup source for each
`source_raw_state_window_ref` without reopening lower boundaries or guessing storage semantics.

### Why sidecars/manifests/generic indexing are still not automatically justified

This proof does **not** automatically justify sidecars, manifests, or generic indexing because:

- the proof identifies a missing locator/binding contract, not a proven implementation mechanism
- the current evidence does not prove that a root-level sidecar or manifest is the smallest honest
  fix
- the current evidence does not prove that a generic cross-family index is needed
- `mimir_export` remains unrelated to the missing locator contract and remains out of scope

The next legal step is therefore a deliberate reopen decision for the missing locator contract, not
an automatic sidecar/manifest/index addition.

## G. PROOF OUTPUT V1

The minimum family-specific proof result is:

- `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`

It contains exactly:

- `specimen_count`
- `group_count`
- `source_planning_disposition`
- `source_planning_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- `proof_disposition`
- `proof_notes`
- `exact_insufficiency_marker`

### Lane-level proof shape

Each `preserved_ordered_lane_results` entry is:

- `LowBoostRecoveryBcRawStateWindowLookupRealizationProofLaneResultV1`

It contains exactly:

- `lane_ordinal`
- ordered `ordered_specimen_results`

### Specimen-level proof shape

Each `ordered_specimen_results` entry is:

- `LowBoostRecoveryBcRawStateWindowLookupRealizationProofSpecimenResultV1`

It contains exactly:

- `specimen_ordinal`
- `artifact_id`

Artifact ids are preserved through:

- `artifact_id`

Lane/specimen order is preserved through:

- lane vector order plus `lane_ordinal`
- specimen vector order plus `specimen_ordinal`

### Exact proof disposition

`proof_disposition` is fixed to exactly:

- `InsufficientForActualReceiptBoundRawStateWindowLookupRealization`

### Exact proof notes

`proof_notes` are fixed to exactly:

- `RawStateWindowLookupObservationAccessPlanningBoundaryPreserved`
- `AuditedFamilyRootReferencePreserved`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `SourceRawStateWindowRefRemainsOpaqueLookupReferenceOnly`
- `MissingReceiptBoundRawStateWindowLocatorContract`
- `AuditedFamilyRootNotInterpretedAsRawStateLookupRoot`
- `ActualLookupRealizationDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationDeferred`

### Exact insufficiency marker

`exact_insufficiency_marker` is populated in v1 and is fixed to exactly:

- `MissingReceiptBoundRawStateWindowLocatorContract`

### Concrete entry function

The concrete entry function is:

- `prove_low_boost_recovery_bc_raw_state_window_lookup_realization_sufficiency_from_planning_v1(...)`

## H. ADMISSION RULES

A raw-state-window lookup / observation-access planning result may enter this proof boundary only
when all of the following hold:

1. the input is `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
2. `source_consumer_disposition == ReadyForLowBoostRecoveryConsumedSpecimenViewOnly`
3. `source_consumer_notes` remain the exact first concrete specimen consumer note set
4. `planning_disposition == ReadyForLowBoostRecoveryRawStateWindowLookupObservationAccessPlanningOnly`
5. `planning_notes` remain the exact planning note set
6. `audited_family_root_directory` basename remains `low_boost_recovery_bc_v1`
7. `group_count > 0`
8. `specimen_count > 0`
9. `preserved_ordered_lane_results` is non-empty
10. every `lane_ordinal` matches the concrete lane position
11. every `ordered_specimen_results` vector is non-empty
12. every `specimen_ordinal` matches the concrete specimen position
13. every `lookup_planning_consumed_specimen_view` still satisfies the exact
    `LowBoostRecoveryBcArtifactConsumerHandoffV1` invariants
14. every `artifact_id` remains present and unique across the full admitted input
15. no lower boundary is silently reopened to recreate or repair the admitted input

Admission here means only:

- this planning result may be evaluated for sufficiency vs insufficiency

Admission here does not mean:

- actual raw-state lookup realization is now legal
- sidecar/manifest realization is justified
- any locator/index implementation is justified
- `mimir_export` may be widened

## I. FAILURE / DEFER RULES

This boundary must hard-fail for:

- malformed or degraded planning input
- wrong first-concrete-consumer or planning disposition/note sets
- missing or drifted counts
- lane/specimen order drift
- invalid or drifted `LowBoostRecoveryBcArtifactConsumerHandoffV1` content
- duplicate or missing artifact ids
- any attempt to reinterpret the admitted family root as a raw-state storage root without a
  dedicated contract
- any attempt to reopen lower boundaries to repair the admitted input

This boundary may return a bounded proof result only when:

- the admitted planning result is fully valid
- the proof method stays contract-only
- the current planning-owned view is evaluated honestly against the sufficiency criterion

### Failure behavior

- no repair is allowed
- no receipt regeneration is allowed
- no filesystem re-audit is allowed
- no specimen is skipped
- no resorting is allowed
- no inferred locator/index is allowed
- no partial proof result is returned

### Defer behavior

There is no soft defer path in v1.

This is deliberate. For valid admitted input, this pass already has enough evidence to decide the
current boundary is insufficient. Inventing a softer state would widen semantics instead of making
the missing contract explicit.

## J. NON-GOALS

This pass does not do any of the following:

- no actual raw-state lookup realization
- no raw-state locator/index implementation
- no `mimir_export` integration
- no sidecar/manifest realization
- no generic multi-family downstream/export framework
- no generic manifest/index framework
- no tensor materialization
- no control/action extraction
- no replay parsing
- no replay ingestion
- no rollout or physics work
- no async/background system
- no database work
- no usefulness proof
- no policy-improvement proof

## K. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- the current planning-owned view has been explicitly tested against the first actual
  receipt-bound raw-state-window lookup realization question
- the answer is now explicit and auditable: the view is insufficient
- the missing contract is explicit:
  `MissingReceiptBoundRawStateWindowLocatorContract`
- counts, lane/specimen order, and artifact ids remain preserved in the proof result
- `mimir_export` remains untouched and still out of scope

### What remains deferred

This pass still does not guarantee:

- actual raw-state lookup realization
- any raw-state locator/index implementation
- sidecar/manifest realization
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- a deliberate low-boost-recovery-specific reopen decision for one receipt-bound raw-state-window
  locator contract above `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
  and informed by `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`
- still without `mimir_export` widening unless that separate decision is explicitly reopened
- still without sidecar/manifest realization unless a separate defect-driven decision proves one of
  those mechanisms is the minimum honest fix

Actual raw-state-window lookup realization is **not** the next pass, because this proof boundary
shows that the current planning-owned view still lacks the locator contract required to do it
honestly.
