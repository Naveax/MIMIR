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
needle = 'set -euo pipefail\n'
trap = r'''trap 'rc=$?; printf "R3_18BM_ERR line=%s rc=%s cmd=%q\n" "$LINENO" "$rc" "$BASH_COMMAND" >&2' ERR
'''
if s.count(needle) != 1:
    raise SystemExit(f'expected exactly one strict-mode anchor, got {s.count(needle)}')
s = s.replace(needle, needle + trap, 1)
old = '--test r3_18bm_probe_tmp -- --nocapture'
new = '--test r3_18bm_probe_tmp r3_18bm_exact_bl_lane_observes_one_header_on_two_true_rows_only -- --nocapture'
if s.count(old) != 1:
    raise SystemExit(f'expected exactly one BM probe command, got {s.count(old)}')
s = s.replace(old, new, 1)
lines = s.splitlines(keepends=True)
targets = [
    i for i, line in enumerate(lines)
    if 'r318bm_boxcars_patch.py' in line and line.lstrip().startswith('python3 ')
]
if len(targets) != 1:
    raise SystemExit(f'expected exactly one Boxcars patch invocation, got {len(targets)}')
i = targets[0]
if lines[i].rstrip().endswith('\\'):
    raise SystemExit('Boxcars patch invocation unexpectedly spans multiple shell lines')
inject = r'''python3 - "$BOXCARS_SHA" "$RUNNER_TEMP/r318bm_boxcars_repro_receipt.txt" <<'PYBMDEP'
from pathlib import Path
import os
import subprocess
import sys
expected_sha = sys.argv[1]
receipt = Path(sys.argv[2])
roots = [Path(os.environ['RUNNER_TEMP']), Path(os.environ['GITHUB_WORKSPACE']), Path('/tmp')]
seen = set()
candidates = []
for root in roots:
    if not root.exists():
        continue
    for cargo in root.rglob('Cargo.toml'):
        try:
            resolved = cargo.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        try:
            text = cargo.read_text(encoding='utf-8')
        except (OSError, UnicodeError):
            continue
        if 'name = "boxcars"' not in text:
            continue
        proc = subprocess.run(
            ['git', '-C', str(cargo.parent), 'rev-parse', 'HEAD'],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip() == expected_sha:
            candidates.append(cargo)
if len(candidates) != 1:
    raise SystemExit(f'R3.18BM expected exactly one exact-SHA Boxcars Cargo.toml, got {len(candidates)}: {[str(x) for x in candidates]}')
cargo = candidates[0]
text = cargo.read_text(encoding='utf-8')
required = ['criterion = "0.8"\n', 'gungraun = "0.19.0"\n']
counts = [text.count(line) for line in required]
if counts != [1, 1]:
    raise SystemExit(f'R3.18BM Boxcars benchmark dev-dependency authority mismatch counts={counts}')
for line in required:
    text = text.replace(line, '', 1)
cargo.write_text(text, encoding='utf-8', newline='\n')
post = cargo.read_text(encoding='utf-8')
if any(line in post for line in required):
    raise SystemExit('R3.18BM Boxcars benchmark dev-dependency strip did not persist')
receipt.write_text(
    f'boxcars_sha={expected_sha}\ncargo_toml={cargo}\ncriterion_removed=0.8\ngungraun_removed=0.19.0\n',
    encoding='utf-8',
    newline='\n',
)
print(f'R3_18BM_BOXCARS_BENCH_DEVDEPS_STRIPPED=PASS sha={expected_sha} criterion=0.8 gungraun=0.19.0')
PYBMDEP
'''
lines.insert(i + 1, inject)
p.write_text(''.join(lines), encoding='utf-8', newline='\n')
print('R3_18BM_FOCUSED_PROBE_PATCH=PASS')
print('R3_18BM_DIRECT_BOXCARS_REPRO_PATCH=PASS')
print('R3_18BM_ERR_TRAP_PATCH=PASS')
PY
cp "$DIR/r318bm_boxcars_patch.py" "$RUNNER_TEMP/r318bm_boxcars_patch.py"
chmod +x "$DIR/_tmp_r318bm_inner.sh"
bash -n "$DIR/_tmp_r318bm_inner.sh"
python3 -m py_compile "$RUNNER_TEMP/r318bm_boxcars_patch.py"
echo R3_18BM_BOOTSTRAP=PASS

LOG="$RUNNER_TEMP/r318bm_execute.log"
set +e
bash "$DIR/_tmp_r318bm_inner.sh" >"$LOG" 2>&1
rc=$?
set -e
cat "$LOG"
if [ "$rc" -ne 0 ]; then
  stage=inner_before_boxcars_strip
  grep -Fq 'R3_18BM_BOXCARS_BENCH_DEVDEPS_STRIPPED=PASS' "$LOG" && stage=inner_after_boxcars_strip
  kind=unknown
  grep -Eqi 'requires rustc|rustc .* is not supported' "$LOG" && kind=msrv
  grep -Eqi 'failed to select a version|failed to resolve|dependency.*conflict' "$LOG" && kind=resolver
  grep -Fqi 'expected exactly one exact-SHA Boxcars Cargo.toml' "$LOG" && kind=boxcars_checkout_discovery
  grep -Fqi 'benchmark dev-dependency authority mismatch' "$LOG" && kind=boxcars_devdep_authority
  grep -Eqi 'native[^[:alnum:]]+oracle|oracle[^[:alnum:]]+mismatch|R3_18BM_NATIVE_ORACLE_MISMATCH=[1-9]' "$LOG" && kind=oracle_mismatch
  grep -Eqi 'No such file or directory|not found' "$LOG" && kind=missing_file
  if grep -Fqi 'privacy scan failed' "$LOG"; then
    kind=privacy_scan
    privacy_diag_file="$RUNNER_TEMP/r318bm-privacy-hits.txt"
    python3 - "$LOG" "$privacy_diag_file" <<'PYPRIV'
import os
from pathlib import PurePosixPath
import re
import sys
src, dst = sys.argv[1:]
lines = open(src, errors='replace').read().splitlines()
failures = [i for i, line in enumerate(lines) if 'privacy scan failed' in line.lower()]
stop = failures[-1] if failures else len(lines)
patterns = [
    ('runner_path', re.compile(r'/home/runner', re.I)),
    ('windows_user_path', re.compile(r'C:\\Users\\', re.I)),
    ('github_pat', re.compile(r'github_pat_', re.I)),
    ('ghp', re.compile(r'ghp_', re.I)),
    ('username', re.compile(r'Omersevik|Maximillan', re.I)),
]
found = []
seen = set()
for raw in reversed(lines[:stop]):
    categories = tuple(name for name, rx in patterns if rx.search(raw))
    if not categories:
        continue
    match = re.match(r'^(.*?):(\d+):(.*)$', raw)
    if match:
        source, lineno = match.group(1), match.group(2)
        source = source.replace('\\', '/')
        parts = [p for p in PurePosixPath(source).parts if p not in ('/', '')]
        safe_file = '/'.join(parts[-2:]) if parts else '<unknown>'
        safe_file = re.sub(r'Omersevik|Maximillan', '<redacted>', safe_file, flags=re.I)
        safe_file = re.sub(r'github_pat_|ghp_', '<credential-prefix>', safe_file, flags=re.I)
    else:
        safe_file, lineno = '<unparsed>', '?'
    marker = f"R3_18BM_PRIVACY_HIT file={safe_file} line={lineno} category={'+'.join(categories)}"
    if marker not in seen:
        seen.add(marker)
        found.append(marker)
    if len(found) >= 4:
        break
if not found:
    found.append('R3_18BM_PRIVACY_HIT file=<unknown> line=? category=unclassified')
with open(dst, 'w', encoding='utf-8', newline='\n') as f:
    for marker in found:
        f.write(marker + '\n')
PYPRIV
    cat "$privacy_diag_file" >> "$LOG"
  fi
  sig="$(sha256sum "$LOG" | awk '{print substr($1,1,12)}')"
  diag_file="$RUNNER_TEMP/r318bm-diag-tail.txt"
  python3 - "$LOG" "$diag_file" <<'PYDIAG'
import os, re, sys
src, dst = sys.argv[1:]
lines = open(src, errors="replace").read().splitlines()
pat = re.compile(r'R3_18BM_PRIVACY_HIT|R3_18BM_ERR|error:|FAILED|panicked|assert|mismatch|Traceback|Caused by|oracle|expected|thread .* panicked', re.I)
chosen = []
def add(s):
    s = s.strip()
    if not s:
        return
    for val, tag in ((os.environ.get("RUNNER_TEMP"), "<tmp>"), (os.environ.get("GITHUB_WORKSPACE"), "<workspace>")):
        if val:
            s = s.replace(val, tag)
    s = re.sub(r'https?://\S+', '<url>', s)
    s = re.sub(r'/(?:home/runner|tmp)/\S+', '<path>', s)
    s = re.sub(r'\b[A-Za-z0-9_+=./-]{32,}\b', '<id>', s)
    s = ' '.join(s.split())[:88]
    if s and s not in chosen:
        chosen.append(s)
for s in reversed(lines):
    if pat.search(s):
        add(s)
        if len(chosen) >= 4:
            break
for s in reversed(lines):
    if len(chosen) >= 4:
        break
    add(s)
with open(dst, 'w', encoding='utf-8', newline='\n') as f:
    for s in chosen[:4]:
        f.write(s + '\n')
PYDIAG
  if [[ -n "${GH_TOKEN:-}" && -n "${GITHUB_REPOSITORY:-}" && -n "${GITHUB_SHA:-}" ]]; then
    i=0
    while IFS= read -r line && (( i < 4 )); do
      [[ -n "$line" ]] || continue
      i=$((i + 1))
      line_sig="$(printf '%s' "$line" | sha256sum | awk '{print substr($1,1,10)}')"
      gh api --method POST "repos/${GITHUB_REPOSITORY}/statuses/${GITHUB_SHA}" \
        -f state=failure -f context="r318bm/diag-tail-${i}" \
        -f description="line=${line};sig=${line_sig}" \
        -f target_url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}" >/dev/null || true
    done < "$diag_file"
  fi
  gh api --method POST "repos/${GITHUB_REPOSITORY}/statuses/${GITHUB_SHA}" \
    -f state=failure -f context='r318bm/diagnostic' \
    -f description="stage=${stage};kind=${kind};rc=${rc};sig=${sig}" \
    -f target_url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}" >/dev/null
  gh api --method POST "repos/${GITHUB_REPOSITORY}/statuses/${GITHUB_SHA}" \
    -f state=failure -f context='r318bm/evidence' \
    -f description='R3.18BM evidence failed; inspect diagnostic statuses' \
    -f target_url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}" >/dev/null
  printf 'R3_18BM_DIAGNOSTIC stage=%s kind=%s rc=%s sig=%s\n' "$stage" "$kind" "$rc" "$sig"
  exit "$rc"
fi

gh api --method POST "repos/${GITHUB_REPOSITORY}/statuses/${GITHUB_SHA}" \
  -f state=success -f context='r318bm/diagnostic' \
  -f description='inner deterministic evidence completed' \
  -f target_url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}" >/dev/null
echo R3_18BM_DIAGNOSTIC=PASS
