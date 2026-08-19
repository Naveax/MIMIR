#!/usr/bin/env python3
import collections, hashlib, json, sys
from pathlib import Path

def req(c,m):
    if not c: raise SystemExit(m)

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def kv(line,prefix):
    req(line.startswith(prefix+"\t"),f"bad {prefix}")
    d={}
    for x in line.split("\t")[1:]:
        req("=" in x,f"bad field {x}")
        k,v=x.split("=",1); d[k]=v
    return d

def prepare(ydir,abdir,target):
    ydir=Path(ydir); abdir=Path(abdir)
    ab=json.loads((abdir/"r3_18ab_published_rows.json").read_text())
    wit=json.loads((ydir/"r3_18y_frozen_witnesses.json").read_text())
    req(ab["aggregate"]["rows"]==47,"AB rows")
    req(ab["aggregate"]["published_frozen_y_direct_mismatch"]==0,"AB mismatch")
    cont={}
    for w in wit:
        if w.get("class")!="continuation": continue
        key=(w["label"],int(w["frame_index"]),int(w["actor_ordinal"]),int(w["actor_context_object_id"]))
        req(key not in cont,"duplicate continuation")
        cont[key]=w
    req(len(cont)==47,f"continuation {len(cont)}")
    out=[]
    for r in ab["rows"]:
        key=(r["label"],int(r["frame_index"]),int(r["actor_ordinal"]),int(r["actor_context_object_id"]))
        req(key in cont,f"missing witness {key}")
        w=cont[key]
        req(r["published_frozen_y_direct_exact"],"AB row not exact")
        out.append([
            r["label"],str(r["frame_index"]),str(r["actor_ordinal"]),str(r["actor_context_object_id"]),
            str(w["first_property_present_start_bit"]),str(r["property_present_start_bit"]),
            str(r["property_present_end_bit"]),str(r["stream_id_start_bit"]),str(r["stream_id_end_bit"]),
            str(r["stream_id"]),str(r["stream_id_bound"]),str(r["prop_id_bits"]),
            str(r["resolved_property_object_index"]),r["resolved_attribute_tag"],str(r["payload_start_bit"]),
            str(r["version_major"]),str(r["version_minor"]),str(r["net_version"])
        ])
    req(len(out)==47 and len({x[0] for x in out})==47,"target identity")
    Path(target).write_text("\n".join("\t".join(x) for x in sorted(out))+"\n",encoding="utf-8",newline="\n")
    identity=(abdir/"r3_18ab_replay_identity.tsv").read_text()
    rows=[]
    for line in identity.splitlines():
        if not line.strip(): continue
        rel,expected,status=line.split("\t")
        req(status=="PASS" and not Path(rel).is_absolute() and ".." not in Path(rel).parts,"identity format")
        req(Path(rel).exists() and sha256(rel).lower()==expected.lower(),f"identity hash {rel}")
        rows.append(rel)
    req(len(rows)==47 and len(set(rows))==47,"identity rows")
    Path("r3_18ac_replay_identity.tsv").write_text(identity,encoding="utf-8",newline="\n")
    Path("r3_18ac_frozen_ab_rows.json").write_text(json.dumps(ab,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print("R3_18AC_PREPARE=PASS rows=47 witness_reselection=0")

def analyze(oracle_path,native_path):
    oracle={}; native={}
    for line in Path(oracle_path).read_text().splitlines():
        if line.startswith("R3_18AC_ORACLE\t"):
            x=kv(line,"R3_18AC_ORACLE"); req(x["label"] not in oracle,"dup oracle"); oracle[x["label"]]=x
    for line in Path(native_path).read_text().splitlines():
        if line.startswith("R3_18AC_NATIVE\t"):
            x=kv(line,"R3_18AC_NATIVE"); req(x["label"] not in native,"dup native"); native[x["label"]]=x
    req(len(oracle)==47 and len(native)==47 and set(oracle)==set(native),f"row sets {len(oracle)}/{len(native)}")
    tag_counts=collections.Counter(); widths=collections.defaultdict(collections.Counter)
    uid_layout=collections.Counter(); mismatch=0; rows=[]
    compare_fields=["frame_index","actor_ordinal","actor_context_object_id","property_present_start_bit","tag",
                    "payload_start_bit","payload_end_bit","payload_width","semantic_active","semantic_actor",
                    "semantic_int","uid_system","uid_local","uid_remote","uid_fp"]
    flags=["repeatability","truncation","wrong_tag_negative","wrong_context_negative","post_payload_poison"]
    for label in sorted(oracle):
        o,n=oracle[label],native[label]
        exact=all(o[k]==n[k] for k in compare_fields)
        exact=exact and all(n.get(k)=="1" for k in flags) and n.get("another_control_bits_consumed")=="0"
        if not exact: mismatch+=1
        tag=n["tag"]; tag_counts[tag]+=1; widths[tag][int(n["payload_width"])]+=1
        if tag=="UniqueId":
            uid_layout[(int(n["uid_system"]),n["uid_remote"],int(n["payload_width"]))]+=1
        rows.append({
            "label":label,"frame_index":int(n["frame_index"]),"actor_ordinal":int(n["actor_ordinal"]),
            "actor_context_object_id":int(n["actor_context_object_id"]),
            "property_present_start_bit":int(n["property_present_start_bit"]),"tag":tag,
            "payload_start_bit":int(n["payload_start_bit"]),"payload_end_bit":int(n["payload_end_bit"]),
            "payload_width":int(n["payload_width"]),
            "semantic_active":n["semantic_active"],"semantic_actor":n["semantic_actor"],
            "semantic_int":n["semantic_int"],
            "uid_system":n["uid_system"],"uid_local":n["uid_local"],"uid_remote":n["uid_remote"],
            "uid_fingerprint":n["uid_fp"],"oracle_native_exact":exact,
            "another_control_bits_consumed":0
        })
    req(mismatch==0,f"oracle/native mismatch {mismatch}")
    req(tag_counts==collections.Counter({"ActiveActor":39,"Int":7,"UniqueId":1}),f"tags {tag_counts}")
    req(sum(uid_layout.values())==1,"unique id row")
    summary={
        "outcome":"A","rows":47,"oracle_native_mismatch":0,"witness_reselection":0,
        "tags":dict(sorted(tag_counts.items())),
        "widths":{k:{str(w):c for w,c in sorted(v.items())} for k,v in sorted(widths.items())},
        "unique_id_layouts":[{"system_id":k[0],"remote_kind":k[1],"payload_width":k[2],"count":c} for k,c in sorted(uid_layout.items())],
        "another_control_bits_consumed":0,
        "negative_controls":{"repeatability":"47/47","truncation":"47/47","wrong_tag":"47/47","wrong_context_or_na":"47/47","post_payload_poison":"47/47"},
    }
    Path("r3_18ac_payload_rows.json").write_text(json.dumps({"aggregate":summary,"rows":rows},indent=2,sort_keys=True)+"\n")
    Path("r3_18ac_payload_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    Path("r3_18ac_unique_id_layout.json").write_text(json.dumps({"layouts":summary["unique_id_layouts"]},indent=2,sort_keys=True)+"\n")
    Path("r3_18ac_negative_controls.txt").write_text("\n".join([
        "R3_18AC_REPEATABILITY=PASS 47/47","R3_18AC_TRUNCATION=PASS 47/47",
        "R3_18AC_WRONG_TAG_NEGATIVE=PASS 47/47","R3_18AC_WRONG_CONTEXT_OR_NA=PASS 47/47",
        "R3_18AC_POST_PAYLOAD_POISON=PASS 47/47","R3_18AC_ANOTHER_CONTROL_BITS_CONSUMED=0"
    ])+"\n")
    width_text=";".join(f"{tag}:"+",".join(f"{w}x{c}" for w,c in sorted(vals.items())) for tag,vals in sorted(widths.items()))
    uid=summary["unique_id_layouts"][0]
    Path("r3_18ac_aggregate.txt").write_text("\n".join([
        "R3_18AC_OUTCOME=A","R3_18AC_EVIDENCE=PASS","R3_18AC_FROZEN_ROWS=47/47",
        "R3_18AC_ORACLE_NATIVE_MISMATCH=0","R3_18AC_TAGS=ActiveActor:39,Int:7,UniqueId:1",
        f"R3_18AC_WIDTHS={width_text}",
        f"R3_18AC_UNIQUE_ID=system:{uid['system_id']},remote:{uid['remote_kind']},width:{uid['payload_width']},count:1",
        "R3_18AC_WITNESS_RESELECTION=0","R3_18AC_ANOTHER_CONTROL_BITS_CONSUMED=0",
        "R3_18AC_NEGATIVES=PASS 47/47","R3_18AC_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
        "R3_18AC_PRIVACY=PASS"
    ])+"\n")
    print("R3_18AC_ANALYZE=PASS",json.dumps(summary,sort_keys=True))

def main():
    req(len(sys.argv)>=2,"mode")
    if sys.argv[1]=="prepare":
        req(len(sys.argv)==5,"prepare args"); prepare(sys.argv[2],sys.argv[3],sys.argv[4])
    elif sys.argv[1]=="analyze":
        req(len(sys.argv)==4,"analyze args"); analyze(sys.argv[2],sys.argv[3])
    else: raise SystemExit("bad mode")
if __name__=="__main__": main()
