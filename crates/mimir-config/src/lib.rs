use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::fmt;
use std::path::PathBuf;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConfigValidationError {
    message: String,
}

impl ConfigValidationError {
    fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

impl fmt::Display for ConfigValidationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.message)
    }
}

impl std::error::Error for ConfigValidationError {}

pub type ConfigValidationResult = Result<(), ConfigValidationError>;

pub trait ValidateConfig {
    fn validate(&self) -> ConfigValidationResult;
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct BaseConfig {
    pub project_name: String,
    pub artifact_root: PathBuf,
    pub replay_root: PathBuf,
}

impl ValidateConfig for BaseConfig {
    fn validate(&self) -> ConfigValidationResult {
        if self.project_name.trim().is_empty() {
            return Err(ConfigValidationError::new(
                "base project_name must not be blank",
            ));
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct AnchorsConfig {
    pub detector: String,
    pub max_anchors_per_replay: usize,
}

impl ValidateConfig for AnchorsConfig {
    fn validate(&self) -> ConfigValidationResult {
        if self.detector.trim().is_empty() {
            return Err(ConfigValidationError::new(
                "anchors detector must not be blank",
            ));
        }
        if self.max_anchors_per_replay == 0 {
            return Err(ConfigValidationError::new(
                "max_anchors_per_replay must be greater than zero",
            ));
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct BranchingConfig {
    pub max_branches_per_anchor: usize,
}

impl ValidateConfig for BranchingConfig {
    fn validate(&self) -> ConfigValidationResult {
        if self.max_branches_per_anchor == 0 {
            return Err(ConfigValidationError::new(
                "max_branches_per_anchor must be greater than zero",
            ));
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ScoringConfig {
    pub weights: BTreeMap<String, f64>,
}

impl ValidateConfig for ScoringConfig {
    fn validate(&self) -> ConfigValidationResult {
        for (name, weight) in &self.weights {
            if !weight.is_finite() {
                return Err(ConfigValidationError::new(format!(
                    "scoring weight {name} must be finite"
                )));
            }
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct LabelingConfig {
    pub label_namespace: String,
    pub default_confidence: f32,
}

impl ValidateConfig for LabelingConfig {
    fn validate(&self) -> ConfigValidationResult {
        if self.label_namespace.trim().is_empty() {
            return Err(ConfigValidationError::new(
                "label_namespace must not be blank",
            ));
        }
        if !self.default_confidence.is_finite() {
            return Err(ConfigValidationError::new(
                "default_confidence must be finite",
            ));
        }
        if !(0.0..=1.0).contains(&self.default_confidence) {
            return Err(ConfigValidationError::new(
                "default_confidence must be within [0, 1]",
            ));
        }
        Ok(())
    }
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

impl ValidateConfig for LoopConfig {
    fn validate(&self) -> ConfigValidationResult {
        if self
            .command_labels
            .iter()
            .any(|label| label.trim().is_empty())
        {
            return Err(ConfigValidationError::new(
                "loop command_labels must not contain blank values",
            ));
        }
        Ok(())
    }
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
