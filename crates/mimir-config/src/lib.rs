use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::fmt;
use std::path::PathBuf;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConfigValidationError {
    pub field: &'static str,
    pub detail: String,
}

impl ConfigValidationError {
    fn new(field: &'static str, detail: impl Into<String>) -> Self {
        Self {
            field,
            detail: detail.into(),
        }
    }
}

impl fmt::Display for ConfigValidationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "invalid config field {}: {}", self.field, self.detail)
    }
}

impl std::error::Error for ConfigValidationError {}

pub trait ValidateConfig {
    fn validate(&self) -> Result<(), ConfigValidationError>;
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct BaseConfig {
    pub project_name: String,
    pub artifact_root: PathBuf,
    pub replay_root: PathBuf,
}

impl ValidateConfig for BaseConfig {
    fn validate(&self) -> Result<(), ConfigValidationError> {
        if self.project_name.trim().is_empty() {
            return Err(ConfigValidationError::new(
                "project_name",
                "must not be blank",
            ));
        }
        if self.artifact_root.as_os_str().is_empty() {
            return Err(ConfigValidationError::new(
                "artifact_root",
                "must not be empty",
            ));
        }
        if self.replay_root.as_os_str().is_empty() {
            return Err(ConfigValidationError::new(
                "replay_root",
                "must not be empty",
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
    fn validate(&self) -> Result<(), ConfigValidationError> {
        if self.detector.trim().is_empty() {
            return Err(ConfigValidationError::new("detector", "must not be blank"));
        }
        if self.max_anchors_per_replay == 0 {
            return Err(ConfigValidationError::new(
                "max_anchors_per_replay",
                "must be greater than zero",
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
    fn validate(&self) -> Result<(), ConfigValidationError> {
        if self.max_branches_per_anchor == 0 {
            return Err(ConfigValidationError::new(
                "max_branches_per_anchor",
                "must be greater than zero",
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
    fn validate(&self) -> Result<(), ConfigValidationError> {
        for (name, weight) in &self.weights {
            if name.trim().is_empty() {
                return Err(ConfigValidationError::new(
                    "weights",
                    "metric names must not be blank",
                ));
            }
            if !weight.is_finite() {
                return Err(ConfigValidationError::new(
                    "weights",
                    format!("metric {name} has a non-finite weight"),
                ));
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
    fn validate(&self) -> Result<(), ConfigValidationError> {
        if self.label_namespace.trim().is_empty() {
            return Err(ConfigValidationError::new(
                "label_namespace",
                "must not be blank",
            ));
        }
        if !self.default_confidence.is_finite()
            || !(0.0_f32..=1.0_f32).contains(&self.default_confidence)
        {
            return Err(ConfigValidationError::new(
                "default_confidence",
                "must be finite and within [0, 1]",
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
    fn validate(&self) -> Result<(), ConfigValidationError> {
        if self.command_labels.iter().any(|label| label.trim().is_empty()) {
            return Err(ConfigValidationError::new(
                "command_labels",
                "entries must not be blank",
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
        config.validate().expect("valid base config");
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
        config.validate().expect("valid loop config");
    }

    #[test]
    fn base_anchor_and_branch_limits_fail_closed_on_invalid_values() {
        let invalid_base = BaseConfig {
            project_name: "   ".to_string(),
            artifact_root: PathBuf::from("artifacts"),
            replay_root: PathBuf::from("replays"),
        };
        assert!(invalid_base.validate().is_err());

        let invalid_anchor = AnchorsConfig {
            detector: "manual".to_string(),
            max_anchors_per_replay: 0,
        };
        assert!(invalid_anchor.validate().is_err());

        let invalid_branch = BranchingConfig {
            max_branches_per_anchor: 0,
        };
        assert!(invalid_branch.validate().is_err());
    }

    #[test]
    fn scoring_validation_rejects_blank_metric_and_non_finite_weight() {
        let blank = ScoringConfig {
            weights: BTreeMap::from([("  ".to_string(), 1.0)]),
        };
        assert!(blank.validate().is_err());

        let non_finite = ScoringConfig {
            weights: BTreeMap::from([("coverage".to_string(), f64::NAN)]),
        };
        assert!(non_finite.validate().is_err());

        let valid = ScoringConfig {
            weights: BTreeMap::from([("coverage".to_string(), -0.25)]),
        };
        valid.validate().expect("finite scoring config");
    }

    #[test]
    fn labeling_validation_enforces_finite_unit_interval_confidence() {
        for value in [f32::NAN, f32::NEG_INFINITY, -0.1, 1.1] {
            let invalid = LabelingConfig {
                label_namespace: "teacher".to_string(),
                default_confidence: value,
            };
            assert!(invalid.validate().is_err());
        }

        for value in [0.0, 0.5, 1.0] {
            let valid = LabelingConfig {
                label_namespace: "teacher".to_string(),
                default_confidence: value,
            };
            valid.validate().expect("bounded labeling confidence");
        }
    }

    #[test]
    fn loop_validation_rejects_blank_entries_without_rejecting_empty_command_lists() {
        LoopConfig {
            backend: LoopBackend::DeterministicFake,
            default_seed: 0,
            command_labels: Vec::new(),
        }
        .validate()
        .expect("an empty deterministic command list remains allowed");

        let invalid = LoopConfig {
            backend: LoopBackend::DeterministicFake,
            default_seed: 0,
            command_labels: vec!["tick".to_string(), "   ".to_string()],
        };
        assert!(invalid.validate().is_err());
    }
}
