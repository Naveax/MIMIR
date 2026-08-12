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
}
