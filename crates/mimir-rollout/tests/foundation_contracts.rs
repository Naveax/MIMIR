use mimir_rollout::{RolloutEngine, RolloutRequest, UnavailableRolloutEngine};
use mimir_types::{
    ActionRecord, AnchorId, BranchId, BranchOrigin, BranchRecord, FieldValue, Metadata,
};

fn request(max_steps: usize, actions: Vec<ActionRecord>) -> RolloutRequest {
    RolloutRequest {
        branch: BranchRecord {
            id: BranchId::new("foundation-branch"),
            anchor_id: AnchorId::new("foundation-anchor"),
            origin: BranchOrigin::Manual,
            label: Some("foundation".to_string()),
            actions,
            legality_hint: Some(true),
            metadata: Metadata::new(),
        },
        max_steps,
    }
}

fn unavailable_error(request: &RolloutRequest) -> String {
    UnavailableRolloutEngine
        .rollout(request)
        .expect_err("scaffold rollout engine must stay unavailable")
        .to_string()
}

#[test]
fn unavailable_engine_fails_closed_for_zero_and_nonzero_step_budgets() {
    let zero = unavailable_error(&request(0, Vec::new()));
    let bounded = unavailable_error(&request(128, Vec::new()));

    assert_eq!(zero, bounded);
    assert!(zero.contains("no rollout engine is bundled in this scaffold"));
}

#[test]
fn branch_actions_cannot_bypass_the_unavailable_rollout_boundary() {
    let action = ActionRecord {
        action_key: "boost".to_string(),
        fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
    };

    let empty_branch_error = unavailable_error(&request(16, Vec::new()));
    let action_branch_error = unavailable_error(&request(16, vec![action]));

    assert_eq!(action_branch_error, empty_branch_error);
}

#[test]
fn repeated_unavailable_calls_return_the_same_explicit_failure() {
    let request = request(8, Vec::new());

    let first = unavailable_error(&request);
    let second = unavailable_error(&request);

    assert_eq!(first, second);
}
