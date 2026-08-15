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
    prefix = "Reservation:"
    if not shape.startswith(prefix):
        raise ValueError(shape)
    body = shape[len(prefix):]
    marker = ":name_"
    id_shape, rest = body.split(marker, 1)
    name_shape, u3 = rest.rsplit(":u3_", 1)
    if u3 != "true":
        raise ValueError(f"current lane expected u3_true: {shape}")
    bits.zeros(3)
    needs_name = True
    if id_shape == "sys0_split24_zero":
        bits.put(0, 8)
        bits.zeros(24)
        needs_name = False
    elif id_shape == "sys0_split24_nonzero":
        bits.put(0, 8)
        bits.put(1, 24)
    elif id_shape == "sys1_steam64":
        bits.put(1, 8)
        bits.zeros(64)
    elif id_shape == "sys2_playstation320":
        bits.put(2, 8)
        bits.zeros(128 + 128 + 64)
    elif id_shape == "sys4_xbox64":
        bits.put(4, 8)
        bits.zeros(64)
    elif id_shape == "sys5_qq64":
        bits.put(5, 8)
        bits.zeros(64)
    elif id_shape == "sys6_switch256":
        bits.put(6, 8)
        bits.zeros(64 + 192)
    elif id_shape == "sys7_psynet64":
        bits.put(7, 8)
        bits.zeros(64)
    elif id_shape.startswith("sys11_epic_"):
        bits.put(11, 8)
        emit_text(bits, id_shape[len("sys11_epic_"):])
    else:
        raise ValueError(f"unsupported reservation id shape {id_shape}")
    bits.zeros(8)
    if needs_name:
        if name_shape == "none":
            raise ValueError(f"name unexpectedly none: {shape}")
        emit_text(bits, name_shape)
    elif name_shape != "none":
        raise ValueError(f"split-zero unexpectedly has name: {shape}")
    bits.zeros(1 + 1 + 6)


def split_side(shape: str, start: int) -> tuple[str, int]:
    open_idx = shape.index("[", start)
    close_idx = shape.index("]", open_idx)
    return shape[start:close_idx + 1], close_idx + 1


def emit_product(bits: Bits, token: str) -> None:
    bits.put(0, 1)
    if token.startswith("Title:"):
        bits.put(2, 32)
        emit_text(bits, token[len("Title:"):])
        return
    if token not in PRODUCT_IDS:
        raise ValueError(f"unobserved/unsupported product token in contract: {token}")
    bits.put(PRODUCT_IDS[token], 32)
    if token == "UserColor:new32":
        bits.zeros(32)
    elif token in {"Paint:new31", "SpecialEdition:31", "TeamEdition:new31"}:
        bits.zeros(31)
    else:
        raise AssertionError(token)


def emit_online_side(bits: Bits, side: str) -> None:
    m = re.fullmatch(r"(blue|orange):outer(\d+)\[(.*)\]", side)
    if not m:
        raise ValueError(f"bad online side: {side[:120]}")
    outer = int(m.group(2))
    groups = [] if not m.group(3) else m.group(3).split(";")
    if len(groups) != outer:
        raise ValueError(f"outer mismatch {outer} != {len(groups)}")
    bits.put(outer, 8)
    for idx, group in enumerate(groups):
        gm = re.fullmatch(r"g(\d+):(\d+)\((.*)\)", group)
        if not gm:
            raise ValueError(f"bad group {group}")
        if int(gm.group(1)) != idx:
            raise ValueError((idx, group))
        count = int(gm.group(2))
        products = [] if gm.group(3) == "" else gm.group(3).split(",")
        if len(products) != count:
            raise ValueError(f"count mismatch {count} != {len(products)} in {group}")
        bits.put(count, 8)
        for product in products:
            emit_product(bits, product)


def emit_shape(shape: str) -> Bits:
    b = Bits()
    if shape == "CamSettings:f32x7":
        b.zeros(7 * 32)
    elif shape == "TeamPaint:u8x3_u32x2":
        b.zeros(3 * 8 + 2 * 32)
    elif shape == "ClubColors:b1_u8_b1_u8":
        b.zeros(1 + 8 + 1 + 8)
    elif shape == "StatEvent:b1_i32":
        b.zeros(1 + 32)
    elif shape == "PlayerHistoryKey:u14":
        b.zeros(14)
    elif shape.startswith("TeamLoadout:blue["):
        m = re.fullmatch(r"TeamLoadout:blue\[(.*)\]:orange\[(.*)\]", shape)
        if not m:
            raise ValueError(shape)
        emit_loadout_side(b, m.group(1))
        emit_loadout_side(b, m.group(2))
    elif shape.startswith("Reservation:"):
        emit_reservation(b, shape)
    elif shape.startswith("DemolishFx:"):
        rest = shape[len("DemolishFx:"):]
        left, right = rest.split(":victim_velocity:", 1)
        b.zeros(1 + 32 + 1 + 32 + 1 + 32)
        emit_vector(b, left, "attack_velocity")
        emit_vector(b, "victim_velocity:" + right, "victim_velocity")
    elif shape.startswith("DemolishExtended:activex5:"):
        rest = shape[len("DemolishExtended:activex5:"):]
        left, right = rest.split(":victim_velocity:", 1)
        b.zeros(5 * 33 + 1)
        emit_vector(b, left, "attacker_velocity")
        emit_vector(b, "victim_velocity:" + right, "victim_velocity")
    elif shape.startswith("ExtendedExplosion:"):
        loc = shape[len("ExtendedExplosion:"):]
        b.zeros(1 + 32)
        emit_vector(b, loc, "location")
        b.zeros(1 + 32)
    elif shape.startswith("LoadoutsOnline:blue:"):
        rest = shape[len("LoadoutsOnline:"):]
        blue, pos = split_side(rest, 0)
        if not rest[pos:].startswith(":orange:"):
            raise ValueError(shape)
        orange = rest[pos + 1:]
        emit_online_side(b, blue)
        emit_online_side(b, orange)
        b.zeros(2)
    else:
        raise ValueError(f"unhandled shape {shape}")
    return b


def rust_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def generate_allowlist(rows: list[dict]) -> str:
    lines = [
        "use super::ReplayNetworkAttributeTagV1;",
        "",
        "#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]",
        "pub struct ReplayNetworkK4AdmittedGroupV1 {",
        "    pub attribute_tag: ReplayNetworkAttributeTagV1,",
        "    pub version_major: i32,",
        "    pub version_minor: i32,",
        "    pub net_version: i32,",
        "    pub is_rl_223: bool,",
        "    pub payload_width: u64,",
        "    pub structural_shape: &'static str,",
        "}",
        "",
        "macro_rules! g {",
        "    ($tag:ident, $major:expr, $minor:expr, $net:expr, $rl223:expr, $width:expr, $shape:expr) => {",
        "        ReplayNetworkK4AdmittedGroupV1 {",
        "            attribute_tag: ReplayNetworkAttributeTagV1::$tag,",
        "            version_major: $major,",
        "            version_minor: $minor,",
        "            net_version: $net,",
        "            is_rl_223: $rl223,",
        "            payload_width: $width,",
        "            structural_shape: $shape,",
        "        }",
        "    };",
        "}",
        "",
        "pub const R3_17N_K4_ADMITTED_GROUPS_V1: &[ReplayNetworkK4AdmittedGroupV1] = &[",
    ]
    for r in rows:
        lines.append(
            f"    g!({TAG_VARIANTS[r['attribute_tag']]}, {r['version_major']}, {r['version_minor']}, "
            f"{r['net_version']}, {str(r['is_rl_223']).lower()}, {r['payload_width']}u64, "
            f"{rust_string(r['shape'])}),"
        )
    lines += [
        "];",
        "",
        "pub(crate) fn contains(",
        "    attribute_tag: ReplayNetworkAttributeTagV1,",
        "    version_major: i32,",
        "    version_minor: i32,",
        "    net_version: i32,",
        "    is_rl_223: bool,",
        "    payload_width: u64,",
        "    structural_shape: &str,",
        ") -> bool {",
        "    R3_17N_K4_ADMITTED_GROUPS_V1.binary_search_by(|group| {",
        "        (",
        "            group.attribute_tag,",
        "            group.version_major,",
        "            group.version_minor,",
        "            group.net_version,",
        "            group.is_rl_223,",
        "            group.payload_width,",
        "            group.structural_shape,",
        "        )",
        "            .cmp(&(",
        "                attribute_tag,",
        "                version_major,",
        "                version_minor,",
        "                net_version,",
        "                is_rl_223,",
        "                payload_width,",
        "                structural_shape,",
        "            ))",
        "    }).is_ok()",
        "}",
        "",
    ]
    keys = [
        (r["attribute_tag"], r["version_major"], r["version_minor"], r["net_version"], r["is_rl_223"], r["payload_width"], r["shape"])
        for r in rows
    ]
    if keys != sorted(keys):
        raise SystemExit("R3.17N rows are not sorted by exact tuple; generator expects canonical sort")
    return "\n".join(lines)


NATIVE_RS = r'''use super::{
    decode_network_windows1252, MimirError, NetworkBitCursor, ReplayNetworkAttributeTagV1,
    ReplayNetworkTextEncodingV1, ReplayNetworkTextV1, ReplayNetworkVector3V1, Result,
};
use crate::k4_admitted_groups;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4DecodeContextV1 {
    pub version_major: i32,
    pub version_minor: i32,
    pub net_version: i32,
    pub is_rl_223: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4LoadoutV1 {
    pub version: u8,
    pub base_fields: Vec<u32>,
    pub unknown2: Option<u32>,
    pub specials: Vec<u32>,
    pub banner: Option<u32>,
    pub product_id: Option<u32>,
    pub v22_extras: Vec<u32>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkK4ReservationIdV1 {
    SplitScreen { split_id: u32, local_id: u8 },
    Steam { online_id: u64, local_id: u8 },
    PlayStation { name_bytes: Vec<u8>, unknown: Vec<u8>, online_id: u64, local_id: u8 },
    Xbox { online_id: u64, local_id: u8 },
    Qq { online_id: u64, local_id: u8 },
    Switch { online_id: u64, unknown: Vec<u8>, local_id: u8 },
    PsyNet { online_id: u64, local_id: u8 },
    Epic { account_id: ReplayNetworkTextV1, local_id: u8 },
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4ReservationV1 {
    pub number: u8,
    pub player_id: ReplayNetworkK4ReservationIdV1,
    pub name: Option<ReplayNetworkTextV1>,
    pub unknown1: bool,
    pub unknown2: bool,
    pub unknown3: Option<u8>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4ActiveActorV1 { pub active: bool, pub actor: i32 }

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkK4ProductValueV1 {
    UserColor(u32), Paint(u32), Title(ReplayNetworkTextV1), SpecialEdition(u32), TeamEdition(u32),
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4OnlineProductV1 {
    pub unknown: bool, pub object_id: i32, pub value: ReplayNetworkK4ProductValueV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ReplayNetworkK4ValueV1 {
    CamSettings { raw_f32_bits: Vec<u32> },
    TeamPaint { team: u8, primary_color: u8, accent_color: u8, primary_finish: u32, accent_finish: u32 },
    TeamLoadout { blue: ReplayNetworkK4LoadoutV1, orange: ReplayNetworkK4LoadoutV1 },
    ClubColors { blue_flag: bool, blue_color: u8, orange_flag: bool, orange_color: u8 },
    Reservation(ReplayNetworkK4ReservationV1),
    StatEvent { unknown1: bool, object_id: i32 },
    PlayerHistoryKey(u16),
    DemolishFx { custom_demo_flag: bool, custom_demo_id: i32, attacker_flag: bool, attacker: i32, victim_flag: bool, victim: i32, attack_velocity: ReplayNetworkVector3V1, victim_velocity: ReplayNetworkVector3V1 },
    DemolishExtended { attacker_pri: ReplayNetworkK4ActiveActorV1, self_demo: ReplayNetworkK4ActiveActorV1, self_demolish: bool, goal_explosion_owner: ReplayNetworkK4ActiveActorV1, attacker: ReplayNetworkK4ActiveActorV1, victim: ReplayNetworkK4ActiveActorV1, attacker_velocity: ReplayNetworkVector3V1, victim_velocity: ReplayNetworkVector3V1 },
    ExtendedExplosion { flag: bool, actor: i32, location: ReplayNetworkVector3V1, unknown1: bool, secondary_actor: i32 },
    LoadoutsOnline { blue: Vec<Vec<ReplayNetworkK4OnlineProductV1>>, orange: Vec<Vec<ReplayNetworkK4OnlineProductV1>>, unknown1: bool, unknown2: bool },
}

impl ReplayNetworkK4ValueV1 {
    pub fn attribute_tag(&self) -> ReplayNetworkAttributeTagV1 {
        match self {
            Self::CamSettings { .. } => ReplayNetworkAttributeTagV1::CamSettings,
            Self::TeamPaint { .. } => ReplayNetworkAttributeTagV1::TeamPaint,
            Self::TeamLoadout { .. } => ReplayNetworkAttributeTagV1::TeamLoadout,
            Self::ClubColors { .. } => ReplayNetworkAttributeTagV1::ClubColors,
            Self::Reservation(_) => ReplayNetworkAttributeTagV1::Reservation,
            Self::StatEvent { .. } => ReplayNetworkAttributeTagV1::StatEvent,
            Self::PlayerHistoryKey(_) => ReplayNetworkAttributeTagV1::PlayerHistoryKey,
            Self::DemolishFx { .. } => ReplayNetworkAttributeTagV1::DemolishFx,
            Self::DemolishExtended { .. } => ReplayNetworkAttributeTagV1::DemolishExtended,
            Self::ExtendedExplosion { .. } => ReplayNetworkAttributeTagV1::ExtendedExplosion,
            Self::LoadoutsOnline { .. } => ReplayNetworkAttributeTagV1::LoadoutsOnline,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkK4DecodeV1 {
    pub attribute_tag: ReplayNetworkAttributeTagV1,
    pub payload_start_bit: u64,
    pub payload_end_bit: u64,
    pub payload_width: u64,
    pub structural_shape: String,
    pub value: ReplayNetworkK4ValueV1,
}

fn k4_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!("replay network k4 error: {category}: {}", detail.into()))
}
fn reset(cursor: &mut NetworkBitCursor<'_>, start: usize) { cursor.bit_position = start; debug_assert_eq!(cursor.position_bits(), start); }
fn read_bits(cursor: &mut NetworkBitCursor<'_>, width: usize) -> Result<u64> {
    if cursor.remaining_bits() < width { return Err(k4_error("insufficient-bits", format!("need {width} bits at position {}, but only {} remain", cursor.position_bits(), cursor.remaining_bits()))); }
    cursor.read_bits_le(width).map_err(|error| k4_error("insufficient-bits", format!("bit read failed: {error}")))
}
fn read_u8(cursor: &mut NetworkBitCursor<'_>) -> Result<u8> { Ok(read_bits(cursor, 8)? as u8) }
fn read_u32(cursor: &mut NetworkBitCursor<'_>) -> Result<u32> { Ok(read_bits(cursor, 32)? as u32) }
fn read_i32(cursor: &mut NetworkBitCursor<'_>) -> Result<i32> { Ok(read_u32(cursor)? as i32) }
fn read_u64(cursor: &mut NetworkBitCursor<'_>) -> Result<u64> { read_bits(cursor, 64) }
fn read_bytes(cursor: &mut NetworkBitCursor<'_>, count: usize) -> Result<Vec<u8>> {
    let required_bits = count.checked_mul(8).ok_or_else(|| k4_error("invalid-length-or-count", "byte count bit width overflows"))?;
    if cursor.remaining_bits() < required_bits { return Err(k4_error("insufficient-bits", format!("need {required_bits} byte-content bits at position {}, but only {} remain", cursor.position_bits(), cursor.remaining_bits()))); }
    let mut out = Vec::new(); out.try_reserve_exact(count).map_err(|_| k4_error("invalid-length-or-count", format!("cannot reserve {count} bytes")))?;
    for _ in 0..count { out.push(read_u8(cursor)?); } Ok(out)
}

fn decode_text(cursor: &mut NetworkBitCursor<'_>) -> Result<(ReplayNetworkTextV1, String)> {
    let declared = read_i32(cursor)?;
    if declared == 0 { return Ok((ReplayNetworkTextV1 { value: String::new(), declared_length: 0, encoding: ReplayNetworkTextEncodingV1::Empty }, "empty".to_owned())); }
    if declared > 0 {
        let count = usize::try_from(declared).map_err(|_| k4_error("invalid-length-or-count", format!("positive text length {declared} does not fit usize")))?;
        let bytes = read_bytes(cursor, count)?;
        let content = bytes.get(..count.saturating_sub(1)).ok_or_else(|| k4_error("invalid-length-or-count", "invalid positive text slice"))?;
        return Ok((ReplayNetworkTextV1 { value: decode_network_windows1252(content), declared_length: declared, encoding: ReplayNetworkTextEncodingV1::Windows1252 }, format!("w1252_{declared}")));
    }
    if declared == i32::MIN { return Err(k4_error("invalid-length-or-count", "i32::MIN cannot be negated for UTF-16 length")); }
    let units = usize::try_from(-declared).map_err(|_| k4_error("invalid-length-or-count", format!("UTF-16 length {declared} does not fit usize")))?;
    let byte_count = units.checked_mul(2).ok_or_else(|| k4_error("invalid-length-or-count", "UTF-16 byte count overflows"))?;
    let bytes = read_bytes(cursor, byte_count)?;
    let content_len = byte_count.saturating_sub(2);
    let mut decoded_units = Vec::new(); decoded_units.try_reserve_exact(content_len / 2).map_err(|_| k4_error("invalid-length-or-count", format!("cannot reserve {} UTF-16 units", content_len / 2)))?;
    for pair in bytes[..content_len].chunks_exact(2) { decoded_units.push(u16::from_le_bytes([pair[0], pair[1]])); }
    Ok((ReplayNetworkTextV1 { value: String::from_utf16_lossy(&decoded_units), declared_length: declared, encoding: ReplayNetworkTextEncodingV1::Utf16Le }, format!("utf16_{}", -declared)))
}

fn validate_context(context: ReplayNetworkK4DecodeContextV1) -> Result<()> {
    if context.version_major != 868 || context.version_minor != 32 || context.net_version != 10 {
        return Err(k4_error("unadmitted-context", format!("K4 requires replay version 868.32 / net10, got {}.{} / net{}", context.version_major, context.version_minor, context.net_version)));
    }
    Ok(())
}

fn decode_vector(cursor: &mut NetworkBitCursor<'_>, name: &str) -> Result<(ReplayNetworkVector3V1, String)> {
    let low = read_bits(cursor, 4)? as u8;
    let candidate = low.checked_add(16).ok_or_else(|| k4_error("unadmitted-k4-shape", "vector candidate overflow"))?;
    let (selected, header_bits) = if candidate < 22 { let discriminator = read_bits(cursor, 1)? != 0; (if discriminator { candidate } else { low }, 5u8) } else { (low, 4u8) };
    if selected >= 20 { return Err(k4_error("unadmitted-k4-shape", format!("vector selected size {selected} is not admitted"))); }
    let component_width = selected.checked_add(2).ok_or_else(|| k4_error("unadmitted-k4-shape", "vector width overflow"))?;
    let raw_x = read_bits(cursor, usize::from(component_width))? as u32;
    let raw_y = read_bits(cursor, usize::from(component_width))? as u32;
    let raw_z = read_bits(cursor, usize::from(component_width))? as u32;
    let bias = 1i64.checked_shl(u32::from(selected + 1)).ok_or_else(|| k4_error("unadmitted-k4-shape", "vector bias overflow"))?;
    let semantic = |raw: u32| (i64::from(raw) - bias) as f32 / 100.0;
    Ok((ReplayNetworkVector3V1 { selected_size_bits: selected, component_width, raw_x, raw_y, raw_z, x: semantic(raw_x), y: semantic(raw_y), z: semantic(raw_z) }, format!("{name}:sb{selected}:h{header_bits}:cw{component_width}")))
}

fn decode_loadout(cursor: &mut NetworkBitCursor<'_>) -> Result<(ReplayNetworkK4LoadoutV1, String)> {
    let version = read_u8(cursor)?; let mut base_fields = Vec::with_capacity(7); for _ in 0..7 { base_fields.push(read_u32(cursor)?); }
    let (unknown2, u2_shape) = if version > 10 { (Some(read_u32(cursor)?), "u2") } else { (None, "nou2") };
    let (specials, specials_shape) = if version >= 16 { (vec![read_u32(cursor)?, read_u32(cursor)?, read_u32(cursor)?], "specials") } else { (Vec::new(), "nospecials") };
    let (banner, banner_shape) = if version >= 17 { (Some(read_u32(cursor)?), "banner") } else { (None, "nobanner") };
    let (product_id, product_shape) = if version >= 19 { (Some(read_u32(cursor)?), "product") } else { (None, "noproduct") };
    let (v22_extras, extra_shape) = if version >= 22 { (vec![read_u32(cursor)?, read_u32(cursor)?, read_u32(cursor)?], "extra3") } else { (Vec::new(), "noextra3") };
    Ok((ReplayNetworkK4LoadoutV1 { version, base_fields, unknown2, specials, banner, product_id, v22_extras }, format!("v{version}:{u2_shape}:{specials_shape}:{banner_shape}:{product_shape}:{extra_shape}")))
}

fn decode_reservation_id(cursor: &mut NetworkBitCursor<'_>, context: ReplayNetworkK4DecodeContextV1) -> Result<(ReplayNetworkK4ReservationIdV1, String, bool)> {
    let system = read_u8(cursor)?;
    let (remote, shape, needs_name) = match system {
        0 => { let split = read_bits(cursor, 24)? as u32; (ReplayNetworkK4ReservationIdV1::SplitScreen { split_id: split, local_id: 0 }, format!("sys0_split24_{}", if split == 0 { "zero" } else { "nonzero" }), split != 0) }
        1 => (ReplayNetworkK4ReservationIdV1::Steam { online_id: read_u64(cursor)?, local_id: 0 }, "sys1_steam64".to_owned(), true),
        2 => (ReplayNetworkK4ReservationIdV1::PlayStation { name_bytes: read_bytes(cursor, 16)?, unknown: read_bytes(cursor, 16)?, online_id: read_u64(cursor)?, local_id: 0 }, "sys2_playstation320".to_owned(), true),
        4 => (ReplayNetworkK4ReservationIdV1::Xbox { online_id: read_u64(cursor)?, local_id: 0 }, "sys4_xbox64".to_owned(), true),
        5 => (ReplayNetworkK4ReservationIdV1::Qq { online_id: read_u64(cursor)?, local_id: 0 }, "sys5_qq64".to_owned(), true),
        6 => (ReplayNetworkK4ReservationIdV1::Switch { online_id: read_u64(cursor)?, unknown: read_bytes(cursor, 24)?, local_id: 0 }, "sys6_switch256".to_owned(), true),
        7 => { let online_id = read_u64(cursor)?; if context.net_version < 10 { let _ = read_bytes(cursor, 24)?; return Err(k4_error("unadmitted-context", "net<10 PsyNet is outside the R3.17N context")); } (ReplayNetworkK4ReservationIdV1::PsyNet { online_id, local_id: 0 }, "sys7_psynet64".to_owned(), true) }
        11 => { let (account_id, text_shape) = decode_text(cursor)?; (ReplayNetworkK4ReservationIdV1::Epic { account_id, local_id: 0 }, format!("sys11_epic_{text_shape}"), true) }
        other => return Err(k4_error("unadmitted-k4-shape", format!("reservation unique-id system {other} is source-unknown/unadmitted"))),
    };
    let local_id = read_u8(cursor)?;
    let remote = match remote {
        ReplayNetworkK4ReservationIdV1::SplitScreen { split_id, .. } => ReplayNetworkK4ReservationIdV1::SplitScreen { split_id, local_id },
        ReplayNetworkK4ReservationIdV1::Steam { online_id, .. } => ReplayNetworkK4ReservationIdV1::Steam { online_id, local_id },
        ReplayNetworkK4ReservationIdV1::PlayStation { name_bytes, unknown, online_id, .. } => ReplayNetworkK4ReservationIdV1::PlayStation { name_bytes, unknown, online_id, local_id },
        ReplayNetworkK4ReservationIdV1::Xbox { online_id, .. } => ReplayNetworkK4ReservationIdV1::Xbox { online_id, local_id },
        ReplayNetworkK4ReservationIdV1::Qq { online_id, .. } => ReplayNetworkK4ReservationIdV1::Qq { online_id, local_id },
        ReplayNetworkK4ReservationIdV1::Switch { online_id, unknown, .. } => ReplayNetworkK4ReservationIdV1::Switch { online_id, unknown, local_id },
        ReplayNetworkK4ReservationIdV1::PsyNet { online_id, .. } => ReplayNetworkK4ReservationIdV1::PsyNet { online_id, local_id },
        ReplayNetworkK4ReservationIdV1::Epic { account_id, .. } => ReplayNetworkK4ReservationIdV1::Epic { account_id, local_id },
    };
    Ok((remote, shape, needs_name))
}

fn decode_active_actor(cursor: &mut NetworkBitCursor<'_>) -> Result<ReplayNetworkK4ActiveActorV1> { Ok(ReplayNetworkK4ActiveActorV1 { active: read_bits(cursor, 1)? != 0, actor: read_i32(cursor)? }) }

fn decode_product(cursor: &mut NetworkBitCursor<'_>, object_table: &[String]) -> Result<(ReplayNetworkK4OnlineProductV1, String)> {
    let unknown = read_bits(cursor, 1)? != 0; let object_id = read_i32(cursor)?;
    let slot = usize::try_from(object_id).map_err(|_| k4_error("unadmitted-k4-shape", format!("negative product attribute object id {object_id}")))?;
    let object_name = object_table.get(slot).ok_or_else(|| k4_error("unadmitted-k4-shape", format!("product attribute object id {object_id} is outside caller object table length {}", object_table.len())))?;
    let (value, shape) = match object_name.as_str() {
        "TAGame.ProductAttribute_UserColor_TA" => (ReplayNetworkK4ProductValueV1::UserColor(read_u32(cursor)?), "UserColor:new32".to_owned()),
        "TAGame.ProductAttribute_Painted_TA" => (ReplayNetworkK4ProductValueV1::Paint(read_bits(cursor, 31)? as u32), "Paint:new31".to_owned()),
        "TAGame.ProductAttribute_TitleID_TA" => { let (text, text_shape) = decode_text(cursor)?; (ReplayNetworkK4ProductValueV1::Title(text), format!("Title:{text_shape}")) }
        "TAGame.ProductAttribute_SpecialEdition_TA" => (ReplayNetworkK4ProductValueV1::SpecialEdition(read_bits(cursor, 31)? as u32), "SpecialEdition:31".to_owned()),
        "TAGame.ProductAttribute_TeamEdition_TA" => (ReplayNetworkK4ProductValueV1::TeamEdition(read_bits(cursor, 31)? as u32), "TeamEdition:new31".to_owned()),
        other => return Err(k4_error("unadmitted-k4-shape", format!("unknown product attribute object branch {other:?}"))),
    };
    Ok((ReplayNetworkK4OnlineProductV1 { unknown, object_id, value }, shape))
}

fn decode_online_side(cursor: &mut NetworkBitCursor<'_>, object_table: &[String], name: &str) -> Result<(Vec<Vec<ReplayNetworkK4OnlineProductV1>>, String)> {
    let outer = usize::from(read_u8(cursor)?); let mut groups = Vec::new(); groups.try_reserve_exact(outer).map_err(|_| k4_error("invalid-length-or-count", format!("cannot reserve {outer} online-loadout groups")))?;
    let mut shape = format!("{name}:outer{outer}[");
    for group_index in 0..outer {
        let count = usize::from(read_u8(cursor)?); let mut products = Vec::new(); products.try_reserve_exact(count).map_err(|_| k4_error("invalid-length-or-count", format!("cannot reserve {count} products in group {group_index}")))?;
        if group_index != 0 { shape.push(';'); } shape.push_str(&format!("g{group_index}:{count}("));
        for product_index in 0..count { let (product, product_shape) = decode_product(cursor, object_table)?; if product_index != 0 { shape.push(','); } shape.push_str(&product_shape); products.push(product); }
        shape.push(')'); groups.push(products);
    }
    shape.push(']'); Ok((groups, shape))
}

fn decode_one(cursor: &mut NetworkBitCursor<'_>, attribute_tag: ReplayNetworkAttributeTagV1, context: ReplayNetworkK4DecodeContextV1, object_table: &[String]) -> Result<(ReplayNetworkK4ValueV1, String)> {
    match attribute_tag {
        ReplayNetworkAttributeTagV1::CamSettings => { let mut raw_f32_bits = Vec::with_capacity(7); for _ in 0..6 { raw_f32_bits.push(read_u32(cursor)?); } let has_transition = (context.version_major, context.version_minor, context.net_version) >= (868,20,0); if has_transition { raw_f32_bits.push(read_u32(cursor)?); } Ok((ReplayNetworkK4ValueV1::CamSettings { raw_f32_bits }, format!("CamSettings:f32x{}", if has_transition {7}else{6}))) }
        ReplayNetworkAttributeTagV1::TeamPaint => Ok((ReplayNetworkK4ValueV1::TeamPaint { team: read_u8(cursor)?, primary_color: read_u8(cursor)?, accent_color: read_u8(cursor)?, primary_finish: read_u32(cursor)?, accent_finish: read_u32(cursor)? }, "TeamPaint:u8x3_u32x2".to_owned())),
        ReplayNetworkAttributeTagV1::TeamLoadout => { let (blue,bs)=decode_loadout(cursor)?; let (orange,os)=decode_loadout(cursor)?; Ok((ReplayNetworkK4ValueV1::TeamLoadout{blue,orange},format!("TeamLoadout:blue[{bs}]:orange[{os}]"))) }
        ReplayNetworkAttributeTagV1::ClubColors => Ok((ReplayNetworkK4ValueV1::ClubColors { blue_flag:read_bits(cursor,1)?!=0, blue_color:read_u8(cursor)?, orange_flag:read_bits(cursor,1)?!=0, orange_color:read_u8(cursor)? }, "ClubColors:b1_u8_b1_u8".to_owned())),
        ReplayNetworkAttributeTagV1::Reservation => { let number=read_bits(cursor,3)? as u8; let (player_id,id_shape,needs_name)=decode_reservation_id(cursor,context)?; let (name,name_shape)=if needs_name { let(v,s)=decode_text(cursor)?;(Some(v),s) } else {(None,"none".to_owned())}; let unknown1=read_bits(cursor,1)?!=0; let unknown2=read_bits(cursor,1)?!=0; let has_unknown3=(context.version_major,context.version_minor,context.net_version)>=(868,12,0); let unknown3=if has_unknown3{Some(read_bits(cursor,6)? as u8)}else{None}; Ok((ReplayNetworkK4ValueV1::Reservation(ReplayNetworkK4ReservationV1{number,player_id,name,unknown1,unknown2,unknown3}),format!("Reservation:{id_shape}:name_{name_shape}:u3_{has_unknown3}"))) }
        ReplayNetworkAttributeTagV1::StatEvent => Ok((ReplayNetworkK4ValueV1::StatEvent{unknown1:read_bits(cursor,1)?!=0,object_id:read_i32(cursor)?},"StatEvent:b1_i32".to_owned())),
        ReplayNetworkAttributeTagV1::PlayerHistoryKey => Ok((ReplayNetworkK4ValueV1::PlayerHistoryKey(read_bits(cursor,14)? as u16),"PlayerHistoryKey:u14".to_owned())),
        ReplayNetworkAttributeTagV1::DemolishFx => { let custom_demo_flag=read_bits(cursor,1)?!=0;let custom_demo_id=read_i32(cursor)?;let attacker_flag=read_bits(cursor,1)?!=0;let attacker=read_i32(cursor)?;let victim_flag=read_bits(cursor,1)?!=0;let victim=read_i32(cursor)?;let(attack_velocity,as_)=decode_vector(cursor,"attack_velocity")?;let(victim_velocity,vs)=decode_vector(cursor,"victim_velocity")?;Ok((ReplayNetworkK4ValueV1::DemolishFx{custom_demo_flag,custom_demo_id,attacker_flag,attacker,victim_flag,victim,attack_velocity,victim_velocity},format!("DemolishFx:{as_}:{vs}"))) }
        ReplayNetworkAttributeTagV1::DemolishExtended => { let attacker_pri=decode_active_actor(cursor)?;let self_demo=decode_active_actor(cursor)?;let self_demolish=read_bits(cursor,1)?!=0;let goal_explosion_owner=decode_active_actor(cursor)?;let attacker=decode_active_actor(cursor)?;let victim=decode_active_actor(cursor)?;let(attacker_velocity,as_)=decode_vector(cursor,"attacker_velocity")?;let(victim_velocity,vs)=decode_vector(cursor,"victim_velocity")?;Ok((ReplayNetworkK4ValueV1::DemolishExtended{attacker_pri,self_demo,self_demolish,goal_explosion_owner,attacker,victim,attacker_velocity,victim_velocity},format!("DemolishExtended:activex5:{as_}:{vs}"))) }
        ReplayNetworkAttributeTagV1::ExtendedExplosion => { let flag=read_bits(cursor,1)?!=0;let actor=read_i32(cursor)?;let(location,ls)=decode_vector(cursor,"location")?;let unknown1=read_bits(cursor,1)?!=0;let secondary_actor=read_i32(cursor)?;Ok((ReplayNetworkK4ValueV1::ExtendedExplosion{flag,actor,location,unknown1,secondary_actor},format!("ExtendedExplosion:{ls}"))) }
        ReplayNetworkAttributeTagV1::LoadoutsOnline => { let(blue,bs)=decode_online_side(cursor,object_table,"blue")?;let(orange,os)=decode_online_side(cursor,object_table,"orange")?;let unknown1=read_bits(cursor,1)?!=0;let unknown2=read_bits(cursor,1)?!=0;Ok((ReplayNetworkK4ValueV1::LoadoutsOnline{blue,orange,unknown1,unknown2},format!("LoadoutsOnline:{bs}:{os}"))) }
        _ => Err(k4_error("unsupported-k4-tag",format!("attribute tag {attribute_tag:?} is not an R3.17N K4 tag"))),
    }
}

pub fn decode_replay_network_k4_v1(network_bytes:&[u8], payload_start_bit:u64, attribute_tag:ReplayNetworkAttributeTagV1, context:ReplayNetworkK4DecodeContextV1, object_table:&[String]) -> Result<ReplayNetworkK4DecodeV1> {
    let total_bits=network_bytes.len().checked_mul(8).ok_or_else(||k4_error("invalid-start","network bit length overflows usize"))?; let total_bits_u64=u64::try_from(total_bits).map_err(|_|k4_error("invalid-start","network bit length does not fit u64"))?;
    if payload_start_bit>total_bits_u64{return Err(k4_error("invalid-start",format!("payload start {payload_start_bit} exceeds network length {total_bits_u64} bits")));}
    let start=usize::try_from(payload_start_bit).map_err(|_|k4_error("invalid-start",format!("payload start {payload_start_bit} does not fit usize")))?; validate_context(context)?;
    let mut cursor=NetworkBitCursor::new(network_bytes);reset(&mut cursor,start);let decoded=decode_one(&mut cursor,attribute_tag,context,object_table);let(value,structural_shape)=match decoded{Ok(v)=>v,Err(e)=>{reset(&mut cursor,start);return Err(e);}};
    let payload_end_bit=u64::try_from(cursor.position_bits()).map_err(|_|{reset(&mut cursor,start);k4_error("invalid-start","decoded end bit does not fit u64")})?;let payload_width=payload_end_bit.checked_sub(payload_start_bit).ok_or_else(||{reset(&mut cursor,start);k4_error("invalid-start","decoded end bit precedes payload start")})?;
    if !k4_admitted_groups::contains(attribute_tag,context.version_major,context.version_minor,context.net_version,context.is_rl_223,payload_width,&structural_shape){reset(&mut cursor,start);return Err(k4_error("unadmitted-k4-shape",format!("exact tuple is absent from R3.17N: tag={attribute_tag:?} context={}.{} net{} rl223={} width={} shape={structural_shape}",context.version_major,context.version_minor,context.net_version,context.is_rl_223,payload_width)));}
    Ok(ReplayNetworkK4DecodeV1{attribute_tag,payload_start_bit,payload_end_bit,payload_width,structural_shape,value})
}
'''


def generate_test(rows: list[dict]) -> str:
    cases = []
    for i, r in enumerate(rows):
        bits = emit_shape(r["shape"])
        if len(bits.bits) != r["payload_width"]:
            raise SystemExit(f"materialized width mismatch row {i}: {r['shape']} {len(bits.bits)} != {r['payload_width']}")
        cases.append((r, bits.bytes().hex()))

    by_tag: dict[str, list[dict]] = {}
    for r in rows:
        by_tag.setdefault(r["attribute_tag"], []).append(r)

    def find_cross(tag: str, prefix: str, right_name: str) -> tuple[dict, str, str]:
        shape_rows = by_tag[tag]
        observed = {r["shape"] for r in shape_rows}
        lefts, rights = set(), set()
        for r in shape_rows:
            rest = r["shape"][len(prefix):]
            marker = f":{right_name}:"
            a, b = rest.split(marker, 1)
            lefts.add(a)
            rights.add(f"{right_name}:{b}")
        for a in sorted(lefts):
            for b in sorted(rights):
                shape = f"{prefix}{a}:{b}"
                if shape not in observed:
                    fake = dict(shape_rows[0]); fake["shape"] = shape; material = emit_shape(shape); fake["payload_width"] = len(material.bits)
                    return fake, material.bytes().hex(), shape
        raise SystemExit(f"no cross-product negative found for {tag}")

    fx_fake, fx_hex, fx_shape = find_cross("DemolishFx", "DemolishFx:", "victim_velocity")
    ext_fake, ext_hex, ext_shape = find_cross("DemolishExtended", "DemolishExtended:activex5:", "victim_velocity")

    reservation_rows = by_tag["Reservation"]; reservation_shapes = {r["shape"] for r in reservation_rows}; reservation_fake = None
    for r in reservation_rows:
        if not re.search(r":name_w1252_(\d+):u3_true$", r["shape"]): continue
        for n in range(1, 40):
            candidate = re.sub(r":name_w1252_\d+:u3_true$", f":name_w1252_{n}:u3_true", r["shape"])
            if candidate not in reservation_shapes:
                fake = dict(r); fake["shape"] = candidate; material = emit_shape(candidate); fake["payload_width"] = len(material.bits); reservation_fake = (fake, material.bytes().hex(), candidate); break
        if reservation_fake: break
    if reservation_fake is None: raise SystemExit("no reservation negative found")

    load_rows = by_tag["LoadoutsOnline"]; load_shapes = {r["shape"] for r in load_rows}; load_fake = None
    for r in load_rows:
        candidate = r["shape"].replace("g0:0()", "g0:1(Paint:new31)", 1)
        if candidate != r["shape"] and candidate not in load_shapes:
            fake = dict(r); fake["shape"] = candidate; material = emit_shape(candidate); fake["payload_width"] = len(material.bits); load_fake = (fake, material.bytes().hex(), candidate); break
    if load_fake is None: raise SystemExit("no LoadoutsOnline negative found")

    lines = [
        "use mimir_replay::{", "    decode_replay_network_k4_v1, ReplayNetworkAttributeTagV1,", "    ReplayNetworkK4DecodeContextV1, R3_17N_K4_ADMITTED_GROUPS_V1,", "};", "",
        "#[derive(Clone, Copy)]", "struct Case { tag: ReplayNetworkAttributeTagV1, major:i32, minor:i32, net:i32, rl223:bool, width:u64, shape:&'static str, payload_hex:&'static str }", "",
        "const CASES:&[Case]=&[",
    ]
    for r, hx in cases:
        lines.append(f"    Case{{tag:ReplayNetworkAttributeTagV1::{TAG_VARIANTS[r['attribute_tag']]},major:{r['version_major']},minor:{r['version_minor']},net:{r['net_version']},rl223:{str(r['is_rl_223']).lower()},width:{r['payload_width']},shape:{rust_string(r['shape'])},payload_hex:{rust_string(hx)}}},")
    lines += [
        "];", "", "const OBJECT_TABLE:&[&str]=&[",
    ]
    for value in OBJECT_TABLE: lines.append(f"    {rust_string(value)},")
    lines += [
        "];", "", "fn object_table()->Vec<String>{OBJECT_TABLE.iter().map(|v|(*v).to_owned()).collect()}",
        "fn hex_bytes(s:&str)->Vec<u8>{fn n(b:u8)->u8{match b{b'0'..=b'9'=>b-b'0',b'a'..=b'f'=>b-b'a'+10,_=>panic!(\"bad hex\")}}let b=s.as_bytes();assert_eq!(b.len()%2,0);b.chunks_exact(2).map(|c|(n(c[0])<<4)|n(c[1])).collect()}",
        "fn repack(case:Case,start:usize,payload_bits:usize,trailing_bits:usize)->Vec<u8>{let p=hex_bytes(case.payload_hex);let total=start+payload_bits+trailing_bits;let mut out=vec![0u8;total.div_ceil(8)];for i in 0..payload_bits{let bit=(p[i/8]>>(i%8))&1;if bit!=0{out[(start+i)/8]|=1<<((start+i)%8);}}for i in 0..trailing_bits{if i%2==0{let q=start+payload_bits+i;out[q/8]|=1<<(q%8);}}out}",
        "fn context(c:Case)->ReplayNetworkK4DecodeContextV1{ReplayNetworkK4DecodeContextV1{version_major:c.major,version_minor:c.minor,net_version:c.net,is_rl_223:c.rl223}}", "",
        "#[test] fn admitted_group_table_is_exactly_161_unique_rows(){assert_eq!(R3_17N_K4_ADMITTED_GROUPS_V1.len(),161);assert_eq!(CASES.len(),161);for(g,c)in R3_17N_K4_ADMITTED_GROUPS_V1.iter().zip(CASES){assert_eq!(g.attribute_tag,c.tag);assert_eq!(g.version_major,c.major);assert_eq!(g.version_minor,c.minor);assert_eq!(g.net_version,c.net);assert_eq!(g.is_rl_223,c.rl223);assert_eq!(g.payload_width,c.width);assert_eq!(g.structural_shape,c.shape);}}",
        "#[test] fn all_161_admitted_rows_decode_exactly_and_repeatably(){let objects=object_table();for c in CASES.iter().copied(){let start=3usize;let network=repack(c,start,c.width as usize,13);let first=decode_replay_network_k4_v1(&network,start as u64,c.tag,context(c),&objects).unwrap_or_else(|e|panic!(\"{}: {e}\",c.shape));assert_eq!(first.attribute_tag,c.tag);assert_eq!(first.value.attribute_tag(),c.tag);assert_eq!(first.payload_start_bit,start as u64);assert_eq!(first.payload_width,c.width);assert_eq!(first.payload_end_bit,start as u64+c.width);assert_eq!(first.structural_shape,c.shape);let second=decode_replay_network_k4_v1(&network,start as u64,c.tag,context(c),&objects).unwrap();assert_eq!(first,second);}}",
        "#[test] fn wrong_context_and_unsupported_tag_fail_closed(){let c=CASES[0];let objects=object_table();let network=repack(c,3,c.width as usize,8);let mut bad=context(c);bad.version_minor=31;let e=decode_replay_network_k4_v1(&network,3,c.tag,bad,&objects).unwrap_err().to_string();assert!(e.contains(\"unadmitted-context\"),\"{e}\");let e=decode_replay_network_k4_v1(&network,3,ReplayNetworkAttributeTagV1::Boolean,context(c),&objects).unwrap_err().to_string();assert!(e.contains(\"unsupported-k4-tag\"),\"{e}\");let e=decode_replay_network_k4_v1(&network,(network.len()*8+1)as u64,c.tag,context(c),&objects).unwrap_err().to_string();assert!(e.contains(\"invalid-start\"),\"{e}\");}",
        "#[test] fn one_bit_truncation_fails_for_fixed_and_variable_payloads(){let objects=object_table();for c in[*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::CamSettings).unwrap(),*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::Reservation&&c.shape.contains(\"sys11_epic\")).unwrap(),*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::LoadoutsOnline).unwrap()]{let w=c.width as usize;let start=(8-((w-1)%8))%8;let network=repack(c,start,w-1,0);assert_eq!(network.len()*8,start+w-1);let e=decode_replay_network_k4_v1(&network,start as u64,c.tag,context(c),&objects).unwrap_err().to_string();assert!(e.contains(\"insufficient-bits\")||e.contains(\"unadmitted-k4-shape\"),\"{}: {e}\",c.shape);}}",
        "#[test] fn exact_tuple_coupling_rejects_cross_products_and_mutations(){let objects=object_table();",
    ]
    negs=[("fx",fx_fake,fx_hex,fx_shape),("ext",ext_fake,ext_hex,ext_shape),("reservation",reservation_fake[0],reservation_fake[1],reservation_fake[2]),("loadouts",load_fake[0],load_fake[1],load_fake[2])]
    for name,r,hx,shape in negs:
        lines += [f"let {name}=Case{{tag:ReplayNetworkAttributeTagV1::{TAG_VARIANTS[r['attribute_tag']]},major:{r['version_major']},minor:{r['version_minor']},net:{r['net_version']},rl223:{str(r['is_rl_223']).lower()},width:{r['payload_width']},shape:{rust_string(shape)},payload_hex:{rust_string(hx)}}};",f"let network=repack({name},3,{name}.width as usize,8);let e=decode_replay_network_k4_v1(&network,3,{name}.tag,context({name}),&objects).unwrap_err().to_string();assert!(e.contains(\"unadmitted-k4-shape\"),\"{name}: {{e}}\");"]
    lines += [
        "}",
        "#[test] fn malformed_text_and_unknown_product_object_fail_closed(){let objects=object_table();let c=*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::Reservation&&c.shape.contains(\"sys11_epic\")).unwrap();let mut raw=vec![0u8;6];fn set(raw:&mut[u8],pos:usize,value:u64,width:usize){for i in 0..width{if((value>>i)&1)!=0{raw[(pos+i)/8]|=1<<((pos+i)%8);}}}set(&mut raw,3,11,8);set(&mut raw,11,0x8000_0000,32);let e=decode_replay_network_k4_v1(&raw,0,c.tag,context(c),&objects).unwrap_err().to_string();assert!(e.contains(\"invalid-length-or-count\"),\"{e}\");let online=*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::LoadoutsOnline).unwrap();let network=repack(online,3,online.width as usize,8);let bad_objects=vec![\"Unknown.Product.Attribute\".to_owned();5];let e=decode_replay_network_k4_v1(&network,3,online.tag,context(online),&bad_objects).unwrap_err().to_string();assert!(e.contains(\"unadmitted-k4-shape\"),\"{e}\");}",
        "#[test] fn unobserved_team_loadout_version_is_rejected(){let observed=*CASES.iter().find(|c|c.tag==ReplayNetworkAttributeTagV1::TeamLoadout).unwrap();let p=hex_bytes(observed.payload_hex);let mut bits=Vec::new();for i in 0..observed.width as usize{bits.push((p[i/8]>>(i%8))&1);}for(base,value)in[(0usize,27u8),(520usize,27u8)]{for i in 0..8{bits[base+i]=(value>>i)&1;}}let mut packed=vec![0u8;bits.len().div_ceil(8)];for(i,b)in bits.into_iter().enumerate(){if b!=0{packed[i/8]|=1<<(i%8);}}let e=decode_replay_network_k4_v1(&packed,0,observed.tag,context(observed),&object_table()).unwrap_err().to_string();assert!(e.contains(\"unadmitted-k4-shape\"),\"{e}\");}",
        "#[test] fn flipping_rl223_for_a_single_context_group_is_rejected(){let objects=object_table();let c=*CASES.iter().find(|candidate|!CASES.iter().any(|other|other.tag==candidate.tag&&other.major==candidate.major&&other.minor==candidate.minor&&other.net==candidate.net&&other.rl223!=candidate.rl223&&other.width==candidate.width&&other.shape==candidate.shape)).unwrap();let network=repack(c,3,c.width as usize,8);let mut ctx=context(c);ctx.is_rl_223=!ctx.is_rl_223;let e=decode_replay_network_k4_v1(&network,3,c.tag,ctx,&objects).unwrap_err().to_string();assert!(e.contains(\"unadmitted-k4-shape\"),\"{e}\");}",
    ]
    return "\n".join(lines)+"\n"


def update_lib() -> None:
    text=LIB_PATH.read_text(encoding="utf-8");anchor="mod k3_admitted_groups;\n"
    if text.count(anchor)!=1:raise SystemExit("lib module anchor mismatch")
    replacement="mod k3_admitted_groups;\nmod k4_admitted_groups;\nmod k4_native;\npub use k4_admitted_groups::{ReplayNetworkK4AdmittedGroupV1, R3_17N_K4_ADMITTED_GROUPS_V1};\npub use k4_native::*;\n"
    LIB_PATH.write_text(text.replace(anchor,replacement,1),encoding="utf-8",newline="\n")


def main() -> None:
    rows=load_rows();ALLOW_PATH.write_text(generate_allowlist(rows),encoding="utf-8",newline="\n");NATIVE_PATH.write_text(NATIVE_RS,encoding="utf-8",newline="\n");TEST_PATH.write_text(generate_test(rows),encoding="utf-8",newline="\n");update_lib()
    print("R3.17O generation complete");print(f"rows={len(rows)}");print(f"allowlist_sha256={hashlib.sha256(ALLOW_PATH.read_bytes()).hexdigest()}");print(f"native_sha256={hashlib.sha256(NATIVE_PATH.read_bytes()).hexdigest()}");print(f"test_sha256={hashlib.sha256(TEST_PATH.read_bytes()).hexdigest()}")


if __name__=="__main__":main()
