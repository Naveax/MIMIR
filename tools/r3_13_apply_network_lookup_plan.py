from pathlib import Path

path = Path('crates/mimir-replay/src/lib.rs')
text = path.read_text(encoding='utf-8')

old_import = 'use std::collections::BTreeSet;'
new_import = 'use std::collections::{BTreeMap, BTreeSet};'
if text.count(old_import) != 1:
    raise SystemExit('R3.13 collections import marker drift')
text = text.replace(old_import, new_import, 1)

marker = '#[derive(Debug, Default, Clone, Copy)]\npub struct MinimalReplayHeaderReader;'
if text.count(marker) != 1:
    raise SystemExit('R3.13 insertion marker drift')
if 'pub struct ReplayNetworkLookupPlanV1' in text:
    raise SystemExit('R3.13 lookup plan already present')

block = r'''
/// One inherited network property available to an actor class in the admitted lookup plan.
///
/// The tag may be `NotImplemented`. That is an explicit fail-closed decoder boundary, not
/// permission to consume an unknown payload.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkResolvedPropertyV1 {
    pub stream_id: u32,
    pub object_index: u32,
    pub tag: ReplayNetworkAttributeTagV1,
}

/// Effective inherited property lookup for one replay object index.
///
/// `max_prop_id` is the exclusive upper bound used by Rocket League's bounded integer decoder.
/// `prop_id_bits` is the corresponding precomputed bit width parameter. This type does not read
/// network payload bits.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkObjectLookupV1 {
    pub object_index: u32,
    pub max_prop_id: u32,
    pub prop_id_bits: u8,
    pub properties: Vec<ReplayNetworkResolvedPropertyV1>,
}

/// Static network-decoder lookup plan derived entirely from admitted header/footer structure.
///
/// The plan deliberately stops before actor/frame bits. `object_lookups[index] == None` preserves
/// the upstream `MissingCache` distinction for object names that do not participate in the
/// admitted inheritance surface. Spawn trajectories are kept as a separate object-index table
/// because spawn semantics and cache availability are independent.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkLookupPlanV1 {
    pub header: ReplayHeader,
    pub footer_lookup: ReplayFooterLookupMaterializationV1,
    pub num_frames: u32,
    pub max_channels: u32,
    pub channel_bits: u8,
    pub is_lan: bool,
    pub qword_string_uses_text: bool,
    pub spawn_trajectories: Vec<ReplayNetworkSpawnTrajectoryV1>,
    pub object_lookups: Vec<Option<ReplayNetworkObjectLookupV1>>,
}

pub trait ReplayNetworkLookupPlanReader {
    fn read_network_lookup_plan(&self, input: &ReplayInput) -> Result<ReplayNetworkLookupPlanV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayNetworkLookupPlanReader;

impl ReplayNetworkLookupPlanReader for MinimalReplayNetworkLookupPlanReader {
    fn read_network_lookup_plan(&self, input: &ReplayInput) -> Result<ReplayNetworkLookupPlanV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_network_lookup_plan_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(network_lookup_plan_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the network lookup-plan reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

fn network_lookup_plan_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network lookup plan error: {category}: {}",
        detail.into()
    ))
}

fn parse_replay_network_lookup_plan_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayNetworkLookupPlanV1> {
    // Reuse the exact production header admission lane. R3.13 does not widen version/build support.
    let header = parse_replay_header_from_memory(label, bytes)?;
    let footer_lookup = parse_replay_footer_lookup_materialization_from_memory(label, bytes)?;

    let num_frames = header.total_frames.ok_or_else(|| {
        network_lookup_plan_error(
            "missing-header-field",
            "NumFrames is required for the admitted network lookup plan",
        )
    })?;

    let max_channels_i64 = match header.metadata.get("MaxChannels") {
        Some(FieldValue::Integer(value)) => *value,
        Some(other) => {
            return Err(network_lookup_plan_error(
                "mapping",
                format!("MaxChannels must be integer metadata, got {other:?}"),
            ));
        }
        None => {
            return Err(network_lookup_plan_error(
                "missing-header-field",
                "MaxChannels is required for the admitted network lookup plan",
            ));
        }
    };
    let max_channels = u32::try_from(max_channels_i64).map_err(|_| {
        network_lookup_plan_error(
            "mapping",
            format!("MaxChannels {max_channels_i64} cannot fit non-negative u32"),
        )
    })?;
    if max_channels == 0 {
        return Err(network_lookup_plan_error(
            "mapping",
            "MaxChannels must be positive for the admitted network lookup plan",
        ));
    }

    if u64::from(num_frames) > u64::from(footer_lookup.scaffold.content.network_size) {
        return Err(network_lookup_plan_error(
            "precondition",
            format!(
                "NumFrames {num_frames} exceeds network byte count {}",
                footer_lookup.scaffold.content.network_size
            ),
        ));
    }

    let match_type = match header.metadata.get("MatchType") {
        Some(FieldValue::Text(value)) => value.as_str(),
        Some(other) => {
            return Err(network_lookup_plan_error(
                "mapping",
                format!("MatchType must be text metadata, got {other:?}"),
            ));
        }
        None => {
            return Err(network_lookup_plan_error(
                "missing-header-field",
                "MatchType is required for the admitted network lookup plan",
            ));
        }
    };
    let build_version = match header.metadata.get("BuildVersion") {
        Some(FieldValue::Text(value)) => value.as_str(),
        Some(other) => {
            return Err(network_lookup_plan_error(
                "mapping",
                format!("BuildVersion must be text metadata, got {other:?}"),
            ));
        }
        None => {
            return Err(network_lookup_plan_error(
                "missing-header-field",
                "BuildVersion is required for the admitted network lookup plan",
            ));
        }
    };

    let channel_width = u32::BITS - max_channels.leading_zeros();
    let channel_bits_u32 = channel_width.saturating_sub(1);
    let channel_bits = u8::try_from(channel_bits_u32).map_err(|_| {
        network_lookup_plan_error(
            "mapping",
            format!("derived channel bit width {channel_bits_u32} cannot fit u8"),
        )
    })?;

    let (spawn_trajectories, object_lookups) = build_replay_network_lookup_tables_v1(
        &footer_lookup.objects,
        &footer_lookup.net_cache,
    )?;

    Ok(ReplayNetworkLookupPlanV1 {
        header,
        footer_lookup,
        num_frames,
        max_channels,
        channel_bits,
        is_lan: match_type == "Lan",
        qword_string_uses_text: replay_network_qword_string_uses_text_v1(build_version),
        spawn_trajectories,
        object_lookups,
    })
}

fn build_replay_network_lookup_tables_v1(
    objects: &[String],
    net_cache: &[ReplayNetCacheEntryV1],
) -> Result<(
    Vec<ReplayNetworkSpawnTrajectoryV1>,
    Vec<Option<ReplayNetworkObjectLookupV1>>,
)> {
    let mut name_index = BTreeMap::<String, u32>::new();
    for (index, name) in objects.iter().enumerate() {
        let index = u32::try_from(index).map_err(|_| {
            network_lookup_plan_error("mapping", "object index cannot fit u32")
        })?;
        if name_index.insert(name.clone(), index).is_some() {
            return Err(network_lookup_plan_error(
                "malformed",
                format!("duplicate object name is outside admitted lookup evidence: {name}"),
            ));
        }
    }

    let mut local_properties = BTreeMap::<u32, BTreeMap<u32, u32>>::new();
    let mut seen_cache_objects = BTreeSet::new();
    for cache in net_cache {
        if cache.object_index as usize >= objects.len() {
            return Err(network_lookup_plan_error(
                "malformed",
                format!(
                    "net-cache object index {} is outside {} objects",
                    cache.object_index,
                    objects.len()
                ),
            ));
        }
        if !seen_cache_objects.insert(cache.object_index) {
            return Err(network_lookup_plan_error(
                "malformed",
                format!(
                    "duplicate net-cache object index {} is outside admitted lookup evidence",
                    cache.object_index
                ),
            ));
        }

        let target = local_properties.entry(cache.object_index).or_default();
        for property in &cache.properties {
            if property.object_index as usize >= objects.len() {
                return Err(network_lookup_plan_error(
                    "malformed",
                    format!(
                        "net-cache property object index {} is outside {} objects",
                        property.object_index,
                        objects.len()
                    ),
                ));
            }
            if target
                .insert(property.stream_id, property.object_index)
                .is_some()
            {
                return Err(network_lookup_plan_error(
                    "malformed",
                    format!(
                        "duplicate stream id {} for net-cache object {}",
                        property.stream_id, cache.object_index
                    ),
                ));
            }
        }
    }

    let mut hierarchy_by_object = Vec::with_capacity(objects.len());
    for object_name in objects {
        hierarchy_by_object.push(replay_network_hierarchy_object_indices_v1(
            object_name,
            &name_index,
        )?);
    }

    // Match the upstream two-stage spawn table: direct class entries first, then inherited
    // values cached while walking the same object hierarchy used by the attribute lookup.
    let mut spawn_cache = objects
        .iter()
        .map(|name| replay_network_spawn_trajectory_class_v1(name))
        .collect::<Vec<_>>();
    for hierarchy in &hierarchy_by_object {
        let mut unresolved = Vec::new();
        let mut resolved = ReplayNetworkSpawnTrajectoryV1::None;
        for object_index in hierarchy {
            match spawn_cache[*object_index as usize] {
                Some(trajectory) => {
                    resolved = trajectory;
                    break;
                }
                None => unresolved.push(*object_index),
            }
        }
        for object_index in unresolved {
            spawn_cache[object_index as usize] = Some(resolved);
        }
    }
    let spawn_trajectories = spawn_cache
        .into_iter()
        .map(|value| value.unwrap_or(ReplayNetworkSpawnTrajectoryV1::None))
        .collect::<Vec<_>>();

    let mut object_lookups = Vec::with_capacity(objects.len());
    for (object_index, hierarchy) in hierarchy_by_object.into_iter().enumerate() {
        if hierarchy.is_empty() {
            object_lookups.push(None);
            continue;
        }

        let mut effective = BTreeMap::<u32, u32>::new();
        for hierarchy_object_index in hierarchy.iter().rev() {
            if let Some(local) = local_properties.get(hierarchy_object_index) {
                for (stream_id, property_object_index) in local {
                    effective.insert(*stream_id, *property_object_index);
                }
            }
        }

        let max_prop_id = effective
            .keys()
            .next_back()
            .copied()
            .unwrap_or(2)
            .saturating_add(1);
        let max_bit_width = u32::BITS - max_prop_id.leading_zeros();
        let prop_id_bits_u32 = max_bit_width.max(1) - 1;
        let prop_id_bits = u8::try_from(prop_id_bits_u32).map_err(|_| {
            network_lookup_plan_error(
                "mapping",
                format!("derived property bit width {prop_id_bits_u32} cannot fit u8"),
            )
        })?;

        let properties = effective
            .into_iter()
            .map(|(stream_id, property_object_index)| ReplayNetworkResolvedPropertyV1 {
                stream_id,
                object_index: property_object_index,
                tag: replay_network_attribute_tag_v1(&objects[property_object_index as usize]),
            })
            .collect::<Vec<_>>();

        object_lookups.push(Some(ReplayNetworkObjectLookupV1 {
            object_index: u32::try_from(object_index).map_err(|_| {
                network_lookup_plan_error("mapping", "object lookup index cannot fit u32")
            })?,
            max_prop_id,
            prop_id_bits,
            properties,
        }));
    }

    Ok((spawn_trajectories, object_lookups))
}

fn replay_network_hierarchy_object_indices_v1(
    object_name: &str,
    name_index: &BTreeMap<String, u32>,
) -> Result<Vec<u32>> {
    let mut current = object_name.to_string();
    let mut seen = BTreeSet::new();
    let mut child_to_parent = Vec::new();

    loop {
        let Some(parent) = replay_network_parent_class_v1(&current) else {
            break;
        };
        if !seen.insert(current.clone()) {
            return Err(network_lookup_plan_error(
                "malformed",
                format!("network parent cycle while resolving {object_name}: {current}"),
            ));
        }
        if let Some(index) = name_index.get(&current) {
            child_to_parent.push(*index);
        }
        current = parent.to_string();
        if seen.len() > OBSERVED_NETWORK_PARENT_CLASSES_V1.len() {
            return Err(network_lookup_plan_error(
                "malformed",
                format!("network parent depth escaped admitted surface for {object_name}"),
            ));
        }
    }

    Ok(child_to_parent)
}

'''
text = text.replace(marker, block + marker, 1)

tests = r'''

    #[test]
    fn network_lookup_plan_reader_rejects_file_input() {
        let input = ReplayInput::file("outside.replay");
        let error = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&input)
            .expect_err("file input must remain outside the lookup-plan reader");
        assert_error_contains(error, "replay network lookup plan error: unsupported-input");
    }

    #[test]
    fn network_lookup_plan_matches_three_historical_fixtures() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let input = ReplayInput::Memory {
                label: label.to_string(),
                bytes,
            };
            let plan = MinimalReplayNetworkLookupPlanReader
                .read_network_lookup_plan(&input)
                .expect("historical fixture should build admitted lookup plan");
            assert_eq!(plan.header.source_label, label);
            assert_eq!(plan.num_frames, plan.header.total_frames.unwrap());
            assert_eq!(plan.channel_bits, 10);
            assert!(!plan.is_lan);
            assert!(plan.qword_string_uses_text);
            assert_eq!(plan.spawn_trajectories.len(), plan.footer_lookup.objects.len());
            assert_eq!(plan.object_lookups.len(), plan.footer_lookup.objects.len());
            assert!(plan.object_lookups.iter().flatten().next().is_some());
        }
    }

    #[test]
    fn network_lookup_plan_does_not_consume_network_payload_bytes() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        let original_input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: bytes.clone(),
        };
        let original = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&original_input)
            .expect("fixture should build original lookup plan");
        let network_start = usize::try_from(original.footer_lookup.scaffold.content.network_start)
            .expect("network_start should fit usize");
        assert!(original.footer_lookup.scaffold.content.network_size >= 8);

        let mut mutated = bytes;
        mutated[network_start..network_start + 8].copy_from_slice(&[
            0xff, 0xff, 0xff, 0xff, 0x01, 0x02, 0x03, 0x04,
        ]);
        let mutated_input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: mutated,
        };
        let after_mutation = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&mutated_input)
            .expect("lookup plan must stay independent of network payload bytes");
        assert_eq!(after_mutation, original);
    }

    #[test]
    fn network_lookup_plan_preserves_supported_47_lane_and_effective_property_evidence() {
        let mut paths = vec![
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_001.replay"),
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_002.replay"),
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_003.replay"),
        ];
        let root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../../test_corpus/largest_100");
        if !root.is_dir() || paths.iter().any(|path| !path.is_file()) {
            eprintln!("skipping R3.13 corpus lookup-plan regression; fixtures are absent");
            return;
        }
        let mut corpus = std::fs::read_dir(&root)
            .expect("largest_100 should be readable")
            .map(|entry| entry.expect("corpus entry should be readable").path())
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        corpus.sort();
        assert_eq!(corpus.len(), 100);
        paths.extend(corpus);

        let mut supported = 0usize;
        let mut unsupported = 0usize;
        let mut total_effective_properties = 0u64;
        let mut effective_not_implemented = 0u64;
        for path in paths {
            let bytes = std::fs::read(&path).expect("replay should be readable");
            let label = path.file_name().unwrap().to_string_lossy().into_owned();
            let input = ReplayInput::Memory { label, bytes };
            match MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input) {
                Ok(plan) => {
                    supported += 1;
                    assert_eq!(plan.object_lookups.len(), plan.footer_lookup.objects.len());
                    assert_eq!(plan.spawn_trajectories.len(), plan.footer_lookup.objects.len());
                    for lookup in plan.object_lookups.iter().flatten() {
                        total_effective_properties += lookup.properties.len() as u64;
                        effective_not_implemented += lookup
                            .properties
                            .iter()
                            .filter(|property| {
                                property.tag == ReplayNetworkAttributeTagV1::NotImplemented
                            })
                            .count() as u64;
                    }
                }
                Err(error) => {
                    unsupported += 1;
                    assert_error_contains(error, "unsupported-version");
                }
            }
        }

        assert_eq!(supported, 47);
        assert_eq!(unsupported, 56);
        assert_eq!(total_effective_properties, 125_781);
        assert!(effective_not_implemented > 0);
    }

    fn synthetic_net_cache_entry(
        object_index: u32,
        properties: Vec<(u32, u32)>,
    ) -> ReplayNetCacheEntryV1 {
        ReplayNetCacheEntryV1 {
            object_index,
            parent_id: 0,
            cache_id: 0,
            properties: properties
                .into_iter()
                .map(|(stream_id, property_object_index)| ReplayNetCachePropertyV1 {
                    object_index: property_object_index,
                    stream_id,
                })
                .collect(),
        }
    }

    #[test]
    fn network_lookup_plan_child_stream_overrides_parent_stream() {
        let objects = vec![
            "Engine.Actor".to_string(),
            "Engine.Pawn".to_string(),
            "ProjectX.Pawn_X".to_string(),
            "TAGame.RBActor_TA".to_string(),
            "Engine.Actor:DrawScale".to_string(),
            "TAGame.RBActor_TA:ReplicatedRBState".to_string(),
        ];
        let net_cache = vec![
            synthetic_net_cache_entry(0, vec![(5, 4)]),
            synthetic_net_cache_entry(3, vec![(5, 5)]),
        ];
        let (spawns, lookups) = build_replay_network_lookup_tables_v1(&objects, &net_cache)
            .expect("synthetic hierarchy should resolve");

        assert_eq!(
            spawns[3],
            ReplayNetworkSpawnTrajectoryV1::LocationAndRotation
        );
        let lookup = lookups[3].as_ref().expect("RBActor should have cache");
        assert_eq!(lookup.max_prop_id, 6);
        assert_eq!(lookup.prop_id_bits, 2);
        assert_eq!(lookup.properties.len(), 1);
        assert_eq!(lookup.properties[0].stream_id, 5);
        assert_eq!(lookup.properties[0].object_index, 5);
        assert_eq!(
            lookup.properties[0].tag,
            ReplayNetworkAttributeTagV1::RigidBody
        );
    }

    #[test]
    fn network_lookup_plan_rejects_duplicate_object_names() {
        let objects = vec!["Engine.Actor".to_string(), "Engine.Actor".to_string()];
        let error = build_replay_network_lookup_tables_v1(&objects, &[])
            .expect_err("duplicate object names are outside admitted evidence");
        assert_error_contains(error, "replay network lookup plan error: malformed");
    }

    #[test]
    fn network_lookup_plan_rejects_duplicate_cache_object_rows() {
        let objects = vec!["Engine.Actor".to_string()];
        let net_cache = vec![
            synthetic_net_cache_entry(0, vec![]),
            synthetic_net_cache_entry(0, vec![]),
        ];
        let error = build_replay_network_lookup_tables_v1(&objects, &net_cache)
            .expect_err("duplicate cache object rows are outside admitted evidence");
        assert_error_contains(error, "duplicate net-cache object index");
    }

    #[test]
    fn network_lookup_plan_rejects_duplicate_local_stream_ids() {
        let objects = vec![
            "Engine.Actor".to_string(),
            "Engine.Actor:DrawScale".to_string(),
            "Engine.Actor:bHidden".to_string(),
        ];
        let net_cache = vec![synthetic_net_cache_entry(0, vec![(7, 1), (7, 2)])];
        let error = build_replay_network_lookup_tables_v1(&objects, &net_cache)
            .expect_err("duplicate local stream ids are outside admitted evidence");
        assert_error_contains(error, "duplicate stream id 7");
    }

    #[test]
    fn network_lookup_plan_rejects_out_of_bounds_property_object() {
        let objects = vec!["Engine.Actor".to_string()];
        let net_cache = vec![synthetic_net_cache_entry(0, vec![(1, 99)])];
        let error = build_replay_network_lookup_tables_v1(&objects, &net_cache)
            .expect_err("property object index must stay in bounds");
        assert_error_contains(error, "net-cache property object index 99");
    }

    #[test]
    fn network_lookup_plan_preserves_missing_cache_for_root_without_parent() {
        let objects = vec!["Core.Object".to_string()];
        let (spawns, lookups) = build_replay_network_lookup_tables_v1(&objects, &[])
            .expect("root-only object table should remain structurally valid");
        assert_eq!(spawns, vec![ReplayNetworkSpawnTrajectoryV1::None]);
        assert_eq!(lookups, vec![None]);
    }
'''

last = text.rfind('\n}')
if last < 0:
    raise SystemExit('R3.13 tests module closing brace not found')
text = text[:last] + tests + text[last:]
path.write_text(text, encoding='utf-8')
print('PASS: applied bounded R3.13 network lookup-plan patch')
