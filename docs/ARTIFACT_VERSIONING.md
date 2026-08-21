# Artifact Versioning

## Why this exists

The workspace now uses strict shared contracts with `serde(deny_unknown_fields)`. That keeps
serialized data honest, but it also means additive persisted fields are not automatically
forward-compatible. Explicit artifact versioning makes those compatibility boundaries visible
before future schema changes land.

## What is versioned

Only top-level persisted artifacts are versioned.

- `ArtifactKind`
- `ArtifactSchema`
- `PersistedAnchorArtifact`
- `PersistedBranchArtifact`
- `PersistedSkillArtifact`
- `PersistedTeacherLabelArtifact`
- `PersistedLowBoostRecoveryBcArtifact`

Each persisted artifact is an `ArtifactEnvelope<T>` with an `ArtifactHeader` and a typed
payload. The header carries:

- `schema_name`
- `schema_version`
- `producer`
- optional `created_by_component`
- optional `metadata`

`ArtifactKind` maps each artifact family to exactly one schema name/version pair. `mimir-io`
now validates persisted artifacts against that paired schema descriptor instead of separate loose
string/version inputs.

Anchor and branch now have the first real persisted producer paths in the workspace:

- `HintAnchorDetector::detect_persisted(...)`
- `BoundedManualBranchGenerator::generate_persisted(...)`

Both paths stamp `ArtifactHeader::for_kind(...)` with the artifact family schema and an explicit
`created_by_component`, while keeping payload contents limited to the already-existing manual/hint
scaffold outputs.

## Internal DTOs vs persisted payloads

Shared DTOs such as `AnchorRecord`, `BranchRecord`, `SkillRecord`, and `TeacherLabelRecord`
stay unwrapped in internal APIs.

The current persisted payload aliases intentionally reuse those DTOs:

- `AnchorArtifactPayload = AnchorRecord`
- `BranchArtifactPayload = BranchRecord`
- `SkillArtifactPayload = SkillRecord`
- `TeacherLabelArtifactPayload = TeacherLabelRecord`

The low-boost-recovery BC artifact is different on purpose:

- `LowBoostRecoveryBcArtifactPayload = LowBoostRecoveryBcSerializedArtifactV1`

That persisted payload is not reused from an internal row DTO because the BC contract row is
intentionally reference-only and does not yet contain the materialized accepted reference window
needed by the persisted serialization boundary.

That boundary is deliberate. These artifacts currently persist exactly one top-level record each,
and the shared DTOs are already the full on-disk contract, so separate persisted-only structs
would duplicate the schema without narrowing it.

## Failure behavior

`mimir-io` reads and writes persisted artifact envelopes, checks the expected `schema_name`, and
requires an explicitly supported `schema_version`.

The first low-boost-recovery BC serialization boundary follows that same rule through the narrow
family-specific wrappers:

- `write_low_boost_recovery_bc_artifact(...)`
- `read_low_boost_recovery_bc_artifact(...)`

The later low-boost-recovery actual filesystem emission boundary is deliberately different:

- `write_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(...)`
- `read_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(...)`

Those helpers read and write one family-specific emitted JSON specimen file contract,
`LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1`, directly. They do not use an
`ArtifactEnvelope`, do not define a new `ArtifactKind`, and do not widen `mimir_export`.

Those wrappers validate only the raw persisted artifact boundary. They do not perform batch export
or widen `mimir_export`.

Batch export orchestration is now separate: `mimir-export` owns the deterministic
`detect/generate -> filename -> write` path for persisted anchor and branch artifacts, while
`mimir-io` stays limited to raw artifact serialization and schema/version validation.

Those export bundles emit JSON `manifest.json` and JSON `index.json` metadata alongside the
`anchors/` and `branches/` artifact directories. Artifact payload encoding may be JSON or TOML;
the bundle manifest and index remain JSON. The manifest has its own `manifest_version`, records
the selected artifact encoding and count fields, and points to the relative index path. The index
owns the per-artifact record id, relative path, artifact kind, schema name/version, and content
hash. Both remain export-orchestration contracts owned by `mimir-export` rather than new
`ArtifactKind` values. The bundle writer stages artifacts, the index, and the manifest in a
temporary subdirectory before renaming the staged directory into place, which reduces partial
visible output after write failures but still does not provide a true multi-file transaction.
`mimir-export::inspect_export_bundle(...)` can re-open one of those bundle directories and verify
that every indexed file exists, reads as a supported persisted artifact, and still matches the
index/header metadata and recorded content hash.

If the version is unsupported, reading fails immediately with an explicit error.

There is no migration layer yet. New persisted versions should be added deliberately alongside
the code that knows how to read them.
