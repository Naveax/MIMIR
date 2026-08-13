import csv,hashlib,json
from collections import Counter
from pathlib import Path
R=Path.cwd()
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for c in iter(lambda:f.read(1<<20),b""): h.update(c)
 return h.hexdigest()
def B(x):
 if x=="true": return True
 if x=="false": return False
 raise ValueError(x)
def I(x): return None if x=="null" else int(x)
paths=[x.strip() for x in (R/"r315a_oracle/r3_15a_paths.txt").read_text().splitlines() if x.strip()]
oracle={}
for line in (R/"r3_15d_oracle_first.jsonl").read_text().splitlines():
 o=json.loads(line); oracle[o["relative_path"]]=o
native={}
with open(R/"r3_15d_native.tsv",newline="") as f:
 for n in csv.DictReader(f,delimiter="\t"):
  p=n["relative_path"]; assert p not in native
  for k in ["actor_present","alive","is_new","opaque_post_name_bit","location_present","rotation_present","yaw_present","pitch_present","roll_present"]: n[k]=B(n[k])
  for k in ["actor_id","location_x","location_y","location_z","yaw","pitch","roll"]: n[k]=I(n[k])
  for k in ["envelope_stop_bit","name_id","object_id","new_actor_stop_bit"]: n[k]=int(n[k])
  native[p]=n
assert set(paths)==set(oracle)==set(native) and len(paths)==47
sm={"none":"none","location":"location","location_rotation":"location_and_rotation"}
keys=["identity","actor_present","actor_id","alive","is_new","envelope_stop","name_id","opaque_bit","object_id","spawn_kind","location_presence","location_x","location_y","location_z","rotation_presence","yaw_presence","yaw","pitch_presence","pitch","roll_presence","roll","trajectory_stop"]
cnt=Counter(); rows=[]; badrows=0
for p in paths:
 o=oracle[p]; n=native[p]
 ck={
 "identity":sha(R/p)==o["sha256"],
 "actor_present":n["actor_present"] is True,
 "actor_id":n["actor_id"]==o["actor_id"],
 "alive":n["alive"] is True,
 "is_new":n["is_new"] is True,
 "envelope_stop":n["envelope_stop_bit"]==o["branch_start_bit"],
 "name_id":n["name_id"]==o["name_id_value"],
 "opaque_bit":n["opaque_post_name_bit"]==o["opaque_bit_value"],
 "object_id":n["object_id"]==o["object_id_value"],
 "spawn_kind":n["spawn_kind"]==sm[o["oracle_spawn_kind"]],
 "location_presence":n["location_present"]==(o["location_start_bit"] is not None),
 "location_x":n["location_x"]==o["location_x_i32"],
 "location_y":n["location_y"]==o["location_y_i32"],
 "location_z":n["location_z"]==o["location_z_i32"],
 "rotation_presence":n["rotation_present"]==(o["rotation_start_bit"] is not None),
 "yaw_presence":n["yaw_present"]==o["yaw_present"],
 "yaw":n["yaw"]==o["yaw_i8"],
 "pitch_presence":n["pitch_present"]==o["pitch_present"],
 "pitch":n["pitch"]==o["pitch_i8"],
 "roll_presence":n["roll_present"]==o["roll_present"],
 "roll":n["roll"]==o["roll_i8"],
 "trajectory_stop":n["new_actor_stop_bit"]==o["trajectory_end_bit"]}
 for k,v in ck.items(): cnt[k]+=int(v)
 bad=[k for k,v in ck.items() if not v]; badrows+=bool(bad)
 rows.append({"relative_path":p,"sha256":sha(R/p),"oracle_spawn_kind":o["oracle_spawn_kind"],"native_spawn_kind":n["spawn_kind"],"oracle_branch_start_bit":o["branch_start_bit"],"native_envelope_stop_bit":n["envelope_stop_bit"],"oracle_trajectory_end_bit":o["trajectory_end_bit"],"native_new_actor_stop_bit":n["new_actor_stop_bit"],"mismatches":bad})
ok=badrows==0 and all(cnt[k]==47 for k in keys)
summary={"production_sha":"bf4bccff82203ed049d33e942681fed07f23beb4","production_source_blob":"f64a5e0d66962f41026b2eb10e176219d4529931","oracle_artifact_id":9184200143,"oracle_artifact_sha256":"a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d","oracle_full_stream_sha256":"ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba","replays_total":47,"oracle_rows_selected":47,"native_success":47,"identity_error_count":47-cnt["identity"],"native_error_count":0,"mismatch_count":badrows,"field_match_counts":dict(cnt),"outcome":"A" if ok else "B"}
Path("r3_15d_comparisons.jsonl").write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in rows))
Path("r3_15d_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
lines=["replays_total=47","oracle_rows_selected=47","native_success=47",f"identity_error_count={summary['identity_error_count']}",f"mismatch_count={badrows}"]+[f"{k}_match={cnt[k]}/47" for k in keys]+[f"R3_15D_OUTCOME={summary['outcome']}","R3_15D_DIFFERENTIAL="+("PASS" if ok else "FAIL")]
Path("r3_15d_aggregate.txt").write_text("\n".join(lines)+"\n"); print("\n".join(lines))
if not ok: raise SystemExit("R3.15D differential mismatch")
