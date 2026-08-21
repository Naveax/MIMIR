use mimir_core::NamedComponent;
use mimir_teacher::{PassThroughTeacherSynthesizer, TeacherSynthesisRequest, TeacherSynthesizer};
use mimir_types::{Metadata, ReplayId, TeacherLabelId, TeacherLabelRecord, TeacherLabelTarget};

fn label(id: &str, replay: &str, text: &str, score: Option<f64>) -> TeacherLabelRecord {
    TeacherLabelRecord {
        id: TeacherLabelId::new(id),
        target: TeacherLabelTarget::Replay(ReplayId::new(replay)),
        label: text.to_owned(),
        score,
        metadata: Metadata::new(),
    }
}

#[test]
fn pass_through_preserves_order_values_and_returns_an_independent_clone() {
    let request = TeacherSynthesisRequest {
        namespace: "teacher-contract".to_owned(),
        labels: vec![
            label("label-b", "replay-2", "second", Some(0.25)),
            label("label-a", "replay-1", "first", None),
        ],
    };

    let mut output = PassThroughTeacherSynthesizer
        .synthesize(&request)
        .expect("pass-through synthesis");

    assert_eq!(output, request.labels);
    assert_eq!(output[0].id, TeacherLabelId::new("label-b"));
    assert_eq!(output[1].id, TeacherLabelId::new("label-a"));

    output[0].label = "mutated-output".to_owned();
    assert_eq!(request.labels[0].label, "second");
    assert_ne!(output, request.labels);
}

#[test]
fn pass_through_component_identity_is_stable_and_empty_input_stays_empty() {
    let synthesizer = PassThroughTeacherSynthesizer;
    assert_eq!(
        synthesizer.component_name(),
        "pass-through-teacher-synthesizer"
    );

    let request = TeacherSynthesisRequest {
        namespace: "empty".to_owned(),
        labels: Vec::new(),
    };
    let output = synthesizer
        .synthesize(&request)
        .expect("empty pass-through synthesis");
    assert!(output.is_empty());
}
