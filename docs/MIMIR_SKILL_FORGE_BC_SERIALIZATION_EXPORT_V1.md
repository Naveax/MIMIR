# MIMIR Skill Forge BC Serialization / Export Boundary v1

## A. PURPOSE

### What this pass owns

This pass owns the first real low-boost-recovery BC serialization / export boundary on top of the
already-defined BC contract row.

It defines:

- one persisted low-boost-recovery BC artifact/schema
- one concrete serialized observation payload boundary
- one concrete serialized target payload boundary
- one narrow constructor boundary from aligned BC row plus accepted shell into that artifact
- one narrow IO boundary for reading and writing that artifact

### Why it exists

The BC contract-definition pass fixed lineage and binding direction, but it intentionally stopped
before concrete persisted artifact semantics existed.

That left the repo with:

- one real `LowBoostRecoveryBcRowV1`
- one strict admission rule for when a BC row may exist
- no persisted specimen contract yet
- no concrete serialized observation payload yet
- no concrete serialized target payload yet

This pass exists so later low-boost-recovery BC export integration or consumer wiring does not have
to guess how a valid BC row becomes a real persisted specimen.

### How it differs from adjacent stages

- BC contract definition owns which lineage and binding fields a row must carry.
- This pass owns how an aligned row becomes one persisted low-boost-recovery BC specimen.
- A later pass may wire this artifact into actual export generation or a concrete consumer path.

This pass is not:

- replay parsing
- corpus ingestion
- real control extraction
- real dataset orchestration
- `mimir_export` integration

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this pass.

The serialization/export boundary stays family-specific because:

- the upstream replay slice, canonicalizer, parameter solver, validator, shell, eval, planning,
  and BC row are all low-boost-recovery-specific
- the accepted reference window semantics are currently tied to one recovery-window family only
- forcing a generic BC artifact family now would create fake universality before a second family
  exists

No generic all-family BC export framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes:

- one valid `LowBoostRecoveryBcRowV1`
- one aligned `LowBoostRecoveryCurriculumExportShellV1`

### Consumed fields from `LowBoostRecoveryBcRowV1`

- `family`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `accepted_reference_variant_id`
- `supervision_window_role`
- `observation_binding_kind`
- `target_binding_kind`
- `carried_confidence_band`
- `carried_unresolved_assumptions`
- `bc_contract_notes`

### Consumed fields from `LowBoostRecoveryCurriculumExportShellV1`

- `family`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `source_phase_window`
- `accepted_reference_variant_id`
- `accepted_reference_variant_window`
- `accepted_decision`
- `decision_reason`
- `confidence_band`
- `carried_unresolved_assumptions`
- `shell_notes`
- `consumer_hint`

### Authority rule

`LowBoostRecoveryBcRowV1` remains the contract authority for:

- specimen admission
- carried lineage
- observation binding direction
- target binding direction

The aligned accepted shell remains the authority for:

- concrete accepted reference-window materialization

That matters because the BC row is intentionally reference-only and does not inline the accepted
reference window.

## D. SERIALIZED BC ARTIFACT / SCHEMA V1

The first real persisted low-boost-recovery BC artifact is:

- artifact kind: `ArtifactKind::LowBoostRecoveryBcArtifact`
- schema name: `mimir.low_boost_recovery_bc_artifact`
- schema version: `1`
- persisted envelope type: `ArtifactEnvelope<LowBoostRecoveryBcSerializedArtifactV1>`

### Artifact identity

Artifact identity is deterministic and family-specific:

- `artifact_id = "<accepted_reference_variant_id>:bc_artifact_v1"`

That ties one persisted specimen directly to the accepted reference-variant lineage that the BC row
already fixed.

### Payload shape

`LowBoostRecoveryBcSerializedArtifactV1` contains exactly:

- `artifact_id`
- `family`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_raw_state_window_ref`
- `source_phase_id`
- `accepted_reference_variant_id`
- `observation`
- `target`
- `carried_confidence_band`
- `carried_unresolved_assumptions`
- `artifact_notes`

### Preserved lineage fields

The artifact preserves:

- slice lineage
- replay provenance lineage
- subject lineage
- raw-state-window linkage
- phase lineage
- accepted-reference-variant lineage

### Preserved carried boundary fields

The artifact preserves:

- `carried_confidence_band`
- `carried_unresolved_assumptions`

### Bounded artifact notes

`artifact_notes` are fixed to:

- `serialized_from_bc_contract_row`
- `accepted_shell_reference_window_materialized`
- `observation_payload_reference_bound`
- `target_payload_control_deferred`
- `provisional_confidence_carried_forward`
- `unresolved_assumptions_carried_forward`
- `not_bc_usefulness_proof`

There is no generic metadata bag.

## E. OBSERVATION SERIALIZATION DECISION

The v1 serialized observation payload is `LowBoostRecoveryBcObservationV1`.

It contains exactly:

- `binding_kind`
- `supervision_window_role`
- `accepted_reference_window`

### What it means

This payload serializes the concrete supervision window as a bounded time window while keeping the
raw state itself out of the artifact.

The observation payload is therefore:

- concrete
- persisted
- reference-bound
- not yet feature-materialized

### What it does not contain

The observation payload does not contain:

- replay frames
- parsed state payloads
- actor-visible feature vectors
- normalization outputs
- clipping rules
- tensor layout
- generic dataset metadata

### How it is derived

It is derived from:

- `observation_binding_kind` from the BC row
- `supervision_window_role` from the BC row
- `accepted_reference_variant_window` from the aligned accepted shell

### Auditable linkage rule

Observation materialization stays auditable because:

- the artifact preserves `source_raw_state_window_ref`
- the artifact preserves `accepted_reference_variant_id`
- the observation payload preserves `accepted_reference_window`
- the accepted shell remains the contract-bound source of that window

## F. TARGET SERIALIZATION DECISION

The v1 serialized target payload is `LowBoostRecoveryBcTargetV1`.

It contains exactly:

- `binding_kind`
- `accepted_reference_variant_id`
- `accepted_reference_window`

### What it means

The target payload serializes the concrete accepted-reference target boundary as:

- the accepted reference-variant lineage
- the accepted supervision window
- the explicit statement that control-target materialization remains deferred

### What it does not contain

The target payload does not contain:

- action labels
- discrete controls
- control records
- logits
- rollout-implied targets
- usefulness scores

### How it is derived

It is derived from:

- `target_binding_kind` from the BC row
- `accepted_reference_variant_id` from the BC row
- `accepted_reference_variant_window` from the aligned accepted shell

### What remains deferred

Even after this pass, the following remain deferred:

- real control extraction
- action serialization format
- observation/target numeric tensors
- any proof that the target is useful for BC

## G. PERSISTENCE / IO BOUNDARY

### Artifact kind and version naming

This artifact uses:

- `ArtifactKind::LowBoostRecoveryBcArtifact`
- `mimir.low_boost_recovery_bc_artifact`
- version `1`

### IO ownership

The artifact belongs under existing narrow IO wrappers only.

This pass adds:

- `write_low_boost_recovery_bc_artifact(...)`
- `read_low_boost_recovery_bc_artifact(...)`

in `mimir-io`.

### Load/save behavior

- writes use the existing `ArtifactEnvelope<T>` plus `ArtifactHeader`
- reads must validate the expected schema name and schema version before deserializing payload
- the wrapper is artifact-family-specific and does not become a batch export framework

### Failure behavior

Load must fail explicitly when:

- schema name is wrong
- schema version is unsupported
- content violates `serde(deny_unknown_fields)`
- payload contents are otherwise invalid JSON/TOML for this exact artifact

This pass does not add `mimir_export` integration.

## H. ADMISSION RULES

A serialized low-boost-recovery BC artifact may be created only when all of the following hold:

1. the input is already a valid `LowBoostRecoveryBcRowV1`
2. the accepted shell still satisfies the accepted low-boost-recovery shell boundary
3. row and shell align for:
   - `family`
   - `source_slice_id`
   - `source_replay`
   - `source_subject`
   - `source_raw_state_window_ref`
   - `source_phase_id`
   - `accepted_reference_variant_id`
   - `carried_confidence_band`
   - `carried_unresolved_assumptions`

### Strict consequences

- no artifact may be created directly from planning results
- no artifact may be created directly from shell output
- no artifact may be created by bypassing the BC row
- readiness or serialization does not imply usefulness

## I. NON-GOALS

This pass does not do any of the following:

- no `mimir_export` integration
- no generic BC export framework
- no generic dataset framework
- no DAgger export
- no PPO auxiliary export
- no runtime bridge
- no replay parsing
- no replay mining/search
- no rollout or physics truth upgrade
- no observation tensor implementation
- no target-action implementation
- no usefulness proof
- no policy-improvement proof

## J. RELATION TO NEXT STAGES

### What this pass now guarantees

The next low-boost-recovery BC export integration or consumer-wiring pass now has:

- one persisted BC specimen schema
- one deterministic artifact identity rule
- one concrete serialized observation boundary
- one concrete serialized target boundary
- one narrow constructor boundary
- one narrow IO boundary

### What this pass does not guarantee yet

This pass still does not guarantee:

- actual export-batch integration
- `mimir_export` compatibility
- feature tensor materialization
- control target materialization
- replay truth
- low-boost truth
- contact truth
- recovery-success truth
- BC usefulness
