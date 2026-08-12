use boxcars::{HeaderProp, ParserBuilder, Replay};
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

fn trajectory_name(location: bool, rotation: bool) -> &'static str {
    match (location, rotation) {
        (false, false) => "None",
        (true, false) => "Location",
        (true, true) => "LocationAndRotation",
        (false, true) => "RotationOnly",
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let paths = replay_paths()?;
    if paths.len() != EXPECTED_REPLAY_COUNT {
        return Err(format!("expected {EXPECTED_REPLAY_COUNT} replays, got {}", paths.len()).into());
    }

    let mut supported_replays = 0usize;
    let mut net_cache_attribute_names = BTreeSet::<String>::new();
    let mut decoded_attribute_names = BTreeSet::<String>::new();
    let mut all_object_names = BTreeSet::<String>::new();
    let mut net_cache_class_names = BTreeSet::<String>::new();
    let mut spawn_shapes = BTreeMap::<String, BTreeSet<&'static str>>::new();
    let mut duplicate_object_names = 0usize;
    let mut net_cache_oob = 0usize;
    let mut net_property_oob = 0usize;
    let mut decoded_attribute_oob = 0usize;
    let mut spawn_oob = 0usize;

    println!("R3.11 Supported Lookup Surface Dump");
    println!("boxcars_git_rev=c70e77df7af81b436cb545d070bb90c82f562d0b");
    println!("expected_replays={EXPECTED_REPLAY_COUNT}");
    println!("expected_supported_lane={EXPECTED_SUPPORTED_LANE}");

    for path in paths {
        let data = fs::read(&path)?;
        let replay = ParserBuilder::new(&data)
            .never_check_crc()
            .must_parse_network_data()
            .parse()?;
        if !is_supported_lane(&replay) {
            continue;
        }
        supported_replays += 1;

        let mut local = BTreeSet::new();
        for name in &replay.objects {
            if !local.insert(name) {
                duplicate_object_names += 1;
            }
            all_object_names.insert(name.clone());
        }

        for cache in &replay.net_cache {
            match replay.objects.get(cache.object_ind as usize) {
                Some(name) => {
                    net_cache_class_names.insert(name.clone());
                }
                None => {
                    net_cache_oob += 1;
                    continue;
                }
            }
            for property in &cache.properties {
                match replay.objects.get(property.object_ind as usize) {
                    Some(name) => {
                        net_cache_attribute_names.insert(name.clone());
                    }
                    None => net_property_oob += 1,
                }
            }
        }

        let frames = replay.network_frames.as_ref().ok_or("missing network frames")?;
        for frame in &frames.frames {
            for update in &frame.updated_actors {
                match replay.objects.get(update.object_id.0 as usize) {
                    Some(name) => {
                        decoded_attribute_names.insert(name.clone());
                    }
                    None => decoded_attribute_oob += 1,
                }
            }
            for actor in &frame.new_actors {
                match replay.objects.get(actor.object_id.0 as usize) {
                    Some(name) => {
                        let shape = trajectory_name(
                            actor.initial_trajectory.location.is_some(),
                            actor.initial_trajectory.rotation.is_some(),
                        );
                        spawn_shapes.entry(name.clone()).or_default().insert(shape);
                    }
                    None => spawn_oob += 1,
                }
            }
        }
    }

    println!("SUMMARY supported_replays={supported_replays}");
    println!(
        "SUMMARY unique_attribute_names_from_net_cache={}",
        net_cache_attribute_names.len()
    );
    println!(
        "SUMMARY unique_decoded_attribute_names={}",
        decoded_attribute_names.len()
    );
    println!("SUMMARY unique_object_names={}", all_object_names.len());
    println!("SUMMARY unique_net_cache_class_names={}", net_cache_class_names.len());
    println!("SUMMARY unique_spawn_object_names={}", spawn_shapes.len());
    println!("SUMMARY duplicate_object_names={duplicate_object_names}");
    println!("SUMMARY net_cache_object_oob={net_cache_oob}");
    println!("SUMMARY net_property_object_oob={net_property_oob}");
    println!("SUMMARY decoded_attribute_object_oob={decoded_attribute_oob}");
    println!("SUMMARY spawn_object_oob={spawn_oob}");

    for name in &net_cache_attribute_names {
        println!("NET_CACHE_ATTRIBUTE_NAME\t{name}");
    }
    for name in &decoded_attribute_names {
        println!("DECODED_ATTRIBUTE_NAME\t{name}");
    }
    for name in &all_object_names {
        println!("OBJECT_NAME\t{name}");
    }
    for name in &net_cache_class_names {
        println!("NET_CACHE_CLASS\t{name}");
    }
    for (name, shapes) in &spawn_shapes {
        println!(
            "SPAWN_SHAPE\t{}\t{}",
            name,
            shapes.iter().copied().collect::<Vec<_>>().join(",")
        );
    }

    if supported_replays != EXPECTED_SUPPORTED_LANE
        || net_cache_oob != 0
        || net_property_oob != 0
        || decoded_attribute_oob != 0
        || spawn_oob != 0
    {
        return Err("supported lookup surface hard invariant failed".into());
    }

    println!("R3_11_LOOKUP_SURFACE_DUMP_COMPLETED=PASS");
    Ok(())
}
