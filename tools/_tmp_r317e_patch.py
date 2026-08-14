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
    "use crate::network::attributes::{Attribute, AttributeDecoder, AttributeTag, ProductValueDecoder, RemoteId, UniqueId};\n",
    "attribute imports",
)

marker = "#[derive(Debug)]\nenum DecodedFrame {"
helper = r'''fn r3_17e_offset(bits: &LittleEndianReader<'_>, total_bits: usize) -> usize {
    total_bits
        - bits
            .bits_remaining()
            .expect("R3.17E instrumentation requires bounded network bits")
}

fn r3_17e_label() -> String {
    std::env::var("MIMIR_R3_17E_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\t', "_")
        .replace('\r', "_")
        .replace('\n', "_")
}

fn r3_17e_clean(value: &str) -> String {
    value.replace('\t', "_").replace('\r', "_").replace('\n', "_")
}

fn r3_17e_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(bytes.len() * 2);
    for &byte in bytes {
        out.push(HEX[(byte >> 4) as usize] as char);
        out.push(HEX[(byte & 0x0f) as usize] as char);
    }
    out
}

fn r3_17e_payload_hex(data: &[u8], start: usize, end: usize) -> String {
    if end < start || end > data.len().saturating_mul(8) {
        return "<invalid>".to_owned();
    }
    let width = end - start;
    let mut packed = vec![0u8; width.div_ceil(8)];
    for rel in 0..width {
        let src = start + rel;
        let bit = (data[src / 8] >> (src % 8)) & 1;
        packed[rel / 8] |= bit << (rel % 8);
    }
    r3_17e_hex(&packed)
}

fn r3_17e_remote_kind(remote: &RemoteId) -> &'static str {
    match remote {
        RemoteId::PlayStation(_) => "PlayStation",
        RemoteId::PsyNet(_) => "PsyNet",
        RemoteId::SplitScreen(_) => "SplitScreen",
        RemoteId::Steam(_) => "Steam",
        RemoteId::Switch(_) => "Switch",
        RemoteId::Xbox(_) => "Xbox",
        RemoteId::QQ(_) => "QQ",
        RemoteId::Epic(_) => "Epic",
    }
}

fn r3_17e_uid_shape(uid: &UniqueId) -> String {
    format!("UniqueId:{}", r3_17e_remote_kind(&uid.remote_id))
}

fn r3_17e_uid_summary(uid: &UniqueId) -> String {
    r3_17e_clean(&format!(
        "system:{};local:{};remote:{};debug:{:?}",
        uid.system_id,
        uid.local_id,
        r3_17e_remote_kind(&uid.remote_id),
        uid
    ))
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
    "        let r3_17e_total_bits = self.body.network_data.len() * 8;\n        let mut r3_17e_actor_ordinal = 0usize;\n        while bits\n            .read_bit()\n            .ok_or(FrameError::NotEnoughDataFor(\"Actor data\"))?\n        {\n            let r3_17e_current_actor_ordinal = r3_17e_actor_ordinal;\n            r3_17e_actor_ordinal += 1;",
    "actor ordinal",
)

s = rep(
    s,
    "                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(\n",
    "                        let r3_17e_payload_start = r3_17e_offset(bits, r3_17e_total_bits);\n                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(\n",
    "payload start",
)

old_after = '''                        )?;

                        updated_actors.push(UpdatedAttribute {
'''
new_after = r'''                        )?;
                        let r3_17e_payload_end = r3_17e_offset(bits, r3_17e_total_bits);
                        let r3_17e_candidate = matches!(
                            attr.attribute,
                            AttributeTag::ActiveActor
                                | AttributeTag::String
                                | AttributeTag::QWordString
                                | AttributeTag::UniqueId
                                | AttributeTag::PartyLeader
                        );
                        if r3_17e_candidate {
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
                            let r3_17e_decoded = match (attr.attribute, &attribute) {
                                (AttributeTag::ActiveActor, Attribute::ActiveActor(value)) => Some((
                                    "ActiveActor",
                                    "ActiveActor33".to_owned(),
                                    format!("active:{};actor:{}", u8::from(value.active), value.actor.0),
                                )),
                                (AttributeTag::String, Attribute::String(value)) => Some((
                                    "String",
                                    "StringText".to_owned(),
                                    format!(
                                        "utf8_bytes:{};utf8_hex:{}",
                                        value.as_bytes().len(),
                                        r3_17e_hex(value.as_bytes())
                                    ),
                                )),
                                (AttributeTag::QWordString, Attribute::QWord(value)) => Some((
                                    "QWordString",
                                    "QWord64".to_owned(),
                                    format!("u64:{}", value),
                                )),
                                (AttributeTag::QWordString, Attribute::String(value)) => Some((
                                    "QWordString",
                                    "StringText".to_owned(),
                                    format!(
                                        "utf8_bytes:{};utf8_hex:{}",
                                        value.as_bytes().len(),
                                        r3_17e_hex(value.as_bytes())
                                    ),
                                )),
                                (AttributeTag::UniqueId, Attribute::UniqueId(value)) => Some((
                                    "UniqueId",
                                    r3_17e_uid_shape(value.as_ref()),
                                    r3_17e_uid_summary(value.as_ref()),
                                )),
                                (AttributeTag::PartyLeader, Attribute::PartyLeader(None)) => Some((
                                    "PartyLeader",
                                    "None".to_owned(),
                                    "none".to_owned(),
                                )),
                                (AttributeTag::PartyLeader, Attribute::PartyLeader(Some(value))) => {
                                    Some((
                                        "PartyLeader",
                                        format!("Some:{}", r3_17e_uid_shape(value.as_ref())),
                                        r3_17e_uid_summary(value.as_ref()),
                                    ))
                                }
                                _ => None,
                            };
                            let raw_hex = r3_17e_payload_hex(
                                &self.body.network_data,
                                r3_17e_payload_start,
                                r3_17e_payload_end,
                            );
                            if let Some((tag_name, shape, decoded)) = r3_17e_decoded {
                                println!(
                                    "R3_17E_K2\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tactor_context_object_id={}\tactor_context_object_name={}\tstream_id={}\tproperty_object_id={}\tproperty_object_name={}\tattribute_tag={}\tshape={}\tversion_major={}\tversion_minor={}\tnet_version={}\tis_rl_223={}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tnext_cursor_bit={}\traw_bits_hex={}\tdecoded={}",
                                    r3_17e_label(),
                                    frame_index,
                                    r3_17e_current_actor_ordinal,
                                    actor_id.0,
                                    object_id.0,
                                    r3_17e_clean(actor_name),
                                    stream_id.0,
                                    attr.object_id.0,
                                    r3_17e_clean(property_name),
                                    tag_name,
                                    shape,
                                    self.version.0,
                                    self.version.1,
                                    self.version.2,
                                    attr_decoder.is_rl_223,
                                    r3_17e_payload_start,
                                    r3_17e_payload_end,
                                    r3_17e_payload_end.saturating_sub(r3_17e_payload_start),
                                    r3_17e_payload_end,
                                    raw_hex,
                                    r3_17e_clean(&decoded),
                                );
                            } else {
                                println!(
                                    "R3_17E_SHAPE_MISMATCH\tlabel={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tstream_id={}\tproperty_object_id={}\tattribute_tag={:?}\tpayload_start_bit={}\tpayload_end_bit={}\traw_bits_hex={}",
                                    r3_17e_label(),
                                    frame_index,
                                    r3_17e_current_actor_ordinal,
                                    actor_id.0,
                                    stream_id.0,
                                    attr.object_id.0,
                                    attr.attribute,
                                    r3_17e_payload_start,
                                    r3_17e_payload_end,
                                    raw_hex,
                                );
                            }
                        }

                        updated_actors.push(UpdatedAttribute {
'''
s = rep(s, old_after, new_after, "payload end and K2 receipt")

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
    println!("R3_17E_ORACLE_PARSE=PASS");
    Ok(())
}
'''
(example_dir / "r3_17e_probe.rs").write_text(example, encoding="utf-8", newline="\n")

manifest = root / "Cargo.toml"
manifest_text = manifest.read_text(encoding="utf-8")
if "\n[workspace]\n" not in f"\n{manifest_text}\n":
    manifest.write_text(
        manifest_text.rstrip() + "\n\n[workspace]\n", encoding="utf-8", newline="\n"
    )

print("R3_17E_BOXCARS_PATCH=PASS")
