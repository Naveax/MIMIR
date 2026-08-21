from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "crates/mimir-replay/src/lib.rs"
TEST = ROOT / "crates/mimir-replay/tests/r3_18an_post_ak_payload.rs"

MARKER = "// R3.18AK END bounded post-AG following-header composition"

INSERT = r'''

// R3.18AN PRE-ADMISSION BEGIN bounded post-AK payload composition
/// Bounded composition of the published R3.18AK following header plus exactly one
/// R3.18AM-observed Int payload.
///
/// `stop_bit` is exactly the first bit after the 32-bit Int payload. This type is
/// deliberately boundary-specific and does not admit another property-control bit,
/// another header/payload, a repeated property loop, or a generic cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
    pub header_composition:
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    pub following_payload: ReplayNetworkPrimitiveScalarDecodeV1,
    pub stop_bit: u64,
}

fn network_existing_actor_post_ak_payload_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-AK payload error: {category}: {}",
        detail.into()
    ))
}

/// Compose exactly one R3.18AM-observed Int payload after a valid published R3.18AK header.
///
/// The nested R3.18AK composition revalidates the supplied R3.18AG control and exact
/// R3.18AJ seven-field header membership. This function then reuses the existing stateless
/// primitive scalar decoder for exactly one Int payload, requires the observed 32-bit width,
/// and stops at the payload end without reading the next `property_present` bit.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1> {
    let header_composition = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        network_bytes,
        prior,
        control,
        lookup_plan,
        context,
    )?;

    let tag = header_composition
        .following_header
        .resolved_attribute_tag
        .ok_or_else(|| {
            network_existing_actor_post_ak_payload_error(
                "missing-resolved-attribute-tag",
                "published R3.18AK header has no resolved attribute tag",
            )
        })?;
    if tag != ReplayNetworkAttributeTagV1::Int {
        return Err(network_existing_actor_post_ak_payload_error(
            "unsupported-payload-tag",
            format!("R3.18AM admits only Int at this boundary, got {tag:?}"),
        ));
    }

    let payload_start_bit = header_composition
        .following_header
        .payload_start_bit
        .ok_or_else(|| {
            network_existing_actor_post_ak_payload_error(
                "missing-payload-start",
                "published R3.18AK header has no payload start",
            )
        })?;
    if payload_start_bit != header_composition.stop_bit
        || payload_start_bit != header_composition.following_header.stop_bit
    {
        return Err(network_existing_actor_post_ak_payload_error(
            "header-stop-mismatch",
            format!(
                "payload_start={payload_start_bit}, composition_stop={}, header_stop={}",
                header_composition.stop_bit, header_composition.following_header.stop_bit,
            ),
        ));
    }

    let following_payload =
        decode_replay_network_primitive_scalar_v1(network_bytes, payload_start_bit, tag)?;
    if following_payload.attribute_tag != ReplayNetworkAttributeTagV1::Int
        || following_payload.payload_start_bit != payload_start_bit
        || following_payload.payload_width != 32
        || following_payload.payload_end_bit != following_payload.stop_bit
        || !matches!(
            following_payload.value,
            ReplayNetworkPrimitiveScalarValueV1::Int(_)
        )
    {
        return Err(network_existing_actor_post_ak_payload_error(
            "int-boundary-mismatch",
            format!(
                "start={}, end={}, width={}, stop={}, value={:?}",
                following_payload.payload_start_bit,
                following_payload.payload_end_bit,
                following_payload.payload_width,
                following_payload.stop_bit,
                following_payload.value,
            ),
        ));
    }
    let expected_end = payload_start_bit.checked_add(32).ok_or_else(|| {
        network_existing_actor_post_ak_payload_error(
            "payload-end-overflow",
            "32-bit Int payload end overflowed u64",
        )
    })?;
    if following_payload.payload_end_bit != expected_end {
        return Err(network_existing_actor_post_ak_payload_error(
            "payload-end-mismatch",
            format!(
                "payload start {payload_start_bit} requires end {expected_end}, got {}",
                following_payload.payload_end_bit,
            ),
        ));
    }

    let stop_bit = following_payload.stop_bit;
    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
        header_composition,
        following_payload,
        stop_bit,
    })
}
// R3.18AN PRE-ADMISSION END bounded post-AK payload composition
'''

TEST_CONTENT = r'''use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
    decode_replay_network_primitive_scalar_v1,
};
use std::path::PathBuf;

fn sample_network_and_plan() -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../external_fixtures/sample_001.replay");
    let replay_bytes = std::fs::read(&path).expect("read sample_001 replay");
    let input = ReplayInput::Memory {
        label: "r318an_sample_001".to_owned(),
        bytes: replay_bytes.clone(),
    };
    let scaffold = MinimalReplayContentScaffoldReader
        .read_content_scaffold(&input)
        .expect("content scaffold");
    let network = replay_bytes[usize::try_from(scaffold.network_start).unwrap()
        ..usize::try_from(scaffold.network_end).unwrap()]
        .to_vec();
    let plan = MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&input)
        .expect("lookup plan");
    (network, plan)
}

fn k2_context() -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version: 10,
        is_rl_223: false,
    }
}

fn k3_context() -> ReplayNetworkK3DecodeContextV1 {
    ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: false,
    }
}

fn ad_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        network, 10227, 98, plan,
    )
    .expect("R3.18B first property");
    let second =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            network,
            &first,
            plan,
            k2_context(),
        )
        .expect("R3.18J second payload");
    let following =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            network,
            &second,
            plan,
            k3_context(),
        )
        .expect("R3.18T following payload");
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        network,
        &following,
        plan,
        k3_context(),
    )
    .expect("R3.18AD payload")
}

fn ag_control(
    network: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        network,
        prior,
        k3_context(),
    )
    .expect("R3.18AG true control")
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

#[test]
fn r3_18an_sample_001_composes_exact_int32_payload_and_matches_primitive() {
    let (network, plan) = sample_network_and_plan();
    let prior = ad_prior(&network, &plan);
    let control = ag_control(&network, &prior);
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
        &network,
        &prior,
        &control,
        &plan,
        k3_context(),
    )
    .expect("R3.18AN bounded Int payload");

    assert_eq!(got.header_composition.stop_bit, 10360);
    assert_eq!(got.following_payload.payload_start_bit, 10360);
    assert_eq!(got.following_payload.payload_end_bit, 10392);
    assert_eq!(got.following_payload.payload_width, 32);
    assert_eq!(got.stop_bit, 10392);
    assert_eq!(
        got.following_payload.value,
        ReplayNetworkPrimitiveScalarValueV1::Int(3)
    );

    let direct = decode_replay_network_primitive_scalar_v1(
        &network,
        10360,
        ReplayNetworkAttributeTagV1::Int,
    )
    .expect("direct Int primitive");
    assert_eq!(got.following_payload, direct);
}

#[test]
fn r3_18an_payload_truncation_fails_closed_after_ak_header() {
    let (network, plan) = sample_network_and_plan();
    let prior = ad_prior(&network, &plan);
    let control = ag_control(&network, &prior);
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
            &network[..1298],
            &prior,
            &control,
            &plan,
            k3_context(),
        )
        .is_err()
    );
}

#[test]
fn r3_18an_wrong_exact_context_and_corrupt_control_fail_closed() {
    let (network, plan) = sample_network_and_plan();
    let prior = ad_prior(&network, &plan);
    let control = ag_control(&network, &prior);

    let mut wrong_context = k3_context();
    wrong_context.version_major -= 1;
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
            &network,
            &prior,
            &control,
            &plan,
            wrong_context,
        )
        .is_err()
    );

    let mut corrupt_control = control.clone();
    corrupt_control.stop_bit += 1;
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
            &network,
            &prior,
            &corrupt_control,
            &plan,
            k3_context(),
        )
        .is_err()
    );
}

#[test]
fn r3_18an_post_payload_poison_proves_zero_next_control_consumption() {
    let (network, plan) = sample_network_and_plan();
    let prior = ad_prior(&network, &plan);
    let control = ag_control(&network, &prior);
    let baseline = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
        &network,
        &prior,
        &control,
        &plan,
        k3_context(),
    )
    .expect("baseline R3.18AN payload");
    assert_eq!(baseline.stop_bit, 10392);

    let mut poisoned = network.clone();
    let original = (poisoned[10392 / 8] >> (10392 % 8)) & 1 != 0;
    set_bit(&mut poisoned, 10392, !original);
    let after = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
        &poisoned,
        &prior,
        &control,
        &plan,
        k3_context(),
    )
    .expect("post-payload poison must not affect R3.18AN");
    assert_eq!(after, baseline);
}
'''

text = LIB.read_text(encoding="utf-8")
if text.count(MARKER) != 1:
    raise SystemExit(f"expected exactly one AK marker, found {text.count(MARKER)}")
if "R3.18AN PRE-ADMISSION BEGIN" in text:
    raise SystemExit("R3.18AN pre-admission implementation already present")
text = text.replace(MARKER, MARKER + INSERT, 1)
LIB.write_text(text, encoding="utf-8", newline="\n")

if TEST.exists():
    raise SystemExit("R3.18AN test unexpectedly already exists")
TEST.write_text(TEST_CONTENT, encoding="utf-8", newline="\n")
