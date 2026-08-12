use mimir_core::{NamedComponent, Result};
use mimir_types::{
    ActionRecord, AnchorRecord, ArtifactHeader, ArtifactKind, BranchId, BranchOrigin, BranchRecord,
    Metadata, PersistedBranchArtifact,
};
use serde::{Deserialize, Serialize};

pub const BRANCH_ARTIFACT_PRODUCER: &str = "mimir-branch";

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct BranchProposal {
    pub label: String,
    pub actions: Vec<ActionRecord>,
    pub legal_hint: Option<bool>,
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct BranchGenerationRequest {
    pub anchor: AnchorRecord,
    pub proposals: Vec<BranchProposal>,
    pub max_branches: usize,
}

pub trait LegalityFilter {
    fn allow(&self, proposal: &BranchProposal) -> bool;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct LegalHintFilter;

impl LegalityFilter for LegalHintFilter {
    fn allow(&self, proposal: &BranchProposal) -> bool {
        proposal.legal_hint != Some(false)
    }
}

pub trait BranchGenerator {
    fn generate(&self, request: &BranchGenerationRequest) -> Result<Vec<BranchRecord>>;
}

#[derive(Debug, Clone)]
pub struct BoundedManualBranchGenerator<F = LegalHintFilter> {
    filter: F,
}

impl Default for BoundedManualBranchGenerator<LegalHintFilter> {
    fn default() -> Self {
        Self {
            filter: LegalHintFilter,
        }
    }
}

impl<F> BoundedManualBranchGenerator<F> {
    pub fn new(filter: F) -> Self {
        Self { filter }
    }
}

impl<F> NamedComponent for BoundedManualBranchGenerator<F> {
    fn component_name(&self) -> &'static str {
        "bounded-manual-branch-generator"
    }
}

impl<F> BranchGenerator for BoundedManualBranchGenerator<F>
where
    F: LegalityFilter,
{
    fn generate(&self, request: &BranchGenerationRequest) -> Result<Vec<BranchRecord>> {
        Ok(request
            .proposals
            .iter()
            .filter(|proposal| self.filter.allow(proposal))
            .take(request.max_branches)
            .enumerate()
            .map(|(index, proposal)| BranchRecord {
                id: BranchId::new(format!("{}:branch:{index}", request.anchor.id)),
                anchor_id: request.anchor.id.clone(),
                origin: BranchOrigin::Manual,
                label: Some(proposal.label.clone()),
                actions: proposal.actions.clone(),
                legality_hint: proposal.legal_hint,
                metadata: proposal.metadata.clone(),
            })
            .collect())
    }
}

impl<F> BoundedManualBranchGenerator<F>
where
    F: LegalityFilter,
{
    pub fn generate_persisted(
        &self,
        request: &BranchGenerationRequest,
    ) -> Result<Vec<PersistedBranchArtifact>> {
        self.generate(request).map(|branches| {
            branches
                .into_iter()
                .map(|branch| {
                    PersistedBranchArtifact::new(
                        ArtifactHeader::for_kind(ArtifactKind::Branch, BRANCH_ARTIFACT_PRODUCER)
                            .with_created_by_component(self.component_name()),
                        branch,
                    )
                })
                .collect()
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_types::{
        AnchorId, AnchorKind, ArtifactHeader, ArtifactKind, FieldValue, FrameIndex, ReplayId,
    };

    #[test]
    fn generator_respects_bound_and_legal_hint_filter() {
        let anchor = AnchorRecord {
            id: AnchorId::new("anchor-1"),
            replay_id: ReplayId::new("replay-1"),
            frame_index: FrameIndex::new(10),
            kind: AnchorKind::Manual,
            metadata: Metadata::new(),
        };

        let proposals = vec![
            BranchProposal {
                label: "keep".to_string(),
                actions: Vec::new(),
                legal_hint: Some(true),
                metadata: Metadata::new(),
            },
            BranchProposal {
                label: "drop".to_string(),
                actions: Vec::new(),
                legal_hint: Some(false),
                metadata: Metadata::new(),
            },
            BranchProposal {
                label: "keep-two".to_string(),
                actions: Vec::new(),
                legal_hint: None,
                metadata: {
                    let mut metadata = Metadata::new();
                    metadata.insert("note".to_string(), FieldValue::Text("manual".to_string()));
                    metadata
                },
            },
        ];

        let request = BranchGenerationRequest {
            anchor,
            proposals,
            max_branches: 2,
        };

        let branches = BoundedManualBranchGenerator::default()
            .generate(&request)
            .expect("manual proposals should convert into branches");

        assert_eq!(branches.len(), 2);
        assert_eq!(branches[0].label.as_deref(), Some("keep"));
        assert_eq!(branches[1].label.as_deref(), Some("keep-two"));
    }

    #[test]
    fn generator_emits_persisted_branch_artifacts() {
        let anchor = AnchorRecord {
            id: AnchorId::new("anchor-1"),
            replay_id: ReplayId::new("replay-1"),
            frame_index: FrameIndex::new(10),
            kind: AnchorKind::Manual,
            metadata: Metadata::new(),
        };
        let actions = vec![ActionRecord {
            action_key: "jump".to_string(),
            fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
        }];
        let metadata = Metadata::from([("source", FieldValue::Text("manual".to_string()))]);
        let request = BranchGenerationRequest {
            anchor: anchor.clone(),
            proposals: vec![BranchProposal {
                label: "keep".to_string(),
                actions: actions.clone(),
                legal_hint: Some(true),
                metadata: metadata.clone(),
            }],
            max_branches: 1,
        };

        let generator = BoundedManualBranchGenerator::default();
        let artifacts = generator
            .generate_persisted(&request)
            .expect("manual proposals should convert into persisted artifacts");

        assert_eq!(artifacts.len(), 1);
        assert_eq!(
            artifacts[0].header,
            ArtifactHeader::for_kind(ArtifactKind::Branch, BRANCH_ARTIFACT_PRODUCER)
                .with_created_by_component(generator.component_name())
        );
        assert_eq!(
            artifacts[0].payload,
            BranchRecord {
                id: BranchId::new("anchor-1:branch:0"),
                anchor_id: anchor.id,
                origin: BranchOrigin::Manual,
                label: Some("keep".to_string()),
                actions,
                legality_hint: Some(true),
                metadata,
            }
        );
    }
}
