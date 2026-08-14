#!/usr/bin/env bash
set -euo pipefail

BASE_SHA='2d338d4244ce07122bb97097c516193f68ff73b7'
PROD_SHA='9bfa837c69c4751f70ca63a17c65f0f89877ff32'
PROD_BLOB='7288238cfb5338653552435be6af41f0dd7a4e85'
TEST_BLOB='92033a72a8a737605ac3bf91e10d130082277e04'
EVIDENCE_HEAD='19db534a3668f84f1c5ce36ef1252c52841d890f'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'
PATCH_SHA256='d3261462d7b83f3864254bf04ead6cf4c5e6d9c023f4d123be90c48befe32700'
ARTIFACT_ID='9219554878'
EXPECTED_DIGEST='sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc'
EXPECTED_WITNESS_SHA='7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b'

mkdir -p .tmp/r317h .tmp/r317e-evidence

test "$(git rev-parse HEAD:crates/mimir-replay/src/lib.rs)" = "$PROD_BLOB"
test "$(git rev-parse HEAD:crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs)" = "$TEST_BLOB"
git cat-file -e "${PROD_SHA}^{commit}"
git cat-file -e "${BASE_SHA}^{commit}"
git cat-file -e "${EVIDENCE_HEAD}^{commit}"
git diff --exit-code "$BASE_SHA"..HEAD -- crates/mimir-replay/src/lib.rs crates/mimir-replay/Cargo.toml Cargo.toml Cargo.lock external_fixtures test_corpus
printf 'base_main=%s\nnative_production_sha=%s\nnative_source_blob=%s\nfocused_test_blob=%s\nproduction_mutation=0\ncargo_mutation=0\ncorpus_fixture_mutation=0\n' \
  "$BASE_SHA" "$PROD_SHA" "$PROD_BLOB" "$TEST_BLOB" > r3_17h_source_scope.txt
echo 'R3_17H_NATIVE_FREEZE=PASS'

META_DIGEST="$(gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${ARTIFACT_ID}" --jq '.digest')"
EXPIRED="$(gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${ARTIFACT_ID}" --jq '.expired')"
test "$META_DIGEST" = "$EXPECTED_DIGEST"
test "$EXPIRED" = 'false'
gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${ARTIFACT_ID}/zip" > .tmp/r317h/r317e.zip
python - <<'PY'
import zipfile
with zipfile.ZipFile('.tmp/r317h/r317e.zip') as z:
    z.extractall('.tmp/r317e-evidence')
PY
test "$(sha256sum .tmp/r317e-evidence/r3_17e_k2_witnesses.jsonl | awk '{print $1}')" = "$EXPECTED_WITNESS_SHA"
test "$(wc -l < .tmp/r317e-evidence/r3_17e_k2_witnesses.jsonl | tr -d ' ')" -eq 469
test "$(wc -l < .tmp/r317e-evidence/r3_17e_replay_identity.tsv | tr -d ' ')" -eq 47
cp .tmp/r317e-evidence/r3_17e_replay_identity.tsv r3_17h_replay_identity.tsv
python - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_17h_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    rel, expected, status = line.split('\t')
    if status != 'PASS': raise SystemExit(f'bad identity status: {line}')
    p=Path(rel)
    if not p.is_file(): raise SystemExit(f'missing replay: {rel}')
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1<<20), b''): h.update(chunk)
    if h.hexdigest()!=expected: raise SystemExit(f'replay SHA mismatch: {rel}')
    rows.append(rel)
if len(rows)!=47 or len(set(rows))!=47: raise SystemExit('expected 47 unique replay identities')
Path('.tmp/r317h/paths.txt').write_text('\n'.join(rows)+'\n',encoding='utf-8',newline='\n')
print('R3_17H_REPLAY_IDENTITIES=PASS rows=47')
PY
printf 'artifact_id=%s\nartifact_digest=%s\nwitness_sha256=%s\n' "$ARTIFACT_ID" "$META_DIGEST" "$EXPECTED_WITNESS_SHA" >> r3_17h_source_scope.txt
echo 'R3_17H_IMMUTABLE_ARTIFACT=PASS'

git show "$EVIDENCE_HEAD:tools/_tmp_r317e_patch.py" > .tmp/r317h/r317e_patch.py
test "$(sha256sum .tmp/r317h/r317e_patch.py | awk '{print $1}')" = "$PATCH_SHA256"
BOXCARS="$PWD/.tmp/boxcars-r317h"
rm -rf "$BOXCARS"
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" hash-object src/network/frame_decoder.rs)" = "$FRAME_BLOB"
test "$(git -C "$BOXCARS" hash-object src/network/attributes.rs)" = "$ATTR_BLOB"
python .tmp/r317h/r317e_patch.py "$BOXCARS"
python tools/_tmp_r317h_enhance.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_17e_probe.rs
git -C "$BOXCARS" diff --check
cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_17e_probe --quiet
sha256sum .tmp/r317h/r317e_patch.py tools/_tmp_r317h_enhance.py tools/_tmp_r317h_audit.py tools/_tmp_r317h_native.rs tools/_tmp_r317h_run.sh > r3_17h_driver_sha256.txt
echo 'R3_17H_BOXCARS_BUILD=PASS'

EXE=''
case "${OSTYPE:-}" in msys*|cygwin*) EXE='.exe' ;; esac
PROBE="$BOXCARS/target/debug/examples/r3_17e_probe$EXE"
test -x "$PROBE"
: > .tmp/r317h/boxcars.log
while IFS= read -r rel; do
  test -n "$rel"
  MIMIR_R3_17E_LABEL="$rel" "$PROBE" "$PWD/$rel" >> .tmp/r317h/boxcars.log 2>&1
done < .tmp/r317h/paths.txt
test "$(grep -c '^R3_17E_ORACLE_PARSE=PASS$' .tmp/r317h/boxcars.log)" -eq 47
test "$(grep -c '^R3_17E_K2' .tmp/r317h/boxcars.log)" -eq 110539
test "$(grep -c '^R3_17E_SHAPE_MISMATCH' .tmp/r317h/boxcars.log || true)" -eq 0
echo 'R3_17H_ORACLE_REGEN=PASS replays=47 occurrences=110539'

python tools/_tmp_r317h_audit.py prepare .tmp/r317e-evidence/r3_17e_k2_witnesses.jsonl .tmp/r317h/boxcars.log .tmp/r317h/native_input.tsv .tmp/r317h/oracle_expected.tsv
test "$(wc -l < .tmp/r317h/native_input.tsv | tr -d ' ')" -eq 469
test "$(wc -l < .tmp/r317h/oracle_expected.tsv | tr -d ' ')" -eq 469

mkdir -p .tmp/r317h-harness/src
cp tools/_tmp_r317h_native.rs .tmp/r317h-harness/src/main.rs
cat > .tmp/r317h-harness/Cargo.toml <<'EOF'
[package]
name = "r317h-audit-harness"
version = "0.0.0"
edition = "2024"

[dependencies]
mimir-replay = { path = "../../crates/mimir-replay" }

[workspace]
EOF
cargo run --quiet --manifest-path .tmp/r317h-harness/Cargo.toml -- .tmp/r317h/native_input.tsv > .tmp/r317h/native_output.tsv
test "$(grep -c '^ROW' .tmp/r317h/native_output.tsv)" -eq 469
test "$(grep -c '^NEG' .tmp/r317h/native_output.tsv)" -eq 7
if grep -q $'^ROW\t.*\tERR\t' .tmp/r317h/native_output.tsv; then
  grep $'^ROW\t.*\tERR\t' .tmp/r317h/native_output.tsv | head -20
  exit 1
fi
echo 'R3_17H_NATIVE_EXECUTION=PASS rows=469 negatives=7'

python tools/_tmp_r317h_audit.py finalize .tmp/r317e-evidence/r3_17e_k2_witnesses.jsonl .tmp/r317h/oracle_expected.tsv .tmp/r317h/native_output.tsv r3_17h_match_rows.jsonl r3_17h_summary.json r3_17h_aggregate.txt
for line in \
  'R3_17H_NATIVE_DECODE_SUCCESS=469' \
  'R3_17H_VARIANT_EXACT=469' \
  'R3_17H_PAYLOAD_WIDTH_EXACT=469' \
  'R3_17H_PAYLOAD_END_EXACT=469' \
  'R3_17H_CONTEXT_GATE_EXACT=469' \
  'R3_17H_SEMANTIC_VALUE_EXACT=469' \
  'R3_17H_NEGATIVE_CONTROLS=PASS' \
  'R3_17H_PRIVACY_SCAN=PASS' \
  'R3_17H_OUTCOME=A'; do
  grep -Fx "$line" r3_17h_aggregate.txt
done
test "$(wc -l < r3_17h_match_rows.jsonl | tr -d ' ')" -eq 469
echo 'R3_17H_DIFFERENTIAL=PASS'

test "$(git rev-parse HEAD:crates/mimir-replay/src/lib.rs)" = "$PROD_BLOB"
git diff --exit-code "$BASE_SHA"..HEAD -- crates/mimir-replay/src/lib.rs crates/mimir-replay/Cargo.toml Cargo.toml Cargo.lock external_fixtures test_corpus
pwsh -NoProfile -File ./scripts/verify_repo.ps1
sha256sum r3_17h_source_scope.txt r3_17h_replay_identity.tsv r3_17h_driver_sha256.txt r3_17h_match_rows.jsonl r3_17h_summary.json r3_17h_aggregate.txt > r3_17h_receipt_sha256.txt
echo 'R3_17H_FINAL_ZERO_MUTATION=PASS'
