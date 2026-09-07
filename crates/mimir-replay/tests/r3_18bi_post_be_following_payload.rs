include!("r3_18be_post_ba_following_header.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1 as decode_bi,
};

fn expected_bi_payload(
    path: &str,
) -> Option<(
    ReplayNetworkAttributeTagV1,
    u64,
    u64,
    u8,
    ReplayNetworkPrimitiveScalarValueV1,
)> {
    if path.ends_with("external_fixtures/sample_002.replay") {
        Some((
            ReplayNetworkAttributeTagV1::Boolean,
            11230,
            11231,
            1,
            ReplayNetworkPrimitiveScalarValueV1::Boolean(true),
        ))
    } else if path.ends_with("external_fixtures/sample_003.replay") {
        Some((
            ReplayNetworkAttributeTagV1::Boolean,
            7814,
            7815,
            1,
            ReplayNetworkPrimitiveScalarValueV1::Boolean(true),
        ))
    } else if path
        .ends_with("test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay")
    {
        let raw_bits = 1_072_986_849u32;
        Some((
            ReplayNetworkAttributeTagV1::Float,
            3166,
            3198,
            32,
            ReplayNetworkPrimitiveScalarValueV1::Float {
                raw_bits,
                value: f32::from_bits(raw_bits),
            },
        ))
    } else {
        None
    }
}

#[test]
fn r3_18bi_exact_bg_lane_composes_three_payloads_and_stops_before_bh_control() {
    let (mut excluded_au, mut excluded_be, mut composed) = (0usize, 0usize, 0usize);

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318bi_{index}"));
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
            assert!(expected_bi_payload(path).is_none(), "{path}");
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
                "BE false terminator reached payload production {path}"
            );
            continue;
        }

        composed += 1;
        let (tag, start, end, width, value) =
            expected_bi_payload(path).unwrap_or_else(|| panic!("unfrozen BI true witness {path}"));
        let got: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 =
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
            .unwrap_or_else(|error| panic!("BI row {index} {path}: {error}"));

        assert_eq!(got.header_composition, be, "{path}");
        assert_eq!(got.following_payload.attribute_tag, tag, "{path}");
        assert_eq!(got.following_payload.payload_start_bit, start, "{path}");
        assert_eq!(got.following_payload.payload_end_bit, end, "{path}");
        assert_eq!(got.following_payload.payload_width, width, "{path}");
        assert_eq!(got.following_payload.stop_bit, end, "{path}");
        assert_eq!(got.following_payload.value, value, "{path}");
        assert_eq!(got.stop_bit, end, "{path}");

        let direct = decode_replay_network_primitive_scalar_v1(&network, start, tag)
            .expect("direct R3.17C primitive scalar");
        assert_eq!(got.following_payload, direct, "{path}");

        let repeated = decode_bi(
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
        .expect("repeat R3.18BI");
        assert_eq!(repeated, got, "{path}");

        let mut poisoned = network.clone();
        let next_bit = usize::try_from(got.stop_bit).expect("BH poison bit fits usize");
        assert!(next_bit / 8 < poisoned.len(), "{path}");
        let old = raw_lsb(&poisoned, got.stop_bit);
        set_bit(&mut poisoned, next_bit, !old);
        let after_poison = decode_bi(
            &poisoned,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
        )
        .expect("BI must not inspect BH control bit");
        assert_eq!(after_poison, got, "{path}");
    }

    assert_eq!(excluded_au, 7, "upstream AU false terminator drift");
    assert_eq!(excluded_be, 37, "BE false terminator drift");
    assert_eq!(composed, 3, "BG payload authority drift");
    assert_eq!(excluded_au + excluded_be + composed, 47);
}

#[test]
fn r3_18bi_float_truncation_and_corrupt_authority_fail_closed() {
    let (path, first_start, actor_object, _) = au_cases()
        .iter()
        .copied()
        .find(|(path, _, _, _)| {
            path.ends_with(
                "test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay",
            )
        })
        .expect("079 BI witness");
    let (network, plan) = frozen_network_and_plan(path, "r318bi_negative");
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
    let base = decode_bi(
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
    .expect("BI baseline");
    assert_eq!(base.following_payload.payload_start_bit, 3166);
    assert_eq!(base.stop_bit, 3198);

    let cut = usize::try_from((base.stop_bit - 1) / 8).expect("truncation cut");
    assert!(cut * 8 >= usize::try_from(be.stop_bit).unwrap());
    assert!(
        decode_bi(
            &network[..cut],
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
        )
        .is_err()
    );

    let mut corrupt_be = be.clone();
    corrupt_be.stop_bit += 1;
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
            &corrupt_be,
        )
        .is_err()
    );

    let mut wrong_tag = be.clone();
    wrong_tag
        .following_header
        .as_mut()
        .expect("true header")
        .resolved_attribute_tag = Some(ReplayNetworkAttributeTagV1::Int);
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
            &wrong_tag,
        )
        .is_err()
    );

    let mut wrong_context = k3_context();
    wrong_context.version_minor -= 1;
    assert!(
        decode_bi(
            &network,
            &prior,
            &control,
            &plan,
            wrong_context,
            &an,
            &ay,
            &ba,
            &be,
        )
        .is_err()
    );
}

#[test]
fn r3_18bi_wrong_actor_lookup_boundary_and_fabricated_header_fail_closed() {
    let (path, first_start, actor_object, _) = au_cases()[1];
    assert!(path.ends_with("external_fixtures/sample_002.replay"));
    assert_eq!(actor_object, 106);
    let (network, plan) = frozen_network_and_plan(path, "r318bi_negative_direct");
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
    let baseline = decode_bi(
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
    .expect("BI baseline");
    assert_eq!(baseline.following_payload.payload_start_bit, 11230);
    assert_eq!(baseline.stop_bit, 11231);

    let mut wrong_actor = an.clone();
    wrong_actor
        .header_composition
        .following_header
        .actor_object_index = u32::MAX;
    assert!(
        decode_bi(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &wrong_actor,
            &ay,
            &ba,
            &be,
        )
        .is_err()
    );

    let mut unresolved = plan.clone();
    unresolved.object_lookups[actor_object as usize]
        .as_mut()
        .expect("actor lookup")
        .properties
        .retain(|property| property.stream_id != 61);
    assert!(
        decode_bi(
            &network,
            &prior,
            &control,
            &unresolved,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
        )
        .is_err()
    );

    let mut corrupt_ba = ba.clone();
    corrupt_ba.stop_bit += 1;
    assert!(
        decode_bi(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &corrupt_ba,
            &be,
        )
        .is_err()
    );

    let mut wrong_payload_start = be.clone();
    let header = wrong_payload_start
        .following_header
        .as_mut()
        .expect("true header");
    header.payload_start_bit = Some(header.payload_start_bit.expect("payload start") + 1);
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
            &wrong_payload_start,
        )
        .is_err()
    );

    let mut wrong_rl223 = k3_context();
    wrong_rl223.is_rl_223 = true;
    assert!(
        decode_bi(
            &network,
            &prior,
            &control,
            &plan,
            wrong_rl223,
            &an,
            &ay,
            &ba,
            &be,
        )
        .is_err()
    );

    let mut fabricated = be.clone();
    fabricated
        .following_header
        .as_mut()
        .expect("true header")
        .actor_object_index = u32::MAX;
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
            &fabricated,
        )
        .is_err()
    );
}

#[test]
fn r3_18bi_source_scope_is_one_be_recompute_one_primitive_payload_no_bh_control() {
    let source = include_str!("../src/lib.rs");
    let begin = source
        .find("// R3.18BI PRE-ADMISSION BEGIN bounded post-BE one-following-payload")
        .expect("BI begin");
    let end_marker = "// R3.18BI PRE-ADMISSION END bounded post-BE one-following-payload";
    let end = source[begin..]
        .find(end_marker)
        .map(|offset| begin + offset + end_marker.len())
        .expect("BI end");
    let block = &source[begin..end];

    assert_eq!(
        block.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(").count(),
        1
    );
    assert_eq!(
        block
            .matches("decode_replay_network_primitive_scalar_v1(")
            .count(),
        1
    );
    assert_eq!(block.matches("cursor.read_bit()").count(), 0);
    assert_eq!(block.matches("NetworkBitCursor").count(), 0);
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
