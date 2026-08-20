use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkK2DecodeContextV1,
    ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
};
use std::path::Path;

fn k2_context() -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 { net_version: 10, is_rl_223: false }
}

fn k3_context() -> ReplayNetworkK3DecodeContextV1 {
    ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: false,
    }
}

fn observe_one_bit(bytes: &[u8], start: u64, bit_limit: u64) -> Result<bool, String> {
    if start >= bit_limit {
        return Err(format!("control bit {start} is outside evidence bit limit {bit_limit}"));
    }
    let total = u64::try_from(bytes.len()).map_err(|_| "network length conversion".to_owned())? * 8;
    if start >= total {
        return Err(format!("control bit {start} is outside network bits {total}"));
    }
    let p = usize::try_from(start).map_err(|_| "control bit position conversion".to_owned())?;
    Ok(((bytes[p / 8] >> (p % 8)) & 1) != 0)
}

fn observe_after_exact_stop(
    bytes: &[u8], actual_stop: u64, expected_stop: u64, bit_limit: u64,
) -> Result<bool, String> {
    if actual_stop != expected_stop {
        return Err(format!("prior R3.18AD stop mismatch: actual {actual_stop}, expected {expected_stop}"));
    }
    observe_one_bit(bytes, actual_stop, bit_limit)
}

fn set_bit(bytes: &mut [u8], position: u64, value: bool) {
    let p = usize::try_from(position).expect("bit position");
    if p / 8 >= bytes.len() { return; }
    if value { bytes[p / 8] |= 1 << (p % 8); }
    else { bytes[p / 8] &= !(1 << (p % 8)); }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let target_path = std::env::args().nth(1).ok_or("usage: _tmp_r318af_probe <targets.tsv>")?;
    let targets = std::fs::read_to_string(target_path)?;
    let mut rows = 0usize;
    for line in targets.lines() {
        if line.trim().is_empty() { continue; }
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 9 { return Err(format!("expected 9 target fields, got {}", f.len()).into()); }
        let label = f[0];
        let frame_index: usize = f[1].parse()?;
        let actor_ordinal: usize = f[2].parse()?;
        let actor_object: u32 = f[3].parse()?;
        let first_start: u64 = f[4].parse()?;
        let expected_payload_start: u64 = f[5].parse()?;
        let expected_payload_end: u64 = f[6].parse()?;
        let expected_width: u64 = f[7].parse()?;
        let expected_tag = f[8];

        let replay_bytes = std::fs::read(Path::new(label))?;
        let input = ReplayInput::Memory { label: label.to_owned(), bytes: replay_bytes.clone() };
        let scaffold = MinimalReplayContentScaffoldReader.read_content_scaffold(&input)?;
        let ns = usize::try_from(scaffold.network_start)?;
        let ne = usize::try_from(scaffold.network_end)?;
        let network = replay_bytes[ns..ne].to_vec();
        let plan = MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input)?;

        let first = decode_replay_network_existing_actor_single_primitive_property_v1(
            &network, first_start, actor_object, &plan,
        )?;
        let second = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &network, &first, &plan, k2_context(),
        )?;
        let prior = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network, &second, &plan, k3_context(),
        )?;
        let published = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
            &network, &prior, &plan, k3_context(),
        )?;

        let actual_tag = match &published.following_payload {
            ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::ActiveActor(_) => "ActiveActor",
            ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::Int(_) => "Int",
            ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::UniqueId(_) => "UniqueId",
        };
        let published_exact = published.payload_start_bit == expected_payload_start
            && published.payload_width == expected_width
            && published.stop_bit == expected_payload_end
            && published.header_composition.stop_bit == expected_payload_start
            && actual_tag == expected_tag;
        if !published_exact {
            return Err(format!("published AD drift for {label}").into());
        }

        let bit_limit = u64::try_from(network.len())? * 8;
        let control = observe_after_exact_stop(&network, published.stop_bit, expected_payload_end, bit_limit)?;
        let repeated = observe_after_exact_stop(&network, published.stop_bit, expected_payload_end, bit_limit)? == control;
        let truncation = observe_one_bit(&network, published.stop_bit, published.stop_bit).is_err();
        let prior_stop_negative = observe_after_exact_stop(
            &network, published.stop_bit, expected_payload_end + 1, bit_limit,
        ).is_err();
        let control_end = published.stop_bit + 1;
        let mut poisoned = network.clone();
        for offset in 0..16u64 {
            set_bit(&mut poisoned, control_end + offset, offset % 2 == 0);
        }
        let poison_ok = observe_after_exact_stop(&poisoned, published.stop_bit, expected_payload_end, bit_limit)? == control;
        let safe_label = label.replace('\t', "_").replace('\r', "_").replace('\n', "_");

        println!(
            "R3_18AF_NATIVE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tprior_ad_stop={}\tcontrol_start={}\tcontrol_end={}\tcontrol_value={}\tpublished_ad_exact=1\trepeatability={}\ttruncation={}\tprior_stop_mismatch_negative={}\tpost_control_poison={}\tnext_stream_bits_consumed=0\tnext_header_bits_consumed=0\tnext_payload_bits_consumed=0\tsecond_later_control_bits_consumed=0",
            safe_label, frame_index, actor_ordinal, actor_object,
            published.stop_bit, published.stop_bit, control_end, if control { 1 } else { 0 },
            if repeated { 1 } else { 0 }, if truncation { 1 } else { 0 },
            if prior_stop_negative { 1 } else { 0 }, if poison_ok { 1 } else { 0 },
        );
        rows += 1;
    }
    if rows != 47 { return Err(format!("expected 47 rows, got {rows}").into()); }
    println!("R3_18AF_NATIVE_PARSE=PASS rows=47");
    Ok(())
}
