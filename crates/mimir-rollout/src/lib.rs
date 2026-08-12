use mimir_core::{MimirError, NamedComponent, Result};
use mimir_types::{ActionRecord, BranchId, BranchRecord, StateSnapshot};
use serde::{Deserialize, Serialize};

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

    #[test]
    fn unavailable_engine_returns_explicit_error() {
        let request = RolloutRequest {
            branch: BranchRecord {
                id: BranchId::new("branch-1"),
                anchor_id: AnchorId::new("anchor-1"),
                origin: BranchOrigin::Manual,
                label: Some("candidate".to_string()),
                actions: Vec::new(),
                legality_hint: Some(true),
                metadata: Default::default(),
            },
            max_steps: 8,
        };

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
}
