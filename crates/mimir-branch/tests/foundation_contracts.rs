use mimir_branch::{
    BoundedManualBranchGenerator, BranchGenerationRequest, BranchGenerator, BranchProposal,
};
use mimir_types::{AnchorId, AnchorKind, AnchorRecord, FieldValue, FrameIndex, Metadata, ReplayId};

fn anchor() -> AnchorRecord {
    AnchorRecord {
        id: AnchorId::new("anchor-foundation"),
        replay_id: ReplayId::new("replay-foundation"),
        frame_index: FrameIndex::new(10),
        kind: AnchorKind::Manual,
        metadata: Metadata::new(),
    }
}

fn proposal(label: &str, legal_hint: Option<bool>) -> BranchProposal {
    BranchProposal {
        label: label.to_string(),
        actions: Vec::new(),
        legal_hint,
        metadata: Metadata::from([("proposal", FieldValue::Text(label.to_string()))]),
    }
}

#[test]
fn generation_is_repeatable_and_filters_illegal_proposals_before_the_bound() {
    let request = BranchGenerationRequest {
        anchor: anchor(),
        proposals: vec![
            proposal("illegal-first", Some(false)),
            proposal("first-admitted", Some(true)),
            proposal("second-admitted", None),
        ],
        max_branches: 1,
    };
    let generator = BoundedManualBranchGenerator::default();

    let first = generator
        .generate(&request)
        .expect("first generation should succeed");
    let second = generator
        .generate(&request)
        .expect("repeated generation should succeed");

    assert_eq!(first, second);
    assert_eq!(first.len(), 1);
    assert_eq!(first[0].id.as_str(), "anchor-foundation:branch:0");
    assert_eq!(first[0].anchor_id, request.anchor.id);
    assert_eq!(first[0].label.as_deref(), Some("first-admitted"));
    assert_eq!(first[0].legality_hint, Some(true));
    assert_eq!(first[0].metadata, request.proposals[1].metadata);
}

#[test]
fn zero_branch_bound_is_an_explicit_empty_result() {
    let request = BranchGenerationRequest {
        anchor: anchor(),
        proposals: vec![proposal("admitted", Some(true))],
        max_branches: 0,
    };

    let branches = BoundedManualBranchGenerator::default()
        .generate(&request)
        .expect("zero bound should remain a valid empty generation");

    assert!(branches.is_empty());
}

#[test]
fn unknown_legality_hint_remains_admitted_by_the_current_filter_contract() {
    let request = BranchGenerationRequest {
        anchor: anchor(),
        proposals: vec![proposal("unknown", None)],
        max_branches: 1,
    };

    let branches = BoundedManualBranchGenerator::default()
        .generate(&request)
        .expect("unknown legality hint should remain admissible");

    assert_eq!(branches.len(), 1);
    assert_eq!(branches[0].label.as_deref(), Some("unknown"));
    assert_eq!(branches[0].legality_hint, None);
}
