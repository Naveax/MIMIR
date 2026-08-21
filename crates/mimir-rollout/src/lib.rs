use mimir_core::{MimirError, NamedComponent, Result};
use mimir_types::{ActionRecord, BranchId, BranchRecord, StateSnapshot};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct RolloutStep {
    pub step_index: u32,
    pub action: Option<ActionRecord>,
    pub state: Option<StateSnapshot>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct RolloutRequest {
    pub branch: BranchRecord,
    pub max_steps: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct RolloutArtifact {
    pub branch_id: BranchId,
    pub steps: Vec<RolloutStep>,
}

pub trait RolloutEngine {
    fn rollout(&self, request: &RolloutRequest) -> Result<RolloutArtifact>;
}

/// Additive validation surface for persisted or cached rollout artifacts.
///
/// This deliberately does not imply that a real rollout engine exists. It only verifies the
/// bounded identity/index invariants that are already explicit in `RolloutRequest` and
/// `RolloutArtifact`, allowing callers to fail closed before reusing an artifact.
pub trait RolloutArtifactVerifier {
    fn verify_artifact(&self, request: &RolloutRequest, artifact: &RolloutArtifact) -> Result<()>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct BoundedRolloutArtifactVerifier;

impl RolloutArtifactVerifier for BoundedRolloutArtifactVerifier {
    fn verify_artifact(&self, request: &RolloutRequest, artifact: &RolloutArtifact) -> Result<()> {
        if request.max_steps == 0 {
            return Err(MimirError::message(
                "rollout request max_steps must be greater than zero",
            ));
        }

        if artifact.branch_id != request.branch.id {
            return Err(MimirError::message(format!(
                "rollout artifact branch mismatch: expected {}, got {}",
                request.branch.id, artifact.branch_id
            )));
        }

        if artifact.steps.len() > request.max_steps {
            return Err(MimirError::message(format!(
                "rollout artifact step count {} exceeds max_steps {}",
                artifact.steps.len(),
                request.max_steps
            )));
        }

        let mut seen_indices = BTreeSet::new();
        for step in &artifact.steps {
            let step_index = usize::try_from(step.step_index)
                .map_err(|_| MimirError::message("rollout step index does not fit usize"))?;
            if step_index >= request.max_steps {
                return Err(MimirError::message(format!(
                    "rollout step index {} is outside max_steps {}",
                    step.step_index, request.max_steps
                )));
            }
            if !seen_indices.insert(step.step_index) {
                return Err(MimirError::message(format!(
                    "duplicate rollout step index {}",
                    step.step_index
                )));
            }
        }

        Ok(())
    }
}

#[derive(Debug, Default, Clone, Copy)]
pub struct UnavailableRolloutEngine;

impl NamedComponent for UnavailableRolloutEngine {
    fn component_name(&self) -> &'static str {
        "unavailable-rollout-engine"
    }
}

impl RolloutEngine for UnavailableRolloutEngine {
    fn rollout(&self, _request: &RolloutRequest) -> Result<RolloutArtifact> {
        Err(MimirError::message(
            "no rollout engine is bundled in this scaffold",
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_types::{AnchorId, AnchorKind, AnchorRecord, BranchOrigin, FrameIndex, ReplayId};

    fn request(max_steps: usize) -> RolloutRequest {
        RolloutRequest {
            branch: BranchRecord {
                id: BranchId::new("branch-1"),
                anchor_id: AnchorId::new("anchor-1"),
                origin: BranchOrigin::Manual,
                label: Some("candidate".to_string()),
                actions: Vec::new(),
                legality_hint: Some(true),
                metadata: Default::default(),
            },
            max_steps,
        }
    }

    #[test]
    fn unavailable_engine_returns_explicit_error() {
        let request = request(8);

        let error = UnavailableRolloutEngine
            .rollout(&request)
            .expect_err("rollout should be unavailable");

        assert!(
            error
                .to_string()
                .contains("no rollout engine is bundled in this scaffold")
        );

        let _anchor = AnchorRecord {
            id: AnchorId::new("anchor-1"),
            replay_id: ReplayId::new("replay-1"),
            frame_index: FrameIndex::new(1),
            kind: AnchorKind::Manual,
            metadata: Default::default(),
        };
    }

    #[test]
    fn bounded_verifier_accepts_sparse_unique_indices_within_request_bound() {
        let request = request(8);
        let artifact = RolloutArtifact {
            branch_id: request.branch.id.clone(),
            steps: vec![
                RolloutStep {
                    step_index: 0,
                    action: None,
                    state: None,
                },
                RolloutStep {
                    step_index: 7,
                    action: None,
                    state: None,
                },
            ],
        };

        BoundedRolloutArtifactVerifier
            .verify_artifact(&request, &artifact)
            .expect("bounded artifact should verify");
    }

    #[test]
    fn bounded_verifier_rejects_branch_and_count_drift() {
        let request = request(1);
        let wrong_branch = RolloutArtifact {
            branch_id: BranchId::new("branch-2"),
            steps: Vec::new(),
        };
        assert!(
            BoundedRolloutArtifactVerifier
                .verify_artifact(&request, &wrong_branch)
                .is_err()
        );

        let too_many = RolloutArtifact {
            branch_id: request.branch.id.clone(),
            steps: vec![
                RolloutStep {
                    step_index: 0,
                    action: None,
                    state: None,
                },
                RolloutStep {
                    step_index: 0,
                    action: None,
                    state: None,
                },
            ],
        };
        assert!(
            BoundedRolloutArtifactVerifier
                .verify_artifact(&request, &too_many)
                .is_err()
        );
    }

    #[test]
    fn bounded_verifier_rejects_zero_bound_duplicate_and_out_of_range_indices() {
        let zero_request = request(0);
        let empty = RolloutArtifact {
            branch_id: zero_request.branch.id.clone(),
            steps: Vec::new(),
        };
        assert!(
            BoundedRolloutArtifactVerifier
                .verify_artifact(&zero_request, &empty)
                .is_err()
        );

        let request = request(4);
        let duplicate = RolloutArtifact {
            branch_id: request.branch.id.clone(),
            steps: vec![
                RolloutStep {
                    step_index: 1,
                    action: None,
                    state: None,
                },
                RolloutStep {
                    step_index: 1,
                    action: None,
                    state: None,
                },
            ],
        };
        assert!(
            BoundedRolloutArtifactVerifier
                .verify_artifact(&request, &duplicate)
                .is_err()
        );

        let out_of_range = RolloutArtifact {
            branch_id: request.branch.id.clone(),
            steps: vec![RolloutStep {
                step_index: 4,
                action: None,
                state: None,
            }],
        };
        assert!(
            BoundedRolloutArtifactVerifier
                .verify_artifact(&request, &out_of_range)
                .is_err()
        );
    }
}
