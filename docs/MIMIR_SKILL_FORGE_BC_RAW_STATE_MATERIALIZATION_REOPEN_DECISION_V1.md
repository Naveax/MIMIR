# MIMIR Skill Forge BC Raw-State Materialization Reopen Decision v1

## A. PURPOSE

### What this pass owns

This pass owns exactly one question above:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`

It defines whether the project must now deliberately reopen a raw-state materialization boundary
for the first low-boost-recovery prototype family.

This pass owns:

- one explicit reopen-decision boundary above the validated specimen-file result
- the criteria used to decide whether reopening is honest at all
- the minimum next contract shape if reopening is justified

### Why it exists

The boundary below this pass already proved all of the following for each admitted low-boost-
recovery BC specimen:

- one deterministic receipt-bound anchored specimen-file path exists
- that anchored path is a file
- the file can be deserialized through the existing repo-local helper
- the read-back specimen remains compatible with the family-specific emitted specimen contract
- the read-back specimen still matches the realized locator on:
  - `lane_ordinal`
  - `specimen_ordinal`
  - `artifact_id`
  - `source_raw_state_window_ref`

After that validation, the remaining unresolved problem is no longer specimen-file location or
readback identity. The remaining unresolved problem is whether the project must now reopen a new
boundary to turn the still-opaque `source_raw_state_window_ref` into an honest raw-state
materialization attempt.

### How it differs from the existence/readback validation boundary below it

- The lower boundary proves specimen-file truth and identity-preserving readback.
- This pass does not perform more filesystem truth checks for their own sake.
- This pass does not materialize raw state.
- This pass decides whether a raw-state materialization contract must now exist at all.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this reopen-decision version.

This pass remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
- the validated read-back specimen contract is only
  `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
- the unresolved reference being evaluated is the low-boost-recovery BC specimen field
  `source_raw_state_window_ref`
- no second family exists that would justify a generic raw-state materialization reopen framework

No generic all-family raw-state/index/export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
- the audited family root directory reference already preserved by that result

Within `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`, this pass
consumes exactly:

- `specimen_count`
- `group_count`
- `source_realization_disposition`
- `source_realization_notes`
- `source_chosen_locator_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `preserved_realized_locator.lane_ordinal`
- each `preserved_realized_locator.specimen_ordinal`
- each `preserved_realized_locator.artifact_id`
- each `preserved_realized_locator.source_raw_state_window_ref`
- each `preserved_realized_locator.deterministic_bc_specimen_file_relative_path`
- each `preserved_realized_locator.anchored_bc_specimen_file_path`
- each `specimen_file_exists`
- each `readback_matches_realized_locator_identity`
- each `readback_specimen.lane_ordinal`
- each `readback_specimen.specimen_ordinal`
- each `readback_specimen.artifact_id`
- each `readback_specimen.source_raw_state_window_ref`
- `validation_disposition`
- `validation_notes`

Direct input is no longer:

- locator-contract results
- locator-realization results
- planning results
- proof results
- reopen decisions below this layer
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

Those lower layers remain frozen. This pass starts strictly from the validated specimen-file
boundary and its preserved audited family root anchor.

## D. DECISION QUESTION

The exact question is:

- should raw-state materialization now be deliberately reopened above the validated specimen-file
  boundary?

This question exists now because the boundaries below this pass have already proved:

- deterministic locator shape
- anchored locator realization
- filesystem existence
- identity-preserving readback

Because those lower questions are already answered, the remaining missing boundary is no longer
about where the specimen file is or whether the specimen file is readable. The remaining missing
boundary is whether `source_raw_state_window_ref` may now drive one honest raw-state
materialization attempt contract.

This is still not actual materialization.

## E. REOPEN CRITERIA

Reopening is justified only if all of the following hold:

1. the admitted input remains an exact
   `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
2. the source locator-realization disposition and note set remain exact
3. the validation disposition and note set remain exact
4. the locator contract shape remains
   `ReceiptBoundSpecimenFileAnchored`
5. the audited family root remains the low-boost-recovery BC specimen-tree anchor and is not
   reinterpreted as a raw-state storage root
6. lane order, specimen order, anchored path shape, and read-back identity still remain exact
7. the remaining unresolved problem is now truly the absence of a raw-state materialization
   boundary, not another locator/readback defect
8. the next boundary can remain low-boost-recovery-specific
9. the next boundary can remain receipt-bound
10. the next boundary can avoid sidecars, manifests, and generic indexing
11. the next boundary can avoid `mimir_export`
12. the next boundary can stay below tensor/control materialization

If any of those criteria fail, this pass must not pretend that raw-state materialization is the
only remaining gap.

## F. DECISION

Decision chosen:

- reopen justified for one narrow raw-state materialization boundary

Reopening is justified because the validated specimen-file boundary already fixed the last honest
pre-materialization uncertainties that existed below it:

- the specimen-file path is no longer hypothetical
- the specimen file is no longer hypothetical
- the identity tuple carried by the specimen file is no longer hypothetical
- `source_raw_state_window_ref` is now the only remaining unresolved access boundary in this slice

The narrowest honest next boundary shape is:

- one receipt-bound, low-boost-recovery-specific raw-state materialization contract above the
  validated specimen-file boundary

That next contract would consume:

- the validated specimen-file boundary
- the explicit reopen decision from this pass

That next contract would expose:

- one family-specific materialization-attempt boundary keyed by validated specimen identity and
  `source_raw_state_window_ref`

What remains deferred even after reopening is justified:

- actual raw-state materialization
- replay parsing implementation
- tensor materialization
- control/action extraction
- `mimir_export` integration
- sidecar/manifest realization

This is the minimum honest reopen because the remaining missing boundary is not generic export
structure, not a second locator boundary, and not observation/control materialization. It is only
the contract required to attempt receipt-bound raw-state access from already validated specimen
identity.

## G. RAW-STATE MATERIALIZATION CONTRACT SHAPE V1

Because reopening is justified, the narrowest contract-only next boundary is defined here.

### Contract name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`

### Exact inputs from the validated specimen-file boundary

The next contract should consume exactly:

- `specimen_count`
- `group_count`
- `validation_disposition`
- `validation_notes`
- `source_chosen_locator_contract_shape`
- `audited_family_root_directory`
- ordered lane/specimen structure
- each validated specimen's:
  - `lane_ordinal`
  - `specimen_ordinal`
  - `preserved_realized_locator.artifact_id`
  - `preserved_realized_locator.source_raw_state_window_ref`
  - `preserved_realized_locator.anchored_bc_specimen_file_path`
  - `readback_specimen.source_slice_id`
  - `readback_specimen.source_replay`
  - `readback_specimen.source_subject`
  - `readback_specimen.source_phase_id`
  - `readback_specimen.accepted_reference_variant_id`
  - `readback_specimen.observation_binding_kind`
  - `readback_specimen.accepted_reference_window`

It should not need to consume:

- sidecar/manifest/index state
- `mimir_export` data
- replay-parser output
- tensor/control payloads

### Exact raw-state materialization output boundary it would expose

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationAttemptResultV1`

That future result should remain an attempt boundary, not a success claim.

### Exact invariant

For one admitted specimen, the next contract must bind exactly one tuple:

- validated specimen-file identity:
  - `lane_ordinal`
  - `specimen_ordinal`
  - `artifact_id`
  - `anchored_bc_specimen_file_path`
- validated opaque lookup reference:
  - `source_raw_state_window_ref`
- preserved receipt-bound lineage:
  - `source_slice_id`
  - `source_replay`
  - `source_subject`
  - `source_phase_id`

to exactly one honest raw-state materialization attempt boundary.

That invariant exists to prevent guessed remapping between validated specimen identity and future
materialization attempts.

### Exact relationship to observation-access planning

The next contract may preserve:

- `observation_binding_kind`
- `accepted_reference_window`

only as deferred observation-access lineage.

It must not reinterpret those fields into observation tensors or broader control semantics.

### What it explicitly refuses to promise

The next contract must still refuse to promise:

- that raw-state payloads already exist in accessible form
- that replay parsing has been implemented
- that raw-state lookup will succeed
- that tensors are available
- that controls are available
- that `mimir_export` may be widened
- that sidecars/manifests are required

## H. ADMISSION RULES

A validation result may enter this reopen-decision boundary only when all of the following hold:

1. the input is exactly
   `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
2. `source_realization_disposition ==
   RealizedForReceiptBoundAnchoredBcSpecimenFilePathOnly`
3. `source_realization_notes` still equal the exact realization-note set frozen below this
   boundary
4. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
5. `validation_disposition ==
   ValidatedForReceiptBoundBcSpecimenFileExistenceAndIdentityPreservingReadbackOnly`
6. `validation_notes` still equal the exact validation-note set frozen below this boundary
7. `specimen_count > 0`
8. `group_count > 0`
9. `group_count` equals the number of preserved ordered lane results
10. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
11. `audited_family_root_directory` still exists as a directory at decision time
12. lane order and specimen order still match concrete lane/specimen position
13. each preserved realized locator still matches the deterministic low-boost-recovery
    lane/specimen path rule
14. each preserved realized locator still matches the audited family root join rule
15. each specimen still preserves:
    - `specimen_file_exists == true`
    - `readback_matches_realized_locator_identity == true`
16. each read-back specimen still matches the preserved realized locator on:
    - `lane_ordinal`
    - `specimen_ordinal`
    - `artifact_id`
    - `source_raw_state_window_ref`

Admission here means only:

- this reopen decision may rely on the validated specimen-file boundary as the last trusted
  pre-materialization layer

Admission here does not mean:

- raw-state materialization has been implemented
- raw-state lookup must succeed
- tensors or controls are available

## I. FAILURE RULES

This pass must hard-fail for:

- degraded validation input
- count/order/path drift
- audited family root drift
- `specimen_file_exists == false`
- `readback_matches_realized_locator_identity == false`
- read-back identity drift
- any attempt to reinterpret the audited family root as raw-state storage
- any attempt to widen this pass into actual raw-state materialization
- any attempt to widen this pass into tensors, controls, sidecars, manifests, generic indexing, or
  `mimir_export`

This v1 pass does not emit a separate no-reopen disposition for admitted inputs.

Reason:

- once the admitted validation boundary is exact, the remaining unresolved boundary is already the
  raw-state materialization boundary

So failure behavior is:

- hard-fail on any admission violation
- otherwise emit the single reopen-justified decision defined above

## J. NON-GOALS

This pass does not do any of the following:

- no actual raw-state materialization
- no replay parsing implementation
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof

## K. RELATION TO NEXT STAGES

This pass now guarantees:

- the project has an explicit answer to whether raw-state materialization must now be reopened
- the answer is tied to the validated specimen-file boundary, not guessed from lower layers
- the minimum next contract shape is now explicit
- the audited family root still remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

This pass still does not guarantee:

- actual raw-state access
- actual raw-state-window materialization
- replay-frame access
- observation/tensor/control materialization

The immediate next pass should be:

- a first narrow contract-definition pass for
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowMaterializationContractV1`

That next pass should consume:

- `LowBoostRecoveryBcReceiptBoundSpecimenFileExistenceReadbackValidationResultV1`
- the explicit reopen decision produced here

That next pass must still not:

- widen `mimir_export` unless explicitly reopened
- implement raw-state materialization
- reopen tensor/control materialization
- add sidecars/manifests unless separately proven necessary
