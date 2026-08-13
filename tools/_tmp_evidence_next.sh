#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
BASE_SHA="a51c0c1bf8c8927f4e2f39691ec63403d70bb0a8"
PRODUCTION_SHA="7b17cb9033b6c71d476e500380d78402cbb3c56d"
BOXCARS_SHA="c70e77df7af81b436cb545d070bb90c82f562d0b"
FRAME_BLOB="6f2ff153d3a27cdacccc65e3f23851489077a7d8"
MODELS_BLOB="73c73991379aeb79dcee49ea31c417141ba3c1a6"
ORACLE_RUN="31690714121"
ORACLE_ARTIFACT_ID="9177314099"
ORACLE_ARTIFACT_NAME="r3-14a-pinned-oracle-evidence-v2-f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1"
ORACLE_ARTIFACT_SHA="d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b"

printf 'R3_15A_HEAD=%s\n' "$(git rev-parse HEAD)"
git cat-file -e "${BASE_SHA}^{commit}"
git cat-file -e "${PRODUCTION_SHA}^{commit}"
git merge-base --is-ancestor "$BASE_SHA" HEAD
test "$(git rev-parse "${PRODUCTION_SHA}:crates/mimir-replay/src/lib.rs")" = "$(git rev-parse 'HEAD:crates/mimir-replay/src/lib.rs')"
test "$(git rev-parse "${PRODUCTION_SHA}:Cargo.lock")" = "$(git rev-parse 'HEAD:Cargo.lock')"
test -z "$(git diff --name-only "$BASE_SHA" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md)"
printf 'production_sha=%s\ncontinuity_base_sha=%s\nevidence_head=%s\n' "$PRODUCTION_SHA" "$BASE_SHA" "$(git rev-parse HEAD)" > r3_15a_source_scope.txt

echo 'Recovering exact R3.14A oracle identity set'
mkdir -p .tmp/r3_14a
artifact_digest="$(gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${ORACLE_ARTIFACT_ID}" --jq .digest)"
test "$artifact_digest" = "sha256:${ORACLE_ARTIFACT_SHA}"
gh run download "$ORACLE_RUN" --repo "$GITHUB_REPOSITORY" --name "$ORACLE_ARTIFACT_NAME" --dir .tmp/r3_14a
test -s .tmp/r3_14a/r3_14a_first_actor_envelope.jsonl
printf 'oracle_run=%s\noracle_artifact_id=%s\noracle_artifact_digest=%s\n' "$ORACLE_RUN" "$ORACLE_ARTIFACT_ID" "$artifact_digest" > r3_15a_oracle_artifact_identity.txt
python - <<'PY'
import json
from pathlib import Path
rows=[json.loads(x) for x in Path('.tmp/r3_14a/r3_14a_first_actor_envelope.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
if len(rows) != 47 or len({r['sha256'].lower() for r in rows}) != 47:
    raise SystemExit('R3.14A identity set is not exact 47 unique replays')
Path('r3_15a_paths.txt').write_text(''.join(r['relative_path']+'\n' for r in rows), encoding='utf-8')
print('R3_15A_INPUT_IDENTITY_ROWS=47')
PY

echo 'Preparing exact pinned Boxcars instrumentation'
BOXCARS="$RUNNER_TEMP/boxcars-r3-15a"
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test -z "$(git -C "$BOXCARS" status --porcelain)"
test "$(git -C "$BOXCARS" hash-object src/network/frame_decoder.rs)" = "$FRAME_BLOB"
test "$(git -C "$BOXCARS" hash-object src/network/models.rs)" = "$MODELS_BLOB"
python tools/_tmp_evidence_next.py patch-boxcars "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_15a_probe.rs
git -C "$BOXCARS" diff --check
mapfile -t changed < <(git -C "$BOXCARS" diff --name-only | sort)
printf '%s\n' "${changed[@]}" > r3_15a_boxcars_changed_paths.txt
test "${#changed[@]}" -eq 2
test "${changed[0]}" = 'examples/r3_15a_probe.rs'
test "${changed[1]}" = 'src/network/frame_decoder.rs'
git -C "$BOXCARS" diff --binary -- examples/r3_15a_probe.rs src/network/frame_decoder.rs > r3_15a_boxcars_instrumentation.patch
sha256sum r3_15a_boxcars_instrumentation.patch > r3_15a_boxcars_instrumentation_sha256.txt
cargo check --manifest-path "$BOXCARS/Cargo.toml" --example r3_15a_probe
cargo test --manifest-path "$BOXCARS/Cargo.toml" --lib --quiet
cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_15a_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_15a_probe"
test -x "$PROBE"

: > r3_15a_boxcars.log
while IFS= read -r rel; do
  test -f "$ROOT/$rel"
  printf 'INPUT\t%s\n' "$rel" >> r3_15a_boxcars.log
  MIMIR_R3_15A_LABEL="$rel" "$PROBE" "$ROOT/$rel" >> r3_15a_boxcars.log 2>&1
done < r3_15a_paths.txt
test "$(grep -c '^R3_15A_ORACLE_PARSE=PASS$' r3_15a_boxcars.log)" -eq 47
test "$(grep -c '^R3_15A_NEWACTOR' r3_15a_boxcars.log)" -gt 0
printf 'R3_15A_BOXCARS_PARSE_SUCCESS=47\n'

echo 'Building independent MIMIR static-spawn plan probe'
python tools/_tmp_evidence_next.py write-mimir-example "$ROOT"
cargo build --locked -p mimir-replay --example _tmp_evidence_plan --quiet
MIMIR_PROBE="$ROOT/target/debug/examples/_tmp_evidence_plan"
test -x "$MIMIR_PROBE"
: > r3_15a_mimir_spawn.log
while IFS= read -r rel; do
  "$MIMIR_PROBE" "$ROOT/$rel" >> r3_15a_mimir_spawn.log 2>&1
done < r3_15a_paths.txt
test "$(grep -c '^R3_15A_MIMIR_PLAN=PASS$' r3_15a_mimir_spawn.log)" -eq 47
printf 'R3_15A_MIMIR_PLAN_SUCCESS=47\n'

echo 'Aggregating full NewActor evidence stream'
python tools/_tmp_evidence_next.py aggregate "$ROOT" .tmp/r3_14a/r3_14a_first_actor_envelope.jsonl r3_15a_boxcars.log r3_15a_mimir_spawn.log | tee r3_15a_aggregate_driver.log
grep -q '^R3_15A_AGGREGATE=PASS$' r3_15a_aggregate_driver.log
sha256sum tools/_tmp_evidence_next.py > r3_15a_driver_sha256.txt

# Evidence-only guarantee: tracked production/current-control files remain byte-identical to the admitted base.
test "$(git rev-parse "${BASE_SHA}:crates/mimir-replay/src/lib.rs")" = "$(git hash-object crates/mimir-replay/src/lib.rs)"
test "$(git rev-parse "${BASE_SHA}:Cargo.lock")" = "$(git hash-object Cargo.lock)"
test -z "$(git diff --name-only "$BASE_SHA" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md)"
printf 'R3_15A_PRODUCTION_MUTATION=0\n'
cat r3_15a_aggregate.txt
