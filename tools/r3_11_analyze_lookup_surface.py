from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

NORMALIZED_INSTANCE_TYPES = (
    "CrowdActor_TA",
    "CrowdManager_TA",
    "VehiclePickup_Boost_TA",
    "InMapScoreboard_TA",
    "BreakOutActor_Platform_TA",
    "PlayerStart_Platform_TA",
)


def section(text: str, start_marker: str, end_marker: str | None = None) -> str:
    start = text.index(start_marker)
    if end_marker is None:
        return text[start:]
    end = text.index(end_marker, start)
    return text[start:end]


def parse_attribute_tags(data_rs: str) -> dict[str, str]:
    body = section(
        data_rs,
        "pub(crate) static ATTRIBUTES",
        "pub(crate) static PARENT_CLASSES",
    )
    rows = re.findall(r'"([^"]+)"\s*=>\s*AttributeTag::([A-Za-z0-9_]+)\s*,', body)
    return dict(rows)


def parse_parent_classes(data_rs: str) -> dict[str, str]:
    body = section(data_rs, "pub(crate) static PARENT_CLASSES")
    rows = re.findall(r'"([^"]+)"\s*=>\s*"([^"]+)"\s*,', body)
    return dict(rows)


def parse_spawn_stats(data_rs: str) -> dict[str, str]:
    body = section(data_rs, "pub(crate) static SPAWN_STATS", "pub(crate) static ATTRIBUTES")
    rows = re.findall(
        r'\(\s*"([^"]+)"\s*,\s*SpawnTrajectory::([A-Za-z0-9_]+)\s*,?\s*\)',
        body,
        re.DOTALL,
    )
    return dict(rows)


def normalize_object(name: str) -> str:
    prefix = "TheWorld:PersistentLevel."
    rest: str | None = None
    if name.startswith(prefix):
        rest = name[len(prefix) :]
    elif "." in name:
        _, suffix = name.split(".", 1)
        if suffix.startswith(prefix):
            rest = suffix[len(prefix) :]
    if rest is None:
        return name
    for kind in NORMALIZED_INSTANCE_TYPES:
        if rest.startswith(kind):
            return prefix + kind
    return name


def parse_dump(path: Path):
    net_attrs: set[str] = set()
    decoded_attrs: set[str] = set()
    objects: set[str] = set()
    net_classes: set[str] = set()
    spawn_shapes: dict[str, set[str]] = defaultdict(set)
    summaries: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if line.startswith("NET_CACHE_ATTRIBUTE_NAME\t"):
            net_attrs.add(line.split("\t", 1)[1])
        elif line.startswith("DECODED_ATTRIBUTE_NAME\t"):
            decoded_attrs.add(line.split("\t", 1)[1])
        elif line.startswith("OBJECT_NAME\t"):
            objects.add(line.split("\t", 1)[1])
        elif line.startswith("NET_CACHE_CLASS\t"):
            net_classes.add(line.split("\t", 1)[1])
        elif line.startswith("SPAWN_SHAPE\t"):
            _, name, shapes = line.split("\t", 2)
            spawn_shapes[name].update(shapes.split(","))
        elif line.startswith("SUMMARY ") and "=" in line:
            key, value = line[len("SUMMARY ") :].split("=", 1)
            summaries[key] = value
    return net_attrs, decoded_attrs, objects, net_classes, spawn_shapes, summaries


def hierarchy_edges(name: str, parents: dict[str, str]):
    current = name
    seen: set[str] = set()
    while True:
        lookup = normalize_object(current)
        parent = parents.get(lookup)
        if parent is None:
            return
        edge = (lookup, parent)
        if lookup in seen:
            raise RuntimeError(f"parent cycle at {lookup}")
        seen.add(lookup)
        yield edge
        current = parent


def source_spawn_candidate(name: str, parents: dict[str, str], spawns: dict[str, str]) -> str | None:
    current = name
    seen: set[str] = set()
    while True:
        if current in spawns:
            return spawns[current]
        lookup = normalize_object(current)
        if lookup in spawns:
            return spawns[lookup]
        if lookup in seen:
            raise RuntimeError(f"spawn parent cycle at {lookup}")
        seen.add(lookup)
        parent = parents.get(lookup)
        if parent is None:
            return None
        current = parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-rs", required=True, type=Path)
    parser.add_argument("--dump", required=True, type=Path)
    args = parser.parse_args()

    data_rs = args.data_rs.read_text(encoding="utf-8")
    attribute_tags = parse_attribute_tags(data_rs)
    parents = parse_parent_classes(data_rs)
    spawns = parse_spawn_stats(data_rs)
    net_attrs, decoded_attrs, objects, net_classes, spawn_shapes, summaries = parse_dump(args.dump)

    # Boxcars intentionally maps a net-cache property absent from ATTRIBUTES to
    # AttributeTag::NotImplemented. Absence from the static map is therefore an
    # explicit wire-registry state, not malformed replay evidence.
    not_implemented_names = sorted(net_attrs - attribute_tags.keys())
    decoded_not_implemented_names = sorted(decoded_attrs - attribute_tags.keys())
    net_tag_counts = Counter(attribute_tags.get(name, "NotImplemented") for name in net_attrs)
    decoded_tag_counts = Counter(attribute_tags.get(name, "NotImplemented") for name in decoded_attrs)

    used_edges: set[tuple[str, str]] = set()
    for name in objects:
        used_edges.update(hierarchy_edges(name, parents))

    used_net_edges: set[tuple[str, str]] = set()
    for name in net_classes:
        used_net_edges.update(hierarchy_edges(name, parents))

    normalized_spawn_names = {normalize_object(name) for name in spawn_shapes}
    spawn_candidate_counts = Counter()
    unresolved_spawn_names: list[str] = []
    multi_shape_names = {name: shapes for name, shapes in spawn_shapes.items() if len(shapes) > 1}
    source_shape_mismatches: list[tuple[str, str, str]] = []
    for name, shapes in sorted(spawn_shapes.items()):
        candidate = source_spawn_candidate(name, parents, spawns)
        if candidate is None:
            unresolved_spawn_names.append(name)
            continue
        spawn_candidate_counts[candidate] += 1
        if len(shapes) == 1:
            observed = next(iter(shapes))
            if observed != candidate:
                source_shape_mismatches.append((name, observed, candidate))

    print("R3.11 Authoritative Lookup Surface Evidence")
    print("boxcars_git_rev=c70e77df7af81b436cb545d070bb90c82f562d0b")
    print(f"source_attribute_registry_entries={len(attribute_tags)}")
    print(f"source_parent_class_entries={len(parents)}")
    print(f"source_spawn_stats_entries={len(spawns)}")
    print(f"supported_attribute_names_from_net_cache={len(net_attrs)}")
    print(f"supported_attribute_names_known_registry={len(net_attrs) - len(not_implemented_names)}")
    print(f"supported_attribute_names_not_implemented_fallback={len(not_implemented_names)}")
    print(f"supported_net_cache_authoritative_tag_kinds={len(net_tag_counts)}")
    print(f"supported_decoded_attribute_names={len(decoded_attrs)}")
    print(f"supported_decoded_attribute_names_not_implemented={len(decoded_not_implemented_names)}")
    print(f"supported_decoded_authoritative_tag_kinds={len(decoded_tag_counts)}")
    print(f"supported_all_object_names={len(objects)}")
    print(f"supported_net_cache_class_names={len(net_classes)}")
    print(f"supported_parent_edges_all_objects={len(used_edges)}")
    print(f"supported_parent_edges_net_cache_classes={len(used_net_edges)}")
    print(f"supported_spawn_object_names={len(spawn_shapes)}")
    print(f"supported_normalized_spawn_names={len(normalized_spawn_names)}")
    print(f"supported_spawn_names_with_multiple_observed_shapes={len(multi_shape_names)}")
    print(f"supported_spawn_names_without_source_candidate={len(unresolved_spawn_names)}")
    print(f"supported_spawn_source_shape_mismatches={len(source_shape_mismatches)}")
    print(f"dump_duplicate_object_names={summaries.get('duplicate_object_names', '<missing>')}")
    print(f"dump_net_cache_object_oob={summaries.get('net_cache_object_oob', '<missing>')}")
    print(f"dump_net_property_object_oob={summaries.get('net_property_object_oob', '<missing>')}")
    print(f"dump_decoded_attribute_object_oob={summaries.get('decoded_attribute_object_oob', '<missing>')}")
    print(f"dump_spawn_object_oob={summaries.get('spawn_object_oob', '<missing>')}")

    for tag, count in sorted(net_tag_counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"NET_CACHE_AUTHORITATIVE_TAG kind={tag} attribute_names={count}")
    for tag, count in sorted(decoded_tag_counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"DECODED_AUTHORITATIVE_TAG kind={tag} attribute_names={count}")
    for name in not_implemented_names:
        print(f"NOT_IMPLEMENTED_FALLBACK name={name}")
    for name in decoded_not_implemented_names:
        print(f"DECODED_NOT_IMPLEMENTED name={name}")
    for child, parent in sorted(used_net_edges):
        print(f"NET_CACHE_PARENT_EDGE child={child} parent={parent}")
    for child, parent in sorted(used_edges - used_net_edges):
        print(f"OTHER_PARENT_EDGE child={child} parent={parent}")
    for kind, count in sorted(spawn_candidate_counts.items()):
        print(f"SOURCE_SPAWN_KIND kind={kind} object_names={count}")
    for name, shapes in sorted(multi_shape_names.items()):
        print(f"MULTI_SPAWN_SHAPE name={name} shapes={','.join(sorted(shapes))}")
    for name in unresolved_spawn_names:
        print(f"UNRESOLVED_SPAWN name={name}")
    for name, observed, candidate in source_shape_mismatches:
        print(f"SPAWN_SHAPE_MISMATCH name={name} observed={observed} source_candidate={candidate}")

    if decoded_not_implemented_names:
        raise SystemExit("an AttributeTag::NotImplemented stream was observed in decoded updates")
    if summaries.get("net_cache_object_oob") != "0" or summaries.get("net_property_object_oob") != "0":
        raise SystemExit("dump contained out-of-bounds net-cache references")
    if summaries.get("decoded_attribute_object_oob") != "0":
        raise SystemExit("dump contained out-of-bounds decoded attribute references")
    if summaries.get("spawn_object_oob") != "0":
        raise SystemExit("dump contained out-of-bounds spawn references")

    print("not_implemented_registry_fallback_admitted=true")
    print("not_implemented_stream_payload_decode_admitted=false")
    print("global_name_to_decoded_variant_admitted=false")
    print("authoritative_attribute_tag_registry_evidence=true")
    print("parent_hierarchy_surface_evidence=true")
    print("production_source_mutation=false")
    print("R3_11_AUTHORITATIVE_LOOKUP_SURFACE_COMPLETED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
