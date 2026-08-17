use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
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

fn fixture(path: &str, label: &str) -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(path);
    network_and_plan(&path, label)
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

fn t_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
    first_property_present_start: u64,
    actor_object_index: u32,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1 {
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        network,
        first_property_present_start,
        actor_object_index,
        plan,
    )
    .expect("R3.18B first property");
    let second =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            network,
            &first,
            plan,
            k2_context(),
        )
        .expect("R3.18J second payload");
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        network,
        &second,
        plan,
        context(),
    )
    .expect("R3.18T following payload")
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

#[test]
fn r3_18w_boolean_real_control_is_true_and_stops_one_bit_later() {
    let (network, plan) = fixture("../../external_fixtures/sample_001.replay", "r318w_boolean");
    let prior = t_prior(&network, &plan, 10227, 98);
    assert_eq!(prior.stop_bit, 10313);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &network, &prior,
    )
    .expect("R3.18W Boolean-lane control");
    assert!(got.following_property_present);
    assert_eq!(got.property_present_start_bit, 10313);
    assert_eq!(got.property_present_end_bit, 10314);
    assert_eq!(got.stop_bit, 10314);
}

#[test]
fn r3_18w_active_actor_real_control_is_true_and_stops_one_bit_later() {
    let (network, plan) = fixture(
        "../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay",
        "r318w_active_actor",
    );
    let prior = t_prior(&network, &plan, 3164, 114);
    assert_eq!(prior.stop_bit, 3282);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &network, &prior,
    )
    .expect("R3.18W ActiveActor-lane control");
    assert_eq!(got.property_present_start_bit, 3282);
    assert_eq!(got.stop_bit, 3283);
}

#[test]
fn r3_18w_real_aligned_control_boundary_is_supported() {
    let (network, plan) = fixture(
        "../../test_corpus/largest_100/036_88b815c9-bc3d-498a-8fa3-80638cfa8709.replay",
        "r318w_aligned",
    );
    let prior = t_prior(&network, &plan, 3243, 120);
    assert_eq!(prior.stop_bit, 3328);
    assert_eq!(prior.stop_bit % 8, 0);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &network, &prior,
    )
    .expect("R3.18W aligned control");
    assert_eq!(got.property_present_start_bit, 3328);
    assert_eq!(got.stop_bit, 3329);
}

#[test]
fn r3_18w_false_control_fails_closed() {
    let (mut network, plan) = fixture("../../external_fixtures/sample_001.replay", "r318w_false");
    let prior = t_prior(&network, &plan, 10227, 98);
    set_bit(&mut network, prior.stop_bit as usize, false);
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &network, &prior,
    )
    .unwrap_err();
    assert!(error.to_string().contains("unadmitted-false-control"));
}

#[test]
fn r3_18w_missing_control_bit_fails_atomically() {
    let (network, plan) = fixture(
        "../../external_fixtures/sample_001.replay",
        "r318w_truncated",
    );
    let prior = t_prior(&network, &plan, 10227, 98);
    let bytes_before_control = usize::try_from(prior.stop_bit / 8).unwrap();
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
            &network[..bytes_before_control], &prior,
        )
        .is_err()
    );
}

#[test]
fn r3_18w_prior_stop_and_payload_boundary_mismatch_fail_before_success() {
    let (network, plan) = fixture(
        "../../external_fixtures/sample_001.replay",
        "r318w_prior_mismatch",
    );
    let prior = t_prior(&network, &plan, 10227, 98);

    let mut bad_stop = prior.clone();
    bad_stop.stop_bit += 1;
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &network, &bad_stop,
    )
    .unwrap_err();
    assert!(error.to_string().contains("invalid-prior-stop"));

    let mut bad_payload = prior.clone();
    match &mut bad_payload.following_payload {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::Boolean(value) => {
            value.payload_width = 2;
        }
        other => panic!("expected Boolean prior, got {other:?}"),
    }
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &network, &bad_payload,
    )
    .unwrap_err();
    assert!(error.to_string().contains("invalid-prior-payload"));
}

#[test]
fn r3_18w_repeatability_and_post_control_poison_preserve_one_bit_result() {
    let (network, plan) = fixture("../../external_fixtures/sample_001.replay", "r318w_repeat");
    let prior = t_prior(&network, &plan, 10227, 98);
    let clean = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &network, &prior,
    )
    .unwrap();
    let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &network, &prior,
    )
    .unwrap();
    assert_eq!(clean, repeated);

    let mut poisoned = network.clone();
    for offset in 0..16usize {
        set_bit(
            &mut poisoned,
            clean.stop_bit as usize + offset,
            offset % 2 == 0,
        );
    }
    let after = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        &poisoned, &prior,
    )
    .unwrap();
    assert_eq!(after, clean);
}

#[test]
fn r3_18w_source_scope_contains_one_bit_read_and_no_following_decode_or_loop() {
    let source = include_str!("../src/lib.rs");
    let start = source
        .find("pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1")
        .expect("R3.18W public function");
    let function = &source[start..];
    assert_eq!(function.matches("cursor.read_bit()").count(), 1);
    assert!(!function.contains("decode_replay_network_existing_actor_first_property_header_v1("));
    assert!(!function.contains("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1("));
    assert!(!function.contains("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1("));
    assert!(!function.contains("lookup_plan"));
    assert!(!function.contains("\n    while "));
    assert!(!function.contains("\n    for "));
}
