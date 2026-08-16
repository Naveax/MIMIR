use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1,
    ReplayNetworkExistingActorSinglePrimitivePropertyV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_property_control_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn sample_001_lookup_plan() -> ReplayNetworkLookupPlanV1 {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let bytes = std::fs::read(&path).expect("read sample_001.replay");
    let input = ReplayInput::Memory {
        label: "r318d_sample_001_context".to_string(),
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
    property_start: usize,
    stream_id: u64,
    stream_width: usize,
    payload_width: usize,
    raw: u64,
    next_property_present: Option<bool>,
    trailing_bits: usize,
) -> Vec<u8> {
    let payload_start = property_start + 1 + stream_width;
    let payload_end = payload_start + payload_width;
    let control_width = if next_property_present.is_some() {
        1
    } else {
        0
    };
    let total_bits = payload_end + control_width + trailing_bits;
    let mut bytes = vec![0u8; total_bits.div_ceil(8)];
    set_bit(&mut bytes, property_start, true);
    write_bits(&mut bytes, property_start + 1, stream_width, stream_id);
    write_bits(&mut bytes, payload_start, payload_width, raw);
    if let Some(value) = next_property_present {
        set_bit(&mut bytes, payload_end, value);
    }
    bytes
}

fn retag_stream(
    plan: &mut ReplayNetworkLookupPlanV1,
    actor_object: usize,
    stream_id: u32,
    tag: ReplayNetworkAttributeTagV1,
) {
    let lookup = plan.object_lookups[actor_object]
        .as_mut()
        .expect("actor lookup must exist");
    let property = lookup
        .properties
        .iter_mut()
        .find(|property| property.stream_id == stream_id)
        .expect("stream must resolve");
    property.tag = tag;
}

fn first_property(
    bytes: &[u8],
    property_start: usize,
    actor_object: u32,
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorSinglePrimitivePropertyV1 {
    decode_replay_network_existing_actor_single_primitive_property_v1(
        bytes,
        property_start as u64,
        actor_object,
        plan,
    )
    .expect("first R3.18B property should decode")
}

fn control(
    bytes: &[u8],
    first: &ReplayNetworkExistingActorSinglePrimitivePropertyV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1 {
    decode_replay_network_existing_actor_after_first_primitive_property_control_v1(bytes, first)
        .expect("R3.18D control bit should decode")
}

#[test]
fn r3_18c_float_terminator_shape_reads_exactly_false_and_stops_one_bit_later() {
    let plan = sample_001_lookup_plan();
    let bytes = packet(0, 17, 5, 32, 1_092_616_192, Some(false), 9);
    let first = first_property(&bytes, 0, 344, &plan);
    assert_eq!(
        first.header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Float)
    );
    assert_eq!(first.stop_bit, 38);

    let decoded = control(&bytes, &first);
    assert!(!decoded.next_property_present);
    assert_eq!(decoded.property_present_start_bit, 38);
    assert_eq!(decoded.property_present_end_bit, 39);
    assert_eq!(decoded.stop_bit, 39);
}

#[test]
fn r3_18c_int_62_continuation_shape_reads_exactly_true_and_stops_one_bit_later() {
    let plan = sample_001_lookup_plan();
    let bytes = packet(0, 27, 6, 32, 62, Some(true), 9);
    let first = first_property(&bytes, 0, 98, &plan);
    assert_eq!(
        first.header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Int)
    );
    assert_eq!(first.stop_bit, 39);

    let decoded = control(&bytes, &first);
    assert!(decoded.next_property_present);
    assert_eq!(decoded.property_present_start_bit, 39);
    assert_eq!(decoded.property_present_end_bit, 40);
    assert_eq!(decoded.stop_bit, 40);
}

#[test]
fn aligned_and_unaligned_first_property_ends_preserve_exact_control_coordinates() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);

    for (property_start, expected_start, next_value) in [(2usize, 40u64, false), (3, 41, true)] {
        let bytes = packet(property_start, 30, 5, 32, 7, Some(next_value), 9);
        let first = first_property(&bytes, property_start, 47, &plan);
        assert_eq!(first.stop_bit, expected_start);
        let decoded = control(&bytes, &first);
        assert_eq!(decoded.next_property_present, next_value);
        assert_eq!(decoded.property_present_start_bit, expected_start);
        assert_eq!(decoded.property_present_end_bit, expected_start + 1);
        assert_eq!(decoded.stop_bit, expected_start + 1);
    }
}

#[test]
fn bits_after_control_stop_do_not_affect_result() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let clean = packet(3, 30, 5, 32, 62, Some(true), 17);
    let first = first_property(&clean, 3, 47, &plan);
    let clean_control = control(&clean, &first);

    let mut poisoned = clean.clone();
    let poison_start = usize::try_from(clean_control.stop_bit).unwrap();
    for offset in 0..8 {
        set_bit(&mut poisoned, poison_start + offset, offset % 2 == 0);
    }
    let poisoned_control = control(&poisoned, &first);
    assert_eq!(poisoned_control, clean_control);
}

#[test]
fn missing_next_property_bit_rejects_atomically() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(2, 30, 5, 32, 62, None, 0);
    assert_eq!(bytes.len() * 8, 40);
    let first = first_property(&bytes, 2, 47, &plan);
    assert_eq!(first.stop_bit, 40);

    let error = decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
        &bytes, &first,
    )
    .expect_err("missing next property_present bit must fail");
    assert!(error.to_string().contains("insufficient-bits"));
}

#[test]
fn malformed_first_property_boundary_is_rejected_before_control_read() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(3, 30, 5, 32, 62, Some(true), 9);
    let mut first = first_property(&bytes, 3, 47, &plan);
    first.stop_bit += 1;

    let error = decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
        &bytes, &first,
    )
    .expect_err("malformed R3.18B boundary must fail before one-bit read");
    assert!(error.to_string().contains("boundary-mismatch"));
}

#[test]
fn control_result_is_exactly_repeatable() {
    let plan = sample_001_lookup_plan();
    let bytes = packet(0, 27, 6, 32, 62, Some(true), 9);
    let first = first_property(&bytes, 0, 98, &plan);
    let first_read = control(&bytes, &first);
    let second_read = control(&bytes, &first);
    assert_eq!(first_read, second_read);
}
