use mimir_cli::run_from;
use serde_json::Value;
use std::path::{Path, PathBuf};

fn config_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(Path::parent)
        .expect("mimir-cli should live under <repo>/crates/mimir-cli")
        .join("configs")
        .join(name)
}

fn run_json(args: Vec<String>) -> Value {
    let output = run_from(args).expect("plan-only CLI command should succeed");
    serde_json::from_str(&output).expect("CLI output should be valid JSON")
}

fn path_text(path: PathBuf) -> String {
    path.to_str()
        .expect("checked-in config paths should be UTF-8")
        .to_string()
}

#[test]
fn mine_plan_uses_checked_in_configs_without_claiming_execution() {
    let report = run_json(vec![
        "mimir-cli".to_string(),
        "mine".to_string(),
        "--base".to_string(),
        path_text(config_path("mimir.base.toml")),
        "--anchors".to_string(),
        path_text(config_path("anchors.toml")),
        "--branching".to_string(),
        path_text(config_path("branching.toml")),
        "--scoring".to_string(),
        path_text(config_path("scoring.toml")),
    ]);

    assert_eq!(report["command"], "mine");
    assert_eq!(report["mode"], "plan-only");
    assert_eq!(report["project_name"], "MIMIR");
    assert_eq!(report["configured_detector"], "manual-hints-only");
    assert_eq!(report["max_anchors_per_replay"], 32);
    assert_eq!(report["max_branches_per_anchor"], 4);
    assert_eq!(report["score_metric_count"], 2);
}

#[test]
fn label_and_library_plans_use_checked_in_labeling_config() {
    let base = path_text(config_path("mimir.base.toml"));
    let labeling = path_text(config_path("labeling.toml"));

    let label = run_json(vec![
        "mimir-cli".to_string(),
        "label".to_string(),
        "--base".to_string(),
        base.clone(),
        "--labeling".to_string(),
        labeling.clone(),
    ]);
    assert_eq!(label["command"], "label");
    assert_eq!(label["mode"], "plan-only");
    assert_eq!(label["project_name"], "MIMIR");
    assert_eq!(label["label_namespace"], "teacher");
    assert_eq!(label["default_confidence"], 1.0);

    let library = run_json(vec![
        "mimir-cli".to_string(),
        "build-library".to_string(),
        "--base".to_string(),
        base,
        "--labeling".to_string(),
        labeling,
    ]);
    assert_eq!(library["command"], "build-library");
    assert_eq!(library["mode"], "plan-only");
    assert_eq!(library["project_name"], "MIMIR");
    assert_eq!(library["label_namespace"], "teacher");
    assert_eq!(library["canonical_namespace"], "teacher");
}

#[test]
fn export_plans_remain_explicitly_plan_only() {
    let base = path_text(config_path("mimir.base.toml"));

    for (command, expected_format) in [
        ("export-bc", "behavior-cloning"),
        ("export-dagger", "dagger"),
    ] {
        let report = run_json(vec![
            "mimir-cli".to_string(),
            command.to_string(),
            "--base".to_string(),
            base.clone(),
        ]);

        assert_eq!(report["command"], "export");
        assert_eq!(report["mode"], "plan-only");
        assert_eq!(report["project_name"], "MIMIR");
        assert_eq!(report["export_format"], expected_format);
        assert_eq!(report["artifact_root"], "artifacts");
    }
}
