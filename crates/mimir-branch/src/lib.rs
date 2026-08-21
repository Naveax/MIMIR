use mimir_core::{MimirError, NamedComponent, Result};
use mimir_types::{
    ActionRecord, AnchorRecord, ArtifactHeader, ArtifactKind, BranchId, BranchOrigin, BranchRecord,
    Metadata, PersistedBranchArtifact,
};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

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

/// Additive validation surface for materialized branch batches.
///
/// It deliberately preserves the historical `anchor:branch:index` generator identity contract.
/// Consumers that reload or compose batches can opt into parent/identity validation without
/// changing proposal filtering, ordering, labels, actions, scores, or generated IDs.
pub trait BranchBatchVerifier {
    fn verify_batch(&self, anchor: &AnchorRecord, branches: &[BranchRecord]) -> Result<()>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct StrictBranchIdentityVerifier;

impl BranchBatchVerifier for StrictBranchIdentityVerifier {
    fn verify_batch(&self, anchor: &AnchorRecord, branches: &[BranchRecord]) -> Result<()> {
        let mut ids = BTreeSet::new();
        for branch in branches {
            if branch.anchor_id != anchor.id {
                return Err(MimirError::message(format!(
                    "branch parent mismatch for {}: expected {}, got {}",
                    branch.id, anchor.id, branch.anchor_id
                )));
            }
            if !ids.insert(branch.id.clone()) {
                return Err(MimirError::message(format!(
                    "duplicate branch id in batch: {}",
                    branch.id
                )));
            }
        }
        Ok(())
    }
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

    fn anchor() -> AnchorRecord {
        AnchorRecord {
            id: AnchorId::new("anchor-1"),
            replay_id: ReplayId::new("replay-1"),
            frame_index: FrameIndex::new(10),
            kind: AnchorKind::Manual,
            metadata: Metadata::new(),
        }
    }

    #[test]
    fn generator_respects_bound_and_legal_hint_filter() {
        let anchor = anchor();

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
        let anchor = anchor();
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

    #[test]
    fn branch_batch_verifier_accepts_generated_batch_without_rewriting_ids() {
        let anchor = anchor();
        let request = BranchGenerationRequest {
            anchor: anchor.clone(),
            proposals: vec![
                BranchProposal {
                    label: "first".to_string(),
                    actions: Vec::new(),
                    legal_hint: Some(true),
                    metadata: Metadata::new(),
                },
                BranchProposal {
                    label: "second".to_string(),
                    actions: Vec::new(),
                    legal_hint: None,
                    metadata: Metadata::new(),
                },
            ],
            max_branches: 2,
        };
        let branches = BoundedManualBranchGenerator::default()
            .generate(&request)
            .expect("generated branches");

        StrictBranchIdentityVerifier
            .verify_batch(&anchor, &branches)
            .expect("generated batch should verify");
        assert_eq!(branches[0].id.as_str(), "anchor-1:branch:0");
        assert_eq!(branches[1].id.as_str(), "anchor-1:branch:1");
    }

    #[test]
    fn branch_batch_verifier_rejects_parent_drift_and_duplicate_ids() {
        let anchor = anchor();
        let valid = BranchRecord {
            id: BranchId::new("branch-a"),
            anchor_id: anchor.id.clone(),
            origin: BranchOrigin::Imported,
            label: None,
            actions: Vec::new(),
            legality_hint: None,
            metadata: Metadata::new(),
        };

        let mut wrong_parent = valid.clone();
        wrong_parent.anchor_id = AnchorId::new("other-anchor");
        assert!(
            StrictBranchIdentityVerifier
                .verify_batch(&anchor, &[wrong_parent])
                .is_err()
        );

        assert!(
            StrictBranchIdentityVerifier
                .verify_batch(&anchor, &[valid.clone(), valid])
                .is_err()
        );
    }
}
