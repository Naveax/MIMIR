use mimir_core::{MimirError, NamedComponent, Result};
use mimir_types::{TeacherLabelId, TeacherLabelRecord};
use serde::{Deserialize, Serialize};

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
/// This does not turn the pass-through scaffold into a learned teacher. It only gives callers a
/// narrow way to reject identity/value corruption before persisting or reusing explicit labels.
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

        let mut seen_ids: Vec<TeacherLabelId> = Vec::with_capacity(request.labels.len());
        for label in &request.labels {
            if seen_ids.iter().any(|id| id == &label.id) {
                return Err(MimirError::message(format!(
                    "duplicate teacher label id in request: {}",
                    label.id
                )));
            }
            seen_ids.push(label.id.clone());

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
    use mimir_types::{Metadata, TeacherLabelTarget};

    fn label(id: &str, score: Option<f32>) -> TeacherLabelRecord {
        TeacherLabelRecord {
            id: TeacherLabelId::new(id),
            target: TeacherLabelTarget::Replay(mimir_types::ReplayId::new("replay-1")),
            label: "interesting".to_string(),
            score,
            metadata: Metadata::new(),
        }
    }

    #[test]
    fn pass_through_synthesizer_preserves_explicit_labels() {
        let request = TeacherSynthesisRequest {
            namespace: "teacher".to_string(),
            labels: vec![label("label-1", Some(1.0))],
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
                labels: vec![label("label-1", Some(0.5)), label("label-2", None)],
            })
            .expect("unique finite labels should verify");
    }

    #[test]
    fn strict_verifier_rejects_blank_namespace_duplicate_ids_and_non_finite_scores() {
        assert!(
            StrictTeacherRequestVerifier
                .verify_request(&TeacherSynthesisRequest {
                    namespace: "   ".to_string(),
                    labels: Vec::new(),
                })
                .is_err()
        );

        assert!(
            StrictTeacherRequestVerifier
                .verify_request(&TeacherSynthesisRequest {
                    namespace: "teacher".to_string(),
                    labels: vec![label("label-1", Some(1.0)), label("label-1", Some(0.0))],
                })
                .is_err()
        );

        assert!(
            StrictTeacherRequestVerifier
                .verify_request(&TeacherSynthesisRequest {
                    namespace: "teacher".to_string(),
                    labels: vec![label("label-1", Some(f32::NAN))],
                })
                .is_err()
        );
    }
}
