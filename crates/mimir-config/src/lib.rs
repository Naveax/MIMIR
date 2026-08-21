use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct BaseConfig {
    pub project_name: String,
    pub artifact_root: PathBuf,
    pub replay_root: PathBuf,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct AnchorsConfig {
    pub detector: String,
    pub max_anchors_per_replay: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct BranchingConfig {
    pub max_branches_per_anchor: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct ScoringConfig {
    pub weights: BTreeMap<String, f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct LabelingConfig {
    pub label_namespace: String,
    pub default_confidence: f32,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum LoopBackend {
    #[serde(rename = "deterministic-fake")]
    DeterministicFake,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LoopConfig {
    pub backend: LoopBackend,
    pub default_seed: u64,
    pub command_labels: Vec<String>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn base_config_deserializes_pathbuf_fields_from_toml() {
        let config: BaseConfig = toml::from_str(
            r#"
project_name = "MIMIR"
artifact_root = "artifacts"
replay_root = "replays/subdir"
"#,
        )
        .expect("base config should deserialize");

        assert_eq!(config.project_name, "MIMIR");
        assert_eq!(config.artifact_root, PathBuf::from("artifacts"));
        assert_eq!(config.replay_root, PathBuf::from("replays/subdir"));
    }

    #[test]
    fn loop_config_deserializes_backend_enum_from_toml() {
        let config: LoopConfig = toml::from_str(
            r#"
backend = "deterministic-fake"
default_seed = 7
command_labels = ["bootstrap", "tick"]
"#,
        )
        .expect("loop config should deserialize");

        assert_eq!(config.backend, LoopBackend::DeterministicFake);
        assert_eq!(config.default_seed, 7);
        assert_eq!(config.command_labels, vec!["bootstrap", "tick"]);
    }

    #[test]
    fn public_config_structs_reject_unknown_fields() {
        let cases = [
            (
                "base",
                r#"
project_name = "MIMIR"
artifact_root = "artifacts"
replay_root = "replays"
unexpected = true
"#,
            ),
            (
                "anchors",
                r#"
detector = "manual-hints-only"
max_anchors_per_replay = 32
unexpected = true
"#,
            ),
            (
                "branching",
                r#"
max_branches_per_anchor = 4
unexpected = true
"#,
            ),
            (
                "labeling",
                r#"
label_namespace = "teacher"
default_confidence = 1.0
unexpected = true
"#,
            ),
            (
                "loop",
                r#"
backend = "deterministic-fake"
default_seed = 7
command_labels = ["bootstrap", "tick"]
unexpected = true
"#,
            ),
        ];

        for (kind, input) in cases {
            let rejected = match kind {
                "base" => toml::from_str::<BaseConfig>(input).is_err(),
                "anchors" => toml::from_str::<AnchorsConfig>(input).is_err(),
                "branching" => toml::from_str::<BranchingConfig>(input).is_err(),
                "labeling" => toml::from_str::<LabelingConfig>(input).is_err(),
                "loop" => toml::from_str::<LoopConfig>(input).is_err(),
                _ => unreachable!("all test cases use known config kinds"),
            };
            assert!(rejected, "{kind} config accepted an unknown field");
        }

        let scoring = r#"
unexpected = true

[weights]
coverage = 1.0
"#;
        assert!(
            toml::from_str::<ScoringConfig>(scoring).is_err(),
            "scoring config accepted an unknown top-level field"
        );
    }
}
