use mimir_anchor::{AnchorDetector, AnchorHint, HintAnchorDetector};
use mimir_types::{AnchorId, AnchorKind, FieldValue, FrameIndex, Metadata, ReplayId};

fn hint(anchor_id: Option<&str>, frame: u32, metadata: Metadata) -> AnchorHint {
    AnchorHint {
        anchor_id: anchor_id.map(AnchorId::new),
        frame_index: FrameIndex::new(frame),
        kind: AnchorKind::Manual,
        metadata,
    }
}

#[test]
fn mixed_explicit_and_generated_anchor_ids_preserve_hint_positions() {
    let replay_id = ReplayId::new("foundation-replay");
    let hints = vec![
        hint(None, 10, Metadata::new()),
        hint(Some("explicit-anchor"), 20, Metadata::new()),
        hint(None, 30, Metadata::new()),
    ];

    let anchors = HintAnchorDetector
        .detect(&replay_id, &hints)
        .expect("hint detection should succeed");

    let ids = anchors
        .iter()
        .map(|anchor| anchor.id.as_str())
        .collect::<Vec<_>>();
    assert_eq!(
        ids,
        vec![
            "foundation-replay:anchor:0",
            "explicit-anchor",
            "foundation-replay:anchor:2",
        ]
    );
    assert_eq!(anchors[0].frame_index, FrameIndex::new(10));
    assert_eq!(anchors[1].frame_index, FrameIndex::new(20));
    assert_eq!(anchors[2].frame_index, FrameIndex::new(30));
}

#[test]
fn detector_copies_metadata_without_mutating_the_hint() {
    let replay_id = ReplayId::new("foundation-replay");
    let metadata = Metadata::from([
        ("source", FieldValue::Text("foundation".to_string())),
        ("confidence", FieldValue::Integer(7)),
    ]);
    let hints = vec![hint(None, 42, metadata.clone())];

    let anchors = HintAnchorDetector
        .detect(&replay_id, &hints)
        .expect("hint detection should succeed");

    assert_eq!(anchors[0].metadata, metadata);
    assert_eq!(hints[0].metadata, metadata);
}

#[test]
fn empty_hint_set_produces_no_records_or_persisted_artifacts() {
    let replay_id = ReplayId::new("foundation-replay");

    let records = HintAnchorDetector
        .detect(&replay_id, &[])
        .expect("empty detection should succeed");
    let artifacts = HintAnchorDetector
        .detect_persisted(&replay_id, &[])
        .expect("empty persisted detection should succeed");

    assert!(records.is_empty());
    assert!(artifacts.is_empty());
}
