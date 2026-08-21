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

old = '''                        let r3_18ai_payload_end_bit =
                            r3_18ai_offset(bits, r3_18ai_total_bits);

                        if r3_18ai_property_ordinal == 0 {
'''
new = r'''                        let r3_18ai_payload_end_bit =
                            r3_18ai_offset(bits, r3_18ai_total_bits);

                        if r3_18ai_property_ordinal == 4
                            && frame_index == r3_18ai_target_usize("MIMIR_R3_18AI_TARGET_FRAME")
                            && r3_18ai_current_actor_ordinal
                                == r3_18ai_target_usize("MIMIR_R3_18AI_TARGET_ACTOR_ORDINAL")
                            && object_id.0 == r3_18ai_target_i32("MIMIR_R3_18AI_TARGET_ACTOR_OBJECT")
                            && r3_18ai_property_present_start_bit
                                == r3_18ai_target_usize("MIMIR_R3_18AI_TARGET_PROPERTY_START")
                        {
                            let width = r3_18ai_payload_end_bit.saturating_sub(r3_18ai_payload_start_bit);
                            match (attr.attribute, &attribute) {
                                (AttributeTag::Int, Attribute::Int(value)) => {
                                    println!(
                                        "R3_18AM_ORACLE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\ttag=Int\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_int={}",
                                        r3_18ai_label(), frame_index, r3_18ai_current_actor_ordinal,
                                        object_id.0, r3_18ai_property_present_start_bit,
                                        r3_18ai_payload_start_bit, r3_18ai_payload_end_bit, width, value,
                                    );
                                }
                                _ => panic!(
                                    "R3.18AM ordinal-4 target unsupported pair: {:?} / {:?}",
                                    attr.attribute, attribute
                                ),
                            }
                        }

                        if r3_18ai_property_ordinal == 0 {
'''
s = rep(s, old, new, "ordinal-4 payload emission")
frame.write_text(s, encoding="utf-8", newline="\n")
print("R3_18AM_BOXCARS_PAYLOAD_PATCH=PASS ordinal=4")
