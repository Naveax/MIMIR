import hashlib, sys
from pathlib import Path
EXPECTED=47
def sha256(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''): h.update(c)
 return h.hexdigest()
root=Path(sys.argv[1]); art=Path(sys.argv[2])
paths=[x.strip().replace('\\','/') for x in (art/'r3_15d_paths.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
if len(paths)!=EXPECTED or len(set(paths))!=EXPECTED: raise SystemExit(f'bad selector count: {len(paths)}')
ids={}
for line in (art/'r3_15d_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
 if not line.strip(): continue
 f=line.split('\t')
 if len(f)!=3 or f[2]!='PASS': raise SystemExit(f'bad identity row: {line!r}')
 ids[f[0].replace('\\','/')]=f[1].lower()
if set(paths)!=set(ids): raise SystemExit('selector/identity set mismatch')
out=[]
for rel in paths:
 p=root/rel
 if not p.is_file(): raise SystemExit(f'missing replay: {rel}')
 actual=sha256(p)
 if actual!=ids[rel]: raise SystemExit(f'SHA mismatch: {rel}')
 out.append(f'{rel}\t{actual}\tPASS')
Path('r3_16a_paths.txt').write_text(''.join(x+'\n' for x in paths),encoding='utf-8')
Path('r3_16a_replay_identity.tsv').write_text('\n'.join(out)+'\n',encoding='utf-8')
Path('r3_16a_parent_evidence_identity.txt').write_text('parent_pass=R3.15D\nparent_run=31736738234\nparent_artifact_id=9195419601\nparent_artifact_digest=sha256:f6e11055c11ed0724c45fcc76c13a9da2dbbb285ab3744f9738f0d4a19ecab8a\nselector_rows=47\nidentity_rows=47\n',encoding='utf-8')
print('R3_16A_SELECTOR_IDENTITY=PASS rows=47')
