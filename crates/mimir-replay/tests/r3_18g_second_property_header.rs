use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorSinglePrimitivePropertyV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn sample_001_lookup_plan() -> ReplayNetworkLookupPlanV1 {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let bytes = std::fs::read(&path).expect("read sample_001.replay");
    let input = ReplayInput::Memory {
        label: "r318g_sample_001_context".to_string(),
        bytes,
    };
    MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&input)
        .expect("materialize admitted lookup plan")
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

fn write_bits(bytes: &mut [u8], start: usize, width: usize, value: u64) {
    for bit in 0..width {
        set_bit(bytes, start + bit, ((value >> bit) & 1) != 0);
    }
}

fn packet(
    first_start: usize,
    first_stream: u64,
    first_stream_width: usize,
    first_raw: u64,
    next_present: bool,
    second_stream: Option<(u64, usize)>,
    trailing_bits: usize,
) -> Vec<u8> {
    let first_payload_start = first_start + 1 + first_stream_width;
    let first_stop = first_payload_start + 32;
    let second_header_width = if next_present {
        1 + second_stream.expect("present second header needs stream").1
    } else {
        1
    };
    let total_bits = first_stop + second_header_width + trailing_bits;
    let mut bytes = vec![0u8; total_bits.div_ceil(8)];
    set_bit(&mut bytes, first_start, true);
    write_bits(
        &mut bytes,
        first_start + 1,
        first_stream_width,
        first_stream,
    );
    write_bits(&mut bytes, first_payload_start, 32, first_raw);
    set_bit(&mut bytes, first_stop, next_present);
    if next_present {
        let (stream, width) = second_stream.expect("present second header needs stream");
        write_bits(&mut bytes, first_stop + 1, width, stream);
    }
    bytes
}

fn first_only_packet(
    first_start: usize,
    first_stream: u64,
    first_stream_width: usize,
    first_raw: u64,
) -> Vec<u8> {
    let payload_start = first_start + 1 + first_stream_width;
    let stop = payload_start + 32;
    let mut bytes = vec![0u8; stop.div_ceil(8)];
    set_bit(&mut bytes, first_start, true);
    write_bits(
        &mut bytes,
        first_start + 1,
        first_stream_width,
        first_stream,
    );
    write_bits(&mut bytes, payload_start, 32, first_raw);
    bytes
}

fn retag_stream(
    plan: &mut ReplayNetworkLookupPlanV1,
    actor_object: usize,
    stream_id: u32,
    tag: ReplayNetworkAttributeTagV1,
) -> u32 {
    let lookup = plan.object_lookups[actor_object]
        .as_mut()
        .expect("actor lookup must exist");
    let property = lookup
        .properties
        .iter_mut()
        .find(|property| property.stream_id == stream_id)
        .expect("stream must resolve");
    property.tag = tag;
    property.object_index
}

fn first_property(
    bytes: &[u8],
    start: usize,
    actor_object: u32,
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorSinglePrimitivePropertyV1 {
    decode_replay_network_existing_actor_single_primitive_property_v1(
        bytes,
        start as u64,
        actor_object,
        plan,
    )
    .expect("first R3.18B primitive property should decode")
}

#[test]
fn false_terminator_returns_none_and_performs_no_lookup_after_control() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(2, 30, 5, 62, false, None, 0);
    let first = first_property(&bytes, 2, 47, &plan);
    assert_eq!(first.stop_bit, 40);

    plan.object_lookups[47] = None;
    let decoded =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &bytes, &first, &plan,
        )
        .expect("false terminator must return before lookup");
    assert!(!decoded.control.next_property_present);
    assert_eq!(decoded.control.property_present_start_bit, 40);
    assert_eq!(decoded.control.property_present_end_bit, 41);
    assert_eq!(decoded.control.stop_bit, 41);
    assert!(decoded.second_header.is_none());
    assert_eq!(decoded.stop_bit, 41);
}

#[test]
fn continuation_int_resolves_one_second_header_and_stops_at_payload_start() {
    let mut plan = sample_001_lookup_plan();
    let property_object = retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(0, 30, 5, 62, true, Some((30, 5)), 16);
    let first = first_property(&bytes, 0, 47, &plan);
    assert_eq!(first.stop_bit, 38);

    let decoded =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &bytes, &first, &plan,
        )
        .expect("Int second header should compose");
    let header = decoded.second_header.as_ref().expect("second header");
    assert!(decoded.control.next_property_present);
    assert_eq!(decoded.control.property_present_start_bit, 38);
    assert_eq!(decoded.control.property_present_end_bit, 39);
    assert_eq!(header.property_present_start_bit, 38);
    assert_eq!(header.property_present_end_bit, 39);
    assert_eq!(header.actor_object_index, 47);
    assert_eq!(header.stream_id, Some(30));
    assert_eq!(header.stream_id_bound, Some(38));
    assert_eq!(header.prop_id_bits, Some(5));
    assert_eq!(header.resolved_property_object_index, Some(property_object));
    assert_eq!(
        header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Int)
    );
    assert_eq!(header.payload_start_bit, Some(44));
    assert_eq!(header.stop_bit, 44);
    assert_eq!(decoded.stop_bit, 44);
}

#[test]
fn continuation_string_is_header_only_and_needs_no_string_payload() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(0, 30, 5, 7, true, Some((30, 5)), 0);
    let first = first_property(&bytes, 0, 47, &plan);
    let property_object = retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::String);

    let decoded =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &bytes, &first, &plan,
        )
        .expect("String must be admitted only as a resolved second-header tag");
    let header = decoded.second_header.as_ref().expect("second header");
    assert_eq!(header.resolved_property_object_index, Some(property_object));
    assert_eq!(
        header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::String)
    );
    assert_eq!(header.payload_start_bit, Some(44));
    assert_eq!(decoded.stop_bit, 44);
}

#[test]
fn aligned_and_unaligned_second_header_starts_preserve_exact_coordinates() {
    for (first_start, expected_second_start) in [(2usize, 40u64), (3usize, 41u64)] {
        let mut plan = sample_001_lookup_plan();
        retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
        let bytes = packet(first_start, 30, 5, 62, true, Some((30, 5)), 9);
        let first = first_property(&bytes, first_start, 47, &plan);
        let decoded =
            decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                &bytes, &first, &plan,
            )
            .unwrap();
        let header = decoded.second_header.unwrap();
        assert_eq!(
            decoded.control.property_present_start_bit,
            expected_second_start
        );
        assert_eq!(header.property_present_start_bit, expected_second_start);
        assert_eq!(header.property_present_end_bit, expected_second_start + 1);
        assert_eq!(decoded.stop_bit, expected_second_start + 6);
    }
}

#[test]
fn r3_18f_shaped_actor98_boundary_reuses_exact_lookup_shape() {
    let plan = sample_001_lookup_plan();
    let bytes = packet(0, 27, 6, 62, true, Some((27, 6)), 8);
    let first = first_property(&bytes, 0, 98, &plan);
    assert_eq!(first.stop_bit, 39);

    let decoded =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &bytes, &first, &plan,
        )
        .expect("R3.18F-shaped actor 98 boundary should compose");
    let header = decoded.second_header.unwrap();
    assert_eq!(decoded.control.property_present_start_bit, 39);
    assert_eq!(header.stream_id, Some(27));
    assert_eq!(header.stream_id_bound, Some(67));
    assert_eq!(header.prop_id_bits, Some(6));
    assert_eq!(header.resolved_property_object_index, Some(55));
    assert_eq!(
        header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Int)
    );
    assert_eq!(header.payload_start_bit, Some(46));
    assert_eq!(decoded.stop_bit, 46);
}

#[test]
fn bits_at_and_after_second_payload_start_do_not_affect_header_result() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let clean = packet(3, 30, 5, 62, true, Some((30, 5)), 24);
    let first = first_property(&clean, 3, 47, &plan);
    let clean_result =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &clean, &first, &plan,
        )
        .unwrap();

    let mut poisoned = clean.clone();
    let poison_start = usize::try_from(clean_result.stop_bit).unwrap();
    for offset in 0..16 {
        set_bit(&mut poisoned, poison_start + offset, offset % 2 == 0);
    }
    let poisoned_result =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &poisoned, &first, &plan,
        )
        .unwrap();
    assert_eq!(poisoned_result, clean_result);
}

#[test]
fn missing_control_bit_rejects_atomically() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = first_only_packet(2, 30, 5, 62);
    assert_eq!(bytes.len() * 8, 40);
    let first = first_property(&bytes, 2, 47, &plan);
    assert_eq!(first.stop_bit, 40);

    let error =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &bytes, &first, &plan,
        )
        .expect_err("missing R3.18D control bit must reject");
    assert!(error.to_string().contains("insufficient-bits"));
}

#[test]
fn truncation_inside_second_stream_header_rejects_atomically() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let full = packet(7, 30, 5, 62, true, Some((30, 5)), 0);
    let first = first_property(&full, 7, 47, &plan);
    assert_eq!(first.stop_bit, 45);
    let mut truncated = full.clone();
    truncated.truncate(6);
    assert_eq!(truncated.len() * 8, 48);

    let error =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &truncated, &first, &plan,
        )
        .expect_err("partial second stream id must reject");
    assert!(error.to_string().contains("insufficient-bits"));
}

#[test]
fn unresolved_second_stream_rejects_without_payload_composition() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(0, 30, 5, 62, true, Some((30, 5)), 8);
    let first = first_property(&bytes, 0, 47, &plan);
    plan.object_lookups[47]
        .as_mut()
        .unwrap()
        .properties
        .retain(|property| property.stream_id != 30);

    let error =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &bytes, &first, &plan,
        )
        .expect_err("unresolved second stream must reject");
    assert!(error.to_string().contains("unresolved-stream-id"));
}

#[test]
fn tag_outside_exact_int_string_set_rejects_before_second_payload() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(0, 30, 5, 62, true, Some((30, 5)), 0);
    let first = first_property(&bytes, 0, 47, &plan);
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Float);

    let error =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &bytes, &first, &plan,
        )
        .expect_err("Float second-header context is outside R3.18F observed set");
    assert!(error.to_string().contains("unsupported-second-header-tag"));
}

#[test]
fn result_is_exactly_repeatable() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(3, 30, 5, 62, true, Some((30, 5)), 8);
    let first = first_property(&bytes, 3, 47, &plan);
    let one = decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
        &bytes, &first, &plan,
    )
    .unwrap();
    let two = decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
        &bytes, &first, &plan,
    )
    .unwrap();
    assert_eq!(one, two);
}
