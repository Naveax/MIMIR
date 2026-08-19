use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkK2DecodeContextV1,
    ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_first_property_header_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::{env, fs, path::Path};

fn set_bit(bytes: &mut Vec<u8>, position: u64, value: bool) -> Result<(), String> {
    let p = usize::try_from(position).map_err(|_| "bit position conversion")?;
    let need = p / 8 + 1;
    if bytes.len() < need {
        bytes.resize(need, 0);
    }
    if value {
        bytes[p / 8] |= 1 << (p % 8);
    } else {
        bytes[p / 8] &= !(1 << (p % 8));
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
    let mut published_exact_n = 0usize;
    let mut direct_equal_n = 0usize;
    let mut repeat_n = 0usize;
    let mut trunc_n = 0usize;
    let mut wrong_actor_n = 0usize;
    let mut unresolved_n = 0usize;
    let mut wrong_context_n = 0usize;
    let mut poison_n = 0usize;

    for line in request.lines().filter(|x| !x.trim().is_empty()) {
        rows += 1;
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 18 {
            return Err(format!("expected 18 fields got {}", f.len()).into());
        }
        let label = f[0];
        let frame_index: usize = f[1].parse()?;
        let actor_ordinal: usize = f[2].parse()?;
        let actor_object: u32 = f[3].parse()?;
        let first_start: u64 = f[4].parse()?;
        let control_start: u64 = f[5].parse()?;
        let control_end: u64 = f[6].parse()?;
        let stream_start: u64 = f[7].parse()?;
        let stream_end: u64 = f[8].parse()?;
        let stream_id: u32 = f[9].parse()?;
        let stream_bound: u32 = f[10].parse()?;
        let prop_bits: u8 = f[11].parse()?;
        let property_object: u32 = f[12].parse()?;
        let tag = f[13];
        let payload_start: u64 = f[14].parse()?;
        let version_major = f[15].parse()?;
        let version_minor = f[16].parse()?;
        let net_version = f[17].parse()?;

        let replay_bytes = fs::read(Path::new(label))?;
        let input = ReplayInput::Memory {
            label: label.to_owned(),
            bytes: replay_bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader.read_content_scaffold(&input)?;
        let ns = usize::try_from(scaffold.network_start)?;
        let ne = usize::try_from(scaffold.network_end)?;
        if ns > ne || ne > replay_bytes.len() {
            return Err(format!("{label}: invalid network slice").into());
        }
        let network = replay_bytes[ns..ne].to_vec();
        let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;

        let first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &network,
            first_start,
            actor_object,
            &plan,
        )?;
        let second = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &network,
            &first,
            &plan,
            ReplayNetworkK2DecodeContextV1 {
                net_version: 10,
                is_rl_223: false,
            },
        )?;
        let context = ReplayNetworkK3DecodeContextV1 {
            version_major,
            version_minor,
            net_version,
            is_rl_223: false,
        };
        let prior = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network,
            &second,
            &plan,
            context,
        )?;
        if prior.stop_bit != control_start {
            return Err(format!(
                "{label}: T stop drift {} expected {control_start}",
                prior.stop_bit
            )
            .into());
        }

        let published = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
            &network,
            &prior,
            &plan,
            context,
        )?;
        let h = &published.following_header;
        let resolved_tag = h
            .resolved_attribute_tag
            .ok_or("published AA missing resolved tag")?;
        let published_exact = published.control.following_property_present
            && published.control.property_present_start_bit == control_start
            && published.control.property_present_end_bit == control_end
            && published.control.stop_bit == control_end
            && h.property_present
            && h.property_present_start_bit == control_start
            && h.property_present_end_bit == control_end
            && h.stream_id_start_bit == Some(stream_start)
            && h.stream_id_end_bit == Some(stream_end)
            && h.stream_id == Some(stream_id)
            && h.stream_id_bound == Some(stream_bound)
            && h.prop_id_bits == Some(prop_bits)
            && h.resolved_property_object_index == Some(property_object)
            && format!("{resolved_tag:?}") == tag
            && h.payload_start_bit == Some(payload_start)
            && h.stop_bit == payload_start
            && published.stop_bit == payload_start;
        if !published_exact {
            return Err(format!("{label}: published AA frozen-Y mismatch {published:?}").into());
        }
        published_exact_n += 1;

        let direct = decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            control_start,
            actor_object,
            &plan,
        )?;
        let direct_equal = direct == published.following_header;
        if !direct_equal {
            return Err(format!("{label}: direct header differs from published AA").into());
        }
        direct_equal_n += 1;

        let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
            &network,
            &prior,
            &plan,
            context,
        )?;
        let repeatability = repeated == published;
        if repeatability {
            repeat_n += 1;
        }

        let trunc_len = usize::try_from(payload_start / 8)?.min(network.len());
        let truncation = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
            &network[..trunc_len],
            &prior,
            &plan,
            context,
        )
        .is_err();
        if truncation {
            trunc_n += 1;
        }

        let mut wrong_actor_prior = prior.clone();
        wrong_actor_prior
            .header_composition
            .following_header
            .actor_object_index = u32::MAX;
        let wrong_actor = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
            &network,
            &wrong_actor_prior,
            &plan,
            context,
        )
        .is_err();
        if wrong_actor {
            wrong_actor_n += 1;
        }

        let mut unresolved_plan = plan.clone();
        let unresolved_lookup = if let Some(slot) = unresolved_plan
            .object_lookups
            .get_mut(usize::try_from(actor_object)?)
        {
            *slot = None;
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
                &network,
                &prior,
                &unresolved_plan,
                context,
            )
            .is_err()
        } else {
            true
        };
        if unresolved_lookup {
            unresolved_n += 1;
        }

        let wrong_context = ReplayNetworkK3DecodeContextV1 {
            version_major: 868,
            version_minor: 31,
            net_version: 10,
            is_rl_223: false,
        };
        let wrong_version = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
            &network,
            &prior,
            &plan,
            wrong_context,
        )
        .is_err();
        if wrong_version {
            wrong_context_n += 1;
        }

        let mut poisoned = network.clone();
        for off in 0..16u64 {
            set_bit(&mut poisoned, payload_start + off, off % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let after_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
            &poisoned,
            &prior,
            &plan,
            context,
        )?;
        let poison_invariance = after_poison == published;
        if poison_invariance {
            poison_n += 1;
        }

        println!(
            "R3_18AB_PUBLISHED\tlabel={label}\tframe_index={frame_index}\tactor_ordinal={actor_ordinal}\tactor_context_object_id={actor_object}\tproperty_present_start_bit={}\tproperty_present_end_bit={}\tstream_id_start_bit={}\tstream_id_end_bit={}\tstream_id={}\tstream_id_bound={}\tprop_id_bits={}\tproperty_object_id={}\tattribute_tag={:?}\tversion_major={}\tversion_minor={}\tnet_version={}\tpayload_start_bit={}\tstop_bit={}\tpublished_exact={}\tdirect_equal={}\trepeatability={}\ttruncation={}\twrong_actor_negative={}\tunresolved_lookup_negative={}\twrong_version_negative={}\tpost_payload_poison={}\tfollowing_payload_bits_consumed=0\tanother_control_bits_consumed=0",
            h.property_present_start_bit,
            h.property_present_end_bit,
            h.stream_id_start_bit.ok_or("missing stream start")?,
            h.stream_id_end_bit.ok_or("missing stream end")?,
            h.stream_id.ok_or("missing stream id")?,
            h.stream_id_bound.ok_or("missing stream bound")?,
            h.prop_id_bits.ok_or("missing prop bits")?,
            h.resolved_property_object_index.ok_or("missing property object")?,
            resolved_tag,
            context.version_major,
            context.version_minor,
            context.net_version,
            h.payload_start_bit.ok_or("missing payload start")?,
            published.stop_bit,
            u8::from(published_exact),
            u8::from(direct_equal),
            u8::from(repeatability),
            u8::from(truncation),
            u8::from(wrong_actor),
            u8::from(unresolved_lookup),
            u8::from(wrong_version),
            u8::from(poison_invariance),
        );
    }

    if rows != 47
        || published_exact_n != 47
        || direct_equal_n != 47
        || repeat_n != 47
        || trunc_n != 47
        || wrong_actor_n != 47
        || unresolved_n != 47
        || wrong_context_n != 47
        || poison_n != 47
    {
        return Err(format!(
            "R3.18AB aggregate failure rows={rows} published={published_exact_n} direct={direct_equal_n} repeat={repeat_n} trunc={trunc_n} wrong_actor={wrong_actor_n} unresolved={unresolved_n} wrong_context={wrong_context_n} poison={poison_n}"
        )
        .into());
    }

    println!(
        "R3_18AB_PUBLISHED_AGG\trows=47\tpublished_exact=47\tdirect_equal=47\trepeatability=47\ttruncation=47\twrong_actor_negative=47\tunresolved_lookup_negative=47\twrong_version_negative=47\tpost_payload_poison=47\tfollowing_payload_bits_consumed=0\tanother_control_bits_consumed=0"
    );
    Ok(())
}
