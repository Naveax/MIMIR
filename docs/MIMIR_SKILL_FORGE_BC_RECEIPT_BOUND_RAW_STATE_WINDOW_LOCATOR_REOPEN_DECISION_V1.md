# MIMIR Skill Forge BC Receipt-Bound Raw-State-Window Locator Reopen Decision v1

## A. PURPOSE

### What this pass owns

This pass owns one bounded low-boost-recovery-specific reopen-decision boundary above
`LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1` and informed by
`LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`.

It answers only one question:

- should one narrow receipt-bound raw-state-window locator contract now be deliberately reopened

If the answer is yes, this pass fixes the narrowest honest contract shape that may be defined next.
If the answer is no, this pass keeps the boundary closed explicitly.

### Why it exists

The lower planning boundary already fixed what the next raw-state-window lookup / observation-access
consumer is allowed to inspect.

The lower realization-proof boundary already proved that the current planning-owned view is still
insufficient for actual receipt-bound raw-state-window lookup realization and isolated one exact
missing piece:

- `MissingReceiptBoundRawStateWindowLocatorContract`

This pass exists because that proof result makes a reopen question unavoidable, but it still does
not justify jumping directly to actual lookup realization, sidecars, manifests, generic indexing,
or `mimir_export`.

### How it differs from the realization-proof boundary below it

- The realization-proof boundary proves insufficiency and names the missing piece.
- This pass decides whether reopening that missing piece is justified at all.
- If reopening is justified, this pass defines only the minimum contract shape that the next pass
  may formalize.
- This pass does not realize raw-state lookup.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This reopen decision remains family-specific because:

- the admitted planning result is low-boost-recovery-specific
- the admitted proof result is low-boost-recovery-specific
- the preserved specimen view is still `LowBoostRecoveryBcArtifactConsumerHandoffV1`
- the deterministic root/lane/specimen naming rules already fixed below this boundary are
  low-boost-recovery BC rules, not generic dataset rules
- no second family exists yet to justify a shared locator-contract reopen framework

No generic all-family lookup/index/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
- `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`
- the audited family root directory reference preserved by the planning result and echoed by the
  proof result

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

Within `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`, this pass consumes:

- `specimen_count`
- `group_count`
- `source_planning_disposition`
- `source_planning_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `artifact_id`
- `proof_disposition`
- `proof_notes`
- `exact_insufficiency_marker`

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

Those lower layers are frozen for this pass. This pass starts strictly from the planning result,
the proof result, and the preserved audited family root directory reference.

## D. DECISION QUESTION

The exact question is:

- should one narrow receipt-bound raw-state-window locator contract now be deliberately reopened

This question exists only because the realization-proof boundary already established that the
current planning-owned view is insufficient for actual receipt-bound raw-state-window lookup
realization.

This is not yet actual lookup realization because this pass still does not:

- bind `source_raw_state_window_ref` to a realized raw-state payload
- parse replays
- materialize observations
- materialize tensors or controls
- introduce sidecars, manifests, generic indexing, or `mimir_export`

It decides only whether the missing locator contract may now be formalized.

## E. REOPEN CRITERIA

Reopening is justified only when all of the following hold:

1. the missing piece isolated by the proof is truly one contract-level defect rather than a broad
   storage redesign
2. that missing contract can stay low-boost-recovery-specific
3. that missing contract can stay strictly receipt-bound
4. the contract can bind `source_raw_state_window_ref` to one concrete lookup source without
   reinterpreting the audited family root as a raw-state storage root
5. the contract can avoid sidecars, manifests, and generic indexing because deterministic
   low-boost-recovery root/lane/specimen path rules are already fixed below this boundary
6. the contract can avoid `mimir_export` because the missing defect lives entirely inside the
   low-boost-recovery receipt-bound BC path
7. the contract can remain contract-only in the next pass, without silently becoming actual
   raw-state lookup realization

## F. DECISION

The decision in v1 is:

- reopen justified for one narrow receipt-bound raw-state-window locator contract

### Why reopening is justified

Reopening is justified because the proof result already narrowed the defect to one missing locator
contract and the repo already preserves enough deterministic receipt-bound truth to define that
contract narrowly:

- the audited family root directory is preserved
- lane order and specimen order are preserved
- lane/specimen ordinals are preserved
- artifact ids are preserved
- `source_raw_state_window_ref` remains preserved in the planning-owned specimen view
- deterministic low-boost-recovery lane/specimen naming rules are already fixed below this
  boundary

That means the minimum honest reopen is not a storage redesign. It is one family-specific contract
that binds each preserved `source_raw_state_window_ref` to one deterministic receipt-bound BC
specimen-file lookup source under the audited family root.

### What exactly is reopened

The reopen is limited to one contract only:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`

### What it binds

It binds one admitted planning-owned specimen view to one deterministic low-boost-recovery BC
specimen file under the audited family root through:

- `audited_family_root_directory`
- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- the preserved planning-owned lineage including `source_raw_state_window_ref`

### What it does not bind

It does not bind:

- the audited family root to a raw-state storage root
- `source_raw_state_window_ref` directly to parsed replay frames
- `source_raw_state_window_ref` directly to tensors
- `source_raw_state_window_ref` directly to controls/actions

### What remains deferred

This decision still defers:

- actual raw-state lookup realization
- replay parsing
- receipt-independent reopening
- sidecar/manifest realization
- generic indexing
- `mimir_export`
- tensor materialization
- control/action extraction

### Why this is the minimum honest reopen

This is the minimum honest reopen because:

- the proof identified a missing locator contract, not a missing export framework
- deterministic specimen-file placement already exists below this boundary
- no current evidence proves that a sidecar, a manifest, or a generic index is required
- no current evidence proves that `mimir_export` participates in the defect path

## G. LOCATOR CONTRACT SHAPE V1

The narrowest acceptable contract shape is:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`

### Exact inputs it would consume

The contract would consume only the admitted planning boundary inputs for one specimen:

- `audited_family_root_directory`
- `lane_ordinal`
- `specimen_ordinal`
- `lookup_planning_consumed_specimen_view.artifact_id`
- `lookup_planning_consumed_specimen_view.source_raw_state_window_ref`
- `lookup_planning_consumed_specimen_view.source_slice_id`
- `lookup_planning_consumed_specimen_view.source_replay`
- `lookup_planning_consumed_specimen_view.source_subject`
- `lookup_planning_consumed_specimen_view.source_phase_id`
- `lookup_planning_consumed_specimen_view.accepted_reference_variant_id`
- `lookup_planning_consumed_specimen_view.observation_binding_kind`
- `lookup_planning_consumed_specimen_view.accepted_reference_window`

The proof result is not a per-lookup operand. It is reopen-justification evidence and an admission
precondition for defining this contract at all.

### Exact locator output it would expose

The contract would expose exactly one locator output per admitted specimen:

- one deterministic receipt-bound BC specimen-file lookup source

That lookup source would minimally identify:

- `artifact_id`
- `source_raw_state_window_ref`
- one deterministic emitted specimen file path under the audited family root

### Exact invariant

The exact invariant is:

- for one admitted low-boost-recovery planning specimen, the tuple
  (`audited_family_root_directory`, `lane_ordinal`, `specimen_ordinal`, `artifact_id`,
  `source_raw_state_window_ref`) binds to exactly one deterministic BC specimen file at:
  `audited_family_root_directory/recovery_context_lane_{lane_ordinal:04}/specimen_{specimen_ordinal:04}.json`
- that bound specimen file is a receipt-bound BC lookup source only
- that bound specimen file must preserve the same `artifact_id` and
  `source_raw_state_window_ref` carried by the planning-owned specimen view

### Exact relationship to the audited family root directory

`audited_family_root_directory` remains:

- the deterministic BC specimen-tree anchor used to derive the specimen-file path

`audited_family_root_directory` does not become:

- a raw-state storage root
- a generic dataset root
- a manifest/index authority

### Exact relationship to observation-access planning

This contract stays subordinate to observation-access planning:

- it consumes the planning-owned specimen view exactly as preserved
- it does not redefine observation semantics
- it only binds the opaque `source_raw_state_window_ref` to one concrete receipt-bound lookup
  source

### What it explicitly refuses to promise

This contract explicitly refuses to promise:

- that the audited family root contains raw state
- that the emitted specimen file contains raw state
- actual raw-state materialization
- receipt-independent reopening
- sidecar/manifest or generic index semantics
- `mimir_export` integration
- tensor materialization
- control/action extraction

## H. ADMISSION RULES

A planning result plus proof result may enter this reopen-decision boundary only when all of the
following hold:

1. the inputs are exactly
   `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1` and
   `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`
2. the planning result still satisfies the exact planning-boundary admission and invariant checks
3. the proof result still satisfies the exact proof-boundary admission and invariant checks
4. `proof_disposition ==
   InsufficientForActualReceiptBoundRawStateWindowLookupRealization`
5. `exact_insufficiency_marker ==
   MissingReceiptBoundRawStateWindowLocatorContract`
6. planning and proof counts match exactly
7. planning and proof audited family root directory references match exactly
8. planning and proof lane/specimen order match exactly
9. every proof `artifact_id` matches the planning artifact id at the same lane/specimen position
10. no lower boundary is silently reopened to recreate or repair the admitted input

Admission here means only:

- the reopen question may be answered against trusted planning/proof evidence

Admission here does not mean:

- the locator contract is already implemented
- actual raw-state lookup realization is legal
- sidecar/manifest is justified
- `mimir_export` may be widened

## I. FAILURE RULES

This pass must hard-fail for:

- malformed or degraded planning input
- malformed or degraded proof input
- proof disposition drift
- proof note drift
- insufficiency-marker drift
- count drift between planning and proof
- audited family root mismatch between planning and proof
- lane/specimen order drift between planning and proof
- artifact-id drift between planning and proof
- any attempt to reinterpret the audited family root as a raw-state storage root
- any attempt to widen this pass into sidecars, manifests, generic indexing, or `mimir_export`
- any attempt to reopen lower boundaries to repair the admitted inputs

This pass produces `reopen justified` only when:

- the planning input is fully admitted
- the proof input is fully admitted
- the exact insufficiency marker is the missing locator contract
- deterministic specimen-file path derivation from the audited family root remains available
- the missing fix can stay family-specific, receipt-bound, sidecar-free, manifest-free, index-free,
  and `mimir_export`-free

There is no `no reopen` output in v1.

That is deliberate. For valid admitted input, the current repo-local evidence is already enough to
justify one narrow reopen. Anything weaker would either contradict the existing proof result or
silently broaden the defect into a different boundary.

## J. NON-GOALS

This pass does not do any of the following:

- no actual raw-state lookup realization
- no raw-state locator/index implementation
- no `mimir_export` integration
- no generic manifest/index framework
- no sidecar/manifest realization
- no tensor materialization
- no control/action extraction
- no usefulness proof
- no policy-improvement proof
- no replay parsing
- no replay ingestion
- no rollout or physics work
- no async/background system
- no database work

## K. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- the reopen decision is explicit and auditable
- the decision stays low-boost-recovery-specific
- the decision stays receipt-bound
- the narrowest honest next contract shape is fixed:
  `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`
- sidecars, manifests, generic indexing, and `mimir_export` remain outside the admitted fix

### What remains deferred

This pass still does not guarantee:

- the contract is implemented
- actual raw-state lookup is realized
- receipt-independent reopening exists
- raw state is materialized
- tensors or controls exist

### Immediate next-stage implication

The immediate next pass should be:

- one first narrow contract-definition pass for
  `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`
- still above `LowBoostRecoveryBcRawStateWindowLookupObservationAccessPlanningResultV1`
- still informed by `LowBoostRecoveryBcRawStateWindowLookupRealizationProofResultV1`
- still without actual raw-state lookup realization
- still without `mimir_export` widening unless that separate boundary is explicitly reopened
