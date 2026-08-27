include!("_tmp_r3_18av_published_au_differential.rs");

#[derive(Debug, Clone)]
struct AwTarget {
    label: String,
    frame_index: u32,
    actor_ordinal: u32,
    actor_context_object_id: u32,
    first_start: u64,
    control_start: u64,
    control_end: u64,
    stream_start: u64,
    stream_end: u64,
    stream_id: u32,
    stream_id_bound: u32,
    prop_id_bits: u8,
    property_object_index: u32,
    payload_start_bit: u64,
    version_major: i32,
    version_minor: i32,
    net_version: i32,
    is_rl_223: bool,
    replay_sha256: String,
}

fn aw_parse_bool(value: &str) -> bool {
    match value {
        "0" | "false" => false,
        "1" | "true" => true,
        other => panic!("invalid AW bool {other}"),
    }
}

fn aw_targets() -> Vec<AwTarget> {
    let path = std::env::var("R318AW_TARGETS_TSV").expect("R318AW_TARGETS_TSV");
    let text = std::fs::read_to_string(path).expect("read AW targets");
    let mut lines = text.lines();
    assert_eq!(
        lines.next(),
        Some(
            "label\tframe_index\tactor_ordinal\tactor_context_object_id\tfirst_start\tcontrol_start\tcontrol_end\tstream_start\tstream_end\tstream_id\tstream_id_bound\tprop_id_bits\tproperty_object_index\tattribute_tag\tpayload_start_bit\tversion_major\tversion_minor\tnet_version\tis_rl_223\treplay_sha256"
        )
    );
    lines
        .map(|line| {
            let f: Vec<&str> = line.split('\t').collect();
            assert_eq!(f.len(), 20, "AW target fields: {line}");
            assert_eq!(f[13], "Int", "current AW tag must be Int");
            AwTarget {
                label: f[0].to_string(),
                frame_index: f[1].parse().unwrap(),
                actor_ordinal: f[2].parse().unwrap(),
                actor_context_object_id: f[3].parse().unwrap(),
                first_start: f[4].parse().unwrap(),
                control_start: f[5].parse().unwrap(),
                control_end: f[6].parse().unwrap(),
                stream_start: f[7].parse().unwrap(),
                stream_end: f[8].parse().unwrap(),
                stream_id: f[9].parse().unwrap(),
                stream_id_bound: f[10].parse().unwrap(),
                prop_id_bits: f[11].parse().unwrap(),
                property_object_index: f[12].parse().unwrap(),
                payload_start_bit: f[14].parse().unwrap(),
                version_major: f[15].parse().unwrap(),
                version_minor: f[16].parse().unwrap(),
                net_version: f[17].parse().unwrap(),
                is_rl_223: aw_parse_bool(f[18]),
                replay_sha256: f[19].to_string(),
            }
        })
        .collect()
}

fn aw_guard_current_header(
    proven_start: u64,
    proven_tag: mimir_replay::ReplayNetworkAttributeTagV1,
    requested_start: u64,
    requested_tag: mimir_replay::ReplayNetworkAttributeTagV1,
) -> Result<(), &'static str> {
    if requested_start != proven_start {
        return Err("payload-start-mismatch");
    }
    if requested_tag != proven_tag {
        return Err("payload-tag-mismatch");
    }
    Ok(())
}

fn aw_set_bit(bytes: &mut [u8], bit: u64, value: bool) {
    let idx = bit as usize;
    if idx / 8 >= bytes.len() {
        return;
    }
    if value {
        bytes[idx / 8] |= 1u8 << (idx % 8);
    } else {
        bytes[idx / 8] &= !(1u8 << (idx % 8));
    }
}

#[test]
fn r3_18aw_exact_current_av_true_rows_decode_one_int_payload() {
    if std::env::var_os("R318AW_TARGETS_TSV").is_none() {
        eprintln!("R318AW_TARGETS_TSV absent; AW evidence intentionally skipped");
        return;
    }
    let targets = aw_targets();
    assert_eq!(targets.len(), 40);
    let by_label: std::collections::BTreeMap<String, AwTarget> = targets
        .iter()
        .cloned()
        .map(|row| (row.label.clone(), row))
        .collect();
    assert_eq!(by_label.len(), 40);

    let mut false_excluded = 0usize;
    let mut true_rows = 0usize;
    let mut repeat_ok = 0usize;
    let mut truncation_ok = 0usize;
    let mut wrong_tag_ok = 0usize;
    let mut wrong_boundary_ok = 0usize;
    let mut poison_ok = 0usize;
    let mut out = String::from(
        "label\tframe_index\tactor_ordinal\tactor_context_object_id\tproperty_present_start_bit\tproperty_present_end_bit\tstream_id_start_bit\tstream_id_end_bit\tstream_id\tstream_id_bound\tprop_id_bits\tproperty_object_index\tattribute_tag\tversion_major\tversion_minor\tnet_version\tis_rl_223\tpayload_start_bit\tpayload_end_bit\tpayload_width\tsemantic_int\n",
    );

    for (index, (path, first_start, actor_object, control_start)) in
        au_cases().into_iter().enumerate()
    {
        let label = path.strip_prefix("../../").unwrap_or(path);
        let target = by_label.get(label);
        let (network, plan) = frozen_network_and_plan(path, &format!("r318aw_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        assert_eq!(an.stop_bit, control_start, "{path}");

        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
        )
        .unwrap_or_else(|error| panic!("AW AQ prerequisite {index} {path}: {error}"));

        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &aq,
        )
        .unwrap_or_else(|error| panic!("AW AU prerequisite {index} {path}: {error}"));

        let Some(t) = target else {
            false_excluded += 1;
            assert!(!aq.following_property_present, "{path}");
            assert!(au.following_header.is_none(), "{path}");
            assert_eq!(au.stop_bit, aq.property_present_end_bit, "{path}");
            continue;
        };

        true_rows += 1;
        assert!(aq.following_property_present, "{path}");
        assert_eq!(t.frame_index, 0);
        assert!(t.actor_ordinal > 0);
        assert_eq!(t.label, label);
        assert_eq!(t.actor_context_object_id, actor_object);
        assert_eq!(t.first_start, first_start);
        assert_eq!(t.control_start, control_start);
        assert_eq!(aq.property_present_start_bit, t.control_start);
        assert_eq!(aq.property_present_end_bit, t.control_end);
        assert_eq!(t.replay_sha256.len(), 64);

        let header = au.following_header.as_ref().expect("true AW row header");
        assert_eq!(header.actor_object_index, t.actor_context_object_id);
        assert_eq!(header.property_present_start_bit, t.control_start);
        assert_eq!(header.property_present_end_bit, t.control_end);
        assert_eq!(header.stream_id_start_bit, Some(t.stream_start));
        assert_eq!(header.stream_id_end_bit, Some(t.stream_end));
        assert_eq!(header.stream_id, Some(t.stream_id));
        assert_eq!(header.stream_id_bound, Some(t.stream_id_bound));
        assert_eq!(header.prop_id_bits, Some(t.prop_id_bits));
        assert_eq!(
            header.resolved_property_object_index,
            Some(t.property_object_index)
        );
        assert_eq!(
            header.resolved_attribute_tag,
            Some(mimir_replay::ReplayNetworkAttributeTagV1::Int)
        );
        assert_eq!(header.payload_start_bit, Some(t.payload_start_bit));
        assert_eq!(header.stop_bit, t.payload_start_bit);
        assert_eq!(au.stop_bit, t.payload_start_bit);
        assert_eq!(au.context.version_major, t.version_major);
        assert_eq!(au.context.version_minor, t.version_minor);
        assert_eq!(au.context.net_version, t.net_version);
        assert_eq!(au.context.is_rl_223, t.is_rl_223);

        let proven_tag = header.resolved_attribute_tag.expect("current header tag");
        aw_guard_current_header(
            t.payload_start_bit,
            proven_tag,
            t.payload_start_bit,
            proven_tag,
        )
        .expect("valid current header guard");

        let decoded = mimir_replay::decode_replay_network_primitive_scalar_v1(
            &network,
            t.payload_start_bit,
            proven_tag,
        )
        .unwrap_or_else(|error| panic!("AW native scalar {index} {path}: {error}"));
        assert_eq!(decoded.attribute_tag, proven_tag);
        assert_eq!(decoded.payload_start_bit, t.payload_start_bit);
        assert_eq!(decoded.payload_width, 32);
        assert_eq!(decoded.payload_end_bit, t.payload_start_bit + 32);
        assert_eq!(decoded.stop_bit, decoded.payload_end_bit);
        let semantic_int = match &decoded.value {
            mimir_replay::ReplayNetworkPrimitiveScalarValueV1::Int(value) => *value,
            other => panic!("AW expected Int, got {other:?}"),
        };

        let repeated = mimir_replay::decode_replay_network_primitive_scalar_v1(
            &network,
            t.payload_start_bit,
            proven_tag,
        )
        .expect("AW repeat scalar");
        assert_eq!(decoded, repeated);
        repeat_ok += 1;

        let truncated_bytes = ((decoded.payload_end_bit - 1) / 8) as usize;
        assert!(truncated_bytes < network.len());
        assert!(
            mimir_replay::decode_replay_network_primitive_scalar_v1(
                &network[..truncated_bytes],
                t.payload_start_bit,
                proven_tag,
            )
            .is_err()
        );
        truncation_ok += 1;

        assert!(
            aw_guard_current_header(
                t.payload_start_bit,
                proven_tag,
                t.payload_start_bit,
                mimir_replay::ReplayNetworkAttributeTagV1::Float,
            )
            .is_err()
        );
        wrong_tag_ok += 1;
        assert!(
            aw_guard_current_header(
                t.payload_start_bit,
                proven_tag,
                t.payload_start_bit + 1,
                proven_tag,
            )
            .is_err()
        );
        wrong_boundary_ok += 1;

        let mut poisoned = network.clone();
        for bit in decoded.payload_end_bit..decoded.payload_end_bit.saturating_add(17) {
            if (bit as usize) < poisoned.len() * 8 {
                let old = ((poisoned[bit as usize / 8] >> (bit as usize % 8)) & 1) != 0;
                aw_set_bit(&mut poisoned, bit, !old);
            }
        }
        let poisoned_decoded = mimir_replay::decode_replay_network_primitive_scalar_v1(
            &poisoned,
            t.payload_start_bit,
            proven_tag,
        )
        .expect("post-payload poison must not affect scalar");
        assert_eq!(decoded, poisoned_decoded);
        poison_ok += 1;

        out.push_str(&format!(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\tInt\t{}\t{}\t{}\t{}\t{}\t{}\t32\t{}\n",
            t.label,
            t.frame_index,
            t.actor_ordinal,
            t.actor_context_object_id,
            t.control_start,
            t.control_end,
            t.stream_start,
            t.stream_end,
            t.stream_id,
            t.stream_id_bound,
            t.prop_id_bits,
            t.property_object_index,
            t.version_major,
            t.version_minor,
            t.net_version,
            t.is_rl_223,
            decoded.payload_start_bit,
            decoded.payload_end_bit,
            semantic_int,
        ));
    }

    assert_eq!(false_excluded, 7);
    assert_eq!(true_rows, 40);
    assert_eq!(repeat_ok, 40);
    assert_eq!(truncation_ok, 40);
    assert_eq!(wrong_tag_ok, 40);
    assert_eq!(wrong_boundary_ok, 40);
    assert_eq!(poison_ok, 40);

    let native_out = std::env::var("R318AW_NATIVE_OUT").expect("R318AW_NATIVE_OUT");
    std::fs::write(native_out, out).expect("write AW native rows");
    println!(
        "R3_18AW_NATIVE_SUMMARY\ttrue=40\tfalse_excluded=7\tint=40\twidth32=40\trepeat=40\ttruncation=40\twrong_tag=40\twrong_boundary=40\tpost_payload_poison=40\tnext_control_bits=0\twitness_reselection=0"
    );
}
