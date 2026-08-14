use mimir_replay::{
    decode_replay_network_existing_actor_first_property_header_v1,
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1,
};
use std::path::PathBuf;

fn sample_001_lookup_plan() -> ReplayNetworkLookupPlanV1 {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../external_fixtures/sample_001.replay");
    let bytes = std::fs::read(&path).expect("read sample_001.replay");
    let input = ReplayInput::Memory {
        label: "r316b_sample_001_context".to_string(),
        bytes,
    };
    MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&input)
        .expect("materialize admitted lookup plan")
}

#[test]
fn r3_16b_property_absent_stops_after_one_bit_without_lookup_or_payload() {
    let plan = sample_001_lookup_plan();
    let zero_tail = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x00], 0, 47, &plan,
    )
    .expect("property absent header");
    let one_tail = decode_replay_network_existing_actor_first_property_header_v1(
        &[0xfe], 0, 47, &plan,
    )
    .expect("property absent header with opaque following bits");

    assert_eq!(zero_tail, one_tail);
    assert!(!zero_tail.property_present);
    assert_eq!(zero_tail.property_present_start_bit, 0);
    assert_eq!(zero_tail.property_present_end_bit, 1);
    assert_eq!(zero_tail.stream_id, None);
    assert_eq!(zero_tail.payload_start_bit, None);
    assert_eq!(zero_tail.stop_bit, 1);
}

#[test]
fn r3_16b_property_present_uses_canonical_bounded_stream_and_resolves_inherited_property() {
    let plan = sample_001_lookup_plan();
    let header = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x3d, 0x00], 0, 47, &plan,
    )
    .expect("stream 30 should resolve for sample_001 actor object 47");

    assert!(header.property_present);
    assert_eq!(header.property_present_start_bit, 0);
    assert_eq!(header.property_present_end_bit, 1);
    assert_eq!(header.stream_id, Some(30));
    assert_eq!(header.stream_id_bound, Some(38));
    assert_eq!(header.prop_id_bits, Some(5));
    assert_eq!(header.stream_id_start_bit, Some(1));
    assert_eq!(header.stream_id_end_bit, Some(6));
    assert_eq!(header.resolved_property_object_index, Some(36));
    assert_eq!(
        header.resolved_property_object_name.as_deref(),
        Some("Engine.GameReplicationInfo:GameClass")
    );
    assert_eq!(
        header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::ActiveActor)
    );
    assert_eq!(header.payload_start_bit, Some(6));
    assert_eq!(header.stop_bit, 6);
}

#[test]
fn r3_16b_payload_bits_are_opaque_and_do_not_change_header_result() {
    let plan = sample_001_lookup_plan();
    let payload_zero = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x3d, 0x00], 0, 47, &plan,
    )
    .expect("header before zero payload bit");
    let payload_one = decode_replay_network_existing_actor_first_property_header_v1(
        &[0xfd, 0xff], 0, 47, &plan,
    )
    .expect("header before one payload bit");

    assert_eq!(payload_zero, payload_one);
    assert_eq!(payload_zero.payload_start_bit, Some(6));
}

#[test]
fn r3_16b_unresolved_stream_fails_closed() {
    let mut plan = sample_001_lookup_plan();
    let actor_lookup = plan
        .object_lookups
        .get_mut(47)
        .and_then(Option::as_mut)
        .expect("sample_001 actor object 47 lookup");
    assert!(actor_lookup.properties.iter().any(|property| property.stream_id == 0));
    actor_lookup.properties.retain(|property| property.stream_id != 0);

    let error = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x01], 0, 47, &plan,
    )
    .expect_err("synthetically unmapped stream zero must fail closed");

    assert!(format!("{error}").contains("unresolved-stream-id"));
}

#[test]
fn r3_16b_truncation_at_property_present_fails() {
    let plan = sample_001_lookup_plan();
    let error = decode_replay_network_existing_actor_first_property_header_v1(
        &[], 0, 47, &plan,
    )
    .expect_err("missing property-present bit must fail");

    assert!(format!("{error}").contains("insufficient-bits"));
}

#[test]
fn r3_16b_truncation_inside_bounded_stream_low_bits_fails() {
    let plan = sample_001_lookup_plan();
    let error = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x10], 4, 47, &plan,
    )
    .expect_err("only three stream low bits remain after property-present");

    assert!(format!("{error}").contains("insufficient-bits"));
}

#[test]
fn r3_16b_truncation_at_required_bounded_discriminator_fails() {
    let plan = sample_001_lookup_plan();
    let error = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x04], 2, 47, &plan,
    )
    .expect_err("stream zero low bits require a discriminator that is absent");

    assert!(format!("{error}").contains("insufficient-bits"));
}

#[test]
fn r3_16b_repeatability_is_exact() {
    let plan = sample_001_lookup_plan();
    let first = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x3d, 0xaa], 0, 47, &plan,
    )
    .expect("first decode");
    let second = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x3d, 0xaa], 0, 47, &plan,
    )
    .expect("second decode");

    assert_eq!(first, second);
}
