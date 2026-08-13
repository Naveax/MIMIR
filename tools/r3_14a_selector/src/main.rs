use mimir_replay::{
    MinimalReplayHeaderReader, MinimalReplayNetworkLookupPlanReader, ReplayInput,
    ReplayNetworkLookupPlanReader, ReplayReader,
};
use mimir_types::FieldValue;
use sha2::{Digest, Sha256};
use std::collections::BTreeSet;
use std::fs;
use std::path::{Path, PathBuf};

const EXPECTED_REPLAY_COUNT: usize = 103;
const EXPECTED_SUPPORTED_LANE: usize = 47;

fn replay_paths() -> Result<Vec<PathBuf>, Box<dyn std::error::Error>> {
    let mut paths = vec![
        PathBuf::from("external_fixtures/sample_001.replay"),
        PathBuf::from("external_fixtures/sample_002.replay"),
        PathBuf::from("external_fixtures/sample_003.replay"),
    ];

    let mut corpus = fs::read_dir("test_corpus/largest_100")?
        .filter_map(|entry| entry.ok())
        .map(|entry| entry.path())
        .filter(|path| path.extension().is_some_and(|ext| ext == "replay"))
        .collect::<Vec<_>>();
    corpus.sort();
    paths.extend(corpus);
    Ok(paths)
}

fn display_path(path: &Path) -> String {
    path.to_string_lossy().replace('\\', "/")
}

fn metadata_text<'a>(
    header: &'a mimir_replay::ReplayHeader,
    key: &str,
) -> Result<&'a str, Box<dyn std::error::Error>> {
    match header.metadata.get(key) {
        Some(FieldValue::Text(value)) => Ok(value.as_str()),
        Some(other) => Err(format!("{key} must be text metadata, got {other:?}").into()),
        None => Err(format!("missing required metadata key {key}").into()),
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let paths = replay_paths()?;
    if paths.len() != EXPECTED_REPLAY_COUNT {
        return Err(format!(
            "expected {EXPECTED_REPLAY_COUNT} replay files, found {}",
            paths.len()
        )
        .into());
    }

    let mut supported = 0usize;
    let mut unsupported = 0usize;
    let mut supported_sha256 = BTreeSet::new();
    let mut manifest_hasher = Sha256::new();

    println!("R3.14A MIMIR Supported-Lane Selector");
    println!("expected_replays={EXPECTED_REPLAY_COUNT}");
    println!("expected_supported_lane={EXPECTED_SUPPORTED_LANE}");

    for (index, path) in paths.iter().enumerate() {
        let bytes = fs::read(path)?;
        let label = path
            .file_name()
            .map(|value| value.to_string_lossy().into_owned())
            .unwrap_or_else(|| display_path(path));
        let input = ReplayInput::Memory {
            label: label.clone(),
            bytes: bytes.clone(),
        };

        let header = match MinimalReplayHeaderReader.read_header(&input) {
            Ok(header) => header,
            Err(_) => {
                unsupported += 1;
                continue;
            }
        };

        let plan = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&input)
            .map_err(|error| {
                format!(
                    "R3.13 production lookup plan failed for supported replay {}: {error}",
                    display_path(path)
                )
            })?;

        if plan.header != header {
            return Err(format!(
                "header/lookup-plan identity drift for {}",
                display_path(path)
            )
            .into());
        }

        let build_version = metadata_text(&plan.header, "BuildVersion")?;
        let network = &plan.footer_lookup.scaffold.content;
        let replay_sha256 = format!("{:x}", Sha256::digest(&bytes));
        let relative_path = display_path(path);
        let canonical_row = format!(
            "{relative_path}\t{}\t{replay_sha256}\t{build_version}\t{}\t{}\t{}\t{}\n",
            bytes.len(),
            network.network_start,
            network.network_size,
            plan.max_channels,
            plan.channel_bits,
        );

        if !supported_sha256.insert(replay_sha256.clone()) {
            return Err(
                format!("duplicate supported replay SHA-256 detected: {replay_sha256}").into(),
            );
        }
        manifest_hasher.update(canonical_row.as_bytes());
        supported += 1;

        println!(
            "SUPPORTED\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            index + 1,
            relative_path,
            bytes.len(),
            replay_sha256,
            build_version,
            network.network_start,
            network.network_size,
            plan.max_channels,
            plan.channel_bits,
        );
    }

    let manifest_sha256 = format!("{:x}", manifest_hasher.finalize());

    println!("SUMMARY total_replays={}", paths.len());
    println!("SUMMARY supported_replays={supported}");
    println!("SUMMARY unsupported_replays={unsupported}");
    println!("SUMMARY unique_supported_sha256={}", supported_sha256.len());
    println!("SUMMARY manifest_sha256={manifest_sha256}");

    if supported != EXPECTED_SUPPORTED_LANE
        || unsupported != EXPECTED_REPLAY_COUNT - EXPECTED_SUPPORTED_LANE
    {
        return Err(format!(
            "supported-lane drift: supported={supported}, unsupported={unsupported}"
        )
        .into());
    }

    if supported_sha256.len() != EXPECTED_SUPPORTED_LANE {
        return Err(format!(
            "supported replay SHA-256 identity drift: expected {EXPECTED_SUPPORTED_LANE} unique hashes, found {}",
            supported_sha256.len()
        )
        .into());
    }

    println!("R3_14A_SELECTOR=PASS");
    Ok(())
}
