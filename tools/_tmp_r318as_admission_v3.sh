#!/usr/bin/env bash
set -euo pipefail
BASE=34897d5c7c24bd6ecba526fb3e951681a69d18c6
TREE=bb2e1ba77432af772f15f32a85c334f1dc2e6bf9
AS_HEAD=475650fea59332f74b9f69da50e3e4471622ab7e
GEN=7c5de5fb3a1e451a49b9620db4e1937b867aa21ffcbb11d7ac37ad4b033c3210
CAND=continuity/r318as-admit-at-v1
repo="$GITHUB_REPOSITORY"
test "$(gh api "repos/$repo/branches/main" --jq .commit.sha)" = "$BASE"
test "$(gh api "repos/$repo/git/commits/$BASE" --jq .tree.sha)" = "$TREE"
for r in 32959321642 32959321531; do test "$(gh api "repos/$repo/actions/runs/$r" --jq .head_sha)" = "$AS_HEAD"; test "$(gh api "repos/$repo/actions/runs/$r" --jq .conclusion)" = success; done
test "$(gh api "repos/$repo/actions/artifacts/9603335255" --jq .digest)" = 'sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45'
if git ls-remote --exit-code --heads "https://github.com/$repo.git" "refs/heads/$CAND" >/dev/null 2>&1; then echo duplicate-candidate >&2; exit 1; fi
cat tools/_tmp_r318as_admit.part{0..7} | base64 -d | gzip -dc > "$RUNNER_TEMP/gen.py"
test "$(sha256sum "$RUNNER_TEMP/gen.py" | awk '{print $1}')" = "$GEN"
python -m py_compile "$RUNNER_TEMP/gen.py"
git fetch --no-tags --depth=1 origin "$BASE"
git reset --hard FETCH_HEAD
git clean -fdx
git switch -C "$CAND" "$BASE"
python "$RUNNER_TEMP/gen.py"
python - <<'PY'
from pathlib import Path
p=Path('docs/continuity/MIMIR_PROGRESS_LEDGER.md')
p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n',encoding='utf-8')
PY
cat > "$RUNNER_TEMP/expected" <<'FILES'
MIMIR_CONTINUE_HERE.md
MIMIR_KNOWLEDGE_GRAPH.md
docs/continuity/MIMIR_BOUNDARY_LOCKS.md
docs/continuity/MIMIR_CONTINUITY_STATE.json
docs/continuity/MIMIR_CURRENT_STATE.md
docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md
docs/continuity/MIMIR_PROGRESS_LEDGER.md
docs/continuity/MIMIR_R3_18AS_DECISION.md
docs/continuity/MIMIR_R3_18AT_EXECUTION_SPEC.md
FILES
{ git diff --name-only; git ls-files --others --exclude-standard; } | sort -u > "$RUNNER_TEMP/actual"
sort -o "$RUNNER_TEMP/expected" "$RUNNER_TEMP/expected"
diff -u "$RUNNER_TEMP/expected" "$RUNNER_TEMP/actual"
test "$(wc -l < "$RUNNER_TEMP/actual")" -eq 9
git diff --check
python -m json.tool docs/continuity/MIMIR_CONTINUITY_STATE.json >/dev/null
pwsh -NoProfile -File scripts/verify_mimir_knowledge_archive.ps1
grep -F 'unique exact contexts                 16' docs/continuity/MIMIR_R3_18AS_DECISION.md
grep -F 'is_rl_223' docs/continuity/MIMIR_R3_18AT_EXECUTION_SPEC.md
grep -F '135. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`' MIMIR_KNOWLEDGE_GRAPH.md
git config user.name 'MIMIR Admission Bot'; git config user.email 'actions@users.noreply.github.com'
git add -- $(cat "$RUNNER_TEMP/expected")
git commit -m 'Admit R3.18AS and open R3.18AT'
test "$(git rev-parse HEAD^)" = "$BASE"
test "$(gh api "repos/$repo/branches/main" --jq .commit.sha)" = "$BASE"
if git ls-remote --exit-code --heads "https://github.com/$repo.git" "refs/heads/$CAND" >/dev/null 2>&1; then echo candidate-race >&2; exit 1; fi
git remote set-url origin "https://x-access-token:${GH_TOKEN}@github.com/${repo}.git"
git push origin "HEAD:refs/heads/$CAND"
mkdir -p "$RUNNER_TEMP/receipt"
printf 'R3_18AS_CONTINUITY_BUILDER_V3=PASS\nbase=%s\ncandidate=%s\ntree=%s\nfiles=9\nnext=R3.18AT\n' "$BASE" "$(git rev-parse HEAD)" "$(git rev-parse HEAD^{tree})" > "$RUNNER_TEMP/receipt/receipt.txt"
