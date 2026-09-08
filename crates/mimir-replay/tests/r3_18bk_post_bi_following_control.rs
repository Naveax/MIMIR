include!("r3_18bi_post_be_following_payload.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_v1 as decode_bk,
};

fn expected_bh_control(path: &str) -> Option<(u64, bool)> {
    if path.ends_with("external_fixtures/sample_002.replay") {
        Some((11231, true))
    } else if path.ends_with("external_fixtures/sample_003.replay") {
        Some((7815, false))
    } else if path
        .ends_with("test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay")
    {
        Some((3198, true))
    } else {
        None
    }
}

#[test]
fn r3_18bk_exact_three_bh_rows_accept_mixed_boolean_and_stop_one_bit_later() {
    let (mut excluded_au, mut excluded_be, mut produced, mut false_count, mut true_count) =
        (0usize, 0usize, 0usize, 0usize, 0usize);

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318bk_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        ).unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        ).unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));

        if au.following_header.is_none() {
            excluded_au += 1;
            assert!(
                expected_bh_control(path).is_none(),
                "unexpected BH authority {path}"
            );
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
            assert!(
                expected_bh_control(path).is_none(),
                "unexpected BH authority {path}"
            );
            assert!(
                decode_bi(
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
                .is_err(),
                "BE false terminator reached BI/BK production {path}"
            );
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
        let (expected_start, expected_value) =
            expected_bh_control(path).unwrap_or_else(|| panic!("unfrozen BK witness {path}"));

        let got: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 =
            decode_bk(
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
            .unwrap_or_else(|error| panic!("BK row {index} {path}: {error}"));

        assert_eq!(got.payload_composition, bi, "{path}");
        assert_eq!(got.property_present_start_bit, expected_start, "{path}");
        assert_eq!(
            got.property_present_start_bit, got.payload_composition.stop_bit,
            "{path}"
        );
        assert_eq!(got.property_present, expected_value, "{path}");
        assert_eq!(raw_lsb(&network, expected_start), expected_value, "{path}");
        assert_eq!(got.property_present_end_bit, expected_start + 1, "{path}");
        assert_eq!(got.stop_bit, expected_start + 1, "{path}");

        if got.property_present {
            true_count += 1;
        } else {
            false_count += 1;
        }
        produced += 1;

        let repeated = decode_bk(
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
        .expect("repeat R3.18BK");
        assert_eq!(repeated, got, "{path}");

        let mut poisoned = network.clone();
        let after_stop = usize::try_from(got.stop_bit).expect("post-BK poison bit fits usize");
        assert!(after_stop / 8 < poisoned.len(), "{path}");
        let old = raw_lsb(&poisoned, got.stop_bit);
        set_bit(&mut poisoned, after_stop, !old);
        let after_poison = decode_bk(
            &poisoned,
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
        .expect("BK must not inspect bits after its stop");
        assert_eq!(after_poison, got, "{path}");
    }

    assert_eq!(excluded_au, 7, "upstream AU false terminator drift");
    assert_eq!(excluded_be, 37, "BE false terminator drift");
    assert_eq!(produced, 3, "BH authority row drift");
    assert_eq!(false_count, 1, "BH false distribution drift");
    assert_eq!(true_count, 2, "BH true distribution drift");
    assert_eq!(excluded_au + excluded_be + produced, 47);
}

#[test]
fn r3_18bk_corrupt_bi_context_lookup_and_truncation_fail_closed() {
    let (path, first_start, actor_object, _) = au_cases()
        .iter()
        .copied()
        .find(|(path, _, _, _)| path.ends_with("external_fixtures/sample_002.replay"))
        .expect("sample_002 BK witness");
    let (network, plan) = frozen_network_and_plan(path, "r318bk_negative");
    let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
    let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network, &prior, &control, &plan, k3_context(), &an,
    ).expect("AQ prerequisite");
    let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, k3_context(), &an, &aq,
    ).expect("AU prerequisite");
    let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au)
        .expect("AY prerequisite");
    let ba = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay)
        .expect("BA prerequisite");
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
    .expect("BE prerequisite");
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
    .expect("BI prerequisite");
    assert_eq!(bi.stop_bit, 11231);

    let mut corrupt_stop = bi.clone();
    corrupt_stop.stop_bit += 1;
    assert!(
        decode_bk(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &corrupt_stop,
        )
        .is_err()
    );

    let mut corrupt_value = bi.clone();
    corrupt_value.following_payload.value = ReplayNetworkPrimitiveScalarValueV1::Boolean(false);
    assert!(
        decode_bk(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &corrupt_value,
        )
        .is_err()
    );

    let mut wrong_context = k3_context();
    wrong_context.version_minor -= 1;
    assert!(
        decode_bk(
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
        )
        .is_err()
    );

    let mut unresolved = plan.clone();
    unresolved.object_lookups[actor_object as usize]
        .as_mut()
        .expect("actor lookup")
        .properties
        .clear();
    assert!(
        decode_bk(
            &network,
            &prior,
            &control,
            &unresolved,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
        )
        .is_err()
    );

    let cut = usize::try_from(bi.stop_bit / 8).expect("byte truncation");
    assert!(
        decode_bk(
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
        )
        .is_err()
    );
}

#[test]
fn r3_18bk_source_scope_is_one_bi_recompute_one_read_bit_and_no_following_decode_or_loop() {
    let source = include_str!("../src/lib.rs");
    let begin = source
        .find("// R3.18BK PRE-ADMISSION BEGIN bounded post-BI following control")
        .expect("BK begin");
    let end_marker = "// R3.18BK PRE-ADMISSION END bounded post-BI following control";
    let end = source[begin..]
        .find(end_marker)
        .map(|offset| begin + offset + end_marker.len())
        .expect("BK end");
    let block = &source[begin..end];

    assert_eq!(
        block.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(").count(),
        1
    );
    assert_eq!(block.matches("cursor.read_bit()").count(), 1);
    assert_eq!(block.matches("NetworkBitCursor::new(").count(), 1);
    assert_eq!(
        block
            .matches("decode_replay_network_primitive_scalar_v1(")
            .count(),
        0
    );
    assert_eq!(
        block
            .matches("decode_replay_network_existing_actor_property_header_suffix_v1(")
            .count(),
        0
    );
    assert!(!block.contains("\n    while "));
    assert!(!block.contains("\n    for "));
    assert!(!block.contains("\n    loop {"));
}
