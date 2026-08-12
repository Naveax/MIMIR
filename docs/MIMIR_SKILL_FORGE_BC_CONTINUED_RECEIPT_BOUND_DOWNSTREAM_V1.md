# MIMIR Skill Forge BC Continued Receipt-Bound Downstream v1

## A. PURPOSE

### What this pass owns

This pass owns the first continued low-boost-recovery-specific downstream boundary above
`LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`.

It defines:

- one exact receipt-bound input boundary above the emitted-output audit/readback result
- one exact first downstream role that is allowed to consume the audited result directly
- one minimal family-specific continued downstream result surface
- one strict admission rule for when an audited emitted-output result may enter this boundary
- one strict failure rule for degraded, drifted, or manually-constructed audited results

### Why it exists

The emitted-output audit/readback pass already proved:

- the emitted family root, lane directories, and specimen files exist where the receipt says
- every emitted specimen JSON file can be re-opened through the family-specific readback helper
- the emitted specimen payloads still satisfy the emitted contract
- lane/specimen order and artifact identity still align with the emitted receipt

The sidecar/manifest decision pass already proved:

- the system must remain strictly receipt-bound above
  `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
- no low-boost-recovery sidecar or manifest contract is justified in this pass

That still left one unresolved question:

- what the first real downstream family-specific consumer is allowed to inspect from the audited
  result, and what exact audited state it must preserve without widening into sidecars,
  manifests, tensors, controls, or `mimir_export`

This pass exists to answer that question narrowly and explicitly.

### How it differs from adjacent stages

- Emitted-output audit/readback proves that the emitted filesystem output still reads back
  honestly.
- The sidecar/manifest decision proves that the family must remain receipt-bound for now.
- This pass defines the first downstream family-specific consumer boundary that is allowed to rely
  on that audited result directly.

This pass is not:

- emitted-output audit/readback
- sidecar/manifest realization
- `mimir_export` integration
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This continued downstream step remains family-specific because:

- the admitted input is one low-boost-recovery-specific audited emitted-output result only
- the preserved specimen payload is one low-boost-recovery-specific emitted specimen contract only:
  `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
- the preserved order, lineage, accepted-reference-window, confidence-band, and unresolved-note
  semantics are low-boost-recovery BC semantics, not generic dataset semantics
- no second BC family exists yet to justify shared continued downstream machinery

No generic all-family continued downstream or export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
- the already-emitted audited family root directory referenced by that result

Within `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`, this pass consumes:

- `specimen_count`
- `group_count`
- `emitted_family_root_directory`
- `family_root_directory_exists`
- ordered `ordered_lane_results`
- each `lane_ordinal`
- each `emitted_lane_directory`
- each `lane_directory_exists`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `artifact_id`
- each `emitted_specimen_file_path`
- each `specimen_file_exists`
- each `readback_matches_receipt_contract`
- each `readback_specimen`
- `audit_disposition`
- `audit_notes`

### Boundary rule

Direct input is no longer:

- actual filesystem emission receipts
- filesystem/export-emission plans
- downstream export-consumer results
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- accepted shells
- lower planning boundaries

Those lower layers are already frozen for this pass. This pass starts strictly from
`LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1` plus the audited family root directory it
references.

## D. FIRST CONTINUED RECEIPT-BOUND DOWNSTREAM ROLE

The first bounded downstream role above the audited result is:

- admit only already-audited low-boost-recovery emitted-output results
- revalidate that the audited result boundary is still intact without reopening the filesystem or
  lower planning layers
- preserve only the exact audited references and specimen payloads that the first downstream
  family-specific consumer may inspect
- return a smaller inspection-only downstream result that is still strictly receipt-bound

### What it is allowed to inspect from the audited result

The first continued downstream consumer may inspect only:

- preserved counts
- the audited family root directory reference
- source audit disposition and notes
- preserved lane order
- `lane_ordinal`
- `emitted_lane_directory`
- preserved specimen order within each lane
- `specimen_ordinal`
- `artifact_id`
- `emitted_specimen_file_path`
- the already-audited `readback_specimen` payload, limited to the emitted contract fields it
  already contains:
  - lineage ids and references
  - accepted reference variant id
  - observation binding kind
  - supervision window role
  - accepted reference window
  - target binding kind
  - carried confidence band
  - carried unresolved assumptions

### What it is not allowed to materialize yet

This pass is not allowed to materialize or infer:

- replay frames or parsed replay payloads behind references
- raw state behind `source_raw_state_window_ref`
- any sidecar or manifest file
- generic manifest/index semantics
- tensors, feature vectors, or normalization outputs
- controls, actions, or labels
- usefulness claims
- policy-improvement claims
- `mimir_export` bundle state

Its role is audited-specimen inspection and preservation only, not materialization.

## E. CONTINUED DOWNSTREAM OUTPUT V1

The minimum family-specific continued downstream result is:

- `LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1`

It contains exactly:

- `specimen_count`
- `group_count`
- `source_audit_disposition`
- `source_audit_notes`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- `downstream_disposition`
- `downstream_notes`

### Lane-level continued downstream shape

Each `preserved_ordered_lane_results` entry is:

- `LowBoostRecoveryBcContinuedReceiptBoundDownstreamLaneResultV1`

It contains exactly:

- `lane_ordinal`
- `emitted_lane_directory`
- ordered `ordered_specimen_results`

### Specimen-level continued downstream shape

Each `ordered_specimen_results` entry is:

- `LowBoostRecoveryBcContinuedReceiptBoundDownstreamSpecimenResultV1`

It contains exactly:

- `specimen_ordinal`
- `artifact_id`
- `emitted_specimen_file_path`
- `readback_specimen`

`readback_specimen` remains the already-audited
`LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`.

### Preserved counts, references, and payload access

`group_count` remains the number of ordered preserved lane results.

`specimen_count` remains the number of ordered preserved specimen results across all lanes.

Lane order is preserved through `preserved_ordered_lane_results` vector order.

Specimen order is preserved through each lane's `ordered_specimen_results` vector order.

The emitted family root directory, emitted lane directories, and emitted specimen file paths stay
visible as receipt-bound references only. This pass does not re-open them through another parser.

### Bounded continued downstream disposition

`downstream_disposition` is fixed to exactly:

- `ready_for_low_boost_recovery_audited_specimen_inspection_only`

That means only:

- the first continued downstream boundary may inspect already-audited specimen payloads and their
  receipt-bound references
- the next pass may refine that inspection boundary further without reopening sidecars or lower
  planning layers

It does not mean:

- ready for sidecar/manifest realization
- ready for `mimir_export`
- ready for tensors
- ready for controls/actions
- usefulness proved

### Bounded continued downstream notes

`downstream_notes` are fixed to exactly:

- `emitted_output_audit_boundary_preserved`
- `receipt_bound_lane_and_specimen_references_preserved`
- `audited_specimen_payload_inspection_only`
- `tensor_and_control_materialization_deferred`
- `mimir_export_integration_deferred`

There is no generic metadata bag.

## F. ADMISSION RULES

An emitted-output audit/readback result may enter this boundary only when all of the following
hold:

1. the input is `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
2. `audit_disposition == ready_for_low_boost_recovery_emitted_output_refinement_only`
3. `audit_notes` remain the exact emitted-output audit/readback note set
4. `family_root_directory_exists == true`
5. `emitted_family_root_directory` basename remains `low_boost_recovery_bc_v1`
6. `group_count > 0`
7. `specimen_count > 0`
8. `ordered_lane_results` is non-empty
9. every `lane_ordinal` matches the concrete lane position
10. every `emitted_lane_directory` remains the deterministic lane path under the audited family
    root
11. every `lane_directory_exists == true`
12. every `ordered_specimen_results` vector is non-empty
13. every `specimen_ordinal` matches the concrete specimen position
14. every `emitted_specimen_file_path` remains the deterministic specimen path under the enclosing
    lane directory
15. every `specimen_file_exists == true`
16. every `readback_matches_receipt_contract == true`
17. every `readback_specimen` still satisfies the emitted specimen contract and still matches the
    enclosing lane/specimen ordinals plus `artifact_id`
18. every `artifact_id` remains present and unique across the full audited result
19. lane/specimen order remains exactly the audited order already proven by the input result
20. no lower boundary is silently reopened to recreate or repair the audited input

Admission here means only:

- this audited low-boost-recovery emitted-output result may be converted into one smaller
  inspection-only continued downstream result

Admission here does not mean:

- sidecar/manifest is justified
- `mimir_export` may be widened
- tensors or controls may be materialized

## G. FAILURE / DEFER RULES

This boundary must hard-fail for:

- malformed or degraded audit/readback result input
- wrong audit disposition
- wrong audit note set
- missing or false audit-existence flags
- count drift inside the audited result
- lane/specimen order drift inside the audited result
- non-deterministic lane/specimen paths inside the audited result
- duplicate or missing audited `artifact_id`
- invalid or mismatched `readback_specimen` payloads
- any attempt to reopen lower boundaries to repair the audited result

This boundary may return a bounded success result only when:

- the admitted audited input is fully valid
- the exact receipt-bound references and audited specimen payloads needed by the first downstream
  consumer are preserved without widening the contract

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

This is deliberate. The emitted-output audit/readback boundary already established the only honest
uncertainty this pass is allowed to preserve, and that uncertainty already lives inside the
audited specimen payload's carried unresolved-assumption fields. This pass adds no new evidence
gate that would justify a second defer disposition.

## H. NON-GOALS

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

## I. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- the first continued downstream consumer above emitted-output audit/readback is explicit
- the system remains strictly receipt-bound above
  `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
- only audited root/lane/specimen references plus audited specimen payloads are preserved as the
  downstream-owned surface
- audit-only booleans and repair semantics are not widened into a generic downstream contract
- `mimir_export` remains untouched and still out of scope

### What remains deferred

This pass still does not guarantee:

- sidecar/manifest realization
- receipt-independent reopening from the family root alone
- generic export/index orchestration
- `mimir_export` wiring
- tensor/control materialization
- usefulness proof

### Immediate next-stage implication

The immediate next pass should be:

- one more continued receipt-bound low-boost-recovery-specific downstream refinement above
  `LowBoostRecoveryBcContinuedReceiptBoundDownstreamResultV1`
- still without sidecar/manifest realization unless that separate decision is explicitly reopened
- still without `mimir_export` widening unless that separate decision is explicitly reopened

That next pass should decide whether the preserved audited specimen payload surface is already
small enough and sufficient for the first concrete non-audit specimen-level family-specific
consumer, or whether a deliberate reopen decision is now required.
