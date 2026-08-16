use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_existing_actor_after_first_primitive_property_control_v1,
    decode_replay_network_existing_actor_first_property_header_v1,
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
        _ => Err(format!("unsupported first K1 tag: {text}")),
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
    let needed_bytes_u64 = needed_bits
        .checked_add(7)
        .ok_or_else(|| "poison length overflow".to_owned())?
        / 8;
    let needed_bytes = usize::try_from(needed_bytes_u64)
        .map_err(|_| "poison length conversion overflow".to_owned())?;
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

fn option_u32(value: Option<u32>) -> String {
    value.map_or_else(|| "None".to_owned(), |x| x.to_string())
}

fn option_u64(value: Option<u64>) -> String {
    value.map_or_else(|| "None".to_owned(), |x| x.to_string())
}

fn option_tag(value: Option<ReplayNetworkAttributeTagV1>) -> String {
    value.map_or_else(|| "None".to_owned(), |x| format!("{x:?}"))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args_os().skip(1);
    let request_path = args.next().ok_or("missing request TSV")?;
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }
    let request = fs::read_to_string(request_path)?;
    let mut row_count = 0usize;
    let mut header_truncation_rows = 0usize;

    for line in request.lines().filter(|line| !line.trim().is_empty()) {
        row_count += 1;
        let fields: Vec<&str> = line.split('\t').collect();
        if fields.len() != 26 {
            return Err(format!("expected 26 TSV fields, got {}", fields.len()).into());
        }
        let class = fields[0];
        let replay_path = fields[1];
        let actor_object: u32 = fields[2].parse()?;
        let expected_first_stream: u32 = fields[3].parse()?;
        let expected_first_property_object: u32 = fields[4].parse()?;
        let first_tag = parse_tag(fields[5]).map_err(std::io::Error::other)?;
        let global_first_property_start: u64 = fields[6].parse()?;
        let global_first_payload_start: u64 = fields[7].parse()?;
        let global_first_payload_end: u64 = fields[8].parse()?;
        let global_second_present_start: u64 = fields[9].parse()?;
        let global_second_present_end: u64 = fields[10].parse()?;
        let expected_next = match fields[11] {
            "0" => false,
            "1" => true,
            other => return Err(format!("invalid second property_present: {other}").into()),
        };
        let window_byte_start: u64 = fields[12].parse()?;
        let local_first_start: u64 = fields[13].parse()?;
        let window = parse_hex(fields[14]).map_err(std::io::Error::other)?;
        let expected_first_lossless = fields[15];

        let expected_second_property_start: i64 = fields[16].parse()?;
        let expected_second_property_end: i64 = fields[17].parse()?;
        let expected_second_stream_start: i64 = fields[18].parse()?;
        let expected_second_stream_end: i64 = fields[19].parse()?;
        let expected_second_stream: i64 = fields[20].parse()?;
        let expected_second_bound: i64 = fields[21].parse()?;
        let expected_second_prop_bits: i64 = fields[22].parse()?;
        let expected_second_property_object: i64 = fields[23].parse()?;
        let expected_second_tag = fields[24];
        let expected_second_payload_start: i64 = fields[25].parse()?;

        let replay_bytes = fs::read(Path::new(replay_path))?;
        let input = ReplayInput::Memory {
            label: replay_path.to_owned(),
            bytes: replay_bytes,
        };
        let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;

        let first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &window,
            local_first_start,
            actor_object,
            &plan,
        )?;
        if first.header.stream_id != Some(expected_first_stream)
            || first.header.resolved_property_object_index != Some(expected_first_property_object)
            || first.header.resolved_attribute_tag != Some(first_tag)
            || lossless(&first.scalar.value) != expected_first_lossless
        {
            return Err(format!("{replay_path} {class}: first-property reconstruction mismatch").into());
        }

        let base_bit = window_byte_start.checked_mul(8).ok_or("window base overflow")?;
        let first_payload_start = first.header.payload_start_bit.ok_or("missing first payload start")?;
        if base_bit + first.header.property_present_start_bit != global_first_property_start
            || base_bit + first_payload_start != global_first_payload_start
            || base_bit + first.scalar.payload_end_bit != global_first_payload_end
            || base_bit + first.stop_bit != global_second_present_start
        {
            return Err(format!("{replay_path} {class}: first-property bit boundary mismatch").into());
        }

        let control = decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
            &window,
            &first,
        )?;
        if control.next_property_present != expected_next
            || base_bit + control.property_present_start_bit != global_second_present_start
            || base_bit + control.property_present_end_bit != global_second_present_end
            || control.stop_bit != control.property_present_end_bit
        {
            return Err(format!("{replay_path} {class}: R3.18D control reconstruction mismatch").into());
        }

        let second = decode_replay_network_existing_actor_first_property_header_v1(
            &window,
            control.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        if second.property_present != expected_next
            || second.property_present_start_bit != control.property_present_start_bit
            || second.property_present_end_bit != control.property_present_end_bit
        {
            return Err(format!("{replay_path} {class}: independent second property_present mismatch").into());
        }

        let repeated = decode_replay_network_existing_actor_first_property_header_v1(
            &window,
            control.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        if repeated != second {
            return Err(format!("{replay_path} {class}: second-header repeatability mismatch").into());
        }

        let mut poisoned = window.clone();
        for offset in 0..8u64 {
            let bit = second.stop_bit.checked_add(offset).ok_or("poison offset overflow")?;
            set_bit(&mut poisoned, bit, offset % 2 == 0).map_err(std::io::Error::other)?;
        }
        let poisoned_second = decode_replay_network_existing_actor_first_property_header_v1(
            &poisoned,
            control.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        if poisoned_second != second {
            return Err(format!("{replay_path} {class}: bits after second-header stop changed result").into());
        }

        let (
            second_stream_range_exact,
            second_stream_value_exact,
            second_stream_shape_exact,
            second_object_exact,
            second_tag_exact,
            second_payload_start_stop_exact,
            terminator_one_bit_stop_exact,
            terminator_optionals_none,
        ) = if expected_next {
            if class != "continuation" {
                return Err(format!("{replay_path}: true control classified as {class}").into());
            }
            let stream_start = second.stream_id_start_bit.ok_or("missing second stream start")?;
            let stream_end = second.stream_id_end_bit.ok_or("missing second stream end")?;
            let stream_id = second.stream_id.ok_or("missing second stream id")?;
            let stream_bound = second.stream_id_bound.ok_or("missing second stream bound")?;
            let prop_bits = second.prop_id_bits.ok_or("missing second prop bits")?;
            let property_object = second
                .resolved_property_object_index
                .ok_or("missing second property object")?;
            let tag = second.resolved_attribute_tag.ok_or("missing second attribute tag")?;
            let payload_start = second.payload_start_bit.ok_or("missing second payload start")?;

            if expected_second_property_start < 0
                || expected_second_property_end < 0
                || expected_second_stream_start < 0
                || expected_second_stream_end < 0
                || expected_second_stream < 0
                || expected_second_bound < 0
                || expected_second_prop_bits < 0
                || expected_second_property_object < 0
                || expected_second_payload_start < 0
            {
                return Err(format!("{replay_path}: missing continuation expectations").into());
            }

            let property_exact = base_bit + second.property_present_start_bit
                == u64::try_from(expected_second_property_start)?
                && base_bit + second.property_present_end_bit
                    == u64::try_from(expected_second_property_end)?;
            if !property_exact {
                return Err(format!("{replay_path}: continuation property_present coordinate mismatch").into());
            }

            let range_exact = base_bit + stream_start == u64::try_from(expected_second_stream_start)?
                && base_bit + stream_end == u64::try_from(expected_second_stream_end)?;
            let value_exact = u64::from(stream_id) == u64::try_from(expected_second_stream)?;
            let shape_exact = u64::from(stream_bound) == u64::try_from(expected_second_bound)?
                && u64::from(prop_bits) == u64::try_from(expected_second_prop_bits)?;
            let object_exact = u64::from(property_object)
                == u64::try_from(expected_second_property_object)?;
            let tag_exact = format!("{tag:?}") == expected_second_tag;
            let payload_exact = base_bit + payload_start
                == u64::try_from(expected_second_payload_start)?
                && second.stop_bit == payload_start;
            if !(range_exact && value_exact && shape_exact && object_exact && tag_exact && payload_exact) {
                return Err(format!("{replay_path}: continuation second-header mismatch").into());
            }

            let next_byte_boundary = ((stream_start / 8) + 1) * 8;
            if stream_start < next_byte_boundary && next_byte_boundary < stream_end {
                let byte_len = usize::try_from(next_byte_boundary / 8)?;
                if byte_len > window.len() {
                    return Err("second-header truncation exceeds window".into());
                }
                let truncated = window[..byte_len].to_vec();
                let error = decode_replay_network_existing_actor_first_property_header_v1(
                    &truncated,
                    control.property_present_start_bit,
                    actor_object,
                    &plan,
                )
                .expect_err("truncation inside second stream id must fail closed");
                if !error.to_string().contains("insufficient-bits") {
                    return Err(format!("{replay_path}: second-header truncation wrong error").into());
                }
                header_truncation_rows += 1;
            }

            (true, true, true, true, true, true, true, true)
        } else {
            if class != "terminator" {
                return Err(format!("{replay_path}: false control classified as {class}").into());
            }
            if second.stop_bit != second.property_present_end_bit {
                return Err(format!("{replay_path}: terminator stop != one-bit end").into());
            }
            let none = second.stream_id_bound.is_none()
                && second.prop_id_bits.is_none()
                && second.stream_id_start_bit.is_none()
                && second.stream_id_end_bit.is_none()
                && second.stream_id.is_none()
                && second.resolved_property_object_index.is_none()
                && second.resolved_attribute_tag.is_none()
                && second.payload_start_bit.is_none();
            if !none {
                return Err(format!("{replay_path}: terminator exposed second-header fields").into());
            }
            (true, true, true, true, true, true, true, true)
        };

        println!(
            "R3_18F_NATIVE\tlabel={}\tclass={}\tfirst_reconstruction_exact=true\tcontrol_reconstruction_exact=true\tsecond_property_present_exact=true\tsecond_stream_range_exact={}\tsecond_stream_value_exact={}\tsecond_stream_shape_exact={}\tsecond_object_exact={}\tsecond_tag_exact={}\tsecond_payload_start_stop_exact={}\tterminator_one_bit_stop_exact={}\tterminator_optionals_none={}\trepeatability=true\tpost_stop_poison=true\tsecond_payload_bits_consumed=0\tthird_property_bits_consumed=0\tnative_second_property_present_start={}\tnative_second_property_present_end={}\tnative_second_stream_start={}\tnative_second_stream_end={}\tnative_second_stream_id={}\tnative_second_stream_bound={}\tnative_second_prop_id_bits={}\tnative_second_property_object={}\tnative_second_attribute_tag={}\tnative_second_payload_start={}\tnative_second_stop={}",
            replay_path.replace('\\', "/"),
            class,
            second_stream_range_exact,
            second_stream_value_exact,
            second_stream_shape_exact,
            second_object_exact,
            second_tag_exact,
            second_payload_start_stop_exact,
            terminator_one_bit_stop_exact,
            terminator_optionals_none,
            base_bit + second.property_present_start_bit,
            base_bit + second.property_present_end_bit,
            second.stream_id_start_bit.map(|x| (base_bit + x).to_string()).unwrap_or_else(|| "None".to_owned()),
            second.stream_id_end_bit.map(|x| (base_bit + x).to_string()).unwrap_or_else(|| "None".to_owned()),
            option_u32(second.stream_id),
            option_u32(second.stream_id_bound),
            second.prop_id_bits.map_or_else(|| "None".to_owned(), |x| x.to_string()),
            option_u32(second.resolved_property_object_index),
            option_tag(second.resolved_attribute_tag),
            second.payload_start_bit.map(|x| (base_bit + x).to_string()).unwrap_or_else(|| "None".to_owned()),
            base_bit + second.stop_bit,
        );
    }

    if row_count != 94 {
        return Err(format!("expected 94 R3.18F request rows, got {row_count}").into());
    }
    if header_truncation_rows == 0 {
        return Err("no real continuation witness crosses a byte boundary inside second stream id".into());
    }

    let sample_path = Path::new("external_fixtures/sample_001.replay");
    let sample_bytes = fs::read(sample_path)?;
    let sample_input = ReplayInput::Memory {
        label: "r318f_synthetic_header_negatives".to_owned(),
        bytes: sample_bytes,
    };
    let sample_plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&sample_input)?;
    let no_lookup = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x00],
        0,
        u32::MAX,
        &sample_plan,
    )?;
    if no_lookup.property_present
        || no_lookup.stop_bit != 1
        || no_lookup.stream_id.is_some()
        || no_lookup.resolved_property_object_index.is_some()
        || no_lookup.payload_start_bit.is_some()
    {
        return Err("false terminator unexpectedly performed lookup".into());
    }
    println!("R3_18F_TERMINATOR_NO_LOOKUP_SYNTHETIC=PASS");

    let mut unresolved_plan = sample_plan;
    let actor_lookup = unresolved_plan
        .object_lookups
        .get_mut(47)
        .and_then(Option::as_mut)
        .ok_or("sample_001 actor object 47 lookup missing")?;
    actor_lookup.properties.retain(|property| property.stream_id != 0);
    let unresolved_error = decode_replay_network_existing_actor_first_property_header_v1(
        &[0x01],
        0,
        47,
        &unresolved_plan,
    )
    .expect_err("synthetically unmapped stream zero must fail closed");
    if !unresolved_error.to_string().contains("unresolved-stream-id") {
        return Err("unresolved-stream synthetic produced wrong error".into());
    }
    println!("R3_18F_UNRESOLVED_STREAM_SYNTHETIC=PASS");
    println!("R3_18F_NATIVE_ROWS={row_count}");
    println!("R3_18F_HEADER_TRUNCATION_ROWS={header_truncation_rows}");
    Ok(())
}
