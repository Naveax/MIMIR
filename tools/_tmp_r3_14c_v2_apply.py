from __future__ import annotations

from pathlib import Path

SOURCE = Path("crates/mimir-replay/src/lib.rs")

PRIMITIVE_ANCHOR = "use std::collections::{BTreeMap, BTreeSet};\nuse std::path::PathBuf;\n"
TEST_ANCHOR = "#[cfg(test)]\nmod tests {\n    use super::*;\n"

PRIMITIVES = r'''

/// Private LSB-first cursor for Rocket League replay network payload bits.
///
/// R3.14C deliberately keeps this primitive internal. Replay-envelope semantics
/// remain closed until R3.14D.
#[cfg_attr(not(test), allow(dead_code))]
#[derive(Debug, Clone)]
struct NetworkBitCursor<'a> {
    bytes: &'a [u8],
    bit_position: usize,
}

#[cfg_attr(not(test), allow(dead_code))]
impl<'a> NetworkBitCursor<'a> {
    fn new(bytes: &'a [u8]) -> Self {
        Self {
            bytes,
            bit_position: 0,
        }
    }

    fn position_bits(&self) -> usize {
        self.bit_position
    }

    fn remaining_bits(&self) -> usize {
        self.bytes
            .len()
            .saturating_mul(8)
            .saturating_sub(self.bit_position)
    }

    fn read_bit(&mut self) -> Result<bool> {
        let total_bits = self.bytes.len().checked_mul(8).ok_or_else(|| {
            network_bit_error("invalid-length", "network bit length overflows usize")
        })?;
        if self.bit_position >= total_bits {
            return Err(network_bit_error(
                "insufficient-bits",
                format!(
                    "need 1 bit at position {}, but no bits remain",
                    self.bit_position
                ),
            ));
        }

        let position = self.bit_position;
        let byte_index = position / 8;
        let bit_index = position % 8;
        let bit = ((self.bytes[byte_index] >> bit_index) & 1) != 0;
        self.bit_position = position + 1;
        Ok(bit)
    }

    fn read_bits_le(&mut self, width: usize) -> Result<u64> {
        if width > 64 {
            return Err(network_bit_error(
                "invalid-width",
                format!("bit width {width} exceeds 64"),
            ));
        }

        let start = self.bit_position;
        let end = start.checked_add(width).ok_or_else(|| {
            network_bit_error("invalid-position", "bit position addition overflows usize")
        })?;
        let total_bits = self.bytes.len().checked_mul(8).ok_or_else(|| {
            network_bit_error("invalid-length", "network bit length overflows usize")
        })?;
        if end > total_bits {
            return Err(network_bit_error(
                "insufficient-bits",
                format!(
                    "need {width} bits at position {start}, but only {} remain",
                    total_bits.saturating_sub(start)
                ),
            ));
        }

        let mut value = 0u64;
        for output_bit in 0..width {
            let position = start + output_bit;
            let byte = self.bytes[position / 8];
            let bit = (byte >> (position % 8)) & 1;
            value |= u64::from(bit) << output_bit;
        }

        self.bit_position = end;
        Ok(value)
    }

    fn read_bounded_u32(&mut self, max_exclusive: u32, low_width: u8) -> Result<u32> {
        if max_exclusive == 0 {
            return Err(network_bit_error(
                "invalid-maximum",
                "bounded integer maximum must be greater than zero",
            ));
        }
        if low_width > 32 {
            return Err(network_bit_error(
                "invalid-low-width",
                format!("bounded integer low width {low_width} exceeds 32"),
            ));
        }

        let range = 1u64 << low_width;
        let max_exclusive_u64 = u64::from(max_exclusive);
        if range > max_exclusive_u64 {
            return Err(network_bit_error(
                "invalid-configuration",
                format!(
                    "bounded integer range {range} from low width {low_width} exceeds maximum {max_exclusive}"
                ),
            ));
        }

        let start = self.bit_position;
        let low = self.read_bits_le(usize::from(low_width))?;
        let up = low + range;
        let value = if up < max_exclusive_u64 {
            match self.read_bit() {
                Ok(true) => up,
                Ok(false) => low,
                Err(error) => {
                    self.bit_position = start;
                    return Err(error);
                }
            }
        } else {
            low
        };

        if value >= max_exclusive_u64 {
            self.bit_position = start;
            return Err(network_bit_error(
                "invalid-bounded-result",
                format!("decoded value {value} is outside maximum {max_exclusive}"),
            ));
        }

        match u32::try_from(value) {
            Ok(value) => Ok(value),
            Err(_) => {
                self.bit_position = start;
                Err(network_bit_error(
                    "invalid-bounded-result",
                    format!("decoded value {value} does not fit in u32"),
                ))
            }
        }
    }
}

fn network_bit_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network bit error: {category}: {}",
        detail.into()
    ))
}
'''

TESTS = r'''

    #[test]
    fn r3_14c_bit_cursor_reads_lsb_first_within_byte() {
        let mut cursor = NetworkBitCursor::new(&[0b1010_0110]);
        let observed = [
            cursor.read_bit().expect("bit 0"),
            cursor.read_bit().expect("bit 1"),
            cursor.read_bit().expect("bit 2"),
            cursor.read_bit().expect("bit 3"),
            cursor.read_bit().expect("bit 4"),
            cursor.read_bit().expect("bit 5"),
            cursor.read_bit().expect("bit 6"),
            cursor.read_bit().expect("bit 7"),
        ];
        assert_eq!(
            observed,
            [false, true, true, false, false, true, false, true]
        );
        assert_eq!(cursor.position_bits(), 8);
        assert_eq!(cursor.remaining_bits(), 0);
    }

    #[test]
    fn r3_14c_bit_cursor_reads_across_byte_boundary() {
        let mut cursor = NetworkBitCursor::new(&[0b1111_0000, 0b0000_0011]);
        assert_eq!(cursor.read_bits_le(4).expect("prefix"), 0);
        assert_eq!(cursor.read_bits_le(8).expect("cross-byte value"), 0x3f);
        assert_eq!(cursor.position_bits(), 12);
        assert_eq!(cursor.remaining_bits(), 4);
    }

    #[test]
    fn r3_14c_bit_cursor_tracks_mixed_width_positions() {
        let mut cursor = NetworkBitCursor::new(&[0b1101_0110, 0b0000_0001]);
        assert_eq!(cursor.read_bits_le(3).expect("first"), 6);
        assert_eq!(cursor.position_bits(), 3);
        assert_eq!(cursor.read_bits_le(2).expect("second"), 2);
        assert_eq!(cursor.position_bits(), 5);
        assert_eq!(cursor.read_bits_le(4).expect("third"), 14);
        assert_eq!(cursor.position_bits(), 9);
        assert_eq!(cursor.remaining_bits(), 7);
    }

    #[test]
    fn r3_14c_bit_cursor_zero_width_is_noop() {
        let mut cursor = NetworkBitCursor::new(&[0xff]);
        assert_eq!(cursor.read_bits_le(0).expect("zero width"), 0);
        assert_eq!(cursor.position_bits(), 0);
        assert_eq!(cursor.remaining_bits(), 8);
    }

    #[test]
    fn r3_14c_bit_cursor_width_64_consumes_exactly_64_bits() {
        let bytes = [0xff; 8];
        let mut cursor = NetworkBitCursor::new(&bytes);
        assert_eq!(cursor.read_bits_le(64).expect("64-bit read"), u64::MAX);
        assert_eq!(cursor.position_bits(), 64);
        assert_eq!(cursor.remaining_bits(), 0);
    }

    #[test]
    fn r3_14c_bit_cursor_width_above_64_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff; 9]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bits_le(65)
            .expect_err("width 65 must be rejected");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("invalid-width"));
    }

    #[test]
    fn r3_14c_bit_cursor_empty_read_bit_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[]);
        let before = cursor.position_bits();
        let error = cursor.read_bit().expect_err("empty cursor must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("insufficient-bits"));
    }

    #[test]
    fn r3_14c_bit_cursor_insufficient_multibit_read_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bits_le(9)
            .expect_err("nine bits from one byte must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("insufficient-bits"));
    }

    #[test]
    fn r3_14c_bounded_u32_zero_maximum_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bounded_u32(0, 0)
            .expect_err("zero maximum must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("invalid-maximum"));
    }

    #[test]
    fn r3_14c_bounded_u32_maximum_one_returns_zero_without_reading() {
        let mut cursor = NetworkBitCursor::new(&[]);
        assert_eq!(cursor.read_bounded_u32(1, 0).expect("only zero is valid"), 0);
        assert_eq!(cursor.position_bits(), 0);
        assert_eq!(cursor.remaining_bits(), 0);
    }

    #[test]
    fn r3_14c_bounded_u32_r3_14a_vector_discriminator_zero() {
        let mut cursor = NetworkBitCursor::new(&[0x00, 0x00]);
        assert_eq!(
            cursor
                .read_bounded_u32(2047, 10)
                .expect("R3.14A actor-id vector"),
            0
        );
        assert_eq!(cursor.position_bits(), 11);
    }

    #[test]
    fn r3_14c_bounded_u32_matches_all_47_r3_14a_actor_id_vectors() {
        for row_index in 0..47 {
            let mut cursor = NetworkBitCursor::new(&[0x00, 0x00]);
            let value = cursor
                .read_bounded_u32(2047, 10)
                .unwrap_or_else(|error| panic!("R3.14A row {row_index} failed: {error}"));
            assert_eq!(value, 0, "R3.14A row {row_index} value drift");
            assert_eq!(
                cursor.position_bits(),
                11,
                "R3.14A row {row_index} end-bit drift"
            );
        }
    }

    #[test]
    fn r3_14c_bounded_u32_discriminator_one_selects_upper_value() {
        let mut cursor = NetworkBitCursor::new(&[0x00, 0x04]);
        assert_eq!(
            cursor
                .read_bounded_u32(2047, 10)
                .expect("upper actor-id branch"),
            1024
        );
        assert_eq!(cursor.position_bits(), 11);
    }

    #[test]
    fn r3_14c_bounded_u32_threshold_skips_discriminator() {
        let mut cursor = NetworkBitCursor::new(&[0xff, 0x03]);
        assert_eq!(
            cursor
                .read_bounded_u32(2047, 10)
                .expect("threshold low value"),
            1023
        );
        assert_eq!(cursor.position_bits(), 10);
        assert_eq!(cursor.remaining_bits(), 6);
    }

    #[test]
    fn r3_14c_bounded_u32_missing_discriminator_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0x00, 0x00]);
        assert_eq!(cursor.read_bits_le(6).expect("prefix"), 0);
        let before = cursor.position_bits();
        let error = cursor
            .read_bounded_u32(2047, 10)
            .expect_err("required discriminator is missing");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("insufficient-bits"));
    }

    #[test]
    fn r3_14c_bounded_u32_back_to_back_reads_stay_aligned() {
        let mut cursor = NetworkBitCursor::new(&[0b0000_0110]);
        assert_eq!(cursor.read_bounded_u32(3, 1).expect("first"), 2);
        assert_eq!(cursor.position_bits(), 2);
        assert_eq!(cursor.read_bounded_u32(3, 1).expect("second"), 1);
        assert_eq!(cursor.position_bits(), 3);
    }

    #[test]
    fn r3_14c_bounded_u32_admitted_synthetic_outputs_stay_below_maximum() {
        let cases = [
            ([0x00, 0x00], 0u32),
            ([0x00, 0x04], 1024u32),
            ([0xff, 0x03], 1023u32),
        ];
        for (bytes, expected) in cases {
            let mut cursor = NetworkBitCursor::new(&bytes);
            let value = cursor
                .read_bounded_u32(2047, 10)
                .expect("synthetic bounded value");
            assert_eq!(value, expected);
            assert!(value < 2047);
        }
    }

    #[test]
    fn r3_14c_bounded_u32_low_width_above_32_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff; 8]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bounded_u32(u32::MAX, 33)
            .expect_err("low width above 32 must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("invalid-low-width"));
    }

    #[test]
    fn r3_14c_bounded_u32_impossible_range_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bounded_u32(3, 2)
            .expect_err("range larger than maximum must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("invalid-configuration"));
    }
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    if "struct NetworkBitCursor<'a>" in text:
        raise SystemExit("R3.14C primitive already appears in source")
    if "fn r3_14c_bit_cursor_reads_lsb_first_within_byte" in text:
        raise SystemExit("R3.14C tests already appear in source")

    text = replace_once(
        text,
        PRIMITIVE_ANCHOR,
        PRIMITIVE_ANCHOR + PRIMITIVES,
        "primitive insertion anchor",
    )
    text = replace_once(
        text,
        TEST_ANCHOR,
        TEST_ANCHOR + TESTS,
        "test insertion anchor",
    )

    SOURCE.write_text(text, encoding="utf-8", newline="\n")
    print("R3_14C_V2_PATCH=PASS")


if __name__ == "__main__":
    main()
