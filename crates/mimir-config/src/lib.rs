use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct BaseConfig {
    pub project_name: String,
    pub artifact_root: PathBuf,
    pub replay_root: PathBuf,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct AnchorsConfig {
    pub detector: String,
    pub max_anchors_per_replay: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct BranchingConfig {
    pub max_branches_per_anchor: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ScoringConfig {
    pub weights: BTreeMap<String, f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
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
}
