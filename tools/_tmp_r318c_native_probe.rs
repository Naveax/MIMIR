use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::env;
use std::fs;
use std::path::Path;

fn parse_hex(text: &str) -> Result<Vec<u8>, String> {
    if text.len() % 2 != 0 {
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
        _ => Err(format!("unsupported R3.18C K1 tag: {text}")),
    }
}

fn lossless(value: &ReplayNetworkPrimitiveScalarValueV1) -> String {
    match value {
        ReplayNetworkPrimitiveScalarValueV1::Boolean(value) => {
            if *value {
                "1".to_owned()
            } else {
                "0".to_owned()
            }
        }
        ReplayNetworkPrimitiveScalarValueV1::Byte(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Enum(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Float { raw_bits, .. } => raw_bits.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int64(value) => value.to_string(),
    }
}

fn read_one_bit(bytes: &[u8], cursor: &mut u64, bit_limit: u64) -> Result<bool, String> {
    if *cursor >= bit_limit {
        return Err("bit-limit".to_owned());
    }
    let total_bits = u64::try_from(bytes.len())
        .map_err(|_| "byte length overflow".to_owned())?
        .checked_mul(8)
        .ok_or_else(|| "bit length overflow".to_owned())?;
    if *cursor >= total_bits {
        return Err("byte-limit".to_owned());
    }
    let index = usize::try_from(*cursor).map_err(|_| "cursor overflow".to_owned())?;
    let value = ((bytes[index / 8] >> (index % 8)) & 1) != 0;
    *cursor = cursor.checked_add(1).ok_or_else(|| "cursor overflow".to_owned())?;
    Ok(value)
}

fn set_bit(bytes: &mut Vec<u8>, position: u64, value: bool) -> Result<(), String> {
    let needed_bits = position
        .checked_add(1)
        .ok_or_else(|| "poison position overflow".to_owned())?;
    let needed_bytes = usize::try_from(needed_bits.div_ceil(8))
        .map_err(|_| "poison length overflow".to_owned())?;
    if bytes.len() < needed_bytes {
        bytes.resize(needed_bytes, 0);
    }
    let index = usize::try_from(position).map_err(|_| "poison index overflow".to_owned())?;
    if value {
        bytes[index / 8] |= 1 << (index % 8);
    } else {
        bytes[index / 8] &= !(1 << (index % 8));
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args_os().skip(1);
    let request_path = args.next().ok_or("missing request TSV")?;
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }
    let request = fs::read_to_string(request_path)?;
    let mut row_count = 0usize;

    for line in request.lines().filter(|line| !line.trim().is_empty()) {
        row_count += 1;
        let fields: Vec<&str> = line.split('\t').collect();
        if fields.len() != 16 {
            return Err(format!("expected 16 TSV fields, got {}", fields.len()).into());
        }
        let class = fields[0];
        let replay_path = fields[1];
        let actor_object: u32 = fields[2].parse()?;
        let expected_stream: u32 = fields[3].parse()?;
        let expected_property_object: u32 = fields[4].parse()?;
        let tag = parse_tag(fields[5]).map_err(std::io::Error::other)?;
        let global_property_start: u64 = fields[6].parse()?;
        let global_payload_start: u64 = fields[7].parse()?;
        let global_payload_end: u64 = fields[8].parse()?;
        let global_next_start: u64 = fields[9].parse()?;
        let global_next_end: u64 = fields[10].parse()?;
        let expected_next = match fields[11] {
            "0" => false,
            "1" => true,
            other => return Err(format!("invalid next-property bit: {other}").into()),
        };
        let window_byte_start: u64 = fields[12].parse()?;
        let local_property_start: u64 = fields[13].parse()?;
        let window = parse_hex(fields[14]).map_err(std::io::Error::other)?;
        let expected_lossless = fields[15];

        let replay_bytes = fs::read(Path::new(replay_path))?;
        let input = ReplayInput::Memory {
            label: replay_path.to_owned(),
            bytes: replay_bytes,
        };
        let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;

        let decoded = decode_replay_network_existing_actor_single_primitive_property_v1(
            &window,
            local_property_start,
            actor_object,
            &plan,
        )?;
        if decoded.header.stream_id != Some(expected_stream) {
            return Err(format!("{class}: stream mismatch").into());
        }
        if decoded.header.resolved_property_object_index != Some(expected_property_object) {
            return Err(format!("{class}: property object mismatch").into());
        }
        if decoded.header.resolved_attribute_tag != Some(tag) {
            return Err(format!("{class}: tag mismatch").into());
        }
        if lossless(&decoded.scalar.value) != expected_lossless {
            return Err(format!("{class}: scalar semantic mismatch").into());
        }

        let base_bit = window_byte_start
            .checked_mul(8)
            .ok_or("window base overflow")?;
        if base_bit + decoded.header.property_present_start_bit != global_property_start {
            return Err(format!("{class}: property start mismatch").into());
        }
        let payload_start = decoded.header.payload_start_bit.ok_or("missing payload start")?;
        if base_bit + payload_start != global_payload_start {
            return Err(format!("{class}: payload start mismatch").into());
        }
        if decoded.header.stop_bit != payload_start {
            return Err(format!("{class}: header stop mismatch").into());
        }
        if base_bit + decoded.scalar.payload_end_bit != global_payload_end {
            return Err(format!("{class}: payload end mismatch").into());
        }
        if decoded.stop_bit != decoded.scalar.payload_end_bit {
            return Err(format!("{class}: wrapper stop mismatch").into());
        }
        if global_payload_end != global_next_start {
            return Err(format!("{class}: oracle payload end != next-property start").into());
        }
        if base_bit + decoded.stop_bit != global_next_start {
            return Err(format!("{class}: native stop != next-property start").into());
        }
        if global_next_end != global_next_start + 1 {
            return Err(format!("{class}: next-property width != 1").into());
        }

        let total_bits = u64::try_from(window.len())?
            .checked_mul(8)
            .ok_or("window bit length overflow")?;
        let mut next_cursor = decoded.stop_bit;
        let next_value = read_one_bit(&window, &mut next_cursor, total_bits)
            .map_err(std::io::Error::other)?;
        if next_value != expected_next {
            return Err(format!("{class}: next-property value mismatch").into());
        }
        if base_bit + next_cursor != global_next_end {
            return Err(format!("{class}: one-bit stop mismatch").into());
        }

        let truncated_start = decoded.stop_bit;
        let mut truncated_cursor = truncated_start;
        if read_one_bit(&window, &mut truncated_cursor, truncated_start).is_ok() {
            return Err(format!("{class}: bit-limit truncation unexpectedly succeeded").into());
        }
        if truncated_cursor != truncated_start {
            return Err(format!("{class}: truncation advanced cursor").into());
        }

        let evidence_stop = next_cursor;
        let mut poisoned = window.clone();
        for offset in 0..8u64 {
            let bit = evidence_stop.checked_add(offset).ok_or("poison offset overflow")?;
            set_bit(&mut poisoned, bit, offset % 2 == 0).map_err(std::io::Error::other)?;
        }
        let poisoned_decoded = decode_replay_network_existing_actor_single_primitive_property_v1(
            &poisoned,
            local_property_start,
            actor_object,
            &plan,
        )?;
        if poisoned_decoded != decoded {
            return Err(format!("{class}: post-stop poison changed first-property decode").into());
        }
        let poisoned_limit = u64::try_from(poisoned.len())?
            .checked_mul(8)
            .ok_or("poisoned bit length overflow")?;
        let mut poisoned_cursor = poisoned_decoded.stop_bit;
        let poisoned_next = read_one_bit(&poisoned, &mut poisoned_cursor, poisoned_limit)
            .map_err(std::io::Error::other)?;
        if poisoned_next != next_value || poisoned_cursor != evidence_stop {
            return Err(format!("{class}: post-stop poison changed one-bit evidence").into());
        }

        let class_expected = if expected_next { "continuation" } else { "terminator" };
        if class != class_expected {
            return Err(format!("{class}: class/value mismatch").into());
        }

        println!(
            "R3_18C_NATIVE\tclass={}\theader_exact=true\tsemantic_exact=true\tpayload_start_exact=true\tpayload_end_exact=true\tstop_equals_next_start=true\tnext_bit_exact=true\tone_bit_stop_exact=true\ttruncation_negative=true\ttruncation_cursor_unchanged=true\tpost_stop_poison=true\tsecond_stream_bits_consumed=0\tsecond_payload_bits_consumed=0\tattribute_tag={:?}\tlossless_value={}\tnative_global_stop={}\tevidence_global_stop={}\tnext_property_present={}",
            class,
            decoded.scalar.attribute_tag,
            lossless(&decoded.scalar.value),
            base_bit + decoded.stop_bit,
            base_bit + evidence_stop,
            if next_value { 1 } else { 0 },
        );
    }

    if row_count == 0 {
        return Err("empty R3.18C request".into());
    }
    println!("R3_18C_NATIVE_ROWS={row_count}");
    Ok(())
}
