from pathlib import Path
import sys


def rep(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


root = Path(sys.argv[1])
frame = root / "src/network/frame_decoder.rs"
s = frame.read_text(encoding="utf-8")
marker = "fn r3_18ai_label() -> String {\n"
helper = r'''fn r3_18ai_target_usize(name: &str) -> usize {
    std::env::var(name)
        .unwrap_or_else(|_| panic!("R3.18AI missing target env {name}"))
        .parse::<usize>()
        .unwrap_or_else(|_| panic!("R3.18AI invalid usize target env {name}"))
}

fn r3_18ai_target_i32(name: &str) -> i32 {
    std::env::var(name)
        .unwrap_or_else(|_| panic!("R3.18AI missing target env {name}"))
        .parse::<i32>()
        .unwrap_or_else(|_| panic!("R3.18AI invalid i32 target env {name}"))
}

'''
s = rep(s, marker, helper + marker, "target helpers")
old = '''                        let r3_18ai_payload_start_bit =
                            r3_18ai_offset(bits, r3_18ai_total_bits);
                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
'''
new = r'''                        let r3_18ai_payload_start_bit =
                            r3_18ai_offset(bits, r3_18ai_total_bits);

                        if r3_18ai_property_ordinal == 4
                            && frame_index == r3_18ai_target_usize("MIMIR_R3_18AI_TARGET_FRAME")
                            && r3_18ai_current_actor_ordinal
                                == r3_18ai_target_usize("MIMIR_R3_18AI_TARGET_ACTOR_ORDINAL")
                            && object_id.0 == r3_18ai_target_i32("MIMIR_R3_18AI_TARGET_ACTOR_OBJECT")
                            && r3_18ai_property_present_start_bit
                                == r3_18ai_target_usize("MIMIR_R3_18AI_TARGET_PROPERTY_START")
                        {
                            println!(
                                "R3_18AI_HEADER\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tactor_context_object_id={}\tproperty_ordinal=4\tproperty_present_start_bit={}\tproperty_present_end_bit={}\tstream_id_start_bit={}\tstream_id_end_bit={}\tstream_id={}\tstream_id_bound={}\tprop_id_bits={}\tproperty_object_id={}\tattribute_tag={:?}\tversion_major={}\tversion_minor={}\tnet_version={}\tpayload_start_bit={}",
                                r3_18ai_label(), frame_index, r3_18ai_current_actor_ordinal, actor_id.0,
                                object_id.0, r3_18ai_property_present_start_bit,
                                r3_18ai_property_present_end_bit, r3_18ai_stream_id_start_bit,
                                r3_18ai_stream_id_end_bit, stream_id.0, cache_info.max_prop_id,
                                cache_info.prop_id_bits, attr.object_id.0, attr.attribute,
                                self.version.0, self.version.1, self.version.2, r3_18ai_payload_start_bit,
                            );
                        }

                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
'''
s = rep(s, old, new, "ordinal-4 header emission")
frame.write_text(s, encoding="utf-8", newline="\n")
print("R3_18AI_BOXCARS_HEADER_PATCH=PASS ordinal=4")
