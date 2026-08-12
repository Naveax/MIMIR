# MIMIR Skill Forge BC Export Integration / Consumer Wiring Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first actual low-boost-recovery BC export-integration / consumer-wiring
boundary on top of the already-persisted BC artifact.

It defines:

- one narrow repo-local consumer handoff boundary
- one exact admission rule for when a persisted low-boost-recovery BC artifact may cross that
  boundary
- one exact failure rule for wrong-kind, schema-drift, or malformed artifact content
- one tiny family-specific handoff surface, only because a concrete consumer path now exists

### Why it exists

The prior BC serialization/export pass fixed how a low-boost-recovery BC specimen is persisted:

- artifact identity
- observation-window serialization
- target-lineage serialization
- carried confidence
- carried unresolved assumptions

That still did not prove the persisted artifact could be consumed anywhere inside the repo without
reaching back into BC rows, accepted shells, or `mimir_export`.

This pass exists to prove one concrete repo-local path:

- load one persisted low-boost-recovery BC artifact
- validate that it still satisfies the persisted artifact boundary
- hand it off through one bounded family-specific consumer surface

### How it differs from adjacent stages

- Persisted artifact definition owns how an aligned BC row plus accepted shell becomes one stored
  specimen.
- This pass owns how that stored specimen is admitted into one repo-local consumer handoff.
- Later work may define batching/orchestration for this family or deliberately revisit
  `mimir_export`, but this pass does not.

This pass is not artifact definition, not batch export orchestration, and not `mimir_export`
integration.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this contract version.

This integration stays family-specific because:

- the persisted artifact kind is already low-boost-recovery-specific
- the only valid observation binding is low-boost-recovery-specific
- the only valid target binding is low-boost-recovery-specific
- no second BC family exists yet to justify a shared integration framework

Forcing a generic export-integration surface now would create fake universality before a second
family exists and before any real consumer needs it.

## C. INPUT BOUNDARY

This pass consumes exactly one persisted low-boost-recovery BC artifact:

- `PersistedLowBoostRecoveryBcArtifact`

Within that persisted artifact, this pass consumes:

- `header.schema_name`
- `header.schema_version`
- `payload.artifact_id`
- `payload.family`
- `payload.source_slice_id`
- `payload.source_replay`
- `payload.source_subject`
- `payload.source_raw_state_window_ref`
- `payload.source_phase_id`
- `payload.accepted_reference_variant_id`
- `payload.observation`
- `payload.target`
- `payload.carried_confidence_band`
- `payload.carried_unresolved_assumptions`
- `payload.artifact_notes`

### Boundary rule

BC rows and accepted shells are no longer direct integration input at this stage.

This pass does not:

- re-open `LowBoostRecoveryBcRowV1` admission
- re-open accepted-shell materialization
- infer specimen semantics from rows or shells

The persisted artifact boundary is the only admitted input.

## D. CHOSEN INTEGRATION POINT

The single chosen integration point is:

- a narrow repo-local BC specimen consumer handoff surface in `mimir-skill`

### Exact boundary

- input function:
  `handoff_persisted_low_boost_recovery_bc_artifact_v1(...)`
- output type:
  `LowBoostRecoveryBcArtifactConsumerHandoffV1`

### Why this integration point was chosen

This was chosen over a new `mimir-io` loading+handoff surface because `mimir-io` already has the
correct narrow ownership:

- raw artifact read/write
- schema/version validation

Adding consumer semantics there would blur a crate that currently stops at persisted artifact IO.

`mimir-skill` already owns every low-boost-recovery family boundary so far:

- canonicalization
- parameter variation
- validation
- accepted shell construction
- eval harness
- consumer planning
- BC contract definition
- BC artifact serialization

That makes `mimir-skill` the narrowest honest owner for the first family-specific consumer handoff.

## E. INTEGRATION OUTPUT / HANDOFF V1

The minimum handoff surface is `LowBoostRecoveryBcArtifactConsumerHandoffV1`.

### What comes in

- one `PersistedLowBoostRecoveryBcArtifact`

### What comes out

- one validated `LowBoostRecoveryBcArtifactConsumerHandoffV1` carrying:
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

### What is preserved

- persisted artifact identity
- source lineage
- raw-state-window linkage
- phase lineage
- accepted-reference-variant lineage
- concrete accepted supervision window
- observation-binding direction
- target-binding direction
- carried confidence
- carried unresolved assumptions

### What is intentionally not handed off

- no artifact header metadata
- no artifact note bag
- no duplicate target window field once equality with the observation window is enforced
- no replay-frame payloads
- no feature vectors
- no tensors
- no controls/actions

### What remains deferred

- loading raw state behind `source_raw_state_window_ref`
- feature materialization
- tensor materialization
- control/action target materialization
- batch export orchestration
- usefulness proof

## F. ADMISSION RULES

A persisted low-boost-recovery BC artifact may cross this handoff boundary only when all of the
following hold:

1. `header.schema_name == "mimir.low_boost_recovery_bc_artifact"`
2. `header.schema_version == 1`
3. `payload.family == low_boost_recovery`
4. `payload.artifact_id == "<accepted_reference_variant_id>:bc_artifact_v1"`
5. persisted lineage fields remain present:
   - `source_slice_id`
   - `source_replay.replay_id`
   - `source_replay.provenance_label`
   - `source_subject`
   - `source_raw_state_window_ref`
   - `accepted_reference_variant_id`
6. persisted observation boundary remains fixed:
   - `observation.binding_kind == accepted_reference_window_from_raw_state_window_ref`
   - `observation.supervision_window_role == accepted_reference_variant_window`
   - `observation.accepted_reference_window` is a valid bounded window
7. persisted target boundary remains fixed:
   - `target.binding_kind == accepted_reference_variant_control_target_deferred`
   - `target.accepted_reference_variant_id == accepted_reference_variant_id`
   - `target.accepted_reference_window == observation.accepted_reference_window`
8. `carried_confidence_band == boundary_stable`
9. `carried_unresolved_assumptions` remains the exact low-boost-recovery carried set
10. `artifact_notes` remains the exact bounded persisted-artifact note set

Admission here means only:

- this persisted specimen is structurally acceptable for one repo-local consumer handoff

Admission here does not mean:

- useful BC data
- valid controls
- correct tensors
- policy improvement

## G. FAILURE RULES

The handoff boundary fails explicitly in the following cases.

### Wrong kind / schema drift

Fail when:

- `header.schema_name` is not `mimir.low_boost_recovery_bc_artifact`
- `header.schema_version` is not `1`

This is an artifact-envelope failure, not a deferred handoff.

### Invalid content

Fail when any payload invariant above is violated, including:

- blank lineage fields
- family drift
- artifact-id drift
- observation-binding drift
- invalid observation window
- target-lineage drift
- target-window drift
- carried-confidence drift
- unresolved-assumption drift
- artifact-note drift

This is a payload failure, not a partial accept.

### Inconsistent payload behavior

If observation and target content disagree, no fallback or repair is allowed.

Specifically:

- do not pick one window arbitrarily
- do not repair `artifact_id`
- do not fill missing lineage
- do not reinterpret carried assumptions

The handoff must reject inconsistent persisted content as malformed.

## H. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic batch export framework
- no multi-family BC export integration framework
- no tensor materialization
- no action/control extraction
- no replay parsing
- no replay ingestion
- no rollout or physics work
- no async/background consumer system
- no database work
- no usefulness proof
- no policy-improvement proof

## I. RELATION TO NEXT STAGES

### What this pass now guarantees

The next pass now has one concrete repo-local path that consumes the persisted BC artifact without
reaching back into rows or shells:

- `mimir-io::read_low_boost_recovery_bc_artifact(...)`
- `mimir-skill::handoff_persisted_low_boost_recovery_bc_artifact_v1(...)`

That means the next pass no longer needs to guess:

- where the consumer boundary lives
- which persisted artifact fields must survive
- which payload invariants are required before handoff

### What still remains deferred

This pass still does not guarantee:

- family-specific batch export directories or manifests for BC artifacts
- any `mimir_export` wiring
- any tensor/control materialization
- any usefulness proof

### Immediate next-stage implication

The immediate next pass should stay narrow and family-specific:

- define the first low-boost-recovery BC consumer refinement or specimen batching step on top of
  this handoff boundary without reopening `mimir_export`

