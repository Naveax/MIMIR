use mimir_teacher::{PassThroughTeacherSynthesizer, TeacherSynthesisRequest, TeacherSynthesizer};
use mimir_types::{Metadata, ReplayId, TeacherLabelId, TeacherLabelRecord, TeacherLabelTarget};

fn label(id: &str, replay: &str, text: &str, score: f32) -> TeacherLabelRecord {
    TeacherLabelRecord {
        id: TeacherLabelId::new(id),
        target: TeacherLabelTarget::Replay(ReplayId::new(replay)),
        label: text.to_string(),
        score: Some(score),
        metadata: Metadata::new(),
    }
}

#[test]
fn pass_through_preserves_order_and_complete_label_payloads() {
    let labels = vec![
        label("label-b", "replay-2", "second", 0.25),
        label("label-a", "replay-1", "first", 0.75),
    ];
    let request = TeacherSynthesisRequest {
        namespace: "foundation.teacher".to_string(),
        labels: labels.clone(),
    };

    let synthesized = PassThroughTeacherSynthesizer
        .synthesize(&request)
        .expect("pass-through synthesis should succeed");

    assert_eq!(synthesized, labels);
    assert_eq!(request.labels, labels);
}

#[test]
fn namespace_is_an_envelope_field_and_does_not_mutate_passed_labels() {
    let labels = vec![label("label-1", "replay-1", "candidate", 1.0)];
    let first = PassThroughTeacherSynthesizer
        .synthesize(&TeacherSynthesisRequest {
            namespace: "teacher.alpha".to_string(),
            labels: labels.clone(),
        })
        .expect("first namespace should synthesize");
    let second = PassThroughTeacherSynthesizer
        .synthesize(&TeacherSynthesisRequest {
            namespace: "teacher.beta".to_string(),
            labels: labels.clone(),
        })
        .expect("second namespace should synthesize");

    assert_eq!(first, labels);
    assert_eq!(second, labels);
    assert_eq!(first, second);
}

#[test]
fn empty_label_set_remains_empty() {
    let synthesized = PassThroughTeacherSynthesizer
        .synthesize(&TeacherSynthesisRequest {
            namespace: "teacher.empty".to_string(),
            labels: Vec::new(),
        })
        .expect("empty pass-through synthesis should succeed");

    assert!(synthesized.is_empty());
}
