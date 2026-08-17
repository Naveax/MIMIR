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

old = '''                        let r3_18o_payload_end_bit =
                            r3_18o_offset(bits, r3_18o_total_bits);

                        if false && r3_18o_property_ordinal == 1 {
'''
new = r'''                        let r3_18o_payload_end_bit =
                            r3_18o_offset(bits, r3_18o_total_bits);

                        if r3_18o_property_ordinal == 2
                            && frame_index == r3_18o_target_usize("MIMIR_R3_18O_TARGET_FRAME")
                            && r3_18o_current_actor_ordinal
                                == r3_18o_target_usize("MIMIR_R3_18O_TARGET_ACTOR_ORDINAL")
                            && object_id.0 == r3_18o_target_i32("MIMIR_R3_18O_TARGET_ACTOR_OBJECT")
                            && r3_18o_property_present_start_bit
                                == r3_18o_target_usize("MIMIR_R3_18O_TARGET_PROPERTY_START")
                        {
                            match (attr.attribute, &attribute) {
                                (AttributeTag::Boolean, Attribute::Boolean(value)) => {
                                    println!(
                                        "R3_18S_ORACLE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\ttag=Boolean\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_bool={}\tsemantic_active=na\tsemantic_actor=na",
                                        r3_18o_label(),
                                        frame_index,
                                        r3_18o_current_actor_ordinal,
                                        object_id.0,
                                        r3_18o_property_present_start_bit,
                                        r3_18o_payload_start_bit,
                                        r3_18o_payload_end_bit,
                                        r3_18o_payload_end_bit.saturating_sub(r3_18o_payload_start_bit),
                                        u8::from(*value),
                                    );
                                }
                                (AttributeTag::ActiveActor, Attribute::ActiveActor(value)) => {
                                    println!(
                                        "R3_18S_ORACLE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\ttag=ActiveActor\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_bool=na\tsemantic_active={}\tsemantic_actor={}",
                                        r3_18o_label(),
                                        frame_index,
                                        r3_18o_current_actor_ordinal,
                                        object_id.0,
                                        r3_18o_property_present_start_bit,
                                        r3_18o_payload_start_bit,
                                        r3_18o_payload_end_bit,
                                        r3_18o_payload_end_bit.saturating_sub(r3_18o_payload_start_bit),
                                        u8::from(value.active),
                                        value.actor.0,
                                    );
                                }
                                _ => {
                                    panic!(
                                        "R3.18S target resolved to unsupported payload pair: {:?} / {:?}",
                                        attr.attribute,
                                        attribute,
                                    );
                                }
                            }
                        }

                        if false && r3_18o_property_ordinal == 1 {
'''
s = rep(s, old, new, "following payload emission after decode")
frame.write_text(s, encoding="utf-8", newline="\n")
print("R3_18S_BOXCARS_FOLLOWING_PAYLOAD_PATCH=PASS")
