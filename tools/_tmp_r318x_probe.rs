use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkK2DecodeContextV1,
    ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
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
    let mut t_exact_count = 0usize;
    let mut exact_count = 0usize;
    let mut trunc_count = 0usize;
    let mut false_count = 0usize;
    let mut prior_count = 0usize;
    let mut repeat_count = 0usize;
    let mut poison_count = 0usize;

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
        let expected_t_stop: u64 = f[5].parse()?;
        let expected_start: u64 = f[6].parse()?;
        let expected_end: u64 = f[7].parse()?;
        let expected_value: u8 = f[8].parse()?;

        let replay_bytes = fs::read(Path::new(label))?;
        let input = ReplayInput::Memory {
            label: label.to_owned(),
            bytes: replay_bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader.read_content_scaffold(&input)?;
        let ns = usize::try_from(scaffold.network_start)?;
        let ne = usize::try_from(scaffold.network_end)?;
        if ns > ne || ne > replay_bytes.len() {
            return Err(format!("{label}: bad network slice").into());
        }
        let network = replay_bytes[ns..ne].to_vec();
        let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;

        let first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &network,
            first_start,
            actor_object,
            &plan,
        )?;
        let j = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &network,
            &first,
            &plan,
            ReplayNetworkK2DecodeContextV1 {
                net_version: 10,
                is_rl_223: false,
            },
        )?;
        let t = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network,
            &j,
            &plan,
            ReplayNetworkK3DecodeContextV1 {
                version_major: 868,
                version_minor: 32,
                net_version: 10,
                is_rl_223: false,
            },
        )?;
        let t_exact = t.stop_bit == expected_t_stop && expected_t_stop == expected_start;
        if !t_exact {
            return Err(format!(
                "{label}: published T stop mismatch got {} expected {expected_t_stop}",
                t.stop_bit
            )
            .into());
        }
        t_exact_count += 1;

        let w = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
            &network, &t,
        )?;
        let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
            &network, &t,
        )?;
        let repeat = w == repeated;
        if repeat {
            repeat_count += 1;
        }
        let exact = w.following_property_present
            && expected_value == 1
            && w.property_present_start_bit == expected_start
            && w.property_present_end_bit == expected_end
            && w.stop_bit == expected_end
            && expected_end == expected_start + 1;
        if !exact {
            return Err(format!("{label}: published W control mismatch {w:?}").into());
        }
        exact_count += 1;

        let trunc_bytes = usize::try_from(expected_start / 8)?.min(network.len());
        let truncation = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
            &network[..trunc_bytes], &t,
        )
        .is_err();
        if truncation {
            trunc_count += 1;
        }

        let mut false_network = network.clone();
        set_bit(&mut false_network, expected_start, false).map_err(std::io::Error::other)?;
        let false_rejection = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
            &false_network, &t,
        )
        .is_err_and(|e| e.to_string().contains("unadmitted-false-control"));
        if false_rejection {
            false_count += 1;
        }

        let mut bad = t.clone();
        bad.stop_bit = bad.stop_bit.checked_add(1).ok_or("stop overflow")?;
        let prior_rejection = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
            &network, &bad,
        )
        .is_err();
        if prior_rejection {
            prior_count += 1;
        }

        let mut poisoned = network.clone();
        for off in 0..16u64 {
            set_bit(&mut poisoned, w.stop_bit + off, off % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let poison_same = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
            &poisoned, &t,
        )? == w;
        if poison_same {
            poison_count += 1;
        }

        println!(
            "R3_18X_NATIVE\tlabel={label}\tframe_index={frame}\tactor_ordinal={actor_ordinal}\tactor_context_object_id={actor_object}\tt_stop={}\tcontrol_start={}\tcontrol_end={}\tcontrol_stop={}\tcontrol_value={}\tpublished_t_exact={}\tw_exact={}\trepeatability={}\ttruncation={}\tfalse_rejection={}\tprior_boundary_rejection={}\tpost_stop_poison={}\tnext_stream_bits_consumed=0\tnext_header_bits_consumed=0\tnext_payload_bits_consumed=0\tsecond_later_control_bits_consumed=0",
            t.stop_bit,
            w.property_present_start_bit,
            w.property_present_end_bit,
            w.stop_bit,
            u8::from(w.following_property_present),
            u8::from(t_exact),
            u8::from(exact),
            u8::from(repeat),
            u8::from(truncation),
            u8::from(false_rejection),
            u8::from(prior_rejection),
            u8::from(poison_same),
        );
    }

    if rows != 47
        || t_exact_count != 47
        || exact_count != 47
        || trunc_count != 47
        || false_count != 47
        || prior_count != 47
        || repeat_count != 47
        || poison_count != 47
    {
        return Err(format!(
            "aggregate fail rows={rows} t={t_exact_count} exact={exact_count} trunc={trunc_count} false={false_count} prior={prior_count} repeat={repeat_count} poison={poison_count}"
        )
        .into());
    }

    println!(
        "R3_18X_NATIVE_AGG\trows=47\tpublished_t_exact=47\tw_exact=47\trepeatability=47\ttruncation=47\tfalse_rejection=47\tprior_boundary_rejection=47\tpost_stop_poison=47\tnext_stream_bits_consumed=0\tnext_header_bits_consumed=0\tnext_payload_bits_consumed=0\tsecond_later_control_bits_consumed=0"
    );
    Ok(())
}
