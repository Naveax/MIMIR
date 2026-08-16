from pathlib import Path

ROOT = Path('.')
LIB = ROOT / 'crates/mimir-replay/src/lib.rs'
TEST = ROOT / 'crates/mimir-replay/tests/r3_18d_next_property_control.rs'


def replace_one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


src = LIB.read_text(encoding='utf-8')
marker = '''/// Decode exactly one R3.17B-admitted primitive scalar payload.\n'''
addition = r'''/// Exactly one loop-control bit immediately after an already-decoded R3.18B first K1 property.
///
/// This result is deliberately not a reusable property-loop cursor. `stop_bit` is exactly one bit
/// after `first_property.stop_bit` and does not authorize a second stream/header/payload decode.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1 {
    pub next_property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

/// Read exactly the next `property_present` bit after one valid R3.18B first K1 property.
///
/// The caller must supply the already-decoded first-property result. This function validates that
/// result's published boundary invariants, reuses the private LSB-first network cursor for one bit,
/// and stops immediately. It never decodes a second stream id, property header, or payload.
pub fn decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
    network_bytes: &[u8],
    first_property: &ReplayNetworkExistingActorSinglePrimitivePropertyV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1> {
    if !first_property.header.property_present {
        return Err(network_existing_actor_after_first_property_control_error(
            "invalid-first-property",
            "first property result is not present",
        ));
    }

    let payload_start_bit = first_property.header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_after_first_property_control_error(
            "invalid-first-property",
            "first property header is missing payload_start_bit",
        )
    })?;
    if first_property.header.stop_bit != payload_start_bit
        || first_property.scalar.payload_start_bit != payload_start_bit
        || first_property.scalar.stop_bit != first_property.scalar.payload_end_bit
        || first_property.stop_bit != first_property.scalar.payload_end_bit
    {
        return Err(network_existing_actor_after_first_property_control_error(
            "boundary-mismatch",
            format!(
                "header_stop={} header_payload_start={} scalar_start={} scalar_end={} scalar_stop={} first_stop={}",
                first_property.header.stop_bit,
                payload_start_bit,
                first_property.scalar.payload_start_bit,
                first_property.scalar.payload_end_bit,
                first_property.scalar.stop_bit,
                first_property.stop_bit,
            ),
        ));
    }

    if first_property.header.resolved_attribute_tag != Some(first_property.scalar.attribute_tag) {
        return Err(network_existing_actor_after_first_property_control_error(
            "tag-mismatch",
            format!(
                "header tag {:?} differs from scalar tag {:?}",
                first_property.header.resolved_attribute_tag, first_property.scalar.attribute_tag
            ),
        ));
    }

    let decoded_width = first_property
        .scalar
        .payload_end_bit
        .checked_sub(first_property.scalar.payload_start_bit)
        .ok_or_else(|| {
            network_existing_actor_after_first_property_control_error(
                "boundary-mismatch",
                "scalar payload end precedes payload start",
            )
        })?;
    if decoded_width != u64::from(first_property.scalar.payload_width) {
        return Err(network_existing_actor_after_first_property_control_error(
            "width-mismatch",
            format!(
                "scalar range width {decoded_width} differs from declared width {}",
                first_property.scalar.payload_width
            ),
        ));
    }

    let property_present_start_bit = first_property.stop_bit;
    let property_present_end_bit = property_present_start_bit.checked_add(1).ok_or_else(|| {
        network_existing_actor_after_first_property_control_error(
            "invalid-position",
            "next property_present end bit overflows u64",
        )
    })?;
    let start = usize::try_from(property_present_start_bit).map_err(|_| {
        network_existing_actor_after_first_property_control_error(
            "invalid-position",
            format!(
                "next property_present start bit {property_present_start_bit} does not fit usize"
            ),
        )
    })?;
    let end = usize::try_from(property_present_end_bit).map_err(|_| {
        network_existing_actor_after_first_property_control_error(
            "invalid-position",
            format!(
                "next property_present end bit {property_present_end_bit} does not fit usize"
            ),
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_existing_actor_after_first_property_control_error(
            "invalid-length",
            "network bit length overflows usize",
        )
    })?;
    if end > total_bits {
        return Err(network_existing_actor_after_first_property_control_error(
            "insufficient-bits",
            format!(
                "need one property_present bit at position {start}, but network bit length is {total_bits}"
            ),
        ));
    }

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;
    let next_property_present = cursor.read_bit()?;
    let stop_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        network_existing_actor_after_first_property_control_error(
            "invalid-position",
            "one-bit control stop does not fit u64",
        )
    })?;
    if stop_bit != property_present_end_bit {
        return Err(network_existing_actor_after_first_property_control_error(
            "control-stop-mismatch",
            format!(
                "one-bit control stopped at {stop_bit}, expected {property_present_end_bit}"
            ),
        ));
    }

    Ok(ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1 {
        next_property_present,
        property_present_start_bit,
        property_present_end_bit,
        stop_bit,
    })
}

'''
src = replace_one(src, marker, addition + marker, 'R3.18D API insertion')

error_marker = '''fn network_existing_actor_single_property_error(\n'''
error_addition = r'''fn network_existing_actor_after_first_property_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay existing actor after first primitive property control error: {category}: {}",
        detail.into()
    ))
}

'''
src = replace_one(src, error_marker, error_addition + error_marker, 'R3.18D error helper')
LIB.write_text(src, encoding='utf-8', newline='\n')

TEST.write_text(r'''use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1,
    ReplayNetworkExistingActorSinglePrimitivePropertyV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_property_control_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn sample_001_lookup_plan() -> ReplayNetworkLookupPlanV1 {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let bytes = std::fs::read(&path).expect("read sample_001.replay");
    let input = ReplayInput::Memory {
        label: "r318d_sample_001_context".to_string(),
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
    next_property_present: Option<bool>,
    trailing_bits: usize,
) -> Vec<u8> {
    let payload_start = property_start + 1 + stream_width;
    let payload_end = payload_start + payload_width;
    let control_width = usize::from(next_property_present.is_some());
    let total_bits = payload_end + control_width + trailing_bits;
    let mut bytes = vec![0u8; total_bits.div_ceil(8)];
    set_bit(&mut bytes, property_start, true);
    write_bits(&mut bytes, property_start + 1, stream_width, stream_id);
    write_bits(&mut bytes, payload_start, payload_width, raw);
    if let Some(value) = next_property_present {
        set_bit(&mut bytes, payload_end, value);
    }
    bytes
}

fn retag_stream(
    plan: &mut ReplayNetworkLookupPlanV1,
    actor_object: usize,
    stream_id: u32,
    tag: ReplayNetworkAttributeTagV1,
) {
    let lookup = plan.object_lookups[actor_object]
        .as_mut()
        .expect("actor lookup must exist");
    let property = lookup
        .properties
        .iter_mut()
        .find(|property| property.stream_id == stream_id)
        .expect("stream must resolve");
    property.tag = tag;
}

fn first_property(
    bytes: &[u8],
    property_start: usize,
    actor_object: u32,
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorSinglePrimitivePropertyV1 {
    decode_replay_network_existing_actor_single_primitive_property_v1(
        bytes,
        property_start as u64,
        actor_object,
        plan,
    )
    .expect("first R3.18B property should decode")
}

fn control(
    bytes: &[u8],
    first: &ReplayNetworkExistingActorSinglePrimitivePropertyV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1 {
    decode_replay_network_existing_actor_after_first_primitive_property_control_v1(bytes, first)
        .expect("R3.18D control bit should decode")
}

#[test]
fn r3_18c_float_terminator_shape_reads_exactly_false_and_stops_one_bit_later() {
    let plan = sample_001_lookup_plan();
    let bytes = packet(0, 17, 5, 32, 1_092_616_192, Some(false), 9);
    let first = first_property(&bytes, 0, 344, &plan);
    assert_eq!(
        first.header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Float)
    );
    assert_eq!(first.stop_bit, 38);

    let decoded = control(&bytes, &first);
    assert!(!decoded.next_property_present);
    assert_eq!(decoded.property_present_start_bit, 38);
    assert_eq!(decoded.property_present_end_bit, 39);
    assert_eq!(decoded.stop_bit, 39);
}

#[test]
fn r3_18c_int_62_continuation_shape_reads_exactly_true_and_stops_one_bit_later() {
    let plan = sample_001_lookup_plan();
    let bytes = packet(0, 27, 6, 32, 62, Some(true), 9);
    let first = first_property(&bytes, 0, 98, &plan);
    assert_eq!(
        first.header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Int)
    );
    assert_eq!(first.stop_bit, 39);

    let decoded = control(&bytes, &first);
    assert!(decoded.next_property_present);
    assert_eq!(decoded.property_present_start_bit, 39);
    assert_eq!(decoded.property_present_end_bit, 40);
    assert_eq!(decoded.stop_bit, 40);
}

#[test]
fn aligned_and_unaligned_first_property_ends_preserve_exact_control_coordinates() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);

    for (property_start, expected_start, next_value) in [(2usize, 40u64, false), (3, 41, true)] {
        let bytes = packet(
            property_start,
            30,
            5,
            32,
            7,
            Some(next_value),
            9,
        );
        let first = first_property(&bytes, property_start, 47, &plan);
        assert_eq!(first.stop_bit, expected_start);
        let decoded = control(&bytes, &first);
        assert_eq!(decoded.next_property_present, next_value);
        assert_eq!(decoded.property_present_start_bit, expected_start);
        assert_eq!(decoded.property_present_end_bit, expected_start + 1);
        assert_eq!(decoded.stop_bit, expected_start + 1);
    }
}

#[test]
fn bits_after_control_stop_do_not_affect_result() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let clean = packet(3, 30, 5, 32, 62, Some(true), 17);
    let first = first_property(&clean, 3, 47, &plan);
    let clean_control = control(&clean, &first);

    let mut poisoned = clean.clone();
    let poison_start = usize::try_from(clean_control.stop_bit).unwrap();
    for offset in 0..8 {
        set_bit(&mut poisoned, poison_start + offset, offset % 2 == 0);
    }
    let poisoned_control = control(&poisoned, &first);
    assert_eq!(poisoned_control, clean_control);
}

#[test]
fn missing_next_property_bit_rejects_atomically() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(2, 30, 5, 32, 62, None, 0);
    assert_eq!(bytes.len() * 8, 40);
    let first = first_property(&bytes, 2, 47, &plan);
    assert_eq!(first.stop_bit, 40);

    let error = decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
        &bytes, &first,
    )
    .expect_err("missing next property_present bit must fail");
    assert!(error.to_string().contains("insufficient-bits"));
}

#[test]
fn malformed_first_property_boundary_is_rejected_before_control_read() {
    let mut plan = sample_001_lookup_plan();
    retag_stream(&mut plan, 47, 30, ReplayNetworkAttributeTagV1::Int);
    let bytes = packet(3, 30, 5, 32, 62, Some(true), 9);
    let mut first = first_property(&bytes, 3, 47, &plan);
    first.stop_bit += 1;

    let error = decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
        &bytes, &first,
    )
    .expect_err("malformed R3.18B boundary must fail before one-bit read");
    assert!(error.to_string().contains("boundary-mismatch"));
}

#[test]
fn control_result_is_exactly_repeatable() {
    let plan = sample_001_lookup_plan();
    let bytes = packet(0, 27, 6, 32, 62, Some(true), 9);
    let first = first_property(&bytes, 0, 98, &plan);
    let first_read = control(&bytes, &first);
    let second_read = control(&bytes, &first);
    assert_eq!(first_read, second_read);
}
''', encoding='utf-8', newline='\n')

print('R3_18D_PATCH=PASS')
