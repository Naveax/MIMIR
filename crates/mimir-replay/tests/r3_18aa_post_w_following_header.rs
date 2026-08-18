use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1,
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
        network, &second, plan, context(),
    ).expect("R3.18T following payload")
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

#[test]
fn r3_18aa_real_active_actor_int_and_unique_id_headers_match_frozen_y_boundaries() {
    let cases = [
        (
            "../../external_fixtures/sample_001.replay",
            "r318aa_active_actor",
            10227,
            98,
            10313,
            10320,
            35,
            67,
            6,
            63,
            ReplayNetworkAttributeTagV1::ActiveActor,
        ),
        (
            "../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay",
            "r318aa_int",
            3164,
            114,
            3282,
            3289,
            35,
            60,
            5,
            87,
            ReplayNetworkAttributeTagV1::Int,
        ),
        (
            "../../test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay",
            "r318aa_unique_id",
            2838,
            117,
            2991,
            2999,
            21,
            110,
            6,
            25,
            ReplayNetworkAttributeTagV1::UniqueId,
        ),
    ];
    for (
        path,
        label,
        first_start,
        actor_object_index,
        control_start,
        payload_start,
        stream_id,
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        tag,
    ) in cases
    {
        let (network, plan) = fixture(path, label);
        let prior = t_prior(&network, &plan, first_start, actor_object_index);
        assert_eq!(prior.stop_bit, control_start);
        let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
            &network, &prior, &plan, context(),
        ).expect("R3.18AA post-W following header");
        assert!(got.control.following_property_present);
        assert_eq!(got.control.property_present_start_bit, control_start);
        assert_eq!(got.control.property_present_end_bit, control_start + 1);
        assert_eq!(
            got.following_header.property_present_start_bit,
            control_start
        );
        assert_eq!(
            got.following_header.property_present_end_bit,
            control_start + 1
        );
        assert_eq!(got.following_header.stream_id, Some(stream_id));
        assert_eq!(got.following_header.stream_id_bound, Some(stream_id_bound));
        assert_eq!(got.following_header.prop_id_bits, Some(prop_id_bits));
        assert_eq!(
            got.following_header.resolved_property_object_index,
            Some(property_object_index)
        );
        assert_eq!(got.following_header.resolved_attribute_tag, Some(tag));
        assert_eq!(got.following_header.payload_start_bit, Some(payload_start));
        assert_eq!(got.following_header.stop_bit, payload_start);
        assert_eq!(got.stop_bit, payload_start);
    }
}

#[test]
fn r3_18aa_repeatability_and_post_payload_poison_preserve_header_result() {
    let (network, plan) = fixture("../../external_fixtures/sample_001.replay", "r318aa_repeat");
    let prior = t_prior(&network, &plan, 10227, 98);
    let clean = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(&network, &prior, &plan, context()).unwrap();
    let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(&network, &prior, &plan, context()).unwrap();
    assert_eq!(clean, repeated);
    let mut poisoned = network.clone();
    for offset in 0..16usize {
        set_bit(
            &mut poisoned,
            clean.stop_bit as usize + offset,
            offset % 2 == 0,
        );
    }
    let after = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(&poisoned, &prior, &plan, context()).unwrap();
    assert_eq!(after, clean);
}

#[test]
fn r3_18aa_header_truncation_and_wrong_actor_fail_closed() {
    let (network, plan) = fixture(
        "../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay",
        "r318aa_truncated",
    );
    let prior = t_prior(&network, &plan, 3164, 114);
    assert_eq!(prior.stop_bit, 3282);
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(&network[..411], &prior, &plan, context()).is_err());
    let mut wrong_actor = prior.clone();
    wrong_actor
        .header_composition
        .following_header
        .actor_object_index = u32::MAX;
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(&network, &wrong_actor, &plan, context()).is_err());
}

#[test]
fn r3_18aa_cartesian_version_and_r3_18p_cross_boundary_widening_are_rejected() {
    let (network, plan) = fixture(
        "../../external_fixtures/sample_001.replay",
        "r318aa_cartesian",
    );
    let prior = t_prior(&network, &plan, 10227, 98);
    let mut fabricated_plan = plan.clone();
    let property = fabricated_plan.object_lookups[98]
        .as_mut()
        .unwrap()
        .properties
        .iter_mut()
        .find(|property| property.stream_id == 35)
        .unwrap();
    assert_eq!(property.object_index, 63);
    property.object_index = 61;
    property.tag = ReplayNetworkAttributeTagV1::Boolean;
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(&network, &prior, &fabricated_plan, context()).unwrap_err();
    assert!(
        error
            .to_string()
            .contains("unadmitted-r3-18z-header-context")
    );

    let wrong_version = ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 31,
        net_version: 10,
        is_rl_223: false,
    };
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(&network, &prior, &plan, wrong_version).unwrap_err();
    assert!(
        error
            .to_string()
            .contains("unadmitted-r3-18z-header-context")
    );

    let (network, plan) = fixture(
        "../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay",
        "r318aa_r318p_only",
    );
    let prior = t_prior(&network, &plan, 3164, 114);
    let mut p_only_plan = plan.clone();
    let property = p_only_plan.object_lookups[114]
        .as_mut()
        .unwrap()
        .properties
        .iter_mut()
        .find(|property| property.stream_id == 35)
        .unwrap();
    assert_eq!(property.object_index, 87);
    property.object_index = 102;
    property.tag = ReplayNetworkAttributeTagV1::Boolean;
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(&network, &prior, &p_only_plan, context()).unwrap_err();
    assert!(
        error
            .to_string()
            .contains("unadmitted-r3-18z-header-context")
    );
}

#[test]
fn r3_18aa_source_scope_is_one_w_control_one_header_and_no_payload_or_loop() {
    let source = include_str!("../src/lib.rs");
    let start = source.find("pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1").expect("R3.18AA public function");
    let w_marker =
        "/// R3.18V observed exactly one next `property_present` bit on the immutable 47-row lane:";
    let end = source[start..]
        .find(w_marker)
        .map(|offset| start + offset)
        .expect("R3.18W boundary marker after R3.18AA");
    let function = &source[start..end];
    assert_eq!(function.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(").count(), 1);
    assert_eq!(
        function
            .matches("decode_replay_network_existing_actor_first_property_header_v1(")
            .count(),
        1
    );
    assert!(!function.contains("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1("));
    assert!(!function.contains("cursor.read_bit()"));
    assert!(!function.contains("\n    while "));
    assert!(!function.contains("\n    for "));
}
