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
    '''static R3_18F_CONTINUATION_EMITTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);
''',
    '''static R3_18F_CONTINUATION_EMITTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);
static R3_18F_SECOND_HEADER_EMITTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);
''',
    "second-header atomic",
)

old = '''                        let r3_18f_payload_start_bit =
                            r3_18f_offset(bits, r3_18f_total_bits);
                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
'''
new = r'''                        let r3_18f_payload_start_bit =
                            r3_18f_offset(bits, r3_18f_total_bits);

                        if r3_18f_property_ordinal == 1 {
                            if let Some(first) = r3_18f_first_scalar.as_ref() {
                                if R3_18F_SECOND_HEADER_EMITTED
                                    .compare_exchange(
                                        false,
                                        true,
                                        std::sync::atomic::Ordering::SeqCst,
                                        std::sync::atomic::Ordering::SeqCst,
                                    )
                                    .is_ok()
                                {
                                    let r3_18f_window_byte_start =
                                        first.property_present_start_bit / 8;
                                    let r3_18f_window_byte_end =
                                        r3_18f_payload_start_bit.div_ceil(8);
                                    let r3_18f_window = &self.body.network_data
                                        [r3_18f_window_byte_start..r3_18f_window_byte_end];
                                    let r3_18f_window_hex = r3_18f_window
                                        .iter()
                                        .map(|value| format!("{value:02x}"))
                                        .collect::<String>();
                                    let r3_18f_local_first_start_bit =
                                        first.property_present_start_bit
                                            - r3_18f_window_byte_start * 8;
                                    println!(
                                        "R3_18F_SECOND\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tactor_context_object_id={}\tproperty_ordinal=1\tfirst_property_present_start_bit={}\tfirst_payload_end_bit={}\tsecond_property_present_start_bit={}\tsecond_property_present_end_bit={}\tsecond_stream_id_start_bit={}\tsecond_stream_id_end_bit={}\tsecond_stream_id={}\tsecond_stream_id_bound={}\tsecond_prop_id_bits={}\tsecond_property_object_id={}\tsecond_attribute_tag={:?}\tsecond_payload_start_bit={}\twindow_byte_start={}\twindow_local_first_start_bit={}\twindow_hex={}",
                                        r3_18f_label(),
                                        frame_index,
                                        r3_18f_current_actor_ordinal,
                                        actor_id.0,
                                        object_id.0,
                                        first.property_present_start_bit,
                                        first.payload_end_bit,
                                        r3_18f_property_present_start_bit,
                                        r3_18f_property_present_end_bit,
                                        r3_18f_stream_id_start_bit,
                                        r3_18f_stream_id_end_bit,
                                        stream_id.0,
                                        cache_info.max_prop_id,
                                        cache_info.prop_id_bits,
                                        attr.object_id.0,
                                        attr.attribute,
                                        r3_18f_payload_start_bit,
                                        r3_18f_window_byte_start,
                                        r3_18f_local_first_start_bit,
                                        r3_18f_window_hex,
                                    );
                                }
                            }
                        }

                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
'''
s = rep(s, old, new, "second-header emission before payload decode")
frame.write_text(s, encoding="utf-8", newline="\n")
print("R3_18F_BOXCARS_SECOND_HEADER_PATCH=PASS")
