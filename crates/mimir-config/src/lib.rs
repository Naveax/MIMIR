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
    fn structured_configs_reject_unknown_fields() {
        let base = toml::from_str::<BaseConfig>(
            r#"
project_name = "MIMIR"
artifact_root = "artifacts"
replay_root = "replays"
project_nmae = "typo"
"#,
        )
        .expect_err("base config must reject unknown fields");
        assert!(base.to_string().contains("unknown field"));

        let anchors = toml::from_str::<AnchorsConfig>(
            r#"
detector = "hint"
max_anchors_per_replay = 8
max_anchors_per_repla = 99
"#,
        )
        .expect_err("anchors config must reject unknown fields");
        assert!(anchors.to_string().contains("unknown field"));

        let branching = toml::from_str::<BranchingConfig>(
            r#"
max_branches_per_anchor = 4
max_branches_per_anchro = 99
"#,
        )
        .expect_err("branching config must reject unknown fields");
        assert!(branching.to_string().contains("unknown field"));

        let scoring = toml::from_str::<ScoringConfig>(
            r#"
extra = "typo"
[weights]
coverage = 1.0
"#,
        )
        .expect_err("scoring config must reject unknown fields");
        assert!(scoring.to_string().contains("unknown field"));

        let labeling = toml::from_str::<LabelingConfig>(
            r#"
label_namespace = "teacher"
default_confidence = 0.5
default_confidnce = 0.9
"#,
        )
        .expect_err("labeling config must reject unknown fields");
        assert!(labeling.to_string().contains("unknown field"));

        let loop_config = toml::from_str::<LoopConfig>(
            r#"
backend = "deterministic-fake"
default_seed = 7
command_labels = ["bootstrap"]
default_sead = 99
"#,
        )
        .expect_err("loop config must reject unknown fields");
        assert!(loop_config.to_string().contains("unknown field"));
    }
}
