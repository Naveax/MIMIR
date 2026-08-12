# MIMIR Skill Forge BC Emitted-Output Refinement / Sidecar-Manifest Decision v1

## A. PURPOSE

### What this pass owns

This pass owns one bounded low-boost-recovery-specific decision boundary above
`LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`.

It answers only one question:

- should audited emitted low-boost-recovery output remain strictly receipt-bound after
  emitted-output audit/readback
- or is one narrow family-specific sidecar/manifest contract justified now

This pass may add a family-specific sidecar/manifest contract only if the current audited boundary
cannot already provide the exact deterministic input needed by the immediate next family-specific
downstream step.

### Why it exists

The emitted-output audit/readback pass already fixed:

- strict admission from `LowBoostRecoveryBcActualFilesystemEmissionReceiptV1`
- emitted root/lane/specimen existence verification
- family-specific specimen readback through `mimir-io`
- lane/specimen order verification against the receipt boundary
- hard failure on malformed receipt, missing output, invalid emitted JSON, or readback mismatch

That still left one unresolved question:

- whether the first audited emitted-output boundary already carries enough deterministic
  family-specific truth for the next pass, or whether a family-specific sidecar/manifest must be
  introduced immediately above it

This pass exists to answer that question without reopening lower boundaries and without widening
into `mimir_export`, generic manifest/index orchestration, tensor materialization, or control
materialization.

### How it differs from adjacent stages

- Emitted-output audit/readback proves that receipt-referenced output exists and still reads back
  honestly.
- This pass decides whether that audited result is already sufficient as the next input boundary.
- Later broader export work, if explicitly reopened, would be separate and must not be smuggled in
  here.

This pass is not:

- emitted-output audit/readback
- actual filesystem emission
- `mimir_export` integration
- generic manifest/index orchestration
- tensor materialization
- control/action extraction

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

Emitted-output refinement or sidecar/manifest semantics remain family-specific because:

- the admitted input is one low-boost-recovery-specific audited result only
- the audited specimen payload is one low-boost-recovery-specific emitted JSON contract only:
  `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`
- the preserved ordering and lineage semantics are low-boost-recovery BC semantics, not generic
  dataset semantics
- no second emitted BC family exists yet to justify shared sidecar/manifest machinery

No generic all-family emitted-output refinement or manifest framework is introduced here.

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
- downstream consumer results
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

## D. DECISION QUESTION

The exact decision in this pass is:

- should low-boost-recovery emitted output remain strictly receipt-bound after
  `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
- or is one narrow family-specific sidecar/manifest contract justified now

### Decision criteria

One narrow family-specific sidecar/manifest is justified only if all of the following are true:

1. the immediate next low-boost-recovery-specific downstream step requires deterministic
   receipt-independent reopening from the emitted family root alone
2. that required reopen information is not already preserved in
   `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
3. the missing information can be expressed without reopening lower boundaries
4. the added contract would remain family-specific and deterministic
5. the added contract would not widen into `mimir_export`, generic manifest/index semantics,
   tensors, controls, or speculative metadata

### Decision taken in v1

The decision taken in this pass is:

- remain strictly receipt-bound after emitted-output audit/readback
- no sidecar/manifest is justified now

### Why the answer is no in v1

`LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1` already preserves, in bounded form:

- the audited family root directory
- verified lane directories and specimen file paths
- lane/specimen order
- counts
- artifact ids
- read-back specimen payloads
- explicit proof that read-back specimen payloads still match the emitted contract

No immediate next-step requirement exists yet that needs more than that. A new sidecar/manifest at
this point would only duplicate audited path/order/specimen identity data or mirror existing
read-back specimen content, which would widen the surface without adding a new proven invariant.

## E. IF NO SIDECAR / MANIFEST IS JUSTIFIED

The exact no-change decision is:

- the family remains strictly receipt-bound through
  `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
- no root-level sidecar file is added
- no lane-level sidecar file is added
- no manifest file is added
- no new Rust surface is added

### What remains sufficient in the current audited boundary

The following remain sufficient for the immediate next pass:

- audited family root path
- verified lane/specimen path set
- deterministic lane/specimen order
- artifact identity alignment
- read-back specimen payloads already validated against the emitted contract

### What remains deferred

This no-change decision defers:

- receipt-independent reopening from the family root alone
- any family-specific root manifest
- any family-specific lane manifest
- any generic manifest/index framework
- any `mimir_export` coupling
- any tensor/control materialization

### What the next pass should focus on

The next pass should be one continued receipt-bound low-boost-recovery-specific downstream step
that consumes `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1` directly and proves whether
that audited result is already sufficient for the first real downstream family-specific consumer.

If that downstream step exposes a concrete insufficiency that cannot be solved without deterministic
receipt-independent reopening, only then may a separate family-specific sidecar/manifest realization
pass be reopened.

## F. IF A SIDECAR / MANIFEST IS JUSTIFIED

If a later pass proves that receipt-independent reopening is required, the narrowest acceptable
family-specific contract would be:

- one root-level file under the emitted family root:
  - `low_boost_recovery_bc_audit_manifest_v1.json`

### Narrowest acceptable hypothetical contents

That hypothetical root-level manifest would contain only:

- `family_root_directory_basename`
- `group_count`
- `specimen_count`
- ordered `lanes`
- for each lane:
  - `lane_ordinal`
  - `relative_lane_directory`
  - ordered `specimens`
- for each specimen:
  - `specimen_ordinal`
  - `artifact_id`
  - `relative_specimen_file_path`

### What that hypothetical manifest would not contain

It would not contain:

- read-back specimen payload copies
- lower planning artifacts or receipt reconstruction inputs
- generic schema/kind metadata copied from `mimir_export`
- tensor/control materialization
- replay parsing output
- rollout/physics output
- speculative metadata bags

### Hypothetical placement rule

If such a manifest is ever justified, it must live at:

- `<emitted_family_root_directory>/low_boost_recovery_bc_audit_manifest_v1.json`

No lane-level manifest and no second index file would be allowed in that first realization.

This hypothetical contract is defined here only to bound future widening. It is not justified and
is not implemented in v1.

## G. ADMISSION RULES

An audited emitted-output result may enter this decision boundary only when all of the following
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
10. every `lane_directory_exists == true`
11. every `ordered_specimen_results` vector is non-empty
12. every `specimen_ordinal` matches the concrete specimen position
13. every `specimen_file_exists == true`
14. every `readback_matches_receipt_contract == true`
15. every `artifact_id` remains present and unique across the full audited result
16. lane/specimen order remains exactly the audited order already proven by the input result
17. no lower boundary is silently reopened to recreate or repair the input

Admission here means only:

- this audited low-boost-recovery emitted-output result may be evaluated for no-change versus one
  family-specific sidecar/manifest decision

Admission here does not mean:

- sidecar/manifest is automatically justified
- `mimir_export` may be widened
- tensors or controls may be materialized

## H. FAILURE RULES

This pass must hard-fail for:

- malformed or degraded audit/readback result input
- wrong audit disposition
- wrong audit note set
- missing or invalid audited family root directory
- count drift inside the audited result
- lane/specimen order drift inside the audited result
- duplicate or missing audited `artifact_id`
- any `lane_directory_exists == false`
- any `specimen_file_exists == false`
- any `readback_matches_receipt_contract == false`
- any attempt to reopen lower boundaries to repair the audited result

This pass must conclude `no sidecar/manifest justified` only when:

- the audited input is fully admitted
- the current audited boundary already preserves all information needed by the immediate next
  family-specific downstream step
- a new sidecar/manifest would only duplicate already-audited information

### Failure behavior

- no repair is allowed
- no receipt regeneration is allowed
- no inferred generic manifest/index is allowed
- no partial sidecar is allowed
- no speculative metadata bag is allowed

Hard failure means the input boundary is untrustworthy.

`No sidecar/manifest justified` means the input boundary is trustworthy and already sufficient.

## I. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic manifest/index framework
- no generic multi-family emitted-output refinement framework
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

- the emitted-output audit/readback result remains the only admitted boundary above actual
  filesystem emission
- no family-specific sidecar/manifest has been added without a demonstrated need
- the current next step must remain receipt-bound and family-specific
- `mimir_export` remains untouched and still out of scope

### What remains deferred

This pass still does not guarantee:

- receipt-independent reopening from the emitted family root alone
- sidecar/manifest realization
- generic export/index orchestration
- `mimir_export` wiring
- tensor/control materialization

### Immediate next-stage implication

The immediate next pass should be:

- one continued receipt-bound low-boost-recovery-specific downstream step above
  `LowBoostRecoveryBcEmittedOutputAuditReadbackResultV1`
- still without sidecar/manifest realization
- still without `mimir_export` widening unless that separate decision is explicitly reopened
