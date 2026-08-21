from pathlib import Path
import sys


def rep(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected one match got {n}")
    return text.replace(old, new, 1)


src = Path(sys.argv[1])
out = Path(sys.argv[2])
s = src.read_text(encoding="utf-8")

s = rep(
    s,
    "    ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,\n",
    "    ReplayNetworkAttributeTagV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,\n    ReplayNetworkPrimitiveScalarDecodeV1, ReplayNetworkPrimitiveScalarValueV1,\n    decode_replay_network_primitive_scalar_v1,\n",
    "imports",
)

helper = r'''
fn decode_checked_int_payload(
    network: &[u8],
    proven_header_stop: u64,
    requested_payload_start: u64,
    header_tag: ReplayNetworkAttributeTagV1,
) -> Result<ReplayNetworkPrimitiveScalarDecodeV1, Box<dyn std::error::Error>> {
    if header_tag != ReplayNetworkAttributeTagV1::Int {
        return Err(format!("R3.18AM boundary requires Int header, got {header_tag:?}").into());
    }
    if requested_payload_start != proven_header_stop {
        return Err(format!(
            "R3.18AM payload start {requested_payload_start} differs from proven header stop {proven_header_stop}"
        )
        .into());
    }
    Ok(decode_replay_network_primitive_scalar_v1(
        network,
        requested_payload_start,
        ReplayNetworkAttributeTagV1::Int,
    )?)
}
'''
s = rep(s, "    Ok(())\n}\n\nfn main()", "    Ok(())\n}\n" + helper + "\nfn main()", "checked payload helper")

s = rep(
    s,
    "    let mut poison_n = 0usize;\n",
    "    let mut poison_n = 0usize;\n    let mut payload_exact_n = 0usize;\n    let mut payload_repeat_n = 0usize;\n    let mut payload_trunc_n = 0usize;\n    let mut wrong_tag_n = 0usize;\n    let mut wrong_boundary_n = 0usize;\n    let mut payload_poison_n = 0usize;\n",
    "payload counters",
)

needle = '''        if poison_invariant {
            poison_n += 1;
        }

        println!(
            "R3_18AL_NATIVE\\tlabel={label}'''
insert = r'''        if poison_invariant {
            poison_n += 1;
        }

        let payload = decode_checked_int_payload(&network, got.stop_bit, payload_start, tag)?;
        let semantic_int = match &payload.value {
            ReplayNetworkPrimitiveScalarValueV1::Int(value) => *value,
            other => return Err(format!("{label}: expected Int scalar, got {other:?}").into()),
        };
        let payload_exact = payload.attribute_tag == ReplayNetworkAttributeTagV1::Int
            && payload.payload_start_bit == payload_start
            && payload.payload_end_bit == payload.stop_bit
            && payload.payload_end_bit > payload.payload_start_bit;
        if !payload_exact {
            return Err(format!("{label}: invalid payload boundary {payload:?}").into());
        }
        payload_exact_n += 1;

        let payload_repeated = decode_checked_int_payload(&network, got.stop_bit, payload_start, tag)?;
        let payload_repeatability = payload_repeated == payload;
        if payload_repeatability {
            payload_repeat_n += 1;
        }

        let payload_cut_bytes = usize::try_from(payload.payload_end_bit.saturating_sub(1) / 8)?
            .min(network.len());
        let payload_truncation = decode_checked_int_payload(
            &network[..payload_cut_bytes],
            got.stop_bit,
            payload_start,
            tag,
        )
        .is_err();
        if payload_truncation {
            payload_trunc_n += 1;
        }

        let wrong_tag_negative = decode_checked_int_payload(
            &network,
            got.stop_bit,
            payload_start,
            ReplayNetworkAttributeTagV1::Boolean,
        )
        .is_err();
        if wrong_tag_negative {
            wrong_tag_n += 1;
        }

        let wrong_boundary_negative = decode_checked_int_payload(
            &network,
            got.stop_bit,
            payload_start.saturating_add(1),
            tag,
        )
        .is_err();
        if wrong_boundary_negative {
            wrong_boundary_n += 1;
        }

        let mut payload_poisoned = network.clone();
        for offset in 0..16u64 {
            set_bit(
                &mut payload_poisoned,
                payload.payload_end_bit + offset,
                offset % 2 == 0,
            )
            .map_err(std::io::Error::other)?;
        }
        let poisoned_payload = decode_checked_int_payload(
            &payload_poisoned,
            got.stop_bit,
            payload_start,
            tag,
        )?;
        let payload_poison = poisoned_payload == payload;
        if payload_poison {
            payload_poison_n += 1;
        }

        println!(
            "R3_18AM_NATIVE\\tlabel={label}\\tframe_index={frame_index}\\tactor_ordinal={actor_ordinal}\\tactor_context_object_id={actor_object}\\tproperty_present_start_bit={}\\ttag=Int\\tpayload_start_bit={}\\tpayload_end_bit={}\\tpayload_width={}\\tsemantic_int={}\\theader_exact={}\\tpayload_repeatability={}\\tpayload_truncation_negative={}\\twrong_tag_negative={}\\twrong_boundary_negative={}\\twrong_context_negative={}\\tcorrupt_control_negative={}\\tcorrupt_prior_negative={}\\tpost_payload_end_poison={}\\tanother_control_bits_consumed=0",
            ag.property_present_start_bit,
            payload.payload_start_bit,
            payload.payload_end_bit,
            payload.payload_width,
            semantic_int,
            u8::from(exact),
            u8::from(payload_repeatability),
            u8::from(payload_truncation),
            u8::from(wrong_tag_negative),
            u8::from(wrong_boundary_negative),
            u8::from(wrong_context),
            u8::from(corrupt_control),
            u8::from(corrupt_prior),
            u8::from(payload_poison),
        );

        println!(
            "R3_18AL_NATIVE\\tlabel={label}'''
s = rep(s, needle, insert, "payload probe injection")

s = rep(
    s,
    "        || poison_n != 47\n    {",
    "        || poison_n != 47\n        || payload_exact_n != 47\n        || payload_repeat_n != 47\n        || payload_trunc_n != 47\n        || wrong_tag_n != 47\n        || wrong_boundary_n != 47\n        || payload_poison_n != 47\n    {",
    "aggregate payload counters",
)

s = rep(
    s,
    "    println!(\n        \"R3_18AL_NATIVE_AGG",
    "    println!(\n        \"R3_18AM_NATIVE_AGG\\\\trows=47\\\\tpayload_exact=47\\\\tpayload_repeatability=47\\\\tpayload_truncation=47\\\\twrong_tag_negative=47\\\\twrong_boundary_negative=47\\\\tpost_payload_end_poison=47\\\\tanother_control_bits_consumed=0\"\n    );\n\n    println!(\n        \"R3_18AL_NATIVE_AGG",
    "AM aggregate print",
)

out.write_text(s, encoding="utf-8", newline="\n")
print("R3_18AM_NATIVE_PROBE_DERIVATION=PASS")
