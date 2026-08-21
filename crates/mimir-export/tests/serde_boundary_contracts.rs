use mimir_export::{
    CandidateRequest, CandidateSelection, ExportEncoding, ExportIndexEntry, ExportManifest,
};

#[test]
fn export_manifest_rejects_unknown_fields() {
    let valid = r#"{
  "manifest_version": 1,
  "export_name": "fixture-export",
  "producer": "mimir-export",
  "artifact_encoding": "json",
  "relative_index_path": "index.json",
  "artifact_count": 0,
  "anchor_count": 0,
  "branch_count": 0
}"#;
    let widened = r#"{
  "manifest_version": 1,
  "export_name": "fixture-export",
  "producer": "mimir-export",
  "artifact_encoding": "json",
  "relative_index_path": "index.json",
  "artifact_count": 0,
  "anchor_count": 0,
  "branch_count": 0,
  "unexpected_manifest_field": true
}"#;

    serde_json::from_str::<ExportManifest>(valid).expect("baseline manifest should deserialize");
    serde_json::from_str::<ExportManifest>(widened)
        .expect_err("manifest contract must fail closed on unknown fields");
}

#[test]
fn export_index_entry_rejects_unknown_fields() {
    let valid = r#"{
  "artifact_kind": "anchor",
  "record_id": "anchor-1",
  "relative_path": "anchors/anchor-1.json",
  "schema_name": "mimir.anchor_artifact",
  "schema_version": 1,
  "content_hash": "deadbeef"
}"#;
    let widened = r#"{
  "artifact_kind": "anchor",
  "record_id": "anchor-1",
  "relative_path": "anchors/anchor-1.json",
  "schema_name": "mimir.anchor_artifact",
  "schema_version": 1,
  "content_hash": "deadbeef",
  "unexpected_index_field": "future"
}"#;

    serde_json::from_str::<ExportIndexEntry>(valid)
        .expect("baseline export index entry should deserialize");
    serde_json::from_str::<ExportIndexEntry>(widened)
        .expect_err("index entry contract must fail closed on unknown fields");
}

#[test]
fn candidate_request_rejects_unknown_fields() {
    let valid = r#"{
  "request_id": "request-1",
  "export_name": "fixture-export",
  "anchor_selection": {"mode": "all"},
  "branch_selection": {"mode": "explicit", "ids": ["branch-1"]}
}"#;
    let widened = r#"{
  "request_id": "request-1",
  "export_name": "fixture-export",
  "anchor_selection": {"mode": "all"},
  "branch_selection": {"mode": "explicit", "ids": ["branch-1"]},
  "unexpected_request_field": 1
}"#;

    serde_json::from_str::<CandidateRequest>(valid)
        .expect("baseline candidate request should deserialize");
    serde_json::from_str::<CandidateRequest>(widened)
        .expect_err("candidate request contract must fail closed on unknown fields");
}

#[test]
fn public_export_enums_reject_unknown_or_mis_cased_variants() {
    assert_eq!(
        serde_json::from_str::<ExportEncoding>(r#""json""#)
            .expect("lowercase json encoding should deserialize"),
        ExportEncoding::Json
    );
    serde_json::from_str::<ExportEncoding>(r#""JSON""#)
        .expect_err("encoding names are exact and must not be guessed case-insensitively");

    assert_eq!(
        serde_json::from_str::<CandidateSelection>(r#"{"mode":"all"}"#)
            .expect("known candidate selection should deserialize"),
        CandidateSelection::All
    );
    serde_json::from_str::<CandidateSelection>(r#"{"mode":"future_mode","ids":[]}"#)
        .expect_err("unknown candidate selection modes must fail closed");
}
