use mimir_replay::{
    decode_replay_network_primitive_scalar_v1, MinimalReplayContentScaffoldReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkPrimitiveScalarValueV1,
};
use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone)]
struct WitnessRow {
    relative_path: String,
    tag: ReplayNetworkAttributeTagV1,
    tag_name: String,
    payload_start_bit: u64,
    payload_end_bit: u64,
    payload_width: u8,
    next_cursor_bit: u64,
    expected: String,
}

fn parse_tag(value: &str) -> ReplayNetworkAttributeTagV1 {
    match value {
        "Boolean" => ReplayNetworkAttributeTagV1::Boolean,
        "Byte" => ReplayNetworkAttributeTagV1::Byte,
        "Enum" => ReplayNetworkAttributeTagV1::Enum,
        "Float" => ReplayNetworkAttributeTagV1::Float,
        "Int" => ReplayNetworkAttributeTagV1::Int,
        "Int64" => ReplayNetworkAttributeTagV1::Int64,
        other => panic!("unsupported R3.17D witness tag: {other}"),
    }
}

fn load_witnesses(path: &Path) -> Vec<WitnessRow> {
    let text = std::fs::read_to_string(path)
        .unwrap_or_else(|error| panic!("read witness TSV {}: {error}", path.display()));
    text.lines()
        .filter(|line| !line.is_empty())
        .map(|line| {
            let fields: Vec<_> = line.split('\t').collect();
            assert_eq!(fields.len(), 7, "unexpected witness column count: {line}");
            let tag_name = fields[1].to_owned();
            WitnessRow {
                relative_path: fields[0].to_owned(),
                tag: parse_tag(fields[1]),
                tag_name,
                payload_start_bit: fields[2]
                    .parse()
                    .unwrap_or_else(|error| panic!("payload_start_bit={}: {error}", fields[2])),
                payload_end_bit: fields[3]
                    .parse()
                    .unwrap_or_else(|error| panic!("payload_end_bit={}: {error}", fields[3])),
                payload_width: fields[4]
                    .parse()
                    .unwrap_or_else(|error| panic!("payload_width={}: {error}", fields[4])),
                next_cursor_bit: fields[5]
                    .parse()
                    .unwrap_or_else(|error| panic!("next_cursor_bit={}: {error}", fields[5])),
                expected: fields[6].to_owned(),
            }
        })
        .collect()
}

fn native_value_repr(value: &ReplayNetworkPrimitiveScalarValueV1) -> String {
    match value {
        ReplayNetworkPrimitiveScalarValueV1::Boolean(value) => {
            if *value { "1".to_owned() } else { "0".to_owned() }
        }
        ReplayNetworkPrimitiveScalarValueV1::Byte(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Enum(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Float { raw_bits, value } => {
            assert_eq!(*raw_bits, value.to_bits(), "float raw/value bit identity");
            raw_bits.to_string()
        }
        ReplayNetworkPrimitiveScalarValueV1::Int(value) => value.to_string(),
        ReplayNetworkPrimitiveScalarValueV1::Int64(value) => value.to_string(),
    }
}

#[test]
#[ignore = "requires immutable R3.17A receipt extraction in GitHub Actions"]
fn r3_17d_native_scalar_decoder_matches_all_96_frozen_r3_17a_witnesses() {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
    let witness_path = std::env::var_os("MIMIR_R317D_WITNESS_TSV")
        .map(PathBuf::from)
        .unwrap_or_else(|| root.join("target/r317d_scalar_witnesses.tsv"));
    let comparison_path = std::env::var_os("MIMIR_R317D_COMPARISON_TSV")
        .map(PathBuf::from)
        .unwrap_or_else(|| root.join("target/r317d_comparison.tsv"));

    let rows = load_witnesses(&witness_path);
    assert_eq!(rows.len(), 96, "R3.17D requires the exact 96 frozen witnesses");

    let mut tag_counts: BTreeMap<String, usize> = BTreeMap::new();
    for row in &rows {
        *tag_counts.entry(row.tag_name.clone()).or_default() += 1;
    }
    for tag in ["Boolean", "Byte", "Enum", "Float", "Int", "Int64"] {
        assert_eq!(tag_counts.get(tag), Some(&16usize), "{tag} witness count");
    }

    let mut by_replay: BTreeMap<String, Vec<WitnessRow>> = BTreeMap::new();
    for row in rows {
        by_replay
            .entry(row.relative_path.clone())
            .or_default()
            .push(row);
    }

    let mut comparison = String::new();
    let mut matched = 0usize;
    for (relative_path, replay_rows) in by_replay {
        let replay_path = root.join(&relative_path);
        let bytes = std::fs::read(&replay_path)
            .unwrap_or_else(|error| panic!("{}: {error}", replay_path.display()));
        let input = ReplayInput::Memory {
            label: relative_path.clone(),
            bytes: bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&input)
            .unwrap_or_else(|error| panic!("{relative_path}: scaffold: {error}"));
        let network_start = usize::try_from(scaffold.network_start).expect("network_start usize");
        let network_end = usize::try_from(scaffold.network_end).expect("network_end usize");
        let network = bytes
            .get(network_start..network_end)
            .unwrap_or_else(|| panic!("{relative_path}: invalid network slice"));

        for row in replay_rows {
            assert_eq!(
                row.payload_end_bit,
                row.payload_start_bit + u64::from(row.payload_width),
                "{relative_path} {} frozen span",
                row.tag_name
            );
            assert_eq!(
                row.next_cursor_bit, row.payload_end_bit,
                "{relative_path} {} frozen next cursor",
                row.tag_name
            );

            let native = decode_replay_network_primitive_scalar_v1(
                network,
                row.payload_start_bit,
                row.tag,
            )
            .unwrap_or_else(|error| {
                panic!(
                    "{relative_path} {} @{} native decode: {error}",
                    row.tag_name, row.payload_start_bit
                )
            });

            assert_eq!(native.attribute_tag, row.tag, "{relative_path}: attribute tag");
            assert_eq!(
                native.payload_start_bit, row.payload_start_bit,
                "{relative_path} {}: payload_start_bit",
                row.tag_name
            );
            assert_eq!(
                native.payload_end_bit, row.payload_end_bit,
                "{relative_path} {}: payload_end_bit",
                row.tag_name
            );
            assert_eq!(
                native.payload_width, row.payload_width,
                "{relative_path} {}: payload_width",
                row.tag_name
            );
            assert_eq!(
                native.stop_bit, row.payload_end_bit,
                "{relative_path} {}: stop_bit",
                row.tag_name
            );

            let native_repr = native_value_repr(&native.value);
            assert_eq!(
                native_repr, row.expected,
                "{relative_path} {} @{}: scalar value",
                row.tag_name, row.payload_start_bit
            );

            comparison.push_str(&format!(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\tPASS\n",
                relative_path,
                row.tag_name,
                row.payload_start_bit,
                row.payload_end_bit,
                row.payload_width,
                row.expected,
                native_repr
            ));
            matched += 1;
        }
    }

    assert_eq!(matched, 96);
    std::fs::write(&comparison_path, comparison)
        .unwrap_or_else(|error| panic!("write {}: {error}", comparison_path.display()));
    println!("R3_17D_NATIVE_DECODE_SUCCESS={matched}");
    println!("R3_17D_EXACT_MATCH={matched}/96");
    println!("R3_17D_MISMATCH_COUNT=0");
    println!("R3_17D_NATIVE_ERROR_COUNT=0");
    println!("R3_17D_DIFFERENTIAL=PASS");
}
