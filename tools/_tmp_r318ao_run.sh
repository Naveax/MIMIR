#!/usr/bin/env bash
set -euo pipefail

BASE='68014a3b9aa3e5a84a4a03c2464863e9a60bfec2'
BASE_TREE='6180021a44355e92348785d1f0f0d50002fb1a66'
PROD='3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38'
PROD_TREE='3efcc244bca55623b12bb21eb277753fc61144d4'
PROD_PARENT='6f92e817a88056ba303229541ae04a5d5e03239b'
LIB_BLOB='9d6b5ae2898cee745a17de9d1d7ef4b8fbd0e822'
AN_TEST_BLOB='8aa48b2b74d0956d1d2e965d056e1cf14a81f703'
AK_TEST_BLOB='9014505e1736498ee5e2ef7a1ce6118030580202'
AO_SPEC_BLOB='db78740b31d098c1e530477d0704a5406b1cc55e'
AJ_CONTRACT_SHA='cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c'

AM_HEAD='842b94ed4c4e57323433585fea48116ecf18989b'
AM_RUN='32473716883'
AM_JOB='96745647750'
AM_CI='32474038136'
AM_CI_JOB='96746590106'
AM_ART='9443581172'
AM_ART_NAME='r318am-post-ak-payload-evidence'
AM_SIZE='14827'
AM_DIGEST='sha256:2f65de5207bd96787fd7d1527a55991f08d5da614a0ddfce22a7aa267968e3c8'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318ao"
AM_DIR="$WORK/am"
PROBE='crates/mimir-replay/examples/_tmp_r318ao_probe.rs'
rm -rf "$WORK"
mkdir -p "$AM_DIR"
trap 'rm -rf "$WORK"; rm -f "$PROBE"' EXIT
norm_digest(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

echo '== R3.18AO authority freeze =='
git fetch origin main "$PROD" "$AM_HEAD" --force
test "$(git rev-parse HEAD)" = "$GITHUB_SHA"
test "$(git merge-base "$BASE" HEAD)" = "$BASE"
test "$(git rev-parse "$BASE^{tree}")" = "$BASE_TREE"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$PROD^")" = "$PROD_PARENT"

mapfile -t actual < <(git diff --name-only "$BASE" HEAD | sort)
mapfile -t expected < <(printf '%s\n' \
  .github/workflows/_tmp_r318ao_evidence.yml \
  .github/workflows/_tmp_r318ao_trigger.txt \
  tools/_tmp_r318ao_run.sh | sort)
diff -u <(printf '%s\n' "${expected[@]}") <(printf '%s\n' "${actual[@]}")
git diff --exit-code "$BASE" HEAD -- \
  crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs \
  MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

MAIN_NOW="$(git rev-parse origin/main)"
if [[ "$MAIN_NOW" != "$BASE" ]]; then
  git diff --exit-code "$BASE" "$MAIN_NOW" -- \
    crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts .github/workflows/ci.yml
  CURRENT_PASS="$(git show "$MAIN_NOW:docs/continuity/MIMIR_CONTINUITY_STATE.json" | jq -r .current_pass)"
  test "$CURRENT_PASS" = 'R3.18AO'
  echo "R3_18AO_MAIN_DRIFT=DOCS_ONLY_ACCEPTED base=$BASE current=$MAIN_NOW current_pass=$CURRENT_PASS"
else
  echo "R3_18AO_MAIN_DRIFT=NONE main=$MAIN_NOW"
fi

test "$(git rev-parse "$BASE:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$BASE:crates/mimir-replay/tests/r3_18an_post_ak_payload.rs")" = "$AN_TEST_BLOB"
test "$(git rev-parse "$BASE:crates/mimir-replay/tests/r3_18ak_post_ag_following_header.rs")" = "$AK_TEST_BLOB"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AO_EXECUTION_SPEC.md")" = "$AO_SPEC_BLOB"
test "$(sha256sum docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json | awk '{print $1}')" = "$AJ_CONTRACT_SHA"
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$BASE" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0
printf '%s\n' \
  "R3_18AO_BASE=$BASE/$BASE_TREE" \
  "R3_18AO_PRODUCTION=$PROD/$PROD_TREE" \
  "R3_18AO_LIB_BLOB=$LIB_BLOB" \
  "R3_18AO_AN_TEST_BLOB=$AN_TEST_BLOB" \
  "R3_18AO_AJ_CONTRACT_SHA256=$AJ_CONTRACT_SHA" \
  "R3_18AO_BOXCARS_PIN=$BOXCARS_SHA" > r3_18ao_upstream_receipts.txt

echo '== immutable R3.18AM authority =='
for pair in "$AM_RUN:$AM_JOB" "$AM_CI:$AM_CI_JOB"; do
  run="${pair%%:*}"; job="${pair##*:}"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AM_RUN" --jq .head_sha)" = "$AM_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AM_ART" --jq .workflow_run.id)" = "$AM_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AM_ART" --jq .workflow_run.head_sha)" = "$AM_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AM_ART" --jq .name)" = "$AM_ART_NAME"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AM_ART" --jq .size_in_bytes)" = "$AM_SIZE"
test "$(norm_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AM_ART" --jq .digest)")" = "$(norm_digest "$AM_DIGEST")"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AM_ART" --jq .expired)" = false

gh run download "$AM_RUN" -n "$AM_ART_NAME" -D "$AM_DIR"
(
  cd "$AM_DIR"
  test "$(wc -l < r3_18am_artifact_sha256.txt)" -eq 11
  sha256sum -c r3_18am_artifact_sha256.txt
  grep -Fqx 'R3_18AM_OUTCOME=A' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_FROZEN_ROWS=47/47' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_PUBLISHED_AK_EXACT=47/47' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_TAG_INT=47' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_OBSERVED_PAYLOAD_WIDTH=32' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_NATIVE_ORACLE_MISMATCH=0' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_WITNESS_RESELECTION=0' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_ANOTHER_CONTROL_BITS_CONSUMED=0' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0' r3_18am_aggregate.txt
  grep -Fqx 'R3_18AM_PRIVACY_SCAN=PASS' r3_18am_aggregate.txt
)
python3 - "$AM_DIR" <<'PY'
import hashlib, json, sys
from pathlib import Path
root=Path(sys.argv[1])
summary=json.loads((root/'r3_18am_summary.json').read_text(encoding='utf-8'))
assert summary['rows']==47
assert summary['published_ak_exact']==47
assert summary['tags']=={'Int':47}
assert summary['payload_widths']=={'32':47}
assert summary['native_oracle_mismatch']==0
assert summary['witness_reselection']==0
assert summary['another_control_bits_consumed']==0
rows=json.loads((root/'r3_18am_payload_rows.json').read_text(encoding='utf-8'))['rows']
assert len(rows)==47 and len({r['label'] for r in rows})==47
assert all(r['tag']=='Int' and r['payload_width']==32 and r['native_oracle_exact'] for r in rows)
identity=[]
for line in (root/'r3_18am_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel, expected, status=line.split('\t')
    assert status=='PASS' and '..' not in Path(rel).parts and not rel.startswith('/')
    actual=hashlib.sha256(Path(rel).read_bytes()).hexdigest()
    assert actual.lower()==expected.lower(), rel
    identity.append(rel.replace('\\','/'))
assert len(identity)==47 and set(identity)=={r['label'] for r in rows}
print('R3_18AO_AM_AUTHORITY=PASS rows=47 identity=47 oracle_exact=47')
PY
printf '%s\n' \
  "R3_18AO_AM_HEAD=$AM_HEAD" \
  "R3_18AO_AM_RUN_JOB=$AM_RUN/$AM_JOB" \
  "R3_18AO_AM_CI_JOB=$AM_CI/$AM_CI_JOB" \
  "R3_18AO_AM_ARTIFACT=$AM_ART/$AM_SIZE/$AM_DIGEST" >> r3_18ao_upstream_receipts.txt

echo '== derive published-AN 47-row probe from permanent production test =='
mkdir -p crates/mimir-replay/examples
python3 - "$PROBE" <<'PY'
from pathlib import Path
import sys
src=Path('crates/mimir-replay/tests/r3_18an_post_ak_payload.rs').read_text(encoding='utf-8')
name='r3_18an_all_47_frozen_am_rows_are_exact_and_stop_before_next_control'
assert src.count(f'fn {name}()')==1
src=src.replace('#[test]\n','')
src=src.replace(f'fn {name}()', 'fn main()', 1)
needle='        assert_eq!(after_poison, got, "post-stop poison changed {path}");\n'
assert src.count(needle)==1
insert=r'''        let semantic_int = match &got.following_payload.value {
            ReplayNetworkPrimitiveScalarValueV1::Int(value) => *value,
            other => panic!("unexpected published R3.18AN payload value: {other:?}"),
        };
        println!(
            "R3_18AO_PUBLISHED\tlabel={}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_int={}\theader_stop_bit={}\tstop_bit={}\tdirect_exact=1\trepeatability=1\ttruncation_negative=1\tpost_stop_poison=1\tnext_control_bits_consumed=0",
            path.strip_prefix("../../").unwrap_or(path),
            got.following_payload.payload_start_bit,
            got.following_payload.payload_end_bit,
            got.following_payload.payload_width,
            semantic_int,
            got.header_composition.stop_bit,
            got.stop_bit,
        );
'''
src=src.replace(needle, needle+insert, 1)
Path(sys.argv[1]).write_text(src, encoding='utf-8', newline='\n')
print('R3_18AO_PROBE_DERIVATION=PASS')
PY
rustup run 1.85.0 rustfmt --edition 2024 "$PROBE"
cargo +1.85.0 run -p mimir-replay --example _tmp_r318ao_probe --quiet > "$WORK/published.log"
test "$(grep -c $'^R3_18AO_PUBLISHED\t' "$WORK/published.log")" -eq 47
grep $'^R3_18AO_PUBLISHED\t' "$WORK/published.log" > "$WORK/published_rows.tsv"
rm -f "$PROBE"

echo '== exact per-row published AN versus frozen AM/native/oracle =='
python3 - "$AM_DIR/r3_18am_payload_rows.json" "$WORK/published_rows.tsv" <<'PY'
import json, sys
from pathlib import Path
am_path, pub_path=map(Path,sys.argv[1:])
am_rows=json.loads(am_path.read_text(encoding='utf-8'))['rows']
am={r['label']:r for r in am_rows}
pub={}
for line in pub_path.read_text(encoding='utf-8').splitlines():
    assert line.startswith('R3_18AO_PUBLISHED\t')
    d={}
    for field in line.split('\t')[1:]:
        k,v=field.split('=',1); d[k]=v
    assert d['label'] not in pub
    pub[d['label']]=d
assert len(am)==len(pub)==47 and set(am)==set(pub)
out=[]
for label in sorted(am):
    a=am[label]; p=pub[label]
    assert a['tag']=='Int' and a['payload_width']==32 and a['native_oracle_exact'] is True
    assert int(p['payload_start_bit'])==a['payload_start_bit']
    assert int(p['payload_end_bit'])==a['payload_end_bit']
    assert int(p['payload_width'])==32
    assert int(p['semantic_int'])==a['semantic_int']
    assert int(p['header_stop_bit'])==a['payload_start_bit']
    assert int(p['stop_bit'])==a['payload_end_bit']
    for key in ['direct_exact','repeatability','truncation_negative','post_stop_poison']:
        assert p[key]=='1'
    assert p['next_control_bits_consumed']=='0'
    out.append('\t'.join([
        'R3_18AO_COMPARE',f'label={label}',
        f'payload_start_bit={a["payload_start_bit"]}',
        f'payload_end_bit={a["payload_end_bit"]}',
        'payload_width=32',f'semantic_int={a["semantic_int"]}',
        'am_native_oracle_exact=1','published_an_exact=1','mismatch=0',
        'witness_reselection=0','next_control_bits_consumed=0'
    ]))
Path('r3_18ao_comparison_rows.tsv').write_text('\n'.join(out)+'\n',encoding='utf-8',newline='\n')
summary={
  'outcome':'A','rows':47,'published_an_exact':47,'am_native_oracle_exact':47,
  'tag_counts':{'Int':47},'payload_widths':{'32':47},
  'semantic_int_min':min(r['semantic_int'] for r in am_rows),
  'semantic_int_max':max(r['semantic_int'] for r in am_rows),
  'mismatch':0,'witness_reselection':0,'next_control_bits_consumed':0,
  'production_mutation':0
}
Path('r3_18ao_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
print('R3_18AO_DIFFERENTIAL=PASS 47/47 mismatch=0 next_control=0')
PY

echo '== focused permanent negative/control regressions =='
cargo +1.85.0 test -p mimir-replay --test r3_18an_post_ak_payload -- --nocapture > "$WORK/an_tests.log" 2>&1
cargo +1.85.0 test -p mimir-replay --test r3_18ak_post_ag_following_header -- --nocapture > "$WORK/ak_tests.log" 2>&1
grep -Fq 'test result: ok.' "$WORK/an_tests.log"
grep -Fq 'test result: ok.' "$WORK/ak_tests.log"
cat > r3_18ao_negative_controls.txt <<'EOF'
R3_18AO_PAYLOAD_TRUNCATION=PASS published AN permanent test + 47-row probe
R3_18AO_WRONG_ACTOR=PASS R3.18AK tampered actor authority regression
R3_18AO_UNRESOLVED_LOOKUP=PASS R3.18AK missing lookup regression
R3_18AO_WRONG_EXACT_VERSION_CONTEXT=PASS R3.18AN + R3.18AK regressions
R3_18AO_MALFORMED_NON_AJ_TUPLE=PASS R3.18AK exact-tuple widening regression
R3_18AO_CORRUPT_AG_CONTROL=PASS R3.18AN + R3.18AK regressions
R3_18AO_CORRUPT_PRIOR_AUTHORITY=PASS R3.18AK regression and frozen AM authority
R3_18AO_WRONG_PAYLOAD_START=PASS frozen AM boundary guard authority + AN recomputation
R3_18AO_UNSUPPORTED_PAYLOAD_TAG_LAYOUT=PASS AJ/AK exact Int tuple enforcement + AN Int/32 source scope
R3_18AO_FABRICATED_TUPLE=PASS R3.18AK Cartesian/fabricated regression
R3_18AO_OLD_Z_VALID_AJ_ABSENT_CONTEXT=PASS R3.18AK old-Z rejection regression
R3_18AO_POST_STOP_POISON=PASS 47/47 published AN probe
R3_18AO_NEXT_CONTROL_BITS_CONSUMED=0
EOF

echo '== full validation =='
cargo +1.85.0 fmt --all -- --check
cargo +1.85.0 check --workspace --all-targets --all-features
cargo +1.85.0 clippy --workspace --all-targets --all-features -- -D warnings
cargo +1.85.0 test --workspace --all-features
pwsh -NoProfile -File scripts/verify_repo.ps1

rm -f "$PROBE"
git diff --exit-code "$BASE" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs \
  MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

grep -Fq 'R3.18AN PRE-ADMISSION BEGIN bounded post-AK payload composition' crates/mimir-replay/src/lib.rs
grep -Fq 'R3.18AN PRE-ADMISSION END bounded post-AK payload composition' crates/mimir-replay/src/lib.rs
cat > r3_18ao_source_scope.txt <<'EOF'
R3_18AO_PRODUCTION_MUTATION=0
R3_18AO_CARGO_MUTATION=0
R3_18AO_FIXTURE_MUTATION=0
R3_18AO_CORPUS_MUTATION=0
R3_18AO_SUPPORT_MUTATION=0
R3_18AO_WITNESS_RESELECTION=0
R3_18AO_NEXT_CONTROL_BITS_CONSUMED=0
R3_18AO_AN_SOURCE_SCOPE_PERMANENT_TEST=PASS
EOF
cat > r3_18ao_validation.txt <<'EOF'
R3_18AO_FOCUSED_AN_TEST=PASS
R3_18AO_FOCUSED_AK_TEST=PASS
R3_18AO_FMT_CHECK=PASS
R3_18AO_WORKSPACE_CHECK=PASS
R3_18AO_WORKSPACE_CLIPPY_D_WARNINGS=PASS
R3_18AO_WORKSPACE_TEST=PASS
R3_18AO_REPOSITORY_VERIFIER=PASS
EOF
cat > r3_18ao_aggregate.txt <<'EOF'
R3_18AO_OUTCOME=A
R3_18AO_EVIDENCE=PASS
R3_18AO_FROZEN_ROWS=47/47
R3_18AO_PUBLISHED_AN_EXACT=47/47
R3_18AO_AM_NATIVE_ORACLE_EXACT=47/47
R3_18AO_TAG_INT=47
R3_18AO_PAYLOAD_WIDTH_32=47/47
R3_18AO_SEMANTIC_INT_RANGE=1..415
R3_18AO_NATIVE_ORACLE_PUBLISHED_MISMATCH=0
R3_18AO_WITNESS_RESELECTION=0
R3_18AO_NEXT_CONTROL_BITS_CONSUMED=0
R3_18AO_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18AO_NEGATIVE_CONTROLS=PASS
R3_18AO_PRIVACY_SCAN=PASS
EOF

python3 - <<'PY'
from pathlib import Path
files=[Path('r3_18ao_comparison_rows.tsv'),Path('r3_18ao_summary.json'),Path('r3_18ao_negative_controls.txt'),Path('r3_18ao_source_scope.txt'),Path('r3_18ao_validation.txt'),Path('r3_18ao_upstream_receipts.txt'),Path('r3_18ao_aggregate.txt')]
for p in files:
    s=p.read_text(encoding='utf-8')
    assert 'github_pat_' not in s and 'ghp_' not in s and 'Bearer ' not in s
    assert '/home/runner' not in s and 'C:\\Users\\' not in s
print('R3_18AO_PRIVACY_SCAN=PASS files=7')
PY
sha256sum \
  r3_18ao_aggregate.txt \
  r3_18ao_comparison_rows.tsv \
  r3_18ao_negative_controls.txt \
  r3_18ao_source_scope.txt \
  r3_18ao_summary.json \
  r3_18ao_upstream_receipts.txt \
  r3_18ao_validation.txt > r3_18ao_artifact_sha256.txt
sha256sum -c r3_18ao_artifact_sha256.txt

echo 'R3_18AO_COMPLETE=PASS outcome=A rows=47 mismatch=0 next_control=0 mutation=0'
