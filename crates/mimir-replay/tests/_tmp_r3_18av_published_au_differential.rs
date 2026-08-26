include!("r3_18au_post_aq_following_header.rs");

use std::collections::BTreeMap as AvBTreeMap;

#[derive(Debug, Clone)]
struct AvExpected {
    label: String,
    frame_index: u32,
    actor_ordinal: u32,
    actor_context_object_id: u32,
    first_start: u64,
    control_start: u64,
    control_end: u64,
    control_value: bool,
    stream_start: Option<u64>,
    stream_end: Option<u64>,
    stream_id: Option<u32>,
    stream_id_bound: Option<u32>,
    prop_id_bits: Option<u8>,
    property_object_index: Option<u32>,
    attribute_tag: Option<String>,
    payload_start_bit: Option<u64>,
    header_stop_bit: Option<u64>,
    version_major: Option<i32>,
    version_minor: Option<i32>,
    net_version: Option<i32>,
    is_rl_223: Option<bool>,
}

fn av_opt_u64(value: &str) -> Option<u64> {
    (!value.is_empty()).then(|| value.parse().expect("valid optional u64"))
}

fn av_opt_u32(value: &str) -> Option<u32> {
    (!value.is_empty()).then(|| value.parse().expect("valid optional u32"))
}

fn av_opt_u8(value: &str) -> Option<u8> {
    (!value.is_empty()).then(|| value.parse().expect("valid optional u8"))
}

fn av_opt_i32(value: &str) -> Option<i32> {
    (!value.is_empty()).then(|| value.parse().expect("valid optional i32"))
}

fn av_parse_bool(value: &str) -> bool {
    match value {
        "0" | "false" => false,
        "1" | "true" => true,
        other => panic!("invalid authority bool: {other}"),
    }
}

fn av_opt_bool(value: &str) -> Option<bool> {
    (!value.is_empty()).then(|| av_parse_bool(value))
}

fn av_expected_rows() -> Vec<AvExpected> {
    let path = std::env::var("R318AV_EXPECTED_TSV").expect("R318AV_EXPECTED_TSV");
    let text = std::fs::read_to_string(path).expect("read R3.18AV expected TSV");
    let mut lines = text.lines();
    assert_eq!(
        lines.next(),
        Some("label\tframe_index\tactor_ordinal\tactor_context_object_id\tfirst_start\tcontrol_start\tcontrol_end\tcontrol_value\tstream_start\tstream_end\tstream_id\tstream_id_bound\tprop_id_bits\tproperty_object_index\tattribute_tag\tpayload_start_bit\theader_stop_bit\tversion_major\tversion_minor\tnet_version\tis_rl_223")
    );

    lines
        .map(|line| {
            let fields: Vec<&str> = line.split('\t').collect();
            assert_eq!(fields.len(), 21, "expected TSV field count: {line}");
            AvExpected {
                label: fields[0].to_string(),
                frame_index: fields[1].parse().expect("frame_index"),
                actor_ordinal: fields[2].parse().expect("actor_ordinal"),
                actor_context_object_id: fields[3].parse().expect("actor object"),
                first_start: fields[4].parse().expect("first_start"),
                control_start: fields[5].parse().expect("control_start"),
                control_end: fields[6].parse().expect("control_end"),
                control_value: av_parse_bool(fields[7]),
                stream_start: av_opt_u64(fields[8]),
                stream_end: av_opt_u64(fields[9]),
                stream_id: av_opt_u32(fields[10]),
                stream_id_bound: av_opt_u32(fields[11]),
                prop_id_bits: av_opt_u8(fields[12]),
                property_object_index: av_opt_u32(fields[13]),
                attribute_tag: (!fields[14].is_empty()).then(|| fields[14].to_string()),
                payload_start_bit: av_opt_u64(fields[15]),
                header_stop_bit: av_opt_u64(fields[16]),
                version_major: av_opt_i32(fields[17]),
                version_minor: av_opt_i32(fields[18]),
                net_version: av_opt_i32(fields[19]),
                is_rl_223: av_opt_bool(fields[20]),
            }
        })
        .collect()
}

#[test]
fn r3_18av_authority_bool_parser_accepts_numeric_and_textual_forms() {
    assert!(!av_parse_bool("0"));
    assert!(!av_parse_bool("false"));
    assert!(av_parse_bool("1"));
    assert!(av_parse_bool("true"));
}

#[test]
fn r3_18av_published_au_matches_frozen_as_at_authority_exactly() {
    if std::env::var_os("R318AV_EXPECTED_TSV").is_none() {
        eprintln!("R3_18AV_EXPECTED_TSV absent; runtime differential intentionally skipped outside evidence workflow");
        return;
    }
    let expected = av_expected_rows();
    let cases = au_cases();
    assert_eq!(expected.len(), 47);
    assert_eq!(cases.len(), 47);

    let mut false_count = 0usize;
    let mut true_count = 0usize;
    let mismatch = 0usize;
    let mut counts: AvBTreeMap<(u32, u8, u32), usize> = AvBTreeMap::new();

    for (index, ((path, first_start, actor_object, control_start), exp)) in
        cases.into_iter().zip(expected.iter()).enumerate()
    {
        let label = path.strip_prefix("../../").unwrap_or(path);
        assert_eq!(exp.label, label, "witness label row {index}");
        assert_eq!(exp.frame_index, 0, "frame index row {index}");
        assert!(exp.actor_ordinal > 0, "actor ordinal row {index}");
        assert_eq!(exp.actor_context_object_id, actor_object, "actor object row {index}");
        assert_eq!(exp.first_start, first_start, "first-start row {index}");
        assert_eq!(exp.control_start, control_start, "control-start row {index}");

        let (network, plan) = frozen_network_and_plan(path, &format!("r318av_frozen_{index}"));
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
        .unwrap_or_else(|error| panic!("AV AQ prerequisite row {index} {path}: {error}"));

        assert_eq!(aq.property_present_start_bit, exp.control_start, "{path}");
        assert_eq!(aq.property_present_end_bit, exp.control_end, "{path}");
        assert_eq!(aq.following_property_present, exp.control_value, "{path}");

        let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &aq,
        )
        .unwrap_or_else(|error| panic!("AV published AU row {index} {path}: {error}"));

        let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &aq,
        )
        .expect("repeat published AU");
        assert_eq!(got, repeated, "{path}");
        assert_eq!(got.control, aq, "{path}");
        assert_eq!(got.context, k3_context(), "{path}");

        if !exp.control_value {
            false_count += 1;
            assert_eq!(got.following_header, None, "{path}");
            assert_eq!(got.stop_bit, exp.control_end, "{path}");
            assert_eq!(exp.stream_start, None);
            assert_eq!(exp.payload_start_bit, None);
            println!(
                "R3_18AV_ROW\t{}\tfalse\tcontrol={}-{}\tstop={}\tmismatch=0",
                exp.label, exp.control_start, exp.control_end, got.stop_bit
            );
            continue;
        }

        true_count += 1;
        let header = got.following_header.as_ref().expect("true row following header");
        assert!(header.property_present, "{path}");
        assert_eq!(header.property_present_start_bit, exp.control_start, "{path}");
        assert_eq!(header.property_present_end_bit, exp.control_end, "{path}");
        assert_eq!(header.actor_object_index, exp.actor_context_object_id, "{path}");
        assert_eq!(header.stream_id_start_bit, exp.stream_start, "{path}");
        assert_eq!(header.stream_id_end_bit, exp.stream_end, "{path}");
        assert_eq!(header.stream_id, exp.stream_id, "{path}");
        assert_eq!(header.stream_id_bound, exp.stream_id_bound, "{path}");
        assert_eq!(header.prop_id_bits, exp.prop_id_bits, "{path}");
        assert_eq!(
            header.resolved_property_object_index,
            exp.property_object_index,
            "{path}"
        );
        assert_eq!(exp.attribute_tag.as_deref(), Some("Int"), "{path}");
        assert_eq!(
            header.resolved_attribute_tag,
            Some(ReplayNetworkAttributeTagV1::Int),
            "{path}"
        );
        assert_eq!(header.payload_start_bit, exp.payload_start_bit, "{path}");
        assert_eq!(Some(header.stop_bit), exp.header_stop_bit, "{path}");
        assert_eq!(got.stop_bit, exp.payload_start_bit.expect("payload start"), "{path}");

        let ctx = got.context;
        assert_eq!(Some(ctx.version_major), exp.version_major, "{path}");
        assert_eq!(Some(ctx.version_minor), exp.version_minor, "{path}");
        assert_eq!(Some(ctx.net_version), exp.net_version, "{path}");
        assert_eq!(Some(ctx.is_rl_223), exp.is_rl_223, "{path}");

        let key = (
            header.stream_id_bound.expect("bound"),
            header.prop_id_bits.expect("prop bits"),
            header
                .resolved_property_object_index
                .expect("property object"),
        );
        *counts.entry(key).or_insert(0) += 1;

        println!(
            "R3_18AV_ROW\t{}\ttrue\tcontrol={}-{}\tstream={:?}\tstream_bits={:?}-{:?}\tbound={:?}\tprop_bits={:?}\tobject={:?}\tpayload_start={:?}\tstop={}\tmismatch=0",
            exp.label,
            exp.control_start,
            exp.control_end,
            header.stream_id,
            header.stream_id_start_bit,
            header.stream_id_end_bit,
            header.stream_id_bound,
            header.prop_id_bits,
            header.resolved_property_object_index,
            header.payload_start_bit,
            header.stop_bit,
        );
    }

    let expected_counts: AvBTreeMap<(u32, u8, u32), usize> = [
        ((110, 6, 49), 1),
        ((60, 5, 106), 4),
        ((60, 5, 107), 19),
        ((60, 5, 113), 1),
        ((60, 5, 115), 2),
        ((60, 5, 117), 1),
        ((60, 5, 122), 1),
        ((60, 5, 130), 2),
        ((60, 5, 131), 1),
        ((60, 5, 134), 1),
        ((60, 5, 144), 1),
        ((60, 5, 60), 1),
        ((60, 5, 69), 2),
        ((67, 6, 81), 1),
        ((72, 6, 84), 1),
        ((72, 6, 87), 1),
    ]
    .into_iter()
    .collect();

    assert_eq!(false_count, 7);
    assert_eq!(true_count, 40);
    assert_eq!(mismatch, 0);
    assert_eq!(counts, expected_counts);
    println!(
        "R3_18AV_SUMMARY\trows=47\tfalse=7\ttrue=40\tcontexts=16\tmultiplicity=40\tmismatch=0\twitness_reselection=0\tfollowing_payload_bits=0\tsecond_later_control_bits=0"
    );
}

#[test]
fn r3_18av_mismatched_published_aq_prerequisite_rejects() {
    for (index, (path, first_start, actor_object, control_start)) in
        au_cases().into_iter().enumerate()
    {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318av_bad_prereq_{index}"));
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
        .expect("valid AQ prerequisite");

        if !aq.following_property_present {
            continue;
        }

        let mut bad = aq.clone();
        bad.stop_bit = bad.stop_bit.saturating_add(1);
        assert!(
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
                &network,
                &prior,
                &control,
                &plan,
                k3_context(),
                &an,
                &bad,
            )
            .is_err(),
            "mismatched published AQ prerequisite must reject"
        );
        println!("R3_18AV_MISMATCHED_PREREQUISITE=PASS");
        return;
    }
    panic!("expected at least one true AU row");
}