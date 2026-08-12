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

fn variant(attribute: &Attribute) -> &'static str {
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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let paths = replay_paths()?;
    if paths.len() != EXPECTED_REPLAY_COUNT {
        return Err(format!("expected {EXPECTED_REPLAY_COUNT} replays, got {}", paths.len()).into());
    }

    let mut supported_replays = 0usize;
    let mut name_variants = BTreeMap::<String, BTreeMap<&'static str, BTreeSet<String>>>::new();
    let mut name_variant_counts = BTreeMap::<(String, &'static str), u64>::new();

    println!("R3.10d Version-Sensitive Wire Conflict Evidence");
    println!("boxcars_git_rev=c70e77df7af81b436cb545d070bb90c82f562d0b");
    println!("expected_replays={EXPECTED_REPLAY_COUNT}");
    println!("expected_supported_lane={EXPECTED_SUPPORTED_LANE}");

    for path in paths {
        let data = fs::read(path)?;
        let replay = ParserBuilder::new(&data)
            .never_check_crc()
            .must_parse_network_data()
            .parse()?;
        if !is_supported_lane(&replay) {
            continue;
        }
        supported_replays += 1;
        let build = header_string(&replay, "BuildVersion")
            .ok_or("supported replay missing BuildVersion")?
            .to_string();
        let frames = replay.network_frames.as_ref().ok_or("missing network frames")?;

        for frame in &frames.frames {
            for update in &frame.updated_actors {
                let name = replay
                    .objects
                    .get(update.object_id.0 as usize)
                    .ok_or("attribute object id out of bounds")?
                    .clone();
                let wire = variant(&update.attribute);
                name_variants
                    .entry(name.clone())
                    .or_default()
                    .entry(wire)
                    .or_default()
                    .insert(build.clone());
                *name_variant_counts.entry((name, wire)).or_default() += 1;
            }
        }
    }

    let conflicts = name_variants
        .iter()
        .filter(|(_, variants)| variants.len() > 1)
        .collect::<Vec<_>>();

    println!("SUMMARY supported_replays={supported_replays}");
    println!("SUMMARY unique_attribute_names={}", name_variants.len());
    println!("SUMMARY conflict_attribute_names={}", conflicts.len());

    for (name, variants) in &conflicts {
        let variant_list = variants.keys().copied().collect::<Vec<_>>().join(",");
        println!("CONFLICT name={} variants={}", name, variant_list);
        for (wire, builds) in variants.iter() {
            let count = name_variant_counts
                .get(&(name.to_string(), *wire))
                .copied()
                .unwrap_or(0);
            println!(
                "CONFLICT_VARIANT name={} variant={} count={} builds={}",
                name,
                wire,
                count,
                builds.iter().cloned().collect::<Vec<_>>().join(",")
            );
        }
    }

    if supported_replays != EXPECTED_SUPPORTED_LANE {
        return Err("supported lane count drift".into());
    }

    println!("global_name_to_wire_mapping_admitted={}", conflicts.is_empty());
    println!("version_sensitive_wire_dispatch_required={}", !conflicts.is_empty());
    println!("native_wire_decoder_admitted=false");
    println!("R3_10D_CONFLICT_EVIDENCE_COMPLETED=PASS");
    Ok(())
}
