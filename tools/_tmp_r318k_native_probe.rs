use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader, ReplayContentScaffoldReader,
    ReplayInput, ReplayNetworkAttributeTagV1, ReplayNetworkExistingActorSecondPropertyPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1, ReplayNetworkPrimitiveScalarValueV1, ReplayNetworkTextEncodingV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::env;
use std::fs;
use std::path::Path;

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

fn scalar_lossless(value: &ReplayNetworkPrimitiveScalarValueV1) -> String {
    match value {
        ReplayNetworkPrimitiveScalarValueV1::Boolean(value) => {
            if *value { "1" } else { "0" }.to_owned()
        }
        ReplayNetworkPrimitiveScalarValueV1::Byte(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Enum(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Float { raw_bits, .. } => raw_bits.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int64(value) => value.to_string(),
    }
}

fn read_bits_le(bytes: &[u8], start: u64, width: usize) -> Result<u64, String> {
    if width > 64 {
        return Err("width > 64".to_owned());
    }
    let start = usize::try_from(start).map_err(|_| "start conversion")?;
    let end = start.checked_add(width).ok_or("end overflow")?;
    let total = bytes.len().checked_mul(8).ok_or("length overflow")?;
    if end > total {
        return Err(format!("insufficient independent wire bits: {start}+{width}>{total}"));
    }
    let mut out = 0u64;
    for offset in 0..width {
        let pos = start + offset;
        out |= u64::from((bytes[pos / 8] >> (pos % 8)) & 1) << offset;
    }
    Ok(out)
}

fn set_bit(bytes: &mut Vec<u8>, position: u64, value: bool) -> Result<(), String> {
    let pos = usize::try_from(position).map_err(|_| "bit conversion")?;
    let needed = pos / 8 + 1;
    if bytes.len() < needed {
        bytes.resize(needed, 0);
    }
    if value {
        bytes[pos / 8] |= 1 << (pos % 8);
    } else {
        bytes[pos / 8] &= !(1 << (pos % 8));
    }
    Ok(())
}

fn windows1252(bytes: &[u8]) -> String {
    let mut output = String::with_capacity(bytes.len());
    for byte in bytes {
        let code = match *byte {
            0x80 => 0x20ac,
            0x81 => 0x0081,
            0x82 => 0x201a,
            0x83 => 0x0192,
            0x84 => 0x201e,
            0x85 => 0x2026,
            0x86 => 0x2020,
            0x87 => 0x2021,
            0x88 => 0x02c6,
            0x89 => 0x2030,
            0x8a => 0x0160,
            0x8b => 0x2039,
            0x8c => 0x0152,
            0x8d => 0x008d,
            0x8e => 0x017d,
            0x8f => 0x008f,
            0x90 => 0x0090,
            0x91 => 0x2018,
            0x92 => 0x2019,
            0x93 => 0x201c,
            0x94 => 0x201d,
            0x95 => 0x2022,
            0x96 => 0x2013,
            0x97 => 0x2014,
            0x98 => 0x02dc,
            0x99 => 0x2122,
            0x9a => 0x0161,
            0x9b => 0x203a,
            0x9c => 0x0153,
            0x9d => 0x009d,
            0x9e => 0x017e,
            0x9f => 0x0178,
            other => u32::from(other),
        };
        output.push(char::from_u32(code).expect("valid Windows-1252 mapping"));
    }
    output
}

fn retag(
    plan: &mut ReplayNetworkLookupPlanV1,
    actor_object: usize,
    stream_id: u32,
    tag: ReplayNetworkAttributeTagV1,
) -> Result<(), String> {
    let lookup = plan
        .object_lookups
        .get_mut(actor_object)
        .ok_or("actor lookup index out of range")?
        .as_mut()
        .ok_or("actor lookup missing")?;
    let property = lookup
        .properties
        .iter_mut()
        .find(|property| property.stream_id == stream_id)
        .ok_or("stream missing for retag")?;
    property.tag = tag;
    Ok(())
}

fn parse_u64(f: &[&str], index: usize) -> Result<u64, Box<dyn std::error::Error>> {
    Ok(f[index].parse()?)
}

fn parse_i64(f: &[&str], index: usize) -> Result<i64, Box<dyn std::error::Error>> {
    Ok(f[index].parse()?)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let request_path = env::args_os().nth(1).ok_or("missing request TSV")?;
    if env::args_os().nth(2).is_some() {
        return Err("unexpected extra argument".into());
    }
    let request = fs::read_to_string(request_path)?;

    let mut rows = 0usize;
    let mut terminators = 0usize;
    let mut continuations = 0usize;
    let mut ints = 0usize;
    let mut strings = 0usize;
    let mut no_lookup_rows = 0usize;
    let mut truncation_rows = 0usize;
    let mut mismatch = 0usize;
    let mut repeatability_all = true;
    let mut poison_all = true;
    let mut string_wrong_context = false;
    let mut tag_outside = false;

    for line in request.lines().filter(|line| !line.trim().is_empty()) {
        rows += 1;
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 28 {
            return Err(format!("expected 28 fields, got {}", f.len()).into());
        }
        let class = f[0];
        let label = f[1];
        let actor_object: u32 = f[2].parse()?;
        let first_tag = parse_tag(f[3]).map_err(std::io::Error::other)?;
        let first_lossless = f[4];
        let first_present_start = parse_u64(&f, 5)?;
        let first_present_end = parse_u64(&f, 6)?;
        let first_stream_start = parse_u64(&f, 7)?;
        let first_stream_end = parse_u64(&f, 8)?;
        let first_stream_id: u32 = f[9].parse()?;
        let first_property_object: u32 = f[10].parse()?;
        let first_payload_start = parse_u64(&f, 11)?;
        let first_payload_end = parse_u64(&f, 12)?;
        let second_present_start = parse_u64(&f, 13)?;
        let second_present_end = parse_u64(&f, 14)?;
        let next_present = match f[15] {
            "0" => false,
            "1" => true,
            value => return Err(format!("invalid next-present bit {value}").into()),
        };
        let second_stream_start = parse_i64(&f, 16)?;
        let second_stream_end = parse_i64(&f, 17)?;
        let second_stream_id = parse_i64(&f, 18)?;
        let second_bound = parse_i64(&f, 19)?;
        let second_prop_bits = parse_i64(&f, 20)?;
        let second_object = parse_i64(&f, 21)?;
        let second_tag = f[22];
        let second_payload_start = parse_i64(&f, 23)?;
        let expected_payload_end = parse_i64(&f, 24)?;
        let expected_payload_width: u64 = f[25].parse()?;
        let _frame_index: u64 = f[26].parse()?;
        let _actor_ordinal: u64 = f[27].parse()?;

        let replay_bytes = fs::read(Path::new(label))?;
        let input = ReplayInput::Memory {
            label: label.to_owned(),
            bytes: replay_bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader.read_content_scaffold(&input)?;
        let network_start = usize::try_from(scaffold.network_start)?;
        let network_end = usize::try_from(scaffold.network_end)?;
        if network_start > network_end || network_end > replay_bytes.len() {
            return Err(format!("{label}: invalid network slice").into());
        }
        let network = &replay_bytes[network_start..network_end];
        let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;

        let base_byte = usize::try_from(first_present_start / 8)?;
        let needed_global = if next_present {
            u64::try_from(expected_payload_end)?
        } else {
            second_present_end
        };
        let padded_global = needed_global.checked_add(16).ok_or("padding overflow")?;
        let end_byte_u64 = padded_global.checked_add(7).ok_or("ceil overflow")? / 8;
        let end_byte = usize::try_from(end_byte_u64)?.min(network.len());
        if base_byte >= end_byte || end_byte > network.len() {
            return Err(format!("{label}: invalid witness window").into());
        }
        let window = network[base_byte..end_byte].to_vec();
        let base_bit = u64::try_from(base_byte)?.checked_mul(8).ok_or("base overflow")?;
        let local_first_start = first_present_start.checked_sub(base_bit).ok_or("first before base")?;

        let first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &window,
            local_first_start,
            actor_object,
            &plan,
        )?;
        let first_header = &first.header;
        let first_exact = base_bit + first_header.property_present_start_bit == first_present_start
            && base_bit + first_header.property_present_end_bit == first_present_end
            && base_bit + first_header.stream_id_start_bit.ok_or("first stream start missing")? == first_stream_start
            && base_bit + first_header.stream_id_end_bit.ok_or("first stream end missing")? == first_stream_end
            && first_header.stream_id == Some(first_stream_id)
            && first_header.resolved_property_object_index == Some(first_property_object)
            && first_header.resolved_attribute_tag == Some(first_tag)
            && base_bit + first_header.payload_start_bit.ok_or("first payload start missing")? == first_payload_start
            && base_bit + first.scalar.payload_end_bit == first_payload_end
            && scalar_lossless(&first.scalar.value) == first_lossless
            && base_bit + first.stop_bit == second_present_start;
        if !first_exact {
            return Err(format!("{label} {class}: first property reconstruction mismatch").into());
        }

        let ctx = ReplayNetworkK2DecodeContextV1 {
            net_version: 10,
            is_rl_223: false,
        };
        let decoded =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                &window,
                &first,
                &plan,
                ctx,
            )?;
        let repeated =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                &window,
                &first,
                &plan,
                ctx,
            )?;
        let repeatability = decoded == repeated;
        repeatability_all &= repeatability;

        let control = &decoded.header_composition.control;
        let control_exact = control.next_property_present == next_present
            && base_bit + control.property_present_start_bit == second_present_start
            && base_bit + control.property_present_end_bit == second_present_end;
        if !control_exact {
            return Err(format!("{label} {class}: control mismatch").into());
        }

        let mut reconstruction_exact = true;
        let mut semantic_exact = true;
        let mut shape_exact = true;
        let mut stop_exact = true;
        let mut truncation = true;
        let mut terminator_no_lookup = false;
        let payload_start_out: i64;
        let payload_end_out: i64;
        let payload_width_out: u64;
        let tag_out: &str;

        if !next_present {
            terminators += 1;
            if class != "terminator"
                || decoded.header_composition.second_header.is_some()
                || decoded.second_payload.is_some()
            {
                return Err(format!("{label}: terminator unexpectedly returned second data").into());
            }
            stop_exact = base_bit + decoded.stop_bit == second_present_end;
            payload_start_out = -1;
            payload_end_out = -1;
            payload_width_out = 0;
            tag_out = "None";

            let mut poison_plan = plan.clone();
            let slot = poison_plan
                .object_lookups
                .get_mut(usize::try_from(actor_object)?)
                .ok_or("terminator actor lookup index missing")?;
            *slot = None;
            let no_lookup =
                decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                    &window,
                    &first,
                    &poison_plan,
                    ctx,
                )?;
            terminator_no_lookup = no_lookup == decoded;
            if terminator_no_lookup {
                no_lookup_rows += 1;
            }
        } else {
            continuations += 1;
            if class != "continuation" {
                return Err(format!("{label}: continuation class mismatch").into());
            }
            let header = decoded
                .header_composition
                .second_header
                .as_ref()
                .ok_or("continuation missing second header")?;
            reconstruction_exact = base_bit + header.property_present_start_bit == second_present_start
                && base_bit + header.property_present_end_bit == second_present_end
                && base_bit + header.stream_id_start_bit.ok_or("second stream start missing")?
                    == u64::try_from(second_stream_start)?
                && base_bit + header.stream_id_end_bit.ok_or("second stream end missing")?
                    == u64::try_from(second_stream_end)?
                && i64::from(header.stream_id.ok_or("second stream missing")?) == second_stream_id
                && i64::from(header.stream_id_bound.ok_or("second bound missing")?) == second_bound
                && i64::from(header.prop_id_bits.ok_or("second prop bits missing")?) == second_prop_bits
                && i64::from(header.resolved_property_object_index.ok_or("second object missing")?)
                    == second_object
                && format!("{:?}", header.resolved_attribute_tag.ok_or("second tag missing")?) == second_tag
                && base_bit + header.payload_start_bit.ok_or("second payload start missing")?
                    == u64::try_from(second_payload_start)?;

            let local_payload_start = u64::try_from(second_payload_start)?
                .checked_sub(base_bit)
                .ok_or("second payload before base")?;
            let local_payload_end = u64::try_from(expected_payload_end)?
                .checked_sub(base_bit)
                .ok_or("payload end before base")?;
            payload_start_out = second_payload_start;
            payload_end_out = expected_payload_end;
            payload_width_out = expected_payload_width;
            tag_out = second_tag;

            match decoded.second_payload.as_ref().ok_or("continuation missing payload")? {
                ReplayNetworkExistingActorSecondPropertyPayloadV1::Int(value) => {
                    ints += 1;
                    if second_tag != "Int" {
                        return Err(format!("{label}: expected {second_tag}, got Int").into());
                    }
                    let wire_raw = read_bits_le(network, u64::try_from(second_payload_start)?, 32)? as u32;
                    let wire_value = wire_raw as i32;
                    semantic_exact = matches!(
                        value.value,
                        ReplayNetworkPrimitiveScalarValueV1::Int(actual) if actual == wire_value
                    );
                    shape_exact = value.payload_start_bit == local_payload_start
                        && value.payload_end_bit == local_payload_end
                        && u64::from(value.payload_width) == expected_payload_width
                        && expected_payload_width == 32;
                    stop_exact = value.stop_bit == local_payload_end
                        && decoded.stop_bit == local_payload_end
                        && base_bit + decoded.stop_bit == u64::try_from(expected_payload_end)?;
                }
                ReplayNetworkExistingActorSecondPropertyPayloadV1::String(value) => {
                    strings += 1;
                    if second_tag != "String" {
                        return Err(format!("{label}: expected {second_tag}, got String").into());
                    }
                    let declared_raw =
                        read_bits_le(network, u64::try_from(second_payload_start)?, 32)? as u32;
                    let declared = declared_raw as i32;
                    if declared != 7 || expected_payload_width != 88 {
                        return Err(format!("{label}: frozen String shape drift").into());
                    }
                    let mut content = Vec::with_capacity(6);
                    let mut bit = u64::try_from(second_payload_start)? + 32;
                    for _ in 0..6 {
                        content.push(read_bits_le(network, bit, 8)? as u8);
                        bit += 8;
                    }
                    let _terminator = read_bits_le(network, bit, 8)? as u8;
                    let wire_text = windows1252(&content);
                    match &value.value {
                        ReplayNetworkK2ValueV1::String(text) => {
                            semantic_exact = text.value == wire_text;
                            shape_exact = value.payload_start_bit == local_payload_start
                                && value.payload_end_bit == local_payload_end
                                && value.payload_width == expected_payload_width
                                && text.declared_length == 7
                                && text.encoding == ReplayNetworkTextEncodingV1::Windows1252;
                        }
                        _ => semantic_exact = false,
                    }
                    stop_exact = decoded.stop_bit == local_payload_end
                        && base_bit + decoded.stop_bit == u64::try_from(expected_payload_end)?;

                    let error =
                        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                            &window,
                            &first,
                            &plan,
                            ReplayNetworkK2DecodeContextV1 {
                                net_version: 10,
                                is_rl_223: true,
                            },
                        )
                        .expect_err("String wrong context must fail");
                    string_wrong_context =
                        error.to_string().contains("unsupported-second-string-context");
                }
            }

            let keep = usize::try_from(
                local_payload_end
                    .checked_add(7)
                    .ok_or("truncation ceil overflow")?
                    / 8,
            )?
            .saturating_sub(1);
            let truncated = window[..keep.min(window.len())].to_vec();
            truncation =
                decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                    &truncated,
                    &first,
                    &plan,
                    ctx,
                )
                .is_err();
            if truncation {
                truncation_rows += 1;
            }

            if !tag_outside && second_tag == "Int" {
                let mut bad_plan = plan.clone();
                retag(
                    &mut bad_plan,
                    usize::try_from(actor_object)?,
                    u32::try_from(second_stream_id)?,
                    ReplayNetworkAttributeTagV1::Float,
                )
                .map_err(std::io::Error::other)?;
                let error =
                    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                        &window,
                        &first,
                        &bad_plan,
                        ctx,
                    )
                    .expect_err("tag outside Int/String must fail");
                let text = error.to_string();
                tag_outside = text.contains("unsupported-second-header-tag")
                    || text.contains("unsupported-second-payload-tag");
            }
        }

        let mut poisoned = window.clone();
        let local_stop = decoded.stop_bit;
        for offset in 0..16u64 {
            set_bit(&mut poisoned, local_stop + offset, offset % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let poisoned_decoded =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                &poisoned,
                &first,
                &plan,
                ctx,
            )?;
        let poison = poisoned_decoded == decoded;
        poison_all &= poison;

        let row_exact = reconstruction_exact
            && semantic_exact
            && shape_exact
            && stop_exact
            && truncation
            && repeatability
            && poison
            && (!next_present || decoded.stop_bit
                == u64::try_from(expected_payload_end)?.checked_sub(base_bit).ok_or("stop base")?);
        if !row_exact || (!next_present && !terminator_no_lookup) {
            mismatch += 1;
        }

        println!(
            "R3_18K_ROW\tlabel={label}\tclass={class}\ttag={tag_out}\tpayload_start={payload_start_out}\tpayload_end={payload_end_out}\tpayload_width={payload_width_out}\treconstruction_exact={}\tsemantic_exact={}\tshape_exact={}\tstop_exact={}\ttruncation={}\trepeatability={}\tpoison={}\tterminator_no_lookup={}\tfollowing_bits_consumed=0",
            u8::from(reconstruction_exact),
            u8::from(semantic_exact),
            u8::from(shape_exact),
            u8::from(stop_exact),
            u8::from(truncation),
            u8::from(repeatability),
            u8::from(poison),
            u8::from(terminator_no_lookup),
        );
    }

    if rows != 94
        || terminators != 47
        || continuations != 47
        || ints != 46
        || strings != 1
        || no_lookup_rows != 47
        || truncation_rows != 47
        || mismatch != 0
        || !repeatability_all
        || !poison_all
        || !string_wrong_context
        || !tag_outside
    {
        return Err(format!(
            "R3.18K aggregate failure rows={rows} term={terminators} cont={continuations} Int={ints} String={strings} no_lookup={no_lookup_rows} trunc={truncation_rows} mismatch={mismatch} repeat={repeatability_all} poison={poison_all} wrong_ctx={string_wrong_context} tag_outside={tag_outside}"
        )
        .into());
    }

    println!(
        "R3_18K_AGG\trows=94\tterminators=47\tcontinuations=47\tints=46\tstrings=1\tterminator_no_lookup_rows=47\ttruncation_rows=47\tmismatch=0\tfollowing_bits_consumed=0\trepeatability=1\tpoison=1\tstring_wrong_context=1\ttag_outside=1"
    );
    Ok(())
}
