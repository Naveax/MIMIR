from __future__ import annotations

from collections import Counter
from pathlib import Path

from r3_7_footer_lookup_evidence import scan


def first_index_by_name(objects: list[str | None]) -> dict[str, int]:
    out: dict[str, int] = {}
    for index, name in enumerate(objects):
        if name is not None and name not in out:
            out[name] = index
    return out


def main() -> None:
    historical_paths = [
        Path("external_fixtures/sample_001.replay"),
        Path("external_fixtures/sample_002.replay"),
        Path("external_fixtures/sample_003.replay"),
    ]
    corpus_paths = sorted(Path("test_corpus/largest_100").glob("*.replay"))
    if len(corpus_paths) != 100:
        raise RuntimeError(f"expected 100 stress replays, found {len(corpus_paths)}")

    rows = [scan(path) for path in historical_paths + corpus_paths]

    cache_id_values: Counter[int] = Counter()
    parent_id_values: Counter[int] = Counter()
    cache_id_duplicate_values: Counter[int] = Counter()
    unresolved_parent_values: Counter[int] = Counter()
    self_parent_values: Counter[int] = Counter()
    rows_with_duplicate_object_names = 0
    duplicate_object_name_entries = 0
    net_cache_on_nonfirst_duplicate_name = 0
    property_refs_on_nonfirst_duplicate_name = 0
    class_indices_on_nonfirst_duplicate_name = 0
    rows_with_nonfirst_lookup_refs = 0
    net_cache_object_index_duplicates = 0
    class_index_object_bounds_failures = 0
    net_cache_object_bounds_failures = 0
    property_object_bounds_failures = 0
    duplicate_stream_ids_within_cache = 0
    negative_stream_ids = 0
    class_index_name_mismatches = 0

    for row in rows:
        object_count = len(row.objects)
        first = first_index_by_name(row.objects)
        name_counts = Counter(name for name in row.objects if name is not None)
        duplicate_names = {name for name, count in name_counts.items() if count > 1}
        if duplicate_names:
            rows_with_duplicate_object_names += 1
            duplicate_object_name_entries += sum(name_counts[name] - 1 for name in duplicate_names)

        cache_ids = [entry.cache_id for entry in row.net_cache]
        parents = [entry.parent_id for entry in row.net_cache]
        cache_id_values.update(cache_ids)
        parent_id_values.update(parents)
        cache_counts = Counter(cache_ids)
        for value, count in cache_counts.items():
            if count > 1:
                cache_id_duplicate_values[value] += count - 1
        cache_set = set(cache_ids)
        for parent in parents:
            if parent not in cache_set:
                unresolved_parent_values[parent] += 1
        for entry in row.net_cache:
            if entry.parent_id == entry.cache_id:
                self_parent_values[entry.parent_id] += 1

        cache_object_indices = [entry.object_index for entry in row.net_cache]
        net_cache_object_index_duplicates += len(cache_object_indices) - len(set(cache_object_indices))

        row_nonfirst_refs = 0
        for entry in row.net_cache:
            if not (0 <= entry.object_index < object_count):
                net_cache_object_bounds_failures += 1
                continue
            name = row.objects[entry.object_index]
            if name is not None and first.get(name) != entry.object_index:
                net_cache_on_nonfirst_duplicate_name += 1
                row_nonfirst_refs += 1

            streams = [prop.stream_id for prop in entry.properties]
            duplicate_stream_ids_within_cache += len(streams) - len(set(streams))
            negative_stream_ids += sum(stream_id < 0 for stream_id in streams)
            for prop in entry.properties:
                if not (0 <= prop.object_index < object_count):
                    property_object_bounds_failures += 1
                    continue
                prop_name = row.objects[prop.object_index]
                if prop_name is not None and first.get(prop_name) != prop.object_index:
                    property_refs_on_nonfirst_duplicate_name += 1
                    row_nonfirst_refs += 1

        for item in row.class_indices:
            if not (0 <= item.object_index < object_count):
                class_index_object_bounds_failures += 1
                continue
            object_name = row.objects[item.object_index]
            if item.class_name != object_name:
                class_index_name_mismatches += 1
            if object_name is not None and first.get(object_name) != item.object_index:
                class_indices_on_nonfirst_duplicate_name += 1
                row_nonfirst_refs += 1

        if row_nonfirst_refs:
            rows_with_nonfirst_lookup_refs += 1

    print("R3.7b Replay Footer Lookup Semantic Refinement")
    print(f"rows_scanned={len(rows)}")
    print(f"rows_with_duplicate_object_names={rows_with_duplicate_object_names}")
    print(f"duplicate_object_name_entries={duplicate_object_name_entries}")
    print(f"net_cache_on_nonfirst_duplicate_name={net_cache_on_nonfirst_duplicate_name}")
    print(f"property_refs_on_nonfirst_duplicate_name={property_refs_on_nonfirst_duplicate_name}")
    print(f"class_indices_on_nonfirst_duplicate_name={class_indices_on_nonfirst_duplicate_name}")
    print(f"rows_with_nonfirst_lookup_refs={rows_with_nonfirst_lookup_refs}")
    print(f"net_cache_object_index_duplicates={net_cache_object_index_duplicates}")
    print(f"class_index_object_bounds_failures={class_index_object_bounds_failures}")
    print(f"net_cache_object_bounds_failures={net_cache_object_bounds_failures}")
    print(f"property_object_bounds_failures={property_object_bounds_failures}")
    print(f"duplicate_stream_ids_within_cache={duplicate_stream_ids_within_cache}")
    print(f"negative_stream_ids={negative_stream_ids}")
    print(f"class_index_name_mismatches={class_index_name_mismatches}")
    print("cache_id_top=" + ",".join(f"{value}:{count}" for value, count in cache_id_values.most_common(20)))
    print("parent_id_top=" + ",".join(f"{value}:{count}" for value, count in parent_id_values.most_common(20)))
    print("cache_id_duplicate_values=" + ",".join(f"{value}:{count}" for value, count in cache_id_duplicate_values.most_common(20)))
    print("unresolved_parent_values=" + ",".join(f"{value}:{count}" for value, count in unresolved_parent_values.most_common(20)))
    print("self_parent_values=" + ",".join(f"{value}:{count}" for value, count in self_parent_values.most_common(20)))
    print("boxcars_lookup_key=net_cache.object_ind")
    print("boxcars_cache_id_used_for_lookup=false")
    print("boxcars_parent_id_used_for_lookup=false")
    print("boxcars_inheritance_source=object_name_hierarchy")
    print("network_bits_decoded=false")
    print("hierarchy_materialized=false")

    hard_failures = (
        net_cache_object_index_duplicates
        + class_index_object_bounds_failures
        + net_cache_object_bounds_failures
        + property_object_bounds_failures
        + duplicate_stream_ids_within_cache
        + negative_stream_ids
        + class_index_name_mismatches
    )
    if hard_failures != 0:
        raise RuntimeError(f"admitted raw lookup invariants failed: total={hard_failures}")

    print("PASS: raw footer lookup invariants hold across 103 replays; cache_id/parent_id retained as opaque raw fields, not hierarchy predicates.")


if __name__ == "__main__":
    main()
