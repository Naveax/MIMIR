include!("r3_18ba_post_ay_payload_control.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1 as decode_be,
};

fn expected_true_header(
    path: &str,
) -> Option<(u64, u32, u32, u8, u32, ReplayNetworkAttributeTagV1, u64)> {
    if path.ends_with("external_fixtures/sample_002.replay") {
        Some((
            11224,
            61,
            72,
            6,
            94,
            ReplayNetworkAttributeTagV1::Boolean,
            11230,
        ))
    } else if path.ends_with("external_fixtures/sample_003.replay") {
        Some((
            7808,
            62,
            72,
            6,
            92,
            ReplayNetworkAttributeTagV1::Boolean,
            7814,
        ))
    } else if path
        .ends_with("test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay")
    {
        Some((
            3160,
            52,
            110,
            6,
            58,
            ReplayNetworkAttributeTagV1::Float,
            3166,
        ))
    } else {
        None
    }
}

#[test]
fn r3_18be_exact_40_ba_rows_preserve_37_terminators_and_compose_three_exact_headers() {
    let (mut excluded, mut false_count, mut true_count) = (0usize, 0usize, 0usize);
    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318be_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        ).unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        ).unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));
        if au.following_header.is_none() {
            excluded += 1;
            continue;
        }
        let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au)
            .unwrap_or_else(|error| panic!("AY prerequisite row {index} {path}: {error}"));
        let ba = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay)
            .unwrap_or_else(|error| panic!("BA prerequisite row {index} {path}: {error}"));
        let got: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 = decode_be(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
        ).unwrap_or_else(|error| panic!("BE row {index} {path}: {error}"));

        assert_eq!(got.control, ba, "{path}");
        assert_eq!(got.context, k3_context(), "{path}");

        if !ba.following_property_present {
            false_count += 1;
            assert!(
                expected_true_header(path).is_none(),
                "unexpected false witness {path}"
            );
            assert!(got.following_header.is_none(), "{path}");
            assert_eq!(got.stop_bit, ba.stop_bit, "{path}");

            let mut poisoned = network.clone();
            let poison_bit = usize::try_from(ba.stop_bit).expect("false poison bit fits usize");
            assert!(poison_bit / 8 < poisoned.len(), "{path}");
            let poison_value = raw_lsb(&poisoned, ba.stop_bit);
            set_bit(&mut poisoned, poison_bit, !poison_value);
            let after_poison = decode_be(
                &poisoned,
                &prior,
                &control,
                &plan,
                k3_context(),
                &an,
                &ay,
                &ba,
            )
            .expect("false path must not inspect post-BA bits");
            assert_eq!(after_poison, got, "{path}");
            continue;
        }

        true_count += 1;
        let (
            expected_stream_start,
            expected_stream_id,
            expected_bound,
            expected_bits,
            expected_object,
            expected_tag,
            expected_payload_start,
        ) = expected_true_header(path).unwrap_or_else(|| panic!("unfrozen true witness {path}"));
        let header = got
            .following_header
            .as_ref()
            .expect("true BA must expose one header");
        assert!(header.property_present, "{path}");
        assert_eq!(header.actor_object_index, actor_object, "{path}");
        assert_eq!(
            header.property_present_start_bit, ba.property_present_start_bit,
            "{path}"
        );
        assert_eq!(
            header.property_present_end_bit, ba.property_present_end_bit,
            "{path}"
        );
        assert_eq!(
            header.stream_id_start_bit,
            Some(expected_stream_start),
            "{path}"
        );
        assert_eq!(expected_stream_start, ba.stop_bit, "{path}");
        assert_eq!(header.stream_id, Some(expected_stream_id), "{path}");
        assert_eq!(header.stream_id_bound, Some(expected_bound), "{path}");
        assert_eq!(header.prop_id_bits, Some(expected_bits), "{path}");
        assert_eq!(
            header.resolved_property_object_index,
            Some(expected_object),
            "{path}"
        );
        assert_eq!(header.resolved_attribute_tag, Some(expected_tag), "{path}");
        assert_eq!(
            header.payload_start_bit,
            Some(expected_payload_start),
            "{path}"
        );
        assert_eq!(header.stop_bit, expected_payload_start, "{path}");
        assert_eq!(got.stop_bit, expected_payload_start, "{path}");

        let repeated = decode_be(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
        )
        .expect("repeat R3.18BE");
        assert_eq!(repeated, got, "{path}");

        assert_eq!(
            ba.stop_bit % 8,
            0,
            "frozen true stream start must be byte-aligned"
        );
        let carrier_cut = usize::try_from(ba.stop_bit / 8).expect("carrier cut fits usize");
        assert!(
            decode_be(
                &network[..carrier_cut],
                &prior,
                &control,
                &plan,
                k3_context(),
                &an,
                &ay,
                &ba,
            )
            .is_err(),
            "truncation before true header stream must fail {path}"
        );

        let mut payload_poisoned = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("payload poison bit fits usize");
        assert!(poison_bit / 8 < payload_poisoned.len(), "{path}");
        let poison_value = raw_lsb(&payload_poisoned, got.stop_bit);
        set_bit(&mut payload_poisoned, poison_bit, !poison_value);
        let after_payload_poison = decode_be(
            &payload_poisoned,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
        )
        .expect("post-payload-start poison must not affect R3.18BE");
        assert_eq!(after_payload_poison, got, "{path}");
    }

    assert_eq!(excluded, 7, "upstream AU false-terminator drift");
    assert_eq!(false_count, 37, "R3.18BE false terminator drift");
    assert_eq!(true_count, 3, "R3.18BE true header drift");
    assert_eq!(excluded + false_count + true_count, 47);
}

#[test]
fn r3_18be_corrupt_ba_wrong_actor_lookup_and_context_drift_fail_closed() {
    let (path, first_start, actor_object, _) = au_cases()[1];
    assert!(path.ends_with("external_fixtures/sample_002.replay"));
    assert_eq!(actor_object, 106);
    let (network, plan) = frozen_network_and_plan(path, "r318be_negative");
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
    assert!(ba.following_property_present);

    let mut corrupt_ba = ba.clone();
    corrupt_ba.stop_bit += 1;
    assert!(
        decode_be(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &corrupt_ba
        )
        .is_err()
    );

    let mut wrong_actor = an.clone();
    wrong_actor
        .header_composition
        .following_header
        .actor_object_index = u32::MAX;
    assert!(
        decode_be(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &wrong_actor,
            &ay,
            &ba
        )
        .is_err()
    );

    let mut unresolved = plan.clone();
    let actor_lookup = unresolved.object_lookups[actor_object as usize]
        .as_mut()
        .expect("actor lookup");
    actor_lookup
        .properties
        .retain(|property| property.stream_id != 61);
    assert!(
        decode_be(
            &network,
            &prior,
            &control,
            &unresolved,
            k3_context(),
            &an,
            &ay,
            &ba
        )
        .is_err()
    );

    let mut wrong_context = k3_context();
    wrong_context.version_major -= 1;
    assert!(
        decode_be(
            &network,
            &prior,
            &control,
            &plan,
            wrong_context,
            &an,
            &ay,
            &ba
        )
        .is_err()
    );

    let mut wrong_rl223 = k3_context();
    wrong_rl223.is_rl_223 = true;
    assert!(
        decode_be(
            &network,
            &prior,
            &control,
            &plan,
            wrong_rl223,
            &an,
            &ay,
            &ba
        )
        .is_err()
    );
}

#[test]
fn r3_18be_source_scope_is_one_ba_recompute_one_suffix_header_no_control_reread_or_loop() {
    let source = include_str!("../src/lib.rs");
    let begin = source
        .find("// R3.18BE PRE-ADMISSION BEGIN bounded post-BA mixed-continuation following header")
        .expect("BE begin");
    let end_marker =
        "// R3.18BE PRE-ADMISSION END bounded post-BA mixed-continuation following header";
    let end = source[begin..]
        .find(end_marker)
        .map(|offset| begin + offset + end_marker.len())
        .expect("BE end");
    let block = &source[begin..end];

    assert_eq!(block.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(").count(), 1);
    assert_eq!(
        block
            .matches("decode_replay_network_existing_actor_property_header_suffix_v1(")
            .count(),
        1
    );
    assert_eq!(block.matches("cursor.read_bit()").count(), 0);
    assert_eq!(block.matches("NetworkBitCursor").count(), 0);
    assert_eq!(block.matches("read_bounded_u32(").count(), 0);
    assert_eq!(
        block
            .matches("decode_replay_network_existing_actor_first_property_header_v1(")
            .count(),
        0
    );
    assert!(!block.contains("\n    while "));
    assert!(!block.contains("\n    for "));
    assert!(!block.contains("\n    loop {"));

    assert_eq!(
        source
            .matches("decode_replay_network_existing_actor_property_header_suffix_v1(")
            .count(),
        3,
        "one definition plus R3.16B and R3.18BE calls"
    );
}
