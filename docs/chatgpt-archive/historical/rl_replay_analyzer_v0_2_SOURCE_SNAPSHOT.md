# SOURCE SNAPSHOT — rl_replay_analyzer_v0_2.py

**Source class:** CURATED_SOURCE_SNAPSHOT
**File Library file:** `rl_replay_analyzer_v0_2.py`
**Created:** 2026-05-20
**Recorded size:** 47,567 bytes
**Purpose:** Historical pre-MIMIR Rocket League replay analyzer / coach prototype.

## Verified source facts

The original source contains:
- UE-style string/property decoding;
- `parse_replay_header`;
- `parse_replay_body`;
- SHA-256 helper;
- levels and keyframe parsing;
- network stream extraction as raw bytes/hash/length;
- footer/tick/package/object/name/class parsing;
- scoreboard/goal timeline analysis;
- event-window generation;
- coaching summary/report generation.

## Important capability boundary

The historical V0.2 analyzer intentionally did **not** claim native network-frame physics decode.
Its own README says car/ball coordinates, boost, velocity/rotation, jump/dodge/input and exact time-to-ball were outside V0.2.

## Key code fragment recovered from File Library

```python
def parse_replay_body(path: Path, header: Dict[str, Any]) -> Dict[str, Any]:
    data = path.read_bytes()
    start = int(header["properties_end_offset"])
    b = Bin(data, start)
    body_size = b.u32()
    body_crc = b.u32()
    body_payload_start = b.off

    levels = []
    level_count = b.i32()
    for _ in range(level_count):
        levels.append(b.string())

    keyframes = []
    keyframe_count = b.i32()
    for idx in range(keyframe_count):
        keyframes.append({
            "index": idx,
            "time_seconds": b.f32(),
            "frame": b.u32(),
            "byte_position": b.u32(),
        })
```

## Relation to current Rust MIMIR

Use as:
- historical parser oracle candidate;
- regression idea source;
- migration candidate.

Do **not** use as:
- current production source of truth;
- native Rust decoder implementation;
- evidence that current MIMIR already performs the same semantics.

The original raw file should be recovered/imported exactly in a future private migration pass if direct byte access becomes available.
