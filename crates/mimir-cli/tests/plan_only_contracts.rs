use mimir_cli::run_from;
use serde_json::Value;
use std::ffi::OsString;
use std::path::Path;
use tempfile::tempdir;

fn write(path: &Path, contents: &str) {
    std::fs::write(path, contents).expect("test config should be written");
}

fn parse_report(args: Vec<OsString>) -> (String, Value) {
    let first = run_from(args.clone()).expect("plan-only command should succeed");
    let second = run_from(args).expect("repeated plan-only command should succeed");
    assert_eq!(first, second, "plan-only reports must be deterministic");
    let value = serde_json::from_str(&first).expect("report should be valid JSON");
    (first, value)
}

#[test]
fn mine_plan_report_binds_all_configured_limits_without_side_effects() {
    let directory = tempdir().expect("tempdir should be created");
    let base = directory.path().join("base.toml");
    let anchors = directory.path().join("anchors.toml");
    let branching = directory.path().join("branching.toml");
    let scoring = directory.path().join("scoring.toml");

    write(
        &base,
        "project_name = \"MIMIR-PLAN\"\nartifact_root = \"planned-artifacts\"\nreplay_root = \"planned-replays\"\n",
    );
    write(
        &anchors,
        "detector = \"manual-hints-only\"\nmax_anchors_per_replay = 17\n",
    );
    write(&branching, "max_branches_per_anchor = 3\n");
    write(
        &scoring,
        "[weights]\ncoverage = 1.0\nstability = 0.5\nnovelty = 0.25\n",
    );

    let before: Vec<_> = std::fs::read_dir(directory.path())
        .unwrap()
        .map(|entry| entry.unwrap().file_name())
        .collect();
    let (_, report) = parse_report(vec![
        OsString::from("mimir-cli"),
        OsString::from("mine"),
        OsString::from("--base"),
        base.into_os_string(),
        OsString::from("--anchors"),
        anchors.into_os_string(),
        OsString::from("--branching"),
        branching.into_os_string(),
        OsString::from("--scoring"),
        scoring.into_os_string(),
    ]);
    let after: Vec<_> = std::fs::read_dir(directory.path())
        .unwrap()
        .map(|entry| entry.unwrap().file_name())
        .collect();

    assert_eq!(before.len(), after.len());
    assert_eq!(report["command"], "mine");
    assert_eq!(report["mode"], "plan-only");
    assert_eq!(report["project_name"], "MIMIR-PLAN");
    assert_eq!(report["configured_detector"], "manual-hints-only");
    assert_eq!(report["max_anchors_per_replay"], 17);
    assert_eq!(report["max_branches_per_anchor"], 3);
    assert_eq!(report["score_metric_count"], 3);
}

#[test]
fn label_plan_report_is_deterministic_and_preserves_config_values() {
    let directory = tempdir().expect("tempdir should be created");
    let base = directory.path().join("base.toml");
    let labeling = directory.path().join("labeling.toml");

    write(
        &base,
        "project_name = \"MIMIR-LABEL\"\nartifact_root = \"artifacts\"\nreplay_root = \"replays\"\n",
    );
    write(
        &labeling,
        "label_namespace = \"teacher.audit\"\ndefault_confidence = 0.625\n",
    );

    let (_, report) = parse_report(vec![
        OsString::from("mimir-cli"),
        OsString::from("label"),
        OsString::from("--base"),
        base.into_os_string(),
        OsString::from("--labeling"),
        labeling.into_os_string(),
    ]);

    assert_eq!(report["command"], "label");
    assert_eq!(report["mode"], "plan-only");
    assert_eq!(report["project_name"], "MIMIR-LABEL");
    assert_eq!(report["label_namespace"], "teacher.audit");
    assert_eq!(report["default_confidence"], 0.625);
    assert!(report["teacher_component"].is_string());
}

#[test]
fn export_commands_remain_plan_only_and_create_no_artifacts() {
    let directory = tempdir().expect("tempdir should be created");
    let base = directory.path().join("base.toml");
    write(
        &base,
        "project_name = \"MIMIR-EXPORT\"\nartifact_root = \"planned-artifacts\"\nreplay_root = \"replays\"\n",
    );

    let before: Vec<_> = std::fs::read_dir(directory.path())
        .unwrap()
        .map(|entry| entry.unwrap().file_name())
        .collect();

    for (command, expected_format) in [
        ("export-bc", "behavior-cloning"),
        ("export-dagger", "dagger"),
    ] {
        let (_, report) = parse_report(vec![
            OsString::from("mimir-cli"),
            OsString::from(command),
            OsString::from("--base"),
            base.clone().into_os_string(),
        ]);

        assert_eq!(report["command"], "export");
        assert_eq!(report["mode"], "plan-only");
        assert_eq!(report["project_name"], "MIMIR-EXPORT");
        assert_eq!(report["export_format"], expected_format);
        assert_eq!(report["artifact_root"], "planned-artifacts");
    }

    let after: Vec<_> = std::fs::read_dir(directory.path())
        .unwrap()
        .map(|entry| entry.unwrap().file_name())
        .collect();
    assert_eq!(before, after, "plan-only export must not create artifacts");
    assert!(!directory.path().join("planned-artifacts").exists());
}
