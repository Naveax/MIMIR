import hashlib, json
from collections import Counter
from pathlib import Path
R=Path.cwd(); O=R/"r315a_oracle"; S=O/"r3_15a_new_actor_all.jsonl"; P?O/"r3_15a_paths.txt"
def h(p):
    x=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): x.update(c)
    return x.hexdigest()
assert h(S)=="ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba"
paths=[x.strip() for x in P.read_text().splitlines() if x.strip()]
assert len(paths)==len(set(paths))==47
sel={}; total=0
for line in S.read_text().splitlines():
    if not line: continue
    total+=1; row=json.loads(line)
    if row["frame_index"]==0 and row["actor_ordinal"]==0:
        assert row["relative_path"] not in sel
        sel[row["relative_path"]]=row
assert total==169538 and len(sel)==47 and set(sel)==set(paths)
assert all(x["branch_start_bit"]==78 and x["do_parse_name"] for x in sel.values())
assert Counter(x["oracle_spawn_kind"] for x in sel.values())==Counter({"location_rotation":31,"location":11,"none":5})
Path("r3_15d_oracle_first.jsonl").write_text("".join(json.dumps(sel[p],sort_keys=True)+"\n" for p in paths))
print("R3_15D_ORACLE_SELECTION=PASS")
