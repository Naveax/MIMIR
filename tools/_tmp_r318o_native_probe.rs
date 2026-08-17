use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader, ReplayContentScaffoldReader,
    ReplayInput, ReplayNetworkAttributeTagV1, ReplayNetworkExistingActorSecondPropertyPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkLookupPlanReader,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_first_property_header_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::env;
use std::fs;
use std::path::Path;

fn parse_first_tag(text: &str) -> Result<ReplayNetworkAttributeTagV1, String> {
    match text {
        "Boolean" => Ok(ReplayNetworkAttributeTagV1::Boolean),
        "Byte" => Ok(ReplayNetworkAttributeTagV1::Byte),
        "Enum" => Ok(ReplayNetworkAttributeTagV1::Enum),
        "Float" => Ok(ReplayNetworkAttributeTagV1::Float),
        "Int" => Ok(ReplayNetworkAttributeTagV1::Int),
        "Int64" => Ok(ReplayNetworkAttributeTagV1::Int64),
        _ => Err(format!("unsupported first tag: {text}")),
    }
}

fn parse_second_tag(text: &str) -> Result<ReplayNetworkAttributeTagV1, String> {
    match text {
        "Int" => Ok(ReplayNetworkAttributeTagV1::Int),
        "String" => Ok(ReplayNetworkAttributeTagV1::String),
        _ => Err(format!("unsupported second tag: {text}")),
    }
}

fn scalar_lossless(value: &mimir_replay::ReplayNetworkPrimitiveScalarValueV1) -> String {
    use mimir_replay::ReplayNetworkPrimitiveScalarValueV1::*;
    match value {
        Boolean(value) => if *value { "1" } else { "0" }.to_owned(),
        Byte(value) => value.to_string(),
        Enum(value) => value.to_string(),
        Float { raw_bits, .. } => raw_bits.to_string(),
        Int(value) => value.to_string(),
        Int64(value) => value.to_string(),
    }
}

fn set_bit(bytes: &mut Vec<u8>, position: u64, value: bool) -> Result<(), String> {
    let pos = usize::try_from(position).map_err(|_| "bit position conversion")?;
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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let request_path = env::args_os().nth(1).ok_or("missing target TSV")?;
    if env::args_os().nth(2).is_some() {
        return Err("unexpected extra argument".into());
    }
    let request = fs::read_to_string(request_path)?;

    let mut rows = 0usize;
    let mut r3_18j_count = 0usize;
    let mut r3_18m_count = 0usize;
    let mut header_count = 0usize;
    let mut trunc_property_count = 0usize;
    let mut trunc_stream_count = 0usize;
    let mut stop_negative_count = 0usize;
    let mut wrong_context_count = 0usize;
    let mut repeat_count = 0usize;
    let mut poison_count = 0usize;

    for line in request.lines().filter(|line| !line.trim().is_empty()) {
        rows += 1;
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 39 {
            return Err(format!("expected 39 fields, got {}", f.len()).into());
        }
        let label = f[0];
        let actor_object: u32 = f[1].parse()?;
        let first_tag = parse_first_tag(f[2]).map_err(std::io::Error::other)?;
        let first_lossless = f[3];
        let first_present_start: u64 = f[4].parse()?;
        let first_present_end: u64 = f[5].parse()?;
        let first_stream_start: u64 = f[6].parse()?;
        let first_stream_end: u64 = f[7].parse()?;
        let first_stream_id: u32 = f[8].parse()?;
        let first_object: u32 = f[9].parse()?;
        let first_payload_start: u64 = f[10].parse()?;
        let first_payload_end: u64 = f[11].parse()?;
        let second_present_start: u64 = f[12].parse()?;
        let second_present_end: u64 = f[13].parse()?;
        let second_stream_start: u64 = f[14].parse()?;
        let second_stream_end: u64 = f[15].parse()?;
        let second_stream_id: u32 = f[16].parse()?;
        let second_bound: u32 = f[17].parse()?;
        let second_prop_bits: u8 = f[18].parse()?;
        let second_object: u32 = f[19].parse()?;
        let second_tag = parse_second_tag(f[20]).map_err(std::io::Error::other)?;
        let second_payload_start: u64 = f[21].parse()?;
        let second_payload_end: u64 = f[22].parse()?;
        let second_payload_width: u64 = f[23].parse()?;
        let _frame_index: usize = f[24].parse()?;
        let _actor_ordinal: usize = f[25].parse()?;
        let expected_present_start: u64 = f[26].parse()?;
        let expected_present_end: u64 = f[27].parse()?;
        let expected_stream_start: u64 = f[28].parse()?;
        let expected_stream_end: u64 = f[29].parse()?;
        let expected_stream_id: u32 = f[30].parse()?;
        let expected_stream_bound: u32 = f[31].parse()?;
        let expected_prop_bits: u8 = f[32].parse()?;
        let expected_property_object: u32 = f[33].parse()?;
        let expected_tag = f[34];
        let expected_payload_start: u64 = f[35].parse()?;
        let _version_major: u32 = f[36].parse()?;
        let _version_minor: u32 = f[37].parse()?;
        let _net_version: u32 = f[38].parse()?;

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
        let network = replay_bytes[network_start..network_end].to_vec();
        let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;

        let first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &network,
            first_present_start,
            actor_object,
            &plan,
        )?;
        let fh = &first.header;
        let first_exact = fh.property_present_start_bit == first_present_start
            && fh.property_present_end_bit == first_present_end
            && fh.stream_id_start_bit == Some(first_stream_start)
            && fh.stream_id_end_bit == Some(first_stream_end)
            && fh.stream_id == Some(first_stream_id)
            && fh.resolved_property_object_index == Some(first_object)
            && fh.resolved_attribute_tag == Some(first_tag)
            && fh.payload_start_bit == Some(first_payload_start)
            && first.scalar.payload_end_bit == first_payload_end
            && first.stop_bit == second_present_start
            && scalar_lossless(&first.scalar.value) == first_lossless;
        if !first_exact {
            return Err(format!("{label}: first property reconstruction mismatch").into());
        }

        let ctx = ReplayNetworkK2DecodeContextV1 { net_version: 10, is_rl_223: false };
        let decoded = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &network, &first, &plan, ctx,
        )?;
        let second = decoded.header_composition.second_header.as_ref().ok_or("missing second header")?;
        let header_exact = decoded.header_composition.control.next_property_present
            && decoded.header_composition.control.property_present_start_bit == second_present_start
            && decoded.header_composition.control.property_present_end_bit == second_present_end
            && second.property_present_start_bit == second_present_start
            && second.property_present_end_bit == second_present_end
            && second.stream_id_start_bit == Some(second_stream_start)
            && second.stream_id_end_bit == Some(second_stream_end)
            && second.stream_id == Some(second_stream_id)
            && second.stream_id_bound == Some(second_bound)
            && second.prop_id_bits == Some(second_prop_bits)
            && second.resolved_property_object_index == Some(second_object)
            && second.resolved_attribute_tag == Some(second_tag)
            && second.payload_start_bit == Some(second_payload_start);
        let payload_exact = match decoded.second_payload.as_ref().ok_or("missing second payload")? {
            ReplayNetworkExistingActorSecondPropertyPayloadV1::Int(value) => {
                second_tag == ReplayNetworkAttributeTagV1::Int
                    && value.payload_start_bit == second_payload_start
                    && value.payload_end_bit == second_payload_end
                    && u64::from(value.payload_width) == second_payload_width
                    && value.stop_bit == second_payload_end
            }
            ReplayNetworkExistingActorSecondPropertyPayloadV1::String(value) => {
                second_tag == ReplayNetworkAttributeTagV1::String
                    && value.payload_start_bit == second_payload_start
                    && value.payload_end_bit == second_payload_end
                    && value.payload_width == second_payload_width
            }
        };
        let r3_18j_exact = header_exact && payload_exact && decoded.stop_bit == second_payload_end;
        if !r3_18j_exact {
            return Err(format!("{label}: R3.18J reconstruction mismatch").into());
        }
        r3_18j_count += 1;

        let control = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(
            &network, &decoded,
        )?;
        let r3_18m_exact = control.following_property_present
            && control.property_present_start_bit == decoded.stop_bit
            && control.property_present_start_bit == second_payload_end
            && control.property_present_start_bit == expected_present_start
            && control.property_present_end_bit == expected_present_end
            && control.stop_bit == expected_present_end;
        if !r3_18m_exact {
            return Err(format!("{label}: R3.18M control mismatch").into());
        }
        r3_18m_count += 1;

        let following = decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            control.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        let header_exact = following.property_present
            && following.property_present_start_bit == expected_present_start
            && following.property_present_end_bit == expected_present_end
            && following.stream_id_start_bit == Some(expected_stream_start)
            && following.stream_id_end_bit == Some(expected_stream_end)
            && following.stream_id == Some(expected_stream_id)
            && following.stream_id_bound == Some(expected_stream_bound)
            && following.prop_id_bits == Some(expected_prop_bits)
            && following.resolved_property_object_index == Some(expected_property_object)
            && following.resolved_attribute_tag.map(|tag| format!("{tag:?}")) == Some(expected_tag.to_owned())
            && following.payload_start_bit == Some(expected_payload_start)
            && following.stop_bit == expected_payload_start;
        if !header_exact {
            return Err(format!("{label}: following header mismatch").into());
        }
        header_count += 1;

        let repeated = decode_replay_network_existing_actor_first_property_header_v1(
            &network, control.property_present_start_bit, actor_object, &plan,
        )?;
        let repeatability = repeated == following;
        if repeatability { repeat_count += 1; }

        let trunc_property_bytes = usize::try_from(control.property_present_start_bit / 8)?;
        let trunc_property = decode_replay_network_existing_actor_first_property_header_v1(
            &network[..trunc_property_bytes.min(network.len())],
            control.property_present_start_bit,
            actor_object,
            &plan,
        ).is_err();
        if trunc_property { trunc_property_count += 1; }

        let trunc_stream_bytes = usize::try_from(expected_stream_end.saturating_sub(1) / 8)?;
        let trunc_stream = decode_replay_network_existing_actor_first_property_header_v1(
            &network[..trunc_stream_bytes.min(network.len())],
            control.property_present_start_bit,
            actor_object,
            &plan,
        ).is_err();
        if trunc_stream { trunc_stream_count += 1; }

        let mut bad_prior = decoded.clone();
        bad_prior.stop_bit = bad_prior.stop_bit.checked_add(1).ok_or("bad prior stop overflow")?;
        let prior_stop_mismatch_negative = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(
            &network, &bad_prior,
        ).is_err();
        if prior_stop_mismatch_negative { stop_negative_count += 1; }

        let wrong_actor_context_negative = decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            control.property_present_start_bit,
            u32::MAX,
            &plan,
        ).is_err();
        if wrong_actor_context_negative { wrong_context_count += 1; }

        let mut poisoned = network.clone();
        for offset in 0..16u64 {
            set_bit(&mut poisoned, expected_payload_start + offset, offset % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let poisoned_header = decode_replay_network_existing_actor_first_property_header_v1(
            &poisoned,
            control.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        let poison = poisoned_header == following;
        if poison { poison_count += 1; }

        println!(
            "R3_18O_NATIVE\tlabel={label}\tpresent_start={}\tpresent_end={}\tstream_start={}\tstream_end={}\tstream_id={}\tstream_bound={}\tprop_bits={}\tproperty_object={}\ttag={}\tpayload_start={}\theader_stop={}\tr3_18j_exact=1\tr3_18m_exact=1\ttrunc_property={}\ttrunc_stream={}\tprior_stop_mismatch_negative={}\twrong_actor_context_negative={}\trepeatability={}\tpoison={}\tfollowing_payload_bits_consumed=0\tanother_control_bits_consumed=0",
            following.property_present_start_bit,
            following.property_present_end_bit,
            following.stream_id_start_bit.ok_or("missing stream start")?,
            following.stream_id_end_bit.ok_or("missing stream end")?,
            following.stream_id.ok_or("missing stream id")?,
            following.stream_id_bound.ok_or("missing stream bound")?,
            following.prop_id_bits.ok_or("missing prop bits")?,
            following.resolved_property_object_index.ok_or("missing property object")?,
            following.resolved_attribute_tag.map(|tag| format!("{tag:?}")).ok_or("missing tag")?,
            following.payload_start_bit.ok_or("missing payload start")?,
            following.stop_bit,
            u8::from(trunc_property),
            u8::from(trunc_stream),
            u8::from(prior_stop_mismatch_negative),
            u8::from(wrong_actor_context_negative),
            u8::from(repeatability),
            u8::from(poison),
        );
    }

    if rows != 47 || r3_18j_count != 47 || r3_18m_count != 47 || header_count != 47
        || trunc_property_count != 47 || trunc_stream_count != 47 || stop_negative_count != 47
        || wrong_context_count != 47 || repeat_count != 47 || poison_count != 47
    {
        return Err(format!(
            "R3.18O aggregate failure rows={rows} r3j={r3_18j_count} r3m={r3_18m_count} header={header_count} trunc_property={trunc_property_count} trunc_stream={trunc_stream_count} stop_negative={stop_negative_count} wrong_context={wrong_context_count} repeat={repeat_count} poison={poison_count}"
        ).into());
    }

    println!(
        "R3_18O_NATIVE_AGG\trows=47\tr3_18j_exact=47\tr3_18m_exact=47\theader_exact=47\ttrunc_property=47\ttrunc_stream=47\tprior_stop_mismatch_negative=47\twrong_actor_context_negative=47\trepeatability=47\tpoison=47\tfollowing_payload_bits_consumed=0\tanother_control_bits_consumed=0"
    );
    Ok(())
}
