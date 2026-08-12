# MIMIR Skill Forge BC Raw-State-Window Lookup / Observation-Access v1

## A. PURPOSE

### What this pass owns

This pass owns the first explicit raw-state-window lookup / observation-access planning boundary
above `LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1`.

It defines:

- one exact planning input boundary above the first concrete specimen consumer result
- one exact first lookup / observation-access planning role
- one exact sufficiency decision for the current consumed specimen view
- one minimal family-specific planning result surface
- one strict admission rule for when a first concrete specimen consumer result may enter
- one strict failure rule for degraded or manually-constructed first concrete specimen consumer
  results

### Why it exists

`LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1` already fixed:

- strict input from `LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1`
- preservation of the audited family root directory reference
- preservation of lane/specimen ordering
- preservation of artifact identity
- narrowing of the specimen payload to `LowBoostRecoveryBcArtifactConsumerHandoffV1`
- continued deferral of tensor/control materialization and `mimir_export`

That still left one unresolved question:

- whether the current `LowBoostRecoveryBcArtifactConsumerHandoffV1` surface is already the first
  honest planning view for raw-state-window lookup / observation access

This pass exists to answer that question explicitly before any later pass tries to realize raw
state lookup, observation materialization, or reopen another boundary.

### How it differs from the first concrete specimen consumer boundary below it

- The first concrete specimen consumer boundary proves what the first consumed specimen view is.
- This pass proves what a later raw-state-window lookup / observation-access planning consumer is
  allowed to inspect from that consumed view.
- This pass does not realize raw-state lookup, observation materialization, tensors, or controls.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This lookup / planning boundary remains family-specific because:

- the admitted input is one low-boost-recovery-specific first concrete specimen consumer result
  only
- the admitted specimen view is one low-boost-recovery BC handoff only:
  `LowBoostRecoveryBcArtifactConsumerHandoffV1`
- `source_raw_state_window_ref`, observation-binding semantics, accepted-reference-window
  semantics, target-binding deferral, confidence, and unresolved-assumption burden are all
  low-boost-recovery BC semantics already fixed by the current repo-local chain
- no second family exists yet to justify a shared lookup / planning abstraction

No generic all-family downstream/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1`
- the audited family root directory reference preserved by that result

Within `LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1`, this pass consumes:

- `specimen_count`
- `group_count`
- `source_downstream_disposition`
- `source_downstream_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `consumed_specimen_view`
- `consumer_disposition`
- `consumer_notes`

### Boundary rule

Direct input is no longer:

- continued receipt-bound downstream results
- emitted-output audit/readback results
- actual emission receipts
- emission plans
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- shells
- lower planning boundaries

Those lower layers are frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1` plus the preserved audited family root
directory reference.

## D. FIRST EXPLICIT RAW-STATE-WINDOW LOOKUP / OBSERVATION-ACCESS ROLE

The first bounded lookup / planning role above the first concrete specimen consumer result is:

- admit only already-validated low-boost-recovery first concrete specimen consumer results
- revalidate that the preserved first concrete consumer surface is still intact without reopening
  filesystem reads or lower planning layers
- preserve only the exact specimen view the next lookup / planning pass is allowed to inspect
- make raw-state-window and observation-binding visibility explicit while still forbidding
  materialization

### What it is allowed to inspect from the first concrete specimen consumer result

This planning boundary may inspect only:

- preserved counts
- source consumer disposition and notes
- the audited family root directory reference as a preserved receipt-bound provenance reference
- preserved lane order
- preserved specimen order
- the exact `LowBoostRecoveryBcArtifactConsumerHandoffV1` view inside each specimen result

Within the handoff view, this planning boundary may inspect only:

- artifact identity
- source lineage
- `source_raw_state_window_ref` as an opaque lookup reference only
- `source_phase_id`
- accepted-reference lineage
- `observation_binding_kind`
- `supervision_window_role`
- `accepted_reference_window`
- `target_binding_kind` only as an explicit deferral constraint
- carried confidence
- carried unresolved assumptions

### What it is not allowed to materialize yet

This pass is not allowed to materialize or infer:

- replay frames or parsed replay payloads
- raw state behind `source_raw_state_window_ref`
- any raw-state locator/index implementation
- sidecars or manifests
- generic manifest/index semantics
- tensors, feature vectors, or normalization outputs
- controls, actions, or labels
- usefulness claims
- policy-improvement claims
- `mimir_export` bundle state

Its role is planning-boundary definition only, not lookup realization.

## E. SUFFICIENCY DECISION FOR THE CONSUMED SPECIMEN VIEW

The decision in v1 is:

- keep `LowBoostRecoveryBcArtifactConsumerHandoffV1` intact as the lookup / planning consumed
  view

### Fields actually needed now

The first raw-state-window lookup / observation-access planning boundary currently needs every
field already present in `LowBoostRecoveryBcArtifactConsumerHandoffV1`, but for three distinct
reasons:

- direct lookup / observation-access planning inputs:
  - `source_raw_state_window_ref`
  - `observation_binding_kind`
  - `supervision_window_role`
  - `accepted_reference_window`
- provenance and identity constraints that keep planning auditable while
  `source_raw_state_window_ref` remains opaque:
  - `artifact_id`
  - `source_slice_id`
  - `source_replay`
  - `source_subject`
  - `source_phase_id`
  - `accepted_reference_variant_id`
- explicit boundary-limit fields that prevent silent widening into target/control or false
  certainty:
  - `target_binding_kind`
  - `carried_confidence_band`
  - `carried_unresolved_assumptions`

### Fields preserved

All fields in `LowBoostRecoveryBcArtifactConsumerHandoffV1` are preserved exactly.

Lane/specimen placement remains preserved separately through:

- lane vector order
- `lane_ordinal`
- specimen vector order inside each lane
- `specimen_ordinal`

The audited family root directory reference remains preserved separately at the top level.

### Fields intentionally dropped

No additional handoff fields are dropped in this pass.

That is deliberate. The current repo still has no concrete raw-state lookup implementation or
scoped locator contract, so dropping source lineage, target deferral, confidence, or unresolved
assumptions now would be speculative rather than proven narrowing.

### Why this is the narrowest honest contract now

Keeping `LowBoostRecoveryBcArtifactConsumerHandoffV1` intact is the narrowest honest contract now
because:

- the first concrete specimen consumer boundary already removed transport placement fields from the
  payload itself
- the repo has no implemented raw-state lookup realization that proves a smaller planning subset is
  sufficient
- `source_raw_state_window_ref` is still opaque, so the remaining lineage fields are the only
  repo-local constraints available to keep later lookup design auditable
- target deferral, confidence, and unresolved assumptions still constrain what this planning
  boundary may honestly promise

Further narrowing in this pass would guess future lookup semantics instead of preserving the
minimum already-proven specimen contract.

## F. LOOKUP / OBSERVATION-ACCESS PLANNING OUTPUT V1

The minimum family-specific lookup / planning result is:

- `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`

It contains exactly:

- `specimen_count`
- `group_count`
- `source_consumer_disposition`
- `source_consumer_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- `planning_disposition`
- `planning_notes`

### Lane-level shape

Each `preserved_ordered_lane_results` entry is:

- `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningLaneResultV1`

It contains exactly:

- `lane_ordinal`
- ordered `ordered_specimen_results`

### Specimen-level shape

Each `ordered_specimen_results` entry is:

- `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningSpecimenResultV1`

It contains exactly:

- `specimen_ordinal`
- `lookup_planning_consumed_specimen_view`

`lookup_planning_consumed_specimen_view` is exactly:

- `LowBoostRecoveryBcArtifactConsumerHandoffV1`

Artifact ids are preserved through:

- `lookup_planning_consumed_specimen_view.artifact_id`

Lane/specimen order is preserved through:

- lane vector order plus `lane_ordinal`
- specimen vector order plus `specimen_ordinal`

### Explicit visibility handling

`source_raw_state_window_ref` remains visible only inside
`lookup_planning_consumed_specimen_view`, and only as an opaque lookup reference. This result does
not reinterpret the audited family root directory as a raw-state storage root and does not perform
lookup realization.

`observation_binding_kind` remains visible only inside
`lookup_planning_consumed_specimen_view`, and only as a planning constraint that currently means:

- observation access is still defined relative to `accepted_reference_window`
- the accepted reference window remains visible for planning
- no tensor or observation payload is materialized

### Bounded planning disposition

`planning_disposition` is fixed to exactly:

- `ReadyForLowBoostRecoveryRawStateWindowLookupObservationAccessPlanningOnly`

That means only:

- the next pass may rely on one explicit planning-owned specimen view for receipt-bound
  raw-state-window lookup / observation-access design work

It does not mean:

- raw-state lookup is realized
- tensors exist
- controls/actions exist
- `mimir_export` is widened
- usefulness is proved

### Bounded planning notes

`planning_notes` are fixed to exactly:

- `FirstConcreteSpecimenConsumerBoundaryPreserved`
- `AuditedFamilyRootReferencePreserved`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactConsumerHandoffViewRetainedForLookupPlanning`
- `SourceRawStateWindowRefVisibleAsOpaqueLookupReferenceOnly`
- `ObservationBindingVisibleForPlanningOnly`
- `TensorAndControlMaterializationDeferred`
- `MimirExportIntegrationDeferred`

### Concrete entry function

The concrete entry function is:

- `plan_low_boost_recovery_bc_raw_state_window_lookup_observation_access_from_first_concrete_specimen_consumer_v1(...)`

## G. ADMISSION RULES

A first concrete specimen consumer result may enter this boundary only when all of the following
hold:

1. the input is `LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1`
2. `source_downstream_disposition == ReadyForLowBoostRecoveryAuditedSpecimenInspectionOnly`
3. `source_downstream_notes` remain the exact continued receipt-bound downstream note set
4. `consumer_disposition == ReadyForLowBoostRecoveryConsumedSpecimenViewOnly`
5. `consumer_notes` remain the exact first concrete specimen consumer note set
6. `audited_family_root_directory` basename remains `low_boost_recovery_bc_v1`
7. `group_count > 0`
8. `specimen_count > 0`
9. `preserved_ordered_lane_results` is non-empty
10. every `lane_ordinal` matches the concrete lane position
11. every `ordered_specimen_results` vector is non-empty
12. every `specimen_ordinal` matches the concrete specimen position
13. every `consumed_specimen_view` still satisfies the exact
    `LowBoostRecoveryBcArtifactConsumerHandoffV1` invariants
14. every `artifact_id` remains present and unique across the full admitted input
15. lane/specimen order remains exactly the preserved order already proven by the input result
16. no lower boundary is silently reopened to recreate or repair the admitted input

Admission here means only:

- this first concrete specimen consumer result may be converted into one explicit planning-owned
  raw-state-window lookup / observation-access planning result

Admission here does not mean:

- raw-state lookup realization is justified
- sidecar/manifest realization is justified
- `mimir_export` may be widened
- tensors or controls may be materialized

## H. FAILURE / DEFER RULES

This boundary must hard-fail for:

- malformed or degraded first concrete specimen consumer input
- wrong continued-downstream or first concrete consumer disposition/note sets
- missing or drifted counts
- lane/specimen order drift
- duplicate or missing artifact ids
- invalid or drifted `LowBoostRecoveryBcArtifactConsumerHandoffV1` content
- any attempt to reopen lower boundaries to repair the admitted input

This boundary may return a bounded success result only when:

- the admitted first concrete specimen consumer result is fully valid
- the current handoff view is preserved intact without widening the contract
- no raw-state or observation materialization is smuggled into this pass

### Failure behavior

- no repair is allowed
- no receipt regeneration is allowed
- no filesystem re-audit is allowed
- no specimen is skipped
- no resorting is allowed
- no inferred locator/index is allowed
- no partial success result is returned

### Defer behavior

There is no soft defer path in v1.

This is deliberate. This pass adds no new evidence gate beyond the already-preserved first
concrete specimen consumer surface. Remaining uncertainty already lives inside the preserved
handoff lineage plus carried unresolved assumptions. Inventing a defer state here would widen
semantics instead of narrowing them.

## I. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no sidecar/manifest realization
- no generic multi-family downstream/export framework
- no generic manifest/index framework
- no tensor materialization
- no control/action extraction
- no usefulness proof
- no policy-improvement proof
- no replay parsing
- no replay ingestion
- no raw-state materialization
- no rollout or physics work
- no async/background system
- no database work

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- the first explicit raw-state-window lookup / observation-access planning boundary is explicit
- the system remains strictly receipt-bound above
  `LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1`
- the planning-owned specimen view is now fixed explicitly instead of being left implicit inside
  the previous boundary
- `source_raw_state_window_ref` visibility is explicit and still opaque
- observation-binding visibility is explicit and still planning-only
- `mimir_export` remains untouched and still out of scope

### What remains deferred

This pass still does not guarantee:

- raw-state lookup realization
- receipt-independent locator/index semantics
- sidecar/manifest realization
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- a concrete proof of whether the current planning-owned view is still insufficient for actual
  receipt-bound raw-state-window lookup / observation-access realization
- still above
  `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
- still without `mimir_export` widening unless that separate decision is explicitly reopened

That next pass should stay family-specific and receipt-bound. It should prove insufficiency before
any reopen decision is entertained.
