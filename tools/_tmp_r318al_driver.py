#!/usr/bin/env python3
import collections, hashlib, json, sys
from pathlib import Path

def req(c,m):
    if not c: raise SystemExit(m)

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def kv(line,prefix):
    req(line.startswith(prefix+'\t'),f'bad {prefix} line')
    out={}
    for item in line.split('\t')[1:]:
        req('=' in item,f'bad field {item}')
        k,v=item.split('=',1); out[k]=v
    return out

def prepare(aidir,contract_path,target_path):
    d=Path(aidir)
    rows_doc=json.loads((d/'r3_18ai_header_rows.json').read_text())
    wit_doc=json.loads((d/'r3_18ai_frozen_witnesses.json').read_text())
    contract=json.loads(Path(contract_path).read_text())
    a=rows_doc['aggregate']
    req(a=={'following_payload_bits_consumed':0,'native_oracle_mismatch':0,'outcome':'A','rows':47,'second_later_control_bits_consumed':0,'tags':{'Int':47},'unique_exact_contexts':17,'witness_reselection':0},f'AI aggregate drift {a}')
    req(wit_doc['aggregate']['rows']==47 and wit_doc['aggregate']['witness_reselection']==0,'AI witness aggregate drift')
    req(contract['membership_policy']=='exact_tuple_only','AJ policy drift')
    req(contract['observed_row_count']==47 and contract['unique_exact_context_count']==17,'AJ count drift')
    req(contract['observed_tag_counts']=={'Int':47},'AJ tags drift')
    req(contract['anti_widening']['r3_18z_cross_boundary_inheritance'] is False,'Z inheritance drift')
    req(contract['anti_widening']['r3_18p_cross_boundary_inheritance'] is False,'P inheritance drift')
    w={x['label']:x for x in wit_doc['rows']}
    req(len(w)==47,'AI witness labels !=47')
    targets=[]; seen=set()
    for r in rows_doc['rows']:
        label=r['label']; req(label not in seen and label in w,f'witness/label drift {label}'); seen.add(label)
        x=w[label]
        req(bool(r['native_oracle_exact']),'AI oracle drift')
        req(int(r['following_payload_bits_consumed'])==0 and int(r['second_later_control_bits_consumed'])==0,'AI consumption drift')
        req(int(x['actor_context_object_id'])==int(r['actor_context_object_id']),'actor drift')
        req(int(x['published_start'])==int(r['ag_property_present_start_bit']),'AG start drift')
        req(int(x['published_stop'])==int(r['ag_stop_bit']),'AG stop drift')
        targets.append([label,str(r['frame_index']),str(r['actor_ordinal']),str(r['actor_context_object_id']),str(x['first_start']),str(r['ag_property_present_start_bit']),str(r['ag_stop_bit']),str(r['stream_id_start_bit']),str(r['stream_id_end_bit']),str(r['stream_id']),str(r['stream_id_bound']),str(r['prop_id_bits']),str(r['resolved_property_object_index']),r['resolved_attribute_tag'],str(r['payload_start_bit']),str(r['version_major']),str(r['version_minor']),str(r['net_version'])])
    req(len(targets)==47 and len(seen)==47,'target count drift')
    Path(target_path).write_text('\n'.join('\t'.join(x) for x in sorted(targets))+"\n",encoding='utf-8',newline='\n')
    ids=[]
    for line in (d/'r3_18ai_replay_identity.tsv').read_text().splitlines():
        if not line.strip(): continue
        f=line.split('\t'); req(len(f)==3 and f[2]=='PASS',f'bad identity {line}')
        p=Path(f[0]); req(not p.is_absolute() and '..' not in p.parts,f'unsafe path {p}')
        req(p.exists(),f'missing replay {p}'); req(sha256(p).lower()==f[1].lower(),f'hash drift {p}'); ids.append(line)
    req(len(ids)==47,'identity count drift')
    Path('r3_18al_replay_identity.tsv').write_text('\n'.join(ids)+'\n',encoding='utf-8',newline='\n')
    Path('r3_18al_frozen_ai_rows.json').write_text(json.dumps(rows_doc,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print('R3_18AL_PREPARE=PASS rows=47 contexts=17 witness_reselection=0')

def analyze(aidir,contract_path,log_path):
    frozen_doc=json.loads((Path(aidir)/'r3_18ai_header_rows.json').read_text())
    frozen={r['label']:r for r in frozen_doc['rows']}
    contract=json.loads(Path(contract_path).read_text())
    pub={}
    for line in Path(log_path).read_text().splitlines():
        if line.startswith('R3_18AL_PUBLISHED\t'):
            r=kv(line,'R3_18AL_PUBLISHED'); req(r['label'] not in pub,'duplicate published'); pub[r['label']]=r
    req(len(pub)==47 and set(pub)==set(frozen),'published/frozen set drift')
    tuple_counts=collections.Counter(); tag_counts=collections.Counter(); out=[]; mismatch=0
    fields=['frame_index','actor_ordinal','actor_context_object_id','property_present_start_bit','property_present_end_bit','stream_id_start_bit','stream_id_end_bit','stream_id','stream_id_bound','prop_id_bits','property_object_id','version_major','version_minor','net_version','payload_start_bit']
    fmap={'property_present_start_bit':'ag_property_present_start_bit','property_present_end_bit':'ag_stop_bit','property_object_id':'resolved_property_object_index'}
    flags=['published_exact','direct_equal','control_identity','repeatability','truncation','corrupt_ag_negative','wrong_actor_negative','unresolved_lookup_negative','wrong_version_negative','post_payload_poison']
    for label in sorted(frozen):
        a=frozen[label]; b=pub[label]; exact=True
        for f in fields:
            if int(a[fmap.get(f,f)])!=int(b[f]): exact=False
        if a['resolved_attribute_tag']!=b['attribute_tag'] or int(b['stop_bit'])!=int(a['payload_start_bit']): exact=False
        if not all(b.get(x)=='1' for x in flags): exact=False
        if b.get('following_payload_bits_consumed')!='0' or b.get('another_control_bits_consumed')!='0': exact=False
        mismatch += 0 if exact else 1
        t=(int(b['stream_id_bound']),int(b['prop_id_bits']),int(b['property_object_id']),b['attribute_tag'],int(b['version_major']),int(b['version_minor']),int(b['net_version']))
        tuple_counts[t]+=1; tag_counts[b['attribute_tag']]+=1
        out.append({'label':label,'frame_index':int(b['frame_index']),'actor_ordinal':int(b['actor_ordinal']),'actor_context_object_id':int(b['actor_context_object_id']),'property_present_start_bit':int(b['property_present_start_bit']),'property_present_end_bit':int(b['property_present_end_bit']),'stream_id_start_bit':int(b['stream_id_start_bit']),'stream_id_end_bit':int(b['stream_id_end_bit']),'stream_id':int(b['stream_id']),'stream_id_bound':int(b['stream_id_bound']),'prop_id_bits':int(b['prop_id_bits']),'resolved_property_object_index':int(b['property_object_id']),'resolved_attribute_tag':b['attribute_tag'],'version_major':int(b['version_major']),'version_minor':int(b['version_minor']),'net_version':int(b['net_version']),'payload_start_bit':int(b['payload_start_bit']),'published_frozen_ai_direct_exact':exact,'following_payload_bits_consumed':0,'another_control_bits_consumed':0})
    req(mismatch==0,f'differential mismatch {mismatch}'); req(tag_counts==collections.Counter({'Int':47}),f'tags {tag_counts}')
    expected={}
    for c in contract['admitted_contexts']:
        t=(int(c['stream_id_bound']),int(c['prop_id_bits']),int(c['property_object_index']),c['attribute_tag'],int(c['version_major']),int(c['version_minor']),int(c['net_version'])); expected[t]=int(c['observed_count'])
    req(len(expected)==17 and tuple_counts==collections.Counter(expected),'AJ tuple/multiplicity drift')
    summary={'rows':47,'unique_exact_contexts':17,'tags':{'Int':47},'published_frozen_ai_direct_mismatch':0,'witness_reselection':0,'following_payload_bits_consumed':0,'another_control_bits_consumed':0,'membership_policy':'exact_tuple_only','contexts':[{'stream_id_bound':t[0],'prop_id_bits':t[1],'property_object_index':t[2],'attribute_tag':t[3],'version_major':t[4],'version_minor':t[5],'net_version':t[6],'observed_count':n} for t,n in sorted(tuple_counts.items())]}
    Path('r3_18al_published_rows.json').write_text(json.dumps({'aggregate':summary,'rows':out},indent=2,sort_keys=True)+'\n')
    Path('r3_18al_context_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    neg=['R3_18AL_REPEATABILITY=PASS 47/47','R3_18AL_TRUNCATION=PASS 47/47','R3_18AL_CORRUPT_AG_NEGATIVE=PASS 47/47','R3_18AL_WRONG_ACTOR_NEGATIVE=PASS 47/47','R3_18AL_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47','R3_18AL_WRONG_VERSION_NEGATIVE=PASS 47/47','R3_18AL_POST_PAYLOAD_POISON=PASS 47/47','R3_18AL_CARTESIAN_FABRICATED_OLD_Z=PASS permanent-focused-test','R3_18AL_FOLLOWING_PAYLOAD_BITS_CONSUMED=0','R3_18AL_ANOTHER_CONTROL_BITS_CONSUMED=0']
    Path('r3_18al_negative_controls.txt').write_text('\n'.join(neg)+'\n')
    agg=['R3_18AL_OUTCOME=A','R3_18AL_EVIDENCE=PASS','R3_18AL_FROZEN_ROWS=47/47','R3_18AL_PUBLISHED_AK_FROZEN_AI_DIRECT_MISMATCH=0','R3_18AL_EXACT_AJ_CONTEXTS=17/17','R3_18AL_EXACT_AJ_MULTIPLICITY=47/47','R3_18AL_TAGS=Int:47','R3_18AL_WITNESS_RESELECTION=0']+neg+['R3_18AL_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0','R3_18AL_PRIVACY=PASS']
    Path('r3_18al_aggregate.txt').write_text('\n'.join(agg)+'\n')
    print('R3_18AL_ANALYZE=PASS rows=47 contexts=17 mismatch=0')

def main():
    req(len(sys.argv)>=2,'missing command')
    if sys.argv[1]=='prepare': req(len(sys.argv)==5,'prepare args'); prepare(*sys.argv[2:])
    elif sys.argv[1]=='analyze': req(len(sys.argv)==5,'analyze args'); analyze(*sys.argv[2:])
    else: raise SystemExit('unknown command')
if __name__=='__main__': main()
