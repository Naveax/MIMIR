use mimir_core::{MimirError, Result};
use mimir_replay::{MinimalReplayHeaderReader, ReplayInput, ReplayReader};
use mimir_types::FieldValue;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Write as _;
use std::fs;
use std::path::{Path, PathBuf};

const EXPECTED_CORPUS_ROWS: usize = 100;
const STATUS_NOT_IMPLEMENTED: &str = "not_implemented";

#[derive(Debug, Clone, Serialize)]
pub(crate) struct ReplayCompatibilityMatrixReport {
    mode: &'static str,
    corpus_root: PathBuf,
    manifest: PathBuf,
    output: PathBuf,
    summary_output: PathBuf,
    summary: ReplayCompatibilitySummary,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub(crate) struct ReplayCompatibilitySummary {
    scanned: usize,
    total_bytes: u64,
    supported: usize,
    unsupported: usize,
    malformed: usize,
    mapping_error: usize,
    other_error: usize,
    unique_version_tuples: usize,
    unique_builds: usize,
    category_counts: BTreeMap<String, usize>,
}

#[derive(Debug, Clone, Deserialize)]
struct ManifestRow {
    rank: usize,
    fixture_id: String,
    filename: String,
    bytes: u64,
    sha256: String,
}

#[derive(Debug, Clone, Serialize)]
struct ReplayCompatibilityRow {
    rank: usize,
    fixture_id: String,
    filename: String,
    bytes: u64,
    sha256: String,
    size_verified: bool,
    sha256_verified: bool,
    header_parse: String,
    major_version: Option<i32>,
    minor_version: Option<i32>,
    net_version: Option<i32>,
    game_type: Option<String>,
    replay_version: Option<i32>,
    build_version: Option<String>,
    failure_stage: Option<String>,
    failure_category: Option<String>,
    failure_reason: Option<String>,
    raw_state_status: &'static str,
    event_layer_status: &'static str,
    skill_layer_status: &'static str,
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
struct HeaderVersionObservation {
    major_version: Option<i32>,
    minor_version: Option<i32>,
    net_version: Option<i32>,
    game_type: Option<String>,
    replay_version: Option<i32>,
    build_version: Option<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct FailureClass {
    header_parse: &'static str,
    stage: &'static str,
    category: &'static str,
}

pub(crate) fn run(corpus_root: PathBuf, output: PathBuf) -> Result<ReplayCompatibilityMatrixReport> {
    let manifest_path = corpus_root.join("manifest.jsonl");
    let manifest_rows = load_manifest(&manifest_path)?;
    validate_manifest(&manifest_rows)?;
    validate_replay_file_count(&corpus_root)?;

    let rows = scan_rows(&corpus_root, &manifest_rows)?;
    let summary = summarize_rows(&rows);
    let summary_output = output.with_extension("summary.json");

    write_jsonl(&output, &rows)?;
    write_pretty_json(&summary_output, &summary)?;

    Ok(ReplayCompatibilityMatrixReport {
        mode: "header-compatibility-v1",
        corpus_root,
        manifest: manifest_path,
        output,
        summary_output,
        summary,
    })
}

fn load_manifest(path: &Path) -> Result<Vec<ManifestRow>> {
    let text = fs::read_to_string(path).map_err(|error| MimirError::io(path, error))?;
    let mut rows = Vec::new();

    for (line_index, line) in text.lines().enumerate() {
        if line.trim().is_empty() {
            continue;
        }

        let row = serde_json::from_str::<ManifestRow>(line).map_err(|error| {
            MimirError::message(format!(
                "replay compatibility manifest JSON error at {} line {}: {error}",
                path.display(),
                line_index + 1
            ))
        })?;
        rows.push(row);
    }

    Ok(rows)
}

fn validate_manifest(rows: &[ManifestRow]) -> Result<()> {
    if rows.len() != EXPECTED_CORPUS_ROWS {
        return Err(MimirError::message(format!(
            "replay compatibility matrix requires exactly {EXPECTED_CORPUS_ROWS} manifest rows, found {}",
            rows.len()
        )));
    }

    let mut fixture_ids = BTreeSet::new();
    let mut filenames = BTreeSet::new();
    let mut hashes = BTreeSet::new();

    for (index, row) in rows.iter().enumerate() {
        let expected_rank = index + 1;
        if row.rank != expected_rank {
            return Err(MimirError::message(format!(
                "manifest rank drift at row {expected_rank}: found {}",
                row.rank
            )));
        }
        if row.fixture_id.trim().is_empty() {
            return Err(MimirError::message(format!(
                "manifest row {expected_rank} has empty fixture_id"
            )));
        }
        if !is_safe_basename(&row.filename) {
            return Err(MimirError::message(format!(
                "manifest row {expected_rank} filename is not a safe basename: {}",
                row.filename
            )));
        }
        if row.bytes == 0 {
            return Err(MimirError::message(format!(
                "manifest row {expected_rank} has zero bytes"
            )));
        }
        if !is_sha256_hex(&row.sha256) {
            return Err(MimirError::message(format!(
                "manifest row {expected_rank} has invalid SHA-256: {}",
                row.sha256
            )));
        }
        if !fixture_ids.insert(row.fixture_id.clone()) {
            return Err(MimirError::message(format!(
                "duplicate fixture_id in manifest: {}",
                row.fixture_id
            )));
        }
        if !filenames.insert(row.filename.clone()) {
            return Err(MimirError::message(format!(
                "duplicate filename in manifest: {}",
                row.filename
            )));
        }
        if !hashes.insert(row.sha256.to_ascii_uppercase()) {
            return Err(MimirError::message(format!(
                "duplicate SHA-256 in manifest: {}",
                row.sha256
            )));
        }
    }

    Ok(())
}

fn validate_replay_file_count(corpus_root: &Path) -> Result<()> {
    let entries = fs::read_dir(corpus_root).map_err(|error| MimirError::io(corpus_root, error))?;
    let mut replay_count = 0usize;

    for entry in entries {
        let entry = entry.map_err(|error| MimirError::io(corpus_root, error))?;
        let path = entry.path();
        if entry
            .file_type()
            .map_err(|error| MimirError::io(&path, error))?
            .is_file()
            && path
                .extension()
                .is_some_and(|extension| extension.eq_ignore_ascii_case("replay"))
        {
            replay_count += 1;
        }
    }

    if replay_count != EXPECTED_CORPUS_ROWS {
        return Err(MimirError::message(format!(
            "replay compatibility matrix requires exactly {EXPECTED_CORPUS_ROWS} .replay files, found {replay_count}"
        )));
    }

    Ok(())
}

fn scan_rows(corpus_root: &Path, manifest_rows: &[ManifestRow]) -> Result<Vec<ReplayCompatibilityRow>> {
    let mut rows = Vec::with_capacity(manifest_rows.len());

    for manifest in manifest_rows {
        let path = corpus_root.join(&manifest.filename);
        let bytes = fs::read(&path).map_err(|error| MimirError::io(&path, error))?;
        let actual_size = u64::try_from(bytes.len())
            .map_err(|_| MimirError::message(format!("file size cannot fit u64: {}", path.display())))?;
        if actual_size != manifest.bytes {
            return Err(MimirError::message(format!(
                "replay size mismatch for {}: manifest={}, actual={actual_size}",
                manifest.filename, manifest.bytes
            )));
        }

        let actual_sha256 = sha256_upper(&bytes);
        if !actual_sha256.eq_ignore_ascii_case(&manifest.sha256) {
            return Err(MimirError::message(format!(
                "replay SHA-256 mismatch for {}: manifest={}, actual={actual_sha256}",
                manifest.filename, manifest.sha256
            )));
        }

        let preamble = observe_header_preamble(&bytes);
        let input = ReplayInput::Memory {
            label: manifest.fixture_id.clone(),
            bytes,
        };

        let row = match MinimalReplayHeaderReader.read_header(&input) {
            Ok(header) => {
                let replay_version = match header.metadata.get("ReplayVersion") {
                    Some(FieldValue::Integer(value)) => i32::try_from(*value).ok(),
                    _ => None,
                };
                let build_version = match header.metadata.get("BuildVersion") {
                    Some(FieldValue::Text(value)) => Some(value.clone()),
                    _ => None,
                };

                if preamble.major_version.is_none()
                    || preamble.minor_version.is_none()
                    || preamble.net_version.is_none()
                    || preamble.game_type.is_none()
                    || replay_version.is_none()
                    || build_version.is_none()
                {
                    return Err(MimirError::message(format!(
                        "scanner observation drift after successful parser result for {}",
                        manifest.filename
                    )));
                }

                ReplayCompatibilityRow {
                    rank: manifest.rank,
                    fixture_id: manifest.fixture_id.clone(),
                    filename: manifest.filename.clone(),
                    bytes: manifest.bytes,
                    sha256: manifest.sha256.to_ascii_uppercase(),
                    size_verified: true,
                    sha256_verified: true,
                    header_parse: "supported".to_string(),
                    major_version: preamble.major_version,
                    minor_version: preamble.minor_version,
                    net_version: preamble.net_version,
                    game_type: preamble.game_type,
                    replay_version,
                    build_version,
                    failure_stage: None,
                    failure_category: None,
                    failure_reason: None,
                    raw_state_status: STATUS_NOT_IMPLEMENTED,
                    event_layer_status: STATUS_NOT_IMPLEMENTED,
                    skill_layer_status: STATUS_NOT_IMPLEMENTED,
                }
            }
            Err(error) => {
                let reason = error.to_string();
                let class = classify_parser_error(&reason);
                let mut observed = preamble;
                if let Some(tuple) = parse_unsupported_version_tuple(&reason) {
                    observed = tuple;
                }

                ReplayCompatibilityRow {
                    rank: manifest.rank,
                    fixture_id: manifest.fixture_id.clone(),
                    filename: manifest.filename.clone(),
                    bytes: manifest.bytes,
                    sha256: manifest.sha256.to_ascii_uppercase(),
                    size_verified: true,
                    sha256_verified: true,
                    header_parse: class.header_parse.to_string(),
                    major_version: observed.major_version,
                    minor_version: observed.minor_version,
                    net_version: observed.net_version,
                    game_type: observed.game_type,
                    replay_version: observed.replay_version,
                    build_version: observed.build_version,
                    failure_stage: Some(class.stage.to_string()),
                    failure_category: Some(class.category.to_string()),
                    failure_reason: Some(reason),
                    raw_state_status: STATUS_NOT_IMPLEMENTED,
                    event_layer_status: STATUS_NOT_IMPLEMENTED,
                    skill_layer_status: STATUS_NOT_IMPLEMENTED,
                }
            }
        };

        rows.push(row);
    }

    Ok(rows)
}

fn summarize_rows(rows: &[ReplayCompatibilityRow]) -> ReplayCompatibilitySummary {
    let mut supported = 0usize;
    let mut unsupported = 0usize;
    let mut malformed = 0usize;
    let mut mapping_error = 0usize;
    let mut other_error = 0usize;
    let mut category_counts = BTreeMap::<String, usize>::new();
    let mut version_tuples = BTreeSet::new();
    let mut builds = BTreeSet::new();
    let mut total_bytes = 0u64;

    for row in rows {
        total_bytes = total_bytes.saturating_add(row.bytes);
        match row.header_parse.as_str() {
            "supported" => supported += 1,
            "unsupported" => unsupported += 1,
            "malformed" => malformed += 1,
            "mapping_error" => mapping_error += 1,
            _ => other_error += 1,
        }

        if let Some(category) = &row.failure_category {
            *category_counts.entry(category.clone()).or_default() += 1;
        }
        if let Some(build) = &row.build_version {
            builds.insert(build.clone());
        }
        if let (
            Some(major),
            Some(minor),
            Some(net),
            Some(game_type),
            Some(replay_version),
            Some(build_version),
        ) = (
            row.major_version,
            row.minor_version,
            row.net_version,
            row.game_type.as_deref(),
            row.replay_version,
            row.build_version.as_deref(),
        ) {
            version_tuples.insert(format!(
                "{major}|{minor}|{net}|{game_type}|{replay_version}|{build_version}"
            ));
        }
    }

    ReplayCompatibilitySummary {
        scanned: rows.len(),
        total_bytes,
        supported,
        unsupported,
        malformed,
        mapping_error,
        other_error,
        unique_version_tuples: version_tuples.len(),
        unique_builds: builds.len(),
        category_counts,
    }
}

fn classify_parser_error(message: &str) -> FailureClass {
    if message.contains("replay header parse error: unsupported-version:") {
        FailureClass {
            header_parse: "unsupported",
            stage: "support_gate",
            category: "unsupported_version",
        }
    } else if message.contains("replay header parse error: unsupported-property:") {
        FailureClass {
            header_parse: "unsupported",
            stage: "header_properties",
            category: "unsupported_property",
        }
    } else if message.contains("replay header parse error: unsupported-text:") {
        FailureClass {
            header_parse: "unsupported",
            stage: "header_text",
            category: "unsupported_text",
        }
    } else if message.contains("replay header parse error: unsupported-input:") {
        FailureClass {
            header_parse: "unsupported",
            stage: "input",
            category: "unsupported_input",
        }
    } else if message.contains("replay header parse error: insufficient:") {
        FailureClass {
            header_parse: "malformed",
            stage: "header_layout",
            category: "insufficient",
        }
    } else if message.contains("replay header parse error: malformed:") {
        FailureClass {
            header_parse: "malformed",
            stage: "header_layout",
            category: "malformed",
        }
    } else if message.contains("replay header mapping error:") {
        FailureClass {
            header_parse: "mapping_error",
            stage: "mapping",
            category: "mapping_error",
        }
    } else {
        FailureClass {
            header_parse: "error",
            stage: "unknown",
            category: "other_error",
        }
    }
}

fn parse_unsupported_version_tuple(message: &str) -> Option<HeaderVersionObservation> {
    let marker = "unsupported tuple major=";
    let mut rest = message.split_once(marker)?.1;
    let (major, next) = rest.split_once(", minor=")?;
    rest = next;
    let (minor, next) = rest.split_once(", net=")?;
    rest = next;
    let (net, next) = rest.split_once(", game_type=")?;
    rest = next;
    let (game_type, next) = rest.split_once(", ReplayVersion=")?;
    rest = next;
    let (replay_version, build_version) = rest.split_once(", BuildVersion=")?;

    Some(HeaderVersionObservation {
        major_version: major.parse().ok(),
        minor_version: minor.parse().ok(),
        net_version: net.parse().ok(),
        game_type: Some(game_type.to_string()),
        replay_version: replay_version.parse().ok(),
        build_version: Some(build_version.to_string()),
    })
}

fn observe_header_preamble(bytes: &[u8]) -> HeaderVersionObservation {
    let mut observed = HeaderVersionObservation::default();
    let Some(header_size) = read_i32_at(bytes, 0, bytes.len()) else {
        return observed;
    };
    if header_size < 0 {
        return observed;
    }
    let Ok(header_len) = usize::try_from(header_size) else {
        return observed;
    };
    let Some(header_end) = 8usize.checked_add(header_len) else {
        return observed;
    };
    if header_end > bytes.len() {
        return observed;
    }

    observed.major_version = read_i32_at(bytes, 8, header_end);
    observed.minor_version = read_i32_at(bytes, 12, header_end);
    observed.net_version = read_i32_at(bytes, 16, header_end);

    let Some(text_len) = read_i32_at(bytes, 20, header_end) else {
        return observed;
    };
    if text_len <= 0 {
        return observed;
    }
    let Ok(text_len) = usize::try_from(text_len) else {
        return observed;
    };
    let text_start = 24usize;
    let Some(text_end) = text_start.checked_add(text_len) else {
        return observed;
    };
    if text_end > header_end {
        return observed;
    }
    let raw = &bytes[text_start..text_end];
    if raw.last() != Some(&0) {
        return observed;
    }
    if let Ok(game_type) = std::str::from_utf8(&raw[..raw.len() - 1]) {
        observed.game_type = Some(game_type.to_string());
    }

    observed
}

fn read_i32_at(bytes: &[u8], offset: usize, limit: usize) -> Option<i32> {
    let end = offset.checked_add(4)?;
    if end > limit || end > bytes.len() {
        return None;
    }
    Some(i32::from_le_bytes(bytes[offset..end].try_into().ok()?))
}

fn is_safe_basename(filename: &str) -> bool {
    let path = Path::new(filename);
    !filename.trim().is_empty()
        && path.file_name().is_some_and(|name| name == path.as_os_str())
        && path.extension().is_some_and(|extension| extension.eq_ignore_ascii_case("replay"))
}

fn is_sha256_hex(value: &str) -> bool {
    value.len() == 64 && value.bytes().all(|byte| byte.is_ascii_hexdigit())
}

fn write_jsonl(path: &Path, rows: &[ReplayCompatibilityRow]) -> Result<()> {
    ensure_parent(path)?;
    let mut encoded = String::new();
    for row in rows {
        encoded.push_str(&serde_json::to_string(row)?);
        encoded.push('\n');
    }
    fs::write(path, encoded).map_err(|error| MimirError::io(path, error))
}

fn write_pretty_json<T: Serialize>(path: &Path, value: &T) -> Result<()> {
    ensure_parent(path)?;
    let encoded = serde_json::to_string_pretty(value)?;
    fs::write(path, format!("{encoded}\n")).map_err(|error| MimirError::io(path, error))
}

fn ensure_parent(path: &Path) -> Result<()> {
    if let Some(parent) = path.parent().filter(|parent| !parent.as_os_str().is_empty()) {
        fs::create_dir_all(parent).map_err(|error| MimirError::io(parent, error))?;
    }
    Ok(())
}

fn sha256_upper(input: &[u8]) -> String {
    const INITIAL: [u32; 8] = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c,
        0x1f83d9ab, 0x5be0cd19,
    ];
    const K: [u32; 64] = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
        0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
        0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
        0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
        0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
        0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ];

    let bit_len = u64::try_from(input.len())
        .expect("usize should fit u64 on supported targets")
        .saturating_mul(8);
    let mut padded = input.to_vec();
    padded.push(0x80);
    while padded.len() % 64 != 56 {
        padded.push(0);
    }
    padded.extend_from_slice(&bit_len.to_be_bytes());

    let mut state = INITIAL;
    for chunk in padded.chunks_exact(64) {
        let mut words = [0u32; 64];
        for (index, word_bytes) in chunk.chunks_exact(4).take(16).enumerate() {
            words[index] = u32::from_be_bytes(
                word_bytes
                    .try_into()
                    .expect("chunks_exact(4) should yield four bytes"),
            );
        }
        for index in 16..64 {
            let s0 = words[index - 15].rotate_right(7)
                ^ words[index - 15].rotate_right(18)
                ^ (words[index - 15] >> 3);
            let s1 = words[index - 2].rotate_right(17)
                ^ words[index - 2].rotate_right(19)
                ^ (words[index - 2] >> 10);
            words[index] = words[index - 16]
                .wrapping_add(s0)
                .wrapping_add(words[index - 7])
                .wrapping_add(s1);
        }

        let mut a = state[0];
        let mut b = state[1];
        let mut c = state[2];
        let mut d = state[3];
        let mut e = state[4];
        let mut f = state[5];
        let mut g = state[6];
        let mut h = state[7];

        for index in 0..64 {
            let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let choose = (e & f) ^ ((!e) & g);
            let temp1 = h
                .wrapping_add(s1)
                .wrapping_add(choose)
                .wrapping_add(K[index])
                .wrapping_add(words[index]);
            let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let majority = (a & b) ^ (a & c) ^ (b & c);
            let temp2 = s0.wrapping_add(majority);

            h = g;
            g = f;
            f = e;
            e = d.wrapping_add(temp1);
            d = c;
            c = b;
            b = a;
            a = temp1.wrapping_add(temp2);
        }

        state[0] = state[0].wrapping_add(a);
        state[1] = state[1].wrapping_add(b);
        state[2] = state[2].wrapping_add(c);
        state[3] = state[3].wrapping_add(d);
        state[4] = state[4].wrapping_add(e);
        state[5] = state[5].wrapping_add(f);
        state[6] = state[6].wrapping_add(g);
        state[7] = state[7].wrapping_add(h);
    }

    let mut output = String::with_capacity(64);
    for word in state {
        write!(&mut output, "{word:08X}").expect("writing to String should not fail");
    }
    output
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sha256_matches_known_vector() {
        assert_eq!(
            sha256_upper(b"abc"),
            "BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD"
        );
    }

    #[test]
    fn unsupported_version_error_yields_structured_tuple() {
        let message = "replay header parse error: unsupported-version: unsupported tuple major=867, minor=32, net=10, game_type=TAGame.Replay_Soccar_TA, ReplayVersion=8, BuildVersion=251020.62592.500295";
        let observed = parse_unsupported_version_tuple(message).expect("tuple should parse");

        assert_eq!(observed.major_version, Some(867));
        assert_eq!(observed.minor_version, Some(32));
        assert_eq!(observed.net_version, Some(10));
        assert_eq!(
            observed.game_type.as_deref(),
            Some("TAGame.Replay_Soccar_TA")
        );
        assert_eq!(observed.replay_version, Some(8));
        assert_eq!(
            observed.build_version.as_deref(),
            Some("251020.62592.500295")
        );
    }

    #[test]
    fn parser_error_taxonomy_is_explicit() {
        assert_eq!(
            classify_parser_error("replay header parse error: unsupported-property: x"),
            FailureClass {
                header_parse: "unsupported",
                stage: "header_properties",
                category: "unsupported_property",
            }
        );
        assert_eq!(
            classify_parser_error("replay header parse error: malformed: x"),
            FailureClass {
                header_parse: "malformed",
                stage: "header_layout",
                category: "malformed",
            }
        );
        assert_eq!(
            classify_parser_error("replay header mapping error: x"),
            FailureClass {
                header_parse: "mapping_error",
                stage: "mapping",
                category: "mapping_error",
            }
        );
    }

    #[test]
    fn preamble_observer_reads_bounded_ascii_game_type() {
        let game_type = b"TAGame.Replay_Soccar_TA";
        let mut header = Vec::new();
        header.extend_from_slice(&868i32.to_le_bytes());
        header.extend_from_slice(&32i32.to_le_bytes());
        header.extend_from_slice(&10i32.to_le_bytes());
        header.extend_from_slice(
            &i32::try_from(game_type.len() + 1)
                .expect("test string length should fit i32")
                .to_le_bytes(),
        );
        header.extend_from_slice(game_type);
        header.push(0);

        let mut replay = Vec::new();
        replay.extend_from_slice(
            &i32::try_from(header.len())
                .expect("test header length should fit i32")
                .to_le_bytes(),
        );
        replay.extend_from_slice(&0u32.to_le_bytes());
        replay.extend_from_slice(&header);

        let observed = observe_header_preamble(&replay);
        assert_eq!(observed.major_version, Some(868));
        assert_eq!(observed.minor_version, Some(32));
        assert_eq!(observed.net_version, Some(10));
        assert_eq!(
            observed.game_type.as_deref(),
            Some("TAGame.Replay_Soccar_TA")
        );
    }
}
