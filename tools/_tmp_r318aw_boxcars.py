from pathlib import Path
import sys


def rep(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly one match, got {n}")
    return text.replace(old, new, 1)


root = Path(sys.argv[1])
frame = root / "src/network/frame_decoder.rs"
s = frame.read_text(encoding="utf-8")

marker = "fn r3_18ai_label() -> String {\n"
helpers = r'''fn r3_18aw_target_usize(name: &str) -> usize {
    std::env::var(name)
        .unwrap_or_else(|_| panic!("R3.18AW missing target env {name}"))
        .parse::<usize>()
        .unwrap_or_else(|_| panic!("R3.18AW invalid usize target env {name}"))
}

fn r3_18aw_target_i32(name: &str) -> i32 {
    std::env::var(name)
        .unwrap_or_else(|_| panic!("R3.18AW missing target env {name}"))
        .parse::<i32>()
        .unwrap_or_else(|_| panic!("R3.18AW invalid i32 target env {name}"))
}

'''
s = rep(s, marker, helpers + marker, "AW target helpers")

old_header = '''                        let r3_18ai_payload_start_bit =
                            r3_18ai_offset(bits, r3_18ai_total_bits);
                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
'''
new_header = r'''                        let r3_18ai_payload_start_bit =
                            r3_18ai_offset(bits, r3_18ai_total_bits);
                        let r3_18aw_target =
                            frame_index == r3_18aw_target_usize("MIMIR_R3_18AW_TARGET_FRAME")
                            && r3_18ai_current_actor_ordinal
                                == r3_18aw_target_usize("MIMIR_R3_18AW_TARGET_ACTOR_ORDINAL")
                            && object_id.0
                                == r3_18aw_target_i32("MIMIR_R3_18AW_TARGET_ACTOR_OBJECT")
                            && r3_18ai_property_present_start_bit
                                == r3_18aw_target_usize("MIMIR_R3_18AW_TARGET_PROPERTY_START");

                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
'''
s = rep(s, old_header, new_header, "AW target selector")

old_payload = '''                        let r3_18ai_payload_end_bit =
                            r3_18ai_offset(bits, r3_18ai_total_bits);

                        if r3_18ai_property_ordinal == 0 {
'''
new_payload = r'''                        let r3_18ai_payload_end_bit =
                            r3_18ai_offset(bits, r3_18ai_total_bits);

                        if r3_18aw_target {
                            let width =
                                r3_18ai_payload_end_bit.saturating_sub(r3_18ai_payload_start_bit);
                            let mimir_contract_rl223 = std::env::var(
                                "MIMIR_R3_18AW_CONTRACT_RL223",
                            )
                            .expect("R3.18AW missing MIMIR contract RL223 env");
                            assert_eq!(
                                mimir_contract_rl223, "false",
                                "R3.18AW current admitted MIMIR contract must remain non-RL223",
                            );
                            match (attr.attribute, &attribute) {
                                (AttributeTag::Int, Attribute::Int(value)) => {
                                    println!(
                                        "R3_18AW_ORACLE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\tproperty_present_end_bit={}\tstream_id_start_bit={}\tstream_id_end_bit={}\tstream_id={}\tstream_id_bound={}\tprop_id_bits={}\tproperty_object_index={}\tattribute_tag=Int\tversion_major={}\tversion_minor={}\tnet_version={}\tmimir_contract_rl223={}\tboxcars_build_rl223={}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_int={}",
                                        r3_18ai_label(),
                                        frame_index,
                                        r3_18ai_current_actor_ordinal,
                                        object_id.0,
                                        r3_18ai_property_present_start_bit,
                                        r3_18ai_property_present_end_bit,
                                        r3_18ai_stream_id_start_bit,
                                        r3_18ai_stream_id_end_bit,
                                        stream_id.0,
                                        cache_info.max_prop_id,
                                        cache_info.prop_id_bits,
                                        attr.object_id.0,
                                        self.version.0,
                                        self.version.1,
                                        self.version.2,
                                        mimir_contract_rl223,
                                        self.is_rl_223,
                                        r3_18ai_payload_start_bit,
                                        r3_18ai_payload_end_bit,
                                        width,
                                        value,
                                    );
                                }
                                _ => panic!(
                                    "R3.18AW current target unsupported pair: {:?} / {:?}",
                                    attr.attribute, attribute
                                ),
                            }
                        }

                        if r3_18ai_property_ordinal == 0 {
'''
s = rep(s, old_payload, new_payload, "AW payload emission")
frame.write_text(s, encoding="utf-8", newline="\n")
print("R3_18AW_BOXCARS_PATCH=PASS selector=current-coordinates ordinal-independent rl223-semantics=separate-names")
