from pathlib import Path
import sys

def rep(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f"{label}: expected one match got {n}")
    return text.replace(old,new,1)

root=Path(sys.argv[1])
frame=root/"src/network/frame_decoder.rs"
s=frame.read_text(encoding="utf-8")

marker="fn r3_18y_label() -> String {\n"
helper=r'''fn r3_18ac_mix(mut hash: u64, bytes: &[u8]) -> u64 {
    for byte in bytes {
        hash ^= u64::from(*byte);
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

fn r3_18ac_unique_parts(value: &crate::network::attributes::UniqueId) -> (&'static str, u64) {
    let mut h = 0xcbf29ce484222325u64;
    match &value.remote_id {
        crate::network::attributes::RemoteId::PlayStation(v) => {
            h = r3_18ac_mix(h, v.name.as_bytes());
            h = r3_18ac_mix(h, &v.unknown1);
            h = r3_18ac_mix(h, &v.online_id.to_le_bytes());
            ("PlayStation", h)
        }
        crate::network::attributes::RemoteId::PsyNet(v) => {
            h = r3_18ac_mix(h, &v.online_id.to_le_bytes());
            ("PsyNet", h)
        }
        crate::network::attributes::RemoteId::SplitScreen(v) => {
            h = r3_18ac_mix(h, &v.to_le_bytes());
            ("SplitScreen", h)
        }
        crate::network::attributes::RemoteId::Steam(v) => {
            h = r3_18ac_mix(h, &v.to_le_bytes());
            ("Steam", h)
        }
        crate::network::attributes::RemoteId::Switch(v) => {
            h = r3_18ac_mix(h, &v.online_id.to_le_bytes());
            h = r3_18ac_mix(h, &v.unknown1);
            ("Switch", h)
        }
        crate::network::attributes::RemoteId::Xbox(v) => {
            h = r3_18ac_mix(h, &v.to_le_bytes());
            ("Xbox", h)
        }
        crate::network::attributes::RemoteId::QQ(v) => {
            h = r3_18ac_mix(h, &v.to_le_bytes());
            ("QQ", h)
        }
        crate::network::attributes::RemoteId::Epic(v) => {
            h = r3_18ac_mix(h, v.as_bytes());
            ("Epic", h)
        }
    }
}

'''
s=rep(s,marker,helper+marker,"fingerprint helper")

old='''                        let r3_18y_payload_end_bit =
                            r3_18y_offset(bits, r3_18y_total_bits);

                        if r3_18y_property_ordinal == 0 {
'''
new=r'''                        let r3_18y_payload_end_bit =
                            r3_18y_offset(bits, r3_18y_total_bits);

                        if r3_18y_property_ordinal == 3
                            && frame_index == r3_18y_target_usize("MIMIR_R3_18Y_TARGET_FRAME")
                            && r3_18y_current_actor_ordinal
                                == r3_18y_target_usize("MIMIR_R3_18Y_TARGET_ACTOR_ORDINAL")
                            && object_id.0 == r3_18y_target_i32("MIMIR_R3_18Y_TARGET_ACTOR_OBJECT")
                            && r3_18y_property_present_start_bit
                                == r3_18y_target_usize("MIMIR_R3_18Y_TARGET_PROPERTY_START")
                        {
                            let width = r3_18y_payload_end_bit.saturating_sub(r3_18y_payload_start_bit);
                            match (attr.attribute, &attribute) {
                                (AttributeTag::ActiveActor, Attribute::ActiveActor(value)) => {
                                    println!(
                                        "R3_18AC_ORACLE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\ttag=ActiveActor\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_active={}\tsemantic_actor={}\tsemantic_int=na\tuid_system=na\tuid_local=na\tuid_remote=na\tuid_fp=na",
                                        r3_18y_label(), frame_index, r3_18y_current_actor_ordinal,
                                        object_id.0, r3_18y_property_present_start_bit,
                                        r3_18y_payload_start_bit, r3_18y_payload_end_bit, width,
                                        u8::from(value.active), value.actor.0,
                                    );
                                }
                                (AttributeTag::Int, Attribute::Int(value)) => {
                                    println!(
                                        "R3_18AC_ORACLE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\ttag=Int\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_active=na\tsemantic_actor=na\tsemantic_int={}\tuid_system=na\tuid_local=na\tuid_remote=na\tuid_fp=na",
                                        r3_18y_label(), frame_index, r3_18y_current_actor_ordinal,
                                        object_id.0, r3_18y_property_present_start_bit,
                                        r3_18y_payload_start_bit, r3_18y_payload_end_bit, width, value,
                                    );
                                }
                                (AttributeTag::UniqueId, Attribute::UniqueId(value)) => {
                                    let (remote_kind, fp) = r3_18ac_unique_parts(value);
                                    println!(
                                        "R3_18AC_ORACLE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\ttag=UniqueId\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_active=na\tsemantic_actor=na\tsemantic_int=na\tuid_system={}\tuid_local={}\tuid_remote={}\tuid_fp={:016x}",
                                        r3_18y_label(), frame_index, r3_18y_current_actor_ordinal,
                                        object_id.0, r3_18y_property_present_start_bit,
                                        r3_18y_payload_start_bit, r3_18y_payload_end_bit, width,
                                        value.system_id, value.local_id, remote_kind, fp,
                                    );
                                }
                                _ => panic!(
                                    "R3.18AC target unsupported pair: {:?} / {:?}",
                                    attr.attribute, attribute
                                ),
                            }
                        }

                        if r3_18y_property_ordinal == 0 {
'''
s=rep(s,old,new,"ordinal-3 payload emission")
frame.write_text(s,encoding="utf-8",newline="\n")
print("R3_18AC_BOXCARS_PAYLOAD_PATCH=PASS ordinal=3")
