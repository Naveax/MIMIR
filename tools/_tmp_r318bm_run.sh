#!/usr/bin/env bash
set -euo pipefail
export CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback
echo R3_18BM_CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback
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
python3 - "$DIR/_tmp_r318bm_inner.sh" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text(encoding='utf-8')
old = '--test r3_18bm_probe_tmp -- --nocapture'
new = '--test r3_18bm_probe_tmp r3_18bm_exact_bl_lane_observes_one_header_on_two_true_rows_only -- --nocapture'
if s.count(old) != 1:
    raise SystemExit(f'expected exactly one BM probe command, got {s.count(old)}')
p.write_text(s.replace(old, new, 1), encoding='utf-8', newline='\n')
print('R3_18BM_FOCUSED_PROBE_PATCH=PASS')
PY
cp "$DIR/r318bm_boxcars_patch.py" "$RUNNER_TEMP/r318bm_boxcars_patch.py"
python3 - "$RUNNER_TEMP/r318bm_boxcars_patch.py" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text(encoding='utf-8')
marker = '\nif __name__ == "__main__":\n'
if s.count(marker) != 1:
    raise SystemExit(f'expected exactly one Boxcars patch main guard, got {s.count(marker)}')
shim = r'''

# R3.18BM reproducibility shim: remove benchmark-only dev-dependencies from
# the ephemeral pinned-Boxcars checkout before the injected oracle unit test.
# Parser source authority remains pinned and separately blob-verified.
def _r318bm_strip_benchmark_only_dev_dependencies() -> None:
    cargo = Path("Cargo.toml")
    if not cargo.is_file():
        raise SystemExit("R3.18BM Boxcars Cargo.toml missing at oracle patch boundary")
    text = cargo.read_text(encoding="utf-8")
    if 'name = "boxcars"' not in text:
        raise SystemExit("R3.18BM Boxcars Cargo.toml identity mismatch")
    required = ['criterion = "0.8"\n', 'gungraun = "0.19.0"\n']
    for line in required:
        if text.count(line) != 1:
            raise SystemExit(f"R3.18BM Boxcars dev-dependency authority mismatch for {line.strip()!r}")
    for line in required:
        text = text.replace(line, "", 1)
    cargo.write_text(text, encoding="utf-8", newline="\n")
    print("R3_18BM_BOXCARS_BENCH_DEVDEPS_STRIPPED=PASS criterion=0.8 gungraun=0.19.0")

_r318bm_strip_benchmark_only_dev_dependencies()
'''
s = s.replace(marker, shim + marker, 1)
p.write_text(s, encoding='utf-8', newline='\n')
print('R3_18BM_BOXCARS_REPRO_PATCH=PASS')
PY
chmod +x "$DIR/_tmp_r318bm_inner.sh"
bash -n "$DIR/_tmp_r318bm_inner.sh"
python3 -m py_compile "$RUNNER_TEMP/r318bm_boxcars_patch.py"
echo R3_18BM_BOOTSTRAP=PASS
exec "$DIR/_tmp_r318bm_inner.sh"
