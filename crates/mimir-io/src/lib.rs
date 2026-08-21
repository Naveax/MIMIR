use mimir_core::{MimirError, Result};
use mimir_score::ScoreVector;
use mimir_types::{
    ArtifactEnvelope, ArtifactHeader, ArtifactSchema, BranchId,
    LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA,
    LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1, PersistedAnchorArtifact,
    PersistedBranchArtifact, PersistedLowBoostRecoveryBcArtifact, PersistedTeacherLabelArtifact,
    PersistedVerticalSliceInputArtifact, SCOREBOARD_ARTIFACT_SCHEMA,
    VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA,
};
use serde::Deserialize;
use serde::Serialize;
use serde::de::{DeserializeOwned, IgnoredAny};
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ArtifactFormat {
    Json,
    Toml,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct PersistedScoreVector {
    pub branch_id: Option<BranchId>,
    pub components: BTreeMap<String, f64>,
    pub total: f64,
}

impl From<ScoreVector> for PersistedScoreVector {
    fn from(value: ScoreVector) -> Self {
        Self {
            branch_id: value.branch_id,
            components: value.components,
            total: value.total,
        }
    }
}

impl From<&ScoreVector> for PersistedScoreVector {
    fn from(value: &ScoreVector) -> Self {
        Self {
            branch_id: value.branch_id.clone(),
            components: value.components.clone(),
            total: value.total,
        }
    }
}

impl From<PersistedScoreVector> for ScoreVector {
    fn from(value: PersistedScoreVector) -> Self {
        Self {
            branch_id: value.branch_id,
            components: value.components,
            total: value.total,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct PersistedScoreRow {
    pub branch_id: BranchId,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub branch_label: Option<String>,
    pub simulation_id: String,
    pub simulation_backend: String,
    pub step_hashes: Vec<String>,
    pub score: PersistedScoreVector,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct PersistedScoreboard {
    pub rows: Vec<PersistedScoreRow>,
}

pub type ScoreboardArtifactPayload = PersistedScoreboard;
pub type PersistedScoreboardArtifact = ArtifactEnvelope<ScoreboardArtifactPayload>;

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct ArtifactHeaderEnvelope {
    header: ArtifactHeader,
    #[serde(rename = "payload")]
    _payload: IgnoredAny,
}

impl ArtifactFormat {
    pub fn from_path(path: impl AsRef<Path>) -> Option<Self> {
        match path.as_ref().extension().and_then(|value| value.to_str()) {
            Some("json") => Some(Self::Json),
            Some("toml") => Some(Self::Toml),
            _ => None,
        }
    }

    pub const fn extension(self) -> &'static str {
        match self {
            Self::Json => "json",
            Self::Toml => "toml",
        }
    }
}

pub fn write_artifact<T>(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &ArtifactEnvelope<T>,
) -> Result<()>
where
    T: Serialize,
{
    let path = path.as_ref();
    let text = match format {
        ArtifactFormat::Json => serde_json::to_string_pretty(artifact)?,
        ArtifactFormat::Toml => toml::to_string_pretty(artifact)?,
    };

    fs::write(path, text).map_err(|error| MimirError::io(path, error))
}

pub fn write_anchor_artifact(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &PersistedAnchorArtifact,
) -> Result<()> {
    write_artifact(path, format, artifact)
}

pub fn write_branch_artifact(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &PersistedBranchArtifact,
) -> Result<()> {
    write_artifact(path, format, artifact)
}

pub fn write_teacher_label_artifact(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &PersistedTeacherLabelArtifact,
) -> Result<()> {
    write_artifact(path, format, artifact)
}

pub fn write_scoreboard_artifact(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &PersistedScoreboardArtifact,
) -> Result<()> {
    validate_scoreboard_payload(&artifact.payload)?;
    write_artifact(path, format, artifact)
}

pub fn write_vertical_slice_input_artifact(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &PersistedVerticalSliceInputArtifact,
) -> Result<()> {
    write_artifact(path, format, artifact)
}

pub fn write_low_boost_recovery_bc_artifact(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &PersistedLowBoostRecoveryBcArtifact,
) -> Result<()> {
    write_artifact(path, format, artifact)
}

pub fn write_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(
    path: impl AsRef<Path>,
    specimen: &LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1,
) -> Result<()> {
    let path = path.as_ref();
    let text = serde_json::to_string_pretty(specimen)?;

    fs::write(path, text).map_err(|error| MimirError::io(path, error))
}

pub fn read_artifact_header(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
) -> Result<ArtifactHeader> {
    let path = path.as_ref();
    let text = fs::read_to_string(path).map_err(|error| MimirError::io(path, error))?;

    let artifact: ArtifactHeaderEnvelope = match format {
        ArtifactFormat::Json => serde_json::from_str(&text).map_err(MimirError::from),
        ArtifactFormat::Toml => toml::from_str(&text).map_err(MimirError::from),
    }?;

    Ok(artifact.header)
}

pub fn read_artifact_header_auto(path: impl AsRef<Path>) -> Result<ArtifactHeader> {
    let path = path.as_ref();
    let format = ArtifactFormat::from_path(path).ok_or_else(|| {
        MimirError::message(format!(
            "cannot infer artifact format from path {}",
            path.display()
        ))
    })?;

    read_artifact_header(path, format)
}

pub fn read_artifact<T>(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    expected_schema: ArtifactSchema,
) -> Result<ArtifactEnvelope<T>>
where
    T: DeserializeOwned,
{
    let path = path.as_ref();
    let text = fs::read_to_string(path).map_err(|error| MimirError::io(path, error))?;

    let header_envelope: ArtifactHeaderEnvelope = match format {
        ArtifactFormat::Json => serde_json::from_str(&text).map_err(MimirError::from),
        ArtifactFormat::Toml => toml::from_str(&text).map_err(MimirError::from),
    }?;
    validate_artifact_header(path, &header_envelope.header, expected_schema)?;

    let artifact: ArtifactEnvelope<T> = match format {
        ArtifactFormat::Json => serde_json::from_str(&text).map_err(MimirError::from),
        ArtifactFormat::Toml => toml::from_str(&text).map_err(MimirError::from),
    }?;

    Ok(artifact)
}

pub fn read_artifact_auto<T>(
    path: impl AsRef<Path>,
    expected_schema: ArtifactSchema,
) -> Result<ArtifactEnvelope<T>>
where
    T: DeserializeOwned,
{
    let path = path.as_ref();
    let format = ArtifactFormat::from_path(path).ok_or_else(|| {
        MimirError::message(format!(
            "cannot infer artifact format from path {}",
            path.display()
        ))
    })?;

    read_artifact(path, format, expected_schema)
}

pub fn read_teacher_label_artifact(
    path: impl AsRef<Path>,
) -> Result<PersistedTeacherLabelArtifact> {
    read_artifact_auto(path, mimir_types::ArtifactKind::TeacherLabel.schema())
}

pub fn read_scoreboard_artifact(path: impl AsRef<Path>) -> Result<PersistedScoreboardArtifact> {
    let artifact: PersistedScoreboardArtifact =
        read_artifact_auto(path, SCOREBOARD_ARTIFACT_SCHEMA)?;
    validate_scoreboard_payload(&artifact.payload)?;
    Ok(artifact)
}

fn validate_scoreboard_payload(scoreboard: &PersistedScoreboard) -> Result<()> {
    for (row_index, row) in scoreboard.rows.iter().enumerate() {
        match row.score.branch_id.as_ref() {
            Some(score_branch_id) if score_branch_id == &row.branch_id => {}
            Some(score_branch_id) => {
                return Err(MimirError::message(format!(
                    "scoreboard row {row_index} branch id mismatch: row has {}, score has {}",
                    row.branch_id, score_branch_id
                )));
            }
            None => {
                return Err(MimirError::message(format!(
                    "scoreboard row {row_index} score is missing branch id for {}",
                    row.branch_id
                )));
            }
        }
    }

    Ok(())
}

pub fn read_vertical_slice_input_artifact(
    path: impl AsRef<Path>,
) -> Result<PersistedVerticalSliceInputArtifact> {
    read_artifact_auto(path, VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA)
}

pub fn read_low_boost_recovery_bc_artifact(
    path: impl AsRef<Path>,
) -> Result<PersistedLowBoostRecoveryBcArtifact> {
    read_artifact_auto(path, LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA)
}

pub fn read_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(
    path: impl AsRef<Path>,
) -> Result<LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1> {
    let path = path.as_ref();
    let text = fs::read_to_string(path).map_err(|error| MimirError::io(path, error))?;

    serde_json::from_str(&text).map_err(Into::into)
}

pub fn scoreboard_artifact_path(root: impl AsRef<Path>) -> PathBuf {
    root.as_ref().join("scoreboard.json")
}

pub fn vertical_slice_input_artifact_path(root: impl AsRef<Path>) -> PathBuf {
    root.as_ref().join("vertical-slice-input.json")
}

fn validate_artifact_header(
    path: &Path,
    header: &ArtifactHeader,
    expected_schema: ArtifactSchema,
) -> Result<()> {
    if header.schema_name != expected_schema.name {
        return Err(MimirError::message(format!(
            "artifact schema mismatch at {}: expected {}, found {}",
            path.display(),
            expected_schema.name,
            header.schema_name
        )));
    }

    if header.schema_version != expected_schema.version {
        return Err(MimirError::message(format!(
            "unsupported schema version {} for {} at {}; supported version is {}",
            header.schema_version,
            header.schema_name,
            path.display(),
            expected_schema.version
        )));
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_types::{
        AnchorArtifactPayload, AnchorId, AnchorKind, ArtifactHeader, ArtifactKind,
        BranchArtifactPayload, BranchId, BranchOrigin, FieldValue, FrameIndex,
        LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1, LowBoostRecoveryBcArtifactId,
        LowBoostRecoveryBcArtifactNoteV1, LowBoostRecoveryBcObservationBindingKindV1,
        LowBoostRecoveryBcObservationV1, LowBoostRecoveryBcSerializedArtifactV1,
        LowBoostRecoveryBcSupervisionWindowRoleV1, LowBoostRecoveryBcTargetBindingKindV1,
        LowBoostRecoveryBcTargetV1, LowBoostRecoveryConfidenceBandV1,
        LowBoostRecoveryUnresolvedAssumptionV1, Metadata, PersistedAnchorArtifact,
        PersistedBranchArtifact, PersistedLowBoostRecoveryBcArtifact,
        PersistedTeacherLabelArtifact, PersistedVerticalSliceAnchorHint,
        PersistedVerticalSliceInput, PersistedVerticalSliceInputArtifact,
        PersistedVerticalSliceProposal, RawStateWindowRef, ReplayId, ReplaySliceFamilyHint,
        ReplaySliceId, ReplaySourceRef, ReplaySubjectRef, TeacherLabelId, TeacherLabelRecord,
        TeacherLabelTarget, TimeWindow,
    };
    use tempfile::tempdir;

    #[test]
    fn reads_and_writes_supported_json_artifacts() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("artifact.json");
        let artifact = PersistedAnchorArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Anchor, "mimir-io-tests")
                .with_created_by_component("unit-test")
                .with_metadata(Metadata::from([(
                    "suite",
                    FieldValue::Text("smoke".to_string()),
                )])),
            AnchorArtifactPayload {
                id: AnchorId::new("anchor-1"),
                replay_id: ReplayId::new("replay-1"),
                frame_index: FrameIndex::new(32),
                kind: AnchorKind::Manual,
                metadata: Metadata::from([("source", FieldValue::Text("manual".to_string()))]),
            },
        );

        write_artifact(&path, ArtifactFormat::Json, &artifact).expect("artifact should write");
        let decoded: PersistedAnchorArtifact =
            read_artifact_auto(&path, ArtifactKind::Anchor.schema()).expect("artifact should read");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn rejects_unsupported_schema_versions() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("artifact.json");
        let artifact = PersistedAnchorArtifact::new(
            ArtifactHeader::new(ArtifactKind::Anchor.schema().name, 2, "mimir-io-tests"),
            AnchorArtifactPayload {
                id: AnchorId::new("anchor-1"),
                replay_id: ReplayId::new("replay-1"),
                frame_index: FrameIndex::new(32),
                kind: AnchorKind::Manual,
                metadata: Metadata::new(),
            },
        );

        write_artifact(&path, ArtifactFormat::Json, &artifact).expect("artifact should write");

        let error =
            read_artifact_auto::<AnchorArtifactPayload>(&path, ArtifactKind::Anchor.schema())
                .expect_err("unsupported schema versions should be rejected");

        assert!(
            error
                .to_string()
                .contains("unsupported schema version 2 for mimir.anchor_artifact")
        );
    }

    #[test]
    fn rejects_wrong_artifact_kind_for_payload_boundary() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("artifact.json");
        let artifact = PersistedBranchArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Branch, "mimir-io-tests"),
            BranchArtifactPayload {
                id: BranchId::new("branch-1"),
                anchor_id: AnchorId::new("anchor-1"),
                origin: BranchOrigin::Imported,
                label: Some("seed".to_string()),
                actions: Vec::new(),
                legality_hint: None,
                metadata: Metadata::new(),
            },
        );

        write_artifact(&path, ArtifactFormat::Json, &artifact).expect("artifact should write");

        let error =
            read_artifact_auto::<BranchArtifactPayload>(&path, ArtifactKind::Anchor.schema())
                .expect_err("wrong artifact kinds should be rejected");

        assert!(
            error
                .to_string()
                .contains("expected mimir.anchor_artifact, found mimir.branch_artifact")
        );
    }

    #[test]
    fn writes_and_reads_anchor_artifact_with_wrapper() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("anchor.json");
        let artifact = PersistedAnchorArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Anchor, "mimir-io-tests")
                .with_created_by_component("unit-test"),
            AnchorArtifactPayload {
                id: AnchorId::new("anchor-1"),
                replay_id: ReplayId::new("replay-1"),
                frame_index: FrameIndex::new(12),
                kind: AnchorKind::Manual,
                metadata: Metadata::from([("source", FieldValue::Text("manual".to_string()))]),
            },
        );

        write_anchor_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let decoded: PersistedAnchorArtifact =
            read_artifact_auto(&path, ArtifactKind::Anchor.schema()).expect("artifact should read");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn writes_and_reads_branch_artifact_with_wrapper() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("branch.json");
        let artifact = PersistedBranchArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Branch, "mimir-io-tests")
                .with_created_by_component("unit-test"),
            BranchArtifactPayload {
                id: BranchId::new("anchor-1:branch:0"),
                anchor_id: AnchorId::new("anchor-1"),
                origin: BranchOrigin::Manual,
                label: Some("keep".to_string()),
                actions: vec![mimir_types::ActionRecord {
                    action_key: "jump".to_string(),
                    fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
                }],
                legality_hint: Some(true),
                metadata: Metadata::from([("source", FieldValue::Text("manual".to_string()))]),
            },
        );

        write_branch_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let decoded: PersistedBranchArtifact =
            read_artifact_auto(&path, ArtifactKind::Branch.schema()).expect("artifact should read");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn writes_and_reads_teacher_label_artifact_with_wrapper() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("teacher-label.json");
        let artifact = PersistedTeacherLabelArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::TeacherLabel, "mimir-io-tests")
                .with_created_by_component("unit-test")
                .with_metadata(Metadata::from([(
                    "teacher_namespace",
                    FieldValue::Text("stage70.teacher".to_string()),
                )])),
            TeacherLabelRecord {
                id: TeacherLabelId::new("teacher-1"),
                target: TeacherLabelTarget::Branch(BranchId::new("branch-1")),
                label: "candidate".to_string(),
                score: Some(4.25),
                metadata: Metadata::from([("teacher_rank", FieldValue::Integer(0))]),
            },
        );

        write_teacher_label_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let decoded = read_teacher_label_artifact(&path).expect("artifact should read");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn teacher_label_wrapper_rejects_schema_mismatch_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("teacher-label.json");
        let artifact = PersistedTeacherLabelArtifact::new(
            ArtifactHeader::new(
                ArtifactKind::TeacherLabel.schema().name,
                2,
                "mimir-io-tests",
            ),
            TeacherLabelRecord {
                id: TeacherLabelId::new("teacher-1"),
                target: TeacherLabelTarget::Branch(BranchId::new("branch-1")),
                label: "candidate".to_string(),
                score: Some(1.0),
                metadata: Metadata::new(),
            },
        );

        write_teacher_label_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let error = read_teacher_label_artifact(&path)
            .expect_err("unsupported schema versions should be rejected");

        assert!(
            error
                .to_string()
                .contains("unsupported schema version 2 for mimir.teacher_label_artifact")
        );
    }

    #[test]
    fn teacher_label_wrapper_rejects_wrong_artifact_kind_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("teacher-label.json");
        let artifact = PersistedBranchArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Branch, "mimir-io-tests"),
            BranchArtifactPayload {
                id: BranchId::new("branch-1"),
                anchor_id: AnchorId::new("anchor-1"),
                origin: BranchOrigin::Imported,
                label: Some("seed".to_string()),
                actions: Vec::new(),
                legality_hint: None,
                metadata: Metadata::new(),
            },
        );

        write_artifact(&path, ArtifactFormat::Json, &artifact).expect("artifact should write");

        let error = read_teacher_label_artifact(&path)
            .expect_err("wrong artifact kinds should be rejected");

        assert!(
            error
                .to_string()
                .contains("expected mimir.teacher_label_artifact, found mimir.branch_artifact")
        );
    }

    #[test]
    fn writes_and_reads_scoreboard_artifact_with_wrapper() {
        let directory = tempdir().expect("tempdir should be created");
        let path = scoreboard_artifact_path(directory.path());
        let artifact = PersistedScoreboardArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Scoreboard, "mimir-io-tests")
                .with_created_by_component("unit-test"),
            PersistedScoreboard {
                rows: vec![PersistedScoreRow {
                    branch_id: BranchId::new("anchor-1:branch:0"),
                    branch_label: Some("candidate-alpha".to_string()),
                    simulation_id: "sim-1".to_string(),
                    simulation_backend: "deterministic_fake".to_string(),
                    step_hashes: vec!["step-a".to_string(), "step-b".to_string()],
                    score: PersistedScoreVector {
                        branch_id: Some(BranchId::new("anchor-1:branch:0")),
                        components: BTreeMap::from([
                            ("coverage".to_string(), 2.0),
                            ("stability".to_string(), 1.5),
                        ]),
                        total: 3.5,
                    },
                }],
            },
        );

        write_scoreboard_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let decoded = read_scoreboard_artifact(&path).expect("artifact should read");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn scoreboard_wrapper_rejects_nested_branch_id_mismatch_before_write() {
        let directory = tempdir().expect("tempdir should be created");
        let path = scoreboard_artifact_path(directory.path());
        let artifact = PersistedScoreboardArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Scoreboard, "mimir-io-tests"),
            PersistedScoreboard {
                rows: vec![PersistedScoreRow {
                    branch_id: BranchId::new("branch-a"),
                    branch_label: None,
                    simulation_id: "sim-1".to_string(),
                    simulation_backend: "deterministic_fake".to_string(),
                    step_hashes: vec!["step-a".to_string()],
                    score: PersistedScoreVector {
                        branch_id: Some(BranchId::new("branch-b")),
                        components: BTreeMap::new(),
                        total: 0.0,
                    },
                }],
            },
        );

        let error = write_scoreboard_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect_err("mismatched nested branch identity must fail before write");

        assert!(
            error
                .to_string()
                .contains("scoreboard row 0 branch id mismatch")
        );
        assert!(!path.exists());
    }

    #[test]
    fn scoreboard_loader_rejects_missing_nested_branch_id_from_generic_write() {
        let directory = tempdir().expect("tempdir should be created");
        let path = scoreboard_artifact_path(directory.path());
        let artifact = PersistedScoreboardArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Scoreboard, "mimir-io-tests"),
            PersistedScoreboard {
                rows: vec![PersistedScoreRow {
                    branch_id: BranchId::new("branch-a"),
                    branch_label: None,
                    simulation_id: "sim-1".to_string(),
                    simulation_backend: "deterministic_fake".to_string(),
                    step_hashes: vec!["step-a".to_string()],
                    score: PersistedScoreVector {
                        branch_id: None,
                        components: BTreeMap::new(),
                        total: 0.0,
                    },
                }],
            },
        );

        write_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("generic artifact write should bypass scoreboard semantic validation");
        let error = read_scoreboard_artifact(&path)
            .expect_err("scoreboard loader must reject missing nested branch identity");

        assert!(
            error
                .to_string()
                .contains("scoreboard row 0 score is missing branch id for branch-a")
        );
    }

    #[test]
    fn scoreboard_wrapper_rejects_schema_mismatch_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = scoreboard_artifact_path(directory.path());
        let artifact = PersistedScoreboardArtifact::new(
            ArtifactHeader::new(ArtifactKind::Scoreboard.schema().name, 2, "mimir-io-tests"),
            PersistedScoreboard {
                rows: vec![PersistedScoreRow {
                    branch_id: BranchId::new("anchor-1:branch:0"),
                    branch_label: None,
                    simulation_id: "sim-1".to_string(),
                    simulation_backend: "deterministic_fake".to_string(),
                    step_hashes: vec!["step-a".to_string()],
                    score: PersistedScoreVector {
                        branch_id: Some(BranchId::new("anchor-1:branch:0")),
                        components: BTreeMap::new(),
                        total: 0.0,
                    },
                }],
            },
        );

        write_scoreboard_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let error = read_scoreboard_artifact(&path)
            .expect_err("unsupported schema versions should be rejected");

        assert!(
            error
                .to_string()
                .contains("unsupported schema version 2 for mimir.scoreboard_artifact")
        );
    }

    #[test]
    fn scoreboard_wrapper_rejects_wrong_artifact_kind_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = scoreboard_artifact_path(directory.path());
        let artifact = PersistedTeacherLabelArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::TeacherLabel, "mimir-io-tests"),
            TeacherLabelRecord {
                id: TeacherLabelId::new("teacher-1"),
                target: TeacherLabelTarget::Branch(BranchId::new("branch-1")),
                label: "candidate".to_string(),
                score: Some(1.0),
                metadata: Metadata::new(),
            },
        );

        write_artifact(&path, ArtifactFormat::Json, &artifact).expect("artifact should write");

        let error =
            read_scoreboard_artifact(&path).expect_err("wrong artifact kinds should be rejected");

        assert!(
            error
                .to_string()
                .contains("expected mimir.scoreboard_artifact, found mimir.teacher_label_artifact")
        );
    }

    #[test]
    fn writes_and_reads_vertical_slice_input_artifact_with_wrapper() {
        let directory = tempdir().expect("tempdir should be created");
        let path = vertical_slice_input_artifact_path(directory.path());
        let artifact = PersistedVerticalSliceInputArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::VerticalSliceInput, "mimir-io-tests")
                .with_created_by_component("unit-test"),
            PersistedVerticalSliceInput {
                replay_id: ReplayId::new("replay-stage69"),
                export_name: "stage69-vertical-slice".to_string(),
                teacher_namespace: "stage69.teacher".to_string(),
                simulation_seed: 69,
                anchor_hint: PersistedVerticalSliceAnchorHint {
                    anchor_id: Some(AnchorId::new("anchor-stage69")),
                    frame_index: FrameIndex::new(128),
                    kind: AnchorKind::Manual,
                    metadata: Metadata::from([(
                        "source",
                        FieldValue::Text("stage69-fixture".to_string()),
                    )]),
                },
                proposals: vec![PersistedVerticalSliceProposal {
                    label: "candidate-alpha".to_string(),
                    actions: vec![mimir_types::ActionRecord {
                        action_key: "jump".to_string(),
                        fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
                    }],
                    legal_hint: Some(true),
                    metadata: Metadata::from([(
                        "proposal_source",
                        FieldValue::Text("fixture-alpha".to_string()),
                    )]),
                    score_signals: BTreeMap::from([
                        ("coverage".to_string(), 2.0),
                        ("stability".to_string(), 3.0),
                    ]),
                }],
                scorer_weights: BTreeMap::from([
                    ("coverage".to_string(), 1.0),
                    ("stability".to_string(), 0.5),
                ]),
            },
        );

        write_vertical_slice_input_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let decoded = read_vertical_slice_input_artifact(&path).expect("artifact should read back");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn vertical_slice_input_wrapper_rejects_schema_mismatch_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = vertical_slice_input_artifact_path(directory.path());
        let artifact = PersistedVerticalSliceInputArtifact::new(
            ArtifactHeader::new(
                ArtifactKind::VerticalSliceInput.schema().name,
                2,
                "mimir-io-tests",
            ),
            PersistedVerticalSliceInput {
                replay_id: ReplayId::new("replay-stage69"),
                export_name: "stage69-vertical-slice".to_string(),
                teacher_namespace: "stage69.teacher".to_string(),
                simulation_seed: 69,
                anchor_hint: PersistedVerticalSliceAnchorHint {
                    anchor_id: Some(AnchorId::new("anchor-stage69")),
                    frame_index: FrameIndex::new(128),
                    kind: AnchorKind::Manual,
                    metadata: Metadata::new(),
                },
                proposals: Vec::new(),
                scorer_weights: BTreeMap::new(),
            },
        );

        write_vertical_slice_input_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let error = read_vertical_slice_input_artifact(&path)
            .expect_err("unsupported schema versions should be rejected");

        assert!(
            error
                .to_string()
                .contains("unsupported schema version 2 for mimir.vertical_slice_input_artifact")
        );
    }

    #[test]
    fn vertical_slice_input_wrapper_rejects_wrong_artifact_kind_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = vertical_slice_input_artifact_path(directory.path());
        let artifact = PersistedScoreboardArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Scoreboard, "mimir-io-tests"),
            PersistedScoreboard { rows: Vec::new() },
        );

        write_artifact(&path, ArtifactFormat::Json, &artifact).expect("artifact should write");

        let error = read_vertical_slice_input_artifact(&path)
            .expect_err("wrong artifact kinds should be rejected");

        assert!(error.to_string().contains(
            "expected mimir.vertical_slice_input_artifact, found mimir.scoreboard_artifact"
        ));
    }

    #[test]
    fn writes_and_reads_low_boost_recovery_bc_artifact_with_wrapper() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("low-boost-recovery-bc.json");
        let artifact = sample_low_boost_recovery_bc_artifact();

        write_low_boost_recovery_bc_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let decoded =
            read_low_boost_recovery_bc_artifact(&path).expect("artifact should read back");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn low_boost_recovery_bc_wrapper_rejects_schema_mismatch_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("low-boost-recovery-bc.json");
        let artifact = PersistedLowBoostRecoveryBcArtifact::new(
            ArtifactHeader::new(
                ArtifactKind::LowBoostRecoveryBcArtifact.schema().name,
                2,
                "mimir-io-tests",
            ),
            sample_low_boost_recovery_bc_artifact().payload,
        );

        write_low_boost_recovery_bc_artifact(&path, ArtifactFormat::Json, &artifact)
            .expect("artifact should write");

        let error = read_low_boost_recovery_bc_artifact(&path)
            .expect_err("unsupported schema versions should be rejected");

        assert!(
            error
                .to_string()
                .contains("unsupported schema version 2 for mimir.low_boost_recovery_bc_artifact")
        );
    }

    #[test]
    fn low_boost_recovery_bc_wrapper_rejects_wrong_artifact_kind_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("low-boost-recovery-bc.json");
        let artifact = PersistedTeacherLabelArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::TeacherLabel, "mimir-io-tests"),
            TeacherLabelRecord {
                id: TeacherLabelId::new("teacher-1"),
                target: TeacherLabelTarget::Branch(BranchId::new("branch-1")),
                label: "candidate".to_string(),
                score: Some(1.0),
                metadata: Metadata::new(),
            },
        );

        write_artifact(&path, ArtifactFormat::Json, &artifact).expect("artifact should write");

        let error = read_low_boost_recovery_bc_artifact(&path)
            .expect_err("wrong artifact kinds should be rejected");

        assert!(error.to_string().contains(
            "expected mimir.low_boost_recovery_bc_artifact, found mimir.teacher_label_artifact"
        ));
    }

    #[test]
    fn writes_and_reads_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("specimen.json");
        let specimen = LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1 {
            lane_ordinal: 0,
            specimen_ordinal: 1,
            artifact_id: LowBoostRecoveryBcArtifactId::new(
                "slice-1:candidate_recovery_window:trim_start_1:bc_artifact_v1",
            ),
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            source_subject: ReplaySubjectRef::new("player:blue:0"),
            source_raw_state_window_ref: RawStateWindowRef::new("window-1"),
            source_phase_id: 0,
            accepted_reference_variant_id: "slice-1:candidate_recovery_window:trim_start_1"
                .into(),
            observation_binding_kind:
                LowBoostRecoveryBcObservationBindingKindV1::AcceptedReferenceWindowFromRawStateWindowRef,
            supervision_window_role:
                LowBoostRecoveryBcSupervisionWindowRoleV1::AcceptedReferenceVariantWindow,
            accepted_reference_window: TimeWindow {
                start: FrameIndex::new(121),
                end_exclusive: FrameIndex::new(180),
            },
            target_binding_kind:
                LowBoostRecoveryBcTargetBindingKindV1::AcceptedReferenceVariantControlTargetDeferred,
            carried_confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
            carried_unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
        };

        write_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(&path, &specimen)
            .expect("emitted specimen file should write");
        let decoded = read_low_boost_recovery_bc_actual_filesystem_emission_specimen_file_v1(&path)
            .expect("emitted specimen file should read");

        assert_eq!(decoded, specimen);
    }

    fn sample_low_boost_recovery_bc_artifact() -> PersistedLowBoostRecoveryBcArtifact {
        PersistedLowBoostRecoveryBcArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::LowBoostRecoveryBcArtifact, "mimir-io-tests")
                .with_created_by_component("unit-test"),
            LowBoostRecoveryBcSerializedArtifactV1 {
                artifact_id: LowBoostRecoveryBcArtifactId::new(
                    "slice-1:candidate_recovery_window:exact:bc_artifact_v1",
                ),
                family: ReplaySliceFamilyHint::LowBoostRecovery,
                source_slice_id: ReplaySliceId::new("slice-1"),
                source_replay: ReplaySourceRef {
                    replay_id: ReplayId::new("replay-1"),
                    provenance_label: "manual.replay".to_string(),
                },
                source_subject: ReplaySubjectRef::new("player:blue:0"),
                source_raw_state_window_ref: RawStateWindowRef::new("window-1"),
                source_phase_id: 0,
                accepted_reference_variant_id: "slice-1:candidate_recovery_window:exact".into(),
                observation: LowBoostRecoveryBcObservationV1 {
                    binding_kind:
                        LowBoostRecoveryBcObservationBindingKindV1::AcceptedReferenceWindowFromRawStateWindowRef,
                    supervision_window_role:
                        LowBoostRecoveryBcSupervisionWindowRoleV1::AcceptedReferenceVariantWindow,
                    accepted_reference_window: TimeWindow {
                        start: FrameIndex::new(120),
                        end_exclusive: FrameIndex::new(180),
                    },
                },
                target: LowBoostRecoveryBcTargetV1 {
                    binding_kind:
                        LowBoostRecoveryBcTargetBindingKindV1::AcceptedReferenceVariantControlTargetDeferred,
                    accepted_reference_variant_id: "slice-1:candidate_recovery_window:exact".into(),
                    accepted_reference_window: TimeWindow {
                        start: FrameIndex::new(120),
                        end_exclusive: FrameIndex::new(180),
                    },
                },
                carried_confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
                carried_unresolved_assumptions: vec![
                    LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                    LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                    LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                    LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                    LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
                ],
                artifact_notes: vec![
                    LowBoostRecoveryBcArtifactNoteV1::SerializedFromBcContractRow,
                    LowBoostRecoveryBcArtifactNoteV1::AcceptedShellReferenceWindowMaterialized,
                    LowBoostRecoveryBcArtifactNoteV1::ObservationPayloadReferenceBound,
                    LowBoostRecoveryBcArtifactNoteV1::TargetPayloadControlDeferred,
                    LowBoostRecoveryBcArtifactNoteV1::ProvisionalConfidenceCarriedForward,
                    LowBoostRecoveryBcArtifactNoteV1::UnresolvedAssumptionsCarriedForward,
                    LowBoostRecoveryBcArtifactNoteV1::NotBcUsefulnessProof,
                ],
            },
        )
    }
}
