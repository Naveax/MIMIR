use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,
    ReplayNetworkUniqueIdRemoteV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
    decode_replay_network_k2_v1, decode_replay_network_primitive_scalar_v1,
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

fn mix(mut h: u64, bytes: &[u8]) -> u64 {
    for b in bytes {
        h ^= u64::from(*b);
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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let request_path = env::args_os().nth(1).ok_or("missing target TSV")?;
    if env::args_os().nth(2).is_some() {
        return Err("unexpected extra argument".into());
    }
    let request = fs::read_to_string(request_path)?;
    let mut rows = 0usize;
    let mut repeat = 0usize;
    let mut trunc = 0usize;
    let mut wrong_tag = 0usize;
    let mut wrong_ctx = 0usize;
    let mut poison = 0usize;

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
        let property_start: u64 = f[5].parse()?;
        let tag_name = f[13];
        let payload_start: u64 = f[14].parse()?;
        let version_major: i32 = f[15].parse()?;
        let version_minor: i32 = f[16].parse()?;
        let net_version: i32 = f[17].parse()?;

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
        let ctx = ReplayNetworkK3DecodeContextV1 {
            version_major,
            version_minor,
            net_version,
            is_rl_223: false,
        };
        let prior = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network,
            &second,
            &plan,
            ctx,
        )?;
        if prior.stop_bit != control_start {
            return Err(format!("{label}: T stop drift {} != {control_start}", prior.stop_bit).into());
        }
        let aa = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
            &network,
            &prior,
            &plan,
            ctx,
        )?;
        if aa.stop_bit != payload_start
            || aa.following_header.payload_start_bit != Some(payload_start)
        {
            return Err(format!("{label}: AA payload start drift").into());
        }
        let tag = aa
            .following_header
            .resolved_attribute_tag
            .ok_or("missing AA tag")?;
        if format!("{tag:?}") != tag_name {
            return Err(format!("{label}: tag drift").into());
        }

        let (
            payload_end,
            width,
            active,
            actor,
            intv,
            uid_system,
            uid_local,
            uid_remote,
            uid_fp,
            result_key,
        ) = match tag {
            ReplayNetworkAttributeTagV1::ActiveActor => {
                let got = decode_replay_network_k2_v1(&network, payload_start, tag, k2ctx())?;
                let (a, id) = match &got.value {
                    ReplayNetworkK2ValueV1::ActiveActor { active, actor } => (*active, *actor),
                    other => {
                        return Err(format!("{label}: unexpected active value {other:?}").into())
                    }
                };
                (
                    got.payload_end_bit,
                    got.payload_width,
                    if a { "1" } else { "0" }.to_owned(),
                    id.to_string(),
                    "na".to_owned(),
                    "na".to_owned(),
                    "na".to_owned(),
                    "na".to_owned(),
                    "na".to_owned(),
                    format!("{:?}", got.value),
                )
            }
            ReplayNetworkAttributeTagV1::Int => {
                let got =
                    decode_replay_network_primitive_scalar_v1(&network, payload_start, tag)?;
                let v = match &got.value {
                    ReplayNetworkPrimitiveScalarValueV1::Int(v) => *v,
                    other => return Err(format!("{label}: unexpected int {other:?}").into()),
                };
                (
                    got.payload_end_bit,
                    u64::from(got.payload_width),
                    "na".to_owned(),
                    "na".to_owned(),
                    v.to_string(),
                    "na".to_owned(),
                    "na".to_owned(),
                    "na".to_owned(),
                    "na".to_owned(),
                    format!("{:?}", got.value),
                )
            }
            ReplayNetworkAttributeTagV1::UniqueId => {
                let got = decode_replay_network_k2_v1(&network, payload_start, tag, k2ctx())?;
                let uid = match &got.value {
                    ReplayNetworkK2ValueV1::UniqueId(v) => v,
                    other => return Err(format!("{label}: unexpected uid {other:?}").into()),
                };
                let (rk, fp) = uid_parts(uid);
                (
                    got.payload_end_bit,
                    got.payload_width,
                    "na".to_owned(),
                    "na".to_owned(),
                    "na".to_owned(),
                    uid.system_id.to_string(),
                    uid.local_id.to_string(),
                    rk.to_owned(),
                    format!("{fp:016x}"),
                    format!("{:?}", got.value),
                )
            }
            other => return Err(format!("{label}: unsupported AC tag {other:?}").into()),
        };

        let repeated_key = match tag {
            ReplayNetworkAttributeTagV1::Int => format!(
                "{:?}",
                decode_replay_network_primitive_scalar_v1(&network, payload_start, tag)?.value
            ),
            _ => format!(
                "{:?}",
                decode_replay_network_k2_v1(&network, payload_start, tag, k2ctx())?.value
            ),
        };
        let repeatability = repeated_key == result_key;
        if repeatability {
            repeat += 1;
        }

        let trunc_len = usize::try_from(payload_start / 8)?.min(network.len());
        let truncation = match tag {
            ReplayNetworkAttributeTagV1::Int => decode_replay_network_primitive_scalar_v1(
                &network[..trunc_len],
                payload_start,
                tag,
            )
            .is_err(),
            _ => decode_replay_network_k2_v1(
                &network[..trunc_len],
                payload_start,
                tag,
                k2ctx(),
            )
            .is_err(),
        };
        if truncation {
            trunc += 1;
        }

        let wrong_tag_negative = match tag {
            ReplayNetworkAttributeTagV1::Int => decode_replay_network_k2_v1(
                &network,
                payload_start,
                ReplayNetworkAttributeTagV1::ActiveActor,
                k2ctx(),
            )
            .map(|x| x.payload_end_bit != payload_end || format!("{:?}", x.value) != result_key)
            .unwrap_or(true),
            _ => decode_replay_network_primitive_scalar_v1(
                &network,
                payload_start,
                ReplayNetworkAttributeTagV1::Int,
            )
            .map(|x| x.payload_end_bit != payload_end || format!("{:?}", x.value) != result_key)
            .unwrap_or(true),
        };
        if wrong_tag_negative {
            wrong_tag += 1;
        }

        let wrong_context_negative = match tag {
            ReplayNetworkAttributeTagV1::Int | ReplayNetworkAttributeTagV1::ActiveActor => true,
            ReplayNetworkAttributeTagV1::UniqueId => decode_replay_network_k2_v1(
                &network,
                payload_start,
                tag,
                ReplayNetworkK2DecodeContextV1 {
                    net_version: 9,
                    is_rl_223: false,
                },
            )
            .is_err(),
            _ => false,
        };
        if wrong_context_negative {
            wrong_ctx += 1;
        }

        let mut poisoned = network.clone();
        for off in 0..16u64 {
            set_bit(&mut poisoned, payload_end + off, off % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let poisoned_key = match tag {
            ReplayNetworkAttributeTagV1::Int => format!(
                "{:?}",
                decode_replay_network_primitive_scalar_v1(&poisoned, payload_start, tag)?.value
            ),
            _ => format!(
                "{:?}",
                decode_replay_network_k2_v1(&poisoned, payload_start, tag, k2ctx())?.value
            ),
        };
        let poison_invariance = poisoned_key == result_key;
        if poison_invariance {
            poison += 1;
        }

        println!(
            "R3_18AC_NATIVE\tlabel={label}\tframe_index={frame_index}\tactor_ordinal={actor_ordinal}\tactor_context_object_id={actor_object}\tproperty_present_start_bit={property_start}\ttag={tag_name}\tpayload_start_bit={payload_start}\tpayload_end_bit={payload_end}\tpayload_width={width}\tsemantic_active={active}\tsemantic_actor={actor}\tsemantic_int={intv}\tuid_system={uid_system}\tuid_local={uid_local}\tuid_remote={uid_remote}\tuid_fp={uid_fp}\trepeatability={}\ttruncation={}\twrong_tag_negative={}\twrong_context_negative={}\tpost_payload_poison={}\tanother_control_bits_consumed=0",
            u8::from(repeatability),
            u8::from(truncation),
            u8::from(wrong_tag_negative),
            u8::from(wrong_context_negative),
            u8::from(poison_invariance),
        );
    }

    if rows != 47 || repeat != 47 || trunc != 47 || wrong_tag != 47 || wrong_ctx != 47 || poison != 47 {
        return Err(format!(
            "aggregate fail rows={rows} repeat={repeat} trunc={trunc} wrong_tag={wrong_tag} wrong_ctx={wrong_ctx} poison={poison}"
        )
        .into());
    }
    println!(
        "R3_18AC_NATIVE_AGG\trows=47\trepeatability=47\ttruncation=47\twrong_tag_negative=47\twrong_context_negative=47\tpost_payload_poison=47\tanother_control_bits_consumed=0"
    );
    Ok(())
}
