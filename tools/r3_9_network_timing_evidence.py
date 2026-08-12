from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import math
import struct

MAX_LIST = 25_000
MAX_TEXT_UNITS = 10_000
TARGET_KEYS = {
    "NumFrames",
    "MaxChannels",
    "MatchType",
    "ReplayVersion",
    "BuildVersion",
}


class ScanError(RuntimeError):
    pass


class Cursor:
    def __init__(self, data: bytes, start: int = 0, end: int | None = None) -> None:
        self.data = data
        self.pos = start
        self.end = len(data) if end is None else end

    def require(self, size: int, field: str) -> None:
        if size < 0:
            raise ScanError(f"negative size for {field}: {size}")
        if self.pos + size > self.end:
            raise ScanError(
                f"truncated {field}: pos={self.pos} need={size} end={self.end}"
            )

    def take(self, size: int, field: str) -> bytes:
        self.require(size, field)
        start = self.pos
        self.pos += size
        return self.data[start:self.pos]

    def skip(self, size: int, field: str) -> None:
        self.take(size, field)

    def i32(self, field: str) -> int:
        return struct.unpack("<i", self.take(4, field))[0]

    def u32(self, field: str) -> int:
        return struct.unpack("<I", self.take(4, field))[0]

    def f32(self, field: str) -> float:
        return struct.unpack("<f", self.take(4, field))[0]

    def raw_utf8_nul(self, field: str) -> str:
        size = self.i32(f"{field}.length")
        if size <= 0 or size > MAX_TEXT_UNITS:
            raise ScanError(f"raw string length out of bounds for {field}: {size}")
        raw = self.take(size, field)
        if not raw.endswith(b"\x00"):
            raise ScanError(f"raw string missing NUL for {field}")
        try:
            return raw[:-1].decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ScanError(f"raw string is not UTF-8 for {field}: {exc}") from exc

    def unreal_text(self, field: str) -> str:
        units = self.i32(f"{field}.length")
        if units < -MAX_TEXT_UNITS or units > MAX_TEXT_UNITS:
            raise ScanError(f"text length out of bounds for {field}: {units}")
        if units == 0:
            return ""
        if units < 0:
            raw = self.take((-units) * 2, field)
            if not raw.endswith(b"\x00\x00"):
                raise ScanError(f"UTF-16 text missing NUL for {field}")
            try:
                return raw[:-2].decode("utf-16-le", errors="strict")
            except UnicodeDecodeError as exc:
                raise ScanError(f"invalid UTF-16 for {field}: {exc}") from exc
        raw = self.take(units, field)
        if not raw.endswith(b"\x00"):
            raise ScanError(f"Windows-1252 text missing NUL for {field}")
        try:
            return raw[:-1].decode("cp1252", errors="strict")
        except UnicodeDecodeError as exc:
            raise ScanError(f"invalid Windows-1252 for {field}: {exc}") from exc

    def count(self, field: str) -> int:
        value = self.i32(field)
        if value < 0:
            raise ScanError(f"negative count for {field}: {value}")
        if value > MAX_LIST:
            raise ScanError(f"count too large for {field}: {value}")
        return value


@dataclass(frozen=True)
class HeaderObservation:
    major: int
    minor: int
    net: int
    game_type: str
    replay_version: int | None
    build_version: str | None
    num_frames: int | None
    max_channels: int | None
    match_type: str | None
    header_end: int


@dataclass(frozen=True)
class Evidence:
    path: str
    header: HeaderObservation
    content_size: int
    network_start: int
    network_size: int
    first_time: float
    first_delta: float
    channel_bits: int
    used_max_channels_fallback: bool
    parse_name_id_branch: bool
    trailer_u32_branch: bool


def parse_property_value(key: str, kind: str, value: bytes) -> object:
    c = Cursor(value)
    if key in {"NumFrames", "MaxChannels", "ReplayVersion"}:
        if kind != "IntProperty" or len(value) != 4:
            raise ScanError(
                f"target {key} expected IntProperty/4 bytes, got {kind}/{len(value)}"
            )
        result = c.i32(f"{key}.value")
    elif key == "BuildVersion":
        if kind != "StrProperty":
            raise ScanError(f"target BuildVersion expected StrProperty, got {kind}")
        result = c.unreal_text("BuildVersion.value")
    elif key == "MatchType":
        if kind != "NameProperty":
            raise ScanError(f"target MatchType expected NameProperty, got {kind}")
        result = c.unreal_text("MatchType.value")
    else:
        raise AssertionError(key)
    if c.pos != c.end:
        raise ScanError(
            f"target {key} did not consume property value: pos={c.pos} end={c.end}"
        )
    return result


def parse_header(data: bytes) -> HeaderObservation:
    outer = Cursor(data)
    header_size = outer.i32("header_size")
    outer.u32("header_crc")
    if header_size < 0:
        raise ScanError(f"negative header_size: {header_size}")
    header_start = outer.pos
    header_end = header_start + header_size
    if header_end > len(data):
        raise ScanError(
            f"header_end beyond file: header_end={header_end} file={len(data)}"
        )

    c = Cursor(data, header_start, header_end)
    major = c.i32("major_version")
    minor = c.i32("minor_version")
    net = c.i32("net_version")
    game_type = c.unreal_text("game_type")

    targets: dict[str, object] = {}
    seen: set[str] = set()
    while c.pos < c.end:
        key = c.raw_utf8_nul("property.key")
        if key == "None":
            break
        if key in seen:
            raise ScanError(f"duplicate top-level property: {key}")
        seen.add(key)
        kind = c.raw_utf8_nul(f"property[{key}].kind")
        size = c.u32(f"property[{key}].size")
        c.u32(f"property[{key}].ignored")

        if kind == "BoolProperty":
            if size != 0:
                raise ScanError(
                    f"BoolProperty {key} declared size {size}, expected zero"
                )
            value = c.take(1, f"property[{key}].bool")
            if value[0] not in (0, 1):
                raise ScanError(f"BoolProperty {key} invalid value {value[0]}")
            if key in TARGET_KEYS:
                raise ScanError(f"target property {key} unexpectedly BoolProperty")
            continue

        value = c.take(size, f"property[{key}].value")
        if key in TARGET_KEYS:
            targets[key] = parse_property_value(key, kind, value)
    else:
        raise ScanError("missing top-level None terminator")

    if c.pos != c.end:
        raise ScanError(f"header terminator offset mismatch: pos={c.pos} end={c.end}")

    def opt_int(key: str) -> int | None:
        value = targets.get(key)
        return None if value is None else int(value)

    def opt_str(key: str) -> str | None:
        value = targets.get(key)
        return None if value is None else str(value)

    return HeaderObservation(
        major=major,
        minor=minor,
        net=net,
        game_type=game_type,
        replay_version=opt_int("ReplayVersion"),
        build_version=opt_str("BuildVersion"),
        num_frames=opt_int("NumFrames"),
        max_channels=opt_int("MaxChannels"),
        match_type=opt_str("MatchType"),
        header_end=header_end,
    )


def parse_network_boundary(data: bytes, header: HeaderObservation) -> tuple[int, int, int]:
    c = Cursor(data, header.header_end, len(data))
    content_size = c.i32("content_size")
    c.u32("content_crc")
    if content_size < 0:
        raise ScanError(f"negative content_size: {content_size}")
    content_start = c.pos
    content_end = content_start + content_size
    if content_end != len(data):
        raise ScanError(
            f"content framing mismatch: content_end={content_end} file={len(data)}"
        )

    levels = c.count("levels.count")
    for index in range(levels):
        c.unreal_text(f"levels[{index}]")
    keyframes = c.count("keyframes.count")
    c.skip(12 * keyframes, "keyframes.data")
    network_size = c.i32("network_size")
    if network_size < 0:
        raise ScanError(f"negative network_size: {network_size}")
    network_start = c.pos
    if network_start + network_size > content_end:
        raise ScanError(
            f"network beyond content: start={network_start} size={network_size} end={content_end}"
        )
    return content_size, network_start, network_size


def version_ge(header: HeaderObservation, target: tuple[int, int, int]) -> bool:
    return (header.major, header.minor, header.net) >= target


def bit_width(value: int) -> int:
    if value < 0:
        raise ScanError(f"negative max channel value: {value}")
    return value.bit_length()


def scan(path: Path) -> Evidence:
    data = path.read_bytes()
    header = parse_header(data)
    content_size, network_start, network_size = parse_network_boundary(data, header)
    if network_size < 8:
        raise ScanError(f"network payload shorter than first frame timing pair: {network_size}")
    first_time, first_delta = struct.unpack_from("<ff", data, network_start)

    max_channels = header.max_channels if header.max_channels is not None else 1023
    if max_channels < 0:
        raise ScanError(f"negative MaxChannels: {max_channels}")
    channel_bits = max(bit_width(max_channels) - 1, 0)
    is_lan = header.match_type == "Lan"
    parse_name_id_branch = version_ge(header, (868, 20, 0)) or (
        version_ge(header, (868, 14, 0)) and not is_lan
    )
    trailer_u32_branch = version_ge(header, (868, 24, 10))

    return Evidence(
        path=str(path),
        header=header,
        content_size=content_size,
        network_start=network_start,
        network_size=network_size,
        first_time=first_time,
        first_delta=first_delta,
        channel_bits=channel_bits,
        used_max_channels_fallback=header.max_channels is None,
        parse_name_id_branch=parse_name_id_branch,
        trailer_u32_branch=trailer_u32_branch,
    )


def timing_invalid(value: float) -> bool:
    return (not math.isfinite(value)) or value < 0.0 or (0.0 < value < 1e-10)


def summarize(label: str, rows: list[Evidence]) -> None:
    print(f"{label}_parsed={len(rows)}")
    print(
        f"{label}_first_time_invalid={sum(timing_invalid(row.first_time) for row in rows)}"
    )
    print(
        f"{label}_first_delta_invalid={sum(timing_invalid(row.first_delta) for row in rows)}"
    )
    print(
        f"{label}_first_zero_zero={sum(row.first_time == 0.0 and row.first_delta == 0.0 for row in rows)}"
    )
    print(f"{label}_first_time_min={min(row.first_time for row in rows):.9g}")
    print(f"{label}_first_time_max={max(row.first_time for row in rows):.9g}")
    print(f"{label}_first_delta_min={min(row.first_delta for row in rows):.9g}")
    print(f"{label}_first_delta_max={max(row.first_delta for row in rows):.9g}")
    print(f"{label}_network_size_min={min(row.network_size for row in rows)}")
    print(f"{label}_network_size_max={max(row.network_size for row in rows)}")
    print(
        f"{label}_num_frames_missing={sum(row.header.num_frames is None for row in rows)}"
    )
    print(
        f"{label}_max_channels_missing={sum(row.header.max_channels is None for row in rows)}"
    )
    print(
        f"{label}_match_type_missing={sum(row.header.match_type is None for row in rows)}"
    )
    print(
        f"{label}_build_version_missing={sum(row.header.build_version is None for row in rows)}"
    )
    print(
        f"{label}_replay_version_missing={sum(row.header.replay_version is None for row in rows)}"
    )
    print(
        f"{label}_num_frames_gt_network_size={sum(row.header.num_frames is not None and row.header.num_frames > row.network_size for row in rows)}"
    )
    print(
        f"{label}_max_channels_fallback_1023={sum(row.used_max_channels_fallback for row in rows)}"
    )
    print(
        f"{label}_parse_name_id_branch={sum(row.parse_name_id_branch for row in rows)}"
    )
    print(
        f"{label}_trailer_u32_branch={sum(row.trailer_u32_branch for row in rows)}"
    )
    channel_counts = Counter(row.channel_bits for row in rows)
    print(
        f"{label}_channel_bits="
        + ",".join(f"{bits}:{count}" for bits, count in sorted(channel_counts.items()))
    )
    version_counts = Counter(
        (row.header.major, row.header.minor, row.header.net) for row in rows
    )
    print(
        f"{label}_version_triplets="
        + ",".join(
            f"{major}.{minor}.{net}:{count}"
            for (major, minor, net), count in sorted(version_counts.items())
        )
    )
    match_counts = Counter(row.header.match_type or "<missing>" for row in rows)
    print(
        f"{label}_match_types="
        + ",".join(f"{name}:{count}" for name, count in sorted(match_counts.items()))
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

    print("R3.9 Replay Network Timing + Decoder Preconditions Evidence")
    summarize("historical", historical)
    summarize("largest_100", corpus)
    summarize("all_103", all_rows)

    anomalies: list[tuple[Evidence, list[str]]] = []
    for row in all_rows:
        reasons: list[str] = []
        if timing_invalid(row.first_time):
            reasons.append("invalid_first_time")
        if timing_invalid(row.first_delta):
            reasons.append("invalid_first_delta")
        if row.first_time == 0.0 and row.first_delta == 0.0:
            reasons.append("first_frame_is_terminal")
        if row.header.num_frames is None:
            reasons.append("missing_num_frames")
        elif row.header.num_frames > row.network_size:
            reasons.append("num_frames_gt_network_size")
        if row.header.max_channels is not None and row.header.max_channels < 0:
            reasons.append("negative_max_channels")
        if row.header.replay_version is None:
            reasons.append("missing_replay_version")
        if row.header.build_version is None:
            reasons.append("missing_build_version")
        if reasons:
            anomalies.append((row, reasons))

    print(f"rows_with_precondition_anomalies={len(anomalies)}")
    for row, reasons in anomalies[:30]:
        print(
            "anomaly "
            f"path={row.path} reasons={','.join(reasons)} "
            f"version={row.header.major}.{row.header.minor}.{row.header.net} "
            f"replay_version={row.header.replay_version} build={row.header.build_version} "
            f"num_frames={row.header.num_frames} max_channels={row.header.max_channels} "
            f"match_type={row.header.match_type} network_size={row.network_size} "
            f"first_time={row.first_time:.9g} first_delta={row.first_delta:.9g} "
            f"channel_bits={row.channel_bits}"
        )

    print("first_frame_actor_bits_decoded=false")
    print("network_frame_iteration=false")
    print("attribute_decode=false")
    print("raw_state_decode=false")
    print("crc_validated=false")

    hard = [
        (row, reasons)
        for row, reasons in anomalies
        if any(
            reason
            in {
                "invalid_first_time",
                "invalid_first_delta",
                "first_frame_is_terminal",
                "missing_num_frames",
                "num_frames_gt_network_size",
                "negative_max_channels",
                "missing_replay_version",
                "missing_build_version",
            }
            for reason in reasons
        )
    ]
    if hard:
        print(f"HARD_PRECONDITION_ANOMALIES={len(hard)}")
    else:
        print("HARD_PRECONDITION_ANOMALIES=0")
    print(
        "PASS: first-frame timing bytes and decoder preconditions observed across 3 historical + 100 stress replays without decoding actor bits."
    )


if __name__ == "__main__":
    main()
