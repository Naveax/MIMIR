use mimir_score::{Scorer, WeightedSumScorer};
use mimir_types::BranchId;
use std::collections::BTreeMap;

#[test]
fn unweighted_signals_are_retained_as_zero_components() {
    let scorer = WeightedSumScorer::new(BTreeMap::from([("known".to_string(), 2.0)]));
    let signals = BTreeMap::from([
        ("known".to_string(), 3.0),
        ("unknown".to_string(), 9.0),
    ]);

    let score = scorer.score(Some(BranchId::new("foundation-branch")), &signals);

    assert_eq!(score.total, 6.0);
    assert_eq!(score.components["known"], 6.0);
    assert_eq!(score.components["unknown"], 0.0);
    assert_eq!(
        score.components.keys().map(String::as_str).collect::<Vec<_>>(),
        vec!["known", "unknown"]
    );
}

#[test]
fn weights_without_matching_signals_do_not_create_components() {
    let scorer = WeightedSumScorer::new(BTreeMap::from([
        ("coverage".to_string(), 1.0),
        ("stability".to_string(), 0.5),
    ]));
    let signals = BTreeMap::from([("coverage".to_string(), 4.0)]);

    let score = scorer.score(None, &signals);

    assert_eq!(score.total, 4.0);
    assert_eq!(score.components.len(), 1);
    assert_eq!(score.components["coverage"], 4.0);
    assert!(!score.components.contains_key("stability"));
}

#[test]
fn empty_signal_set_preserves_branch_identity_and_zero_total() {
    let scorer = WeightedSumScorer::new(BTreeMap::from([("coverage".to_string(), 1.0)]));
    let branch_id = BranchId::new("foundation-branch");

    let score = scorer.score(Some(branch_id.clone()), &BTreeMap::new());

    assert_eq!(score.branch_id, Some(branch_id));
    assert!(score.components.is_empty());
    assert_eq!(score.total, 0.0);
}

#[test]
fn component_iteration_is_lexical_under_the_current_btreemap_implementation() {
    let scorer = WeightedSumScorer::new(BTreeMap::from([
        ("zeta".to_string(), 1.0),
        ("alpha".to_string(), 1.0),
        ("middle".to_string(), 1.0),
    ]));
    let signals = BTreeMap::from([
        ("zeta".to_string(), 1.0),
        ("alpha".to_string(), 2.0),
        ("middle".to_string(), 3.0),
    ]);

    let score = scorer.score(None, &signals);
    let keys = score
        .components
        .keys()
        .map(String::as_str)
        .collect::<Vec<_>>();

    assert_eq!(keys, vec!["alpha", "middle", "zeta"]);
}
