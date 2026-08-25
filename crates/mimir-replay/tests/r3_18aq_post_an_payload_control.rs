include!("r3_18an_post_ak_payload.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1,
};

fn aq_from_frozen(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
    first_start: u64,
    actor_object: u32,
) -> (
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
){
    let prior = frozen_ad_prior(network, plan, first_start, actor_object);
    let control = ag_control(network, &prior);
    let an = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
        network,
        &prior,
        &control,
        plan,
        k3_context(),
    )
    .expect("R3.18AN frozen prerequisite");
    (prior, control, an)
}

fn raw_lsb(bytes: &[u8], bit: u64) -> bool {
    let bit = usize::try_from(bit).expect("bit fits usize");
    ((bytes[bit / 8] >> (bit % 8)) & 1) != 0
}

#[test]
fn r3_18aq_all_47_frozen_ap_rows_accept_mixed_boolean_and_stop_exactly_one_bit_later() {
    let cases: [(&str, u64, u32, u64); 47] = [
        (
            "../../external_fixtures/sample_001.replay",
            10227,
            98,
            10392,
        ),
        (
            "../../external_fixtures/sample_002.replay",
            11019,
            106,
            11184,
        ),
        ("../../external_fixtures/sample_003.replay", 7603, 103, 7768),
        (
            "../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay",
            2848,
            112,
            3012,
        ),
        (
            "../../test_corpus/largest_100/010_27f8a623-4388-41da-9473-5f59df5fa93b.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay",
            3164,
            114,
            3360,
        ),
        (
            "../../test_corpus/largest_100/012_0c83fe49-b7f6-427a-ae97-b1a4f53d6117.replay",
            3042,
            112,
            3206,
        ),
        (
            "../../test_corpus/largest_100/016_b473f51b-abdd-4896-872f-26fb7d8bd939.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/019_bd1a83e2-5ac0-4a79-beba-df8547515782.replay",
            3006,
            111,
            3202,
        ),
        (
            "../../test_corpus/largest_100/023_d9186df1-af02-4ab1-ba1b-b2c3b6fb1a67.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/027_abfd6c12-e5e0-46a3-aaee-4d086a4d6ee5.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/033_e8ab232b-24e4-401c-b5ac-db2d5587cfcf.replay",
            3168,
            127,
            3332,
        ),
        (
            "../../test_corpus/largest_100/035_6b90776b-1784-4d30-a8ff-d37b66ae4a38.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/036_88b815c9-bc3d-498a-8fa3-80638cfa8709.replay",
            3243,
            120,
            3407,
        ),
        (
            "../../test_corpus/largest_100/038_c44e3655-bcc9-41fb-9548-808ee70c66e7.replay",
            2892,
            74,
            3056,
        ),
        (
            "../../test_corpus/largest_100/039_4c5e5ad8-c72f-49b2-890c-d936e172160c.replay",
            3006,
            111,
            3202,
        ),
        (
            "../../test_corpus/largest_100/040_0a38f81b-862d-4776-9d27-3c221355f839.replay",
            3006,
            111,
            3170,
        ),
        (
            "../../test_corpus/largest_100/042_be1e76bd-258a-4067-8d06-57481459f946.replay",
            3042,
            112,
            3206,
        ),
        (
            "../../test_corpus/largest_100/049_6c45a00b-d14b-4eba-86b8-4a3e99faf545.replay",
            3164,
            111,
            3328,
        ),
        (
            "../../test_corpus/largest_100/050_6e301fcc-239b-4a29-863b-8c2561e56042.replay",
            2970,
            135,
            3134,
        ),
        (
            "../../test_corpus/largest_100/054_9ed418f3-9eaf-4a18-a591-633db1120790.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/057_4fab5b3d-17de-4a7b-86d7-432ba973c524.replay",
            3042,
            111,
            3206,
        ),
        (
            "../../test_corpus/largest_100/059_d86eb20b-396c-49bc-80bb-71bec6949f94.replay",
            3243,
            120,
            3407,
        ),
        (
            "../../test_corpus/largest_100/060_6bc2e5f5-e243-4db0-b6f9-1b8173472c29.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/061_2b7d3c05-ff84-44fd-ae1b-9e745b9a9350.replay",
            3164,
            135,
            3328,
        ),
        (
            "../../test_corpus/largest_100/065_62d26477-6502-49ba-b48e-1990a4ea3e2b.replay",
            3217,
            122,
            3381,
        ),
        (
            "../../test_corpus/largest_100/066_0e3f475c-ab4e-45b3-8857-f0f5583da70b.replay",
            3032,
            65,
            3196,
        ),
        (
            "../../test_corpus/largest_100/068_fdb826bc-63a7-4aba-b6b9-70327ccd9af9.replay",
            3042,
            112,
            3206,
        ),
        (
            "../../test_corpus/largest_100/069_2ee7342c-a8cd-47cf-bc6e-536150bc2e2f.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/072_60e8a19d-6782-4599-b2c7-13194b1719f6.replay",
            2892,
            74,
            3056,
        ),
        (
            "../../test_corpus/largest_100/073_e435deab-aaed-4848-bdd0-c49858bce7e4.replay",
            3006,
            111,
            3202,
        ),
        (
            "../../test_corpus/largest_100/074_a6e89dc6-09ca-4c1a-b2da-c7383009ce8c.replay",
            3489,
            149,
            3653,
        ),
        (
            "../../test_corpus/largest_100/075_2533649e-b2d9-4438-9261-0e6eea032525.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/078_e4841be3-229e-410c-8a67-b88e76f46ade.replay",
            3006,
            111,
            3202,
        ),
        (
            "../../test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay",
            2838,
            117,
            3119,
        ),
        (
            "../../test_corpus/largest_100/082_ca9dcc03-e630-464a-a76d-8edb8fc78d0f.replay",
            3006,
            111,
            3170,
        ),
        (
            "../../test_corpus/largest_100/083_0d530715-6b10-421c-8af2-9b5b1feff4f6.replay",
            2848,
            111,
            3044,
        ),
        (
            "../../test_corpus/largest_100/085_24c94755-bf07-44ff-a745-17ec46fdf0dd.replay",
            3060,
            118,
            3224,
        ),
        (
            "../../test_corpus/largest_100/086_12e3b253-fa87-45b0-973b-307aafc0a41f.replay",
            3006,
            111,
            3202,
        ),
        (
            "../../test_corpus/largest_100/089_927d8bb2-1999-4a4d-aaf3-482dae6348c4.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/093_893c8162-4390-4fc3-bd87-5eba4b2b5065.replay",
            3200,
            112,
            3364,
        ),
        (
            "../../test_corpus/largest_100/094_5ca1d62e-ede6-4829-95cd-ac1f3b462750.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/095_544eb235-f537-4e93-955e-77c4a1ed3380.replay",
            2848,
            112,
            3012,
        ),
        (
            "../../test_corpus/largest_100/096_898e1ab6-2fe4-4446-8086-a5963a3b7b0c.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/097_ab8382c3-d2f8-4481-a0c0-5ea2d5b5653e.replay",
            3006,
            112,
            3170,
        ),
        (
            "../../test_corpus/largest_100/098_be5b3375-17ec-42f2-b58b-e2fca2e61ce4.replay",
            3218,
            139,
            3382,
        ),
        (
            "../../test_corpus/largest_100/100_1f669eef-b24a-45d8-9d67-bb5abf46b553.replay",
            3152,
            136,
            3316,
        ),
    ];

    let mut false_count = 0usize;
    let mut true_count = 0usize;

    for (index, (path, first_start, actor_object, control_start)) in cases.into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318aq_frozen_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        assert_eq!(an.stop_bit, control_start, "{path}");

        let expected = raw_lsb(&network, control_start);
        let got: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
        )
        .unwrap_or_else(|error| panic!("AQ frozen row {index} {path}: {error}"));

        assert_eq!(got.payload_composition, an, "{path}");
        assert_eq!(got.following_property_present, expected, "{path}");
        assert_eq!(got.property_present_start_bit, control_start, "{path}");
        assert_eq!(got.property_present_end_bit, control_start + 1, "{path}");
        assert_eq!(got.stop_bit, control_start + 1, "{path}");

        if got.following_property_present {
            true_count += 1;
        } else {
            false_count += 1;
        }

        let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
        )
        .expect("repeat frozen R3.18AQ");
        assert_eq!(repeated, got, "{path}");

        let mut poisoned = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("poison bit fits usize");
        assert!(poison_bit / 8 < poisoned.len(), "{path}");
        let poison_value = raw_lsb(&poisoned, got.stop_bit);
        set_bit(&mut poisoned, poison_bit, !poison_value);
        let after_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &poisoned,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
        )
        .expect("post-control poison must not affect R3.18AQ");
        assert_eq!(after_poison, got, "{path}");
    }

    assert_eq!(false_count, 7, "R3.18AP false distribution drift");
    assert_eq!(true_count, 40, "R3.18AP true distribution drift");
    assert_eq!(false_count + true_count, 47);
}

#[test]
fn r3_18aq_wrong_actor_and_unresolved_lookup_fail_closed() {
    let (network, plan) = sample_network_and_plan();
    let prior = ad_prior(&network, &plan);
    let control = ag_control(&network, &prior);
    let an = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
        &network,
        &prior,
        &control,
        &plan,
        k3_context(),
    )
    .expect("sample R3.18AN authority");

    let mut bad_prior = prior.clone();
    bad_prior
        .header_composition
        .following_header
        .actor_object_index = u32::MAX;
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &bad_prior,
            &control,
            &plan,
            k3_context(),
            &an,
        )
        .is_err(),
        "wrong actor authority must reject before advancing the AQ control boundary"
    );

    let mut missing_lookup = plan.clone();
    missing_lookup.object_lookups[98] = None;
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &prior,
            &control,
            &missing_lookup,
            k3_context(),
            &an,
        )
        .is_err(),
        "unresolved actor lookup must reject before advancing the AQ control boundary"
    );
}

#[test]
fn r3_18aq_truncation_corrupt_prior_and_wrong_context_fail_closed() {
    let (network, plan) = sample_network_and_plan();
    let prior = ad_prior(&network, &plan);
    let control = ag_control(&network, &prior);
    let an = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
        &network,
        &prior,
        &control,
        &plan,
        k3_context(),
    )
    .expect("sample R3.18AN");
    assert_eq!(an.stop_bit, 10392);
    assert_eq!(an.stop_bit % 8, 0);

    let exact_payload_bytes = usize::try_from(an.stop_bit / 8).unwrap();
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network[..exact_payload_bytes],
        &prior,
        &control,
        &plan,
        k3_context(),
        &an,
    )
    .expect_err("missing following control bit must reject");
    assert!(error.to_string().contains("insufficient-bits"), "{error}");

    let mut corrupt = an.clone();
    corrupt.stop_bit += 1;
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &corrupt,
        )
        .is_err()
    );

    let mut wrong_context = k3_context();
    wrong_context.version_major -= 1;
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &prior,
            &control,
            &plan,
            wrong_context,
            &an,
        )
        .is_err()
    );
}

#[test]
fn r3_18aq_source_scope_is_one_an_recompute_one_read_bit_and_no_following_decode_or_loop() {
    let source = include_str!("../src/lib.rs");
    let begin = source
        .find("// R3.18AQ PRE-ADMISSION BEGIN bounded post-AN following control")
        .expect("R3.18AQ begin marker");
    let end_marker = "// R3.18AQ PRE-ADMISSION END bounded post-AN following control";
    let end = source[begin..]
        .find(end_marker)
        .map(|offset| begin + offset + end_marker.len())
        .expect("R3.18AQ end marker");
    let block = &source[begin..end];

    assert_eq!(block.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(").count(), 1);
    assert_eq!(block.matches("cursor.read_bit()").count(), 1);
    assert!(!block.contains("cursor.read_bits_le("));
    assert!(!block.contains("read_bounded_u32("));
    assert!(!block.contains("decode_replay_network_existing_actor_property_header_v1("));
    assert!(!block.contains("decode_replay_network_primitive_scalar_v1("));
    assert!(!block.contains("unadmitted-following-control-false"));
    assert!(!block.contains("if !following_property_present"));
    assert!(!block.contains("\n    while "));
    assert!(!block.contains("\n    for "));
}
