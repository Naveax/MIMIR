include!("r3_18bo_post_bk_following_header.rs");

use mimir_replay::{
    ReplayNetworkPostBoFollowingPayloadDecodeV1 as R3_18BsResultV1,
    ReplayNetworkPostBoFollowingPayloadValueV1 as R3_18BsPayloadValueV1,
    decode_replay_network_post_bo_following_payload_v1 as decode_bs,
};

fn expected_bs_payload(path: &str) -> Option<(ReplayNetworkAttributeTagV1, u64, u64)> {
    if path.ends_with("external_fixtures/sample_002.replay") {
        Some((ReplayNetworkAttributeTagV1::Boolean, 11238, 11239))
    } else if path
        .ends_with("test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay")
    {
        Some((ReplayNetworkAttributeTagV1::ActiveActor, 3205, 3238))
    } else {
        None
    }
}

#[test]
fn r3_18bs_exact_bq_lane_composes_two_payloads_and_rejects_false_terminator() {
    let (
        mut excluded_au,
        mut excluded_be,
        mut bo_rows,
        mut false_terminators,
        mut boolean_rows,
        mut active_actor_rows,
    ) = (0usize, 0usize, 0usize, 0usize, 0usize, 0usize);

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318bs_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        ).unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        ).unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));

        if au.following_header.is_none() {
            excluded_au += 1;
            continue;
        }

        let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au)
            .unwrap_or_else(|error| panic!("AY prerequisite row {index} {path}: {error}"));
        let ba = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay)
            .unwrap_or_else(|error| panic!("BA prerequisite row {index} {path}: {error}"));
        let be = decode_be(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
        )
        .unwrap_or_else(|error| panic!("BE prerequisite row {index} {path}: {error}"));

        if be.following_header.is_none() {
            excluded_be += 1;
            continue;
        }

        let bi = decode_bi(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
        )
        .unwrap_or_else(|error| panic!("BI prerequisite row {index} {path}: {error}"));
        let bk = decode_bk(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
        )
        .unwrap_or_else(|error| panic!("BK prerequisite row {index} {path}: {error}"));
        let bo = decode_bo(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
        )
        .unwrap_or_else(|error| panic!("BO prerequisite row {index} {path}: {error}"));
        bo_rows += 1;

        if bo.following_header.is_none() {
            false_terminators += 1;
            assert!(
                path.ends_with("external_fixtures/sample_003.replay"),
                "{path}"
            );
            assert!(expected_bs_payload(path).is_none(), "{path}");
            let error = decode_bs(
                &network,
                &prior,
                &control,
                &plan,
                k3_context(),
                &an,
                &ay,
                &ba,
                &be,
                &bi,
                &bk,
                &bo,
            )
            .expect_err("R3.18BO false terminator must stay outside BS payload lane");
            assert!(
                error
                    .to_string()
                    .contains("false-terminator-has-no-payload"),
                "unexpected false terminator error: {error}"
            );
            continue;
        }

        let got: R3_18BsResultV1 = decode_bs(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
            &bo,
        )
        .unwrap_or_else(|error| panic!("BS row {index} {path}: {error}"));
        assert_eq!(got.header_composition, bo, "{path}");

        let (expected_tag, expected_start, expected_end) =
            expected_bs_payload(path).unwrap_or_else(|| panic!("unfrozen BS witness {path}"));
        assert_eq!(bo.stop_bit, expected_start, "{path}");
        assert_eq!(got.stop_bit, expected_end, "{path}");

        match (&got.following_payload, expected_tag) {
            (R3_18BsPayloadValueV1::Boolean(decoded), ReplayNetworkAttributeTagV1::Boolean) => {
                boolean_rows += 1;
                assert_eq!(
                    decoded.attribute_tag,
                    ReplayNetworkAttributeTagV1::Boolean,
                    "{path}"
                );
                assert_eq!(decoded.payload_start_bit, expected_start, "{path}");
                assert_eq!(decoded.payload_width, 1, "{path}");
                assert_eq!(decoded.payload_end_bit, expected_end, "{path}");
                assert_eq!(decoded.stop_bit, expected_end, "{path}");
                assert_eq!(
                    decoded.value,
                    ReplayNetworkPrimitiveScalarValueV1::Boolean(true),
                    "{path}"
                );
                let direct = mimir_replay::decode_replay_network_primitive_scalar_v1(
                    &network,
                    expected_start,
                    ReplayNetworkAttributeTagV1::Boolean,
                )
                .expect("direct BQ Boolean payload");
                assert_eq!(decoded, &direct, "{path}");
            }
            (
                R3_18BsPayloadValueV1::ActiveActor(decoded),
                ReplayNetworkAttributeTagV1::ActiveActor,
            ) => {
                active_actor_rows += 1;
                assert_eq!(
                    decoded.attribute_tag,
                    ReplayNetworkAttributeTagV1::ActiveActor,
                    "{path}"
                );
                assert_eq!(decoded.payload_start_bit, expected_start, "{path}");
                assert_eq!(decoded.payload_width, 33, "{path}");
                assert_eq!(decoded.payload_end_bit, expected_end, "{path}");
                assert_eq!(
                    decoded.value,
                    mimir_replay::ReplayNetworkK2ValueV1::ActiveActor {
                        active: true,
                        actor: 1,
                    },
                    "{path}"
                );
                let direct = mimir_replay::decode_replay_network_k2_v1(
                    &network,
                    expected_start,
                    ReplayNetworkAttributeTagV1::ActiveActor,
                    mimir_replay::ReplayNetworkK2DecodeContextV1 {
                        net_version: 10,
                        is_rl_223: false,
                    },
                )
                .expect("direct BQ ActiveActor payload");
                assert_eq!(decoded, &direct, "{path}");
            }
            (payload, tag) => {
                panic!("unexpected BS payload/tag pair {payload:?}/{tag:?} for {path}")
            }
        }

        let repeated = decode_bs(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
            &bo,
        )
        .expect("repeat BS payload");
        assert_eq!(repeated, got, "{path}");

        let mut next_control_poisoned = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("BR poison bit fits usize");
        assert!(poison_bit / 8 < next_control_poisoned.len(), "{path}");
        let old = raw_lsb(&next_control_poisoned, got.stop_bit);
        set_bit(&mut next_control_poisoned, poison_bit, !old);
        let after_poison = decode_bs(
            &next_control_poisoned,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
            &bo,
        )
        .expect("BR control poison must not affect BS payload result");
        assert_eq!(after_poison, got, "{path}");

        let mut corrupt_bo = bo.clone();
        corrupt_bo.stop_bit += 1;
        assert!(
            decode_bs(
                &network,
                &prior,
                &control,
                &plan,
                k3_context(),
                &an,
                &ay,
                &ba,
                &be,
                &bi,
                &bk,
                &corrupt_bo,
            )
            .is_err(),
            "corrupt BO authority must fail for {path}"
        );

        let wrong_context = ReplayNetworkK3DecodeContextV1 {
            version_major: 868,
            version_minor: 32,
            net_version: 10,
            is_rl_223: true,
        };
        assert!(
            decode_bs(
                &network,
                &prior,
                &control,
                &plan,
                wrong_context,
                &an,
                &ay,
                &ba,
                &be,
                &bi,
                &bk,
                &bo,
            )
            .is_err(),
            "wrong context must fail for {path}"
        );

        if expected_tag == ReplayNetworkAttributeTagV1::ActiveActor {
            let cut = usize::try_from(expected_start.div_ceil(8) + 1)
                .expect("partial ActiveActor payload cut fits usize");
            assert!(cut < network.len(), "{path}");
            assert!(
                decode_bs(
                    &network[..cut],
                    &prior,
                    &control,
                    &plan,
                    k3_context(),
                    &an,
                    &ay,
                    &ba,
                    &be,
                    &bi,
                    &bk,
                    &bo,
                )
                .is_err(),
                "partial ActiveActor payload must fail"
            );

            let mut wrong_tag_bo = bo.clone();
            wrong_tag_bo
                .following_header
                .as_mut()
                .expect("true BO header")
                .resolved_attribute_tag = Some(ReplayNetworkAttributeTagV1::Float);
            assert!(
                decode_bs(
                    &network,
                    &prior,
                    &control,
                    &plan,
                    k3_context(),
                    &an,
                    &ay,
                    &ba,
                    &be,
                    &bi,
                    &bk,
                    &wrong_tag_bo,
                )
                .is_err(),
                "fabricated/wrong BN tag must fail"
            );

            let mut wrong_actor_bo = bo.clone();
            wrong_actor_bo
                .following_header
                .as_mut()
                .expect("true BO header")
                .actor_object_index += 1;
            assert!(
                decode_bs(
                    &network,
                    &prior,
                    &control,
                    &plan,
                    k3_context(),
                    &an,
                    &ay,
                    &ba,
                    &be,
                    &bi,
                    &bk,
                    &wrong_actor_bo,
                )
                .is_err(),
                "wrong actor BO header must fail"
            );
        }
    }

    assert_eq!(excluded_au, 7, "upstream AU false-terminator drift");
    assert_eq!(excluded_be, 37, "BE false-terminator drift");
    assert_eq!(bo_rows, 3, "BO authority row drift");
    assert_eq!(false_terminators, 1, "BO false terminator drift");
    assert_eq!(boolean_rows, 1, "BQ Boolean row drift");
    assert_eq!(active_actor_rows, 1, "BQ ActiveActor row drift");
    assert_eq!(
        excluded_au + excluded_be + false_terminators + boolean_rows + active_actor_rows,
        47
    );
}

#[test]
fn r3_18bs_source_scope_is_one_bo_recompute_two_closed_decoders_and_no_control_read_or_loop() {
    let source = include_str!("../src/lib.rs");
    let begin_marker = "// R3.18BS PRE-ADMISSION BEGIN bounded post-BO one-following-payload";
    let end_marker = "// R3.18BS PRE-ADMISSION END bounded post-BO one-following-payload";
    let begin = source.find(begin_marker).expect("BS begin marker");
    let relative_end = source[begin..].find(end_marker).expect("BS end marker");
    let block = &source[begin..begin + relative_end + end_marker.len()];

    assert_eq!(
        block.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_following_header_v1(").count(),
        1,
        "BS must recompute BO exactly once",
    );
    assert_eq!(
        block
            .matches("decode_replay_network_primitive_scalar_v1(")
            .count(),
        1,
        "BS must invoke the Boolean scalar decoder exactly once in source",
    );
    assert_eq!(
        block.matches("decode_replay_network_k2_v1(").count(),
        1,
        "BS must invoke the ActiveActor K2 decoder exactly once in source",
    );
    assert_eq!(
        block.matches(".read_bit(").count(),
        0,
        "BS must not directly consume the R3.18BR or later control bit",
    );
    assert!(
        !block.contains("while "),
        "BS must not contain a while loop"
    );
    assert!(
        !block.contains("loop {"),
        "BS must not contain a generic loop"
    );
}
