use mimir_core::{MimirError, NamedComponent, Result, hash_serializable};
use mimir_types::{ActionRecord, BranchId, BranchRecord, StateSnapshot};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

pub const ROLLOUT_REQUEST_BINDING_DOMAIN_V1: &str = "mimir.rollout.request-binding.v1";

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

/// Versioned wrapper that binds an existing rollout artifact to the exact serialized request
/// content used to authorize it. The legacy `RolloutArtifact` wire contract remains unchanged.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct BoundRolloutArtifactV1 {
    pub request_digest: String,
    pub artifact: RolloutArtifact,
}

pub trait RolloutEngine {
    fn rollout(&self, request: &RolloutRequest) -> Result<RolloutArtifact>;
}

/// Computes a deterministic, domain-separated digest over the complete rollout request.
///
/// `BranchRecord` includes its opaque ID plus anchor, origin, label, actions, legality hint, and
/// metadata. `Metadata` is backed by `BTreeMap`, so the serde representation used by
/// `hash_serializable` has deterministic key ordering. `max_steps` is included as part of the
/// request. Changing branch content while reusing the same `BranchId` therefore changes this
/// digest.
pub fn rollout_request_digest_v1(request: &RolloutRequest) -> Result<String> {
    hash_serializable(&(ROLLOUT_REQUEST_BINDING_DOMAIN_V1, request))
}

/// Creates a content-bound wrapper only after the artifact satisfies the request's explicit
/// branch and step-bound invariants.
pub fn bind_rollout_artifact_v1(
    request: &RolloutRequest,
    artifact: RolloutArtifact,
) -> Result<BoundRolloutArtifactV1> {
    verify_rollout_artifact_bounds(request, &artifact)?;

    Ok(BoundRolloutArtifactV1 {
        request_digest: rollout_request_digest_v1(request)?,
        artifact,
    })
}

/// Verifies both the full request-content binding and the existing bounded rollout invariants.
pub fn verify_bound_rollout_artifact_v1(
    request: &RolloutRequest,
    bound: &BoundRolloutArtifactV1,
) -> Result<()> {
    let expected_digest = rollout_request_digest_v1(request)?;
    if bound.request_digest != expected_digest {
        return Err(MimirError::message(format!(
            "rollout request digest mismatch: expected {expected_digest}, got {}",
            bound.request_digest
        )));
    }

    verify_rollout_artifact_bounds(request, &bound.artifact)
}

fn verify_rollout_artifact_bounds(
    request: &RolloutRequest,
    artifact: &RolloutArtifact,
) -> Result<()> {
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
    use mimir_types::{
        AnchorId, AnchorKind, AnchorRecord, BranchOrigin, FieldValue, FrameIndex, Metadata,
        ReplayId,
    };

    fn request(max_steps: usize) -> RolloutRequest {
        RolloutRequest {
            branch: BranchRecord {
                id: BranchId::new("branch-1"),
                anchor_id: AnchorId::new("anchor-1"),
                origin: BranchOrigin::Manual,
                label: Some("candidate".to_string()),
                actions: vec![ActionRecord {
                    action_key: "jump".to_string(),
                    fields: Metadata::from([("strength", FieldValue::Integer(1))]),
                }],
                legality_hint: Some(true),
                metadata: Metadata::from([(
                    "source",
                    FieldValue::Text("manual".to_string()),
                )]),
            },
            max_steps,
        }
    }

    fn artifact(request: &RolloutRequest) -> RolloutArtifact {
        RolloutArtifact {
            branch_id: request.branch.id.clone(),
            steps: vec![RolloutStep {
                step_index: 0,
                action: None,
                state: None,
            }],
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
    fn request_digest_is_repeatable_and_domain_separated() {
        let request = request(8);
        let first = rollout_request_digest_v1(&request).expect("request digest");
        let repeated = rollout_request_digest_v1(&request).expect("request digest");

        assert_eq!(first, repeated);
        assert_eq!(first.len(), 64);
        assert_eq!(
            hash_serializable(&("different-domain", &request))
                .expect("comparison digest"),
            hash_serializable(&("different-domain", &request)).expect("comparison digest")
        );
        assert_ne!(
            first,
            hash_serializable(&("different-domain", &request)).expect("comparison digest")
        );
    }

    #[test]
    fn digest_changes_when_request_content_drifts_under_same_branch_id() {
        let baseline = request(8);
        let baseline_digest = rollout_request_digest_v1(&baseline).expect("baseline digest");

        let mut changed_action = baseline.clone();
        changed_action.branch.actions[0].action_key = "boost".to_string();
        assert_eq!(changed_action.branch.id, baseline.branch.id);
        assert_ne!(
            rollout_request_digest_v1(&changed_action).expect("changed action digest"),
            baseline_digest
        );

        let mut changed_metadata = baseline.clone();
        changed_metadata.branch.metadata.insert(
            "source",
            FieldValue::Text("counterfactual".to_string()),
        );
        assert_eq!(changed_metadata.branch.id, baseline.branch.id);
        assert_ne!(
            rollout_request_digest_v1(&changed_metadata).expect("changed metadata digest"),
            baseline_digest
        );

        let mut changed_bound = baseline.clone();
        changed_bound.max_steps = 9;
        assert_ne!(
            rollout_request_digest_v1(&changed_bound).expect("changed bound digest"),
            baseline_digest
        );
    }

    #[test]
    fn bound_artifact_verifies_against_exact_request_content() {
        let request = request(8);
        let bound = bind_rollout_artifact_v1(&request, artifact(&request))
            .expect("artifact should bind to request");

        verify_bound_rollout_artifact_v1(&request, &bound)
            .expect("exact request should verify bound artifact");
    }

    #[test]
    fn bound_artifact_rejects_stale_request_content_with_same_branch_id() {
        let request = request(8);
        let bound = bind_rollout_artifact_v1(&request, artifact(&request))
            .expect("artifact should bind to request");

        let mut drifted = request.clone();
        drifted.branch.actions[0].action_key = "boost".to_string();
        assert_eq!(drifted.branch.id, request.branch.id);

        let error = verify_bound_rollout_artifact_v1(&drifted, &bound)
            .expect_err("same BranchId with changed content must fail closed");
        assert!(error.to_string().contains("request digest mismatch"));
    }

    #[test]
    fn bound_artifact_rejects_tampered_digest_and_invalid_artifact_bounds() {
        let request = request(4);
        let mut bound = bind_rollout_artifact_v1(&request, artifact(&request))
            .expect("artifact should bind to request");

        bound.request_digest = "0".repeat(64);
        assert!(verify_bound_rollout_artifact_v1(&request, &bound).is_err());

        let out_of_range = RolloutArtifact {
            branch_id: request.branch.id.clone(),
            steps: vec![RolloutStep {
                step_index: 4,
                action: None,
                state: None,
            }],
        };
        assert!(bind_rollout_artifact_v1(&request, out_of_range).is_err());

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
        assert!(bind_rollout_artifact_v1(&request, duplicate).is_err());
    }

    #[test]
    fn bound_wrapper_rejects_unknown_json_fields() {
        let request = request(8);
        let bound = bind_rollout_artifact_v1(&request, artifact(&request))
            .expect("artifact should bind to request");
        let mut value = serde_json::to_value(&bound).expect("bound artifact should serialize");
        value
            .as_object_mut()
            .expect("wrapper should serialize as an object")
            .insert("unexpected".to_string(), serde_json::json!(true));

        assert!(serde_json::from_value::<BoundRolloutArtifactV1>(value).is_err());
    }
}
