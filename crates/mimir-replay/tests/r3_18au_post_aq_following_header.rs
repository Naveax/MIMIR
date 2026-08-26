include!("r3_18aq_post_an_payload_control.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1,
};
use std::collections::BTreeMap;

fn au_cases() -> [(&'static str, u64, u32, u64); 47] {
    [
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
    ]
}

#[test]
fn r3_18au_exact_47_row_lane_preserves_seven_terminators_and_composes_forty_headers() {
    let mut false_count = 0usize;
    let mut true_count = 0usize;
    let mut counts: BTreeMap<(u32, u8, u32), usize> = BTreeMap::new();
    let mut false_isolation_checked = false;
    let mut true_negative_checked = false;
    let mut true_truncation_checked = false;

    for (index, (path, first_start, actor_object, control_start)) in
        au_cases().into_iter().enumerate()
    {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318au_frozen_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        assert_eq!(an.stop_bit, control_start, "{path}");
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
  &network,
  &prior,
  &control,
  &plan,
  k3_context(),
  &an,
        )
        .unwrap_or_else(|error| panic!("AQ frozen prerequisite row {index} {path}: {error}"));

        let got: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
  &network,
  &prior,
  &control,
  &plan,
  k3_context(),
  &an,
  &aq,
        )
        .unwrap_or_else(|error| panic!("AU frozen row {index} {path}: {error}"));

        assert_eq!(got.control, aq, "{path}");
        assert_eq!(got.context, k3_context(), "{path}");
        let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
  &network,
  &prior,
  &control,
  &plan,
  k3_context(),
  &an,
  &aq,
        )
        .expect("repeat frozen R3.18AU");
        assert_eq!(repeated, got, "{path}");

        if !aq.following_property_present {
            false_count += 1;
            assert_eq!(got.following_header, None, "{path}");
            assert_eq!(got.stop_bit, aq.stop_bit, "{path}");

            if !false_isolation_checked {
                let mut poisoned = network.clone();
                let start = usize::try_from(aq.stop_bit).expect("AQ stop fits usize");
                let total = poisoned.len() * 8;
                for bit in start..usize::min(start + 32, total) {
                    let old = ((poisoned[bit / 8] >> (bit % 8)) & 1) != 0;
                    set_bit(&mut poisoned, bit, !old);
                }
                let after_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
          &poisoned,
          &prior,
          &control,
          &plan,
          k3_context(),
          &an,
          &aq,
      )
      .expect("false terminator must ignore all post-AQ bits");
                assert_eq!(after_poison, got);
                false_isolation_checked = true;
            }
            continue;
        }

        true_count += 1;
        let header = got
            .following_header
            .as_ref()
            .expect("true AQ row must expose exactly one header");
        assert!(header.property_present, "{path}");
        assert_eq!(
            header.property_present_start_bit, aq.property_present_start_bit,
            "{path}"
        );
        assert_eq!(
            header.property_present_end_bit, aq.property_present_end_bit,
            "{path}"
        );
        assert_eq!(
            header.actor_object_index, an.header_composition.following_header.actor_object_index,
            "{path}"
        );
        assert_eq!(
            header.resolved_attribute_tag,
            Some(ReplayNetworkAttributeTagV1::Int),
            "{path}"
        );
        assert_eq!(header.payload_start_bit, Some(got.stop_bit), "{path}");
        assert_eq!(header.stop_bit, got.stop_bit, "{path}");

        let key = (
            header.stream_id_bound.expect("AT bound"),
            header.prop_id_bits.expect("AT prop bits"),
            header.resolved_property_object_index.expect("AT object"),
        );
        *counts.entry(key).or_insert(0) += 1;

        let mut poisoned = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("payload start fits usize");
        if poison_bit < poisoned.len() * 8 {
            let old = ((poisoned[poison_bit / 8] >> (poison_bit % 8)) & 1) != 0;
            set_bit(&mut poisoned, poison_bit, !old);
            let after_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
      &poisoned,
      &prior,
      &control,
      &plan,
      k3_context(),
      &an,
      &aq,
  )
  .expect("payload poison must not affect AU header result");
            assert_eq!(after_poison, got, "{path}");
        }

        if !true_truncation_checked {
            let bytes_needed_for_aq = usize::try_from(aq.stop_bit.div_ceil(8)).unwrap();
            if bytes_needed_for_aq * 8 < usize::try_from(got.stop_bit).unwrap() {
                let truncated = &network[..bytes_needed_for_aq];
                assert!(
          decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
              truncated,
              &prior,
              &control,
              &plan,
              k3_context(),
              &an,
              &aq,
          )
          .is_err(),
          "truncation inside true following header must reject: {path}",
      );
                true_truncation_checked = true;
            }
        }

        if !true_negative_checked {
            let mut wrong_an = an.clone();
            wrong_an
                .header_composition
                .following_header
                .actor_object_index = u32::MAX;
            assert!(
      decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
          &network,
          &prior,
          &control,
          &plan,
          k3_context(),
          &wrong_an,
          &aq,
      )
      .is_err(),
      "wrong actor authority must reject",
  );

            let mut wrong_version = k3_context();
            wrong_version.version_minor -= 1;
            assert!(
      decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
          &network,
          &prior,
          &control,
          &plan,
          wrong_version,
          &an,
          &aq,
      )
      .is_err(),
      "wrong exact replay version must reject",
  );

            let mut wrong_rl223 = k3_context();
            wrong_rl223.is_rl_223 = true;
            assert!(
      decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
          &network,
          &prior,
          &control,
          &plan,
          wrong_rl223,
          &an,
          &aq,
      )
      .is_err(),
      "RL223 false-to-true widening must reject",
  );

            let mut unresolved_plan = plan.clone();
            let actor_index = usize::try_from(header.actor_object_index).unwrap();
            let stream_id = header.stream_id.expect("true header stream id");
            if let Some(lookup) = unresolved_plan
                .object_lookups
                .get_mut(actor_index)
                .and_then(Option::as_mut)
            {
                lookup
                    .properties
                    .retain(|property| property.stream_id != stream_id);
                assert!(
          decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
              &network,
              &prior,
              &control,
              &unresolved_plan,
              k3_context(),
              &an,
              &aq,
          )
          .is_err(),
          "unresolved following stream/property lookup must reject",
      );
            }
            true_negative_checked = true;
        }
    }

    let expected: BTreeMap<(u32, u8, u32), usize> = [
        ((110, 6, 49), 1),
        ((60, 5, 106), 4),
        ((60, 5, 107), 19),
        ((60, 5, 113), 1),
        ((60, 5, 115), 2),
        ((60, 5, 117), 1),
        ((60, 5, 122), 1),
        ((60, 5, 130), 2),
        ((60, 5, 131), 1),
        ((60, 5, 134), 1),
        ((60, 5, 144), 1),
        ((60, 5, 60), 1),
        ((60, 5, 69), 2),
        ((67, 6, 81), 1),
        ((72, 6, 84), 1),
        ((72, 6, 87), 1),
    ]
    .into_iter()
    .collect();

    assert_eq!(false_count, 7);
    assert_eq!(true_count, 40);
    assert_eq!(counts, expected);
    assert!(false_isolation_checked);
    assert!(true_negative_checked);
    assert!(true_truncation_checked);
}

#[test]
fn r3_18au_source_scope_is_one_header_call_and_zero_payload_or_loop_work() {
    let source = include_str!("../src/lib.rs");
    let begin =
        "// R3.18AU PRE-ADMISSION BEGIN bounded post-AQ mixed-continuation following header";
    let end = "// R3.18AU PRE-ADMISSION END bounded post-AQ mixed-continuation following header";
    let block = source
        .split_once(begin)
        .expect("AU begin marker")
        .1
        .split_once(end)
        .expect("AU end marker")
        .0;

    assert_eq!(
        block
            .matches("decode_replay_network_existing_actor_first_property_header_v1(")
            .count(),
        1,
    );
    for forbidden in [
        "decode_replay_network_primitive_scalar_v1(",
        "decode_replay_network_k2_v1(",
        "NetworkBitCursor",
        "loop {",
        "while ",
    ] {
        assert_eq!(
            block.matches(forbidden).count(),
            0,
            "forbidden AU source token: {forbidden}"
        );
    }
}
