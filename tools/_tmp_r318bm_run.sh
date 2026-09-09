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
anchor = 'cp "$DIR/r318bm_boxcars_patch.py" "$RUNNER_TEMP/r318bm_boxcars_patch.py"\n'
patch = r"""python3 - "$DIR/_tmp_r318bm_inner.sh" <<'PYBMPATHPATCH'
from pathlib import Path
import sys

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
lines = s.splitlines(keepends=True)
targets = [
    i for i, line in enumerate(lines)
    if 'grep -RniE' in line and '"$OUT"' in line and '/home/runner' in line
]
if len(targets) != 1:
    raise SystemExit(f"expected exactly one R3.18BM privacy-scan anchor, got {len(targets)}")
normalizer = r'''python3 - "$OUT" <<'PYBMPATH'
from pathlib import Path
import os
import sys

root = Path(sys.argv[1])
mappings = [
    (os.environ.get("GITHUB_WORKSPACE"), "<workspace>"),
    (os.environ.get("RUNNER_TEMP"), "<runner-temp>"),
]
mappings = [(value, tag) for value, tag in mappings if value]
mappings.sort(key=lambda item: len(item[0]), reverse=True)

files_changed = 0
replacements = 0
for path in sorted(p for p in root.rglob("*") if p.is_file()):
    try:
        original = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    text = original
    local = 0
    for value, tag in mappings:
        count = text.count(value)
        if count:
            text = text.replace(value, tag)
            local += count
    if text != original:
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        files_changed += 1
        replacements += local

if replacements == 0:
    raise SystemExit("R3.18BM expected at least one ephemeral runner path to normalize")
print(f"R3_18BM_PATH_NORMALIZATION=PASS files={files_changed} replacements={replacements}")
PYBMPATH
'''
lines.insert(targets[0], normalizer)
p.write_text("".join(lines), encoding="utf-8", newline="\n")
print("R3_18BM_PATH_NORMALIZER_PATCH=PASS")
PYBMPATHPATCH
"""
if s.count(anchor) != 1:
    raise SystemExit(f"expected exactly one runner pre-execution anchor, got {s.count(anchor)}")
s = s.replace(anchor, patch + anchor, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("R3_18BM_INLINE_PATH_NORMALIZER_PATCH=PASS")
PY

bash -n "$PATCHED_RUNNER"
exec bash "$PATCHED_RUNNER"
