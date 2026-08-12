use boxcars::{Attribute, HeaderProp, ParserBuilder, Replay};
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::PathBuf;

const EXPECTED_REPLAY_COUNT: usize = 103;
const EXPECTED_SUPPORTED_LANE: usize = 47;
const SUPPORTED_BUILDS: [&str; 13] = [
    "241206.55345.468477",
    "250811.43331.492665",
    "251020.62592.500294",
    "220826.56130.393105",
    "230224.54624.415510",
    "230823.66121.430366",
    "231010.63095.433650",
    "211110.58467.353926",
    "211123.48895.355454",
    "230113.44243.411503",
    "230413.76047.419576",
    "240425.56865.448852",
    "240717.49861.454952",
];

fn header_i32(replay: &Replay, key: &str) -> Option<i32> {
    replay.properties.iter().find_map(|(name, value)| {
        if name == key {
            match value {
                HeaderProp::Int(value) => Some(*value),
                _ => None,
            }
        } else {
            None
        }
    })
}

fn header_string<'a>(replay: &'a Replay, key: &str) -> Option<&'a str> {
    replay.properties.iter().find_map(|(name, value)| {
        if name == key {
            match value {
                HeaderProp::Name(value) | HeaderProp::Str(value) => Some(value.as_str()),
                _ => None,
            }
        } else {
            None
        }
    })
}

fn is_supported_lane(replay: &Replay) -> bool {
    replay.major_version == 868
        && replay.minor_version == 32
        && replay.net_version == Some(10)
        && replay.game_type == "TAGame.Replay_Soccar_TA"
        && header_i32(replay, "ReplayVersion") == Some(8)
        && header_string(replay, "BuildVersion").is_some_and(|build| SUPPORTED_BUILDS.contains(&build))
}

fn attribute_variant(attribute: &Attribute) -> &'static str {
    match attribute {
        Attribute::Boolean(_) => "Boolean",
        Attribute::Byte(_) => "Byte",
        Attribute::AppliedDamage(_) => "AppliedDamage",
        Attribute::DamageState(_) => "DamageState",
        Attribute::CamSettings(_) => "CamSettings",
        Attribute::ClubColors(_) => "ClubColors",
        Attribute::Demolish(_) => "Demolish",
        Attribute::DemolishExtended(_) => "DemolishExtended",
        Attribute::DemolishFx(_) => "DemolishFx",
        Attribute::Enum(_) => "Enum",
        Attribute::Explosion(_) => "Explosion",
        Attribute::ExtendedExplosion(_) => "ExtendedExplosion",
        Attribute::FlaggedByte(_, _) => "FlaggedByte",
        Attribute::ActiveActor(_) => "ActiveActor",
        Attribute::Float(_) => "Float",
        Attribute::GameMode(_, _) => "GameMode",
        Attribute::Int(_) => "Int",
        Attribute::Int64(_) => "Int64",
        Attribute::Loadout(_) => "Loadout",
        Attribute::TeamLoadout(_) => "TeamLoadout",
        Attribute::Location(_) => "Location",
        Attribute::MusicStinger(_) => "MusicStinger",
        Attribute::PlayerHistoryKey(_) => "PlayerHistoryKey",
        Attribute::Pickup(_) => "Pickup",
        Attribute::PickupNew(_) => "PickupNew",
        Attribute::QWord(_) => "QWord",
        Attribute::Welded(_) => "Welded",
        Attribute::Title(..) => "Title",
        Attribute::TeamPaint(_) => "TeamPaint",
        Attribute::RigidBody(_) => "RigidBody",
        Attribute::String(_) => "String",
        Attribute::UniqueId(_) => "UniqueId",
        Attribute::Reservation(_) => "Reservation",
        Attribute::PartyLeader(_) => "PartyLeader",
        Attribute::PrivateMatch(_) => "PrivateMatch",
        Attribute::LoadoutOnline(_) => "LoadoutOnline",
        Attribute::LoadoutsOnline(_) => "LoadoutsOnline",
        Attribute::StatEvent(_) => "StatEvent",
        Attribute::Rotation(_) => "Rotation",
        Attribute::RepStatTitle(_) => "RepStatTitle",
        Attribute::PickupInfo(_) => "PickupInfo",
        Attribute::Impulse(_) => "Impulse",
        Attribute::ReplicatedBoost(_) => "ReplicatedBoost",
        Attribute::LogoData(_) => "LogoData",
    }
}

fn replay_paths() -> Result<Vec<PathBuf>, Box<dyn std::error::Error>> {
    let mut paths = vec![
        PathBuf::from("external_fixtures/sample_001.replay"),
        PathBuf::from("external_fixtures/sample_002.replay"),
        PathBuf::from("external_fixtures/sample_003.replay"),
    ];
    let mut corpus = fs::read_dir("test_corpus/largest_100")?
        .filter_map(|entry| entry.ok())
        .map(|entry| entry.path())
        .filter(|path| path.extension().is_some_and(|ext| ext == "replay"))
        .collect::<Vec<_>>();
    corpus.sort();
    paths.extend(corpus);
    Ok(paths)
}

fn bump(map: &mut BTreeMap<&'static str, u64>, key: &'static str) {
    *map.entry(key).or_default() += 1;
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let paths = replay_paths()?;
    if paths.len() != EXPECTED_REPLAY_COUNT {
        return Err(format!("expected {EXPECTED_REPLAY_COUNT} replays, got {}", paths.len()).into());
    }

    let mut supported_replays = 0usize;
    let mut all_variants = BTreeMap::<&'static str, u64>::new();
    let mut supported_variants = BTreeMap::<&'static str, u64>::new();
    let mut supported_variant_names = BTreeMap::<&'static str, BTreeSet<String>>::new();
    let mut supported_name_variant = BTreeMap::<String, &'static str>::new();
    let mut name_variant_conflicts = 0usize;
    let mut trajectory_none = 0u64;
    let mut trajectory_location = 0u64;
    let mut trajectory_location_rotation = 0u64;
    let mut trajectory_rotation_only = 0u64;

    println!("R3.10c Wire Decoder Surface Evidence");
    println!("boxcars_git_rev=c70e77df7af81b436cb545d070bb90c82f562d0b");
    println!("expected_replays={EXPECTED_REPLAY_COUNT}");
    println!("expected_supported_lane={EXPECTED_SUPPORTED_LANE}");

    for path in paths {
        let data = fs::read(&path)?;
        let replay = ParserBuilder::new(&data)
            .never_check_crc()
            .must_parse_network_data()
            .parse()?;
        let supported = is_supported_lane(&replay);
        if supported {
            supported_replays += 1;
        }
        let frames = replay.network_frames.as_ref().ok_or("missing network frames")?;

        for frame in &frames.frames {
            for update in &frame.updated_actors {
                let variant = attribute_variant(&update.attribute);
                bump(&mut all_variants, variant);
                if supported {
                    bump(&mut supported_variants, variant);
                    let name = replay
                        .objects
                        .get(update.object_id.0 as usize)
                        .ok_or("attribute object id out of bounds")?
                        .clone();
                    supported_variant_names
                        .entry(variant)
                        .or_default()
                        .insert(name.clone());
                    match supported_name_variant.insert(name, variant) {
                        Some(previous) if previous != variant => name_variant_conflicts += 1,
                        _ => {}
                    }
                }
            }

            if supported {
                for actor in &frame.new_actors {
                    match (
                        actor.initial_trajectory.location.is_some(),
                        actor.initial_trajectory.rotation.is_some(),
                    ) {
                        (false, false) => trajectory_none += 1,
                        (true, false) => trajectory_location += 1,
                        (true, true) => trajectory_location_rotation += 1,
                        (false, true) => trajectory_rotation_only += 1,
                    }
                }
            }
        }
    }

    println!("SUMMARY supported_replays={supported_replays}");
    println!("SUMMARY unique_wire_variants_all={}", all_variants.len());
    println!("SUMMARY unique_wire_variants_supported={}", supported_variants.len());
    println!("SUMMARY supported_name_variant_conflicts={name_variant_conflicts}");
    println!("SUMMARY supported_trajectory_none={trajectory_none}");
    println!("SUMMARY supported_trajectory_location={trajectory_location}");
    println!("SUMMARY supported_trajectory_location_rotation={trajectory_location_rotation}");
    println!("SUMMARY supported_trajectory_rotation_only={trajectory_rotation_only}");

    let mut variants = supported_variants.iter().collect::<Vec<_>>();
    variants.sort_by(|a, b| b.1.cmp(a.1).then_with(|| a.0.cmp(b.0)));
    for (rank, (variant, count)) in variants.into_iter().enumerate() {
        let unique_names = supported_variant_names.get(variant).map_or(0, BTreeSet::len);
        println!(
            "SUPPORTED_WIRE_VARIANT rank={} count={} unique_attribute_names={} variant={}",
            rank + 1,
            count,
            unique_names,
            variant
        );
    }

    for (name, variant) in &supported_name_variant {
        println!("SUPPORTED_NAME_WIRE variant={} name={}", variant, name);
    }

    if supported_replays != EXPECTED_SUPPORTED_LANE {
        return Err("supported lane count drift".into());
    }
    if name_variant_conflicts != 0 {
        return Err("same supported attribute name decoded to multiple variants".into());
    }
    if trajectory_rotation_only != 0 {
        return Err("unobserved rotation-only spawn trajectory appeared".into());
    }

    println!("native_wire_decoder_admitted=false");
    println!("raw_state_semantics_admitted=false");
    println!("R3_10C_WIRE_SURFACE_COMPLETED=PASS");
    Ok(())
}
