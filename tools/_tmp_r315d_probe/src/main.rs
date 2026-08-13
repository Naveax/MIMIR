use mimir_replay::{
    MinimalReplayNetworkFirstNewActorEnvelopeReader, ReplayInput,
    ReplayNetworkFirstNewActorEnvelopeReader, ReplayNetworkSpawnTrajectoryV1,
};
use std::error::Error;
use std::fs::{self, File};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::PathBuf;

fn opt_i32(value: Option<i32>) -> String {
    value.map(|v| v.to_string()).unwrap_or_else(|| "null".to_owned())
}

fn opt_i8(value: Option<i8>) -> String {
    value.map(|v| v.to_string()).unwrap_or_else(|| "null".to_owned())
}

fn spawn_name(value: ReplayNetworkSpawnTrajectoryV1) -> &'static str {
    match value {
        ReplayNetworkSpawnTrajectoryV1::None => "none",
        ReplayNetworkSpawnTrajectoryV1::Location => "location",
        ReplayNetworkSpawnTrajectoryV1::LocationAndRotation => "location_and_rotation",
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args_os().skip(1);
    let paths_file = PathBuf::from(args.next().ok_or("missing paths file")?);
    let output_file = PathBuf::from(args.next().ok_or("missing output file")?);
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }

    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..").canonicalize()?;
    let reader = MinimalReplayNetworkFirstNewActorEnvelopeReader;
    let input = BufReader::new(File::open(paths_file)?);
    let mut out = BufWriter::new(File::create(output_file)?);
    writeln!(out, "relative_path\tactor_present\tactor_id\talive\tis_new\tenvelope_stop_bit\tname_id\topaque_post_name_bit\tobject_id\tspawn_kind\tlocation_present\tlocation_x\tlocation_y\tlocation_z\trotation_present\tyaw_present\tyaw\tpitch_present\tpitch\troll_present\troll\tnew_actor_stop_bit")?;

    let mut count = 0usize;
    for line in input.lines() {
        let path = line?;
        if path.trim().is_empty() {
            continue;
        }
        if path.contains('\t') || path.contains('\n') || path.contains('\r') {
            return Err(format!("invalid path delimiter in {path:?}").into());
        }
        let bytes = fs::read(root.join(&path))?;
        let replay_input = ReplayInput::Memory {
            label: path.clone(),
            bytes,
        };
        let result = reader.read_network_first_new_actor_envelope(&replay_input)?;
        let actor = result
            .new_actor
            .ok_or_else(|| format!("first actor was not NewActor for {path}"))?;
        let location = actor.location;
        let rotation = actor.rotation;
        let actor_id = result.envelope.actor_id.map(|v| v as i32);
        let yaw = rotation.and_then(|r| r.yaw);
        let pitch = rotation.and_then(|r| r.pitch);
        let roll = rotation.and_then(|r| r.roll);
        writeln!(
            out,
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            path,
            result.envelope.actor_present,
            opt_i32(actor_id),
            result.envelope.alive.unwrap_or(false),
            result.envelope.is_new.unwrap_or(false),
            result.envelope.stop_bit,
            actor.name_id,
            actor.opaque_post_name_bit,
            actor.object_id,
            spawn_name(actor.spawn_kind),
            location.is_some(),
            opt_i32(location.map(|v| v.x)),
            opt_i32(location.map(|v| v.y)),
            opt_i32(location.map(|v| v.z)),
            rotation.is_some(),
            yaw.is_some(),
            opt_i8(yaw),
            pitch.is_some(),
            opt_i8(pitch),
            roll.is_some(),
            opt_i8(roll),
            actor.stop_bit,
        )?;
        count += 1;
    }
    out.flush()?;
    if count != 47 {
        return Err(format!("expected 47 native rows, wrote {count}").into());
    }
    println!("R3_15D_NATIVE_ROWS={count}");
    println!("R3_15D_NATIVE_PROBE=PASS");
    Ok(())
}
