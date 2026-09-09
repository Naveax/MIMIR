from pathlib import Path

LIB = Path('crates/mimir-replay/src/lib.rs')
TEST = Path('crates/mimir-replay/tests/r3_18bo_post_bk_following_header.rs')

source = LIB.read_text(encoding='utf-8')
marker = '// R3.18BK PRE-ADMISSION END bounded post-BI following control\n'
if source.count(marker) != 1:
    raise SystemExit(f'expected exactly one BK end marker, found {source.count(marker)}')
if '// R3.18BO PRE-ADMISSION BEGIN bounded post-BK mixed-continuation following header' in source:
    raise SystemExit('R3.18BO block already exists')

block = r'''

// R3.18BO PRE-ADMISSION BEGIN bounded post-BK mixed-continuation following header
/// Bounded composition of one validated published R3.18BK mixed control plus at most one
/// R3.18BN-admitted following existing-actor property header.
///
/// False is a successful terminator with no post-BK read. True reuses the shared R3.16B
/// presence-after suffix decoder at the validated BK stop, requires exact eight-field R3.18BN
/// membership, and stops at payload_start without consuming payload or another control.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 {
    pub control: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    pub following_header: Option<ReplayNetworkExistingActorFirstPropertyHeaderV1>,
    pub context: ReplayNetworkK3DecodeContextV1,
    pub stop_bit: u64,
}

fn network_existing_actor_post_bk_following_header_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-BK following-header error: {category}: {}",
        detail.into()
    ))
}

fn r3_18bn_post_bk_following_header_context_admitted_v1(
    stream_id_bound: u32,
    prop_id_bits: u8,
    property_object_index: u32,
    attribute_tag: ReplayNetworkAttributeTagV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> bool {
    matches!(
        (
            stream_id_bound,
            prop_id_bits,
            property_object_index,
            attribute_tag,
            context.version_major,
            context.version_minor,
            context.net_version,
            context.is_rl_223,
        ),
        (
            72,
            6,
            95,
            ReplayNetworkAttributeTagV1::Boolean,
            868,
            32,
            10,
            false
        ) | (
            110,
            6,
            66,
            ReplayNetworkAttributeTagV1::ActiveActor,
            868,
            32,
            10,
            false
        )
    )
}

#[allow(clippy::too_many_arguments)]
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_following_header_v1(
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
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1> {
    let expected_bk = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_v1(
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
    )?;
    if &expected_bk != bk_prior {
        return Err(network_existing_actor_post_bk_following_header_error(
            "invalid-r3-18bk-prior",
            "supplied R3.18BK mixed-control result differs from recomputed published authority",
        ));
    }

    let expected_control_end = bk_prior
        .property_present_start_bit
        .checked_add(1)
        .ok_or_else(|| {
            network_existing_actor_post_bk_following_header_error(
                "invalid-control-boundary",
                "R3.18BK control end overflows u64",
            )
        })?;
    if bk_prior.property_present_start_bit != bi_prior.stop_bit
        || bk_prior.property_present_end_bit != expected_control_end
        || bk_prior.stop_bit != expected_control_end
    {
        return Err(network_existing_actor_post_bk_following_header_error(
            "invalid-control-boundary",
            format!(
                "BI stop={} BK start={} end={} stop={} expected_end={expected_control_end}",
                bi_prior.stop_bit,
                bk_prior.property_present_start_bit,
                bk_prior.property_present_end_bit,
                bk_prior.stop_bit,
            ),
        ));
    }

    if !bk_prior.property_present {
        return Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 {
            control: bk_prior.clone(),
            following_header: None,
            context,
            stop_bit: bk_prior.stop_bit,
        });
    }

    let actor_object_index = bi_prior
        .header_composition
        .following_header
        .as_ref()
        .ok_or_else(|| {
            network_existing_actor_post_bk_following_header_error(
                "missing-prior-header",
                "valid R3.18BI authority must retain the existing-actor header identity",
            )
        })?
        .actor_object_index;

    let following_header = decode_replay_network_existing_actor_property_header_suffix_v1(
        network_bytes,
        bk_prior.property_present_start_bit,
        bk_prior.property_present_end_bit,
        bk_prior.stop_bit,
        actor_object_index,
        lookup_plan,
    )?;

    if !following_header.property_present
        || following_header.property_present_start_bit != bk_prior.property_present_start_bit
        || following_header.property_present_end_bit != bk_prior.property_present_end_bit
        || following_header.stream_id_start_bit != Some(bk_prior.stop_bit)
        || following_header.actor_object_index != actor_object_index
    {
        return Err(network_existing_actor_post_bk_following_header_error(
            "header-boundary-mismatch",
            format!(
                "BK=[{},{}) stop={} header=[{},{}) stream_start={:?} actor={} expected_actor={actor_object_index}",
                bk_prior.property_present_start_bit,
                bk_prior.property_present_end_bit,
                bk_prior.stop_bit,
                following_header.property_present_start_bit,
                following_header.property_present_end_bit,
                following_header.stream_id_start_bit,
                following_header.actor_object_index,
            ),
        ));
    }

    let payload_start_bit = following_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_post_bk_following_header_error(
            "missing-payload-start",
            "present R3.18BN following header has no payload start",
        )
    })?;
    if following_header.stop_bit != payload_start_bit {
        return Err(network_existing_actor_post_bk_following_header_error(
            "payload-boundary-mismatch",
            format!(
                "following header stop {} differs from payload start {payload_start_bit}",
                following_header.stop_bit,
            ),
        ));
    }

    let (
        Some(stream_id_bound),
        Some(prop_id_bits),
        Some(property_object_index),
        Some(attribute_tag),
    ) = (
        following_header.stream_id_bound,
        following_header.prop_id_bits,
        following_header.resolved_property_object_index,
        following_header.resolved_attribute_tag,
    )
    else {
        return Err(network_existing_actor_post_bk_following_header_error(
            "incomplete-r3-18bn-header-context",
            "following header is missing one or more exact R3.18BN structural fields",
        ));
    };

    if !r3_18bn_post_bk_following_header_context_admitted_v1(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context,
    ) {
        return Err(network_existing_actor_post_bk_following_header_error(
            "unadmitted-r3-18bn-header-context",
            format!(
                "R3.18BN exact tuple rejected bound={stream_id_bound} bits={prop_id_bits} object={property_object_index} tag={attribute_tag:?} version={}.{} net{} rl223={}",
                context.version_major,
                context.version_minor,
                context.net_version,
                context.is_rl_223,
            ),
        ));
    }

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 {
        control: bk_prior.clone(),
        following_header: Some(following_header),
        context,
        stop_bit: payload_start_bit,
    })
}

#[cfg(test)]
mod r3_18bo_exact_contract_tests {
    use super::*;

    fn context(
        major: i32,
        minor: i32,
        net: i32,
        is_rl_223: bool,
    ) -> ReplayNetworkK3DecodeContextV1 {
        ReplayNetworkK3DecodeContextV1 {
            version_major: major,
            version_minor: minor,
            net_version: net,
            is_rl_223,
        }
    }

    #[test]
    fn r3_18bo_exact_two_r3_18bn_contexts_are_admitted() {
        let ctx = context(868, 32, 10, false);
        assert!(r3_18bn_post_bk_following_header_context_admitted_v1(
            72,
            6,
            95,
            ReplayNetworkAttributeTagV1::Boolean,
            ctx,
        ));
        assert!(r3_18bn_post_bk_following_header_context_admitted_v1(
            110,
            6,
            66,
            ReplayNetworkAttributeTagV1::ActiveActor,
            ctx,
        ));
    }

    #[test]
    fn r3_18bo_exact_membership_rejects_widening_cross_boundary_and_fabrication() {
        let ctx = context(868, 32, 10, false);
        let rejected = [
            (72, 6, 66, ReplayNetworkAttributeTagV1::ActiveActor, ctx),
            (72, 6, 92, ReplayNetworkAttributeTagV1::Boolean, ctx),
            (72, 6, 999, ReplayNetworkAttributeTagV1::Boolean, ctx),
            (72, 6, 95, ReplayNetworkAttributeTagV1::ActiveActor, ctx),
            (110, 6, 66, ReplayNetworkAttributeTagV1::Boolean, ctx),
            (72, 6, 95, ReplayNetworkAttributeTagV1::Boolean, context(867, 32, 10, false)),
            (72, 6, 95, ReplayNetworkAttributeTagV1::Boolean, context(868, 31, 10, false)),
            (72, 6, 95, ReplayNetworkAttributeTagV1::Boolean, context(868, 32, 9, false)),
            (72, 6, 95, ReplayNetworkAttributeTagV1::Boolean, context(868, 32, 10, true)),
        ];
        for (bound, bits, object, tag, rejected_context) in rejected {
            assert!(!r3_18bn_post_bk_following_header_context_admitted_v1(
                bound,
                bits,
                object,
                tag,
                rejected_context,
            ));
        }
    }
}
// R3.18BO PRE-ADMISSION END bounded post-BK mixed-continuation following header
'''

source = source.replace(marker, marker + block, 1)
LIB.write_text(source, encoding='utf-8')

test = r'''include!("r3_18bk_post_bi_following_control.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_following_header_v1 as decode_bo,
};

fn expected_bo_header(
    path: &str,
) -> Option<(u64, u32, u32, u8, u32, ReplayNetworkAttributeTagV1, u64)> {
    if path.ends_with("external_fixtures/sample_002.replay") {
        Some((
            11232,
            62,
            72,
            6,
            95,
            ReplayNetworkAttributeTagV1::Boolean,
            11238,
        ))
    } else if path
        .ends_with("test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay")
    {
        Some((
            3199,
            60,
            110,
            6,
            66,
            ReplayNetworkAttributeTagV1::ActiveActor,
            3205,
        ))
    } else {
        None
    }
}

#[test]
fn r3_18bo_exact_three_bk_rows_preserve_one_terminator_and_compose_two_exact_headers() {
    let (mut excluded_au, mut excluded_be, mut bk_rows, mut false_count, mut true_count) =
        (0usize, 0usize, 0usize, 0usize, 0usize);

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318bo_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        ).unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        ).unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));

        if au.following_header.is_none() {
            excluded_au += 1;
            assert!(expected_bh_control(path).is_none(), "unexpected BK authority {path}");
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
            assert!(expected_bh_control(path).is_none(), "unexpected BK authority {path}");
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
        bk_rows += 1;

        let got: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 = decode_bo(
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
        ).unwrap_or_else(|error| panic!("BO row {index} {path}: {error}"));

        assert_eq!(got.control, bk, "{path}");
        assert_eq!(got.context, k3_context(), "{path}");

        if !bk.property_present {
            false_count += 1;
            assert!(path.ends_with("external_fixtures/sample_003.replay"));
            assert!(expected_bo_header(path).is_none(), "{path}");
            assert!(got.following_header.is_none(), "{path}");
            assert_eq!(got.stop_bit, bk.stop_bit, "{path}");

            let mut poisoned = network.clone();
            let poison_bit = usize::try_from(bk.stop_bit).expect("false post-BK poison fits usize");
            assert!(poison_bit / 8 < poisoned.len(), "{path}");
            let old = raw_lsb(&poisoned, bk.stop_bit);
            set_bit(&mut poisoned, poison_bit, !old);
            let after_poison = decode_bo(
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
                &bk,
            ).expect("false BO path must not inspect post-BK bits");
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
        ) = expected_bo_header(path).unwrap_or_else(|| panic!("unfrozen BO true witness {path}"));
        let header = got.following_header.as_ref().expect("true BK must expose one header");
        assert!(header.property_present, "{path}");
        assert_eq!(header.property_present_start_bit, bk.property_present_start_bit, "{path}");
        assert_eq!(header.property_present_end_bit, bk.property_present_end_bit, "{path}");
        assert_eq!(header.stream_id_start_bit, Some(expected_stream_start), "{path}");
        assert_eq!(expected_stream_start, bk.stop_bit, "{path}");
        assert_eq!(header.stream_id, Some(expected_stream_id), "{path}");
        assert_eq!(header.stream_id_bound, Some(expected_bound), "{path}");
        assert_eq!(header.prop_id_bits, Some(expected_bits), "{path}");
        assert_eq!(header.resolved_property_object_index, Some(expected_object), "{path}");
        assert_eq!(header.resolved_attribute_tag, Some(expected_tag), "{path}");
        assert_eq!(header.payload_start_bit, Some(expected_payload_start), "{path}");
        assert_eq!(header.stop_bit, expected_payload_start, "{path}");
        assert_eq!(got.stop_bit, expected_payload_start, "{path}");

        let repeated = decode_bo(
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
        ).expect("repeat R3.18BO");
        assert_eq!(repeated, got, "{path}");

        let mut payload_poisoned = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("payload poison fits usize");
        assert!(poison_bit / 8 < payload_poisoned.len(), "{path}");
        let old = raw_lsb(&payload_poisoned, got.stop_bit);
        set_bit(&mut payload_poisoned, poison_bit, !old);
        let after_payload_poison = decode_bo(
            &payload_poisoned,
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
        ).expect("post-payload_start poison must not affect BO");
        assert_eq!(after_payload_poison, got, "{path}");

        if path.ends_with("external_fixtures/sample_002.replay") {
            assert_eq!(bk.stop_bit % 8, 0, "sample_002 BO stream start alignment drift");
            let carrier_cut = usize::try_from(bk.stop_bit / 8).expect("carrier cut fits usize");
            assert!(decode_bo(
                &network[..carrier_cut],
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
            ).is_err(), "truncation before true BO header must fail");

            let mut corrupt_bk = bk.clone();
            corrupt_bk.stop_bit += 1;
            assert!(decode_bo(
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
                &corrupt_bk,
            ).is_err(), "corrupt BK authority must fail");

            let mut corrupt_bi = bi.clone();
            corrupt_bi
                .header_composition
                .following_header
                .as_mut()
                .expect("sample_002 BI header")
                .actor_object_index += 1;
            assert!(decode_bo(
                &network,
                &prior,
                &control,
                &plan,
                k3_context(),
                &an,
                &ay,
                &ba,
                &be,
                &corrupt_bi,
                &bk,
            ).is_err(), "wrong actor authority must fail");

            let mut missing_lookup = plan.clone();
            let actor_slot = usize::try_from(
                bi.header_composition
                    .following_header
                    .as_ref()
                    .expect("sample_002 BI header")
                    .actor_object_index,
            ).expect("actor object fits usize");
            missing_lookup.object_lookups[actor_slot] = None;
            assert!(decode_bo(
                &network,
                &prior,
                &control,
                &missing_lookup,
                k3_context(),
                &an,
                &ay,
                &ba,
                &be,
                &bi,
                &bk,
            ).is_err(), "missing actor lookup must fail");

            let wrong_context = ReplayNetworkK3DecodeContextV1 {
                version_major: 868,
                version_minor: 32,
                net_version: 10,
                is_rl_223: true,
            };
            assert!(decode_bo(
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
            ).is_err(), "RL223 false-to-true must fail");
        }
    }

    assert_eq!(excluded_au, 7, "upstream AU false-terminator drift");
    assert_eq!(excluded_be, 37, "BE false-terminator drift");
    assert_eq!(bk_rows, 3, "BK authority row drift");
    assert_eq!(false_count, 1, "BO false terminator drift");
    assert_eq!(true_count, 2, "BO true header drift");
    assert_eq!(excluded_au + excluded_be + false_count + true_count, 47);
}

#[test]
fn r3_18bo_source_scope_is_one_bk_recompute_one_header_suffix_no_payload_or_loop() {
    let source = include_str!("../src/lib.rs");
    let begin_marker = "// R3.18BO PRE-ADMISSION BEGIN bounded post-BK mixed-continuation following header";
    let end_marker = "// R3.18BO PRE-ADMISSION END bounded post-BK mixed-continuation following header";
    let begin = source.find(begin_marker).expect("BO begin marker");
    let relative_end = source[begin..].find(end_marker).expect("BO end marker");
    let block = &source[begin..begin + relative_end + end_marker.len()];

    assert_eq!(
        block
            .matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_v1(")
            .count(),
        1,
        "BO must recompute BK exactly once",
    );
    assert_eq!(
        block
            .matches("decode_replay_network_existing_actor_property_header_suffix_v1(")
            .count(),
        1,
        "BO must call the stateless header suffix exactly once",
    );
    assert_eq!(block.matches("decode_replay_network_primitive_scalar_v1(").count(), 0);
    assert_eq!(block.matches(".read_bit(").count(), 0, "BO must not re-read BK or later control bits");
    assert!(!block.contains("while "), "BO must not contain a while loop");
    assert!(!block.contains("loop {"), "BO must not contain a generic loop");
}
'''

TEST.write_text(test, encoding='utf-8')
print('R3_18BO_GENERATOR=PASS')
