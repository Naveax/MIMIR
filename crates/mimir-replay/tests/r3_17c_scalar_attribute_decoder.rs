use mimir_replay::{
    ReplayNetworkAttributeTagV1, ReplayNetworkPrimitiveScalarValueV1,
    decode_replay_network_primitive_scalar_v1,
};

fn scalar_width(tag: ReplayNetworkAttributeTagV1) -> usize {
    match tag {
        ReplayNetworkAttributeTagV1::Boolean => 1,
        ReplayNetworkAttributeTagV1::Byte => 8,
        ReplayNetworkAttributeTagV1::Enum => 11,
        ReplayNetworkAttributeTagV1::Float | ReplayNetworkAttributeTagV1::Int => 32,
        ReplayNetworkAttributeTagV1::Int64 => 64,
        _ => panic!("test helper received unsupported tag"),
    }
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

fn encode_raw(start: usize, width: usize, raw: u64, trailing_bits: usize) -> Vec<u8> {
    let total_bits = start + width + trailing_bits;
    let mut bytes = vec![0u8; total_bits.div_ceil(8)];
    for bit in 0..width {
        set_bit(&mut bytes, start + bit, ((raw >> bit) & 1) != 0);
    }
    bytes
}

fn expected_value(
    tag: ReplayNetworkAttributeTagV1,
    raw: u64,
) -> ReplayNetworkPrimitiveScalarValueV1 {
    match tag {
        ReplayNetworkAttributeTagV1::Boolean => {
            ReplayNetworkPrimitiveScalarValueV1::Boolean(raw != 0)
        }
        ReplayNetworkAttributeTagV1::Byte => ReplayNetworkPrimitiveScalarValueV1::Byte(raw as u8),
        ReplayNetworkAttributeTagV1::Enum => ReplayNetworkPrimitiveScalarValueV1::Enum(raw as u16),
        ReplayNetworkAttributeTagV1::Float => {
            let raw_bits = raw as u32;
            ReplayNetworkPrimitiveScalarValueV1::Float {
                raw_bits,
                value: f32::from_bits(raw_bits),
            }
        }
        ReplayNetworkAttributeTagV1::Int => {
            ReplayNetworkPrimitiveScalarValueV1::Int((raw as u32) as i32)
        }
        ReplayNetworkAttributeTagV1::Int64 => {
            ReplayNetworkPrimitiveScalarValueV1::Int64(raw as i64)
        }
        _ => panic!("test helper received unsupported tag"),
    }
}

#[test]
fn all_admitted_tags_decode_at_aligned_and_unaligned_offsets() {
    let cases = [
        (ReplayNetworkAttributeTagV1::Boolean, 1u64),
        (ReplayNetworkAttributeTagV1::Byte, 0xa5),
        (ReplayNetworkAttributeTagV1::Enum, 0x5a3),
        (
            ReplayNetworkAttributeTagV1::Float,
            u64::from(1.5f32.to_bits()),
        ),
        (
            ReplayNetworkAttributeTagV1::Int,
            u64::from((-12345i32) as u32),
        ),
        (
            ReplayNetworkAttributeTagV1::Int64,
            (-9_876_543_210i64) as u64,
        ),
    ];

    for (tag, raw) in cases {
        let width = scalar_width(tag);
        for start in [0usize, 3usize] {
            let bytes = encode_raw(start, width, raw, 7);
            let decoded = decode_replay_network_primitive_scalar_v1(&bytes, start as u64, tag)
                .expect("admitted scalar should decode");
            assert_eq!(decoded.attribute_tag, tag);
            assert_eq!(decoded.payload_start_bit, start as u64);
            assert_eq!(decoded.payload_width, width as u8);
            assert_eq!(decoded.payload_end_bit, (start + width) as u64);
            assert_eq!(decoded.stop_bit, decoded.payload_end_bit);
            assert_eq!(decoded.value, expected_value(tag, raw));
        }
    }
}

#[test]
fn boolean_zero_and_one_are_exact() {
    for raw in [0u64, 1] {
        let bytes = encode_raw(5, 1, raw, 2);
        let decoded = decode_replay_network_primitive_scalar_v1(
            &bytes,
            5,
            ReplayNetworkAttributeTagV1::Boolean,
        )
        .unwrap();
        assert_eq!(
            decoded.value,
            ReplayNetworkPrimitiveScalarValueV1::Boolean(raw == 1)
        );
    }
}

#[test]
fn byte_and_enum_extremes_are_exact() {
    for raw in [0u64, 255] {
        let bytes = encode_raw(2, 8, raw, 4);
        let decoded =
            decode_replay_network_primitive_scalar_v1(&bytes, 2, ReplayNetworkAttributeTagV1::Byte)
                .unwrap();
        assert_eq!(
            decoded.value,
            ReplayNetworkPrimitiveScalarValueV1::Byte(raw as u8)
        );
    }

    for raw in [0u64, 2047] {
        let bytes = encode_raw(5, 11, raw, 4);
        let decoded =
            decode_replay_network_primitive_scalar_v1(&bytes, 5, ReplayNetworkAttributeTagV1::Enum)
                .unwrap();
        assert_eq!(
            decoded.value,
            ReplayNetworkPrimitiveScalarValueV1::Enum(raw as u16)
        );
    }
}

#[test]
fn float_preserves_raw_ieee_identity_including_nan_and_signed_zero() {
    let patterns = [
        0x0000_0000u32,
        0x8000_0000,
        0x7f80_0000,
        0xff80_0000,
        0x7fc0_1234,
    ];

    for raw_bits in patterns {
        let bytes = encode_raw(3, 32, u64::from(raw_bits), 5);
        let decoded = decode_replay_network_primitive_scalar_v1(
            &bytes,
            3,
            ReplayNetworkAttributeTagV1::Float,
        )
        .unwrap();
        match decoded.value {
            ReplayNetworkPrimitiveScalarValueV1::Float {
                raw_bits: raw,
                value,
            } => {
                assert_eq!(raw, raw_bits);
                assert_eq!(value.to_bits(), raw_bits);
            }
            other => panic!("unexpected scalar value: {other:?}"),
        }
    }
}

#[test]
fn int_preserves_twos_complement_boundaries() {
    for value in [i32::MIN, -1, 0, i32::MAX] {
        let raw = u64::from(value as u32);
        let bytes = encode_raw(1, 32, raw, 7);
        let decoded =
            decode_replay_network_primitive_scalar_v1(&bytes, 1, ReplayNetworkAttributeTagV1::Int)
                .unwrap();
        assert_eq!(
            decoded.value,
            ReplayNetworkPrimitiveScalarValueV1::Int(value)
        );
    }
}

#[test]
fn int64_preserves_twos_complement_boundaries() {
    for value in [i64::MIN, -1, 0, i64::MAX] {
        let raw = value as u64;
        let bytes = encode_raw(3, 64, raw, 5);
        let decoded = decode_replay_network_primitive_scalar_v1(
            &bytes,
            3,
            ReplayNetworkAttributeTagV1::Int64,
        )
        .unwrap();
        assert_eq!(
            decoded.value,
            ReplayNetworkPrimitiveScalarValueV1::Int64(value)
        );
    }
}

#[test]
fn every_admitted_tag_fails_when_truncated_by_one_bit() {
    let cases = [
        (ReplayNetworkAttributeTagV1::Boolean, 0usize, 0usize),
        (ReplayNetworkAttributeTagV1::Byte, 1, 1),
        (ReplayNetworkAttributeTagV1::Enum, 6, 2),
        (ReplayNetworkAttributeTagV1::Float, 1, 4),
        (ReplayNetworkAttributeTagV1::Int, 1, 4),
        (ReplayNetworkAttributeTagV1::Int64, 1, 8),
    ];

    for (tag, start, byte_len) in cases {
        let bytes = vec![0u8; byte_len];
        let available = byte_len * 8 - start;
        assert_eq!(available + 1, scalar_width(tag));
        assert!(decode_replay_network_primitive_scalar_v1(&bytes, start as u64, tag).is_err());
    }
}

#[test]
fn invalid_start_positions_fail_closed() {
    let bytes = [0u8];
    assert!(
        decode_replay_network_primitive_scalar_v1(&bytes, 8, ReplayNetworkAttributeTagV1::Boolean,)
            .is_err()
    );
    assert!(
        decode_replay_network_primitive_scalar_v1(&bytes, 9, ReplayNetworkAttributeTagV1::Boolean,)
            .is_err()
    );
}

#[test]
fn unsupported_compound_tags_are_rejected_before_any_payload_read() {
    for tag in [
        ReplayNetworkAttributeTagV1::RigidBody,
        ReplayNetworkAttributeTagV1::ActiveActor,
    ] {
        let error = decode_replay_network_primitive_scalar_v1(&[], u64::MAX, tag)
            .expect_err("unsupported tag must fail");
        assert!(error.to_string().contains("unsupported-tag"));
    }
}

#[test]
fn poison_bits_after_scalar_are_not_consumed() {
    let tag = ReplayNetworkAttributeTagV1::Enum;
    let start = 3usize;
    let width = scalar_width(tag);
    let raw = 0x341u64;
    let mut clean = encode_raw(start, width, raw, 13);
    let mut poisoned = clean.clone();
    for position in (start + width)..(start + width + 13) {
        set_bit(&mut poisoned, position, true);
    }

    let clean_result =
        decode_replay_network_primitive_scalar_v1(&clean, start as u64, tag).unwrap();
    let poisoned_result =
        decode_replay_network_primitive_scalar_v1(&poisoned, start as u64, tag).unwrap();
    assert_eq!(clean_result, poisoned_result);
    assert_eq!(clean_result.stop_bit, (start + width) as u64);

    // Keep the clean buffer mutable in the test so accidental helper assumptions are visible.
    set_bit(&mut clean, start + width, false);
}

#[test]
fn repeatability_is_bit_exact_even_for_nan() {
    let tag = ReplayNetworkAttributeTagV1::Float;
    let raw_bits = 0x7fc0_1234u32;
    let bytes = encode_raw(7, 32, u64::from(raw_bits), 9);
    let first = decode_replay_network_primitive_scalar_v1(&bytes, 7, tag).unwrap();
    let second = decode_replay_network_primitive_scalar_v1(&bytes, 7, tag).unwrap();
    assert_eq!(first, second);
    match first.value {
        ReplayNetworkPrimitiveScalarValueV1::Float {
            raw_bits: raw,
            value,
        } => {
            assert_eq!(raw, raw_bits);
            assert_eq!(value.to_bits(), raw_bits);
            assert!(value.is_nan());
        }
        other => panic!("unexpected scalar value: {other:?}"),
    }
}
