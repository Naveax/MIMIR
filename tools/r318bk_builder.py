from pathlib import Path

LIB = Path("crates/mimir-replay/src/lib.rs")
TEST = Path("crates/mimir-replay/tests/r3_18bk_post_bi_following_control.rs")

marker = "// R3.18BI PRE-ADMISSION END bounded post-BE one-following-payload\n"
source = LIB.read_text(encoding="utf-8")
if "// R3.18BK PRE-ADMISSION BEGIN bounded post-BI following control" in source:
    raise SystemExit("R3.18BK block already present")
if source.count(marker) != 1:
    raise SystemExit(f"expected exactly one BI end marker, got {source.count(marker)}")

block = r'''
// R3.18BK PRE-ADMISSION BEGIN bounded post-BI following control
/// One validated R3.18BI payload result plus exactly one R3.18BH-admitted
/// following `property_present` control bit.
///
/// Both boolean values are admitted at this exact boundary. The result stops
/// exactly one bit after the validated BI payload end and deliberately does not
/// inspect a following stream, header, payload, or second control bit.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
    pub payload_composition: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    pub property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

fn network_existing_actor_post_bi_following_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-BI following-control error: {category}: {}",
        detail.into()
    ))
}

/// Recompute exactly one published R3.18BI payload result, validate the supplied
/// BI authority, then consume exactly one following LSB-first `property_present`
/// bit. False and true are both successful data at this boundary.
#[allow(clippy::too_many_arguments)]
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_v1(
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
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1> {
    let expected_bi = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
        network_bytes,
        prior,
        control,
        lookup_plan,
        context,
        an_prior,
        ay_prior,
        ba_prior,
        be_prior,
    )?;
    if &expected_bi != bi_prior {
        return Err(network_existing_actor_post_bi_following_control_error(
            "invalid-r3-18bi-prior",
            "supplied R3.18BI payload result differs from recomputed published authority",
        ));
    }

    if bi_prior.header_composition.stop_bit != bi_prior.following_payload.payload_start_bit
        || bi_prior.following_payload.payload_end_bit != bi_prior.following_payload.stop_bit
        || bi_prior.stop_bit != bi_prior.following_payload.payload_end_bit
    {
        return Err(network_existing_actor_post_bi_following_control_error(
            "invalid-prior-boundary",
            "R3.18BK requires the exact validated R3.18BI payload-end boundary",
        ));
    }

    let property_present_start_bit = bi_prior.stop_bit;
    let property_present_start = usize::try_from(property_present_start_bit).map_err(|_| {
        network_existing_actor_post_bi_following_control_error(
            "invalid-position",
            format!("R3.18BI stop bit {property_present_start_bit} does not fit usize"),
        )
    })?;
    let property_present_end = property_present_start.checked_add(1).ok_or_else(|| {
        network_existing_actor_post_bi_following_control_error(
            "invalid-position",
            "following-control bit end overflows usize",
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_existing_actor_post_bi_following_control_error(
            "invalid-length",
            "network bit length overflows usize",
        )
    })?;
    if property_present_end > total_bits {
        return Err(network_existing_actor_post_bi_following_control_error(
            "insufficient-bits",
            format!(
                "need one following control bit at {property_present_start}, but network ends at {total_bits}"
            ),
        ));
    }

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = property_present_start;
    let property_present = cursor.read_bit().map_err(|error| {
        network_existing_actor_post_bi_following_control_error(
            "control-read-failed",
            error.to_string(),
        )
    })?;
    if cursor.position_bits() != property_present_end {
        return Err(network_existing_actor_post_bi_following_control_error(
            "invalid-stop",
            format!(
                "one control bit must stop at {property_present_end}, got {}",
                cursor.position_bits()
            ),
        ));
    }

    let property_present_end_bit = u64::try_from(property_present_end).map_err(|_| {
        network_existing_actor_post_bi_following_control_error(
            "invalid-position",
            "following-control end does not fit u64",
        )
    })?;

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
        payload_composition: bi_prior.clone(),
        property_present,
        property_present_start_bit,
        property_present_end_bit,
        stop_bit: property_present_end_bit,
    })
}
// R3.18BK PRE-ADMISSION END bounded post-BI following control
'''.lstrip("\n")

source = source.replace(marker, marker + "\n" + block, 1)
LIB.write_text(source, encoding="utf-8")

TEST.write_text(r'''include!("r3_18bi_post_be_following_payload.rs");

use mimir_replay::{
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_control_v1 as decode_bk,
};

fn expected_bh_control(path: &str) -> Option<(u64, bool)> {
    if path.ends_with("external_fixtures/sample_002.replay") {
        Some((11231, true))
    } else if path.ends_with("external_fixtures/sample_003.replay") {
        Some((7815, false))
    } else if path.ends_with(
        "test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay",
    ) {
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
            assert!(expected_bh_control(path).is_none(), "unexpected BH authority {path}");
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
            assert!(expected_bh_control(path).is_none(), "unexpected BH authority {path}");
            assert!(decode_bi(
                &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be,
            ).is_err(), "BE false terminator reached BI/BK production {path}");
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
        assert_eq!(got.property_present_start_bit, got.payload_composition.stop_bit, "{path}");
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
            &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi,
        ).expect("repeat R3.18BK");
        assert_eq!(repeated, got, "{path}");

        let mut poisoned = network.clone();
        let after_stop = usize::try_from(got.stop_bit).expect("post-BK poison bit fits usize");
        assert!(after_stop / 8 < poisoned.len(), "{path}");
        let old = raw_lsb(&poisoned, got.stop_bit);
        set_bit(&mut poisoned, after_stop, !old);
        let after_poison = decode_bk(
            &poisoned, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi,
        ).expect("BK must not inspect bits after its stop");
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
        &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba,
    ).expect("BE prerequisite");
    let bi = decode_bi(
        &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be,
    ).expect("BI prerequisite");
    assert_eq!(bi.stop_bit, 11231);

    let mut corrupt_stop = bi.clone();
    corrupt_stop.stop_bit += 1;
    assert!(decode_bk(
        &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &corrupt_stop,
    ).is_err());

    let mut corrupt_value = bi.clone();
    corrupt_value.following_payload.value = ReplayNetworkPrimitiveScalarValueV1::Boolean(false);
    assert!(decode_bk(
        &network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &corrupt_value,
    ).is_err());

    let mut wrong_context = k3_context();
    wrong_context.version_minor -= 1;
    assert!(decode_bk(
        &network, &prior, &control, &plan, wrong_context, &an, &ay, &ba, &be, &bi,
    ).is_err());

    let mut unresolved = plan.clone();
    unresolved.object_lookups[actor_object as usize]
        .as_mut()
        .expect("actor lookup")
        .properties
        .clear();
    assert!(decode_bk(
        &network, &prior, &control, &unresolved, k3_context(), &an, &ay, &ba, &be, &bi,
    ).is_err());

    let cut = usize::try_from(bi.stop_bit / 8).expect("byte truncation");
    assert!(decode_bk(
        &network[..cut], &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi,
    ).is_err());
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
    assert_eq!(block.matches("decode_replay_network_primitive_scalar_v1(").count(), 0);
    assert_eq!(block.matches("decode_replay_network_existing_actor_property_header_suffix_v1(").count(), 0);
    assert!(!block.contains("\n    while "));
    assert!(!block.contains("\n    for "));
    assert!(!block.contains("\n    loop {"));
}
''', encoding="utf-8")
