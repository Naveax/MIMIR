use mimir_export::{
    EXPORT_BUNDLE_PRODUCER, EXPORT_INDEX_FILE_NAME, EXPORT_MANIFEST_VERSION, ExportEncoding,
    ExportManifest, load_export_index,
};
use tempfile::tempdir;

fn manifest_with_index_path(relative_index_path: impl Into<String>) -> ExportManifest {
    ExportManifest {
        manifest_version: EXPORT_MANIFEST_VERSION,
        export_name: "path-boundary-contract".to_owned(),
        producer: EXPORT_BUNDLE_PRODUCER.to_owned(),
        created_by_component: Some("integration-test".to_owned()),
        artifact_encoding: ExportEncoding::Json,
        relative_index_path: relative_index_path.into(),
        artifact_count: 0,
        anchor_count: 0,
        branch_count: 0,
    }
}

#[test]
fn absolute_manifest_index_path_is_rejected_before_filesystem_read() {
    let directory = tempdir().expect("tempdir should be created");
    let absolute = directory.path().join("outside-index.json");
    assert!(absolute.is_absolute());

    let error = load_export_index(
        directory.path(),
        &manifest_with_index_path(absolute.to_string_lossy()),
    )
    .expect_err("absolute export index path must fail closed");

    assert!(
        error
            .to_string()
            .contains("absolute paths are not allowed in export index"),
        "unexpected error: {error}"
    );
}

#[test]
fn current_directory_component_is_rejected_as_non_normal_path() {
    let directory = tempdir().expect("tempdir should be created");

    let error = load_export_index(
        directory.path(),
        &manifest_with_index_path(format!("./{EXPORT_INDEX_FILE_NAME}")),
    )
    .expect_err("current-directory export index path must fail closed");

    assert!(
        error
            .to_string()
            .contains("non-normal relative path component"),
        "unexpected error: {error}"
    );
}

#[test]
fn whitespace_only_manifest_index_path_is_rejected() {
    let directory = tempdir().expect("tempdir should be created");

    let error = load_export_index(directory.path(), &manifest_with_index_path("   "))
        .expect_err("blank export index path must fail closed");

    assert!(
        error.to_string().contains("relative path must not be empty"),
        "unexpected error: {error}"
    );
}
