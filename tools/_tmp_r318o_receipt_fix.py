#!/usr/bin/env python3
import json, sys
from pathlib import Path

OLD_DIG="e6dc02f087395e2d6b5fb568233484430feba51223848367edd2c6cf15b4b94d"
NEW_DIG="e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d"
HASHES={
"6120672ca758c4d951e63cb6c5e3dc4cdd003dc7438319c9d459a36331f0e123":"f0e12fcd241779c9e0d4d362e5364b309aacafc86d00b188816ab081d4156fa4",
"8f933b6601538d79624969e38290297389bcba217908c0b7ecd3526b807bd547":"54d12c79d829f74f139f3490c38d4886faea0dabad86e7e2bf4c8a70f164c735",
"f76e15fb1cec92e5f2604b2ace1be194446eda88613527dbfe1015fbceb815cb":"8b85d625067b7bc27e585aa5cf21e6f182c79212d6923b881197bce3cabc9848",
"a261368f51770efee56e3d8d760390f633b6190bed81446feaf57b076189ae01":"f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc",
"03e6d06c5435013df92ba9d1bcf799816352718795c6a02ece0ae97ea8336adb":"448a6402f24fa9d8ba8ebdaa0cf8f8de34970a50d25b8705d9de7f21c198ad0b",
"458329fb7924805774056c3187032c6149401143d31ff8f0f8d055bafa0cc625":"c4a8e5ef1df2bdfee34b1d97dc08c75ee19d843bd1ceb012e1cb7feb7da509e9",
"503bae96ac51ff27532fc80b5e537b3cb7ccd58cea1584a9a1f975da8a4748a9":"599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4",
"5993bff36da50dbb19a75dc7a42d1fc68a57d429636e8776dc972ba244c4b598":"5bb2b701b4156b53468a064c75e9259acb4264312bdf41274452633c5b4a73c0",
"02324f5a0caa68257a0af93999245124242569f8d582ab2aba2f8119fe6cd676":"170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233",
}
OLD=[(60,5,12,"Boolean",1),(60,5,13,"Boolean",2),(60,5,14,"ActiveActor",3),(60,5,17,"Boolean",3),(60,5,18,"Boolean",3),(60,5,19,"Boolean",7),(60,5,21,"Boolean",1),(60,5,22,"Boolean",2),(60,5,23,"Boolean",8),(60,5,27,"ActiveActor",3),(60,5,30,"ActiveActor",2),(60,5,42,"Boolean",1),(60,5,43,"Boolean",1),(60,5,44,"Boolean",3),(60,5,54,"Boolean",3),(67,6,37,"Boolean",1),(72,6,15,"Boolean",2),(110,6,44,"Boolean",1)]
NEW=[(60,5,32,"Boolean",1),(60,5,41,"Boolean",2),(60,5,78,"Boolean",4),(60,5,79,"Boolean",19),(60,5,80,"ActiveActor",6),(60,5,83,"ActiveActor",1),(60,5,85,"Boolean",1),(60,5,87,"Boolean",2),(60,5,89,"Boolean",1),(60,5,94,"Boolean",1),(60,5,102,"Boolean",2),(60,5,103,"Boolean",1),(60,5,106,"Boolean",1),(60,5,116,"Boolean",1),(67,6,61,"Boolean",1),(72,6,62,"Boolean",1),(72,6,65,"Boolean",1),(110,6,36,"ActiveActor",1)]
def req(c,m):
    if not c: raise SystemExit(m)
def table(rows):
    out=["| stream_id_bound | prop_id_bits | property object index | attribute tag | version | observed rows |","|---:|---:|---:|---|---|---:|"]
    out += [f"| {a} | {b} | {c} | `{t}` | `868.32 / net10` | {n} |" for a,b,c,t,n in rows]
    return "\n".join(out)
def write(p,s): p.write_text(s.rstrip()+"\n",encoding="utf-8",newline="\n")
def main():
    root=Path(sys.argv[1]); oldt=table(OLD); newt=table(NEW)
    targets=[root/'docs/continuity/MIMIR_R3_18O_DECISION.md',root/'docs/continuity/MIMIR_R3_18P_EXECUTION_SPEC.md',root/'docs/continuity/MIMIR_CURRENT_STATE.md',root/'docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md',root/'docs/continuity/MIMIR_PROGRESS_LEDGER.md',root/'MIMIR_KNOWLEDGE_GRAPH.md',root/'MIMIR_CONTINUE_HERE.md']
    for p in targets:
        s=p.read_text(encoding='utf-8'); s=s.replace(OLD_DIG,NEW_DIG)
        for a,b in HASHES.items(): s=s.replace(a,b)
        if oldt in s: s=s.replace(oldt,newt)
        write(p,s)
    # structured state
    p=root/'docs/continuity/MIMIR_CONTINUITY_STATE.json'; d=json.loads(p.read_text(encoding='utf-8'))
    req(d['current_pass']=='R3.18P','current pass drift'); d['r3_18o']['artifact_sha256']=NEW_DIG
    d['r3_18o']['receipt_correction']='2026-08-17 canonical GitHub artifact metadata + fresh run download; exact tuple identities and immutable hashes corrected; Outcome A unchanged'
    corr='docs/continuity/MIMIR_R3_18O_RECEIPT_CORRECTION.md'; files=d['next_files_to_read'];
    if corr in files: files.remove(corr)
    i=files.index('docs/continuity/MIMIR_R3_18O_DECISION.md')+1; files.insert(i,corr); d['next_files_to_read']=files
    write(p,json.dumps(d,indent=2,ensure_ascii=False))
    correction=f'''# MIMIR R3.18O Receipt Correction

Date: 2026-08-17  
Type: **continuity / immutable-receipt correction only**

## Why this correction exists

After R3.18O was admitted, a fresh download from the exact GitHub Actions run exposed that the published continuity receipt did not match the authoritative artifact bytes. R3.18P correctly failed its authority gate instead of inheriting those stale values.

Canonical authority is now established by **both** current GitHub artifact metadata and a fresh `gh run download` from run `32017369100`, artifact `9284144768`.

## Correct immutable receipt

- evidence head: `5046e1594b87ce2828db5faa48aceba456c3166f`
- run/job: `32017369100 / 95349613184` — SUCCESS
- artifact: `9284144768` / `25129` bytes
- artifact ZIP SHA-256: `{NEW_DIG}`
- source scope: `f0e12fcd241779c9e0d4d362e5364b309aacafc86d00b188816ab081d4156fa4`
- replay identity: `b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf`
- frozen witnesses: `99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7`
- R3.18N authority file: `54d12c79d829f74f139f3490c38d4886faea0dabad86e7e2bf4c8a70f164c735`
- Boxcars instrumentation receipt: `8b85d625067b7bc27e585aa5cf21e6f182c79212d6923b881197bce3cabc9848`
- source summary: `f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc`
- targets: `448a6402f24fa9d8ba8ebdaa0cf8f8de34970a50d25b8705d9de7f21c198ad0b`
- oracle header rows: `c4a8e5ef1df2bdfee34b1d97dc08c75ee19d843bd1ceb012e1cb7feb7da509e9`
- native header rows: `599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4`
- negatives: `5bb2b701b4156b53468a064c75e9259acb4264312bdf41274452633c5b4a73c0`
- aggregate: `170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233`
- inner-manifest file: `8082c22bdd0606f887700c720913b38b2dff7e758e261d41e22c31a195bb174d`

## Correct exact 18 structural contexts

{newt}

The aggregate facts remain unchanged: 47/47 following headers exact, mismatch 0, `Boolean=39`, `ActiveActor=8`, bounds `60=43, 67=1, 72=2, 110=1`, widths `5=43, 6=4`, all `868.32/net10`, payload/another-control consumption `0/0`.

## Impact

R3.18O **Outcome A remains valid**. No production capability changes. This correction repairs provenance hashes and exact tuple identities only. R3.18P remains active and must derive its contract from this corrected immutable authority.
'''
    write(root/'docs/continuity/MIMIR_R3_18O_RECEIPT_CORRECTION.md',correction)
    # KG mandatory insertion
    kp=root/'MIMIR_KNOWLEDGE_GRAPH.md'; s=kp.read_text(encoding='utf-8'); a=s.index('## Mandatory reading order'); b=s.index('\n### R3.18I payload evidence',a); paths=[]
    for line in s[a:b].splitlines():
        z=line.strip()
        if z and z[0].isdigit() and '`' in z: paths.append(z.split('`',2)[1])
    if corr in paths: paths.remove(corr)
    i=paths.index('docs/continuity/MIMIR_R3_18O_DECISION.md')+1; paths.insert(i,corr)
    rebuilt='## Mandatory reading order\n\n'+'\n'.join(f'{i}. `{x}`' for i,x in enumerate(paths,1))+'\n'; s=s[:a]+rebuilt+s[b:]
    marker='### R3.18O following-property header evidence: OUTCOME A / CLOSED\n'
    pos=s.index(marker); note=f'''### R3.18O receipt correction: CLOSED\n- canonical artifact digest `{NEW_DIG}` verified against current GitHub artifact metadata and fresh run download\n- exact 18 tuple identities + inner hashes corrected; Outcome A unchanged; production unchanged\n\n'''
    # place correction after O section, before P heading
    phead=s.index('### R3.18P following-property header context contract: ACTIVE',pos); s=s[:phead]+note+s[phead:]; write(kp,s)
    # master final note before current checklist
    hp=root/'MIMIR_CONTINUE_HERE.md'; h=hp.read_text(encoding='utf-8'); final=h.rfind('# CURRENT PASS CHECKLIST — R3.18P'); req(final>=0,'P checklist missing')
    note=f'''# R3.18O RECEIPT CORRECTION — 2026-08-17\n\nCanonical GitHub artifact digest is `sha256:{NEW_DIG}`. Exact 18 tuple identities and inner hashes are those in `docs/continuity/MIMIR_R3_18O_RECEIPT_CORRECTION.md`. R3.18O Outcome A is unchanged; R3.18P must use only the corrected authority.\n\n'''; h=h[:final]+note+h[final:]; write(hp,h)
    # ledger append explicit correction
    lp=root/'docs/continuity/MIMIR_PROGRESS_LEDGER.md'; l=lp.read_text(encoding='utf-8').rstrip()+f'''\n\n## 2026-08-17 — R3.18O immutable receipt correction\n\nFresh exact-run artifact re-download caught stale receipt values before R3.18P admission. Correct ZIP digest: `{NEW_DIG}`. Exact tuple identities and inner hashes were corrected; aggregate Outcome A facts and production boundary are unchanged. R3.18P remains active and must use corrected authority.\n'''; write(lp,l)
    print('R3_18O_RECEIPT_CORRECTION_PATCH=PASS')
if __name__=='__main__': main()
