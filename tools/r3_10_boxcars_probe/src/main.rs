use boxcars::{HeaderProp, ParserBuilder, Replay};
use std::fs;
use std::path::{Path, PathBuf};

const EXPECTED_REPLAY_COUNT: usize = 103;

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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let paths = replay_paths()?;
    if paths.len() != EXPECTED_REPLAY_COUNT {
        return Err(format!(
            "expected {EXPECTED_REPLAY_COUNT} replay files, found {}",
            paths.len()
        )
        .into());
    }

    let mut decode_ok = 0usize;
    let mut decode_fail = 0usize;
    let mut missing_network_frames = 0usize;
    let mut declared_frames_missing = 0usize;
    let mut declared_equal_decoded = 0usize;
    let mut declared_gt_decoded = 0usize;
    let mut declared_lt_decoded = 0usize;
    let mut first_delta_zero = 0usize;
    let mut first_delta_nonzero = 0usize;
    let mut nonfinite_timing_values = 0usize;
    let mut negative_timing_values = 0usize;
    let mut time_regressions = 0usize;
    let mut delta_vs_time_step_mismatches = 0usize;
    let mut total_frames = 0usize;
    let mut total_new_actors = 0usize;
    let mut total_deleted_actors = 0usize;
    let mut total_updated_attributes = 0usize;
    let mut min_frames: Option<usize> = None;
    let mut max_frames: Option<usize> = None;
    let mut min_first_time: Option<f32> = None;
    let mut max_first_time: Option<f32> = None;
    let mut min_last_time: Option<f32> = None;
    let mut max_last_time: Option<f32> = None;

    println!("R3.10 Boxcars Full-Network Differential Evidence");
    println!("boxcars_git_rev=c70e77df7af81b436cb545d070bb90c82f562d0b");
    println!("crc_policy=never_check_crc");
    println!("network_policy=must_parse_network_data");
    println!("expected_replays={EXPECTED_REPLAY_COUNT}");

    for path in &paths {
        let data = fs::read(path)?;
        match ParserBuilder::new(&data)
            .never_check_crc()
            .must_parse_network_data()
            .parse()
        {
            Ok(replay) => {
                let Some(network) = replay.network_frames.as_ref() else {
                    missing_network_frames += 1;
                    decode_fail += 1;
                    println!("FAIL\t{}\tmissing_network_frames", display_path(path));
                    continue;
                };

                decode_ok += 1;
                let frames = &network.frames;
                let frame_count = frames.len();
                total_frames += frame_count;
                min_frames = Some(min_frames.map_or(frame_count, |value| value.min(frame_count)));
                max_frames = Some(max_frames.map_or(frame_count, |value| value.max(frame_count)));

                let declared = header_i32(&replay, "NumFrames");
                match declared {
                    Some(value) if value >= 0 => {
                        let declared = value as usize;
                        if declared == frame_count {
                            declared_equal_decoded += 1;
                        } else if declared > frame_count {
                            declared_gt_decoded += 1;
                        } else {
                            declared_lt_decoded += 1;
                        }
                    }
                    _ => declared_frames_missing += 1,
                }

                if let Some(first) = frames.first() {
                    if first.delta == 0.0 {
                        first_delta_zero += 1;
                    } else {
                        first_delta_nonzero += 1;
                    }
                    min_first_time = Some(min_first_time.map_or(first.time, |value| value.min(first.time)));
                    max_first_time = Some(max_first_time.map_or(first.time, |value| value.max(first.time)));
                }
                if let Some(last) = frames.last() {
                    min_last_time = Some(min_last_time.map_or(last.time, |value| value.min(last.time)));
                    max_last_time = Some(max_last_time.map_or(last.time, |value| value.max(last.time)));
                }

                for frame in frames {
                    if !frame.time.is_finite() {
                        nonfinite_timing_values += 1;
                    }
                    if !frame.delta.is_finite() {
                        nonfinite_timing_values += 1;
                    }
                    if frame.time < 0.0 {
                        negative_timing_values += 1;
                    }
                    if frame.delta < 0.0 {
                        negative_timing_values += 1;
                    }
                    total_new_actors += frame.new_actors.len();
                    total_deleted_actors += frame.deleted_actors.len();
                    total_updated_attributes += frame.updated_actors.len();
                }

                for pair in frames.windows(2) {
                    let previous = &pair[0];
                    let current = &pair[1];
                    if current.time < previous.time {
                        time_regressions += 1;
                    }
                    let observed_step = current.time - previous.time;
                    if (observed_step - current.delta).abs() > 0.001 {
                        delta_vs_time_step_mismatches += 1;
                    }
                }

                println!(
                    "OK\t{}\tmajor={}\tminor={}\tnet={}\tbuild={}\treplay_version={}\tdeclared_frames={}\tdecoded_frames={}\tfirst_time={}\tlast_time={}\tnew={}\tdeleted={}\tupdated={}",
                    display_path(path),
                    replay.major_version,
                    replay.minor_version,
                    replay.net_version.unwrap_or(0),
                    header_string(&replay, "BuildVersion").unwrap_or("<missing>"),
                    header_i32(&replay, "ReplayVersion")
                        .map(|value| value.to_string())
                        .unwrap_or_else(|| "<missing>".to_string()),
                    declared
                        .map(|value| value.to_string())
                        .unwrap_or_else(|| "<missing>".to_string()),
                    frame_count,
                    frames.first().map(|frame| frame.time).unwrap_or(0.0),
                    frames.last().map(|frame| frame.time).unwrap_or(0.0),
                    frames.iter().map(|frame| frame.new_actors.len()).sum::<usize>(),
                    frames
                        .iter()
                        .map(|frame| frame.deleted_actors.len())
                        .sum::<usize>(),
                    frames
                        .iter()
                        .map(|frame| frame.updated_actors.len())
                        .sum::<usize>(),
                );
            }
            Err(error) => {
                decode_fail += 1;
                println!("FAIL\t{}\t{:?}", display_path(path), error);
            }
        }
    }

    println!("SUMMARY files_seen={}", paths.len());
    println!("SUMMARY decode_ok={decode_ok}");
    println!("SUMMARY decode_fail={decode_fail}");
    println!("SUMMARY missing_network_frames={missing_network_frames}");
    println!("SUMMARY declared_frames_missing={declared_frames_missing}");
    println!("SUMMARY declared_equal_decoded={declared_equal_decoded}");
    println!("SUMMARY declared_gt_decoded={declared_gt_decoded}");
    println!("SUMMARY declared_lt_decoded={declared_lt_decoded}");
    println!("SUMMARY first_delta_zero={first_delta_zero}");
    println!("SUMMARY first_delta_nonzero={first_delta_nonzero}");
    println!("SUMMARY nonfinite_timing_values={nonfinite_timing_values}");
    println!("SUMMARY negative_timing_values={negative_timing_values}");
    println!("SUMMARY time_regressions={time_regressions}");
    println!("SUMMARY delta_vs_time_step_mismatches={delta_vs_time_step_mismatches}");
    println!("SUMMARY total_frames={total_frames}");
    println!("SUMMARY total_new_actors={total_new_actors}");
    println!("SUMMARY total_deleted_actors={total_deleted_actors}");
    println!("SUMMARY total_updated_attributes={total_updated_attributes}");
    println!("SUMMARY min_frames={}", min_frames.unwrap_or(0));
    println!("SUMMARY max_frames={}", max_frames.unwrap_or(0));
    println!("SUMMARY min_first_time={}", min_first_time.unwrap_or(0.0));
    println!("SUMMARY max_first_time={}", max_first_time.unwrap_or(0.0));
    println!("SUMMARY min_last_time={}", min_last_time.unwrap_or(0.0));
    println!("SUMMARY max_last_time={}", max_last_time.unwrap_or(0.0));
    println!("actor_semantics_admitted=false");
    println!("attribute_semantics_admitted=false");
    println!("raw_state_contract_admitted=false");
    println!("mimir_production_dependency_added=false");
    println!("R3_10_PROBE_COMPLETED=PASS");
    Ok(())
}
