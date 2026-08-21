use mimir_core::{MimirError, NamedComponent, Result};
use mimir_types::{TeacherLabelId, TeacherLabelRecord, TeacherLabelTarget};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct TeacherSynthesisRequest {
    pub namespace: String,
    pub labels: Vec<TeacherLabelRecord>,
}

pub trait TeacherSynthesizer {
    fn synthesize(&self, request: &TeacherSynthesisRequest) -> Result<Vec<TeacherLabelRecord>>;
}

/// Additive fail-closed validation for explicit teacher synthesis requests.
///
/// This does not turn the pass-through scaffold into a learned teacher. It rejects malformed
/// explicit identity/text/value boundaries before callers persist or reuse them.
pub trait TeacherSynthesisRequestVerifier {
    fn verify_request(&self, request: &TeacherSynthesisRequest) -> Result<()>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct StrictTeacherRequestVerifier;

impl TeacherSynthesisRequestVerifier for StrictTeacherRequestVerifier {
    fn verify_request(&self, request: &TeacherSynthesisRequest) -> Result<()> {
        if request.namespace.trim().is_empty() {
            return Err(MimirError::message(
                "teacher synthesis namespace must not be blank",
            ));
        }

        let mut seen_ids = BTreeSet::<TeacherLabelId>::new();
        for label in &request.labels {
            if label.id.as_str().trim().is_empty() {
                return Err(MimirError::message("teacher label id must not be blank"));
            }
            if !seen_ids.insert(label.id.clone()) {
                return Err(MimirError::message(format!(
                    "duplicate teacher label id in request: {}",
                    label.id
                )));
            }
            if label.label.trim().is_empty() {
                return Err(MimirError::message(format!(
                    "teacher label text must not be blank for {}",
                    label.id
                )));
            }
            if target_id(&label.target).trim().is_empty() {
                return Err(MimirError::message(format!(
                    "teacher label target id must not be blank for {}",
                    label.id
                )));
            }
            if label.score.is_some_and(|score| !score.is_finite()) {
                return Err(MimirError::message(format!(
                    "non-finite teacher label score for {}",
                    label.id
                )));
            }
        }

        Ok(())
    }
}

fn target_id(target: &TeacherLabelTarget) -> &str {
    match target {
        TeacherLabelTarget::Replay(id) => id.as_str(),
        TeacherLabelTarget::Anchor(id) => id.as_str(),
        TeacherLabelTarget::Branch(id) => id.as_str(),
        TeacherLabelTarget::Skill(id) => id.as_str(),
    }
}

#[derive(Debug, Default, Clone, Copy)]
pub struct PassThroughTeacherSynthesizer;

impl NamedComponent for PassThroughTeacherSynthesizer {
    fn component_name(&self) -> &'static str {
        "pass-through-teacher-synthesizer"
    }
}

impl TeacherSynthesizer for PassThroughTeacherSynthesizer {
    fn synthesize(&self, request: &TeacherSynthesisRequest) -> Result<Vec<TeacherLabelRecord>> {
        Ok(request.labels.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_types::{AnchorId, BranchId, Metadata, ReplayId, SkillId};

    fn label(
        id: &str,
        target: TeacherLabelTarget,
        text: &str,
        score: Option<f32>,
    ) -> TeacherLabelRecord {
        TeacherLabelRecord {
            id: TeacherLabelId::new(id),
            target,
            label: text.to_string(),
            score,
            metadata: Metadata::new(),
        }
    }

    fn replay_label(id: &str, score: Option<f32>) -> TeacherLabelRecord {
        label(
            id,
            TeacherLabelTarget::Replay(ReplayId::new("replay-1")),
            "interesting",
            score,
        )
    }

    #[test]
    fn pass_through_synthesizer_preserves_explicit_labels() {
        let request = TeacherSynthesisRequest {
            namespace: "teacher".to_string(),
            labels: vec![replay_label("label-1", Some(1.0))],
        };

        let labels = PassThroughTeacherSynthesizer
            .synthesize(&request)
            .expect("labels should pass through");

        assert_eq!(labels, request.labels);
    }

    #[test]
    fn strict_verifier_accepts_empty_or_unique_finite_label_sets() {
        StrictTeacherRequestVerifier
            .verify_request(&TeacherSynthesisRequest {
                namespace: "teacher".to_string(),
                labels: Vec::new(),
            })
            .expect("empty explicit set remains valid");

        StrictTeacherRequestVerifier
            .verify_request(&TeacherSynthesisRequest {
                namespace: "teacher".to_string(),
                labels: vec![
                    replay_label("label-1", Some(0.5)),
                    replay_label("label-2", None),
                ],
            })
            .expect("unique finite labels should verify");
    }

    #[test]
    fn strict_verifier_rejects_blank_namespace_ids_text_and_non_finite_scores() {
        let verifier = StrictTeacherRequestVerifier;

        assert!(
            verifier
                .verify_request(&TeacherSynthesisRequest {
                    namespace: "   ".to_string(),
                    labels: Vec::new(),
                })
                .is_err()
        );
        assert!(
            verifier
                .verify_request(&TeacherSynthesisRequest {
                    namespace: "teacher".to_string(),
                    labels: vec![replay_label("   ", Some(1.0))],
                })
                .is_err()
        );
        assert!(
            verifier
                .verify_request(&TeacherSynthesisRequest {
                    namespace: "teacher".to_string(),
                    labels: vec![label(
                        "label-1",
                        TeacherLabelTarget::Replay(ReplayId::new("replay-1")),
                        "   ",
                        Some(1.0),
                    )],
                })
                .is_err()
        );
        assert!(
            verifier
                .verify_request(&TeacherSynthesisRequest {
                    namespace: "teacher".to_string(),
                    labels: vec![replay_label("label-1", Some(f32::NAN))],
                })
                .is_err()
        );
    }

    #[test]
    fn strict_verifier_rejects_duplicate_label_ids() {
        assert!(
            StrictTeacherRequestVerifier
                .verify_request(&TeacherSynthesisRequest {
                    namespace: "teacher".to_string(),
                    labels: vec![
                        replay_label("label-1", Some(1.0)),
                        replay_label("label-1", None),
                    ],
                })
                .is_err()
        );
    }

    #[test]
    fn strict_verifier_rejects_blank_ids_for_every_target_variant() {
        let targets = [
            TeacherLabelTarget::Replay(ReplayId::new("   ")),
            TeacherLabelTarget::Anchor(AnchorId::new("   ")),
            TeacherLabelTarget::Branch(BranchId::new("   ")),
            TeacherLabelTarget::Skill(SkillId::new("   ")),
        ];

        for (index, target) in targets.into_iter().enumerate() {
            let request = TeacherSynthesisRequest {
                namespace: "teacher".to_string(),
                labels: vec![label(
                    &format!("label-{index}"),
                    target,
                    "interesting",
                    Some(1.0),
                )],
            };
            assert!(
                StrictTeacherRequestVerifier
                    .verify_request(&request)
                    .is_err(),
                "target variant {index} should reject a blank id"
            );
        }
    }
}
