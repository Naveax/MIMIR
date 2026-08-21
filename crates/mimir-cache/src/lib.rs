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

impl<V> InMemoryArtifactCache<V> {
    pub fn new() -> Self {
        Self {
            entries: BTreeMap::new(),
        }
    }

    pub fn len(&self) -> usize {
        self.entries.len()
    }

    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    pub fn contains_key(&self, key: &CacheKey) -> bool {
        self.entries.contains_key(key)
    }

    pub fn remove(&mut self, key: &CacheKey) -> Option<V> {
        self.entries.remove(key)
    }

    pub fn clear(&mut self) {
        self.entries.clear();
    }

    pub fn iter(&self) -> impl Iterator<Item = (&CacheKey, &V)> {
        self.entries.iter()
    }
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

    pub fn len(&self) -> usize {
        self.seen_hashes.len()
    }

    pub fn is_empty(&self) -> bool {
        self.seen_hashes.is_empty()
    }

    pub fn contains_hash(&self, content_hash: &str) -> bool {
        self.seen_hashes.contains(content_hash)
    }

    pub fn clear(&mut self) {
        self.seen_hashes.clear();
    }
}

pub fn key_for<T>(namespace: &str, value: &T) -> Result<CacheKey>
where
    T: Serialize,
{
    let digest = hash_serializable(value)?;
    Ok(CacheKey::new(format!("{namespace}:{digest}")))
}

/// Builds a deterministic, explicitly versioned cache key without changing the legacy
/// `key_for` contract. The namespace and schema version are included in both the readable
/// prefix and the hashed material so callers can invalidate a cache family by version rather
/// than silently reusing artifacts produced under a different schema.
pub fn key_for_version<T>(namespace: &str, schema_version: u32, value: &T) -> Result<CacheKey>
where
    T: Serialize,
{
    let digest = hash_serializable(&(namespace, schema_version, value))?;
    Ok(CacheKey::new(format!(
        "{namespace}:v{schema_version}:{digest}"
    )))
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

    #[test]
    fn novelty_identity_is_content_based_across_distinct_keys() {
        let mut novelty = NoveltyIndex::default();
        let first = novelty.observe(CacheKey::new("artifact:1"), "hash-1");
        let second = novelty.observe(CacheKey::new("artifact:2"), "hash-1");

        assert!(first.is_new);
        assert!(!second.is_new);
        assert_eq!(novelty.len(), 1);
        assert!(novelty.contains_hash("hash-1"));

        novelty.clear();
        assert!(novelty.is_empty());
    }

    #[test]
    fn in_memory_cache_exposes_deterministic_management_primitives() {
        let mut cache = InMemoryArtifactCache::new();
        let key_b = CacheKey::new("b");
        let key_a = CacheKey::new("a");

        assert!(cache.is_empty());
        assert_eq!(cache.put(key_b.clone(), 2), None);
        assert_eq!(cache.put(key_a.clone(), 1), None);
        assert_eq!(cache.len(), 2);
        assert!(cache.contains_key(&key_a));
        assert_eq!(cache.get(&key_b), Some(&2));

        let ordered_keys = cache
            .iter()
            .map(|(key, _)| key.as_str().to_owned())
            .collect::<Vec<_>>();
        assert_eq!(ordered_keys, vec!["a".to_string(), "b".to_string()]);

        assert_eq!(cache.remove(&key_a), Some(1));
        assert!(!cache.contains_key(&key_a));
        cache.clear();
        assert!(cache.is_empty());
    }

    #[test]
    fn versioned_cache_keys_are_repeatable_and_domain_separated() {
        let value = BTreeMap::from([("alpha".to_string(), 7_u32)]);
        let first = key_for_version("raw-state", 1, &value).expect("versioned key");
        let repeated = key_for_version("raw-state", 1, &value).expect("versioned key");
        let next_version = key_for_version("raw-state", 2, &value).expect("versioned key");
        let other_namespace = key_for_version("events", 1, &value).expect("versioned key");

        assert_eq!(first, repeated);
        assert_ne!(first, next_version);
        assert_ne!(first, other_namespace);
        assert!(first.as_str().starts_with("raw-state:v1:"));
    }
}
