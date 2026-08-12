use mimir_core::{NamedComponent, Result};
use mimir_types::{
    AnchorId, AnchorKind, AnchorRecord, ArtifactHeader, ArtifactKind, FrameIndex, Metadata,
    PersistedAnchorArtifact, ReplayId,
};
use serde::{Deserialize, Serialize};

pub const ANCHOR_ARTIFACT_PRODUCER: &str = "mimir-anchor";

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct AnchorHint {
    pub anchor_id: Option<AnchorId>,
    pub frame_index: FrameIndex,
    pub kind: AnchorKind,
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct AnchorDetectionRequest {
    pub replay_id: ReplayId,
    pub hint_count: usize,
}

pub trait AnchorDetector {
    fn detect(&self, replay_id: &ReplayId, hints: &[AnchorHint]) -> Result<Vec<AnchorRecord>>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct HintAnchorDetector;

impl NamedComponent for HintAnchorDetector {
    fn component_name(&self) -> &'static str {
        "hint-anchor-detector"
    }
}

impl AnchorDetector for HintAnchorDetector {
    fn detect(&self, replay_id: &ReplayId, hints: &[AnchorHint]) -> Result<Vec<AnchorRecord>> {
        Ok(hints
            .iter()
            .enumerate()
            .map(|(index, hint)| AnchorRecord {
                id: hint
                    .anchor_id
                    .clone()
                    .unwrap_or_else(|| AnchorId::new(format!("{replay_id}:anchor:{index}"))),
                replay_id: replay_id.clone(),
                frame_index: hint.frame_index,
                kind: hint.kind.clone(),
                metadata: hint.metadata.clone(),
            })
            .collect())
    }
}

impl HintAnchorDetector {
    pub fn detect_persisted(
        &self,
        replay_id: &ReplayId,
        hints: &[AnchorHint],
    ) -> Result<Vec<PersistedAnchorArtifact>> {
        self.detect(replay_id, hints).map(|anchors| {
            anchors
                .into_iter()
                .map(|anchor| {
                    PersistedAnchorArtifact::new(
                        ArtifactHeader::for_kind(ArtifactKind::Anchor, ANCHOR_ARTIFACT_PRODUCER)
                            .with_created_by_component(self.component_name()),
                        anchor,
                    )
                })
                .collect()
        })
    }
}

pub fn summarize_request(replay_id: ReplayId, hints: &[AnchorHint]) -> AnchorDetectionRequest {
    AnchorDetectionRequest {
        replay_id,
        hint_count: hints.len(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_types::{ArtifactHeader, ArtifactKind, FieldValue};

    #[test]
    fn hint_detector_materializes_records_from_explicit_hints() {
        let replay_id = ReplayId::new("replay-1");
        let mut metadata = Metadata::new();
        metadata.insert("source".to_string(), FieldValue::Text("manual".to_string()));

        let hints = vec![AnchorHint {
            anchor_id: None,
            frame_index: FrameIndex::new(12),
            kind: AnchorKind::Manual,
            metadata,
        }];

        let anchors = HintAnchorDetector
            .detect(&replay_id, &hints)
            .expect("hints should convert into anchors");

        assert_eq!(anchors.len(), 1);
        assert_eq!(anchors[0].frame_index, FrameIndex::new(12));
        assert_eq!(anchors[0].id.as_str(), "replay-1:anchor:0");
    }

    #[test]
    fn hint_detector_emits_persisted_anchor_artifacts() {
        let replay_id = ReplayId::new("replay-1");
        let metadata = Metadata::from([("source", FieldValue::Text("manual".to_string()))]);
        let hints = vec![AnchorHint {
            anchor_id: Some(AnchorId::new("anchor-explicit")),
            frame_index: FrameIndex::new(24),
            kind: AnchorKind::Manual,
            metadata: metadata.clone(),
        }];

        let artifacts = HintAnchorDetector
            .detect_persisted(&replay_id, &hints)
            .expect("hints should convert into persisted artifacts");

        assert_eq!(artifacts.len(), 1);
        assert_eq!(
            artifacts[0].header,
            ArtifactHeader::for_kind(ArtifactKind::Anchor, ANCHOR_ARTIFACT_PRODUCER)
                .with_created_by_component(HintAnchorDetector.component_name())
        );
        assert_eq!(
            artifacts[0].payload,
            AnchorRecord {
                id: AnchorId::new("anchor-explicit"),
                replay_id,
                frame_index: FrameIndex::new(24),
                kind: AnchorKind::Manual,
                metadata,
            }
        );
    }
}
