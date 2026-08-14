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
    "use fnv::FnvHashMap;\n",
    "use fnv::FnvHashMap;\nuse std::collections::BTreeMap;\n",
    "collections import",
)
s = rep(
    s,
    "use crate::network::attributes::{AttributeDecoder, ProductValueDecoder};\n",
    "use crate::network::attributes::{Attribute, AttributeDecoder, AttributeTag, ProductValueDecoder};\n",
    "attribute imports",
)

marker = "#[derive(Debug)]\nenum DecodedFrame {"
helper = r'''fn r3_17i_offset(bits: &LittleEndianReader<'_>, total_bits: usize) -> usize {
    total_bits
        - bits
            .bits_remaining()
            .expect("R3.17I instrumentation requires bounded network bits")
}

fn r3_17i_label() -> String {
    std::env::var("MIMIR_R3_17I_LABEL")
        .unwrap_or_else(|_| "<unset>".to_owned())
        .replace('\t', "_")
        .replace('\r', "_")
        .replace('\n', "_")
}

fn r3_17i_clean(value: &str) -> String {
    value.replace('\t', "_").replace('\r', "_").replace('\n', "_")
}

fn r3_17i_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(bytes.len() * 2);
    for &byte in bytes {
        out.push(HEX[(byte >> 4) as usize] as char);
        out.push(HEX[(byte & 0x0f) as usize] as char);
    }
    out
}

fn r3_17i_payload_hex(data: &[u8], start: usize, end: usize) -> String {
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
    r3_17i_hex(&packed)
}

fn r3_17i_read_le(data: &[u8], cursor: &mut usize, end: usize, width: usize) -> Option<u64> {
    if width > 64 || cursor.checked_add(width)? > end || end > data.len().checked_mul(8)? {
        return None;
    }
    let mut value = 0u64;
    for shift in 0..width {
        let bit_pos = *cursor + shift;
        let bit = (data[bit_pos / 8] >> (bit_pos % 8)) & 1;
        value |= u64::from(bit) << shift;
    }
    *cursor += width;
    Some(value)
}

fn r3_17i_vector_shape(
    data: &[u8],
    cursor: &mut usize,
    end: usize,
    net_version: i32,
    name: &str,
) -> Option<(String, String)> {
    let start = *cursor;
    let low = r3_17i_read_le(data, cursor, end, 4)?;
    let max = if net_version >= 7 { 22u64 } else { 20u64 };
    let up = low + 16;
    let (size_bits, discriminator_bits, discriminator_value) = if up >= max {
        (low, 0usize, 0u64)
    } else {
        let d = r3_17i_read_le(data, cursor, end, 1)?;
        (if d != 0 { up } else { low }, 1usize, d)
    };
    let component_width = usize::try_from(size_bits + 2).ok()?;
    let x_start = *cursor;
    let _x = r3_17i_read_le(data, cursor, end, component_width)?;
    let y_start = *cursor;
    let _y = r3_17i_read_le(data, cursor, end, component_width)?;
    let z_start = *cursor;
    let _z = r3_17i_read_le(data, cursor, end, component_width)?;
    let stop = *cursor;
    let shape = format!(
        "{}:sb{}:h{}:cw{}",
        name,
        size_bits,
        4 + discriminator_bits,
        component_width
    );
    let boundary = format!(
        "{}=[{},{});size_low={};disc_bits={};disc={};size_bits={};x=[{},{});y=[{},{});z=[{},{});component_width={}",
        name,
        start,
        stop,
        low,
        discriminator_bits,
        discriminator_value,
        size_bits,
        x_start,
        x_start + component_width,
        y_start,
        y_start + component_width,
        z_start,
        z_start + component_width,
        component_width,
    );
    Some((shape, boundary))
}

fn r3_17i_classify(
    tag: AttributeTag,
    attribute: &Attribute,
    data: &[u8],
    start: usize,
    end: usize,
    net_version: i32,
) -> Option<(String, String, String)> {
    let mut cursor = start;
    match (tag, attribute) {
        (AttributeTag::Location, Attribute::Location(value)) => {
            let (vec_shape, vec_boundary) =
                r3_17i_vector_shape(data, &mut cursor, end, net_version, "location")?;
            if cursor != end {
                return None;
            }
            Some((
                format!("Location:{}", vec_shape),
                vec_boundary,
                format!("x={:.6};y={:.6};z={:.6}", value.x, value.y, value.z),
            ))
        }
        (AttributeTag::RigidBody, Attribute::RigidBody(value)) => {
            let sleep_start = cursor;
            let sleeping_raw = r3_17i_read_le(data, &mut cursor, end, 1)?;
            if (sleeping_raw != 0) != value.sleeping {
                return None;
            }
            let (loc_shape, loc_boundary) =
                r3_17i_vector_shape(data, &mut cursor, end, net_version, "location")?;
            let rot_start = cursor;
            let rot_width = if net_version >= 7 { 56usize } else { 48usize };
            let _ = r3_17i_read_le(data, &mut cursor, end, rot_width)?;
            let rot_end = cursor;
            let mut shape = format!(
                "RigidBody:{}:{}:quat{}",
                if value.sleeping { "sleeping" } else { "awake" },
                loc_shape,
                rot_width
            );
            let mut boundary = format!(
                "sleep=[{},{});{};rotation=[{},{});rotation_codec=quat{}",
                sleep_start,
                sleep_start + 1,
                loc_boundary,
                rot_start,
                rot_end,
                rot_width
            );
            if !value.sleeping {
                let (lin_shape, lin_boundary) =
                    r3_17i_vector_shape(data, &mut cursor, end, net_version, "linear")?;
                let (ang_shape, ang_boundary) =
                    r3_17i_vector_shape(data, &mut cursor, end, net_version, "angular")?;
                shape.push_str(&format!(":{}:{}", lin_shape, ang_shape));
                boundary.push_str(&format!(";{};{}", lin_boundary, ang_boundary));
                if value.linear_velocity.is_none() || value.angular_velocity.is_none() {
                    return None;
                }
            } else if value.linear_velocity.is_some() || value.angular_velocity.is_some() {
                return None;
            }
            if cursor != end {
                return None;
            }
            let lin = value
                .linear_velocity
                .map(|v| format!("{:.4},{:.4},{:.4}", v.x, v.y, v.z))
                .unwrap_or_else(|| "none".to_owned());
            let ang = value
                .angular_velocity
                .map(|v| format!("{:.4},{:.4},{:.4}", v.x, v.y, v.z))
                .unwrap_or_else(|| "none".to_owned());
            Some((
                shape,
                boundary,
                format!(
                    "sleeping={};loc={:.4},{:.4},{:.4};quat={:.7},{:.7},{:.7},{:.7};lin={};ang={}",
                    u8::from(value.sleeping),
                    value.location.x,
                    value.location.y,
                    value.location.z,
                    value.rotation.x,
                    value.rotation.y,
                    value.rotation.z,
                    value.rotation.w,
                    lin,
                    ang
                ),
            ))
        }
        (AttributeTag::ReplicatedBoost, Attribute::ReplicatedBoost(value)) => {
            if end.checked_sub(start)? != 32 {
                return None;
            }
            let grant = r3_17i_read_le(data, &mut cursor, end, 8)? as u8;
            let amount = r3_17i_read_le(data, &mut cursor, end, 8)? as u8;
            let unused1 = r3_17i_read_le(data, &mut cursor, end, 8)? as u8;
            let unused2 = r3_17i_read_le(data, &mut cursor, end, 8)? as u8;
            if cursor != end
                || grant != value.grant_count
                || amount != value.boost_amount
                || unused1 != value.unused1
                || unused2 != value.unused2
            {
                return None;
            }
            Some((
                "ReplicatedBoost:u8x4".to_owned(),
                format!(
                    "grant=[{},{});boost=[{},{});unused1=[{},{});unused2=[{},{});",
                    start,
                    start + 8,
                    start + 8,
                    start + 16,
                    start + 16,
                    start + 24,
                    start + 24,
                    start + 32
                ),
                format!(
                    "grant={};boost={};unused1={};unused2={}",
                    value.grant_count, value.boost_amount, value.unused1, value.unused2
                ),
            ))
        }
        (AttributeTag::PickupNew, Attribute::PickupNew(value)) => {
            let present_start = cursor;
            let present = r3_17i_read_le(data, &mut cursor, end, 1)? != 0;
            let actor_range = if present {
                let actor_start = cursor;
                let actor = r3_17i_read_le(data, &mut cursor, end, 32)? as u32 as i32;
                if value.instigator.map(|x| x.0) != Some(actor) {
                    return None;
                }
                format!("actor=[{},{});", actor_start, actor_start + 32)
            } else {
                if value.instigator.is_some() {
                    return None;
                }
                "actor=none;".to_owned()
            };
            let picked_start = cursor;
            let picked = r3_17i_read_le(data, &mut cursor, end, 8)? as u8;
            if cursor != end || picked != value.picked_up {
                return None;
            }
            Some((
                format!("PickupNew:{}", if present { "SomeI32" } else { "None" }),
                format!(
                    "present=[{},{});{}picked=[{},{});",
                    present_start,
                    present_start + 1,
                    actor_range,
                    picked_start,
                    picked_start + 8
                ),
                format!(
                    "instigator={};picked={}",
                    value
                        .instigator
                        .map(|x| x.0.to_string())
                        .unwrap_or_else(|| "none".to_owned()),
                    value.picked_up
                ),
            ))
        }
        _ => None,
    }
}

'''
s = rep(s, marker, helper + marker, "helper insertion")

s = rep(
    s,
    "        deleted_actors: &mut Vec<ActorId>,\n        updated_actors: &mut Vec<UpdatedAttribute>,\n    ) -> Result<DecodedFrame, FrameError> {",
    "        deleted_actors: &mut Vec<ActorId>,\n        updated_actors: &mut Vec<UpdatedAttribute>,\n        frame_index: usize,\n        r3_17i_counts: &mut BTreeMap<String, u64>,\n        r3_17i_witnesses: &mut BTreeMap<String, Vec<String>>,\n    ) -> Result<DecodedFrame, FrameError> {",
    "decode frame signature",
)

s = rep(
    s,
    "        while bits\n            .read_bit()\n            .ok_or(FrameError::NotEnoughDataFor(\"Actor data\"))?\n        {",
    "        let r3_17i_total_bits = self.body.network_data.len() * 8;\n        let mut r3_17i_actor_ordinal = 0usize;\n        while bits\n            .read_bit()\n            .ok_or(FrameError::NotEnoughDataFor(\"Actor data\"))?\n        {\n            let r3_17i_current_actor_ordinal = r3_17i_actor_ordinal;\n            r3_17i_actor_ordinal += 1;",
    "actor ordinal",
)

s = rep(
    s,
    "                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(\n",
    "                        let r3_17i_payload_start = r3_17i_offset(bits, r3_17i_total_bits);\n                        let attribute = attr_decoder.decode(attr.attribute, bits, buf).map_err(\n",
    "payload start",
)

old_after = '''                        )?;

                        updated_actors.push(UpdatedAttribute {
'''
new_after = r'''                        )?;
                        let r3_17i_payload_end = r3_17i_offset(bits, r3_17i_total_bits);
                        let r3_17i_candidate = matches!(
                            attr.attribute,
                            AttributeTag::Location
                                | AttributeTag::RigidBody
                                | AttributeTag::ReplicatedBoost
                                | AttributeTag::PickupNew
                        );
                        if r3_17i_candidate {
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
                            let tag_name = match attr.attribute {
                                AttributeTag::Location => "Location",
                                AttributeTag::RigidBody => "RigidBody",
                                AttributeTag::ReplicatedBoost => "ReplicatedBoost",
                                AttributeTag::PickupNew => "PickupNew",
                                _ => unreachable!(),
                            };
                            let classified = r3_17i_classify(
                                attr.attribute,
                                &attribute,
                                &self.body.network_data,
                                r3_17i_payload_start,
                                r3_17i_payload_end,
                                self.version.net_version(),
                            );
                            let (shape, boundary, semantic) = classified.unwrap_or_else(|| (
                                "<unclassified>".to_owned(),
                                "<unclassified>".to_owned(),
                                "<unclassified>".to_owned(),
                            ));
                            let width = r3_17i_payload_end.saturating_sub(r3_17i_payload_start);
                            let key = format!(
                                "tag={}\tshape={}\tversion_major={}\tversion_minor={}\tnet_version={}\tis_rl_223={}\tpayload_width={}",
                                tag_name,
                                shape,
                                self.version.0,
                                self.version.1,
                                self.version.2,
                                attr_decoder.is_rl_223,
                                width,
                            );
                            *r3_17i_counts.entry(key.clone()).or_insert(0) += 1;
                            let witnesses = r3_17i_witnesses.entry(key).or_default();
                            if witnesses.len() < 4 {
                                let raw_hex = r3_17i_payload_hex(
                                    &self.body.network_data,
                                    r3_17i_payload_start,
                                    r3_17i_payload_end,
                                );
                                witnesses.push(format!(
                                    "label={}\tframe_index={}\tactor_ordinal={}\tactor_id={}\tactor_context_object_id={}\tactor_context_object_name={}\tstream_id={}\tproperty_object_id={}\tproperty_object_name={}\tattribute_tag={}\tshape={}\tversion_major={}\tversion_minor={}\tnet_version={}\tis_rl_223={}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tboundary={}\traw_bits_hex={}\tsemantic={}",
                                    r3_17i_label(),
                                    frame_index,
                                    r3_17i_current_actor_ordinal,
                                    actor_id.0,
                                    object_id.0,
                                    r3_17i_clean(actor_name),
                                    stream_id.0,
                                    attr.object_id.0,
                                    r3_17i_clean(property_name),
                                    tag_name,
                                    shape,
                                    self.version.0,
                                    self.version.1,
                                    self.version.2,
                                    attr_decoder.is_rl_223,
                                    r3_17i_payload_start,
                                    r3_17i_payload_end,
                                    width,
                                    r3_17i_clean(&boundary),
                                    raw_hex,
                                    r3_17i_clean(&semantic),
                                ));
                            }
                        }

                        updated_actors.push(UpdatedAttribute {
'''
s = rep(s, old_after, new_after, "payload end and K3 evidence")

s = rep(
    s,
    "        let mut buf = [0u8; 1024];\n",
    "        let mut buf = [0u8; 1024];\n        let mut r3_17i_counts: BTreeMap<String, u64> = BTreeMap::new();\n        let mut r3_17i_witnesses: BTreeMap<String, Vec<String>> = BTreeMap::new();\n",
    "aggregate declarations",
)

s = rep(
    s,
    "                    &mut deleted_actors,\n                    &mut updated_actors,\n                )",
    "                    &mut deleted_actors,\n                    &mut updated_actors,\n                    frames.len(),\n                    &mut r3_17i_counts,\n                    &mut r3_17i_witnesses,\n                )",
    "decode frame call",
)

s = rep(
    s,
    "        Ok(frames)\n",
    r'''        for (key, count) in &r3_17i_counts {
            println!("R3_17I_AGG\tlabel={}\t{}\tcount={}", r3_17i_label(), key, count);
        }
        for (key, rows) in &r3_17i_witnesses {
            for (ordinal, row) in rows.iter().enumerate() {
                println!("R3_17I_WITNESS\tgroup={}\twitness_ordinal={}\t{}", r3_17i_clean(key), ordinal, row);
            }
        }
        println!("R3_17I_REPLAY_DONE\tlabel={}\tframes={}", r3_17i_label(), frames.len());
        Ok(frames)
''',
    "aggregate output",
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
    println!("R3_17I_ORACLE_PARSE=PASS");
    Ok(())
}
'''
(example_dir / "r3_17i_probe.rs").write_text(example, encoding="utf-8", newline="\n")

manifest = root / "Cargo.toml"
manifest_text = manifest.read_text(encoding="utf-8")
if "\n[workspace]\n" not in f"\n{manifest_text}\n":
    manifest.write_text(
        manifest_text.rstrip() + "\n\n[workspace]\n", encoding="utf-8", newline="\n"
    )

print("R3_17I_BOXCARS_PATCH=PASS")
