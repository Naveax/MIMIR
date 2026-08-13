from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PARENT_STREAM_SHA = "ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba"
PARENT_ROWS = 169538
REPLAYS = 47


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(cond: bool, message: str) -> None:
    if not cond:
        raise SystemExit(message)


def marker(line: str, prefix: str) -> dict[str, str]:
    parts = line.rstrip("\n").split("\t")
    require(bool(parts) and parts[0] == prefix, f"bad marker prefix: {line[:100]!r}")
    out: dict[str, str] = {}
    for item in parts[1:]:
        key, sep, value = item.partition("=")
        require(bool(sep) and bool(key) and key not in out, f"bad marker field: {item!r}")
        out[key] = value
    return out


def norm(value: str) -> str:
    return value.replace("\\", "/")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--artifact", required=True)
    ap.add_argument("--log", required=True)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    artifact = Path(args.artifact).resolve()
    log = Path(args.log).resolve()
    paths_file = artifact / "r3_15a_paths.txt"
    parent_stream = artifact / "r3_15a_new_actor_all.jsonl"

    require(paths_file.is_file(), f"missing {paths_file}")
    require(parent_stream.is_file(), f"missing {parent_stream}")
    require(sha256_file(parent_stream) == PARENT_STREAM_SHA, "R3.15A parent stream SHA-256 mismatch")

    parent_first: dict[str, dict] = {}
    parent_rows = 0
    with parent_stream.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            parent_rows += 1
            row = json.loads(line)
            if row.get("frame_index") == 0 and row.get("actor_ordinal") == 0:
                rel = norm(str(row["relative_path"]))
                require(rel not in parent_first, f"duplicate parent identity: {rel}")
                parent_first[rel] = row
    require(parent_rows == PARENT_ROWS, f"parent row count mismatch: {parent_rows}")

    paths = [norm(x.strip()) for x in paths_file.read_text(encoding="utf-8").splitlines() if x.strip()]
    require(len(paths) == REPLAYS and len(set(paths)) == REPLAYS, f"selector identity count mismatch: {len(paths)}")
    require(set(parent_first) == set(paths), "parent first-row identities differ from selector")

    identity_lines: list[str] = []
    for rel in paths:
        replay = root / rel
        require(replay.is_file(), f"missing replay: {rel}")
        digest = sha256_file(replay)
        expected = str(parent_first[rel]["sha256"]).lower()
        require(digest.lower() == expected, f"replay SHA-256 mismatch: {rel}")
        identity_lines.append(f"{rel}\t{digest}\tPASS")

    oracle: dict[str, dict[str, str]] = {}
    parsed: set[str] = set()
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("R3_16A_PROPERTY\t"):
            row = marker(line, "R3_16A_PROPERTY")
            rel = norm(row["label"])
            require(rel in set(paths), f"unexpected oracle replay: {rel}")
            require(rel not in oracle, f"multiple candidates emitted for: {rel}")
            oracle[rel] = row
        elif line.startswith("R3_16A_PARSE\t"):
            parts = line.split("\t", 1)
            require(len(parts) == 2 and bool(parts[1]), f"bad parse marker: {line!r}")
            parsed.add(norm(parts[1]))

    require(parsed == set(paths), f"oracle parse-success identity mismatch: {len(parsed)}/47")
    require(set(oracle) == set(paths), f"candidate identity mismatch: {len(oracle)}/47")

    required = [
        "frame_index", "actor_ordinal", "frame_time_raw_bits", "frame_delta_raw_bits",
        "actor_id", "actor_context_object_id", "actor_context_object_name", "new_bit_end",
        "property_present_start_bit", "property_present_end_bit", "property_present_value",
        "stream_id_start_bit", "stream_id_end_bit", "stream_id_value", "stream_id_bound",
        "prop_id_bits", "resolved_property_object_id", "resolved_property_object_name",
        "resolved_attribute_tag", "payload_start_bit",
    ]
    selected: list[dict] = []
    requests: list[str] = []
    for rel in paths:
        row = oracle[rel]
        for key in required:
            require(key in row, f"{rel}: missing field {key}")
        require(row["property_present_value"] == "true", f"{rel}: selected property_present != true")
        item = {
            "relative_path": rel,
            "replay_sha256": parent_first[rel]["sha256"],
            "frame_index": int(row["frame_index"]),
            "actor_ordinal": int(row["actor_ordinal"]),
            "frame_time_raw_bits": int(row["frame_time_raw_bits"]),
            "frame_delta_raw_bits": int(row["frame_delta_raw_bits"]),
            "actor_id": int(row["actor_id"]),
            "actor_context_object_id": int(row["actor_context_object_id"]),
            "actor_context_object_name": row["actor_context_object_name"],
            "new_bit_end": int(row["new_bit_end"]),
            "property_present_start_bit": int(row["property_present_start_bit"]),
            "property_present_end_bit": int(row["property_present_end_bit"]),
            "property_present_value": True,
            "stream_id_start_bit": int(row["stream_id_start_bit"]),
            "stream_id_end_bit": int(row["stream_id_end_bit"]),
            "stream_id_value": int(row["stream_id_value"]),
            "stream_id_bound": int(row["stream_id_bound"]),
            "prop_id_bits": int(row["prop_id_bits"]),
            "resolved_property_object_id": int(row["resolved_property_object_id"]),
            "resolved_property_object_name": row["resolved_property_object_name"],
            "resolved_attribute_tag": row["resolved_attribute_tag"],
            "payload_start_bit": int(row["payload_start_bit"]),
        }
        selected.append(item)
        requests.append(f"{rel}\t{item['actor_context_object_id']}\t{item['stream_id_value']}")

    Path("r3_16a_replay_identity.tsv").write_text("\n".join(identity_lines) + "\n", encoding="utf-8")
    Path("r3_16a_paths.txt").write_text("".join(f"{rel}\n" for rel in paths), encoding="utf-8")
    Path("r3_16a_first_property.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in selected),
        encoding="utf-8",
    )
    Path("r3_16a_mimir_requests.tsv").write_text("\n".join(requests) + "\n", encoding="utf-8")
    lane_sha = sha256_file(Path("r3_16a_first_property.jsonl"))
    print(
        f"R3_16A_SELECT=PASS replays=47 candidates=47 parent_rows={parent_rows} "
        f"identity=47/47 lane_sha256={lane_sha}"
    )


if __name__ == "__main__":
    main()
