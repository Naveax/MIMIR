use mimir_branch::{
    BoundedManualBranchGenerator, BranchGenerationRequest, BranchGenerator, BranchProposal,
};
use mimir_types::{
    ActionRecord, AnchorId, AnchorKind, AnchorRecord, FieldValue, FrameIndex, Metadata, ReplayId,
};

fn anchor() -> AnchorRecord {
    AnchorRecord {
        id: AnchorId::new("foundation-anchor"),
        replay_id: ReplayId::new("foundation-replay"),
        frame_index: FrameIndex::new(9),
        kind: AnchorKind::Manual,
        metadata: Metadata::new(),
    }
}

fn proposal(label: &str, legal_hint: Option<bool>) -> BranchProposal {
    BranchProposal {
        label: label.to_string(),
        actions: Vec::new(),
        legal_hint,
        metadata: Metadata::new(),
    }
}

#[test]
fn rejected_proposals_are_filtered_before_dense_branch_id_enumeration() {
    let request = BranchGenerationRequest {
        anchor: anchor(),
        proposals: vec![
            proposal("reject-first", Some(false)),
            proposal("accept-true", Some(true)),
            proposal("accept-unspecified", None),
        ],
        max_branches: 2,
    };

    let branches = BoundedManualBranchGenerator::default()
        .generate(&request)
        .expect("branch generation should succeed");

    assert_eq!(branches.len(), 2);
    assert_eq!(branches[0].id.as_str(), "foundation-anchor:branch:0");
    assert_eq!(branches[1].id.as_str(), "foundation-anchor:branch:1");
    assert_eq!(branches[0].label.as_deref(), Some("accept-true"));
    assert_eq!(branches[1].label.as_deref(), Some("accept-unspecified"));
}

#[test]
fn zero_branch_budget_returns_no_branches_even_for_legal_proposals() {
    let request = BranchGenerationRequest {
        anchor: anchor(),
        proposals: vec![proposal("candidate", Some(true))],
        max_branches: 0,
    };

    let branches = BoundedManualBranchGenerator::default()
        .generate(&request)
        .expect("zero-budget generation should succeed");

    assert!(branches.is_empty());
}

#[test]
fn accepted_proposal_payload_is_copied_exactly() {
    let actions = vec![ActionRecord {
        action_key: "jump".to_string(),
        fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
    }];
    let metadata = Metadata::from([
        ("source", FieldValue::Text("foundation".to_string())),
        ("ordinal", FieldValue::Integer(3)),
    ]);
    let request = BranchGenerationRequest {
        anchor: anchor(),
        proposals: vec![BranchProposal {
            label: "candidate".to_string(),
            actions: actions.clone(),
            legal_hint: None,
            metadata: metadata.clone(),
        }],
        max_branches: 1,
    };

    let branches = BoundedManualBranchGenerator::default()
        .generate(&request)
        .expect("branch generation should succeed");

    assert_eq!(branches.len(), 1);
    assert_eq!(branches[0].actions, actions);
    assert_eq!(branches[0].legality_hint, None);
    assert_eq!(branches[0].metadata, metadata);
    assert_eq!(request.proposals[0].actions, actions);
    assert_eq!(request.proposals[0].metadata, metadata);
}
