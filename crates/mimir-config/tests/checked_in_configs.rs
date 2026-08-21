use mimir_config::{
    AnchorsConfig, BaseConfig, BranchingConfig, LabelingConfig, LoopBackend, LoopConfig,
    ScoringConfig,
};
use std::path::{Path, PathBuf};

fn config_text(name: &str) -> String {
    let repo_root = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(Path::parent)
        .expect("mimir-config should live under <repo>/crates/mimir-config");
    let path = repo_root.join("configs").join(name);
    std::fs::read_to_string(&path)
        .unwrap_or_else(|error| panic!("failed to read checked-in config {}: {error}", path.display()))
}

#[test]
fn checked_in_configs_match_public_models_and_expected_defaults() {
    let base: BaseConfig =
        toml::from_str(&config_text("mimir.base.toml")).expect("base config should parse");
    assert_eq!(base.project_name, "MIMIR");
    assert_eq!(base.artifact_root, PathBuf::from("artifacts"));
    assert_eq!(base.replay_root, PathBuf::from("replays"));

    let anchors: AnchorsConfig =
        toml::from_str(&config_text("anchors.toml")).expect("anchors config should parse");
    assert_eq!(anchors.detector, "manual-hints-only");
    assert_eq!(anchors.max_anchors_per_replay, 32);

    let branching: BranchingConfig =
        toml::from_str(&config_text("branching.toml")).expect("branching config should parse");
    assert_eq!(branching.max_branches_per_anchor, 4);

    let scoring: ScoringConfig =
        toml::from_str(&config_text("scoring.toml")).expect("scoring config should parse");
    assert_eq!(scoring.weights.len(), 2);
    assert_eq!(scoring.weights.get("coverage"), Some(&1.0));
    assert_eq!(scoring.weights.get("stability"), Some(&0.5));

    let labeling: LabelingConfig =
        toml::from_str(&config_text("labeling.toml")).expect("labeling config should parse");
    assert_eq!(labeling.label_namespace, "teacher");
    assert_eq!(labeling.default_confidence, 1.0);

    let loop_config: LoopConfig =
        toml::from_str(&config_text("loop.toml")).expect("loop config should parse");
    assert_eq!(loop_config.backend, LoopBackend::DeterministicFake);
    assert_eq!(loop_config.default_seed, 7);
    assert_eq!(loop_config.command_labels, vec!["bootstrap", "tick"]);
}
