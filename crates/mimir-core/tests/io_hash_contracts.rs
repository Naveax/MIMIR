use mimir_core::{MimirError, hash_bytes, hash_serializable, load_json_file, read_text_file};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::fs;
use tempfile::tempdir;

#[derive(Debug, Serialize, Deserialize, PartialEq)]
struct JsonFixture {
    name: String,
    enabled: bool,
}

#[test]
fn json_loader_preserves_typed_content_and_rejects_malformed_input() {
    let directory = tempdir().expect("tempdir");
    let valid = directory.path().join("valid.json");
    fs::write(&valid, r#"{"name":"MIMIR","enabled":true}"#).expect("write valid json");

    let decoded: JsonFixture = load_json_file(&valid).expect("valid json should load");
    assert_eq!(
        decoded,
        JsonFixture {
            name: "MIMIR".to_owned(),
            enabled: true,
        }
    );

    let malformed = directory.path().join("malformed.json");
    fs::write(&malformed, b"{not-json}").expect("write malformed json");
    match load_json_file::<JsonFixture>(&malformed).expect_err("malformed json must fail") {
        MimirError::Json(_) => {}
        other => panic!("expected JSON error, got {other}"),
    }
}

#[test]
fn missing_text_file_keeps_exact_path_in_io_error() {
    let directory = tempdir().expect("tempdir");
    let missing = directory.path().join("missing.txt");

    match read_text_file(&missing).expect_err("missing file must fail") {
        MimirError::Io { path, .. } => assert_eq!(path, missing),
        other => panic!("expected path-aware I/O error, got {other}"),
    }
}

#[test]
fn byte_and_serializable_hashes_are_repeatable_and_content_sensitive() {
    let first = hash_bytes(b"MIMIR-core-contract");
    let repeated = hash_bytes(b"MIMIR-core-contract");
    let changed = hash_bytes(b"MIMIR-core-contracu");

    assert_eq!(first, repeated);
    assert_ne!(first, changed);
    assert_eq!(first.len(), 64);
    assert!(first.bytes().all(|byte| byte.is_ascii_hexdigit()));

    let mut left = BTreeMap::new();
    left.insert("alpha", 1_u32);
    left.insert("beta", 2_u32);
    let mut right = BTreeMap::new();
    right.insert("beta", 2_u32);
    right.insert("alpha", 1_u32);

    assert_eq!(
        hash_serializable(&left).expect("hash left"),
        hash_serializable(&right).expect("hash right")
    );
}
