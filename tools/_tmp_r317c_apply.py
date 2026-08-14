from pathlib import Path

path = Path('crates/mimir-replay/src/lib.rs')
text = path.read_text(encoding='utf-8')
marker = 'fn network_existing_actor_property_error(category: &str, detail: impl Into<String>) -> MimirError {'
if text.count(marker) != 1:
    raise SystemExit(f'expected exactly one insertion marker, got {text.count(marker)}')
if 'pub enum ReplayNetworkPrimitiveScalarValueV1' in text:
    raise SystemExit('R3.17C production addition already present')

addition = r'''
/// One R3.17B-admitted primitive scalar attribute value.
///
/// Float identity preserves both the exact raw IEEE-754 bit pattern and its `f32`
/// interpretation. Equality is bit-exact for Float so NaN payloads and signed zero
/// remain deterministic evidence identities.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ReplayNetworkPrimitiveScalarValueV1 {
    Boolean(bool),
    Byte(u8),
    Enum(u16),
    Float { raw_bits: u32, value: f32 },
    Int(i32),
    Int64(i64),
}

impl PartialEq for ReplayNetworkPrimitiveScalarValueV1 {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Boolean(left), Self::Boolean(right)) => left == right,
            (Self::Byte(left), Self::Byte(right)) => left == right,
            (Self::Enum(left), Self::Enum(right)) => left == right,
            (
                Self::Float {
                    raw_bits: left_raw,
                    value: left_value,
                },
                Self::Float {
                    raw_bits: right_raw,
                    value: right_value,
                },
            ) => left_raw == right_raw && left_value.to_bits() == right_value.to_bits(),
            (Self::Int(left), Self::Int(right)) => left == right,
            (Self::Int64(left), Self::Int64(right)) => left == right,
            _ => false,
        }
    }
}

impl Eq for ReplayNetworkPrimitiveScalarValueV1 {}

/// Exact result of decoding one admitted primitive scalar payload.
///
/// This result is deliberately one-value only. `stop_bit` is exactly the first bit
/// after the scalar and does not imply permission to read another property, actor,
/// frame, or compound/spatial attribute.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkPrimitiveScalarDecodeV1 {
    pub attribute_tag: ReplayNetworkAttributeTagV1,
    pub payload_start_bit: u64,
    pub payload_end_bit: u64,
    pub payload_width: u8,
    pub value: ReplayNetworkPrimitiveScalarValueV1,
    pub stop_bit: u64,
}

/// Decode exactly one R3.17B-admitted primitive scalar payload.
///
/// The caller supplies an already resolved attribute tag and the exact
/// `payload_start_bit` returned by the existing property-header boundary. Reads use
/// the existing LSB-first network cursor, require no byte alignment, and stop after
/// exactly one scalar. Unsupported/compound tags are rejected before any payload read.
pub fn decode_replay_network_primitive_scalar_v1(
    network_bytes: &[u8],
    payload_start_bit: u64,
    attribute_tag: ReplayNetworkAttributeTagV1,
) -> Result<ReplayNetworkPrimitiveScalarDecodeV1> {
    let payload_width = match attribute_tag {
        ReplayNetworkAttributeTagV1::Boolean => 1,
        ReplayNetworkAttributeTagV1::Byte => 8,
        ReplayNetworkAttributeTagV1::Enum => 11,
        ReplayNetworkAttributeTagV1::Float | ReplayNetworkAttributeTagV1::Int => 32,
        ReplayNetworkAttributeTagV1::Int64 => 64,
        _ => {
            return Err(network_primitive_scalar_error(
                "unsupported-tag",
                format!("attribute tag {attribute_tag:?} is not an admitted primitive scalar"),
            ));
        }
    };

    let start = usize::try_from(payload_start_bit).map_err(|_| {
        network_primitive_scalar_error(
            "invalid-position",
            format!("payload start bit {payload_start_bit} does not fit usize"),
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_primitive_scalar_error(
            "invalid-length",
            "network bit length overflows usize",
        )
    })?;
    if start > total_bits {
        return Err(network_primitive_scalar_error(
            "invalid-position",
            format!(
                "payload start bit {payload_start_bit} exceeds network bit length {total_bits}"
            ),
        ));
    }

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;
    let raw = cursor.read_bits_le(usize::from(payload_width))?;

    let value = match attribute_tag {
        ReplayNetworkAttributeTagV1::Boolean => {
            ReplayNetworkPrimitiveScalarValueV1::Boolean(raw != 0)
        }
        ReplayNetworkAttributeTagV1::Byte => ReplayNetworkPrimitiveScalarValueV1::Byte(
            u8::try_from(raw).map_err(|_| {
                network_primitive_scalar_error(
                    "invalid-value",
                    format!("8-bit scalar value {raw} does not fit u8"),
                )
            })?,
        ),
        ReplayNetworkAttributeTagV1::Enum => ReplayNetworkPrimitiveScalarValueV1::Enum(
            u16::try_from(raw).map_err(|_| {
                network_primitive_scalar_error(
                    "invalid-value",
                    format!("11-bit scalar value {raw} does not fit u16"),
                )
            })?,
        ),
        ReplayNetworkAttributeTagV1::Float => {
            let raw_bits = u32::try_from(raw).map_err(|_| {
                network_primitive_scalar_error(
                    "invalid-value",
                    format!("32-bit float value {raw} does not fit u32"),
                )
            })?;
            ReplayNetworkPrimitiveScalarValueV1::Float {
                raw_bits,
                value: f32::from_bits(raw_bits),
            }
        }
        ReplayNetworkAttributeTagV1::Int => {
            let raw_bits = u32::try_from(raw).map_err(|_| {
                network_primitive_scalar_error(
                    "invalid-value",
                    format!("32-bit integer value {raw} does not fit u32"),
                )
            })?;
            ReplayNetworkPrimitiveScalarValueV1::Int(raw_bits as i32)
        }
        ReplayNetworkAttributeTagV1::Int64 => ReplayNetworkPrimitiveScalarValueV1::Int64(raw as i64),
        _ => unreachable!("unsupported tags return before payload read"),
    };

    let payload_end_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        network_primitive_scalar_error(
            "invalid-position",
            format!(
                "payload end bit {} does not fit u64",
                cursor.position_bits()
            ),
        )
    })?;

    Ok(ReplayNetworkPrimitiveScalarDecodeV1 {
        attribute_tag,
        payload_start_bit,
        payload_end_bit,
        payload_width,
        value,
        stop_bit: payload_end_bit,
    })
}

fn network_primitive_scalar_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay primitive scalar attribute error: {category}: {}",
        detail.into()
    ))
}

'''

path.write_text(text.replace(marker, addition + marker), encoding='utf-8', newline='\n')
print('R3_17C_PRODUCTION_INSERT=PASS')
