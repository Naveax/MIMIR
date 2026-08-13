#!/usr/bin/env bash
set -euo pipefail

BASE_SHA="76cbcc2094189e637e135f8c7d99e999e32311a0"
PRODUCTION_SHA="bf4bccff82203ed049d33e942681fed07f23beb4"
PRODUCTION_SOURCE_BLOB="f64a5e0d66962f41026b2eb10e176219d4529931"
BOXCARS_SHA="c70e77df7af81b436cb545d070bb90c82f562d0b"
BOXCARS_FRAME_BLOB="6f2ff153d3a27cdacccc65e3f23851489077a7d8"
R3_15A_RUN="31708322309"
R3_15A_ARTIFACT_ID="9184200143"
R3_15A_ARTIFACT_NAME="evidence-next-1e27674625fdff26e05436e882014db5c7c5116d"
R3_15A_ARTIFACT_DIGEST="sha256:a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d"

test "$(git rev-parse HEAD:crates/mimir-replay/src/lib.rs)" = "$PRODUCTION_SOURCE_BLOB"
git diff --exit-code "$BASE_SHA" HEAD -- \
  crates/mimir-replay/src/lib.rs crates/mimir-replay/Cargo.toml \
  Cargo.toml Cargo.lock external_fixtures test_corpus
mapfile -t changed < <(git diff --name-only "$BASE_SHA" HEAD | sort)
printf '%s\n' "${changed[@]}"
test "${#changed[@]}" -eq 6
for path in "${changed[@]}"; do
  case "$path" in
    .github/workflows/_tmp_r316a.yml|crates/mimir-replay/examples/_tmp_r316a_plan.rs|tools/_tmp_r316a_compare.py|tools/_tmp_r316a_driver.sh|tools/_tmp_r316a_patch.py|tools/_tmp_r316a_select.py) ;;
    *) echo "unexpected R3.16A temp path: $path" >&2; exit 1 ;;
  esac
done
{
  printf 'base_sha=%s\n' "$BASE_SHA"
  printf 'production_sha=%s\n' "$PRODUCTION_SHA"
  printf 'production_source_blob=%s\n' "$PRODUCTION_SOURCE_BLOB"
  printf 'production_mutation_count=0\ncargo_mutation_count=0\nfixture_corpus_mutation_count=0\n'
  printf 'temporary_paths=%s\n' "${changed[*]}"
} | tee r3_16a_source_scope.txt

digest="$(gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${R3_15A_ARTIFACT_ID}" --jq '.digest')"
test "$digest" = "$R3_15A_ARTIFACT_DIGEST"
mkdir -p .tmp/r3_15a
gh run download "$R3_15A_RUN" --repo "$GITHUB_REPOSITORY" \
  --name "$R3_15A_ARTIFACT_NAME" --dir .tmp/r3_15a
{
  printf 'parent_run=%s\n' "$R3_15A_RUN"
  printf 'parent_artifact_id=%s\n' "$R3_15A_ARTIFACT_ID"
  printf 'parent_artifact_name=%s\n' "$R3_15A_ARTIFACT_NAME"
  printf 'parent_artifact_digest=%s\n' "$digest"
} | tee r3_16a_parent_artifact_identity.txt
test -s .tmp/r3_15a/r3_15a_paths.txt
test -s .tmp/r3_15a/r3_15a_new_actor_all.jsonl

git clone --quiet https://github.com/nickbabcock/boxcars.git .tmp/boxcars
git -C .tmp/boxcars checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C .tmp/boxcars rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C .tmp/boxcars rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
git show 1e27674625fdff26e05436e882014db5c7c5116d:tools/_tmp_evidence_next.py > .tmp/r3_15a_patcher.py
python .tmp/r3_15a_patcher.py patch-boxcars .tmp/boxcars
python tools/_tmp_r316a_patch.py .tmp/boxcars
python - <<'PY'
from pathlib import Path
p = Path(".tmp/boxcars/src/network/frame_decoder.rs")
text = p.read_text(encoding="utf-8")
bad = '.ok_or(FrameEror::NotEnoughDataFor("Is prop present")))?;'
good = '.ok_or(FrameError::NotEnoughDataFor("Is prop present"))?;'
if text.count(bad) != 1:
    raise SystemExit(f"temporary instrumentation repair anchor count={text.count(bad)}")
p.write_text(text.replace(bad, good, 1), encoding="utf-8", newline="\n")
PY
git -C .tmp/boxcars diff --check
git -C .tmp/boxcars diff -- src/network/frame_decoder.rs > r3_16a_boxcars_instrumentation.patch
sha256sum r3_16a_boxcars_instrumentation.patch > r3_16a_boxcars_instrumentation_sha256.txt
{
  printf 'boxcars_sha=%s\n' "$BOXCARS_SHA"
  printf 'frame_blob=%s\n' "$BOXCARS_FRAME_BLOB"
  printf 'instrumentation_patch_sha256=%s\n' "$(sha256sum r3_16a_boxcars_instrumentation.patch | awk '{print $1}')"
} | tee r3_16a_boxcars_identity.txt

cargo build --manifest-path .tmp/boxcars/Cargo.toml --release --example r3_16a_probe

: > r3_16a_boxcars.log
while IFS= read -r rel; do
  test -n "$rel"
  export MIMIR_R3_16A_LABEL="$rel"
  .tmp/boxcars/target/release/examples/r3_16a_probe "$PWD/$rel" >> r3_16a_boxcars.log 2>&1
  printf 'R3_16A_PARSE\t%s\n' "$rel" >> r3_16a_boxcars.log
done < .tmp/r3_15a/r3_15a_paths.txt
test "$(grep -c '^R3_16A_PROPERTY' r3_16a_boxcars.log)" -eq 47
test "$(grep -c '^R3_16A_PARSE' r3_16a_boxcars.log)" -eq 47
python tools/_tmp_r316a_select.py --root "$PWD" --artifact .tmp/r3_15a --log r3_16a_boxcars.log

cargo fmt --all -- --check
cargo build --locked -p mimir-replay --example _tmp_r316a_plan

: > r3_16a_mimir.tsv
while IFS=$'\t' read -r rel actor_object_id stream_id; do
  test -n "$rel"
  target/debug/examples/_tmp_r316a_plan \
    "$rel" "$PWD/$rel" "$actor_object_id" "$stream_id" >> r3_16a_mimir.tsv
done < r3_16a_mimir_requests.tsv
test "$(grep -c '^R3_16A_MIMIR' r3_16a_mimir.tsv)" -eq 47
python tools/_tmp_r316a_compare.py --mimir r3_16a_mimir.tsv
grep -Fx 'R3_16A_OUTCOME=A' r3_16a_aggregate.txt
grep -Fx 'R3_16A_EVIDENCE=PASS' r3_16a_aggregate.txt

test "$(git rev-parse HEAD:crates/mimir-replay/src/lib.rs)" = "$PRODUCTION_SOURCE_BLOB"
git diff --exit-code "$BASE_SHA" HEAD -- \
  crates/mimir-replay/src/lib.rs crates/mimir-replay/Cargo.toml \
  Cargo.toml Cargo.lock external_fixtures test_corpus
printf 'production_mutation_count=0\ncargo_mutation_count=0\n' >> r3_16a_aggregate.txt
