use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_existing_actor_first_property_header_v1,
    decode_replay_network_primitive_scalar_v1,
};
use std::env;
use std::fs;

fn parse_hex(text: &str) -> Result<Vec<u8>, String> {
    if !text.len().is_multiple_of(2) {
        return Err("hex length must be even".to_owned());
    }
    (0..text.len())
        .step_by(2)
        .map(|offset| u8::from_str_radix(&text[offset..offset + 2], 16).map_err(|e| e.to_string()))
        .collect()
}

fn parse_tag(text: &str) -> Result<ReplayNetworkAttributeTagV1, String> {
    match text {
        "Boolean" => Ok(ReplayNetworkAttributeTagV1::Boolean),
        "Byte" => Ok(ReplayNetworkAttributeTagV1::Byte),
        "Enum" => Ok(ReplayNetworkAttributeTagV1::Enum),
        "Float" => Ok(ReplayNetworkAttributeTagV1::Float),
        "Int" => Ok(ReplayNetworkAttributeTagV1::Int),
        "Int64" => Ok(ReplayNetworkAttributeTagV1::Int64),
        _ => Err(format!("unsupported R3.18A scalar tag: {text}")),
    }
}

fn lossless(value: &ReplayNetworkPrimitiveScalarValueV1) -> String {
    match value {
        ReplayNetworkPrimitiveScalarValueV1::Boolean(value) => {
            if *value { "1".to_owned() } else { "0".to_owned() }
        }
        ReplayNetworkPrimitiveScalarValueV1::Byte(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Enum(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Float { raw_bits, .. } => raw_bits.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int64(value) => value.to_string(),
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 13 {
        return Err(format!(
            "usage: {} replay label actor_object stream property_object tag global_property_start global_payload_start global_payload_end window_byte_start window_local_start window_hex",
            args.first().map(String::as_str).unwrap_or("probe")
        )
        .into());
    }

    let replay_path = &args[1];
    let label = &args[2];
    let actor_object: u32 = args[3].parse()?;
    let expected_stream: u32 = args[4].parse()?;
    let expected_property_object: u32 = args[5].parse()?;
    let tag = parse_tag(&args[6]).map_err(std::io::Error::other)?;
    let global_property_start: u64 = args[7].parse()?;
    let global_payload_start: u64 = args[8].parse()?;
    let global_payload_end: u64 = args[9].parse()?;
    let window_byte_start: u64 = args[10].parse()?;
    let local_property_start: u64 = args[11].parse()?;
    let window = parse_hex(&args[12]).map_err(std::io::Error::other)?;

    let replay_bytes = fs::read(replay_path)?;
    let input = ReplayInput::Memory {
        label: label.clone(),
        bytes: replay_bytes,
    };
    let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;

    let header = decode_replay_network_existing_actor_first_property_header_v1(
        &window,
        local_property_start,
        actor_object,
        &plan,
    )?;
    if !header.property_present {
        return Err("selected property unexpectedly absent".into());
    }
    if header.stream_id != Some(expected_stream) {
        return Err(format!("stream mismatch: {:?} != {expected_stream}", header.stream_id).into());
    }
    if header.resolved_property_object_index != Some(expected_property_object) {
        return Err(format!(
            "property object mismatch: {:?} != {expected_property_object}",
            header.resolved_property_object_index
        )
        .into());
    }
    if header.resolved_attribute_tag != Some(tag) {
        return Err(format!("tag mismatch: {:?} != {:?}", header.resolved_attribute_tag, tag).into());
    }

    let base_bit = window_byte_start.checked_mul(8).ok_or("window base overflow")?;
    if base_bit + header.property_present_start_bit != global_property_start {
        return Err("property-present global start mismatch".into());
    }
    let native_payload_start = header.payload_start_bit.ok_or("missing payload start")?;
    if base_bit + native_payload_start != global_payload_start {
        return Err("payload global start mismatch".into());
    }
    if header.stop_bit != native_payload_start {
        return Err("header did not stop exactly at payload start".into());
    }

    let decoded = decode_replay_network_primitive_scalar_v1(&window, native_payload_start, tag)?;
    if base_bit + decoded.payload_end_bit != global_payload_end {
        return Err(format!(
            "payload global end mismatch: {} != {global_payload_end}",
            base_bit + decoded.payload_end_bit
        )
        .into());
    }
    if decoded.stop_bit != decoded.payload_end_bit {
        return Err("scalar stop bit differs from payload end".into());
    }

    let required_bytes = usize::try_from(decoded.payload_end_bit.div_ceil(8))?;
    if required_bytes == 0 || required_bytes > window.len() {
        return Err("invalid selected window length".into());
    }
    let truncated = &window[..required_bytes - 1];
    let truncated_header = decode_replay_network_existing_actor_first_property_header_v1(
        truncated,
        local_property_start,
        actor_object,
        &plan,
    )?;
    let truncated_payload_start = truncated_header
        .payload_start_bit
        .ok_or("truncated header unexpectedly lacks payload start")?;
    if decode_replay_network_primitive_scalar_v1(truncated, truncated_payload_start, tag).is_ok() {
        return Err("truncated scalar unexpectedly decoded".into());
    }

    println!(
        "R3_18A_NATIVE\theader_exact=true\tpayload_start_exact=true\tpayload_end_exact=true\tstop_exact=true\tnegative_truncation=true\tattribute_tag={:?}\tlossless_value={}\tlocal_payload_start={}\tlocal_payload_end={}",
        decoded.attribute_tag,
        lossless(&decoded.value),
        decoded.payload_start_bit,
        decoded.payload_end_bit,
    );
    Ok(())
}
