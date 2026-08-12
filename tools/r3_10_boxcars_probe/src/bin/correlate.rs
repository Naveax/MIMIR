use boxcars::{HeaderProp, ParserBuilder, Replay};
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

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

fn display_path(path: &Path) -> String {
    path.to_string_lossy().replace('\\', "/")
}

fn bump(map: &mut BTreeMap<String, u64>, key: String) {
    *map.entry(key).or_default() += 1;
}

fn print_top(label: &str, values: &BTreeMap<String, u64>, limit: usize) {
    let mut rows = values.iter().collect::<Vec<_>>();
    rows.sort_by(|a, b| b.1.cmp(a.1).then_with(|| a.0.cmp(b.0)));
    for (rank, (name, count)) in rows.into_iter().take(limit).enumerate() {
        println!("{label} rank={} count={} name={}", rank + 1, count, name);
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let paths = replay_paths()?;
    if paths.len() != EXPECTED_REPLAY_COUNT {
        return Err(format!("expected {EXPECTED_REPLAY_COUNT} replays, found {}", paths.len()).into());
    }

    let mut supported_replays = 0usize;
    let mut unsupported_replays = 0usize;
    let mut supported_decode_ok = 0usize;
    let mut unsupported_decode_ok = 0usize;
    let mut supported_mismatches = 0u64;
    let mut unsupported_mismatches = 0u64;
    let mut mismatch_gt_005 = 0u64;
    let mut mismatch_gt_01 = 0u64;
    let mut mismatch_gt_05 = 0u64;
    let mut mismatch_gt_1 = 0u64;
    let mut mismatch_gt_100m = 0u64;
    let mut max_abs_delta_step_diff = 0.0f32;
    let mut max_abs_delta_step_diff_path = String::new();
    let mut replay_rows_with_mismatch = 0usize;
    let mut supported_rows_with_mismatch = 0usize;
    let mut unsupported_rows_with_mismatch = 0usize;
    let mut attr_oob = 0u64;
    let mut spawn_object_oob = 0u64;
    let mut all_attribute_names = BTreeMap::<String, u64>::new();
    let mut supported_attribute_names = BTreeMap::<String, u64>::new();
    let mut all_spawn_object_names = BTreeMap::<String, u64>::new();
    let mut supported_spawn_object_names = BTreeMap::<String, u64>::new();

    println!("R3.10b Supported-Lane Timing + Attribute Surface Correlation");
    println!("boxcars_git_rev=c70e77df7af81b436cb545d070bb90c82f562d0b");
    println!("expected_replays={EXPECTED_REPLAY_COUNT}");
    println!("expected_supported_lane={EXPECTED_SUPPORTED_LANE}");

    for path in &paths {
        let data = fs::read(path)?;
        let replay = ParserBuilder::new(&data)
            .never_check_crc()
            .must_parse_network_data()
            .parse()?;
        let supported = is_supported_lane(&replay);
        if supported {
            supported_replays += 1;
            supported_decode_ok += 1;
        } else {
            unsupported_replays += 1;
            unsupported_decode_ok += 1;
        }

        let frames = replay
            .network_frames
            .as_ref()
            .ok_or_else(|| format!("missing network frames for {}", display_path(path)))?;

        let mut row_mismatches = 0u64;
        let mut row_max = 0.0f32;
        for pair in frames.frames.windows(2) {
            let previous = &pair[0];
            let current = &pair[1];
            let diff = ((current.time - previous.time) - current.delta).abs();
            if diff > 0.001 {
                row_mismatches += 1;
                if supported {
                    supported_mismatches += 1;
                } else {
                    unsupported_mismatches += 1;
                }
                if diff > 0.005 {
                    mismatch_gt_005 += 1;
                }
                if diff > 0.01 {
                    mismatch_gt_01 += 1;
                }
                if diff > 0.05 {
                    mismatch_gt_05 += 1;
                }
                if diff > 0.1 {
                    mismatch_gt_1 += 1;
                }
                if diff > 100.0 {
                    mismatch_gt_100m += 1;
                }
                row_max = row_max.max(diff);
                if diff > max_abs_delta_step_diff {
                    max_abs_delta_step_diff = diff;
                    max_abs_delta_step_diff_path = display_path(path);
                }
            }
        }
        if row_mismatches > 0 {
            replay_rows_with_mismatch += 1;
            if supported {
                supported_rows_with_mismatch += 1;
            } else {
                unsupported_rows_with_mismatch += 1;
            }
            println!(
                "MISMATCH_ROW path={} supported={} build={} count={} max_abs_diff={}",
                display_path(path),
                supported,
                header_string(&replay, "BuildVersion").unwrap_or("<missing>"),
                row_mismatches,
                row_max
            );
        }

        for frame in &frames.frames {
            for update in &frame.updated_actors {
                match replay.objects.get(update.object_id.0 as usize) {
                    Some(name) => {
                        bump(&mut all_attribute_names, name.clone());
                        if supported {
                            bump(&mut supported_attribute_names, name.clone());
                        }
                    }
                    None => attr_oob += 1,
                }
            }
            for actor in &frame.new_actors {
                match replay.objects.get(actor.object_id.0 as usize) {
                    Some(name) => {
                        bump(&mut all_spawn_object_names, name.clone());
                        if supported {
                            bump(&mut supported_spawn_object_names, name.clone());
                        }
                    }
                    None => spawn_object_oob += 1,
                }
            }
        }
    }

    println!("SUMMARY supported_replays={supported_replays}");
    println!("SUMMARY unsupported_replays={unsupported_replays}");
    println!("SUMMARY supported_decode_ok={supported_decode_ok}");
    println!("SUMMARY unsupported_decode_ok={unsupported_decode_ok}");
    println!("SUMMARY supported_delta_step_mismatches={supported_mismatches}");
    println!("SUMMARY unsupported_delta_step_mismatches={unsupported_mismatches}");
    println!("SUMMARY mismatch_gt_0_005={mismatch_gt_005}");
    println!("SUMMARY mismatch_gt_0_01={mismatch_gt_01}");
    println!("SUMMARY mismatch_gt_0_05={mismatch_gt_05}");
    println!("SUMMARY mismatch_gt_0_1={mismatch_gt_1}");
    println!("SUMMARY mismatch_gt_100={mismatch_gt_100m}");
    println!("SUMMARY max_abs_delta_step_diff={max_abs_delta_step_diff}");
    println!("SUMMARY max_abs_delta_step_diff_path={max_abs_delta_step_diff_path}");
    println!("SUMMARY replay_rows_with_mismatch={replay_rows_with_mismatch}");
    println!("SUMMARY supported_rows_with_mismatch={supported_rows_with_mismatch}");
    println!("SUMMARY unsupported_rows_with_mismatch={unsupported_rows_with_mismatch}");
    println!("SUMMARY attribute_object_oob={attr_oob}");
    println!("SUMMARY spawn_object_oob={spawn_object_oob}");
    println!("SUMMARY unique_attribute_names_all={}", all_attribute_names.len());
    println!("SUMMARY unique_attribute_names_supported={}", supported_attribute_names.len());
    println!("SUMMARY unique_spawn_object_names_all={}", all_spawn_object_names.len());
    println!("SUMMARY unique_spawn_object_names_supported={}", supported_spawn_object_names.len());
    print_top("SUPPORTED_ATTRIBUTE", &supported_attribute_names, 80);
    print_top("SUPPORTED_SPAWN_OBJECT", &supported_spawn_object_names, 50);

    if supported_replays != EXPECTED_SUPPORTED_LANE {
        return Err(format!(
            "supported lane drift: expected {EXPECTED_SUPPORTED_LANE}, found {supported_replays}"
        )
        .into());
    }
    if attr_oob != 0 || spawn_object_oob != 0 {
        return Err("decoded object id escaped replay.objects bounds".into());
    }

    println!("attribute_semantics_admitted=false");
    println!("native_frame_decoder_admitted=false");
    println!("R3_10B_CORRELATION_COMPLETED=PASS");
    Ok(())
}
