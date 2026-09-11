from pathlib import Path

LIB = Path('crates/mimir-replay/src/lib.rs')
TEST = Path('crates/mimir-replay/tests/r3_18bs_post_bo_payload.rs')

source = LIB.read_text(encoding='utf-8')
marker = '// R3.18BO PRE-ADMISSION END bounded post-BK mixed-continuation following header\n'
begin_marker = '// R3.18BS PRE-ADMISSION BEGIN bounded post-BO one-following-payload'
if source.count(marker) != 1:
    raise SystemExit(f'expected exactly one BO end marker, found {source.count(marker)}')
if begin_marker in source:
    raise SystemExit('R3.18BS block already exists')
if TEST.exists():
    raise SystemExit(f'{TEST} already exists')

block = r'''

// R3.18BS PRE-ADMISSION BEGIN bounded post-BO one-following-payload
/// Exactly one R3.18BQ-admitted payload after the bounded R3.18BO following header.
///
/// This enum is deliberately closed to the two payload forms proven on the immutable
/// R3.18BQ lane. It is not a generic property-payload carrier.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1 {
    Boolean(ReplayNetworkPrimitiveScalarDecodeV1),
    ActiveActor(ReplayNetworkK2DecodeV1),
}

/// Bounded composition of one validated R3.18BO true following header plus exactly one
/// R3.18BQ-admitted payload. The result stops at payload end and does not consume the
/// R3.18BR following property-control bit.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
    pub header_composition: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    pub following_payload: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1,
    pub stop_bit: u64,
}

fn network_existing_actor_post_bo_following_payload_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-BO following-payload error: {category}: {}",
        detail.into()
    ))
}

#[allow(clippy::too_many_arguments)]
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
    an_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ay_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ba_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    be_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    bi_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    bk_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    bo_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1> {
    let expected_bo = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_following_header_v1(
        network_bytes,
        prior,
        control,
        lookup_plan,
        context,
        an_prior,
        ay_prior,
        ba_prior,
        be_prior,
        bi_prior,
        bk_prior,
    )?;
    if &expected_bo != bo_prior {
        return Err(network_existing_actor_post_bo_following_payload_error(
            "invalid-r3-18bo-prior",
            "supplied R3.18BO following-header result differs from recomputed published authority",
        ));
    }

    let header = bo_prior.following_header.as_ref().ok_or_else(|| {
        network_existing_actor_post_bo_following_payload_error(
            "false-terminator-has-no-payload",
            "R3.18BO false terminator is outside the R3.18BQ payload lane",
        )
    })?;
    if !header.property_present || bo_prior.context != context {
        return Err(network_existing_actor_post_bo_following_payload_error(
            "invalid-r3-18bo-header",
            "R3.18BO payload composition requires one present header in the exact supplied context",
        ));
    }

    let payload_start_bit = header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_post_bo_following_payload_error(
            "missing-payload-start",
            "present R3.18BO following header has no payload start",
        )
    })?;
    if header.stop_bit != payload_start_bit || bo_prior.stop_bit != payload_start_bit {
        return Err(network_existing_actor_post_bo_following_payload_error(
            "payload-start-boundary-mismatch",
            format!(
                "header stop={} BO stop={} payload_start={payload_start_bit}",
                header.stop_bit, bo_prior.stop_bit,
            ),
        ));
    }

    let attribute_tag = header.resolved_attribute_tag.ok_or_else(|| {
        network_existing_actor_post_bo_following_payload_error(
            "missing-attribute-tag",
            "R3.18BO following header did not retain its exact R3.18BN attribute tag",
        )
    })?;

    let k2_context = ReplayNetworkK2DecodeContextV1 {
        net_version: context.net_version,
        is_rl_223: context.is_rl_223,
    };

    let (following_payload, stop_bit) = match attribute_tag {
        ReplayNetworkAttributeTagV1::Boolean => {
            let decoded = decode_replay_network_primitive_scalar_v1(
                network_bytes,
                payload_start_bit,
                ReplayNetworkAttributeTagV1::Boolean,
            )?;
            let expected_end = payload_start_bit.checked_add(1).ok_or_else(|| {
                network_existing_actor_post_bo_following_payload_error(
                    "boolean-payload-end-overflow",
                    "Boolean payload end overflows u64",
                )
            })?;
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::Boolean
                || decoded.payload_start_bit != payload_start_bit
                || decoded.payload_width != 1
                || decoded.payload_end_bit != expected_end
                || decoded.stop_bit != expected_end
                || !matches!(
                    &decoded.value,
                    ReplayNetworkPrimitiveScalarValueV1::Boolean(_)
                )
            {
                return Err(network_existing_actor_post_bo_following_payload_error(
                    "boolean-payload-boundary-mismatch",
                    format!(
                        "start={} end={} width={} stop={} expected=[{payload_start_bit},{expected_end})",
                        decoded.payload_start_bit,
                        decoded.payload_end_bit,
                        decoded.payload_width,
                        decoded.stop_bit,
                    ),
                ));
            }
            (
                ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::Boolean(decoded),
                expected_end,
            )
        }
        ReplayNetworkAttributeTagV1::ActiveActor => {
            let decoded = decode_replay_network_k2_v1(
                network_bytes,
                payload_start_bit,
                ReplayNetworkAttributeTagV1::ActiveActor,
                k2_context,
            )?;
            let expected_end = payload_start_bit.checked_add(33).ok_or_else(|| {
                network_existing_actor_post_bo_following_payload_error(
                    "active-actor-payload-end-overflow",
                    "ActiveActor payload end overflows u64",
                )
            })?;
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::ActiveActor
                || decoded.payload_start_bit != payload_start_bit
                || decoded.payload_width != 33
                || decoded.payload_end_bit != expected_end
                || !matches!(&decoded.value, ReplayNetworkK2ValueV1::ActiveActor { .. })
            {
                return Err(network_existing_actor_post_bo_following_payload_error(
                    "active-actor-payload-boundary-mismatch",
                    format!(
                        "start={} end={} width={} expected=[{payload_start_bit},{expected_end})",
                        decoded.payload_start_bit, decoded.payload_end_bit, decoded.payload_width,
                    ),
                ));
            }
            (
                ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::ActiveActor(decoded),
                expected_end,
            )
        }
        other => {
            return Err(network_existing_actor_post_bo_following_payload_error(
                "unadmitted-r3-18bq-payload-tag",
                format!("R3.18BQ admits only Boolean or ActiveActor, got {other:?}"),
            ));
        }
    };

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
        header_composition: bo_prior.clone(),
        following_payload,
        stop_bit,
    })
}
// R3.18BS PRE-ADMISSION END bounded post-BO one-following-payload
'''

source = source.replace(marker, marker + block, 1)
LIB.write_text(source, encoding='utf-8')

test = r'''include!("r3_18bo_post_bk_following_header.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 as R3_18BsResultV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1 as R3_18BsPayloadValueV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1 as decode_bs,
};

fn expected_bs_payload(
    path: &str,
) -> Option<(ReplayNetworkAttributeTagV1, u64, u64)> {
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
            assert!(path.ends_with("external_fixtures/sample_003.replay"), "{path}");
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
                error.to_string().contains("false-terminator-has-no-payload"),
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
                assert_eq!(decoded.attribute_tag, ReplayNetworkAttributeTagV1::Boolean, "{path}");
                assert_eq!(decoded.payload_start_bit, expected_start, "{path}");
                assert_eq!(decoded.payload_width, 1, "{path}");
                assert_eq!(decoded.payload_end_bit, expected_end, "{path}");
                assert_eq!(decoded.stop_bit, expected_end, "{path}");
                assert_eq!(decoded.value, ReplayNetworkPrimitiveScalarValueV1::Boolean(true), "{path}");
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
                assert_eq!(decoded.attribute_tag, ReplayNetworkAttributeTagV1::ActiveActor, "{path}");
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
            (payload, tag) => panic!("unexpected BS payload/tag pair {payload:?}/{tag:?} for {path}"),
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
            let cut = usize::try_from((expected_start + 7) / 8 + 1)
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
    assert_eq!(excluded_au + excluded_be + false_terminators + boolean_rows + active_actor_rows, 47);
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
        block.matches("decode_replay_network_primitive_scalar_v1(").count(),
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
    assert!(!block.contains("while "), "BS must not contain a while loop");
    assert!(!block.contains("loop {"), "BS must not contain a generic loop");
}
'''

TEST.write_text(test, encoding='utf-8')
print('R3.18BS patch staged: lib.rs + focused integration test')
