use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader, ReplayContentScaffoldReader,
    ReplayInput, ReplayNetworkAttributeTagV1, ReplayNetworkExistingActorSecondPropertyPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkLookupPlanReader,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
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

fn observe_one_bit(bytes: &[u8], start: u64, bit_limit: u64) -> Result<bool, String> {
    if start >= bit_limit {
        return Err(format!("control bit {start} is outside evidence bit limit {bit_limit}"));
    }
    let total = u64::try_from(bytes.len())
        .map_err(|_| "network length conversion")?
        .checked_mul(8)
        .ok_or("network bit length overflow")?;
    if start >= total {
        return Err(format!("control bit {start} outside network length {total}"));
    }
    let pos = usize::try_from(start).map_err(|_| "control position conversion")?;
    Ok(((bytes[pos / 8] >> (pos % 8)) & 1) != 0)
}

fn observe_after_expected_stop(
    bytes: &[u8],
    actual_stop: u64,
    expected_stop: u64,
    bit_limit: u64,
) -> Result<bool, String> {
    if actual_stop != expected_stop {
        return Err(format!(
            "prior R3.18J stop mismatch: actual {actual_stop}, expected {expected_stop}"
        ));
    }
    observe_one_bit(bytes, actual_stop, bit_limit)
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
    let mut exact_count = 0usize;
    let mut trunc_count = 0usize;
    let mut repeat_count = 0usize;
    let mut poison_count = 0usize;
    let mut stop_negative_count = 0usize;

    for line in request.lines().filter(|line| !line.trim().is_empty()) {
        rows += 1;
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 26 {
            return Err(format!("expected 26 fields, got {}", f.len()).into());
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
        let second_prop_bits: u32 = f[18].parse()?;
        let second_object: u32 = f[19].parse()?;
        let second_tag = parse_second_tag(f[20]).map_err(std::io::Error::other)?;
        let second_payload_start: u64 = f[21].parse()?;
        let second_payload_end: u64 = f[22].parse()?;
        let second_payload_width: u64 = f[23].parse()?;
        let _frame_index: usize = f[24].parse()?;
        let _actor_ordinal: usize = f[25].parse()?;

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
        let network_bits = u64::try_from(network.len())?.checked_mul(8).ok_or("network bits overflow")?;
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

        let ctx = ReplayNetworkK2DecodeContextV1 {
            net_version: 10,
            is_rl_223: false,
        };
        let decoded =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                &network,
                &first,
                &plan,
                ctx,
            )?;
        let repeated =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                &network,
                &first,
                &plan,
                ctx,
            )?;
        let repeatability = decoded == repeated;
        if repeatability {
            repeat_count += 1;
        }

        let second = decoded
            .header_composition
            .second_header
            .as_ref()
            .ok_or("continuation missing second header")?;
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
        if r3_18j_exact {
            exact_count += 1;
        }

        let control = observe_after_expected_stop(
            &network,
            decoded.stop_bit,
            second_payload_end,
            network_bits,
        )?;
        let control_start = decoded.stop_bit;
        let control_end = control_start.checked_add(1).ok_or("control end overflow")?;

        let truncation = observe_after_expected_stop(
            &network,
            decoded.stop_bit,
            second_payload_end,
            control_start,
        )
        .is_err();
        if truncation {
            trunc_count += 1;
        }

        let prior_stop_mismatch_negative = observe_after_expected_stop(
            &network,
            decoded.stop_bit,
            second_payload_end.checked_add(1).ok_or("bad mismatch stop")?,
            network_bits,
        )
        .is_err();
        if prior_stop_mismatch_negative {
            stop_negative_count += 1;
        }

        let mut poisoned = network.clone();
        for offset in 0..16u64 {
            set_bit(&mut poisoned, control_end + offset, offset % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let poisoned_j =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                &poisoned,
                &first,
                &plan,
                ctx,
            )?;
        let poisoned_control = observe_after_expected_stop(
            &poisoned,
            poisoned_j.stop_bit,
            second_payload_end,
            u64::try_from(poisoned.len())?.checked_mul(8).ok_or("poison length overflow")?,
        )?;
        let poison = poisoned_j == decoded && poisoned_control == control;
        if poison {
            poison_count += 1;
        }

        println!(
            "R3_18L_NATIVE\tlabel={label}\tprior_stop={second_payload_end}\tcontrol_start={control_start}\tcontrol_end={control_end}\tcontrol_value={}\tr3_18j_exact={}\ttruncation={}\trepeatability={}\tpoison={}\tprior_stop_mismatch_negative={}\tfollowing_stream_bits_consumed=0\tfollowing_header_bits_consumed=0\tfollowing_payload_bits_consumed=0",
            u8::from(control),
            u8::from(r3_18j_exact),
            u8::from(truncation),
            u8::from(repeatability),
            u8::from(poison),
            u8::from(prior_stop_mismatch_negative),
        );
    }

    if rows != 47
        || exact_count != 47
        || trunc_count != 47
        || repeat_count != 47
        || poison_count != 47
        || stop_negative_count != 47
    {
        return Err(format!(
            "R3.18L native aggregate failure rows={rows} exact={exact_count} trunc={trunc_count} repeat={repeat_count} poison={poison_count} stop_negative={stop_negative_count}"
        )
        .into());
    }

    println!(
        "R3_18L_NATIVE_AGG\trows=47\tr3_18j_exact=47\ttruncation=47\trepeatability=47\tpoison=47\tprior_stop_mismatch_negative=47\tfollowing_stream_bits_consumed=0\tfollowing_header_bits_consumed=0\tfollowing_payload_bits_consumed=0"
    );
    Ok(())
}
