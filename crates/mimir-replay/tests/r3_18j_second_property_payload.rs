use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorSecondPropertyPayloadV1,
    ReplayNetworkExistingActorSinglePrimitivePropertyV1, ReplayNetworkK2DecodeContextV1,
    ReplayNetworkK2ValueV1, ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1,
    ReplayNetworkPrimitiveScalarValueV1, ReplayNetworkTextEncodingV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn sample_plan() -> ReplayNetworkLookupPlanV1 {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let bytes = std::fs::read(path).expect("read sample replay");
    MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&ReplayInput::Memory {
            label: "r318j_sample_context".to_owned(),
            bytes,
        })
        .expect("lookup plan")
}

fn ctx(net_version: i32, is_rl_223: bool) -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version,
        is_rl_223,
    }
}

fn set_bit(bytes: &mut Vec<u8>, position: usize, value: bool) {
    let needed = position / 8 + 1;
    if bytes.len() < needed {
        bytes.resize(needed, 0);
    }
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

fn write_bits(bytes: &mut Vec<u8>, start: usize, width: usize, value: u64) {
    for offset in 0..width {
        set_bit(bytes, start + offset, ((value >> offset) & 1) != 0);
    }
}

fn retag(
    plan: &mut ReplayNetworkLookupPlanV1,
    actor: usize,
    stream: u32,
    tag: ReplayNetworkAttributeTagV1,
) {
    let property = plan.object_lookups[actor]
        .as_mut()
        .expect("actor lookup")
        .properties
        .iter_mut()
        .find(|property| property.stream_id == stream)
        .expect("stream");
    property.tag = tag;
}

fn first_property(
    bytes: &[u8],
    start: usize,
    actor: u32,
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorSinglePrimitivePropertyV1 {
    decode_replay_network_existing_actor_single_primitive_property_v1(
        bytes,
        start as u64,
        actor,
        plan,
    )
    .expect("first property")
}

fn int_packet(
    first_start: usize,
    next_present: bool,
    second_raw: u32,
    trailing_bits: usize,
) -> Vec<u8> {
    let first_stream_width = 5usize;
    let first_payload_start = first_start + 1 + first_stream_width;
    let first_end = first_payload_start + 32;
    let mut bytes = Vec::new();
    set_bit(&mut bytes, first_start, true);
    write_bits(&mut bytes, first_start + 1, first_stream_width, 30);
    write_bits(&mut bytes, first_payload_start, 32, 62);
    set_bit(&mut bytes, first_end, next_present);
    if next_present {
        write_bits(&mut bytes, first_end + 1, 5, 30);
        let second_start = first_end + 6;
        write_bits(&mut bytes, second_start, 32, u64::from(second_raw));
        if trailing_bits > 0 {
            set_bit(&mut bytes, second_start + 32 + trailing_bits - 1, false);
        }
    }
    bytes
}

fn string_packet(first_start: usize, content: &[u8], trailing_bits: usize) -> Vec<u8> {
    let first_payload_start = first_start + 6;
    let first_end = first_payload_start + 32;
    let second_start = first_end + 6;
    let mut bytes = Vec::new();
    set_bit(&mut bytes, first_start, true);
    write_bits(&mut bytes, first_start + 1, 5, 30);
    write_bits(&mut bytes, first_payload_start, 32, 62);
    set_bit(&mut bytes, first_end, true);
    write_bits(&mut bytes, first_end + 1, 5, 30);
    write_bits(&mut bytes, second_start, 32, (content.len() + 1) as u64);
    let mut bit = second_start + 32;
    for byte in content {
        write_bits(&mut bytes, bit, 8, u64::from(*byte));
        bit += 8;
    }
    write_bits(&mut bytes, bit, 8, 0x7f);
    bit += 8;
    if trailing_bits > 0 {
        set_bit(&mut bytes, bit + trailing_bits - 1, false);
    }
    bytes
}

#[test]
fn terminator_returns_none_without_post_control_lookup_or_payload_decode() {
    let mut plan = sample_plan();
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = int_packet(2, false, 0, 0);
    let first = first_property(&bytes, 2, 47, &plan);
    assert_eq!(first.stop_bit, 40);
    plan.object_lookups[47] = None;
    let decoded =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &bytes,
            &first,
            &plan,
            ctx(10, false),
        )
        .expect("terminator");
    assert!(decoded.header_composition.second_header.is_none());
    assert!(decoded.second_payload.is_none());
    assert_eq!(decoded.stop_bit, 41);
}

#[test]
fn int_second_payload_decodes_exact_value_width_and_end_at_unaligned_starts() {
    for first_start in [0usize, 3usize, 7usize] {
        let mut plan = sample_plan();
        retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
        let raw = (-12345i32) as u32;
        let bytes = int_packet(first_start, true, raw, 11);
        let first = first_property(&bytes, first_start, 47, &plan);
        let decoded =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                &bytes,
                &first,
                &plan,
                ctx(10, false),
            )
            .unwrap();
        let payload_start = first.stop_bit + 6;
        match decoded.second_payload.as_ref().unwrap() {
            ReplayNetworkExistingActorSecondPropertyPayloadV1::Int(value) => {
                assert_eq!(value.payload_start_bit, payload_start);
                assert_eq!(value.payload_width, 32);
                assert_eq!(value.payload_end_bit, payload_start + 32);
                assert_eq!(value.stop_bit, payload_start + 32);
                assert_eq!(
                    value.value,
                    ReplayNetworkPrimitiveScalarValueV1::Int(-12345)
                );
            }
            other => panic!("unexpected payload: {other:?}"),
        }
        assert_eq!(decoded.stop_bit, payload_start + 32);
    }
}

#[test]
fn string_second_payload_is_exact_r318i_windows1252_shape() {
    let mut plan = sample_plan();
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = string_packet(0, b"ABCDEF", 13);
    let first = first_property(&bytes, 0, 47, &plan);
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::String);
    let decoded =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &bytes,
            &first,
            &plan,
            ctx(10, false),
        )
        .unwrap();
    let payload_start = first.stop_bit + 6;
    match decoded.second_payload.as_ref().unwrap() {
        ReplayNetworkExistingActorSecondPropertyPayloadV1::String(value) => {
            assert_eq!(value.payload_start_bit, payload_start);
            assert_eq!(value.payload_width, 88);
            assert_eq!(value.payload_end_bit, payload_start + 88);
            match &value.value {
                ReplayNetworkK2ValueV1::String(text) => {
                    assert_eq!(text.value, "ABCDEF");
                    assert_eq!(text.declared_length, 7);
                    assert_eq!(text.encoding, ReplayNetworkTextEncodingV1::Windows1252);
                }
                other => panic!("unexpected K2 value: {other:?}"),
            }
        }
        other => panic!("unexpected payload: {other:?}"),
    }
    assert_eq!(decoded.stop_bit, payload_start + 88);
}

#[test]
fn string_wrong_context_fails_closed_before_semantic_widening() {
    let mut plan = sample_plan();
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = string_packet(0, b"ABCDEF", 0);
    let first = first_property(&bytes, 0, 47, &plan);
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::String);
    let error =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &bytes,
            &first,
            &plan,
            ctx(10, true),
        )
        .unwrap_err();
    assert!(
        error
            .to_string()
            .contains("unsupported-second-string-context")
    );
}

#[test]
fn int_truncation_rejects_and_post_payload_poison_is_invariant() {
    let mut plan = sample_plan();
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let clean = int_packet(3, true, 0x1234_5678, 24);
    let first = first_property(&clean, 3, 47, &plan);
    let expected =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &clean,
            &first,
            &plan,
            ctx(10, false),
        )
        .unwrap();
    let end = usize::try_from(expected.stop_bit).unwrap();

    let mut truncated = clean.clone();
    truncated.truncate(end.div_ceil(8).saturating_sub(1));
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &truncated,
            &first,
            &plan,
            ctx(10, false),
        )
        .is_err()
    );

    let mut poisoned = clean.clone();
    for offset in 0..16 {
        set_bit(&mut poisoned, end + offset, offset % 2 == 0);
    }
    let got =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &poisoned,
            &first,
            &plan,
            ctx(10, false),
        )
        .unwrap();
    assert_eq!(got, expected);
}

#[test]
fn string_truncation_and_malformed_length_reject_atomically() {
    let mut plan = sample_plan();
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let full = string_packet(0, b"ABCDEF", 0);
    let first = first_property(&full, 0, 47, &plan);
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::String);
    let mut truncated = full.clone();
    truncated.truncate(truncated.len() - 1);
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &truncated,
            &first,
            &plan,
            ctx(10, false),
        )
        .is_err()
    );

    let mut malformed = full.clone();
    let payload_start = usize::try_from(first.stop_bit + 6).unwrap();
    write_bits(
        &mut malformed,
        payload_start,
        32,
        u64::from(i32::MIN as u32),
    );
    let error =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &malformed,
            &first,
            &plan,
            ctx(10, false),
        )
        .unwrap_err();
    assert!(error.to_string().contains("invalid-text-length"));
}

#[test]
fn result_is_repeatable_and_tag_outside_int_string_stays_closed() {
    let mut plan = sample_plan();
    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = int_packet(3, true, 42, 8);
    let first = first_property(&bytes, 3, 47, &plan);
    let one =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &bytes,
            &first,
            &plan,
            ctx(10, false),
        )
        .unwrap();
    let two =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &bytes,
            &first,
            &plan,
            ctx(10, false),
        )
        .unwrap();
    assert_eq!(one, two);

    retag(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Float);
    let error =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &bytes,
            &first,
            &plan,
            ctx(10, false),
        )
        .unwrap_err();
    assert!(error.to_string().contains("unsupported-second-header-tag"));
}
