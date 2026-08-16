use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_existing_actor_after_first_primitive_property_control_v1,
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
        .map(|offset| {
            u8::from_str_radix(&text[offset..offset + 2], 16).map_err(|error| error.to_string())
        })
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
        _ => Err(format!("unsupported R3.18E K1 tag: {text}")),
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
    let mut aligned_truncation_rows = 0usize;

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
        let global_control_start: u64 = fields[9].parse()?;
        let global_control_end: u64 = fields[10].parse()?;
        let expected_next = match fields[11] {
            "0" => false,
            "1" => true,
            other => return Err(format!("invalid control bit: {other}").into()),
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

        let first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &window,
            local_property_start,
            actor_object,
            &plan,
        )?;
        if first.header.stream_id != Some(expected_stream) {
            return Err(format!("{replay_path} {class}: stream mismatch").into());
        }
        if first.header.resolved_property_object_index != Some(expected_property_object) {
            return Err(format!("{replay_path} {class}: property object mismatch").into());
        }
        if first.header.resolved_attribute_tag != Some(tag) {
            return Err(format!("{replay_path} {class}: tag mismatch").into());
        }
        if lossless(&first.scalar.value) != expected_lossless {
            return Err(format!("{replay_path} {class}: scalar semantic mismatch").into());
        }

        let base_bit = window_byte_start.checked_mul(8).ok_or("window base overflow")?;
        if base_bit + first.header.property_present_start_bit != global_property_start {
            return Err(format!("{replay_path} {class}: property start mismatch").into());
        }
        let payload_start = first.header.payload_start_bit.ok_or("missing payload start")?;
        if base_bit + payload_start != global_payload_start {
            return Err(format!("{replay_path} {class}: payload start mismatch").into());
        }
        if base_bit + first.scalar.payload_end_bit != global_payload_end {
            return Err(format!("{replay_path} {class}: payload end mismatch").into());
        }
        if first.stop_bit != first.scalar.payload_end_bit || global_payload_end != global_control_start {
            return Err(format!("{replay_path} {class}: first stop mismatch").into());
        }
        if base_bit + first.stop_bit != global_control_start {
            return Err(format!("{replay_path} {class}: native first stop != oracle control start").into());
        }
        if global_control_end != global_control_start + 1 {
            return Err(format!("{replay_path} {class}: oracle control width != 1").into());
        }

        let control = decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
            &window,
            &first,
        )?;
        if control.property_present_start_bit != first.stop_bit {
            return Err(format!("{replay_path} {class}: control start != first stop").into());
        }
        if control.next_property_present != expected_next {
            return Err(format!("{replay_path} {class}: control value mismatch").into());
        }
        if base_bit + control.property_present_start_bit != global_control_start
            || base_bit + control.property_present_end_bit != global_control_end
            || control.stop_bit != control.property_present_end_bit
        {
            return Err(format!("{replay_path} {class}: control end/stop mismatch").into());
        }

        let repeated = decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
            &window,
            &first,
        )?;
        if repeated != control {
            return Err(format!("{replay_path} {class}: repeatability mismatch").into());
        }

        let mut poisoned = window.clone();
        for offset in 0..8u64 {
            let bit = control.stop_bit.checked_add(offset).ok_or("poison offset overflow")?;
            set_bit(&mut poisoned, bit, offset % 2 == 0).map_err(std::io::Error::other)?;
        }
        let poisoned_first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &poisoned,
            local_property_start,
            actor_object,
            &plan,
        )?;
        let poisoned_control =
            decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
                &poisoned,
                &poisoned_first,
            )?;
        if poisoned_first != first || poisoned_control != control {
            return Err(format!("{replay_path} {class}: post-stop poison changed result").into());
        }

        let mut malformed_first = first.clone();
        malformed_first.stop_bit = malformed_first.stop_bit.checked_add(1).ok_or("malformed overflow")?;
        let malformed_error =
            decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
                &window,
                &malformed_first,
            )
            .expect_err("malformed first-property boundary must reject");
        if !malformed_error.to_string().contains("boundary-mismatch") {
            return Err(format!("{replay_path} {class}: malformed boundary wrong error").into());
        }

        if first.stop_bit % 8 == 0 {
            let byte_len = usize::try_from(first.stop_bit / 8)?;
            if byte_len > window.len() {
                return Err("aligned truncation exceeds window".into());
            }
            let truncated = window[..byte_len].to_vec();
            let truncation_error =
                decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
                    &truncated,
                    &first,
                )
                .expect_err("exactly missing control bit must reject");
            if !truncation_error.to_string().contains("insufficient-bits") {
                return Err(format!("{replay_path} {class}: truncation wrong error").into());
            }
            aligned_truncation_rows += 1;
        }

        let class_expected = if expected_next { "continuation" } else { "terminator" };
        if class != class_expected {
            return Err(format!("{replay_path} {class}: class/value mismatch").into());
        }

        println!(
            "R3_18E_NATIVE\tlabel={}\tclass={}\tfirst_header_exact=true\tfirst_semantic_exact=true\tfirst_payload_start_exact=true\tfirst_payload_end_exact=true\tfirst_stop_equals_oracle_control_start=true\tcontrol_start_exact=true\tcontrol_value_exact=true\tcontrol_end_exact=true\tcontrol_stop_exact=true\trepeatability=true\tpost_stop_poison=true\tmalformed_first_rejected=true\tsecond_stream_bits_consumed=0\tsecond_header_bits_consumed=0\tsecond_payload_bits_consumed=0\tattribute_tag={:?}\tlossless_value={}\tnative_global_first_stop={}\tnative_global_control_start={}\tnative_global_control_end={}\tnext_property_present={}",
            replay_path.replace('\\', "/"),
            class,
            first.scalar.attribute_tag,
            lossless(&first.scalar.value),
            base_bit + first.stop_bit,
            base_bit + control.property_present_start_bit,
            base_bit + control.property_present_end_bit,
            if control.next_property_present { 1 } else { 0 },
        );
    }

    if row_count != 94 {
        return Err(format!("expected 94 R3.18E request rows, got {row_count}").into());
    }
    if aligned_truncation_rows == 0 {
        return Err("no byte-aligned witness for exact truncation negative".into());
    }
    println!("R3_18E_NATIVE_ROWS={row_count}");
    println!("R3_18E_ALIGNED_TRUNCATION_ROWS={aligned_truncation_rows}");
    Ok(())
}
