from pathlib import Path
import sys


def rep(text: str, old: str, new: str, name: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{name}: expected exactly one match, got {count}")
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
helper = r'''fn r3_17a_offset(bits: &LittleEndianReader<'_>, total_bits: usize) -> usize {
    total_bits
        - bits
            .bits_remaining()
            .expect("R3.17A instrumentation requires bounded network bits")
}

fn r3_17a_label() -> String {
    std::env::var("MIMIR_R3_17A_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\t', "_")
        .replace('\r', "_")
        .replace('\n', "_")
}

fn r3_17a_clean(value: &str) -> String {
    value.replace('\t', "_").replace('\r', "_").replace('\n', "_")
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
    "        while bits\n            .read_bit()\n            .ok_or(FrameError::NotEnoughDataFor(\"Actor data\"))?\n        {",
    "        let r3_17a_total_bits = self.body.network_data.len() * 8;\n        let mut r3_17a_actor_ordinal = 0usize;\n        while bits\n            .read_bit()\n            .ok_or(FrameError::NotEnoughDataFor(\"Actor data\"))?\n        {\n            let r3_17a_current_actor_ordinal = r3_17a_actor_ordinal;\n            r3_17a_actor_ordinal += 1;",
    "actor ordinal",
)

s = rep(
    s,
    "                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(\n",
    "                        let r3_17a_payload_start = r3_17a_offset(bits, r3_17a_total_bits);\n                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(\n",
    "payload start",
)

old_after = '''                        )?;

                        updated_actors.push(UpdatedAttribute {
'''
new_after = r'''                        )?;
                        let r3_17a_payload_end = r3_17a_offset(bits, r3_17a_total_bits);
                        let r3_17a_scalar = match (attr.attribute, &attribute) {
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
                        let r3_17a_scalar_tag = matches!(
                            attr.attribute,
                            AttributeTag::Boolean
                                | AttributeTag::Byte
                                | AttributeTag::Enum
                                | AttributeTag::Float
                                | AttributeTag::Int
                                | AttributeTag::Int64
                        );
                        if r3_17a_scalar_tag {
                            let actor_index = usize::from(*object_id);
                            let property_index = usize::from(attr.object_id);
                            let actor_name = self
                                .body
                                .objects
                                .get(actor_index)
                                .map(String::as_str)
                                .unwrap_or("<actor-oob>");
                            let property_name = self
                                .body
                                .objects
                                .get(property_index)
                                .map(String::as_str)
                                .unwrap_or("<property-oob>");
                            if let Some((tag_name, raw_value)) = r3_17a_scalar {
                                println!(
                                    "R3_17A_SCALAR\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tactor_context_object_id={}\tactor_context_object_name={}\tstream_id={}\tproperty_object_id={}\tproperty_object_name={}\tattribute_tag={}\tversion_major={}\tversion_minor={}\tnet_version={}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tnext_cursor_bit={}\tlossless_value={}",
                                    r3_17a_label(),
                                    frame_index,
                                    r3_17a_current_actor_ordinal,
                                    actor_id.0,
                                    object_id.0,
                                    r3_17a_clean(actor_name),
                                    stream_id.0,
                                    attr.object_id.0,
                                    r3_17a_clean(property_name),
                                    tag_name,
                                    self.version.0,
                                    self.version.1,
                                    self.version.2,
                                    r3_17a_payload_start,
                                    r3_17a_payload_end,
                                    r3_17a_payload_end.saturating_sub(r3_17a_payload_start),
                                    r3_17a_payload_end,
                                    raw_value,
                                );
                            } else {
                                println!(
                                    "R3_17A_SHAPE_MISMATCH\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tstream_id={}\tproperty_object_id={}\tattribute_tag={:?}\tpayload_start_bit={}\tpayload_end_bit={}",
                                    r3_17a_label(),
                                    frame_index,
                                    r3_17a_current_actor_ordinal,
                                    actor_id.0,
                                    stream_id.0,
                                    attr.object_id.0,
                                    attr.attribute,
                                    r3_17a_payload_start,
                                    r3_17a_payload_end,
                                );
                            }
                        }

                        updated_actors.push(UpdatedAttribute {
'''
s = rep(s, old_after, new_after, "payload end and scalar receipt")

s = rep(
    s,
    "                    &mut deleted_actors,\n                    &mut updated_actors,\n                )",
    "                    &mut deleted_actors,\n                    &mut updated_actors,\n                    frames.len(),\n                )",
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
    println!("R3_17A_ORACLE_PARSE=PASS");
    Ok(())
}
'''
(example_dir / "r3_17a_probe.rs").write_text(example, encoding="utf-8", newline="\n")

# Hosted CI clones Boxcars below MIMIR's workspace. Prevent Cargo from walking
# upward and treating the oracle clone as a MIMIR workspace member.
manifest = root / "Cargo.toml"
manifest_text = manifest.read_text(encoding="utf-8")
if "\n[workspace]\n" not in f"\n{manifest_text}\n":
    manifest.write_text(
        manifest_text.rstrip() + "\n\n[workspace]\n", encoding="utf-8", newline="\n"
    )

print("R3_17A_BOXCARS_PATCH=PASS")
