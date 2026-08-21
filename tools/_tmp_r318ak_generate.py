from pathlib import Path

LIB = Path("crates/mimir-replay/src/lib.rs")
TEST = Path("crates/mimir-replay/tests/r3_18ak_post_ag_following_header.rs")
MARKER = "/// The published R3.18W true-only control is recomputed from the supplied R3.18T prior and used"

INSERT = r'''
// R3.18AK BEGIN bounded post-AG following-header composition
const R3_18AJ_POST_AG_HEADER_CONTEXTS_V1: [
    (u32, u8, u32, ReplayNetworkAttributeTagV1, i32, i32, i32);
    17
] = [
    (60, 5, 38, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 47, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 84, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 85, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 91, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 93, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 95, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 100, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 106, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 108, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 109, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 112, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 122, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (67, 6, 68, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (72, 6, 70, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (72, 6, 73, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (110, 6, 37, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
];

fn r3_18aj_post_ag_header_context_contains_v1(
    stream_id_bound: u32,
    prop_id_bits: u8,
    property_object_index: u32,
    attribute_tag: ReplayNetworkAttributeTagV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> bool {
    R3_18AJ_POST_AG_HEADER_CONTEXTS_V1.contains(&(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context.version_major,
        context.version_minor,
        context.net_version,
    ))
}

/// Exactly one R3.18AJ-admitted property header after a valid published R3.18AG true control.
///
/// The supplied R3.18AG control is recomputed from the R3.18AD payload prior and must match
/// exactly. The existing stateless property-header primitive is then replayed from the same
/// property-present coordinate. This result stops at `payload_start` and consumes no payload or
/// later property-control bit.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 {
    pub control: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    pub following_header: ReplayNetworkExistingActorFirstPropertyHeaderV1,
    pub stop_bit: u64,
}

fn network_existing_actor_post_ag_following_header_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-AG following-header error: {category}: {}",
        detail.into()
    ))
}

/// Compose exactly one R3.18AJ-admitted post-AG following header through `payload_start`.
///
/// This function is deliberately boundary-specific. It validates the supplied R3.18AG result by
/// recomputing it from the exact R3.18AD prior, reuses the existing stateless header primitive,
/// requires full seven-field R3.18AJ tuple membership, and exposes no payload decoder, later
/// control bit, property iterator, or reusable cursor.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1> {
    let expected_control = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        network_bytes,
        prior,
        context,
    )?;
    if expected_control != *control {
        return Err(network_existing_actor_post_ag_following_header_error(
            "invalid-r3-18ag-control",
            format!(
                "supplied R3.18AG control {:?} differs from recomputed {:?}",
                control, expected_control
            ),
        ));
    }
    if !control.following_property_present {
        return Err(network_existing_actor_post_ag_following_header_error(
            "invalid-r3-18ag-control",
            "R3.18AK requires the published R3.18AG admitted true control",
        ));
    }
    if control.property_present_start_bit != prior.stop_bit
        || control.property_present_end_bit != control.stop_bit
        || control.property_present_end_bit != control.property_present_start_bit + 1
    {
        return Err(network_existing_actor_post_ag_following_header_error(
            "control-boundary-mismatch",
            format!(
                "prior stop {}, control [{}, {}) stop {}",
                prior.stop_bit,
                control.property_present_start_bit,
                control.property_present_end_bit,
                control.stop_bit,
            ),
        ));
    }

    let actor_object_index = prior.header_composition.following_header.actor_object_index;
    let following_header = decode_replay_network_existing_actor_first_property_header_v1(
        network_bytes,
        control.property_present_start_bit,
        actor_object_index,
        lookup_plan,
    )?;
    if !following_header.property_present {
        return Err(network_existing_actor_post_ag_following_header_error(
            "control-header-mismatch",
            "R3.18AG reported a present property but the post-AG header primitive did not",
        ));
    }
    if following_header.property_present_start_bit != control.property_present_start_bit
        || following_header.property_present_end_bit != control.property_present_end_bit
        || control.stop_bit != following_header.property_present_end_bit
    {
        return Err(network_existing_actor_post_ag_following_header_error(
            "control-header-boundary-mismatch",
            format!(
                "control bits [{}, {}) stop {}, header bits [{}, {})",
                control.property_present_start_bit,
                control.property_present_end_bit,
                control.stop_bit,
                following_header.property_present_start_bit,
                following_header.property_present_end_bit,
            ),
        ));
    }
    if following_header.actor_object_index != actor_object_index {
        return Err(network_existing_actor_post_ag_following_header_error(
            "actor-mismatch",
            format!(
                "prior actor {actor_object_index} differs from post-AG header actor {}",
                following_header.actor_object_index,
            ),
        ));
    }

    let payload_start_bit = following_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_post_ag_following_header_error(
            "missing-payload-start",
            "present post-AG header has no payload start",
        )
    })?;
    if following_header.stop_bit != payload_start_bit {
        return Err(network_existing_actor_post_ag_following_header_error(
            "payload-boundary-mismatch",
            format!(
                "post-AG header stop {} differs from payload start {payload_start_bit}",
                following_header.stop_bit,
            ),
        ));
    }

    let (Some(stream_id_bound), Some(prop_id_bits), Some(property_object_index), Some(attribute_tag)) = (
        following_header.stream_id_bound,
        following_header.prop_id_bits,
        following_header.resolved_property_object_index,
        following_header.resolved_attribute_tag,
    ) else {
        return Err(network_existing_actor_post_ag_following_header_error(
            "incomplete-r3-18aj-header-context",
            "post-AG header is missing one or more R3.18AJ tuple fields",
        ));
    };
    if !r3_18aj_post_ag_header_context_contains_v1(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context,
    ) {
        return Err(network_existing_actor_post_ag_following_header_error(
            "unadmitted-r3-18aj-header-context",
            format!(
                "R3.18AJ exact tuple rejected bound={stream_id_bound} bits={prop_id_bits} object={property_object_index} tag={attribute_tag:?} version={}.{} net{}",
                context.version_major, context.version_minor, context.net_version,
            ),
        ));
    }

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 {
        control: control.clone(),
        following_header,
        stop_bit: payload_start_bit,
    })
}
// R3.18AK END bounded post-AG following-header composition

'''

TEST_CONTENT = r'''use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::{Path, PathBuf};

fn network_and_plan(path: &Path, label: &str) -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let replay_bytes = std::fs::read(path).expect("read replay");
    let input = ReplayInput::Memory {
        label: label.to_owned(),
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

fn fixture(path: &str, label: &str) -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(path);
    network_and_plan(&path, label)
}

fn k2_context() -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 { net_version: 10, is_rl_223: false }
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
    first_start: u64,
    actor_object: u32,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        network, first_start, actor_object, plan,
    ).expect("R3.18B first");
    let second = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
        network, &first, plan, k2_context(),
    ).expect("R3.18J second");
    let t = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        network, &second, plan, k3_context(),
    ).expect("R3.18T payload");
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        network, &t, plan, k3_context(),
    ).expect("R3.18AD payload")
}

fn ag_control(
    network: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        network, prior, k3_context(),
    ).expect("R3.18AG control")
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value { bytes[position / 8] |= 1 << (position % 8); }
    else { bytes[position / 8] &= !(1 << (position % 8)); }
}

#[test]
fn r3_18ak_representative_ai_headers_match_exact_boundaries() {
    let cases = [
        ("../../external_fixtures/sample_001.replay", 10227, 98, 10353, 10354, 10360, 39, 67, 6, 68),
        ("../../external_fixtures/sample_002.replay", 11019, 106, 11145, 11146, 11152, 41, 72, 6, 73),
        ("../../external_fixtures/sample_003.replay", 7603, 103, 7729, 7730, 7736, 41, 72, 6, 70),
        ("../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay", 2848, 112, 2973, 2974, 2980, 35, 60, 5, 85),
        ("../../test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay", 2838, 117, 3079, 3080, 3087, 33, 110, 6, 37),
    ];
    for (index, (path, first_start, actor, ag_start, ag_stop, payload_start, stream_id, bound, bits, object)) in cases.into_iter().enumerate() {
        let (network, plan) = fixture(path, &format!("r318ak_positive_{index}"));
        let prior = ad_prior(&network, &plan, first_start, actor);
        assert_eq!(prior.stop_bit, ag_start);
        let control = ag_control(&network, &prior);
        assert_eq!(control.property_present_start_bit, ag_start);
        assert_eq!(control.stop_bit, ag_stop);
        let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(),
        ).unwrap();
        assert_eq!(got.control, control);
        assert_eq!(got.following_header.property_present_start_bit, ag_start);
        assert_eq!(got.following_header.property_present_end_bit, ag_stop);
        assert_eq!(got.following_header.stream_id, Some(stream_id));
        assert_eq!(got.following_header.stream_id_bound, Some(bound));
        assert_eq!(got.following_header.prop_id_bits, Some(bits));
        assert_eq!(got.following_header.resolved_property_object_index, Some(object));
        assert_eq!(got.following_header.resolved_attribute_tag, Some(ReplayNetworkAttributeTagV1::Int));
        assert_eq!(got.following_header.payload_start_bit, Some(payload_start));
        assert_eq!(got.following_header.stop_bit, payload_start);
        assert_eq!(got.stop_bit, payload_start);
    }
}

#[test]
fn r3_18ak_repeatability_and_post_payload_poison_preserve_result() {
    let (network, plan) = fixture("../../external_fixtures/sample_001.replay", "r318ak_repeat");
    let prior = ad_prior(&network, &plan, 10227, 98);
    let control = ag_control(&network, &prior);
    let clean = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, k3_context(),
    ).unwrap();
    let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, k3_context(),
    ).unwrap();
    assert_eq!(clean, repeated);
    let mut poisoned = network.clone();
    for offset in 0..16usize {
        set_bit(&mut poisoned, clean.stop_bit as usize + offset, offset % 2 == 0);
    }
    let after = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &poisoned, &prior, &control, &plan, k3_context(),
    ).unwrap();
    assert_eq!(after, clean);
}

#[test]
fn r3_18ak_tampered_ag_truncation_actor_lookup_and_version_fail_closed() {
    let (network, plan) = fixture("../../external_fixtures/sample_001.replay", "r318ak_fail_closed");
    let prior = ad_prior(&network, &plan, 10227, 98);
    let control = ag_control(&network, &prior);

    let mut bad_control = control.clone();
    bad_control.stop_bit += 1;
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &bad_control, &plan, k3_context(),
    ).unwrap_err();
    assert!(error.to_string().contains("invalid-r3-18ag-control"));

    let mut bad_prior = prior.clone();
    bad_prior.header_composition.following_header.actor_object_index = u32::MAX;
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &bad_prior, &control, &plan, k3_context(),
    ).is_err());

    let mut missing_lookup = plan.clone();
    missing_lookup.object_lookups[98] = None;
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &missing_lookup, k3_context(),
    ).is_err());

    let wrong = ReplayNetworkK3DecodeContextV1 { version_major: 868, version_minor: 31, net_version: 10, is_rl_223: false };
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, wrong,
    ).is_err());

    let (network, plan) = fixture("../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay", "r318ak_trunc");
    let prior = ad_prior(&network, &plan, 2848, 112);
    let control = ag_control(&network, &prior);
    assert_eq!(control.stop_bit, 2974);
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network[..372], &prior, &control, &plan, k3_context(),
    ).is_err());
}

#[test]
fn r3_18ak_cartesian_fabricated_and_old_z_contexts_are_rejected() {
    let (network, plan) = fixture("../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay", "r318ak_widening");
    let prior = ad_prior(&network, &plan, 2848, 112);
    let control = ag_control(&network, &prior);
    for (object_index, tag) in [
        (68, ReplayNetworkAttributeTagV1::Int),
        (39, ReplayNetworkAttributeTagV1::Int),
        (34, ReplayNetworkAttributeTagV1::ActiveActor),
    ] {
        let mut widened = plan.clone();
        let property = widened.object_lookups[112]
            .as_mut().unwrap().properties.iter_mut()
            .find(|property| property.stream_id == 35).unwrap();
        assert_eq!(property.object_index, 85);
        property.object_index = object_index;
        property.tag = tag;
        let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &widened, k3_context(),
        ).unwrap_err();
        assert!(error.to_string().contains("unadmitted-r3-18aj-header-context"), "{error}");
    }
}

#[test]
fn r3_18ak_source_scope_is_one_ag_control_one_header_and_no_payload_or_loop() {
    let source = include_str!("../src/lib.rs");
    let start = source.find("pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1").expect("R3.18AK function");
    let tail = &source[start..];
    let end = tail.find("/// The published R3.18W true-only control is recomputed from the supplied R3.18T prior and used").expect("R3.18AA boundary after R3.18AK");
    let function = &tail[..end];
    assert_eq!(function.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(").count(), 1);
    assert_eq!(function.matches("decode_replay_network_existing_actor_first_property_header_v1(").count(), 1);
    assert_eq!(function.matches("r3_18aj_post_ag_header_context_contains_v1(").count(), 1);
    assert!(!function.contains("decode_replay_network_primitive_scalar_v1("));
    assert!(!function.contains("decode_replay_network_k2_v1("));
    assert!(!function.contains("decode_replay_network_k3_v1("));
    assert!(!function.contains("cursor.read_bit()"));
    assert!(!function.contains("\n    while "));
    assert!(!function.contains("\n    for "));
}
'''

source = LIB.read_text(encoding="utf-8")
if "R3.18AK BEGIN bounded post-AG following-header composition" in source:
    raise SystemExit("AK block already present")
if source.count(MARKER) != 1:
    raise SystemExit(f"expected exactly one AA marker, got {source.count(MARKER)}")
source = source.replace(MARKER, INSERT + MARKER, 1)
LIB.write_text(source, encoding="utf-8", newline="\n")
if TEST.exists():
    raise SystemExit("AK focused test already exists")
TEST.write_text(TEST_CONTENT, encoding="utf-8", newline="\n")
print("PASS generated R3.18AK two-file production candidate")
