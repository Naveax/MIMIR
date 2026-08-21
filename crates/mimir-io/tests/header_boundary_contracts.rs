use mimir_io::{ArtifactFormat, read_artifact_auto, read_artifact_header_auto};
use mimir_types::{AnchorArtifactPayload, ArtifactKind};
use tempfile::tempdir;

fn write_text(path: &std::path::Path, text: &str) {
    std::fs::write(path, text).expect("test fixture should be written");
}

#[test]
fn header_only_read_does_not_require_payload_schema_deserialization() {
    let directory = tempdir().expect("tempdir should be created");
    let path = directory.path().join("opaque-payload.json");

    write_text(
        &path,
        r#"{
  "header": {
    "schema_name": "mimir.anchor_artifact",
    "schema_version": 1,
    "producer": "mimir-io-header-boundary-test"
  },
  "payload": {
    "opaque_future_shape": true,
    "nested": [1, 2, 3]
  }
}"#,
    );

    let header = read_artifact_header_auto(&path)
        .expect("header-only inspection should ignore the payload schema");
    assert_eq!(header.schema_name, ArtifactKind::Anchor.schema().name);
    assert_eq!(header.schema_version, ArtifactKind::Anchor.schema().version);
    assert_eq!(header.producer, "mimir-io-header-boundary-test");

    read_artifact_auto::<AnchorArtifactPayload>(&path, ArtifactKind::Anchor.schema())
        .expect_err("typed payload loading must still reject the opaque payload shape");
}

#[test]
fn header_only_read_rejects_unknown_envelope_fields() {
    let directory = tempdir().expect("tempdir should be created");
    let path = directory.path().join("unknown-envelope-field.json");

    write_text(
        &path,
        r#"{
  "header": {
    "schema_name": "mimir.anchor_artifact",
    "schema_version": 1,
    "producer": "mimir-io-header-boundary-test"
  },
  "payload": {},
  "unexpected_top_level": true
}"#,
    );

    read_artifact_header_auto(&path)
        .expect_err("header inspection must fail closed on unknown envelope fields");
}

#[test]
fn header_only_read_rejects_unknown_header_fields() {
    let directory = tempdir().expect("tempdir should be created");
    let path = directory.path().join("unknown-header-field.json");

    write_text(
        &path,
        r#"{
  "header": {
    "schema_name": "mimir.anchor_artifact",
    "schema_version": 1,
    "producer": "mimir-io-header-boundary-test",
    "unexpected_header_field": true
  },
  "payload": {}
}"#,
    );

    read_artifact_header_auto(&path)
        .expect_err("header inspection must fail closed on unknown header fields");
}

#[test]
fn artifact_format_inference_is_exact_and_extension_bounded() {
    assert_eq!(
        ArtifactFormat::from_path("artifact.json"),
        Some(ArtifactFormat::Json)
    );
    assert_eq!(
        ArtifactFormat::from_path("artifact.toml"),
        Some(ArtifactFormat::Toml)
    );
    assert_eq!(ArtifactFormat::from_path("artifact.JSON"), None);
    assert_eq!(ArtifactFormat::from_path("artifact"), None);
    assert_eq!(ArtifactFormat::from_path("artifact.json.tmp"), None);
}
