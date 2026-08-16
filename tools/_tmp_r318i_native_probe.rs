use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkPrimitiveScalarValueV1, ReplayNetworkTextEncodingV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
    decode_replay_network_k2_v1, decode_replay_network_primitive_scalar_v1,
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

fn parse_first_tag(text: &str) -> Result<ReplayNetworkAttributeTagV1, String> {
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
        ReplayNetworkPrimitiveScalarValueV1::Boolean(value) => if *value { "1" } else { "0" }.to_owned(),
        ReplayNetworkPrimitiveScalarValueV1::Byte(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Enum(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Float { raw_bits, .. } => raw_bits.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int64(value) => value.to_string(),
    }
}

fn fnv64(bytes: &[u8]) -> String {
    let mut hash = 0xcbf29ce484222325u64;
    for byte in bytes {
        hash ^= u64::from(*byte);
        hash = hash.wrapping_mul(0x100000001b3);
    }
    format!("{hash:016x}")
}

fn set_bit(bytes: &mut Vec<u8>, position: u64, value: bool) -> Result<(), String> {
    let needed_bits = position.checked_add(1).ok_or("bit position overflow")?;
    let needed_bytes = usize::try_from(needed_bits.checked_add(7).ok_or("bit length overflow")? / 8)
        .map_err(|_| "bit length conversion overflow")?;
    if bytes.len() < needed_bytes {
        bytes.resize(needed_bytes, 0);
    }
    let pos = usize::try_from(position).map_err(|_| "bit index overflow")?;
    if value {
        bytes[pos / 8] |= 1 << (pos % 8);
    } else {
        bytes[pos / 8] &= !(1 << (pos % 8));
    }
    Ok(())
}

fn trunc_before_end(bytes: &[u8], end_bit: u64) -> Result<Vec<u8>, String> {
    let ceil = end_bit.checked_add(7).ok_or("truncation overflow")? / 8;
    if ceil == 0 {
        return Err("cannot truncate zero-width prefix".to_owned());
    }
    let keep = usize::try_from(ceil - 1).map_err(|_| "truncation conversion overflow")?;
    if keep > bytes.len() {
        return Err("truncation exceeds input".to_owned());
    }
    Ok(bytes[..keep].to_vec())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args_os().skip(1);
    let request_path = args.next().ok_or("missing request TSV")?;
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }
    let request = fs::read_to_string(request_path)?;

    let mut rows = 0usize;
    let mut terminators = 0usize;
    let mut continuations = 0usize;
    let mut int_rows = 0usize;
    let mut string_rows = 0usize;
    let mut terminator_no_payload = 0usize;
    let mut truncation_rows = 0usize;
    let mut mismatch = 0usize;
    let mut repeatability_all = true;
    let mut poison_all = true;

    for line in request.lines().filter(|line| !line.trim().is_empty()) {
        rows += 1;
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 34 {
            return Err(format!("expected 34 TSV fields, got {}", f.len()).into());
        }
        let class = f[0];
        let replay_path = f[1];
        let actor_object: u32 = f[2].parse()?;
        let expected_first_stream: u32 = f[3].parse()?;
        let expected_first_object: u32 = f[4].parse()?;
        let first_tag = parse_first_tag(f[5]).map_err(std::io::Error::other)?;
        let global_first_start: u64 = f[6].parse()?;
        let global_first_payload_start: u64 = f[7].parse()?;
        let global_first_payload_end: u64 = f[8].parse()?;
        let global_second_present_start: u64 = f[9].parse()?;
        let global_second_present_end: u64 = f[10].parse()?;
        let expected_next = match f[11] { "0" => false, "1" => true, x => return Err(format!("bad next bit {x}").into()) };
        let window_byte_start: u64 = f[12].parse()?;
        let local_first_start: u64 = f[13].parse()?;
        let window = parse_hex(f[14]).map_err(std::io::Error::other)?;
        let expected_first_lossless = f[15];
        let expected_second_property_start: i64 = f[16].parse()?;
        let expected_second_property_end: i64 = f[17].parse()?;
        let expected_second_stream_start: i64 = f[18].parse()?;
        let expected_second_stream_end: i64 = f[19].parse()?;
        let expected_second_stream: i64 = f[20].parse()?;
        let expected_second_bound: i64 = f[21].parse()?;
        let expected_second_prop_bits: i64 = f[22].parse()?;
        let expected_second_object: i64 = f[23].parse()?;
        let expected_second_tag = f[24];
        let expected_second_payload_start: i64 = f[25].parse()?;
        let expected_payload_end: i64 = f[26].parse()?;
        let expected_payload_width: u64 = f[27].parse()?;
        let expected_semantic_kind = f[28];
        let expected_i32 = f[29];
        let expected_fnv = f[30];
        let expected_utf8_len: usize = f[31].parse()?;
        let expected_declared: i32 = f[32].parse()?;
        let expected_encoding = f[33];

        let replay_bytes = fs::read(Path::new(replay_path))?;
        let input = ReplayInput::Memory { label: replay_path.to_owned(), bytes: replay_bytes };
        let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;
        let base_bit = window_byte_start.checked_mul(8).ok_or("window base overflow")?;

        let first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &window, local_first_start, actor_object, &plan,
        )?;
        let first_payload_start = first.header.payload_start_bit.ok_or("missing first payload start")?;
        let first_exact = first.header.stream_id == Some(expected_first_stream)
            && first.header.resolved_property_object_index == Some(expected_first_object)
            && first.header.resolved_attribute_tag == Some(first_tag)
            && lossless(&first.scalar.value) == expected_first_lossless
            && base_bit + first.header.property_present_start_bit == global_first_start
            && base_bit + first_payload_start == global_first_payload_start
            && base_bit + first.scalar.payload_end_bit == global_first_payload_end
            && base_bit + first.stop_bit == global_second_present_start;
        if !first_exact {
            return Err(format!("{replay_path} {class}: first reconstruction mismatch").into());
        }

        let composed = decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &window, &first, &plan,
        )?;
        let repeated_header = decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            &window, &first, &plan,
        )?;
        if repeated_header != composed {
            return Err(format!("{replay_path} {class}: second header repeatability mismatch").into());
        }
        let control_exact = composed.control.next_property_present == expected_next
            && base_bit + composed.control.property_present_start_bit == global_second_present_start
            && base_bit + composed.control.property_present_end_bit == global_second_present_end;
        if !control_exact {
            return Err(format!("{replay_path} {class}: control mismatch").into());
        }

        let mut tag_out = "None".to_owned();
        let mut payload_start_global = -1i64;
        let mut payload_end_global = -1i64;
        let mut payload_width = 0u64;
        let mut payload_exact = true;
        let mut semantic_exact = true;
        let mut shape_exact = true;
        let mut truncation = true;
        let mut poison = true;

        if !expected_next {
            terminators += 1;
            if class != "terminator" || composed.second_header.is_some() || expected_payload_end != -1 {
                return Err(format!("{replay_path}: malformed terminator evidence row").into());
            }
            let mut poison_plan = plan.clone();
            let slot = poison_plan.object_lookups.get_mut(usize::try_from(actor_object)?)
                .ok_or("terminator actor lookup index missing")?;
            *slot = None;
            let no_lookup = decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
                &window, &first, &poison_plan,
            )?;
            if no_lookup.second_header.is_some() || no_lookup.control.next_property_present {
                return Err(format!("{replay_path}: terminator attempted second payload/header lookup").into());
            }
            terminator_no_payload += 1;
        } else {
            continuations += 1;
            if class != "continuation" {
                return Err(format!("{replay_path}: true control classified as {class}").into());
            }
            let second = composed.second_header.as_ref().ok_or("missing second header")?;
            let stream_start = second.stream_id_start_bit.ok_or("missing second stream start")?;
            let stream_end = second.stream_id_end_bit.ok_or("missing second stream end")?;
            let stream_id = second.stream_id.ok_or("missing second stream id")?;
            let stream_bound = second.stream_id_bound.ok_or("missing second stream bound")?;
            let prop_bits = second.prop_id_bits.ok_or("missing prop bits")?;
            let property_object = second.resolved_property_object_index.ok_or("missing second object")?;
            let second_tag = second.resolved_attribute_tag.ok_or("missing second tag")?;
            let payload_start = second.payload_start_bit.ok_or("missing payload start")?;
            let header_exact = base_bit + second.property_present_start_bit == u64::try_from(expected_second_property_start)?
                && base_bit + second.property_present_end_bit == u64::try_from(expected_second_property_end)?
                && base_bit + stream_start == u64::try_from(expected_second_stream_start)?
                && base_bit + stream_end == u64::try_from(expected_second_stream_end)?
                && i64::from(stream_id) == expected_second_stream
                && i64::from(stream_bound) == expected_second_bound
                && i64::from(prop_bits) == expected_second_prop_bits
                && i64::from(property_object) == expected_second_object
                && format!("{second_tag:?}") == expected_second_tag
                && base_bit + payload_start == u64::try_from(expected_second_payload_start)?
                && composed.stop_bit == payload_start;
            if !header_exact {
                return Err(format!("{replay_path}: second header reconstruction mismatch").into());
            }

            let expected_end_local = u64::try_from(expected_payload_end)?
                .checked_sub(base_bit).ok_or("payload end before window base")?;
            let expected_start_local = u64::try_from(expected_second_payload_start)?
                .checked_sub(base_bit).ok_or("payload start before window base")?;
            if expected_start_local != payload_start {
                return Err("native/oracle payload local start mismatch".into());
            }

            if expected_second_tag == "Int" {
                int_rows += 1;
                tag_out = "Int".to_owned();
                let decoded = decode_replay_network_primitive_scalar_v1(
                    &window, payload_start, ReplayNetworkAttributeTagV1::Int,
                )?;
                let repeated = decode_replay_network_primitive_scalar_v1(
                    &window, payload_start, ReplayNetworkAttributeTagV1::Int,
                )?;
                if repeated != decoded { repeatability_all = false; }
                payload_exact = decoded.payload_start_bit == payload_start
                    && decoded.payload_end_bit == expected_end_local
                    && u64::from(decoded.payload_width) == expected_payload_width;
                semantic_exact = matches!(&decoded.value, ReplayNetworkPrimitiveScalarValueV1::Int(value) if value.to_string() == expected_i32)
                    && expected_semantic_kind == "Int" && expected_fnv == "none";
                shape_exact = expected_payload_width == 32 && expected_encoding == "None" && expected_declared == 0;

                let truncated = trunc_before_end(&window, expected_end_local).map_err(std::io::Error::other)?;
                truncation = decode_replay_network_primitive_scalar_v1(
                    &truncated, payload_start, ReplayNetworkAttributeTagV1::Int,
                ).is_err();

                let mut poisoned = window.clone();
                for offset in 0..16u64 {
                    set_bit(&mut poisoned, expected_end_local + offset, offset % 2 == 0).map_err(std::io::Error::other)?;
                }
                let poisoned_decoded = decode_replay_network_primitive_scalar_v1(
                    &poisoned, payload_start, ReplayNetworkAttributeTagV1::Int,
                )?;
                poison = poisoned_decoded == decoded;
            } else if expected_second_tag == "String" {
                string_rows += 1;
                tag_out = "String".to_owned();
                let ctx = ReplayNetworkK2DecodeContextV1 { net_version: 10, is_rl_223: false };
                let decoded = decode_replay_network_k2_v1(
                    &window, payload_start, ReplayNetworkAttributeTagV1::String, ctx,
                )?;
                let repeated = decode_replay_network_k2_v1(
                    &window, payload_start, ReplayNetworkAttributeTagV1::String, ctx,
                )?;
                if repeated != decoded { repeatability_all = false; }
                payload_exact = decoded.payload_start_bit == payload_start
                    && decoded.payload_end_bit == expected_end_local
                    && decoded.payload_width == expected_payload_width;
                match &decoded.value {
                    ReplayNetworkK2ValueV1::String(text) => {
                        semantic_exact = expected_semantic_kind == "String"
                            && expected_i32 == "none"
                            && fnv64(text.value.as_bytes()) == expected_fnv
                            && text.value.len() == expected_utf8_len;
                        let encoding = match text.encoding {
                            ReplayNetworkTextEncodingV1::Empty => "Empty",
                            ReplayNetworkTextEncodingV1::Windows1252 => "Windows1252",
                            ReplayNetworkTextEncodingV1::Utf16Le => "Utf16Le",
                        };
                        shape_exact = text.declared_length == expected_declared && encoding == expected_encoding;
                    }
                    _ => { semantic_exact = false; shape_exact = false; }
                }

                let truncated = trunc_before_end(&window, expected_end_local).map_err(std::io::Error::other)?;
                truncation = decode_replay_network_k2_v1(
                    &truncated, payload_start, ReplayNetworkAttributeTagV1::String, ctx,
                ).is_err();

                let mut poisoned = window.clone();
                for offset in 0..16u64 {
                    set_bit(&mut poisoned, expected_end_local + offset, offset % 2 == 0).map_err(std::io::Error::other)?;
                }
                let poisoned_decoded = decode_replay_network_k2_v1(
                    &poisoned, payload_start, ReplayNetworkAttributeTagV1::String, ctx,
                )?;
                poison = poisoned_decoded == decoded;
            } else {
                return Err(format!("{replay_path}: second payload tag outside Int/String").into());
            }

            payload_start_global = expected_second_payload_start;
            payload_end_global = expected_payload_end;
            payload_width = expected_payload_width;
            if !payload_exact || !semantic_exact || !shape_exact || !truncation || !poison {
                mismatch += 1;
            }
            if !truncation { truncation_rows += 0; } else { truncation_rows += 1; }
            if !poison { poison_all = false; }
        }

        println!(
            "R3_18I_NATIVE\tclass={}\tlabel={}\ttag={}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\treconstruction_exact=true\tpayload_exact={}\tsemantic_exact={}\tshape_exact={}\trepeatability={}\ttruncation={}\tpoison={}\tthird_property_bits_consumed=0",
            class, replay_path.replace('\\', "/"), tag_out, payload_start_global, payload_end_global,
            payload_width, payload_exact, semantic_exact, shape_exact, repeatability_all, truncation, poison,
        );
    }

    let scalar_wrong = decode_replay_network_primitive_scalar_v1(
        &[0u8; 8], 0, ReplayNetworkAttributeTagV1::String,
    ).is_err();
    if !scalar_wrong { return Err("wrong scalar tag unexpectedly decoded".into()); }
    let k2_wrong = decode_replay_network_k2_v1(
        &[0u8; 8], 0, ReplayNetworkAttributeTagV1::Int,
        ReplayNetworkK2DecodeContextV1 { net_version: 10, is_rl_223: false },
    ).is_err();
    if !k2_wrong { return Err("wrong K2 tag unexpectedly decoded".into()); }

    println!("R3_18I_NATIVE_ROWS={rows}");
    println!("R3_18I_TERMINATOR_ROWS={terminators}");
    println!("R3_18I_CONTINUATION_ROWS={continuations}");
    println!("R3_18I_INT_ROWS={int_rows}");
    println!("R3_18I_STRING_ROWS={string_rows}");
    println!("R3_18I_TERMINATOR_NO_PAYLOAD_ROWS={terminator_no_payload}");
    println!("R3_18I_PAYLOAD_TRUNCATION_ROWS={truncation_rows}");
    println!("R3_18I_THIRD_PROPERTY_BITS_CONSUMED=0");
    println!("R3_18I_MISMATCH_COUNT={mismatch}");
    println!("R3_18I_WRONG_SCALAR_TAG_NEGATIVE=PASS");
    println!("R3_18I_WRONG_K2_TAG_NEGATIVE=PASS");
    if repeatability_all { println!("R3_18I_REPEATABILITY=PASS"); } else { return Err("payload repeatability mismatch".into()); }
    if poison_all { println!("R3_18I_POST_PAYLOAD_POISON=PASS"); } else { return Err("post-payload poison changed result".into()); }

    if rows != 94 || terminators != 47 || continuations != 47 || int_rows != 46 || string_rows != 1
        || terminator_no_payload != 47 || truncation_rows != 47 || mismatch != 0
    {
        return Err("R3.18I aggregate native evidence mismatch".into());
    }
    Ok(())
}
