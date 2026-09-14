from pathlib import Path

LIB = Path('crates/mimir-replay/src/lib.rs')
TEST = Path('crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs')

begin = '// R3.18BY PRE-ADMISSION BEGIN bounded post-BU mixed-continuation following header'
end = '// R3.18BY PRE-ADMISSION END bounded post-BU mixed-continuation following header'

source = LIB.read_text(encoding='utf-8')
if begin in source or end in source:
    raise SystemExit('R3.18BY source block already present')

block = r'''

// R3.18BY PRE-ADMISSION BEGIN bounded post-BU mixed-continuation following header
/// Bounded composition of one validated published R3.18BU mixed control plus at most one
/// R3.18BX-admitted following existing-actor property header.
///
/// False is a successful terminator with no post-BU read. True reuses the shared R3.16B
/// presence-after suffix decoder at the validated BU stop, requires exact eight-field R3.18BX
/// membership, and stops at payload_start without consuming payload or another control.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkPostBuFollowingHeaderDecodeV1 {
    pub control_composition: ReplayNetworkPostBsFollowingControlDecodeV1,
    pub following_header: Option<ReplayNetworkExistingActorFirstPropertyHeaderV1>,
    pub context: ReplayNetworkK3DecodeContextV1,
    pub stop_bit: u64,
}

fn network_existing_actor_post_bu_following_header_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-BU following-header error: {category}: {}",
        detail.into()
    ))
}

fn r3_18bx_post_bu_following_header_context_admitted_v1(
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
            110,
            6,
            67,
            ReplayNetworkAttributeTagV1::LoadoutsOnline,
            868,
            32,
            10,
            false
        )
    )
}

#[allow(clippy::too_many_arguments)]
pub fn decode_replay_network_post_bu_following_header_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    authority_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
    an_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ay_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ba_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    be_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    bi_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    bk_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    bo_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    bs_prior: &ReplayNetworkPostBoFollowingPayloadDecodeV1,
    bu_prior: &ReplayNetworkPostBsFollowingControlDecodeV1,
) -> Result<ReplayNetworkPostBuFollowingHeaderDecodeV1> {
    let expected_bu = decode_replay_network_post_bs_following_control_v1(
        network_bytes,
        prior,
        control,
        authority_plan,
        context,
        an_prior,
        ay_prior,
        ba_prior,
        be_prior,
        bi_prior,
        bk_prior,
        bo_prior,
        bs_prior,
    )?;
    if &expected_bu != bu_prior {
        return Err(network_existing_actor_post_bu_following_header_error(
            "invalid-r3-18bu-prior",
            "supplied R3.18BU mixed-control result differs from recomputed published authority",
        ));
    }

    let expected_control_end = expected_bu
        .control_start_bit
        .checked_add(1)
        .ok_or_else(|| {
            network_existing_actor_post_bu_following_header_error(
                "invalid-control-boundary",
                "R3.18BU control end overflows u64",
            )
        })?;
    if expected_bu.control_start_bit != bs_prior.stop_bit
        || expected_bu.control_end_bit != expected_control_end
        || expected_bu.stop_bit != expected_control_end
    {
        return Err(network_existing_actor_post_bu_following_header_error(
            "invalid-control-boundary",
            format!(
                "BS stop={} BU start={} end={} stop={} expected_end={expected_control_end}",
                bs_prior.stop_bit,
                expected_bu.control_start_bit,
                expected_bu.control_end_bit,
                expected_bu.stop_bit,
            ),
        ));
    }

    if !expected_bu.property_control {
        let stop_bit = expected_bu.stop_bit;
        return Ok(ReplayNetworkPostBuFollowingHeaderDecodeV1 {
            control_composition: expected_bu,
            following_header: None,
            context,
            stop_bit,
        });
    }

    let actor_object_index = expected_bu
        .payload_composition
        .header_composition
        .following_header
        .as_ref()
        .ok_or_else(|| {
            network_existing_actor_post_bu_following_header_error(
                "missing-prior-header",
                "valid R3.18BS authority must retain the existing-actor header identity",
            )
        })?
        .actor_object_index;

    let decode_header_suffix = decode_replay_network_existing_actor_property_header_suffix_v1;
    let following_header = decode_header_suffix(
        network_bytes,
        expected_bu.control_start_bit,
        expected_bu.control_end_bit,
        expected_bu.stop_bit,
        actor_object_index,
        authority_plan,
    )?;

    if !following_header.property_present
        || following_header.property_present_start_bit != expected_bu.control_start_bit
        || following_header.property_present_end_bit != expected_bu.control_end_bit
        || following_header.stream_id_start_bit != Some(expected_bu.stop_bit)
        || following_header.actor_object_index != actor_object_index
    {
        return Err(network_existing_actor_post_bu_following_header_error(
            "header-boundary-mismatch",
            format!(
                "BU=[{},{}) stop={} header=[{},{}) stream_start={:?} actor={} expected_actor={actor_object_index}",
                expected_bu.control_start_bit,
                expected_bu.control_end_bit,
                expected_bu.stop_bit,
                following_header.property_present_start_bit,
                following_header.property_present_end_bit,
                following_header.stream_id_start_bit,
                following_header.actor_object_index,
            ),
        ));
    }

    let payload_start_bit = following_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_post_bu_following_header_error(
            "missing-payload-start",
            "present R3.18BX following header has no payload start",
        )
    })?;
    if following_header.stop_bit != payload_start_bit {
        return Err(network_existing_actor_post_bu_following_header_error(
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
        return Err(network_existing_actor_post_bu_following_header_error(
            "incomplete-r3-18bx-header-context",
            "following header is missing one or more exact R3.18BX structural fields",
        ));
    };

    if !r3_18bx_post_bu_following_header_context_admitted_v1(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context,
    ) {
        return Err(network_existing_actor_post_bu_following_header_error(
            "unadmitted-r3-18bx-header-context",
            format!(
                "R3.18BX exact tuple rejected bound={stream_id_bound} bits={prop_id_bits} object={property_object_index} tag={attribute_tag:?} version={}.{} net{} rl223={}",
                context.version_major,
                context.version_minor,
                context.net_version,
                context.is_rl_223,
            ),
        ));
    }

    Ok(ReplayNetworkPostBuFollowingHeaderDecodeV1 {
        control_composition: expected_bu,
        following_header: Some(following_header),
        context,
        stop_bit: payload_start_bit,
    })
}

#[cfg(test)]
mod r3_18by_exact_contract_tests {
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
    fn r3_18by_only_exact_r3_18bx_context_is_admitted() {
        let ctx = context(868, 32, 10, false);
        assert!(r3_18bx_post_bu_following_header_context_admitted_v1(
            110,
            6,
            67,
            ReplayNetworkAttributeTagV1::LoadoutsOnline,
            ctx,
        ));

        let rejected = [
            (110, 6, 66, ReplayNetworkAttributeTagV1::ActiveActor, ctx),
            (110, 6, 67, ReplayNetworkAttributeTagV1::ActiveActor, ctx),
            (72, 6, 67, ReplayNetworkAttributeTagV1::LoadoutsOnline, ctx),
            (110, 5, 67, ReplayNetworkAttributeTagV1::LoadoutsOnline, ctx),
            (110, 6, 68, ReplayNetworkAttributeTagV1::LoadoutsOnline, ctx),
            (
                110,
                6,
                67,
                ReplayNetworkAttributeTagV1::LoadoutsOnline,
                context(867, 32, 10, false),
            ),
            (
                110,
                6,
                67,
                ReplayNetworkAttributeTagV1::LoadoutsOnline,
                context(868, 31, 10, false),
            ),
            (
                110,
                6,
                67,
                ReplayNetworkAttributeTagV1::LoadoutsOnline,
                context(868, 32, 9, false),
            ),
            (
                110,
                6,
                67,
                ReplayNetworkAttributeTagV1::LoadoutsOnline,
                context(868, 32, 10, true),
            ),
        ];
        for (bound, bits, object, tag, rejected_context) in rejected {
            assert!(!r3_18bx_post_bu_following_header_context_admitted_v1(
                bound,
                bits,
                object,
                tag,
                rejected_context,
            ));
        }
    }
}
// R3.18BY PRE-ADMISSION END bounded post-BU mixed-continuation following header
'''

LIB.write_text(source.rstrip() + block + '\n', encoding='utf-8')

test = r'''include!("r3_18bu_post_bs_following_control.rs");

#[test]
fn r3_18by_exact_two_row_lane_terminates_false_and_decodes_one_true_header() {
    let (mut false_rows, mut true_rows, mut valid_rows) = (0usize, 0usize, 0usize);

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        if expected_bu_control(path).is_none() {
            continue;
        }

        let (network, plan) = frozen_network_and_plan(path, &format!("r318by_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        ).unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        ).unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));
        let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au)
            .unwrap_or_else(|error| panic!("AY prerequisite row {index} {path}: {error}"));
        let ba = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay)
            .unwrap_or_else(|error| panic!("BA prerequisite row {index} {path}: {error}"));
        let be = decode_be(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba,
        )
        .unwrap_or_else(|error| panic!("BE prerequisite row {index} {path}: {error}"));
        let bi = decode_bi(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be,
        )
        .unwrap_or_else(|error| panic!("BI prerequisite row {index} {path}: {error}"));
        let bk = decode_bk(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi,
        )
        .unwrap_or_else(|error| panic!("BK prerequisite row {index} {path}: {error}"));
        let bo = decode_bo(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk,
        )
        .unwrap_or_else(|error| panic!("BO prerequisite row {index} {path}: {error}"));
        let bs = decode_bs(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk, &bo,
        )
        .unwrap_or_else(|error| panic!("BS prerequisite row {index} {path}: {error}"));
        let bu = decode_bu(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk, &bo,
            &bs,
        )
        .unwrap_or_else(|error| panic!("BU prerequisite row {index} {path}: {error}"));

        let got = mimir_replay::decode_replay_network_post_bu_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk, &bo,
            &bs, &bu,
        )
        .unwrap_or_else(|error| panic!("BY row {index} {path}: {error}"));

        valid_rows += 1;
        assert_eq!(got.control_composition, bu, "{path}");
        assert_eq!(got.context, k3_context(), "{path}");

        if bu.property_control {
            true_rows += 1;
            assert!(
                path.ends_with("test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay"),
                "{path}"
            );
            assert_eq!(bu.control_start_bit, 3238, "{path}");
            assert_eq!(bu.control_end_bit, 3239, "{path}");
            assert_eq!(bu.stop_bit, 3239, "{path}");

            let header = got.following_header.as_ref().expect("true BU row must expose one header");
            assert!(header.property_present, "{path}");
            assert_eq!(header.property_present_start_bit, 3238, "{path}");
            assert_eq!(header.property_present_end_bit, 3239, "{path}");
            assert_eq!(header.stream_id_start_bit, Some(3239), "{path}");
            assert_eq!(header.stream_id_end_bit, Some(3245), "{path}");
            assert_eq!(header.stream_id, Some(61), "{path}");
            assert_eq!(header.stream_id_bound, Some(110), "{path}");
            assert_eq!(header.prop_id_bits, Some(6), "{path}");
            assert_eq!(header.resolved_property_object_index, Some(67), "{path}");
            assert_eq!(
                header.resolved_property_object_name.as_deref(),
                Some("TAGame.PRI_TA:ClientLoadoutsOnline"),
                "{path}"
            );
            assert_eq!(
                header.resolved_attribute_tag,
                Some(mimir_replay::ReplayNetworkAttributeTagV1::LoadoutsOnline),
                "{path}"
            );
            assert_eq!(header.payload_start_bit, Some(3245), "{path}");
            assert_eq!(header.stop_bit, 3245, "{path}");
            assert_eq!(got.stop_bit, 3245, "{path}");

            let truncation_bytes = usize::try_from((bu.stop_bit + 7) / 8)
                .expect("true-row truncation byte count fits usize");
            assert!(truncation_bytes < network.len(), "{path}");
            assert!(
                mimir_replay::decode_replay_network_post_bu_following_header_v1(
                    &network[..truncation_bytes],
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
                    &bs,
                    &bu,
                )
                .is_err(),
                "truncation inside the true-row header must reject"
            );

            let mut unresolved_plan = plan.clone();
            let actor_index = usize::try_from(header.actor_object_index)
                .expect("actor object index fits usize");
            assert!(actor_index < unresolved_plan.object_lookups.len(), "{path}");
            unresolved_plan.object_lookups[actor_index] = None;
            assert!(
                mimir_replay::decode_replay_network_post_bu_following_header_v1(
                    &network,
                    &prior,
                    &control,
                    &unresolved_plan,
                    k3_context(),
                    &an,
                    &ay,
                    &ba,
                    &be,
                    &bi,
                    &bk,
                    &bo,
                    &bs,
                    &bu,
                )
                .is_err(),
                "unresolved actor lookup must reject"
            );
        } else {
            false_rows += 1;
            assert!(path.ends_with("external_fixtures/sample_002.replay"), "{path}");
            assert_eq!(bu.control_start_bit, 11239, "{path}");
            assert_eq!(bu.control_end_bit, 11240, "{path}");
            assert_eq!(bu.stop_bit, 11240, "{path}");
            assert!(got.following_header.is_none(), "{path}");
            assert_eq!(got.stop_bit, 11240, "{path}");
        }

        let repeated = mimir_replay::decode_replay_network_post_bu_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk, &bo,
            &bs, &bu,
        )
        .expect("repeat BY decode");
        assert_eq!(repeated, got, "{path}");

        let mut post_stop_poison = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("post-BY poison bit fits usize");
        assert!(poison_bit / 8 < post_stop_poison.len(), "{path}");
        let old_after_stop = raw_lsb(&post_stop_poison, got.stop_bit);
        set_bit(&mut post_stop_poison, poison_bit, !old_after_stop);
        let after_poison = mimir_replay::decode_replay_network_post_bu_following_header_v1(
            &post_stop_poison,
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
            &bs,
            &bu,
        )
        .expect("post-BY poison must not affect bounded result");
        assert_eq!(after_poison, got, "{path}");

        let mut corrupt_bu = bu.clone();
        corrupt_bu.stop_bit += 1;
        assert!(
            mimir_replay::decode_replay_network_post_bu_following_header_v1(
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
                &bs,
                &corrupt_bu,
            )
            .is_err(),
            "corrupt supplied BU prerequisite must reject"
        );

        let mut corrupt_bs = bs.clone();
        let prior_header = corrupt_bs
            .header_composition
            .following_header
            .as_mut()
            .expect("BS row retains BO header");
        prior_header.actor_object_index = prior_header
            .actor_object_index
            .checked_add(1)
            .expect("actor index increment");
        assert!(
            mimir_replay::decode_replay_network_post_bu_following_header_v1(
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
                &corrupt_bs,
                &bu,
            )
            .is_err(),
            "wrong actor identity in supplied BS prerequisite must reject"
        );

        let wrong_context = mimir_replay::ReplayNetworkK3DecodeContextV1 {
            version_major: 868,
            version_minor: 32,
            net_version: 10,
            is_rl_223: true,
        };
        assert!(
            mimir_replay::decode_replay_network_post_bu_following_header_v1(
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
                &bs,
                &bu,
            )
            .is_err(),
            "RL223 widening must reject"
        );
    }

    assert_eq!(valid_rows, 2, "BY authority-row drift");
    assert_eq!(false_rows, 1, "BY false-terminator drift");
    assert_eq!(true_rows, 1, "BY true-continuation drift");
}

#[test]
fn r3_18by_source_scope_recomputes_bu_once_decodes_one_header_suffix_and_no_payload() {
    let source = include_str!("../src/lib.rs");
    let begin_marker = "// R3.18BY PRE-ADMISSION BEGIN bounded post-BU mixed-continuation following header";
    let end_marker = "// R3.18BY PRE-ADMISSION END bounded post-BU mixed-continuation following header";
    let begin = source.find(begin_marker).expect("BY begin marker");
    let relative_end = source[begin..].find(end_marker).expect("BY end marker");
    let block = &source[begin..begin + relative_end + end_marker.len()];

    assert_eq!(
        block
            .matches("decode_replay_network_post_bs_following_control_v1(")
            .count(),
        1,
        "BY must recompute BU exactly once",
    );
    assert_eq!(
        block
            .matches("decode_replay_network_existing_actor_property_header_suffix_v1(")
            .count(),
        1,
        "BY must invoke the existing header suffix exactly once",
    );
    assert_eq!(
        block.matches("decode_replay_network_primitive_scalar_v1(").count(),
        0,
        "BY must not decode a following primitive payload"
    );
    assert_eq!(
        block.matches("decode_replay_network_k2_v1(").count(),
        0,
        "BY must not decode a following K2 payload"
    );
    assert_eq!(block.matches(".read_bit(").count(), 0, "BY must not read another control bit");
    assert!(!block.contains("while "), "BY must not contain a while loop");
    assert!(!block.contains("loop {"), "BY must not contain a generic loop");
}
'''

if TEST.exists():
    raise SystemExit(f'{TEST} already exists')
TEST.write_text(test, encoding='utf-8')
