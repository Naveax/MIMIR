from __future__ import annotations

from pathlib import Path
import runpy
import sys


def rep(text: str, old: str, new: str, name: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{name}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: _tmp_r317m_transform.py <boxcars-root> <r317i-base-patch>")
    root = Path(sys.argv[1])
    base_patch = Path(sys.argv[2])

    old_argv = sys.argv[:]
    try:
        sys.argv = [str(base_patch), str(root)]
        runpy.run_path(str(base_patch), run_name="__main__")
    finally:
        sys.argv = old_argv

    frame = root / "src/network/frame_decoder.rs"
    s = frame.read_text(encoding="utf-8")
    s = s.replace("r3_17i", "r3_17m").replace("R3_17I", "R3_17M")

    old_candidate = '''                        let r3_17m_candidate = matches!(
                            attr.attribute,
                            AttributeTag::Location
                                | AttributeTag::RigidBody
                                | AttributeTag::ReplicatedBoost
                                | AttributeTag::PickupNew
                        );'''
    new_candidate = '''                        let r3_17m_candidate = matches!(
                            attr.attribute,
                            AttributeTag::CamSettings
                                | AttributeTag::TeamPaint
                                | AttributeTag::TeamLoadout
                                | AttributeTag::ClubColors
                                | AttributeTag::Reservation
                                | AttributeTag::StatEvent
                                | AttributeTag::PlayerHistoryKey
                                | AttributeTag::DemolishFx
                                | AttributeTag::DemolishExtended
                                | AttributeTag::ExtendedExplosion
                                | AttributeTag::LoadoutsOnline
                        );'''
    s = rep(s, old_candidate, new_candidate, "candidate tag surface")

    old_tag_match = '''                            let tag_name = match attr.attribute {
                                AttributeTag::Location => "Location",
                                AttributeTag::RigidBody => "RigidBody",
                                AttributeTag::ReplicatedBoost => "ReplicatedBoost",
                                AttributeTag::PickupNew => "PickupNew",
                                _ => unreachable!(),
                            };'''
    new_tag_match = '''                            let tag_name = match attr.attribute {
                                AttributeTag::CamSettings => "CamSettings",
                                AttributeTag::TeamPaint => "TeamPaint",
                                AttributeTag::TeamLoadout => "TeamLoadout",
                                AttributeTag::ClubColors => "ClubColors",
                                AttributeTag::Reservation => "Reservation",
                                AttributeTag::StatEvent => "StatEvent",
                                AttributeTag::PlayerHistoryKey => "PlayerHistoryKey",
                                AttributeTag::DemolishFx => "DemolishFx",
                                AttributeTag::DemolishExtended => "DemolishExtended",
                                AttributeTag::ExtendedExplosion => "ExtendedExplosion",
                                AttributeTag::LoadoutsOnline => "LoadoutsOnline",
                                _ => unreachable!(),
                            };'''
    s = rep(s, old_tag_match, new_tag_match, "tag names")

    old_call = '''                            let classified = r3_17m_classify(
                                attr.attribute,
                                &attribute,
                                &self.body.network_data,
                                r3_17m_payload_start,
                                r3_17m_payload_end,
                                self.version.net_version(),
                            );'''
    new_call = '''                            let classified = r3_17m_classify(
                                attr.attribute,
                                &attribute,
                                &self.body.network_data,
                                r3_17m_payload_start,
                                r3_17m_payload_end,
                                self.version.0,
                                self.version.1,
                                self.version.net_version(),
                                &self.body.objects,
                            );'''
    s = rep(s, old_call, new_call, "classifier call")

    start = s.index("fn r3_17m_classify(")
    end = s.index("#[derive(Debug)]\nenum DecodedFrame {", start)
    classifier = r'''fn r3_17m_skip(cursor: &mut usize, end: usize, width: usize) -> Option<(usize, usize)> {
    let start = *cursor;
    let stop = start.checked_add(width)?;
    if stop > end {
        return None;
    }
    *cursor = stop;
    Some((start, stop))
}

fn r3_17m_version_ge(major: i32, minor: i32, net: i32, a: i32, b: i32, c: i32) -> bool {
    (major, minor, net) >= (a, b, c)
}

fn r3_17m_text_shape(
    data: &[u8],
    cursor: &mut usize,
    end: usize,
    name: &str,
) -> Option<(String, String)> {
    let len_start = *cursor;
    let declared = r3_17m_read_le(data, cursor, end, 32)? as u32 as i32;
    let data_start = *cursor;
    let (shape, bytes) = if declared == 0 {
        ("empty".to_owned(), 0usize)
    } else if declared > 0 {
        (format!("w1252_{}", declared), usize::try_from(declared).ok()?)
    } else {
        let units = declared.checked_neg()?;
        let bytes = usize::try_from(units).ok()?.checked_mul(2)?;
        (format!("utf16_{}", units), bytes)
    };
    let bit_width = bytes.checked_mul(8)?;
    let (_, data_stop) = r3_17m_skip(cursor, end, bit_width)?;
    Some((
        shape,
        format!(
            "{}.len=[{},{});{}.data=[{},{});declared={};bytes={}",
            name,
            len_start,
            len_start + 32,
            name,
            data_start,
            data_stop,
            declared,
            bytes
        ),
    ))
}

fn r3_17m_bounded_3_14(
    data: &[u8],
    cursor: &mut usize,
    end: usize,
    name: &str,
) -> Option<(String, String)> {
    let start = *cursor;
    let low = r3_17m_read_le(data, cursor, end, 3)?;
    let up = low + 8;
    let (disc_bits, disc) = if up >= 14 {
        (0usize, 0u64)
    } else {
        (1usize, r3_17m_read_le(data, cursor, end, 1)?)
    };
    let stop = *cursor;
    Some((
        format!("b3d{}_{}", disc_bits, if disc != 0 { 1 } else { 0 }),
        format!(
            "{}=[{},{});low={};disc_bits={};disc={}",
            name, start, stop, low, disc_bits, disc
        ),
    ))
}

fn r3_17m_unique_id_shape(
    data: &[u8],
    cursor: &mut usize,
    end: usize,
    net_version: i32,
    name: &str,
) -> Option<(String, String, bool)> {
    let system_start = *cursor;
    let system = r3_17m_read_le(data, cursor, end, 8)? as u8;
    let mut boundary = format!("{}.system=[{},{});system={}", name, system_start, system_start + 8, system);
    let mut needs_name = system != 0;
    let remote_shape = match system {
        0 => {
            let remote_start = *cursor;
            let split = r3_17m_read_le(data, cursor, end, 24)?;
            boundary.push_str(&format!(";{}.split=[{},{});split_nonzero={}", name, remote_start, remote_start + 24, split != 0));
            needs_name = split != 0;
            format!("split24_{}", if split == 0 { "zero" } else { "nonzero" })
        }
        1 => {
            let (a, b) = r3_17m_skip(cursor, end, 64)?;
            boundary.push_str(&format!(";{}.steam=[{},{});", name, a, b));
            "steam64".to_owned()
        }
        2 => {
            let (a0, a1) = r3_17m_skip(cursor, end, 128)?;
            let (b0, b1) = r3_17m_skip(cursor, end, 128)?;
            let (c0, c1) = r3_17m_skip(cursor, end, 64)?;
            boundary.push_str(&format!(";{}.ps_name=[{},{});{}.ps_unknown=[{},{});{}.ps_online=[{},{});", name, a0, a1, name, b0, b1, name, c0, c1));
            "playstation320".to_owned()
        }
        4 => {
            let (a, b) = r3_17m_skip(cursor, end, 64)?;
            boundary.push_str(&format!(";{}.xbox=[{},{});", name, a, b));
            "xbox64".to_owned()
        }
        5 => {
            let (a, b) = r3_17m_skip(cursor, end, 64)?;
            boundary.push_str(&format!(";{}.qq=[{},{});", name, a, b));
            "qq64".to_owned()
        }
        6 => {
            let (a0, a1) = r3_17m_skip(cursor, end, 64)?;
            let (b0, b1) = r3_17m_skip(cursor, end, 192)?;
            boundary.push_str(&format!(";{}.switch_online=[{},{});{}.switch_unknown=[{},{});", name, a0, a1, name, b0, b1));
            "switch256".to_owned()
        }
        7 => {
            let (a0, a1) = r3_17m_skip(cursor, end, 64)?;
            boundary.push_str(&format!(";{}.psynet_online=[{},{});", name, a0, a1));
            if net_version < 10 {
                let (b0, b1) = r3_17m_skip(cursor, end, 192)?;
                boundary.push_str(&format!("{}.psynet_unknown=[{},{});", name, b0, b1));
                "psynet256".to_owned()
            } else {
                "psynet64".to_owned()
            }
        }
        11 => {
            let (shape, text_boundary) = r3_17m_text_shape(data, cursor, end, &format!("{}.epic", name))?;
            boundary.push(';');
            boundary.push_str(&text_boundary);
            format!("epic_{}", shape)
        }
        _ => return None,
    };
    let local_start = *cursor;
    let _ = r3_17m_read_le(data, cursor, end, 8)?;
    boundary.push_str(&format!(";{}.local=[{},{});", name, local_start, local_start + 8));
    Some((format!("sys{}_{}", system, remote_shape), boundary, needs_name))
}

fn r3_17m_loadout_shape(
    data: &[u8],
    cursor: &mut usize,
    end: usize,
    name: &str,
) -> Option<(String, String)> {
    let version_start = *cursor;
    let version = r3_17m_read_le(data, cursor, end, 8)? as u8;
    let mut boundary = format!("{}.version=[{},{});version={}", name, version_start, version_start + 8, version);
    for field in ["body", "decal", "wheels", "rocket_trail", "antenna", "topper", "unknown1"] {
        let (a, b) = r3_17m_skip(cursor, end, 32)?;
        boundary.push_str(&format!(";{}.{}=[{},{});", name, field, a, b));
    }
    let mut shape = format!("v{}", version);
    if version > 10 {
        let (a, b) = r3_17m_skip(cursor, end, 32)?;
        boundary.push_str(&format!("{}.unknown2=[{},{});", name, a, b));
        shape.push_str(":u2");
    } else {
        shape.push_str(":nou2");
    }
    if version >= 16 {
        for field in ["engine_audio", "trail", "goal_explosion"] {
            let (a, b) = r3_17m_skip(cursor, end, 32)?;
            boundary.push_str(&format!("{}.{}=[{},{});", name, field, a, b));
        }
        shape.push_str(":specials");
    } else {
        shape.push_str(":nospecials");
    }
    if version >= 17 {
        let (a, b) = r3_17m_skip(cursor, end, 32)?;
        boundary.push_str(&format!("{}.banner=[{},{});", name, a, b));
        shape.push_str(":banner");
    } else {
        shape.push_str(":nobanner");
    }
    if version >= 19 {
        let (a, b) = r3_17m_skip(cursor, end, 32)?;
        boundary.push_str(&format!("{}.product_id=[{},{});", name, a, b));
        shape.push_str(":product");
    } else {
        shape.push_str(":noproduct");
    }
    if version >= 22 {
        for idx in 0..3 {
            let (a, b) = r3_17m_skip(cursor, end, 32)?;
            boundary.push_str(&format!("{}.v22_extra{}=[{},{});", name, idx, a, b));
        }
        shape.push_str(":extra3");
    } else {
        shape.push_str(":noextra3");
    }
    Some((shape, boundary))
}

fn r3_17m_product_shape(
    data: &[u8],
    cursor: &mut usize,
    end: usize,
    major: i32,
    minor: i32,
    net: i32,
    objects: &[String],
    name: &str,
) -> Option<(String, String)> {
    let unknown_start = *cursor;
    let unknown = r3_17m_read_le(data, cursor, end, 1)?;
    let object_start = *cursor;
    let object_id = r3_17m_read_le(data, cursor, end, 32)? as u32 as i32;
    let object_name = usize::try_from(object_id)
        .ok()
        .and_then(|idx| objects.get(idx))
        .map(String::as_str)
        .unwrap_or("");
    let mut boundary = format!(
        "{}.unknown=[{},{});unknown={};{}.object=[{},{});",
        name,
        unknown_start,
        unknown_start + 1,
        unknown,
        name,
        object_start,
        object_start + 32
    );
    let shape = if object_name == "TAGame.ProductAttribute_UserColor_TA" {
        if r3_17m_version_ge(major, minor, net, 868, 23, 8) {
            let (a, b) = r3_17m_skip(cursor, end, 32)?;
            boundary.push_str(&format!("{}.user_color_new=[{},{});", name, a, b));
            "UserColor:new32".to_owned()
        } else {
            let present_start = *cursor;
            let present = r3_17m_read_le(data, cursor, end, 1)? != 0;
            boundary.push_str(&format!("{}.user_color_present=[{},{});present={};", name, present_start, present_start + 1, present));
            if present {
                let (a, b) = r3_17m_skip(cursor, end, 31)?;
                boundary.push_str(&format!("{}.user_color_old=[{},{});", name, a, b));
                "UserColor:old31".to_owned()
            } else {
                "UserColor:none".to_owned()
            }
        }
    } else if object_name == "TAGame.ProductAttribute_Painted_TA" {
        if r3_17m_version_ge(major, minor, net, 868, 18, 0) {
            let (a, b) = r3_17m_skip(cursor, end, 31)?;
            boundary.push_str(&format!("{}.paint_new=[{},{});", name, a, b));
            "Paint:new31".to_owned()
        } else {
            let (bshape, bboundary) = r3_17m_bounded_3_14(data, cursor, end, &format!("{}.paint_old", name))?;
            boundary.push_str(&bboundary);
            format!("Paint:old:{}", bshape)
        }
    } else if object_name == "TAGame.ProductAttribute_TitleID_TA" {
        let (tshape, tboundary) = r3_17m_text_shape(data, cursor, end, &format!("{}.title", name))?;
        boundary.push_str(&tboundary);
        format!("Title:{}", tshape)
    } else if object_name == "TAGame.ProductAttribute_SpecialEdition_TA" {
        let (a, b) = r3_17m_skip(cursor, end, 31)?;
        boundary.push_str(&format!("{}.special=[{},{});", name, a, b));
        "SpecialEdition:31".to_owned()
    } else if object_name == "TAGame.ProductAttribute_TeamEdition_TA" {
        if r3_17m_version_ge(major, minor, net, 868, 18, 0) {
            let (a, b) = r3_17m_skip(cursor, end, 31)?;
            boundary.push_str(&format!("{}.team_new=[{},{});", name, a, b));
            "TeamEdition:new31".to_owned()
        } else {
            let (bshape, bboundary) = r3_17m_bounded_3_14(data, cursor, end, &format!("{}.team_old", name))?;
            boundary.push_str(&bboundary);
            format!("TeamEdition:old:{}", bshape)
        }
    } else {
        "Absent".to_owned()
    };
    Some((shape, boundary))
}

fn r3_17m_online_side_shape(
    data: &[u8],
    cursor: &mut usize,
    end: usize,
    major: i32,
    minor: i32,
    net: i32,
    objects: &[String],
    name: &str,
) -> Option<(String, String)> {
    let outer_start = *cursor;
    let outer = r3_17m_read_le(data, cursor, end, 8)? as usize;
    let mut shape = format!("{}:outer{}[", name, outer);
    let mut boundary = format!("{}.outer=[{},{});count={};", name, outer_start, outer_start + 8, outer);
    for group_idx in 0..outer {
        let count_start = *cursor;
        let count = r3_17m_read_le(data, cursor, end, 8)? as usize;
        boundary.push_str(&format!("{}.g{}.count=[{},{});count={};", name, group_idx, count_start, count_start + 8, count));
        shape.push_str(&format!("g{}:{}(", group_idx, count));
        for product_idx in 0..count {
            let pname = format!("{}.g{}.p{}", name, group_idx, product_idx);
            let (pshape, pboundary) = r3_17m_product_shape(
                data, cursor, end, major, minor, net, objects, &pname,
            )?;
            if product_idx != 0 {
                shape.push(',');
            }
            shape.push_str(&pshape);
            boundary.push_str(&pboundary);
        }
        shape.push(')');
        if group_idx + 1 != outer {
            shape.push(';');
        }
    }
    shape.push(']');
    Some((shape, boundary))
}

fn r3_17m_active_actor_shape(
    data: &[u8],
    cursor: &mut usize,
    end: usize,
    name: &str,
) -> Option<String> {
    let active_start = *cursor;
    let _ = r3_17m_read_le(data, cursor, end, 1)?;
    let actor_start = *cursor;
    let _ = r3_17m_read_le(data, cursor, end, 32)?;
    Some(format!(
        "{}.active=[{},{});{}.actor=[{},{});",
        name,
        active_start,
        active_start + 1,
        name,
        actor_start,
        actor_start + 32
    ))
}

fn r3_17m_classify(
    tag: AttributeTag,
    attribute: &Attribute,
    data: &[u8],
    start: usize,
    end: usize,
    major: i32,
    minor: i32,
    net_version: i32,
    objects: &[String],
) -> Option<(String, String, String)> {
    let mut cursor = start;
    let semantic = "decoded_variant_ok".to_owned();
    match (tag, attribute) {
        (AttributeTag::CamSettings, Attribute::CamSettings(_)) => {
            let mut boundary = String::new();
            for field in ["fov", "height", "angle", "distance", "stiffness", "swivel"] {
                let (a, b) = r3_17m_skip(&mut cursor, end, 32)?;
                boundary.push_str(&format!("{}=[{},{});", field, a, b));
            }
            let has_transition = r3_17m_version_ge(major, minor, net_version, 868, 20, 0);
            if has_transition {
                let (a, b) = r3_17m_skip(&mut cursor, end, 32)?;
                boundary.push_str(&format!("transition=[{},{});", a, b));
            }
            if cursor != end { return None; }
            Some((format!("CamSettings:f32x{}", if has_transition { 7 } else { 6 }), boundary, semantic))
        }
        (AttributeTag::TeamPaint, Attribute::TeamPaint(_)) => {
            let mut boundary = String::new();
            for (field, width) in [("team",8usize),("primary_color",8),("accent_color",8),("primary_finish",32),("accent_finish",32)] {
                let (a,b)=r3_17m_skip(&mut cursor,end,width)?;
                boundary.push_str(&format!("{}=[{},{});",field,a,b));
            }
            if cursor != end { return None; }
            Some(("TeamPaint:u8x3_u32x2".to_owned(), boundary, semantic))
        }
        (AttributeTag::TeamLoadout, Attribute::TeamLoadout(_)) => {
            let (blue_shape, blue_boundary)=r3_17m_loadout_shape(data,&mut cursor,end,"blue")?;
            let (orange_shape, orange_boundary)=r3_17m_loadout_shape(data,&mut cursor,end,"orange")?;
            if cursor != end { return None; }
            Some((format!("TeamLoadout:blue[{}]:orange[{}]",blue_shape,orange_shape),format!("{};{}",blue_boundary,orange_boundary),semantic))
        }
        (AttributeTag::ClubColors, Attribute::ClubColors(_)) => {
            let mut boundary=String::new();
            for (field,width) in [("blue_flag",1usize),("blue_color",8),("orange_flag",1),("orange_color",8)] {
                let (a,b)=r3_17m_skip(&mut cursor,end,width)?;
                boundary.push_str(&format!("{}=[{},{});",field,a,b));
            }
            if cursor != end { return None; }
            Some(("ClubColors:b1_u8_b1_u8".to_owned(),boundary,semantic))
        }
        (AttributeTag::Reservation, Attribute::Reservation(_)) => {
            let number_start=cursor;
            let _=r3_17m_read_le(data,&mut cursor,end,3)?;
            let (id_shape,id_boundary,needs_name)=r3_17m_unique_id_shape(data,&mut cursor,end,net_version,"id")?;
            let mut boundary=format!("number=[{},{});{};",number_start,number_start+3,id_boundary);
            let name_shape=if needs_name {
                let (shape,b)=r3_17m_text_shape(data,&mut cursor,end,"name")?;
                boundary.push_str(&b);
                shape
            } else { "none".to_owned() };
            let u1=cursor; let _=r3_17m_read_le(data,&mut cursor,end,1)?;
            let u2=cursor; let _=r3_17m_read_le(data,&mut cursor,end,1)?;
            boundary.push_str(&format!(";unknown1=[{},{});unknown2=[{},{});",u1,u1+1,u2,u2+1));
            let has_u3=r3_17m_version_ge(major,minor,net_version,868,12,0);
            if has_u3 {
                let a=cursor; let _=r3_17m_read_le(data,&mut cursor,end,6)?;
                boundary.push_str(&format!("unknown3=[{},{});",a,a+6));
            }
            if cursor != end { return None; }
            Some((format!("Reservation:{}:name_{}:u3_{}",id_shape,name_shape,has_u3),boundary,semantic))
        }
        (AttributeTag::StatEvent, Attribute::StatEvent(_)) => {
            let a=cursor; let _=r3_17m_read_le(data,&mut cursor,end,1)?;
            let b=cursor; let _=r3_17m_read_le(data,&mut cursor,end,32)?;
            if cursor != end { return None; }
            Some(("StatEvent:b1_i32".to_owned(),format!("unknown1=[{},{});object_id=[{},{});",a,a+1,b,b+32),semantic))
        }
        (AttributeTag::PlayerHistoryKey, Attribute::PlayerHistoryKey(_)) => {
            let a=cursor; let _=r3_17m_read_le(data,&mut cursor,end,14)?;
            if cursor != end { return None; }
            Some(("PlayerHistoryKey:u14".to_owned(),format!("key=[{},{});",a,a+14),semantic))
        }
        (AttributeTag::DemolishFx, Attribute::DemolishFx(_)) => {
            let mut boundary=String::new();
            for (field,width) in [("custom_demo_flag",1usize),("custom_demo_id",32),("attacker_flag",1),("attacker",32),("victim_flag",1),("victim",32)] {
                let (a,b)=r3_17m_skip(&mut cursor,end,width)?;
                boundary.push_str(&format!("{}=[{},{});",field,a,b));
            }
            let (av_shape,av_boundary)=r3_17m_vector_shape(data,&mut cursor,end,net_version,"attack_velocity")?;
            let (vv_shape,vv_boundary)=r3_17m_vector_shape(data,&mut cursor,end,net_version,"victim_velocity")?;
            boundary.push_str(&av_boundary); boundary.push(';'); boundary.push_str(&vv_boundary);
            if cursor != end { return None; }
            Some((format!("DemolishFx:{}:{}",av_shape,vv_shape),boundary,semantic))
        }
        (AttributeTag::DemolishExtended, Attribute::DemolishExtended(_)) => {
            let mut boundary=String::new();
            boundary.push_str(&r3_17m_active_actor_shape(data,&mut cursor,end,"attacker_pri")?);
            boundary.push_str(&r3_17m_active_actor_shape(data,&mut cursor,end,"self_demo")?);
            let sd=cursor; let _=r3_17m_read_le(data,&mut cursor,end,1)?;
            boundary.push_str(&format!("self_demolish=[{},{});",sd,sd+1));
            boundary.push_str(&r3_17m_active_actor_shape(data,&mut cursor,end,"goal_explosion_owner")?);
            boundary.push_str(&r3_17m_active_actor_shape(data,&mut cursor,end,"attacker")?);
            boundary.push_str(&r3_17m_active_actor_shape(data,&mut cursor,end,"victim")?);
            let (av_shape,av_boundary)=r3_17m_vector_shape(data,&mut cursor,end,net_version,"attacker_velocity")?;
            let (vv_shape,vv_boundary)=r3_17m_vector_shape(data,&mut cursor,end,net_version,"victim_velocity")?;
            boundary.push_str(&av_boundary); boundary.push(';'); boundary.push_str(&vv_boundary);
            if cursor != end { return None; }
            Some((format!("DemolishExtended:activex5:{}:{}",av_shape,vv_shape),boundary,semantic))
        }
        (AttributeTag::ExtendedExplosion, Attribute::ExtendedExplosion(_)) => {
            let flag=cursor; let _=r3_17m_read_le(data,&mut cursor,end,1)?;
            let actor=cursor; let _=r3_17m_read_le(data,&mut cursor,end,32)?;
            let (loc_shape,loc_boundary)=r3_17m_vector_shape(data,&mut cursor,end,net_version,"location")?;
            let u1=cursor; let _=r3_17m_read_le(data,&mut cursor,end,1)?;
            let secondary=cursor; let _=r3_17m_read_le(data,&mut cursor,end,32)?;
            if cursor != end { return None; }
            Some((format!("ExtendedExplosion:{}",loc_shape),format!("flag=[{},{});actor=[{},{});{};unknown1=[{},{});secondary_actor=[{},{});",flag,flag+1,actor,actor+32,loc_boundary,u1,u1+1,secondary,secondary+32),semantic))
        }
        (AttributeTag::LoadoutsOnline, Attribute::LoadoutsOnline(_)) => {
            let (blue_shape,blue_boundary)=r3_17m_online_side_shape(data,&mut cursor,end,major,minor,net_version,objects,"blue")?;
            let (orange_shape,orange_boundary)=r3_17m_online_side_shape(data,&mut cursor,end,major,minor,net_version,objects,"orange")?;
            let u1=cursor; let _=r3_17m_read_le(data,&mut cursor,end,1)?;
            let u2=cursor; let _=r3_17m_read_le(data,&mut cursor,end,1)?;
            if cursor != end { return None; }
            Some((format!("LoadoutsOnline:{}:{}",blue_shape,orange_shape),format!("{};{};unknown1=[{},{});unknown2=[{},{});",blue_boundary,orange_boundary,u1,u1+1,u2,u2+1),semantic))
        }
        _ => None,
    }
}

'''
    s = s[:start] + classifier + s[end:]
    frame.write_text(s, encoding="utf-8", newline="\n")

    old_probe = root / "examples/r3_17i_probe.rs"
    new_probe = root / "examples/r3_17m_probe.rs"
    if not old_probe.is_file():
        raise SystemExit("base patch did not create r3_17i_probe.rs")
    p = old_probe.read_text(encoding="utf-8")
    p = p.replace("r3_17i", "r3_17m").replace("R3_17I", "R3_17M")
    new_probe.write_text(p, encoding="utf-8", newline="\n")
    old_probe.unlink()

    cargo = root / "Cargo.toml"
    c = cargo.read_text(encoding="utf-8")
    c = c.replace("r3_17i_probe", "r3_17m_probe")
    cargo.write_text(c, encoding="utf-8", newline="\n")

    print("R3.17M Boxcars transformation applied")


if __name__ == "__main__":
    main()
