from __future__ import annotations

from pathlib import Path

PATH = Path("crates/mimir-replay/src/lib.rs")


def insert_before(text: str, marker: str, insertion: str) -> str:
    count = text.count(marker)
    if count != 1:
        raise RuntimeError(f"expected exactly one marker, found {count}: {marker[:100]!r}")
    return text.replace(marker, insertion + marker, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    if "ReplayFooterLookupMaterializationV1" in text:
        raise RuntimeError("R3.8 footer lookup materializer already present")

    public_api = r'''
/// Raw class-index row materialized from the replay footer.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayClassIndexV1 {
    pub class_name: String,
    pub object_index: u32,
}

/// Raw network-cache property row materialized from the replay footer.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetCachePropertyV1 {
    pub object_index: u32,
    pub stream_id: u32,
}

/// Raw network-cache row materialized from the replay footer.
///
/// `parent_id` and `cache_id` are intentionally preserved as opaque signed values.
/// This pass does not treat them as hierarchy identifiers or uniqueness predicates.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetCacheEntryV1 {
    pub object_index: u32,
    pub parent_id: i32,
    pub cache_id: i32,
    pub properties: Vec<ReplayNetCachePropertyV1>,
}

/// Typed raw lookup tables from the replay footer.
///
/// This is not a network decoder and not an inheritance/attribute resolver. It materializes
/// only the raw object/name/class-index/net-cache tables proven by the checked-in evidence.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayFooterLookupMaterializationV1 {
    pub scaffold: ReplayFooterScaffoldV1,
    pub objects: Vec<String>,
    pub names: Vec<String>,
    pub class_indices: Vec<ReplayClassIndexV1>,
    pub net_cache: Vec<ReplayNetCacheEntryV1>,
}

pub trait ReplayFooterLookupMaterializationReader {
    fn read_footer_lookup_materialization(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayFooterLookupMaterializationV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayFooterLookupMaterializationReader;

impl ReplayFooterLookupMaterializationReader for MinimalReplayFooterLookupMaterializationReader {
    fn read_footer_lookup_materialization(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayFooterLookupMaterializationV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_footer_lookup_materialization_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(footer_lookup_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the footer lookup materializer: {}",
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
fn parse_replay_footer_lookup_materialization_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayFooterLookupMaterializationV1> {
    let scaffold = parse_replay_footer_scaffold_from_memory(label, bytes)?;
    let content_end = lookup_offset_usize(scaffold.content.boundary.content_end, "content_end")?;

    let mut objects_cursor = lookup_offset_usize(scaffold.objects_count_offset, "objects_count_offset")?;
    let objects_count = read_footer_lookup_count(bytes, &mut objects_cursor, content_end, "objects")?;
    require_lookup_count(objects_count, scaffold.objects_count, "objects")?;
    let mut objects = Vec::with_capacity(objects_count);
    for index in 0..objects_count {
        objects.push(read_footer_lookup_unreal_text(
            bytes,
            &mut objects_cursor,
            content_end,
            &format!("objects[{index}]"),
        )?);
    }
    require_lookup_cursor(
        objects_cursor,
        scaffold.objects_end,
        "objects_end",
    )?;

    let mut names_cursor = lookup_offset_usize(scaffold.names_count_offset, "names_count_offset")?;
    let names_count = read_footer_lookup_count(bytes, &mut names_cursor, content_end, "names")?;
    require_lookup_count(names_count, scaffold.names_count, "names")?;
    let mut names = Vec::with_capacity(names_count);
    for index in 0..names_count {
        names.push(read_footer_lookup_unreal_text(
            bytes,
            &mut names_cursor,
            content_end,
            &format!("names[{index}]"),
        )?);
    }
    require_lookup_cursor(names_cursor, scaffold.names_end, "names_end")?;

    let mut class_cursor =
        lookup_offset_usize(scaffold.class_indices_count_offset, "class_indices_count_offset")?;
    let class_count = read_footer_lookup_count(bytes, &mut class_cursor, content_end, "class indices")?;
    require_lookup_count(class_count, scaffold.class_indices_count, "class indices")?;
    let mut class_indices = Vec::with_capacity(class_count);
    for index in 0..class_count {
        let class_name = read_footer_lookup_raw_utf8_string(
            bytes,
            &mut class_cursor,
            content_end,
            &format!("class_indices[{index}].class"),
        )?;
        let object_index_i32 = read_footer_lookup_i32(
            bytes,
            &mut class_cursor,
            content_end,
            &format!("class_indices[{index}].index"),
        )?;
        let object_index = lookup_index_u32(
            object_index_i32,
            objects.len(),
            &format!("class_indices[{index}].index"),
        )?;
        let object_name = &objects[object_index as usize];
        if object_name != &class_name {
            return Err(footer_lookup_error(
                "mapping",
                format!(
                    "class_indices[{index}] class {class_name:?} does not match objects[{object_index}] {object_name:?}"
                ),
            ));
        }
        class_indices.push(ReplayClassIndexV1 {
            class_name,
            object_index,
        });
    }
    require_lookup_cursor(
        class_cursor,
        scaffold.class_indices_end,
        "class_indices_end",
    )?;

    let mut cache_cursor =
        lookup_offset_usize(scaffold.net_cache_count_offset, "net_cache_count_offset")?;
    let cache_count = read_footer_lookup_count(bytes, &mut cache_cursor, content_end, "net cache")?;
    require_lookup_count(cache_count, scaffold.net_cache_count, "net cache")?;
    let mut net_cache = Vec::with_capacity(cache_count);
    let mut total_properties = 0usize;
    for index in 0..cache_count {
        let object_index_i32 = read_footer_lookup_i32(
            bytes,
            &mut cache_cursor,
            content_end,
            &format!("net_cache[{index}].object_ind"),
        )?;
        let object_index = lookup_index_u32(
            object_index_i32,
            objects.len(),
            &format!("net_cache[{index}].object_ind"),
        )?;
        let parent_id = read_footer_lookup_i32(
            bytes,
            &mut cache_cursor,
            content_end,
            &format!("net_cache[{index}].parent_id"),
        )?;
        let cache_id = read_footer_lookup_i32(
            bytes,
            &mut cache_cursor,
            content_end,
            &format!("net_cache[{index}].cache_id"),
        )?;
        let property_count = read_footer_lookup_count(
            bytes,
            &mut cache_cursor,
            content_end,
            &format!("net_cache[{index}].properties"),
        )?;
        total_properties = total_properties.checked_add(property_count).ok_or_else(|| {
            footer_lookup_error("malformed", "net-cache property total overflows usize")
        })?;
        let mut properties = Vec::with_capacity(property_count);
        for property_index in 0..property_count {
            let property_object_i32 = read_footer_lookup_i32(
                bytes,
                &mut cache_cursor,
                content_end,
                &format!("net_cache[{index}].properties[{property_index}].object_ind"),
            )?;
            let property_object_index = lookup_index_u32(
                property_object_i32,
                objects.len(),
                &format!("net_cache[{index}].properties[{property_index}].object_ind"),
            )?;
            let stream_id_i32 = read_footer_lookup_i32(
                bytes,
                &mut cache_cursor,
                content_end,
                &format!("net_cache[{index}].properties[{property_index}].stream_id"),
            )?;
            if stream_id_i32 < 0 {
                return Err(footer_lookup_error(
                    "mapping",
                    format!(
                        "net_cache[{index}].properties[{property_index}].stream_id {stream_id_i32} is negative"
                    ),
                ));
            }
            let stream_id = u32::try_from(stream_id_i32).map_err(|_| {
                footer_lookup_error(
                    "mapping",
                    format!(
                        "net_cache[{index}].properties[{property_index}].stream_id {stream_id_i32} cannot fit u32"
                    ),
                )
            })?;
            properties.push(ReplayNetCachePropertyV1 {
                object_index: property_object_index,
                stream_id,
            });
        }
        net_cache.push(ReplayNetCacheEntryV1 {
            object_index,
            parent_id,
            cache_id,
            properties,
        });
    }
    require_lookup_count(
        total_properties,
        scaffold.net_cache_properties_count,
        "net-cache properties total",
    )?;
    require_lookup_cursor(cache_cursor, scaffold.net_cache_end, "net_cache_end")?;

    Ok(ReplayFooterLookupMaterializationV1 {
        scaffold,
        objects,
        names,
        class_indices,
        net_cache,
    })
}

fn read_footer_lookup_count(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<usize> {
    let value = read_footer_lookup_i32(bytes, cursor, content_end, &format!("{context} count"))?;
    if value < 0 {
        return Err(footer_lookup_error(
            "malformed",
            format!("{context} count {value} is negative"),
        ));
    }
    if value > MAX_CONTENT_SCAFFOLD_LIST_ITEMS {
        return Err(footer_lookup_error(
            "malformed",
            format!(
                "{context} count {value} exceeds structural bound {MAX_CONTENT_SCAFFOLD_LIST_ITEMS}"
            ),
        ));
    }
    usize::try_from(value).map_err(|_| {
        footer_lookup_error(
            "malformed",
            format!("{context} count {value} cannot fit usize"),
        )
    })
}

fn read_footer_lookup_i32(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<i32> {
    let raw = take_footer_lookup_bytes(bytes, cursor, content_end, 4, context)?;
    Ok(i32::from_le_bytes(
        raw.try_into().expect("footer lookup read exactly four bytes"),
    ))
}

fn read_footer_lookup_unreal_text(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<String> {
    let units = read_footer_lookup_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if units < 0 {
        return Err(footer_lookup_error(
            "unsupported-text",
            format!(
                "{context} uses negative-length UTF-16 text; R3.8 lookup admission covers only observed non-negative Windows-1252 text"
            ),
        ));
    }
    if units > MAX_CONTENT_SCAFFOLD_TEXT_UNITS {
        return Err(footer_lookup_error(
            "malformed",
            format!(
                "{context} length {units} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let byte_len = usize::try_from(units).map_err(|_| {
        footer_lookup_error(
            "malformed",
            format!("{context} length {units} cannot fit usize"),
        )
    })?;
    if byte_len == 0 {
        return Ok(String::new());
    }
    let raw = take_footer_lookup_bytes(bytes, cursor, content_end, byte_len, context)?;
    if raw.last() != Some(&0) {
        return Err(footer_lookup_error(
            "malformed",
            format!("{context} is missing trailing NUL"),
        ));
    }
    decode_footer_lookup_windows1252(&raw[..raw.len() - 1], context)
}

fn read_footer_lookup_raw_utf8_string(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<String> {
    let byte_len_i32 =
        read_footer_lookup_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if byte_len_i32 <= 0 {
        return Err(footer_lookup_error(
            "malformed",
            format!("{context} raw string length {byte_len_i32} must be positive"),
        ));
    }
    if byte_len_i32 > MAX_CONTENT_SCAFFOLD_TEXT_UNITS {
        return Err(footer_lookup_error(
            "malformed",
            format!(
                "{context} raw string length {byte_len_i32} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let byte_len = usize::try_from(byte_len_i32).map_err(|_| {
        footer_lookup_error(
            "malformed",
            format!("{context} raw string length cannot fit usize"),
        )
    })?;
    let raw = take_footer_lookup_bytes(bytes, cursor, content_end, byte_len, context)?;
    if raw.last() != Some(&0) {
        return Err(footer_lookup_error(
            "malformed",
            format!("{context} raw string is missing trailing NUL"),
        ));
    }
    std::str::from_utf8(&raw[..raw.len() - 1])
        .map(str::to_owned)
        .map_err(|error| {
            footer_lookup_error(
                "malformed",
                format!("{context} raw string is not UTF-8: {error}"),
            )
        })
}

fn decode_footer_lookup_windows1252(bytes: &[u8], context: &str) -> Result<String> {
    let mut decoded = String::with_capacity(bytes.len());
    for &byte in bytes {
        let character = match byte {
            0x00..=0x7F => char::from(byte),
            0x80 => '\u{20AC}',
            0x82 => '\u{201A}',
            0x83 => '\u{0192}',
            0x84 => '\u{201E}',
            0x85 => '\u{2026}',
            0x86 => '\u{2020}',
            0x87 => '\u{2021}',
            0x88 => '\u{02C6}',
            0x89 => '\u{2030}',
            0x8A => '\u{0160}',
            0x8B => '\u{2039}',
            0x8C => '\u{0152}',
            0x8E => '\u{017D}',
            0x91 => '\u{2018}',
            0x92 => '\u{2019}',
            0x93 => '\u{201C}',
            0x94 => '\u{201D}',
            0x95 => '\u{2022}',
            0x96 => '\u{2013}',
            0x97 => '\u{2014}',
            0x98 => '\u{02DC}',
            0x99 => '\u{2122}',
            0x9A => '\u{0161}',
            0x9B => '\u{203A}',
            0x9C => '\u{0153}',
            0x9E => '\u{017E}',
            0x9F => '\u{0178}',
            0x81 | 0x8D | 0x8F | 0x90 | 0x9D => {
                return Err(footer_lookup_error(
                    "malformed",
                    format!("{context} contains undefined Windows-1252 byte 0x{byte:02X}"),
                ));
            }
            _ => char::from(byte),
        };
        decoded.push(character);
    }
    Ok(decoded)
}

fn take_footer_lookup_bytes<'a>(
    bytes: &'a [u8],
    cursor: &mut usize,
    content_end: usize,
    len: usize,
    context: &str,
) -> Result<&'a [u8]> {
    let end = cursor.checked_add(len).ok_or_else(|| {
        footer_lookup_error(
            "malformed",
            format!("{context} length {len} overflows cursor"),
        )
    })?;
    if end > content_end || end > bytes.len() {
        return Err(footer_lookup_error(
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

fn lookup_index_u32(value: i32, object_count: usize, context: &str) -> Result<u32> {
    if value < 0 {
        return Err(footer_lookup_error(
            "mapping",
            format!("{context} {value} is negative"),
        ));
    }
    let index = usize::try_from(value).map_err(|_| {
        footer_lookup_error("mapping", format!("{context} {value} cannot fit usize"))
    })?;
    if index >= object_count {
        return Err(footer_lookup_error(
            "mapping",
            format!(
                "{context} {value} is outside objects length {object_count}"
            ),
        ));
    }
    u32::try_from(index).map_err(|_| {
        footer_lookup_error("mapping", format!("{context} {value} cannot fit u32"))
    })
}

fn lookup_offset_usize(value: u64, context: &str) -> Result<usize> {
    usize::try_from(value).map_err(|_| {
        footer_lookup_error("malformed", format!("{context} {value} cannot fit usize"))
    })
}

fn require_lookup_count(actual: usize, expected: u32, context: &str) -> Result<()> {
    let expected = usize::try_from(expected).map_err(|_| {
        footer_lookup_error(
            "malformed",
            format!("{context} scaffold count {expected} cannot fit usize"),
        )
    })?;
    if actual == expected {
        Ok(())
    } else {
        Err(footer_lookup_error(
            "mapping",
            format!(
                "{context} materialized count {actual} does not match scaffold count {expected}"
            ),
        ))
    }
}

fn require_lookup_cursor(actual: usize, expected: u64, context: &str) -> Result<()> {
    let expected = lookup_offset_usize(expected, context)?;
    if actual == expected {
        Ok(())
    } else {
        Err(footer_lookup_error(
            "mapping",
            format!(
                "{context} materialization cursor {actual} does not match scaffold boundary {expected}"
            ),
        ))
    }
}

'''
    text = insert_before(
        text,
        "fn parse_replay_header_from_memory(label: &str, bytes: &[u8]) -> Result<ReplayHeader> {",
        implementation,
    )

    error_helper = r'''
fn footer_lookup_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay footer lookup error: {category}: {}",
        detail.into()
    ))
}

'''
    text = insert_before(
        text,
        "fn footer_scaffold_error(category: &str, detail: impl Into<String>) -> MimirError {",
        error_helper,
    )

    tests = r'''
    fn push_lookup_unreal_text(content: &mut Vec<u8>, payload_without_nul: &[u8]) {
        let len = i32::try_from(payload_without_nul.len() + 1).expect("synthetic text fits i32");
        content.extend_from_slice(&len.to_le_bytes());
        content.extend_from_slice(payload_without_nul);
        content.push(0);
    }

    fn push_lookup_raw_utf8(content: &mut Vec<u8>, value: &str) {
        let len = i32::try_from(value.len() + 1).expect("synthetic raw string fits i32");
        content.extend_from_slice(&len.to_le_bytes());
        content.extend_from_slice(value.as_bytes());
        content.push(0);
    }

    fn build_lookup_footer_content() -> Vec<u8> {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes()); // levels
        content.extend_from_slice(&0i32.to_le_bytes()); // keyframes
        content.extend_from_slice(&0i32.to_le_bytes()); // network size
        content.extend_from_slice(&0i32.to_le_bytes()); // debug info
        content.extend_from_slice(&0i32.to_le_bytes()); // tickmarks
        content.extend_from_slice(&0i32.to_le_bytes()); // packages

        content.extend_from_slice(&2i32.to_le_bytes()); // objects
        push_lookup_unreal_text(&mut content, b"Core.Object");
        push_lookup_unreal_text(&mut content, b"TAGame.Vehicle_TA");

        content.extend_from_slice(&1i32.to_le_bytes()); // names
        push_lookup_unreal_text(&mut content, &[b'E', 0x80]);

        content.extend_from_slice(&1i32.to_le_bytes()); // class indices
        push_lookup_raw_utf8(&mut content, "Core.Object");
        content.extend_from_slice(&0i32.to_le_bytes());

        content.extend_from_slice(&2i32.to_le_bytes()); // net cache
        content.extend_from_slice(&0i32.to_le_bytes()); // object_ind
        content.extend_from_slice(&40i32.to_le_bytes()); // opaque unresolved parent_id
        content.extend_from_slice(&23i32.to_le_bytes()); // duplicate cache_id admitted
        content.extend_from_slice(&1i32.to_le_bytes()); // properties
        content.extend_from_slice(&1i32.to_le_bytes()); // property object_ind
        content.extend_from_slice(&5i32.to_le_bytes()); // stream_id

        content.extend_from_slice(&1i32.to_le_bytes()); // object_ind
        content.extend_from_slice(&40i32.to_le_bytes()); // same unresolved parent_id
        content.extend_from_slice(&23i32.to_le_bytes()); // same cache_id
        content.extend_from_slice(&0i32.to_le_bytes()); // properties
        content.extend_from_slice(&[0, 0, 0, 0]); // observed opaque tail
        content
    }

    #[test]
    fn minimal_footer_lookup_materializer_matches_three_historical_fixtures() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let lookup = MinimalReplayFooterLookupMaterializationReader
                .read_footer_lookup_materialization(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical footer lookup tables should materialize");
            assert_eq!(lookup.objects.len(), lookup.scaffold.objects_count as usize);
            assert_eq!(lookup.names.len(), lookup.scaffold.names_count as usize);
            assert_eq!(
                lookup.class_indices.len(),
                lookup.scaffold.class_indices_count as usize
            );
            assert_eq!(lookup.net_cache.len(), lookup.scaffold.net_cache_count as usize);
            let property_total: usize = lookup.net_cache.iter().map(|entry| entry.properties.len()).sum();
            assert_eq!(
                property_total,
                lookup.scaffold.net_cache_properties_count as usize
            );
            for class_index in &lookup.class_indices {
                assert_eq!(
                    class_index.class_name,
                    lookup.objects[class_index.object_index as usize]
                );
            }
            for entry in &lookup.net_cache {
                assert!((entry.object_index as usize) < lookup.objects.len());
                for property in &entry.properties {
                    assert!((property.object_index as usize) < lookup.objects.len());
                }
            }
        }
    }

    #[test]
    fn minimal_footer_lookup_materializer_matches_checked_in_largest_100_corpus() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 footer-lookup regression; corpus root is absent");
            return;
        }
        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| entry.expect("corpus directory entry should be readable").path())
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        replay_paths.sort();
        assert_eq!(replay_paths.len(), 100);

        for path in replay_paths {
            let bytes = fs::read(&path).expect("checked-in corpus replay should be readable");
            let label = path
                .file_name()
                .expect("corpus replay should have a file name")
                .to_string_lossy()
                .into_owned();
            let lookup = MinimalReplayFooterLookupMaterializationReader
                .read_footer_lookup_materialization(&ReplayInput::Memory {
                    label: label.clone(),
                    bytes,
                })
                .unwrap_or_else(|error| panic!("footer lookup failed for {label}: {error}"));
            assert_eq!(lookup.objects.len(), lookup.scaffold.objects_count as usize);
            assert_eq!(lookup.names.len(), lookup.scaffold.names_count as usize);
            assert_eq!(
                lookup.class_indices.len(),
                lookup.scaffold.class_indices_count as usize
            );
            assert_eq!(lookup.net_cache.len(), lookup.scaffold.net_cache_count as usize);
            for class_index in &lookup.class_indices {
                assert_eq!(
                    class_index.class_name,
                    lookup.objects[class_index.object_index as usize]
                );
            }
            for entry in &lookup.net_cache {
                assert!((entry.object_index as usize) < lookup.objects.len());
                for property in &entry.properties {
                    assert!((property.object_index as usize) < lookup.objects.len());
                }
            }
        }
    }

    #[test]
    fn minimal_footer_lookup_materializer_preserves_opaque_cache_and_parent_ids() {
        let lookup = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(build_lookup_footer_content()))
            .expect("duplicate cache_id and unresolved parent_id are raw fields, not rejection predicates");
        assert_eq!(lookup.objects, ["Core.Object", "TAGame.Vehicle_TA"]);
        assert_eq!(lookup.names, ["E€"]);
        assert_eq!(lookup.net_cache.len(), 2);
        assert_eq!(lookup.net_cache[0].parent_id, 40);
        assert_eq!(lookup.net_cache[1].parent_id, 40);
        assert_eq!(lookup.net_cache[0].cache_id, 23);
        assert_eq!(lookup.net_cache[1].cache_id, 23);
        assert_eq!(lookup.net_cache[0].properties[0].stream_id, 5);
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_file_input() {
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside footer lookup materialization");
        assert_error_contains(error, "replay footer lookup error: unsupported-input");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_utf16_object_text() {
        let mut content = build_lookup_footer_content();
        let objects_count_offset = 24usize;
        let object_text_offset = objects_count_offset + 4;
        content[object_text_offset..object_text_offset + 4]
            .copy_from_slice(&(-2i32).to_le_bytes());
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("R3.8 lookup admission does not claim UTF-16 object text");
        assert_error_contains(error, "replay footer lookup error: unsupported-text");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_missing_object_nul() {
        let mut content = build_lookup_footer_content();
        let objects_count_offset = 24usize;
        let object_text_offset = objects_count_offset + 4;
        let object_len = i32::from_le_bytes(
            content[object_text_offset..object_text_offset + 4]
                .try_into()
                .unwrap(),
        ) as usize;
        let last = object_text_offset + 4 + object_len - 1;
        content[last] = b'X';
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("lookup Unreal text requires trailing NUL");
        assert_error_contains(error, "replay footer lookup error: malformed");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_undefined_windows1252_byte() {
        let mut content = build_lookup_footer_content();
        let objects_count_offset = 24usize;
        let object_text_offset = objects_count_offset + 4;
        content[object_text_offset + 4] = 0x81;
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("undefined Windows-1252 bytes are malformed lookup text");
        assert_error_contains(error, "replay footer lookup error: malformed");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_class_index_name_mismatch() {
        let mut content = build_lookup_footer_content();
        let needle = b"Core.Object\0";
        let positions = content
            .windows(needle.len())
            .enumerate()
            .filter_map(|(index, window)| (window == needle).then_some(index))
            .collect::<Vec<_>>();
        assert_eq!(positions.len(), 2);
        let class_name_start = positions[1];
        content[class_name_start] = b'X';
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("class-index class names must match objects[index]");
        assert_error_contains(error, "replay footer lookup error: mapping");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_negative_class_index() {
        let mut content = build_lookup_footer_content();
        let needle = b"Core.Object\0";
        let positions = content
            .windows(needle.len())
            .enumerate()
            .filter_map(|(index, window)| (window == needle).then_some(index))
            .collect::<Vec<_>>();
        let class_name_start = positions[1];
        let index_offset = class_name_start + needle.len();
        content[index_offset..index_offset + 4].copy_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("negative class-index object indices are invalid mappings");
        assert_error_contains(error, "replay footer lookup error: mapping");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_out_of_bounds_net_cache_object() {
        let mut content = build_lookup_footer_content();
        let tail_start = content.len() - 4;
        let second_entry_size = 16usize;
        let first_entry_size = 24usize;
        let net_cache_start = tail_start - second_entry_size - first_entry_size - 4;
        let first_object_offset = net_cache_start + 4;
        content[first_object_offset..first_object_offset + 4].copy_from_slice(&99i32.to_le_bytes());
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("net-cache object indices must resolve into objects");
        assert_error_contains(error, "replay footer lookup error: mapping");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_negative_stream_id() {
        let mut content = build_lookup_footer_content();
        let tail_start = content.len() - 4;
        let second_entry_size = 16usize;
        let first_entry_size = 24usize;
        let net_cache_start = tail_start - second_entry_size - first_entry_size - 4;
        let first_stream_id_offset = net_cache_start + 4 + 16 + 4;
        content[first_stream_id_offset..first_stream_id_offset + 4]
            .copy_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("negative stream ids are outside raw lookup admission");
        assert_error_contains(error, "replay footer lookup error: mapping");
    }

'''
    text = insert_before(
        text,
        "    #[test]\n    fn unsupported_reader_fails_explicitly() {",
        tests,
    )

    PATH.write_text(text, encoding="utf-8")
    print("PASS: applied R3.8 raw footer lookup materializer patch")


if __name__ == "__main__":
    main()
