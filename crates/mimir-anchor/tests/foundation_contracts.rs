use mimir_anchor::{AnchorDetector, AnchorHint, HintAnchorDetector, summarize_request};
use mimir_types::{AnchorId, AnchorKind, FieldValue, FrameIndex, Metadata, ReplayId};

fn fixture_hints() -> Vec<AnchorHint> {
    vec![
        AnchorHint {
            anchor_id: Some(AnchorId::new("anchor-explicit")),
            frame_index: FrameIndex::new(12),
            kind: AnchorKind::Manual,
            metadata: Metadata::from([(
                "source",
                FieldValue::Text("explicit-fixture".to_string()),
            )]),
        },
        AnchorHint {
            anchor_id: None,
            frame_index: FrameIndex::new(24),
            kind: AnchorKind::Manual,
            metadata: Metadata::from([("stable", FieldValue::Boolean(true))]),
        },
    ]
}

#[test]
fn hint_detection_is_repeatable_and_preserves_explicit_identity_and_metadata() {
    let replay_id = ReplayId::new("replay-foundation");
    let hints = fixture_hints();

    let first = HintAnchorDetector
        .detect(&replay_id, &hints)
        .expect("first detection should succeed");
    let second = HintAnchorDetector
        .detect(&replay_id, &hints)
        .expect("repeated detection should succeed");

    assert_eq!(first, second);
    assert_eq!(first.len(), 2);
    assert_eq!(first[0].id.as_str(), "anchor-explicit");
    assert_eq!(first[0].replay_id, replay_id);
    assert_eq!(first[0].frame_index, FrameIndex::new(12));
    assert_eq!(first[0].metadata, hints[0].metadata);

    assert_eq!(first[1].id.as_str(), "replay-foundation:anchor:1");
    assert_eq!(first[1].frame_index, FrameIndex::new(24));
    assert_eq!(first[1].metadata, hints[1].metadata);
    assert_ne!(first[0].id, first[1].id);
}

#[test]
fn empty_hint_lane_is_empty_and_request_summary_tracks_exact_count() {
    let replay_id = ReplayId::new("replay-empty");
    let hints = Vec::<AnchorHint>::new();

    let anchors = HintAnchorDetector
        .detect(&replay_id, &hints)
        .expect("empty detection should succeed");
    let summary = summarize_request(replay_id.clone(), &hints);

    assert!(anchors.is_empty());
    assert_eq!(summary.replay_id, replay_id);
    assert_eq!(summary.hint_count, 0);
}
