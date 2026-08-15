use super::{
    MimirError, NetworkBitCursor, ReplayNetworkAttributeTagV1, ReplayNetworkTextEncodingV1,
    ReplayNetworkTextV1, ReplayNetworkVector3V1, Result, decode_network_windows1252,
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
    SplitScreen {
        split_id: u32,
        local_id: u8,
    },
    Steam {
        online_id: u64,
        local_id: u8,
    },
    PlayStation {
        name_bytes: Vec<u8>,
        unknown: Vec<u8>,
        online_id: u64,
        local_id: u8,
    },
    Xbox {
        online_id: u64,
        local_id: u8,
    },
    Qq {
        online_id: u64,
        local_id: u8,
    },
    Switch {
        online_id: u64,
        unknown: Vec<u8>,
        local_id: u8,
    },
    PsyNet {
        online_id: u64,
        local_id: u8,
    },
    Epic {
        account_id: ReplayNetworkTextV1,
        local_id: u8,
    },
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
pub struct ReplayNetworkK4ActiveActorV1 {
    pub active: bool,
    pub actor: i32,
}
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkK4ProductValueV1 {
    UserColor(u32),
    Paint(u32),
    Title(ReplayNetworkTextV1),
    SpecialEdition(u32),
    TeamEdition(u32),
}
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK4OnlineProductV1 {
    pub unknown: bool,
    pub object_id: i32,
    pub value: ReplayNetworkK4ProductValueV1,
}
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ReplayNetworkK4ValueV1 {
    CamSettings {
        raw_f32_bits: Vec<u32>,
    },
    TeamPaint {
        team: u8,
        primary_color: u8,
        accent_color: u8,
        primary_finish: u32,
        accent_finish: u32,
    },
    TeamLoadout {
        blue: ReplayNetworkK4LoadoutV1,
        orange: ReplayNetworkK4LoadoutV1,
    },
    ClubColors {
        blue_flag: bool,
        blue_color: u8,
        orange_flag: bool,
        orange_color: u8,
    },
    Reservation(ReplayNetworkK4ReservationV1),
    StatEvent {
        unknown1: bool,
        object_id: i32,
    },
    PlayerHistoryKey(u16),
    DemolishFx {
        custom_demo_flag: bool,
        custom_demo_id: i32,
        attacker_flag: bool,
        attacker: i32,
        victim_flag: bool,
        victim: i32,
        attack_velocity: ReplayNetworkVector3V1,
        victim_velocity: ReplayNetworkVector3V1,
    },
    DemolishExtended {
        attacker_pri: ReplayNetworkK4ActiveActorV1,
        self_demo: ReplayNetworkK4ActiveActorV1,
        self_demolish: bool,
        goal_explosion_owner: ReplayNetworkK4ActiveActorV1,
        attacker: ReplayNetworkK4ActiveActorV1,
        victim: ReplayNetworkK4ActiveActorV1,
        attacker_velocity: ReplayNetworkVector3V1,
        victim_velocity: ReplayNetworkVector3V1,
    },
    ExtendedExplosion {
        flag: bool,
        actor: i32,
        location: ReplayNetworkVector3V1,
        unknown1: bool,
        secondary_actor: i32,
    },
    LoadoutsOnline {
        blue: Vec<Vec<ReplayNetworkK4OnlineProductV1>>,
        orange: Vec<Vec<ReplayNetworkK4OnlineProductV1>>,
        unknown1: bool,
        unknown2: bool,
    },
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
    MimirError::message(format!(
        "replay network k4 error: {category}: {}",
        detail.into()
    ))
}
fn reset(cursor: &mut NetworkBitCursor<'_>, start: usize) {
    cursor.bit_position = start;
    debug_assert_eq!(cursor.position_bits(), start);
}
fn read_bits(cursor: &mut NetworkBitCursor<'_>, width: usize) -> Result<u64> {
    if cursor.remaining_bits() < width {
        return Err(k4_error(
            "insufficient-bits",
            format!(
                "need {width} bits at position {}, but only {} remain",
                cursor.position_bits(),
                cursor.remaining_bits()
            ),
        ));
    }
    cursor
        .read_bits_le(width)
        .map_err(|e| k4_error("insufficient-bits", format!("bit read failed: {e}")))
}
fn read_u8(c: &mut NetworkBitCursor<'_>) -> Result<u8> {
    Ok(read_bits(c, 8)? as u8)
}
fn read_u32(c: &mut NetworkBitCursor<'_>) -> Result<u32> {
    Ok(read_bits(c, 32)? as u32)
}
fn read_i32(c: &mut NetworkBitCursor<'_>) -> Result<i32> {
    Ok(read_u32(c)? as i32)
}
fn read_u64(c: &mut NetworkBitCursor<'_>) -> Result<u64> {
    read_bits(c, 64)
}
fn read_bytes(c: &mut NetworkBitCursor<'_>, count: usize) -> Result<Vec<u8>> {
    let required = count
        .checked_mul(8)
        .ok_or_else(|| k4_error("invalid-length-or-count", "byte count bit width overflows"))?;
    if c.remaining_bits() < required {
        return Err(k4_error(
            "insufficient-bits",
            format!(
                "need {required} byte-content bits at position {}, but only {} remain",
                c.position_bits(),
                c.remaining_bits()
            ),
        ));
    }
    let mut out = Vec::new();
    out.try_reserve_exact(count).map_err(|_| {
        k4_error(
            "invalid-length-or-count",
            format!("cannot reserve {count} bytes"),
        )
    })?;
    for _ in 0..count {
        out.push(read_u8(c)?);
    }
    Ok(out)
}
fn decode_text(c: &mut NetworkBitCursor<'_>) -> Result<(ReplayNetworkTextV1, String)> {
    let d = read_i32(c)?;
    if d == 0 {
        return Ok((
            ReplayNetworkTextV1 {
                value: String::new(),
                declared_length: 0,
                encoding: ReplayNetworkTextEncodingV1::Empty,
            },
            "empty".to_owned(),
        ));
    }
    if d > 0 {
        let n = usize::try_from(d).map_err(|_| {
            k4_error(
                "invalid-length-or-count",
                format!("positive text length {d} does not fit usize"),
            )
        })?;
        let bytes = read_bytes(c, n)?;
        let content = &bytes[..n - 1];
        return Ok((
            ReplayNetworkTextV1 {
                value: decode_network_windows1252(content),
                declared_length: d,
                encoding: ReplayNetworkTextEncodingV1::Windows1252,
            },
            format!("w1252_{d}"),
        ));
    }
    if d == i32::MIN {
        return Err(k4_error(
            "invalid-length-or-count",
            "i32::MIN cannot be negated for UTF-16 length",
        ));
    }
    let units = usize::try_from(-d).map_err(|_| {
        k4_error(
            "invalid-length-or-count",
            format!("UTF-16 length {d} does not fit usize"),
        )
    })?;
    let count = units
        .checked_mul(2)
        .ok_or_else(|| k4_error("invalid-length-or-count", "UTF-16 byte count overflows"))?;
    let bytes = read_bytes(c, count)?;
    let content = &bytes[..count - 2];
    let mut u = Vec::new();
    u.try_reserve_exact(content.len() / 2)
        .map_err(|_| k4_error("invalid-length-or-count", "UTF-16 reserve failed"))?;
    for p in content.chunks_exact(2) {
        u.push(u16::from_le_bytes([p[0], p[1]]));
    }
    Ok((
        ReplayNetworkTextV1 {
            value: String::from_utf16_lossy(&u),
            declared_length: d,
            encoding: ReplayNetworkTextEncodingV1::Utf16Le,
        },
        format!("utf16_{}", -d),
    ))
}
fn validate_context(x: ReplayNetworkK4DecodeContextV1) -> Result<()> {
    if x.version_major != 868 || x.version_minor != 32 || x.net_version != 10 {
        return Err(k4_error(
            "unadmitted-context",
            format!(
                "K4 requires replay version 868.32 / net10, got {}.{} / net{}",
                x.version_major, x.version_minor, x.net_version
            ),
        ));
    }
    Ok(())
}
fn decode_vector(
    c: &mut NetworkBitCursor<'_>,
    name: &str,
) -> Result<(ReplayNetworkVector3V1, String)> {
    let low = read_bits(c, 4)? as u8;
    let candidate = low + 16;
    let (selected, h) = if candidate < 22 {
        let d = read_bits(c, 1)? != 0;
        (if d { candidate } else { low }, 5u8)
    } else {
        (low, 4u8)
    };
    if selected >= 20 {
        return Err(k4_error(
            "unadmitted-k4-shape",
            format!("vector selected size {selected} is not admitted"),
        ));
    }
    let cw = selected + 2;
    let x = read_bits(c, cw as usize)? as u32;
    let y = read_bits(c, cw as usize)? as u32;
    let z = read_bits(c, cw as usize)? as u32;
    let bias = 1i64 << (selected + 1);
    let f = |r: u32| (i64::from(r) - bias) as f32 / 100.0;
    Ok((
        ReplayNetworkVector3V1 {
            selected_size_bits: selected,
            component_width: cw,
            raw_x: x,
            raw_y: y,
            raw_z: z,
            x: f(x),
            y: f(y),
            z: f(z),
        },
        format!("{name}:sb{selected}:h{h}:cw{cw}"),
    ))
}
fn decode_loadout(c: &mut NetworkBitCursor<'_>) -> Result<(ReplayNetworkK4LoadoutV1, String)> {
    let v = read_u8(c)?;
    let mut base = Vec::with_capacity(7);
    for _ in 0..7 {
        base.push(read_u32(c)?);
    }
    let (u2, u2s) = if v > 10 {
        (Some(read_u32(c)?), "u2")
    } else {
        (None, "nou2")
    };
    let (sp, sps) = if v >= 16 {
        (vec![read_u32(c)?, read_u32(c)?, read_u32(c)?], "specials")
    } else {
        (Vec::new(), "nospecials")
    };
    let (ban, bans) = if v >= 17 {
        (Some(read_u32(c)?), "banner")
    } else {
        (None, "nobanner")
    };
    let (prod, prods) = if v >= 19 {
        (Some(read_u32(c)?), "product")
    } else {
        (None, "noproduct")
    };
    let (ex, exs) = if v >= 22 {
        (vec![read_u32(c)?, read_u32(c)?, read_u32(c)?], "extra3")
    } else {
        (Vec::new(), "noextra3")
    };
    Ok((
        ReplayNetworkK4LoadoutV1 {
            version: v,
            base_fields: base,
            unknown2: u2,
            specials: sp,
            banner: ban,
            product_id: prod,
            v22_extras: ex,
        },
        format!("v{v}:{u2s}:{sps}:{bans}:{prods}:{exs}"),
    ))
}
fn decode_reservation_id(
    c: &mut NetworkBitCursor<'_>,
    ctx: ReplayNetworkK4DecodeContextV1,
) -> Result<(ReplayNetworkK4ReservationIdV1, String, bool)> {
    let s = read_u8(c)?;
    let (remote, shape, needs) = match s {
        0 => {
            let split = read_bits(c, 24)? as u32;
            (
                ReplayNetworkK4ReservationIdV1::SplitScreen {
                    split_id: split,
                    local_id: 0,
                },
                format!(
                    "sys0_split24_{}",
                    if split == 0 { "zero" } else { "nonzero" }
                ),
                split != 0,
            )
        }
        1 => (
            ReplayNetworkK4ReservationIdV1::Steam {
                online_id: read_u64(c)?,
                local_id: 0,
            },
            "sys1_steam64".to_owned(),
            true,
        ),
        2 => (
            ReplayNetworkK4ReservationIdV1::PlayStation {
                name_bytes: read_bytes(c, 16)?,
                unknown: read_bytes(c, 16)?,
                online_id: read_u64(c)?,
                local_id: 0,
            },
            "sys2_playstation320".to_owned(),
            true,
        ),
        4 => (
            ReplayNetworkK4ReservationIdV1::Xbox {
                online_id: read_u64(c)?,
                local_id: 0,
            },
            "sys4_xbox64".to_owned(),
            true,
        ),
        5 => (
            ReplayNetworkK4ReservationIdV1::Qq {
                online_id: read_u64(c)?,
                local_id: 0,
            },
            "sys5_qq64".to_owned(),
            true,
        ),
        6 => (
            ReplayNetworkK4ReservationIdV1::Switch {
                online_id: read_u64(c)?,
                unknown: read_bytes(c, 24)?,
                local_id: 0,
            },
            "sys6_switch256".to_owned(),
            true,
        ),
        7 => {
            let id = read_u64(c)?;
            if ctx.net_version < 10 {
                let _ = read_bytes(c, 24)?;
                return Err(k4_error(
                    "unadmitted-context",
                    "net<10 PsyNet is outside R3.17N",
                ));
            }
            (
                ReplayNetworkK4ReservationIdV1::PsyNet {
                    online_id: id,
                    local_id: 0,
                },
                "sys7_psynet64".to_owned(),
                true,
            )
        }
        11 => {
            let (t, ts) = decode_text(c)?;
            (
                ReplayNetworkK4ReservationIdV1::Epic {
                    account_id: t,
                    local_id: 0,
                },
                format!("sys11_epic_{ts}"),
                true,
            )
        }
        o => {
            return Err(k4_error(
                "unadmitted-k4-shape",
                format!("reservation unique-id system {o} is unadmitted"),
            ));
        }
    };
    let local = read_u8(c)?;
    let remote = match remote {
        ReplayNetworkK4ReservationIdV1::SplitScreen { split_id, .. } => {
            ReplayNetworkK4ReservationIdV1::SplitScreen {
                split_id,
                local_id: local,
            }
        }
        ReplayNetworkK4ReservationIdV1::Steam { online_id, .. } => {
            ReplayNetworkK4ReservationIdV1::Steam {
                online_id,
                local_id: local,
            }
        }
        ReplayNetworkK4ReservationIdV1::PlayStation {
            name_bytes,
            unknown,
            online_id,
            ..
        } => ReplayNetworkK4ReservationIdV1::PlayStation {
            name_bytes,
            unknown,
            online_id,
            local_id: local,
        },
        ReplayNetworkK4ReservationIdV1::Xbox { online_id, .. } => {
            ReplayNetworkK4ReservationIdV1::Xbox {
                online_id,
                local_id: local,
            }
        }
        ReplayNetworkK4ReservationIdV1::Qq { online_id, .. } => {
            ReplayNetworkK4ReservationIdV1::Qq {
                online_id,
                local_id: local,
            }
        }
        ReplayNetworkK4ReservationIdV1::Switch {
            online_id, unknown, ..
        } => ReplayNetworkK4ReservationIdV1::Switch {
            online_id,
            unknown,
            local_id: local,
        },
        ReplayNetworkK4ReservationIdV1::PsyNet { online_id, .. } => {
            ReplayNetworkK4ReservationIdV1::PsyNet {
                online_id,
                local_id: local,
            }
        }
        ReplayNetworkK4ReservationIdV1::Epic { account_id, .. } => {
            ReplayNetworkK4ReservationIdV1::Epic {
                account_id,
                local_id: local,
            }
        }
    };
    Ok((remote, shape, needs))
}
fn active(c: &mut NetworkBitCursor<'_>) -> Result<ReplayNetworkK4ActiveActorV1> {
    Ok(ReplayNetworkK4ActiveActorV1 {
        active: read_bits(c, 1)? != 0,
        actor: read_i32(c)?,
    })
}
fn product(
    c: &mut NetworkBitCursor<'_>,
    objects: &[String],
) -> Result<(ReplayNetworkK4OnlineProductV1, String)> {
    let unknown = read_bits(c, 1)? != 0;
    let id = read_i32(c)?;
    let slot = usize::try_from(id).map_err(|_| {
        k4_error(
            "unadmitted-k4-shape",
            format!("negative product object id {id}"),
        )
    })?;
    let name = objects.get(slot).ok_or_else(|| {
        k4_error(
            "unadmitted-k4-shape",
            format!("product object id {id} outside table"),
        )
    })?;
    let (value, shape) = match name.as_str() {
        "TAGame.ProductAttribute_UserColor_TA" => (
            ReplayNetworkK4ProductValueV1::UserColor(read_u32(c)?),
            "UserColor:new32".to_owned(),
        ),
        "TAGame.ProductAttribute_Painted_TA" => (
            ReplayNetworkK4ProductValueV1::Paint(read_bits(c, 31)? as u32),
            "Paint:new31".to_owned(),
        ),
        "TAGame.ProductAttribute_TitleID_TA" => {
            let (t, s) = decode_text(c)?;
            (
                ReplayNetworkK4ProductValueV1::Title(t),
                format!("Title:{s}"),
            )
        }
        "TAGame.ProductAttribute_SpecialEdition_TA" => (
            ReplayNetworkK4ProductValueV1::SpecialEdition(read_bits(c, 31)? as u32),
            "SpecialEdition:31".to_owned(),
        ),
        "TAGame.ProductAttribute_TeamEdition_TA" => (
            ReplayNetworkK4ProductValueV1::TeamEdition(read_bits(c, 31)? as u32),
            "TeamEdition:new31".to_owned(),
        ),
        other => {
            return Err(k4_error(
                "unadmitted-k4-shape",
                format!("unknown product attribute object branch {other:?}"),
            ));
        }
    };
    Ok((
        ReplayNetworkK4OnlineProductV1 {
            unknown,
            object_id: id,
            value,
        },
        shape,
    ))
}
fn online_side(
    c: &mut NetworkBitCursor<'_>,
    objects: &[String],
    name: &str,
) -> Result<(Vec<Vec<ReplayNetworkK4OnlineProductV1>>, String)> {
    let outer = read_u8(c)? as usize;
    let mut groups = Vec::new();
    groups
        .try_reserve_exact(outer)
        .map_err(|_| k4_error("invalid-length-or-count", "outer reserve"))?;
    let mut shape = format!("{name}:outer{outer}[");
    for gi in 0..outer {
        let count = read_u8(c)? as usize;
        let mut ps = Vec::new();
        ps.try_reserve_exact(count)
            .map_err(|_| k4_error("invalid-length-or-count", "product reserve"))?;
        if gi != 0 {
            shape.push(';');
        }
        shape.push_str(&format!("g{gi}:{count}("));
        for pi in 0..count {
            let (p, s) = product(c, objects)?;
            if pi != 0 {
                shape.push(',');
            }
            shape.push_str(&s);
            ps.push(p);
        }
        shape.push(')');
        groups.push(ps);
    }
    shape.push(']');
    Ok((groups, shape))
}
fn decode_one(
    c: &mut NetworkBitCursor<'_>,
    tag: ReplayNetworkAttributeTagV1,
    ctx: ReplayNetworkK4DecodeContextV1,
    objects: &[String],
) -> Result<(ReplayNetworkK4ValueV1, String)> {
    match tag {
        ReplayNetworkAttributeTagV1::CamSettings => {
            let mut v = Vec::with_capacity(7);
            for _ in 0..6 {
                v.push(read_u32(c)?);
            }
            let t = (ctx.version_major, ctx.version_minor, ctx.net_version) >= (868, 20, 0);
            if t {
                v.push(read_u32(c)?);
            }
            Ok((
                ReplayNetworkK4ValueV1::CamSettings { raw_f32_bits: v },
                format!("CamSettings:f32x{}", if t { 7 } else { 6 }),
            ))
        }
        ReplayNetworkAttributeTagV1::TeamPaint => Ok((
            ReplayNetworkK4ValueV1::TeamPaint {
                team: read_u8(c)?,
                primary_color: read_u8(c)?,
                accent_color: read_u8(c)?,
                primary_finish: read_u32(c)?,
                accent_finish: read_u32(c)?,
            },
            "TeamPaint:u8x3_u32x2".to_owned(),
        )),
        ReplayNetworkAttributeTagV1::TeamLoadout => {
            let (b, bs) = decode_loadout(c)?;
            let (o, os) = decode_loadout(c)?;
            Ok((
                ReplayNetworkK4ValueV1::TeamLoadout { blue: b, orange: o },
                format!("TeamLoadout:blue[{bs}]:orange[{os}]"),
            ))
        }
        ReplayNetworkAttributeTagV1::ClubColors => Ok((
            ReplayNetworkK4ValueV1::ClubColors {
                blue_flag: read_bits(c, 1)? != 0,
                blue_color: read_u8(c)?,
                orange_flag: read_bits(c, 1)? != 0,
                orange_color: read_u8(c)?,
            },
            "ClubColors:b1_u8_b1_u8".to_owned(),
        )),
        ReplayNetworkAttributeTagV1::Reservation => {
            let number = read_bits(c, 3)? as u8;
            let (id, is, needs) = decode_reservation_id(c, ctx)?;
            let (name, ns) = if needs {
                let (t, s) = decode_text(c)?;
                (Some(t), s)
            } else {
                (None, "none".to_owned())
            };
            let u1 = read_bits(c, 1)? != 0;
            let u2 = read_bits(c, 1)? != 0;
            let h = (ctx.version_major, ctx.version_minor, ctx.net_version) >= (868, 12, 0);
            let u3 = if h {
                Some(read_bits(c, 6)? as u8)
            } else {
                None
            };
            Ok((
                ReplayNetworkK4ValueV1::Reservation(ReplayNetworkK4ReservationV1 {
                    number,
                    player_id: id,
                    name,
                    unknown1: u1,
                    unknown2: u2,
                    unknown3: u3,
                }),
                format!("Reservation:{is}:name_{ns}:u3_{h}"),
            ))
        }
        ReplayNetworkAttributeTagV1::StatEvent => Ok((
            ReplayNetworkK4ValueV1::StatEvent {
                unknown1: read_bits(c, 1)? != 0,
                object_id: read_i32(c)?,
            },
            "StatEvent:b1_i32".to_owned(),
        )),
        ReplayNetworkAttributeTagV1::PlayerHistoryKey => Ok((
            ReplayNetworkK4ValueV1::PlayerHistoryKey(read_bits(c, 14)? as u16),
            "PlayerHistoryKey:u14".to_owned(),
        )),
        ReplayNetworkAttributeTagV1::DemolishFx => {
            let f = read_bits(c, 1)? != 0;
            let di = read_i32(c)?;
            let af = read_bits(c, 1)? != 0;
            let a = read_i32(c)?;
            let vf = read_bits(c, 1)? != 0;
            let v = read_i32(c)?;
            let (av, as_) = decode_vector(c, "attack_velocity")?;
            let (vv, vs) = decode_vector(c, "victim_velocity")?;
            Ok((
                ReplayNetworkK4ValueV1::DemolishFx {
                    custom_demo_flag: f,
                    custom_demo_id: di,
                    attacker_flag: af,
                    attacker: a,
                    victim_flag: vf,
                    victim: v,
                    attack_velocity: av,
                    victim_velocity: vv,
                },
                format!("DemolishFx:{as_}:{vs}"),
            ))
        }
        ReplayNetworkAttributeTagV1::DemolishExtended => {
            let ap = active(c)?;
            let sd = active(c)?;
            let sdb = read_bits(c, 1)? != 0;
            let ge = active(c)?;
            let a = active(c)?;
            let v = active(c)?;
            let (av, as_) = decode_vector(c, "attacker_velocity")?;
            let (vv, vs) = decode_vector(c, "victim_velocity")?;
            Ok((
                ReplayNetworkK4ValueV1::DemolishExtended {
                    attacker_pri: ap,
                    self_demo: sd,
                    self_demolish: sdb,
                    goal_explosion_owner: ge,
                    attacker: a,
                    victim: v,
                    attacker_velocity: av,
                    victim_velocity: vv,
                },
                format!("DemolishExtended:activex5:{as_}:{vs}"),
            ))
        }
        ReplayNetworkAttributeTagV1::ExtendedExplosion => {
            let f = read_bits(c, 1)? != 0;
            let a = read_i32(c)?;
            let (l, ls) = decode_vector(c, "location")?;
            let u = read_bits(c, 1)? != 0;
            let s = read_i32(c)?;
            Ok((
                ReplayNetworkK4ValueV1::ExtendedExplosion {
                    flag: f,
                    actor: a,
                    location: l,
                    unknown1: u,
                    secondary_actor: s,
                },
                format!("ExtendedExplosion:{ls}"),
            ))
        }
        ReplayNetworkAttributeTagV1::LoadoutsOnline => {
            let (b, bs) = online_side(c, objects, "blue")?;
            let (o, os) = online_side(c, objects, "orange")?;
            let u1 = read_bits(c, 1)? != 0;
            let u2 = read_bits(c, 1)? != 0;
            Ok((
                ReplayNetworkK4ValueV1::LoadoutsOnline {
                    blue: b,
                    orange: o,
                    unknown1: u1,
                    unknown2: u2,
                },
                format!("LoadoutsOnline:{bs}:{os}"),
            ))
        }
        _ => Err(k4_error(
            "unsupported-k4-tag",
            format!("attribute tag {tag:?} is not an R3.17N K4 tag"),
        )),
    }
}
pub fn decode_replay_network_k4_v1(
    bytes: &[u8],
    start_bit: u64,
    tag: ReplayNetworkAttributeTagV1,
    ctx: ReplayNetworkK4DecodeContextV1,
    objects: &[String],
) -> Result<ReplayNetworkK4DecodeV1> {
    let total = bytes
        .len()
        .checked_mul(8)
        .ok_or_else(|| k4_error("invalid-start", "network bit length overflows"))?;
    if start_bit > total as u64 {
        return Err(k4_error(
            "invalid-start",
            format!("payload start {start_bit} exceeds network length {total}"),
        ));
    }
    let start = usize::try_from(start_bit)
        .map_err(|_| k4_error("invalid-start", "start does not fit usize"))?;
    validate_context(ctx)?;
    let mut c = NetworkBitCursor::new(bytes);
    reset(&mut c, start);
    let (value, shape) = match decode_one(&mut c, tag, ctx, objects) {
        Ok(x) => x,
        Err(e) => {
            reset(&mut c, start);
            return Err(e);
        }
    };
    let end = c.position_bits() as u64;
    let width = end - start_bit;
    if !k4_admitted_groups::contains(
        tag,
        ctx.version_major,
        ctx.version_minor,
        ctx.net_version,
        ctx.is_rl_223,
        width,
        &shape,
    ) {
        reset(&mut c, start);
        return Err(k4_error(
            "unadmitted-k4-shape",
            format!(
                "exact tuple absent from R3.17N: tag={tag:?} rl223={} width={width} shape={shape}",
                ctx.is_rl_223
            ),
        ));
    }
    Ok(ReplayNetworkK4DecodeV1 {
        attribute_tag: tag,
        payload_start_bit: start_bit,
        payload_end_bit: end,
        payload_width: width,
        structural_shape: shape,
        value,
    })
}
