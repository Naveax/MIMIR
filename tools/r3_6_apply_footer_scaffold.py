from __future__ import annotations

from pathlib import Path

PATH = Path("crates/mimir-replay/src/lib.rs")


def insert_before(text: str, marker: str, insertion: str) -> str:
    count = text.count(marker)
    if count != 1:
        raise RuntimeError(f"expected exactly one marker, found {count}: {marker[:80]!r}")
    return text.replace(marker, insertion + marker, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    if "ReplayFooterScaffoldV1" in text:
        raise RuntimeError("footer scaffold implementation already present")

    public_api = r'''
/// Structural footer scaffold after the raw replay network payload.
///
/// This type records bounded offsets and counts only. It does not decode network bits,
/// interpret footer strings, build object/name/net-cache lookup semantics, validate CRCs,
/// extract frames/raw states/events, or assign meaning to the optional opaque tail bytes.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayFooterScaffoldV1 {
    pub content: ReplayContentScaffoldV1,
    pub debug_info_count_offset: u64,
    pub debug_info_count: u32,
    pub debug_info_data_start: u64,
    pub debug_info_end: u64,
    pub tickmarks_count_offset: u64,
    pub tickmarks_count: u32,
    pub tickmarks_data_start: u64,
    pub tickmarks_end: u64,
    pub packages_count_offset: u64,
    pub packages_count: u32,
    pub packages_data_start: u64,
    pub packages_end: u64,
    pub objects_count_offset: u64,
    pub objects_count: u32,
    pub objects_data_start: u64,
    pub objects_end: u64,
    pub names_count_offset: u64,
    pub names_count: u32,
    pub names_data_start: u64,
    pub names_end: u64,
    pub class_indices_count_offset: u64,
    pub class_indices_count: u32,
    pub class_indices_data_start: u64,
    pub class_indices_end: u64,
    pub net_cache_count_offset: u64,
    pub net_cache_count: u32,
    pub net_cache_data_start: u64,
    pub net_cache_properties_count: u32,
    pub net_cache_end: u64,
    /// First byte after the structurally known footer fields.
    pub opaque_tail_start: u64,
    /// Admitted observed forms are zero bytes or exactly four zero bytes.
    /// No semantic meaning is assigned to either form.
    pub opaque_tail_size: u32,
    pub footer_end: u64,
}

pub trait ReplayFooterScaffoldReader {
    fn read_footer_scaffold(&self, input: &ReplayInput) -> Result<ReplayFooterScaffoldV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayFooterScaffoldReader;

impl ReplayFooterScaffoldReader for MinimalReplayFooterScaffoldReader {
    fn read_footer_scaffold(&self, input: &ReplayInput) -> Result<ReplayFooterScaffoldV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_footer_scaffold_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(footer_scaffold_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the minimal footer-scaffold reader: {}",
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
fn parse_replay_footer_scaffold_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayFooterScaffoldV1> {
    let content = parse_replay_content_scaffold_from_memory(label, bytes)?;
    let content_end = usize::try_from(content.boundary.content_end)
        .map_err(|_| footer_scaffold_error("malformed", "content_end cannot fit usize"))?;
    let mut cursor = usize::try_from(content.footer_start)
        .map_err(|_| footer_scaffold_error("malformed", "footer_start cannot fit usize"))?;

    let debug_info_count_offset = cursor;
    let debug_info_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "debug info")?;
    let debug_info_data_start = cursor;
    for index in 0..debug_info_count {
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            4,
            &format!("debug_info[{index}].frame"),
        )?;
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("debug_info[{index}].user"),
        )?;
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("debug_info[{index}].text"),
        )?;
    }
    let debug_info_end = cursor;

    let tickmarks_count_offset = cursor;
    let tickmarks_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "tickmarks")?;
    let tickmarks_data_start = cursor;
    for index in 0..tickmarks_count {
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("tickmarks[{index}].description"),
        )?;
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            4,
            &format!("tickmarks[{index}].frame"),
        )?;
    }
    let tickmarks_end = cursor;

    let packages_count_offset = cursor;
    let packages_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "packages")?;
    let packages_data_start = cursor;
    for index in 0..packages_count {
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("packages[{index}]"),
        )?;
    }
    let packages_end = cursor;

    let objects_count_offset = cursor;
    let objects_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "objects")?;
    let objects_data_start = cursor;
    for index in 0..objects_count {
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("objects[{index}]"),
        )?;
    }
    let objects_end = cursor;

    let names_count_offset = cursor;
    let names_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "names")?;
    let names_data_start = cursor;
    for index in 0..names_count {
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("names[{index}]"),
        )?;
    }
    let names_end = cursor;

    let class_indices_count_offset = cursor;
    let class_indices_count =
        read_footer_scaffold_count(bytes, &mut cursor, content_end, "class indices")?;
    let class_indices_data_start = cursor;
    for index in 0..class_indices_count {
        skip_footer_scaffold_raw_string(
            bytes,
            &mut cursor,
            content_end,
            &format!("class_indices[{index}].class"),
        )?;
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            4,
            &format!("class_indices[{index}].index"),
        )?;
    }
    let class_indices_end = cursor;

    let net_cache_count_offset = cursor;
    let net_cache_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "net cache")?;
    let net_cache_data_start = cursor;
    let mut net_cache_properties_count = 0usize;
    for index in 0..net_cache_count {
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            12,
            &format!("net_cache[{index}] identity tuple"),
        )?;
        let property_count = read_footer_scaffold_count(
            bytes,
            &mut cursor,
            content_end,
            &format!("net_cache[{index}].properties"),
        )?;
        net_cache_properties_count = net_cache_properties_count
            .checked_add(property_count)
            .ok_or_else(|| {
                footer_scaffold_error("malformed", "net-cache property total overflows usize")
            })?;
        let property_bytes = property_count.checked_mul(8).ok_or_else(|| {
            footer_scaffold_error("malformed", "net-cache property byte length overflows usize")
        })?;
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            property_bytes,
            &format!("net_cache[{index}].properties"),
        )?;
    }
    let net_cache_end = cursor;
    let opaque_tail_start = cursor;
    let opaque_tail_size = content_end.saturating_sub(cursor);
    match opaque_tail_size {
        0 => {}
        4 => {
            let tail = take_footer_scaffold_bytes(
                bytes,
                &mut cursor,
                content_end,
                4,
                "opaque footer tail",
            )?;
            if tail != [0, 0, 0, 0] {
                return Err(footer_scaffold_error(
                    "unsupported-layout",
                    format!("observed four-byte opaque tail is non-zero: {tail:02X?}"),
                ));
            }
        }
        other => {
            return Err(footer_scaffold_error(
                "unsupported-layout",
                format!(
                    "known footer fields leave {other} opaque tail bytes; admitted observed forms are 0 or four zero bytes"
                ),
            ));
        }
    }
    if cursor != content_end {
        return Err(footer_scaffold_error(
            "malformed",
            "footer cursor did not reach content_end after admitted opaque tail",
        ));
    }

    Ok(ReplayFooterScaffoldV1 {
        content,
        debug_info_count_offset: footer_offset_u64(
            debug_info_count_offset,
            "debug_info_count_offset",
        )?,
        debug_info_count: footer_count_u32(debug_info_count, "debug_info_count")?,
        debug_info_data_start: footer_offset_u64(debug_info_data_start, "debug_info_data_start")?,
        debug_info_end: footer_offset_u64(debug_info_end, "debug_info_end")?,
        tickmarks_count_offset: footer_offset_u64(tickmarks_count_offset, "tickmarks_count_offset")?,
        tickmarks_count: footer_count_u32(tickmarks_count, "tickmarks_count")?,
        tickmarks_data_start: footer_offset_u64(tickmarks_data_start, "tickmarks_data_start")?,
        tickmarks_end: footer_offset_u64(tickmarks_end, "tickmarks_end")?,
        packages_count_offset: footer_offset_u64(packages_count_offset, "packages_count_offset")?,
        packages_count: footer_count_u32(packages_count, "packages_count")?,
        packages_data_start: footer_offset_u64(packages_data_start, "packages_data_start")?,
        packages_end: footer_offset_u64(packages_end, "packages_end")?,
        objects_count_offset: footer_offset_u64(objects_count_offset, "objects_count_offset")?,
        objects_count: footer_count_u32(objects_count, "objects_count")?,
        objects_data_start: footer_offset_u64(objects_data_start, "objects_data_start")?,
        objects_end: footer_offset_u64(objects_end, "objects_end")?,
        names_count_offset: footer_offset_u64(names_count_offset, "names_count_offset")?,
        names_count: footer_count_u32(names_count, "names_count")?,
        names_data_start: footer_offset_u64(names_data_start, "names_data_start")?,
        names_end: footer_offset_u64(names_end, "names_end")?,
        class_indices_count_offset: footer_offset_u64(
            class_indices_count_offset,
            "class_indices_count_offset",
        )?,
        class_indices_count: footer_count_u32(class_indices_count, "class_indices_count")?,
        class_indices_data_start: footer_offset_u64(
            class_indices_data_start,
            "class_indices_data_start",
        )?,
        class_indices_end: footer_offset_u64(class_indices_end, "class_indices_end")?,
        net_cache_count_offset: footer_offset_u64(net_cache_count_offset, "net_cache_count_offset")?,
        net_cache_count: footer_count_u32(net_cache_count, "net_cache_count")?,
        net_cache_data_start: footer_offset_u64(net_cache_data_start, "net_cache_data_start")?,
        net_cache_properties_count: footer_count_u32(
            net_cache_properties_count,
            "net_cache_properties_count",
        )?,
        net_cache_end: footer_offset_u64(net_cache_end, "net_cache_end")?,
        opaque_tail_start: footer_offset_u64(opaque_tail_start, "opaque_tail_start")?,
        opaque_tail_size: footer_count_u32(opaque_tail_size, "opaque_tail_size")?,
        footer_end: footer_offset_u64(content_end, "footer_end")?,
    })
}

fn read_footer_scaffold_count(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<usize> {
    let value = read_footer_scaffold_i32(bytes, cursor, content_end, &format!("{context} count"))?;
    if value < 0 {
        return Err(footer_scaffold_error(
            "malformed",
            format!("{context} count {value} is negative"),
        ));
    }
    if value > MAX_CONTENT_SCAFFOLD_LIST_ITEMS {
        return Err(footer_scaffold_error(
            "malformed",
            format!(
                "{context} count {value} exceeds structural bound {MAX_CONTENT_SCAFFOLD_LIST_ITEMS}"
            ),
        ));
    }
    usize::try_from(value).map_err(|_| {
        footer_scaffold_error(
            "malformed",
            format!("{context} count {value} cannot fit usize"),
        )
    })
}

fn read_footer_scaffold_i32(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<i32> {
    let raw = take_footer_scaffold_bytes(bytes, cursor, content_end, 4, context)?;
    Ok(i32::from_le_bytes(
        raw.try_into().expect("footer scaffold read exactly four bytes"),
    ))
}

fn skip_footer_scaffold_unreal_text(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<()> {
    let units = read_footer_scaffold_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if !(-MAX_CONTENT_SCAFFOLD_TEXT_UNITS..=MAX_CONTENT_SCAFFOLD_TEXT_UNITS).contains(&units) {
        return Err(footer_scaffold_error(
            "malformed",
            format!(
                "{context} text length {units} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let unit_count = usize::try_from(units.unsigned_abs()).map_err(|_| {
        footer_scaffold_error(
            "malformed",
            format!("{context} text length {units} cannot fit usize"),
        )
    })?;
    let byte_len = if units < 0 {
        unit_count.checked_mul(2).ok_or_else(|| {
            footer_scaffold_error(
                "malformed",
                format!("{context} UTF-16 byte length overflows"),
            )
        })?
    } else {
        unit_count
    };
    skip_footer_scaffold_bytes(bytes, cursor, content_end, byte_len, context)
}

fn skip_footer_scaffold_raw_string(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<()> {
    let byte_len_i32 =
        read_footer_scaffold_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if byte_len_i32 < 0 {
        return Err(footer_scaffold_error(
            "malformed",
            format!("{context} raw string length {byte_len_i32} is negative"),
        ));
    }
    if byte_len_i32 > MAX_CONTENT_SCAFFOLD_TEXT_UNITS {
        return Err(footer_scaffold_error(
            "malformed",
            format!(
                "{context} raw string length {byte_len_i32} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let byte_len = usize::try_from(byte_len_i32).map_err(|_| {
        footer_scaffold_error(
            "malformed",
            format!("{context} raw string length cannot fit usize"),
        )
    })?;
    skip_footer_scaffold_bytes(bytes, cursor, content_end, byte_len, context)
}

fn skip_footer_scaffold_bytes(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    len: usize,
    context: &str,
) -> Result<()> {
    take_footer_scaffold_bytes(bytes, cursor, content_end, len, context)?;
    Ok(())
}

fn take_footer_scaffold_bytes<'a>(
    bytes: &'a [u8],
    cursor: &mut usize,
    content_end: usize,
    len: usize,
    context: &str,
) -> Result<&'a [u8]> {
    let end = cursor.checked_add(len).ok_or_else(|| {
        footer_scaffold_error(
            "malformed",
            format!("{context} length {len} overflows cursor"),
        )
    })?;
    if end > content_end || end > bytes.len() {
        return Err(footer_scaffold_error(
            "insufficient",
            format!(
                "{context} needs {len} bytes at offset {}, content ends at {content_end}",
                *cursor
            ),
        ));
    }
    let start = *cursor;
    *cursor = end;
    Ok(&bytes[start..end])
}

fn footer_offset_u64(value: usize, context: &str) -> Result<u64> {
    u64::try_from(value)
        .map_err(|_| footer_scaffold_error("malformed", format!("{context} cannot fit u64")))
}

fn footer_count_u32(value: usize, context: &str) -> Result<u32> {
    u32::try_from(value)
        .map_err(|_| footer_scaffold_error("malformed", format!("{context} cannot fit u32")))
}

'''
    text = insert_before(
        text,
        "fn parse_replay_header_from_memory(label: &str, bytes: &[u8]) -> Result<ReplayHeader> {",
        implementation,
    )

    error_helper = r'''
fn footer_scaffold_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay footer scaffold error: {category}: {}",
        detail.into()
    ))
}

'''
    text = insert_before(
        text,
        "fn content_scaffold_error(category: &str, detail: impl Into<String>) -> MimirError {",
        error_helper,
    )

    tests = r'''
    fn build_minimal_footer_content(tail: &[u8]) -> Vec<u8> {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes()); // levels
        content.extend_from_slice(&0i32.to_le_bytes()); // keyframes
        content.extend_from_slice(&0i32.to_le_bytes()); // network size
        content.extend_from_slice(&0i32.to_le_bytes()); // debug info
        content.extend_from_slice(&0i32.to_le_bytes()); // tickmarks
        content.extend_from_slice(&0i32.to_le_bytes()); // packages
        content.extend_from_slice(&0i32.to_le_bytes()); // objects
        content.extend_from_slice(&0i32.to_le_bytes()); // names
        content.extend_from_slice(&0i32.to_le_bytes()); // class indices
        content.extend_from_slice(&0i32.to_le_bytes()); // net cache
        content.extend_from_slice(tail);
        content
    }

    fn build_footer_replay(content: Vec<u8>) -> ReplayInput {
        let content_size = i32::try_from(content.len()).expect("synthetic footer content fits i32");
        ReplayInput::Memory {
            label: "synthetic-footer".to_string(),
            bytes: build_body_boundary_bytes(&[], 0xA1B2C3D4, content_size, &content),
        }
    }

    #[test]
    fn minimal_footer_scaffold_reader_matches_three_historical_fixtures() {
        let cases = [
            (
                FIXTURE_001_PATH,
                FIXTURE_001_LABEL,
                0u32,
                16u32,
                3u32,
                398u32,
                416u32,
                41u32,
                36u32,
                301u32,
                3_001_017u64,
                4u32,
                3_001_021u64,
            ),
            (
                FIXTURE_002_PATH,
                FIXTURE_002_LABEL,
                0u32,
                8u32,
                6u32,
                429u32,
                344u32,
                43u32,
                38u32,
                327u32,
                2_632_899u64,
                4u32,
                2_632_903u64,
            ),
            (
                FIXTURE_003_PATH,
                FIXTURE_003_LABEL,
                0u32,
                16u32,
                8u32,
                433u32,
                351u32,
                42u32,
                37u32,
                335u32,
                1_638_534u64,
                4u32,
                1_638_538u64,
            ),
        ];

        for (
            path,
            label,
            debug_info_count,
            tickmarks_count,
            packages_count,
            objects_count,
            names_count,
            class_indices_count,
            net_cache_count,
            net_cache_properties_count,
            known_footer_end,
            opaque_tail_size,
            footer_end,
        ) in cases
        {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let scaffold = MinimalReplayFooterScaffoldReader
                .read_footer_scaffold(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical fixture footer scaffold should be structurally valid");

            assert_eq!(scaffold.debug_info_count, debug_info_count);
            assert_eq!(scaffold.tickmarks_count, tickmarks_count);
            assert_eq!(scaffold.packages_count, packages_count);
            assert_eq!(scaffold.objects_count, objects_count);
            assert_eq!(scaffold.names_count, names_count);
            assert_eq!(scaffold.class_indices_count, class_indices_count);
            assert_eq!(scaffold.net_cache_count, net_cache_count);
            assert_eq!(
                scaffold.net_cache_properties_count,
                net_cache_properties_count
            );
            assert_eq!(scaffold.net_cache_end, known_footer_end);
            assert_eq!(scaffold.opaque_tail_start, known_footer_end);
            assert_eq!(scaffold.opaque_tail_size, opaque_tail_size);
            assert_eq!(scaffold.footer_end, footer_end);
            assert_eq!(scaffold.footer_end, scaffold.content.boundary.content_end);
            assert_eq!(scaffold.content.boundary.content_crc, scaffold.content.boundary.content_crc);
        }
    }

    #[test]
    fn minimal_footer_scaffold_reader_frames_checked_in_largest_100_corpus() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 footer-scaffold regression; corpus root is absent");
            return;
        }
        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| entry.expect("corpus directory entry should be readable").path())
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        replay_paths.sort();
        assert_eq!(replay_paths.len(), 100);

        let mut empty_tail = 0usize;
        let mut zero_word_tail = 0usize;
        for path in replay_paths {
            let bytes = fs::read(&path).expect("checked-in corpus replay should be readable");
            let label = path
                .file_name()
                .expect("corpus replay should have a file name")
                .to_string_lossy()
                .into_owned();
            let scaffold = MinimalReplayFooterScaffoldReader
                .read_footer_scaffold(&ReplayInput::Memory {
                    label: label.clone(),
                    bytes,
                })
                .unwrap_or_else(|error| panic!("footer scaffold failed for {label}: {error}"));
            assert_eq!(scaffold.footer_end, scaffold.content.boundary.content_end);
            assert_eq!(scaffold.opaque_tail_start, scaffold.net_cache_end);
            match scaffold.opaque_tail_size {
                0 => empty_tail += 1,
                4 => zero_word_tail += 1,
                other => panic!("unexpected admitted opaque tail size {other} for {label}"),
            }
        }
        assert_eq!(empty_tail, 1);
        assert_eq!(zero_word_tail, 99);
    }

    #[test]
    fn minimal_footer_scaffold_reader_accepts_observed_empty_tail() {
        let content = build_minimal_footer_content(&[]);
        let scaffold = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect("empty opaque footer tail is an observed admitted form");
        assert_eq!(scaffold.opaque_tail_size, 0);
        assert_eq!(scaffold.net_cache_end, scaffold.footer_end);
        assert_eq!(scaffold.content.boundary.content_crc, 0xA1B2C3D4);
    }

    #[test]
    fn minimal_footer_scaffold_reader_accepts_observed_zero_word_tail() {
        let content = build_minimal_footer_content(&[0, 0, 0, 0]);
        let scaffold = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect("four zero opaque footer bytes are an observed admitted form");
        assert_eq!(scaffold.opaque_tail_size, 4);
        assert_eq!(scaffold.opaque_tail_start + 4, scaffold.footer_end);
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_nonzero_four_byte_tail() {
        let content = build_minimal_footer_content(&[1, 0, 0, 0]);
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("non-zero four-byte footer tail is outside observed layout admission");
        assert_error_contains(error, "replay footer scaffold error: unsupported-layout");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_unobserved_tail_length() {
        let content = build_minimal_footer_content(&[0]);
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("one-byte footer tail is outside observed layout admission");
        assert_error_contains(error, "replay footer scaffold error: unsupported-layout");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_file_input() {
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside the footer-scaffold reader");
        assert_error_contains(error, "replay footer scaffold error: unsupported-input");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_negative_debug_info_count() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("negative footer list counts are malformed");
        assert_error_contains(error, "replay footer scaffold error: malformed");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_truncated_debug_info_entry() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&7i32.to_le_bytes());
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("debug-info entry without user text length is truncated");
        assert_error_contains(error, "replay footer scaffold error: insufficient");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_negative_class_index_string_length() {
        let mut content = build_minimal_footer_content(&[]);
        content.truncate(12 + 5 * 4);
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("negative class-index raw string length is malformed");
        assert_error_contains(error, "replay footer scaffold error: malformed");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_negative_net_cache_property_count() {
        let mut content = build_minimal_footer_content(&[]);
        content.truncate(12 + 6 * 4);
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("negative net-cache property count is malformed");
        assert_error_contains(error, "replay footer scaffold error: malformed");
    }

'''
    text = insert_before(
        text,
        "    #[test]\n    fn unsupported_reader_fails_explicitly() {",
        tests,
    )

    PATH.write_text(text, encoding="utf-8")
    print("PASS: applied R3.6 footer scaffold reader patch to crates/mimir-replay/src/lib.rs")


if __name__ == "__main__":
    main()
