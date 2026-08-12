use mimir_core::{NamedComponent, Result};
use mimir_types::TeacherLabelRecord;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct TeacherSynthesisRequest {
    pub namespace: String,
    pub labels: Vec<TeacherLabelRecord>,
}

pub trait TeacherSynthesizer {
    fn synthesize(&self, request: &TeacherSynthesisRequest) -> Result<Vec<TeacherLabelRecord>>;
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
    use mimir_types::{Metadata, TeacherLabelId, TeacherLabelTarget};

    #[test]
    fn pass_through_synthesizer_preserves_explicit_labels() {
        let request = TeacherSynthesisRequest {
            namespace: "teacher".to_string(),
            labels: vec![mimir_types::TeacherLabelRecord {
                id: TeacherLabelId::new("label-1"),
                target: TeacherLabelTarget::Replay(mimir_types::ReplayId::new("replay-1")),
                label: "interesting".to_string(),
                score: Some(1.0),
                metadata: Metadata::new(),
            }],
        };

        let labels = PassThroughTeacherSynthesizer
            .synthesize(&request)
            .expect("labels should pass through");

        assert_eq!(labels, request.labels);
    }
}
