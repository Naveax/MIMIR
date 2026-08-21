use serde::Serialize;
use serde::de::DeserializeOwned;
use std::fs;
use std::path::{Path, PathBuf};
use thiserror::Error;

pub type Result<T> = std::result::Result<T, MimirError>;

#[derive(Debug, Error)]
pub enum MimirError {
    #[error("I/O error at {path}: {source}")]
    Io {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),
    #[error("TOML serialization error: {0}")]
    TomlSerialize(#[from] toml::ser::Error),
    #[error("TOML deserialization error: {0}")]
    TomlDeserialize(#[from] toml::de::Error),
    #[error("{0}")]
    Message(String),
}

impl MimirError {
    pub fn io(path: impl Into<PathBuf>, source: std::io::Error) -> Self {
        Self::Io {
            path: path.into(),
            source,
        }
    }

    pub fn message(message: impl Into<String>) -> Self {
        Self::Message(message.into())
    }
}

pub trait NamedComponent {
    fn component_name(&self) -> &'static str;
}

pub fn read_text_file(path: impl AsRef<Path>) -> Result<String> {
    let path = path.as_ref();
    fs::read_to_string(path).map_err(|error| MimirError::io(path, error))
}

pub fn load_toml_file<T>(path: impl AsRef<Path>) -> Result<T>
where
    T: DeserializeOwned,
{
    let text = read_text_file(&path)?;
    toml::from_str(&text).map_err(Into::into)
}

pub fn load_json_file<T>(path: impl AsRef<Path>) -> Result<T>
where
    T: DeserializeOwned,
{
    let text = read_text_file(&path)?;
    serde_json::from_str(&text).map_err(Into::into)
}

pub fn hash_bytes(bytes: &[u8]) -> String {
    blake3::hash(bytes).to_hex().to_string()
}

pub fn hash_serializable<T>(value: &T) -> Result<String>
where
    T: Serialize,
{
    let encoded = serde_json::to_vec(value)?;
    Ok(hash_bytes(&encoded))
}

/// Exact digest receipt for one file's current byte representation.
///
/// This is deliberately an operational helper rather than a persisted artifact schema. It lets
/// callers pin byte length plus the repository's canonical BLAKE3 digest before reusing external,
/// cached, or exported files without changing existing serialization contracts.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FileDigestReceipt {
    pub byte_len: u64,
    pub blake3: String,
}

pub fn digest_file(path: impl AsRef<Path>) -> Result<FileDigestReceipt> {
    let path = path.as_ref();
    let bytes = fs::read(path).map_err(|error| MimirError::io(path, error))?;
    let byte_len = u64::try_from(bytes.len())
        .map_err(|_| MimirError::message("file length does not fit in u64"))?;

    Ok(FileDigestReceipt {
        byte_len,
        blake3: hash_bytes(&bytes),
    })
}

pub fn verify_file_digest(
    path: impl AsRef<Path>,
    expected: &FileDigestReceipt,
) -> Result<FileDigestReceipt> {
    let path = path.as_ref();
    let actual = digest_file(path)?;

    if actual.byte_len != expected.byte_len {
        return Err(MimirError::message(format!(
            "file length mismatch at {}: expected {}, got {}",
            path.display(),
            expected.byte_len,
            actual.byte_len
        )));
    }
    if actual.blake3 != expected.blake3 {
        return Err(MimirError::message(format!(
            "file digest mismatch at {}: expected {}, got {}",
            path.display(),
            expected.blake3,
            actual.blake3
        )));
    }

    Ok(actual)
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde::{Deserialize, Serialize};
    use tempfile::tempdir;

    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    struct ExampleConfig {
        project_name: String,
        strict_mode: bool,
    }

    #[test]
    fn loads_toml_config_and_hashes_stably() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("example.toml");

        fs::write(&path, "project_name = \"MIMIR\"\nstrict_mode = true\n")
            .expect("config should be written");

        let config: ExampleConfig = load_toml_file(&path).expect("config should load");
        assert_eq!(
            config,
            ExampleConfig {
                project_name: "MIMIR".to_string(),
                strict_mode: true,
            }
        );

        let first_hash = hash_serializable(&config).expect("hash should be computed");
        let second_hash = hash_serializable(&config).expect("hash should be computed");

        assert_eq!(first_hash, second_hash);
    }

    #[test]
    fn file_digest_receipt_is_exact_and_repeatable() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("payload.bin");
        fs::write(&path, b"MIMIR\0artifact\n").expect("payload should write");

        let first = digest_file(&path).expect("file digest");
        let second = digest_file(&path).expect("file digest");

        assert_eq!(first, second);
        assert_eq!(first.byte_len, 15);
        assert_eq!(first.blake3, hash_bytes(b"MIMIR\0artifact\n"));
        assert_eq!(
            verify_file_digest(&path, &first).expect("receipt should verify"),
            first
        );
    }

    #[test]
    fn file_digest_verifier_fails_closed_after_length_or_content_drift() {
        let directory = tempdir().expect("tempdir should be created");
        let path = directory.path().join("payload.bin");
        fs::write(&path, b"alpha").expect("payload should write");
        let expected = digest_file(&path).expect("file digest");

        fs::write(&path, b"alphb").expect("same-length mutation should write");
        let digest_error = verify_file_digest(&path, &expected)
            .expect_err("same-length content mutation must fail");
        assert!(digest_error.to_string().contains("file digest mismatch"));

        fs::write(&path, b"longer").expect("length mutation should write");
        let length_error =
            verify_file_digest(&path, &expected).expect_err("length mutation must fail");
        assert!(length_error.to_string().contains("file length mismatch"));
    }
}
