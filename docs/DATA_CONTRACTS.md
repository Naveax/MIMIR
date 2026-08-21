# Data Contracts

## IDs

All important entities use explicit newtype wrappers:

- `ReplayId`
- `AnchorId`
- `BranchId`
- `SkillId`
- `TeacherLabelId`
- `CacheKey`

This keeps cross-crate APIs honest and avoids mixing unrelated identifiers by accident.

## Shared metadata

`Metadata` is a transparent wrapper around a deterministic `BTreeMap<String, FieldValue>`.
It is intentionally generic so the scaffold can carry externally-derived annotations without
pretending to understand Rocket League semantics that are not implemented yet.

`FieldValue` stays small on purpose. It supports:

- `text`
- `integer`
- `float` (finite values only)
- `boolean`
- `string_list`

## Internal shared DTOs

- `StateSnapshot` stores a replay/frame reference plus generic fields.
- `ReplaySliceRef` stores the bounded Skill Forge v1 replay-slice seed contract:
  explicit slice identity, source replay provenance label, frame window, subject identity,
  low-boost-recovery family hint, raw-state-window linkage, and an optional audit note.
- `LowBoostRecoveryCanonicalStateV1` stores the family-specific canonical replay-slice boundary
  for the first Skill Forge prototype: slice linkage, provenance, subject/window linkage,
  raw-state-window linkage, one explicit orientation note, bounded subject/environment envelopes,
  and a fixed list of unresolved semantic notes.
- `LowBoostRecoveryEventContactGraphV1` stores the minimum low-boost-recovery extraction surface:
  slice linkage, frame-window linkage, explicit boundary event nodes and the observed-window edge,
  plus one explicit contact-semantics status showing that contact truth is still unresolved.
- `LowBoostRecoveryPhasePlanV1` stores the bounded phase output for this pass: one deterministic
  `candidate_recovery_window` phase over the replay slice frame window. It is intentionally not a
  universal mechanics ontology.
- `LowBoostRecoveryBcRowV1` stores the first real low-boost-recovery BC contract row: lineage,
  observation/target binding direction, carried confidence, and unresolved assumptions, while
  keeping observation and target payloads reference-only.
- `LowBoostRecoveryBcSerializedArtifactV1` stores the first persisted low-boost-recovery BC
  specimen boundary: the BC row lineage plus one materialized accepted reference window for the
  serialized observation and target payloads.
- `LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1` stores the first family-specific
  emitted on-disk low-boost-recovery BC specimen contract above the deterministic filesystem
  emission plan: emitted lane/specimen ordinals plus preserved lineage, binding kinds, accepted
  reference window, carried confidence, and unresolved assumptions.
- `ActionRecord` stores a caller-provided action key plus generic fields.
- `AnchorRecord` stores an explicit anchor id, replay/frame reference, a narrow anchor kind,
  and optional metadata.
- `BranchRecord` stores an explicit branch id, its parent `AnchorId`, optional action records,
  and an optional `legality_hint` field. The hint is not authoritative validation.
- `SkillRecord` stores a stable `SkillId`, family/name strings, optional aliases, and metadata.
- `TeacherLabelRecord` stores a typed target reference, a label string, an optional finite
  score, and metadata.

## Persisted artifacts

Top-level persisted artifacts now use an explicit envelope instead of writing shared records
directly. The envelope types live in `mimir-types`:

- `ArtifactHeader`
- `ArtifactEnvelope<T>`
- `ArtifactKind`
- `ArtifactSchema`
- `AnchorArtifactPayload`
- `BranchArtifactPayload`
- `SkillArtifactPayload`
- `TeacherLabelArtifactPayload`
- `PersistedAnchorArtifact`
- `PersistedBranchArtifact`
- `PersistedSkillArtifact`
- `PersistedTeacherLabelArtifact`
- `PersistedLowBoostRecoveryBcArtifact`

`ArtifactHeader` currently includes:

- `schema_name`
- `schema_version`
- `producer`
- optional `created_by_component`
- optional `metadata`

Only persisted top-level artifacts are versioned. Internal DTOs such as `AnchorRecord`,
`BranchRecord`, `SkillRecord`, and `TeacherLabelRecord` remain plain shared payload types.

Anchor and branch now also have real producer paths built on top of the existing manual scaffold:

- `HintAnchorDetector::detect_persisted(...)` turns explicit anchor hints into
  `PersistedAnchorArtifact` values.
- `BoundedManualBranchGenerator::generate_persisted(...)` turns bounded manual proposals into
  `PersistedBranchArtifact` values.
- `mimir-export::export_anchor_artifacts(...)` and
  `mimir-export::export_branch_artifacts(...)` provide the minimal bundle export orchestration.
  Artifact payload files use deterministic ordinal paths under `anchors/` and `branches/`, for
  example `anchors/anchor-0000.json` / `anchors/anchor-0000.toml` and
  `branches/branch-0000.json` / `branches/branch-0000.toml`. JSON versus TOML is selected for the
  artifact payload files only; bundle control metadata remains JSON. `manifest.json` records the
  bundle version/name/producer, selected artifact encoding, relative `index.json` path, and
  aggregate artifact/anchor/branch counts. `index.json` records one entry per written artifact,
  including artifact kind, logical record id, relative path, schema name/version, and content
  hash. Export first writes the complete bundle into a unique staging directory, validates that
  staged bundle, and then renames the staging directory into the requested output directory. This
  reduces partially visible bundle trees after failures but is not a general multi-file
  transaction. `inspect_export_bundle(...)` reopens the manifest/index and validates bundle
  structure, relative paths, artifact existence, encoding/extension agreement, and persisted
  artifact header kind/schema metadata. `load_export_bundle(...)` builds on that inspection path,
  reads the currently supported anchor/branch artifacts in index order, and additionally validates
  each loaded artifact's logical record id and content hash against its index entry before
  returning typed values. These checks intentionally do not claim same-kind logical record-id
  uniqueness beyond what current production validation actually enforces.

`mimir-io` is intentionally narrower. It owns raw artifact read/write helpers, artifact format
selection, and schema/version validation, but not producer-coupled export orchestration.

These producer paths only wrap already-materialized shared records in versioned envelopes. They do
not add replay parsing, physics, scoring, teacher synthesis, or inferred game semantics.

The current persisted payload aliases intentionally reuse those shared DTOs:

- `AnchorArtifactPayload = AnchorRecord`
- `BranchArtifactPayload = BranchRecord`
- `SkillArtifactPayload = SkillRecord`
- `TeacherLabelArtifactPayload = TeacherLabelRecord`

That boundary is deliberate. The shared DTOs are already the exact persisted shape for these
single-record artifacts, so introducing parallel persisted-only structs would duplicate the
contract without narrowing it.

Artifact kind and schema pairing now come from one explicit source of truth:

- `ArtifactKind::Anchor` -> `ANCHOR_ARTIFACT_SCHEMA`
- `ArtifactKind::Branch` -> `BRANCH_ARTIFACT_SCHEMA`
- `ArtifactKind::Skill` -> `SKILL_ARTIFACT_SCHEMA`
- `ArtifactKind::TeacherLabel` -> `TEACHER_LABEL_ARTIFACT_SCHEMA`
- `ArtifactKind::LowBoostRecoveryBcArtifact` -> `LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA`

The schema name/version constants remain available for compatibility:

- `ANCHOR_ARTIFACT_SCHEMA_NAME` / `ANCHOR_ARTIFACT_SCHEMA_VERSION`
- `BRANCH_ARTIFACT_SCHEMA_NAME` / `BRANCH_ARTIFACT_SCHEMA_VERSION`
- `SKILL_ARTIFACT_SCHEMA_NAME` / `SKILL_ARTIFACT_SCHEMA_VERSION`
- `TEACHER_LABEL_ARTIFACT_SCHEMA_NAME` / `TEACHER_LABEL_ARTIFACT_SCHEMA_VERSION`
- `LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA_NAME` / `LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA_VERSION`

## Serialization

Important records derive `Debug`, `Clone`, `Serialize`, and `Deserialize` where appropriate.
The main shared records have focused JSON round-trip tests, reject unknown record fields, and
reject non-finite floating-point payloads in shared generic values and teacher-label scores.
Persisted artifact envelopes also reject unknown fields, round-trip deterministically through
JSON, and fail explicitly when `mimir-io` encounters an unsupported schema version.

The new replay-slice seed DTO is intentionally not a persisted artifact yet. In this pass it is
only the bounded shared contract for the first Skill Forge prototype family, not a full replay
ingestion system, parser output schema, or export bundle extension.

The new low-boost-recovery canonical/event/phase DTOs are also intentionally not persisted
artifacts yet. They are shared cross-crate contracts for the next Skill Forge solver/validator
stages, not replay-parser outputs, runtime commands, or export-bundle schema growth.

The new low-boost-recovery BC serialized artifact is intentionally narrower than a generic dataset
row. It persists only the family-specific BC specimen boundary and is not wired into
`mimir-export`.

The new low-boost-recovery BC actual filesystem emission specimen file is intentionally not a
top-level persisted artifact envelope and is intentionally not a `mimir_export` bundle entry. It
is the first family-specific emitted JSON specimen contract produced directly from
`LowBoostRecoveryBcFilesystemExportEmissionPlanResultV1`.
