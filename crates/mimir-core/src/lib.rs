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
}
