from pathlib import Path

replacements = {
    "d811879bb647de5e5bb56930244b9fddaa4ec583": "28d213f831c8968e6756a6ccea2cd7aa6cdbdfba",
    "2e7cc89699c2754a4ac66eb091d6422700715a23": "da545a7144fefabab7f5be4f07fde71311065293",
    "bbad0b405f4f27af309c3b71f2f3ba0a4da60c7b": "4d1434cc0e59a6e5c72a8404c102a87d71b8b223",
}

paths = [
    Path("MIMIR_CONTINUE_HERE.md"),
    Path("MIMIR_KNOWLEDGE_GRAPH.md"),
    Path("docs/continuity/MIMIR_CONTINUITY_STATE.json"),
    Path("docs/continuity/MIMIR_CURRENT_STATE.md"),
    Path("docs/continuity/MIMIR_R3_17K_DECISION.md"),
    Path("docs/continuity/MIMIR_R3_17L_EXECUTION_SPEC.md"),
]

counts = {old: 0 for old in replacements}
for path in paths:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        n = text.count(old)
        counts[old] += n
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8", newline="\n")

for old, count in counts.items():
    if count == 0:
        raise SystemExit(f"stale blob receipt not found for correction: {old}")

print("R3.17K blob receipts corrected from canonical production readback")
for old, new in replacements.items():
    print(f"{old} -> {new} ({counts[old]} replacements)")
