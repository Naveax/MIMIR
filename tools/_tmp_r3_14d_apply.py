from __future__ import annotations

from pathlib import Path

SOURCE = Path("crates/mimir-replay/src/lib.rs")

PUBLIC_ANCHOR = "/// Conservative network attribute wire-tag registry admitted from the supported replay lane.\n"
HELPER_ANCHOR = "fn validate_network_timing_component(name: &str, value: f32) -> Result<()> {\n"
TEST_ANCHOR = "#[cfg(test)]\nmod tests {\n    use super::*;\n"

PUBLIC_API = r'''
/// First native replay-network frame / actor-envelope header admitted through the `new` bit.
///
/// This type deliberately stops before `name_id`, object/spawn payloads, property payloads,
/// additional actors, or additional frames.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkFirstActorEnvelopeV1 {
    pub timing: ReplayNetworkTimingPreambleV1,
    pub first_frame_time_raw_u32: u32,
    pub first_frame_delta_raw_u32: u32,
    pub actor_present: bool,
    pub actor_id: Option<u32>,
    pub alive: Option<bool>,
    pub is_new: Option<bool>,
    pub stop_bit: u64,
}

pub trait ReplayNetworkFirstActorEnvelopeReader {
    fn read_network_first_actor_envelope(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkFirstActorEnvelopeV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayNetworkFirstActorEnvelopeReader;

impl ReplayNetworkFirstActorEnvelopeReader for MinimalReplayNetworkFirstActorEnvelopeReader {
    fn read_network_first_actor_envelope(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkFirstActorEnvelopeV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_network_first_actor_envelope_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(network_first_actor_envelope_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the first actor-envelope reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

'''

PRIVATE_HELPERS = r'''
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct DecodedNetworkFirstActorHeaderV1 {
    time_raw_u32: u32,
    delta_raw_u32: u32,
    actor_present: bool,
    actor_id: Option<u32>,
    alive: Option<bool>,
    is_new: Option<bool>,
    stop_bit: usize,
}

fn parse_replay_network_first_actor_envelope_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayNetworkFirstActorEnvelopeV1> {
    // Reuse the exact admitted timing/header/content lane. R3.14D must not widen support.
    let timing = parse_replay_network_timing_preamble_from_memory(label, bytes)?;

    let network_start = usize::try_from(timing.content.network_start).map_err(|_| {
        network_first_actor_envelope_error("malformed", "network_start cannot fit usize")
    })?;
    let network_size = usize::try_from(timing.content.network_size).map_err(|_| {
        network_first_actor_envelope_error("malformed", "network_size cannot fit usize")
    })?;
    let network_end = network_start.checked_add(network_size).ok_or_else(|| {
        network_first_actor_envelope_error("malformed", "network byte range overflows usize")
    })?;
    if network_end > bytes.len() {
        return Err(network_first_actor_envelope_error(
            "insufficient",
            "network payload extends beyond replay bytes",
        ));
    }

    let decoded = decode_network_first_actor_header(
        &bytes[network_start..network_end],
        timing.max_channels,
        timing.channel_bits,
        timing.first_frame_time.to_bits(),
        timing.first_frame_delta.to_bits(),
    )?;
    let stop_bit = u64::try_from(decoded.stop_bit).map_err(|_| {
        network_first_actor_envelope_error("mapping", "stop bit cannot fit u64")
    })?;

    Ok(ReplayNetworkFirstActorEnvelopeV1 {
        timing,
        first_frame_time_raw_u32: decoded.time_raw_u32,
        first_frame_delta_raw_u32: decoded.delta_raw_u32,
        actor_present: decoded.actor_present,
        actor_id: decoded.actor_id,
        alive: decoded.alive,
        is_new: decoded.is_new,
        stop_bit,
    })
}

fn decode_network_first_actor_header(
    network: &[u8],
    max_channels: u32,
    channel_bits: u8,
    expected_time_raw_u32: u32,
    expected_delta_raw_u32: u32,
) -> Result<DecodedNetworkFirstActorHeaderV1> {
    let mut cursor = NetworkBitCursor::new(network);

    let time_raw_u32 = u32::try_from(cursor.read_bits_le(32)?).map_err(|_| {
        network_first_actor_envelope_error("mapping", "time raw bits cannot fit u32")
    })?;
    let delta_raw_u32 = u32::try_from(cursor.read_bits_le(32)?).map_err(|_| {
        network_first_actor_envelope_error("mapping", "delta raw bits cannot fit u32")
    })?;

    if time_raw_u32 != expected_time_raw_u32 {
        return Err(network_first_actor_envelope_error(
            "timing-mismatch",
            format!(
                "cursor time raw bits {time_raw_u32:#010x} differ from admitted timing preamble {expected_time_raw_u32:#010x}"
            ),
        ));
    }
    if delta_raw_u32 != expected_delta_raw_u32 {
        return Err(network_first_actor_envelope_error(
            "timing-mismatch",
            format!(
                "cursor delta raw bits {delta_raw_u32:#010x} differ from admitted timing preamble {expected_delta_raw_u32:#010x}"
            ),
        ));
    }

    // The preamble has already validated these values. Re-materialize them from cursor bits so
    // the reader cannot silently skip the first 64 network bits.
    let _time = f32::from_bits(time_raw_u32);
    let _delta = f32::from_bits(delta_raw_u32);

    let actor_present = cursor.read_bit().map_err(|error| {
        network_first_actor_envelope_error(
            "actor-present",
            format!("cannot read first actor_present bit: {error}"),
        )
    })?;
    if !actor_present {
        return Ok(DecodedNetworkFirstActorHeaderV1 {
            time_raw_u32,
            delta_raw_u32,
            actor_present,
            actor_id: None,
            alive: None,
            is_new: None,
            stop_bit: cursor.position_bits(),
        });
    }

    let actor_id = cursor
        .read_bounded_u32(max_channels, channel_bits)
        .map_err(|error| {
            network_first_actor_envelope_error(
                "actor-id",
                format!("cannot read first bounded actor_id: {error}"),
            )
        })?;

    let alive = cursor.read_bit().map_err(|error| {
        network_first_actor_envelope_error(
            "alive",
            format!("cannot read first actor alive bit: {error}"),
        )
    })?;
    if !alive {
        return Ok(DecodedNetworkFirstActorHeaderV1 {
            time_raw_u32,
            delta_raw_u32,
            actor_present,
            actor_id: Some(actor_id),
            alive: Some(false),
            is_new: None,
            stop_bit: cursor.position_bits(),
        });
    }

    let is_new = cursor.read_bit().map_err(|error| {
        network_first_actor_envelope_error(
            "new",
            format!("cannot read first actor new bit: {error}"),
        )
    })?;

    Ok(DecodedNetworkFirstActorHeaderV1 {
        time_raw_u32,
        delta_raw_u32,
        actor_present,
        actor_id: Some(actor_id),
        alive: Some(true),
        is_new: Some(is_new),
        stop_bit: cursor.position_bits(),
    })
}

fn network_first_actor_envelope_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network first actor envelope error: {category}: {}",
        detail.into()
    ))
}

'''

TESTS = r'''

    fn r3_14d_append_bit(bytes: &mut Vec<u8>, bit_position: &mut usize, value: bool) {
        let byte_index = *bit_position / 8;
        let bit_index = *bit_position % 8;
        if byte_index == bytes.len() {
            bytes.push(0);
        }
        if value {
            bytes[byte_index] |= 1 << bit_index;
        }
        *bit_position += 1;
    }

    fn r3_14d_append_bits(bytes: &mut Vec<u8>, bit_position: &mut usize, value: u64, width: usize) {
        for bit in 0..width {
            r3_14d_append_bit(bytes, bit_position, ((value >> bit) & 1) != 0);
        }
    }

    fn r3_14d_append_bounded(
        bytes: &mut Vec<u8>,
        bit_position: &mut usize,
        value: u32,
        max_exclusive: u32,
        low_width: u8,
    ) {
        let range = 1u64 << low_width;
        let low = u64::from(value) & (range - 1);
        r3_14d_append_bits(bytes, bit_position, low, usize::from(low_width));
        if low + range < u64::from(max_exclusive) {
            r3_14d_append_bit(bytes, bit_position, u64::from(value) >= range);
        }
    }

    fn r3_14d_network_prefix(time: f32, delta: f32) -> (Vec<u8>, usize) {
        let mut bytes = Vec::with_capacity(16);
        bytes.extend_from_slice(&time.to_bits().to_le_bytes());
        bytes.extend_from_slice(&delta.to_bits().to_le_bytes());
        (bytes, 64)
    }

    #[test]
    fn r3_14d_consumes_timing_raw_bits_through_native_cursor() {
        let time = 1.25f32;
        let delta = 0.008f32;
        let (mut network, mut bit) = r3_14d_network_prefix(time, delta);
        r3_14d_append_bit(&mut network, &mut bit, false);

        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            time.to_bits(),
            delta.to_bits(),
        )
        .expect("timing + absent actor envelope should decode");
        assert_eq!(decoded.time_raw_u32, time.to_bits());
        assert_eq!(decoded.delta_raw_u32, delta.to_bits());
        assert_eq!(decoded.stop_bit, 65);
    }

    #[test]
    fn r3_14d_rejects_timing_raw_bit_mismatch() {
        let time = 1.25f32;
        let delta = 0.008f32;
        let (mut network, mut bit) = r3_14d_network_prefix(time, delta);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let error = decode_network_first_actor_header(
            &network,
            2047,
            10,
            2.0f32.to_bits(),
            delta.to_bits(),
        )
        .expect_err("timing raw mismatch must fail closed");
        assert_error_contains(error, "replay network first actor envelope error: timing-mismatch");
    }

    #[test]
    fn r3_14d_actor_absent_branch_stops_at_65_and_preserves_none_fields() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("actor absent branch");
        assert!(!decoded.actor_present);
        assert_eq!(decoded.actor_id, None);
        assert_eq!(decoded.alive, None);
        assert_eq!(decoded.is_new, None);
        assert_eq!(decoded.stop_bit, 65);
    }

    #[test]
    fn r3_14d_alive_false_branch_stops_before_new() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 0, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("alive false branch");
        assert_eq!(decoded.actor_id, Some(0));
        assert_eq!(decoded.alive, Some(false));
        assert_eq!(decoded.is_new, None);
        assert_eq!(decoded.stop_bit, 77);
    }

    #[test]
    fn r3_14d_alive_true_new_false_branch_stops_after_new() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 0, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("new false branch");
        assert_eq!(decoded.actor_id, Some(0));
        assert_eq!(decoded.alive, Some(true));
        assert_eq!(decoded.is_new, Some(false));
        assert_eq!(decoded.stop_bit, 78);
    }

    #[test]
    fn r3_14d_alive_true_new_true_branch_stops_at_r3_14a_boundary() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 0, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bits(&mut network, &mut bit, 0b11_1111, 6);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("new true branch");
        assert_eq!(decoded.actor_id, Some(0));
        assert_eq!(decoded.alive, Some(true));
        assert_eq!(decoded.is_new, Some(true));
        assert_eq!(decoded.stop_bit, 78);
    }

    #[test]
    fn r3_14d_bounded_actor_id_discriminator_one_path() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 1024, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("discriminator one path");
        assert_eq!(decoded.actor_id, Some(1024));
        assert_eq!(decoded.stop_bit, 77);
    }

    #[test]
    fn r3_14d_bounded_actor_id_threshold_skips_discriminator() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 1023, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("threshold path");
        assert_eq!(decoded.actor_id, Some(1023));
        assert_eq!(decoded.stop_bit, 76);
    }

    #[test]
    fn r3_14d_missing_actor_present_fails() {
        let (network, _) = r3_14d_network_prefix(1.0, 0.01);
        let error = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("actor_present is required after timing");
        assert_error_contains(error, "replay network first actor envelope error: actor-present");
    }

    #[test]
    fn r3_14d_truncated_actor_id_low_bits_fail() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        // One extra byte provides only seven bits after actor_present, fewer than low_width=10.
        while network.len() < 9 {
            network.push(0);
        }
        let error = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("actor id low bits are truncated");
        assert_error_contains(error, "replay network first actor envelope error: actor-id");
    }

    #[test]
    fn r3_14d_missing_required_actor_id_discriminator_fails() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bits(&mut network, &mut bit, 0, 7);
        assert_eq!(bit, 72);
        let error = decode_network_first_actor_header(
            &network,
            255,
            7,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("required bounded discriminator is truncated at byte end");
        assert_error_contains(error, "replay network first actor envelope error: actor-id");
    }

    #[test]
    fn r3_14d_missing_alive_fails() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bits(&mut network, &mut bit, 0, 7);
        assert_eq!(bit, 72);
        let error = decode_network_first_actor_header(
            &network,
            128,
            7,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("alive bit is truncated at byte end");
        assert_error_contains(error, "replay network first actor envelope error: alive");
    }

    #[test]
    fn r3_14d_missing_new_when_alive_true_fails() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bits(&mut network, &mut bit, 0, 6);
        r3_14d_append_bit(&mut network, &mut bit, true);
        assert_eq!(bit, 72);
        let error = decode_network_first_actor_header(
            &network,
            64,
            6,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("new bit is truncated at byte end");
        assert_error_contains(error, "replay network first actor envelope error: new");
    }

    #[test]
    fn r3_14d_public_reader_rejects_file_input() {
        let error = MinimalReplayNetworkFirstActorEnvelopeReader
            .read_network_first_actor_envelope(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside first actor-envelope reader");
        assert_error_contains(
            error,
            "replay network first actor envelope error: unsupported-input",
        );
    }

    #[test]
    fn r3_14d_public_reader_preserves_terminal_first_frame_rejection() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        mutate_first_network_timing(&mut bytes, 0.0, 0.0);
        let error = MinimalReplayNetworkFirstActorEnvelopeReader
            .read_network_first_actor_envelope(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("terminal first frame must fail before actor parsing");
        assert_error_contains(error, "replay network timing error: terminal-first-frame");
    }

    #[test]
    fn r3_14d_public_reader_matches_three_historical_fixtures_through_new_only() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let envelope = MinimalReplayNetworkFirstActorEnvelopeReader
                .read_network_first_actor_envelope(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical admitted fixture should expose first actor envelope");
            assert_eq!(
                envelope.first_frame_time_raw_u32,
                envelope.timing.first_frame_time.to_bits()
            );
            assert_eq!(
                envelope.first_frame_delta_raw_u32,
                envelope.timing.first_frame_delta.to_bits()
            );
            assert!(envelope.actor_present);
            assert_eq!(envelope.actor_id, Some(0));
            assert_eq!(envelope.alive, Some(true));
            assert_eq!(envelope.is_new, Some(true));
            assert_eq!(envelope.stop_bit, 78);
        }
    }
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one source match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    if "ReplayNetworkFirstActorEnvelopeV1" in text:
        raise SystemExit("R3.14D public result already appears in source")
    if "fn r3_14d_consumes_timing_raw_bits_through_native_cursor" in text:
        raise SystemExit("R3.14D focused tests already appear in source")

    text = replace_once(text, PUBLIC_ANCHOR, PUBLIC_API + PUBLIC_ANCHOR, "public API anchor")
    text = replace_once(text, HELPER_ANCHOR, PRIVATE_HELPERS + HELPER_ANCHOR, "private helper anchor")
    text = replace_once(text, TEST_ANCHOR, TEST_ANCHOR + TESTS, "test module anchor")
    SOURCE.write_text(text, encoding="utf-8", newline="\n")
    print("R3_14D_PATCH=PASS")


if __name__ == "__main__":
    main()
