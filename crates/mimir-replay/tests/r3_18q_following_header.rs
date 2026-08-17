use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn sample_network_and_plan() -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let replay_bytes = std::fs::read(path).expect("read sample_001.replay");
    let input = ReplayInput::Memory {
        label: "r318q_sample_001".to_owned(),
        bytes: replay_bytes.clone(),
    };
    let scaffold = MinimalReplayContentScaffoldReader
        .read_content_scaffold(&input)
        .expect("content scaffold");
    let network = replay_bytes[usize::try_from(scaffold.network_start).unwrap()
        ..usize::try_from(scaffold.network_end).unwrap()]
        .to_vec();
    let plan = MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&input)
        .expect("lookup plan");
    (network, plan)
}

fn r3_18j_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1 {
    let first =
        decode_replay_network_existing_actor_single_primitive_property_v1(network, 10227, 98, plan)
            .expect("R3.18B first property");
    assert_eq!(first.stop_bit, 10266);
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
        network,
        &first,
        plan,
        ReplayNetworkK2DecodeContextV1 {
            net_version: 10,
            is_rl_223: false,
        },
    )
    .expect("R3.18J second payload")
}

fn context() -> ReplayNetworkK3DecodeContextV1 {
    ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: false,
    }
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

#[test]
fn r3_18q_sample_001_composes_exact_admitted_header_and_preserves_r3_18m_control() {
    let (network, plan) = sample_network_and_plan();
    let prior = r3_18j_prior(&network, &plan);
    assert_eq!(prior.stop_bit, 10305);
    let m = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(
        &network, &prior,
    )
    .expect("R3.18M control");
    let q = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &network, &prior, &plan, context(),
    )
    .expect("R3.18Q following header");

    assert_eq!(q.control, m);
    assert_eq!(q.control.property_present_start_bit, 10305);
    assert_eq!(q.control.stop_bit, 10306);
    assert!(q.following_header.property_present);
    assert_eq!(q.following_header.stream_id, Some(33));
    assert_eq!(q.following_header.stream_id_bound, Some(67));
    assert_eq!(q.following_header.prop_id_bits, Some(6));
    assert_eq!(q.following_header.resolved_property_object_index, Some(61));
    assert_eq!(
        q.following_header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Boolean)
    );
    assert_eq!(q.following_header.payload_start_bit, Some(10312));
    assert_eq!(q.following_header.stop_bit, 10312);
    assert_eq!(q.stop_bit, 10312);
}

#[test]
fn r3_18q_post_payload_poison_cannot_change_header_result() {
    let (network, plan) = sample_network_and_plan();
    let prior = r3_18j_prior(&network, &plan);
    let clean = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &network, &prior, &plan, context(),
    )
    .unwrap();
    let mut poisoned = network.clone();
    for offset in 0..16usize {
        set_bit(&mut poisoned, 10312 + offset, offset % 2 == 0);
    }
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &poisoned, &prior, &plan, context(),
    )
    .unwrap();
    assert_eq!(got, clean);
}

#[test]
fn r3_18q_truncation_and_wrong_actor_fail_closed() {
    let (network, plan) = sample_network_and_plan();
    let prior = r3_18j_prior(&network, &plan);
    let truncated = &network[..1288];
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
            truncated, &prior, &plan, context(),
        )
        .is_err()
    );

    let mut wrong_actor = prior.clone();
    wrong_actor
        .header_composition
        .second_header
        .as_mut()
        .unwrap()
        .actor_object_index = u32::MAX;
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
            &network, &wrong_actor, &plan, context(),
        )
        .is_err()
    );
}

#[test]
fn r3_18q_fabricated_cartesian_tuple_and_wrong_version_are_rejected() {
    let (network, plan) = sample_network_and_plan();
    let prior = r3_18j_prior(&network, &plan);

    let mut fabricated_plan = plan.clone();
    let property = fabricated_plan.object_lookups[98]
        .as_mut()
        .unwrap()
        .properties
        .iter_mut()
        .find(|property| property.stream_id == 33)
        .unwrap();
    assert_eq!(property.object_index, 61);
    property.object_index = 62;
    let fabricated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &network, &prior, &fabricated_plan, context(),
    )
    .unwrap_err();
    assert!(
        fabricated
            .to_string()
            .contains("unadmitted-following-header-context")
    );

    let wrong_version = ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 31,
        net_version: 10,
        is_rl_223: false,
    };
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &network, &prior, &plan, wrong_version,
    )
    .unwrap_err();
    assert!(
        error
            .to_string()
            .contains("unadmitted-following-header-context")
    );
}
