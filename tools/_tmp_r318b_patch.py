from pathlib import Path

ROOT = Path('.')
LIB = ROOT / 'crates/mimir-replay/src/lib.rs'
TEST = ROOT / 'crates/mimir-replay/tests/r3_18b_single_k1_property.rs'


def replace_one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


src = LIB.read_text(encoding='utf-8')
marker = '''/// Decode exactly one R3.17B-admitted primitive scalar payload.
///
/// The caller supplies an already resolved attribute tag and the exact
'''
addition = r'''/// One complete existing-actor first property composed from the already-published
/// property-header boundary and primitive K1 scalar decoder.
///
/// This type is deliberately one-property only. `stop_bit` is exactly the first bit after the
/// primitive scalar payload. It does not authorize or consume the next `property_present` bit.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorSinglePrimitivePropertyV1 {
    pub header: ReplayNetworkExistingActorFirstPropertyHeaderV1,
    pub scalar: ReplayNetworkPrimitiveScalarDecodeV1,
    pub stop_bit: u64,
}

/// Decode exactly one existing-actor property when its resolved tag is an admitted K1 scalar.
///
/// The existing R3.16B header decoder remains the sole authority for `property_present`, bounded
/// stream decoding, inherited lookup resolution, and `payload_start_bit`. The existing R3.17C
/// primitive scalar decoder remains the sole authority for Boolean/Byte/Enum/Float/Int/Int64 wire
/// decoding. This composition stops at the scalar end and never reads the next property bit.
pub fn decode_replay_network_existing_actor_single_primitive_property_v1(
    network_bytes: &[u8],
    property_start_bit: u64,
    actor_object_index: u32,
    lookup_plan: &ReplayNetworkLookupPlanV1,
) -> Result<ReplayNetworkExistingActorSinglePrimitivePropertyV1> {
    let header = decode_replay_network_existing_actor_first_property_header_v1(
        network_bytes,
        property_start_bit,
        actor_object_index,
        lookup_plan,
    )?;

    if !header.property_present {
        return Err(network_existing_actor_single_property_error(
            "property-absent",
            "the selected first property is absent; no payload may be composed",
        ));
    }

    let attribute_tag = header.resolved_attribute_tag.ok_or_else(|| {
        network_existing_actor_single_property_error(
            "missing-tag",
            "resolved property header did not contain an attribute tag",
        )
    })?;
    let payload_start_bit = header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_single_property_error(
            "missing-payload-start",
            "resolved property header did not contain a payload start bit",
        )
    })?;

    if header.stop_bit != payload_start_bit {
        return Err(network_existing_actor_single_property_error(
            "header-stop-mismatch",
            format!(
                "property header stop bit {} differs from payload start bit {payload_start_bit}",
                header.stop_bit
            ),
        ));
    }

    match attribute_tag {
        ReplayNetworkAttributeTagV1::Boolean
        | ReplayNetworkAttributeTagV1::Byte
        | ReplayNetworkAttributeTagV1::Enum
        | ReplayNetworkAttributeTagV1::Float
        | ReplayNetworkAttributeTagV1::Int
        | ReplayNetworkAttributeTagV1::Int64 => {}
        _ => {
            return Err(network_existing_actor_single_property_error(
                "unsupported-tag",
                format!(
                    "attribute tag {attribute_tag:?} is outside the R3.18B primitive K1 composition"
                ),
            ));
        }
    }

    let scalar = decode_replay_network_primitive_scalar_v1(
        network_bytes,
        payload_start_bit,
        attribute_tag,
    )?;
    if scalar.payload_start_bit != payload_start_bit || scalar.stop_bit != scalar.payload_end_bit {
        return Err(network_existing_actor_single_property_error(
            "scalar-boundary-mismatch",
            format!(
                "scalar boundary start/end/stop = {}/{}/{} but expected start {payload_start_bit}",
                scalar.payload_start_bit, scalar.payload_end_bit, scalar.stop_bit
            ),
        ));
    }

    let stop_bit = scalar.stop_bit;
    Ok(ReplayNetworkExistingActorSinglePrimitivePropertyV1 {
        header,
        scalar,
        stop_bit,
    })
}

'''
src = replace_one(src, marker, addition + marker, 'single-property insertion')

error_marker = '''fn network_existing_actor_property_error(category: &str, detail: impl Into<String>) -> MimirError {
'''
error_addition = r'''fn network_existing_actor_single_property_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay existing actor single primitive property error: {category}: {}",
        detail.into()
    ))
}

'''
src = replace_one(src, error_marker, error_addition + error_marker, 'composition error helper')
LIB.write_text(src, encoding='utf-8', newline='\n')

TEST.write_text(r'''use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn sample_001_lookup_plan() -> ReplayNetworkLookupPlanV1 {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let bytes = std::fs::read(&path).expect("read sample_001.replay");
    let input = ReplayInput::Memory {
        label: "r318b_sample_001_context".to_string(),
        bytes,
    };
    MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&input)
        .expect("materialize admitted lookup plan")
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

fn write_bits(bytes: &mut [u8], start: usize, width: usize, value: u64) {
    for bit in 0..width {
        set_bit(bytes, start + bit, ((value >> bit) & 1) != 0);
    }
}

fn packet(
    property_start: usize,
    stream_id: u64,
    stream_width: usize,
    payload_width: usize,
    raw: u64,
    trailing_bits: usize,
) -> Vec<u8> {
    let payload_start = property_start + 1 + stream_width;
    let total_bits = payload_start + payload_width + trailing_bits;
    let mut bytes = vec![0u8; total_bits.div_ceil(8)];
    set_bit(&mut bytes, property_start, true);
    write_bits(&mut bytes, property_start + 1, stream_width, stream_id);
    write_bits(&mut bytes, payload_start, payload_width, raw);
    bytes
}

fn scalar_width(tag: ReplayNetworkAttributeTagV1) -> usize {
    match tag {
        ReplayNetworkAttributeTagV1::Boolean => 1,
        ReplayNetworkAttributeTagV1::Byte => 8,
        ReplayNetworkAttributeTagV1::Enum => 11,
        ReplayNetworkAttributeTagV1::Float | ReplayNetworkAttributeTagV1::Int => 32,
        ReplayNetworkAttributeTagV1::Int64 => 64,
        _ => panic!("non-K1 tag in test helper"),
    }
}

fn expected_value(
    tag: ReplayNetworkAttributeTagV1,
    raw: u64,
) -> ReplayNetworkPrimitiveScalarValueV1 {
    match tag {
        ReplayNetworkAttributeTagV1::Boolean => {
            ReplayNetworkPrimitiveScalarValueV1::Boolean(raw != 0)
        }
        ReplayNetworkAttributeTagV1::Byte => ReplayNetworkPrimitiveScalarValueV1::Byte(raw as u8),
        ReplayNetworkAttributeTagV1::Enum => ReplayNetworkPrimitiveScalarValueV1::Enum(raw as u16),
        ReplayNetworkAttributeTagV1::Float => {
            let raw_bits = raw as u32;
            ReplayNetworkPrimitiveScalarValueV1::Float {
                raw_bits,
                value: f32::from_bits(raw_bits),
            }
        }
        ReplayNetworkAttributeTagV1::Int => {
            ReplayNetworkPrimitiveScalarValueV1::Int((raw as u32) as i32)
        }
        ReplayNetworkAttributeTagV1::Int64 => {
            ReplayNetworkPrimitiveScalarValueV1::Int64(raw as i64)
        }
        _ => panic!("non-K1 tag in test helper"),
    }
}

fn retag_stream(
    plan: &mut ReplayNetworkLookupPlanV1,
    actor_object: usize,
    stream_id: u32,
    tag: ReplayNetworkAttributeTagV1,
) -> u32 {
    let lookup = plan.object_lookups[actor_object]
        .as_mut()
        .expect("actor lookup must exist");
    let property = lookup
        .properties
        .iter_mut()
        .find(|property| property.stream_id == stream_id)
        .expect("stream must resolve");
    property.tag = tag;
    property.object_index
}

#[test]
fn all_six_k1_tags_compose_at_aligned_and_unaligned_property_starts() {
    let cases = [
        (ReplayNetworkAttributeTagV1::Boolean, 1u64),
        (ReplayNetworkAttributeTagV1::Byte, 0xa5),
        (ReplayNetworkAttributeTagV1::Enum, 0x5a3),
        (
            ReplayNetworkAttributeTagV1::Float,
            u64::from(1.5f32.to_bits()),
        ),
        (
            ReplayNetworkAttributeTagV1::Int,
            u64::from((-12_345i32) as u32),
        ),
        (ReplayNetworkAttributeTagV1::Int64, (-9_876_543_210i64) as u64),
    ];

    for (tag, raw) in cases {
        for property_start in [0usize, 3usize] {
            let mut plan = sample_001_lookup_plan();
            let property_object = retag_stream(&mut plan, 47, 30, tag);
            let width = scalar_width(tag);
            let bytes = packet(property_start, 30, 5, width, raw, 13);
            let decoded = decode_replay_network_existing_actor_single_primitive_property_v1(
                &bytes,
                property_start as u64,
                47,
                &plan,
            )
            .expect("admitted K1 property should compose");

            assert!(decoded.header.property_present);
            assert_eq!(decoded.header.actor_object_index, 47);
            assert_eq!(decoded.header.stream_id, Some(30));
            assert_eq!(decoded.header.stream_id_bound, Some(38));
            assert_eq!(decoded.header.prop_id_bits, Some(5));
            assert_eq!(decoded.header.resolved_property_object_index, Some(property_object));
            assert_eq!(decoded.header.resolved_attribute_tag, Some(tag));
            assert_eq!(
                decoded.header.payload_start_bit,
                Some((property_start + 6) as u64)
            );
            assert_eq!(decoded.header.stop_bit, (property_start + 6) as u64);
            assert_eq!(decoded.scalar.attribute_tag, tag);
            assert_eq!(decoded.scalar.payload_start_bit, (property_start + 6) as u64);
            assert_eq!(decoded.scalar.payload_width, width as u8);
            assert_eq!(
                decoded.scalar.payload_end_bit,
                (property_start + 6 + width) as u64
            );
            assert_eq!(decoded.scalar.value, expected_value(tag, raw));
            assert_eq!(decoded.scalar.stop_bit, decoded.scalar.payload_end_bit);
            assert_eq!(decoded.stop_bit, decoded.scalar.payload_end_bit);
        }
    }
}

#[test]
fn r3_18a_shaped_real_context_int_62_composes_and_stops_at_payload_end() {
    let plan = sample_001_lookup_plan();
    let bytes = packet(0, 27, 6, 32, 62, 17);
    let decoded = decode_replay_network_existing_actor_single_primitive_property_v1(
        &bytes, 0, 98, &plan,
    )
    .expect("R3.18A selected actor/property context should compose");

    assert_eq!(decoded.header.stream_id, Some(27));
    assert_eq!(decoded.header.stream_id_bound, Some(67));
    assert_eq!(decoded.header.prop_id_bits, Some(6));
    assert_eq!(decoded.header.resolved_property_object_index, Some(55));
    assert_eq!(
        decoded.header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Int)
    );
    assert_eq!(decoded.header.payload_start_bit, Some(7));
    assert_eq!(decoded.scalar.payload_start_bit, 7);
    assert_eq!(decoded.scalar.payload_end_bit, 39);
    assert_eq!(decoded.stop_bit, 39);
    assert_eq!(
        decoded.scalar.value,
        ReplayNetworkPrimitiveScalarValueV1::Int(62)
    );
}

#[test]
fn trailing_and_next_property_poison_bits_are_never_consumed() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let clean = packet(3, 30, 5, 32, 62, 17);
    let mut poisoned = clean.clone();
    let payload_end = 3 + 6 + 32;
    for bit in payload_end..(payload_end + 17) {
        set_bit(&mut poisoned, bit, true);
    }

    let clean_result = decode_replay_network_existing_actor_single_primitive_property_v1(
        &clean, 3, 47, &plan,
    )
    .unwrap();
    let poisoned_result = decode_replay_network_existing_actor_single_primitive_property_v1(
        &poisoned, 3, 47, &plan,
    )
    .unwrap();
    assert_eq!(clean_result, poisoned_result);
    assert_eq!(clean_result.stop_bit, payload_end as u64);
}

#[test]
fn absent_first_property_is_rejected_without_payload_composition() {
    let plan = sample_001_lookup_plan();
    let error = decode_replay_network_existing_actor_single_primitive_property_v1(
        &[0xfe], 0, 47, &plan,
    )
    .expect_err("absent property must reject composition");
    assert!(error.to_string().contains("property-absent"));
}

#[test]
fn non_k1_resolved_tag_is_rejected_before_payload_read() {
    let plan = sample_001_lookup_plan();
    let error = decode_replay_network_existing_actor_single_primitive_property_v1(
        &[0x3d], 0, 47, &plan,
    )
    .expect_err("ActiveActor must remain outside R3.18B composition");
    assert!(error.to_string().contains("unsupported-tag"));
}

#[test]
fn header_truncation_fails_closed() {
    let plan = sample_001_lookup_plan();
    let error = decode_replay_network_existing_actor_single_primitive_property_v1(
        &[], 0, 47, &plan,
    )
    .expect_err("missing property-present bit must fail");
    assert!(error.to_string().contains("insufficient-bits"));
}

#[test]
fn payload_truncation_fails_closed_after_exact_header_resolution() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let mut bytes = vec![0u8; 5];
    set_bit(&mut bytes, 3, true);
    write_bits(&mut bytes, 4, 5, 30);
    let error = decode_replay_network_existing_actor_single_primitive_property_v1(
        &bytes, 3, 47, &plan,
    )
    .expect_err("31 payload bits cannot satisfy Int");
    assert!(error.to_string().contains("insufficient-bits"));
}

#[test]
fn repeatability_is_exact() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Enum);
    let bytes = packet(5, 30, 5, 11, 0x341, 9);
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        &bytes, 5, 47, &plan,
    )
    .unwrap();
    let second = decode_replay_network_existing_actor_single_primitive_property_v1(
        &bytes, 5, 47, &plan,
    )
    .unwrap();
    assert_eq!(first, second);
}
''', encoding='utf-8', newline='\n')

print('R3_18B_PATCH=PASS')
