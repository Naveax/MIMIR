use mimir_config::{
    AnchorsConfig, BaseConfig, BranchingConfig, LabelingConfig, LoopBackend, LoopConfig,
    ScoringConfig, ValidateConfig,
};
use std::collections::BTreeMap;
use std::path::PathBuf;

#[test]
fn semantic_validation_accepts_finite_nonzero_baseline_configs() {
    BaseConfig {
        project_name: "MIMIR".to_string(),
        artifact_root: PathBuf::from("artifacts"),
        replay_root: PathBuf::from("replays"),
    }
    .validate()
    .expect("base config");

    AnchorsConfig {
        detector: "hint".to_string(),
        max_anchors_per_replay: 1,
    }
    .validate()
    .expect("anchors config");

    BranchingConfig {
        max_branches_per_anchor: 1,
    }
    .validate()
    .expect("branching config");

    ScoringConfig {
        weights: BTreeMap::from([("quality".to_string(), -2.5), ("novelty".to_string(), 0.0)]),
    }
    .validate()
    .expect("scoring config");

    LabelingConfig {
        label_namespace: "teacher".to_string(),
        default_confidence: 0.5,
    }
    .validate()
    .expect("labeling config");

    LoopConfig {
        backend: LoopBackend::DeterministicFake,
        default_seed: 0,
        command_labels: vec!["bootstrap".to_string(), "tick".to_string()],
    }
    .validate()
    .expect("loop config");
}

#[test]
fn semantic_validation_rejects_blank_names_and_zero_bounds() {
    assert!(
        BaseConfig {
            project_name: "   ".to_string(),
            artifact_root: PathBuf::from("artifacts"),
            replay_root: PathBuf::from("replays"),
        }
        .validate()
        .is_err()
    );
    assert!(
        AnchorsConfig {
            detector: "   ".to_string(),
            max_anchors_per_replay: 1,
        }
        .validate()
        .is_err()
    );
    assert!(
        AnchorsConfig {
            detector: "hint".to_string(),
            max_anchors_per_replay: 0,
        }
        .validate()
        .is_err()
    );
    assert!(
        BranchingConfig {
            max_branches_per_anchor: 0,
        }
        .validate()
        .is_err()
    );
    assert!(
        LabelingConfig {
            label_namespace: "   ".to_string(),
            default_confidence: 0.5,
        }
        .validate()
        .is_err()
    );
    assert!(
        LoopConfig {
            backend: LoopBackend::DeterministicFake,
            default_seed: 7,
            command_labels: vec!["bootstrap".to_string(), "   ".to_string()],
        }
        .validate()
        .is_err()
    );
}

#[test]
fn semantic_validation_rejects_non_finite_values_and_out_of_range_confidence() {
    for weight in [f64::NAN, f64::INFINITY, f64::NEG_INFINITY] {
        assert!(
            ScoringConfig {
                weights: BTreeMap::from([("quality".to_string(), weight)]),
            }
            .validate()
            .is_err()
        );
    }

    for confidence in [f32::NAN, f32::INFINITY, f32::NEG_INFINITY, -0.01, 1.01] {
        assert!(
            LabelingConfig {
                label_namespace: "teacher".to_string(),
                default_confidence: confidence,
            }
            .validate()
            .is_err()
        );
    }

    for confidence in [0.0, 1.0] {
        LabelingConfig {
            label_namespace: "teacher".to_string(),
            default_confidence: confidence,
        }
        .validate()
        .expect("closed confidence interval endpoints remain valid");
    }
}
