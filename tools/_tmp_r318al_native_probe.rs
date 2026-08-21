use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_first_property_header_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::{env, fs, path::Path};

fn k2_context() -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version: 10,
        is_rl_223: false,
    }
}

fn k3_context() -> ReplayNetworkK3DecodeContextV1 {
    ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: false,
    }
}

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
    let mut ag_exact_n = 0usize;
    let mut ak_exact_n = 0usize;
    let mut direct_exact_n = 0usize;
    let mut repeat_n = 0usize;
    let mut trunc_n = 0usize;
    let mut corrupt_ag_n = 0usize;
    let mut wrong_actor_n = 0usize;
    let mut unresolved_n = 0usize;
    let mut wrong_context_n = 0usize;
    let mut poison_n = 0usize;
    let mut cartesian_negative = false;
    let mut fabricated_negative = false;
    let mut old_z_negative = false;

    for line in request.lines().filter(|x| !x.trim().is_empty()) {
        rows += 1;
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 20 {
            return Err(format!("expected 20 fields got {}", f.len()).into());
        }
        let label = f[0];
        let frame: usize = f[1].parse()?;
        let actor_ordinal: usize = f[2].parse()?;
        let actor_object: u32 = f[3].parse()?;
        let first_start: u64 = f[4].parse()?;
        let expected_ad_stop: u64 = f[5].parse()?;
        let expected_ag_start: u64 = f[6].parse()?;
        let expected_ag_end: u64 = f[7].parse()?;
        let expected_ag_stop: u64 = f[8].parse()?;
        let expected_present_start: u64 = f[9].parse()?;
        let expected_present_end: u64 = f[10].parse()?;
        let expected_stream_start: u64 = f[11].parse()?;
        let expected_stream_end: u64 = f[12].parse()?;
        let expected_stream_id: u32 = f[13].parse()?;
        let expected_stream_bound: u32 = f[14].parse()?;
        let expected_prop_bits: u32 = f[15].parse()?;
        let expected_property_object: u32 = f[16].parse()?;
        let expected_tag = f[17];
        let expected_payload_start: u64 = f[18].parse()?;
        let expected_header_stop: u64 = f[19].parse()?;

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
        let second =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
                &network,
                &first,
                &plan,
                k2_context(),
            )?;
        let ctx = k3_context();
        let t = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network,
            &second,
            &plan,
            ctx,
        )?;
        let ad = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
            &network,
            &t,
            &plan,
            ctx,
        )?;
        if ad.stop_bit != expected_ad_stop || expected_ad_stop != expected_ag_start {
            return Err(format!(
                "{label}: AD stop drift {} expected {expected_ad_stop}",
                ad.stop_bit
            )
            .into());
        }

        let ag = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &ad,
            ctx,
        )?;
        let ag_exact = ag.following_property_present
            && ag.property_present_start_bit == expected_ag_start
            && ag.property_present_end_bit == expected_ag_end
            && ag.stop_bit == expected_ag_stop
            && ag.property_present_end_bit == ag.property_present_start_bit + 1
            && ag.stop_bit == ag.property_present_end_bit;
        if !ag_exact {
            return Err(format!("{label}: AG drift {ag:?}").into());
        }
        ag_exact_n += 1;

        let ak = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &ad,
            &ag,
            &plan,
            ctx,
        )?;
        let header = &ak.following_header;
        let tag = header.resolved_attribute_tag.ok_or("missing attribute tag")?;
        let stream_start = header.stream_id_start_bit.ok_or("missing stream start")?;
        let stream_end = header.stream_id_end_bit.ok_or("missing stream end")?;
        let stream_id = header.stream_id.ok_or("missing stream id")?;
        let stream_bound = header.stream_id_bound.ok_or("missing stream bound")?;
        let prop_bits = header.prop_id_bits.ok_or("missing prop bits")?;
        let property_object = header
            .resolved_property_object_index
            .ok_or("missing property object")?;
        let payload_start = header.payload_start_bit.ok_or("missing payload start")?;

        let ak_exact = ak.control == ag
            && header.property_present
            && header.property_present_start_bit == expected_present_start
            && header.property_present_end_bit == expected_present_end
            && stream_start == expected_stream_start
            && stream_end == expected_stream_end
            && stream_id == expected_stream_id
            && stream_bound == expected_stream_bound
            && prop_bits == expected_prop_bits
            && property_object == expected_property_object
            && format!("{tag:?}") == expected_tag
            && payload_start == expected_payload_start
            && header.stop_bit == expected_header_stop
            && ak.stop_bit == expected_payload_start
            && expected_header_stop == expected_payload_start;
        if !ak_exact {
            return Err(format!("{label}: AK drift {ak:?}").into());
        }
        ak_exact_n += 1;

        let direct = decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            ag.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        let direct_exact = direct == ak.following_header;
        if !direct_exact {
            return Err(format!("{label}: direct header differs from AK").into());
        }
        direct_exact_n += 1;

        let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &ad,
            &ag,
            &plan,
            ctx,
        )?;
        let repeatability = repeated == ak;
        if repeatability {
            repeat_n += 1;
        }

        let cut_bytes =
            usize::try_from(expected_payload_start.saturating_sub(1) / 8)?.min(network.len());
        let truncation = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network[..cut_bytes],
            &ad,
            &ag,
            &plan,
            ctx,
        )
        .is_err();
        if truncation {
            trunc_n += 1;
        }

        let mut bad_ag = ag.clone();
        bad_ag.stop_bit = bad_ag.stop_bit.saturating_add(1);
        let corrupt_ag = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &ad,
            &bad_ag,
            &plan,
            ctx,
        )
        .is_err();
        if corrupt_ag {
            corrupt_ag_n += 1;
        }

        let mut bad_prior = ad.clone();
        bad_prior.header_composition.following_header.actor_object_index = u32::MAX;
        let wrong_actor = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &bad_prior,
            &ag,
            &plan,
            ctx,
        )
        .is_err();
        if wrong_actor {
            wrong_actor_n += 1;
        }

        let mut unresolved_plan = plan.clone();
        if let Some(slot) = unresolved_plan
            .object_lookups
            .get_mut(usize::try_from(actor_object)?)
        {
            *slot = None;
        }
        let unresolved = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &ad,
            &ag,
            &unresolved_plan,
            ctx,
        )
        .is_err();
        if unresolved {
            unresolved_n += 1;
        }

        let wrong_ctx = ReplayNetworkK3DecodeContextV1 {
            version_major: 868,
            version_minor: 31,
            net_version: 10,
            is_rl_223: false,
        };
        let wrong_context = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network,
            &ad,
            &ag,
            &plan,
            wrong_ctx,
        )
        .is_err();
        if wrong_context {
            wrong_context_n += 1;
        }

        let mut poisoned = network.clone();
        for off in 0..16u64 {
            set_bit(&mut poisoned, expected_payload_start + off, off % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let poisoned_ak = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &poisoned,
            &ad,
            &ag,
            &plan,
            ctx,
        )?;
        let poison = poisoned_ak == ak;
        if poison {
            poison_n += 1;
        }

        if label.ends_with("003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay") {
            for (object_index, mutated_tag, target) in [
                (68, ReplayNetworkAttributeTagV1::Int, "cartesian"),
                (39, ReplayNetworkAttributeTagV1::Int, "fabricated"),
                (34, ReplayNetworkAttributeTagV1::ActiveActor, "old_z"),
            ] {
                let mut widened = plan.clone();
                let property = widened.object_lookups[usize::try_from(actor_object)?]
                    .as_mut()
                    .ok_or("missing representative actor lookup")?
                    .properties
                    .iter_mut()
                    .find(|property| property.stream_id == expected_stream_id)
                    .ok_or("missing representative stream")?;
                property.object_index = object_index;
                property.tag = mutated_tag;
                let rejected = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
                    &network,
                    &ad,
                    &ag,
                    &widened,
                    ctx,
                )
                .is_err();
                match target {
                    "cartesian" => cartesian_negative = rejected,
                    "fabricated" => fabricated_negative = rejected,
                    "old_z" => old_z_negative = rejected,
                    _ => unreachable!(),
                }
            }
        }

        println!(
            "R3_18AL_NATIVE\tlabel={label}\tframe_index={frame}\tactor_ordinal={actor_ordinal}\tactor_context_object_id={actor_object}\tag_start={}\tag_end={}\tag_stop={}\tpresent_start={}\tpresent_end={}\tstream_start={stream_start}\tstream_end={stream_end}\tstream_id={stream_id}\tstream_bound={stream_bound}\tprop_bits={prop_bits}\tproperty_object={property_object}\ttag={tag:?}\tversion_major=868\tversion_minor=32\tnet_version=10\tpayload_start={payload_start}\theader_stop={}\tak_stop={}\tag_exact={}\tak_exact={}\tdirect_exact={}\trepeatability={}\ttruncation={}\tcorrupt_ag_negative={}\twrong_actor_negative={}\tunresolved_lookup_negative={}\twrong_context_negative={}\tpost_payload_poison={}\tfollowing_payload_bits_consumed=0\tsecond_later_control_bits_consumed=0",
            ag.property_present_start_bit,
            ag.property_present_end_bit,
            ag.stop_bit,
            header.property_present_start_bit,
            header.property_present_end_bit,
            header.stop_bit,
            ak.stop_bit,
            u8::from(ag_exact),
            u8::from(ak_exact),
            u8::from(direct_exact),
            u8::from(repeatability),
            u8::from(truncation),
            u8::from(corrupt_ag),
            u8::from(wrong_actor),
            u8::from(unresolved),
            u8::from(wrong_context),
            u8::from(poison),
        );
    }

    if rows != 47
        || ag_exact_n != 47
        || ak_exact_n != 47
        || direct_exact_n != 47
        || repeat_n != 47
        || trunc_n != 47
        || corrupt_ag_n != 47
        || wrong_actor_n != 47
        || unresolved_n != 47
        || wrong_context_n != 47
        || poison_n != 47
        || !cartesian_negative
        || !fabricated_negative
        || !old_z_negative
    {
        return Err(format!(
            "R3.18AL aggregate failure rows={rows} ag={ag_exact_n} ak={ak_exact_n} direct={direct_exact_n} repeat={repeat_n} trunc={trunc_n} corrupt_ag={corrupt_ag_n} wrong_actor={wrong_actor_n} unresolved={unresolved_n} wrong_context={wrong_context_n} poison={poison_n} cartesian={cartesian_negative} fabricated={fabricated_negative} old_z={old_z_negative}"
        )
        .into());
    }

    println!(
        "R3_18AL_NATIVE_AGG\trows=47\tag_exact=47\tak_exact=47\tdirect_exact=47\trepeatability=47\ttruncation=47\tcorrupt_ag_negative=47\twrong_actor_negative=47\tunresolved_lookup_negative=47\twrong_context_negative=47\tpost_payload_poison=47\tcartesian_negative=1\tfabricated_negative=1\told_z_negative=1\tfollowing_payload_bits_consumed=0\tsecond_later_control_bits_consumed=0"
    );
    Ok(())
}
