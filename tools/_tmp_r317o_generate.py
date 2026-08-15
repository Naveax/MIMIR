from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

EXPECTED_MAIN = "3392c28ba8ec7d72766303646c0ceb57ed1e5a19"
EXPECTED_PROD = "7390e3b145372252caaa8fa1fe3e0cd13b83336c"
EXPECTED_CONTRACT = "c8ebb872e510574bb69ab28c719f415ece8b7665"
EXPECTED_GROUP_SHA = "80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b"
EXPECTED_ROWS = 161

ROOT = Path(__file__).resolve().parents[1]
GROUP_PATH = ROOT / "docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl"
LIB_PATH = ROOT / "crates/mimir-replay/src/lib.rs"
ALLOW_PATH = ROOT / "crates/mimir-replay/src/k4_admitted_groups.rs"
NATIVE_PATH = ROOT / "crates/mimir-replay/src/k4_native.rs"
TEST_PATH = ROOT / "crates/mimir-replay/tests/r3_17o_k4_attribute_decoder.rs"

TAG_VARIANTS = {
    "CamSettings": "CamSettings",
    "ClubColors": "ClubColors",
    "DemolishExtended": "DemolishExtended",
    "DemolishFx": "DemolishFx",
    "ExtendedExplosion": "ExtendedExplosion",
    "LoadoutsOnline": "LoadoutsOnline",
    "PlayerHistoryKey": "PlayerHistoryKey",
    "Reservation": "Reservation",
    "StatEvent": "StatEvent",
    "TeamLoadout": "TeamLoadout",
    "TeamPaint": "TeamPaint",
}

PRODUCT_IDS = {
    "Paint:new31": 0,
    "UserColor:new32": 1,
    "SpecialEdition:31": 3,
    "TeamEdition:new31": 4,
}

OBJECT_TABLE = [
    "TAGame.ProductAttribute_Painted_TA",
    "TAGame.ProductAttribute_UserColor_TA",
    "TAGame.ProductAttribute_TitleID_TA",
    "TAGame.ProductAttribute_SpecialEdition_TA",
    "TAGame.ProductAttribute_TeamEdition_TA",
]


class Bits:
    def __init__(self) -> None:
        self.bits: list[int] = []

    def put(self, value: int, width: int) -> None:
        if width < 0:
            raise ValueError(width)
        if value < 0:
            value &= (1 << width) - 1
        if width and value >= (1 << width):
            raise ValueError((value, width))
        for i in range(width):
            self.bits.append((value >> i) & 1)

    def zeros(self, width: int) -> None:
        self.bits.extend([0] * width)

    def bytes(self) -> bytes:
        out = bytearray((len(self.bits) + 7) // 8)
        for i, bit in enumerate(self.bits):
            if bit:
                out[i // 8] |= 1 << (i % 8)
        return bytes(out)


def load_rows() -> list[dict]:
    raw = GROUP_PATH.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECTED_GROUP_SHA:
        raise SystemExit(f"group sha mismatch: {sha}")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(f"expected {EXPECTED_ROWS} rows, got {len(rows)}")
    seen = set()
    for row in rows:
        key = (
            row["attribute_tag"],
            row["version_major"],
            row["version_minor"],
            row["net_version"],
            row["is_rl_223"],
            row["payload_width"],
            row["shape"],
        )
        if key in seen:
            raise SystemExit(f"duplicate group: {key}")
        seen.add(key)
        if row["attribute_tag"] not in TAG_VARIANTS:
            raise SystemExit(f"unexpected tag: {row['attribute_tag']}")
    return rows


def emit_text(bits: Bits, token: str) -> None:
    if token == "empty":
        bits.put(0, 32)
        return
    m = re.fullmatch(r"w1252_(\d+)", token)
    if m:
        n = int(m.group(1))
        bits.put(n, 32)
        bits.zeros(n * 8)
        return
    m = re.fullmatch(r"utf16_(\d+)", token)
    if m:
        n = int(m.group(1))
        bits.put((-n) & 0xFFFFFFFF, 32)
        bits.zeros(n * 16)
        return
    raise ValueError(f"unknown text token {token}")


def emit_vector(bits: Bits, token: str, expected_name: str | None = None) -> None:
    m = re.fullmatch(r"([^:]+):sb(\d+):h([45]):cw(\d+)", token)
    if not m:
        raise ValueError(f"bad vector token {token}")
    name, sb_s, h_s, cw_s = m.groups()
    if expected_name is not None and name != expected_name:
        raise ValueError((name, expected_name))
    sb = int(sb_s)
    header = int(h_s)
    cw = int(cw_s)
    if cw != sb + 2:
        raise ValueError(token)
    if header == 4:
        if not (6 <= sb <= 15):
            raise ValueError(f"invalid h4 vector {token}")
        bits.put(sb, 4)
    else:
        if 0 <= sb <= 5:
            bits.put(sb, 4)
            bits.put(0, 1)
        elif 16 <= sb <= 19:
            bits.put(sb - 16, 4)
            bits.put(1, 1)
        else:
            raise ValueError(f"invalid h5 vector {token}")
    bits.zeros(cw * 3)


def emit_loadout_side(bits: Bits, token: str) -> None:
    m = re.fullmatch(
        r"v(\d+):(u2|nou2):(specials|nospecials):(banner|nobanner):(product|noproduct):(extra3|noextra3)",
        token,
    )
    if not m:
        raise ValueError(f"bad loadout token {token}")
    version = int(m.group(1))
    bits.put(version, 8)
    bits.zeros(7 * 32)
    if m.group(2) == "u2":
        bits.zeros(32)
    if m.group(3) == "specials":
        bits.zeros(3 * 32)
    if m.group(4) == "banner":
        bits.zeros(32)
    if m.group(5) == "product":
        bits.zeros(32)
    if m.group(6) == "extra3":
        bits.zeros(3 * 32)


def emit_reservation(bits: Bits, shape: str) -> None:
    body = shape[len("Reservation:"):]
    id_shape, rest = body.split(":name_", 1)
    name_shape, u3 = rest.rsplit(":u3_", 1)
    if u3 != "true":
        raise ValueError(f"current lane expected u3_true: {shape}")
    bits.zeros(3)
    needs_name = True
    if id_shape == "sys0_split24_zero":
        bits.put(0, 8); bits.zeros(24); needs_name = False
    elif id_shape == "sys0_split24_nonzero":
        bits.put(0, 8); bits.put(1, 24)
    elif id_shape == "sys1_steam64":
        bits.put(1, 8); bits.zeros(64)
    elif id_shape == "sys2_playstation320":
        bits.put(2, 8); bits.zeros(128 + 128 + 64)
    elif id_shape == "sys4_xbox64":
        bits.put(4, 8); bits.zeros(64)
    elif id_shape == "sys5_qq64":
        bits.put(5, 8); bits.zeros(64)
    elif id_shape == "sys6_switch256":
        bits.put(6, 8); bits.zeros(64 + 192)
    elif id_shape == "sys7_psynet64":
        bits.put(7, 8); bits.zeros(64)
    elif id_shape.startswith("sys11_epic_"):
        bits.put(11, 8); emit_text(bits, id_shape[len("sys11_epic_"):])
    else:
        raise ValueError(f"unsupported reservation id shape {id_shape}")
    bits.zeros(8)
    if needs_name:
        if name_shape == "none": raise ValueError(shape)
        emit_text(bits, name_shape)
    elif name_shape != "none":
        raise ValueError(shape)
    bits.zeros(8)


def split_side(shape: str, start: int) -> tuple[str, int]:
    open_idx = shape.index("[", start)
    close_idx = shape.index("]", open_idx)
    return shape[start:close_idx + 1], close_idx + 1


def emit_product(bits: Bits, token: str) -> None:
    bits.put(0, 1)
    if token.startswith("Title:"):
        bits.put(2, 32); emit_text(bits, token[len("Title:"):]); return
    if token not in PRODUCT_IDS:
        raise ValueError(f"unobserved/unsupported product token in contract: {token}")
    bits.put(PRODUCT_IDS[token], 32)
    if token == "UserColor:new32": bits.zeros(32)
    else: bits.zeros(31)


def emit_online_side(bits: Bits, side: str) -> None:
    m = re.fullmatch(r"(blue|orange):outer(\d+)\[(.*)\]", side)
    if not m: raise ValueError(side[:120])
    outer = int(m.group(2)); groups = [] if not m.group(3) else m.group(3).split(";")
    if len(groups) != outer: raise ValueError((outer, len(groups)))
    bits.put(outer, 8)
    for idx, group in enumerate(groups):
        gm = re.fullmatch(r"g(\d+):(\d+)\((.*)\)", group)
        if not gm or int(gm.group(1)) != idx: raise ValueError(group)
        count = int(gm.group(2)); products = [] if gm.group(3) == "" else gm.group(3).split(",")
        if len(products) != count: raise ValueError(group)
        bits.put(count, 8)
        for product in products: emit_product(bits, product)


def emit_shape(shape: str) -> Bits:
    b = Bits()
    if shape == "CamSettings:f32x7": b.zeros(224)
    elif shape == "TeamPaint:u8x3_u32x2": b.zeros(88)
    elif shape == "ClubColors:b1_u8_b1_u8": b.zeros(18)
    elif shape == "StatEvent:b1_i32": b.zeros(33)
    elif shape == "PlayerHistoryKey:u14": b.zeros(14)
    elif shape.startswith("TeamLoadout:blue["):
        m = re.fullmatch(r"TeamLoadout:blue\[(.*)\]:orange\[(.*)\]", shape); assert m
        emit_loadout_side(b, m.group(1)); emit_loadout_side(b, m.group(2))
    elif shape.startswith("Reservation:"): emit_reservation(b, shape)
    elif shape.startswith("DemolishFx:"):
        left, right = shape[len("DemolishFx:"):].split(":victim_velocity:", 1)
        b.zeros(99); emit_vector(b, left, "attack_velocity"); emit_vector(b, "victim_velocity:" + right, "victim_velocity")
    elif shape.startswith("DemolishExtended:activex5:"):
        left, right = shape[len("DemolishExtended:activex5:"):].split(":victim_velocity:", 1)
        b.zeros(166); emit_vector(b, left, "attacker_velocity"); emit_vector(b, "victim_velocity:" + right, "victim_velocity")
    elif shape.startswith("ExtendedExplosion:"):
        b.zeros(33); emit_vector(b, shape[len("ExtendedExplosion:"):], "location"); b.zeros(33)
    elif shape.startswith("LoadoutsOnline:blue:"):
        rest = shape[len("LoadoutsOnline:"):]; blue, pos = split_side(rest, 0)
        if not rest[pos:].startswith(":orange:"): raise ValueError(shape)
        emit_online_side(b, blue); emit_online_side(b, rest[pos + 1:]); b.zeros(2)
    else: raise ValueError(f"unhandled shape {shape}")
    return b


def rust_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def generate_allowlist(rows: list[dict]) -> str:
    lines = [
        "use super::ReplayNetworkAttributeTagV1;", "",
        "#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]",
        "pub struct ReplayNetworkK4AdmittedGroupV1 {",
        "    pub attribute_tag: ReplayNetworkAttributeTagV1,", "    pub version_major: i32,", "    pub version_minor: i32,", "    pub net_version: i32,", "    pub is_rl_223: bool,", "    pub payload_width: u64,", "    pub structural_shape: &'static str,", "}", "",
        "macro_rules! g {", "    ($tag:ident, $major:expr, $minor:expr, $net:expr, $rl223:expr, $width:expr, $shape:expr) => {", "        ReplayNetworkK4AdmittedGroupV1 {", "            attribute_tag: ReplayNetworkAttributeTagV1::$tag,", "            version_major: $major,", "            version_minor: $minor,", "            net_version: $net,", "            is_rl_223: $rl223,", "            payload_width: $width,", "            structural_shape: $shape,", "        }", "    };", "}", "",
        "pub const R3_17N_K4_ADMITTED_GROUPS_V1: &[ReplayNetworkK4AdmittedGroupV1] = &[",
    ]
    for r in rows:
        lines.append(f"    g!({TAG_VARIANTS[r['attribute_tag']]}, {r['version_major']}, {r['version_minor']}, {r['net_version']}, {str(r['is_rl_223']).lower()}, {r['payload_width']}u64, {rust_string(r['shape'])}),")
    lines += [
        "];", "", "pub(crate) fn contains(", "    attribute_tag: ReplayNetworkAttributeTagV1,", "    version_major: i32,", "    version_minor: i32,", "    net_version: i32,", "    is_rl_223: bool,", "    payload_width: u64,", "    structural_shape: &str,", ") -> bool {",
        "    R3_17N_K4_ADMITTED_GROUPS_V1.iter().any(|group| {", "        group.attribute_tag == attribute_tag", "            && group.version_major == version_major", "            && group.version_minor == version_minor", "            && group.net_version == net_version", "            && group.is_rl_223 == is_rl_223", "            && group.payload_width == payload_width", "            && group.structural_shape == structural_shape", "    })", "}", "",
    ]
    return "\n".join(lines)


NATIVE_RS = r'''use super::{
    decode_network_windows1252, MimirError, NetworkBitCursor, ReplayNetworkAttributeTagV1,
    ReplayNetworkTextEncodingV1, ReplayNetworkTextV1, ReplayNetworkVector3V1, Result,
};
use crate::k4_admitted_groups;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4DecodeContextV1 { pub version_major:i32, pub version_minor:i32, pub net_version:i32, pub is_rl_223:bool }
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4LoadoutV1 { pub version:u8, pub base_fields:Vec<u32>, pub unknown2:Option<u32>, pub specials:Vec<u32>, pub banner:Option<u32>, pub product_id:Option<u32>, pub v22_extras:Vec<u32> }
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkK4ReservationIdV1 {
    SplitScreen{split_id:u32,local_id:u8}, Steam{online_id:u64,local_id:u8}, PlayStation{name_bytes:Vec<u8>,unknown:Vec<u8>,online_id:u64,local_id:u8}, Xbox{online_id:u64,local_id:u8}, Qq{online_id:u64,local_id:u8}, Switch{online_id:u64,unknown:Vec<u8>,local_id:u8}, PsyNet{online_id:u64,local_id:u8}, Epic{account_id:ReplayNetworkTextV1,local_id:u8}
}
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4ReservationV1 { pub number:u8, pub player_id:ReplayNetworkK4ReservationIdV1, pub name:Option<ReplayNetworkTextV1>, pub unknown1:bool, pub unknown2:bool, pub unknown3:Option<u8> }
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4ActiveActorV1 { pub active:bool, pub actor:i32 }
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkK4ProductValueV1 { UserColor(u32), Paint(u32), Title(ReplayNetworkTextV1), SpecialEdition(u32), TeamEdition(u32) }
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4OnlineProductV1 { pub unknown:bool, pub object_id:i32, pub value:ReplayNetworkK4ProductValueV1 }
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ReplayNetworkK4ValueV1 {
    CamSettings{raw_f32_bits:Vec<u32>}, TeamPaint{team:u8,primary_color:u8,accent_color:u8,primary_finish:u32,accent_finish:u32}, TeamLoadout{blue:ReplayNetworkK4LoadoutV1,orange:ReplayNetworkK4LoadoutV1}, ClubColors{blue_flag:bool,blue_color:u8,orange_flag:bool,orange_color:u8}, Reservation(ReplayNetworkK4ReservationV1), StatEvent{unknown1:bool,object_id:i32}, PlayerHistoryKey(u16),
    DemolishFx{custom_demo_flag:bool,custom_demo_id:i32,attacker_flag:bool,attacker:i32,victim_flag:bool,victim:i32,attack_velocity:ReplayNetworkVector3V1,victim_velocity:ReplayNetworkVector3V1},
    DemolishExtended{attacker_pri:ReplayNetworkK4ActiveActorV1,self_demo:ReplayNetworkK4ActiveActorV1,self_demolish:bool,goal_explosion_owner:ReplayNetworkK4ActiveActorV1,attacker:ReplayNetworkK4ActiveActorV1,victim:ReplayNetworkK4ActiveActorV1,attacker_velocity:ReplayNetworkVector3V1,victim_velocity:ReplayNetworkVector3V1},
    ExtendedExplosion{flag:bool,actor:i32,location:ReplayNetworkVector3V1,unknown1:bool,secondary_actor:i32}, LoadoutsOnline{blue:Vec<Vec<ReplayNetworkK4OnlineProductV1>>,orange:Vec<Vec<ReplayNetworkK4OnlineProductV1>>,unknown1:bool,unknown2:bool}
}
impl ReplayNetworkK4ValueV1 { pub fn attribute_tag(&self)->ReplayNetworkAttributeTagV1 { match self { Self::CamSettings{..}=>ReplayNetworkAttributeTagV1::CamSettings,Self::TeamPaint{..}=>ReplayNetworkAttributeTagV1::TeamPaint,Self::TeamLoadout{..}=>ReplayNetworkAttributeTagV1::TeamLoadout,Self::ClubColors{..}=>ReplayNetworkAttributeTagV1::ClubColors,Self::Reservation(_)=>ReplayNetworkAttributeTagV1::Reservation,Self::StatEvent{..}=>ReplayNetworkAttributeTagV1::StatEvent,Self::PlayerHistoryKey(_)=>ReplayNetworkAttributeTagV1::PlayerHistoryKey,Self::DemolishFx{..}=>ReplayNetworkAttributeTagV1::DemolishFx,Self::DemolishExtended{..}=>ReplayNetworkAttributeTagV1::DemolishExtended,Self::ExtendedExplosion{..}=>ReplayNetworkAttributeTagV1::ExtendedExplosion,Self::LoadoutsOnline{..}=>ReplayNetworkAttributeTagV1::LoadoutsOnline } } }
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkK4DecodeV1 { pub attribute_tag:ReplayNetworkAttributeTagV1,pub payload_start_bit:u64,pub payload_end_bit:u64,pub payload_width:u64,pub structural_shape:String,pub value:ReplayNetworkK4ValueV1 }

fn k4_error(category:&str,detail:impl Into<String>)->MimirError{MimirError::message(format!("replay network k4 error: {category}: {}",detail.into()))}
fn reset(cursor:&mut NetworkBitCursor<'_>,start:usize){cursor.bit_position=start;debug_assert_eq!(cursor.position_bits(),start);}
fn read_bits(cursor:&mut NetworkBitCursor<'_>,width:usize)->Result<u64>{if cursor.remaining_bits()<width{return Err(k4_error("insufficient-bits",format!("need {width} bits at position {}, but only {} remain",cursor.position_bits(),cursor.remaining_bits())));}cursor.read_bits_le(width).map_err(|e|k4_error("insufficient-bits",format!("bit read failed: {e}")))}
fn read_u8(c:&mut NetworkBitCursor<'_>)->Result<u8>{Ok(read_bits(c,8)? as u8)} fn read_u32(c:&mut NetworkBitCursor<'_>)->Result<u32>{Ok(read_bits(c,32)? as u32)} fn read_i32(c:&mut NetworkBitCursor<'_>)->Result<i32>{Ok(read_u32(c)? as i32)} fn read_u64(c:&mut NetworkBitCursor<'_>)->Result<u64>{read_bits(c,64)}
fn read_bytes(c:&mut NetworkBitCursor<'_>,count:usize)->Result<Vec<u8>>{let required=count.checked_mul(8).ok_or_else(||k4_error("invalid-length-or-count","byte count bit width overflows"))?;if c.remaining_bits()<required{return Err(k4_error("insufficient-bits",format!("need {required} byte-content bits at position {}, but only {} remain",c.position_bits(),c.remaining_bits())));}let mut out=Vec::new();out.try_reserve_exact(count).map_err(|_|k4_error("invalid-length-or-count",format!("cannot reserve {count} bytes")))?;for _ in 0..count{out.push(read_u8(c)?);}Ok(out)}
fn decode_text(c:&mut NetworkBitCursor<'_>)->Result<(ReplayNetworkTextV1,String)>{let d=read_i32(c)?;if d==0{return Ok((ReplayNetworkTextV1{value:String::new(),declared_length:0,encoding:ReplayNetworkTextEncodingV1::Empty},"empty".to_owned()));}if d>0{let n=usize::try_from(d).map_err(|_|k4_error("invalid-length-or-count",format!("positive text length {d} does not fit usize")))?;let bytes=read_bytes(c,n)?;let content=&bytes[..n-1];return Ok((ReplayNetworkTextV1{value:decode_network_windows1252(content),declared_length:d,encoding:ReplayNetworkTextEncodingV1::Windows1252},format!("w1252_{d}")));}if d==i32::MIN{return Err(k4_error("invalid-length-or-count","i32::MIN cannot be negated for UTF-16 length"));}let units=usize::try_from(-d).map_err(|_|k4_error("invalid-length-or-count",format!("UTF-16 length {d} does not fit usize")))?;let count=units.checked_mul(2).ok_or_else(||k4_error("invalid-length-or-count","UTF-16 byte count overflows"))?;let bytes=read_bytes(c,count)?;let content=&bytes[..count-2];let mut u=Vec::new();u.try_reserve_exact(content.len()/2).map_err(|_|k4_error("invalid-length-or-count","UTF-16 reserve failed"))?;for p in content.chunks_exact(2){u.push(u16::from_le_bytes([p[0],p[1]]));}Ok((ReplayNetworkTextV1{value:String::from_utf16_lossy(&u),declared_length:d,encoding:ReplayNetworkTextEncodingV1::Utf16Le},format!("utf16_{}",-d)))}
fn validate_context(x:ReplayNetworkK4DecodeContextV1)->Result<()>{if x.version_major!=868||x.version_minor!=32||x.net_version!=10{return Err(k4_error("unadmitted-context",format!("K4 requires replay version 868.32 / net10, got {}.{} / net{}",x.version_major,x.version_minor,x.net_version)));}Ok(())}
fn decode_vector(c:&mut NetworkBitCursor<'_>,name:&str)->Result<(ReplayNetworkVector3V1,String)>{let low=read_bits(c,4)? as u8;let candidate=low+16;let(selected,h)=if candidate<22{let d=read_bits(c,1)?!=0;(if d{candidate}else{low},5u8)}else{(low,4u8)};if selected>=20{return Err(k4_error("unadmitted-k4-shape",format!("vector selected size {selected} is not admitted")));}let cw=selected+2;let x=read_bits(c,cw as usize)? as u32;let y=read_bits(c,cw as usize)? as u32;let z=read_bits(c,cw as usize)? as u32;let bias=1i64<<(selected+1);let f=|r:u32|(i64::from(r)-bias)as f32/100.0;Ok((ReplayNetworkVector3V1{selected_size_bits:selected,component_width:cw,raw_x:x,raw_y:y,raw_z:z,x:f(x),y:f(y),z:f(z)},format!("{name}:sb{selected}:h{h}:cw{cw}")))}
fn decode_loadout(c:&mut NetworkBitCursor<'_>)->Result<(ReplayNetworkK4LoadoutV1,String)>{let v=read_u8(c)?;let mut base=Vec::with_capacity(7);for _ in 0..7{base.push(read_u32(c)?);}let(u2,u2s)=if v>10{(Some(read_u32(c)?),"u2")}else{(None,"nou2")};let(sp,sps)=if v>=16{(vec![read_u32(c)?,read_u32(c)?,read_u32(c)?],"specials")}else{(Vec::new(),"nospecials")};let(ban,bans)=if v>=17{(Some(read_u32(c)?),"banner")}else{(None,"nobanner")};let(prod,prods)=if v>=19{(Some(read_u32(c)?),"product")}else{(None,"noproduct")};let(ex,exs)=if v>=22{(vec![read_u32(c)?,read_u32(c)?,read_u32(c)?],"extra3")}else{(Vec::new(),"noextra3")};Ok((ReplayNetworkK4LoadoutV1{version:v,base_fields:base,unknown2:u2,specials:sp,banner:ban,product_id:prod,v22_extras:ex},format!("v{v}:{u2s}:{sps}:{bans}:{prods}:{exs}")))}
fn decode_reservation_id(c:&mut NetworkBitCursor<'_>,ctx:ReplayNetworkK4DecodeContextV1)->Result<(ReplayNetworkK4ReservationIdV1,String,bool)>{let s=read_u8(c)?;let(remote,shape,needs)=match s{0=>{let split=read_bits(c,24)? as u32;(ReplayNetworkK4ReservationIdV1::SplitScreen{split_id:split,local_id:0},format!("sys0_split24_{}",if split==0{"zero"}else{"nonzero"}),split!=0)},1=>(ReplayNetworkK4ReservationIdV1::Steam{online_id:read_u64(c)?,local_id:0},"sys1_steam64".to_owned(),true),2=>(ReplayNetworkK4ReservationIdV1::PlayStation{name_bytes:read_bytes(c,16)?,unknown:read_bytes(c,16)?,online_id:read_u64(c)?,local_id:0},"sys2_playstation320".to_owned(),true),4=>(ReplayNetworkK4ReservationIdV1::Xbox{online_id:read_u64(c)?,local_id:0},"sys4_xbox64".to_owned(),true),5=>(ReplayNetworkK4ReservationIdV1::Qq{online_id:read_u64(c)?,local_id:0},"sys5_qq64".to_owned(),true),6=>(ReplayNetworkK4ReservationIdV1::Switch{online_id:read_u64(c)?,unknown:read_bytes(c,24)?,local_id:0},"sys6_switch256".to_owned(),true),7=>{let id=read_u64(c)?;if ctx.net_version<10{let _=read_bytes(c,24)?;return Err(k4_error("unadmitted-context","net<10 PsyNet is outside R3.17N"));}(ReplayNetworkK4ReservationIdV1::PsyNet{online_id:id,local_id:0},"sys7_psynet64".to_owned(),true)},11=>{let(t,ts)=decode_text(c)?;(ReplayNetworkK4ReservationIdV1::Epic{account_id:t,local_id:0},format!("sys11_epic_{ts}"),true)},o=>return Err(k4_error("unadmitted-k4-shape",format!("reservation unique-id system {o} is unadmitted")))};let local=read_u8(c)?;let remote=match remote{ReplayNetworkK4ReservationIdV1::SplitScreen{split_id,..}=>ReplayNetworkK4ReservationIdV1::SplitScreen{split_id,local_id:local},ReplayNetworkK4ReservationIdV1::Steam{online_id,..}=>ReplayNetworkK4ReservationIdV1::Steam{online_id,local_id:local},ReplayNetworkK4ReservationIdV1::PlayStation{name_bytes,unknown,online_id,..}=>ReplayNetworkK4ReservationIdV1::PlayStation{name_bytes,unknown,online_id,local_id:local},ReplayNetworkK4ReservationIdV1::Xbox{online_id,..}=>ReplayNetworkK4ReservationIdV1::Xbox{online_id,local_id:local},ReplayNetworkK4ReservationIdV1::Qq{online_id,..}=>ReplayNetworkK4ReservationIdV1::Qq{online_id,local_id:local},ReplayNetworkK4ReservationIdV1::Switch{online_id,unknown,..}=>ReplayNetworkK4ReservationIdV1::Switch{online_id,unknown,local_id:local},ReplayNetworkK4ReservationIdV1::PsyNet{online_id,..}=>ReplayNetworkK4ReservationIdV1::PsyNet{online_id,local_id:local},ReplayNetworkK4ReservationIdV1::Epic{account_id,..}=>ReplayNetworkK4ReservationIdV1::Epic{account_id,local_id:local}};Ok((remote,shape,needs))}
fn active(c:&mut NetworkBitCursor<'_>)->Result<ReplayNetworkK4ActiveActorV1>{Ok(ReplayNetworkK4ActiveActorV1{active:read_bits(c,1)?!=0,actor:read_i32(c)?})}
fn product(c:&mut NetworkBitCursor<'_>,objects:&[String])->Result<(ReplayNetworkK4OnlineProductV1,String)>{let unknown=read_bits(c,1)?!=0;let id=read_i32(c)?;let slot=usize::try_from(id).map_err(|_|k4_error("unadmitted-k4-shape",format!("negative product object id {id}")))?;let name=objects.get(slot).ok_or_else(||k4_error("unadmitted-k4-shape",format!("product object id {id} outside table")))?;let(value,shape)=match name.as_str(){"TAGame.ProductAttribute_UserColor_TA"=>(ReplayNetworkK4ProductValueV1::UserColor(read_u32(c)?),"UserColor:new32".to_owned()),"TAGame.ProductAttribute_Painted_TA"=>(ReplayNetworkK4ProductValueV1::Paint(read_bits(c,31)? as u32),"Paint:new31".to_owned()),"TAGame.ProductAttribute_TitleID_TA"=>{let(t,s)=decode_text(c)?;(ReplayNetworkK4ProductValueV1::Title(t),format!("Title:{s}"))},"TAGame.ProductAttribute_SpecialEdition_TA"=>(ReplayNetworkK4ProductValueV1::SpecialEdition(read_bits(c,31)? as u32),"SpecialEdition:31".to_owned()),"TAGame.ProductAttribute_TeamEdition_TA"=>(ReplayNetworkK4ProductValueV1::TeamEdition(read_bits(c,31)? as u32),"TeamEdition:new31".to_owned()),other=>return Err(k4_error("unadmitted-k4-shape",format!("unknown product attribute object branch {other:?}")))};Ok((ReplayNetworkK4OnlineProductV1{unknown,object_id:id,value},shape))}
fn online_side(c:&mut NetworkBitCursor<'_>,objects:&[String],name:&str)->Result<(Vec<Vec<ReplayNetworkK4OnlineProductV1>>,String)>{let outer=read_u8(c)? as usize;let mut groups=Vec::new();groups.try_reserve_exact(outer).map_err(|_|k4_error("invalid-length-or-count","outer reserve"))?;let mut shape=format!("{name}:outer{outer}[");for gi in 0..outer{let count=read_u8(c)? as usize;let mut ps=Vec::new();ps.try_reserve_exact(count).map_err(|_|k4_error("invalid-length-or-count","product reserve"))?;if gi!=0{shape.push(';');}shape.push_str(&format!("g{gi}:{count}("));for pi in 0..count{let(p,s)=product(c,objects)?;if pi!=0{shape.push(',');}shape.push_str(&s);ps.push(p);}shape.push(')');groups.push(ps);}shape.push(']');Ok((groups,shape))}
fn decode_one(c:&mut NetworkBitCursor<'_>,tag:ReplayNetworkAttributeTagV1,ctx:ReplayNetworkK4DecodeContextV1,objects:&[String])->Result<(ReplayNetworkK4ValueV1,String)>{match tag{ReplayNetworkAttributeTagV1::CamSettings=>{let mut v=Vec::with_capacity(7);for _ in 0..6{v.push(read_u32(c)?);}let t=(ctx.version_major,ctx.version_minor,ctx.net_version)>=(868,20,0);if t{v.push(read_u32(c)?);}Ok((ReplayNetworkK4ValueV1::CamSettings{raw_f32_bits:v},format!("CamSettings:f32x{}",if t{7}else{6})))}ReplayNetworkAttributeTagV1::TeamPaint=>Ok((ReplayNetworkK4ValueV1::TeamPaint{team:read_u8(c)?,primary_color:read_u8(c)?,accent_color:read_u8(c)?,primary_finish:read_u32(c)?,accent_finish:read_u32(c)?},"TeamPaint:u8x3_u32x2".to_owned())),ReplayNetworkAttributeTagV1::TeamLoadout=>{let(b,bs)=decode_loadout(c)?;let(o,os)=decode_loadout(c)?;Ok((ReplayNetworkK4ValueV1::TeamLoadout{blue:b,orange:o},format!("TeamLoadout:blue[{bs}]:orange[{os}]")))}ReplayNetworkAttributeTagV1::ClubColors=>Ok((ReplayNetworkK4ValueV1::ClubColors{blue_flag:read_bits(c,1)?!=0,blue_color:read_u8(c)?,orange_flag:read_bits(c,1)?!=0,orange_color:read_u8(c)?},"ClubColors:b1_u8_b1_u8".to_owned())),ReplayNetworkAttributeTagV1::Reservation=>{let number=read_bits(c,3)? as u8;let(id,is,needs)=decode_reservation_id(c,ctx)?;let(name,ns)=if needs{let(t,s)=decode_text(c)?;(Some(t),s)}else{(None,"none".to_owned())};let u1=read_bits(c,1)?!=0;let u2=read_bits(c,1)?!=0;let h=(ctx.version_major,ctx.version_minor,ctx.net_version)>=(868,12,0);let u3=if h{Some(read_bits(c,6)? as u8)}else{None};Ok((ReplayNetworkK4ValueV1::Reservation(ReplayNetworkK4ReservationV1{number,player_id:id,name,unknown1:u1,unknown2:u2,unknown3:u3}),format!("Reservation:{is}:name_{ns}:u3_{h}")))}ReplayNetworkAttributeTagV1::StatEvent=>Ok((ReplayNetworkK4ValueV1::StatEvent{unknown1:read_bits(c,1)?!=0,object_id:read_i32(c)?},"StatEvent:b1_i32".to_owned())),ReplayNetworkAttributeTagV1::PlayerHistoryKey=>Ok((ReplayNetworkK4ValueV1::PlayerHistoryKey(read_bits(c,14)? as u16),"PlayerHistoryKey:u14".to_owned())),ReplayNetworkAttributeTagV1::DemolishFx=>{let f=read_bits(c,1)?!=0;let di=read_i32(c)?;let af=read_bits(c,1)?!=0;let a=read_i32(c)?;let vf=read_bits(c,1)?!=0;let v=read_i32(c)?;let(av,as_)=decode_vector(c,"attack_velocity")?;let(vv,vs)=decode_vector(c,"victim_velocity")?;Ok((ReplayNetworkK4ValueV1::DemolishFx{custom_demo_flag:f,custom_demo_id:di,attacker_flag:af,attacker:a,victim_flag:vf,victim:v,attack_velocity:av,victim_velocity:vv},format!("DemolishFx:{as_}:{vs}")))}ReplayNetworkAttributeTagV1::DemolishExtended=>{let ap=active(c)?;let sd=active(c)?;let sdb=read_bits(c,1)?!=0;let ge=active(c)?;let a=active(c)?;let v=active(c)?;let(av,as_)=decode_vector(c,"attacker_velocity")?;let(vv,vs)=decode_vector(c,"victim_velocity")?;Ok((ReplayNetworkK4ValueV1::DemolishExtended{attacker_pri:ap,self_demo:sd,self_demolish:sdb,goal_explosion_owner:ge,attacker:a,victim:v,attacker_velocity:av,victim_velocity:vv},format!("DemolishExtended:activex5:{as_}:{vs}")))}ReplayNetworkAttributeTagV1::ExtendedExplosion=>{let f=read_bits(c,1)?!=0;let a=read_i32(c)?;let(l,ls)=decode_vector(c,"location")?;let u=read_bits(c,1)?!=0;let s=read_i32(c)?;Ok((ReplayNetworkK4ValueV1::ExtendedExplosion{flag:f,actor:a,location:l,unknown1:u,secondary_actor:s},format!("ExtendedExplosion:{ls}")))}ReplayNetworkAttributeTagV1::LoadoutsOnline=>{let(b,bs)=online_side(c,objects,"blue")?;let(o,os)=online_side(c,objects,"orange")?;let u1=read_bits(c,1)?!=0;let u2=read_bits(c,1)?!=0;Ok((ReplayNetworkK4ValueV1::LoadoutsOnline{blue:b,orange:o,unknown1:u1,unknown2:u2},format!("LoadoutsOnline:{bs}:{os}")))}_=>Err(k4_error("unsupported-k4-tag",format!("attribute tag {tag:?} is not an R3.17N K4 tag")))}}
pub fn decode_replay_network_k4_v1(bytes:&[u8],start_bit:u64,tag:ReplayNetworkAttributeTagV1,ctx:ReplayNetworkK4DecodeContextV1,objects:&[String])->Result<ReplayNetworkK4DecodeV1>{let total=bytes.len().checked_mul(8).ok_or_else(||k4_error("invalid-start","network bit length overflows"))?;if start_bit>total as u64{return Err(k4_error("invalid-start",format!("payload start {start_bit} exceeds network length {total}")));}let start=usize::try_from(start_bit).map_err(|_|k4_error("invalid-start","start does not fit usize"))?;validate_context(ctx)?;let mut c=NetworkBitCursor::new(bytes);reset(&mut c,start);let(value,shape)=match decode_one(&mut c,tag,ctx,objects){Ok(x)=>x,Err(e)=>{reset(&mut c,start);return Err(e)}};let end=c.position_bits() as u64;let width=end-start_bit;if !k4_admitted_groups::contains(tag,ctx.version_major,ctx.version_minor,ctx.net_version,ctx.is_rl_223,width,&shape){reset(&mut c,start);return Err(k4_error("unadmitted-k4-shape",format!("exact tuple absent from R3.17N: tag={tag:?} rl223={} width={width} shape={shape}",ctx.is_rl_223)));}Ok(ReplayNetworkK4DecodeV1{attribute_tag:tag,payload_start_bit:start_bit,payload_end_bit:end,payload_width:width,structural_shape:shape,value})}
'''


def generate_test(rows: list[dict]) -> str:
    cases=[]
    for i,r in enumerate(rows):
        b=emit_shape(r["shape"])
        if len(b.bits)!=r["payload_width"]:raise SystemExit(f"materialized width mismatch row {i}: {r['shape']} {len(b.bits)} != {r['payload_width']}")
        cases.append((r,b.bytes().hex()))
    by_tag={}
    for r in rows:by_tag.setdefault(r["attribute_tag"],[]).append(r)
    def cross(tag,prefix,right_name):
        rs=by_tag[tag];obs={r["shape"] for r in rs};lefts=set();rights=set()
        for r in rs:
            a,b=r["shape"][len(prefix):].split(f":{right_name}:",1);lefts.add(a);rights.add(f"{right_name}:{b}")
        for a in sorted(lefts):
            for b in sorted(rights):
                s=f"{prefix}{a}:{b}"
                if s not in obs:
                    f=dict(rs[0]);m=emit_shape(s);f["shape"]=s;f["payload_width"]=len(m.bits);return f,m.bytes().hex(),s
        raise SystemExit("no cross negative")
    fx=cross("DemolishFx","DemolishFx:","victim_velocity");ext=cross("DemolishExtended","DemolishExtended:activex5:","victim_velocity")
    rr=by_tag["Reservation"];ro={r["shape"] for r in rr};res=None
    for r in rr:
        if not re.search(r":name_w1252_\d+:u3_true$",r["shape"]):continue
        for n in range(1,40):
            s=re.sub(r":name_w1252_\d+:u3_true$",f":name_w1252_{n}:u3_true",r["shape"])
            if s not in ro:
                f=dict(r);m=emit_shape(s);f["shape"]=s;f["payload_width"]=len(m.bits);res=(f,m.bytes().hex(),s);break
        if res:break
    lr=by_tag["LoadoutsOnline"];lo={r["shape"] for r in lr};load=None
    for r in lr:
        s=r["shape"].replace("g0:0()","g0:1(Paint:new31)",1)
        if s!=r["shape"] and s not in lo:
            f=dict(r);m=emit_shape(s);f["shape"]=s;f["payload_width"]=len(m.bits);load=(f,m.bytes().hex(),s);break
    if not res or not load:raise SystemExit("missing negative")
    L=["use mimir_replay::{decode_replay_network_k4_v1,ReplayNetworkAttributeTagV1,ReplayNetworkK4DecodeContextV1,R3_17N_K4_ADMITTED_GROUPS_V1};","#[derive(Clone,Copy)]struct Case{tag:ReplayNetworkAttributeTagV1,major:i32,minor:i32,net:i32,rl223:bool,width:u64,shape:&'static str,payload_hex:&'static str}","const CASES:&[Case]=&["]
    for r,h in cases:L.append(f"Case{{tag:ReplayNetworkAttributeTagV1::{TAG_VARIANTS[r['attribute_tag']]},major:{r['version_major']},minor:{r['version_minor']},net:{r['net_version']},rl223:{str(r['is_rl_223']).lower()},width:{r['payload_width']},shape:{rust_string(r['shape'])},payload_hex:{rust_string(h)}}},")
    L += ["];","const OBJECT_TABLE:&[&str]=&["+",".join(rust_string(x) for x in OBJECT_TABLE)+"];","fn objects()->Vec<String>{OBJECT_TABLE.iter().map(|x|(*x).to_owned()).collect()}","fn hex(s:&str)->Vec<u8>{fn n(b:u8)->u8{match b{b'0'..=b'9'=>b-b'0',b'a'..=b'f'=>b-b'a'+10,_=>panic!()}}let b=s.as_bytes();b.chunks_exact(2).map(|c|(n(c[0])<<4)|n(c[1])).collect()}","fn pack(c:Case,start:usize,payload:usize,trail:usize)->Vec<u8>{let p=hex(c.payload_hex);let total=start+payload+trail;let mut o=vec![0u8;total.div_ceil(8)];for i in 0..payload{if((p[i/8]>>(i%8))&1)!=0{o[(start+i)/8]|=1<<((start+i)%8);}}for i in 0..trail{if i%2==0{let q=start+payload+i;o[q/8]|=1<<(q%8);}}o}","fn ctx(c:Case)->ReplayNetworkK4DecodeContextV1{ReplayNetworkK4DecodeContextV1{version_major:c.major,version_minor:c.minor,net_version:c.net,is_rl_223:c.rl223}}","#[test]fn exact_table(){assert_eq!(CASES.len(),161);assert_eq!(R3_17N_K4_ADMITTED_GROUPS_V1.len(),161);for(g,c)in R3_17N_K4_ADMITTED_GROUPS_V1.iter().zip(CASES){assert_eq!(g.attribute_tag,c.tag);assert_eq!(g.version_major,c.major);assert_eq!(g.version_minor,c.minor);assert_eq!(g.net_version,c.net);assert_eq!(g.is_rl_223,c.rl223);assert_eq!(g.payload_width,c.width);assert_eq!(g.structural_shape,c.shape);}}","#[test]fn positives_161(){let o=objects();for c in CASES.iter().copied(){let b=pack(c,3,c.width as usize,13);let a=decode_replay_network_k4_v1(&b,3,c.tag,ctx(c),&o).unwrap_or_else(|e|panic!(\"{} {e}\",c.shape));assert_eq!(a.structural_shape,c.shape);assert_eq!(a.payload_width,c.width);assert_eq!(a.payload_end_bit,3+c.width);assert_eq!(a.value.attribute_tag(),c.tag);assert_eq!(a,decode_replay_network_k4_v1(&b,3,c.tag,ctx(c),&o).unwrap());}}","#[test]fn basics_negative(){let c=CASES[0];let o=objects();let b=pack(c,3,c.width as usize,8);let mut x=ctx(c);x.version_minor=31;assert!(decode_replay_network_k4_v1(&b,3,c.tag,x,&o).unwrap_err().to_string().contains(\"unadmitted-context\"));assert!(decode_replay_network_k4_v1(&b,3,ReplayNetworkAttributeTagV1::Boolean,ctx(c),&o).unwrap_err().to_string().contains(\"unsupported-k4-tag\"));assert!(decode_replay_network_k4_v1(&b,(b.len()*8+1)as u64,c.tag,ctx(c),&o).unwrap_err().to_string().contains(\"invalid-start\"));}","#[test]fn truncation(){let o=objects();for c in[*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::CamSettings).unwrap(),*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::Reservation&&c.shape.contains(\"sys11_epic\")).unwrap(),*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::LoadoutsOnline).unwrap()]{let w=c.width as usize;let start=(8-((w-1)%8))%8;let b=pack(c,start,w-1,0);assert_eq!(b.len()*8,start+w-1);let e=decode_replay_network_k4_v1(&b,start as u64,c.tag,ctx(c),&o).unwrap_err().to_string();assert!(e.contains(\"insufficient-bits\")||e.contains(\"unadmitted-k4-shape\"),\"{e}\");}}","#[test]fn cross_products(){let o=objects();"]
    for name,(r,h,s) in [("fx",fx),("ext",ext),("res",res),("load",load)]:L += [f"let {name}=Case{{tag:ReplayNetworkAttributeTagV1::{TAG_VARIANTS[r['attribute_tag']]},major:{r['version_major']},minor:{r['version_minor']},net:{r['net_version']},rl223:{str(r['is_rl_223']).lower()},width:{r['payload_width']},shape:{rust_string(s)},payload_hex:{rust_string(h)}}};",f"let b=pack({name},3,{name}.width as usize,8);assert!(decode_replay_network_k4_v1(&b,3,{name}.tag,ctx({name}),&o).unwrap_err().to_string().contains(\"unadmitted-k4-shape\"));"]
    L += ["}","#[test]fn malformed_text_unknown_object(){let o=objects();let c=*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::Reservation&&c.shape.contains(\"sys11_epic\")).unwrap();let mut b=vec![0u8;6];fn set(b:&mut[u8],p:usize,v:u64,w:usize){for i in 0..w{if((v>>i)&1)!=0{b[(p+i)/8]|=1<<((p+i)%8);}}}set(&mut b,3,11,8);set(&mut b,11,0x8000_0000,32);assert!(decode_replay_network_k4_v1(&b,0,c.tag,ctx(c),&o).unwrap_err().to_string().contains(\"invalid-length-or-count\"));let c=*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::LoadoutsOnline).unwrap();let b=pack(c,3,c.width as usize,8);let bad=vec![\"Unknown\".to_owned();5];assert!(decode_replay_network_k4_v1(&b,3,c.tag,ctx(c),&bad).unwrap_err().to_string().contains(\"unadmitted-k4-shape\"));}","#[test]fn teamloadout_unobserved_version(){let c=*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::TeamLoadout).unwrap();let p=hex(c.payload_hex);let mut bits=(0..c.width as usize).map(|i|(p[i/8]>>(i%8))&1).collect::<Vec<_>>();for(base,v)in[(0usize,27u8),(520,27u8)]{for i in 0..8{bits[base+i]=(v>>i)&1;}}let mut b=vec![0u8;bits.len().div_ceil(8)];for(i,x)in bits.into_iter().enumerate(){if x!=0{b[i/8]|=1<<(i%8);}}assert!(decode_replay_network_k4_v1(&b,0,c.tag,ctx(c),&objects()).unwrap_err().to_string().contains(\"unadmitted-k4-shape\"));}","#[test]fn rl223_exact_coupling(){let o=objects();let c=*CASES.iter().find(|c|!CASES.iter().any(|x|x.tag==c.tag&&x.major==c.major&&x.minor==c.minor&&x.net==c.net&&x.rl223!=c.rl223&&x.width==c.width&&x.shape==c.shape)).unwrap();let b=pack(c,3,c.width as usize,8);let mut x=ctx(c);x.is_rl_223=!x.is_rl_223;assert!(decode_replay_network_k4_v1(&b,3,c.tag,x,&o).unwrap_err().to_string().contains(\"unadmitted-k4-shape\"));}"]
    return "\n".join(L)+"\n"


def update_lib():
    text=LIB_PATH.read_text(encoding="utf-8");anchor="mod k3_admitted_groups;\n"
    if text.count(anchor)!=1:raise SystemExit("lib anchor")
    LIB_PATH.write_text(text.replace(anchor,"mod k3_admitted_groups;\nmod k4_admitted_groups;\nmod k4_native;\npub use k4_admitted_groups::{ReplayNetworkK4AdmittedGroupV1, R3_17N_K4_ADMITTED_GROUPS_V1};\npub use k4_native::*;\n",1),encoding="utf-8",newline="\n")


def main():
    rows=load_rows();ALLOW_PATH.write_text(generate_allowlist(rows),encoding="utf-8",newline="\n");NATIVE_PATH.write_text(NATIVE_RS,encoding="utf-8",newline="\n");TEST_PATH.write_text(generate_test(rows),encoding="utf-8",newline="\n");update_lib();print("R3.17O generation complete rows=161")

if __name__=="__main__":main()
