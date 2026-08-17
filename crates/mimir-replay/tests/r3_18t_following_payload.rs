use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1, decode_replay_network_k2_v1,
    decode_replay_network_primitive_scalar_v1,
};
use std::path::{Path, PathBuf};

fn network_and_plan(path: &Path, label: &str) -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let replay_bytes = std::fs::read(path).expect("read replay");
    let input = ReplayInput::Memory {
        label: label.to_owned(),
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

fn sample_network_and_plan() -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    network_and_plan(&path, "r318t_sample_001")
}

fn active_actor_network_and_plan() -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay");
    network_and_plan(&path, "r318t_active_actor_witness")
}

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

fn sample_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1 {
    let first =
        decode_replay_network_existing_actor_single_primitive_property_v1(network, 10227, 98, plan)
            .expect("R3.18B first property");
    assert_eq!(first.stop_bit, 10266);
    let prior =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            network,
            &first,
            plan,
            k2_context(),
        )
        .expect("R3.18J second payload");
    assert_eq!(prior.stop_bit, 10305);
    prior
}

fn active_actor_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1 {
    let first =
        decode_replay_network_existing_actor_single_primitive_property_v1(network, 3164, 114, plan)
            .expect("R3.18B active-actor witness first property");
    assert_eq!(first.stop_bit, 3203);
    let prior =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            network,
            &first,
            plan,
            k2_context(),
        )
        .expect("R3.18J active-actor witness second payload");
    assert_eq!(prior.stop_bit, 3242);
    prior
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

#[test]
fn r3_18t_boolean_composes_exact_one_bit_payload_and_matches_lower_decoder() {
    let (network, plan) = sample_network_and_plan();
    let prior = sample_prior(&network, &plan);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        &network, &prior, &plan, context(),
    )
    .expect("R3.18T Boolean payload");
    assert_eq!(got.header_composition.stop_bit, 10312);
    assert_eq!(got.stop_bit, 10313);
    let direct = decode_replay_network_primitive_scalar_v1(
        &network,
        10312,
        ReplayNetworkAttributeTagV1::Boolean,
    )
    .expect("direct Boolean payload");
    match &got.following_payload {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::Boolean(value) => {
            assert_eq!(value, &direct);
            assert_eq!(value.payload_start_bit, 10312);
            assert_eq!(value.payload_width, 1);
            assert_eq!(value.payload_end_bit, 10313);
        }
        other => panic!("expected Boolean payload, got {other:?}"),
    }
}

#[test]
fn r3_18t_active_actor_real_boundary_is_exact_33_bits_and_matches_lower_decoder() {
    let (network, plan) = active_actor_network_and_plan();
    let prior = active_actor_prior(&network, &plan);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        &network, &prior, &plan, context(),
    )
    .expect("R3.18T ActiveActor payload");
    assert_eq!(got.header_composition.stop_bit, 3249);
    assert_eq!(got.stop_bit, 3282);
    let direct = decode_replay_network_k2_v1(
        &network,
        3249,
        ReplayNetworkAttributeTagV1::ActiveActor,
        k2_context(),
    )
    .expect("direct ActiveActor payload");
    match &got.following_payload {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::ActiveActor(value) => {
            assert_eq!(value, &direct);
            assert_eq!(value.payload_start_bit, 3249);
            assert_eq!(value.payload_width, 33);
            assert_eq!(value.payload_end_bit, 3282);
            assert_eq!(value.value, ReplayNetworkK2ValueV1::ActiveActor { active: false, actor: 342 });
        }
        other => panic!("expected ActiveActor payload, got {other:?}"),
    }
}

#[test]
fn r3_18t_payload_truncation_fails_after_q_header_boundary() {
    let (network, plan) = sample_network_and_plan();
    let prior = sample_prior(&network, &plan);
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network[..1289], &prior, &plan, context(),
        )
        .is_err()
    );

    let (active_network, active_plan) = active_actor_network_and_plan();
    let active_prior = active_actor_prior(&active_network, &active_plan);
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &active_network[..410], &active_prior, &active_plan, context(),
        )
        .is_err()
    );
}

#[test]
fn r3_18t_wrong_exact_context_and_fabricated_tuple_fail_closed() {
    let (network, plan) = sample_network_and_plan();
    let prior = sample_prior(&network, &plan);
    let wrong_version = ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 31,
        net_version: 10,
        is_rl_223: false,
    };
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        &network, &prior, &plan, wrong_version,
    )
    .unwrap_err();
    assert!(
        error
            .to_string()
            .contains("unadmitted-following-header-context")
    );

    let mut fabricated_plan = plan.clone();
    let property = fabricated_plan.object_lookups[98]
        .as_mut()
        .unwrap()
        .properties
        .iter_mut()
        .find(|property| property.stream_id == 33)
        .unwrap();
    property.object_index = 62;
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        &network, &prior, &fabricated_plan, context(),
    )
    .unwrap_err();
    assert!(
        error
            .to_string()
            .contains("unadmitted-following-header-context")
    );
}

#[test]
fn r3_18t_repeatability_and_next_control_poison_prove_payload_end_stop() {
    let (network, plan) = sample_network_and_plan();
    let prior = sample_prior(&network, &plan);
    let clean = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        &network, &prior, &plan, context(),
    )
    .unwrap();
    let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        &network, &prior, &plan, context(),
    )
    .unwrap();
    assert_eq!(clean, repeated);
    assert_eq!(clean.stop_bit, 10313);

    let mut poisoned = network.clone();
    for offset in 0..16usize {
        set_bit(
            &mut poisoned,
            clean.stop_bit as usize + offset,
            offset % 2 == 0,
        );
    }
    let after_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        &poisoned, &prior, &plan, context(),
    )
    .unwrap();
    assert_eq!(after_poison, clean);
}
