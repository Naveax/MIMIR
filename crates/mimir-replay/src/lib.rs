use mimir_core::{MimirError, Result};
use mimir_types::{FieldValue, Metadata, ReplayId};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayInput {
    File(PathBuf),
    Memory { label: String, bytes: Vec<u8> },
}

impl ReplayInput {
    pub fn file(path: impl Into<PathBuf>) -> Self {
        Self::File(path.into())
    }

    pub fn label(&self) -> String {
        match self {
            Self::File(path) => path
                .file_name()
                .map(|value| value.to_string_lossy().into_owned())
                .unwrap_or_else(|| path.display().to_string()),
            Self::Memory { label, .. } => label.clone(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayHeader {
    pub replay_id: ReplayId,
    pub source_label: String,
    pub total_frames: Option<u32>,
    pub metadata: Metadata,
}

pub trait ReplayReader {
    fn read_header(&self, input: &ReplayInput) -> Result<ReplayHeader>;
}

/// Structural framing facts immediately after the replay header.
///
/// This type does not imply supported ReplayHeader semantics, CRC validity,
/// replay-body semantic validity, frame decoding, raw-state extraction, or events.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayBodyBoundaryV1 {
    pub source_label: String,
    pub header_size: u32,
    pub header_end: u64,
    pub content_size: u32,
    /// Stored content CRC field. MinimalReplayBodyBoundaryReader does not validate it.
    pub content_crc: u32,
    pub content_start: u64,
    pub content_end: u64,
    pub input_len: u64,
}

pub trait ReplayBodyBoundaryReader {
    fn read_body_boundary(&self, input: &ReplayInput) -> Result<ReplayBodyBoundaryV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayBodyBoundaryReader;

impl ReplayBodyBoundaryReader for MinimalReplayBodyBoundaryReader {
    fn read_body_boundary(&self, input: &ReplayInput) -> Result<ReplayBodyBoundaryV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_body_boundary_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(body_boundary_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the minimal body-boundary reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayHeaderReader;

impl ReplayReader for MinimalReplayHeaderReader {
    fn read_header(&self, input: &ReplayInput) -> Result<ReplayHeader> {
        match input {
            ReplayInput::Memory { label, bytes } => parse_replay_header_from_memory(label, bytes),
            ReplayInput::File(path) => Err(parse_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the first minimal parser boundary: {}",
                    path.display()
                ),
            )),
        }
    }
}

#[derive(Debug, Default, Clone, Copy)]
pub struct UnsupportedReplayReader;

impl ReplayReader for UnsupportedReplayReader {
    fn read_header(&self, input: &ReplayInput) -> Result<ReplayHeader> {
        Err(MimirError::message(format!(
            "no replay parser is bundled in this scaffold for {}",
            input.label()
        )))
    }
}

const SUPPORTED_MAJOR_VERSION: i32 = 868;
const SUPPORTED_MINOR_VERSION: i32 = 32;
const SUPPORTED_NET_VERSION: i32 = 10;
const SUPPORTED_GAME_TYPE: &str = "TAGame.Replay_Soccar_TA";
const SUPPORTED_REPLAY_VERSION: i32 = 8;
const SUPPORTED_BUILD_VERSION_FIXTURE_001: &str = "241206.55345.468477";
const SUPPORTED_BUILD_VERSION_FIXTURE_002: &str = "250811.43331.492665";
const SUPPORTED_BUILD_VERSION_FIXTURE_003: &str = "251020.62592.500294";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_001: &str = "220826.56130.393105";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_002: &str = "230224.54624.415510";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_003: &str = "230823.66121.430366";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_004: &str = "231010.63095.433650";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_005: &str = "211110.58467.353926";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_006: &str = "211123.48895.355454";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_007: &str = "230113.44243.411503";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_008: &str = "230413.76047.419576";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_009: &str = "240425.56865.448852";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_010: &str = "240717.49861.454952";
const SUPPORTED_BUILD_VERSIONS_V1: [&str; 13] = [
    SUPPORTED_BUILD_VERSION_FIXTURE_001,
    SUPPORTED_BUILD_VERSION_FIXTURE_002,
    SUPPORTED_BUILD_VERSION_FIXTURE_003,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_001,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_002,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_003,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_004,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_005,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_006,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_007,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_008,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_009,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_010,
];
const MAX_ADMITTED_TEXT_BYTES: i32 = 10_000;

const KIND_ARRAY: &str = "ArrayProperty";
const KIND_BOOL: &str = "BoolProperty";
const KIND_FLOAT: &str = "FloatProperty";
const KIND_INT: &str = "IntProperty";
const KIND_NAME: &str = "NameProperty";
const KIND_QWORD: &str = "QWordProperty";
const KIND_STR: &str = "StrProperty";

fn is_supported_replay_header_tuple_v1(
    major_version: i32,
    minor_version: i32,
    net_version: i32,
    game_type: &str,
    replay_version: i32,
    build_version: &str,
) -> bool {
    if major_version != SUPPORTED_MAJOR_VERSION
        || minor_version != SUPPORTED_MINOR_VERSION
        || net_version != SUPPORTED_NET_VERSION
        || game_type != SUPPORTED_GAME_TYPE
        || replay_version != SUPPORTED_REPLAY_VERSION
    {
        return false;
    }

    SUPPORTED_BUILD_VERSIONS_V1.contains(&build_version)
}
struct HeaderCursor<'a> {
    bytes: &'a [u8],
    offset: usize,
}

impl<'a> HeaderCursor<'a> {
    fn new(bytes: &'a [u8]) -> Self {
        Self { bytes, offset: 0 }
    }

    fn remaining(&self) -> usize {
        self.bytes.len().saturating_sub(self.offset)
    }

    fn position(&self) -> usize {
        self.offset
    }

    fn read_exact(&mut self, len: usize, context: impl AsRef<str>) -> Result<&'a [u8]> {
        if len > self.remaining() {
            return Err(parse_error(
                "insufficient",
                format!(
                    "{} needs {} bytes at offset {}, only {} remain",
                    context.as_ref(),
                    len,
                    self.offset,
                    self.remaining()
                ),
            ));
        }

        let start = self.offset;
        self.offset += len;
        Ok(&self.bytes[start..self.offset])
    }

    fn read_i32_le(&mut self, context: impl AsRef<str>) -> Result<i32> {
        let raw = self.read_exact(4, context)?;
        Ok(i32::from_le_bytes(
            raw.try_into().expect("read_exact returned 4 bytes"),
        ))
    }

    fn read_u32_le(&mut self, context: impl AsRef<str>) -> Result<u32> {
        let raw = self.read_exact(4, context)?;
        Ok(u32::from_le_bytes(
            raw.try_into().expect("read_exact returned 4 bytes"),
        ))
    }

    fn read_f32_le(&mut self, context: impl AsRef<str>) -> Result<f32> {
        let raw = self.read_exact(4, context)?;
        Ok(f32::from_le_bytes(
            raw.try_into().expect("read_exact returned 4 bytes"),
        ))
    }

    fn read_parse_str_utf8_nul(&mut self, context: impl AsRef<str>) -> Result<String> {
        let context = context.as_ref();
        let bytes = self.read_len_prefixed_nul_bytes(context)?;
        std::str::from_utf8(bytes)
            .map(str::to_owned)
            .map_err(|error| malformed(format!("{context} is not UTF-8: {error}")))
    }

    fn read_parse_text_windows1252_nul(&mut self, context: impl AsRef<str>) -> Result<String> {
        let context = context.as_ref();
        let bytes = self.read_len_prefixed_nul_bytes(context)?;
        decode_windows1252(bytes, context)
    }

    fn read_len_prefixed_nul_bytes(&mut self, context: &str) -> Result<&'a [u8]> {
        let len = self.read_i32_le(format!("{context} length"))?;
        if len < 0 {
            return Err(parse_error(
                "unsupported-text",
                format!("{context} uses negative-length UTF-16 text, which is unsupported"),
            ));
        }
        if len > MAX_ADMITTED_TEXT_BYTES {
            return Err(malformed(format!(
                "{context} length {len} exceeds admitted bound {MAX_ADMITTED_TEXT_BYTES}"
            )));
        }

        let len = usize::try_from(len)
            .map_err(|_| malformed(format!("{context} length cannot fit usize")))?;
        if len == 0 {
            return Err(malformed(format!(
                "{context} has zero length and no trailing NUL"
            )));
        }

        let raw = self.read_exact(len, context)?;
        if raw.last() != Some(&0) {
            return Err(malformed(format!("{context} is missing trailing NUL")));
        }

        Ok(&raw[..raw.len() - 1])
    }

    fn skip_bounded(&mut self, len: usize, context: impl AsRef<str>) -> Result<()> {
        self.read_exact(len, context)?;
        Ok(())
    }
}

#[derive(Default)]
struct ParsedHeaderProperties {
    replay_id: Option<String>,
    total_frames: Option<u32>,
    replay_version: Option<i32>,
    build_version: Option<String>,
    metadata: Metadata,
}

fn parse_replay_body_boundary_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayBodyBoundaryV1> {
    if label.is_empty() {
        return Err(body_boundary_error(
            "mapping",
            "ReplayInput::Memory.label must be non-empty for ReplayBodyBoundaryV1.source_label",
        ));
    }

    if bytes.len() < 8 {
        return Err(body_boundary_error(
            "insufficient",
            format!(
                "body-boundary framing needs the 8-byte replay preamble, input has {} bytes",
                bytes.len()
            ),
        ));
    }

    let header_size_i32 =
        i32::from_le_bytes(bytes[0..4].try_into().expect("slice is exactly four bytes"));
    if header_size_i32 < 0 {
        return Err(body_boundary_error(
            "malformed",
            format!("header_size {header_size_i32} is negative"),
        ));
    }

    let header_size = usize::try_from(header_size_i32).map_err(|_| {
        body_boundary_error(
            "malformed",
            format!("header_size {header_size_i32} cannot fit usize"),
        )
    })?;
    let header_end = 8usize.checked_add(header_size).ok_or_else(|| {
        body_boundary_error(
            "malformed",
            format!("header_size {header_size_i32} overflows header_end"),
        )
    })?;
    let framing_end = header_end
        .checked_add(8)
        .ok_or_else(|| body_boundary_error("malformed", "content framing end overflows usize"))?;

    if framing_end > bytes.len() {
        return Err(body_boundary_error(
            "insufficient",
            format!(
                "header_end {header_end} requires 8 content-framing bytes through {framing_end}, input has {} bytes",
                bytes.len()
            ),
        ));
    }

    let content_size_i32 = i32::from_le_bytes(
        bytes[header_end..header_end + 4]
            .try_into()
            .expect("slice is exactly four bytes"),
    );
    if content_size_i32 < 0 {
        return Err(body_boundary_error(
            "malformed",
            format!("content_size {content_size_i32} is negative"),
        ));
    }
    let content_crc = u32::from_le_bytes(
        bytes[header_end + 4..header_end + 8]
            .try_into()
            .expect("slice is exactly four bytes"),
    );
    let content_size = usize::try_from(content_size_i32).map_err(|_| {
        body_boundary_error(
            "malformed",
            format!("content_size {content_size_i32} cannot fit usize"),
        )
    })?;
    let content_start = framing_end;
    let content_end = content_start.checked_add(content_size).ok_or_else(|| {
        body_boundary_error(
            "malformed",
            format!("content_size {content_size_i32} overflows content_end"),
        )
    })?;

    if content_end > bytes.len() {
        return Err(body_boundary_error(
            "insufficient",
            format!(
                "content_size {content_size_i32} requires content_end {content_end}, input has {} bytes",
                bytes.len()
            ),
        ));
    }
    if content_end < bytes.len() {
        return Err(body_boundary_error(
            "malformed",
            format!(
                "content_size {content_size_i32} leaves {} trailing bytes after content_end {content_end}",
                bytes.len() - content_end
            ),
        ));
    }

    let header_size = u32::try_from(header_size_i32)
        .map_err(|_| body_boundary_error("malformed", "non-negative header_size cannot fit u32"))?;
    let content_size = u32::try_from(content_size_i32).map_err(|_| {
        body_boundary_error("malformed", "non-negative content_size cannot fit u32")
    })?;
    let header_end = u64::try_from(header_end)
        .map_err(|_| body_boundary_error("malformed", "header_end cannot fit u64"))?;
    let content_start = u64::try_from(content_start)
        .map_err(|_| body_boundary_error("malformed", "content_start cannot fit u64"))?;
    let content_end = u64::try_from(content_end)
        .map_err(|_| body_boundary_error("malformed", "content_end cannot fit u64"))?;
    let input_len = u64::try_from(bytes.len())
        .map_err(|_| body_boundary_error("malformed", "input length cannot fit u64"))?;

    Ok(ReplayBodyBoundaryV1 {
        source_label: label.to_string(),
        header_size,
        header_end,
        content_size,
        content_crc,
        content_start,
        content_end,
        input_len,
    })
}

fn parse_replay_header_from_memory(label: &str, bytes: &[u8]) -> Result<ReplayHeader> {
    if label.is_empty() {
        return Err(mapping_error(
            "ReplayInput::Memory.label must be non-empty for ReplayHeader.source_label",
        ));
    }

    let mut outer = HeaderCursor::new(bytes);
    let header_size = outer.read_i32_le("header_size")?;
    let _header_crc = outer.read_u32_le("header_crc")?;

    if header_size < 0 {
        return Err(malformed(format!("header_size {header_size} is negative")));
    }

    let header_len = usize::try_from(header_size)
        .map_err(|_| malformed(format!("header_size {header_size} cannot fit usize")))?;
    let header_end = 8usize
        .checked_add(header_len)
        .ok_or_else(|| malformed(format!("header_size {header_size} overflows header_end")))?;

    if header_end > bytes.len() {
        return Err(parse_error(
            "insufficient",
            format!(
                "header_size {header_size} requires header_end {header_end}, input has {} bytes",
                bytes.len()
            ),
        ));
    }

    let header_bytes = &bytes[8..header_end];
    let mut header = HeaderCursor::new(header_bytes);
    let major_version = header.read_i32_le("major_version")?;
    let minor_version = header.read_i32_le("minor_version")?;
    let net_version = header.read_i32_le("net_version")?;
    let game_type = header.read_parse_text_windows1252_nul("game_type")?;

    let parsed = parse_top_level_properties(&mut header)?;

    if header.position() != header_bytes.len() {
        return Err(malformed(format!(
            "header terminator ended at {}, expected {}",
            header.position(),
            header_bytes.len()
        )));
    }

    let replay_version = parsed.replay_version.ok_or_else(|| {
        mapping_error("missing required ReplayVersion for supported-version tuple")
    })?;
    let build_version = parsed.build_version.as_deref().ok_or_else(|| {
        mapping_error("missing required BuildVersion for supported-version tuple")
    })?;

    if !is_supported_replay_header_tuple_v1(
        major_version,
        minor_version,
        net_version,
        &game_type,
        replay_version,
        build_version,
    ) {
        return Err(parse_error(
            "unsupported-version",
            format!(
                "unsupported tuple major={major_version}, minor={minor_version}, net={net_version}, game_type={game_type}, ReplayVersion={replay_version}, BuildVersion={build_version}"
            ),
        ));
    }
    let replay_id = parsed
        .replay_id
        .ok_or_else(|| mapping_error("missing required Id property for ReplayHeader.replay_id"))?;

    Ok(ReplayHeader {
        replay_id: ReplayId::new(replay_id),
        source_label: label.to_string(),
        total_frames: parsed.total_frames,
        metadata: parsed.metadata,
    })
}

fn parse_top_level_properties(cursor: &mut HeaderCursor<'_>) -> Result<ParsedHeaderProperties> {
    let mut seen = BTreeSet::new();
    let mut parsed = ParsedHeaderProperties::default();
    let mut terminated = false;

    while cursor.position() < cursor.bytes.len() {
        let key_offset = cursor.position();
        let key = cursor.read_parse_str_utf8_nul("property key")?;
        if key == "None" {
            terminated = true;
            break;
        }

        if !seen.insert(key.clone()) {
            if is_selected_property(&key) {
                return Err(mapping_error(format!("duplicate selected property {key}")));
            }
            return Err(malformed(format!(
                "duplicate top-level property {key} at header offset {key_offset}"
            )));
        }

        let kind = cursor.read_parse_str_utf8_nul(format!("property {key} kind"))?;
        let property_size = cursor.read_u32_le(format!("property {key} size"))?;
        let _ignored = cursor.read_u32_le(format!("property {key} ignored field"))?;
        let value_len = usize::try_from(property_size).map_err(|_| {
            malformed(format!(
                "property {key} size {property_size} cannot fit usize"
            ))
        })?;

        if value_len > cursor.remaining() {
            return Err(malformed(format!(
                "property {key} size {property_size} exceeds header boundary at offset {}",
                cursor.position()
            )));
        }

        if is_selected_property(&key) {
            parse_selected_property(&mut parsed, &key, &kind, cursor, value_len)?;
        } else {
            skip_non_selected_property(&key, &kind, cursor, value_len)?;
        }
    }

    if !terminated {
        return Err(malformed("missing top-level property terminator None"));
    }

    Ok(parsed)
}

fn parse_selected_property(
    parsed: &mut ParsedHeaderProperties,
    key: &str,
    kind: &str,
    cursor: &mut HeaderCursor<'_>,
    value_len: usize,
) -> Result<()> {
    let value_bytes = cursor.read_exact(value_len, format!("property {key} value"))?;
    let mut value = HeaderCursor::new(value_bytes);

    match key {
        "Id" => {
            require_kind(key, kind, KIND_STR)?;
            let id = value.read_parse_text_windows1252_nul("Id value")?;
            ensure_consumed(&value, key)?;
            if !is_admitted_replay_id(&id) {
                return Err(mapping_error(
                    "Id must be exactly 32 ASCII hexadecimal digits",
                ));
            }
            parsed.replay_id = Some(id);
        }
        "NumFrames" => {
            require_kind(key, kind, KIND_INT)?;
            require_value_len(key, value_len, 4)?;
            let frames = value.read_i32_le("NumFrames value")?;
            ensure_consumed(&value, key)?;
            if frames < 0 {
                return Err(mapping_error(format!("NumFrames {frames} is negative")));
            }
            parsed.total_frames = Some(frames as u32);
        }
        "ReplayName" | "Date" | "BuildVersion" => {
            require_kind(key, kind, KIND_STR)?;
            let text = value.read_parse_text_windows1252_nul(format!("{key} value"))?;
            ensure_consumed(&value, key)?;
            if key == "BuildVersion" {
                parsed.build_version = Some(text.clone());
            }
            parsed.metadata.insert(key, FieldValue::Text(text));
        }
        "MapName" | "MatchType" => {
            require_kind(key, kind, KIND_NAME)?;
            let text = value.read_parse_text_windows1252_nul(format!("{key} value"))?;
            ensure_consumed(&value, key)?;
            parsed.metadata.insert(key, FieldValue::Text(text));
        }
        "ReplayVersion" | "MaxChannels" | "TeamSize" => {
            require_kind(key, kind, KIND_INT)?;
            require_value_len(key, value_len, 4)?;
            let number = value.read_i32_le(format!("{key} value"))?;
            ensure_consumed(&value, key)?;
            if key == "ReplayVersion" {
                parsed.replay_version = Some(number);
            }
            parsed
                .metadata
                .insert(key, FieldValue::Integer(i64::from(number)));
        }
        "RecordFPS" => {
            require_kind(key, kind, KIND_FLOAT)?;
            require_value_len(key, value_len, 4)?;
            let number = value.read_f32_le("RecordFPS value")?;
            ensure_consumed(&value, key)?;
            if !number.is_finite() {
                return Err(mapping_error("RecordFPS must be finite"));
            }
            parsed
                .metadata
                .insert(key, FieldValue::Float(f64::from(number)));
        }
        _ => unreachable!("is_selected_property and parse_selected_property are out of sync"),
    }

    Ok(())
}

fn skip_non_selected_property(
    key: &str,
    kind: &str,
    cursor: &mut HeaderCursor<'_>,
    value_len: usize,
) -> Result<()> {
    match kind {
        KIND_BOOL => skip_non_selected_bool_property(key, cursor, value_len),
        KIND_ARRAY | KIND_FLOAT | KIND_INT | KIND_NAME | KIND_QWORD | KIND_STR => {
            cursor.skip_bounded(value_len, format!("property {key} value"))
        }
        _ => Err(parse_error(
            "unsupported-property",
            format!("property {key} uses unsupported kind {kind}"),
        )),
    }
}

fn skip_non_selected_bool_property(
    key: &str,
    cursor: &mut HeaderCursor<'_>,
    value_len: usize,
) -> Result<()> {
    if value_len != 0 {
        return Err(malformed(format!(
            "property {key} BoolProperty has declared size {value_len}, expected 0"
        )));
    }

    let value = cursor.read_exact(1, format!("property {key} BoolProperty value"))?[0];
    match value {
        0 | 1 => Ok(()),
        _ => Err(malformed(format!(
            "property {key} BoolProperty value must be 0 or 1, got {value}"
        ))),
    }
}

fn require_kind(key: &str, actual: &str, expected: &str) -> Result<()> {
    if actual == expected {
        return Ok(());
    }

    if is_admitted_property_kind(actual) {
        return Err(mapping_error(format!(
            "selected property {key} has kind {actual}, expected {expected}"
        )));
    }

    Err(parse_error(
        "unsupported-property",
        format!("selected property {key} uses unsupported kind {actual}"),
    ))
}

fn require_value_len(key: &str, actual: usize, expected: usize) -> Result<()> {
    if actual == expected {
        Ok(())
    } else {
        Err(malformed(format!(
            "selected property {key} has value length {actual}, expected {expected}"
        )))
    }
}

fn ensure_consumed(cursor: &HeaderCursor<'_>, key: &str) -> Result<()> {
    if cursor.remaining() == 0 {
        Ok(())
    } else {
        Err(malformed(format!(
            "selected property {key} left {} trailing value bytes",
            cursor.remaining()
        )))
    }
}

fn is_selected_property(key: &str) -> bool {
    matches!(
        key,
        "Id" | "NumFrames"
            | "ReplayName"
            | "Date"
            | "MapName"
            | "ReplayVersion"
            | "BuildVersion"
            | "MaxChannels"
            | "MatchType"
            | "TeamSize"
            | "RecordFPS"
    )
}

fn is_admitted_property_kind(kind: &str) -> bool {
    matches!(
        kind,
        KIND_ARRAY | KIND_FLOAT | KIND_INT | KIND_NAME | KIND_QWORD | KIND_STR
    )
}

fn is_admitted_replay_id(value: &str) -> bool {
    value.len() == 32 && value.bytes().all(|byte| byte.is_ascii_hexdigit())
}

fn decode_windows1252(bytes: &[u8], context: &str) -> Result<String> {
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
                return Err(malformed(format!(
                    "{context} contains undefined Windows-1252 byte 0x{byte:02X}"
                )));
            }
            _ => char::from(byte),
        };
        decoded.push(character);
    }
    Ok(decoded)
}

fn body_boundary_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay body boundary error: {category}: {}",
        detail.into()
    ))
}

fn parse_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay header parse error: {category}: {}",
        detail.into()
    ))
}

fn malformed(detail: impl Into<String>) -> MimirError {
    parse_error("malformed", detail)
}

fn mapping_error(detail: impl Into<String>) -> MimirError {
    MimirError::message(format!("replay header mapping error: {}", detail.into()))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::path::PathBuf;

    const FIXTURE_001_LABEL: &str = "rl_replay_header_fixture_001";
    const FIXTURE_001_PATH: &str = concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../external_fixtures/sample_001.replay"
    );
    const FIXTURE_002_LABEL: &str = "rl_replay_header_fixture_002";
    const FIXTURE_002_PATH: &str = concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../external_fixtures/sample_002.replay"
    );
    const FIXTURE_003_LABEL: &str = "rl_replay_header_fixture_003";
    const FIXTURE_003_PATH: &str = concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../external_fixtures/sample_003.replay"
    );

    #[test]
    fn supported_build_version_registry_v1_contains_only_expected_exact_entries() {
        assert_eq!(
            SUPPORTED_BUILD_VERSIONS_V1,
            [
                SUPPORTED_BUILD_VERSION_FIXTURE_001,
                SUPPORTED_BUILD_VERSION_FIXTURE_002,
                SUPPORTED_BUILD_VERSION_FIXTURE_003,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_001,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_002,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_003,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_004,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_005,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_006,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_007,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_008,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_009,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_010,
            ]
        );
    }

    #[test]
    fn supported_build_version_registry_v1_has_no_duplicates() {
        let unique: BTreeSet<_> = SUPPORTED_BUILD_VERSIONS_V1.iter().copied().collect();
        assert_eq!(unique.len(), SUPPORTED_BUILD_VERSIONS_V1.len());
    }
    #[test]
    fn minimal_body_boundary_reader_matches_three_historical_fixtures() {
        let cases = [
            (
                FIXTURE_001_PATH,
                FIXTURE_001_LABEL,
                13_200u32,
                13_208u64,
                2_987_805u32,
                2_323_044_833u32,
                13_216u64,
                3_001_021u64,
            ),
            (
                FIXTURE_002_PATH,
                FIXTURE_002_LABEL,
                11_273u32,
                11_281u64,
                2_621_614u32,
                3_734_167_123u32,
                11_289u64,
                2_632_903u64,
            ),
            (
                FIXTURE_003_PATH,
                FIXTURE_003_LABEL,
                11_190u32,
                11_198u64,
                1_627_332u32,
                3_991_282_011u32,
                11_206u64,
                1_638_538u64,
            ),
        ];

        for (
            path,
            label,
            header_size,
            header_end,
            content_size,
            content_crc,
            content_start,
            input_len,
        ) in cases
        {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let boundary = MinimalReplayBodyBoundaryReader
                .read_body_boundary(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical fixture body boundary should be structurally valid");

            assert_eq!(boundary.source_label, label);
            assert_eq!(boundary.header_size, header_size);
            assert_eq!(boundary.header_end, header_end);
            assert_eq!(boundary.content_size, content_size);
            assert_eq!(boundary.content_crc, content_crc);
            assert_eq!(boundary.content_start, content_start);
            assert_eq!(boundary.content_end, input_len);
            assert_eq!(boundary.input_len, input_len);
        }
    }

    #[test]
    fn minimal_body_boundary_reader_exactly_frames_checked_in_largest_100_corpus() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 body-boundary regression; corpus root is absent");
            return;
        }

        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| {
                entry
                    .expect("corpus directory entry should be readable")
                    .path()
            })
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
            let boundary = MinimalReplayBodyBoundaryReader
                .read_body_boundary(&ReplayInput::Memory {
                    label: label.clone(),
                    bytes,
                })
                .unwrap_or_else(|error| panic!("body boundary failed for {label}: {error}"));
            assert_eq!(boundary.source_label, label);
            assert_eq!(boundary.content_end, boundary.input_len);
        }
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_file_input() {
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside the body-boundary reader");
        assert_error_contains(error, "replay body boundary error: unsupported-input");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_empty_memory_label() {
        let bytes = build_body_boundary_bytes(&[], 0, 0, &[]);
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: String::new(),
                bytes,
            })
            .expect_err("empty source labels are not admitted");
        assert_error_contains(error, "replay body boundary error: mapping");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_truncated_preamble() {
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes: vec![0; 7],
            })
            .expect_err("an eight-byte replay preamble is required");
        assert_error_contains(error, "replay body boundary error: insufficient");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_negative_header_size() {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&(-1i32).to_le_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes());
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("negative header_size is malformed");
        assert_error_contains(error, "replay body boundary error: malformed");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_truncated_content_framing() {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&0i32.to_le_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes());
        bytes.extend_from_slice(&0i32.to_le_bytes());
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("content_size without content_crc is truncated framing");
        assert_error_contains(error, "replay body boundary error: insufficient");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_negative_content_size() {
        let bytes = build_body_boundary_bytes(&[], 0, -1, &[]);
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("negative content_size is malformed");
        assert_error_contains(error, "replay body boundary error: malformed");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_content_size_beyond_input() {
        let bytes = build_body_boundary_bytes(&[1, 2, 3], 0, 4, &[9, 8, 7]);
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("declared content beyond input is insufficient");
        assert_error_contains(error, "replay body boundary error: insufficient");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_trailing_bytes_after_content() {
        let mut bytes = build_body_boundary_bytes(&[1, 2], 0, 2, &[3, 4]);
        bytes.push(5);
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("bytes after declared content are malformed framing");
        assert_error_contains(error, "replay body boundary error: malformed");
    }

    #[test]
    fn minimal_body_boundary_reader_reports_crc_without_validating_it() {
        let bytes = build_body_boundary_bytes(&[0xAA; 12], 0xDEADBEEF, 3, &[1, 2, 3]);
        let boundary = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect("arbitrary stored CRC must not be validated in this pass");
        assert_eq!(boundary.content_crc, 0xDEADBEEF);
        assert_eq!(boundary.content_size, 3);
        assert_eq!(boundary.content_end, boundary.input_len);
    }

    #[test]
    fn unsupported_reader_fails_explicitly() {
        let reader = UnsupportedReplayReader;
        let error = reader
            .read_header(&ReplayInput::file("sample.replay"))
            .expect_err("reader should be unavailable");

        assert!(
            error
                .to_string()
                .contains("no replay parser is bundled in this scaffold")
        );
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_001_and_header_only_slice() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };

        let reader = MinimalReplayHeaderReader;
        let input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: bytes.clone(),
        };

        let header = reader
            .read_header(&input)
            .expect("fixture header should parse");
        assert_fixture_001_header(&header);

        let header_size = i32::from_le_bytes(
            bytes[0..4]
                .try_into()
                .expect("fixture should contain header_size"),
        );
        assert_eq!(header_size, 13_200);
        let header_end =
            8 + usize::try_from(header_size).expect("fixture header_size should fit usize");
        assert_eq!(header_end, 13_208);
        let header_only = bytes[..header_end].to_vec();
        let header_only_input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: header_only,
        };
        let header_from_header_only = reader
            .read_header(&header_only_input)
            .expect("complete header-only slice should parse without body bytes");

        assert_eq!(header_from_header_only, header);
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_002_exact_happy_path() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_002_PATH, FIXTURE_002_LABEL) else {
            return;
        };

        let header = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_002_LABEL.to_string(),
                bytes,
            })
            .expect("fixture_002 exact header should parse");

        assert_fixture_002_header(&header);
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_002_header_only_slice() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_002_PATH, FIXTURE_002_LABEL) else {
            return;
        };

        let header_size = i32::from_le_bytes(
            bytes[0..4]
                .try_into()
                .expect("fixture should contain header_size"),
        );
        assert_eq!(header_size, 11_273);
        let header_end =
            8 + usize::try_from(header_size).expect("fixture header_size should fit usize");
        assert_eq!(header_end, 11_281);

        let full_header = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_002_LABEL.to_string(),
                bytes: bytes.clone(),
            })
            .expect("fixture_002 full bytes should parse");
        let header_only = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_002_LABEL.to_string(),
                bytes: bytes[..header_end].to_vec(),
            })
            .expect("fixture_002 complete header-only slice should parse without body bytes");

        assert_fixture_002_header(&header_only);
        assert_eq!(header_only, full_header);
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_003_exact_happy_path() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_003_PATH, FIXTURE_003_LABEL) else {
            return;
        };

        let header = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_003_LABEL.to_string(),
                bytes,
            })
            .expect("fixture_003 exact header should parse");

        assert_fixture_003_header(&header);
        assert!(header.metadata.get("bForfeit").is_none());
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_003_header_only_slice() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_003_PATH, FIXTURE_003_LABEL) else {
            return;
        };

        let header_size = i32::from_le_bytes(
            bytes[0..4]
                .try_into()
                .expect("fixture should contain header_size"),
        );
        assert_eq!(header_size, 11_190);
        let header_end =
            8 + usize::try_from(header_size).expect("fixture header_size should fit usize");
        assert_eq!(header_end, 11_198);

        let full_header = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_003_LABEL.to_string(),
                bytes: bytes.clone(),
            })
            .expect("fixture_003 full bytes should parse");
        let header_only = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_003_LABEL.to_string(),
                bytes: bytes[..header_end].to_vec(),
            })
            .expect("fixture_003 complete header-only slice should parse without body bytes");

        assert_fixture_003_header(&header_only);
        assert!(header_only.metadata.get("bForfeit").is_none());
        assert_eq!(header_only, full_header);
    }

    #[test]
    fn minimal_reader_rejects_file_input() {
        let error = MinimalReplayHeaderReader
            .read_header(&ReplayInput::file("sample.replay"))
            .expect_err("file input is outside the first minimal parser boundary");

        assert_error_contains(error, "replay header parse error: unsupported-input");
    }

    #[test]
    fn minimal_reader_rejects_empty_memory_label() {
        let error = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: String::new(),
                bytes: minimal_valid_replay_bytes(),
            })
            .expect_err("empty labels are not admitted source_label values");

        assert_error_contains(error, "replay header mapping error");
    }

    #[test]
    fn minimal_reader_rejects_fewer_than_4_bytes() {
        let error = read_synthetic(vec![1, 2, 3]).expect_err("header_size is truncated");

        assert_error_contains(error, "replay header parse error: insufficient");
    }

    #[test]
    fn minimal_reader_rejects_fewer_than_8_bytes() {
        let error =
            read_synthetic(0i32.to_le_bytes().to_vec()).expect_err("header_crc is truncated");

        assert_error_contains(error, "replay header parse error: insufficient");
    }

    #[test]
    fn minimal_reader_rejects_negative_header_size() {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&(-1i32).to_le_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes());

        let error = read_synthetic(bytes).expect_err("negative header_size is malformed");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_rejects_header_size_larger_than_bytes() {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&100i32.to_le_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes());

        let error = read_synthetic(bytes).expect_err("header region is truncated");

        assert_error_contains(error, "replay header parse error: insufficient");
    }

    #[test]
    fn minimal_reader_rejects_unsupported_version_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            major_version: SUPPORTED_MAJOR_VERSION - 1,
            ..HeaderSpec::minimal()
        }));

        let error = read_synthetic(bytes).expect_err("only the admitted exact tuple is supported");

        assert_error_contains(error, "replay header parse error: unsupported-version");
    }

    #[test]
    fn minimal_reader_admits_top_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_001.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("top-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_001.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_second_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_002.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("second-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_002.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_third_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_003.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("third-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_003.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_fourth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_004.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("fourth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_004.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_fifth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_005.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("fifth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_005.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_sixth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_006.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("sixth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_006.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_seventh_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_007.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("seventh-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_007.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_eighth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_008.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("eighth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_008.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_ninth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_009.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("ninth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_009.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_tenth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_010.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("tenth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_010.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_rejects_unknown_build_version_for_otherwise_supported_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: "251020.62592.500295".to_string(),
            ..HeaderSpec::minimal()
        }));

        let error = read_synthetic(bytes).expect_err(
            "unknown BuildVersion near fixture_003 must not be accepted by wildcard policy",
        );

        assert_error_contains(error, "replay header parse error: unsupported-version");
    }

    #[test]
    fn minimal_reader_rejects_missing_terminator() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            include_terminator: false,
            ..HeaderSpec::minimal()
        }));

        let error = read_synthetic(bytes).expect_err("top-level None terminator is required");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_rejects_duplicate_selected_property() {
        let mut spec = HeaderSpec::minimal();
        spec.extra_properties
            .push(PropertySpec::str("Id", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"));
        let bytes = build_replay_bytes(build_header(spec));

        let error = read_synthetic(bytes).expect_err("duplicate selected properties are forbidden");

        assert_error_contains(error, "replay header mapping error");
    }

    #[test]
    fn minimal_reader_rejects_duplicate_top_level_property() {
        let mut spec = HeaderSpec::minimal();
        spec.extra_properties
            .push(PropertySpec::int("Team0Score", 1));
        spec.extra_properties
            .push(PropertySpec::int("Team0Score", 2));
        let bytes = build_replay_bytes(build_header(spec));

        let error =
            read_synthetic(bytes).expect_err("top-level duplicate properties are forbidden");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_skips_non_selected_bool_property_false_without_metadata() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 0, &[0], true);

        let header =
            read_synthetic(bytes).expect("non-selected false BoolProperty should be skipped");

        assert!(header.metadata.get("bForfeit").is_none());
    }

    #[test]
    fn minimal_reader_skips_non_selected_bool_property_true_without_metadata() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 0, &[1], true);

        let header =
            read_synthetic(bytes).expect("non-selected true BoolProperty should be skipped");

        assert!(header.metadata.get("bForfeit").is_none());
    }

    #[test]
    fn minimal_reader_rejects_selected_bool_property() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal_without_id(), "Id", 0, &[1], true);

        let error =
            read_synthetic(bytes).expect_err("selected BoolProperty must remain unsupported");

        assert_error_contains(error, "replay header parse error: unsupported-property");
    }

    #[test]
    fn minimal_reader_rejects_non_selected_bool_property_nonzero_declared_size() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 1, &[1], true);

        let error = read_synthetic(bytes)
            .expect_err("BoolProperty declared size other than zero must be malformed");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_rejects_truncated_non_selected_bool_property_value() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 0, &[], false);

        let error = read_synthetic(bytes)
            .expect_err("BoolProperty missing its separate one-byte value must be insufficient");

        assert_error_contains(error, "replay header parse error: insufficient");
    }

    #[test]
    fn minimal_reader_rejects_invalid_non_selected_bool_property_value() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 0, &[2], true);

        let error =
            read_synthetic(bytes).expect_err("BoolProperty values other than 0 or 1 are malformed");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_rejects_unknown_property_kind() {
        let mut spec = HeaderSpec::minimal();
        spec.extra_properties.push(PropertySpec {
            key: "Unselected".to_string(),
            kind: "ByteProperty".to_string(),
            value: vec![1],
        });
        let bytes = build_replay_bytes(build_header(spec));

        let error = read_synthetic(bytes).expect_err("unknown property kinds are unsupported");

        assert_error_contains(error, "replay header parse error: unsupported-property");
    }

    #[test]
    fn minimal_reader_rejects_negative_length_text() {
        let mut header = Vec::new();
        header.extend_from_slice(&SUPPORTED_MAJOR_VERSION.to_le_bytes());
        header.extend_from_slice(&SUPPORTED_MINOR_VERSION.to_le_bytes());
        header.extend_from_slice(&SUPPORTED_NET_VERSION.to_le_bytes());
        header.extend_from_slice(&(-1i32).to_le_bytes());
        let bytes = build_replay_bytes(header);

        let error = read_synthetic(bytes).expect_err("UTF-16 negative-length text is unsupported");

        assert_error_contains(error, "replay header parse error: unsupported-text");
    }

    #[test]
    fn minimal_reader_rejects_selected_array_property() {
        let mut spec = HeaderSpec::minimal_without_id();
        spec.extra_properties.push(PropertySpec {
            key: "Id".to_string(),
            kind: KIND_ARRAY.to_string(),
            value: 0i32.to_le_bytes().to_vec(),
        });
        let bytes = build_replay_bytes(build_header(spec));

        let error = read_synthetic(bytes).expect_err("selected arrays are unsupported");

        assert_error_contains(error, "replay header mapping error");
    }

    #[test]
    fn minimal_reader_rejects_selected_non_finite_float() {
        let mut spec = HeaderSpec::minimal();
        spec.extra_properties
            .push(PropertySpec::float("RecordFPS", f32::INFINITY));
        let bytes = build_replay_bytes(build_header(spec));

        let error = read_synthetic(bytes).expect_err("selected floats must be finite");

        assert_error_contains(error, "replay header mapping error");
    }

    #[test]
    fn minimal_reader_does_not_validate_header_crc() {
        let reader = MinimalReplayHeaderReader;
        let original = minimal_valid_replay_bytes();
        let original_header =
            read_synthetic(original.clone()).expect("baseline header should parse");

        let mut changed_crc = original;
        changed_crc[4..8].copy_from_slice(&0xA5A5_A5A5u32.to_le_bytes());
        let changed_header = reader
            .read_header(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes: changed_crc,
            })
            .expect("header_crc is read as layout only, not validated");

        assert_eq!(changed_header, original_header);
    }

    fn load_fixture_bytes_or_skip(default_path: &str, fixture_id: &str) -> Option<Vec<u8>> {
        let path = PathBuf::from(default_path);

        match fs::read(&path) {
            Ok(bytes) => Some(bytes),
            Err(error) => {
                eprintln!(
                    "fixture missing or unreadable at {}; skipping {fixture_id} fixture-specific test: {}",
                    path.display(),
                    error
                );
                None
            }
        }
    }

    fn assert_fixture_001_header(header: &ReplayHeader) {
        assert_eq!(
            header.replay_id,
            ReplayId::new("7F59297811EFD8B19C444A81FB07660C")
        );
        assert_eq!(header.source_label, FIXTURE_001_LABEL);
        assert_eq!(header.total_frames, Some(13_555));
        assert_eq!(
            header.metadata.get("ReplayName"),
            Some(&FieldValue::Text(
                "Frestyle double touch but not ball".to_string()
            ))
        );
        assert_eq!(
            header.metadata.get("Date"),
            Some(&FieldValue::Text("2025-01-22 11-10-32".to_string()))
        );
        assert_eq!(
            header.metadata.get("MapName"),
            Some(&FieldValue::Text("Stadium_Winter_P".to_string()))
        );
        assert_eq!(
            header.metadata.get("ReplayVersion"),
            Some(&FieldValue::Integer(8))
        );
        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_FIXTURE_001.to_string()
            ))
        );
        assert_eq!(
            header.metadata.get("MaxChannels"),
            Some(&FieldValue::Integer(2047))
        );
        assert_eq!(
            header.metadata.get("MatchType"),
            Some(&FieldValue::Text("Online".to_string()))
        );
        assert_eq!(
            header.metadata.get("TeamSize"),
            Some(&FieldValue::Integer(3))
        );
        assert_eq!(
            header.metadata.get("RecordFPS"),
            Some(&FieldValue::Float(30.0))
        );
    }

    fn assert_fixture_002_header(header: &ReplayHeader) {
        assert_eq!(
            header.replay_id,
            ReplayId::new("D9DA34DA11F0811EAC139A94CBF30AF2")
        );
        assert_eq!(header.source_label, FIXTURE_002_LABEL);
        assert_eq!(header.total_frames, Some(10_351));
        assert_eq!(
            header.metadata.get("ReplayName"),
            Some(&FieldValue::Text("asdasd".to_string()))
        );
        assert_eq!(
            header.metadata.get("Date"),
            Some(&FieldValue::Text("2025-08-24 19-16-35".to_string()))
        );
        assert_eq!(
            header.metadata.get("MapName"),
            Some(&FieldValue::Text("NeoTokyo_Standard_P".to_string()))
        );
        assert_eq!(
            header.metadata.get("ReplayVersion"),
            Some(&FieldValue::Integer(8))
        );
        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_FIXTURE_002.to_string()
            ))
        );
        assert_eq!(
            header.metadata.get("MaxChannels"),
            Some(&FieldValue::Integer(2047))
        );
        assert_eq!(
            header.metadata.get("MatchType"),
            Some(&FieldValue::Text("Online".to_string()))
        );
        assert_eq!(
            header.metadata.get("TeamSize"),
            Some(&FieldValue::Integer(3))
        );
        assert_eq!(
            header.metadata.get("RecordFPS"),
            Some(&FieldValue::Float(30.0))
        );
    }

    fn assert_fixture_003_header(header: &ReplayHeader) {
        assert_eq!(
            header.replay_id,
            ReplayId::new("DF72482811F0B757082C458D84251EFF")
        );
        assert_eq!(header.source_label, FIXTURE_003_LABEL);
        assert_eq!(header.total_frames, Some(8_288));
        assert_eq!(
            header.metadata.get("ReplayName"),
            Some(&FieldValue::Text("asdasd".to_string()))
        );
        assert_eq!(
            header.metadata.get("Date"),
            Some(&FieldValue::Text("2025-11-01 19-20-48".to_string()))
        );
        assert_eq!(
            header.metadata.get("MapName"),
            Some(&FieldValue::Text("cs_day_p".to_string()))
        );
        assert_eq!(
            header.metadata.get("ReplayVersion"),
            Some(&FieldValue::Integer(8))
        );
        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_FIXTURE_003.to_string()
            ))
        );
        assert_eq!(
            header.metadata.get("MaxChannels"),
            Some(&FieldValue::Integer(2047))
        );
        assert_eq!(
            header.metadata.get("MatchType"),
            Some(&FieldValue::Text("Online".to_string()))
        );
        assert_eq!(
            header.metadata.get("TeamSize"),
            Some(&FieldValue::Integer(2))
        );
        assert_eq!(
            header.metadata.get("RecordFPS"),
            Some(&FieldValue::Float(30.0))
        );
        assert!(header.metadata.get("bForfeit").is_none());
    }

    fn read_synthetic(bytes: Vec<u8>) -> Result<ReplayHeader> {
        MinimalReplayHeaderReader.read_header(&ReplayInput::Memory {
            label: "synthetic".to_string(),
            bytes,
        })
    }

    fn assert_error_contains(error: MimirError, expected: &str) {
        let message = error.to_string();
        assert!(
            message.contains(expected),
            "expected error to contain {expected:?}, got {message:?}"
        );
    }

    fn minimal_valid_replay_bytes() -> Vec<u8> {
        build_replay_bytes(build_header(HeaderSpec::minimal()))
    }

    struct HeaderSpec {
        major_version: i32,
        minor_version: i32,
        net_version: i32,
        game_type: String,
        include_id: bool,
        include_replay_version: bool,
        include_build_version: bool,
        build_version: String,
        include_terminator: bool,
        extra_properties: Vec<PropertySpec>,
    }

    impl HeaderSpec {
        fn minimal() -> Self {
            Self {
                major_version: SUPPORTED_MAJOR_VERSION,
                minor_version: SUPPORTED_MINOR_VERSION,
                net_version: SUPPORTED_NET_VERSION,
                game_type: SUPPORTED_GAME_TYPE.to_string(),
                include_id: true,
                include_replay_version: true,
                include_build_version: true,
                build_version: SUPPORTED_BUILD_VERSION_FIXTURE_001.to_string(),
                include_terminator: true,
                extra_properties: Vec::new(),
            }
        }

        fn minimal_without_id() -> Self {
            Self {
                include_id: false,
                ..Self::minimal()
            }
        }
    }

    struct PropertySpec {
        key: String,
        kind: String,
        value: Vec<u8>,
    }

    impl PropertySpec {
        fn str(key: &str, value: &str) -> Self {
            Self {
                key: key.to_string(),
                kind: KIND_STR.to_string(),
                value: encode_text(value),
            }
        }

        fn int(key: &str, value: i32) -> Self {
            Self {
                key: key.to_string(),
                kind: KIND_INT.to_string(),
                value: value.to_le_bytes().to_vec(),
            }
        }

        fn float(key: &str, value: f32) -> Self {
            Self {
                key: key.to_string(),
                kind: KIND_FLOAT.to_string(),
                value: value.to_le_bytes().to_vec(),
            }
        }
    }

    fn build_header(spec: HeaderSpec) -> Vec<u8> {
        let mut header = Vec::new();
        header.extend_from_slice(&spec.major_version.to_le_bytes());
        header.extend_from_slice(&spec.minor_version.to_le_bytes());
        header.extend_from_slice(&spec.net_version.to_le_bytes());
        header.extend_from_slice(&encode_text(&spec.game_type));

        if spec.include_id {
            append_property(
                &mut header,
                &PropertySpec::str("Id", "7F59297811EFD8B19C444A81FB07660C"),
            );
        }
        if spec.include_replay_version {
            append_property(
                &mut header,
                &PropertySpec::int("ReplayVersion", SUPPORTED_REPLAY_VERSION),
            );
        }
        if spec.include_build_version {
            append_property(
                &mut header,
                &PropertySpec::str("BuildVersion", &spec.build_version),
            );
        }
        for property in spec.extra_properties {
            append_property(&mut header, &property);
        }
        if spec.include_terminator {
            header.extend_from_slice(&encode_str("None"));
        }

        header
    }

    fn append_property(header: &mut Vec<u8>, property: &PropertySpec) {
        header.extend_from_slice(&encode_str(&property.key));
        header.extend_from_slice(&encode_str(&property.kind));
        header.extend_from_slice(
            &(u32::try_from(property.value.len()).expect("synthetic value should fit u32"))
                .to_le_bytes(),
        );
        header.extend_from_slice(&0u32.to_le_bytes());
        header.extend_from_slice(&property.value);
    }

    fn build_replay_with_bool_property(
        mut spec: HeaderSpec,
        key: &str,
        declared_size: u32,
        value_bytes: &[u8],
        include_terminator: bool,
    ) -> Vec<u8> {
        spec.include_terminator = false;
        let mut header = build_header(spec);
        append_bool_property(&mut header, key, declared_size, value_bytes);
        if include_terminator {
            header.extend_from_slice(&encode_str("None"));
        }
        build_replay_bytes(header)
    }

    fn append_bool_property(
        header: &mut Vec<u8>,
        key: &str,
        declared_size: u32,
        value_bytes: &[u8],
    ) {
        header.extend_from_slice(&encode_str(key));
        header.extend_from_slice(&encode_str(KIND_BOOL));
        header.extend_from_slice(&declared_size.to_le_bytes());
        header.extend_from_slice(&0u32.to_le_bytes());
        header.extend_from_slice(value_bytes);
    }

    fn build_replay_bytes(header: Vec<u8>) -> Vec<u8> {
        let mut replay = Vec::new();
        replay.extend_from_slice(
            &(i32::try_from(header.len()).expect("synthetic header should fit i32")).to_le_bytes(),
        );
        replay.extend_from_slice(&0u32.to_le_bytes());
        replay.extend_from_slice(&header);
        replay
    }

    fn build_body_boundary_bytes(
        header: &[u8],
        content_crc: u32,
        declared_content_size: i32,
        content: &[u8],
    ) -> Vec<u8> {
        let mut replay = Vec::new();
        replay.extend_from_slice(
            &(i32::try_from(header.len()).expect("synthetic header should fit i32")).to_le_bytes(),
        );
        replay.extend_from_slice(&0u32.to_le_bytes());
        replay.extend_from_slice(header);
        replay.extend_from_slice(&declared_content_size.to_le_bytes());
        replay.extend_from_slice(&content_crc.to_le_bytes());
        replay.extend_from_slice(content);
        replay
    }

    fn encode_str(value: &str) -> Vec<u8> {
        encode_len_prefixed_nul(value.as_bytes())
    }

    fn encode_text(value: &str) -> Vec<u8> {
        assert!(
            value.is_ascii(),
            "synthetic text helper only encodes ASCII admitted test values"
        );
        encode_len_prefixed_nul(value.as_bytes())
    }

    fn encode_len_prefixed_nul(bytes: &[u8]) -> Vec<u8> {
        let len = i32::try_from(bytes.len() + 1).expect("synthetic string should fit i32");
        let mut encoded = Vec::with_capacity(4 + bytes.len() + 1);
        encoded.extend_from_slice(&len.to_le_bytes());
        encoded.extend_from_slice(bytes);
        encoded.push(0);
        encoded
    }
}
