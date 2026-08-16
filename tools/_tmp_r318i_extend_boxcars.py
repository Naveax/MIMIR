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

s = rep(
    s,
    '''static R3_18F_SECOND_HEADER_EMITTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);
''',
    '''static R3_18F_SECOND_HEADER_EMITTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);
static R3_18I_SECOND_PAYLOAD_EMITTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);
''',
    "payload atomic",
)

old = '''                        let r3_18f_payload_end_bit =
                            r3_18f_offset(bits, r3_18f_total_bits);

                        if r3_18f_property_ordinal == 0 {
'''
new = r'''                        let r3_18f_payload_end_bit =
                            r3_18f_offset(bits, r3_18f_total_bits);

                        if r3_18f_property_ordinal == 1 {
                            if let Some(first) = r3_18f_first_scalar.as_ref() {
                                let r3_18i_semantic = match (attr.attribute, &attribute) {
                                    (AttributeTag::Int, Attribute::Int(value)) => Some((
                                        "Int",
                                        value.to_string(),
                                        "none".to_owned(),
                                        0usize,
                                    )),
                                    (AttributeTag::String, Attribute::String(value)) => {
                                        let mut hash = 0xcbf29ce484222325u64;
                                        for byte in value.as_bytes() {
                                            hash ^= u64::from(*byte);
                                            hash = hash.wrapping_mul(0x100000001b3);
                                        }
                                        Some((
                                            "String",
                                            "none".to_owned(),
                                            format!("{hash:016x}"),
                                            value.len(),
                                        ))
                                    }
                                    _ => None,
                                };
                                if let Some((kind, semantic_i32, semantic_fnv64, semantic_utf8_len)) =
                                    r3_18i_semantic
                                {
                                    if R3_18I_SECOND_PAYLOAD_EMITTED
                                        .compare_exchange(
                                            false,
                                            true,
                                            std::sync::atomic::Ordering::SeqCst,
                                            std::sync::atomic::Ordering::SeqCst,
                                        )
                                        .is_ok()
                                    {
                                        let window_byte_start = first.property_present_start_bit / 8;
                                        let window_byte_end = r3_18f_payload_end_bit.div_ceil(8);
                                        let window = &self.body.network_data
                                            [window_byte_start..window_byte_end];
                                        let window_hex = window
                                            .iter()
                                            .map(|value| format!("{value:02x}"))
                                            .collect::<String>();
                                        let local_first_start_bit =
                                            first.property_present_start_bit - window_byte_start * 8;
                                        println!(
                                            "R3_18I_PAYLOAD\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tactor_context_object_id={}\tproperty_ordinal=1\tsecond_attribute_tag={}\tsecond_payload_start_bit={}\tsecond_payload_end_bit={}\tsecond_payload_width={}\tsemantic_kind={}\tsemantic_i32={}\tsemantic_fnv64={}\tsemantic_utf8_len={}\twindow_byte_start={}\twindow_local_first_start_bit={}\twindow_hex={}",
                                            r3_18f_label(),
                                            frame_index,
                                            r3_18f_current_actor_ordinal,
                                            actor_id.0,
                                            object_id.0,
                                            kind,
                                            r3_18f_payload_start_bit,
                                            r3_18f_payload_end_bit,
                                            r3_18f_payload_end_bit.saturating_sub(r3_18f_payload_start_bit),
                                            kind,
                                            semantic_i32,
                                            semantic_fnv64,
                                            semantic_utf8_len,
                                            window_byte_start,
                                            local_first_start_bit,
                                            window_hex,
                                        );
                                    }
                                }
                            }
                        }

                        if r3_18f_property_ordinal == 0 {
'''
s = rep(s, old, new, "second payload emission after decode")
frame.write_text(s, encoding="utf-8", newline="\n")
print("R3_18I_BOXCARS_SECOND_PAYLOAD_PATCH=PASS")
