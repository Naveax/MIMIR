use crate::vertical_slice_result::VerticalSliceGoldenScoreboardRow;
use crate::vertical_slice_test_support::{
    VerticalSliceFixtureLane,
    assert_fixture_lane_extra_teacher_artifact_count_drift_fails_explicitly,
    assert_fixture_lane_matches_expected_contract,
    assert_fixture_lane_missing_teacher_artifact_fails_explicitly,
    assert_fixture_lane_non_branch_teacher_target_drift_fails_explicitly,
    assert_fixture_lane_repeated_runs_are_identical,
    assert_fixture_lane_scoreboard_component_schema_drift_fails_explicitly,
    assert_fixture_lane_scoreboard_row_count_drift_fails_explicitly,
    assert_fixture_lane_snapshot_fails_explicitly_when_anchor_count_is_not_one,
    assert_fixture_lane_teacher_artifact_ordinal_file_drift_changes_snapshot,
    assert_fixture_lanes_have_distinct_golden_snapshots, expected_golden_snapshot_for_lane,
    expected_stage73_golden_snapshot, load_result, load_snapshot,
    persisted_input_artifact_for_lane_with_anchor_metadata,
    persisted_input_artifact_for_lane_with_export_name,
    persisted_input_artifact_for_lane_with_proposal_score_signals,
    persisted_input_artifact_for_lane_with_proposal_surface,
    persisted_input_artifact_for_lane_with_scorer_weights,
    persisted_input_artifact_for_lane_with_simulation_seed,
    persisted_input_artifact_for_lane_with_teacher_namespace, rewrite_scoreboard_artifact,
    run_persisted_input_artifact_and_capture_simulation_requests,
    run_persisted_input_artifact_and_load, run_sample_fixture, sample_fixture,
};
use mimir_anchor::{AnchorHint, HintAnchorDetector};
use mimir_branch::{BoundedManualBranchGenerator, BranchGenerationRequest, BranchProposal};
use mimir_core::{MimirError, NamedComponent, Result};
use mimir_export::{
    ConsumerExport, ExportBundleInput, ExportEncoding, ExportManifest,
    adapt_loaded_export_for_consumer, export_bundle, load_export_bundle,
};
use mimir_io::{
    ArtifactFormat, PersistedScoreRow, PersistedScoreVector, PersistedScoreboard,
    PersistedScoreboardArtifact, scoreboard_artifact_path, write_scoreboard_artifact,
    write_teacher_label_artifact,
};
use mimir_score::{ScoreVector, Scorer, WeightedSumScorer};
use mimir_sim_bridge::{SimBackend, SimulationCommand, SimulationRequest};
use mimir_teacher::{PassThroughTeacherSynthesizer, TeacherSynthesisRequest, TeacherSynthesizer};
use mimir_types::{
    ActionRecord, ArtifactHeader, ArtifactKind, BranchId, BranchRecord, FieldValue, Metadata,
    PersistedTeacherLabelArtifact, ReplayId, TeacherLabelId, TeacherLabelRecord,
    TeacherLabelTarget,
};
use std::collections::BTreeMap;
use std::fs;
use std::path::Path;
use tempfile::tempdir;

#[cfg(test)]
use mimir_core::hash_serializable;
#[cfg(test)]
use mimir_export::{EXPORT_INDEX_FILE_NAME, inspect_export_bundle};
#[cfg(test)]
use mimir_io::{
    read_artifact_auto, read_vertical_slice_input_artifact, vertical_slice_input_artifact_path,
    write_vertical_slice_input_artifact,
};
#[cfg(test)]
use serde_json::Value;
#[cfg(test)]
use std::path::PathBuf;

const VERTICAL_SLICE_EXPORT_COMPONENT: &str = "mimir-cli-vertical-slice";
pub(crate) const VERTICAL_SLICE_TEACHER_DIR_NAME: &str = "teacher_labels";
pub(crate) const VERTICAL_SLICE_EXPORT_DIR_NAME: &str = "export_bundle";

#[derive(Debug, Clone)]
pub(crate) struct VerticalSliceFixture {
    pub(crate) replay_id: ReplayId,
    pub(crate) export_name: String,
    pub(crate) teacher_namespace: String,
    pub(crate) simulation_seed: u64,
    pub(crate) anchor_hint: AnchorHint,
    pub(crate) proposals: Vec<VerticalSliceProposalFixture>,
    pub(crate) scorer_weights: BTreeMap<String, f64>,
}

#[derive(Debug, Clone)]
pub(crate) struct VerticalSliceProposalFixture {
    pub(crate) branch_proposal: BranchProposal,
    pub(crate) score_signals: BTreeMap<String, f64>,
}

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct VerticalSliceRunOutput {
    pub(crate) manifest: ExportManifest,
    pub(crate) consumer_export: ConsumerExport,
    pub(crate) scoreboard: PersistedScoreboard,
    pub(crate) teacher_artifacts: Vec<PersistedTeacherLabelArtifact>,
}

pub(crate) fn run_deterministic_vertical_slice(
    output_dir: &Path,
    fixture: &VerticalSliceFixture,
    backend: Option<&dyn SimBackend>,
) -> Result<VerticalSliceRunOutput> {
    let backend = backend.ok_or_else(|| {
        MimirError::message("deterministic vertical slice requires deterministic fake backend")
    })?;

    fs::create_dir_all(output_dir).map_err(|error| MimirError::io(output_dir, error))?;

    let anchor_artifacts = HintAnchorDetector.detect_persisted(
        &fixture.replay_id,
        std::slice::from_ref(&fixture.anchor_hint),
    )?;
    let anchor = anchor_artifacts
        .first()
        .map(|artifact| artifact.payload.clone())
        .ok_or_else(|| MimirError::message("deterministic vertical slice produced no anchors"))?;

    let branch_request = BranchGenerationRequest {
        anchor,
        proposals: fixture
            .proposals
            .iter()
            .map(|proposal| proposal.branch_proposal.clone())
            .collect(),
        max_branches: fixture.proposals.len(),
    };
    let branch_artifacts =
        BoundedManualBranchGenerator::default().generate_persisted(&branch_request)?;
    if branch_artifacts.len() != fixture.proposals.len() {
        return Err(MimirError::message(format!(
            "deterministic vertical slice branch count drift: expected {}, found {}",
            fixture.proposals.len(),
            branch_artifacts.len()
        )));
    }
    let scorer = WeightedSumScorer::new(fixture.scorer_weights.clone());

    let mut scoreboard_rows = Vec::with_capacity(branch_artifacts.len());
    let mut teacher_seed_labels = Vec::with_capacity(branch_artifacts.len());

    for (index, (artifact, proposal_fixture)) in
        branch_artifacts.iter().zip(&fixture.proposals).enumerate()
    {
        let simulation_request = simulation_request_for_branch(
            &artifact.payload.id,
            fixture.simulation_seed,
            &artifact.payload.actions,
        );
        let simulation_result = backend.simulate(&simulation_request)?;
        let score = score_branch(
            &scorer,
            &artifact.payload.id,
            &proposal_fixture.score_signals,
        );

        scoreboard_rows.push(PersistedScoreRow {
            branch_id: artifact.payload.id.clone(),
            branch_label: artifact.payload.label.clone(),
            simulation_id: simulation_result.simulation_id.clone(),
            simulation_backend: simulation_result.backend.clone(),
            step_hashes: simulation_result.step_hashes.clone(),
            score: PersistedScoreVector::from(score.clone()),
        });
        teacher_seed_labels.push(teacher_seed_label(
            fixture,
            index,
            artifact.payload.id.clone(),
            artifact.payload.label.as_deref(),
            score.total,
        )?);
    }

    let scoreboard = PersistedScoreboard {
        rows: scoreboard_rows,
    };
    persist_scoreboard(output_dir, &scoreboard)?;

    let synthesized_teacher_labels =
        synthesize_teacher_labels(&fixture.teacher_namespace, teacher_seed_labels)?;
    let teacher_artifacts = persist_teacher_artifacts(
        output_dir,
        &fixture.teacher_namespace,
        &synthesized_teacher_labels,
    )?;

    let export_dir = output_dir.join(VERTICAL_SLICE_EXPORT_DIR_NAME);
    let manifest = export_bundle(
        &export_dir,
        &ExportBundleInput {
            export_name: fixture.export_name.clone(),
            artifact_encoding: ExportEncoding::Json,
            anchor_artifacts,
            branch_artifacts,
            created_by_component: Some(VERTICAL_SLICE_EXPORT_COMPONENT.to_string()),
        },
    )?;
    let consumer_export = adapt_loaded_export_for_consumer(load_export_bundle(&export_dir)?);

    Ok(VerticalSliceRunOutput {
        manifest,
        consumer_export,
        scoreboard,
        teacher_artifacts,
    })
}

fn simulation_request_for_branch(
    branch_id: &BranchId,
    simulation_seed: u64,
    actions: &[ActionRecord],
) -> SimulationRequest {
    SimulationRequest {
        simulation_id: format!("{branch_id}:deterministic-vertical-slice"),
        seed: simulation_seed,
        commands: actions
            .iter()
            .map(|action| SimulationCommand {
                label: action.action_key.clone(),
                metadata: action.fields.clone(),
            })
            .collect(),
    }
}

fn score_branch(
    scorer: &WeightedSumScorer,
    branch_id: &BranchId,
    score_signals: &BTreeMap<String, f64>,
) -> ScoreVector {
    scorer.score(Some(branch_id.clone()), score_signals)
}

fn teacher_seed_label(
    fixture: &VerticalSliceFixture,
    ordinal: usize,
    branch_id: BranchId,
    branch_label: Option<&str>,
    total_score: f64,
) -> Result<TeacherLabelRecord> {
    let score = if total_score.is_finite()
        && total_score >= f32::MIN as f64
        && total_score <= f32::MAX as f64
    {
        Some(total_score as f32)
    } else {
        return Err(MimirError::message(format!(
            "teacher score for branch {} is not representable as finite f32",
            branch_id
        )));
    };

    Ok(TeacherLabelRecord {
        id: TeacherLabelId::new(format!("{}:teacher:{ordinal}", fixture.export_name)),
        target: TeacherLabelTarget::Branch(branch_id),
        label: branch_label.unwrap_or("unnamed-branch").to_string(),
        score,
        metadata: Metadata::from([
            (
                "teacher_namespace",
                FieldValue::Text(fixture.teacher_namespace.clone()),
            ),
            (
                "ordinal",
                FieldValue::Integer(
                    i64::try_from(ordinal).expect("teacher ordinal should fit in i64"),
                ),
            ),
        ]),
    })
}

fn synthesize_teacher_labels(
    teacher_namespace: &str,
    mut labels: Vec<TeacherLabelRecord>,
) -> Result<Vec<TeacherLabelRecord>> {
    labels.sort_by(|left, right| {
        let left_score = left.score.unwrap_or(f32::NEG_INFINITY);
        let right_score = right.score.unwrap_or(f32::NEG_INFINITY);
        right_score
            .total_cmp(&left_score)
            .then_with(|| left.id.as_str().cmp(right.id.as_str()))
    });

    let labels = labels
        .into_iter()
        .enumerate()
        .map(|(rank, mut label)| {
            label.metadata.insert(
                "teacher_rank",
                FieldValue::Integer(i64::try_from(rank).expect("rank should fit in i64")),
            );
            label.metadata.insert(
                "teacher_namespace_copy",
                FieldValue::Text(teacher_namespace.to_string()),
            );
            label
        })
        .collect::<Vec<_>>();

    PassThroughTeacherSynthesizer.synthesize(&TeacherSynthesisRequest {
        namespace: teacher_namespace.to_string(),
        labels,
    })
}

fn persist_scoreboard(output_dir: &Path, scoreboard: &PersistedScoreboard) -> Result<()> {
    let scoreboard_path = scoreboard_artifact_path(output_dir);
    let artifact = PersistedScoreboardArtifact::new(
        ArtifactHeader::for_kind(ArtifactKind::Scoreboard, VERTICAL_SLICE_EXPORT_COMPONENT),
        scoreboard.clone(),
    );
    write_scoreboard_artifact(&scoreboard_path, ArtifactFormat::Json, &artifact)
}

fn persist_teacher_artifacts(
    output_dir: &Path,
    teacher_namespace: &str,
    labels: &[TeacherLabelRecord],
) -> Result<Vec<PersistedTeacherLabelArtifact>> {
    let teacher_dir = output_dir.join(VERTICAL_SLICE_TEACHER_DIR_NAME);
    fs::create_dir_all(&teacher_dir).map_err(|error| MimirError::io(&teacher_dir, error))?;

    labels
        .iter()
        .enumerate()
        .map(|(index, label)| {
            let artifact = PersistedTeacherLabelArtifact::new(
                ArtifactHeader::for_kind(
                    ArtifactKind::TeacherLabel,
                    VERTICAL_SLICE_EXPORT_COMPONENT,
                )
                .with_created_by_component(PassThroughTeacherSynthesizer.component_name())
                .with_metadata(Metadata::from([(
                    "teacher_namespace",
                    FieldValue::Text(teacher_namespace.to_string()),
                )])),
                label.clone(),
            );
            let path = teacher_dir.join(format!("teacher-label-{index}.json"));
            write_teacher_label_artifact(&path, ArtifactFormat::Json, &artifact)?;
            Ok(artifact)
        })
        .collect()
}

#[test]
fn deterministic_vertical_slice_persists_reloadable_outputs() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_matches_expected_contract(
        directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("stage69 fixture should satisfy the shared parity contract");
}

#[test]
fn deterministic_vertical_slice_is_identical_across_repeated_runs() {
    let first = tempdir().expect("tempdir should be created");
    let second = tempdir().expect("tempdir should be created");
    assert_fixture_lane_repeated_runs_are_identical(
        first.path(),
        second.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("stage69 repeated runs should satisfy the shared parity contract");
}

#[test]
fn deterministic_vertical_slice_preserves_branch_score_and_teacher_ordering() {
    let directory = tempdir().expect("tempdir should be created");
    run_sample_fixture(directory.path()).expect("vertical slice should succeed");
    let canonical = load_result(directory.path()).expect("result should reload");

    let branch_labels = canonical
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.label.clone())
        .collect::<Vec<_>>();
    assert_eq!(
        branch_labels,
        vec![
            Some("candidate-alpha".to_string()),
            Some("candidate-beta".to_string())
        ]
    );

    let score_branch_ids = canonical
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.branch_id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        score_branch_ids,
        vec![
            "anchor-stage69:branch:0".to_string(),
            "anchor-stage69:branch:1".to_string()
        ]
    );

    let teacher_targets = canonical
        .teacher_branch_targets_in_order()
        .expect("teacher targets should stay branch-typed");
    assert_eq!(
        teacher_targets,
        vec![
            "anchor-stage69:branch:1".to_string(),
            "anchor-stage69:branch:0".to_string()
        ]
    );
}

#[test]
fn deterministic_vertical_slice_scorer_weights_directly_change_totals_and_teacher_ordering() {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let (_, baseline) = crate::vertical_slice_test_support::run_fixture_lane_and_load(
        baseline_directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("baseline stage69 lane should reload canonically");

    let mutated_artifact = persisted_input_artifact_for_lane_with_scorer_weights(
        VerticalSliceFixtureLane::Stage69Sample,
        BTreeMap::from([
            ("coverage".to_string(), 1.0),
            ("stability".to_string(), 2.5),
        ]),
    );
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage69 lane should reload canonically");

    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_branch_ids,
        vec![
            "anchor-stage69:branch:0".to_string(),
            "anchor-stage69:branch:1".to_string()
        ]
    );
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    let baseline_rows = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| (row.branch_id.as_str().to_string(), row.score.total))
        .collect::<Vec<_>>();
    let mutated_rows = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| (row.branch_id.as_str().to_string(), row.score.total))
        .collect::<Vec<_>>();
    assert_eq!(baseline_rows.len(), 2);
    assert_eq!(mutated_rows.len(), baseline_rows.len());
    assert_eq!(
        baseline_rows,
        vec![
            ("anchor-stage69:branch:0".to_string(), 3.5),
            ("anchor-stage69:branch:1".to_string(), 5.0),
        ]
    );
    assert_eq!(
        mutated_rows,
        vec![
            ("anchor-stage69:branch:0".to_string(), 9.5),
            ("anchor-stage69:branch:1".to_string(), 9.0),
        ]
    );
    let score_deltas = mutated_rows
        .iter()
        .zip(&baseline_rows)
        .map(|(mutated_row, baseline_row)| {
            (mutated_row.0.clone(), (mutated_row.1 - baseline_row.1))
        })
        .collect::<Vec<_>>();
    assert_eq!(
        score_deltas,
        vec![
            ("anchor-stage69:branch:0".to_string(), 6.0),
            ("anchor-stage69:branch:1".to_string(), 4.0),
        ]
    );

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(
        baseline_teacher_targets,
        vec![
            "anchor-stage69:branch:1".to_string(),
            "anchor-stage69:branch:0".to_string()
        ]
    );
    assert_eq!(
        mutated_teacher_targets,
        vec![
            "anchor-stage69:branch:0".to_string(),
            "anchor-stage69:branch:1".to_string()
        ]
    );
}

#[test]
fn deterministic_vertical_slice_directly_consumes_simulation_seed_from_persisted_input() {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_artifact = persisted_input_artifact_for_lane_with_simulation_seed(
        VerticalSliceFixtureLane::Stage69Sample,
        69,
    );
    let mutated_seed = 6901;
    let mutated_artifact = persisted_input_artifact_for_lane_with_simulation_seed(
        VerticalSliceFixtureLane::Stage69Sample,
        mutated_seed,
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.simulation_seed = mutated_seed;
    assert_eq!(mutated_artifact, expected_mutated_artifact);

    let (_, baseline, baseline_requests) =
        run_persisted_input_artifact_and_capture_simulation_requests(
            baseline_directory.path(),
            &baseline_artifact,
        )
        .expect("baseline stage69 lane should expose consumed simulation requests");
    let (_, mutated, mutated_requests) =
        run_persisted_input_artifact_and_capture_simulation_requests(
            mutated_directory.path(),
            &mutated_artifact,
        )
        .expect("mutated stage69 lane should expose consumed simulation requests");

    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    let baseline_request_ids = baseline_requests
        .iter()
        .map(|request| request.simulation_id.clone())
        .collect::<Vec<_>>();
    let mutated_request_ids = mutated_requests
        .iter()
        .map(|request| request.simulation_id.clone())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_request_ids,
        vec![
            "anchor-stage69:branch:0:deterministic-vertical-slice".to_string(),
            "anchor-stage69:branch:1:deterministic-vertical-slice".to_string(),
        ]
    );
    assert_eq!(mutated_request_ids, baseline_request_ids);
    assert!(baseline_requests.iter().all(|request| request.seed == 69));
    assert!(
        mutated_requests
            .iter()
            .all(|request| request.seed == mutated_seed)
    );

    let baseline_totals = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    let mutated_totals = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    assert_eq!(mutated_totals, baseline_totals);

    let baseline_step_hashes = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.step_hashes.clone())
        .collect::<Vec<_>>();
    let mutated_step_hashes = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.step_hashes.clone())
        .collect::<Vec<_>>();
    assert_eq!(mutated_step_hashes.len(), baseline_step_hashes.len());
    assert_ne!(mutated_step_hashes, baseline_step_hashes);
}

#[test]
fn deterministic_vertical_slice_explicitly_propagates_teacher_namespace_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_artifact = persisted_input_artifact_for_lane_with_teacher_namespace(
        VerticalSliceFixtureLane::Stage69Sample,
        "stage69.teacher",
    );
    let mutated_namespace = "stage69.teacher.explicit-propagation";
    let mutated_artifact = persisted_input_artifact_for_lane_with_teacher_namespace(
        VerticalSliceFixtureLane::Stage69Sample,
        mutated_namespace,
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.teacher_namespace = mutated_namespace.to_string();
    assert_eq!(mutated_artifact, expected_mutated_artifact);

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage69 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage69 lane should reload canonically");

    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    let baseline_totals = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    let mutated_totals = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    assert_eq!(mutated_totals, baseline_totals);

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(mutated_teacher_targets, baseline_teacher_targets);

    for artifact in &baseline.teacher_artifacts {
        assert_eq!(
            artifact.payload.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text("stage69.teacher".to_string()))
        );
        assert_eq!(
            artifact.payload.metadata.get("teacher_namespace_copy"),
            Some(&FieldValue::Text("stage69.teacher".to_string()))
        );
        assert_eq!(
            artifact.header.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text("stage69.teacher".to_string()))
        );
    }

    for artifact in &mutated.teacher_artifacts {
        assert_eq!(
            artifact.payload.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text(mutated_namespace.to_string()))
        );
        assert_eq!(
            artifact.payload.metadata.get("teacher_namespace_copy"),
            Some(&FieldValue::Text(mutated_namespace.to_string()))
        );
        assert_eq!(
            artifact.header.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text(mutated_namespace.to_string()))
        );
    }
}

#[test]
fn second_deterministic_vertical_slice_explicitly_propagates_teacher_namespace_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_artifact = persisted_input_artifact_for_lane_with_teacher_namespace(
        VerticalSliceFixtureLane::Stage77Second,
        "stage77.second.teacher",
    );
    let mutated_namespace = "stage77.second.teacher.explicit-propagation";
    let mutated_artifact = persisted_input_artifact_for_lane_with_teacher_namespace(
        VerticalSliceFixtureLane::Stage77Second,
        mutated_namespace,
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.teacher_namespace = mutated_namespace.to_string();
    assert_eq!(mutated_artifact, expected_mutated_artifact);

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage77 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage77 lane should reload canonically");

    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    let baseline_totals = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    let mutated_totals = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    assert_eq!(mutated_totals, baseline_totals);

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(mutated_teacher_targets, baseline_teacher_targets);

    assert_eq!(
        mutated.consumer_export.anchors,
        baseline.consumer_export.anchors
    );

    let baseline_snapshot = load_snapshot(baseline_directory.path())
        .expect("baseline stage77 lane should load the frozen snapshot");
    let mutated_snapshot = load_snapshot(mutated_directory.path())
        .expect("mutated stage77 lane should load the frozen snapshot");
    assert_eq!(mutated_snapshot.export_name, baseline_snapshot.export_name);
    assert_eq!(mutated_snapshot.replay_id, baseline_snapshot.replay_id);
    assert_eq!(mutated_snapshot.anchor_id, baseline_snapshot.anchor_id);
    assert_eq!(
        mutated_snapshot.anchor_frame_index,
        baseline_snapshot.anchor_frame_index
    );
    assert_eq!(mutated_snapshot.anchor_kind, baseline_snapshot.anchor_kind);
    assert_eq!(
        mutated_snapshot.export_directory_name,
        baseline_snapshot.export_directory_name
    );
    assert_eq!(
        mutated_snapshot.scoreboard_artifact_relative_path,
        baseline_snapshot.scoreboard_artifact_relative_path
    );
    assert_eq!(
        mutated_snapshot.teacher_artifact_relative_paths,
        baseline_snapshot.teacher_artifact_relative_paths
    );
    assert_eq!(
        mutated_snapshot.branch_ids_in_order,
        baseline_snapshot.branch_ids_in_order
    );
    assert_eq!(
        mutated_snapshot.scoreboard_rows_in_order,
        baseline_snapshot.scoreboard_rows_in_order
    );
    assert_eq!(
        mutated_snapshot.teacher_targets_in_order,
        baseline_snapshot.teacher_targets_in_order
    );

    for artifact in &baseline.teacher_artifacts {
        assert_eq!(
            artifact.payload.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text("stage77.second.teacher".to_string()))
        );
        assert_eq!(
            artifact.payload.metadata.get("teacher_namespace_copy"),
            Some(&FieldValue::Text("stage77.second.teacher".to_string()))
        );
        assert_eq!(
            artifact.header.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text("stage77.second.teacher".to_string()))
        );
    }

    for artifact in &mutated.teacher_artifacts {
        assert_eq!(
            artifact.payload.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text(mutated_namespace.to_string()))
        );
        assert_eq!(
            artifact.payload.metadata.get("teacher_namespace_copy"),
            Some(&FieldValue::Text(mutated_namespace.to_string()))
        );
        assert_eq!(
            artifact.header.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text(mutated_namespace.to_string()))
        );
    }
}

#[test]
fn deterministic_vertical_slice_explicitly_propagates_anchor_metadata_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_metadata =
        Metadata::from([("source", FieldValue::Text("stage69-fixture".to_string()))]);
    let mutated_metadata = Metadata::from([
        (
            "anchor_contract_tag",
            FieldValue::Text("stage88-explicit-propagation".to_string()),
        ),
        (
            "anchor_origin",
            FieldValue::Text("stage69-fixture-mutated".to_string()),
        ),
    ]);
    let baseline_artifact = persisted_input_artifact_for_lane_with_anchor_metadata(
        VerticalSliceFixtureLane::Stage69Sample,
        baseline_metadata.clone(),
    );
    let mutated_artifact = persisted_input_artifact_for_lane_with_anchor_metadata(
        VerticalSliceFixtureLane::Stage69Sample,
        mutated_metadata.clone(),
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.anchor_hint.metadata = mutated_metadata.clone();
    assert_eq!(mutated_artifact, expected_mutated_artifact);

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage69 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage69 lane should reload canonically");

    assert_eq!(baseline.consumer_export.anchors.len(), 1);
    assert_eq!(mutated.consumer_export.anchors.len(), 1);
    assert_eq!(
        baseline.consumer_export.anchors[0].metadata,
        baseline_metadata
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].metadata,
        mutated_metadata
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].id,
        baseline.consumer_export.anchors[0].id
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].frame_index,
        baseline.consumer_export.anchors[0].frame_index
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].kind,
        baseline.consumer_export.anchors[0].kind
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].replay_id,
        baseline.consumer_export.anchors[0].replay_id
    );

    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    let baseline_totals = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    let mutated_totals = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    assert_eq!(mutated_totals, baseline_totals);

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(mutated_teacher_targets, baseline_teacher_targets);

    let baseline_snapshot = load_snapshot(baseline_directory.path())
        .expect("baseline stage69 lane should load the frozen snapshot");
    let mutated_snapshot = load_snapshot(mutated_directory.path())
        .expect("mutated stage69 lane should load the frozen snapshot");
    assert_eq!(baseline_snapshot, expected_stage73_golden_snapshot());
    assert_eq!(mutated_snapshot, baseline_snapshot);
}

#[test]
fn second_deterministic_vertical_slice_explicitly_propagates_anchor_metadata_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_metadata = Metadata::from([(
        "source",
        FieldValue::Text("stage77-second-fixture".to_string()),
    )]);
    let mutated_metadata = Metadata::from([
        (
            "anchor_contract_tag",
            FieldValue::Text("stage97-stage77-explicit-propagation".to_string()),
        ),
        (
            "anchor_origin",
            FieldValue::Text("stage77-second-fixture-mutated".to_string()),
        ),
    ]);
    let baseline_artifact = persisted_input_artifact_for_lane_with_anchor_metadata(
        VerticalSliceFixtureLane::Stage77Second,
        baseline_metadata.clone(),
    );
    let mutated_artifact = persisted_input_artifact_for_lane_with_anchor_metadata(
        VerticalSliceFixtureLane::Stage77Second,
        mutated_metadata.clone(),
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.anchor_hint.metadata = mutated_metadata.clone();
    assert_eq!(mutated_artifact, expected_mutated_artifact);
    assert_eq!(mutated_artifact.header, baseline_artifact.header);
    assert_eq!(
        mutated_artifact.payload.replay_id,
        baseline_artifact.payload.replay_id
    );
    assert_eq!(
        mutated_artifact.payload.export_name,
        baseline_artifact.payload.export_name
    );
    assert_eq!(
        mutated_artifact.payload.teacher_namespace,
        baseline_artifact.payload.teacher_namespace
    );
    assert_eq!(
        mutated_artifact.payload.simulation_seed,
        baseline_artifact.payload.simulation_seed
    );
    assert_eq!(
        mutated_artifact.payload.anchor_hint.anchor_id,
        baseline_artifact.payload.anchor_hint.anchor_id
    );
    assert_eq!(
        mutated_artifact.payload.anchor_hint.frame_index,
        baseline_artifact.payload.anchor_hint.frame_index
    );
    assert_eq!(
        mutated_artifact.payload.anchor_hint.kind,
        baseline_artifact.payload.anchor_hint.kind
    );
    assert_eq!(
        mutated_artifact.payload.proposals,
        baseline_artifact.payload.proposals
    );
    assert_eq!(
        mutated_artifact.payload.scorer_weights,
        baseline_artifact.payload.scorer_weights
    );
    assert_ne!(
        mutated_artifact.payload.anchor_hint.metadata,
        baseline_artifact.payload.anchor_hint.metadata
    );

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage77 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage77 lane should reload canonically");

    assert_eq!(baseline.consumer_export.anchors.len(), 1);
    assert_eq!(mutated.consumer_export.anchors.len(), 1);
    assert_eq!(
        baseline.consumer_export.anchors[0].metadata,
        baseline_metadata
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].metadata,
        mutated_metadata
    );
    assert_ne!(
        mutated.consumer_export.anchors[0].metadata,
        baseline.consumer_export.anchors[0].metadata
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].id,
        baseline.consumer_export.anchors[0].id
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].frame_index,
        baseline.consumer_export.anchors[0].frame_index
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].kind,
        baseline.consumer_export.anchors[0].kind
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].replay_id,
        baseline.consumer_export.anchors[0].replay_id
    );

    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_branch_ids,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string()
        ]
    );
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    let baseline_totals = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    let mutated_totals = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    assert_eq!(baseline_totals, vec![6.0, 2.5]);
    assert_eq!(mutated_totals, baseline_totals);

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(
        baseline_teacher_targets,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string()
        ]
    );
    assert_eq!(mutated_teacher_targets, baseline_teacher_targets);

    assert_eq!(mutated.teacher_artifacts, baseline.teacher_artifacts);

    let expected_snapshot =
        expected_golden_snapshot_for_lane(VerticalSliceFixtureLane::Stage77Second);
    let baseline_snapshot = load_snapshot(baseline_directory.path())
        .expect("baseline stage77 lane should load the frozen snapshot");
    let mutated_snapshot = load_snapshot(mutated_directory.path())
        .expect("mutated stage77 lane should load the frozen snapshot");
    assert_eq!(baseline_snapshot, expected_snapshot);
    assert_eq!(mutated_snapshot, expected_snapshot);
}

#[test]
fn deterministic_vertical_slice_explicitly_propagates_proposal_actions_legal_hint_and_metadata_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage69Sample,
        1,
        "candidate-beta",
        vec![
            ActionRecord {
                action_key: "boost".to_string(),
                fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
            },
            ActionRecord {
                action_key: "steer".to_string(),
                fields: Metadata::from([("direction", FieldValue::Float(0.5))]),
            },
        ],
        Some(true),
        Metadata::from([(
            "proposal_source",
            FieldValue::Text("fixture-beta".to_string()),
        )]),
    );
    let mutated_actions = vec![
        ActionRecord {
            action_key: "boost".to_string(),
            fields: Metadata::from([
                ("pressed", FieldValue::Boolean(false)),
                (
                    "stage89_action_tag",
                    FieldValue::Text("proposal-surface".to_string()),
                ),
            ]),
        },
        ActionRecord {
            action_key: "steer".to_string(),
            fields: Metadata::from([("direction", FieldValue::Float(-0.25))]),
        },
    ];
    let mutated_legal_hint = Some(true);
    let mutated_metadata = Metadata::from([
        (
            "proposal_contract_tag",
            FieldValue::Text("stage89-explicit-propagation".to_string()),
        ),
        (
            "proposal_source",
            FieldValue::Text("fixture-beta-mutated".to_string()),
        ),
    ]);
    let mutated_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage69Sample,
        1,
        "candidate-beta",
        mutated_actions.clone(),
        mutated_legal_hint,
        mutated_metadata.clone(),
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.proposals[1].actions = mutated_actions.clone();
    expected_mutated_artifact.payload.proposals[1].legal_hint = mutated_legal_hint;
    expected_mutated_artifact.payload.proposals[1].metadata = mutated_metadata.clone();
    assert_eq!(mutated_artifact, expected_mutated_artifact);

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage69 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage69 lane should reload canonically");

    assert_eq!(baseline.consumer_export.branches.len(), 2);
    assert_eq!(mutated.consumer_export.branches.len(), 2);
    assert_eq!(
        baseline.consumer_export.branches[1].label.as_deref(),
        Some("candidate-beta")
    );
    assert_eq!(
        mutated.consumer_export.branches[1].label.as_deref(),
        Some("candidate-beta")
    );
    assert_eq!(
        baseline.consumer_export.branches[1].actions,
        baseline_artifact.payload.proposals[1].actions
    );
    assert_eq!(
        baseline.consumer_export.branches[1].legality_hint,
        baseline_artifact.payload.proposals[1].legal_hint
    );
    assert_eq!(
        baseline.consumer_export.branches[1].metadata,
        baseline_artifact.payload.proposals[1].metadata
    );
    assert_eq!(mutated.consumer_export.branches[1].actions, mutated_actions);
    assert_eq!(
        mutated.consumer_export.branches[1].legality_hint,
        mutated_legal_hint
    );
    assert_eq!(
        mutated.consumer_export.branches[1].metadata,
        mutated_metadata
    );

    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    let baseline_totals = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    let mutated_totals = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| row.score.total)
        .collect::<Vec<_>>();
    assert_eq!(mutated_totals, baseline_totals);

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(mutated_teacher_targets, baseline_teacher_targets);

    let baseline_snapshot = load_snapshot(baseline_directory.path())
        .expect("baseline stage69 lane should load the frozen snapshot");
    let mutated_snapshot = load_snapshot(mutated_directory.path())
        .expect("mutated stage69 lane should load the frozen snapshot");
    assert_eq!(baseline_snapshot, expected_stage73_golden_snapshot());
    assert_eq!(mutated_snapshot, baseline_snapshot);
}

#[test]
fn deterministic_vertical_slice_export_name_changes_only_export_name_derived_teacher_ids() {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_export_name = "stage69-vertical-slice";
    let mutated_export_name = "stage69-vertical-slice-export-name-drift";
    let baseline_artifact = persisted_input_artifact_for_lane_with_export_name(
        VerticalSliceFixtureLane::Stage69Sample,
        baseline_export_name,
    );
    let mutated_artifact = persisted_input_artifact_for_lane_with_export_name(
        VerticalSliceFixtureLane::Stage69Sample,
        mutated_export_name,
    );

    assert_eq!(
        baseline_artifact.payload.replay_id,
        mutated_artifact.payload.replay_id
    );
    assert_ne!(
        baseline_artifact.payload.export_name,
        mutated_artifact.payload.export_name
    );
    assert_eq!(
        baseline_artifact.payload.teacher_namespace,
        mutated_artifact.payload.teacher_namespace
    );
    assert_eq!(
        baseline_artifact.payload.simulation_seed,
        mutated_artifact.payload.simulation_seed
    );
    assert_eq!(
        baseline_artifact.payload.anchor_hint,
        mutated_artifact.payload.anchor_hint
    );
    assert_eq!(
        baseline_artifact.payload.proposals,
        mutated_artifact.payload.proposals
    );
    assert_eq!(
        baseline_artifact.payload.scorer_weights,
        mutated_artifact.payload.scorer_weights
    );

    let (baseline_output, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline export-name lane should reload canonically");
    let (mutated_output, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated export-name lane should reload canonically");

    assert_eq!(baseline_output.manifest.export_name, baseline_export_name);
    assert_eq!(mutated_output.manifest.export_name, mutated_export_name);
    assert_eq!(
        baseline.consumer_export.manifest.export_name,
        baseline_export_name
    );
    assert_eq!(
        mutated.consumer_export.manifest.export_name,
        mutated_export_name
    );

    let baseline_teacher_ids = baseline
        .teacher_artifacts
        .iter()
        .map(|artifact| artifact.payload.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_teacher_ids = mutated
        .teacher_artifacts
        .iter()
        .map(|artifact| artifact.payload.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_teacher_ids,
        vec![
            format!("{baseline_export_name}:teacher:1"),
            format!("{baseline_export_name}:teacher:0"),
        ]
    );
    assert_eq!(
        mutated_teacher_ids,
        vec![
            format!("{mutated_export_name}:teacher:1"),
            format!("{mutated_export_name}:teacher:0"),
        ]
    );
    assert_ne!(baseline_teacher_ids, mutated_teacher_ids);

    for (baseline_artifact, mutated_artifact) in baseline
        .teacher_artifacts
        .iter()
        .zip(mutated.teacher_artifacts.iter())
    {
        assert_eq!(
            baseline_artifact.payload.target,
            mutated_artifact.payload.target
        );
        assert_eq!(
            baseline_artifact.payload.label,
            mutated_artifact.payload.label
        );
        assert_eq!(
            baseline_artifact.payload.score,
            mutated_artifact.payload.score
        );
        assert_eq!(
            baseline_artifact.payload.metadata,
            mutated_artifact.payload.metadata
        );
    }

    assert_eq!(
        baseline.consumer_export.anchors,
        mutated.consumer_export.anchors
    );
    assert_eq!(
        baseline.consumer_export.branches,
        mutated.consumer_export.branches
    );
    assert_eq!(
        baseline.scoreboard_artifact.payload,
        mutated.scoreboard_artifact.payload
    );
    assert_eq!(
        baseline
            .teacher_branch_targets_in_order()
            .expect("baseline teacher targets should stay branch-typed"),
        mutated
            .teacher_branch_targets_in_order()
            .expect("mutated teacher targets should stay branch-typed")
    );

    let baseline_snapshot = load_snapshot(baseline_directory.path())
        .expect("baseline export-name lane should load the snapshot");
    let mutated_snapshot = load_snapshot(mutated_directory.path())
        .expect("mutated export-name lane should load the snapshot");
    assert_eq!(baseline_snapshot.export_name, baseline_export_name);
    assert_eq!(mutated_snapshot.export_name, mutated_export_name);
    assert_ne!(baseline_snapshot.export_name, mutated_snapshot.export_name);
    assert_eq!(baseline_snapshot.replay_id, mutated_snapshot.replay_id);
    assert_eq!(baseline_snapshot.anchor_id, mutated_snapshot.anchor_id);
    assert_eq!(
        baseline_snapshot.anchor_frame_index,
        mutated_snapshot.anchor_frame_index
    );
    assert_eq!(baseline_snapshot.anchor_kind, mutated_snapshot.anchor_kind);
    assert_eq!(
        baseline_snapshot.export_directory_name,
        mutated_snapshot.export_directory_name
    );
    assert_eq!(
        baseline_snapshot.scoreboard_artifact_relative_path,
        mutated_snapshot.scoreboard_artifact_relative_path
    );
    assert_eq!(
        baseline_snapshot.teacher_artifact_relative_paths,
        mutated_snapshot.teacher_artifact_relative_paths
    );
    assert_eq!(
        baseline_snapshot.branch_ids_in_order,
        mutated_snapshot.branch_ids_in_order
    );
    assert_eq!(
        baseline_snapshot.scoreboard_rows_in_order,
        mutated_snapshot.scoreboard_rows_in_order
    );
    assert_eq!(
        baseline_snapshot.teacher_targets_in_order,
        mutated_snapshot.teacher_targets_in_order
    );
}

#[test]
fn deterministic_vertical_slice_score_signals_directly_change_score_output_and_teacher_ordering_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_score_signals = BTreeMap::from([
        ("coverage".to_string(), 2.0),
        ("stability".to_string(), 3.0),
    ]);
    let mutated_score_signals = BTreeMap::from([
        ("coverage".to_string(), 4.0),
        ("stability".to_string(), 3.0),
    ]);
    let baseline_artifact = persisted_input_artifact_for_lane_with_proposal_score_signals(
        VerticalSliceFixtureLane::Stage69Sample,
        0,
        baseline_score_signals.clone(),
    );
    let mutated_artifact = persisted_input_artifact_for_lane_with_proposal_score_signals(
        VerticalSliceFixtureLane::Stage69Sample,
        0,
        mutated_score_signals.clone(),
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.proposals[0].score_signals = mutated_score_signals.clone();
    assert_eq!(mutated_artifact, expected_mutated_artifact);

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage69 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage69 lane should reload canonically");

    assert_eq!(
        baseline.consumer_export.anchors.len(),
        1,
        "stage69 lane should keep a single anchor"
    );
    assert_eq!(mutated.consumer_export.anchors.len(), 1);
    assert_eq!(
        mutated.consumer_export.anchors[0].id,
        baseline.consumer_export.anchors[0].id
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].frame_index,
        baseline.consumer_export.anchors[0].frame_index
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].kind,
        baseline.consumer_export.anchors[0].kind
    );
    assert_eq!(
        mutated.consumer_export.anchors[0].metadata,
        baseline.consumer_export.anchors[0].metadata
    );

    assert_eq!(baseline.consumer_export.branches.len(), 2);
    assert_eq!(mutated.consumer_export.branches.len(), 2);
    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_branch_ids,
        vec![
            "anchor-stage69:branch:0".to_string(),
            "anchor-stage69:branch:1".to_string()
        ]
    );
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    assert_eq!(
        baseline.consumer_export.branches[0].actions,
        baseline_artifact.payload.proposals[0].actions
    );
    assert_eq!(
        baseline.consumer_export.branches[0].legality_hint,
        baseline_artifact.payload.proposals[0].legal_hint
    );
    assert_eq!(
        baseline.consumer_export.branches[0].metadata,
        baseline_artifact.payload.proposals[0].metadata
    );
    assert_eq!(
        mutated.consumer_export.branches[0].actions,
        baseline.consumer_export.branches[0].actions
    );
    assert_eq!(
        mutated.consumer_export.branches[0].legality_hint,
        baseline.consumer_export.branches[0].legality_hint
    );
    assert_eq!(
        mutated.consumer_export.branches[0].metadata,
        baseline.consumer_export.branches[0].metadata
    );
    assert_eq!(
        mutated.consumer_export.branches[1].actions,
        baseline.consumer_export.branches[1].actions
    );
    assert_eq!(
        mutated.consumer_export.branches[1].legality_hint,
        baseline.consumer_export.branches[1].legality_hint
    );
    assert_eq!(
        mutated.consumer_export.branches[1].metadata,
        baseline.consumer_export.branches[1].metadata
    );

    let baseline_rows = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.clone(),
                row.score.total,
            )
        })
        .collect::<Vec<_>>();
    let mutated_rows = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.clone(),
                row.score.total,
            )
        })
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_rows,
        vec![
            (
                "anchor-stage69:branch:0".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 2.0),
                    ("stability".to_string(), 1.5),
                ]),
                3.5,
            ),
            (
                "anchor-stage69:branch:1".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 4.0),
                    ("stability".to_string(), 1.0),
                ]),
                5.0,
            ),
        ]
    );
    assert_eq!(
        mutated_rows,
        vec![
            (
                "anchor-stage69:branch:0".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 4.0),
                    ("stability".to_string(), 1.5),
                ]),
                5.5,
            ),
            (
                "anchor-stage69:branch:1".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 4.0),
                    ("stability".to_string(), 1.0),
                ]),
                5.0,
            ),
        ]
    );

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(
        baseline_teacher_targets,
        vec![
            "anchor-stage69:branch:1".to_string(),
            "anchor-stage69:branch:0".to_string()
        ]
    );
    assert_eq!(
        mutated_teacher_targets,
        vec![
            "anchor-stage69:branch:0".to_string(),
            "anchor-stage69:branch:1".to_string()
        ]
    );

    let baseline_snapshot = load_snapshot(baseline_directory.path())
        .expect("baseline stage69 lane should load the frozen snapshot");
    let mutated_snapshot = load_snapshot(mutated_directory.path())
        .expect("mutated stage69 lane should load the frozen snapshot");
    assert_eq!(baseline_snapshot, expected_stage73_golden_snapshot());
    assert_eq!(mutated_snapshot.export_name, baseline_snapshot.export_name);
    assert_eq!(mutated_snapshot.replay_id, baseline_snapshot.replay_id);
    assert_eq!(mutated_snapshot.anchor_id, baseline_snapshot.anchor_id);
    assert_eq!(
        mutated_snapshot.anchor_frame_index,
        baseline_snapshot.anchor_frame_index
    );
    assert_eq!(mutated_snapshot.anchor_kind, baseline_snapshot.anchor_kind);
    assert_eq!(
        mutated_snapshot.export_directory_name,
        baseline_snapshot.export_directory_name
    );
    assert_eq!(
        mutated_snapshot.scoreboard_artifact_relative_path,
        baseline_snapshot.scoreboard_artifact_relative_path
    );
    assert_eq!(
        mutated_snapshot.teacher_artifact_relative_paths,
        baseline_snapshot.teacher_artifact_relative_paths
    );
    assert_eq!(
        mutated_snapshot.branch_ids_in_order,
        baseline_snapshot.branch_ids_in_order
    );
    assert_ne!(
        mutated_snapshot.scoreboard_rows_in_order,
        baseline_snapshot.scoreboard_rows_in_order
    );
    assert_ne!(
        mutated_snapshot.teacher_targets_in_order,
        baseline_snapshot.teacher_targets_in_order
    );
}

#[test]
fn second_deterministic_vertical_slice_explicitly_propagates_proposal_label_actions_legal_hint_and_metadata_into_exported_branch_payload_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_label = "candidate-delta";
    let baseline_actions = vec![
        ActionRecord {
            action_key: "jump".to_string(),
            fields: Metadata::from([("pressed", FieldValue::Boolean(false))]),
        },
        ActionRecord {
            action_key: "roll".to_string(),
            fields: Metadata::from([("direction", FieldValue::Float(0.75))]),
        },
    ];
    let baseline_legal_hint = None;
    let baseline_metadata = Metadata::from([(
        "proposal_source",
        FieldValue::Text("fixture-delta".to_string()),
    )]);
    let baseline_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        baseline_label,
        baseline_actions.clone(),
        baseline_legal_hint,
        baseline_metadata.clone(),
    );

    let mutated_label = "candidate-delta-stage101";
    let mutated_actions = vec![
        ActionRecord {
            action_key: "jump".to_string(),
            fields: Metadata::from([
                ("pressed", FieldValue::Boolean(true)),
                (
                    "stage101_action_tag",
                    FieldValue::Text("proposal-surface".to_string()),
                ),
            ]),
        },
        ActionRecord {
            action_key: "roll".to_string(),
            fields: Metadata::from([("direction", FieldValue::Float(-0.5))]),
        },
    ];
    let mutated_legal_hint = Some(true);
    let mutated_metadata = Metadata::from([
        (
            "proposal_contract_tag",
            FieldValue::Text("stage101-stage77-proposal-surface".to_string()),
        ),
        (
            "proposal_source",
            FieldValue::Text("fixture-delta-mutated".to_string()),
        ),
    ]);
    let mutated_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        mutated_label,
        mutated_actions.clone(),
        mutated_legal_hint,
        mutated_metadata.clone(),
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.proposals[1].label = mutated_label.to_string();
    expected_mutated_artifact.payload.proposals[1].actions = mutated_actions.clone();
    expected_mutated_artifact.payload.proposals[1].legal_hint = mutated_legal_hint;
    expected_mutated_artifact.payload.proposals[1].metadata = mutated_metadata.clone();
    assert_eq!(mutated_artifact, expected_mutated_artifact);
    assert_eq!(mutated_artifact.header, baseline_artifact.header);
    assert_eq!(
        mutated_artifact.payload.replay_id,
        baseline_artifact.payload.replay_id
    );
    assert_eq!(
        mutated_artifact.payload.export_name,
        baseline_artifact.payload.export_name
    );
    assert_eq!(
        mutated_artifact.payload.teacher_namespace,
        baseline_artifact.payload.teacher_namespace
    );
    assert_eq!(
        mutated_artifact.payload.simulation_seed,
        baseline_artifact.payload.simulation_seed
    );
    assert_eq!(
        mutated_artifact.payload.anchor_hint,
        baseline_artifact.payload.anchor_hint
    );
    assert_eq!(
        mutated_artifact.payload.proposals[0],
        baseline_artifact.payload.proposals[0]
    );
    assert_ne!(
        mutated_artifact.payload.proposals[1].label,
        baseline_artifact.payload.proposals[1].label
    );
    assert_ne!(
        mutated_artifact.payload.proposals[1].actions,
        baseline_artifact.payload.proposals[1].actions
    );
    assert_ne!(
        mutated_artifact.payload.proposals[1].legal_hint,
        baseline_artifact.payload.proposals[1].legal_hint
    );
    assert_ne!(
        mutated_artifact.payload.proposals[1].metadata,
        baseline_artifact.payload.proposals[1].metadata
    );
    assert_eq!(
        mutated_artifact.payload.proposals[1].score_signals,
        baseline_artifact.payload.proposals[1].score_signals
    );
    assert_eq!(
        mutated_artifact.payload.scorer_weights,
        baseline_artifact.payload.scorer_weights
    );

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage77 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage77 lane should reload canonically");

    assert_eq!(baseline.consumer_export.anchors.len(), 1);
    assert_eq!(mutated.consumer_export.anchors.len(), 1);
    assert_eq!(
        mutated.consumer_export.anchors[0],
        baseline.consumer_export.anchors[0]
    );

    assert_eq!(baseline.consumer_export.branches.len(), 2);
    assert_eq!(mutated.consumer_export.branches.len(), 2);
    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_branch_ids,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string()
        ]
    );
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    assert_eq!(
        baseline.consumer_export.branches[0],
        mutated.consumer_export.branches[0]
    );
    assert_eq!(
        baseline.consumer_export.branches[1].label.as_deref(),
        Some(baseline_label)
    );
    assert_eq!(
        baseline.consumer_export.branches[1].actions,
        baseline_actions
    );
    assert_eq!(
        baseline.consumer_export.branches[1].legality_hint,
        baseline_legal_hint
    );
    assert_eq!(
        baseline.consumer_export.branches[1].metadata,
        baseline_metadata
    );
    assert_eq!(
        mutated.consumer_export.branches[1].label.as_deref(),
        Some(mutated_label)
    );
    assert_eq!(mutated.consumer_export.branches[1].actions, mutated_actions);
    assert_eq!(
        mutated.consumer_export.branches[1].legality_hint,
        mutated_legal_hint
    );
    assert_eq!(
        mutated.consumer_export.branches[1].metadata,
        mutated_metadata
    );

    let baseline_rows = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.clone(),
                row.score.total,
            )
        })
        .collect::<Vec<_>>();
    let mutated_rows = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.clone(),
                row.score.total,
            )
        })
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_rows,
        vec![
            (
                "anchor-stage77-second:branch:0".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 5.0),
                    ("stability".to_string(), 1.0),
                ]),
                6.0,
            ),
            (
                "anchor-stage77-second:branch:1".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 2.0),
                    ("stability".to_string(), 0.5),
                ]),
                2.5,
            ),
        ]
    );
    assert_eq!(mutated_rows, baseline_rows);

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(
        baseline_teacher_targets,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string()
        ]
    );
    assert_eq!(mutated_teacher_targets, baseline_teacher_targets);

    let baseline_teacher_branch_zero = baseline
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:0"
            )
        })
        .expect("baseline branch zero teacher artifact should exist");
    let baseline_teacher_branch_one = baseline
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:1"
            )
        })
        .expect("baseline branch one teacher artifact should exist");
    let mutated_teacher_branch_zero = mutated
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:0"
            )
        })
        .expect("mutated branch zero teacher artifact should exist");
    let mutated_teacher_branch_one = mutated
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:1"
            )
        })
        .expect("mutated branch one teacher artifact should exist");

    assert_eq!(
        baseline_teacher_branch_zero.payload.id,
        mutated_teacher_branch_zero.payload.id
    );
    assert_eq!(
        baseline_teacher_branch_zero.payload.label,
        mutated_teacher_branch_zero.payload.label
    );
    assert_eq!(
        baseline_teacher_branch_zero.payload.score,
        mutated_teacher_branch_zero.payload.score
    );
    assert_eq!(
        baseline_teacher_branch_zero.payload.metadata,
        mutated_teacher_branch_zero.payload.metadata
    );
    assert_eq!(
        baseline_teacher_branch_one.payload.id,
        mutated_teacher_branch_one.payload.id
    );
    assert_eq!(
        baseline_teacher_branch_one.payload.score,
        mutated_teacher_branch_one.payload.score
    );
    assert_eq!(
        baseline_teacher_branch_one.payload.metadata,
        mutated_teacher_branch_one.payload.metadata
    );
    assert_eq!(baseline_teacher_branch_one.payload.label, baseline_label);
    assert_eq!(mutated_teacher_branch_one.payload.label, mutated_label);

    assert_eq!(
        baseline.consumer_export.manifest.export_name,
        mutated.consumer_export.manifest.export_name
    );
    assert_eq!(
        baseline.consumer_export.anchors[0].replay_id,
        mutated.consumer_export.anchors[0].replay_id
    );
}

#[test]
fn second_deterministic_vertical_slice_score_signals_directly_change_component_values_total_score_and_teacher_ordering_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_score_signals = BTreeMap::from([
        ("coverage".to_string(), 2.0),
        ("stability".to_string(), 1.0),
    ]);
    let mutated_score_signals = BTreeMap::from([
        ("coverage".to_string(), 6.0),
        ("stability".to_string(), 1.0),
    ]);
    let baseline_artifact = persisted_input_artifact_for_lane_with_proposal_score_signals(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        baseline_score_signals.clone(),
    );
    let mutated_artifact = persisted_input_artifact_for_lane_with_proposal_score_signals(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        mutated_score_signals.clone(),
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.proposals[1].score_signals = mutated_score_signals.clone();
    assert_eq!(mutated_artifact, expected_mutated_artifact);
    assert_eq!(mutated_artifact.header, baseline_artifact.header);
    assert_eq!(
        mutated_artifact.payload.replay_id,
        baseline_artifact.payload.replay_id
    );
    assert_eq!(
        mutated_artifact.payload.export_name,
        baseline_artifact.payload.export_name
    );
    assert_eq!(
        mutated_artifact.payload.teacher_namespace,
        baseline_artifact.payload.teacher_namespace
    );
    assert_eq!(
        mutated_artifact.payload.simulation_seed,
        baseline_artifact.payload.simulation_seed
    );
    assert_eq!(
        mutated_artifact.payload.anchor_hint,
        baseline_artifact.payload.anchor_hint
    );
    assert_eq!(
        mutated_artifact.payload.proposals[0],
        baseline_artifact.payload.proposals[0]
    );
    assert_eq!(
        mutated_artifact.payload.proposals[1].label,
        baseline_artifact.payload.proposals[1].label
    );
    assert_eq!(
        mutated_artifact.payload.proposals[1].actions,
        baseline_artifact.payload.proposals[1].actions
    );
    assert_eq!(
        mutated_artifact.payload.proposals[1].legal_hint,
        baseline_artifact.payload.proposals[1].legal_hint
    );
    assert_eq!(
        mutated_artifact.payload.proposals[1].metadata,
        baseline_artifact.payload.proposals[1].metadata
    );
    assert_ne!(
        mutated_artifact.payload.proposals[1].score_signals,
        baseline_artifact.payload.proposals[1].score_signals
    );
    assert_eq!(
        mutated_artifact.payload.scorer_weights,
        baseline_artifact.payload.scorer_weights
    );

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage77 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage77 lane should reload canonically");

    assert_eq!(baseline.consumer_export.anchors.len(), 1);
    assert_eq!(mutated.consumer_export.anchors.len(), 1);
    assert_eq!(
        mutated.consumer_export.anchors[0],
        baseline.consumer_export.anchors[0]
    );

    assert_eq!(baseline.consumer_export.branches.len(), 2);
    assert_eq!(mutated.consumer_export.branches.len(), 2);
    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_branch_ids,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string()
        ]
    );
    assert_eq!(mutated_branch_ids, baseline_branch_ids);
    assert_eq!(
        baseline.consumer_export.branches[0].actions,
        baseline_artifact.payload.proposals[0].actions
    );
    assert_eq!(
        baseline.consumer_export.branches[0].legality_hint,
        baseline_artifact.payload.proposals[0].legal_hint
    );
    assert_eq!(
        baseline.consumer_export.branches[0].metadata,
        baseline_artifact.payload.proposals[0].metadata
    );
    assert_eq!(
        mutated.consumer_export.branches[0].actions,
        baseline.consumer_export.branches[0].actions
    );
    assert_eq!(
        mutated.consumer_export.branches[0].legality_hint,
        baseline.consumer_export.branches[0].legality_hint
    );
    assert_eq!(
        mutated.consumer_export.branches[0].metadata,
        baseline.consumer_export.branches[0].metadata
    );
    assert_eq!(
        baseline.consumer_export.branches[1].actions,
        baseline_artifact.payload.proposals[1].actions
    );
    assert_eq!(
        baseline.consumer_export.branches[1].legality_hint,
        baseline_artifact.payload.proposals[1].legal_hint
    );
    assert_eq!(
        baseline.consumer_export.branches[1].metadata,
        baseline_artifact.payload.proposals[1].metadata
    );
    assert_eq!(
        mutated.consumer_export.branches[1].actions,
        baseline.consumer_export.branches[1].actions
    );
    assert_eq!(
        mutated.consumer_export.branches[1].legality_hint,
        baseline.consumer_export.branches[1].legality_hint
    );
    assert_eq!(
        mutated.consumer_export.branches[1].metadata,
        baseline.consumer_export.branches[1].metadata
    );

    let baseline_component_keys = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.keys().cloned().collect::<Vec<_>>(),
            )
        })
        .collect::<Vec<_>>();
    let mutated_component_keys = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.keys().cloned().collect::<Vec<_>>(),
            )
        })
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_component_keys,
        vec![
            (
                "anchor-stage77-second:branch:0".to_string(),
                vec!["coverage".to_string(), "stability".to_string()],
            ),
            (
                "anchor-stage77-second:branch:1".to_string(),
                vec!["coverage".to_string(), "stability".to_string()],
            ),
        ]
    );
    assert_eq!(mutated_component_keys, baseline_component_keys);

    let baseline_rows = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.clone(),
                row.score.total,
            )
        })
        .collect::<Vec<_>>();
    let mutated_rows = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.clone(),
                row.score.total,
            )
        })
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_rows,
        vec![
            (
                "anchor-stage77-second:branch:0".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 5.0),
                    ("stability".to_string(), 1.0),
                ]),
                6.0,
            ),
            (
                "anchor-stage77-second:branch:1".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 2.0),
                    ("stability".to_string(), 0.5),
                ]),
                2.5,
            ),
        ]
    );
    assert_eq!(
        mutated_rows,
        vec![
            (
                "anchor-stage77-second:branch:0".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 5.0),
                    ("stability".to_string(), 1.0),
                ]),
                6.0,
            ),
            (
                "anchor-stage77-second:branch:1".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 6.0),
                    ("stability".to_string(), 0.5),
                ]),
                6.5,
            ),
        ]
    );
    assert_eq!(mutated_rows[0], baseline_rows[0]);
    assert_ne!(mutated_rows[1], baseline_rows[1]);

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(
        baseline_teacher_targets,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string()
        ]
    );
    assert_eq!(
        mutated_teacher_targets,
        vec![
            "anchor-stage77-second:branch:1".to_string(),
            "anchor-stage77-second:branch:0".to_string()
        ]
    );

    let baseline_teacher_ids = baseline
        .teacher_artifacts
        .iter()
        .map(|artifact| artifact.payload.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_teacher_ids = mutated
        .teacher_artifacts
        .iter()
        .map(|artifact| artifact.payload.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_teacher_ids,
        vec![
            "stage77-second-vertical-slice:teacher:0".to_string(),
            "stage77-second-vertical-slice:teacher:1".to_string(),
        ]
    );
    assert_eq!(
        mutated_teacher_ids,
        vec![
            "stage77-second-vertical-slice:teacher:1".to_string(),
            "stage77-second-vertical-slice:teacher:0".to_string(),
        ]
    );

    let baseline_teacher_branch_zero = baseline
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:0"
            )
        })
        .expect("baseline branch zero teacher artifact should exist");
    let baseline_teacher_branch_one = baseline
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:1"
            )
        })
        .expect("baseline branch one teacher artifact should exist");
    let mutated_teacher_branch_zero = mutated
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:0"
            )
        })
        .expect("mutated branch zero teacher artifact should exist");
    let mutated_teacher_branch_one = mutated
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:1"
            )
        })
        .expect("mutated branch one teacher artifact should exist");

    for artifact in &baseline.teacher_artifacts {
        assert_eq!(
            artifact.header.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text("stage77.second.teacher".to_string()))
        );
    }
    for artifact in &mutated.teacher_artifacts {
        assert_eq!(
            artifact.header.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text("stage77.second.teacher".to_string()))
        );
    }

    assert_eq!(
        baseline_teacher_branch_zero.payload.id.as_str(),
        "stage77-second-vertical-slice:teacher:0"
    );
    assert_eq!(
        baseline_teacher_branch_zero.payload.label,
        "candidate-gamma"
    );
    assert_eq!(baseline_teacher_branch_zero.payload.score, Some(6.0));
    assert_eq!(
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace"),
        Some(&FieldValue::Text("stage77.second.teacher".to_string()))
    );
    assert_eq!(
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace_copy"),
        Some(&FieldValue::Text("stage77.second.teacher".to_string()))
    );
    assert_eq!(
        baseline_teacher_branch_zero.payload.metadata.get("ordinal"),
        Some(&FieldValue::Integer(0))
    );
    assert_eq!(
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_rank"),
        Some(&FieldValue::Integer(0))
    );

    assert_eq!(
        mutated_teacher_branch_zero.payload.id,
        baseline_teacher_branch_zero.payload.id
    );
    assert_eq!(
        mutated_teacher_branch_zero.payload.label,
        baseline_teacher_branch_zero.payload.label
    );
    assert_eq!(
        mutated_teacher_branch_zero.payload.score,
        baseline_teacher_branch_zero.payload.score
    );
    assert_eq!(
        mutated_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace"),
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace")
    );
    assert_eq!(
        mutated_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace_copy"),
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace_copy")
    );
    assert_eq!(
        mutated_teacher_branch_zero.payload.metadata.get("ordinal"),
        baseline_teacher_branch_zero.payload.metadata.get("ordinal")
    );
    assert_eq!(
        mutated_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_rank"),
        Some(&FieldValue::Integer(1))
    );

    assert_eq!(
        baseline_teacher_branch_one.payload.id.as_str(),
        "stage77-second-vertical-slice:teacher:1"
    );
    assert_eq!(baseline_teacher_branch_one.payload.label, "candidate-delta");
    assert_eq!(baseline_teacher_branch_one.payload.score, Some(2.5));
    assert_eq!(
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace"),
        Some(&FieldValue::Text("stage77.second.teacher".to_string()))
    );
    assert_eq!(
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace_copy"),
        Some(&FieldValue::Text("stage77.second.teacher".to_string()))
    );
    assert_eq!(
        baseline_teacher_branch_one.payload.metadata.get("ordinal"),
        Some(&FieldValue::Integer(1))
    );
    assert_eq!(
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_rank"),
        Some(&FieldValue::Integer(1))
    );

    assert_eq!(
        mutated_teacher_branch_one.payload.id,
        baseline_teacher_branch_one.payload.id
    );
    assert_eq!(
        mutated_teacher_branch_one.payload.label,
        baseline_teacher_branch_one.payload.label
    );
    assert_eq!(mutated_teacher_branch_one.payload.score, Some(6.5));
    assert_eq!(
        mutated_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace"),
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace")
    );
    assert_eq!(
        mutated_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace_copy"),
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace_copy")
    );
    assert_eq!(
        mutated_teacher_branch_one.payload.metadata.get("ordinal"),
        baseline_teacher_branch_one.payload.metadata.get("ordinal")
    );
    assert_eq!(
        mutated_teacher_branch_one
            .payload
            .metadata
            .get("teacher_rank"),
        Some(&FieldValue::Integer(0))
    );

    let expected_snapshot =
        expected_golden_snapshot_for_lane(VerticalSliceFixtureLane::Stage77Second);
    let baseline_snapshot = load_snapshot(baseline_directory.path())
        .expect("baseline stage77 lane should load the frozen snapshot");
    let mutated_snapshot = load_snapshot(mutated_directory.path())
        .expect("mutated stage77 lane should load the frozen snapshot");
    assert_eq!(baseline_snapshot, expected_snapshot);
    assert_eq!(mutated_snapshot.export_name, baseline_snapshot.export_name);
    assert_eq!(mutated_snapshot.replay_id, baseline_snapshot.replay_id);
    assert_eq!(mutated_snapshot.anchor_id, baseline_snapshot.anchor_id);
    assert_eq!(
        mutated_snapshot.anchor_frame_index,
        baseline_snapshot.anchor_frame_index
    );
    assert_eq!(mutated_snapshot.anchor_kind, baseline_snapshot.anchor_kind);
    assert_eq!(
        mutated_snapshot.export_directory_name,
        baseline_snapshot.export_directory_name
    );
    assert_eq!(
        mutated_snapshot.scoreboard_artifact_relative_path,
        baseline_snapshot.scoreboard_artifact_relative_path
    );
    assert_eq!(
        mutated_snapshot.teacher_artifact_relative_paths,
        baseline_snapshot.teacher_artifact_relative_paths
    );
    assert_eq!(
        mutated_snapshot.branch_ids_in_order,
        baseline_snapshot.branch_ids_in_order
    );
    assert_eq!(
        mutated_snapshot.scoreboard_rows_in_order,
        vec![
            VerticalSliceGoldenScoreboardRow {
                branch_id: "anchor-stage77-second:branch:0".to_string(),
                total_score: 6.0,
            },
            VerticalSliceGoldenScoreboardRow {
                branch_id: "anchor-stage77-second:branch:1".to_string(),
                total_score: 6.5,
            },
        ]
    );
    assert_eq!(
        mutated_snapshot.teacher_targets_in_order,
        vec![
            "anchor-stage77-second:branch:1".to_string(),
            "anchor-stage77-second:branch:0".to_string()
        ]
    );
}

#[test]
fn second_deterministic_vertical_slice_scorer_weights_directly_change_component_values_total_score_and_teacher_ordering_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_artifact = persisted_input_artifact_for_lane_with_scorer_weights(
        VerticalSliceFixtureLane::Stage77Second,
        BTreeMap::from([
            ("coverage".to_string(), 1.0),
            ("stability".to_string(), 0.5),
        ]),
    );
    let mutated_artifact = persisted_input_artifact_for_lane_with_scorer_weights(
        VerticalSliceFixtureLane::Stage77Second,
        BTreeMap::from([
            ("coverage".to_string(), 1.0),
            ("stability".to_string(), -4.0),
        ]),
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.scorer_weights = BTreeMap::from([
        ("coverage".to_string(), 1.0),
        ("stability".to_string(), -4.0),
    ]);
    assert_eq!(mutated_artifact, expected_mutated_artifact);
    assert_eq!(mutated_artifact.header, baseline_artifact.header);
    assert_eq!(
        mutated_artifact.payload.replay_id,
        baseline_artifact.payload.replay_id
    );
    assert_eq!(
        mutated_artifact.payload.export_name,
        baseline_artifact.payload.export_name
    );
    assert_eq!(
        mutated_artifact.payload.teacher_namespace,
        baseline_artifact.payload.teacher_namespace
    );
    assert_eq!(
        mutated_artifact.payload.simulation_seed,
        baseline_artifact.payload.simulation_seed
    );
    assert_eq!(
        mutated_artifact.payload.anchor_hint,
        baseline_artifact.payload.anchor_hint
    );
    assert_eq!(
        mutated_artifact.payload.proposals,
        baseline_artifact.payload.proposals
    );
    assert_ne!(
        mutated_artifact.payload.scorer_weights,
        baseline_artifact.payload.scorer_weights
    );

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage77 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage77 lane should reload canonically");

    assert_eq!(baseline.consumer_export.anchors.len(), 1);
    assert_eq!(mutated.consumer_export.anchors.len(), 1);
    assert_eq!(
        mutated.consumer_export.anchors[0],
        baseline.consumer_export.anchors[0]
    );

    assert_eq!(baseline.consumer_export.branches.len(), 2);
    assert_eq!(mutated.consumer_export.branches.len(), 2);
    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_branch_ids,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string()
        ]
    );
    assert_eq!(mutated_branch_ids, baseline_branch_ids);
    assert_eq!(
        mutated.consumer_export.branches[0].actions,
        baseline.consumer_export.branches[0].actions
    );
    assert_eq!(
        mutated.consumer_export.branches[0].legality_hint,
        baseline.consumer_export.branches[0].legality_hint
    );
    assert_eq!(
        mutated.consumer_export.branches[0].metadata,
        baseline.consumer_export.branches[0].metadata
    );
    assert_eq!(
        mutated.consumer_export.branches[1].actions,
        baseline.consumer_export.branches[1].actions
    );
    assert_eq!(
        mutated.consumer_export.branches[1].legality_hint,
        baseline.consumer_export.branches[1].legality_hint
    );
    assert_eq!(
        mutated.consumer_export.branches[1].metadata,
        baseline.consumer_export.branches[1].metadata
    );

    let baseline_component_keys = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.keys().cloned().collect::<Vec<_>>(),
            )
        })
        .collect::<Vec<_>>();
    let mutated_component_keys = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.keys().cloned().collect::<Vec<_>>(),
            )
        })
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_component_keys,
        vec![
            (
                "anchor-stage77-second:branch:0".to_string(),
                vec!["coverage".to_string(), "stability".to_string()],
            ),
            (
                "anchor-stage77-second:branch:1".to_string(),
                vec!["coverage".to_string(), "stability".to_string()],
            ),
        ]
    );
    assert_eq!(mutated_component_keys, baseline_component_keys);

    let baseline_rows = baseline
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.clone(),
                row.score.total,
            )
        })
        .collect::<Vec<_>>();
    let mutated_rows = mutated
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .map(|row| {
            (
                row.branch_id.as_str().to_string(),
                row.score.components.clone(),
                row.score.total,
            )
        })
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_rows,
        vec![
            (
                "anchor-stage77-second:branch:0".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 5.0),
                    ("stability".to_string(), 1.0),
                ]),
                6.0,
            ),
            (
                "anchor-stage77-second:branch:1".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 2.0),
                    ("stability".to_string(), 0.5),
                ]),
                2.5,
            ),
        ]
    );
    assert_eq!(
        mutated_rows,
        vec![
            (
                "anchor-stage77-second:branch:0".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 5.0),
                    ("stability".to_string(), -8.0),
                ]),
                -3.0,
            ),
            (
                "anchor-stage77-second:branch:1".to_string(),
                BTreeMap::from([
                    ("coverage".to_string(), 2.0),
                    ("stability".to_string(), -4.0),
                ]),
                -2.0,
            ),
        ]
    );
    assert_eq!(
        mutated_rows
            .iter()
            .map(|(branch_id, components, _)| {
                (
                    branch_id.clone(),
                    components
                        .get("coverage")
                        .copied()
                        .expect("coverage exists"),
                )
            })
            .collect::<Vec<_>>(),
        baseline_rows
            .iter()
            .map(|(branch_id, components, _)| {
                (
                    branch_id.clone(),
                    components
                        .get("coverage")
                        .copied()
                        .expect("coverage exists"),
                )
            })
            .collect::<Vec<_>>()
    );
    assert_ne!(
        mutated_rows
            .iter()
            .map(|(branch_id, components, _)| {
                (
                    branch_id.clone(),
                    components
                        .get("stability")
                        .copied()
                        .expect("stability exists"),
                )
            })
            .collect::<Vec<_>>(),
        baseline_rows
            .iter()
            .map(|(branch_id, components, _)| {
                (
                    branch_id.clone(),
                    components
                        .get("stability")
                        .copied()
                        .expect("stability exists"),
                )
            })
            .collect::<Vec<_>>()
    );

    let baseline_teacher_targets = baseline
        .teacher_branch_targets_in_order()
        .expect("baseline teacher targets should stay branch-typed");
    let mutated_teacher_targets = mutated
        .teacher_branch_targets_in_order()
        .expect("mutated teacher targets should stay branch-typed");
    assert_eq!(
        baseline_teacher_targets,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string()
        ]
    );
    assert_eq!(
        mutated_teacher_targets,
        vec![
            "anchor-stage77-second:branch:1".to_string(),
            "anchor-stage77-second:branch:0".to_string()
        ]
    );

    let baseline_teacher_ids = baseline
        .teacher_artifacts
        .iter()
        .map(|artifact| artifact.payload.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_teacher_ids = mutated
        .teacher_artifacts
        .iter()
        .map(|artifact| artifact.payload.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_teacher_ids,
        vec![
            "stage77-second-vertical-slice:teacher:0".to_string(),
            "stage77-second-vertical-slice:teacher:1".to_string(),
        ]
    );
    assert_eq!(
        mutated_teacher_ids,
        vec![
            "stage77-second-vertical-slice:teacher:1".to_string(),
            "stage77-second-vertical-slice:teacher:0".to_string(),
        ]
    );

    let baseline_teacher_branch_zero = baseline
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:0"
            )
        })
        .expect("baseline branch zero teacher artifact should exist");
    let baseline_teacher_branch_one = baseline
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:1"
            )
        })
        .expect("baseline branch one teacher artifact should exist");
    let mutated_teacher_branch_zero = mutated
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:0"
            )
        })
        .expect("mutated branch zero teacher artifact should exist");
    let mutated_teacher_branch_one = mutated
        .teacher_artifacts
        .iter()
        .find(|artifact| {
            matches!(
                &artifact.payload.target,
                TeacherLabelTarget::Branch(branch_id)
                    if branch_id.as_str() == "anchor-stage77-second:branch:1"
            )
        })
        .expect("mutated branch one teacher artifact should exist");

    for artifact in &baseline.teacher_artifacts {
        assert_eq!(
            artifact.header.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text("stage77.second.teacher".to_string()))
        );
    }
    for artifact in &mutated.teacher_artifacts {
        assert_eq!(
            artifact.header.metadata.get("teacher_namespace"),
            Some(&FieldValue::Text("stage77.second.teacher".to_string()))
        );
    }

    assert_eq!(
        baseline_teacher_branch_zero.payload.id.as_str(),
        "stage77-second-vertical-slice:teacher:0"
    );
    assert_eq!(
        baseline_teacher_branch_zero.payload.label,
        "candidate-gamma"
    );
    assert_eq!(baseline_teacher_branch_zero.payload.score, Some(6.0));
    assert_eq!(
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace"),
        Some(&FieldValue::Text("stage77.second.teacher".to_string()))
    );
    assert_eq!(
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace_copy"),
        Some(&FieldValue::Text("stage77.second.teacher".to_string()))
    );
    assert_eq!(
        baseline_teacher_branch_zero.payload.metadata.get("ordinal"),
        Some(&FieldValue::Integer(0))
    );
    assert_eq!(
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_rank"),
        Some(&FieldValue::Integer(0))
    );

    assert_eq!(
        mutated_teacher_branch_zero.payload.id,
        baseline_teacher_branch_zero.payload.id
    );
    assert_eq!(
        mutated_teacher_branch_zero.payload.label,
        baseline_teacher_branch_zero.payload.label
    );
    assert_eq!(mutated_teacher_branch_zero.payload.score, Some(-3.0));
    assert_eq!(
        mutated_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace"),
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace")
    );
    assert_eq!(
        mutated_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace_copy"),
        baseline_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_namespace_copy")
    );
    assert_eq!(
        mutated_teacher_branch_zero.payload.metadata.get("ordinal"),
        baseline_teacher_branch_zero.payload.metadata.get("ordinal")
    );
    assert_eq!(
        mutated_teacher_branch_zero
            .payload
            .metadata
            .get("teacher_rank"),
        Some(&FieldValue::Integer(1))
    );

    assert_eq!(
        baseline_teacher_branch_one.payload.id.as_str(),
        "stage77-second-vertical-slice:teacher:1"
    );
    assert_eq!(baseline_teacher_branch_one.payload.label, "candidate-delta");
    assert_eq!(baseline_teacher_branch_one.payload.score, Some(2.5));
    assert_eq!(
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace"),
        Some(&FieldValue::Text("stage77.second.teacher".to_string()))
    );
    assert_eq!(
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace_copy"),
        Some(&FieldValue::Text("stage77.second.teacher".to_string()))
    );
    assert_eq!(
        baseline_teacher_branch_one.payload.metadata.get("ordinal"),
        Some(&FieldValue::Integer(1))
    );
    assert_eq!(
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_rank"),
        Some(&FieldValue::Integer(1))
    );

    assert_eq!(
        mutated_teacher_branch_one.payload.id,
        baseline_teacher_branch_one.payload.id
    );
    assert_eq!(
        mutated_teacher_branch_one.payload.label,
        baseline_teacher_branch_one.payload.label
    );
    assert_eq!(mutated_teacher_branch_one.payload.score, Some(-2.0));
    assert_eq!(
        mutated_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace"),
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace")
    );
    assert_eq!(
        mutated_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace_copy"),
        baseline_teacher_branch_one
            .payload
            .metadata
            .get("teacher_namespace_copy")
    );
    assert_eq!(
        mutated_teacher_branch_one.payload.metadata.get("ordinal"),
        baseline_teacher_branch_one.payload.metadata.get("ordinal")
    );
    assert_eq!(
        mutated_teacher_branch_one
            .payload
            .metadata
            .get("teacher_rank"),
        Some(&FieldValue::Integer(0))
    );

    let expected_snapshot =
        expected_golden_snapshot_for_lane(VerticalSliceFixtureLane::Stage77Second);
    let baseline_snapshot = load_snapshot(baseline_directory.path())
        .expect("baseline stage77 lane should load the frozen snapshot");
    let mutated_snapshot = load_snapshot(mutated_directory.path())
        .expect("mutated stage77 lane should load the frozen snapshot");
    assert_eq!(baseline_snapshot, expected_snapshot);
    assert_eq!(mutated_snapshot.export_name, baseline_snapshot.export_name);
    assert_eq!(mutated_snapshot.replay_id, baseline_snapshot.replay_id);
    assert_eq!(mutated_snapshot.anchor_id, baseline_snapshot.anchor_id);
    assert_eq!(
        mutated_snapshot.anchor_frame_index,
        baseline_snapshot.anchor_frame_index
    );
    assert_eq!(mutated_snapshot.anchor_kind, baseline_snapshot.anchor_kind);
    assert_eq!(
        mutated_snapshot.export_directory_name,
        baseline_snapshot.export_directory_name
    );
    assert_eq!(
        mutated_snapshot.scoreboard_artifact_relative_path,
        baseline_snapshot.scoreboard_artifact_relative_path
    );
    assert_eq!(
        mutated_snapshot.teacher_artifact_relative_paths,
        baseline_snapshot.teacher_artifact_relative_paths
    );
    assert_eq!(
        mutated_snapshot.branch_ids_in_order,
        baseline_snapshot.branch_ids_in_order
    );
    assert_eq!(
        mutated_snapshot.scoreboard_rows_in_order,
        vec![
            VerticalSliceGoldenScoreboardRow {
                branch_id: "anchor-stage77-second:branch:0".to_string(),
                total_score: -3.0,
            },
            VerticalSliceGoldenScoreboardRow {
                branch_id: "anchor-stage77-second:branch:1".to_string(),
                total_score: -2.0,
            },
        ]
    );
    assert_eq!(
        mutated_snapshot.teacher_targets_in_order,
        vec![
            "anchor-stage77-second:branch:1".to_string(),
            "anchor-stage77-second:branch:0".to_string()
        ]
    );
}

#[test]
fn deterministic_vertical_slice_matches_frozen_stage73_golden_snapshot() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_matches_expected_contract(
        directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("stage69 fixture should satisfy the shared parity contract");
}

#[test]
fn deterministic_vertical_slice_repeated_runs_match_frozen_stage73_golden_snapshot() {
    let first = tempdir().expect("tempdir should be created");
    let second = tempdir().expect("tempdir should be created");
    assert_fixture_lane_repeated_runs_are_identical(
        first.path(),
        second.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("stage69 repeated runs should satisfy the shared parity contract");
}

#[test]
fn canonical_vertical_slice_snapshot_detects_persisted_scoreboard_order_drift() {
    let directory = tempdir().expect("tempdir should be created");
    run_sample_fixture(directory.path()).expect("vertical slice should succeed");

    let mut scoreboard_artifact = load_result(directory.path()).expect("result should reload");
    scoreboard_artifact
        .scoreboard_artifact
        .payload
        .rows
        .swap(0, 1);
    rewrite_scoreboard_artifact(directory.path(), &scoreboard_artifact.scoreboard_artifact)
        .expect("drifted scoreboard should rewrite");

    let snapshot = load_snapshot(directory.path())
        .expect("snapshot should build from drifted canonical result");

    assert_ne!(snapshot, expected_stage73_golden_snapshot());
    assert_eq!(
        snapshot.scoreboard_rows_in_order,
        vec![
            VerticalSliceGoldenScoreboardRow {
                branch_id: "anchor-stage69:branch:1".to_string(),
                total_score: 5.0,
            },
            VerticalSliceGoldenScoreboardRow {
                branch_id: "anchor-stage69:branch:0".to_string(),
                total_score: 3.5,
            },
        ]
    );
}

#[test]
fn canonical_vertical_slice_result_loader_fails_explicitly_on_scoreboard_row_count_drift() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_scoreboard_row_count_drift_fails_explicitly(
        directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("stage69 scoreboard row drift should fail explicitly");
}

#[test]
fn canonical_vertical_slice_result_loader_fails_explicitly_on_extra_teacher_artifact_drift() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_extra_teacher_artifact_count_drift_fails_explicitly(
        directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("stage69 extra teacher artifact drift should fail explicitly");
}

#[test]
fn canonical_vertical_slice_teacher_targets_fail_explicitly_on_non_branch_target_drift() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_non_branch_teacher_target_drift_fails_explicitly(
        directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
        "replay-drifted-away-from-branch-contract",
    )
    .expect("stage69 non-branch teacher target drift should fail explicitly");
}

#[test]
fn canonical_vertical_slice_snapshot_detects_teacher_artifact_ordinal_file_drift() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_teacher_artifact_ordinal_file_drift_changes_snapshot(
        directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("stage69 teacher ordinal file drift should change the snapshot");
}

#[test]
fn canonical_vertical_slice_snapshot_fails_explicitly_when_anchor_count_is_not_one() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_snapshot_fails_explicitly_when_anchor_count_is_not_one(
        directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
    )
    .expect("stage69 duplicate anchor drift should fail explicitly");
}

#[test]
fn canonical_vertical_slice_result_loader_fails_explicitly_when_required_artifact_is_missing() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_missing_teacher_artifact_fails_explicitly(
        directory.path(),
        VerticalSliceFixtureLane::Stage69Sample,
        1,
    )
    .expect("stage69 missing teacher artifact drift should fail explicitly");
}

#[test]
fn deterministic_vertical_slice_fails_explicitly_without_fake_backend() {
    let directory = tempdir().expect("tempdir should be created");
    let error = run_deterministic_vertical_slice(directory.path(), &sample_fixture(), None)
        .expect_err("vertical slice should reject missing fake backend");

    assert_eq!(
        error.to_string(),
        "deterministic vertical slice requires deterministic fake backend"
    );
}

#[test]
fn second_deterministic_vertical_slice_persists_reloadable_outputs() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_matches_expected_contract(
        directory.path(),
        VerticalSliceFixtureLane::Stage77Second,
    )
    .expect("stage77 second fixture should satisfy the shared parity contract");
}

#[test]
fn second_deterministic_vertical_slice_matches_its_frozen_golden_snapshot() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_matches_expected_contract(
        directory.path(),
        VerticalSliceFixtureLane::Stage77Second,
    )
    .expect("stage77 second fixture should satisfy the shared parity contract");
}

#[test]
fn second_deterministic_vertical_slice_is_identical_across_repeated_runs() {
    let first = tempdir().expect("tempdir should be created");
    let second = tempdir().expect("tempdir should be created");
    assert_fixture_lane_repeated_runs_are_identical(
        first.path(),
        second.path(),
        VerticalSliceFixtureLane::Stage77Second,
    )
    .expect("stage77 second repeated runs should satisfy the shared parity contract");
}

#[test]
fn second_deterministic_vertical_slice_loader_fails_explicitly_on_scoreboard_row_count_drift() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_scoreboard_row_count_drift_fails_explicitly(
        directory.path(),
        VerticalSliceFixtureLane::Stage77Second,
    )
    .expect("stage77 second scoreboard row drift should fail explicitly");
}

#[test]
fn second_deterministic_vertical_slice_detects_explicit_scoreboard_component_schema_drift() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_scoreboard_component_schema_drift_fails_explicitly(
        directory.path(),
        VerticalSliceFixtureLane::Stage77Second,
    )
    .expect("stage77 second scoreboard component drift should fail explicitly");
}

#[test]
fn second_deterministic_vertical_slice_snapshot_detects_teacher_artifact_ordinal_file_drift() {
    let directory = tempdir().expect("tempdir should be created");
    assert_fixture_lane_teacher_artifact_ordinal_file_drift_changes_snapshot(
        directory.path(),
        VerticalSliceFixtureLane::Stage77Second,
    )
    .expect("stage77 second teacher ordinal file drift should change the snapshot");
}

#[test]
fn second_deterministic_vertical_slice_directly_consumes_simulation_seed_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_artifact = persisted_input_artifact_for_lane_with_simulation_seed(
        VerticalSliceFixtureLane::Stage77Second,
        77,
    );
    let mutated_seed = 7701;
    let mutated_artifact = persisted_input_artifact_for_lane_with_simulation_seed(
        VerticalSliceFixtureLane::Stage77Second,
        mutated_seed,
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.simulation_seed = mutated_seed;
    assert_eq!(mutated_artifact, expected_mutated_artifact);
    assert_eq!(mutated_artifact.header, baseline_artifact.header);
    assert_eq!(
        mutated_artifact.payload.replay_id,
        baseline_artifact.payload.replay_id
    );
    assert_eq!(
        mutated_artifact.payload.export_name,
        baseline_artifact.payload.export_name
    );
    assert_eq!(
        mutated_artifact.payload.teacher_namespace,
        baseline_artifact.payload.teacher_namespace
    );
    assert_eq!(
        mutated_artifact.payload.anchor_hint,
        baseline_artifact.payload.anchor_hint
    );
    assert_eq!(
        mutated_artifact.payload.proposals,
        baseline_artifact.payload.proposals
    );
    assert_eq!(
        mutated_artifact.payload.scorer_weights,
        baseline_artifact.payload.scorer_weights
    );
    assert_ne!(
        mutated_artifact.payload.simulation_seed,
        baseline_artifact.payload.simulation_seed
    );

    let (baseline_output, baseline, baseline_requests) =
        run_persisted_input_artifact_and_capture_simulation_requests(
            baseline_directory.path(),
            &baseline_artifact,
        )
        .expect("baseline stage77 lane should capture consumed simulation requests");
    let (mutated_output, mutated, mutated_requests) =
        run_persisted_input_artifact_and_capture_simulation_requests(
            mutated_directory.path(),
            &mutated_artifact,
        )
        .expect("mutated stage77 lane should capture consumed simulation requests");

    let baseline_request_ids = baseline_requests
        .iter()
        .map(|request| request.simulation_id.clone())
        .collect::<Vec<_>>();
    let mutated_request_ids = mutated_requests
        .iter()
        .map(|request| request.simulation_id.clone())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_request_ids,
        vec![
            "anchor-stage77-second:branch:0:deterministic-vertical-slice".to_string(),
            "anchor-stage77-second:branch:1:deterministic-vertical-slice".to_string(),
        ]
    );
    assert_eq!(mutated_request_ids, baseline_request_ids);
    assert_eq!(
        baseline_requests
            .iter()
            .map(|request| request.seed)
            .collect::<Vec<_>>(),
        vec![77, 77]
    );
    assert_eq!(
        mutated_requests
            .iter()
            .map(|request| request.seed)
            .collect::<Vec<_>>(),
        vec![mutated_seed, mutated_seed]
    );

    assert_eq!(
        baseline_output.manifest.export_name,
        "stage77-second-vertical-slice"
    );
    assert_eq!(
        mutated_output.manifest.export_name,
        baseline_output.manifest.export_name
    );
    assert_eq!(
        baseline_output.consumer_export.anchors,
        mutated_output.consumer_export.anchors
    );
    assert_eq!(
        baseline_output.consumer_export.branches,
        mutated_output.consumer_export.branches
    );
    assert_eq!(baseline.consumer_export, mutated.consumer_export);
    assert_eq!(baseline.teacher_artifacts, mutated.teacher_artifacts);
    assert_eq!(
        baseline_output.teacher_artifacts,
        mutated_output.teacher_artifacts
    );

    let baseline_branch_ids = baseline
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    let mutated_branch_ids = mutated
        .consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();
    assert_eq!(
        baseline_branch_ids,
        vec![
            "anchor-stage77-second:branch:0".to_string(),
            "anchor-stage77-second:branch:1".to_string(),
        ]
    );
    assert_eq!(mutated_branch_ids, baseline_branch_ids);

    assert_eq!(
        baseline_output
            .scoreboard
            .rows
            .iter()
            .map(|row| row.branch_id.as_str().to_string())
            .collect::<Vec<_>>(),
        mutated_output
            .scoreboard
            .rows
            .iter()
            .map(|row| row.branch_id.as_str().to_string())
            .collect::<Vec<_>>()
    );
    assert_eq!(
        baseline_output
            .scoreboard
            .rows
            .iter()
            .map(|row| row.score.clone())
            .collect::<Vec<_>>(),
        mutated_output
            .scoreboard
            .rows
            .iter()
            .map(|row| row.score.clone())
            .collect::<Vec<_>>()
    );
    assert_ne!(
        baseline_output
            .scoreboard
            .rows
            .iter()
            .map(|row| row.step_hashes.clone())
            .collect::<Vec<_>>(),
        mutated_output
            .scoreboard
            .rows
            .iter()
            .map(|row| row.step_hashes.clone())
            .collect::<Vec<_>>()
    );
    assert_eq!(
        baseline.scoreboard_artifact.payload.rows,
        baseline_output.scoreboard.rows
    );
    assert_eq!(
        mutated.scoreboard_artifact.payload.rows,
        mutated_output.scoreboard.rows
    );
}

#[cfg(test)]
fn read_json_value(path: &Path) -> Value {
    serde_json::from_slice(&fs::read(path).expect("json file should be readable"))
        .expect("json file should parse")
}

#[cfg(test)]
fn write_json_value(path: &Path, value: &Value) {
    fs::write(
        path,
        serde_json::to_vec_pretty(value).expect("json value should serialize"),
    )
    .expect("json value should be written");
}

#[cfg(test)]
fn stage77_branch_artifact_path(output_dir: &Path, branch_id: &str) -> PathBuf {
    let export_dir = output_dir.join(VERTICAL_SLICE_EXPORT_DIR_NAME);
    let inspection =
        inspect_export_bundle(&export_dir).expect("stage77 export bundle should inspect");
    let entry = inspection
        .index
        .entries
        .iter()
        .find(|entry| entry.record_id == branch_id)
        .expect("stage77 branch index entry should exist");
    export_dir.join(&entry.relative_path)
}

#[cfg(test)]
fn refresh_stage77_branch_index_hash(output_dir: &Path, branch_id: &str) -> Result<()> {
    let branch_path = stage77_branch_artifact_path(output_dir, branch_id);
    let branch_artifact: mimir_types::PersistedBranchArtifact =
        read_artifact_auto(&branch_path, ArtifactKind::Branch.schema())?;
    let content_hash = hash_serializable(&branch_artifact)?;
    let index_path = output_dir
        .join(VERTICAL_SLICE_EXPORT_DIR_NAME)
        .join(EXPORT_INDEX_FILE_NAME);
    let mut index_value = read_json_value(&index_path);
    let entries = index_value["entries"]
        .as_array_mut()
        .expect("export index entries should be an array");
    let entry = entries
        .iter_mut()
        .find(|entry| entry["record_id"].as_str() == Some(branch_id))
        .expect("stage77 branch index entry should exist");
    entry["content_hash"] = Value::String(content_hash);
    write_json_value(&index_path, &index_value);
    Ok(())
}

#[cfg(test)]
fn simulation_commands_from_actions(actions: &[ActionRecord]) -> Vec<SimulationCommand> {
    actions
        .iter()
        .map(|action| SimulationCommand {
            label: action.action_key.clone(),
            metadata: action.fields.clone(),
        })
        .collect()
}

#[cfg(test)]
fn assert_branch_payload_surface_matches(
    branches: &[BranchRecord],
    branch_id: &str,
    expected_label: Option<&str>,
    expected_actions: &[ActionRecord],
    expected_legality_hint: Option<bool>,
    expected_metadata: &Metadata,
) -> Result<()> {
    let branch = branches
        .iter()
        .find(|branch| branch.id.as_str() == branch_id)
        .ok_or_else(|| {
            MimirError::message(format!(
                "vertical-slice branch payload drift: missing branch {branch_id}"
            ))
        })?;

    if branch.label.as_deref() != expected_label {
        return Err(MimirError::message(format!(
            "vertical-slice branch payload drift: branch {branch_id}, expected label {:?}, found {:?}",
            expected_label, branch.label
        )));
    }
    if branch.actions != expected_actions {
        return Err(MimirError::message(format!(
            "vertical-slice branch payload drift: branch {branch_id}, expected actions {:?}, found {:?}",
            expected_actions, branch.actions
        )));
    }
    if branch.legality_hint != expected_legality_hint {
        return Err(MimirError::message(format!(
            "vertical-slice branch payload drift: branch {branch_id}, expected legality_hint {:?}, found {:?}",
            expected_legality_hint, branch.legality_hint
        )));
    }
    if &branch.metadata != expected_metadata {
        return Err(MimirError::message(format!(
            "vertical-slice branch payload drift: branch {branch_id}, expected metadata {:?}, found {:?}",
            expected_metadata, branch.metadata
        )));
    }

    Ok(())
}

#[test]
fn second_deterministic_vertical_slice_preserves_branch_metadata_value_shapes_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_label = "candidate-delta";
    let baseline_actions = vec![
        ActionRecord {
            action_key: "jump".to_string(),
            fields: Metadata::from([("pressed", FieldValue::Boolean(false))]),
        },
        ActionRecord {
            action_key: "roll".to_string(),
            fields: Metadata::from([("direction", FieldValue::Float(0.75))]),
        },
    ];
    let baseline_legal_hint = None;
    let baseline_metadata = Metadata::from([(
        "proposal_source",
        FieldValue::Text("fixture-delta".to_string()),
    )]);
    let baseline_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        baseline_label,
        baseline_actions.clone(),
        baseline_legal_hint,
        baseline_metadata.clone(),
    );

    let mutated_metadata = Metadata::from([
        ("contract_flag", FieldValue::Boolean(true)),
        ("contract_float", FieldValue::Float(-0.125)),
        ("contract_integer", FieldValue::Integer(77)),
        (
            "contract_tags",
            FieldValue::StringList(vec!["stage77".to_string(), "metadata-shape".to_string()]),
        ),
        (
            "proposal_source",
            FieldValue::Text("fixture-delta-shaped".to_string()),
        ),
    ]);
    let mutated_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        baseline_label,
        baseline_actions.clone(),
        baseline_legal_hint,
        mutated_metadata.clone(),
    );

    let mut expected_mutated_artifact = baseline_artifact.clone();
    expected_mutated_artifact.payload.proposals[1].metadata = mutated_metadata.clone();
    assert_eq!(mutated_artifact, expected_mutated_artifact);
    assert_eq!(
        mutated_artifact.payload.proposals[1].label,
        baseline_artifact.payload.proposals[1].label
    );
    assert_eq!(
        mutated_artifact.payload.proposals[1].actions,
        baseline_artifact.payload.proposals[1].actions
    );
    assert_eq!(
        mutated_artifact.payload.proposals[1].legal_hint,
        baseline_artifact.payload.proposals[1].legal_hint
    );
    assert_ne!(
        mutated_artifact.payload.proposals[1].metadata,
        baseline_artifact.payload.proposals[1].metadata
    );

    let (_, baseline) =
        run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
            .expect("baseline stage77 lane should reload canonically");
    let (_, mutated) =
        run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
            .expect("mutated stage77 lane should reload canonically");

    assert_eq!(
        baseline.consumer_export.branches[0],
        mutated.consumer_export.branches[0]
    );
    assert_eq!(
        baseline.consumer_export.branches[1].label,
        mutated.consumer_export.branches[1].label
    );
    assert_eq!(
        baseline.consumer_export.branches[1].actions,
        mutated.consumer_export.branches[1].actions
    );
    assert_eq!(
        baseline.consumer_export.branches[1].legality_hint,
        mutated.consumer_export.branches[1].legality_hint
    );
    assert_eq!(
        baseline.consumer_export.branches[1].metadata,
        baseline_metadata
    );
    assert_eq!(
        mutated.consumer_export.branches[1].metadata,
        mutated_metadata
    );
    assert_eq!(
        baseline.scoreboard_artifact.payload.rows,
        mutated.scoreboard_artifact.payload.rows
    );
    assert_eq!(baseline.teacher_artifacts, mutated.teacher_artifacts);
}

#[test]
fn second_deterministic_vertical_slice_detects_exported_branch_payload_negative_drift_for_proposal_surface()
 {
    let directory = tempdir().expect("tempdir should be created");
    let branch_id = "anchor-stage77-second:branch:1";
    let mutated_label = "candidate-delta-stage77-negative-drift";
    let mutated_actions = vec![
        ActionRecord {
            action_key: "jump".to_string(),
            fields: Metadata::from([
                ("pressed", FieldValue::Boolean(true)),
                (
                    "negative_drift_tag",
                    FieldValue::Text("stage77-branch-surface".to_string()),
                ),
            ]),
        },
        ActionRecord {
            action_key: "roll".to_string(),
            fields: Metadata::from([("direction", FieldValue::Float(-0.5))]),
        },
    ];
    let mutated_legal_hint = Some(true);
    let mutated_metadata = Metadata::from([
        (
            "proposal_contract_tag",
            FieldValue::Text("stage77-negative-drift".to_string()),
        ),
        (
            "proposal_source",
            FieldValue::Text("fixture-delta-negative-drift".to_string()),
        ),
    ]);
    let mutated_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        mutated_label,
        mutated_actions.clone(),
        mutated_legal_hint,
        mutated_metadata.clone(),
    );

    let (_, baseline) = run_persisted_input_artifact_and_load(directory.path(), &mutated_artifact)
        .expect("mutated stage77 lane should reload canonically before drift injection");

    let branch_path = stage77_branch_artifact_path(directory.path(), branch_id);
    let mut branch_value = read_json_value(&branch_path);
    let payload = branch_value["payload"]
        .as_object_mut()
        .expect("branch payload should be an object");
    payload.remove("label");
    payload.remove("actions");
    payload.remove("legality_hint");
    payload.remove("metadata");
    write_json_value(&branch_path, &branch_value);
    refresh_stage77_branch_index_hash(directory.path(), branch_id)
        .expect("negative drift branch hash should be refreshed");

    let drifted = load_result(directory.path())
        .expect("negative drift branch artifact should still reload through defaulted schema");

    assert_eq!(
        drifted.consumer_export.branches[0],
        baseline.consumer_export.branches[0]
    );
    let error = assert_branch_payload_surface_matches(
        &drifted.consumer_export.branches,
        branch_id,
        Some(mutated_label),
        &mutated_actions,
        mutated_legal_hint,
        &mutated_metadata,
    )
    .expect_err("proposal-surface negative drift should fail explicitly");

    assert_eq!(
        error.to_string(),
        format!(
            "vertical-slice branch payload drift: branch {branch_id}, expected label {:?}, found {:?}",
            Some(mutated_label),
            None::<String>
        )
    );
}

#[test]
fn second_deterministic_vertical_slice_rejects_targeted_branch_artifact_corruption_at_canonical_load_boundary()
 {
    let directory = tempdir().expect("tempdir should be created");
    let branch_id = "anchor-stage77-second:branch:1";
    run_persisted_input_artifact_and_load(
        directory.path(),
        &persisted_input_artifact_for_lane_with_proposal_surface(
            VerticalSliceFixtureLane::Stage77Second,
            1,
            "candidate-delta",
            vec![
                ActionRecord {
                    action_key: "jump".to_string(),
                    fields: Metadata::from([("pressed", FieldValue::Boolean(false))]),
                },
                ActionRecord {
                    action_key: "roll".to_string(),
                    fields: Metadata::from([("direction", FieldValue::Float(0.75))]),
                },
            ],
            None,
            Metadata::from([(
                "proposal_source",
                FieldValue::Text("fixture-delta".to_string()),
            )]),
        ),
    )
    .expect("baseline stage77 lane should reload canonically before corruption injection");

    let branch_path = stage77_branch_artifact_path(directory.path(), branch_id);
    let mut branch_value = read_json_value(&branch_path);
    branch_value["payload"]["actions"] = Value::String("corrupted-actions".to_string());
    write_json_value(&branch_path, &branch_value);

    let error = load_result(directory.path())
        .expect_err("corrupted branch artifact should fail explicitly");

    assert!(error.to_string().contains(&format!(
                "failed to load vertical-slice export bundle from {}",
                directory.path().join(VERTICAL_SLICE_EXPORT_DIR_NAME).display()
            )));
    assert!(
        error
            .to_string()
            .contains("invalid type: string \"corrupted-actions\", expected a sequence")
    );
}

#[test]
fn second_deterministic_vertical_slice_persisted_input_rejects_missing_proposal_label_before_runtime_materialization()
 {
    let directory = tempdir().expect("tempdir should be created");
    let input_path = vertical_slice_input_artifact_path(directory.path());
    let artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        "candidate-delta",
        vec![
            ActionRecord {
                action_key: "jump".to_string(),
                fields: Metadata::from([("pressed", FieldValue::Boolean(false))]),
            },
            ActionRecord {
                action_key: "roll".to_string(),
                fields: Metadata::from([("direction", FieldValue::Float(0.75))]),
            },
        ],
        None,
        Metadata::from([(
            "proposal_source",
            FieldValue::Text("fixture-delta".to_string()),
        )]),
    );

    write_vertical_slice_input_artifact(&input_path, ArtifactFormat::Json, &artifact)
        .expect("stage77 input artifact should write");
    let mut input_value = read_json_value(&input_path);
    input_value["payload"]["proposals"][1]
        .as_object_mut()
        .expect("stage77 proposal should be an object")
        .remove("label");
    write_json_value(&input_path, &input_value);

    let error = read_vertical_slice_input_artifact(&input_path)
        .expect_err("missing proposal label should fail explicitly");

    assert!(error.to_string().contains("missing field `label`"));
}

#[test]
fn second_deterministic_vertical_slice_directly_consumes_proposal_actions_into_simulation_requests_without_perturbing_other_contract_edges()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_actions = vec![
        ActionRecord {
            action_key: "jump".to_string(),
            fields: Metadata::from([("pressed", FieldValue::Boolean(false))]),
        },
        ActionRecord {
            action_key: "roll".to_string(),
            fields: Metadata::from([("direction", FieldValue::Float(0.75))]),
        },
    ];
    let mutated_actions = vec![
        ActionRecord {
            action_key: "pitch".to_string(),
            fields: Metadata::from([("direction", FieldValue::Float(0.125))]),
        },
        ActionRecord {
            action_key: "boost".to_string(),
            fields: Metadata::from([
                ("pressed", FieldValue::Boolean(true)),
                (
                    "action_contract_tag",
                    FieldValue::Text("stage77-sim-request".to_string()),
                ),
            ]),
        },
    ];
    let baseline_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        "candidate-delta",
        baseline_actions.clone(),
        None,
        Metadata::from([(
            "proposal_source",
            FieldValue::Text("fixture-delta".to_string()),
        )]),
    );
    let mutated_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        "candidate-delta",
        mutated_actions.clone(),
        None,
        Metadata::from([(
            "proposal_source",
            FieldValue::Text("fixture-delta".to_string()),
        )]),
    );

    let (baseline_output, baseline, baseline_requests) =
        run_persisted_input_artifact_and_capture_simulation_requests(
            baseline_directory.path(),
            &baseline_artifact,
        )
        .expect("baseline stage77 lane should capture simulation requests");
    let (mutated_output, mutated, mutated_requests) =
        run_persisted_input_artifact_and_capture_simulation_requests(
            mutated_directory.path(),
            &mutated_artifact,
        )
        .expect("mutated stage77 lane should capture simulation requests");

    assert_eq!(
        baseline_requests
            .iter()
            .map(|request| request.simulation_id.clone())
            .collect::<Vec<_>>(),
        mutated_requests
            .iter()
            .map(|request| request.simulation_id.clone())
            .collect::<Vec<_>>()
    );
    assert_eq!(
        baseline_requests
            .iter()
            .map(|request| request.seed)
            .collect::<Vec<_>>(),
        vec![77, 77]
    );
    assert_eq!(
        mutated_requests
            .iter()
            .map(|request| request.seed)
            .collect::<Vec<_>>(),
        vec![77, 77]
    );
    assert_eq!(
        baseline_requests[0].commands,
        simulation_commands_from_actions(&baseline_artifact.payload.proposals[0].actions)
    );
    assert_eq!(mutated_requests[0].commands, baseline_requests[0].commands);
    assert_eq!(
        baseline_requests[1].commands,
        simulation_commands_from_actions(&baseline_actions)
    );
    assert_eq!(
        mutated_requests[1].commands,
        simulation_commands_from_actions(&mutated_actions)
    );

    assert_eq!(
        baseline_output.consumer_export.branches[0],
        mutated_output.consumer_export.branches[0]
    );
    assert_eq!(
        baseline_output.consumer_export.branches[1].label,
        mutated_output.consumer_export.branches[1].label
    );
    assert_eq!(
        baseline_output.consumer_export.branches[1].legality_hint,
        mutated_output.consumer_export.branches[1].legality_hint
    );
    assert_eq!(
        baseline_output.consumer_export.branches[1].metadata,
        mutated_output.consumer_export.branches[1].metadata
    );
    assert_eq!(
        baseline_output.consumer_export.branches[1].actions,
        baseline_actions
    );
    assert_eq!(
        mutated_output.consumer_export.branches[1].actions,
        mutated_actions
    );
    assert_eq!(
        baseline
            .scoreboard_artifact
            .payload
            .rows
            .iter()
            .map(|row| (row.branch_id.clone(), row.score.clone()))
            .collect::<Vec<_>>(),
        mutated
            .scoreboard_artifact
            .payload
            .rows
            .iter()
            .map(|row| (row.branch_id.clone(), row.score.clone()))
            .collect::<Vec<_>>()
    );
    assert_eq!(
        baseline.scoreboard_artifact.payload.rows[0].step_hashes,
        mutated.scoreboard_artifact.payload.rows[0].step_hashes
    );
    assert_ne!(
        baseline.scoreboard_artifact.payload.rows[1].step_hashes,
        mutated.scoreboard_artifact.payload.rows[1].step_hashes
    );
    assert_eq!(baseline.teacher_artifacts, mutated.teacher_artifacts);
}

#[test]
fn second_deterministic_vertical_slice_keeps_manifest_and_index_stable_except_for_the_mutated_branch_payload_hash()
 {
    let baseline_directory = tempdir().expect("tempdir should be created");
    let mutated_directory = tempdir().expect("tempdir should be created");

    let baseline_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        "candidate-delta",
        vec![
            ActionRecord {
                action_key: "jump".to_string(),
                fields: Metadata::from([("pressed", FieldValue::Boolean(false))]),
            },
            ActionRecord {
                action_key: "roll".to_string(),
                fields: Metadata::from([("direction", FieldValue::Float(0.75))]),
            },
        ],
        None,
        Metadata::from([(
            "proposal_source",
            FieldValue::Text("fixture-delta".to_string()),
        )]),
    );
    let mutated_artifact = persisted_input_artifact_for_lane_with_proposal_surface(
        VerticalSliceFixtureLane::Stage77Second,
        1,
        "candidate-delta-stage77-packaging",
        vec![
            ActionRecord {
                action_key: "jump".to_string(),
                fields: Metadata::from([
                    ("pressed", FieldValue::Boolean(true)),
                    ("packaging_tag", FieldValue::Text("stage77".to_string())),
                ]),
            },
            ActionRecord {
                action_key: "roll".to_string(),
                fields: Metadata::from([("direction", FieldValue::Float(-0.5))]),
            },
        ],
        Some(true),
        Metadata::from([
            (
                "proposal_contract_tag",
                FieldValue::Text("stage77-packaging".to_string()),
            ),
            (
                "proposal_source",
                FieldValue::Text("fixture-delta-packaging".to_string()),
            ),
        ]),
    );

    run_persisted_input_artifact_and_load(baseline_directory.path(), &baseline_artifact)
        .expect("baseline stage77 lane should reload canonically");
    run_persisted_input_artifact_and_load(mutated_directory.path(), &mutated_artifact)
        .expect("mutated stage77 lane should reload canonically");

    let baseline_export_dir = baseline_directory
        .path()
        .join(VERTICAL_SLICE_EXPORT_DIR_NAME);
    let mutated_export_dir = mutated_directory
        .path()
        .join(VERTICAL_SLICE_EXPORT_DIR_NAME);
    let baseline_inspection =
        inspect_export_bundle(&baseline_export_dir).expect("baseline export should inspect");
    let mutated_inspection =
        inspect_export_bundle(&mutated_export_dir).expect("mutated export should inspect");

    assert_eq!(baseline_inspection.manifest, mutated_inspection.manifest);
    assert_eq!(
        baseline_inspection.index.entries.len(),
        mutated_inspection.index.entries.len()
    );

    let changed_record_ids = baseline_inspection
        .index
        .entries
        .iter()
        .zip(&mutated_inspection.index.entries)
        .filter_map(|(baseline_entry, mutated_entry)| {
            assert_eq!(baseline_entry.artifact_kind, mutated_entry.artifact_kind);
            assert_eq!(baseline_entry.record_id, mutated_entry.record_id);
            assert_eq!(baseline_entry.relative_path, mutated_entry.relative_path);
            assert_eq!(baseline_entry.schema_name, mutated_entry.schema_name);
            assert_eq!(baseline_entry.schema_version, mutated_entry.schema_version);
            if baseline_entry.content_hash != mutated_entry.content_hash {
                Some(baseline_entry.record_id.clone())
            } else {
                None
            }
        })
        .collect::<Vec<_>>();

    assert_eq!(
        changed_record_ids,
        vec!["anchor-stage77-second:branch:1".to_string()]
    );
}

#[test]
fn deterministic_fixture_lanes_do_not_collapse_to_the_same_golden_snapshot() {
    let first_lane = tempdir().expect("tempdir should be created");
    let second_lane = tempdir().expect("tempdir should be created");
    assert_fixture_lanes_have_distinct_golden_snapshots(
        first_lane.path(),
        VerticalSliceFixtureLane::Stage69Sample,
        second_lane.path(),
        VerticalSliceFixtureLane::Stage77Second,
    )
    .expect("fixture lanes should keep distinct frozen golden snapshots");
}
