from pathlib import Path

lib_path = Path("crates/mimir-replay/src/lib.rs")
test_path = Path("crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs")

text = lib_path.read_text(encoding="utf-8")
if "pub struct ReplayNetworkK2DecodeContextV1" in text:
    raise SystemExit("R3.17G K2 implementation already present")

marker = "/// This result is deliberately one-value only. `stop_bit` is exactly the first bit\n"
if marker not in text:
    raise SystemExit("R3.17G insertion marker not found")

insert = r'''
/// Caller-resolved context for one evidence-admitted K2 payload decode.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK2DecodeContextV1 {
    pub net_version: i32,
    pub is_rl_223: bool,
}

/// Wire encoding identity retained for an admitted length-prefixed network string.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ReplayNetworkTextEncodingV1 {
    Empty,
    Windows1252,
    Utf16Le,
}

/// One decoded network text value plus the signed length that selected its wire branch.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkTextV1 {
    pub value: String,
    pub declared_length: i32,
    pub encoding: ReplayNetworkTextEncodingV1,
}

/// Evidence-admitted remote identity variants for one direct K2 value.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkUniqueIdRemoteV1 {
    Steam {
        online_id: u64,
    },
    PlayStation {
        name: String,
        unknown: Vec<u8>,
        online_id: u64,
    },
    PsyNet {
        online_id: u64,
    },
    Epic {
        account_id: ReplayNetworkTextV1,
    },
}

/// One evidence-admitted network unique id.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkUniqueIdV1 {
    pub system_id: u8,
    pub remote_id: ReplayNetworkUniqueIdRemoteV1,
    pub local_id: u8,
}

/// Semantic value returned by the direct one-value K2 decoder.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkK2ValueV1 {
    ActiveActor { active: bool, actor: i32 },
    String(ReplayNetworkTextV1),
    QWordStringQWord(u64),
    QWordStringText(ReplayNetworkTextV1),
    UniqueId(ReplayNetworkUniqueIdV1),
    PartyLeader(ReplayNetworkUniqueIdV1),
}

/// Exactly one already-resolved evidence-admitted K2 payload decode.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK2DecodeV1 {
    pub attribute_tag: ReplayNetworkAttributeTagV1,
    pub payload_start_bit: u64,
    pub payload_end_bit: u64,
    pub payload_width: u64,
    pub value: ReplayNetworkK2ValueV1,
}

fn replay_network_k2_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network k2 error: {category}: {}",
        detail.into()
    ))
}

fn network_k2_read_u8(cursor: &mut NetworkBitCursor<'_>) -> Result<u8> {
    cursor.read_bits_le(8).map(|value| value as u8)
}

fn network_k2_read_u64(cursor: &mut NetworkBitCursor<'_>) -> Result<u64> {
    cursor.read_bits_le(64)
}

fn network_k2_read_bytes(cursor: &mut NetworkBitCursor<'_>, count: usize) -> Result<Vec<u8>> {
    let required_bits = count.checked_mul(8).ok_or_else(|| {
        replay_network_k2_error("invalid-text-length", "byte length overflows bit width")
    })?;
    if cursor.remaining_bits() < required_bits {
        return Err(replay_network_k2_error(
            "insufficient-bits",
            format!(
                "need {required_bits} content bits at position {}, but only {} remain",
                cursor.position_bits(),
                cursor.remaining_bits()
            ),
        ));
    }

    let mut output = Vec::new();
    output.try_reserve_exact(count).map_err(|_| {
        replay_network_k2_error(
            "invalid-text-length",
            format!("unable to reserve {count} decoded bytes"),
        )
    })?;
    for _ in 0..count {
        output.push(network_k2_read_u8(cursor)?);
    }
    Ok(output)
}

fn decode_network_windows1252(bytes: &[u8]) -> String {
    let mut output = String::with_capacity(bytes.len());
    for byte in bytes {
        let character = match *byte {
            0x80 => '\u{20ac}',
            0x81 => '\u{0081}',
            0x82 => '\u{201a}',
            0x83 => '\u{0192}',
            0x84 => '\u{201e}',
            0x85 => '\u{2026}',
            0x86 => '\u{2020}',
            0x87 => '\u{2021}',
            0x88 => '\u{02c6}',
            0x89 => '\u{2030}',
            0x8a => '\u{0160}',
            0x8b => '\u{2039}',
            0x8c => '\u{0152}',
            0x8d => '\u{008d}',
            0x8e => '\u{017d}',
            0x8f => '\u{008f}',
            0x90 => '\u{0090}',
            0x91 => '\u{2018}',
            0x92 => '\u{2019}',
            0x93 => '\u{201c}',
            0x94 => '\u{201d}',
            0x95 => '\u{2022}',
            0x96 => '\u{2013}',
            0x97 => '\u{2014}',
            0x98 => '\u{02dc}',
            0x99 => '\u{2122}',
            0x9a => '\u{0161}',
            0x9b => '\u{203a}',
            0x9c => '\u{0153}',
            0x9d => '\u{009d}',
            0x9e => '\u{017e}',
            0x9f => '\u{0178}',
            value => char::from_u32(u32::from(value)).expect("u8 is always a Unicode scalar"),
        };
        output.push(character);
    }
    output
}

fn decode_network_text_v1(cursor: &mut NetworkBitCursor<'_>) -> Result<ReplayNetworkTextV1> {
    let declared_length = cursor.read_bits_le(32)? as u32 as i32;
    if declared_length == 0 {
        return Ok(ReplayNetworkTextV1 {
            value: String::new(),
            declared_length,
            encoding: ReplayNetworkTextEncodingV1::Empty,
        });
    }

    if declared_length > 0 {
        let byte_count = usize::try_from(declared_length).map_err(|_| {
            replay_network_k2_error(
                "invalid-text-length",
                format!("positive text length {declared_length} does not fit usize"),
            )
        })?;
        let bytes = network_k2_read_bytes(cursor, byte_count)?;
        let content = &bytes[..byte_count - 1];
        return Ok(ReplayNetworkTextV1 {
            value: decode_network_windows1252(content),
            declared_length,
            encoding: ReplayNetworkTextEncodingV1::Windows1252,
        });
    }

    if declared_length == i32::MIN {
        return Err(replay_network_k2_error(
            "invalid-text-length",
            "i32::MIN cannot be negated for UTF-16 byte length",
        ));
    }

    let code_unit_count = usize::try_from(-declared_length).map_err(|_| {
        replay_network_k2_error(
            "invalid-text-length",
            format!("UTF-16 code-unit length {declared_length} does not fit usize"),
        )
    })?;
    let byte_count = code_unit_count.checked_mul(2).ok_or_else(|| {
        replay_network_k2_error(
            "invalid-text-length",
            format!("UTF-16 byte length overflows for {declared_length}"),
        )
    })?;
    let bytes = network_k2_read_bytes(cursor, byte_count)?;
    let content = &bytes[..byte_count - 2];
    let mut units = Vec::new();
    units.try_reserve_exact(content.len() / 2).map_err(|_| {
        replay_network_k2_error(
            "invalid-text-length",
            format!("unable to reserve {} UTF-16 code units", content.len() / 2),
        )
    })?;
    for chunk in content.chunks_exact(2) {
        units.push(u16::from_le_bytes([chunk[0], chunk[1]]));
    }

    Ok(ReplayNetworkTextV1 {
        value: String::from_utf16_lossy(&units),
        declared_length,
        encoding: ReplayNetworkTextEncodingV1::Utf16Le,
    })
}

fn decode_network_unique_id_v1(
    cursor: &mut NetworkBitCursor<'_>,
    context: ReplayNetworkK2DecodeContextV1,
) -> Result<ReplayNetworkUniqueIdV1> {
    if context.net_version != 10 {
        return Err(replay_network_k2_error(
            "unadmitted-context",
            format!(
                "UniqueId requires net_version 10, got {}",
                context.net_version
            ),
        ));
    }

    let system_id = network_k2_read_u8(cursor)?;
    let remote_id = match system_id {
        1 => ReplayNetworkUniqueIdRemoteV1::Steam {
            online_id: network_k2_read_u64(cursor)?,
        },
        2 => {
            if !context.is_rl_223 {
                return Err(replay_network_k2_error(
                    "unadmitted-context",
                    "PlayStation UniqueId was observed only in RL223 context",
                ));
            }
            let name_bytes = network_k2_read_bytes(cursor, 16)?;
            let name_end = name_bytes
                .iter()
                .position(|byte| *byte == 0)
                .unwrap_or(name_bytes.len());
            let name = decode_network_windows1252(&name_bytes[..name_end]);
            let unknown = network_k2_read_bytes(cursor, 16)?;
            let online_id = network_k2_read_u64(cursor)?;
            ReplayNetworkUniqueIdRemoteV1::PlayStation {
                name,
                unknown,
                online_id,
            }
        }
        7 => {
            if !context.is_rl_223 {
                return Err(replay_network_k2_error(
                    "unadmitted-context",
                    "PsyNet UniqueId was observed only in RL223 context",
                ));
            }
            ReplayNetworkUniqueIdRemoteV1::PsyNet {
                online_id: network_k2_read_u64(cursor)?,
            }
        }
        11 => {
            let account_id = decode_network_text_v1(cursor)?;
            if account_id.encoding != ReplayNetworkTextEncodingV1::Windows1252
                || account_id.declared_length != 33
            {
                return Err(replay_network_k2_error(
                    "unadmitted-k2-shape",
                    format!(
                        "Epic UniqueId requires Windows-1252 declared length 33, got {:?} / {}",
                        account_id.encoding, account_id.declared_length
                    ),
                ));
            }
            ReplayNetworkUniqueIdRemoteV1::Epic { account_id }
        }
        value => {
            return Err(replay_network_k2_error(
                "unadmitted-k2-shape",
                format!("UniqueId system id {value} is not admitted by R3.17F"),
            ));
        }
    };
    let local_id = network_k2_read_u8(cursor)?;
    Ok(ReplayNetworkUniqueIdV1 {
        system_id,
        remote_id,
        local_id,
    })
}

/// Decode exactly one already-resolved R3.17F-admitted K2 payload.
///
/// This API is intentionally stateless: it receives the exact payload start and returns
/// the first bit after one K2 value. It does not continue a property loop or mutate actor state.
pub fn decode_replay_network_k2_v1(
    network_bytes: &[u8],
    payload_start_bit: u64,
    attribute_tag: ReplayNetworkAttributeTagV1,
    context: ReplayNetworkK2DecodeContextV1,
) -> Result<ReplayNetworkK2DecodeV1> {
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        replay_network_k2_error("invalid-start", "network bit length overflows usize")
    })?;
    let total_bits_u64 = u64::try_from(total_bits).map_err(|_| {
        replay_network_k2_error("invalid-start", "network bit length does not fit u64")
    })?;
    if payload_start_bit > total_bits_u64 {
        return Err(replay_network_k2_error(
            "invalid-start",
            format!(
                "payload start {payload_start_bit} exceeds network length {total_bits_u64} bits"
            ),
        ));
    }
    let start = usize::try_from(payload_start_bit).map_err(|_| {
        replay_network_k2_error(
            "invalid-start",
            format!("payload start {payload_start_bit} does not fit usize"),
        )
    })?;

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;
    let decoded = (|| -> Result<ReplayNetworkK2ValueV1> {
        match attribute_tag {
            ReplayNetworkAttributeTagV1::ActiveActor => {
                let active = cursor.read_bit()?;
                let actor = cursor.read_bits_le(32)? as u32 as i32;
                Ok(ReplayNetworkK2ValueV1::ActiveActor { active, actor })
            }
            ReplayNetworkAttributeTagV1::String => {
                decode_network_text_v1(&mut cursor).map(ReplayNetworkK2ValueV1::String)
            }
            ReplayNetworkAttributeTagV1::QWordString => {
                if context.is_rl_223 {
                    let value = decode_network_text_v1(&mut cursor)?;
                    if value.encoding != ReplayNetworkTextEncodingV1::Windows1252
                        || value.declared_length <= 0
                    {
                        return Err(replay_network_k2_error(
                            "unadmitted-k2-shape",
                            format!(
                                "RL223 QWordString requires positive Windows-1252 text, got {:?} / {}",
                                value.encoding, value.declared_length
                            ),
                        ));
                    }
                    Ok(ReplayNetworkK2ValueV1::QWordStringText(value))
                } else {
                    network_k2_read_u64(&mut cursor)
                        .map(ReplayNetworkK2ValueV1::QWordStringQWord)
                }
            }
            ReplayNetworkAttributeTagV1::UniqueId => {
                decode_network_unique_id_v1(&mut cursor, context)
                    .map(ReplayNetworkK2ValueV1::UniqueId)
            }
            ReplayNetworkAttributeTagV1::PartyLeader => {
                if context.net_version != 10 || !context.is_rl_223 {
                    return Err(replay_network_k2_error(
                        "unadmitted-context",
                        format!(
                            "PartyLeader requires net_version 10 and RL223 context, got {} / {}",
                            context.net_version, context.is_rl_223
                        ),
                    ));
                }
                let unique = decode_network_unique_id_v1(&mut cursor, context)?;
                if !matches!(unique.remote_id, ReplayNetworkUniqueIdRemoteV1::Epic { .. }) {
                    return Err(replay_network_k2_error(
                        "unadmitted-k2-shape",
                        "PartyLeader admits only Some(Epic declared=33)",
                    ));
                }
                Ok(ReplayNetworkK2ValueV1::PartyLeader(unique))
            }
            _ => Err(replay_network_k2_error(
                "unsupported-k2-tag",
                format!("attribute tag {attribute_tag:?} is not an admitted K2 tag"),
            )),
        }
    })();

    let value = match decoded {
        Ok(value) => value,
        Err(error) => {
            cursor.bit_position = start;
            return Err(error);
        }
    };
    let payload_end_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        cursor.bit_position = start;
        replay_network_k2_error("invalid-start", "decoded end bit does not fit u64")
    })?;
    let payload_width = payload_end_bit.checked_sub(payload_start_bit).ok_or_else(|| {
        cursor.bit_position = start;
        replay_network_k2_error("invalid-start", "decoded end bit precedes payload start")
    })?;

    Ok(ReplayNetworkK2DecodeV1 {
        attribute_tag,
        payload_start_bit,
        payload_end_bit,
        payload_width,
        value,
    })
}

'''

text = text.replace(marker, insert + marker, 1)
lib_path.write_text(text, encoding="utf-8", newline="\n")

test_content = r'''use mimir_replay::{
    ReplayNetworkAttributeTagV1, ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1,
    ReplayNetworkTextEncodingV1, ReplayNetworkTextV1, ReplayNetworkUniqueIdRemoteV1,
    decode_replay_network_k2_v1,
};

fn push_bits(bytes: &mut Vec<u8>, bit: &mut usize, value: u64, width: usize) {
    for offset in 0..width {
        let position = *bit + offset;
        let byte_index = position / 8;
        let bit_index = position % 8;
        while bytes.len() <= byte_index {
            bytes.push(0);
        }
        if ((value >> offset) & 1) != 0 {
            bytes[byte_index] |= 1 << bit_index;
        }
    }
    *bit += width;
}

fn push_u8(bytes: &mut Vec<u8>, bit: &mut usize, value: u8) {
    push_bits(bytes, bit, u64::from(value), 8);
}

fn push_u16(bytes: &mut Vec<u8>, bit: &mut usize, value: u16) {
    push_bits(bytes, bit, u64::from(value), 16);
}

fn push_i32(bytes: &mut Vec<u8>, bit: &mut usize, value: i32) {
    push_bits(bytes, bit, u64::from(value as u32), 32);
}

fn push_u64(bytes: &mut Vec<u8>, bit: &mut usize, value: u64) {
    push_bits(bytes, bit, value, 64);
}

fn push_windows_text(bytes: &mut Vec<u8>, bit: &mut usize, content: &[u8], terminator: u8) {
    push_i32(bytes, bit, i32::try_from(content.len() + 1).unwrap());
    for value in content {
        push_u8(bytes, bit, *value);
    }
    push_u8(bytes, bit, terminator);
}

fn push_utf16_text(bytes: &mut Vec<u8>, bit: &mut usize, content: &[u16], terminator: u16) {
    let declared = -i32::try_from(content.len() + 1).unwrap();
    push_i32(bytes, bit, declared);
    for value in content {
        push_u16(bytes, bit, *value);
    }
    push_u16(bytes, bit, terminator);
}

fn new_bits(start: usize) -> (Vec<u8>, usize) {
    (vec![0; start.div_ceil(8)], start)
}

fn ctx(net_version: i32, is_rl_223: bool) -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version,
        is_rl_223,
    }
}

fn assert_error_contains(error: mimir_core::MimirError, needle: &str) {
    let text = error.to_string();
    assert!(text.contains(needle), "expected {needle:?} in {text:?}");
}

#[test]
fn active_actor_decodes_exact_33_bits_at_unaligned_starts() {
    let cases = [
        (1usize, false, 0i32),
        (3usize, true, 42i32),
        (5usize, false, -1i32),
        (7usize, true, -123_456i32),
    ];
    for (start, active, actor) in cases {
        let (mut bytes, mut bit) = new_bits(start);
        push_bits(&mut bytes, &mut bit, u64::from(active), 1);
        push_i32(&mut bytes, &mut bit, actor);
        let decoded = decode_replay_network_k2_v1(
            &bytes,
            start as u64,
            ReplayNetworkAttributeTagV1::ActiveActor,
            ctx(10, true),
        )
        .unwrap();
        assert_eq!(decoded.payload_end_bit, bit as u64);
        assert_eq!(decoded.payload_width, 33);
        assert_eq!(
            decoded.value,
            ReplayNetworkK2ValueV1::ActiveActor { active, actor }
        );
    }

    let error = decode_replay_network_k2_v1(
        &[0; 4],
        0,
        ReplayNetworkAttributeTagV1::ActiveActor,
        ctx(10, false),
    )
    .unwrap_err();
    assert_error_contains(error, "insufficient-bits");
}

#[test]
fn string_decodes_empty_windows1252_and_utf16_with_exact_shape_identity() {
    let start = 3usize;
    let (mut empty_bytes, mut empty_bit) = new_bits(start);
    push_i32(&mut empty_bytes, &mut empty_bit, 0);
    let empty = decode_replay_network_k2_v1(
        &empty_bytes,
        start as u64,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap();
    assert_eq!(empty.payload_end_bit, empty_bit as u64);
    assert_eq!(
        empty.value,
        ReplayNetworkK2ValueV1::String(ReplayNetworkTextV1 {
            value: String::new(),
            declared_length: 0,
            encoding: ReplayNetworkTextEncodingV1::Empty,
        })
    );

    let (mut windows_bytes, mut windows_bit) = new_bits(5);
    push_windows_text(&mut windows_bytes, &mut windows_bit, &[b'A', 0x80, b'Z'], 0x7f);
    let windows = decode_replay_network_k2_v1(
        &windows_bytes,
        5,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(windows.payload_end_bit, windows_bit as u64);
    assert_eq!(
        windows.value,
        ReplayNetworkK2ValueV1::String(ReplayNetworkTextV1 {
            value: "A€Z".to_owned(),
            declared_length: 4,
            encoding: ReplayNetworkTextEncodingV1::Windows1252,
        })
    );

    let (mut utf16_bytes, mut utf16_bit) = new_bits(7);
    push_utf16_text(&mut utf16_bytes, &mut utf16_bit, &[0x0041, 0xd800, 0x0042], 0x1234);
    let utf16 = decode_replay_network_k2_v1(
        &utf16_bytes,
        7,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap();
    assert_eq!(utf16.payload_end_bit, utf16_bit as u64);
    assert_eq!(
        utf16.value,
        ReplayNetworkK2ValueV1::String(ReplayNetworkTextV1 {
            value: "A�B".to_owned(),
            declared_length: -4,
            encoding: ReplayNetworkTextEncodingV1::Utf16Le,
        })
    );
}

#[test]
fn string_rejects_invalid_length_and_truncation() {
    let (mut min_bytes, mut min_bit) = new_bits(0);
    push_i32(&mut min_bytes, &mut min_bit, i32::MIN);
    let error = decode_replay_network_k2_v1(
        &min_bytes,
        0,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap_err();
    assert_error_contains(error, "invalid-text-length");

    let error = decode_replay_network_k2_v1(
        &[0; 3],
        0,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap_err();
    assert_error_contains(error, "insufficient-bits");

    let mut truncated = vec![0; 7];
    let mut bit = 0usize;
    push_i32(&mut truncated, &mut bit, 4);
    let error = decode_replay_network_k2_v1(
        &truncated,
        0,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap_err();
    assert_error_contains(error, "insufficient-bits");
}

#[test]
fn qword_string_obeys_rl223_gate() {
    let (mut legacy_bytes, mut legacy_bit) = new_bits(3);
    push_u64(&mut legacy_bytes, &mut legacy_bit, 0x0123_4567_89ab_cdef);
    let legacy = decode_replay_network_k2_v1(
        &legacy_bytes,
        3,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, false),
    )
    .unwrap();
    assert_eq!(legacy.payload_end_bit, legacy_bit as u64);
    assert_eq!(
        legacy.value,
        ReplayNetworkK2ValueV1::QWordStringQWord(0x0123_4567_89ab_cdef)
    );

    let (mut text_bytes, mut text_bit) = new_bits(1);
    push_windows_text(&mut text_bytes, &mut text_bit, b"rl223", 0xff);
    let text = decode_replay_network_k2_v1(
        &text_bytes,
        1,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(text.payload_end_bit, text_bit as u64);
    assert!(matches!(
        text.value,
        ReplayNetworkK2ValueV1::QWordStringText(ReplayNetworkTextV1 {
            encoding: ReplayNetworkTextEncodingV1::Windows1252,
            declared_length: 6,
            ..
        })
    ));

    let (mut empty_bytes, mut empty_bit) = new_bits(0);
    push_i32(&mut empty_bytes, &mut empty_bit, 0);
    let error = decode_replay_network_k2_v1(
        &empty_bytes,
        0,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");

    let (mut utf16_bytes, mut utf16_bit) = new_bits(0);
    push_utf16_text(&mut utf16_bytes, &mut utf16_bit, &[0x41], 0);
    let error = decode_replay_network_k2_v1(
        &utf16_bytes,
        0,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");
}

fn push_epic(bytes: &mut Vec<u8>, bit: &mut usize, local_id: u8) {
    push_u8(bytes, bit, 11);
    push_windows_text(bytes, bit, &[b'E'; 32], 0x55);
    push_u8(bytes, bit, local_id);
}

#[test]
fn unique_id_decodes_all_admitted_systems() {
    let (mut steam_bytes, mut steam_bit) = new_bits(1);
    push_u8(&mut steam_bytes, &mut steam_bit, 1);
    push_u64(&mut steam_bytes, &mut steam_bit, 0x1111_2222_3333_4444);
    push_u8(&mut steam_bytes, &mut steam_bit, 7);
    for rl223 in [false, true] {
        let steam = decode_replay_network_k2_v1(
            &steam_bytes,
            1,
            ReplayNetworkAttributeTagV1::UniqueId,
            ctx(10, rl223),
        )
        .unwrap();
        assert_eq!(steam.payload_end_bit, steam_bit as u64);
        assert!(matches!(
            steam.value,
            ReplayNetworkK2ValueV1::UniqueId(mimir_replay::ReplayNetworkUniqueIdV1 {
                system_id: 1,
                remote_id: ReplayNetworkUniqueIdRemoteV1::Steam {
                    online_id: 0x1111_2222_3333_4444
                },
                local_id: 7,
            })
        ));
    }

    let (mut ps_bytes, mut ps_bit) = new_bits(3);
    push_u8(&mut ps_bytes, &mut ps_bit, 2);
    let mut name = [0u8; 16];
    name[..6].copy_from_slice(b"Player");
    for value in name {
        push_u8(&mut ps_bytes, &mut ps_bit, value);
    }
    for _ in 0..16 {
        push_u8(&mut ps_bytes, &mut ps_bit, 0xa5);
    }
    push_u64(&mut ps_bytes, &mut ps_bit, 0x1234);
    push_u8(&mut ps_bytes, &mut ps_bit, 9);
    let ps = decode_replay_network_k2_v1(
        &ps_bytes,
        3,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(ps.payload_width, 336);
    assert_eq!(ps.payload_end_bit, ps_bit as u64);
    assert!(matches!(
        ps.value,
        ReplayNetworkK2ValueV1::UniqueId(mimir_replay::ReplayNetworkUniqueIdV1 {
            system_id: 2,
            remote_id: ReplayNetworkUniqueIdRemoteV1::PlayStation { ref name, ref unknown, online_id: 0x1234 },
            local_id: 9,
        }) if name == "Player" && unknown == &vec![0xa5; 16]
    ));

    let (mut psy_bytes, mut psy_bit) = new_bits(5);
    push_u8(&mut psy_bytes, &mut psy_bit, 7);
    push_u64(&mut psy_bytes, &mut psy_bit, 0xaabb_ccdd_eeff_0011);
    push_u8(&mut psy_bytes, &mut psy_bit, 3);
    let psy = decode_replay_network_k2_v1(
        &psy_bytes,
        5,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(psy.payload_width, 80);
    assert_eq!(psy.payload_end_bit, psy_bit as u64);
    assert!(matches!(
        psy.value,
        ReplayNetworkK2ValueV1::UniqueId(mimir_replay::ReplayNetworkUniqueIdV1 {
            system_id: 7,
            remote_id: ReplayNetworkUniqueIdRemoteV1::PsyNet { online_id: 0xaabb_ccdd_eeff_0011 },
            local_id: 3,
        })
    ));

    let (mut epic_bytes, mut epic_bit) = new_bits(7);
    push_epic(&mut epic_bytes, &mut epic_bit, 4);
    for rl223 in [false, true] {
        let epic = decode_replay_network_k2_v1(
            &epic_bytes,
            7,
            ReplayNetworkAttributeTagV1::UniqueId,
            ctx(10, rl223),
        )
        .unwrap();
        assert_eq!(epic.payload_width, 312);
        assert_eq!(epic.payload_end_bit, epic_bit as u64);
        assert!(matches!(
            epic.value,
            ReplayNetworkK2ValueV1::UniqueId(mimir_replay::ReplayNetworkUniqueIdV1 {
                system_id: 11,
                remote_id: ReplayNetworkUniqueIdRemoteV1::Epic {
                    account_id: ReplayNetworkTextV1 {
                        declared_length: 33,
                        encoding: ReplayNetworkTextEncodingV1::Windows1252,
                        ..
                    }
                },
                local_id: 4,
            })
        ));
    }
}

#[test]
fn unique_id_rejects_unadmitted_contexts_systems_and_epic_shape() {
    let error = decode_replay_network_k2_v1(
        &[1; 16],
        0,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(9, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-context");

    for system_id in [0u8, 4, 5, 6, 99] {
        let (mut bytes, mut bit) = new_bits(0);
        push_u8(&mut bytes, &mut bit, system_id);
        let error = decode_replay_network_k2_v1(
            &bytes,
            0,
            ReplayNetworkAttributeTagV1::UniqueId,
            ctx(10, true),
        )
        .unwrap_err();
        assert_error_contains(error, "unadmitted-k2-shape");
    }

    for system_id in [2u8, 7] {
        let (mut bytes, mut bit) = new_bits(0);
        push_u8(&mut bytes, &mut bit, system_id);
        let error = decode_replay_network_k2_v1(
            &bytes,
            0,
            ReplayNetworkAttributeTagV1::UniqueId,
            ctx(10, false),
        )
        .unwrap_err();
        assert_error_contains(error, "unadmitted-context");
    }

    let (mut epic_bytes, mut epic_bit) = new_bits(0);
    push_u8(&mut epic_bytes, &mut epic_bit, 11);
    push_windows_text(&mut epic_bytes, &mut epic_bit, &[b'X'; 31], 0);
    let error = decode_replay_network_k2_v1(
        &epic_bytes,
        0,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");
}

#[test]
fn party_leader_admits_only_rl223_epic_declared_33() {
    let (mut epic_bytes, mut epic_bit) = new_bits(3);
    push_epic(&mut epic_bytes, &mut epic_bit, 8);
    let decoded = decode_replay_network_k2_v1(
        &epic_bytes,
        3,
        ReplayNetworkAttributeTagV1::PartyLeader,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(decoded.payload_width, 312);
    assert_eq!(decoded.payload_end_bit, epic_bit as u64);
    assert!(matches!(
        decoded.value,
        ReplayNetworkK2ValueV1::PartyLeader(mimir_replay::ReplayNetworkUniqueIdV1 {
            system_id: 11,
            remote_id: ReplayNetworkUniqueIdRemoteV1::Epic { .. },
            local_id: 8,
        })
    ));

    let error = decode_replay_network_k2_v1(
        &[0],
        0,
        ReplayNetworkAttributeTagV1::PartyLeader,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");

    let (mut steam_bytes, mut steam_bit) = new_bits(0);
    push_u8(&mut steam_bytes, &mut steam_bit, 1);
    push_u64(&mut steam_bytes, &mut steam_bit, 7);
    push_u8(&mut steam_bytes, &mut steam_bit, 1);
    let error = decode_replay_network_k2_v1(
        &steam_bytes,
        0,
        ReplayNetworkAttributeTagV1::PartyLeader,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");

    for context in [ctx(10, false), ctx(9, true)] {
        let error = decode_replay_network_k2_v1(
            &epic_bytes,
            3,
            ReplayNetworkAttributeTagV1::PartyLeader,
            context,
        )
        .unwrap_err();
        assert_error_contains(error, "unadmitted-context");
    }
}

#[test]
fn k2_decoder_rejects_non_k2_tag_and_invalid_start() {
    let error = decode_replay_network_k2_v1(
        &[0xff; 8],
        0,
        ReplayNetworkAttributeTagV1::Boolean,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unsupported-k2-tag");

    let error = decode_replay_network_k2_v1(
        &[0xff],
        9,
        ReplayNetworkAttributeTagV1::ActiveActor,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "invalid-start");
}
'''

test_path.write_text(test_content, encoding="utf-8", newline="\n")
print("R3.17G patch applied")
