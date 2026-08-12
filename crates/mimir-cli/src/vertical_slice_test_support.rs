use crate::vertical_slice::{
    VERTICAL_SLICE_EXPORT_DIR_NAME, VERTICAL_SLICE_TEACHER_DIR_NAME, VerticalSliceFixture,
    VerticalSliceProposalFixture, VerticalSliceRunOutput, run_deterministic_vertical_slice,
};
use crate::vertical_slice_result::{
    CanonicalVerticalSliceResult, VerticalSliceGoldenScoreboardRow, VerticalSliceGoldenSnapshot,
    load_canonical_vertical_slice_result,
};
use mimir_anchor::AnchorHint;
use mimir_branch::BranchProposal;
use mimir_core::{MimirError, Result};
use mimir_export::{adapt_loaded_export_for_consumer, inspect_export_bundle, load_export_bundle};
use mimir_io::{
    ArtifactFormat, PersistedScoreboardArtifact, read_vertical_slice_input_artifact,
    scoreboard_artifact_path, vertical_slice_input_artifact_path, write_scoreboard_artifact,
    write_teacher_label_artifact, write_vertical_slice_input_artifact,
};
use mimir_sim_bridge::DeterministicFakeBackend;
use mimir_sim_bridge::{SimBackend, SimulationCommand, SimulationRequest, SimulationResult};
use mimir_types::{
    ActionRecord, AnchorId, AnchorKind, ArtifactKind, FieldValue, FrameIndex, Metadata,
    PersistedTeacherLabelArtifact, PersistedVerticalSliceAnchorHint, PersistedVerticalSliceInput,
    PersistedVerticalSliceInputArtifact, PersistedVerticalSliceProposal, ReplayId,
    TeacherLabelTarget,
};
use std::cell::RefCell;
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

pub(crate) const VERTICAL_SLICE_SCOREBOARD_FILE_NAME: &str = "scoreboard.json";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum VerticalSliceFixtureLane {
    Stage69Sample,
    Stage77Second,
}

pub(crate) fn sample_fixture() -> VerticalSliceFixture {
    fixture_for_lane(VerticalSliceFixtureLane::Stage69Sample)
}

fn fixture_for_lane(lane: VerticalSliceFixtureLane) -> VerticalSliceFixture {
    fixture_from_persisted_input(&persisted_input_artifact_for_lane(lane))
}

fn persisted_input_artifact_for_lane(
    lane: VerticalSliceFixtureLane,
) -> PersistedVerticalSliceInputArtifact {
    match lane {
        VerticalSliceFixtureLane::Stage69Sample => PersistedVerticalSliceInputArtifact::new(
            vertical_slice_input_header("Stage69Sample"),
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
                proposals: vec![
                    PersistedVerticalSliceProposal {
                        label: "candidate-alpha".to_string(),
                        actions: vec![ActionRecord {
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
                    },
                    PersistedVerticalSliceProposal {
                        label: "candidate-beta".to_string(),
                        actions: vec![
                            ActionRecord {
                                action_key: "boost".to_string(),
                                fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
                            },
                            ActionRecord {
                                action_key: "steer".to_string(),
                                fields: Metadata::from([("direction", FieldValue::Float(0.5))]),
                            },
                        ],
                        legal_hint: Some(true),
                        metadata: Metadata::from([(
                            "proposal_source",
                            FieldValue::Text("fixture-beta".to_string()),
                        )]),
                        score_signals: BTreeMap::from([
                            ("coverage".to_string(), 4.0),
                            ("stability".to_string(), 2.0),
                        ]),
                    },
                ],
                scorer_weights: BTreeMap::from([
                    ("coverage".to_string(), 1.0),
                    ("stability".to_string(), 0.5),
                ]),
            },
        ),
        VerticalSliceFixtureLane::Stage77Second => PersistedVerticalSliceInputArtifact::new(
            vertical_slice_input_header("Stage77Second"),
            PersistedVerticalSliceInput {
                replay_id: ReplayId::new("replay-stage77-second"),
                export_name: "stage77-second-vertical-slice".to_string(),
                teacher_namespace: "stage77.second.teacher".to_string(),
                simulation_seed: 77,
                anchor_hint: PersistedVerticalSliceAnchorHint {
                    anchor_id: Some(AnchorId::new("anchor-stage77-second")),
                    frame_index: FrameIndex::new(256),
                    kind: AnchorKind::Manual,
                    metadata: Metadata::from([(
                        "source",
                        FieldValue::Text("stage77-second-fixture".to_string()),
                    )]),
                },
                proposals: vec![
                    PersistedVerticalSliceProposal {
                        label: "candidate-gamma".to_string(),
                        actions: vec![
                            ActionRecord {
                                action_key: "throttle".to_string(),
                                fields: Metadata::from([("amount", FieldValue::Float(1.0))]),
                            },
                            ActionRecord {
                                action_key: "yaw".to_string(),
                                fields: Metadata::from([("direction", FieldValue::Float(-0.25))]),
                            },
                        ],
                        legal_hint: Some(true),
                        metadata: Metadata::from([(
                            "proposal_source",
                            FieldValue::Text("fixture-gamma".to_string()),
                        )]),
                        score_signals: BTreeMap::from([
                            ("coverage".to_string(), 5.0),
                            ("stability".to_string(), 2.0),
                        ]),
                    },
                    PersistedVerticalSliceProposal {
                        label: "candidate-delta".to_string(),
                        actions: vec![
                            ActionRecord {
                                action_key: "jump".to_string(),
                                fields: Metadata::from([("pressed", FieldValue::Boolean(false))]),
                            },
                            ActionRecord {
                                action_key: "roll".to_string(),
                                fields: Metadata::from([("direction", FieldValue::Float(0.75))]),
                            },
                        ],
                        legal_hint: None,
                        metadata: Metadata::from([(
                            "proposal_source",
                            FieldValue::Text("fixture-delta".to_string()),
                        )]),
                        score_signals: BTreeMap::from([
                            ("coverage".to_string(), 2.0),
                            ("stability".to_string(), 1.0),
                        ]),
                    },
                ],
                scorer_weights: BTreeMap::from([
                    ("coverage".to_string(), 1.0),
                    ("stability".to_string(), 0.5),
                ]),
            },
        ),
    }
}

fn vertical_slice_input_header(fixture_lane: &str) -> mimir_types::ArtifactHeader {
    mimir_types::ArtifactHeader::for_kind(ArtifactKind::VerticalSliceInput, "mimir-cli-tests")
        .with_created_by_component("vertical-slice-test-support")
        .with_metadata(Metadata::from([(
            "fixture_lane",
            FieldValue::Text(fixture_lane.to_string()),
        )]))
}

fn fixture_from_persisted_input(
    artifact: &PersistedVerticalSliceInputArtifact,
) -> VerticalSliceFixture {
    VerticalSliceFixture {
        replay_id: artifact.payload.replay_id.clone(),
        export_name: artifact.payload.export_name.clone(),
        teacher_namespace: artifact.payload.teacher_namespace.clone(),
        simulation_seed: artifact.payload.simulation_seed,
        anchor_hint: AnchorHint {
            anchor_id: artifact.payload.anchor_hint.anchor_id.clone(),
            frame_index: artifact.payload.anchor_hint.frame_index,
            kind: artifact.payload.anchor_hint.kind.clone(),
            metadata: artifact.payload.anchor_hint.metadata.clone(),
        },
        proposals: artifact
            .payload
            .proposals
            .iter()
            .map(|proposal| VerticalSliceProposalFixture {
                branch_proposal: BranchProposal {
                    label: proposal.label.clone(),
                    actions: proposal.actions.clone(),
                    legal_hint: proposal.legal_hint,
                    metadata: proposal.metadata.clone(),
                },
                score_signals: proposal.score_signals.clone(),
            })
            .collect(),
        scorer_weights: artifact.payload.scorer_weights.clone(),
    }
}

pub(crate) fn expected_stage73_golden_snapshot() -> VerticalSliceGoldenSnapshot {
    expected_golden_snapshot_for_lane(VerticalSliceFixtureLane::Stage69Sample)
}

pub(crate) fn expected_golden_snapshot_for_lane(
    lane: VerticalSliceFixtureLane,
) -> VerticalSliceGoldenSnapshot {
    match lane {
        VerticalSliceFixtureLane::Stage69Sample => VerticalSliceGoldenSnapshot {
            export_name: "stage69-vertical-slice".to_string(),
            replay_id: "replay-stage69".to_string(),
            anchor_id: "anchor-stage69".to_string(),
            anchor_frame_index: 128,
            anchor_kind: AnchorKind::Manual,
            export_directory_name: VERTICAL_SLICE_EXPORT_DIR_NAME.to_string(),
            scoreboard_artifact_relative_path: VERTICAL_SLICE_SCOREBOARD_FILE_NAME.to_string(),
            teacher_artifact_relative_paths: vec![
                "teacher_labels/teacher-label-0.json".to_string(),
                "teacher_labels/teacher-label-1.json".to_string(),
            ],
            branch_ids_in_order: vec![
                "anchor-stage69:branch:0".to_string(),
                "anchor-stage69:branch:1".to_string(),
            ],
            scoreboard_rows_in_order: vec![
                VerticalSliceGoldenScoreboardRow {
                    branch_id: "anchor-stage69:branch:0".to_string(),
                    total_score: 3.5,
                },
                VerticalSliceGoldenScoreboardRow {
                    branch_id: "anchor-stage69:branch:1".to_string(),
                    total_score: 5.0,
                },
            ],
            teacher_targets_in_order: vec![
                "anchor-stage69:branch:1".to_string(),
                "anchor-stage69:branch:0".to_string(),
            ],
        },
        VerticalSliceFixtureLane::Stage77Second => VerticalSliceGoldenSnapshot {
            export_name: "stage77-second-vertical-slice".to_string(),
            replay_id: "replay-stage77-second".to_string(),
            anchor_id: "anchor-stage77-second".to_string(),
            anchor_frame_index: 256,
            anchor_kind: AnchorKind::Manual,
            export_directory_name: VERTICAL_SLICE_EXPORT_DIR_NAME.to_string(),
            scoreboard_artifact_relative_path: VERTICAL_SLICE_SCOREBOARD_FILE_NAME.to_string(),
            teacher_artifact_relative_paths: vec![
                "teacher_labels/teacher-label-0.json".to_string(),
                "teacher_labels/teacher-label-1.json".to_string(),
            ],
            branch_ids_in_order: vec![
                "anchor-stage77-second:branch:0".to_string(),
                "anchor-stage77-second:branch:1".to_string(),
            ],
            scoreboard_rows_in_order: vec![
                VerticalSliceGoldenScoreboardRow {
                    branch_id: "anchor-stage77-second:branch:0".to_string(),
                    total_score: 6.0,
                },
                VerticalSliceGoldenScoreboardRow {
                    branch_id: "anchor-stage77-second:branch:1".to_string(),
                    total_score: 2.5,
                },
            ],
            teacher_targets_in_order: vec![
                "anchor-stage77-second:branch:0".to_string(),
                "anchor-stage77-second:branch:1".to_string(),
            ],
        },
    }
}

pub(crate) fn run_sample_fixture(output_dir: &Path) -> Result<VerticalSliceRunOutput> {
    run_fixture_lane(output_dir, VerticalSliceFixtureLane::Stage69Sample)
}

pub(crate) fn run_fixture_lane(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<VerticalSliceRunOutput> {
    let fixture = load_persisted_fixture_for_lane(output_dir, lane)?;
    run_deterministic_vertical_slice(output_dir, &fixture, Some(&DeterministicFakeBackend))
}

pub(crate) fn run_fixture_lane_and_load(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<(VerticalSliceRunOutput, CanonicalVerticalSliceResult)> {
    let output = run_fixture_lane(output_dir, lane)?;
    let canonical = load_canonical_vertical_slice_result(output_dir)?;
    Ok((output, canonical))
}

pub(crate) fn persisted_input_artifact_for_lane_with_scorer_weights(
    lane: VerticalSliceFixtureLane,
    scorer_weights: BTreeMap<String, f64>,
) -> PersistedVerticalSliceInputArtifact {
    let mut artifact = persisted_input_artifact_for_lane(lane);
    artifact.payload.scorer_weights = scorer_weights;
    artifact
}

pub(crate) fn persisted_input_artifact_for_lane_with_simulation_seed(
    lane: VerticalSliceFixtureLane,
    simulation_seed: u64,
) -> PersistedVerticalSliceInputArtifact {
    let mut artifact = persisted_input_artifact_for_lane(lane);
    artifact.payload.simulation_seed = simulation_seed;
    artifact
}

pub(crate) fn persisted_input_artifact_for_lane_with_teacher_namespace(
    lane: VerticalSliceFixtureLane,
    teacher_namespace: impl Into<String>,
) -> PersistedVerticalSliceInputArtifact {
    let mut artifact = persisted_input_artifact_for_lane(lane);
    artifact.payload.teacher_namespace = teacher_namespace.into();
    artifact
}

pub(crate) fn persisted_input_artifact_for_lane_with_export_name(
    lane: VerticalSliceFixtureLane,
    export_name: impl Into<String>,
) -> PersistedVerticalSliceInputArtifact {
    let mut artifact = persisted_input_artifact_for_lane(lane);
    artifact.payload.export_name = export_name.into();
    artifact
}

pub(crate) fn persisted_input_artifact_for_lane_with_anchor_metadata(
    lane: VerticalSliceFixtureLane,
    anchor_metadata: Metadata,
) -> PersistedVerticalSliceInputArtifact {
    let mut artifact = persisted_input_artifact_for_lane(lane);
    artifact.payload.anchor_hint.metadata = anchor_metadata;
    artifact
}

pub(crate) fn persisted_input_artifact_for_lane_with_proposal_surface(
    lane: VerticalSliceFixtureLane,
    proposal_index: usize,
    label: impl Into<String>,
    actions: Vec<ActionRecord>,
    legal_hint: Option<bool>,
    metadata: Metadata,
) -> PersistedVerticalSliceInputArtifact {
    let mut artifact = persisted_input_artifact_for_lane(lane);
    let proposal = artifact
        .payload
        .proposals
        .get_mut(proposal_index)
        .expect("proposal index should exist in persisted fixture lane");
    proposal.label = label.into();
    proposal.actions = actions;
    proposal.legal_hint = legal_hint;
    proposal.metadata = metadata;
    artifact
}

pub(crate) fn persisted_input_artifact_for_lane_with_proposal_score_signals(
    lane: VerticalSliceFixtureLane,
    proposal_index: usize,
    score_signals: BTreeMap<String, f64>,
) -> PersistedVerticalSliceInputArtifact {
    let mut artifact = persisted_input_artifact_for_lane(lane);
    let proposal = artifact
        .payload
        .proposals
        .get_mut(proposal_index)
        .expect("proposal index should exist in persisted fixture lane");
    proposal.score_signals = score_signals;
    artifact
}

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct CapturedSimulationRequest {
    pub(crate) simulation_id: String,
    pub(crate) seed: u64,
    pub(crate) commands: Vec<SimulationCommand>,
}

#[derive(Debug, Default)]
struct RecordingDeterministicFakeBackend {
    captured_requests: RefCell<Vec<CapturedSimulationRequest>>,
}

impl RecordingDeterministicFakeBackend {
    fn captured_requests(&self) -> Vec<CapturedSimulationRequest> {
        self.captured_requests.borrow().clone()
    }
}

impl SimBackend for RecordingDeterministicFakeBackend {
    fn simulate(&self, request: &SimulationRequest) -> Result<SimulationResult> {
        self.captured_requests
            .borrow_mut()
            .push(CapturedSimulationRequest {
                simulation_id: request.simulation_id.clone(),
                seed: request.seed,
                commands: request.commands.clone(),
            });
        DeterministicFakeBackend.simulate(request)
    }
}

pub(crate) fn run_persisted_input_artifact_and_load(
    output_dir: &Path,
    input_artifact: &PersistedVerticalSliceInputArtifact,
) -> Result<(VerticalSliceRunOutput, CanonicalVerticalSliceResult)> {
    let fixture = load_persisted_fixture(output_dir, input_artifact)?;
    let output =
        run_deterministic_vertical_slice(output_dir, &fixture, Some(&DeterministicFakeBackend))?;
    let canonical = load_canonical_vertical_slice_result(output_dir)?;
    Ok((output, canonical))
}

pub(crate) fn run_persisted_input_artifact_and_capture_simulation_requests(
    output_dir: &Path,
    input_artifact: &PersistedVerticalSliceInputArtifact,
) -> Result<(
    VerticalSliceRunOutput,
    CanonicalVerticalSliceResult,
    Vec<CapturedSimulationRequest>,
)> {
    let fixture = load_persisted_fixture(output_dir, input_artifact)?;
    let backend = RecordingDeterministicFakeBackend::default();
    let output = run_deterministic_vertical_slice(output_dir, &fixture, Some(&backend))?;
    let canonical = load_canonical_vertical_slice_result(output_dir)?;
    Ok((output, canonical, backend.captured_requests()))
}

pub(crate) fn assert_fixture_lane_matches_expected_contract(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<()> {
    let expected_snapshot = expected_golden_snapshot_for_lane(lane);
    let (output, canonical) = run_fixture_lane_and_load(output_dir, lane)?;

    assert_eq!(output.manifest.export_name, expected_snapshot.export_name);
    assert_eq!(output.consumer_export.anchors.len(), 1);
    assert_eq!(output.consumer_export.branches.len(), 2);
    assert_eq!(output.scoreboard.rows.len(), 2);
    assert_eq!(output.teacher_artifacts.len(), 2);

    let export_dir = output_dir.join(VERTICAL_SLICE_EXPORT_DIR_NAME);
    let inspection = inspect_export_bundle(&export_dir)?;
    assert_eq!(inspection.manifest.anchor_count, 1);
    assert_eq!(inspection.manifest.branch_count, 2);

    let reloaded_consumer_export =
        adapt_loaded_export_for_consumer(load_export_bundle(&export_dir)?);
    assert_eq!(reloaded_consumer_export, output.consumer_export);

    assert_eq!(
        canonical.scoreboard_artifact.header.schema_name,
        ArtifactKind::Scoreboard.schema().name
    );
    assert_eq!(canonical.consumer_export, output.consumer_export);
    assert_eq!(canonical.scoreboard_artifact.payload, output.scoreboard);
    assert_eq!(canonical.teacher_artifacts, output.teacher_artifacts);

    let snapshot = canonical.golden_snapshot(
        VERTICAL_SLICE_EXPORT_DIR_NAME,
        VERTICAL_SLICE_SCOREBOARD_FILE_NAME,
        VERTICAL_SLICE_TEACHER_DIR_NAME,
    )?;
    assert_eq!(snapshot, expected_snapshot);

    Ok(())
}

pub(crate) fn assert_fixture_lane_repeated_runs_are_identical(
    first_output_dir: &Path,
    second_output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<()> {
    let expected_snapshot = expected_golden_snapshot_for_lane(lane);
    let first_output = run_fixture_lane(first_output_dir, lane)?;
    let second_output = run_fixture_lane(second_output_dir, lane)?;

    assert_eq!(first_output, second_output);

    let first_result = load_result(first_output_dir)?;
    let second_result = load_result(second_output_dir)?;
    assert_eq!(first_result, second_result);

    let first_snapshot = first_result.golden_snapshot(
        VERTICAL_SLICE_EXPORT_DIR_NAME,
        VERTICAL_SLICE_SCOREBOARD_FILE_NAME,
        VERTICAL_SLICE_TEACHER_DIR_NAME,
    )?;
    let second_snapshot = second_result.golden_snapshot(
        VERTICAL_SLICE_EXPORT_DIR_NAME,
        VERTICAL_SLICE_SCOREBOARD_FILE_NAME,
        VERTICAL_SLICE_TEACHER_DIR_NAME,
    )?;
    assert_eq!(first_snapshot, expected_snapshot);
    assert_eq!(second_snapshot, expected_snapshot);
    assert_eq!(first_snapshot, second_snapshot);

    Ok(())
}

pub(crate) fn assert_fixture_lanes_have_distinct_golden_snapshots(
    first_output_dir: &Path,
    first_lane: VerticalSliceFixtureLane,
    second_output_dir: &Path,
    second_lane: VerticalSliceFixtureLane,
) -> Result<()> {
    let first_snapshot = load_snapshot_after_run(first_output_dir, first_lane)?;
    let second_snapshot = load_snapshot_after_run(second_output_dir, second_lane)?;

    assert_eq!(
        first_snapshot,
        expected_golden_snapshot_for_lane(first_lane)
    );
    assert_eq!(
        second_snapshot,
        expected_golden_snapshot_for_lane(second_lane)
    );
    assert_ne!(first_snapshot, second_snapshot);

    Ok(())
}

pub(crate) fn assert_fixture_lane_scoreboard_row_count_drift_fails_explicitly(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<()> {
    run_fixture_lane(output_dir, lane)?;

    let mut canonical = load_result(output_dir)?;
    canonical.scoreboard_artifact.payload.rows.pop();
    let expected_branch_count = canonical.consumer_export.branches.len();
    let drifted_row_count = canonical.scoreboard_artifact.payload.rows.len();
    rewrite_scoreboard_artifact(output_dir, &canonical.scoreboard_artifact)?;

    let error = load_result(output_dir).expect_err("scoreboard row drift should fail explicitly");

    assert_eq!(
        error.to_string(),
        format!(
            "vertical-slice scoreboard row count drift: expected {} rows from export bundle, found {}",
            expected_branch_count, drifted_row_count
        )
    );

    Ok(())
}

pub(crate) fn assert_fixture_lane_scoreboard_component_schema_drift_fails_explicitly(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<()> {
    run_fixture_lane(output_dir, lane)?;

    let baseline = load_result(output_dir)?;
    let drifted_branch_id = "anchor-stage77-second:branch:0";
    let expected_component_keys = vec!["coverage".to_string(), "stability".to_string()];

    let mut drifted = baseline.clone();
    let drifted_row = drifted
        .scoreboard_artifact
        .payload
        .rows
        .iter_mut()
        .find(|row| row.branch_id.as_str() == drifted_branch_id)
        .expect("stage77 scoreboard row should exist");
    let coverage_value = drifted_row
        .score
        .components
        .remove("coverage")
        .expect("stage77 branch row should contain coverage");
    drifted_row
        .score
        .components
        .insert("coverage_drifted".to_string(), coverage_value);
    rewrite_scoreboard_artifact(output_dir, &drifted.scoreboard_artifact)?;

    let reloaded = load_result(output_dir)?;
    let error =
        assert_scoreboard_component_keys_match(&baseline, &reloaded, lane, drifted_branch_id)
            .expect_err("scoreboard component drift should fail explicitly");

    assert_eq!(
        error.to_string(),
        format!(
            "vertical-slice scoreboard component schema drift: lane {lane:?}, branch {drifted_branch_id}, expected component keys {expected_component_keys:?}, found {:?}",
            vec!["coverage_drifted".to_string(), "stability".to_string()]
        )
    );

    Ok(())
}

pub(crate) fn assert_fixture_lane_extra_teacher_artifact_count_drift_fails_explicitly(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<()> {
    let output = run_fixture_lane(output_dir, lane)?;
    let expected_teacher_count = output.scoreboard.rows.len();

    rewrite_teacher_artifact(
        output_dir,
        output.teacher_artifacts.len(),
        &output.teacher_artifacts[0],
    )?;

    let error = load_result(output_dir).expect_err("extra teacher artifact should fail explicitly");

    assert_eq!(
        error.to_string(),
        format!(
            "vertical-slice teacher artifact count drift: expected {} artifacts from scoreboard-derived branch count, found {}",
            expected_teacher_count,
            expected_teacher_count + 1
        )
    );

    Ok(())
}

pub(crate) fn assert_fixture_lane_non_branch_teacher_target_drift_fails_explicitly(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
    replay_id: &str,
) -> Result<()> {
    run_fixture_lane(output_dir, lane)?;

    let mut canonical = load_result(output_dir)?;
    rewrite_teacher_target_as_replay(
        output_dir,
        0,
        &mut canonical.teacher_artifacts[0],
        replay_id,
    )?;

    let error = load_result(output_dir)?
        .teacher_branch_targets_in_order()
        .expect_err("non-branch target drift should fail explicitly");

    assert_eq!(
        error.to_string(),
        format!(
            "vertical-slice teacher target drift: expected branch target, found Replay(ReplayId(\"{replay_id}\"))"
        )
    );

    Ok(())
}

pub(crate) fn assert_fixture_lane_teacher_artifact_ordinal_file_drift_changes_snapshot(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<()> {
    let output = run_fixture_lane(output_dir, lane)?;
    assert_eq!(
        output.teacher_artifacts.len(),
        2,
        "ordinal swap helper expects exactly two teacher artifacts"
    );

    rewrite_teacher_artifact(output_dir, 0, &output.teacher_artifacts[1])?;
    rewrite_teacher_artifact(output_dir, 1, &output.teacher_artifacts[0])?;

    let snapshot = load_snapshot(output_dir)?;
    let expected_snapshot = expected_golden_snapshot_for_lane(lane);
    let expected_swapped_targets = expected_snapshot
        .teacher_targets_in_order
        .iter()
        .rev()
        .cloned()
        .collect::<Vec<_>>();

    assert_ne!(snapshot, expected_snapshot);
    assert_eq!(snapshot.teacher_targets_in_order, expected_swapped_targets);

    Ok(())
}

pub(crate) fn assert_fixture_lane_snapshot_fails_explicitly_when_anchor_count_is_not_one(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<()> {
    run_fixture_lane(output_dir, lane)?;

    let mut canonical = load_result(output_dir)?;
    canonical
        .consumer_export
        .anchors
        .push(canonical.consumer_export.anchors[0].clone());

    let error = canonical
        .golden_snapshot(
            VERTICAL_SLICE_EXPORT_DIR_NAME,
            VERTICAL_SLICE_SCOREBOARD_FILE_NAME,
            VERTICAL_SLICE_TEACHER_DIR_NAME,
        )
        .expect_err("snapshot should reject duplicate anchors");

    assert_eq!(
        error.to_string(),
        "vertical-slice snapshot requires exactly one anchor, found 2"
    );

    Ok(())
}

pub(crate) fn assert_fixture_lane_missing_teacher_artifact_fails_explicitly(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
    missing_ordinal: usize,
) -> Result<()> {
    let output = run_fixture_lane(output_dir, lane)?;
    let expected_teacher_count = output.teacher_artifacts.len();
    let missing_path = teacher_artifact_path(output_dir, missing_ordinal);
    fs::remove_file(&missing_path).expect("teacher artifact should be removable");

    let error = load_result(output_dir).expect_err("missing required teacher artifact should fail");

    assert_eq!(
        error.to_string(),
        format!(
            "vertical-slice teacher artifact count drift: expected {} artifacts from scoreboard-derived branch count, found {}",
            expected_teacher_count,
            expected_teacher_count - 1
        )
    );

    Ok(())
}

fn load_snapshot_after_run(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<VerticalSliceGoldenSnapshot> {
    run_fixture_lane(output_dir, lane)?;
    load_snapshot(output_dir)
}

pub(crate) fn load_result(output_dir: &Path) -> Result<CanonicalVerticalSliceResult> {
    load_canonical_vertical_slice_result(output_dir)
}

pub(crate) fn load_snapshot(output_dir: &Path) -> Result<VerticalSliceGoldenSnapshot> {
    load_result(output_dir)?.golden_snapshot(
        VERTICAL_SLICE_EXPORT_DIR_NAME,
        VERTICAL_SLICE_SCOREBOARD_FILE_NAME,
        VERTICAL_SLICE_TEACHER_DIR_NAME,
    )
}

pub(crate) fn scoreboard_path(output_dir: &Path) -> PathBuf {
    scoreboard_artifact_path(output_dir)
}

fn load_persisted_fixture_for_lane(
    output_dir: &Path,
    lane: VerticalSliceFixtureLane,
) -> Result<VerticalSliceFixture> {
    let input_artifact = persisted_input_artifact_for_lane(lane);
    load_persisted_fixture(output_dir, &input_artifact)
}

fn load_persisted_fixture(
    output_dir: &Path,
    input_artifact: &PersistedVerticalSliceInputArtifact,
) -> Result<VerticalSliceFixture> {
    let input_path = vertical_slice_input_artifact_path(output_dir);
    write_vertical_slice_input_artifact(&input_path, ArtifactFormat::Json, input_artifact)?;
    let reloaded_artifact = read_vertical_slice_input_artifact(&input_path)?;
    Ok(fixture_from_persisted_input(&reloaded_artifact))
}

pub(crate) fn teacher_artifact_path(output_dir: &Path, ordinal: usize) -> PathBuf {
    output_dir
        .join(VERTICAL_SLICE_TEACHER_DIR_NAME)
        .join(format!("teacher-label-{ordinal}.json"))
}

pub(crate) fn rewrite_scoreboard_artifact(
    output_dir: &Path,
    artifact: &PersistedScoreboardArtifact,
) -> Result<()> {
    write_scoreboard_artifact(scoreboard_path(output_dir), ArtifactFormat::Json, artifact)
}

pub(crate) fn rewrite_teacher_artifact(
    output_dir: &Path,
    ordinal: usize,
    artifact: &PersistedTeacherLabelArtifact,
) -> Result<()> {
    write_teacher_label_artifact(
        teacher_artifact_path(output_dir, ordinal),
        ArtifactFormat::Json,
        artifact,
    )
}

pub(crate) fn rewrite_teacher_target_as_replay(
    output_dir: &Path,
    ordinal: usize,
    artifact: &mut PersistedTeacherLabelArtifact,
    replay_id: &str,
) -> Result<()> {
    artifact.payload.target = TeacherLabelTarget::Replay(ReplayId::new(replay_id));
    rewrite_teacher_artifact(output_dir, ordinal, artifact)
}

fn assert_scoreboard_component_keys_match(
    expected: &CanonicalVerticalSliceResult,
    observed: &CanonicalVerticalSliceResult,
    lane: VerticalSliceFixtureLane,
    branch_id: &str,
) -> Result<()> {
    let expected_row = expected
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .find(|row| row.branch_id.as_str() == branch_id)
        .ok_or_else(|| {
            MimirError::message(format!(
                "vertical-slice scoreboard component schema drift: lane {lane:?}, branch {branch_id}, expected branch row missing from baseline scoreboard"
            ))
        })?;
    let observed_row = observed
        .scoreboard_artifact
        .payload
        .rows
        .iter()
        .find(|row| row.branch_id.as_str() == branch_id)
        .ok_or_else(|| {
            MimirError::message(format!(
                "vertical-slice scoreboard component schema drift: lane {lane:?}, branch {branch_id}, observed branch row missing from scoreboard"
            ))
        })?;

    let expected_component_keys = expected_row
        .score
        .components
        .keys()
        .cloned()
        .collect::<Vec<_>>();
    let observed_component_keys = observed_row
        .score
        .components
        .keys()
        .cloned()
        .collect::<Vec<_>>();

    if expected_component_keys != observed_component_keys {
        return Err(MimirError::message(format!(
            "vertical-slice scoreboard component schema drift: lane {lane:?}, branch {branch_id}, expected component keys {expected_component_keys:?}, found {observed_component_keys:?}"
        )));
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_io::{PersistedScoreboard, read_artifact_auto, write_artifact};
    use mimir_types::ArtifactHeader;
    use tempfile::tempdir;

    #[test]
    fn persisted_vertical_slice_input_contract_round_trips_exactly() {
        let directory = tempdir().expect("tempdir should be created");
        let expected = persisted_input_artifact_for_lane(VerticalSliceFixtureLane::Stage69Sample);
        let path = vertical_slice_input_artifact_path(directory.path());

        write_vertical_slice_input_artifact(&path, ArtifactFormat::Json, &expected)
            .expect("vertical-slice input artifact should write");
        let decoded =
            read_vertical_slice_input_artifact(&path).expect("vertical-slice input should read");

        assert_eq!(decoded, expected);
    }

    #[test]
    fn persisted_stage69_vertical_slice_input_materializes_same_frozen_snapshot() {
        let directory = tempdir().expect("tempdir should be created");
        assert_fixture_lane_matches_expected_contract(
            directory.path(),
            VerticalSliceFixtureLane::Stage69Sample,
        )
        .expect("stage69 persisted input lane should keep the frozen snapshot");
    }

    #[test]
    fn persisted_stage77_vertical_slice_input_materializes_same_frozen_snapshot() {
        let directory = tempdir().expect("tempdir should be created");
        assert_fixture_lane_matches_expected_contract(
            directory.path(),
            VerticalSliceFixtureLane::Stage77Second,
        )
        .expect("stage77 persisted input lane should keep the frozen snapshot");
    }

    #[test]
    fn persisted_vertical_slice_input_repeated_runs_stay_identical() {
        let first = tempdir().expect("tempdir should be created");
        let second = tempdir().expect("tempdir should be created");
        assert_fixture_lane_repeated_runs_are_identical(
            first.path(),
            second.path(),
            VerticalSliceFixtureLane::Stage69Sample,
        )
        .expect("persisted stage69 input should remain deterministic");
    }

    #[test]
    fn persisted_vertical_slice_input_wrong_kind_fails_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = vertical_slice_input_artifact_path(directory.path());
        let wrong_kind = PersistedScoreboardArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Scoreboard, "mimir-cli-tests"),
            PersistedScoreboard { rows: Vec::new() },
        );

        write_artifact(&path, ArtifactFormat::Json, &wrong_kind)
            .expect("wrong-kind artifact should write");

        let error = read_vertical_slice_input_artifact(&path)
            .expect_err("wrong-kind input artifact should fail explicitly");

        assert_eq!(
            error.to_string(),
            format!(
                "artifact schema mismatch at {}: expected mimir.vertical_slice_input_artifact, found mimir.scoreboard_artifact",
                path.display()
            )
        );
    }

    #[test]
    fn persisted_vertical_slice_input_schema_mismatch_fails_explicitly() {
        let directory = tempdir().expect("tempdir should be created");
        let path = vertical_slice_input_artifact_path(directory.path());
        let mismatched = PersistedVerticalSliceInputArtifact::new(
            ArtifactHeader::new("mimir.vertical_slice_input_artifact", 2, "mimir-cli-tests"),
            persisted_input_artifact_for_lane(VerticalSliceFixtureLane::Stage69Sample).payload,
        );

        write_vertical_slice_input_artifact(&path, ArtifactFormat::Json, &mismatched)
            .expect("schema-mismatched artifact should write");

        let error = read_artifact_auto::<PersistedVerticalSliceInput>(
            &path,
            ArtifactKind::VerticalSliceInput.schema(),
        )
        .expect_err("schema mismatch should fail explicitly");

        assert_eq!(
            error.to_string(),
            format!(
                "unsupported schema version 2 for mimir.vertical_slice_input_artifact at {}; supported version is 1",
                path.display()
            )
        );
    }
}
