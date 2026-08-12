# MIMIR Skill Forge BC First Concrete Specimen Consumer v1

## A. PURPOSE

### What this pass owns

This pass owns the first concrete non-audit specimen-level consumer boundary above
`LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1`.

It defines:

- one exact specimen-level input boundary above the inspection-only continued downstream result
- one exact first concrete specimen-level consumer role
- one exact consumed-specimen-view decision
- one minimal family-specific specimen-level consumer result surface
- one strict admission rule for when a continued receipt-bound downstream result may enter
- one strict failure rule for degraded or manually-constructed downstream results

### Why it exists

The continued receipt-bound downstream boundary already fixed:

- strict input from `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
- revalidation of the admitted audit result without reopening filesystem reads
- preservation of the audited family root reference
- preservation of ordered lane/specimen references and artifact ids
- preservation of `readback_specimen` payload access
- stripping of audit-only success flags from the downstream-owned surface

That still left one unresolved question:

- whether `readback_specimen` is already the first honest consumed specimen-level view
- or whether the first concrete specimen-level consumer should narrow it further before any later
  family-specific work

This pass answers that question and fixes the first concrete consumed specimen-level surface
without widening into sidecars, manifests, `mimir_export`, tensors, or controls.

### How it differs from the boundary below it

- `LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1` is inspection-only and still
  exposes transport placement and receipt-bound file references.
- This pass converts that inspection-only surface into the first concrete specimen-level consumed
  view the next family-specific pass is allowed to rely on.
- This pass narrows the specimen payload itself instead of keeping the full emitted readback
  struct as the downstream-owned specimen contract.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This first concrete specimen-level consumer remains family-specific because:

- the admitted input is one low-boost-recovery-specific continued downstream result only
- the narrowed consumed specimen view is one low-boost-recovery-specific field set only
- the lineage, accepted-reference-window, binding-kind, confidence-band, and unresolved-assumption
  semantics remain low-boost-recovery BC semantics
- no second family exists yet to justify a shared specimen-consumer abstraction

No generic all-family downstream/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1`
- the audited family root directory reference preserved by that result

Within `LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1`, this pass consumes:

- `specimen_count`
- `group_count`
- `source_audit_disposition`
- `source_audit_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each `emitted_lane_directory`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `artifact_id`
- each `emitted_specimen_file_path`
- each `readback_specimen`
- `downstream_disposition`
- `downstream_notes`

### Boundary rule

Direct input is no longer:

- emitted-output audit/readback results
- actual filesystem emission receipts
- filesystem/export-emission plans
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- accepted shells
- lower planning boundaries

Those lower layers are frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1` plus the audited family root
directory reference it preserves.

## D. FIRST CONCRETE SPECIMEN-LEVEL CONSUMER ROLE

The first bounded non-audit specimen-level consumer role is:

- admit only already-validated low-boost-recovery continued downstream results
- revalidate the preserved continued-downstream surface without reopening filesystem reads or lower
  planning layers
- extract one smaller family-specific consumed specimen view from each admitted `readback_specimen`
- preserve only the receipt-bound root reference and ordered lane/specimen structure the next pass
  still needs

### What it is allowed to inspect

This first concrete specimen-level consumer may inspect only:

- preserved counts
- source downstream disposition and notes
- the audited family root directory reference
- preserved lane order
- preserved specimen order
- preserved artifact identity
- the already-audited `readback_specimen` payload only to derive the first concrete consumed
  specimen view
- deterministic lane/specimen path references only for admission revalidation of the lower result

### What it is not allowed to materialize

This pass is not allowed to materialize or infer:

- replay frames or parsed replay payloads
- raw state behind `source_raw_state_window_ref`
- sidecars or manifests
- generic manifest/index semantics
- tensors, feature vectors, or normalization outputs
- controls, actions, or labels
- usefulness claims
- policy-improvement claims
- `mimir_export` bundle state

Its role is consumed-specimen admission only, not materialization.

## E. SPECIMEN-LEVEL CONSUMED VIEW DECISION

The decision in v1 is:

- narrow `readback_specimen` further into a smaller family-specific consumed specimen view

The chosen consumed view is the exact low-boost-recovery field set already represented locally by:

- `LowBoostRecoveryBcArtifactConsumerHandoffV1`

### Fields actually needed now

The first concrete specimen-level consumer needs exactly:

- `artifact_id`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `accepted_reference_variant_id`
- `observation_binding_kind`
- `supervision_window_role`
- `accepted_reference_window`
- `target_binding_kind`
- `carried_confidence_band`
- `carried_unresolved_assumptions`

### Fields preserved

The consumed specimen view preserves all of the fields above exactly.

Lane/specimen order is preserved separately through:

- lane vector order
- `lane_ordinal`
- specimen vector order inside each lane
- `specimen_ordinal`

The audited family root reference is preserved separately at the top level.

### Fields intentionally dropped from the consumed view

The following `readback_specimen` fields are intentionally dropped from the consumed view:

- `lane_ordinal`
- `specimen_ordinal`

They are transport placement fields, not family-specific specimen semantics, and this pass already
preserves that placement outside the consumed view.

The following lower-boundary transport references are also intentionally dropped from the new
specimen-level output surface:

- `emitted_lane_directory`
- `emitted_specimen_file_path`

Those references remain useful for admission revalidation of the continued downstream result, but
they are not part of the first concrete consumed specimen contract.

### Why this is the narrowest honest contract now

This is the narrowest honest contract now because:

- the repo already has one exact local semantic subset with this field shape:
  `LowBoostRecoveryBcArtifactConsumerHandoffV1`
- the emitted-specimen audit validator already rebuilds that same field set from
  `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
- no current repo-local need requires carrying lane/specimen placement inside the consumed payload
  itself once order is preserved externally
- no current repo-local need requires keeping emitted lane/specimen path references in the
  specimen-level output surface

Keeping `readback_specimen` intact would preserve duplicated transport placement fields without
adding a proven specimen-level invariant.

## F. FIRST CONCRETE SPECIMEN-LEVEL CONSUMER OUTPUT V1

The minimum family-specific specimen-level consumer result is:

- `LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1`

It contains exactly:

- `specimen_count`
- `group_count`
- `source_downstream_disposition`
- `source_downstream_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- `consumer_disposition`
- `consumer_notes`

### Lane-level shape

Each `preserved_ordered_lane_results` entry is:

- `LowBoostRecoveryBcFirstConcreteSpecimenConsumerLaneResultV1`

It contains exactly:

- `lane_ordinal`
- ordered `ordered_specimen_results`

### Specimen-level shape

Each `ordered_specimen_results` entry is:

- `LowBoostRecoveryBcFirstConcreteSpecimenConsumerSpecimenResultV1`

It contains exactly:

- `specimen_ordinal`
- `consumed_specimen_view`

`consumed_specimen_view` is exactly:

- `LowBoostRecoveryBcArtifactConsumerHandoffV1`

Artifact ids are preserved through:

- `consumed_specimen_view.artifact_id`

Lane/specimen order is preserved through:

- lane vector order plus `lane_ordinal`
- specimen vector order plus `specimen_ordinal`

### Bounded disposition

`consumer_disposition` is fixed to exactly:

- `ReadyForLowBoostRecoveryConsumedSpecimenViewOnly`

That means only:

- the first concrete consumed specimen view is admitted and preserved for another
  receipt-bound low-boost-recovery-specific refinement

It does not mean:

- ready for `mimir_export`
- ready for tensors
- ready for controls/actions
- usefulness proved

### Bounded notes

`consumer_notes` are fixed to exactly:

- `ContinuedReceiptBoundDownstreamBoundaryPreserved`
- `AuditedFamilyRootReferencePreserved`
- `LaneAndSpecimenOrderPreserved`
- `ConsumedSpecimenViewNarrowedToArtifactConsumerHandoff`
- `TensorAndControlMaterializationDeferred`
- `MimirExportIntegrationDeferred`

There is no generic metadata bag.

### Concrete entry function

The concrete entry function is:

- `consume_low_boost_recovery_bc_continued_receipt_bound_downstream_for_first_concrete_specimen_consumer_v1(...)`

## G. ADMISSION RULES

A continued receipt-bound downstream result may enter this boundary only when all of the
following hold:

1. the input is `LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1`
2. `source_audit_disposition == ReadyForLowBoostRecoveryEmittedOutputRefinementOnly`
3. `source_audit_notes` remain the exact emitted-output audit/readback note set
4. `downstream_disposition == ReadyForLowBoostRecoveryAuditedSpecimenInspectionOnly`
5. `downstream_notes` remain the exact continued receipt-bound downstream note set
6. `audited_family_root_directory` basename remains `low_boost_recovery_bc_v1`
7. `group_count > 0`
8. `specimen_count > 0`
9. `preserved_ordered_lane_results` is non-empty
10. every `lane_ordinal` matches the concrete lane position
11. every `emitted_lane_directory` remains the deterministic lane path under the audited family
    root
12. every `ordered_specimen_results` vector is non-empty
13. every `specimen_ordinal` matches the concrete specimen position
14. every `artifact_id` remains present and unique across the full continued downstream result
15. every `emitted_specimen_file_path` remains the deterministic specimen path under the enclosing
    lane directory
16. every `readback_specimen` still satisfies the emitted specimen contract
17. every `readback_specimen.lane_ordinal` matches the enclosing lane result
18. every `readback_specimen.specimen_ordinal` matches the enclosing specimen result
19. every `readback_specimen.artifact_id` matches the enclosing specimen result
20. no lower boundary is silently reopened to recreate or repair the admitted input

Admission here means only:

- this continued receipt-bound low-boost-recovery result may be converted into the first concrete
  consumed specimen view

Admission here does not mean:

- sidecar/manifest realization is justified
- `mimir_export` may be widened
- tensors or controls may be materialized

## H. FAILURE / DEFER RULES

This boundary must hard-fail for:

- malformed or degraded continued downstream input
- wrong source audit disposition or note set
- wrong continued-downstream disposition or note set
- missing or drifted counts
- lane/specimen order drift
- non-deterministic lane/specimen path drift inside the admitted input
- duplicate or missing artifact ids
- invalid or mismatched `readback_specimen` payloads
- any attempt to reopen lower boundaries to repair the admitted input

This boundary may return a bounded success result only when:

- the admitted continued downstream result is fully valid
- the narrowed consumed specimen view preserves all currently needed family-specific specimen
  semantics
- no later-stage materialization is smuggled into this pass

### Failure behavior

- no repair is allowed
- no receipt regeneration is allowed
- no filesystem re-audit is allowed
- no specimen is skipped
- no resorting is allowed
- no inferred manifest/index is allowed
- no partial success result is returned

### Defer behavior

There is no soft defer path in v1.

This is deliberate. This pass adds no new evidence gate beyond the already-preserved receipt-bound
surface. Remaining uncertainty already lives inside the carried unresolved-assumption fields of the
consumed specimen view.

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
- no rollout or physics work
- no async/background system
- no database work

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- the first concrete non-audit specimen-level consumer boundary is explicit
- the system remains strictly receipt-bound above
  `LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1`
- the consumed specimen payload is now narrower than `readback_specimen`
- ordered lane/specimen placement remains preserved without keeping placement fields inside the
  consumed payload itself
- the audited family root reference remains visible
- `mimir_export` remains untouched and still out of scope

### What remains deferred

This pass still does not guarantee:

- sidecar/manifest realization
- receipt-independent reopening from the family root alone
- raw-state lookup realization from `source_raw_state_window_ref`
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- another continued receipt-bound low-boost-recovery-specific refinement above
  `LowBoostRecoveryBcFirstConcreteSpecimenConsumerResultV1`
- still without sidecar/manifest realization unless that separate decision is explicitly reopened
- still without `mimir_export` widening unless that separate decision is explicitly reopened

That next pass should test whether the new `LowBoostRecoveryBcArtifactConsumerHandoffV1`-shaped
consumed specimen view is already sufficient for the first explicit raw-state-window lookup /
observation-access planning boundary, or whether a deliberate reopen decision is now required.
