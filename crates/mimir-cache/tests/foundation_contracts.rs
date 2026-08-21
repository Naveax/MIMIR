use mimir_cache::{ArtifactCache, InMemoryArtifactCache, NoveltyIndex};
use mimir_types::CacheKey;

#[test]
fn cache_put_returns_replaced_value_and_get_returns_latest_value() {
    let key = CacheKey::new("foundation:key");
    let mut cache = InMemoryArtifactCache::default();

    assert_eq!(cache.put(key.clone(), "first".to_string()), None);
    assert_eq!(cache.get(&key).map(String::as_str), Some("first"));
    assert_eq!(
        cache.put(key.clone(), "second".to_string()),
        Some("first".to_string())
    );
    assert_eq!(cache.get(&key).map(String::as_str), Some("second"));
}

#[test]
fn novelty_is_content_global_even_when_cache_keys_differ() {
    let mut novelty = NoveltyIndex::default();

    let first = novelty.observe(CacheKey::new("artifact:a"), "same-content-hash");
    let second = novelty.observe(CacheKey::new("artifact:b"), "same-content-hash");

    assert!(first.is_new);
    assert!(!second.is_new);
    assert_ne!(first.key, second.key);
    assert_eq!(first.content_hash, second.content_hash);
}

#[test]
fn distinct_content_hashes_are_each_new_on_first_observation() {
    let mut novelty = NoveltyIndex::default();

    let first = novelty.observe(CacheKey::new("artifact:a"), "hash-a");
    let second = novelty.observe(CacheKey::new("artifact:a"), "hash-b");

    assert!(first.is_new);
    assert!(second.is_new);
}
