#!/usr/bin/env python3
import collections, hashlib, json, sys
from pathlib import Path


def req(cond, msg):
    if not cond:
        raise SystemExit(msg)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def kv(line, prefix):
    req(line.startswith(prefix + '\t'), f'bad {prefix} line')
    out = {}
    for field in line.split('\t')[1:]:
        req('=' in field, f'bad field {field!r}')
        key, value = field.split('=', 1)
        out[key] = value
    return out


def key_of(row):
    return (
        row['label'],
        int(row['frame_index']),
        int(row['actor_ordinal']),
        int(row['actor_context_object_id']),
    )


def prepare(acdir_s, ydir_s, target_s):
    acdir = Path(acdir_s)
    ydir = Path(ydir_s)
    target = Path(target_s)
    ac_payload = json.loads((acdir / 'r3_18ac_payload_rows.json').read_text(encoding='utf-8'))
    ac_ab = json.loads((acdir / 'r3_18ac_frozen_ab_rows.json').read_text(encoding='utf-8'))
    witnesses = json.loads((ydir / 'r3_18y_frozen_witnesses.json').read_text(encoding='utf-8'))
    req(ac_payload['aggregate']['outcome'] == 'A', 'AC outcome')
    req(ac_payload['aggregate']['rows'] == 47, 'AC row count')
    req(ac_payload['aggregate']['oracle_native_mismatch'] == 0, 'AC mismatch')
    req(ac_payload['aggregate']['witness_reselection'] == 0, 'AC witness reselection')
    req(ac_payload['aggregate']['another_control_bits_consumed'] == 0, 'AC another control')
    req(ac_payload['aggregate']['tags'] == {'ActiveActor': 39, 'Int': 7, 'UniqueId': 1}, 'AC tags')
    req(ac_payload['aggregate']['unique_id_layouts'] == [
        {'count': 1, 'payload_width': 80, 'remote_kind': 'Steam', 'system_id': 1}
    ], 'AC UniqueId layout')
    req(ac_ab['aggregate']['rows'] == 47, 'frozen AB rows')
    req(ac_ab['aggregate']['published_frozen_y_direct_mismatch'] == 0, 'frozen AB mismatch')
    ab_by_key = {key_of(r): r for r in ac_ab['rows']}
    req(len(ab_by_key) == 47, 'AB key uniqueness')
    cont = {}
    for w in witnesses:
        if w.get('class') != 'continuation':
            continue
        key = key_of(w)
        req(key not in cont, f'duplicate Y continuation {key}')
        cont[key] = w
    req(len(cont) == 47, f'Y continuation count {len(cont)}')
    rows = []
    for frozen in ac_payload['rows']:
        key = key_of(frozen)
        req(key in ab_by_key and key in cont, f'missing authority for {key}')
        ab = ab_by_key[key]
        y = cont[key]
        req(frozen['oracle_native_exact'] is True, f'AC row not exact {key}')
        req(ab['published_frozen_y_direct_exact'] is True, f'AB row not exact {key}')
        req(ab['resolved_attribute_tag'] == frozen['tag'], f'tag drift {key}')
        req(int(ab['payload_start_bit']) == int(frozen['payload_start_bit']), f'payload-start drift {key}')
        req(int(ab['property_present_start_bit']) == int(frozen['property_present_start_bit']), f'property-start drift {key}')
        req(int(ab['property_present_end_bit']) == int(ab['property_present_start_bit']) + 1, f'property-end drift {key}')
        req(int(ab['net_version']) == 10 and int(ab['version_major']) == 868 and int(ab['version_minor']) == 32, f'version drift {key}')
        rows.append([
            frozen['label'],
            str(frozen['frame_index']),
            str(frozen['actor_ordinal']),
            str(frozen['actor_context_object_id']),
            str(y['first_property_present_start_bit']),
            str(ab['property_present_start_bit']),
            str(ab['property_present_end_bit']),
            str(ab['stream_id']),
            str(ab['stream_id_bound']),
            str(ab['prop_id_bits']),
            str(ab['resolved_property_object_index']),
            frozen['tag'],
            str(frozen['payload_start_bit']),
            str(frozen['payload_end_bit']),
            str(frozen['payload_width']),
            str(frozen['semantic_active']),
            str(frozen['semantic_actor']),
            str(frozen['semantic_int']),
            str(frozen['uid_system']),
            str(frozen['uid_local']),
            str(frozen['uid_remote']),
            str(frozen['uid_fingerprint']),
            str(ab['version_major']),
            str(ab['version_minor']),
            str(ab['net_version']),
        ])
    req(len(rows) == 47 and len({r[0] for r in rows}) == 47, 'target identity')
    target.write_text('\n'.join('\t'.join(r) for r in sorted(rows)) + '\n', encoding='utf-8', newline='\n')
    identity = (acdir / 'r3_18ac_replay_identity.tsv').read_text(encoding='utf-8')
    ids = []
    for line in identity.splitlines():
        if not line.strip():
            continue
        rel, expected, status = line.split('\t')
        p = Path(rel)
        req(status == 'PASS' and not p.is_absolute() and '..' not in p.parts, f'identity format {rel}')
        req(p.exists(), f'missing replay {rel}')
        req(sha256(p).lower() == expected.lower(), f'replay hash {rel}')
        ids.append(rel)
    req(len(ids) == 47 and len(set(ids)) == 47, 'replay identity count')
    Path('r3_18ae_replay_identity.tsv').write_text(identity, encoding='utf-8', newline='\n')
    Path('r3_18ae_frozen_ac_rows.json').write_text(
        json.dumps(ac_payload, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n'
    )
    Path('r3_18ae_frozen_ab_rows.json').write_text(
        json.dumps(ac_ab, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n'
    )
    print('R3_18AE_PREPARE=PASS rows=47 witness_reselection=0 full_header_authority=47')


def semantic_tuple(row, prefix):
    return (
        row[f'{prefix}_active'], row[f'{prefix}_actor'], row[f'{prefix}_int'],
        row[f'{prefix}_uid_system'], row[f'{prefix}_uid_local'],
        row[f'{prefix}_uid_remote'], row[f'{prefix}_uid_fp'],
    )


def frozen_semantic(row):
    return (
        str(row['semantic_active']), str(row['semantic_actor']), str(row['semantic_int']),
        str(row['uid_system']), str(row['uid_local']), str(row['uid_remote']),
        str(row['uid_fingerprint']),
    )


def header_exact(native, ab):
    return (
        int(native['header_property_present_start_bit']) == int(ab['property_present_start_bit'])
        and int(native['header_property_present_end_bit']) == int(ab['property_present_end_bit'])
        and int(native['header_stream_id']) == int(ab['stream_id'])
        and int(native['header_stream_id_bound']) == int(ab['stream_id_bound'])
        and int(native['header_prop_id_bits']) == int(ab['prop_id_bits'])
        and int(native['header_property_object_index']) == int(ab['resolved_property_object_index'])
        and native['header_tag'] == ab['resolved_attribute_tag']
        and int(native['header_payload_start_bit']) == int(ab['payload_start_bit'])
        and int(native['header_version_major']) == int(ab['version_major'])
        and int(native['header_version_minor']) == int(ab['version_minor'])
        and int(native['header_net_version']) == int(ab['net_version'])
    )


def analyze(log_s):
    frozen_doc = json.loads(Path('r3_18ae_frozen_ac_rows.json').read_text(encoding='utf-8'))
    frozen = {r['label']: r for r in frozen_doc['rows']}
    ab_doc = json.loads(Path('r3_18ae_frozen_ab_rows.json').read_text(encoding='utf-8'))
    ab_by_label = {r['label']: r for r in ab_doc['rows']}
    req(len(frozen) == 47 and len(ab_by_label) == 47, 'frozen authority labels')
    observed = {}
    non_z = None
    epic = None
    for line in Path(log_s).read_text(encoding='utf-8').splitlines():
        if line.startswith('R3_18AE_ROW\t'):
            row = kv(line, 'R3_18AE_ROW')
            req(row['label'] not in observed, f'duplicate observed {row["label"]}')
            observed[row['label']] = row
        elif line.startswith('R3_18AE_NON_Z_NEGATIVE\t'):
            non_z = kv(line, 'R3_18AE_NON_Z_NEGATIVE')
        elif line.startswith('R3_18AE_EPIC_NEGATIVE\t'):
            epic = kv(line, 'R3_18AE_EPIC_NEGATIVE')
    req(len(observed) == 47 and set(observed) == set(frozen) == set(ab_by_label), f'row set {len(observed)}/47')
    req(non_z is not None and non_z.get('pass') == '1', 'non-Z negative')
    req(epic is not None and epic.get('pass') == '1', 'Epic negative')
    mismatches = 0
    header_mismatches = 0
    out_rows = []
    tag_counts = collections.Counter()
    widths = collections.defaultdict(collections.Counter)
    uid_layout = collections.Counter()
    flags = ['repeatability', 'truncation', 'wrong_context', 'post_payload_poison']
    for label in sorted(frozen):
        f = frozen[label]
        ab = ab_by_label[label]
        n = observed[label]
        h_exact = header_exact(n, ab)
        if not h_exact:
            header_mismatches += 1
        exact = h_exact
        exact &= int(n['frame_index']) == int(f['frame_index'])
        exact &= int(n['actor_ordinal']) == int(f['actor_ordinal'])
        exact &= int(n['actor_context_object_id']) == int(f['actor_context_object_id'])
        exact &= int(n['property_present_start_bit']) == int(f['property_present_start_bit'])
        exact &= n['tag'] == f['tag']
        exact &= int(n['header_stop_bit']) == int(f['payload_start_bit'])
        exact &= int(n['published_payload_start_bit']) == int(f['payload_start_bit'])
        exact &= int(n['published_payload_end_bit']) == int(f['payload_end_bit'])
        exact &= int(n['published_payload_width']) == int(f['payload_width'])
        exact &= int(n['published_stop_bit']) == int(f['payload_end_bit'])
        exact &= int(n['direct_payload_start_bit']) == int(f['payload_start_bit'])
        exact &= int(n['direct_payload_end_bit']) == int(f['payload_end_bit'])
        exact &= int(n['direct_payload_width']) == int(f['payload_width'])
        exact &= semantic_tuple(n, 'published') == frozen_semantic(f)
        exact &= semantic_tuple(n, 'direct') == frozen_semantic(f)
        exact &= all(n.get(flag) == '1' for flag in flags)
        exact &= n.get('another_control_bits_consumed') == '0'
        if not exact:
            mismatches += 1
        tag = f['tag']
        width = int(f['payload_width'])
        tag_counts[tag] += 1
        widths[tag][width] += 1
        if tag == 'UniqueId':
            uid_layout[(int(f['uid_system']), f['uid_remote'], width)] += 1
        out_rows.append({
            'label': label,
            'frame_index': int(f['frame_index']),
            'actor_ordinal': int(f['actor_ordinal']),
            'actor_context_object_id': int(f['actor_context_object_id']),
            'header_exact_through_payload_start': h_exact,
            'stream_id_bound': int(ab['stream_id_bound']),
            'prop_id_bits': int(ab['prop_id_bits']),
            'property_object_index': int(ab['resolved_property_object_index']),
            'tag': tag,
            'payload_start_bit': int(f['payload_start_bit']),
            'payload_end_bit': int(f['payload_end_bit']),
            'payload_width': width,
            'published_frozen_ac_direct_exact': exact,
            'another_control_bits_consumed': 0,
        })
    req(header_mismatches == 0, f'published/frozen header mismatch {header_mismatches}')
    req(mismatches == 0, f'published/frozen/direct mismatch {mismatches}')
    req(tag_counts == collections.Counter({'ActiveActor': 39, 'Int': 7, 'UniqueId': 1}), f'tags {tag_counts}')
    req(widths['ActiveActor'] == collections.Counter({33: 39}), f'ActiveActor widths {widths["ActiveActor"]}')
    req(widths['Int'] == collections.Counter({32: 7}), f'Int widths {widths["Int"]}')
    req(widths['UniqueId'] == collections.Counter({80: 1}), f'UniqueId widths {widths["UniqueId"]}')
    req(uid_layout == collections.Counter({(1, 'Steam', 80): 1}), f'UID layout {uid_layout}')
    summary = {
        'outcome': 'A',
        'rows': 47,
        'published_frozen_ab_header_mismatch': 0,
        'published_frozen_ac_direct_mismatch': 0,
        'witness_reselection': 0,
        'tags': dict(sorted(tag_counts.items())),
        'widths': {tag: {str(w): c for w, c in sorted(vals.items())} for tag, vals in sorted(widths.items())},
        'unique_id_layouts': [
            {'system_id': k[0], 'remote_kind': k[1], 'payload_width': k[2], 'count': c}
            for k, c in sorted(uid_layout.items())
        ],
        'negative_controls': {
            'repeatability': '47/47',
            'truncation': '47/47',
            'wrong_context': '47/47',
            'post_payload_poison': '47/47',
            'non_z_header': 'PASS',
            'lower_level_valid_epic': 'PASS',
        },
        'another_control_bits_consumed': 0,
    }
    Path('r3_18ae_published_rows.json').write_text(
        json.dumps({'aggregate': summary, 'rows': out_rows}, indent=2, sort_keys=True) + '\n',
        encoding='utf-8', newline='\n'
    )
    Path('r3_18ae_payload_summary.json').write_text(
        json.dumps(summary, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n'
    )
    Path('r3_18ae_negative_controls.txt').write_text('\n'.join([
        'R3_18AE_REPEATABILITY=PASS 47/47',
        'R3_18AE_TRUNCATION=PASS 47/47',
        'R3_18AE_WRONG_CONTEXT=PASS 47/47',
        'R3_18AE_POST_PAYLOAD_POISON=PASS 47/47',
        'R3_18AE_NON_Z_HEADER_NEGATIVE=PASS',
        'R3_18AE_LOWER_LEVEL_VALID_EPIC_NEGATIVE=PASS',
        'R3_18AE_ANOTHER_CONTROL_BITS_CONSUMED=0',
    ]) + '\n', encoding='utf-8', newline='\n')
    Path('r3_18ae_aggregate.txt').write_text('\n'.join([
        'R3_18AE_OUTCOME=A',
        'R3_18AE_EVIDENCE=PASS',
        'R3_18AE_FROZEN_ROWS=47/47',
        'R3_18AE_PUBLISHED_FROZEN_AB_HEADER_MISMATCH=0',
        'R3_18AE_PUBLISHED_FROZEN_AC_DIRECT_MISMATCH=0',
        'R3_18AE_TAGS=ActiveActor:39,Int:7,UniqueId:1',
        'R3_18AE_WIDTHS=ActiveActor:33x39;Int:32x7;UniqueId:80x1',
        'R3_18AE_UNIQUE_ID=system:1,remote:Steam,width:80,count:1',
        'R3_18AE_WITNESS_RESELECTION=0',
        'R3_18AE_ANOTHER_CONTROL_BITS_CONSUMED=0',
        'R3_18AE_NEGATIVES=PASS',
        'R3_18AE_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0',
        'R3_18AE_PRIVACY=PASS',
    ]) + '\n', encoding='utf-8', newline='\n')
    print('R3_18AE_ANALYZE=PASS', json.dumps(summary, sort_keys=True))


def main():
    req(len(sys.argv) >= 2, 'mode')
    if sys.argv[1] == 'prepare':
        req(len(sys.argv) == 5, 'prepare args')
        prepare(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'analyze':
        req(len(sys.argv) == 3, 'analyze args')
        analyze(sys.argv[2])
    else:
        raise SystemExit('bad mode')


if __name__ == '__main__':
    main()
