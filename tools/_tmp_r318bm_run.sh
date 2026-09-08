#!/usr/bin/env bash
set -euo pipefail
B64="$RUNNER_TEMP/r318bm_payload.b64"
TGZ="$RUNNER_TEMP/r318bm_payload.tar.gz"
DIR="$RUNNER_TEMP/r318bm_payload"
: > "$B64"
cat tools/_tmp_r318bm_payload_01.txt tools/_tmp_r318bm_payload_02.txt | tr -d '\r\n' >> "$B64"
REMOTE_P03=(
  7dcce95e3cc48d405cebbe285ab53ecca26379a6
  2128cdaf3a547ca296c87bf162fc816b5401cf18
  1b81fd7cc9f95d139990b8984cfbd6bc0d384a85
  1cf528dc9fbf9c4ba0679d3d471b55a829e212fc
)
for sha in "${REMOTE_P03[@]}"; do
  json="$(gh api "repos/${GITHUB_REPOSITORY}/git/blobs/${sha}")"
  test "$(jq -r .sha <<<"$json")" = "$sha"
  test "$(jq -r .encoding <<<"$json")" = base64
  printf '%s' "$(jq -r .content <<<"$json" | tr -d '\n')" | base64 -d >> "$B64"
done
cat tools/_tmp_r318bm_payload_04.txt tools/_tmp_r318bm_payload_05.txt | tr -d '\r\n' >> "$B64"
test "$(wc -c < "$B64")" -eq 12484
test "$(sha256sum "$B64" | awk '{print $1}')" = 09fb68091fee4d67e925a9e5c5dc9fdaee280692f16b581422d24eead9dafbc5
base64 -d "$B64" > "$TGZ"
test "$(sha256sum "$TGZ" | awk '{print $1}')" = d30d8660428d072d3caebe30954f1c44766d2546758df889ed142f2acfa31c78
rm -rf "$DIR"
mkdir -p "$DIR"
tar -xzf "$TGZ" -C "$DIR"
test "$(sha256sum "$DIR/_tmp_r318bm_inner.sh" | awk '{print $1}')" = 427e863fc6e7aa96f72382ceddb1f8b34b9fe07bf57d21a6c121027925c2dde9
test "$(sha256sum "$DIR/r318bm_boxcars_patch.py" | awk '{print $1}')" = 0426dd8091fe6d3648dcdb5ae854d66c56c76a32db3421afeed40bd9c672f3ce
cp "$DIR/r318bm_boxcars_patch.py" "$RUNNER_TEMP/r318bm_boxcars_patch.py"
chmod +x "$DIR/_tmp_r318bm_inner.sh"
bash -n "$DIR/_tmp_r318bm_inner.sh"
python3 -m py_compile "$RUNNER_TEMP/r318bm_boxcars_patch.py"
echo R3_18BM_BOOTSTRAP=PASS
exec "$DIR/_tmp_r318bm_inner.sh"
