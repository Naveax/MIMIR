# MIMIR Skill Forge BC Receipt-Bound Specimen-File-Anchored Raw-State-Window Locator Realization v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual locator-realization boundary above:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`

It realizes only:

- one anchored receipt-bound BC specimen-file locator path per admitted specimen
- the exact identity checks that keep that realized locator aligned with:
  - `artifact_id`
  - `source_raw_state_window_ref`
  - `lane_ordinal`
  - `specimen_ordinal`
  - the deterministic specimen-file path already fixed by the contract
- one bounded locator-realization result, disposition, notes, and failure surface

### Why it exists

The contract-definition boundary below this pass already fixed the deterministic relative
specimen-file path shape and preserved the receipt-bound lineage needed to audit it.

What was still missing was one actual realized locator boundary that turns that relative
specimen-file lookup source into one concrete anchored path under the audited family root without
pretending that raw state has been found, read, or materialized.

### How it differs from the locator contract-definition boundary below it

- The lower contract-definition boundary defines the admitted contract surface and preserves the
  deterministic relative specimen-file path only.
- This pass realizes that relative path into one anchored locator path under the preserved audited
  family root.
- This pass still does not verify specimen-file existence.
- This pass still does not read specimen files.
- This pass still does not materialize raw state, tensors, or controls.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this realization version.

This locator-realization boundary remains family-specific because:

- the only admitted source contract is
  `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`
- the deterministic lane/specimen naming rule is still the low-boost-recovery BC rule:
  - `recovery_context_lane_{lane_ordinal:04}`
  - `specimen_{specimen_ordinal:04}.json`
- the anchored path remains a BC specimen-tree path only, not a family-agnostic dataset locator
- no second family exists yet to justify a generic locator-realization framework

No generic all-family locator/index/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`
- the audited family root directory reference already preserved by that contract

Within `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`, this
pass consumes:

- `specimen_count`
- `group_count`
- `contract_disposition`
- `contract_notes`
- `chosen_locator_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `admitted_planning_specimen.artifact_id`
- each `admitted_planning_specimen.source_raw_state_window_ref`
- each `deterministic_lookup_source.lane_ordinal`
- each `deterministic_lookup_source.specimen_ordinal`
- each `deterministic_lookup_source.artifact_id`
- each `deterministic_lookup_source.source_raw_state_window_ref`
- each `deterministic_lookup_source.deterministic_bc_specimen_file_relative_path`

The remaining admitted planning lineage preserved in the contract
(`source_slice_id`, `source_replay`, `source_subject`, `source_phase_id`,
`accepted_reference_variant_id`, `observation_binding_kind`, `accepted_reference_window`) remains
below this boundary as contract provenance. It is not a new locator-realization operand in v1.

Direct input is no longer:

- planning results
- proof results
- reopen decisions
- first concrete specimen consumer results
- continued receipt-bound downstream results
- emitted-output audit/readback results
- actual emission receipts
- plans
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- shells
- lower planning boundaries

This pass starts strictly from the defined contract and its preserved audited family root anchor.

## D. LOCATOR-REALIZATION ROLE

This pass owns exactly one thing:

- realizing one deterministic receipt-bound BC specimen-file relative path into one anchored locator
  path under the audited family root while preserving the contract's receipt-bound identity tuple

This pass is allowed to realize:

- `audited_family_root_directory.join(deterministic_bc_specimen_file_relative_path)`
- path-only locator outputs for each admitted specimen
- invariant checks that the realized locator remains aligned with:
  - `artifact_id`
  - `source_raw_state_window_ref`
  - `lane_ordinal`
  - `specimen_ordinal`
  - the deterministic relative path rule fixed below

This pass is not allowed to realize yet:

- raw-state payload lookup
- specimen-file existence truth
- specimen-file readback
- replay parsing
- raw-state materialization
- observation materialization
- tensor materialization
- control/action extraction
- sidecar/manifest/index authority
- `mimir_export` integration

## E. REALIZED LOCATOR SHAPE V1

The realized locator type is fixed to exactly:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowRealizedLocatorV1`

For one admitted specimen, it contains exactly:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `source_raw_state_window_ref`
- `deterministic_bc_specimen_file_relative_path`
- `anchored_bc_specimen_file_path`

The per-specimen contract input consumed to build that realized locator is exactly:

- enclosing `lane_ordinal`
- enclosing `specimen_ordinal`
- `admitted_planning_specimen.artifact_id`
- `admitted_planning_specimen.source_raw_state_window_ref`
- `deterministic_lookup_source.lane_ordinal`
- `deterministic_lookup_source.specimen_ordinal`
- `deterministic_lookup_source.artifact_id`
- `deterministic_lookup_source.source_raw_state_window_ref`
- `deterministic_lookup_source.deterministic_bc_specimen_file_relative_path`
- `audited_family_root_directory`

The realized path semantics are fixed to exactly:

- `anchored_bc_specimen_file_path =
  audited_family_root_directory.join(deterministic_bc_specimen_file_relative_path)`

The deterministic relative path must remain exactly:

- `recovery_context_lane_{lane_ordinal:04}/specimen_{specimen_ordinal:04}.json`

The identity checks that must hold for one realized locator are exactly:

1. `lane_ordinal` must match the concrete lane position and the contract lookup source lane ordinal
2. `specimen_ordinal` must match the concrete specimen position and the contract lookup source
   specimen ordinal
3. `artifact_id` preserved in the realized locator must equal both:
   - `admitted_planning_specimen.artifact_id`
   - `deterministic_lookup_source.artifact_id`
4. `source_raw_state_window_ref` preserved in the realized locator must equal both:
   - `admitted_planning_specimen.source_raw_state_window_ref`
   - `deterministic_lookup_source.source_raw_state_window_ref`
5. `deterministic_bc_specimen_file_relative_path` must equal the exact deterministic lane/specimen
   rule above
6. `anchored_bc_specimen_file_path` must be derived only by joining that exact relative path under
   the preserved audited family root directory

Existence verification in v1 is:

- deferred

This realized locator is path-only. It does not promise:

- that the anchored path exists on disk
- that the specimen file can be opened
- that the specimen file contains raw state
- that raw-state windows can be materialized from the specimen file
- that replay frames have been parsed
- that tensors or controls are available

## F. LOCATOR-REALIZATION OUTPUT V1

The minimum family-specific locator-realization output is:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorRealizationResultV1`

It contains exactly:

- preserved `specimen_count`
- preserved `group_count`
- preserved `source_contract_disposition`
- preserved `source_contract_notes`
- preserved `source_chosen_locator_contract_shape`
- preserved `audited_family_root_directory`
- preserved ordered lane/specimen results
- chosen `realization_disposition`
- bounded `realization_notes`

The lane/specimen result types are:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorRealizationLaneResultV1`
- `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorRealizationSpecimenResultV1`

Each lane result contains:

- `lane_ordinal`
- ordered `ordered_specimen_results`

Each specimen result contains:

- `specimen_ordinal`
- `realized_locator`

`realization_disposition` is fixed to exactly:

- `RealizedForReceiptBoundAnchoredBcSpecimenFilePathOnly`

`realization_notes` are fixed to exactly:

- `ReceiptBoundSpecimenFileAnchoredLocatorContractBoundaryPreserved`
- `ContractInputsRevalidated`
- `AuditedFamilyRootReferencePreservedAsBcSpecimenTreeAnchor`
- `LaneAndSpecimenOrderPreserved`
- `ArtifactIdsPreserved`
- `SourceRawStateWindowRefsPreserved`
- `DeterministicRelativeSpecimenFilePathShapeRevalidated`
- `ReceiptBoundAnchoredBcSpecimenFilePathRealized`
- `SpecimenFileExistenceVerificationDeferred`
- `RawStateMaterializationDeferred`
- `SidecarManifestAndGenericIndexStillUnjustified`
- `MimirExportIntegrationStillForbidden`

## G. ADMISSION RULES

The contract-definition result may enter this realization boundary only when all of the following
hold:

1. the input is exactly
   `LowBoostRecoveryBcReceiptBoundSpecimenFileAnchoredRawStateWindowLocatorContractV1`
2. the source planning, proof, reopen, and contract dispositions still match their exact admitted
   values
3. the source planning, proof, reopen, and contract note sets still match their exact admitted
   note sets
4. `source_exact_insufficiency_marker ==
   MissingReceiptBoundRawStateWindowLocatorContract`
5. `chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
6. `contract_disposition == ContractDefinedForReceiptBoundSpecimenFileLookupSourceOnly`
7. `specimen_count > 0`
8. `group_count > 0`
9. `group_count` equals the number of preserved ordered lane results
10. the audited family root directory still ends in `low_boost_recovery_bc_v1`
11. lane order, specimen order, artifact ids, and source raw-state-window refs remain aligned
    between the admitted planning specimen view and the deterministic lookup source
12. the deterministic relative path shape still matches the exact lane/specimen naming rule
13. no lower boundary is silently reopened to repair or reinterpret the admitted contract input

Admission here means only:

- this path-only anchored locator may be realized from the trusted contract

Admission here does not mean:

- specimen files exist
- specimen files were read back
- raw-state materialization is legal
- sidecar/manifest realization is justified
- `mimir_export` may be widened

## H. FAILURE RULES

This boundary must hard-fail for:

- degraded contract input
- mismatched counts
- mismatched audited family root identity
- mismatched lane order
- mismatched specimen order
- mismatched artifact ids
- mismatched `source_raw_state_window_ref`
- invalid deterministic relative path shape
- any attempt to reinterpret the audited family root as raw-state storage
- any attempt to widen this pass into specimen-file existence/readback
- any attempt to widen this pass into raw-state materialization
- any attempt to widen this pass into sidecars, manifests, generic indexing, or `mimir_export`

Failure behavior is strict:

- no repair is allowed
- no path canonicalization is used as a substitute for contract truth
- no specimen is skipped
- no resorting is allowed
- no guessed path repair is allowed
- no partial realization result is returned

## I. NON-GOALS

This pass does not do any of the following:

- no raw-state payload materialization
- no replay parsing
- no raw-state locator/index implementation beyond the first actual receipt-bound anchored locator
- no specimen-file existence verification
- no specimen-file readback
- no `mimir_export` integration
- no sidecar/manifest realization
- no generic manifest/index framework
- no generic multi-family downstream/export framework
- no tensor materialization
- no control/action extraction
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

This pass now guarantees:

- one machine-verifiable path-only locator-realization result exists above the contract
- one admitted specimen now yields one concrete anchored receipt-bound BC specimen-file path under
  the preserved audited family root
- the realized locator remains aligned with `artifact_id`, `source_raw_state_window_ref`,
  `lane_ordinal`, and `specimen_ordinal`
- the audited family root remains only a BC specimen-tree anchor
- raw-state materialization remains deferred
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- specimen-file existence
- specimen-file readback
- raw-state lookup success
- raw-state materialization
- observation/tensor/control materialization

The immediate next pass should be:

- a first BC specimen-file existence/readback validation pass above this realized locator result

That next pass should consume the realized locator result, verify only filesystem existence and
contract-preserving readback behavior if justified, and still keep raw-state materialization
deferred.

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- reinterpret the audited family root as raw-state storage
- materialize raw state, tensors, or controls
