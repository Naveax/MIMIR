from __future__ import annotations

import hashlib
import json
from pathlib import Path

ORACLE_PATH = Path('.tmp/r3_14a/r3_14a_first_actor_envelope.jsonl')
EXPECTED_ORACLE_SHA = 'c70e77df7af81b436cb545d070bb90c82f562d0b'
EXPECTED_EVIDENCE_HEAD = 'f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1'
EXPECTED_SELECTOR = '28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55'
EXPECTED_R3_14A_PRODUCTION = 'ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa'


def rust_string(value: object) -> str:
    return json.dumps(str(value))


def rust_opt_bool(value: object) -> str:
    if value is None:
        return 'None'
    return f'Some({str(bool(value)).lower()})'


def rust_opt_u32(value: object) -> str:
    if value is None:
        return 'None'
    return f'Some({int(value)}u32)'


rows = [json.loads(line) for line in ORACLE_PATH.read_text(encoding='utf-8').splitlines() if line.strip()]
errors: list[str] = []

if len(rows) != 47:
    errors.append(f'row count {len(rows)} != 47')
if len({row['sha256'].lower() for row in rows}) != 47:
    errors.append('unique replay SHA-256 count != 47')
if len({row['relative_path'] for row in rows}) != 47:
    errors.append('unique replay path count != 47')

verified_inputs = []
for index, row in enumerate(rows, 1):
    if row.get('oracle_sha') != EXPECTED_ORACLE_SHA:
        errors.append(f'row {index}: oracle SHA mismatch')
    if row.get('mimir_evidence_head') != EXPECTED_EVIDENCE_HEAD:
        errors.append(f'row {index}: evidence head mismatch')
    if row.get('selector_manifest_sha256') != EXPECTED_SELECTOR:
        errors.append(f'row {index}: selector manifest mismatch')
    if row.get('production_code_sha') != EXPECTED_R3_14A_PRODUCTION:
        errors.append(f'row {index}: R3.14A production identity mismatch')

    path = Path(row['relative_path'])
    if not path.is_file():
        errors.append(f'row {index}: missing replay {path}')
        continue
    data = path.read_bytes()
    actual_length = len(data)
    actual_sha = hashlib.sha256(data).hexdigest()
    if actual_length != int(row['byte_length']):
        errors.append(f'row {index}: byte length mismatch for {path}')
    if actual_sha != row['sha256'].lower():
        errors.append(f'row {index}: SHA-256 mismatch for {path}')

    verified_inputs.append({
        'corpus_index': row['corpus_index'],
        'relative_path': row['relative_path'],
        'byte_length': actual_length,
        'sha256': actual_sha,
        'build_version': row['build_version'],
        'network_start': row['network_start'],
        'network_size': row['network_size'],
        'max_channels': row['max_channels'],
        'channel_bits': row['channel_bits'],
    })

if errors:
    Path('r3_14e_identity_errors.txt').write_text('\n'.join(errors) + '\n', encoding='utf-8')
    raise SystemExit('\n'.join(errors))

Path('r3_14e_verified_inputs.json').write_text(
    json.dumps(verified_inputs, indent=2, sort_keys=True) + '\n',
    encoding='utf-8',
)

cases: list[str] = []
for row in rows:
    actor = row.get('actor_id')
    actor_value = None if actor is None else actor.get('value')
    cases.append(f'''    Case {{
        path: {rust_string(row['relative_path'])},
        build_version: {rust_string(row['build_version'])},
        network_start: {int(row['network_start'])}u64,
        network_size: {int(row['network_size'])}u32,
        max_channels: {int(row['max_channels'])}u32,
        channel_bits: {int(row['channel_bits'])}u8,
        time_raw: {int(row['time_raw_u32'])}u32,
        delta_raw: {int(row['delta_raw_u32'])}u32,
        actor_present: {str(bool(row['actor_present'])).lower()},
        actor_id: {rust_opt_u32(actor_value)},
        alive: {rust_opt_bool(row.get('alive'))},
        is_new: {rust_opt_bool(row.get('new'))},
        stop_bit: {int(row['stop_bit'])}u64,
    }}''')

source = '''use mimir_replay::{
    MinimalReplayNetworkFirstActorEnvelopeReader, ReplayInput,
    ReplayNetworkFirstActorEnvelopeReader,
};
use mimir_types::FieldValue;
use std::fs;
use std::path::PathBuf;

#[derive(Clone, Copy)]
struct Case {
    path: &'static str,
    build_version: &'static str,
    network_start: u64,
    network_size: u32,
    max_channels: u32,
    channel_bits: u8,
    time_raw: u32,
    delta_raw: u32,
    actor_present: bool,
    actor_id: Option<u32>,
    alive: Option<bool>,
    is_new: Option<bool>,
    stop_bit: u64,
}

const CASES: &[Case] = &[
''' + ',\n'.join(cases) + '''
];

#[test]
fn r3_14e_native_matches_pinned_oracle_on_exact_47() {
    assert_eq!(CASES.len(), 47);
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
    let reader = MinimalReplayNetworkFirstActorEnvelopeReader;
    let mut parsed = 0usize;

    for (index, case) in CASES.iter().enumerate() {
        let bytes = fs::read(root.join(case.path))
            .unwrap_or_else(|error| panic!("case {} {} read failed: {error}", index + 1, case.path));
        let input = ReplayInput::Memory {
            label: case.path.to_string(),
            bytes,
        };
        let native = reader
            .read_network_first_actor_envelope(&input)
            .unwrap_or_else(|error| panic!("case {} {} native parse failed: {error}", index + 1, case.path));

        let build_version = match native.timing.header.metadata.get("BuildVersion") {
            Some(FieldValue::Text(value)) => value.as_str(),
            other => panic!("case {} {} BuildVersion metadata mismatch: {:?}", index + 1, case.path, other),
        };
        assert_eq!(build_version, case.build_version, "case {} {} BuildVersion", index + 1, case.path);
        assert_eq!(native.timing.content.network_start, case.network_start, "case {} {} network_start", index + 1, case.path);
        assert_eq!(native.timing.content.network_size, case.network_size, "case {} {} network_size", index + 1, case.path);
        assert_eq!(native.timing.max_channels, case.max_channels, "case {} {} max_channels", index + 1, case.path);
        assert_eq!(native.timing.channel_bits, case.channel_bits, "case {} {} channel_bits", index + 1, case.path);
        assert_eq!(native.first_frame_time_raw_u32, case.time_raw, "case {} {} time_raw", index + 1, case.path);
        assert_eq!(native.first_frame_delta_raw_u32, case.delta_raw, "case {} {} delta_raw", index + 1, case.path);
        assert_eq!(native.actor_present, case.actor_present, "case {} {} actor_present", index + 1, case.path);
        assert_eq!(native.actor_id, case.actor_id, "case {} {} actor_id", index + 1, case.path);
        assert_eq!(native.alive, case.alive, "case {} {} alive", index + 1, case.path);
        assert_eq!(native.is_new, case.is_new, "case {} {} new", index + 1, case.path);
        assert_eq!(native.stop_bit, case.stop_bit, "case {} {} stop_bit", index + 1, case.path);
        parsed += 1;
    }

    assert_eq!(parsed, 47);
    println!("R3_14E_NATIVE_PARSE_SUCCESS=47");
    println!("R3_14E_EXACT_MATCH=47");
}
'''

test_path = Path('crates/mimir-replay/tests/_tmp_r3_14e_differential.rs')
test_path.parent.mkdir(parents=True, exist_ok=True)
test_path.write_text(source, encoding='utf-8', newline='\n')
print('R3_14E_IDENTITY_VERIFICATION=PASS')
print('R3_14E_INPUT_COUNT=47')
print('R3_14E_UNIQUE_SHA=47')
