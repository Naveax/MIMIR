from __future__ import annotations

import os
from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: r318bm_path_normalize.py <evidence-out>")

    root = Path(sys.argv[1])
    if not root.is_dir():
        raise SystemExit(f"R3.18BM evidence output directory missing: {root}")

    mappings = [
        (os.environ.get("RUNNER_TEMP"), "<runner-temp>"),
        (os.environ.get("GITHUB_WORKSPACE"), "<workspace>"),
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
        local_replacements = 0
        for value, tag in mappings:
            count = text.count(value)
            if count:
                text = text.replace(value, tag)
                local_replacements += count

        if text != original:
            with path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
            files_changed += 1
            replacements += local_replacements

    if replacements == 0:
        raise SystemExit("R3.18BM expected at least one ephemeral runner path to normalize")

    print(
        "R3_18BM_PATH_NORMALIZATION=PASS "
        f"files={files_changed} replacements={replacements}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
