use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::{Path, PathBuf};

const AF_ROWS: &[(&str, u64, u32, u64)] = &[
    (
        "../../external_fixtures/sample_001.replay",
        10227,
        98,
        10353,
    ),
    (
        "../../external_fixtures/sample_002.replay",
        11019,
        106,
        11145,
    ),
    ("../../external_fixtures/sample_003.replay", 7603, 103, 7729),
    (
        "../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay",
        2848,
        112,
        2973,
    ),
    (
        "../../test_corpus/largest_100/010_27f8a623-4388-41da-9473-5f59df5fa93b.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay",
        3164,
        114,
        3321,
    ),
    (
        "../../test_corpus/largest_100/012_0c83fe49-b7f6-427a-ae97-b1a4f53d6117.replay",
        3042,
        112,
        3167,
    ),
    (
        "../../test_corpus/largest_100/016_b473f51b-abdd-4896-872f-26fb7d8bd939.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/019_bd1a83e2-5ac0-4a79-beba-df8547515782.replay",
        3006,
        111,
        3163,
    ),
    (
        "../../test_corpus/largest_100/023_d9186df1-af02-4ab1-ba1b-b2c3b6fb1a67.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/027_abfd6c12-e5e0-46a3-aaee-4d086a4d6ee5.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/033_e8ab232b-24e4-401c-b5ac-db2d5587cfcf.replay",
        3168,
        127,
        3293,
    ),
    (
        "../../test_corpus/largest_100/035_6b90776b-1784-4d30-a8ff-d37b66ae4a38.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/036_88b815c9-bc3d-498a-8fa3-80638cfa8709.replay",
        3243,
        120,
        3368,
    ),
    (
        "../../test_corpus/largest_100/038_c44e3655-bcc9-41fb-9548-808ee70c66e7.replay",
        2892,
        74,
        3017,
    ),
    (
        "../../test_corpus/largest_100/039_4c5e5ad8-c72f-49b2-890c-d936e172160c.replay",
        3006,
        111,
        3163,
    ),
    (
        "../../test_corpus/largest_100/040_0a38f81b-862d-4776-9d27-3c221355f839.replay",
        3006,
        111,
        3131,
    ),
    (
        "../../test_corpus/largest_100/042_be1e76bd-258a-4067-8d06-57481459f946.replay",
        3042,
        112,
        3167,
    ),
    (
        "../../test_corpus/largest_100/049_6c45a00b-d14b-4eba-86b8-4a3e99faf545.replay",
        3164,
        111,
        3289,
    ),
    (
        "../../test_corpus/largest_100/050_6e301fcc-239b-4a29-863b-8c2561e56042.replay",
        2970,
        135,
        3095,
    ),
    (
        "../../test_corpus/largest_100/054_9ed418f3-9eaf-4a18-a591-633db1120790.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/057_4fab5b3d-17de-4a7b-86d7-432ba973c524.replay",
        3042,
        111,
        3167,
    ),
    (
        "../../test_corpus/largest_100/059_d86eb20b-396c-49bc-80bb-71bec6949f94.replay",
        3243,
        120,
        3368,
    ),
    (
        "../../test_corpus/largest_100/060_6bc2e5f5-e243-4db0-b6f9-1b8173472c29.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/061_2b7d3c05-ff84-44fd-ae1b-9e745b9a9350.replay",
        3164,
        135,
        3289,
    ),
    (
        "../../test_corpus/largest_100/065_62d26477-6502-49ba-b48e-1990a4ea3e2b.replay",
        3217,
        122,
        3342,
    ),
    (
        "../../test_corpus/largest_100/066_0e3f475c-ab4e-45b3-8857-f0f5583da70b.replay",
        3032,
        65,
        3157,
    ),
    (
        "../../test_corpus/largest_100/068_fdb826bc-63a7-4aba-b6b9-70327ccd9af9.replay",
        3042,
        112,
        3167,
    ),
    (
        "../../test_corpus/largest_100/069_2ee7342c-a8cd-47cf-bc6e-536150bc2e2f.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/072_60e8a19d-6782-4599-b2c7-13194b1719f6.replay",
        2892,
        74,
        3017,
    ),
    (
        "../../test_corpus/largest_100/073_e435deab-aaed-4848-bdd0-c49858bce7e4.replay",
        3006,
        111,
        3163,
    ),
    (
        "../../test_corpus/largest_100/074_a6e89dc6-09ca-4c1a-b2da-c7383009ce8c.replay",
        3489,
        149,
        3614,
    ),
    (
        "../../test_corpus/largest_100/075_2533649e-b2d9-4438-9261-0e6eea032525.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/078_e4841be3-229e-410c-8a67-b88e76f46ade.replay",
        3006,
        111,
        3163,
    ),
    (
        "../../test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay",
        2838,
        117,
        3079,
    ),
    (
        "../../test_corpus/largest_100/082_ca9dcc03-e630-464a-a76d-8edb8fc78d0f.replay",
        3006,
        111,
        3131,
    ),
    (
        "../../test_corpus/largest_100/083_0d530715-6b10-421c-8af2-9b5b1feff4f6.replay",
        2848,
        111,
        3005,
    ),
    (
        "../../test_corpus/largest_100/085_24c94755-bf07-44ff-a745-17ec46fdf0dd.replay",
        3060,
        118,
        3185,
    ),
    (
        "../../test_corpus/largest_100/086_12e3b253-fa87-45b0-973b-307aafc0a41f.replay",
        3006,
        111,
        3163,
    ),
    (
        "../../test_corpus/largest_100/089_927d8bb2-1999-4a4d-aaf3-482dae6348c4.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/093_893c8162-4390-4fc3-bd87-5eba4b2b5065.replay",
        3200,
        112,
        3325,
    ),
    (
        "../../test_corpus/largest_100/094_5ca1d62e-ede6-4829-95cd-ac1f3b462750.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/095_544eb235-f537-4e93-955e-77c4a1ed3380.replay",
        2848,
        112,
        2973,
    ),
    (
        "../../test_corpus/largest_100/096_898e1ab6-2fe4-4446-8086-a5963a3b7b0c.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/097_ab8382c3-d2f8-4481-a0c0-5ea2d5b5653e.replay",
        3006,
        112,
        3131,
    ),
    (
        "../../test_corpus/largest_100/098_be5b3375-17ec-42f2-b58b-e2fca2e61ce4.replay",
        3218,
        139,
        3343,
    ),
    (
        "../../test_corpus/largest_100/100_1f669eef-b24a-45d8-9d67-bb5abf46b553.replay",
        3152,
        136,
        3277,
    ),
];

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

fn ad_prior(network: &[u8], plan: &ReplayNetworkLookupPlanV1, first_start: u64, actor_object: u32) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1{
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
    let t = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(network, &second, plan, k3_context()).expect("R3.18T payload");
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(network, &t, plan, k3_context()).expect("R3.18AD payload")
}

fn ag(network: &[u8], prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1) -> mimir_core::Result<mimir_replay::ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1>{
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(network, prior, k3_context())
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

#[test]
fn r3_18ag_frozen_af_lane_is_exact_47_of_47() {
    assert_eq!(AF_ROWS.len(), 47);
    for (index, &(path, first_start, actor_object, expected_start)) in AF_ROWS.iter().enumerate() {
        let (network, plan) = fixture(path, &format!("r318ag_af_{index:02}"));
        let prior = ad_prior(&network, &plan, first_start, actor_object);
        assert_eq!(prior.stop_bit, expected_start, "row {index} prior stop");
        let got = ag(&network, &prior).unwrap_or_else(|error| panic!("row {index} AG: {error}"));
        assert!(got.following_property_present, "row {index}");
        assert_eq!(
            got.property_present_start_bit, expected_start,
            "row {index}"
        );
        assert_eq!(
            got.property_present_end_bit,
            expected_start + 1,
            "row {index}"
        );
        assert_eq!(got.stop_bit, expected_start + 1, "row {index}");
    }
}

#[test]
fn r3_18ag_false_truncation_repeatability_and_post_control_poison_are_bounded() {
    let (network, plan) = fixture(
        "../../external_fixtures/sample_001.replay",
        "r318ag_controls",
    );
    let prior = ad_prior(&network, &plan, 10227, 98);
    let clean = ag(&network, &prior).unwrap();
    assert_eq!(ag(&network, &prior).unwrap(), clean);

    let mut false_network = network.clone();
    set_bit(&mut false_network, prior.stop_bit as usize, false);
    assert!(
        ag(&false_network, &prior)
            .unwrap_err()
            .to_string()
            .contains("unadmitted-false-control")
    );

    let bytes_before_control = usize::try_from(prior.stop_bit / 8).unwrap();
    assert!(ag(&network[..bytes_before_control], &prior).is_err());

    let mut poisoned = network.clone();
    for offset in 0..16usize {
        set_bit(
            &mut poisoned,
            clean.stop_bit as usize + offset,
            offset % 2 == 0,
        );
    }
    assert_eq!(ag(&poisoned, &prior).unwrap(), clean);
}

#[test]
fn r3_18ag_tampered_prior_boundary_tag_width_and_uid_shape_fail_closed() {
    let (network, plan) = fixture("../../external_fixtures/sample_001.replay", "r318ag_tamper");
    let prior = ad_prior(&network, &plan, 10227, 98);

    let mut bad_stop = prior.clone();
    bad_stop.stop_bit += 1;
    assert!(
        ag(&network, &bad_stop)
            .unwrap_err()
            .to_string()
            .contains("invalid-prior-stop")
    );

    let mut bad_header = prior.clone();
    bad_header
        .header_composition
        .following_header
        .resolved_attribute_tag = Some(ReplayNetworkAttributeTagV1::Int);
    assert!(
        ag(&network, &bad_header)
            .unwrap_err()
            .to_string()
            .contains("invalid-prior-payload")
    );

    let mut bad_width = prior.clone();
    if let ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::ActiveActor(decoded) = &mut bad_width.following_payload {
        decoded.payload_width = 32;
    } else { panic!("expected ActiveActor"); }
    assert!(
        ag(&network, &bad_width)
            .unwrap_err()
            .to_string()
            .contains("invalid-prior-payload")
    );

    let (uid_network, uid_plan) = fixture(
        "../../test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay",
        "r318ag_uid_tamper",
    );
    let mut uid_prior = ad_prior(&uid_network, &uid_plan, 2838, 117);
    if let ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::UniqueId(decoded) = &mut uid_prior.following_payload {
        if let ReplayNetworkK2ValueV1::UniqueId(value) = &mut decoded.value { value.system_id = 2; } else { panic!("expected UniqueId value"); }
    } else { panic!("expected UniqueId prior"); }
    assert!(
        ag(&uid_network, &uid_prior)
            .unwrap_err()
            .to_string()
            .contains("invalid-prior-payload")
    );
}

#[test]
fn r3_18ag_wrong_context_fails_before_control_read() {
    let (network, plan) = fixture(
        "../../external_fixtures/sample_001.replay",
        "r318ag_context",
    );
    let prior = ad_prior(&network, &plan, 10227, 98);
    let wrong = ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: true,
    };
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(&network, &prior, wrong).unwrap_err();
    assert!(error.to_string().contains("unadmitted-context"));
}

#[test]
fn r3_18ag_source_scope_is_exactly_one_bit_and_no_following_decode_or_loop() {
    let source = include_str!("../src/lib.rs");
    let start = source.find("pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1").expect("R3.18AG function");
    let tail = &source[start..];
    let end = tail.find("/// The published R3.18W true-only control is recomputed from the supplied R3.18T prior and used").expect("R3.18AA boundary after R3.18AG");
    let function = &tail[..end];
    assert_eq!(function.matches("cursor.read_bit()").count(), 1);
    assert!(!function.contains("lookup_plan"));
    assert!(!function.contains("decode_replay_network_existing_actor_first_property_header_v1("));
    assert!(!function.contains("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1("));
    assert!(!function.contains("\n    while "));
    assert!(!function.contains("\n    for "));
}
