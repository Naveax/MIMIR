use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1,
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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args_os().skip(1);
    let request_path = args.next().ok_or("missing request TSV")?;
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }

    let request = fs::read_to_string(request_path)?;
    let mut row_count = 0usize;
    let mut terminator_rows = 0usize;
    let mut continuation_rows = 0usize;
    let mut terminator_no_lookup_rows = 0usize;
    let mut header_truncation_rows = 0usize;
    let mut unresolved_negative_done = false;
    let mut tag_negative_done = false;

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

        let composed =
            decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                &window,
                &first,
                &plan,
            )?;
        if composed.control.next_property_present != expected_next
            || base_bit + composed.control.property_present_start_bit != global_second_present_start
            || base_bit + composed.control.property_present_end_bit != global_second_present_end
            || composed.control.stop_bit != composed.control.property_present_end_bit
        {
            return Err(format!("{replay_path} {class}: production control mismatch").into());
        }

        let repeated =
            decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                &window,
                &first,
                &plan,
            )?;
        if repeated != composed {
            return Err(format!("{replay_path} {class}: production repeatability mismatch").into());
        }

        let mut poisoned = window.clone();
        for offset in 0..16u64 {
            let bit = composed.stop_bit.checked_add(offset).ok_or("poison offset overflow")?;
            set_bit(&mut poisoned, bit, offset % 2 == 0).map_err(std::io::Error::other)?;
        }
        let poisoned_result =
            decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                &poisoned,
                &first,
                &plan,
            )?;
        if poisoned_result != composed {
            return Err(format!("{replay_path} {class}: bits at/after production stop changed result").into());
        }

        let second_tag_out;
        let native_stop_global;
        if expected_next {
            continuation_rows += 1;
            if class != "continuation" {
                return Err(format!("{replay_path}: true control classified as {class}").into());
            }
            let second = composed.second_header.as_ref().ok_or("missing production second header")?;
            if !second.property_present || second.actor_object_index != actor_object {
                return Err(format!("{replay_path}: malformed production continuation header").into());
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
            if expected_second_tag != "Int" && expected_second_tag != "String" {
                return Err(format!("{replay_path}: frozen continuation tag outside Int/String: {expected_second_tag}").into());
            }

            let exact = base_bit + second.property_present_start_bit
                == u64::try_from(expected_second_property_start)?
                && base_bit + second.property_present_end_bit
                    == u64::try_from(expected_second_property_end)?
                && base_bit + stream_start == u64::try_from(expected_second_stream_start)?
                && base_bit + stream_end == u64::try_from(expected_second_stream_end)?
                && u64::from(stream_id) == u64::try_from(expected_second_stream)?
                && u64::from(stream_bound) == u64::try_from(expected_second_bound)?
                && u64::from(prop_bits) == u64::try_from(expected_second_prop_bits)?
                && u64::from(property_object) == u64::try_from(expected_second_property_object)?
                && format!("{tag:?}") == expected_second_tag
                && base_bit + payload_start == u64::try_from(expected_second_payload_start)?
                && second.stop_bit == payload_start
                && composed.stop_bit == payload_start;
            if !exact {
                return Err(format!("{replay_path}: published R3.18G continuation mismatch").into());
            }

            let next_byte_boundary = ((stream_start / 8) + 1) * 8;
            if stream_start < next_byte_boundary && next_byte_boundary < stream_end {
                let byte_len = usize::try_from(next_byte_boundary / 8)?;
                if byte_len > window.len() {
                    return Err("second-header truncation exceeds window".into());
                }
                let truncated = window[..byte_len].to_vec();
                let error = decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                    &truncated,
                    &first,
                    &plan,
                )
                .expect_err("truncation inside production second stream id must fail closed");
                if !error.to_string().contains("insufficient-bits") {
                    return Err(format!("{replay_path}: production truncation wrong error").into());
                }
                header_truncation_rows += 1;
            }

            if !unresolved_negative_done {
                let mut unresolved_plan = plan.clone();
                let lookup = unresolved_plan
                    .object_lookups
                    .get_mut(usize::try_from(actor_object)?)
                    .and_then(Option::as_mut)
                    .ok_or("continuation actor lookup missing for unresolved negative")?;
                lookup.properties.retain(|property| property.stream_id != stream_id);
                let error = decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                    &window,
                    &first,
                    &unresolved_plan,
                )
                .expect_err("unresolved production second stream must fail closed");
                if !error.to_string().contains("unresolved-stream-id") {
                    return Err("unresolved production negative produced wrong error".into());
                }
                unresolved_negative_done = true;
            }

            if !tag_negative_done {
                let mut retagged_plan = plan.clone();
                let lookup = retagged_plan
                    .object_lookups
                    .get_mut(usize::try_from(actor_object)?)
                    .and_then(Option::as_mut)
                    .ok_or("continuation actor lookup missing for tag negative")?;
                let property = lookup
                    .properties
                    .iter_mut()
                    .find(|property| property.stream_id == stream_id)
                    .ok_or("continuation property missing for tag negative")?;
                property.tag = ReplayNetworkAttributeTagV1::Float;
                let error = decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                    &window,
                    &first,
                    &retagged_plan,
                )
                .expect_err("Float production second-header context must reject");
                if !error.to_string().contains("unsupported-second-header-tag") {
                    return Err("production tag negative produced wrong error".into());
                }
                tag_negative_done = true;
            }

            second_tag_out = format!("{tag:?}");
            native_stop_global = base_bit + composed.stop_bit;
        } else {
            terminator_rows += 1;
            if class != "terminator" {
                return Err(format!("{replay_path}: false control classified as {class}").into());
            }
            if composed.second_header.is_some()
                || composed.stop_bit != composed.control.property_present_end_bit
                || base_bit + composed.stop_bit != global_second_present_end
            {
                return Err(format!("{replay_path}: published terminator boundary mismatch").into());
            }

            let mut poison_plan = plan.clone();
            let slot = poison_plan
                .object_lookups
                .get_mut(usize::try_from(actor_object)?)
                .ok_or("terminator actor lookup index missing")?;
            *slot = None;
            let no_lookup =
                decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                    &window,
                    &first,
                    &poison_plan,
                )?;
            if no_lookup.control.next_property_present
                || no_lookup.second_header.is_some()
                || no_lookup.stop_bit != composed.stop_bit
            {
                return Err(format!("{replay_path}: terminator performed lookup after false control").into());
            }
            terminator_no_lookup_rows += 1;
            second_tag_out = "None".to_owned();
            native_stop_global = base_bit + composed.stop_bit;
        }

        println!(
            "R3_18H_NATIVE\tlabel={}\tclass={}\tfirst_exact=true\tcontrol_exact=true\tsecond_header_exact=true\trepeatability=true\tpost_stop_poison=true\tsecond_attribute_tag={}\tsecond_payload_bits_consumed=0\tthird_property_bits_consumed=0\tnative_stop_global={}",
            replay_path.replace('\\', "/"),
            class,
            second_tag_out,
            native_stop_global,
        );
    }

    if row_count != 94 || terminator_rows != 47 || continuation_rows != 47 {
        return Err(format!(
            "expected 94 rows as 47/47, got rows={row_count} terminator={terminator_rows} continuation={continuation_rows}"
        )
        .into());
    }
    if terminator_no_lookup_rows != 47 {
        return Err(format!("expected 47 terminator no-lookup proofs, got {terminator_no_lookup_rows}").into());
    }
    if header_truncation_rows != 32 {
        return Err(format!("expected frozen 32 real header truncation rows, got {header_truncation_rows}").into());
    }
    if !unresolved_negative_done || !tag_negative_done {
        return Err("required production synthetic negatives did not execute".into());
    }

    println!("R3_18H_NATIVE_ROWS={row_count}");
    println!("R3_18H_TERMINATOR_ROWS={terminator_rows}");
    println!("R3_18H_CONTINUATION_ROWS={continuation_rows}");
    println!("R3_18H_TERMINATOR_NO_LOOKUP_ROWS={terminator_no_lookup_rows}");
    println!("R3_18H_HEADER_TRUNCATION_ROWS={header_truncation_rows}");
    println!("R3_18H_UNRESOLVED_STREAM_NEGATIVE=PASS");
    println!("R3_18H_TAG_OUTSIDE_INT_STRING_NEGATIVE=PASS");
    println!("R3_18H_SECOND_PAYLOAD_BITS_CONSUMED=0");
    println!("R3_18H_THIRD_PROPERTY_BITS_CONSUMED=0");
    Ok(())
}
