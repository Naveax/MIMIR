use mimir_core::{MimirError, Result};
use mimir_types::BranchId;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ScoreVector {
    pub branch_id: Option<BranchId>,
    pub components: BTreeMap<String, f64>,
    pub total: f64,
}

pub trait Scorer {
    fn score(&self, branch_id: Option<BranchId>, signals: &BTreeMap<String, f64>) -> ScoreVector;
}

/// Additive fail-closed scoring surface for callers that cannot tolerate NaN/Infinity leakage.
///
/// The legacy `Scorer` trait is intentionally preserved for compatibility. New correctness-
/// sensitive pipelines can opt into this checked surface and receive an explicit error instead
/// of a non-finite score vector.
pub trait CheckedScorer {
    fn score_checked(
        &self,
        branch_id: Option<BranchId>,
        signals: &BTreeMap<String, f64>,
    ) -> Result<ScoreVector>;
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct WeightedSumScorer {
    pub weights: BTreeMap<String, f64>,
}

impl WeightedSumScorer {
    pub fn new(weights: BTreeMap<String, f64>) -> Self {
        Self { weights }
    }

    pub fn metric_count(&self) -> usize {
        self.weights.len()
    }

    pub fn validate_finite(&self) -> Result<()> {
        for (name, weight) in &self.weights {
            if !weight.is_finite() {
                return Err(MimirError::message(format!(
                    "non-finite scorer weight for metric {name}"
                )));
            }
        }
        Ok(())
    }
}

impl Scorer for WeightedSumScorer {
    fn score(&self, branch_id: Option<BranchId>, signals: &BTreeMap<String, f64>) -> ScoreVector {
        let mut components = BTreeMap::new();
        let mut total = 0.0;

        for (name, signal) in signals {
            let weighted_value = self.weights.get(name).copied().unwrap_or(0.0) * signal;
            components.insert(name.clone(), weighted_value);
            total += weighted_value;
        }

        ScoreVector {
            branch_id,
            components,
            total,
        }
    }
}

impl CheckedScorer for WeightedSumScorer {
    fn score_checked(
        &self,
        branch_id: Option<BranchId>,
        signals: &BTreeMap<String, f64>,
    ) -> Result<ScoreVector> {
        self.validate_finite()?;

        let mut components = BTreeMap::new();
        let mut total = 0.0_f64;

        for (name, signal) in signals {
            if !signal.is_finite() {
                return Err(MimirError::message(format!(
                    "non-finite scorer signal for metric {name}"
                )));
            }

            let weight = self.weights.get(name).copied().unwrap_or(0.0);
            let weighted_value = weight * signal;
            if !weighted_value.is_finite() {
                return Err(MimirError::message(format!(
                    "non-finite weighted scorer component for metric {name}"
                )));
            }

            let next_total = total + weighted_value;
            if !next_total.is_finite() {
                return Err(MimirError::message(format!(
                    "non-finite scorer total after metric {name}"
                )));
            }

            components.insert(name.clone(), weighted_value);
            total = next_total;
        }

        Ok(ScoreVector {
            branch_id,
            components,
            total,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn weighted_sum_is_deterministic() {
        let scorer = WeightedSumScorer::new(BTreeMap::from([
            ("coverage".to_string(), 1.0),
            ("stability".to_string(), 0.5),
        ]));
        let signals = BTreeMap::from([
            ("coverage".to_string(), 3.0),
            ("stability".to_string(), 4.0),
        ]);

        let score = scorer.score(Some(BranchId::new("branch-1")), &signals);

        assert_eq!(score.total, 5.0);
        assert_eq!(score.components["coverage"], 3.0);
        assert_eq!(score.components["stability"], 2.0);
    }

    #[test]
    fn checked_weighted_sum_matches_legacy_for_finite_inputs() {
        let scorer = WeightedSumScorer::new(BTreeMap::from([
            ("coverage".to_string(), 1.0),
            ("stability".to_string(), 0.5),
        ]));
        let signals = BTreeMap::from([
            ("coverage".to_string(), 3.0),
            ("stability".to_string(), 4.0),
            ("unweighted".to_string(), 99.0),
        ]);
        let branch_id = Some(BranchId::new("branch-1"));

        let legacy = scorer.score(branch_id.clone(), &signals);
        let checked = scorer
            .score_checked(branch_id, &signals)
            .expect("finite score should validate");

        assert_eq!(checked, legacy);
        assert_eq!(checked.components["unweighted"], 0.0);
    }

    #[test]
    fn checked_weighted_sum_rejects_non_finite_configuration_and_signals() {
        let bad_weight =
            WeightedSumScorer::new(BTreeMap::from([("coverage".to_string(), f64::NAN)]));
        let finite_signals = BTreeMap::from([("coverage".to_string(), 1.0)]);
        assert!(bad_weight.score_checked(None, &finite_signals).is_err());

        let scorer = WeightedSumScorer::new(BTreeMap::from([("coverage".to_string(), 1.0)]));
        let bad_signal = BTreeMap::from([("coverage".to_string(), f64::INFINITY)]);
        assert!(scorer.score_checked(None, &bad_signal).is_err());
    }

    #[test]
    fn checked_weighted_sum_rejects_finite_inputs_that_overflow() {
        let scorer = WeightedSumScorer::new(BTreeMap::from([("overflow".to_string(), f64::MAX)]));
        let signals = BTreeMap::from([("overflow".to_string(), 2.0)]);

        let error = scorer
            .score_checked(None, &signals)
            .expect_err("overflow must fail closed");
        assert!(
            error
                .to_string()
                .contains("non-finite weighted scorer component")
        );
    }
}
