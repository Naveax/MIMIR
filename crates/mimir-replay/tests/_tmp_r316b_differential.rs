use mimir_replay::{
    decode_replay_network_existing_actor_first_property_header_v1,
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader, ReplayContentScaffoldReader,
    ReplayInput, ReplayNetworkLookupPlanReader,
};
use std::path::{Path, PathBuf};

#[derive(Debug)]
struct OracleRow {
    relative_path: String,
    actor_object_index: u32,
    property_present_start_bit: u64,
    property_present_end_bit: u64,
    stream_id_start_bit: u64,
    stream_id_end_bit: u64,
    stream_id: u32,
    stream_id_bound: u32,
    prop_id_bits: u8,
    property_object_index: u32,
    property_object_name: String,
    attribute_tag: String,
    payload_start_bit: u64,
}

fn parse_u32(value: &str, label: &str) -> u32 {
    value.parse().unwrap_or_else(|error| panic!("{label}={value}: {error}"))
}

fn parse_u64(value: &str, label: &str) -> u64 {
    value.parse().unwrap_or_else(|error| panic!("{label}={value}: {error}"))
}

fn load_oracle(path: &Path) -> Vec<OracleRow> {
    let text = std::fs::read_to_string(path)
        .unwrap_or_else(|error| panic!("read oracle {}: {error}", path.display()));
    text.lines()
        .filter(|line| !line.is_empty())
        .map(|line| {
            let fields: Vec<_> = line.split('\t').collect();
            assert_eq!(fields.len(), 13, "unexpected oracle column count: {line}");
            OracleRow {
                relative_path: fields[0].to_owned(),
                actor_object_index: parse_u32(fields[1], "actor_object_index"),
                property_present_start_bit: parse_u64(fields[2], "property_present_start_bit"),
                property_present_end_bit: parse_u64(fields[3], "property_present_end_bit"),
                stream_id_start_bit: parse_u64(fields[4], "stream_id_start_bit"),
                stream_id_end_bit: parse_u64(fields[5], "stream_id_end_bit"),
                stream_id: parse_u32(fields[6], "stream_id"),
                stream_id_bound: parse_u32(fields[7], "stream_id_bound"),
                prop_id_bits: fields[8]
                    .parse()
                    .unwrap_or_else(|error| panic!("prop_id_bits={}: {error}", fields[8])),
                property_object_index: parse_u32(fields[9], "property_object_index"),
                property_object_name: fields[10].to_owned(),
                attribute_tag: fields[11].to_owned(),
                payload_start_bit: parse_u64(fields[12], "payload_start_bit"),
            }
        })
        .collect()
}

#[test]
#[ignore = "requires immutable R3.16A receipt extraction in GitHub Actions"]
fn r3_16b_native_property_header_matches_all_47_r3_16a_oracle_rows() {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
    let oracle_path = std::env::var_os("MIMIR_R316B_ORACLE_TSV")
        .map(PathBuf::from)
        .unwrap_or_else(|| root.join("target/r316b_oracle.tsv"));
    let rows = load_oracle(&oracle_path);
    assert_eq!(rows.len(), 47, "R3.16B requires the exact 47-row R3.16A oracle");

    let mut matched = 0usize;
    for row in rows {
        let replay_path = root.join(&row.relative_path);
        let bytes = std::fs::read(&replay_path)
            .unwrap_or_else(|error| panic!("{}: {error}", replay_path.display()));
        let input = ReplayInput::Memory {
            label: row.relative_path.clone(),
            bytes: bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&input)
            .unwrap_or_else(|error| panic!("{}: scaffold: {error}", row.relative_path));
        let network_start = usize::try_from(scaffold.network_start).expect("network_start usize");
        let network_end = usize::try_from(scaffold.network_end).expect("network_end usize");
        let network = bytes
            .get(network_start..network_end)
            .unwrap_or_else(|| panic!("{}: invalid network slice", row.relative_path));
        let plan = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&input)
            .unwrap_or_else(|error| panic!("{}: lookup plan: {error}", row.relative_path));

        let header = decode_replay_network_existing_actor_first_property_header_v1(
            network,
            row.property_present_start_bit,
            row.actor_object_index,
            &plan,
        )
        .unwrap_or_else(|error| panic!("{}: native header: {error}", row.relative_path));

        assert!(header.property_present, "{}: property_present", row.relative_path);
        assert_eq!(
            header.property_present_start_bit, row.property_present_start_bit,
            "{}: property_present_start_bit", row.relative_path
        );
        assert_eq!(
            header.property_present_end_bit, row.property_present_end_bit,
            "{}: property_present_end_bit", row.relative_path
        );
        assert_eq!(
            header.stream_id_start_bit,
            Some(row.stream_id_start_bit),
            "{}: stream_id_start_bit", row.relative_path
        );
        assert_eq!(
            header.stream_id_end_bit,
            Some(row.stream_id_end_bit),
            "{}: stream_id_end_bit", row.relative_path
        );
        assert_eq!(header.stream_id, Some(row.stream_id), "{}: stream_id", row.relative_path);
        assert_eq!(
            header.stream_id_bound,
            Some(row.stream_id_bound),
            "{}: stream_id_bound", row.relative_path
        );
        assert_eq!(
            header.prop_id_bits,
            Some(row.prop_id_bits),
            "{}: prop_id_bits", row.relative_path
        );
        assert_eq!(
            header.resolved_property_object_index,
            Some(row.property_object_index),
            "{}: property_object_index", row.relative_path
        );
        assert_eq!(
            header.resolved_property_object_name.as_deref(),
            Some(row.property_object_name.as_str()),
            "{}: property_object_name", row.relative_path
        );
        assert_eq!(
            header
                .resolved_attribute_tag
                .map(|tag| format!("{tag:?}"))
                .as_deref(),
            Some(row.attribute_tag.as_str()),
            "{}: attribute_tag", row.relative_path
        );
        assert_eq!(
            header.payload_start_bit,
            Some(row.payload_start_bit),
            "{}: payload_start_bit", row.relative_path
        );
        assert_eq!(
            header.stop_bit, row.payload_start_bit,
            "{}: hard stop must equal payload start", row.relative_path
        );
        matched += 1;
    }

    assert_eq!(matched, 47);
    println!("R3_16B_DIFFERENTIAL_MATCHED={matched}");
    println!("R3_16B_DIFFERENTIAL=PASS");
}
