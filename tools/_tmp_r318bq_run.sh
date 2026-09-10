#!/usr/bin/env bash
set -euo pipefail
RUN="$RUNNER_TEMP/r318bq_runner.sh"
cat tools/_tmp_r318bq_run_part_01.txt tools/_tmp_r318bq_run_part_02.txt tools/_tmp_r318bq_run_part_03.txt tools/_tmp_r318bq_run_part_04.txt tools/_tmp_r318bq_run_part_05.txt tools/_tmp_r318bq_run_part_06.txt > "$RUN"
python3 - "$RUN" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
replacements = [
    ("(AttributeTag::Boolean, Attribute::Boolean(value))", "(crate::AttributeTag::Boolean, crate::Attribute::Boolean(value))"),
    ("(AttributeTag::ActiveActor, Attribute::ActiveActor(value))", "(crate::AttributeTag::ActiveActor, crate::Attribute::ActiveActor(value))"),
]
for old, new in replacements:
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"R3.18BQ Boxcars qualification anchor mismatch for {old!r}: {count}")
    s = s.replace(old, new, 1)
lines = s.splitlines(keepends=True)
targets = [i for i, line in enumerate(lines) if '"R3_18BQ_ORACLE' in line]
if len(targets) != 2:
    raise SystemExit(f"R3.18BQ oracle emitter line count mismatch: {len(targets)}")
replaced = 0
for i in targets:
    count = lines[i].count(r'\\t')
    if count != 13:
        raise SystemExit(f"R3.18BQ oracle separator count mismatch line={i+1}: {count}")
    lines[i] = lines[i].replace(r'\\t', r'\t')
    replaced += count
s = ''.join(lines)
if replaced != 26:
    raise SystemExit(f"R3.18BQ oracle separator replacement mismatch: {replaced}")
p.write_text(s, encoding="utf-8", newline="\n")
print("R3_18BQ_BOXCARS_ENUM_QUALIFICATION=PASS")
print("R3_18BQ_ORACLE_SEPARATORS=PASS lines=2 separators=26")
PY
chmod +x "$RUN"
bash -n "$RUN"
exec bash "$RUN"
