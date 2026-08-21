use mimir_types::{
    ANCHOR_ARTIFACT_SCHEMA, ArtifactHeader, ArtifactKind, AnchorId, BranchId, CacheKey,
    FieldValue, LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA, LowBoostRecoveryBcArtifactId,
    LowBoostRecoveryVariantId, Metadata, RawStateWindowRef, ReplayId, ReplaySliceId,
    ReplaySubjectRef, SCOREBOARD_ARTIFACT_SCHEMA, SKILL_ARTIFACT_SCHEMA, SkillId,
    TEACHER_LABEL_ARTIFACT_SCHEMA, TeacherLabelId, VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA,
    BRANCH_ARTIFACT_SCHEMA,
};
use serde::{de::DeserializeOwned, Serialize};
use serde_json::json;

fn assert_transparent_string_id<T>(value: &str)
where
    T: From<String> + AsRef<str> + std::fmt::Display + Serialize + DeserializeOwned + PartialEq + std::fmt::Debug,
{
    let id = T::from(value.to_owned());
    assert_eq!(id.as_ref(), value);
    assert_eq!(id.to_string(), value);

    let encoded = serde_json::to_string(&id).expect("string id should serialize");
    assert_eq!(encoded, serde_json::to_string(value).unwrap());

    let decoded: T = serde_json::from_str(&encoded).expect("string id should deserialize");
    assert_eq!(decoded, id);
}

#[test]
fn all_public_string_ids_keep_transparent_wire_contract() {
    assert_transparent_string_id::<ReplayId>("replay-001");
    assert_transparent_string_id::<ReplaySliceId>("slice-001");
    assert_transparent_string_id::<AnchorId>("anchor-001");
    assert_transparent_string_id::<BranchId>("branch-001");
    assert_transparent_string_id::<SkillId>("skill-001");
    assert_transparent_string_id::<TeacherLabelId>("label-001");
    assert_transparent_string_id::<CacheKey>("cache-001");
    assert_transparent_string_id::<ReplaySubjectRef>("player:blue:0");
    assert_transparent_string_id::<RawStateWindowRef>("window-001");
    assert_transparent_string_id::<LowBoostRecoveryVariantId>("variant-001");
    assert_transparent_string_id::<LowBoostRecoveryBcArtifactId>("bc-artifact-001");
}

#[test]
fn artifact_kind_wire_schema_names_and_versions_are_exactly_locked() {
    let cases = [
        (ArtifactKind::Anchor, ANCHOR_ARTIFACT_SCHEMA, "mimir.anchor_artifact"),
        (ArtifactKind::Branch, BRANCH_ARTIFACT_SCHEMA, "mimir.branch_artifact"),
        (ArtifactKind::Skill, SKILL_ARTIFACT_SCHEMA, "mimir.skill_artifact"),
        (
            ArtifactKind::TeacherLabel,
            TEACHER_LABEL_ARTIFACT_SCHEMA,
            "mimir.teacher_label_artifact",
        ),
        (
            ArtifactKind::Scoreboard,
            SCOREBOARD_ARTIFACT_SCHEMA,
            "mimir.scoreboard_artifact",
        ),
        (
            ArtifactKind::VerticalSliceInput,
            VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA,
            "mimir.vertical_slice_input_artifact",
        ),
        (
            ArtifactKind::LowBoostRecoveryBcArtifact,
            LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA,
            "mimir.low_boost_recovery_bc_artifact",
        ),
    ];

    for (kind, constant, expected_name) in cases {
        let schema = kind.schema();
        assert_eq!(schema, constant);
        assert_eq!(schema.kind, kind);
        assert_eq!(schema.name, expected_name);
        assert_eq!(schema.version, 1);
    }
}

#[test]
fn metadata_json_and_iteration_are_deterministic_by_key() {
    let metadata = Metadata::from([
        ("zeta", FieldValue::Text("last".to_owned())),
        ("alpha", FieldValue::Integer(7)),
        ("middle", FieldValue::Boolean(true)),
    ]);

    let keys: Vec<_> = metadata.iter().map(|(key, _)| key.as_str()).collect();
    assert_eq!(keys, ["alpha", "middle", "zeta"]);

    let encoded = serde_json::to_string(&metadata).expect("metadata should serialize");
    assert_eq!(
        encoded,
        r#"{"alpha":{"type":"integer","value":7},"middle":{"type":"boolean","value":true},"zeta":{"type":"text","value":"last"}}"#
    );

    let decoded: Metadata = serde_json::from_str(&encoded).expect("metadata should deserialize");
    assert_eq!(decoded, metadata);
}

#[test]
fn metadata_duplicate_keys_are_last_write_wins_without_order_drift() {
    let metadata: Metadata = [
        ("beta", FieldValue::Integer(1)),
        ("alpha", FieldValue::Integer(2)),
        ("beta", FieldValue::Integer(3)),
    ]
    .into_iter()
    .collect();

    assert_eq!(metadata.len(), 2);
    assert_eq!(metadata.get("beta"), Some(&FieldValue::Integer(3)));
    let keys: Vec<_> = metadata.into_iter().map(|(key, _)| key).collect();
    assert_eq!(keys, ["alpha".to_owned(), "beta".to_owned()]);
}

#[test]
fn artifact_header_and_field_value_fail_closed_on_unknown_wire_fields_or_tags() {
    let header_error = serde_json::from_value::<ArtifactHeader>(json!({
        "schema_name": "mimir.anchor_artifact",
        "schema_version": 1,
        "producer": "foundation-contract-test",
        "unexpected": true
    }))
    .expect_err("ArtifactHeader must deny unknown fields");
    assert!(header_error.to_string().contains("unknown field"));

    let value_error = serde_json::from_value::<FieldValue>(json!({
        "type": "opaque_future_value",
        "value": "x"
    }))
    .expect_err("FieldValue must reject unknown tags");
    assert!(value_error.to_string().contains("unknown variant"));
}
