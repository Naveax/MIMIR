include!("r3_18ay_post_au_payload.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1 as decode_ba,
};

#[test]
fn r3_18ba_exact_40_ay_rows_accept_mixed_boolean_and_stop_exactly_one_bit_later() {
    let (mut excluded, mut false_count, mut true_count) = (0usize, 0usize, 0usize);
    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318ba_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        ).unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        ).unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));

        if au.following_header.is_none() {
            excluded += 1;
            assert!(decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).is_err());
            continue;
        }

        let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au)
            .unwrap_or_else(|error| panic!("AY prerequisite row {index} {path}: {error}"));
        let expected = raw_lsb(&network, ay.stop_bit);
        let got: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 =
            decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay)
                .unwrap_or_else(|error| panic!("BA row {index} {path}: {error}"));

        assert_eq!(got.payload_composition, ay, "{path}");
        assert_eq!(got.following_property_present, expected, "{path}");
        assert_eq!(got.property_present_start_bit, ay.stop_bit, "{path}");
        assert_eq!(got.property_present_end_bit, ay.stop_bit + 1, "{path}");
        assert_eq!(got.stop_bit, ay.stop_bit + 1, "{path}");
        if got.following_property_present {
            true_count += 1;
        } else {
            false_count += 1;
        }

        let repeated = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay)
            .expect("repeat R3.18BA");
        assert_eq!(repeated, got, "{path}");

        let mut poisoned = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("poison bit fits usize");
        assert!(poison_bit / 8 < poisoned.len(), "{path}");
        let poison_value = raw_lsb(&poisoned, got.stop_bit);
        set_bit(&mut poisoned, poison_bit, !poison_value);
        let after_poison = decode_ba(&poisoned, &prior, &control, &plan, k3_context(), &an, &ay)
            .expect("post-control poison must not affect R3.18BA");
        assert_eq!(after_poison, got, "{path}");
    }

    assert_eq!(excluded, 7, "upstream AU false-terminator drift");
    assert_eq!(false_count, 37, "R3.18AX false distribution drift");
    assert_eq!(true_count, 3, "R3.18AX true distribution drift");
    assert_eq!(excluded + false_count + true_count, 47);
}

#[test]
fn r3_18ba_prerequisite_corruption_truncation_and_context_drift_fail_closed() {
    let (path, first_start, actor_object, _) = au_cases()[0];
    let (network, plan) = frozen_network_and_plan(path, "r318ba_negative");
    let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
    let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network, &prior, &control, &plan, k3_context(), &an,
    ).expect("AQ prerequisite");
    let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, k3_context(), &an, &aq,
    ).expect("AU prerequisite");
    let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au)
        .expect("AY prerequisite");

    let mut corrupt_ay = ay.clone();
    corrupt_ay.stop_bit += 1;
    assert!(
        decode_ba(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &corrupt_ay
        )
        .is_err()
    );

    let mut bad_prior = prior.clone();
    bad_prior
        .header_composition
        .following_header
        .actor_object_index = u32::MAX;
    assert!(
        decode_ba(
            &network,
            &bad_prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay
        )
        .is_err()
    );

    let mut missing_lookup = plan.clone();
    missing_lookup.object_lookups[98] = None;
    assert!(
        decode_ba(
            &network,
            &prior,
            &control,
            &missing_lookup,
            k3_context(),
            &an,
            &ay
        )
        .is_err()
    );

    let mut wrong_context = k3_context();
    wrong_context.version_major -= 1;
    assert!(decode_ba(&network, &prior, &control, &plan, wrong_context, &an, &ay).is_err());

    let carrier_cut = usize::try_from(ay.stop_bit / 8).expect("carrier cut fits usize");
    assert!(
        decode_ba(
            &network[..carrier_cut],
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay
        )
        .is_err()
    );
}

#[test]
fn r3_18ba_source_scope_is_one_ay_recompute_one_read_bit_and_no_following_decode_or_loop() {
    let source = include_str!("../src/lib.rs");
    let begin = source
        .find("// R3.18BA PRE-ADMISSION BEGIN bounded post-AY mixed following control")
        .expect("BA begin");
    let end_marker = "// R3.18BA PRE-ADMISSION END bounded post-AY mixed following control";
    let end = source[begin..]
        .find(end_marker)
        .map(|offset| begin + offset + end_marker.len())
        .expect("BA end");
    let block = &source[begin..end];
    assert_eq!(block.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(").count(), 1);
    assert_eq!(block.matches("cursor.read_bit()").count(), 1);
    assert!(!block.contains("cursor.read_bits_le("));
    assert!(!block.contains("read_bounded_u32("));
    assert!(!block.contains("decode_replay_network_existing_actor_property_header_v1("));
    assert!(!block.contains("decode_replay_network_primitive_scalar_v1("));
    assert!(!block.contains("if !following_property_present"));
    assert!(!block.contains("\n    while "));
    assert!(!block.contains("\n    for "));
}
