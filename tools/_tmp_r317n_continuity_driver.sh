#!/usr/bin/env bash
set -euo pipefail
BASE_MAIN='c8ebb872e510574bb69ab28c719f415ece8b7665'
PROD_SHA='7390e3b145372252caaa8fa1fe3e0cd13b83336c'
PROD_TREE='eebe4e21de77a43b5d9d43a34a0bfb08e06bab02'
LIB_BLOB='28d213f831c8968e6756a6ccea2cd7aa6cdbdfba'
K3_GROUP_BLOB='da545a7144fefabab7f5be4f07fde71311065293'
K3_TEST_BLOB='4d1434cc0e59a6e5c72a8404c102a87d71b8b223'
N_GROUP_BLOB='b5fa6aaa729772ab3d113703952effe2346c9866'
N_CONTRACT_BLOB='76deabf8241b419ca224645106d2a19b041e20f8'
N_GROUP_SHA='80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b'
N_AUTH_HEAD='086ec251aea4eea9881cfc224bfac2d09596269f'

files=(
  MIMIR_CONTINUE_HERE.md
  MIMIR_KNOWLEDGE_GRAPH.md
  docs/continuity/MIMIR_CONTINUITY_STATE.json
  docs/continuity/MIMIR_CURRENT_STATE.md
  docs/continuity/MIMIR_R3_17N_DECISION.md
  docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md
)

echo '=== frozen authority ==='
git fetch origin main agent/r317n-contract-admission-v4
test "$(git rev-parse origin/main)" = "$BASE_MAIN"
test "$(git rev-parse origin/agent/r317n-contract-admission-v4)" = "$N_AUTH_HEAD"
test "$(git rev-parse "${PROD_SHA}^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "${PROD_SHA}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${PROD_SHA}:crates/mimir-replay/src/k3_admitted_groups.rs")" = "$K3_GROUP_BLOB"
test "$(git rev-parse "${PROD_SHA}:crates/mimir-replay/tests/r3_17k_k3_attribute_decoder.rs")" = "$K3_TEST_BLOB"
test "$(git rev-parse "${BASE_MAIN}:docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl")" = "$N_GROUP_BLOB"
test "$(git rev-parse "${BASE_MAIN}:docs/continuity/MIMIR_R3_17N_CONTRACT.md")" = "$N_CONTRACT_BLOB"
python - <<'PY'
import hashlib, subprocess
expected='80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b'
data=subprocess.check_output(['git','show','c8ebb872e510574bb69ab28c719f415ece8b7665:docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl'])
assert hashlib.sha256(data).hexdigest()==expected
print('R3_17N_CONTINUITY_FROZEN_AUTHORITY=PASS')
PY

echo '=== generate ==='
python tools/_tmp_r317n_continuity.py
python tools/_tmp_r317n_authority_fix.py
python tools/_tmp_r317n_continuity_trim.py

echo '=== scope ==='
git add -- "${files[@]}"
mapfile -t actual < <(git diff --cached --name-only | sort)
mapfile -t expected < <(printf '%s\n' "${files[@]}" | sort)
test "${#actual[@]}" -eq 6
test "$(printf '%s\n' "${actual[@]}")" = "$(printf '%s\n' "${expected[@]}")"
git diff --cached --check
if git diff --cached --name-only | grep -Eq '(^|/)(Cargo\.toml|Cargo\.lock)$|^crates/|^external_fixtures/|^test_corpus/|MIMIR_R3_17N_(CONTRACT|ADMITTED_GROUPS)'; then
  echo 'forbidden continuity mutation' >&2; exit 1
fi
echo 'R3_17N_CONTINUITY_SCOPE=PASS'

echo '=== semantics ==='
python - <<'PY'
import json
from pathlib import Path
main='c8ebb872e510574bb69ab28c719f415ece8b7665'
prod='7390e3b145372252caaa8fa1fe3e0cd13b83336c'
auth='086ec251aea4eea9881cfc224bfac2d09596269f'
group='80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b'
state=json.loads(Path('docs/continuity/MIMIR_CONTINUITY_STATE.json').read_text(encoding='utf-8'))
assert state['last_production_code_sha']==prod
assert state['last_production_milestone']=='R3.17K'
assert state['last_completed_contract_pass']=='R3.17N'
assert state['current_pass']=='R3.17O'
n=state['r3_17n']
assert n['authority_head']==auth
assert n['workflow_run']==31883205829 and n['workflow_job']==95008550716
assert n['clean_contract_sha']==main
assert n['clean_contract_tree']=='61e36d40e6af3853a887e840b22f759dda26ed75'
assert n['exact_candidate_ci_run']==31883438754 and n['exact_candidate_ci_job']==95009080782
assert n['published_knowledge_archive_run']==31883625387 and n['published_knowledge_archive_job']==95009532717
assert n['published_main_ci_run']==31883625362 and n['published_main_ci_job']==95009532734
assert n['evidence_equality']=='161/161 byte-identical'
assert n['admitted_groups_sha256']==group
assert n['cross_product_widening']==0
assert n['production_cargo_fixture_corpus_support_mutation']=='0/0/0/0/0'
for item in ['docs/continuity/MIMIR_R3_17N_CONTRACT.md','docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl','docs/continuity/MIMIR_R3_17N_DECISION.md','docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md']:
    assert item in state['next_files_to_read']
paths=['MIMIR_CONTINUE_HERE.md','MIMIR_KNOWLEDGE_GRAPH.md','docs/continuity/MIMIR_CURRENT_STATE.md','docs/continuity/MIMIR_R3_17N_DECISION.md','docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md']
texts=[Path(p).read_text(encoding='utf-8') for p in paths]
for t in texts[:4]: assert 'R3.17N' in t and '161' in t
for t in texts[:3]+[texts[4]]: assert 'R3.17O' in t
assert auth in texts[0] and auth in texts[1] and auth in texts[3]
for t in texts: assert group in t
assert 'R3.17P' in texts[3] and 'R3.17P' in texts[4]
assert 'R3.18 remains closed' in texts[3] and 'R3.18 remains closed' in texts[4]
assert '161/161' in texts[4] and 'cross-product widening' in texts[4]
print('R3_17N_CONTINUITY_SEMANTICS=PASS')
PY

echo '=== archive/verifier ==='
pwsh -NoProfile -File scripts/verify_mimir_knowledge_archive.ps1
rustup component add rustfmt clippy
pwsh -NoProfile -File scripts/verify_repo.ps1

echo '=== clean publication ==='
git fetch origin main
test "$(git rev-parse origin/main)" = "$BASE_MAIN"
export GIT_INDEX_FILE="$RUNNER_TEMP/r317n-continuity-v2.index"
rm -f "$GIT_INDEX_FILE"
git read-tree "$BASE_MAIN"
for f in "${files[@]}"; do
  blob="$(git hash-object -w -- "$f")"
  git update-index --add --cacheinfo "100644,$blob,$f"
done
tree="$(git write-tree)"
base_tree="$(git rev-parse "${BASE_MAIN}^{tree}")"
mapfile -t actual < <(git diff-tree --no-commit-id --name-only -r "$base_tree" "$tree" | sort)
mapfile -t expected < <(printf '%s\n' "${files[@]}" | sort)
test "${#actual[@]}" -eq 6
test "$(printf '%s\n' "${actual[@]}")" = "$(printf '%s\n' "${expected[@]}")"
git diff-tree --check "$base_tree" "$tree"
export GIT_AUTHOR_NAME='github-actions[bot]'
export GIT_AUTHOR_EMAIL='41898282+github-actions[bot]@users.noreply.github.com'
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
sha="$(printf '%s\n' 'Close R3.17N and open R3.17O K4 implementation' | git commit-tree "$tree" -p "$BASE_MAIN")"
test "$(git rev-parse "${sha}^")" = "$BASE_MAIN"
git push origin "${sha}:refs/heads/candidate/r3-17n-continuity-clean-v2"
echo "CANDIDATE_SHA=$sha"
echo "CANDIDATE_TREE=$tree"
echo 'R3_17N_CONTINUITY_CANDIDATE=PASS'
