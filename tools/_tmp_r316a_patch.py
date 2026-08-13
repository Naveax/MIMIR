from pathlib import Path
import sys


def rep(text: str, old: str, new: str, name: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{name}: expected 1 match, got {n}")
    return text.replace(old, new, 1)


root = Path(sys.argv[1])
p = root / "src/network/frame_decoder.rs"
s = p.read_text(encoding="utf-8")
s = rep(
    s,
    "        updated_actors: &mut Vec<UpdatedAttribute>,\n        frame_index: usize,\n    ) -> Result<DecodedFrame, FrameError> {",
    "        updated_actors: &mut Vec<UpdatedAttribute>,\n        frame_index: usize,\n        r3_16a_selected: &mut bool,\n    ) -> Result<DecodedFrame, FrameError> {",
    "decode-frame-signature",
)
s = rep(
    s,
    "        let mut r3_15a_actor_ordinal = 0usize;\n        while bits",
    "        let r3_16a_total_bits = self.body.network_data.len() * 8;\n        let mut r3_15a_actor_ordinal = 0usize;\n        while bits",
    "total-bits",
)
s = rep(
    s,
    "                // new\n                if bits\n                    .read_bit()\n                    .ok_or(FrameError::NotEnoughDataFor(\"Is new actor\"))?\n                {",
    "                // new\n                let r3_16a_is_new = bits\n                    .read_bit()\n                    .ok_or(FrameError::NotEnoughDataFor(\"Is new actor\"))?;\n                let r3_16a_new_bit_end = r3_15a_offset(bits, r3_16a_total_bits);\n                if r3_16a_is_new {",
    "new-bit",
)
s = rep(
    s,
    "                    // While there are more attributes to update for our actor:\n                    while bits\n                        .read_bit()\n                        .ok_or(FrameError::NotEnoughDataFor(\"Is prop present\"))?\n                    {",
    "                    // While there are more attributes to update for our actor:\n                    loop {\n                        let r3_16a_property_present_start =\n                            r3_15a_offset(bits, r3_16a_total_bits);\n                        let r3_16a_property_present = bits\n                            .read_bit()\n                            .ok_or(FrameError::NotEnoughDataFor(\"Is prop present\"))?;\n                        let r3_16a_property_present_end =\n                            r3_15a_offset(bits, r3_16a_total_bits);\n                        if !r3_16a_property_present { break; }",
    "property-present",
)
s = rep(
    s,
    "                        bits.refill_lookahead();\n                        if bits.lookahead_bits() < cache_info.prop_id_bits + 1 {",
    "                        let r3_16a_stream_start = r3_15a_offset(bits, r3_16a_total_bits);\n                        bits.refill_lookahead();\n                        if bits.lookahead_bits() < cache_info.prop_id_bits + 1 {",
    "stream-start",
)
s = rep(
    s,
    "                        let stream_id = StreamId(stream_id_raw as i32);\n\n                        // Look the stream id up",
    "                        let stream_id = StreamId(stream_id_raw as i32);\n                        let r3_16a_stream_end = r3_15a_offset(bits, r3_16a_total_bits);\n\n                        // Look the stream id up",
    "stream-end",
)
needle = "                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(\n                            |e| match e {"
insert = '''                        let r3_16a_payload_start = r3_15a_offset(bits, r3_16a_total_bits);
                        if !*r3_16a_selected {
                            let actor_index = usize::from(*object_id);
                            let property_index = usize::from(attr.object_id);
                            let actor_name = self.body.objects.get(actor_index).map(String::as_str).unwrap_or("<actor-oob>");
                            let property_name = self.body.objects.get(property_index).map(String::as_str).unwrap_or("<property-oob>");
                            println!("R3_16A_PROPERTY\\tlabel={}\\tframe_index={}\\tactor_ordinal={}\\tframe_time_raw_bits={}\\tframe_delta_raw_bits={}\\tactor_id={}\\tactor_context_object_id={}\\tactor_context_object_name={}\\tnew_bit_end={}\\tproperty_present_start_bit={}\\tproperty_present_end_bit={}\\tproperty_present_value=true\\tstream_id_start_bit={}\\tstream_id_end_bit={}\\tstream_id_value={}\\tstream_id_bound={}\\tprop_id_bits={}\\tresolved_property_object_id={}\\tresolved_property_object_name={}\\tresolved_attribute_tag={:?}\\tpayload_start_bit={}", r3_15a_label(), frame_index, r3_15a_current_actor_ordinal, time.to_bits(), delta.to_bits(), actor_id.0, object_id.0, actor_name, r3_16a_new_bit_end, r3_16a_property_present_start, r3_16a_property_present_end, r3_16a_stream_start, r3_16a_stream_end, stream_id.0, cache_info.max_prop_id, cache_info.prop_id_bits, attr.object_id.0, property_name, attr.attribute, r3_16a_payload_start);
                            *r3_16a_selected = true;
                        }

                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
                            |e| match e {'''
s = rep(s, needle, insert, "payload-boundary")
s = rep(
    s,
    "        let mut buf = [0u8; 1024];\n\n        while !bits.is_empty()",
    "        let mut buf = [0u8; 1024];\n        let mut r3_16a_selected = false;\n\n        while !bits.is_empty()",
    "selected-state",
)
s = rep(
    s,
    "                    &mut updated_actors,\n                    frames.len(),\n                )",
    "                    &mut updated_actors,\n                    frames.len(),\n                    &mut r3_16a_selected,\n                )",
    "decode-call",
)
p.write_text(s, encoding="utf-8", newline="\n")

# The clone lives below MIMIR's repository root on hosted Windows CI. Without an
# explicit workspace root Cargo walks upward and incorrectly treats Boxcars as a
# MIMIR workspace member. This marker changes orchestration only, not oracle code.
manifest = root / "Cargo.toml"
manifest_text = manifest.read_text(encoding="utf-8")
if "\n[workspace]\n" not in f"\n{manifest_text}\n":
    manifest.write_text(manifest_text.rstrip() + "\n\n[workspace]\n", encoding="utf-8", newline="\n")

print("R3_16A_BOXCARS_PATCH=PASS")
