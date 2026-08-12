from pathlib import Path

PATH = Path("crates/mimir-replay/src/lib.rs")


def insert_before(text: str, marker: str, insertion: str) -> str:
    if text.count(marker) != 1:
        raise RuntimeError(f"expected one marker {marker!r}, found {text.count(marker)}")
    return text.replace(marker, insertion + marker, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    if "ReplayNetworkTimingPreambleV1" in text:
        raise RuntimeError("R3.9 network timing preamble already present")

    public_api = r'''
/// Byte-aligned timing preamble and decoder prerequisites for the first admitted network frame.
///
/// This type deliberately stops after the first 8 network bytes (`f32 time`, `f32 delta`).
/// It does not consume actor bits, iterate frames, resolve attributes, extract raw state/events,
/// or validate replay CRC fields.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkTimingPreambleV1 {
    pub header: ReplayHeader,
    pub content: ReplayContentScaffoldV1,
    pub num_frames: u32,
    pub max_channels: u32,
    pub channel_bits: u8,
    pub first_frame_time: f32,
    pub first_frame_delta: f32,
}

pub trait ReplayNetworkTimingPreambleReader {
    fn read_network_timing_preamble(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkTimingPreambleV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayNetworkTimingPreambleReader;

impl ReplayNetworkTimingPreambleReader for MinimalReplayNetworkTimingPreambleReader {
    fn read_network_timing_preamble(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkTimingPreambleV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_network_timing_preamble_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(network_timing_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the network timing preamble reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

'''
    text = insert_before(
        text,
        "#[derive(Debug, Default, Clone, Copy)]\npub struct MinimalReplayHeaderReader;",
        public_api,
    )

    implementation = r'''
fn parse_replay_network_timing_preamble_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayNetworkTimingPreambleV1> {
    // Reuse the exact admitted header lane. R3.9 must not widen BuildVersion/version support.
    let header = parse_replay_header_from_memory(label, bytes)?;
    let content = parse_replay_content_scaffold_from_memory(label, bytes)?;

    let num_frames = header.total_frames.ok_or_else(|| {
        network_timing_error(
            "missing-header-field",
            "NumFrames is required for the admitted network timing preamble",
        )
    })?;

    let max_channels_i64 = match header.metadata.get("MaxChannels") {
        Some(FieldValue::Integer(value)) => *value,
        Some(other) => {
            return Err(network_timing_error(
                "mapping",
                format!("MaxChannels must be integer metadata, got {other:?}"),
            ));
        }
        None => {
            return Err(network_timing_error(
                "missing-header-field",
                "MaxChannels is required for the admitted network timing preamble",
            ));
        }
    };
    let max_channels = u32::try_from(max_channels_i64).map_err(|_| {
        network_timing_error(
            "mapping",
            format!("MaxChannels {max_channels_i64} cannot fit non-negative u32"),
        )
    })?;
    if max_channels == 0 {
        return Err(network_timing_error(
            "mapping",
            "MaxChannels must be positive for the admitted network timing preamble",
        ));
    }

    let network_size = usize::try_from(content.network_size).map_err(|_| {
        network_timing_error("malformed", "network_size cannot fit usize")
    })?;
    if network_size < 8 {
        return Err(network_timing_error(
            "insufficient",
            format!("network payload has {network_size} bytes; first timing pair needs 8"),
        ));
    }
    if usize::try_from(num_frames)
        .map_err(|_| network_timing_error("mapping", "NumFrames cannot fit usize"))?
        > network_size
    {
        return Err(network_timing_error(
            "precondition",
            format!(
                "NumFrames {num_frames} exceeds network payload byte length {network_size}"
            ),
        ));
    }

    let network_start = usize::try_from(content.network_start).map_err(|_| {
        network_timing_error("malformed", "network_start cannot fit usize")
    })?;
    let timing_end = network_start.checked_add(8).ok_or_else(|| {
        network_timing_error("malformed", "first timing byte range overflows usize")
    })?;
    if timing_end > bytes.len() {
        return Err(network_timing_error(
            "insufficient",
            "first network timing pair extends beyond replay bytes",
        ));
    }

    let first_frame_time = f32::from_le_bytes(
        bytes[network_start..network_start + 4]
            .try_into()
            .expect("timing range checked for four bytes"),
    );
    let first_frame_delta = f32::from_le_bytes(
        bytes[network_start + 4..timing_end]
            .try_into()
            .expect("timing range checked for four bytes"),
    );
    validate_network_timing_component("time", first_frame_time)?;
    validate_network_timing_component("delta", first_frame_delta)?;
    if first_frame_time == 0.0 && first_frame_delta == 0.0 {
        return Err(network_timing_error(
            "terminal-first-frame",
            "first network timing pair is the 0/0 terminal marker",
        ));
    }

    let bit_width = u32::BITS - max_channels.leading_zeros();
    let channel_bits_u32 = bit_width.saturating_sub(1);
    let channel_bits = u8::try_from(channel_bits_u32).map_err(|_| {
        network_timing_error(
            "mapping",
            format!("derived channel bit width {channel_bits_u32} cannot fit u8"),
        )
    })?;

    Ok(ReplayNetworkTimingPreambleV1 {
        header,
        content,
        num_frames,
        max_channels,
        channel_bits,
        first_frame_time,
        first_frame_delta,
    })
}

fn validate_network_timing_component(name: &str, value: f32) -> Result<()> {
    if !value.is_finite() || value < 0.0 || (value > 0.0 && value < 1.0e-10) {
        return Err(network_timing_error(
            "malformed",
            format!("first frame {name} is outside admitted finite timing bounds: {value:?}"),
        ));
    }
    Ok(())
}

'''
    text = insert_before(
        text,
        "fn parse_replay_header_from_memory(label: &str, bytes: &[u8]) -> Result<ReplayHeader> {",
        implementation,
    )

    error_helper = r'''
fn network_timing_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network timing error: {category}: {}",
        detail.into()
    ))
}

'''
    text = insert_before(
        text,
        "fn footer_lookup_error(category: &str, detail: impl Into<String>) -> MimirError {",
        error_helper,
    )

    tests = r'''
    fn mutate_first_network_timing(
        bytes: &mut [u8],
        time: f32,
        delta: f32,
    ) -> ReplayContentScaffoldV1 {
        let input = ReplayInput::Memory {
            label: "timing-mutation-source".to_string(),
            bytes: bytes.to_vec(),
        };
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&input)
            .expect("fixture content scaffold should be valid before timing mutation");
        let start = scaffold.network_start as usize;
        bytes[start..start + 4].copy_from_slice(&time.to_le_bytes());
        bytes[start + 4..start + 8].copy_from_slice(&delta.to_le_bytes());
        scaffold
    }

    fn rename_unique_ascii_property(bytes: &mut [u8], needle: &[u8]) {
        let positions = bytes
            .windows(needle.len())
            .enumerate()
            .filter_map(|(index, window)| (window == needle).then_some(index))
            .collect::<Vec<_>>();
        assert_eq!(positions.len(), 1, "property marker must be unique");
        bytes[positions[0]] = b'X';
    }

    #[test]
    fn minimal_network_timing_preamble_reader_matches_three_historical_fixtures() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let timing = MinimalReplayNetworkTimingPreambleReader
                .read_network_timing_preamble(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical exact-admitted fixture should expose first timing preamble");
            assert!(timing.first_frame_time.is_finite());
            assert!(timing.first_frame_time > 0.0);
            assert_eq!(timing.first_frame_delta, 0.0);
            assert_eq!(timing.channel_bits, 10);
            assert_eq!(timing.num_frames, timing.header.total_frames.unwrap());
            assert!(timing.max_channels > 0);
            assert!(timing.content.network_size >= 8);
        }
    }

    #[test]
    fn minimal_network_timing_preamble_reader_preserves_44_56_header_admission_gate() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 timing-preamble regression; corpus root is absent");
            return;
        }
        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| entry.expect("corpus directory entry should be readable").path())
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        replay_paths.sort();
        assert_eq!(replay_paths.len(), 100);

        let mut supported = 0usize;
        let mut unsupported = 0usize;
        for path in replay_paths {
            let bytes = fs::read(&path).expect("checked-in corpus replay should be readable");
            let label = path.file_name().unwrap().to_string_lossy().into_owned();
            let input = ReplayInput::Memory { label, bytes };
            let header_result = MinimalReplayHeaderReader.read_header(&input);
            let timing_result = MinimalReplayNetworkTimingPreambleReader
                .read_network_timing_preamble(&input);
            match header_result {
                Ok(_) => {
                    supported += 1;
                    let timing = timing_result.expect(
                        "every currently admitted header row must satisfy R3.9 timing evidence",
                    );
                    assert!(timing.first_frame_time > 0.0);
                    assert_eq!(timing.first_frame_delta, 0.0);
                    assert_eq!(timing.channel_bits, 10);
                }
                Err(_) => {
                    unsupported += 1;
                    assert!(
                        timing_result.is_err(),
                        "timing reader must not bypass exact header admission"
                    );
                }
            }
        }
        assert_eq!(supported, 44);
        assert_eq!(unsupported, 56);
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_file_input() {
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside timing preamble reader");
        assert_error_contains(error, "replay network timing error: unsupported-input");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_invalid_timing_components() {
        let Some(original) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        for (time, delta) in [
            (f32::NAN, 0.0),
            (-1.0, 0.0),
            (1.0e-20, 0.0),
            (1.0, -0.01),
            (1.0, 1.0e-20),
        ] {
            let mut bytes = original.clone();
            mutate_first_network_timing(&mut bytes, time, delta);
            let error = MinimalReplayNetworkTimingPreambleReader
                .read_network_timing_preamble(&ReplayInput::Memory {
                    label: FIXTURE_001_LABEL.to_string(),
                    bytes,
                })
                .expect_err("invalid first timing component must fail closed");
            assert_error_contains(error, "replay network timing error: malformed");
        }
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_terminal_zero_zero_pair() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        mutate_first_network_timing(&mut bytes, 0.0, 0.0);
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("0/0 first timing pair is the terminal marker");
        assert_error_contains(error, "replay network timing error: terminal-first-frame");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_network_shorter_than_eight_bytes() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        let input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&input)
            .expect("fixture scaffold should be valid");
        let offset = scaffold.network_size_offset as usize;
        bytes[offset..offset + 4].copy_from_slice(&7i32.to_le_bytes());
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("network payload shorter than one timing pair must fail");
        assert_error_contains(error, "replay network timing error: insufficient");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_num_frames_over_network_bytes() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        let input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&input)
            .expect("fixture scaffold should be valid");
        let offset = scaffold.network_size_offset as usize;
        bytes[offset..offset + 4].copy_from_slice(&8i32.to_le_bytes());
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("NumFrames above network byte count violates decoder precondition");
        assert_error_contains(error, "replay network timing error: precondition");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_requires_max_channels_metadata() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        rename_unique_ascii_property(&mut bytes, b"MaxChannels\0");
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("R3.9 admission requires observed MaxChannels instead of fallback");
        assert_error_contains(error, "replay network timing error: missing-header-field");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_requires_num_frames_header_mapping() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        rename_unique_ascii_property(&mut bytes, b"NumFrames\0");
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("R3.9 admission requires NumFrames mapping");
        assert_error_contains(error, "replay network timing error: missing-header-field");
    }

'''
    text = insert_before(
        text,
        "    #[test]\n    fn unsupported_reader_fails_explicitly() {",
        tests,
    )

    PATH.write_text(text, encoding="utf-8")
    print("PASS: applied bounded R3.9 network timing preamble reader patch")


if __name__ == "__main__":
    main()
