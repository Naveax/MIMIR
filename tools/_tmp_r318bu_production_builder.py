from pathlib import Path

lib_path = Path('crates/mimir-replay/src/lib.rs')
test_path = Path('crates/mimir-replay/tests/r3_18bu_post_bs_following_control.rs')

source = lib_path.read_text(encoding='utf-8')
if 'R3.18BU PRE-ADMISSION BEGIN bounded post-BS next property-control' in source:
    raise SystemExit('R3.18BU block already exists')

block = r'''

// R3.18BU PRE-ADMISSION BEGIN bounded post-BS next property-control
/// Bounded composition of the published R3.18BS payload plus exactly one
/// R3.18BR-observed property-control bit. The result stops immediately after
/// that bit and does not consume any later stream/header/payload/control data.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkPostBsFollowingControlDecodeV1 {
    pub payload_composition: ReplayNetworkPostBoFollowingPayloadDecodeV1,
    pub property_control: bool,
    pub control_start_bit: u64,
    pub control_end_bit: u64,
    pub stop_bit: u64,
}

#[allow(clippy::too_many_arguments)]
pub fn decode_replay_network_post_bs_following_control_v1(
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
    bs_prior: &ReplayNetworkPostBoFollowingPayloadDecodeV1,
) -> Result<ReplayNetworkPostBsFollowingControlDecodeV1> {
    let expected_bs = decode_replay_network_post_bo_following_payload_v1(
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
        bo_prior,
    )?;

    if &expected_bs != bs_prior {
        return Err(network_bit_error(
            "r3.18bu-mismatched-bs-prerequisite",
            "supplied R3.18BS result does not equal the exact recomputed prerequisite",
        ));
    }

    let (expected_control, payload_end_bit) = match &expected_bs.following_payload {
        ReplayNetworkPostBoFollowingPayloadValueV1::Boolean(decoded) => {
            let exact = decoded.attribute_tag == ReplayNetworkAttributeTagV1::Boolean
                && decoded.payload_start_bit == 11238
                && decoded.payload_width == 1
                && decoded.payload_end_bit == 11239
                && decoded.stop_bit == 11239
                && decoded.value == ReplayNetworkPrimitiveScalarValueV1::Boolean(true);
            if !exact {
                return Err(network_bit_error(
                    "r3.18bu-non-authority-boolean-row",
                    "Boolean payload is outside the immutable R3.18BT/BQ/BR row",
                ));
            }
            (false, 11239u64)
        }
        ReplayNetworkPostBoFollowingPayloadValueV1::ActiveActor(decoded) => {
            let exact = decoded.attribute_tag == ReplayNetworkAttributeTagV1::ActiveActor
                && decoded.payload_start_bit == 3205
                && decoded.payload_width == 33
                && decoded.payload_end_bit == 3238
                && decoded.value
                    == ReplayNetworkK2ValueV1::ActiveActor {
                        active: true,
                        actor: 1,
                    };
            if !exact {
                return Err(network_bit_error(
                    "r3.18bu-non-authority-active-actor-row",
                    "ActiveActor payload is outside the immutable R3.18BT/BQ/BR row",
                ));
            }
            (true, 3238u64)
        }
    };

    if expected_bs.stop_bit != payload_end_bit {
        return Err(network_bit_error(
            "r3.18bu-payload-stop-mismatch",
            format!(
                "R3.18BS stop {} does not equal immutable payload end {payload_end_bit}",
                expected_bs.stop_bit
            ),
        ));
    }

    let control_start_bit = expected_bs.stop_bit;
    let bit_position = usize::try_from(control_start_bit).map_err(|_| {
        network_bit_error(
            "r3.18bu-invalid-control-position",
            format!("control start {control_start_bit} does not fit usize"),
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_bit_error(
            "r3.18bu-invalid-network-length",
            "network bit length overflows usize",
        )
    })?;
    if bit_position >= total_bits {
        return Err(network_bit_error(
            "r3.18bu-insufficient-control-bit",
            format!("need one control bit at {control_start_bit}, but no bit remains"),
        ));
    }

    let byte_index = bit_position / 8;
    let bit_index = bit_position % 8;
    let property_control = ((network_bytes[byte_index] >> bit_index) & 1) != 0;
    if property_control != expected_control {
        return Err(network_bit_error(
            "r3.18bu-immutable-control-mismatch",
            format!(
                "observed control bit {property_control} does not equal immutable R3.18BR authority {expected_control}"
            ),
        ));
    }

    let control_end_bit = control_start_bit.checked_add(1).ok_or_else(|| {
        network_bit_error(
            "r3.18bu-control-end-overflow",
            "control end bit overflows u64",
        )
    })?;

    Ok(ReplayNetworkPostBsFollowingControlDecodeV1 {
        payload_composition: expected_bs,
        property_control,
        control_start_bit,
        control_end_bit,
        stop_bit: control_end_bit,
    })
}
// R3.18BU PRE-ADMISSION END bounded post-BS next property-control
'''
lib_path.write_text(source.rstrip() + block + '\n', encoding='utf-8')

test = r'''include!("r3_18bs_post_bo_payload.rs");

use mimir_replay::{
    ReplayNetworkPostBsFollowingControlDecodeV1 as R3_18BuResultV1,
    decode_replay_network_post_bs_following_control_v1 as decode_bu,
};

fn expected_bu_control(path: &str) -> Option<bool> {
    if path.ends_with("external_fixtures/sample_002.replay") {
        Some(false)
    } else if path
        .ends_with("test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay")
    {
        Some(true)
    } else {
        None
    }
}

#[test]
fn r3_18bu_exact_two_row_lane_consumes_one_control_bit_and_stops() {
    let (mut excluded_au, mut excluded_be, mut false_terminators, mut valid_rows) =
        (0usize, 0usize, 0usize, 0usize);
    let (mut false_controls, mut true_controls) = (0usize, 0usize);

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318bu_{index}"));
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
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba,
        )
        .unwrap_or_else(|error| panic!("BE prerequisite row {index} {path}: {error}"));

        if be.following_header.is_none() {
            excluded_be += 1;
            continue;
        }

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

        if bo.following_header.is_none() {
            false_terminators += 1;
            assert!(path.ends_with("external_fixtures/sample_003.replay"), "{path}");
            assert!(expected_bu_control(path).is_none(), "{path}");
            assert!(
                decode_bs(
                    &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be,
                    &bi, &bk, &bo,
                )
                .is_err(),
                "BP/BO false terminator must not obtain a BS prerequisite"
            );
            continue;
        }

        let expected_control = expected_bu_control(path)
            .unwrap_or_else(|| panic!("unfrozen BU authority row {path}"));
        let bs = decode_bs(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk,
            &bo,
        )
        .unwrap_or_else(|error| panic!("BS prerequisite row {index} {path}: {error}"));

        let got: R3_18BuResultV1 = decode_bu(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk,
            &bo, &bs,
        )
        .unwrap_or_else(|error| panic!("BU row {index} {path}: {error}"));

        valid_rows += 1;
        if got.property_control {
            true_controls += 1;
        } else {
            false_controls += 1;
        }
        assert_eq!(got.payload_composition, bs, "{path}");
        assert_eq!(got.control_start_bit, bs.stop_bit, "{path}");
        assert_eq!(got.control_end_bit, bs.stop_bit + 1, "{path}");
        assert_eq!(got.stop_bit, got.control_end_bit, "{path}");
        assert_eq!(got.property_control, expected_control, "{path}");
        assert_eq!(raw_lsb(&network, got.control_start_bit), expected_control, "{path}");

        let repeated = decode_bu(
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk,
            &bo, &bs,
        )
        .expect("repeat BU control");
        assert_eq!(repeated, got, "{path}");

        let mut post_stop_poison = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("post-BU poison bit fits usize");
        assert!(poison_bit / 8 < post_stop_poison.len(), "{path}");
        let old_after_stop = raw_lsb(&post_stop_poison, got.stop_bit);
        set_bit(&mut post_stop_poison, poison_bit, !old_after_stop);
        let after_poison = decode_bu(
            &post_stop_poison, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be,
            &bi, &bk, &bo, &bs,
        )
        .expect("bit after BU stop must not affect BU result");
        assert_eq!(after_poison, got, "{path}");

        let mut wrong_control = network.clone();
        let control_bit = usize::try_from(got.control_start_bit).expect("control bit fits usize");
        set_bit(&mut wrong_control, control_bit, !expected_control);
        let wrong_control_error = decode_bu(
            &wrong_control, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi,
            &bk, &bo, &bs,
        )
        .expect_err("mutated BR authority bit must fail");
        assert!(
            wrong_control_error
                .to_string()
                .contains("r3.18bu-immutable-control-mismatch"),
            "unexpected wrong-control error for {path}: {wrong_control_error}"
        );

        let mut corrupt_bs = bs.clone();
        corrupt_bs.stop_bit += 1;
        assert!(
            decode_bu(
                &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi,
                &bk, &bo, &corrupt_bs,
            )
            .is_err(),
            "corrupt supplied BS prerequisite must fail for {path}"
        );

        let wrong_context = ReplayNetworkK3DecodeContextV1 {
            version_major: 868,
            version_minor: 32,
            net_version: 10,
            is_rl_223: true,
        };
        assert!(
            decode_bu(
                &network, &prior, &control, &plan, wrong_context, &an, &ay, &ba, &be, &bi,
                &bk, &bo, &bs,
            )
            .is_err(),
            "wrong context must fail for {path}"
        );

        let truncation_byte = usize::try_from(got.control_start_bit / 8)
            .expect("truncation byte fits usize");
        assert!(truncation_byte < network.len(), "{path}");
        assert!(
            decode_bu(
                &network[..truncation_byte], &prior, &control, &plan, k3_context(), &an, &ay,
                &ba, &be, &bi, &bk, &bo, &bs,
            )
            .is_err(),
            "truncation before the control-containing byte must fail for {path}"
        );
    }

    assert_eq!(excluded_au, 7, "upstream AU false-terminator drift");
    assert_eq!(excluded_be, 37, "BE false-terminator drift");
    assert_eq!(false_terminators, 1, "BO false terminator drift");
    assert_eq!(valid_rows, 2, "BU authority-row drift");
    assert_eq!(false_controls, 1, "BU false-control drift");
    assert_eq!(true_controls, 1, "BU true-control drift");
    assert_eq!(excluded_au + excluded_be + false_terminators + valid_rows, 47);
}

#[test]
fn r3_18bu_source_scope_recomputes_bs_once_reads_one_direct_bit_and_has_no_loop() {
    let source = include_str!("../src/lib.rs");
    let begin_marker = "// R3.18BU PRE-ADMISSION BEGIN bounded post-BS next property-control";
    let end_marker = "// R3.18BU PRE-ADMISSION END bounded post-BS next property-control";
    let begin = source.find(begin_marker).expect("BU begin marker");
    let relative_end = source[begin..].find(end_marker).expect("BU end marker");
    let block = &source[begin..begin + relative_end + end_marker.len()];

    assert_eq!(
        block.matches("decode_replay_network_post_bo_following_payload_v1(").count(),
        1,
        "BU must recompute BS exactly once",
    );
    assert_eq!(
        block.matches("network_bytes[byte_index]").count(),
        1,
        "BU must inspect exactly one direct LSB-first byte location",
    );
    assert_eq!(block.matches(".read_bit(").count(), 0, "BU must not use a cursor read");
    assert!(!block.contains("while "), "BU must not contain a while loop");
    assert!(!block.contains("loop {"), "BU must not contain a generic loop");
}
'''

test_path.write_text(test, encoding='utf-8')
print('R3.18BU candidate staged')
