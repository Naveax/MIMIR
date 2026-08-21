use mimir_core::{MimirError, hash_bytes, load_json_file, load_toml_file, read_text_file};
use serde::Deserialize;
use std::fs;
use tempfile::tempdir;

#[derive(Debug, Deserialize)]
struct TinyConfig {
    _name: String,
}

#[test]
fn missing_text_file_preserves_the_exact_path_in_the_io_error() {
    let directory = tempdir().expect("tempdir should be created");
    let path = directory.path().join("missing.txt");

    let error = read_text_file(&path).expect_err("missing file must fail");

    match error {
        MimirError::Io {
            path: error_path, ..
        } => assert_eq!(error_path, path),
        other => panic!("expected I/O error, found {other}"),
    }
}

#[test]
fn invalid_json_and_toml_are_classified_separately() {
    let directory = tempdir().expect("tempdir should be created");
    let json_path = directory.path().join("invalid.json");
    let toml_path = directory.path().join("invalid.toml");
    fs::write(&json_path, "{not-json").expect("invalid json fixture should write");
    fs::write(&toml_path, "name = [").expect("invalid toml fixture should write");

    assert!(matches!(
        load_json_file::<TinyConfig>(&json_path),
        Err(MimirError::Json(_))
    ));
    assert!(matches!(
        load_toml_file::<TinyConfig>(&toml_path),
        Err(MimirError::TomlDeserialize(_))
    ));
}

#[test]
fn byte_hash_is_repeatable_and_changes_after_a_single_byte_mutation() {
    let baseline = b"mimir-foundation";
    let mutated = b"mimir-foundatioN";

    let first = hash_bytes(baseline);
    let second = hash_bytes(baseline);
    let changed = hash_bytes(mutated);

    assert_eq!(first, second);
    assert_ne!(first, changed);
    assert_eq!(first.len(), 64);
    assert_eq!(changed.len(), 64);
}
