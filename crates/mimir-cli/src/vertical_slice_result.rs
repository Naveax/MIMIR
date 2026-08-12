use crate::vertical_slice::{VERTICAL_SLICE_EXPORT_DIR_NAME, VERTICAL_SLICE_TEACHER_DIR_NAME};
use mimir_core::{MimirError, Result};
use mimir_export::{ConsumerExport, adapt_loaded_export_for_consumer, load_export_bundle};
use mimir_io::{
    PersistedScoreboardArtifact, read_scoreboard_artifact, read_teacher_label_artifact,
    scoreboard_artifact_path,
};
use mimir_types::{AnchorKind, PersistedTeacherLabelArtifact, TeacherLabelTarget};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct CanonicalVerticalSliceResult {
    pub(crate) consumer_export: ConsumerExport,
    pub(crate) scoreboard_artifact: PersistedScoreboardArtifact,
    pub(crate) teacher_artifacts: Vec<PersistedTeacherLabelArtifact>,
}

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct VerticalSliceGoldenSnapshot {
    pub(crate) export_name: String,
    pub(crate) replay_id: String,
    pub(crate) anchor_id: String,
    pub(crate) anchor_frame_index: u32,
    pub(crate) anchor_kind: AnchorKind,
    pub(crate) export_directory_name: String,
    pub(crate) scoreboard_artifact_relative_path: String,
    pub(crate) teacher_artifact_relative_paths: Vec<String>,
    pub(crate) branch_ids_in_order: Vec<String>,
    pub(crate) scoreboard_rows_in_order: Vec<VerticalSliceGoldenScoreboardRow>,
    pub(crate) teacher_targets_in_order: Vec<String>,
}

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct VerticalSliceGoldenScoreboardRow {
    pub(crate) branch_id: String,
    pub(crate) total_score: f64,
}

pub(crate) fn load_canonical_vertical_slice_result(
    root_dir: &Path,
) -> Result<CanonicalVerticalSliceResult> {
    let export_dir = root_dir.join(VERTICAL_SLICE_EXPORT_DIR_NAME);
    let consumer_export =
        adapt_loaded_export_for_consumer(load_export_bundle(&export_dir).map_err(|error| {
            MimirError::message(format!(
                "failed to load vertical-slice export bundle from {}: {error}",
                export_dir.display()
            ))
        })?);

    let scoreboard_path = scoreboard_artifact_path(root_dir);
    let scoreboard_artifact = read_scoreboard_artifact(&scoreboard_path).map_err(|error| {
        MimirError::message(format!(
            "failed to load vertical-slice scoreboard artifact from {}: {error}",
            scoreboard_path.display()
        ))
    })?;

    let expected_branch_count = consumer_export.branches.len();
    let scoreboard_row_count = scoreboard_artifact.payload.rows.len();
    if scoreboard_row_count != expected_branch_count {
        return Err(MimirError::message(format!(
            "vertical-slice scoreboard row count drift: expected {} rows from export bundle, found {}",
            expected_branch_count, scoreboard_row_count
        )));
    }

    let teacher_dir = root_dir.join(VERTICAL_SLICE_TEACHER_DIR_NAME);
    let teacher_artifact_count = count_teacher_label_files(&teacher_dir)?;
    if teacher_artifact_count != scoreboard_row_count {
        return Err(MimirError::message(format!(
            "vertical-slice teacher artifact count drift: expected {} artifacts from scoreboard-derived branch count, found {}",
            scoreboard_row_count, teacher_artifact_count
        )));
    }

    let teacher_artifacts = (0..scoreboard_row_count)
        .map(|index| {
            let path = teacher_dir.join(format!("teacher-label-{index}.json"));
            read_teacher_label_artifact(&path).map_err(|error| {
                MimirError::message(format!(
                    "failed to load vertical-slice teacher-label artifact {} from {}: {error}",
                    index,
                    path.display()
                ))
            })
        })
        .collect::<Result<Vec<_>>>()?;

    Ok(CanonicalVerticalSliceResult {
        consumer_export,
        scoreboard_artifact,
        teacher_artifacts,
    })
}

fn count_teacher_label_files(teacher_dir: &Path) -> Result<usize> {
    let entries = fs::read_dir(teacher_dir).map_err(|error| MimirError::io(teacher_dir, error))?;
    let mut count = 0usize;

    for entry in entries {
        let entry = entry.map_err(|error| MimirError::io(teacher_dir, error))?;
        if !entry
            .file_type()
            .map_err(|error| MimirError::io(entry.path(), error))?
            .is_file()
        {
            continue;
        }

        let file_name = entry.file_name();
        let Some(file_name) = file_name.to_str() else {
            continue;
        };

        if file_name.starts_with("teacher-label-") && file_name.ends_with(".json") {
            count += 1;
        }
    }

    Ok(count)
}

impl CanonicalVerticalSliceResult {
    pub(crate) fn teacher_branch_targets_in_order(&self) -> Result<Vec<String>> {
        self.teacher_artifacts
            .iter()
            .map(|artifact| match &artifact.payload.target {
                TeacherLabelTarget::Branch(branch_id) => Ok(branch_id.as_str().to_string()),
                other => Err(MimirError::message(format!(
                    "vertical-slice teacher target drift: expected branch target, found {other:?}"
                ))),
            })
            .collect()
    }

    pub(crate) fn golden_snapshot(
        &self,
        export_directory_name: &str,
        scoreboard_artifact_relative_path: &str,
        teacher_directory_name: &str,
    ) -> Result<VerticalSliceGoldenSnapshot> {
        let anchor_count = self.consumer_export.anchors.len();
        if anchor_count != 1 {
            return Err(MimirError::message(format!(
                "vertical-slice snapshot requires exactly one anchor, found {anchor_count}"
            )));
        }
        let anchor = self
            .consumer_export
            .anchors
            .first()
            .expect("anchor count already checked");

        Ok(VerticalSliceGoldenSnapshot {
            export_name: self.consumer_export.manifest.export_name.clone(),
            replay_id: anchor.replay_id.as_str().to_string(),
            anchor_id: anchor.id.as_str().to_string(),
            anchor_frame_index: anchor.frame_index.get(),
            anchor_kind: anchor.kind.clone(),
            export_directory_name: export_directory_name.to_string(),
            scoreboard_artifact_relative_path: scoreboard_artifact_relative_path.to_string(),
            teacher_artifact_relative_paths: (0..self.teacher_artifacts.len())
                .map(|index| format!("{teacher_directory_name}/teacher-label-{index}.json"))
                .collect(),
            branch_ids_in_order: self
                .consumer_export
                .branches
                .iter()
                .map(|branch| branch.id.as_str().to_string())
                .collect(),
            scoreboard_rows_in_order: self
                .scoreboard_artifact
                .payload
                .rows
                .iter()
                .map(|row| VerticalSliceGoldenScoreboardRow {
                    branch_id: row.branch_id.as_str().to_string(),
                    total_score: row.score.total,
                })
                .collect(),
            teacher_targets_in_order: self.teacher_branch_targets_in_order()?,
        })
    }
}
