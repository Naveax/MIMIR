use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,
    ReplayNetworkUniqueIdRemoteV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1, decode_replay_network_k2_v1,
    decode_replay_network_primitive_scalar_v1,
};
use std::{env, fs, path::Path};

#[derive(Debug, Clone, PartialEq, Eq)]
struct Semantic {
    active: String,
    actor: String,
    intv: String,
    uid_system: String,
    uid_local: String,
    uid_remote: String,
    uid_fp: String,
}

fn na_semantic() -> Semantic {
    Semantic {
        active: "na".to_owned(),
        actor: "na".to_owned(),
        intv: "na".to_owned(),
        uid_system: "na".to_owned(),
        uid_local: "na".to_owned(),
        uid_remote: "na".to_owned(),
        uid_fp: "na".to_owned(),
    }
}

fn mix(mut h: u64, bytes: &[u8]) -> u64 {
    for byte in bytes {
        h ^= u64::from(*byte);
        h = h.wrapping_mul(0x100000001b3);
    }
    h
}

fn uid_parts(value: &mimir_replay::ReplayNetworkUniqueIdV1) -> (&'static str, u64) {
    let mut h = 0xcbf29ce484222325u64;
    match &value.remote_id {
        ReplayNetworkUniqueIdRemoteV1::Steam { online_id } => {
            h = mix(h, &online_id.to_le_bytes());
            ("Steam", h)
        }
        ReplayNetworkUniqueIdRemoteV1::PlayStation {
            name,
            unknown,
            online_id,
        } => {
            h = mix(h, name.as_bytes());
            h = mix(h, unknown);
            h = mix(h, &online_id.to_le_bytes());
            ("PlayStation", h)
        }
        ReplayNetworkUniqueIdRemoteV1::PsyNet { online_id } => {
            h = mix(h, &online_id.to_le_bytes());
            ("PsyNet", h)
        }
        ReplayNetworkUniqueIdRemoteV1::Epic { account_id } => {
            h = mix(h, account_id.value.as_bytes());
            ("Epic", h)
        }
    }
}

fn k2ctx() -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version: 10,
        is_rl_223: false,
    }
}

fn k3ctx() -> ReplayNetworkK3DecodeContextV1 {
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

fn write_bits(bytes: &mut Vec<u8>, bit: &mut u64, value: u64, width: u64) -> Result<(), String> {
    for offset in 0..width {
        set_bit(bytes, *bit + offset, ((value >> offset) & 1) != 0)?;
    }
    *bit += width;
    Ok(())
}

fn write_u8(bytes: &mut Vec<u8>, bit: &mut u64, value: u8) -> Result<(), String> {
    write_bits(bytes, bit, u64::from(value), 8)
}

fn write_i32(bytes: &mut Vec<u8>, bit: &mut u64, value: i32) -> Result<(), String> {
    write_bits(bytes, bit, u64::from(value as u32), 32)
}

fn write_epic_unique_id(bytes: &mut Vec<u8>, start: u64) -> Result<u64, String> {
    let mut bit = start;
    write_u8(bytes, &mut bit, 11)?;
    write_i32(bytes, &mut bit, 33)?;
    for _ in 0..32 {
        write_u8(bytes, &mut bit, b'E')?;
    }
    write_u8(bytes, &mut bit, 0x55)?;
    write_u8(bytes, &mut bit, 4)?;
    if bit - start != 312 {
        return Err("Epic width mismatch".to_owned());
    }
    Ok(bit)
}

fn semantic_from_k2(value: &ReplayNetworkK2ValueV1) -> Result<Semantic, String> {
    match value {
        ReplayNetworkK2ValueV1::ActiveActor { active, actor } => {
            let mut out = na_semantic();
            out.active = if *active { "1" } else { "0" }.to_owned();
            out.actor = actor.to_string();
            Ok(out)
        }
        ReplayNetworkK2ValueV1::UniqueId(uid) => {
            let mut out = na_semantic();
            let (remote, fp) = uid_parts(uid);
            out.uid_system = uid.system_id.to_string();
            out.uid_local = uid.local_id.to_string();
            out.uid_remote = remote.to_owned();
            out.uid_fp = format!("{fp:016x}");
            Ok(out)
        }
        other => Err(format!("unexpected K2 value {other:?}")),
    }
}

fn semantic_from_published(
    value: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1,
) -> Result<Semantic, String> {
    match value {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::ActiveActor(decoded) => {
            semantic_from_k2(&decoded.value)
        }
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::Int(decoded) => {
            let mut out = na_semantic();
            match &decoded.value {
                ReplayNetworkPrimitiveScalarValueV1::Int(value) => {
                    out.intv = value.to_string();
                    Ok(out)
                }
                other => Err(format!("unexpected scalar value {other:?}")),
            }
        }
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::UniqueId(decoded) => {
            semantic_from_k2(&decoded.value)
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let request_path = env::args_os().nth(1).ok_or("missing target TSV")?;
    if env::args_os().nth(2).is_some() {
        return Err("unexpected extra argument".into());
    }
    let request = fs::read_to_string(request_path)?;
    let mut rows = 0usize;
    let mut repeat_ok = 0usize;
    let mut trunc_ok = 0usize;
    let mut wrong_ctx_ok = 0usize;
    let mut poison_ok = 0usize;
    let mut non_z_done = false;
    let mut epic_done = false;

    for line in request.lines().filter(|line| !line.trim().is_empty()) {
        rows += 1;
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() != 22 {
            return Err(format!("expected 22 fields, got {}", f.len()).into());
        }
        let label = f[0];
        let frame_index: usize = f[1].parse()?;
        let actor_ordinal: usize = f[2].parse()?;
        let actor_object: u32 = f[3].parse()?;
        let first_start: u64 = f[4].parse()?;
        let property_start: u64 = f[5].parse()?;
        let stream_start: u64 = f[6].parse()?;
        let stream_end: u64 = f[7].parse()?;
        let tag_name = f[8];
        let frozen_payload_start: u64 = f[9].parse()?;
        let frozen_payload_end: u64 = f[10].parse()?;
        let frozen_width: u64 = f[11].parse()?;
        let version_major: i32 = f[19].parse()?;
        let version_minor: i32 = f[20].parse()?;
        let net_version: i32 = f[21].parse()?;
        if version_major != 868 || version_minor != 32 || net_version != 10 {
            return Err(format!("{label}: frozen version drift").into());
        }

        let replay_bytes = fs::read(Path::new(label))?;
        let input = ReplayInput::Memory {
            label: label.to_owned(),
            bytes: replay_bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader.read_content_scaffold(&input)?;
        let ns = usize::try_from(scaffold.network_start)?;
        let ne = usize::try_from(scaffold.network_end)?;
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
            k2ctx(),
        )?;
        let prior = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network,
            &second,
            &plan,
            k3ctx(),
        )?;
        if prior.stop_bit != property_start {
            return Err(format!("{label}: prior stop {} != {property_start}", prior.stop_bit).into());
        }

        let published = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
            &network,
            &prior,
            &plan,
            k3ctx(),
        )?;
        let published_tag = published
            .header_composition
            .following_header
            .resolved_attribute_tag
            .ok_or("missing published tag")?;
        if format!("{published_tag:?}") != tag_name {
            return Err(format!("{label}: published tag drift").into());
        }
        let pub_sem = semantic_from_published(&published.following_payload)
            .map_err(std::io::Error::other)?;

        let (direct_start, direct_end, direct_width, direct_sem) = match published_tag {
            ReplayNetworkAttributeTagV1::ActiveActor | ReplayNetworkAttributeTagV1::UniqueId => {
                let direct = decode_replay_network_k2_v1(
                    &network,
                    frozen_payload_start,
                    published_tag,
                    k2ctx(),
                )?;
                let sem = semantic_from_k2(&direct.value).map_err(std::io::Error::other)?;
                (
                    direct.payload_start_bit,
                    direct.payload_end_bit,
                    direct.payload_width,
                    sem,
                )
            }
            ReplayNetworkAttributeTagV1::Int => {
                let direct = decode_replay_network_primitive_scalar_v1(
                    &network,
                    frozen_payload_start,
                    ReplayNetworkAttributeTagV1::Int,
                )?;
                let mut sem = na_semantic();
                match &direct.value {
                    ReplayNetworkPrimitiveScalarValueV1::Int(value) => sem.intv = value.to_string(),
                    other => return Err(format!("{label}: direct Int got {other:?}").into()),
                }
                (
                    direct.payload_start_bit,
                    direct.payload_end_bit,
                    u64::from(direct.payload_width),
                    sem,
                )
            }
            other => return Err(format!("{label}: unadmitted tag {other:?}").into()),
        };

        let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
            &network,
            &prior,
            &plan,
            k3ctx(),
        )? == published;
        if repeated {
            repeat_ok += 1;
        }

        let trunc_len = usize::try_from(frozen_payload_start / 8)?.min(network.len());
        let truncation = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
            &network[..trunc_len],
            &prior,
            &plan,
            k3ctx(),
        )
        .is_err();
        if truncation {
            trunc_ok += 1;
        }

        let wrong_context = ReplayNetworkK3DecodeContextV1 {
            version_major: 868,
            version_minor: 32,
            net_version: 10,
            is_rl_223: true,
        };
        let wrong_context_negative = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
            &network,
            &prior,
            &plan,
            wrong_context,
        )
        .is_err();
        if wrong_context_negative {
            wrong_ctx_ok += 1;
        }

        let mut poisoned = network.clone();
        for offset in 0..16u64 {
            set_bit(&mut poisoned, frozen_payload_end + offset, offset % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let post_payload_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
            &poisoned,
            &prior,
            &plan,
            k3ctx(),
        )? == published;
        if post_payload_poison {
            poison_ok += 1;
        }

        if !non_z_done {
            let mut rejected = false;
            for bit in stream_start..stream_end {
                let mut mutated = network.clone();
                let p = usize::try_from(bit)?;
                let current = ((mutated[p / 8] >> (p % 8)) & 1) != 0;
                set_bit(&mut mutated, bit, !current).map_err(std::io::Error::other)?;
                if decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
                    &mutated,
                    &prior,
                    &plan,
                    k3ctx(),
                )
                .is_err()
                {
                    rejected = true;
                    break;
                }
            }
            if !rejected {
                return Err(format!("{label}: unable to construct rejected non-Z header mutation").into());
            }
            println!("R3_18AE_NON_Z_NEGATIVE\tpass=1\tlabel={label}");
            non_z_done = true;
        }

        if published_tag == ReplayNetworkAttributeTagV1::UniqueId {
            let mut mutated = network.clone();
            let epic_end = write_epic_unique_id(&mut mutated, frozen_payload_start)
                .map_err(std::io::Error::other)?;
            if epic_end - frozen_payload_start != 312 {
                return Err("Epic synthetic width".into());
            }
            let lower = decode_replay_network_k2_v1(
                &mutated,
                frozen_payload_start,
                ReplayNetworkAttributeTagV1::UniqueId,
                k2ctx(),
            )?;
            let lower_valid = lower.payload_width == 312
                && matches!(
                    &lower.value,
                    ReplayNetworkK2ValueV1::UniqueId(uid)
                        if uid.system_id == 11
                            && matches!(&uid.remote_id, ReplayNetworkUniqueIdRemoteV1::Epic { .. })
                );
            let ad_rejects = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
                &mutated,
                &prior,
                &plan,
                k3ctx(),
            )
            .is_err();
            if !lower_valid || !ad_rejects {
                return Err("Epic lower-valid / AD-reject negative failed".into());
            }
            println!("R3_18AE_EPIC_NEGATIVE\tpass=1\tlabel={label}\twidth=312\tsystem=11\tremote=Epic");
            epic_done = true;
        }

        println!(
            "R3_18AE_ROW\tlabel={label}\tframe_index={frame_index}\tactor_ordinal={actor_ordinal}\tactor_context_object_id={actor_object}\tproperty_present_start_bit={property_start}\ttag={tag_name}\theader_stop_bit={}\tpublished_payload_start_bit={}\tpublished_payload_end_bit={}\tpublished_payload_width={}\tpublished_stop_bit={}\tdirect_payload_start_bit={direct_start}\tdirect_payload_end_bit={direct_end}\tdirect_payload_width={direct_width}\tpublished_active={}\tpublished_actor={}\tpublished_int={}\tpublished_uid_system={}\tpublished_uid_local={}\tpublished_uid_remote={}\tpublished_uid_fp={}\tdirect_active={}\tdirect_actor={}\tdirect_int={}\tdirect_uid_system={}\tdirect_uid_local={}\tdirect_uid_remote={}\tdirect_uid_fp={}\trepeatability={}\ttruncation={}\twrong_context={}\tpost_payload_poison={}\tanother_control_bits_consumed=0",
            published.header_composition.stop_bit,
            published.payload_start_bit,
            published.stop_bit,
            published.payload_width,
            published.stop_bit,
            pub_sem.active,
            pub_sem.actor,
            pub_sem.intv,
            pub_sem.uid_system,
            pub_sem.uid_local,
            pub_sem.uid_remote,
            pub_sem.uid_fp,
            direct_sem.active,
            direct_sem.actor,
            direct_sem.intv,
            direct_sem.uid_system,
            direct_sem.uid_local,
            direct_sem.uid_remote,
            direct_sem.uid_fp,
            u8::from(repeated),
            u8::from(truncation),
            u8::from(wrong_context_negative),
            u8::from(post_payload_poison),
        );

        if published.payload_start_bit != frozen_payload_start
            || published.stop_bit != frozen_payload_end
            || published.payload_width != frozen_width
            || direct_start != frozen_payload_start
            || direct_end != frozen_payload_end
            || direct_width != frozen_width
            || pub_sem != direct_sem
        {
            return Err(format!("{label}: immediate published/direct boundary mismatch").into());
        }
    }

    if rows != 47
        || repeat_ok != 47
        || trunc_ok != 47
        || wrong_ctx_ok != 47
        || poison_ok != 47
        || !non_z_done
        || !epic_done
    {
        return Err(format!(
            "aggregate fail rows={rows} repeat={repeat_ok} trunc={trunc_ok} wrong_ctx={wrong_ctx_ok} poison={poison_ok} non_z={non_z_done} epic={epic_done}"
        )
        .into());
    }
    println!(
        "R3_18AE_NATIVE_AGG\trows=47\trepeatability=47\ttruncation=47\twrong_context=47\tpost_payload_poison=47\tnon_z=1\tepic=1\tanother_control_bits_consumed=0"
    );
    Ok(())
}
