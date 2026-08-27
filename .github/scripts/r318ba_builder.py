from pathlib import Path

LIB = Path("crates/mimir-replay/src/lib.rs")
TEST = Path("crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs")
marker = "// R3.18AY PRE-ADMISSION END bounded post-AU one-following-payload\n"

block = r'''
// R3.18BA PRE-ADMISSION BEGIN bounded post-AY mixed following control
/// One validated R3.18AY Int/32 payload composition plus exactly one
/// R3.18AX-admitted following `property_present` control bit.
/// Both boolean values are admitted. The decoder stops exactly one bit later.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
    pub payload_composition: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    pub following_property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

fn network_existing_actor_post_ay_following_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-AY following-control error: {category}: {}",
        detail.into()
    ))
}

pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
    an_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    au_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    ay_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1> {
    let expected_ay =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
            network_bytes,
            prior,
            control,
            lookup_plan,
            context,
            an_prior,
            au_prior,
        )?;

    if expected_ay != *ay_prior {
        return Err(network_existing_actor_post_ay_following_control_error(
            "invalid-r3-18ay-prior",
            "supplied R3.18AY payload result does not match recomputed authority",
        ));
    }

    let payload = &ay_prior.following_payload;
    if ay_prior.header_composition != *au_prior
        || ay_prior.header_composition.stop_bit != payload.payload_start_bit
        || payload.attribute_tag != ReplayNetworkAttributeTagV1::Int
        || payload.payload_width != 32
        || payload.payload_end_bit != payload.stop_bit
        || payload.stop_bit != ay_prior.stop_bit
        || !matches!(&payload.value, ReplayNetworkPrimitiveScalarValueV1::Int(_))
    {
        return Err(network_existing_actor_post_ay_following_control_error(
            "invalid-ay-boundary",
            format!(
                "header_stop={} payload_start={} payload_end={} payload_stop={} ay_stop={} width={} tag={:?} value={:?}",
                ay_prior.header_composition.stop_bit,
                payload.payload_start_bit,
                payload.payload_end_bit,
                payload.stop_bit,
                ay_prior.stop_bit,
                payload.payload_width,
                payload.attribute_tag,
                payload.value
            ),
        ));
    }

    let start = ay_prior.stop_bit;
    let start_usize = usize::try_from(start).map_err(|_| {
        network_existing_actor_post_ay_following_control_error(
            "invalid-position",
            format!("R3.18AY stop bit {start} does not fit usize"),
        )
    })?;
    let expected_end = start.checked_add(1).ok_or_else(|| {
        network_existing_actor_post_ay_following_control_error(
            "invalid-position",
            "one-bit following-control end overflows u64",
        )
    })?;

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start_usize;
    let property_present_start_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        network_existing_actor_post_ay_following_control_error(
            "invalid-position",
            "following-control start does not fit u64",
        )
    })?;
    let following_property_present = cursor.read_bit().map_err(|error| {
        network_existing_actor_post_ay_following_control_error(
            "control-read",
            format!("cannot read one following property_present bit: {error}"),
        )
    })?;
    let property_present_end_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        network_existing_actor_post_ay_following_control_error(
            "invalid-position",
            "following-control end does not fit u64",
        )
    })?;

    if property_present_start_bit != start || property_present_end_bit != expected_end {
        return Err(network_existing_actor_post_ay_following_control_error(
            "control-stop-mismatch",
            format!(
                "start={} expected_start={start} end={} expected_end={expected_end}",
                property_present_start_bit, property_present_end_bit
            ),
        ));
    }

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
        payload_composition: ay_prior.clone(),
        following_property_present,
        property_present_start_bit,
        property_present_end_bit,
        stop_bit: property_present_end_bit,
    })
}
// R3.18BA PRE-ADMISSION END bounded post-AY mixed following control
'''

test = r'''include!("r3_18ay_post_au_payload.rs");

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
            decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &au, &ay)
                .unwrap_or_else(|error| panic!("BA row {index} {path}: {error}"));

        assert_eq!(got.payload_composition, ay, "{path}");
        assert_eq!(got.following_property_present, expected, "{path}");
        assert_eq!(got.property_present_start_bit, ay.stop_bit, "{path}");
        assert_eq!(got.property_present_end_bit, ay.stop_bit + 1, "{path}");
        assert_eq!(got.stop_bit, ay.stop_bit + 1, "{path}");
        if got.following_property_present { true_count += 1; } else { false_count += 1; }

        let repeated = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &au, &ay)
            .expect("repeat R3.18BA");
        assert_eq!(repeated, got, "{path}");

        let mut poisoned = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("poison bit fits usize");
        assert!(poison_bit / 8 < poisoned.len(), "{path}");
        let poison_value = raw_lsb(&poisoned, got.stop_bit);
        set_bit(&mut poisoned, poison_bit, !poison_value);
        let after_poison = decode_ba(&poisoned, &prior, &control, &plan, k3_context(), &an, &au, &ay)
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
    let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).expect("AY prerequisite");

    let mut corrupt_ay = ay.clone();
    corrupt_ay.stop_bit += 1;
    assert!(decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &au, &corrupt_ay).is_err());

    let mut bad_prior = prior.clone();
    bad_prior.header_composition.following_header.actor_object_index = u32::MAX;
    assert!(decode_ba(&network, &bad_prior, &control, &plan, k3_context(), &an, &au, &ay).is_err());

    let mut missing_lookup = plan.clone();
    missing_lookup.object_lookups[98] = None;
    assert!(decode_ba(&network, &prior, &control, &missing_lookup, k3_context(), &an, &au, &ay).is_err());

    let mut wrong_context = k3_context();
    wrong_context.version_major -= 1;
    assert!(decode_ba(&network, &prior, &control, &plan, wrong_context, &an, &au, &ay).is_err());

    let carrier_cut = usize::try_from(ay.stop_bit / 8).expect("carrier cut fits usize");
    assert!(decode_ba(&network[..carrier_cut], &prior, &control, &plan, k3_context(), &an, &au, &ay).is_err());
}

#[test]
fn r3_18ba_source_scope_is_one_ay_recompute_one_read_bit_and_no_following_decode_or_loop() {
    let source = include_str!("../src/lib.rs");
    let begin = source.find("// R3.18BA PRE-ADMISSION BEGIN bounded post-AY mixed following control").expect("BA begin");
    let end_marker = "// R3.18BA PRE-ADMISSION END bounded post-AY mixed following control";
    let end = source[begin..].find(end_marker).map(|offset| begin + offset + end_marker.len()).expect("BA end");
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
'''

text = LIB.read_text(encoding="utf-8")
if text.count(marker) != 1:
    raise SystemExit(f"expected one AY end marker, found {text.count(marker)}")
if "R3.18BA PRE-ADMISSION BEGIN" in text:
    raise SystemExit("R3.18BA block already present")
LIB.write_text(text.replace(marker, marker + "\n" + block + "\n", 1), encoding="utf-8", newline="\n")
if TEST.exists():
    raise SystemExit(f"{TEST} already exists")
TEST.write_text(test, encoding="utf-8", newline="\n")
