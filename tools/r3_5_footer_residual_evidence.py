from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import struct

MAX_LIST = 25_000
MAX_TEXT_CHARS = 10_000


class ScanError(RuntimeError):
    pass


@dataclass(frozen=True)
class Result:
    path: str
    content_end: int
    network_end: int
    footer_start: int
    known_footer_end: int
    residual_len: int
    residual_hex: str
    debug_info: int
    tickmarks: int
    packages: int
    objects: int
    names: int
    class_indices: int
    net_cache: int
    net_cache_properties: int


class Cursor:
    def __init__(self, data: bytes, end: int | None = None) -> None:
        self.data = data
        self.pos = 0
        self.end = len(data) if end is None else end

    def require(self, size: int, field: str) -> None:
        if size < 0:
            raise ScanError(f"negative size for {field}: {size}")
        if self.pos + size > self.end:
            raise ScanError(
                f"truncated {field}: pos={self.pos} need={size} end={self.end}"
            )

    def i32(self, field: str) -> int:
        self.require(4, field)
        value = struct.unpack_from("<i", self.data, self.pos)[0]
        self.pos += 4
        return value

    def skip(self, size: int, field: str) -> None:
        self.require(size, field)
        self.pos += size

    def count(self, field: str) -> int:
        value = self.i32(field)
        if value < 0:
            raise ScanError(f"negative count for {field}: {value}")
        if value > MAX_LIST:
            raise ScanError(f"count too large for {field}: {value}")
        return value

    def text(self, field: str) -> None:
        chars = self.i32(f"{field}.length")
        if chars < -MAX_TEXT_CHARS or chars > MAX_TEXT_CHARS:
            raise ScanError(f"text length out of bounds for {field}: {chars}")
        size = -2 * chars if chars < 0 else chars
        self.skip(size, field)

    def raw_string(self, field: str) -> None:
        size = self.i32(f"{field}.length")
        if size < 0 or size > MAX_TEXT_CHARS:
            raise ScanError(f"raw string length out of bounds for {field}: {size}")
        self.skip(size, field)

    def text_list(self, field: str) -> int:
        count = self.count(f"{field}.count")
        for i in range(count):
            self.text(f"{field}[{i}]")
        return count


def scan(path: Path) -> Result:
    data = path.read_bytes()
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

    c.text_list("levels")
    keyframes = c.count("keyframes.count")
    c.skip(12 * keyframes, "keyframes.data")

    network_size = c.i32("network_size")
    if network_size < 0:
        raise ScanError(f"negative network_size: {network_size}")
    c.skip(network_size, "network_data")
    network_end = c.pos
    footer_start = c.pos

    debug_info = c.count("debug_info.count")
    for i in range(debug_info):
        c.i32(f"debug_info[{i}].frame")
        c.text(f"debug_info[{i}].user")
        c.text(f"debug_info[{i}].text")

    tickmarks = c.count("tickmarks.count")
    for i in range(tickmarks):
        c.text(f"tickmarks[{i}].description")
        c.i32(f"tickmarks[{i}].frame")

    packages = c.text_list("packages")
    objects = c.text_list("objects")
    names = c.text_list("names")

    class_indices = c.count("class_indices.count")
    for i in range(class_indices):
        c.raw_string(f"class_indices[{i}].class")
        c.i32(f"class_indices[{i}].index")

    net_cache = c.count("net_cache.count")
    net_cache_properties = 0
    for i in range(net_cache):
        c.i32(f"net_cache[{i}].object_ind")
        c.i32(f"net_cache[{i}].parent_id")
        c.i32(f"net_cache[{i}].cache_id")
        prop_count = c.count(f"net_cache[{i}].properties.count")
        net_cache_properties += prop_count
        c.skip(8 * prop_count, f"net_cache[{i}].properties")

    known_footer_end = c.pos
    residual = data[known_footer_end:content_end]
    return Result(
        path=str(path),
        content_end=content_end,
        network_end=network_end,
        footer_start=footer_start,
        known_footer_end=known_footer_end,
        residual_len=len(residual),
        residual_hex=residual[:64].hex(),
        debug_info=debug_info,
        tickmarks=tickmarks,
        packages=packages,
        objects=objects,
        names=names,
        class_indices=class_indices,
        net_cache=net_cache,
        net_cache_properties=net_cache_properties,
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

    historical = [scan(p) for p in historical_paths]
    corpus = [scan(p) for p in corpus_paths]

    print("R3.5 Known-Footer Residual Evidence")
    for row in historical:
        print(
            "historical "
            f"path={row.path} network_end={row.network_end} "
            f"known_footer_end={row.known_footer_end} content_end={row.content_end} "
            f"residual_len={row.residual_len} residual_hex={row.residual_hex} "
            f"debug={row.debug_info} tickmarks={row.tickmarks} packages={row.packages} "
            f"objects={row.objects} names={row.names} class_indices={row.class_indices} "
            f"net_cache={row.net_cache} net_cache_properties={row.net_cache_properties}"
        )

    length_counts = Counter(r.residual_len for r in corpus)
    hex_counts = Counter(r.residual_hex for r in corpus)
    print(f"largest_100_scanned={len(corpus)}")
    print("residual_length_counts=" + ",".join(f"{k}:{v}" for k, v in sorted(length_counts.items())))
    print("residual_hex_counts=" + ",".join(f"{k or '<empty>'}:{v}" for k, v in sorted(hex_counts.items())))
    print(f"residual_len_min={min(r.residual_len for r in corpus)}")
    print(f"residual_len_max={max(r.residual_len for r in corpus)}")
    print(f"known_footer_parsed=100/100")
    print("network_bits_decoded=false")
    print("crc_validated=false")
    print("residual_semantics_assigned=false")
    print("PASS: known footer structure parsed across 3 historical + 100 stress replays; residual bytes reported without interpretation.")


if __name__ == "__main__":
    main()
