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
    "use crate::network::attributes::{AttributeDecoder, ProductValueDecoder};\n",
    "use crate::network::attributes::{Attribute, AttributeDecoder, AttributeTag, ProductValueDecoder};\n",
    "attribute imports",
)

marker = "#[derive(Debug)]\nenum DecodedFrame {"
helper = r'''static R3_18A_EMITTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);

fn r3_18a_offset(bits: &LittleEndianReader<'_>, total_bits: usize) -> usize {
    total_bits
        - bits
            .bits_remaining()
            .expect("R3.18A instrumentation requires bounded network bits")
}

fn r3_18a_label() -> String {
    std::env::var("MIMIR_R3_18A_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\t', "_")
        .replace('\r', "_")
        .replace('\n', "_")
}

'''
s = rep(s, marker, helper + marker, "helper insertion")

s = rep(
    s,
    "        deleted_actors: &mut Vec<ActorId>,\n        updated_actors: &mut Vec<UpdatedAttribute>,\n    ) -> Result<DecodedFrame, FrameError> {",
    "        deleted_actors: &mut Vec<ActorId>,\n        updated_actors: &mut Vec<UpdatedAttribute>,\n        frame_index: usize,\n    ) -> Result<DecodedFrame, FrameError> {",
    "decode frame signature",
)

s = rep(
    s,
    '''        if time == 0.0 && delta == 0.0 {
            return Ok(DecodedFrame::EndFrame);
        }

        while bits
''',
    '''        if time == 0.0 && delta == 0.0 {
            return Ok(DecodedFrame::EndFrame);
        }

        let r3_18a_total_bits = self.body.network_data.len() * 8;
        let mut r3_18a_actor_ordinal = 0usize;
        while bits
''',
    "frame total bits",
)

s = rep(
    s,
    '''        {
            bits.refill_lookahead();
            if bits.lookahead_bits() < self.channel_bits + 1 + 1 {
''',
    '''        {
            let r3_18a_current_actor_ordinal = r3_18a_actor_ordinal;
            r3_18a_actor_ordinal += 1;
            bits.refill_lookahead();
            if bits.lookahead_bits() < self.channel_bits + 1 + 1 {
''',
    "actor ordinal",
)

s = rep(
    s,
    '''                    // While there are more attributes to update for our actor:
                    while bits
                        .read_bit()
                        .ok_or(FrameError::NotEnoughDataFor("Is prop present"))?
                    {
''',
    '''                    // While there are more attributes to update for our actor:
                    let mut r3_18a_property_ordinal = 0usize;
                    loop {
                        let r3_18a_property_present_start_bit =
                            r3_18a_offset(bits, r3_18a_total_bits);
                        let r3_18a_property_present = bits
                            .read_bit()
                            .ok_or(FrameError::NotEnoughDataFor("Is prop present"))?;
                        let r3_18a_property_present_end_bit =
                            r3_18a_offset(bits, r3_18a_total_bits);
                        if !r3_18a_property_present {
                            break;
                        }
''',
    "property loop header",
)

s = rep(
    s,
    '''                        let stream_id_raw = bits.peek_bits_max_computed(
                            cache_info.prop_id_bits,
                            u64::from(cache_info.max_prop_id),
                        );
                        let stream_id = StreamId(stream_id_raw as i32);
''',
    '''                        let r3_18a_stream_id_start_bit =
                            r3_18a_offset(bits, r3_18a_total_bits);
                        let stream_id_raw = bits.peek_bits_max_computed(
                            cache_info.prop_id_bits,
                            u64::from(cache_info.max_prop_id),
                        );
                        let r3_18a_stream_id_end_bit =
                            r3_18a_offset(bits, r3_18a_total_bits);
                        let stream_id = StreamId(stream_id_raw as i32);
''',
    "stream offsets",
)

s = rep(
    s,
    '''                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
''',
    '''                        let r3_18a_payload_start_bit =
                            r3_18a_offset(bits, r3_18a_total_bits);
                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(
''',
    "payload start",
)

old_after = '''                        )?;

                        updated_actors.push(UpdatedAttribute {
'''
new_after = r'''                        )?;
                        let r3_18a_payload_end_bit =
                            r3_18a_offset(bits, r3_18a_total_bits);

                        let r3_18a_scalar = match (attr.attribute, &attribute) {
                            (AttributeTag::Boolean, Attribute::Boolean(value)) => {
                                Some(("Boolean", if *value { "1".to_owned() } else { "0".to_owned() }))
                            }
                            (AttributeTag::Byte, Attribute::Byte(value)) => {
                                Some(("Byte", value.to_string()))
                            }
                            (AttributeTag::Enum, Attribute::Enum(value)) => {
                                Some(("Enum", value.to_string()))
                            }
                            (AttributeTag::Float, Attribute::Float(value)) => {
                                Some(("Float", value.to_bits().to_string()))
                            }
                            (AttributeTag::Int, Attribute::Int(value)) => {
                                Some(("Int", value.to_string()))
                            }
                            (AttributeTag::Int64, Attribute::Int64(value)) => {
                                Some(("Int64", value.to_string()))
                            }
                            _ => None,
                        };

                        if r3_18a_property_ordinal == 0 {
                            if let Some((r3_18a_tag_name, r3_18a_lossless_value)) = r3_18a_scalar {
                                if R3_18A_EMITTED
                                    .compare_exchange(
                                        false,
                                        true,
                                        std::sync::atomic::Ordering::SeqCst,
                                        std::sync::atomic::Ordering::SeqCst,
                                    )
                                    .is_ok()
                                {
                                    let r3_18a_window_byte_start =
                                        r3_18a_property_present_start_bit / 8;
                                    let r3_18a_window_byte_end =
                                        r3_18a_payload_end_bit.div_ceil(8);
                                    let r3_18a_window = &self.body.network_data
                                        [r3_18a_window_byte_start..r3_18a_window_byte_end];
                                    let r3_18a_window_hex = r3_18a_window
                                        .iter()
                                        .map(|value| format!("{value:02x}"))
                                        .collect::<String>();
                                    let r3_18a_local_start_bit =
                                        r3_18a_property_present_start_bit
                                            - r3_18a_window_byte_start * 8;
                                    println!(
                                        "R3_18A_ORACLE\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tactor_context_object_id={}\tproperty_ordinal=0\tproperty_present_start_bit={}\tproperty_present_end_bit={}\tstream_id_start_bit={}\tstream_id_end_bit={}\tstream_id={}\tstream_id_bound={}\tprop_id_bits={}\tproperty_object_id={}\tattribute_tag={}\tversion_major={}\tversion_minor={}\tnet_version={}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tnext_property_present_start_bit={}\tlossless_value={}\twindow_byte_start={}\twindow_local_start_bit={}\twindow_hex={}",
                                        r3_18a_label(),
                                        frame_index,
                                        r3_18a_current_actor_ordinal,
                                        actor_id.0,
                                        object_id.0,
                                        r3_18a_property_present_start_bit,
                                        r3_18a_property_present_end_bit,
                                        r3_18a_stream_id_start_bit,
                                        r3_18a_stream_id_end_bit,
                                        stream_id.0,
                                        cache_info.max_prop_id,
                                        cache_info.prop_id_bits,
                                        attr.object_id.0,
                                        r3_18a_tag_name,
                                        self.version.0,
                                        self.version.1,
                                        self.version.2,
                                        r3_18a_payload_start_bit,
                                        r3_18a_payload_end_bit,
                                        r3_18a_payload_end_bit.saturating_sub(r3_18a_payload_start_bit),
                                        r3_18a_payload_end_bit,
                                        r3_18a_lossless_value,
                                        r3_18a_window_byte_start,
                                        r3_18a_local_start_bit,
                                        r3_18a_window_hex,
                                    );
                                }
                            }
                        }
                        r3_18a_property_ordinal += 1;

                        updated_actors.push(UpdatedAttribute {
'''
s = rep(s, old_after, new_after, "payload end and oracle receipt")

s = rep(
    s,
    '''                    &mut deleted_actors,
                    &mut updated_actors,
                )''',
    '''                    &mut deleted_actors,
                    &mut updated_actors,
                    frames.len(),
                )''',
    "decode frame call",
)

frame.write_text(s, encoding="utf-8", newline="\n")

example_dir = root / "examples"
example_dir.mkdir(exist_ok=True)
example = r'''use boxcars::ParserBuilder;
use std::error::Error;
use std::fs;
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args_os().skip(1);
    let replay_path = PathBuf::from(args.next().ok_or("missing replay path")?);
    if args.next().is_some() {
        return Err("unexpected extra argument".into());
    }
    let bytes = fs::read(&replay_path)?;
    let _replay = ParserBuilder::new(&bytes).must_parse_network_data().parse()?;
    println!("R3_18A_ORACLE_PARSE=PASS");
    Ok(())
}
'''
(example_dir / "r3_18a_probe.rs").write_text(example, encoding="utf-8", newline="\n")

manifest = root / "Cargo.toml"
manifest_text = manifest.read_text(encoding="utf-8")
if "\n[workspace]\n" not in f"\n{manifest_text}\n":
    manifest.write_text(
        manifest_text.rstrip() + "\n\n[workspace]\n", encoding="utf-8", newline="\n"
    )

print("R3_18A_BOXCARS_PATCH=PASS")
