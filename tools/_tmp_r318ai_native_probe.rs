use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkK2DecodeContextV1,
    ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_first_property_header_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::{env, fs, path::Path};

macro_rules! ag_valid {
    ($x:expr, $prior:expr) => {
        $x.following_property_present
            && $x.property_present_start_bit == $prior.stop_bit
            && $x.property_present_end_bit == $x.property_present_start_bit + 1
            && $x.stop_bit == $x.property_present_end_bit
    };
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
    let mut header_n = 0usize;
    let mut repeat_n = 0usize;
    let mut trunc_n = 0usize;
    let mut corrupt_ag_n = 0usize;
    let mut wrong_actor_n = 0usize;
    let mut unresolved_n = 0usize;
    let mut wrong_context_n = 0usize;
    let mut poison_n = 0usize;

    for line in request.lines().filter(|x| !x.trim().is_empty()) {
        rows += 1;
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 9 {
            return Err(format!("expected 9 fields got {}", f.len()).into());
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
        let ctx = ReplayNetworkK3DecodeContextV1 {
            version_major: 868,
            version_minor: 32,
            net_version: 10,
            is_rl_223: false,
        };
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
            return Err(format!("{label}: AD stop drift {} expected {expected_ad_stop}", ad.stop_bit).into());
        }

        let ag = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network,
            &ad,
            ctx,
        )?;
        let ag_exact = ag_valid!(ag, ad)
            && ag.property_present_start_bit == expected_ag_start
            && ag.property_present_end_bit == expected_ag_end
            && ag.stop_bit == expected_ag_stop;
        if !ag_exact {
            return Err(format!("{label}: AG drift {ag:?}").into());
        }
        ag_exact_n += 1;

        let header = decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            ag.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        let stream_start = header.stream_id_start_bit.ok_or("missing stream start")?;
        let stream_end = header.stream_id_end_bit.ok_or("missing stream end")?;
        let stream_id = header.stream_id.ok_or("missing stream id")?;
        let stream_bound = header.stream_id_bound.ok_or("missing stream bound")?;
        let prop_bits = header.prop_id_bits.ok_or("missing prop bits")?;
        let property_object = header
            .resolved_property_object_index
            .ok_or("missing property object")?;
        let tag = header.resolved_attribute_tag.ok_or("missing attribute tag")?;
        let payload_start = header.payload_start_bit.ok_or("missing payload start")?;
        let header_exact = header.property_present
            && header.property_present_start_bit == ag.property_present_start_bit
            && header.property_present_end_bit == ag.stop_bit
            && stream_start == ag.stop_bit
            && stream_end > stream_start
            && payload_start == stream_end
            && header.stop_bit == payload_start;
        if !header_exact {
            return Err(format!("{label}: AI header boundary mismatch {header:?}").into());
        }
        header_n += 1;

        let repeated = decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            ag.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        let repeatability = repeated == header;
        if repeatability {
            repeat_n += 1;
        }

        let cut_bytes = usize::try_from(payload_start.saturating_sub(1) / 8)?.min(network.len());
        let trunc_header = decode_replay_network_existing_actor_first_property_header_v1(
            &network[..cut_bytes],
            ag.property_present_start_bit,
            actor_object,
            &plan,
        )
        .is_err();
        if trunc_header {
            trunc_n += 1;
        }

        let mut bad_start = ag.clone();
        bad_start.property_present_start_bit = bad_start.property_present_start_bit.saturating_add(1);
        let mut bad_end = ag.clone();
        bad_end.property_present_end_bit = bad_end.property_present_end_bit.saturating_add(1);
        let mut bad_stop = ag.clone();
        bad_stop.stop_bit = bad_stop.stop_bit.saturating_add(1);
        let mut bad_false = ag.clone();
        bad_false.following_property_present = false;
        let corrupt_ag_negative = !ag_valid!(bad_start, ad)
            && !ag_valid!(bad_end, ad)
            && !ag_valid!(bad_stop, ad)
            && !ag_valid!(bad_false, ad);
        if corrupt_ag_negative {
            corrupt_ag_n += 1;
        }

        let wrong_actor = decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            ag.property_present_start_bit,
            u32::MAX,
            &plan,
        )
        .is_err();
        if wrong_actor {
            wrong_actor_n += 1;
        }

        let mut unresolved_plan = plan.clone();
        let unresolved_lookup = if let Some(slot) = unresolved_plan
            .object_lookups
            .get_mut(usize::try_from(actor_object)?)
            .and_then(Option::as_mut)
        {
            slot.properties.retain(|property| property.stream_id != stream_id);
            decode_replay_network_existing_actor_first_property_header_v1(
                &network,
                ag.property_present_start_bit,
                actor_object,
                &unresolved_plan,
            )
            .is_err()
        } else {
            true
        };
        if unresolved_lookup {
            unresolved_n += 1;
        }

        let wrong_context = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network,
            &second,
            &plan,
            ReplayNetworkK3DecodeContextV1 {
                version_major: 868,
                version_minor: 31,
                net_version: 10,
                is_rl_223: false,
            },
        )
        .is_err();
        if wrong_context {
            wrong_context_n += 1;
        }

        let mut poisoned = network.clone();
        for off in 0..16u64 {
            set_bit(&mut poisoned, payload_start + off, off % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let poisoned_header = decode_replay_network_existing_actor_first_property_header_v1(
            &poisoned,
            ag.property_present_start_bit,
            actor_object,
            &plan,
        )?;
        let poison = poisoned_header == header;
        if poison {
            poison_n += 1;
        }

        println!(
            "R3_18AI_NATIVE\tlabel={label}\tframe_index={frame}\tactor_ordinal={actor_ordinal}\tactor_context_object_id={actor_object}\tag_start={}\tag_end={}\tag_stop={}\tpresent_start={}\tpresent_end={}\tstream_start={stream_start}\tstream_end={stream_end}\tstream_id={stream_id}\tstream_bound={stream_bound}\tprop_bits={prop_bits}\tproperty_object={property_object}\ttag={tag:?}\tversion_major=868\tversion_minor=32\tnet_version=10\tpayload_start={payload_start}\theader_stop={}\tag_exact={}\trepeatability={}\ttrunc_header={}\tcorrupt_ag_negative={}\twrong_actor_negative={}\tunresolved_lookup_negative={}\twrong_context_negative={}\tpost_payload_poison={}\tfollowing_payload_bits_consumed=0\tsecond_later_control_bits_consumed=0",
            ag.property_present_start_bit,
            ag.property_present_end_bit,
            ag.stop_bit,
            header.property_present_start_bit,
            header.property_present_end_bit,
            header.stop_bit,
            u8::from(ag_exact),
            u8::from(repeatability),
            u8::from(trunc_header),
            u8::from(corrupt_ag_negative),
            u8::from(wrong_actor),
            u8::from(unresolved_lookup),
            u8::from(wrong_context),
            u8::from(poison),
        );
    }

    if rows != 47
        || ag_exact_n != 47
        || header_n != 47
        || repeat_n != 47
        || trunc_n != 47
        || corrupt_ag_n != 47
        || wrong_actor_n != 47
        || unresolved_n != 47
        || wrong_context_n != 47
        || poison_n != 47
    {
        return Err(format!(
            "R3.18AI aggregate failure rows={rows} ag={ag_exact_n} header={header_n} repeat={repeat_n} trunc={trunc_n} corrupt_ag={corrupt_ag_n} wrong_actor={wrong_actor_n} unresolved={unresolved_n} wrong_context={wrong_context_n} poison={poison_n}"
        )
        .into());
    }

    println!(
        "R3_18AI_NATIVE_AGG\trows=47\tag_exact=47\theader_exact=47\trepeatability=47\ttrunc_header=47\tcorrupt_ag_negative=47\twrong_actor_negative=47\tunresolved_lookup_negative=47\twrong_context_negative=47\tpost_payload_poison=47\tfollowing_payload_bits_consumed=0\tsecond_later_control_bits_consumed=0"
    );
    Ok(())
}
