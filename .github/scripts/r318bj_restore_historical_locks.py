from pathlib import Path

p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
s = p.read_text(encoding="utf-8")

repairs = [
    (
        '    "following-header success on any R3.18AQ false terminator",\n    "second later property control bit after R3.18AU",',
        '    "following-header success on any R3.18AQ false terminator",\n    "production composition of the following payload after R3.18AU before a later production pass",\n    "second later property control bit after R3.18AU",',
    ),
    (
        '    "second payload or following header after R3.18BG",\n    "historical R3.18AW/R3.18AM/R3.18AN payload coordinate/value inheritance at R3.18BG",',
        '    "second payload or following header after R3.18BG",\n    "production composition of the R3.18BG-observed payload before a later production pass",\n    "historical R3.18AW/R3.18AM/R3.18AN payload coordinate/value inheritance at R3.18BG",',
    ),
]

for old, new in repairs:
    if s.count(old) != 1:
        raise SystemExit(f"expected one historical-lock insertion point, got {s.count(old)}")
    s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8", newline="\n")
print("R3_18BJ_HISTORICAL_LOCK_REPAIR=PASS")
