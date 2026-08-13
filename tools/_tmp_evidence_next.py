from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

BOXCARS_SHA = "c70e77df7af81b436cb545d070bb90c82f562d0b"
FRAME_BLOB = "6f2ff153d3a27cdacccc65e3f23851489077a7d8"
MODELS_BLOB = "73c73991379aeb79dcee49ea31c417141ba3c1a6"
R3_14A_ARTIFACT_SHA256 = "d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one source match, found {count}")
    return text.replace(old, new, 1)


def patch_boxcars(root: Path) -> None:
    frame = root / "src/network/frame_decoder.rs"
    text = frame.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "use fnv::FnvHashMap;\n",
        "use fnv::FnvHashMap;\nuse std::fmt::Display;\n",
        "display import",
    )
    text = replace_once(
        text,
        "    ActorId, Frame, NewActor, ObjectId, SpawnTrajectory, StreamId, Trajectory, UpdatedAttribute,\n",
        "    ActorId, Frame, NewActor, ObjectId, Rotation, SpawnTrajectory, StreamId, Trajectory,\n    UpdatedAttribute, Vector3i,\n",
        "trajectory imports",
    )

    marker = "#[derive(Debug)]\nenum DecodedFrame {"
    helper = r'''fn r3_15a_offset(bits: &LittleEndianReader<'_>, total_bits: usize) -> usize {
    total_bits
        - bits
            .bits_remaining()
            .expect("R3.15A instrumentation requires bounded network bits")
}

fn r3_15a_optional<T: Display>(value: Option<T>) -> String {
    value
        .map(|value| value.to_string())
        .unwrap_or_else(|| "null".to_owned())
}

fn r3_15a_bool(value: bool) -> &'static str {
    if value { "true" } else { "false" }
}

fn r3_15a_label() -> String {
    std::env::var("MIMIR_R3_15A_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\t', "_")
        .replace('\r', "_")
        .replace('\n', "_")
}

'''
    text = replace_once(text, marker, helper + marker, "helper insertion")

    original = r'''    fn parse_new_actor(
        &self,
        bits: &mut LittleEndianReader<'_>,
        actor_id: ActorId,
    ) -> Result<NewActor, FrameError> {
        let component = "New Actor";
        let mut name_id = None;
        let do_parse_name = self.version >= VersionTriplet(868, 20, 0)
            || (self.version >= VersionTriplet(868, 14, 0) && !self.is_lan);
        if do_parse_name {
            name_id = bits
                .read_i32()
                .ok_or(FrameError::NotEnoughDataFor(component))
                .map(Some)?;
        }

        let _ = bits
            .read_bit()
            .ok_or(FrameError::NotEnoughDataFor(component))?;
        let object_id = bits
            .read_i32()
            .map(ObjectId)
            .ok_or(FrameError::NotEnoughDataFor(component))?;
        let spawn = self
            .spawns
            .get(usize::from(object_id))
            .ok_or(FrameError::ObjectIdOutOfRange { obj: object_id })?;

        let traj = Trajectory::from_spawn(bits, *spawn, self.version.net_version())
            .ok_or(FrameError::NotEnoughDataFor(component))?;
        Ok(NewActor {
            actor_id,
            name_id,
            object_id,
            initial_trajectory: traj,
        })
    }
'''
    instrumented = r'''    fn parse_new_actor(
        &self,
        bits: &mut LittleEndianReader<'_>,
        actor_id: ActorId,
        frame_index: usize,
        actor_ordinal: usize,
    ) -> Result<NewActor, FrameError> {
        let component = "New Actor";
        let total_bits = self.body.network_data.len() * 8;
        let branch_start_bit = r3_15a_offset(bits, total_bits);
        let new_bit_end = branch_start_bit;

        let mut name_id = None;
        let do_parse_name = self.version >= VersionTriplet(868, 20, 0)
            || (self.version >= VersionTriplet(868, 14, 0) && !self.is_lan);
        let name_id_start_bit = if do_parse_name {
            Some(r3_15a_offset(bits, total_bits))
        } else {
            None
        };
        if do_parse_name {
            name_id = bits
                .read_i32()
                .ok_or(FrameError::NotEnoughDataFor(component))
                .map(Some)?;
        }
        let name_id_end_bit = if do_parse_name {
            Some(r3_15a_offset(bits, total_bits))
        } else {
            None
        };

        let opaque_bit_start = r3_15a_offset(bits, total_bits);
        let opaque_bit = bits
            .read_bit()
            .ok_or(FrameError::NotEnoughDataFor(component))?;
        let opaque_bit_end = r3_15a_offset(bits, total_bits);

        let object_id_start_bit = r3_15a_offset(bits, total_bits);
        let object_id = bits
            .read_i32()
            .map(ObjectId)
            .ok_or(FrameError::NotEnoughDataFor(component))?;
        let object_id_end_bit = r3_15a_offset(bits, total_bits);
        let object_index = usize::from(object_id);
        let spawn = self
            .spawns
            .get(object_index)
            .ok_or(FrameError::ObjectIdOutOfRange { obj: object_id })?;
        let object_name = self
            .body
            .objects
            .get(object_index)
            .map(String::as_str)
            .unwrap_or("<out-of-range>")
            .replace('\t', "_")
            .replace('\r', "_")
            .replace('\n', "_");

        let trajectory_start_bit = r3_15a_offset(bits, total_bits);
        let mut location_start_bit = None;
        let mut location_end_bit = None;
        let mut rotation_start_bit = None;
        let mut rotation_end_bit = None;

        let traj = match *spawn {
            SpawnTrajectory::None => Trajectory {
                location: None,
                rotation: None,
            },
            SpawnTrajectory::Location => {
                location_start_bit = Some(r3_15a_offset(bits, total_bits));
                let location = Vector3i::decode(bits, self.version.net_version())
                    .ok_or(FrameError::NotEnoughDataFor(component))?;
                location_end_bit = Some(r3_15a_offset(bits, total_bits));
                Trajectory {
                    location: Some(location),
                    rotation: None,
                }
            }
            SpawnTrajectory::LocationAndRotation => {
                location_start_bit = Some(r3_15a_offset(bits, total_bits));
                let location = Vector3i::decode(bits, self.version.net_version())
                    .ok_or(FrameError::NotEnoughDataFor(component))?;
                location_end_bit = Some(r3_15a_offset(bits, total_bits));
                rotation_start_bit = Some(r3_15a_offset(bits, total_bits));
                let rotation = Rotation::decode(bits)
                    .ok_or(FrameError::NotEnoughDataFor(component))?;
                rotation_end_bit = Some(r3_15a_offset(bits, total_bits));
                Trajectory {
                    location: Some(location),
                    rotation: Some(rotation),
                }
            }
        };
        let trajectory_end_bit = r3_15a_offset(bits, total_bits);
        let branch_end_bit = trajectory_end_bit;

        let spawn_name = match *spawn {
            SpawnTrajectory::None => "none",
            SpawnTrajectory::Location => "location",
            SpawnTrajectory::LocationAndRotation => "location_rotation",
        };
        let location = traj.location;
        let rotation = traj.rotation;
        println!(
            "R3_15A_NEWACTOR\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tnew_bit_end={}\tbranch_start_bit={}\tversion_major={}\tversion_minor={}\tnet_version={}\tis_lan={}\tdo_parse_name={}\tname_id_present={}\tname_id_value={}\tname_id_start_bit={}\tname_id_end_bit={}\topaque_bit_value={}\topaque_bit_start={}\topaque_bit_end={}\tobject_id_value={}\tobject_id_start_bit={}\tobject_id_end_bit={}\tobject_table_length={}\tobject_id_in_range=true\tobject_name={}\toracle_spawn_kind={}\ttrajectory_start_bit={}\ttrajectory_end_bit={}\tlocation_start_bit={}\tlocation_end_bit={}\tlocation_x_i32={}\tlocation_y_i32={}\tlocation_z_i32={}\trotation_start_bit={}\trotation_end_bit={}\tyaw_present={}\tyaw_i8={}\tpitch_present={}\tpitch_i8={}\troll_present={}\troll_i8={}\tbranch_end_bit={}\tbranch_bit_length={}",
            r3_15a_label(),
            frame_index,
            actor_ordinal,
            actor_id.0,
            new_bit_end,
            branch_start_bit,
            self.version.0,
            self.version.1,
            self.version.2,
            r3_15a_bool(self.is_lan),
            r3_15a_bool(do_parse_name),
            r3_15a_bool(name_id.is_some()),
            r3_15a_optional(name_id),
            r3_15a_optional(name_id_start_bit),
            r3_15a_optional(name_id_end_bit),
            r3_15a_bool(opaque_bit),
            opaque_bit_start,
            opaque_bit_end,
            object_id.0,
            object_id_start_bit,
            object_id_end_bit,
            self.body.objects.len(),
            object_name,
            spawn_name,
            trajectory_start_bit,
            trajectory_end_bit,
            r3_15a_optional(location_start_bit),
            r3_15a_optional(location_end_bit),
            r3_15a_optional(location.map(|value| value.x)),
            r3_15a_optional(location.map(|value| value.y)),
            r3_15a_optional(location.map(|value| value.z)),
            r3_15a_optional(rotation_start_bit),
            r3_15a_optional(rotation_end_bit),
            r3_15a_bool(rotation.and_then(|value| value.yaw).is_some()),
            r3_15a_optional(rotation.and_then(|value| value.yaw)),
            r3_15a_bool(rotation.and_then(|value| value.pitch).is_some()),
            r3_15a_optional(rotation.and_then(|value| value.pitch)),
            r3_15a_bool(rotation.and_then(|value| value.roll).is_some()),
            r3_15a_optional(rotation.and_then(|value| value.roll)),
            branch_end_bit,
            branch_end_bit.saturating_sub(branch_start_bit),
        );

        Ok(NewActor {
            actor_id,
            name_id,
            object_id,
            initial_trajectory: traj,
        })
    }
'''
    text = replace_once(text, original, instrumented, "parse_new_actor instrumentation")

    text = replace_once(
        text,
        "        updated_actors: &mut Vec<UpdatedAttribute>,\n    ) -> Result<DecodedFrame, FrameError> {",
        "        updated_actors: &mut Vec<UpdatedAttribute>,\n        frame_index: usize,\n    ) -> Result<DecodedFrame, FrameError> {",
        "decode_frame frame index argument",
    )
    text = replace_once(
        text,
        "        while bits\n            .read_bit()\n            .ok_or(FrameError::NotEnoughDataFor(\"Actor data\"))?\n        {",
        "        let mut r3_15a_actor_ordinal = 0usize;\n        while bits\n            .read_bit()\n            .ok_or(FrameError::NotEnoughDataFor(\"Actor data\"))?\n        {\n            let r3_15a_current_actor_ordinal = r3_15a_actor_ordinal;\n            r3_15a_actor_ordinal += 1;",
        "actor ordinal instrumentation",
    )
    text = replace_once(
        text,
        "                    let actor = self.parse_new_actor(bits, actor_id)?;",
        "                    let actor = self.parse_new_actor(\n                        bits,\n                        actor_id,\n                        frame_index,\n                        r3_15a_current_actor_ordinal,\n                    )?;",
        "parse_new_actor call",
    )
    text = replace_once(
        text,
        "                    &mut updated_actors,\n                )",
        "                    &mut updated_actors,\n                    frames.len(),\n                )",
        "decode_frame call",
    )
    frame.write_text(text, encoding="utf-8", newline="\n")

    example_dir = root / "examples"
    example_dir.mkdir(exist_ok=True)
    example = r'''use boxcars::ParserBuilder;
use std::error::Error;
use std::fs;
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args_os().skip(1);
    let replay_path = PathBuf::from(args.next().ok_or("missing replay path")?);
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }
    let bytes = fs::read(&replay_path)?;
    let _replay = ParserBuilder::new(&bytes).must_parse_network_data().parse()?;
    println!("R3_15A_ORACLE_PARSE=PASS");
    Ok(())
}
'''
    (example_dir / "r3_15a_probe.rs").write_text(example, encoding="utf-8", newline="\n")


def write_mimir_example(root: Path) -> None:
    path = root / "crates/mimir-replay/examples/_tmp_evidence_plan.rs"
    path.parent.mkdir(parents=True, exist_ok=True)
    source = r'''use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkLookupPlanReader,
    ReplayNetworkSpawnTrajectoryV1,
};
use std::error::Error;
use std::fs;
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args_os().skip(1);
    let replay_path = PathBuf::from(args.next().ok_or("missing replay path")?);
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }
    let bytes = fs::read(&replay_path)?;
    let label = replay_path.to_string_lossy().into_owned();
    let input = ReplayInput::Memory { label: label.clone(), bytes };
    let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;
    for (object_id, spawn) in plan.spawn_trajectories.iter().enumerate() {
        let kind = match spawn {
            ReplayNetworkSpawnTrajectoryV1::None => "none",
            ReplayNetworkSpawnTrajectoryV1::Location => "location",
            ReplayNetworkSpawnTrajectoryV1::LocationAndRotation => "location_rotation",
        };
        println!("R3_15A_MIMIR_SPAWN\tlabel={}\tobject_id={}\tspawn={}", label, object_id, kind);
    }
    println!("R3_15A_MIMIR_PLAN=PASS");
    Ok(())
}
'''
    path.write_text(source, encoding="utf-8", newline="\n")


def parse_tsv_line(line: str, prefix: str) -> dict[str, str]:
    parts = line.rstrip("\n").split("\t")
    if not parts or parts[0] != prefix:
        raise ValueError(f"unexpected prefix: {line[:80]!r}")
    out: dict[str, str] = {}
    for part in parts[1:]:
        key, sep, value = part.partition("=")
        if not sep or key in out:
            raise ValueError(f"bad field {part!r}")
        out[key] = value
    return out


def normalize_label(value: str) -> str:
    return value.replace("\\", "/")


def as_int(value: str | None) -> int | None:
    if value is None or value == "null":
        return None
    return int(value)


def as_bool(value: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(value)


def aggregate(root: Path, oracle_jsonl: Path, oracle_log: Path, mimir_log: Path) -> None:
    base_rows = [json.loads(line) for line in oracle_jsonl.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(base_rows) != 47:
        raise SystemExit(f"expected 47 R3.14A identity rows, got {len(base_rows)}")
    identities: dict[str, dict] = {}
    for row in base_rows:
        label = normalize_label(row["relative_path"])
        path = root / row["relative_path"]
        data = path.read_bytes()
        actual_sha = hashlib.sha256(data).hexdigest()
        if len(data) != int(row["byte_length"]) or actual_sha != row["sha256"].lower():
            raise SystemExit(f"identity mismatch: {label}")
        identities[label] = row
    if len(identities) != 47:
        raise SystemExit("R3.14A identity set is not 47 unique paths")

    oracle_lines = oracle_log.read_text(encoding="utf-8", errors="replace").splitlines()
    if sum(line == "R3_15A_ORACLE_PARSE=PASS" for line in oracle_lines) != 47:
        raise SystemExit("oracle parse PASS count is not 47")
    raw_rows = [parse_tsv_line(line, "R3_15A_NEWACTOR") for line in oracle_lines if line.startswith("R3_15A_NEWACTOR\t")]
    if not raw_rows:
        raise SystemExit("no NewActor evidence rows emitted")

    mimir_lines = mimir_log.read_text(encoding="utf-8", errors="replace").splitlines()
    if sum(line == "R3_15A_MIMIR_PLAN=PASS" for line in mimir_lines) != 47:
        raise SystemExit("MIMIR plan PASS count is not 47")
    spawn_map: dict[tuple[str, int], str] = {}
    for line in mimir_lines:
        if not line.startswith("R3_15A_MIMIR_SPAWN\t"):
            continue
        row = parse_tsv_line(line, "R3_15A_MIMIR_SPAWN")
        label = normalize_label(row["label"])
        marker = "/test_corpus/"
        if marker in label:
            label = "test_corpus/" + label.split(marker, 1)[1]
        elif "/external_fixtures/" in label:
            label = "external_fixtures/" + label.split("/external_fixtures/", 1)[1]
        spawn_map[(label, int(row["object_id"]))] = row["spawn"]

    evidence: list[dict] = []
    mismatches: list[dict] = []
    for raw in raw_rows:
        label = normalize_label(raw["label"])
        if label not in identities:
            raise SystemExit(f"oracle row label not in frozen 47 identities: {label}")
        identity = identities[label]
        object_id = int(raw["object_id_value"])
        mimir_spawn = spawn_map.get((label, object_id))
        oracle_spawn = raw["oracle_spawn_kind"]
        match = mimir_spawn == oracle_spawn
        if not match:
            mismatches.append({"relative_path": label, "object_id": object_id, "oracle": oracle_spawn, "mimir": mimir_spawn})
        rec = {
            "relative_path": label,
            "sha256": identity["sha256"].lower(),
            "BuildVersion": identity["build_version"],
            "network_start": identity["network_start"],
            "network_size": identity["network_size"],
            "frame_index": int(raw["frame_index"]),
            "actor_ordinal": int(raw["actor_ordinal"]),
            "actor_id": int(raw["actor_id"]),
            "new_bit_end": int(raw["new_bit_end"]),
            "branch_start_bit": int(raw["branch_start_bit"]),
            "version_major": int(raw["version_major"]),
            "version_minor": int(raw["version_minor"]),
            "net_version": int(raw["net_version"]),
            "is_lan": as_bool(raw["is_lan"]),
            "do_parse_name": as_bool(raw["do_parse_name"]),
            "name_id_present": as_bool(raw["name_id_present"]),
            "name_id_value": as_int(raw["name_id_value"]),
            "name_id_start_bit": as_int(raw["name_id_start_bit"]),
            "name_id_end_bit": as_int(raw["name_id_end_bit"]),
            "opaque_bit_value": as_bool(raw["opaque_bit_value"]),
            "opaque_bit_start": int(raw["opaque_bit_start"]),
            "opaque_bit_end": int(raw["opaque_bit_end"]),
            "object_id_value": object_id,
            "object_id_start_bit": int(raw["object_id_start_bit"]),
            "object_id_end_bit": int(raw["object_id_end_bit"]),
            "object_table_length": int(raw["object_table_length"]),
            "object_id_in_range": as_bool(raw["object_id_in_range"]),
            "object_name": raw["object_name"],
            "oracle_spawn_kind": oracle_spawn,
            "mimir_static_spawn_kind": mimir_spawn,
            "spawn_kind_match": match,
            "trajectory_start_bit": int(raw["trajectory_start_bit"]),
            "trajectory_end_bit": int(raw["trajectory_end_bit"]),
            "location_start_bit": as_int(raw["location_start_bit"]),
            "location_end_bit": as_int(raw["location_end_bit"]),
            "location_x_i32": as_int(raw["location_x_i32"]),
            "location_y_i32": as_int(raw["location_y_i32"]),
            "location_z_i32": as_int(raw["location_z_i32"]),
            "rotation_start_bit": as_int(raw["rotation_start_bit"]),
            "rotation_end_bit": as_int(raw["rotation_end_bit"]),
            "yaw_present": as_bool(raw["yaw_present"]),
            "yaw_i8": as_int(raw["yaw_i8"]),
            "pitch_present": as_bool(raw["pitch_present"]),
            "pitch_i8": as_int(raw["pitch_i8"]),
            "roll_present": as_bool(raw["roll_present"]),
            "roll_i8": as_int(raw["roll_i8"]),
            "branch_end_bit": int(raw["branch_end_bit"]),
            "branch_bit_length": int(raw["branch_bit_length"]),
        }
        if rec["branch_start_bit"] != rec["new_bit_end"]:
            raise SystemExit("branch start/new end mismatch")
        if rec["opaque_bit_end"] != rec["opaque_bit_start"] + 1:
            raise SystemExit("opaque bit width mismatch")
        if rec["object_id_end_bit"] != rec["object_id_start_bit"] + 32:
            raise SystemExit("object_id is not exact raw i32 width")
        if rec["do_parse_name"]:
            if rec["name_id_start_bit"] is None or rec["name_id_end_bit"] != rec["name_id_start_bit"] + 32:
                raise SystemExit("name_id gate true but exact i32 range missing")
        elif any(rec[key] is not None for key in ("name_id_value", "name_id_start_bit", "name_id_end_bit")):
            raise SystemExit("name_id bits consumed while gate false")
        if rec["trajectory_end_bit"] != rec["branch_end_bit"]:
            raise SystemExit("branch hard stop drift")
        evidence.append(rec)

    all_path_counts = {label: 0 for label in identities}
    for rec in evidence:
        all_path_counts[rec["relative_path"]] += 1
    missing_new = sorted(label for label, count in all_path_counts.items() if count == 0)

    loc_lengths = [rec["location_end_bit"] - rec["location_start_bit"] for rec in evidence if rec["location_start_bit"] is not None]
    rot_lengths = [rec["rotation_end_bit"] - rec["rotation_start_bit"] for rec in evidence if rec["rotation_start_bit"] is not None]
    spawn_counts = {kind: sum(rec["oracle_spawn_kind"] == kind for rec in evidence) for kind in ("none", "location", "location_rotation")}

    summary = {
        "replays_total": 47,
        "replays_with_new_actor": 47 - len(missing_new),
        "replays_without_new_actor": missing_new,
        "oracle_decode_success": 47,
        "new_actor_total": len(evidence),
        "name_gate_true": sum(rec["do_parse_name"] for rec in evidence),
        "name_gate_false": sum(not rec["do_parse_name"] for rec in evidence),
        "name_id_present": sum(rec["name_id_present"] for rec in evidence),
        "spawn_none": spawn_counts["none"],
        "spawn_location": spawn_counts["location"],
        "spawn_location_rotation": spawn_counts["location_rotation"],
        "object_id_min": min(rec["object_id_value"] for rec in evidence),
        "object_id_max": max(rec["object_id_value"] for rec in evidence),
        "invalid_object_id": sum(not rec["object_id_in_range"] for rec in evidence),
        "mimir_spawn_kind_match": sum(rec["spawn_kind_match"] for rec in evidence),
        "mimir_spawn_kind_mismatch": len(mismatches),
        "location_payload_bit_length_min": min(loc_lengths) if loc_lengths else None,
        "location_payload_bit_length_max": max(loc_lengths) if loc_lengths else None,
        "rotation_payload_bit_length_min": min(rot_lengths) if rot_lengths else None,
        "rotation_payload_bit_length_max": max(rot_lengths) if rot_lengths else None,
        "instrumentation_error_count": 0,
    }

    evidence_path = Path("r3_15a_new_actor_all.jsonl")
    evidence_path.write_text("".join(json.dumps(rec, sort_keys=True) + "\n" for rec in evidence), encoding="utf-8")
    stream_sha = hashlib.sha256(evidence_path.read_bytes()).hexdigest()

    selected: dict[tuple, dict] = {}
    def keep(key: tuple, rec: dict) -> None:
        selected.setdefault(key, rec)

    for rec in evidence:
        keep(("first-replay", rec["relative_path"]), rec)
        keep(("family", rec["version_major"], rec["version_minor"], rec["net_version"], rec["is_lan"], rec["do_parse_name"], rec["oracle_spawn_kind"]), rec)
        keep(("spawn", rec["oracle_spawn_kind"]), rec)

    for tag, key, func in (
        ("object-min", "object_id_value", min),
        ("object-max", "object_id_value", max),
    ):
        target = func(rec[key] for rec in evidence)
        keep((tag,), next(rec for rec in evidence if rec[key] == target))
    for prefix, start_key, end_key in (
        ("location", "location_start_bit", "location_end_bit"),
        ("rotation", "rotation_start_bit", "rotation_end_bit"),
    ):
        subset = [rec for rec in evidence if rec[start_key] is not None]
        if subset:
            lengths = [(rec[end_key] - rec[start_key], rec) for rec in subset]
            keep((prefix, "min"), min(lengths, key=lambda item: item[0])[1])
            keep((prefix, "max"), max(lengths, key=lambda item: item[0])[1])

    witnesses = list(selected.values())
    Path("r3_15a_witnesses.jsonl").write_text("".join(json.dumps(rec, sort_keys=True) + "\n" for rec in witnesses), encoding="utf-8")
    summary["full_stream_sha256"] = stream_sha
    summary["witness_count"] = len(witnesses)
    summary["witness_sha256"] = hashlib.sha256(Path("r3_15a_witnesses.jsonl").read_bytes()).hexdigest()
    summary["mismatches"] = mismatches
    Path("r3_15a_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    outcome = "A" if summary["oracle_decode_success"] == 47 and not missing_new and not mismatches else "B"
    aggregate_lines = [
        "pass=R3.15A",
        f"oracle_sha={BOXCARS_SHA}",
        f"replays_total={summary['replays_total']}",
        f"oracle_decode_success={summary['oracle_decode_success']}",
        f"new_actor_total={summary['new_actor_total']}",
        f"name_gate_true={summary['name_gate_true']}",
        f"name_gate_false={summary['name_gate_false']}",
        f"name_id_present={summary['name_id_present']}",
        f"spawn_none={summary['spawn_none']}",
        f"spawn_location={summary['spawn_location']}",
        f"spawn_location_rotation={summary['spawn_location_rotation']}",
        f"object_id_min={summary['object_id_min']}",
        f"object_id_max={summary['object_id_max']}",
        f"invalid_object_id={summary['invalid_object_id']}",
        f"mimir_spawn_kind_match={summary['mimir_spawn_kind_match']}",
        f"mimir_spawn_kind_mismatch={summary['mimir_spawn_kind_mismatch']}",
        f"location_payload_bit_length_min={summary['location_payload_bit_length_min']}",
        f"location_payload_bit_length_max={summary['location_payload_bit_length_max']}",
        f"rotation_payload_bit_length_min={summary['rotation_payload_bit_length_min']}",
        f"rotation_payload_bit_length_max={summary['rotation_payload_bit_length_max']}",
        f"instrumentation_error_count={summary['instrumentation_error_count']}",
        f"full_stream_sha256={summary['full_stream_sha256']}",
        f"witness_count={summary['witness_count']}",
        f"witness_sha256={summary['witness_sha256']}",
        f"outcome_candidate={outcome}",
    ]
    Path("r3_15a_aggregate.txt").write_text("\n".join(aggregate_lines) + "\n", encoding="utf-8")
    print("R3_15A_AGGREGATE=PASS")
    print(f"R3_15A_NEW_ACTOR_TOTAL={len(evidence)}")
    print(f"R3_15A_SPAWN_MISMATCHES={len(mismatches)}")
    print(f"R3_15A_OUTCOME_CANDIDATE={outcome}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("patch-boxcars")
    p.add_argument("root")
    p = sub.add_parser("write-mimir-example")
    p.add_argument("root")
    p = sub.add_parser("aggregate")
    p.add_argument("root")
    p.add_argument("oracle_jsonl")
    p.add_argument("oracle_log")
    p.add_argument("mimir_log")
    args = parser.parse_args()
    if args.command == "patch-boxcars":
        patch_boxcars(Path(args.root).resolve())
    elif args.command == "write-mimir-example":
        write_mimir_example(Path(args.root).resolve())
    elif args.command == "aggregate":
        aggregate(Path(args.root).resolve(), Path(args.oracle_jsonl), Path(args.oracle_log), Path(args.mimir_log))


if __name__ == "__main__":
    main()
