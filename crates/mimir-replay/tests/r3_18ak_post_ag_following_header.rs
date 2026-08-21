use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
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

fn k2_context() -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version: 10,
        is_rl_223: false,
    }
}

fn k3_context() -> ReplayNetworkK3DecodeContextV1 {
    ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: false,
    }
}

fn ad_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
    first_start: u64,
    actor_object: u32,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1{
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        network,
        first_start,
        actor_object,
        plan,
    )
    .expect("R3.18B first");
    let second =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            network,
            &first,
            plan,
            k2_context(),
        )
        .expect("R3.18J second");
    let t = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        network, &second, plan, k3_context(),
    ).expect("R3.18T payload");
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        network, &t, plan, k3_context(),
    ).expect("R3.18AD payload")
}

fn ag_control(
    network: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1{
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        network, prior, k3_context(),
    ).expect("R3.18AG control")
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

#[test]
fn r3_18ak_representative_ai_headers_match_exact_boundaries() {
    let cases = [
        (
            "../../external_fixtures/sample_001.replay",
            10227,
            98,
            10353,
            10354,
            10360,
            39,
            67,
            6,
            68,
        ),
        (
            "../../external_fixtures/sample_002.replay",
            11019,
            106,
            11145,
            11146,
            11152,
            41,
            72,
            6,
            73,
        ),
        (
            "../../external_fixtures/sample_003.replay",
            7603,
            103,
            7729,
            7730,
            7736,
            41,
            72,
            6,
            70,
        ),
        (
            "../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay",
            2848,
            112,
            2973,
            2974,
            2980,
            35,
            60,
            5,
            85,
        ),
        (
            "../../test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay",
            2838,
            117,
            3079,
            3080,
            3087,
            33,
            110,
            6,
            37,
        ),
    ];
    for (
        index,
        (
            path,
            first_start,
            actor,
            ag_start,
            ag_stop,
            payload_start,
            stream_id,
            bound,
            bits,
            object,
        ),
    ) in cases.into_iter().enumerate()
    {
        let (network, plan) = fixture(path, &format!("r318ak_positive_{index}"));
        let prior = ad_prior(&network, &plan, first_start, actor);
        assert_eq!(prior.stop_bit, ag_start);
        let control = ag_control(&network, &prior);
        assert_eq!(control.property_present_start_bit, ag_start);
        assert_eq!(control.stop_bit, ag_stop);
        let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(),
        ).unwrap();
        assert_eq!(got.control, control);
        assert_eq!(got.following_header.property_present_start_bit, ag_start);
        assert_eq!(got.following_header.property_present_end_bit, ag_stop);
        assert_eq!(got.following_header.stream_id, Some(stream_id));
        assert_eq!(got.following_header.stream_id_bound, Some(bound));
        assert_eq!(got.following_header.prop_id_bits, Some(bits));
        assert_eq!(
            got.following_header.resolved_property_object_index,
            Some(object)
        );
        assert_eq!(
            got.following_header.resolved_attribute_tag,
            Some(ReplayNetworkAttributeTagV1::Int)
        );
        assert_eq!(got.following_header.payload_start_bit, Some(payload_start));
        assert_eq!(got.following_header.stop_bit, payload_start);
        assert_eq!(got.stop_bit, payload_start);
    }
}

#[test]
fn r3_18ak_repeatability_and_post_payload_poison_preserve_result() {
    let (network, plan) = fixture("../../external_fixtures/sample_001.replay", "r318ak_repeat");
    let prior = ad_prior(&network, &plan, 10227, 98);
    let control = ag_control(&network, &prior);
    let clean = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, k3_context(),
    ).unwrap();
    let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, k3_context(),
    ).unwrap();
    assert_eq!(clean, repeated);
    let mut poisoned = network.clone();
    for offset in 0..16usize {
        set_bit(
            &mut poisoned,
            clean.stop_bit as usize + offset,
            offset % 2 == 0,
        );
    }
    let after = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &poisoned, &prior, &control, &plan, k3_context(),
    ).unwrap();
    assert_eq!(after, clean);
}

#[test]
fn r3_18ak_tampered_ag_truncation_actor_lookup_and_version_fail_closed() {
    let (network, plan) = fixture(
        "../../external_fixtures/sample_001.replay",
        "r318ak_fail_closed",
    );
    let prior = ad_prior(&network, &plan, 10227, 98);
    let control = ag_control(&network, &prior);

    let mut bad_control = control.clone();
    bad_control.stop_bit += 1;
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &bad_control, &plan, k3_context(),
    ).unwrap_err();
    assert!(error.to_string().contains("invalid-r3-18ag-control"));

    let mut bad_prior = prior.clone();
    bad_prior
        .header_composition
        .following_header
        .actor_object_index = u32::MAX;
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &bad_prior, &control, &plan, k3_context(),
    ).is_err());

    let mut missing_lookup = plan.clone();
    missing_lookup.object_lookups[98] = None;
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &missing_lookup, k3_context(),
    ).is_err());

    let wrong = ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 31,
        net_version: 10,
        is_rl_223: false,
    };
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, wrong,
    ).is_err());

    let (network, plan) = fixture(
        "../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay",
        "r318ak_trunc",
    );
    let prior = ad_prior(&network, &plan, 2848, 112);
    let control = ag_control(&network, &prior);
    assert_eq!(control.stop_bit, 2974);
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network[..372], &prior, &control, &plan, k3_context(),
    ).is_err());
}

#[test]
fn r3_18ak_cartesian_fabricated_and_old_z_contexts_are_rejected() {
    let (network, plan) = fixture(
        "../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay",
        "r318ak_widening",
    );
    let prior = ad_prior(&network, &plan, 2848, 112);
    let control = ag_control(&network, &prior);
    for (object_index, tag) in [
        (68, ReplayNetworkAttributeTagV1::Int),
        (39, ReplayNetworkAttributeTagV1::Int),
        (34, ReplayNetworkAttributeTagV1::ActiveActor),
    ] {
        let mut widened = plan.clone();
        let property = widened.object_lookups[112]
            .as_mut()
            .unwrap()
            .properties
            .iter_mut()
            .find(|property| property.stream_id == 35)
            .unwrap();
        assert_eq!(property.object_index, 85);
        property.object_index = object_index;
        property.tag = tag;
        let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &widened, k3_context(),
        ).unwrap_err();
        assert!(
            error
                .to_string()
                .contains("unadmitted-r3-18aj-header-context"),
            "{error}"
        );
    }
}

#[test]
fn r3_18ak_source_scope_is_one_ag_control_one_header_and_no_payload_or_loop() {
    let source = include_str!("../src/lib.rs");
    let start = source.find("pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1").expect("R3.18AK function");
    let tail = &source[start..];
    let end = tail
        .find("#[cfg(test)]\nmod tests {")
        .expect("internal test-module boundary after R3.18AK");
    let function = &tail[..end];
    assert_eq!(function.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(").count(), 1);
    assert_eq!(
        function
            .matches("decode_replay_network_existing_actor_first_property_header_v1(")
            .count(),
        1
    );
    assert_eq!(
        function
            .matches("r3_18aj_post_ag_header_context_contains_v1(")
            .count(),
        1
    );
    assert!(!function.contains("decode_replay_network_primitive_scalar_v1("));
    assert!(!function.contains("decode_replay_network_k2_v1("));
    assert!(!function.contains("decode_replay_network_k3_v1("));
    assert!(!function.contains("cursor.read_bit()"));
    assert!(!function.contains("\n    while "));
    assert!(!function.contains("\n    for "));
}
