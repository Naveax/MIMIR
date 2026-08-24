use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
    decode_replay_network_primitive_scalar_v1,
};
use std::path::Path;

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

fn observe_one_bit(
    bytes: &[u8],
    start: u64,
    bit_limit: u64,
) -> Result<(u64, bool, u64), String> {
    let total_bits = u64::try_from(bytes.len())
        .map_err(|_| "network length conversion".to_owned())?
        .checked_mul(8)
        .ok_or_else(|| "network bit length overflow".to_owned())?;
    if start >= bit_limit || start >= total_bits {
        return Err(format!("control bit {start} outside bounded input"));
    }
    let position =
        usize::try_from(start).map_err(|_| "control bit position conversion".to_owned())?;
    let value = ((bytes[position / 8] >> (position % 8)) & 1) != 0;
    Ok((start, value, start + 1))
}

fn observe_after_exact_stop(
    bytes: &[u8],
    actual_stop: u64,
    expected_stop: u64,
    bit_limit: u64,
) -> Result<(u64, bool, u64), String> {
    if actual_stop != expected_stop {
        return Err(format!(
            "prior R3.18AN stop mismatch: actual {actual_stop}, expected {expected_stop}"
        ));
    }
    observe_one_bit(bytes, actual_stop, bit_limit)
}

fn set_bit(bytes: &mut [u8], position: u64, value: bool) {
    let Ok(position) = usize::try_from(position) else {
        return;
    };
    if position / 8 >= bytes.len() {
        return;
    }
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let targets_path = std::env::args()
        .nth(1)
        .ok_or("usage: _tmp_r318ap_probe <targets.tsv>")?;
    let targets = std::fs::read_to_string(targets_path)?;
    let mut rows = 0usize;

    for line in targets.lines() {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split('\t').collect();
        if fields.len() != 8 {
            return Err(format!("expected 8 target fields, got {}", fields.len()).into());
        }

        let label = fields[0];
        let frame_index: usize = fields[1].parse()?;
        let actor_ordinal: usize = fields[2].parse()?;
        let actor_object: u32 = fields[3].parse()?;
        let first_start: u64 = fields[4].parse()?;
        let expected_payload_start: u64 = fields[5].parse()?;
        let expected_payload_end: u64 = fields[6].parse()?;
        let expected_semantic_int: i32 = fields[7].parse()?;

        let replay_bytes = std::fs::read(Path::new(label))?;
        let input = ReplayInput::Memory {
            label: label.to_owned(),
            bytes: replay_bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader.read_content_scaffold(&input)?;
        let network_start = usize::try_from(scaffold.network_start)?;
        let network_end = usize::try_from(scaffold.network_end)?;
        let network = replay_bytes[network_start..network_end].to_vec();
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
        let following =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
                &network,
                &second,
                &plan,
                k3_context(),
            )?;
        let prior_ad =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
                &network,
                &following,
                &plan,
                k3_context(),
            )?;
        let control_ag =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
                &network,
                &prior_ad,
                k3_context(),
            )?;
        let published_an =
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
                &network,
                &prior_ad,
                &control_ag,
                &plan,
                k3_context(),
            )?;

        let semantic_int = match &published_an.following_payload.value {
            ReplayNetworkPrimitiveScalarValueV1::Int(value) => *value,
            other => return Err(format!("unexpected R3.18AN payload for {label}: {other:?}").into()),
        };
        let direct = decode_replay_network_primitive_scalar_v1(
            &network,
            expected_payload_start,
            ReplayNetworkAttributeTagV1::Int,
        )?;
        let published_exact = published_an.header_composition.stop_bit == expected_payload_start
            && published_an.following_payload.payload_start_bit == expected_payload_start
            && published_an.following_payload.payload_end_bit == expected_payload_end
            && published_an.following_payload.payload_width == 32
            && published_an.stop_bit == expected_payload_end
            && semantic_int == expected_semantic_int
            && published_an.following_payload == direct;
        if !published_exact {
            return Err(format!("published R3.18AN drift for {label}").into());
        }

        let bit_limit = u64::try_from(network.len())?
            .checked_mul(8)
            .ok_or("network bit length overflow")?;
        let first_observation = observe_after_exact_stop(
            &network,
            published_an.stop_bit,
            expected_payload_end,
            bit_limit,
        )?;
        let repeated = observe_after_exact_stop(
            &network,
            published_an.stop_bit,
            expected_payload_end,
            bit_limit,
        )?;
        if repeated != first_observation {
            return Err(format!("repeatability mismatch for {label}").into());
        }

        let truncation_negative =
            observe_one_bit(&network, published_an.stop_bit, published_an.stop_bit).is_err();
        let prior_stop_negative = observe_after_exact_stop(
            &network,
            published_an.stop_bit,
            expected_payload_end + 1,
            bit_limit,
        )
        .is_err();
        if !truncation_negative || !prior_stop_negative {
            return Err(format!("negative control failed for {label}").into());
        }

        let mut poisoned = network.clone();
        for offset in 0..16u64 {
            set_bit(
                &mut poisoned,
                first_observation.2 + offset,
                offset % 2 == 0,
            );
        }
        let after_poison = observe_after_exact_stop(
            &poisoned,
            published_an.stop_bit,
            expected_payload_end,
            bit_limit,
        )?;
        if after_poison != first_observation {
            return Err(format!("post-control poison changed observation for {label}").into());
        }

        let safe_label = label
            .replace('\t', "_")
            .replace('\r', "_")
            .replace('\n', "_");
        println!(
            "R3_18AP_NATIVE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tprior_an_stop={}\tcontrol_start={}\tcontrol_end={}\tcontrol_value={}\tpublished_an_exact=1\trepeatability=1\ttruncation_negative=1\tprior_stop_negative=1\tpost_control_poison=1\tnext_stream_bits=0\tnext_header_bits=0\tnext_payload_bits=0\tsecond_control_bits=0",
            safe_label,
            frame_index,
            actor_ordinal,
            actor_object,
            published_an.stop_bit,
            first_observation.0,
            first_observation.2,
            if first_observation.1 { 1 } else { 0 },
        );
        rows += 1;
    }

    if rows != 47 {
        return Err(format!("expected 47 rows, got {rows}").into());
    }
    println!("R3_18AP_NATIVE_PARSE=PASS rows=47");
    Ok(())
}
