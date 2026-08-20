use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,
    ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::{Path, PathBuf};

fn network_and_plan(path: &Path, label: &str) -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let replay_bytes = std::fs::read(path).expect("read replay");
    let input = ReplayInput::Memory {
        label: label.to_owned(),
        bytes: replay_bytes.clone(),
    };
    let scaffold = MinimalReplayContentScaffoldReader
        .read_content_scaffold(&input)
        .expect("content scaffold");
    let network = replay_bytes[usize::try_from(scaffold.network_start).unwrap()
        ..usize::try_from(scaffold.network_end).unwrap()]
        .to_vec();
    let plan = MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&input)
        .expect("lookup plan");
    (network, plan)
}

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

fn ad_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
    first_start: u64,
    actor_object: u32,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1{
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        network,
        first_start,
        actor_object,
        plan,
    )
    .expect("R3.18B first");
    let second =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            network,
            &first,
            plan,
            k2_context(),
        )
        .expect("R3.18J second");
    let t = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        network,
        &second,
        plan,
        k3_context(),
    )
    .expect("R3.18T payload");
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        network,
        &t,
        plan,
        k3_context(),
    )
    .expect("R3.18AD payload")
}

fn native_bit(network: &[u8], bit: u64) -> Option<bool> {
    let pos = usize::try_from(bit).ok()?;
    let byte = *network.get(pos / 8)?;
    Some(((byte >> (pos % 8)) & 1) != 0)
}

fn set_bit(bytes: &mut [u8], bit: u64, value: bool) {
    let pos = usize::try_from(bit).expect("bit position usize");
    let mask = 1u8 << (pos % 8);
    if value {
        bytes[pos / 8] |= mask;
    } else {
        bytes[pos / 8] &= !mask;
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 5 {
        eprintln!(
            "usage: r318ah_probe <root-relative replay> <first_start> <actor_object> <frozen_start>"
        );
        std::process::exit(2);
    }
    let label = &args[1];
    let first_start: u64 = args[2].parse().expect("first_start");
    let actor_object: u32 = args[3].parse().expect("actor_object");
    let frozen_start: u64 = args[4].parse().expect("frozen_start");
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
    let replay = root.join(label);
    let (network, plan) = network_and_plan(&replay, label);
    let prior = ad_prior(&network, &plan, first_start, actor_object);

    let published = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network,
        &prior,
        k3_context(),
    )
    .expect("published R3.18AG");
    let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network,
        &prior,
        k3_context(),
    )
    .expect("published R3.18AG repeat");
    let native = native_bit(&network, frozen_start).expect("native one-bit read");

    let mut false_network = network.clone();
    set_bit(&mut false_network, frozen_start, false);
    let false_reject = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &false_network,
        &prior,
        k3_context(),
    )
    .err()
    .map(|e| e.to_string().contains("unadmitted-false-control"))
    .unwrap_or(false);

    let bytes_before_control = usize::try_from(prior.stop_bit / 8).expect("prefix length");
    let trunc_reject = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network[..bytes_before_control],
        &prior,
        k3_context(),
    )
    .is_err();

    let mut poisoned = network.clone();
    let needed_bits = poisoned.len().saturating_mul(8);
    for offset in 0..16u64 {
        let bit = published.stop_bit.saturating_add(offset);
        if usize::try_from(bit).ok().is_some_and(|p| p < needed_bits) {
            set_bit(&mut poisoned, bit, offset % 2 == 0);
        }
    }
    let poison_same = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &poisoned,
        &prior,
        k3_context(),
    )
    .ok()
    .is_some_and(|x| x == published);

    let mut bad_stop = prior.clone();
    bad_stop.stop_bit = bad_stop.stop_bit.saturating_add(1);
    let prior_stop_reject = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network,
        &bad_stop,
        k3_context(),
    )
    .is_err();

    let wrong_context = ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: true,
    };
    let wrong_context_reject = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network,
        &prior,
        wrong_context,
    )
    .is_err();

    println!(
        "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        label,
        first_start,
        actor_object,
        frozen_start,
        prior.stop_bit,
        u8::from(published.following_property_present),
        published.property_present_start_bit,
        published.property_present_end_bit,
        published.stop_bit,
        u8::from(native),
        u8::from(repeated == published),
        u8::from(false_reject),
        u8::from(trunc_reject),
        u8::from(poison_same),
        u8::from(prior_stop_reject),
        u8::from(wrong_context_reject),
    );
}
