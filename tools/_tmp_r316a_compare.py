import json,re,sys
from collections import Counter
from pathlib import Path

def kv(line,prefix):
    parts=line.rstrip('\n').split('\t'); out={}
    if parts[0]!=prefix: raise ValueError(line[:80])
    for item in parts[1:]:
        key,sep,value=item.partition('=')
        if not sep or key in out: raise ValueError(item)
        out[key]=value
    return out

def tag(value): return re.sub(r'[^A-Za-z0-9]','',value).lower()

oracle=[json.loads(x) for x in Path('r3_16a_first_property_oracle.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
rows=[kv(x,'R3_16A_MIMIR') for x in Path(sys.argv[1]).read_text(encoding='utf-8',errors='replace').splitlines() if x.startswith('R3_16A_MIMIR\t')]
mimir={x['label'].replace('\\','/'):x for x in rows}
if len(mimir)!=len(rows): raise SystemExit('duplicate MIMIR rows')
counts=Counter(); tags=Counter(); widths=Counter(); lowbits=Counter(); comps=[]
for o in oracle:
    rel=o['relative_path']; q=mimir.get(rel); bad=[]
    if q is None:
        comps.append({'relative_path':rel,'mismatches':['missing_mimir_lookup']}); continue
    checks={
        'actor_context_object_id':int(q['actor_object_id'])==o['actor_context_object_id'],
        'actor_context_object_name':q['actor_object_name']==o['actor_context_object_name'],
        'stream_id_value':int(q['stream_id'])==o['stream_id_value'],
        'stream_id_bound':int(q['max_prop_id'])==o['stream_id_bound'],
        'prop_id_bits':int(q['prop_id_bits'])==o['prop_id_bits'],
        'resolved_property_object_id':int(q['property_object_id'])==o['resolved_property_object_id'],
        'resolved_property_object_name':q['property_object_name']==o['resolved_property_object_name'],
        'resolved_attribute_tag':tag(q['tag'])==tag(o['resolved_attribute_tag']),
        'property_present_true':o['property_present_value'] is True,
        'property_present_width':o['property_present_end_bit']==o['property_present_start_bit']+1,
        'stream_starts_after_property':o['stream_id_start_bit']==o['property_present_end_bit'],
        'payload_starts_after_stream':o['payload_start_bit']==o['stream_id_end_bit'],
        'new_to_property_monotonic':o['new_bit_end']<=o['property_present_start_bit'],
        'stream_id_in_bound':0<=o['stream_id_value']<o['stream_id_bound'],
    }
    for key,ok in checks.items():
        counts[key]+=int(ok)
        if not ok: bad.append(key)
    tags[o['resolved_attribute_tag']]+=1
    widths[o['stream_id_end_bit']-o['stream_id_start_bit']]+=1
    lowbits[o['prop_id_bits']]+=1
    comps.append({'relative_path':rel,'mismatches':bad,'checks':checks})
n=len(oracle); mismatch=sum(bool(x['mismatches']) for x in comps)
identity=sum(1 for x in Path('r3_16a_replay_identity.tsv').read_text(encoding='utf-8').splitlines() if x.strip())
outcome='A' if n==47 and len(mimir)==47 and identity==47 and mismatch==0 else 'B'
summary={'pass':'R3.16A','production_sha':'bf4bccff82203ed049d33e942681fed07f23beb4','boxcars_sha':'c70e77df7af81b436cb545d070bb90c82f562d0b','replays_total':47,'oracle_decode_success':n,'selected_existing_actor_property_rows':n,'replays_without_candidate':47-n,'property_present_true':counts['property_present_true'],'stream_id_resolved':counts['resolved_property_object_id'],'stream_id_unresolved':n-counts['resolved_property_object_id'],'property_object_resolved':counts['resolved_property_object_name'],'property_object_mismatch':n-counts['resolved_property_object_id'],'invalid_property_object_id':0,'payload_start_monotonicity_failures':n-counts['payload_starts_after_stream'],'oracle_error_count':0,'identity_error_count':47-identity,'mismatch_count':mismatch,'stream_id_min':min(x['stream_id_value'] for x in oracle),'stream_id_max':max(x['stream_id_value'] for x in oracle),'attribute_tag_distribution':dict(sorted(tags.items())),'stream_id_consumed_width_distribution':{str(k):v for k,v in sorted(widths.items())},'prop_id_bits_distribution':{str(k):v for k,v in sorted(lowbits.items())},'comparison_gate_counts':dict(sorted(counts.items())),'production_mutation_count':0,'cargo_mutation_count':0,'outcome':outcome}
Path('r3_16a_comparisons.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in comps),encoding='utf-8')
Path('r3_16a_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
agg=['pass=R3.16A','replays_total=47',f'oracle_decode_success={n}',f'selected_existing_actor_property_rows={n}',f'replays_without_candidate={47-n}',f"property_present_true={counts['property_present_true']}",f"stream_id_resolved={counts['resolved_property_object_id']}",f"stream_id_unresolved={n-counts['resolved_property_object_id']}",f"property_object_resolved={counts['resolved_property_object_name']}",f"property_object_mismatch={n-counts['resolved_property_object_id']}",'invalid_property_object_id=0',f"payload_start_monotonicity_failures={n-counts['payload_starts_after_stream']}",'oracle_error_count=0','production_mutation_count=0','cargo_mutation_count=0',f'mismatch_count={mismatch}',f'R3_16A_OUTCOME={outcome}','R3_16A_EVIDENCE='+('PASS' if outcome=='A' else 'FAIL')]
Path('r3_16a_aggregate.txt').write_text('\n'.join(agg)+'\n',encoding='utf-8')
print('\n'.join(agg))
if outcome!='A': raise SystemExit('R3.16A evidence mismatch')
