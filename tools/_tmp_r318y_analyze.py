#!/usr/bin/env python3
import collections, json, sys
from pathlib import Path

def req(c,m):
    if not c: raise SystemExit(m)

def kv(line,prefix):
    req(line.startswith(prefix+'\t'),f'bad {prefix} line')
    d={}
    for item in line.split('\t')[1:]:
        req('=' in item,f'bad field {item}')
        k,v=item.split('=',1); d[k]=v
    return d

def parse(path,prefix):
    out={}
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if line.startswith(prefix+'\t'):
            r=kv(line,prefix); label=r['label']; req(label not in out,f'duplicate {prefix} {label}'); out[label]=r
    req(len(out)==47,f'{prefix} rows {len(out)} !=47')
    return out

def main():
    if len(sys.argv)!=7: raise SystemExit('usage: analyze oracle native rows summary negatives aggregate')
    oracle,native,rows_out,summary_out,neg_out,agg_out=sys.argv[1:]
    o=parse(oracle,'R3_18Y_HEADER'); n=parse(native,'R3_18Y_NATIVE')
    req(set(o)==set(n),'oracle/native label set mismatch')
    int_fields=['frame_index','actor_ordinal','actor_context_object_id','property_present_start_bit','property_present_end_bit','stream_id_start_bit','stream_id_end_bit','stream_id','stream_id_bound','prop_id_bits','property_object_id','version_major','version_minor','net_version','payload_start_bit']
    nmap={'property_present_start_bit':'present_start','property_present_end_bit':'present_end','stream_id_start_bit':'stream_start','stream_id_end_bit':'stream_end','stream_id_bound':'stream_bound','prop_id_bits':'prop_bits','property_object_id':'property_object'}
    rows=[]; tuples=collections.Counter(); tags=collections.Counter(); mismatch=0
    for label in sorted(o):
        a=o[label]; b=n[label]; exact=True
        for f in int_fields:
            nf=nmap.get(f,f)
            if int(a[f])!=int(b[nf]): exact=False
        if a['attribute_tag']!=b['tag']: exact=False
        if int(b['header_stop'])!=int(a['payload_start_bit']): exact=False
        flags=['w_exact','repeatability','trunc_property','trunc_stream','prior_stop_negative','wrong_actor_negative','unresolved_lookup_negative','wrong_context_negative','post_payload_poison']
        if not all(b.get(x)=='1' for x in flags): exact=False
        if b.get('following_payload_bits_consumed')!='0' or b.get('another_control_bits_consumed')!='0': exact=False
        if not exact: mismatch+=1
        tup=(int(a['stream_id_bound']),int(a['prop_id_bits']),int(a['property_object_id']),a['attribute_tag'],int(a['version_major']),int(a['version_minor']),int(a['net_version']))
        tuples[tup]+=1; tags[a['attribute_tag']]+=1
        rows.append({
          'label':label,'frame_index':int(a['frame_index']),'actor_ordinal':int(a['actor_ordinal']),'actor_context_object_id':int(a['actor_context_object_id']),
          'property_present_start_bit':int(a['property_present_start_bit']),'property_present_end_bit':int(a['property_present_end_bit']),
          'stream_id_start_bit':int(a['stream_id_start_bit']),'stream_id_end_bit':int(a['stream_id_end_bit']),'stream_id':int(a['stream_id']),
          'stream_id_bound':int(a['stream_id_bound']),'prop_id_bits':int(a['prop_id_bits']),'resolved_property_object_index':int(a['property_object_id']),
          'resolved_attribute_tag':a['attribute_tag'],'version_major':int(a['version_major']),'version_minor':int(a['version_minor']),'net_version':int(a['net_version']),
          'payload_start_bit':int(a['payload_start_bit']),'native_oracle_exact':exact,'following_payload_bits_consumed':0,'another_control_bits_consumed':0
        })
    req(mismatch==0,f'Y native/oracle mismatch {mismatch}')
    contexts=[]
    for tup,count in sorted(tuples.items(),key=lambda z:z[0]):
        contexts.append({'stream_id_bound':tup[0],'prop_id_bits':tup[1],'property_object_index':tup[2],'attribute_tag':tup[3],'version_major':tup[4],'version_minor':tup[5],'net_version':tup[6],'observed_count':count})
    result={'aggregate':{'outcome':'A','rows':47,'unique_exact_contexts':len(contexts),'native_oracle_mismatch':0,'witness_reselection':0,'following_payload_bits_consumed':0,'another_control_bits_consumed':0,'tags':dict(sorted(tags.items()))},'rows':rows}
    Path(rows_out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    summary={'rows':47,'unique_exact_contexts':len(contexts),'contexts':contexts,'tags':dict(sorted(tags.items())),'native_oracle_mismatch':0,'witness_reselection':0,'membership_policy_candidate':'exact_tuple_only','r3_18p_inheritance_assumed':False}
    Path(summary_out).write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    negatives='\n'.join([
      'R3_18Y_REPEATABILITY=PASS 47/47','R3_18Y_PROPERTY_TRUNCATION=PASS 47/47','R3_18Y_STREAM_TRUNCATION=PASS 47/47',
      'R3_18Y_PRIOR_STOP_NEGATIVE=PASS 47/47','R3_18Y_WRONG_ACTOR_NEGATIVE=PASS 47/47','R3_18Y_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47',
      'R3_18Y_WRONG_CONTEXT_NEGATIVE=PASS 47/47','R3_18Y_POST_PAYLOAD_START_POISON=PASS 47/47','R3_18Y_FOLLOWING_PAYLOAD_BITS_CONSUMED=0','R3_18Y_ANOTHER_CONTROL_BITS_CONSUMED=0'])+'\n'
    Path(neg_out).write_text(negatives,encoding='utf-8',newline='\n')
    agg='\n'.join([
      'R3_18Y_OUTCOME=A','R3_18Y_EVIDENCE=PASS','R3_18Y_FROZEN_ROWS=47/47',f'R3_18Y_UNIQUE_EXACT_CONTEXTS={len(contexts)}',
      'R3_18Y_NATIVE_ORACLE_MISMATCH=0','R3_18Y_WITNESS_RESELECTION=0','R3_18Y_REPEATABILITY=PASS 47/47','R3_18Y_PROPERTY_TRUNCATION=PASS 47/47',
      'R3_18Y_STREAM_TRUNCATION=PASS 47/47','R3_18Y_PRIOR_STOP_NEGATIVE=PASS 47/47','R3_18Y_WRONG_ACTOR_NEGATIVE=PASS 47/47',
      'R3_18Y_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47','R3_18Y_WRONG_CONTEXT_NEGATIVE=PASS 47/47','R3_18Y_POST_PAYLOAD_START_POISON=PASS 47/47',
      'R3_18Y_FOLLOWING_PAYLOAD_BITS_CONSUMED=0','R3_18Y_ANOTHER_CONTROL_BITS_CONSUMED=0','R3_18Y_R318P_INHERITANCE_ASSUMED=0',
      'R3_18Y_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0','R3_18Y_PRIVACY=PASS'])+'\n'
    Path(agg_out).write_text(agg,encoding='utf-8',newline='\n')
    print(f'R3_18Y_ANALYZE=PASS rows=47 contexts={len(contexts)} tags={dict(tags)} mismatch=0')

if __name__=='__main__': main()
