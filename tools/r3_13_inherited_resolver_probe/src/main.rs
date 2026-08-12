use boxcars::ParserBuilder;
use mimir_replay::{
    replay_network_attribute_tag_v1, replay_network_parent_class_v1,
    MinimalReplayFooterLookupMaterializationReader, MinimalReplayHeaderReader,
    ReplayFooterLookupMaterializationReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayReader,
};
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Path, PathBuf};

const EXPECTED_REPLAY_COUNT: usize = 103;
const EXPECTED_SUPPORTED_LANE: usize = 47;
const MAX_FAILURE_SAMPLES: usize = 40;

type StreamMap = BTreeMap<u32, u32>;

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

fn build_name_index(objects: &[String]) -> (BTreeMap<&str, u32>, usize) {
    let mut result = BTreeMap::new();
    let mut duplicates = 0usize;
    for (index, name) in objects.iter().enumerate() {
        if result.entry(name.as_str()).or_insert(index as u32) != &(index as u32) {
            duplicates += 1;
        }
    }
    (result, duplicates)
}

fn hierarchy_object_indices(
    object_name: &str,
    name_index: &BTreeMap<&str, u32>,
) -> Result<Vec<u32>, String> {
    let mut current = object_name.to_string();
    let mut seen = BTreeSet::new();
    let mut child_to_parent = Vec::new();

    loop {
        let Some(parent) = replay_network_parent_class_v1(&current) else {
            break;
        };
        if !seen.insert(current.clone()) {
            return Err(format!("parent cycle while resolving {object_name}: {current}"));
        }
        if let Some(index) = name_index.get(current.as_str()) {
            child_to_parent.push(*index);
        }
        current = parent.to_string();
        if seen.len() > 65 {
            return Err(format!(
                "parent depth escaped admitted surface for {object_name}"
            ));
        }
    }

    Ok(child_to_parent)
}

fn build_effective_maps(
    objects: &[String],
    local_properties: &BTreeMap<u32, StreamMap>,
) -> Result<Vec<StreamMap>, String> {
    let (name_index, duplicates) = build_name_index(objects);
    if duplicates != 0 {
        return Err(format!(
            "duplicate object names are outside admitted R3.13 evidence: {duplicates}"
        ));
    }

    let mut effective = Vec::with_capacity(objects.len());
    for object_name in objects {
        let mut hierarchy = hierarchy_object_indices(object_name, &name_index)?;
        let mut properties = StreamMap::new();
        hierarchy.reverse();
        for object_index in hierarchy {
            if let Some(local) = local_properties.get(&object_index) {
                for (stream_id, property_object_index) in local {
                    properties.insert(*stream_id, *property_object_index);
                }
            }
        }
        effective.push(properties);
    }
    Ok(effective)
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

    let mut supported_replays = 0usize;
    let mut unsupported_replays = 0usize;
    let mut object_table_mismatches = 0usize;
    let mut duplicate_local_stream_entries = 0u64;
    let mut local_not_implemented_entries = 0u64;
    let mut total_effective_properties = 0u64;
    let mut total_frames = 0u64;
    let mut total_updates = 0u64;
    let mut total_new_actors = 0u64;
    let mut total_deleted_actors = 0u64;
    let mut actor_class_oob = 0u64;
    let mut property_object_oob = 0u64;
    let mut missing_active_actor = 0u64;
    let mut unresolved_stream = 0u64;
    let mut property_object_mismatch = 0u64;
    let mut decoded_not_implemented_hits = 0u64;
    let mut same_frame_new_delete = 0u64;
    let mut active_actor_overwrite_same_class = 0u64;
    let mut active_actor_overwrite_class_changed = 0u64;
    let mut delete_missing_actor = 0u64;
    let mut failure_samples = Vec::<String>::new();

    println!("R3.13 Inherited Stream Resolver Differential Evidence");
    println!("boxcars_git_rev=c70e77df7af81b436cb545d070bb90c82f562d0b");
    println!("registry_source=mimir_replay_production_r3_12");
    println!("expected_replays={EXPECTED_REPLAY_COUNT}");
    println!("expected_supported_lane={EXPECTED_SUPPORTED_LANE}");

    for path in paths {
        let bytes = fs::read(&path)?;
        let label = path
            .file_name()
            .map(|value| value.to_string_lossy().into_owned())
            .unwrap_or_else(|| display_path(&path));
        let input = ReplayInput::Memory {
            label: label.clone(),
            bytes: bytes.clone(),
        };

        if MinimalReplayHeaderReader.read_header(&input).is_err() {
            unsupported_replays += 1;
            continue;
        }
        supported_replays += 1;

        let footer = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&input)
            .map_err(|error| {
                format!(
                    "MIMIR footer lookup failed for {}: {error}",
                    display_path(&path)
                )
            })?;
        let replay = ParserBuilder::new(&bytes)
            .never_check_crc()
            .must_parse_network_data()
            .parse()
            .map_err(|error| {
                format!(
                    "Boxcars decode failed for {}: {error:?}",
                    display_path(&path)
                )
            })?;
        let frames = replay.network_frames.as_ref().ok_or_else(|| {
            format!(
                "Boxcars omitted network frames for {}",
                display_path(&path)
            )
        })?;

        if footer.objects != replay.objects {
            object_table_mismatches += 1;
            if failure_samples.len() < MAX_FAILURE_SAMPLES {
                failure_samples.push(format!(
                    "OBJECT_TABLE_MISMATCH path={}",
                    display_path(&path)
                ));
            }
            continue;
        }

        let objects = &footer.objects;
        let mut local_properties = BTreeMap::<u32, StreamMap>::new();
        for cache in &footer.net_cache {
            if cache.object_index as usize >= objects.len() {
                actor_class_oob += 1;
                continue;
            }
            let target = local_properties.entry(cache.object_index).or_default();
            for property in &cache.properties {
                if property.object_index as usize >= objects.len() {
                    property_object_oob += 1;
                    continue;
                }
                if target
                    .insert(property.stream_id, property.object_index)
                    .is_some()
                {
                    duplicate_local_stream_entries += 1;
                }
                if replay_network_attribute_tag_v1(&objects[property.object_index as usize])
                    == ReplayNetworkAttributeTagV1::NotImplemented
                {
                    local_not_implemented_entries += 1;
                }
            }
        }

        let effective = build_effective_maps(objects, &local_properties)
            .map_err(|error| format!("{}: {error}", display_path(&path)))?;
        total_effective_properties += effective.iter().map(|map| map.len() as u64).sum::<u64>();

        let mut active_actors = BTreeMap::<i32, u32>::new();
        for (frame_index, frame) in frames.frames.iter().enumerate() {
            total_frames += 1;
            total_new_actors += frame.new_actors.len() as u64;
            total_deleted_actors += frame.deleted_actors.len() as u64;
            total_updates += frame.updated_actors.len() as u64;

            let new_ids = frame
                .new_actors
                .iter()
                .map(|actor| actor.actor_id.0)
                .collect::<BTreeSet<_>>();
            let deleted_ids = frame
                .deleted_actors
                .iter()
                .map(|actor| actor.0)
                .collect::<BTreeSet<_>>();
            same_frame_new_delete += new_ids.intersection(&deleted_ids).count() as u64;

            for actor in &frame.new_actors {
                if actor.object_id.0 < 0 || actor.object_id.0 as usize >= objects.len() {
                    actor_class_oob += 1;
                    continue;
                }
                let new_object_index = actor.object_id.0 as u32;
                if let Some(previous_object_index) =
                    active_actors.insert(actor.actor_id.0, new_object_index)
                {
                    if previous_object_index == new_object_index {
                        active_actor_overwrite_same_class += 1;
                    } else {
                        active_actor_overwrite_class_changed += 1;
                        if failure_samples.len() < MAX_FAILURE_SAMPLES {
                            failure_samples.push(format!(
                                "ACTOR_CLASS_CHANGED path={} frame={} actor={} previous_object={} previous_name={} new_object={} new_name={}",
                                display_path(&path),
                                frame_index,
                                actor.actor_id.0,
                                previous_object_index,
                                objects[previous_object_index as usize],
                                new_object_index,
                                objects[new_object_index as usize]
                            ));
                        }
                    }
                }
            }

            for update in &frame.updated_actors {
                let Some(actor_object_index) = active_actors.get(&update.actor_id.0).copied() else {
                    missing_active_actor += 1;
                    if failure_samples.len() < MAX_FAILURE_SAMPLES {
                        failure_samples.push(format!(
                            "MISSING_ACTOR path={} frame={} actor={} stream={} oracle_object={}",
                            display_path(&path),
                            frame_index,
                            update.actor_id.0,
                            update.stream_id.0,
                            update.object_id.0
                        ));
                    }
                    continue;
                };
                if actor_object_index as usize >= effective.len() {
                    actor_class_oob += 1;
                    continue;
                }
                if update.stream_id.0 < 0 {
                    unresolved_stream += 1;
                    continue;
                }
                let stream_id = update.stream_id.0 as u32;
                let Some(property_object_index) =
                    effective[actor_object_index as usize].get(&stream_id).copied()
                else {
                    unresolved_stream += 1;
                    if failure_samples.len() < MAX_FAILURE_SAMPLES {
                        failure_samples.push(format!(
                            "UNRESOLVED_STREAM path={} frame={} actor={} actor_class={} stream={} oracle_object={}",
                            display_path(&path),
                            frame_index,
                            update.actor_id.0,
                            objects[actor_object_index as usize],
                            stream_id,
                            update.object_id.0
                        ));
                    }
                    continue;
                };
                if property_object_index as usize >= objects.len() {
                    property_object_oob += 1;
                    continue;
                }
                if property_object_index as i32 != update.object_id.0 {
                    property_object_mismatch += 1;
                    if failure_samples.len() < MAX_FAILURE_SAMPLES {
                        failure_samples.push(format!(
                            "PROPERTY_MISMATCH path={} frame={} actor={} actor_class={} stream={} expected_object={} expected_name={} oracle_object={} oracle_name={}",
                            display_path(&path),
                            frame_index,
                            update.actor_id.0,
                            objects[actor_object_index as usize],
                            stream_id,
                            property_object_index,
                            objects[property_object_index as usize],
                            update.object_id.0,
                            replay
                                .objects
                                .get(update.object_id.0.max(0) as usize)
                                .map(String::as_str)
                                .unwrap_or("<oob>")
                        ));
                    }
                }
                if replay_network_attribute_tag_v1(&objects[property_object_index as usize])
                    == ReplayNetworkAttributeTagV1::NotImplemented
                {
                    decoded_not_implemented_hits += 1;
                }
            }

            for actor in &frame.deleted_actors {
                if active_actors.remove(&actor.0).is_none() {
                    delete_missing_actor += 1;
                }
            }
        }
    }

    println!("SUMMARY supported_replays={supported_replays}");
    println!("SUMMARY unsupported_replays={unsupported_replays}");
    println!("SUMMARY object_table_mismatches={object_table_mismatches}");
    println!("SUMMARY duplicate_local_stream_entries={duplicate_local_stream_entries}");
    println!("SUMMARY local_not_implemented_entries={local_not_implemented_entries}");
    println!("SUMMARY total_effective_properties={total_effective_properties}");
    println!("SUMMARY total_frames={total_frames}");
    println!("SUMMARY total_updates={total_updates}");
    println!("SUMMARY total_new_actors={total_new_actors}");
    println!("SUMMARY total_deleted_actors={total_deleted_actors}");
    println!("SUMMARY actor_class_oob={actor_class_oob}");
    println!("SUMMARY property_object_oob={property_object_oob}");
    println!("SUMMARY missing_active_actor={missing_active_actor}");
    println!("SUMMARY unresolved_stream={unresolved_stream}");
    println!("SUMMARY property_object_mismatch={property_object_mismatch}");
    println!("SUMMARY decoded_not_implemented_hits={decoded_not_implemented_hits}");
    println!("SUMMARY same_frame_new_delete={same_frame_new_delete}");
    println!(
        "SUMMARY active_actor_overwrite_same_class={active_actor_overwrite_same_class}"
    );
    println!(
        "SUMMARY active_actor_overwrite_class_changed={active_actor_overwrite_class_changed}"
    );
    println!("SUMMARY delete_missing_actor={delete_missing_actor}");
    for sample in &failure_samples {
        println!("FAILURE_SAMPLE {sample}");
    }

    if supported_replays != EXPECTED_SUPPORTED_LANE
        || unsupported_replays != EXPECTED_REPLAY_COUNT - EXPECTED_SUPPORTED_LANE
        || object_table_mismatches != 0
        || duplicate_local_stream_entries != 0
        || actor_class_oob != 0
        || property_object_oob != 0
        || missing_active_actor != 0
        || unresolved_stream != 0
        || property_object_mismatch != 0
        || decoded_not_implemented_hits != 0
        || same_frame_new_delete != 0
        || delete_missing_actor != 0
    {
        return Err("R3.13 inherited resolver differential evidence found a hard mismatch".into());
    }

    println!("network_payload_decoded_by_mimir=false");
    println!("inherited_stream_resolver_production_admitted=false");
    println!("R3_13_DIFFERENTIAL_EVIDENCE=PASS");
    Ok(())
}
