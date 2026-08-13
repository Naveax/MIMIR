import json
import sys
from pathlib import Path


def parse_kv(line, prefix):
    parts = line.rstrip('\n').split('\t')
    if parts[0] != prefix:
        raise ValueError(line[:80])
    out = {}
    for item in parts[1:]:
        key, sep, value = item.partition('=')
        if not sep or key in out:
            raise ValueError(item)
        out[key] = value
    return out


lines = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace').splitlines()
parse_ok = sum(line == 'R3_15A_ORACLE_PARSE=PASS' for line in lines)
raw_rows = [
    parse_kv(line, 'R3_16A_PROPERTY')
    for line in lines
    if line.startswith('R3_16A_PROPERTY\t')
]
paths = [
    line.strip()
    for line in Path('r3_16a_paths.txt').read_text(encoding='utf-8').splitlines()
    if line.strip()
]
path_set = set(paths)
by_path = {}
for raw in raw_rows:
    rel = raw['label'].replace('\\', '/')
    if rel in by_path:
        raise SystemExit(f'duplicate oracle row: {rel}')
    by_path[rel] = raw

missing = [rel for rel in paths if rel not in by_path]
extras = [rel for rel in by_path if rel not in path_set]
if extras:
    raise SystemExit(f'unknown oracle rows: {extras[:3]}')

selected = []
queries = []
for rel in paths:
    raw = by_path.get(rel)
    if raw is None:
        continue
    row = {
        'relative_path': rel,
        'frame_index': int(raw['frame_index']),
        'actor_ordinal': int(raw['actor_ordinal']),
        'frame_time_raw_bits': int(raw['frame_time_raw_bits']),
        'frame_delta_raw_bits': int(raw['frame_delta_raw_bits']),
        'actor_id': int(raw['actor_id']),
        'actor_context_object_id': int(raw['actor_context_object_id']),
        'actor_context_object_name': raw['actor_context_object_name'],
        'new_bit_end': int(raw['new_bit_end']),
        'property_present_start_bit': int(raw['property_present_start_bit']),
        'property_present_end_bit': int(raw['property_present_end_bit']),
        'property_present_value': raw['property_present_value'] == 'true',
        'stream_id_start_bit': int(raw['stream_id_start_bit']),
        'stream_id_end_bit': int(raw['stream_id_end_bit']),
        'stream_id_value': int(raw['stream_id_value']),
        'stream_id_bound': int(raw['stream_id_bound']),
        'prop_id_bits': int(raw['prop_id_bits']),
        'resolved_property_object_id': int(raw['resolved_property_object_id']),
        'resolved_property_object_name': raw['resolved_property_object_name'],
        'resolved_attribute_tag': raw['resolved_attribute_tag'],
        'payload_start_bit': int(raw['payload_start_bit']),
    }
    selected.append(row)
    queries.append(
        f"{rel}\t{row['actor_context_object_id']}\t{row['stream_id_value']}"
    )

Path('r3_16a_first_property_oracle.jsonl').write_text(
    ''.join(json.dumps(row, sort_keys=True) + '\n' for row in selected),
    encoding='utf-8',
)
Path('r3_16a_mimir_queries.tsv').write_text(
    '\n'.join(queries) + '\n',
    encoding='utf-8',
)
Path('r3_16a_oracle_selection_summary.json').write_text(
    json.dumps(
        {
            'replays_total': 47,
            'oracle_decode_success': parse_ok,
            'selected_existing_actor_property_rows': len(selected),
            'replays_without_candidate': len(missing),
            'missing_paths': missing,
        },
        indent=2,
        sort_keys=True,
    ) + '\n',
    encoding='utf-8',
)
print(
    f'R3_16A_ORACLE_SELECTION parse_success={parse_ok} '
    f'selected={len(selected)} missing={len(missing)}'
)
if parse_ok != 47 or len(selected) != 47 or missing:
    raise SystemExit('R3.16A oracle selection not complete')
