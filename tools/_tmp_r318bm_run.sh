#!/usr/bin/env bash
set -euo pipefail

BASE_RUNNER_BLOB=8dd483c9fc775a7060432a4dbaf82526299952a0
PATCHED_RUNNER="$RUNNER_TEMP/r318bm_base_runner.sh"

git cat-file blob "$BASE_RUNNER_BLOB" > "$PATCHED_RUNNER"
test "$(git hash-object "$PATCHED_RUNNER")" = "$BASE_RUNNER_BLOB"

python3 - "$PATCHED_RUNNER" <<'PY'
from pathlib import Path
import sys

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
anchor = """lines.insert(i + 1, inject)
p.write_text(''.join(lines), encoding='utf-8', newline='\\n')
"""
replacement = """lines.insert(i + 1, inject)
privacy_targets = [
    j for j, line in enumerate(lines)
    if 'grep -RniE' in line and '\"$OUT\"' in line and '/home/runner' in line
]
if len(privacy_targets) != 1:
    raise SystemExit(f'expected exactly one R3.18BM privacy-scan anchor, got {len(privacy_targets)}')
normalizer_line = 'python3 \"$GITHUB_WORKSPACE/tools/_tmp_r318bm_path_normalize.py\" \"$OUT\"\\n'
lines.insert(privacy_targets[0], normalizer_line)
p.write_text(''.join(lines), encoding='utf-8', newline='\\n')
"""
if s.count(anchor) != 1:
    raise SystemExit(f"expected exactly one outer runner write anchor, got {s.count(anchor)}")
s = s.replace(anchor, replacement, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("R3_18BM_PATH_NORMALIZER_PATCH=PASS")
PY

bash -n "$PATCHED_RUNNER"
exec bash "$PATCHED_RUNNER"
