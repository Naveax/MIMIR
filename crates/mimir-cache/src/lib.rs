use mimir_core::{Result, hash_serializable};
use mimir_types::CacheKey;
use serde::Serialize;
use serde::{Deserialize, Serialize as DeriveSerialize};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, DeriveSerialize, Deserialize, PartialEq, Eq)]
pub struct NoveltyObservation {
    pub key: CacheKey,
    pub content_hash: String,
    pub is_new: bool,
}

pub trait ArtifactCache<V> {
    fn get(&self, key: &CacheKey) -> Option<&V>;
    fn put(&mut self, key: CacheKey, value: V) -> Option<V>;
}

#[derive(Debug, Clone, Default)]
pub struct InMemoryArtifactCache<V> {
    entries: BTreeMap<CacheKey, V>,
}

impl<V> ArtifactCache<V> for InMemoryArtifactCache<V> {
    fn get(&self, key: &CacheKey) -> Option<&V> {
        self.entries.get(key)
    }

    fn put(&mut self, key: CacheKey, value: V) -> Option<V> {
        self.entries.insert(key, value)
    }
}

#[derive(Debug, Clone, Default)]
pub struct NoveltyIndex {
    seen_hashes: BTreeSet<String>,
}

impl NoveltyIndex {
    pub fn observe(
        &mut self,
        key: CacheKey,
        content_hash: impl Into<String>,
    ) -> NoveltyObservation {
        let content_hash = content_hash.into();
        let is_new = self.seen_hashes.insert(content_hash.clone());

        NoveltyObservation {
            key,
            content_hash,
            is_new,
        }
    }
}

pub fn key_for<T>(namespace: &str, value: &T) -> Result<CacheKey>
where
    T: Serialize,
{
    let digest = hash_serializable(value)?;
    Ok(CacheKey::new(format!("{namespace}:{digest}")))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn novelty_index_reports_first_observation_only_once() {
        let key = CacheKey::new("artifact:1");
        let mut novelty = NoveltyIndex::default();
        let first = novelty.observe(key.clone(), "hash-1");
        let second = novelty.observe(key, "hash-1");

        assert!(first.is_new);
        assert!(!second.is_new);
    }
}
