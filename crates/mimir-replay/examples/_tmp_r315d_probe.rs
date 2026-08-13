use mimir_replay::{
    MinimalReplayNetworkFirstNewActorEnvelopeReader as Reader, ReplayInput,
    ReplayNetworkFirstNewActorEnvelopeReader, ReplayNetworkSpawnTrajectoryV1 as Spawn,
};
use std::{env, fs, process};

fn opt<T: ToString>(value: Option<T>) -> String {
    value
        .map(|v| v.to_string())
        .unwrap_or_else(|| "null".to_owned())
}

fn main() {
    let mut args = env::args().skip(1);
    let rel = args.next().unwrap_or_else(|| {
        eprintln!("usage: _tmp_r315d_probe <relative-path> <replay-path>");
        process::exit(2);
    });
    let path = args.next().unwrap_or_else(|| {
        eprintln!("usage: _tmp_r315d_probe <relative-path> <replay-path>");
        process::exit(2);
    });
    if args.next().is_some() {
        eprintln!("too many arguments");
        process::exit(2);
    }

    let bytes = fs::read(&path).unwrap_or_else(|e| {
        eprintln!("{rel}: {e}");
        process::exit(3);
    });
    let input = ReplayInput::Memory {
        label: rel.clone(),
        bytes,
    };
    let decoded = Reader
        .read_network_first_new_actor_envelope(&input)
        .unwrap_or_else(|e| {
            eprintln!("{rel}: {e}");
            process::exit(4);
        });

    let actor_id = opt(decoded.envelope.actor_id);
    let alive = opt(decoded.envelope.alive);
    let is_new = opt(decoded.envelope.is_new);
    let actor = decoded.new_actor.unwrap_or_else(|| {
        eprintln!("{rel}: expected first NewActor payload");
        process::exit(5);
    });

    let spawn = match actor.spawn_kind {
        Spawn::None => "none",
        Spawn::Location => "location",
        Spawn::LocationAndRotation => "location_and_rotation",
    };
    let location_present = actor.location.is_some();
    let rotation_present = actor.rotation.is_some();
    let (lx, ly, lz) = actor
        .location
        .map(|v| (Some(v.x), Some(v.y), Some(v.z)))
        .unwrap_or((None, None, None));
    let (yaw, pitch, roll) = actor
        .rotation
        .map(|r| (r.yaw, r.pitch, r.roll))
        .unwrap_or((None, None, None));

    println!(
        "R3_15D_NATIVE\t{rel}\t{}\t{actor_id}\t{alive}\t{is_new}\t{}\t{}\t{}\t{}\t{spawn}\t{location_present}\t{}\t{}\t{}\t{rotation_present}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        decoded.envelope.actor_present,
        decoded.envelope.stop_bit,
        actor.name_id,
        actor.opaque_post_name_bit,
        actor.object_id,
        opt(lx),
        opt(ly),
        opt(lz),
        yaw.is_some(),
        opt(yaw),
        pitch.is_some(),
        opt(pitch),
        roll.is_some(),
        opt(roll),
        actor.stop_bit
    );
}
