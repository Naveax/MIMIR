from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
import struct

MAX_LIST = 25_000
MAX_TEXT_UNITS = 10_000


class ScanError(RuntimeError):
    pass


@dataclass
class EncodingStats:
    positive: int = 0
    negative_utf16: int = 0
    zero_length: int = 0
    nul_ok: int = 0
    nul_bad: int = 0
    decode_ok: int = 0
    decode_error: int = 0

    def add(self, other: "EncodingStats") -> None:
        for name in self.__dataclass_fields__:
            setattr(self, name, getattr(self, name) + getattr(other, name))


@dataclass(frozen=True)
class ClassIndex:
    class_name: str | None
    object_index: int


@dataclass(frozen=True)
class CacheProp:
    object_index: int
    stream_id: int


@dataclass(frozen=True)
class NetCache:
    object_index: int
    parent_id: int
    cache_id: int
    properties: tuple[CacheProp, ...]


@dataclass
class ReplayEvidence:
    path: str
    objects: list[str | None]
    names: list[str | None]
    class_indices: list[ClassIndex]
    net_cache: list[NetCache]
    section_encoding: dict[str, EncodingStats]
    class_string_nul_bad: int = 0
    class_string_decode_error: int = 0
    class_index_oob: int = 0
    class_index_name_mismatch: int = 0
    class_index_name_uncheckable: int = 0
    net_cache_object_oob: int = 0
    cache_id_duplicates: int = 0
    parent_id_unresolved: int = 0
    parent_id_self: int = 0
    property_object_oob: int = 0
    negative_stream_ids: int = 0
    duplicate_stream_ids_within_cache: int = 0
    duplicate_property_objects_within_cache: int = 0
    duplicate_cache_object_indices: int = 0
    max_stream_id: int = -1
    tail_size: int = 0
    tail_hex: str = ""


class Cursor:
    def __init__(self, data: bytes, end: int | None = None) -> None:
        self.data = data
        self.pos = 0
        self.end = len(data) if end is None else end

    def require(self, size: int, field_name: str) -> None:
        if size < 0:
            raise ScanError(f"negative size for {field_name}: {size}")
        if self.pos + size > self.end:
            raise ScanError(
                f"truncated {field_name}: pos={self.pos} need={size} end={self.end}"
            )

    def take(self, size: int, field_name: str) -> bytes:
        self.require(size, field_name)
        start = self.pos
        self.pos += size
        return self.data[start:self.pos]

    def skip(self, size: int, field_name: str) -> None:
        self.take(size, field_name)

    def i32(self, field_name: str) -> int:
        raw = self.take(4, field_name)
        return struct.unpack("<i", raw)[0]

    def count(self, field_name: str) -> int:
        value = self.i32(field_name)
        if value < 0:
            raise ScanError(f"negative count for {field_name}: {value}")
        if value > MAX_LIST:
            raise ScanError(f"count too large for {field_name}: {value}")
        return value

    def unreal_text(self, field_name: str, stats: EncodingStats) -> str | None:
        units = self.i32(f"{field_name}.length")
        if units < -MAX_TEXT_UNITS or units > MAX_TEXT_UNITS:
            raise ScanError(f"text length out of bounds for {field_name}: {units}")
        if units == 0:
            stats.zero_length += 1
            stats.decode_ok += 1
            return ""

        if units < 0:
            stats.negative_utf16 += 1
            raw = self.take((-units) * 2, field_name)
            if raw.endswith(b"\x00\x00"):
                stats.nul_ok += 1
                payload = raw[:-2]
            else:
                stats.nul_bad += 1
                payload = raw
            try:
                value = payload.decode("utf-16-le", errors="strict")
            except UnicodeDecodeError:
                stats.decode_error += 1
                return None
            stats.decode_ok += 1
            return value

        stats.positive += 1
        raw = self.take(units, field_name)
        if raw.endswith(b"\x00"):
            stats.nul_ok += 1
            payload = raw[:-1]
        else:
            stats.nul_bad += 1
            payload = raw
        try:
            value = payload.decode("cp1252", errors="strict")
        except UnicodeDecodeError:
            stats.decode_error += 1
            return None
        stats.decode_ok += 1
        return value

    def raw_utf8_string(self, field_name: str) -> tuple[str | None, bool, bool]:
        size = self.i32(f"{field_name}.length")
        if size < 0 or size > MAX_TEXT_UNITS:
            raise ScanError(f"raw string length out of bounds for {field_name}: {size}")
        if size == 0:
            return "", False, False
        raw = self.take(size, field_name)
        nul_bad = not raw.endswith(b"\x00")
        payload = raw[:-1] if not nul_bad else raw
        try:
            return payload.decode("utf-8", errors="strict"), nul_bad, False
        except UnicodeDecodeError:
            return None, nul_bad, True

    def text_list(self, field_name: str, stats: EncodingStats) -> list[str | None]:
        count = self.count(f"{field_name}.count")
        return [self.unreal_text(f"{field_name}[{i}]", stats) for i in range(count)]


def skip_to_footer(data: bytes) -> tuple[Cursor, int]:
    outer = Cursor(data)
    header_size = outer.i32("header_size")
    if header_size < 0:
        raise ScanError(f"negative header_size: {header_size}")
    outer.skip(4, "header_crc")
    outer.skip(header_size, "header_data")
    content_size = outer.i32("content_size")
    if content_size < 0:
        raise ScanError(f"negative content_size: {content_size}")
    outer.skip(4, "content_crc")
    content_start = outer.pos
    content_end = content_start + content_size
    if content_end != len(data):
        raise ScanError(
            f"content framing mismatch: content_end={content_end} file_end={len(data)}"
        )

    c = Cursor(data, content_end)
    c.pos = content_start
    ignored = EncodingStats()
    c.text_list("levels", ignored)
    keyframes = c.count("keyframes.count")
    c.skip(12 * keyframes, "keyframes.data")
    network_size = c.i32("network_size")
    if network_size < 0:
        raise ScanError(f"negative network_size: {network_size}")
    c.skip(network_size, "network_data")
    return c, content_end


def scan(path: Path) -> ReplayEvidence:
    data = path.read_bytes()
    c, content_end = skip_to_footer(data)
    section_encoding = {
        "debug_user": EncodingStats(),
        "debug_text": EncodingStats(),
        "tickmark_description": EncodingStats(),
        "packages": EncodingStats(),
        "objects": EncodingStats(),
        "names": EncodingStats(),
    }

    debug_info = c.count("debug_info.count")
    for i in range(debug_info):
        c.i32(f"debug_info[{i}].frame")
        c.unreal_text(f"debug_info[{i}].user", section_encoding["debug_user"])
        c.unreal_text(f"debug_info[{i}].text", section_encoding["debug_text"])

    tickmarks = c.count("tickmarks.count")
    for i in range(tickmarks):
        c.unreal_text(
            f"tickmarks[{i}].description", section_encoding["tickmark_description"]
        )
        c.i32(f"tickmarks[{i}].frame")

    c.text_list("packages", section_encoding["packages"])
    objects = c.text_list("objects", section_encoding["objects"])
    names = c.text_list("names", section_encoding["names"])

    class_indices: list[ClassIndex] = []
    class_string_nul_bad = 0
    class_string_decode_error = 0
    for i in range(c.count("class_indices.count")):
        class_name, nul_bad, decode_error = c.raw_utf8_string(
            f"class_indices[{i}].class"
        )
        class_string_nul_bad += int(nul_bad)
        class_string_decode_error += int(decode_error)
        class_indices.append(ClassIndex(class_name, c.i32(f"class_indices[{i}].index")))

    net_cache: list[NetCache] = []
    for i in range(c.count("net_cache.count")):
        object_index = c.i32(f"net_cache[{i}].object_ind")
        parent_id = c.i32(f"net_cache[{i}].parent_id")
        cache_id = c.i32(f"net_cache[{i}].cache_id")
        properties: list[CacheProp] = []
        for j in range(c.count(f"net_cache[{i}].properties.count")):
            properties.append(
                CacheProp(
                    c.i32(f"net_cache[{i}].properties[{j}].object_ind"),
                    c.i32(f"net_cache[{i}].properties[{j}].stream_id"),
                )
            )
        net_cache.append(NetCache(object_index, parent_id, cache_id, tuple(properties)))

    tail = data[c.pos:content_end]
    evidence = ReplayEvidence(
        path=str(path),
        objects=objects,
        names=names,
        class_indices=class_indices,
        net_cache=net_cache,
        section_encoding=section_encoding,
        class_string_nul_bad=class_string_nul_bad,
        class_string_decode_error=class_string_decode_error,
        tail_size=len(tail),
        tail_hex=tail.hex(),
    )

    object_count = len(objects)
    for item in class_indices:
        if item.object_index < 0 or item.object_index >= object_count:
            evidence.class_index_oob += 1
        elif item.class_name is None or objects[item.object_index] is None:
            evidence.class_index_name_uncheckable += 1
        elif item.class_name != objects[item.object_index]:
            evidence.class_index_name_mismatch += 1

    cache_ids = [entry.cache_id for entry in net_cache]
    cache_id_set = set(cache_ids)
    evidence.cache_id_duplicates = len(cache_ids) - len(cache_id_set)
    cache_object_indices = [entry.object_index for entry in net_cache]
    evidence.duplicate_cache_object_indices = len(cache_object_indices) - len(
        set(cache_object_indices)
    )

    for entry in net_cache:
        if entry.object_index < 0 or entry.object_index >= object_count:
            evidence.net_cache_object_oob += 1
        if entry.parent_id not in cache_id_set:
            evidence.parent_id_unresolved += 1
        if entry.parent_id == entry.cache_id:
            evidence.parent_id_self += 1

        stream_ids = [prop.stream_id for prop in entry.properties]
        property_objects = [prop.object_index for prop in entry.properties]
        evidence.duplicate_stream_ids_within_cache += len(stream_ids) - len(set(stream_ids))
        evidence.duplicate_property_objects_within_cache += len(property_objects) - len(
            set(property_objects)
        )
        for prop in entry.properties:
            if prop.object_index < 0 or prop.object_index >= object_count:
                evidence.property_object_oob += 1
            if prop.stream_id < 0:
                evidence.negative_stream_ids += 1
            evidence.max_stream_id = max(evidence.max_stream_id, prop.stream_id)

    return evidence


def sum_attr(rows: list[ReplayEvidence], name: str) -> int:
    return sum(int(getattr(row, name)) for row in rows)


def emit_group(label: str, rows: list[ReplayEvidence]) -> None:
    print(f"{label}_parsed={len(rows)}")
    print(f"{label}_class_index_oob={sum_attr(rows, 'class_index_oob')}")
    print(
        f"{label}_class_index_name_mismatch={sum_attr(rows, 'class_index_name_mismatch')}"
    )
    print(
        f"{label}_class_index_name_uncheckable={sum_attr(rows, 'class_index_name_uncheckable')}"
    )
    print(f"{label}_net_cache_object_oob={sum_attr(rows, 'net_cache_object_oob')}")
    print(f"{label}_cache_id_duplicates={sum_attr(rows, 'cache_id_duplicates')}")
    print(f"{label}_parent_id_unresolved={sum_attr(rows, 'parent_id_unresolved')}")
    print(f"{label}_parent_id_self={sum_attr(rows, 'parent_id_self')}")
    print(f"{label}_property_object_oob={sum_attr(rows, 'property_object_oob')}")
    print(f"{label}_negative_stream_ids={sum_attr(rows, 'negative_stream_ids')}")
    print(
        f"{label}_duplicate_stream_ids_within_cache={sum_attr(rows, 'duplicate_stream_ids_within_cache')}"
    )
    print(
        f"{label}_duplicate_property_objects_within_cache={sum_attr(rows, 'duplicate_property_objects_within_cache')}"
    )
    print(
        f"{label}_duplicate_cache_object_indices={sum_attr(rows, 'duplicate_cache_object_indices')}"
    )
    print(f"{label}_class_string_nul_bad={sum_attr(rows, 'class_string_nul_bad')}")
    print(
        f"{label}_class_string_decode_error={sum_attr(rows, 'class_string_decode_error')}"
    )
    print(f"{label}_max_stream_id={max(row.max_stream_id for row in rows)}")
    print(
        f"{label}_object_count_range={min(len(row.objects) for row in rows)}..{max(len(row.objects) for row in rows)}"
    )
    print(
        f"{label}_name_count_range={min(len(row.names) for row in rows)}..{max(len(row.names) for row in rows)}"
    )
    print(
        f"{label}_class_index_count_range={min(len(row.class_indices) for row in rows)}..{max(len(row.class_indices) for row in rows)}"
    )
    print(
        f"{label}_net_cache_count_range={min(len(row.net_cache) for row in rows)}..{max(len(row.net_cache) for row in rows)}"
    )
    print(
        f"{label}_tail_forms="
        + ",".join(
            f"{key}:{count}"
            for key, count in sorted(Counter((row.tail_size, row.tail_hex) for row in rows).items())
        )
    )


def emit_encodings(rows: list[ReplayEvidence]) -> None:
    sections = sorted(rows[0].section_encoding)
    for section in sections:
        total = EncodingStats()
        for row in rows:
            total.add(row.section_encoding[section])
        print(
            f"encoding[{section}] positive={total.positive} utf16={total.negative_utf16} "
            f"zero={total.zero_length} nul_ok={total.nul_ok} nul_bad={total.nul_bad} "
            f"decode_ok={total.decode_ok} decode_error={total.decode_error}"
        )


def main() -> None:
    historical_paths = [
        Path("external_fixtures/sample_001.replay"),
        Path("external_fixtures/sample_002.replay"),
        Path("external_fixtures/sample_003.replay"),
    ]
    corpus_paths = sorted(Path("test_corpus/largest_100").glob("*.replay"))
    if len(corpus_paths) != 100:
        raise ScanError(f"expected 100 stress replays, found {len(corpus_paths)}")

    historical = [scan(path) for path in historical_paths]
    corpus = [scan(path) for path in corpus_paths]
    all_rows = historical + corpus

    print("R3.7 Replay Footer Lookup Evidence")
    emit_group("historical", historical)
    emit_group("largest_100", corpus)
    emit_group("all_103", all_rows)
    emit_encodings(all_rows)

    suspicious_fields = (
        "class_index_oob",
        "class_index_name_mismatch",
        "class_index_name_uncheckable",
        "net_cache_object_oob",
        "cache_id_duplicates",
        "parent_id_unresolved",
        "property_object_oob",
        "negative_stream_ids",
        "duplicate_stream_ids_within_cache",
        "duplicate_property_objects_within_cache",
        "duplicate_cache_object_indices",
        "class_string_nul_bad",
        "class_string_decode_error",
    )
    suspicious = [
        row
        for row in all_rows
        if any(int(getattr(row, field_name)) != 0 for field_name in suspicious_fields)
    ]
    print(f"rows_with_lookup_anomalies={len(suspicious)}")
    for row in suspicious[:20]:
        details = " ".join(
            f"{field_name}={getattr(row, field_name)}"
            for field_name in suspicious_fields
            if int(getattr(row, field_name)) != 0
        )
        print(f"anomaly path={row.path} {details}")

    print("network_bits_decoded=false")
    print("crc_validated=false")
    print("frame_decode=false")
    print("lookup_semantics_admitted=false")
    print("PASS: footer lookup candidates decoded and cross-references measured across 3 historical + 100 stress replays.")


if __name__ == "__main__":
    main()
