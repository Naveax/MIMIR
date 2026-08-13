import hashlib
import json
import sys
from pathlib import Path

EXPECTED_STREAM_SHA = "ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba"
EXPECTED_ARTIFACT_DIGEST = "sha256:a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d"
EXPECTED_PRODUCTION_SHA = "bf4bccff82203ed049d33e942681fed07f23beb4"
EXPECTED_PRODUCTION_BLOB = "f64a5e0d66962f41026b2eb10e176219d4529931"
EXPECTED_ORACLE_ROWS = 169538
EXPECTED_REPLAYS = 47


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(cond: bool, message: str) -> None:
    if not cond:
        raise SystemExit(message)


def select(root: Path, artifact_dir: Path) -> None:
    paths_file = artifact_dir / "r3_15a_paths.txt"
    stream_file = artifact_dir / "r3_15a_new_actor_all.jsonl"
    summary_file = artifact_dir / "r3_15a_summary.json"
    aggregate_file = artifact_dir / "r3_15a_aggregate.txt"
    for required in (paths_file, stream_file, summary_file, aggregate_file):
        require(required.is_file(), f"missing artifact member: {required}")

    stream_sha = sha256_file(stream_file)
    require(stream_sha == EXPECTED_STREAM_SHA, f"full stream SHA-256 mismatch: {stream_sha}")

    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    require(summary.get("full_stream_sha256") == EXPECTED_STREAM_SHA, "summary full_stream_sha256 mismatch")
    require(summary.get("new_actor_total") == EXPECTED_ORACLE_ROWS, "summary new_actor_total mismatch")
    require(summary.get("replays_total") == EXPECTED_REPLAYS, "summary replays_total mismatch")
    require(summary.get("oracle_decode_success") == EXPECTED_REPLAYS, "summary oracle_decode_success mismatch")

    aggregate = aggregate_file.read_text(encoding="utf-8")
    require(f"new_actor_total={EXPECTED_ORACLE_ROWS}" in aggregate, "aggregate new_actor_total mismatch")
    require(f"full_stream_sha256={EXPECTED_STREAM_SHA}" in aggregate, "aggregate full stream SHA mismatch")

    paths = [line.strip().replace("\\", "/") for line in paths_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(len(paths) == EXPECTED_REPLAYS, f"expected 47 paths, got {len(paths)}")
    require(len(set(paths)) == EXPECTED_REPLAYS, "replay path list contains duplicates")

    selected = {}
    total_rows = 0
    with stream_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            total_rows += 1
            row = json.loads(line)
            if row.get("frame_index") == 0 and row.get("actor_ordinal") == 0:
                rel = str(row["relative_path"]).replace("\\", "/")
                require(rel not in selected, f"duplicate first-NewActor oracle row: {rel}")
                selected[rel] = row
    require(total_rows == EXPECTED_ORACLE_ROWS, f"full stream row count mismatch: {total_rows}")
    require(set(selected) == set(paths), "selected oracle identities do not equal path manifest")
    require(len(selected) == EXPECTED_REPLAYS, f"selected oracle row count mismatch: {len(selected)}")

    ordered = []
    identity_lines = []
    for rel in paths:
        replay = root / Path(rel)
        require(replay.is_file(), f"missing admitted replay: {rel}")
        digest = sha256_file(replay)
        row = selected[rel]
        expected = str(row["sha256"]).lower()
        require(digest.lower() == expected, f"replay SHA-256 mismatch: {rel}")
        ordered.append(row)
        identity_lines.append(f"{rel}\t{digest}\tPASS")

    Path("r3_15d_paths.txt").write_text("".join(f"{p}\n" for p in paths), encoding="utf-8")
    Path("r3_15d_oracle_first.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in ordered), encoding="utf-8"
    )
    Path("r3_15d_replay_identity.tsv").write_text("\n".join(identity_lines) + "\n", encoding="utf-8")
    lane_sha = sha256_file(Path("r3_15d_oracle_first.jsonl"))
    Path("r3_15d_oracle_lane_identity.txt").write_text(
        f"parent_artifact_id=9184200143\n"
        f"parent_artifact_digest={EXPECTED_ARTIFACT_DIGEST}\n"
        f"parent_full_stream_sha256={EXPECTED_STREAM_SHA}\n"
        f"parent_full_stream_rows={EXPECTED_ORACLE_ROWS}\n"
        f"selected_rows={EXPECTED_REPLAYS}\n"
        f"selected_lane_sha256={lane_sha}\n",
        encoding="utf-8",
    )
    print(f"R3_15D_ORACLE_SELECT=PASS rows=47 full_stream_rows={total_rows} identity=47/47 lane_sha256={lane_sha}")


def parse_bool(value: str):
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "null":
        return None
    raise ValueError(value)


def parse_int(value: str):
    return None if value == "null" else int(value)


def compare() -> None:
    oracle_rows = [json.loads(line) for line in Path("r3_15d_oracle_first.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    oracle = {row["relative_path"].replace("\\", "/"): row for row in oracle_rows}
    require(len(oracle) == EXPECTED_REPLAYS, f"oracle selected row count mismatch: {len(oracle)}")

    native = {}
    native_lines = Path("r3_15d_native.tsv").read_text(encoding="utf-8").splitlines()
    for line in native_lines:
        if not line.startswith("R3_15D_NATIVE\t"):
            continue
        fields = line.split("\t")
        require(len(fields) == 23, f"native field count mismatch: {len(fields)}")
        rel = fields[1].replace("\\", "/")
        require(rel not in native, f"duplicate native row: {rel}")
        native[rel] = {
            "actor_present": parse_bool(fields[2]),
            "actor_id": parse_int(fields[3]),
            "alive": parse_bool(fields[4]),
            "is_new": parse_bool(fields[5]),
            "envelope_stop": int(fields[6]),
            "name_id": int(fields[7]),
            "opaque": parse_bool(fields[8]),
            "object_id": int(fields[9]),
            "spawn_kind": fields[10],
            "location_present": parse_bool(fields[11]),
            "location_x": parse_int(fields[12]),
            "location_y": parse_int(fields[13]),
            "location_z": parse_int(fields[14]),
            "rotation_present": parse_bool(fields[15]),
            "yaw_present": parse_bool(fields[16]),
            "yaw": parse_int(fields[17]),
            "pitch_present": parse_bool(fields[18]),
            "pitch": parse_int(fields[19]),
            "roll_present": parse_bool(fields[20]),
            "roll": parse_int(fields[21]),
            "trajectory_stop": int(fields[22]),
        }

    require(len(native) == EXPECTED_REPLAYS, f"native success count mismatch: {len(native)}")
    require(set(native) == set(oracle), "native/oracle replay identity sets differ")

    spawn_map = {
        "none": "none",
        "location": "location",
        "location_rotation": "location_and_rotation",
    }
    gates = [
        "actor_present", "actor_id", "alive", "is_new", "envelope_stop", "name_id", "opaque",
        "object_id", "spawn_kind", "location_presence", "location_x", "location_y", "location_z",
        "rotation_presence", "yaw_presence", "yaw", "pitch_presence", "pitch", "roll_presence",
        "roll", "trajectory_stop",
    ]
    counts = {gate: 0 for gate in gates}
    comparisons = []
    mismatch_count = 0

    for row in oracle_rows:
        rel = row["relative_path"].replace("\\", "/")
        n = native[rel]
        checks = {
            "actor_present": n["actor_present"] is True,
            "actor_id": n["actor_id"] == row["actor_id"],
            "alive": n["alive"] is True,
            "is_new": n["is_new"] is True,
            "envelope_stop": n["envelope_stop"] == row["branch_start_bit"],
            "name_id": n["name_id"] == row["name_id_value"],
            "opaque": n["opaque"] == row["opaque_bit_value"],
            "object_id": n["object_id"] == row["object_id_value"],
            "spawn_kind": n["spawn_kind"] == spawn_map[row["oracle_spawn_kind"]],
            "location_presence": n["location_present"] == (row["location_start_bit"] is not None),
            "location_x": n["location_x"] == row["location_x_i32"],
            "location_y": n["location_y"] == row["location_y_i32"],
            "location_z": n["location_z"] == row["location_z_i32"],
            "rotation_presence": n["rotation_present"] == (row["rotation_start_bit"] is not None),
            "yaw_presence": n["yaw_present"] == row["yaw_present"],
            "yaw": n["yaw"] == row["yaw_i8"],
            "pitch_presence": n["pitch_present"] == row["pitch_present"],
            "pitch": n["pitch"] == row["pitch_i8"],
            "roll_presence": n["roll_present"] == row["roll_present"],
            "roll": n["roll"] == row["roll_i8"],
            "trajectory_stop": n["trajectory_stop"] == row["trajectory_end_bit"],
        }
        for gate, ok in checks.items():
            counts[gate] += int(ok)
        mismatches = [gate for gate, ok in checks.items() if not ok]
        mismatch_count += int(bool(mismatches))
        comparisons.append({
            "relative_path": rel,
            "sha256": row["sha256"],
            "oracle_spawn_kind": row["oracle_spawn_kind"],
            "native_spawn_kind": n["spawn_kind"],
            "oracle_branch_start_bit": row["branch_start_bit"],
            "native_envelope_stop_bit": n["envelope_stop"],
            "oracle_trajectory_end_bit": row["trajectory_end_bit"],
            "native_trajectory_stop_bit": n["trajectory_stop"],
            "mismatches": mismatches,
        })

    ok = mismatch_count == 0 and all(value == EXPECTED_REPLAYS for value in counts.values())
    summary = {
        "production_sha": EXPECTED_PRODUCTION_SHA,
        "production_source_blob": EXPECTED_PRODUCTION_BLOB,
        "oracle_artifact_id": 9184200143,
        "oracle_artifact_digest": EXPECTED_ARTIFACT_DIGEST,
        "oracle_full_stream_sha256": EXPECTED_STREAM_SHA,
        "oracle_full_stream_rows": EXPECTED_ORACLE_ROWS,
        "replays_total": EXPECTED_REPLAYS,
        "oracle_rows_selected": EXPECTED_REPLAYS,
        "native_success": len(native),
        "identity_error_count": 0,
        "native_error_count": 0,
        "mismatch_count": mismatch_count,
        "field_match_counts": counts,
        "outcome": "A" if ok else "B",
    }
    Path("r3_15d_comparisons.jsonl").write_text(
        "".join(json.dumps(item, sort_keys=True) + "\n" for item in comparisons), encoding="utf-8"
    )
    Path("r3_15d_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    aggregate = [
        "pass=R3.15D",
        f"production_sha={EXPECTED_PRODUCTION_SHA}",
        "replays_total=47",
        "oracle_rows_selected=47",
        "native_success=47",
        "identity_error_count=0",
        "native_error_count=0",
        f"mismatch_count={mismatch_count}",
    ]
    aggregate.extend(f"{gate}_match={counts[gate]}/47" for gate in gates)
    aggregate.append(f"R3_15D_OUTCOME={summary['outcome']}")
    aggregate.append("R3_15D_DIFFERENTIAL=" + ("PASS" if ok else "FAIL"))
    Path("r3_15d_aggregate.txt").write_text("\n".join(aggregate) + "\n", encoding="utf-8")
    print("\n".join(aggregate))
    require(ok, "R3.15D differential mismatch")


def main() -> None:
    require(len(sys.argv) >= 2, "usage: _tmp_r315d_exact.py select <root> <artifact-dir> | compare")
    command = sys.argv[1]
    if command == "select":
        require(len(sys.argv) == 4, "select requires <root> <artifact-dir>")
        select(Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
    elif command == "compare":
        require(len(sys.argv) == 2, "compare takes no extra arguments")
        compare()
    else:
        raise SystemExit(f"unknown command: {command}")


if __name__ == "__main__":
    main()
