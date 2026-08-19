use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1, ReplayNetworkPrimitiveScalarValueV1,
    ReplayNetworkUniqueIdRemoteV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1, decode_replay_network_k2_v1,
};
use std::path::PathBuf;

const ACTIVE_PATH: &str = "../../external_fixtures/sample_001.replay";
const INT_PATH: &str =
    "../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay";
const UID_PATH: &str =
    "../../test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay";

fn context() -> ReplayNetworkK3DecodeContextV1 {
    ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: false,
    }
}

fn k2_context() -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version: 10,
        is_rl_223: false,
    }
}

fn network_and_plan(relative: &str, label: &str) -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(relative);
    let replay_bytes = std::fs::read(&path)
        .unwrap_or_else(|error| panic!("read frozen R3.18AC replay {}: {error}", path.display()));
    let input = ReplayInput::Memory {
        label: label.to_owned(),
        bytes: replay_bytes.clone(),
    };
    let scaffold = MinimalReplayContentScaffoldReader
        .read_content_scaffold(&input)
        .expect("content scaffold");
    let ns = usize::try_from(scaffold.network_start).expect("network start");
    let ne = usize::try_from(scaffold.network_end).expect("network end");
    let network = replay_bytes[ns..ne].to_vec();
    let plan = MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&input)
        .expect("lookup plan");
    (network, plan)
}

fn build_prior(
    relative: &str,
    label: &str,
    first_start: u64,
    actor_object: u32,
) -> (
    Vec<u8>,
    ReplayNetworkLookupPlanV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1,
) {
    let (network, plan) = network_and_plan(relative, label);
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        &network,
        first_start,
        actor_object,
        &plan,
    )
    .expect("R3.18B first property");
    let second =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &network,
            &first,
            &plan,
            k2_context(),
        )
        .expect("R3.18J second payload");
    let prior = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        &network,
        &second,
        &plan,
        context(),
    )
    .expect("R3.18T following payload");
    (network, plan, prior)
}

fn set_bit(bytes: &mut Vec<u8>, position: u64, value: bool) {
    let p = usize::try_from(position).expect("bit position");
    let need = p / 8 + 1;
    if bytes.len() < need {
        bytes.resize(need, 0);
    }
    if value {
        bytes[p / 8] |= 1 << (p % 8);
    } else {
        bytes[p / 8] &= !(1 << (p % 8));
    }
}

fn write_bits(bytes: &mut Vec<u8>, bit: &mut u64, value: u64, width: u64) {
    for offset in 0..width {
        set_bit(bytes, *bit + offset, ((value >> offset) & 1) != 0);
    }
    *bit += width;
}

fn write_u8(bytes: &mut Vec<u8>, bit: &mut u64, value: u8) {
    write_bits(bytes, bit, u64::from(value), 8);
}

fn write_i32(bytes: &mut Vec<u8>, bit: &mut u64, value: i32) {
    write_bits(bytes, bit, u64::from(value as u32), 32);
}

fn write_epic_unique_id(bytes: &mut Vec<u8>, start: u64) -> u64 {
    let mut bit = start;
    write_u8(bytes, &mut bit, 11);
    write_i32(bytes, &mut bit, 33);
    for _ in 0..32 {
        write_u8(bytes, &mut bit, b'E');
    }
    write_u8(bytes, &mut bit, 0x55);
    write_u8(bytes, &mut bit, 4);
    assert_eq!(bit - start, 312);
    bit
}

fn assert_error_contains(error: mimir_core::MimirError, needle: &str) {
    let text = error.to_string();
    assert!(text.contains(needle), "expected {needle:?} in {text:?}");
}

#[test]
fn frozen_active_actor_composes_exact_33_bits_and_stops_at_ac_end() {
    let (network, plan, prior) = build_prior(ACTIVE_PATH, "r318ad_active", 10227, 98);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &network, &prior, &plan, context(),
    )
    .expect("R3.18AD ActiveActor");
    assert_eq!(got.payload_start_bit, 10320);
    assert_eq!(got.payload_width, 33);
    assert_eq!(got.stop_bit, 10353);
    assert_eq!(got.header_composition.stop_bit, 10320);
    match &got.following_payload {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::ActiveActor(decoded) => {
            assert_eq!(decoded.payload_start_bit, 10320);
            assert_eq!(decoded.payload_end_bit, 10353);
            assert_eq!(decoded.payload_width, 33);
            assert_eq!(
                decoded.value,
                ReplayNetworkK2ValueV1::ActiveActor {
                    active: false,
                    actor: 350,
                }
            );
        }
        other => panic!("expected ActiveActor, got {other:?}"),
    }

    let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &network, &prior, &plan, context(),
    )
    .expect("repeat ActiveActor");
    assert_eq!(repeated, got);

    let mut poisoned = network.clone();
    for offset in 0..16 {
        set_bit(&mut poisoned, got.stop_bit + offset, offset % 2 == 0);
    }
    let after_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &poisoned, &prior, &plan, context(),
    )
    .expect("post-payload poison must not matter");
    assert_eq!(after_poison, got);

    let trunc = usize::try_from(got.payload_start_bit / 8).expect("truncation length");
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &network[..trunc], &prior, &plan, context(),
    ).is_err());
}

#[test]
fn frozen_int_composes_exact_32_bits_and_preserves_value() {
    let (network, plan, prior) = build_prior(INT_PATH, "r318ad_int", 3164, 114);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &network, &prior, &plan, context(),
    )
    .expect("R3.18AD Int");
    assert_eq!(got.payload_start_bit, 3289);
    assert_eq!(got.payload_width, 32);
    assert_eq!(got.stop_bit, 3321);
    match &got.following_payload {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::Int(decoded) => {
            assert_eq!(decoded.payload_start_bit, 3289);
            assert_eq!(decoded.payload_end_bit, 3321);
            assert_eq!(decoded.payload_width, 32);
            assert_eq!(decoded.stop_bit, 3321);
            assert_eq!(decoded.value, ReplayNetworkPrimitiveScalarValueV1::Int(1));
        }
        other => panic!("expected Int, got {other:?}"),
    }
}

#[test]
fn frozen_unique_id_composes_only_system1_steam_80_bit_shape() {
    let (network, plan, prior) = build_prior(UID_PATH, "r318ad_uid", 2838, 117);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &network, &prior, &plan, context(),
    )
    .expect("R3.18AD UniqueId");
    assert_eq!(got.payload_start_bit, 2999);
    assert_eq!(got.payload_width, 80);
    assert_eq!(got.stop_bit, 3079);
    match &got.following_payload {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::UniqueId(decoded) => {
            assert_eq!(decoded.payload_width, 80);
            match &decoded.value {
                ReplayNetworkK2ValueV1::UniqueId(uid) => {
                    assert_eq!(uid.system_id, 1);
                    assert_eq!(uid.local_id, 0);
                    assert!(matches!(&uid.remote_id, ReplayNetworkUniqueIdRemoteV1::Steam { .. }));
                }
                other => panic!("expected UniqueId K2 value, got {other:?}"),
            }
        }
        other => panic!("expected UniqueId, got {other:?}"),
    }
}

#[test]
fn lower_level_valid_epic_unique_id_is_rejected_at_ad_boundary() {
    let (network, plan, prior) = build_prior(UID_PATH, "r318ad_uid_epic_negative", 2838, 117);
    let original = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &network, &prior, &plan, context(),
    )
    .expect("original Steam witness");
    assert_eq!(original.payload_start_bit, 2999);

    let mut mutated = network.clone();
    let epic_end = write_epic_unique_id(&mut mutated, original.payload_start_bit);
    assert_eq!(epic_end - original.payload_start_bit, 312);
    let lower = decode_replay_network_k2_v1(
        &mutated,
        original.payload_start_bit,
        ReplayNetworkAttributeTagV1::UniqueId,
        k2_context(),
    )
    .expect("lower-level K2 admits Epic shape");
    assert_eq!(lower.payload_width, 312);
    assert!(matches!(
        &lower.value,
        ReplayNetworkK2ValueV1::UniqueId(uid)
            if uid.system_id == 11
                && matches!(&uid.remote_id, ReplayNetworkUniqueIdRemoteV1::Epic { .. })
    ));

    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &mutated, &prior, &plan, context(),
    )
    .expect_err("R3.18AD must reject AC-unadmitted Epic layout");
    assert_error_contains(error, "unadmitted-unique-id-shape");
}

#[test]
fn wrong_replay_context_fails_before_payload_widening() {
    let (network, plan, prior) = build_prior(ACTIVE_PATH, "r318ad_wrong_context", 10227, 98);
    let wrong = ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: true,
    };
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        &network, &prior, &plan, wrong,
    )
    .expect_err("RL223 context is outside AC/AD boundary");
    assert_error_contains(error, "unadmitted-context");
}
